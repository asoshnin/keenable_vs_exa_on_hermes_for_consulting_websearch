# Search-Backend Benchmark

A task-specific, **blind, multi-judge** harness for comparing two web-search backends on
research work that consultancies actually do — market sizing, M&A/valuation, finance
benchmarks, technical due diligence, regulatory tracking, and multi-hop deep research.

It does not use a public leaderboard. It defines its own query set, its own rubric, and then
scores the same anonymised evidence with **more than one independent scoring method**, each
seeing both candidates and then again with them swapped — so a position artefact cannot
masquerade as a finding.

The harness produced the accompanying report — `paper/REPORT.md` and `paper/report.pdf` —
comparing **Keenable.ai** against **Exa**: 30 queries captured across six categories, of which
**10 pairs** were scored blind by two independent scoring methods in both presentation orders.

[![One-slide summary: Keenable.ai leads Exa on analytical depth (+0.31 of 2) and source authority; freshness shows no clear difference. The consulting lead is consistent in direction but its confidence interval includes zero; deep research is contested. Ten blind-scored pairs drawn from 30 captured queries.](assets/slide.png?v=5efb1794)](paper/report.pdf)

*One-slide summary — click for the [full report](paper/report.pdf), or open the
[full-size PNG](assets/slide.png) (3200×1800).*

> **Regenerating the slide:** `make slide` re-renders `assets/slide.png` from `assets/slide.html`
> and **automatically re-stamps the `?v=` hash in the image URL above**. That stamp matters:
> GitHub serves README images through its Camo CDN, which caches by URL, so without it an
> unchanged filename keeps showing the previous render no matter how often you refresh.

---

## The finding, in one paragraph

Keenable.ai wins, but not for the reason usually claimed. Across **10 blind-scored pairs** (from
30 captured queries) its advantage concentrates in **analytical depth** (+0.31 of 2, the largest
of six criteria) and **source authority** (+0.23). On **recency and freshness** — the criterion
everyone expects a challenger to compete on — it is ahead by only **+0.042**: below the
pre-declared 0.10 clear-win floor, and level with relevance precision. That is **no clear
difference, and specifically not a deficit** — it never trails in aggregate, though it does lose
one query (SaaS comps) and draw another. No test was run at the criterion level; the "no clear
difference" call is the pre-declared floor, not a significance test.

The lead is consistent in **direction** on consulting-style research — clear wins on **3 of 5**
pairs on the scorecard and **5 of 5** on the frontier judge — but the scorecard's 95% interval,
**−0.04 to +0.43, includes zero**, so the *size* of the consulting lead is not established. Deep
research is **contested**: one clear win, one pair leaning Exa, three below the floor.

---

## Why the method is built this way

Most "search engine X is better" claims fail on one of four things. Each is addressed here.

| Failure | What this harness does |
|---|---|
| **Unverifiable inputs.** The comparison silently ran against a fallback engine. | Every capture records `served_by`, `keyless` and the HTTP status. A failed call raises; it never becomes another engine's data. |
| **One judge = one narrative.** | More than one scoring method — an MCDA decision plane and a frontier LLM, on top of a single-judge body pass. Their disagreements are reported as findings. |
| **Position bias.** The judge prefers whichever candidate it reads second. | Every pair is judged in **both** presentation orders. Winner flips and score drift are reported per query. |
| **Category aggregate hides a loss.** "Both 4.2 — tie." | Queries are scored individually and only then grouped. The harness flags `mixed` winners inside a category. |

---

## License

**MIT, for the whole repository** — the harness, the report (`paper/REPORT.md`) and the
rendered PDF alike. One license, no split, no attribution beyond keeping the copyright
notice. Use it, fork it, re-run it against your own engines, quote it, sell services built on
it.

## Where this came from

The benchmark was originally run from **Hermes Agent** (a Nous Research desktop agent) using
its built-in search tool, and the repo name reflects that provenance. The harness here
deliberately depends on **none** of it: `requests` and a Python interpreter are the whole
requirement, so results can be reproduced and audited without installing Hermes. Only the
*judge* is model-agnostic — point `JUDGE_BASE_URL` at any OpenAI-compatible endpoint.

## Quick start

```bash
git clone <this repo> && cd keenable_vs_exa_on_hermes_for_consulting_websearch
cp .env.example .env          # add your keys — .env is gitignored
make install
make test                     # 11 offline tests, no network, no keys
make all                      # capture -> cards -> judge -> aggregate
make report                   # HTML + PDF      (needs Chrome or Chromium)
make slide                    # the one-slide summary PNG (same requirement)
```

`make capture` works with **no Keenable key at all** — the challenger has a documented
anonymous tier. Only the incumbent (`EXA_API_KEY`) and the judge (`JUDGE_*`) require
credentials. If a credential is missing the harness **aborts and names the variable**
rather than substituting another engine.

You need:

| Credential | Required? | Where |
|---|---|---|
| `KEENABLE_API_KEY` | **No** — the challenger has an anonymous free tier | https://app.keenable.ai/signup (free: 100k req/month) |
| `EXA_API_KEY` | **Yes**, for the default incumbent | https://dashboard.exa.ai |
| `JUDGE_MODEL` + `JUDGE_API_KEY` | **Yes**, any OpenAI-compatible endpoint | OpenAI, Azure/Foundry, OpenRouter, vLLM, Ollama… |

**No API keys live in this repository.** `.env` and generated artefacts are gitignored;
`.env.example` documents the variables with empty values.

### Using a different incumbent

The harness is not tied to Exa. Implement a function returning a `Result` in
`src/bench/providers.py` and register it in `BACKENDS`:

```python
def search_brave(query, limit=10, api_key=None) -> Result:
    ...
    return Result(engine="brave", query=query, limit=limit, hits=hits,
                  served_by="brave", keyless=False)
BACKENDS["brave"] = search_brave
```

Then set `INCUMBENT = "brave"` in `src/bench/cli.py`. Nothing else changes.

---

## What it costs to re-run

| Stage | Calls | Notes |
|---|---|---|
| Capture | 60 | 30 queries × 2 engines, 1 request each |
| Judge, all 30 pairs | 60 | 30 pairs × 2 presentation orders |
| Judge, **as published** | 20 | 10 pairs were scored, × 2 presentation orders |
| **Total as published** | **80 requests** | |

Wall-clock: ~10 min for judging on a hosted frontier model at ~15 s/call, plus rate-limit
delays on capture. Server-side cost is your judge model's per-call price — with a
mid-tier model this run is typically well under a few dollars.

---

## Repository layout

```
config/
  queries.yaml          the 30 queries, grouped by category (edit this to test your own domain)
  rubric.yaml           6 dimensions, ordinal 0..2 anchors, fixed weights
  report_template.html  print-ready shell with a __BODY__ placeholder
src/bench/
  providers.py          direct HTTP clients (Keenable, Exa) + Result/Hit types
  cards.py              anonymised evidence cards with a pre-computed facts block
  judge.py              OpenAI-compatible judge, both presentation orders
  aggregate.py          per-query summary, agreement, stability
  render.py             Markdown -> HTML -> PDF (Chrome/Edge, else WeasyPrint)
  cli.py                capture | cards | judge | aggregate | render | all
assets/
  slide.html            source of the one-slide summary
  slide.png             render of that slide (regenerate: make slide)
paper/                  the published report: REPORT.md + report.pdf
data/                   raw captures, cards, verdicts  (gitignored)
out/                    summary.json, results_table.md, report.html, report.pdf
tests/                  offline tests — no network, no keys
```

Every stage is **resumable**: existing artefacts are reused unless you pass `--force`.

---

## Reading the output honestly

The composite is a **weighted mean over ordinal 0–2 anchors**. It is a ranking device,
not a measurement on an interval scale. Consequently:

- Differences below ≈0.1 on the 0–2 scale are not meaningful at n=10 pairs.
- Report the **direction** and the **winner count**; treat the margin as indicative.
- Do **not** compute ratios of composites, or compare composites across different rubrics.
- A category mean is not a finding. Read the per-query rows: the harness prints `mixed`
  when a category contains winners from both engines.

`out/summary.json` carries, per query: both engines' composites, the delta, which engine
led, the declared winner in each order, whether it was stable, and the score drift.

---

## Known limitations

- **Judge families correlate.** The report's layers share a rubric and are not fully
  independent instruments: the body judge read raw results, the two appendix judges read the
  same summarised evidence cards. Agreement is reported as agreement, not as validation.
- **The evidence cards are summaries.** They carry every returned domain, title and a
  truncated snippet plus a machine-counted facts block. A judge that scores "depth" from
  a card is scoring the card's fidelity as well as the engine's.
- **Published results are one snapshot.** Search indices move; re-running will produce
  different result sets. Run IDs and dates are recorded in `data/capture_manifest.json`.
- **Rate limits and cost** are yours to manage; the harness only inserts a fixed delay.
- **Terms of service.** You are responsible for whether you may redistribute third-party
  search results. The repo ships no captured results — only code.

---

## Licence

MIT. See `LICENSE`.