"""Aggregate judge output into the numbers the report quotes.

Two rules this module enforces, because both were violated in an earlier draft:

1. Never score a CATEGORY in aggregate. Per-query results are computed first and
   only then grouped — an aggregate can hide a clear win and a clear loss.
2. Report winner stability and score stability separately. A judge can pick the
   same winner twice while its scores move 0.25 on a 0-2 scale.
"""
from __future__ import annotations

import statistics
from typing import Any


def summarise(judged: dict[str, dict], dims: list[dict]) -> dict[str, Any]:
    """judged: {query_id: judge_pair() output} -> full summary."""
    keys = [d["key"] for d in dims]
    qids = list(judged)

    rows = []
    for q in qids:
        j = judged[q]
        ab, ba = j["orders"]["AB"], j["orders"]["BA"]
        engs = list(j["mean_composite"])
        hi, lo = max(engs, key=lambda e: j["mean_composite"][e]), min(
            engs, key=lambda e: j["mean_composite"][e])
        rows.append({
            "query": q,
            "composite": {e: round(j["mean_composite"][e], 3) for e in engs},
            "delta": round(j["mean_composite"][hi] - j["mean_composite"][lo], 3),
            "leader": hi,
            "declared_ab": ab["declared_winner_engine"],
            "declared_ba": ba["declared_winner_engine"],
            "winner_stable": j["winner_stable"],
            "drift": {e: round(v, 3) for e, v in j["score_drift"].items()},
            "scores": {e: {k: (ab["scores"][e][k] + ba["scores"][e][k]) / 2 for k in keys}
                       for e in engs},
        })

    engs = list(rows[0]["composite"]) if rows else []
    per_dim = {k: {e: round(statistics.mean(r["scores"][e][k] for r in rows), 3)
                   for e in engs} for k in keys}

    counts = {e: sum(1 for r in rows if r["leader"] == e) for e in engs}
    stable = sum(1 for r in rows if r["winner_stable"])

    return {
        "n": len(rows),
        "rows": rows,
        "per_dimension": per_dim,
        "leader_counts": counts,
        "winner_stable": stable,
        "mean_drift": {e: round(statistics.mean(r["drift"][e] for r in rows), 3)
                       for e in engs} if rows else {},
        "max_drift": {e: round(max(r["drift"][e] for r in rows), 3) for e in engs} if rows else {},
        "mean_composite": {e: round(statistics.mean(r["composite"][e] for r in rows), 3)
                           for e in engs} if rows else {},
    }


def slice_by_category(summary: dict, judged_categories: dict[str, str]) -> dict[str, dict]:
    """Group rows by category WITHOUT averaging away per-query outcomes."""
    out: dict[str, list] = {}
    for r in summary["rows"]:
        out.setdefault(judged_categories[r["query"]], []).append(r)
    res = {}
    for cat, rows in out.items():
        engs = list(rows[0]["composite"])
        hi = max(engs, key=lambda e: statistics.mean(r["composite"][e] for r in rows))
        res[cat] = {
            "n": len(rows),
            "mean": {e: round(statistics.mean(r["composite"][e] for r in rows), 3) for e in engs},
            "leaders": {e: sum(1 for r in rows if r["leader"] == e) for e in engs},
            "mixed": len({r["leader"] for r in rows}) > 1,
            "margin": round(
                statistics.mean(r["composite"][hi] for r in rows)
                - statistics.mean(r["composite"][e] for e in engs if e != hi), 3),
        }
    return res


def markdown_table(summary: dict, engine_a: str, engine_b: str) -> str:
    """Per-query results table. Every number carries its n in the caption."""
    s = summary
    head = (f"| Query | {engine_a} | {engine_b} | Δ | Leader | Winner stable | "
            f"Score drift ({engine_a}/{engine_b}) |\n|---|---|---|---|---|---|---|")
    body = []
    for r in s["rows"]:
        stab = "yes" if r["winner_stable"] else "**NO**"
        body.append(
            f"| {r['query']} | {r['composite'][engine_a]:.3f} | {r['composite'][engine_b]:.3f} | "
            f"{r['delta']:+.3f} | {r['leader']} | {stab} | "
            f"{r['drift'][engine_a]:.3f} / {r['drift'][engine_b]:.3f} |"
        )
    caption = (f"\n*Table. Per-query composites on a 0–2 ordinal scale (higher is better), "
               f"n={s['n']} query pairs, each judged in both presentation orders. "
               f"'Winner stable' = same engine declared on top in both orders. "
               f"Δ is the gap between the two mean composites.*\n")
    return head + "\n" + "\n".join(body) + "\n" + caption