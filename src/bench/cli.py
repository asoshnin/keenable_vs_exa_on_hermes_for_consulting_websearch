"""Command-line interface.

    python -m bench capture      # fetch paired results, provenance-guarded
    python -m bench cards        # build blind evidence cards
    python -m bench judge        # score cards with an LLM, both orders
    python -m bench aggregate    # summarise to JSON + markdown table
    python -m bench render       # HTML + PDF
    python -m bench all          # capture -> cards -> judge -> aggregate -> render

Every stage is resumable: existing artefacts are reused unless --force is passed,
so an interrupted run costs nothing to restart.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import yaml

from . import aggregate as agg
from .cards import write_cards
from .judge import JudgeConfig, judge_pair
from .providers import BackendError, search
from .render import html_to_pdf, write_html

ROOT = Path(__file__).resolve().parents[2]
CFG = ROOT / "config"
DATA = ROOT / "data"
OUT = ROOT / "out"

CHALLENGER = "keenable"   # side A
INCUMBENT = "exa"         # side B


def _queries() -> tuple[list[dict], int]:
    spec = yaml.safe_load((CFG / "queries.yaml").read_text())
    return spec["queries"], int(spec.get("defaults", {}).get("limit", 10))


def _rubric() -> tuple[list[dict], dict]:
    spec = yaml.safe_load((CFG / "rubric.yaml").read_text())
    return spec["dimensions"], spec["scale"]


# --------------------------------------------------------------------------- #
def cmd_capture(args) -> None:
    qs, default_limit = _queries()
    raw = DATA / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    manifest, failures = [], []

    for q in qs:
        qid = q["id"]
        limit = int(q.get("limit", default_limit))
        for engine in (CHALLENGER, INCUMBENT):
            dest = raw / f"{engine}__{qid}.json"
            if dest.exists() and not args.force:
                print(f"  cached  {engine:9} {qid}")
                continue
            try:
                res = search(engine, q["query"], limit=limit)
            except BackendError as exc:
                # A failed engine must never silently become another engine's data.
                failures.append({"query": qid, "engine": engine, "error": str(exc)})
                print(f"  FAILED  {engine:9} {qid}: {exc}", file=sys.stderr)
                continue
            if not res.hits:
                failures.append({"query": qid, "engine": engine, "error": "zero results"})
                print(f"  EMPTY   {engine:9} {qid}", file=sys.stderr)
                continue
            dest.write_text(json.dumps({
                "engine": res.engine, "query": res.query, "limit": res.limit,
                "served_by": res.served_by, "keyless": res.keyless, "meta": res.meta,
                "hits": [h.__dict__ for h in res.hits],
            }, indent=2))
            print(f"  ok      {engine:9} {qid}  n={len(res.hits)}  served_by={res.served_by}")
            manifest.append({"query": qid, "engine": engine, "n": len(res.hits)})
            time.sleep(float(args.delay))

    (DATA / "capture_manifest.json").write_text(json.dumps(
        {"captured": manifest, "failures": failures}, indent=2))
    if failures:
        print(f"\n{len(failures)} failed call(s). Nothing was substituted. "
              f"See data/capture_manifest.json.", file=sys.stderr)
        raise SystemExit(2)
    print(f"\ncaptured {len(manifest)} result sets -> {raw}")


def _load_results():
    from .providers import Hit, Result

    qs, _ = _queries()
    out = {}
    for q in qs:
        sides = {}
        for side, engine in (("A", CHALLENGER), ("B", INCUMBENT)):
            p = DATA / "raw" / f"{engine}__{q['id']}.json"
            if not p.exists():
                continue
            d = json.loads(p.read_text())
            sides[side] = Result(
                engine=d["engine"], query=d["query"], limit=d["limit"],
                hits=[Hit(**h) for h in d["hits"]],
                served_by=d.get("served_by", d["engine"]),
                keyless=d.get("keyless", False), meta=d.get("meta", {}),
            )
        if len(sides) == 2:
            out[q["id"]] = sides
    return out


def cmd_cards(args) -> None:
    res = _load_results()
    if not res:
        raise SystemExit("no paired captures found — run `capture` first")
    paths = write_cards(res, DATA / "cards")
    print(f"wrote {len(paths)} evidence cards -> {DATA / 'cards'}")


def cmd_judge(args) -> None:
    dims, _ = _rubric()
    qs, _ = _queries()
    cats = {q["id"]: q["category"] for q in qs}
    res = _load_results()
    cfg = JudgeConfig.from_env()
    out_dir = DATA / "judged"
    out_dir.mkdir(parents=True, exist_ok=True)

    only = args.only.split(",") if args.only else list(res)
    for qid in only:
        if qid not in res:
            print(f"  skip {qid} (no paired captures)"); continue
        dest = out_dir / f"{qid}.json"
        if dest.exists() and not args.force:
            print(f"  cached  {qid}"); continue
        print(f"  judging {qid} ({cats.get(qid,'?')}) with {cfg.model}, both orders…")
        j = judge_pair(cfg, qs[[q['id'] for q in qs].index(qid)]["query"],
                       res[qid]["A"], res[qid]["B"], dims,
                       sides=(CHALLENGER, INCUMBENT))
        dest.write_text(json.dumps(j, indent=2))
        print(f"    -> {CHALLENGER} {j['mean_composite'][CHALLENGER]:.3f} / "
              f"{INCUMBENT} {j['mean_composite'][INCUMBENT]:.3f}  "
              f"stable={j['winner_stable']}")

    if args.only:
        return
    print(f"\njudged {len(list(out_dir.glob('*.json')))} pairs -> {out_dir}")


def cmd_aggregate(args) -> None:
    dims, _ = _rubric()
    qs, _ = _queries()
    cats = {q["id"]: q["category"] for q in qs}
    judged = {p.stem: json.loads(p.read_text()) for p in (DATA / "judged").glob("*.json")}
    if not judged:
        raise SystemExit("nothing judged yet — run `judge` first")

    summary = agg.summarise(judged, dims)
    summary["per_category"] = agg.slice_by_category(summary, cats)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))
    table = agg.markdown_table(summary, CHALLENGER, INCUMBENT)
    (OUT / "results_table.md").write_text(table)
    print(table)

    for cat, s in summary["per_category"].items():
        mixed = "  <-- MIXED winners" if s["mixed"] else ""
        print(f"{cat:22} n={s['n']} {s['mean']} margin={s['margin']:+.3f}{mixed}")


def cmd_render(args) -> None:
    if args.src:
        src = Path(args.src)
    else:
        # Prefer a locally generated report, fall back to the committed paper so a
        # fresh clone can render immediately without running the whole pipeline.
        for cand in (OUT / "REPORT.md", ROOT / "paper" / "REPORT.md"):
            if cand.exists():
                src = cand
                break
        else:
            src = OUT / "REPORT.md"
    if not src.exists():
        raise SystemExit(
            f"report source not found: {src}\n"
            "Generate one with `make all`, or pass --src <path.md>."
        )
    OUT.mkdir(parents=True, exist_ok=True)
    html = args.html_template
    html_text = Path(html).read_text().replace("__BODY__", _md_to_html(src.read_text()))
    hp = write_html(html_text, OUT / "report.html")
    print(f"HTML -> {hp}")
    ok, msg = html_to_pdf(hp, OUT / "report.pdf")
    print(("PDF  -> " + str(OUT / "report.pdf") + "  ") + msg if ok else msg)
    if not ok:
        raise SystemExit(3)


def _md_to_html(md: str) -> str:
    try:
        import markdown as mdlib
    except ImportError:  # pragma: no cover - fail loudly, never emit a <pre> blob
        raise SystemExit(
            "The 'markdown' package is required to render the report "
            "(headings and tables are otherwise emitted as raw text).\n"
            "  pip install -r requirements.txt"
        )
    return mdlib.markdown(md, extensions=["tables", "fenced_code", "toc", "sane_lists"])


def cmd_all(args) -> None:
    cmd_capture(args); cmd_cards(args); cmd_judge(args); cmd_aggregate(args)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(prog="bench", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("capture"); p.add_argument("--force", action="store_true")
    p.add_argument("--delay", default="1.5"); p.set_defaults(fn=cmd_capture)
    sub.add_parser("cards").set_defaults(fn=cmd_cards)
    p = sub.add_parser("judge"); p.add_argument("--force", action="store_true")
    p.add_argument("--only", default=""); p.set_defaults(fn=cmd_judge)
    sub.add_parser("aggregate").set_defaults(fn=cmd_aggregate)
    p = sub.add_parser("render"); p.add_argument("--src", default="")
    p.add_argument("--html-template", default=str(ROOT / "config" / "report_template.html"))
    p.set_defaults(fn=cmd_render)
    p = sub.add_parser("all"); p.add_argument("--force", action="store_true")
    p.add_argument("--delay", default="1.5"); p.add_argument("--only", default="")
    p.set_defaults(fn=cmd_all)

    args = ap.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()