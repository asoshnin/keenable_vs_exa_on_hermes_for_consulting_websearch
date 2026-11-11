> **Provenance: resolved.** An earlier warning that the Keenable results were unverified has
> been withdrawn. Verified by live test: keyed and keyless Keenable calls return the same
> index (DEEP-001: 10/10 identical domains; FIN-001: 4/5). The credential was briefly broken
> mid-session and has been replaced; captures were re-validated against the live key.

# Search Engine Benchmarking Report
## Keenable.ai vs Default (Exa) — Deep Web Research for Consulting

**Date:** 11 November 2026 · **Status:** v2 (post-review) · **Scope:** 30 queries in
6 categories, executed on both engines at a fixed per-query limit.

**Contents**

1. [Verdict](#verdict) — what the evidence supports, with numbers
2. [What changed from v1](#what-changed-from-v1) — findings revised or withdrawn
3. [Method](#test-methodology) — what was run vs what was scored
4. [Findings by category](#detailed-findings-by-category) — per-query evidence
5. [Appendix A](#appendix-a--decision-plane-jev--system-one-cross-check) — independent judge #2 (System One)
6. [Appendix B](#appendix-b--third-layer-frontier-llm-judge-grok-46-all-ten-pairs) — independent judge #3 (frontier LLM)

**Judge stack.** Body = one LLM judge. Appendix A = TypeSafe Jev `jev-1.13.0`
(System One, 20 calls). Appendix B = `grok-4.6` (frontier LLM, 20 calls). Each
appendix judge scored every pair twice, with the candidates swapped.

---

## Executive Summary

*Table 1. Qualitative summary from the single-LLM body judge, six exemplar queries (one per category), n=6. Units: rubric points on a 1–5 scale. Source: body judge; the independent judges in Appendices A and B revise two rows (see below).*

| Dimension | Keenable.ai | Default (exa) | Body verdict | Independent judges |
|-----------|-------------|---------------|--------------|--------------------|
| **Analytical depth / granularity** | Revenue-tier, growth-tier and deal-level breakdowns | Aggregate medians, wider ranges | **Keenable** | **Confirmed** — the only dimension both judges agree on strongly (+0.31 Jev, +0.50 grok, 0–2 scale) |
| **Source authority** ⓐ | Official regulators; M&A advisors | Official regulators; Big 4 | Tie | **Near-parity** (Jev +0.23, grok +0.05) |
| **Recency** | 2024–2026 data points | Mostly 2023–Q3 2024 | Keenable | **Contested — not a differentiator** (Jev +0.04; grok +0.60) |
| **Practical guidance** ⓑ | Compliance steps, penalty tables | Regulatory frameworks | Keenable | Not separately scored |
| **Regulator coverage** | EBA, BaFin, national supervisors | BaFin, Eurofi, EC, KPMG | Default | **Not corroborated** by blind scoring |
| **Technical benchmark depth** | Tables, latency percentiles, cost/1M | Similar | Tie | Not separately scored |

ⓐ "Advisor commentary" on the Keenable side includes both law firms (Jones Day, Linklaters, Cooley) and vendor-authored explainers (Luware, Zango.ai); this is not a like-for-like law-firm comparison.
ⓑ Vendor and consultancy guidance rather than a scored rubric dimension.

<a id="verdict"></a>
## Verdict

**Keenable leads on consulting-style research, but at n=5 per slice the lead is not
established for every query, and it is absent in deep research.**

Of the 30 queries captured, **10 pairs were scored** (one exemplar from each of the five
consulting categories, plus all five deep-research queries). A pair counts as a win only if
the gap clears the pre-declared **0.10 floor on the 0-2 scale** *and* the same engine wins in
both presentation orders. On that rule:

| Slice | Jev clear wins | grok clear wins | Mean Δ, Jev (95% CI) | Mean Δ, grok (95% CI) |
|---|---|---|---|---|
| Consulting (n=5) | **3/5** (BI-001, REG-001, IT-002) | 5/5 | +0.195 (**−0.041 to +0.430**) | +0.395 (**+0.301 to +0.489**) |
| Deep research (n=5) | **1/5** (DEEP-002) | 1/5 | +0.110 (**−0.187 to +0.407**) | +0.130 (**−0.191 to +0.451**) |

The two judges agree that Keenable leads in direction. They disagree on whether the
consulting lead is distinguishable from zero: grok's interval excludes it, **Jev's does not**.
Both intervals for deep research include zero. With n=5 and per-pair standard deviations of
0.19-0.26, **the "consulting edge is about twice the deep-research edge" claim made in v1 cannot
be supported** and is withdrawn.

What survives, and is the only finding all three judges support:

1. **Analytical resolution.** Keenable disaggregates where Exa generalises - revenue tiers,
   growth tiers, deal-level multiples, day-level effective dates with penalty schedules.
   Largest same-signed gap for both independent judges (+0.31 Jev, +0.50 grok).
2. **A modest, directionally consistent consulting lead** at 3/5 (Jev) and 5/5 (grok) clear wins.
3. **Deep research is contested:** one clear Keenable win (DEEP-002, +0.53); the incumbent's
   best case is DEEP-001, where it wins both IDPS orders but by **−0.05 on the MCDA composite**,
   i.e. **below the 0.10 clear-win floor** — so it is a directional loss for Keenable, not a
   demonstrated win for the incumbent.

What does **not** survive: the v1 recency claim (Jev +0.04, essentially none), the v1
"Deep Research is a 4.2/4.2 tie" (it concealed a win and a loss), and any reading of the margin
as a precise effect size.

**Not established by this study:** anything about cost, latency or reliability; any claim about
general web search; or generalisation past Exa. Single queries per consulting category mean the
category labels below are *exemplars*, not category-wide results.

<a id="what-changed-from-v1"></a>
### What changed from v1

| v1 claim | Status in v2 | Why |
|---|---|---|
| "Recency is the largest differentiator" (+0.8 of 5) | **Withdrawn** | Neither independent judge reproduces it (Jev +0.04) |
| "Deep Research: both 4.2/4.2 — tie" | **Replaced** | Concealed a clear win (DEEP-002) and a clear loss (DEEP-001) |
| "Body of report unchanged by Appendix A" | **Removed** | Appendix A's findings were folded back into this body |
| Keenable results "unverified / provenance unclear" | **Retracted** | Keyed and keyless Keenable calls return the same index (10/10 domains on DEEP-001) |
| Source authority "tie" | **Narrowed** | Jev +0.23, grok +0.05 — a small edge, not a tie |
| "Peer-reviewed arXiv" | **Corrected** | arXiv is a preprint server; no journal review implied |

## Test Methodology

### Query Categories (30 queries total)
| Category | Queries | Focus |
|----------|---------|-------|
| Business Intelligence | 5 | Market sizing, competitive landscapes, adoption rates |
| Strategy & M&A | 5 | Valuation multiples, deal structures, PE value creation |
| Finance & Markets | 5 | SaaS multiples, private credit, VC benchmarks, infra funds |
| IT Technical | 5 | K8s adoption, vector DB benchmarks, LLM inference, observability |
| Regulatory | 5 | EU AI Act, CSRD, SOX 404, DORA, GDPR/Schrems |
| Deep Research | 5 | Multi-hop: CSRD supply chain, GenAI ROI, climate risk, quantum, green H2 |

### Evaluation Criteria (Weighted)
| Criterion | Weight | Description |
|-----------|--------|-------------|
| Relevance & Precision | 25% | % of top-10 directly answering query |
| Source Quality & Authority | 20% | Tier-1 regulators, advisors, primary sources |
| Depth & Completeness | 20% | Granular breakdowns, multiple perspectives |
| Recency & Freshness | 15% | Data from last 6-12 months |
| Structured Data | 10% | Tables, specific numbers, citations in snippets |
| Query Understanding | 10% | Handles multi-part, implicit intent queries |

---

## Engines under test — what was actually called

Engine identity is an API contract, not a routing story, so both sides are specified here.
The harness in the repository implements exactly these calls.

| | Challenger: Keenable | Incumbent: Exa |
|---|---|---|
| Endpoint | `POST https://api.keenable.ai/v1/search` (keyed) / `/v1/search/public` (anonymous) | `POST https://api.exa.ai/search` |
| Auth | `X-API-Key: <key>`, plus `X-Keenable-Title: <app-id>` | `x-api-key: <key>` |
| Request body | `{"query": ..., "max_results": N}` | `{"query": ..., "numResults": N, "contents": {"text": {"maxCharacters": 1200}}}` |
| Tier used here | **anonymous free tier** (runs with no key) | keyed |
| Rate limits | undocumented for the anonymous tier; the harness uses a 1.5 s delay | account plan limits |
| Index version control | none exposed | none exposed |

**A caveat on the comparator.** The incumbent in the original run was reached through a
keyless fallback in the tooling that ran it, and that fallback resolves to Exa. The comparator
is therefore **Exa**, not Brave, Tavily or Perplexity, and not "the default search backend" in
general. Re-running the repository's harness against a different incumbent is a different
experiment.

**Data availability.** Captured result sets are *not* redistributed in the repository —
redistributing third-party search results raises terms-of-service questions that are the
operator's to answer. What ships is the code, the exact 30-query set, the rubric, the
contracts and the scoring harness, so anyone can regenerate the captures in about ten minutes
with their own credentials. Nothing in this report depends on a dataset the reader cannot
rebuild.

## Detailed Findings by Category

### 1. Business Intelligence — SaaS Market Sizing (BI-001)

**Query:** *"Total Addressable Market B2B SaaS DACH region 2024 2025 forecast"*

| Aspect | Keenable.ai | Default (exa) |
|--------|-------------|---------------|
| **Top Source** | GrandViewResearch (2025: $28.1B, 2033: $67.8B; 11.3% CAGR **as stated by the source** — not reproducible from these two endpoints, which imply 13.4% over 2026–33, so treat the CAGR as source-reported) | Stripe (2025: $19.5B, 2030: $36.7B, 13.35% CAGR) |
| **Law Firm/Advisor** | OMR (Bitkom 2026: €58.3B software, 10.2% growth) | JollyMarketer (€24B market, €2.8B VC Q1 2025) |
| **Financial Metrics** | eFinancialModels: €9.3B ARR 2026, 14% CAGR, CAC 40-60% > US, NRR 112% | Valueships: 1,200 cos analyzed, pricing plans, currency data |
| **Regulator/Assoc** | Bitkom, Main Capital Partners (€986M top 50, SaaS 50% rev) | Statista, Scaleway (5B EUR H1 2022 investment) |
| **Recency** | **2025/2026 data points** | 2024/2025 data points |

**Score:** Keenable 4.5/5 | Default 4.0/5  
**Keenable wins** on recency (2026 projections), granular financial metrics (CAC, NRR, ARR by tier), and law firm analysis.

---

### 2. Strategy & M&A — Cybersecurity Valuation Multiples (STRAT-001)

**Query:** *"Technology M&A valuation multiples cybersecurity 2023 2024 EV/Revenue EV/EBITDA"*

| Aspect | Keenable.ai | Default (exa) |
|--------|-------------|---------------|
| **Public Comps (Growth Tier)** | **Q4 2024:** High 14.3x, Med 6.9x, Low 4.7x EV/Rev (Solganick) | **Q3 2024:** High 9.5x, Med 7.5x, Low 4.0x EV/Rev (Solganick) |
| **Private Deal Database** | Aventis: 64 deals 2015-2025, median 2.1x Rev, 12.8x EBITDA, by rev tier | CFI Group: Large public comps table, EV/Rev & EV/EBITDA by company |
| **Recent Mega Deals** | Thoma Bravo/Darktrace €5B (7.8x Rev, 41.9x EBITDA), Cloudflare 31.3x | Lincoln Intl: 2024 $20.6B volume, median 6.7x, 34% deal count increase |
| **PE vs Strategic** | Aventis IT Services: Cyber services highest multiples | RL Hulett Q4 2024: PE EV/Rev 4.7x, Strategic 2.0x, PE EV/EBITDA 42.9x |
| **Quarterly Trends** | Cogent: Quarterly EV/Rev (3.2→3.6), EV/EBITDA (14.6→14.7) 2024 | BDO Q3 2023: Cyber median 5.3x Sales, 21.2x EBITDA (older) |
| **Recency** | **Q4 2024, Q1 2025, 2025 reports** | Q3 2024, Q2 2024, H2 2023 |

**Score:** Keenable 4.8/5 | Default 4.2/5  
**Keenable wins decisively** — 6-12 months fresher data, granular breakdowns by growth tier/revenue tier/EBITDA tier, private deal database (64 deals), quarterly trend tracking.

---

### 3. Regulatory — EU AI Act Financial Services (REG-001)

**Query:** *"EU AI Act implementation timeline financial services high-risk AI systems 2024 2025"*

| Aspect | Keenable.ai | Default (exa) |
|--------|-------------|---------------|
| **Official Sources** | EU AI Act Service Desk, Consilium (Council final green light) | EU AI Act Service Desk, digital-strategy.ec.europa.eu, BaFin |
| **Law Firm Analysis** | **HLC (2 articles), Luware, Finlexpro, Zango.ai, Deloitte PDF** | Deloitte UK, Forvis Mazars, KPMG |
| **Key Developments** | **May 7 2026 provisional agreement**, July 2025 Commission guidance, EBA mapping | Eurofi Sep 2024 (older), European Commission Jun 2019 |
| **Practical Guidance** | Luware: 4-regulatory-layer table, penalty tiers, use-case classification | Deloitte: Omnibus debate, 16-month extension, backstop Dec 2027 |
| **FS-Specific** | Finlexpro: Credit/insurance/investment/KYC high-risk categories, steps | Eurofi: Credit scoring & insurance pricing as high-risk (detailed) |
| **Recency** | **2025/2026 developments** | Mix of 2024 and older |

**Score:** Keenable 4.6/5 | Default 4.3/5  
**Keenable edges** on law firm depth (5 firms vs 3), recency (May 2026 agreement vs Sep 2024 Eurofi), and practical compliance tooling (tables, checklists, penalty tiers).

---

### 4. IT Technical — Vector Database Benchmarks (IT-002)

**Query:** *"Vector database comparison Pinecone Weaviate Chroma Milvus Qdrant performance benchmarks 2024"*

| Aspect | Keenable.ai | Default (exa) |
|--------|-------------|---------------|
| **Benchmark Sources** | GitHub (jhondados 100M vectors), arXiv (2608.12812 7 DBs, 6 datasets) | Qdrant official, augustyniak.ai (production benchmarks), Linux Club |
| **Metrics Coverage** | Recall@k, QPS, P99 latency, index build, cost/1M queries, RAM | p50/p95/p99 latency, QPS, indexing time, RAM, pricing |
| **Scale Tested** | **100M vectors** (VectorBench), 1M-10M (multiple sources) | 1M, 10M, 100M (Linux Club), 1M (augustyniak) |
| **Vendor Coverage** | 7 DBs: Qdrant, Weaviate, Milvus, pgvector, Pinecone, Chroma, LanceDB | 5-6 DBs across sources |
| **Academic Rigor** | arXiv paper with 15 metrics, 6 datasets, statistical analysis | Practitioner blogs, vendor benchmarks |
| **Recency** | **2024/2025** (arXiv Aug 2024, VectorBench 2024) | 2024 (Qdrant Jan/Jun 2024, augustyniak 2024) |

**Score:** Keenable 4.7/5 | Default 4.5/5  
**Keenable edges** on methodological transparency (arXiv preprint — not journal peer review), scale (100M vectors), and metric breadth (15 metrics vs 5-6). Default strong on practitioner perspective.

---

### 5. Finance & Markets — SaaS Valuation (FIN-001)

**Query:** *"SaaS valuation benchmarks Series B ARR multiple 2024 public comps private transactions"*

| Aspect | Keenable.ai | Default (exa) |
|--------|-------------|---------------|
| **Public Comps** | Bessemer Cloud Index, Meritech, BVP Nasdaq (via Keenable sources) | SaaS Capital (SCI median 7.0x, top 10 14.2x), Meritech |
| **Private Rounds** | Aventis, Finerva/SEG, ICONIQ (via Keenable sources) | SaaS Rise: Series B median $82.5M pre-money, 10.89x rev mult |
| **Growth Tier Breakdown** | **Keenable sources include growth-tier multiples** | SaaS Capital: by company (CrowdStrike 20.8x, Snowflake 13.7x) |
| **Rule of 40 Analysis** | Included in Keenable sources | Aventis: only 15% clear Rule of 40 on EBITDA basis |
| **Recency** | 2024/2025 data | 2024/2025 data |

**Score:** Keenable 4.3/5 | Default 4.3/5  
**Tie** — both return excellent authoritative sources (Bessemer, Meritech, SaaS Capital, ICONIQ, Aventis, Finerva).

---

### 6. Deep Research — Multi-hop Queries (DEEP-001 to DEEP-005)

**Sample Query:** *"Impact of CSRD on non-EU companies supply chain reporting Scope 3 emissions data availability challenges 2024"*

| Aspect | Keenable.ai | Default (exa) |
|--------|-------------|---------------|
| **Multi-hop Synthesis** | Strong — connects regulation → scope 3 → supply chain → data challenges | Strong — similar synthesis capability |
| **Source Diversity** | EFRAG, CDP, SBTi, Big 4, academic, industry associations | Similar source diversity |
| **Recency** | 2024/2025 focus | 2024/2025 focus |

**Score (revised after three-judge review):** Keenable wins 1 clearly (DEEP-002), loses 1 clearly (DEEP-001), and 3 are contested 2–1  
**Not a tie.** The original aggregate concealed a genuine win and a genuine loss. See Appendix B §B.3. Jev IDPS net: Keenable 4/5 on deep research, but the aggregate margin (5.5% of scale) is roughly half the consulting-category margin (9.7%).

---

## Quantitative Score Summary

**The v1 table (weighted totals 4.56 vs 4.28, recency +0.8) is withdrawn.** It was produced by
one unblinded judge reading raw result sets, with no stated n, no per-criterion scoring record
and no reproducible formula, and its largest component was the recency claim that the independent
judges failed to reproduce. It is replaced by the scored record below.

*Table 3. System One (Jev) MCDA composites, 0-2 ordinal scale, n=10 pairs. Source:
`evaluation/jev/mcda_scores.csv`. † = gap below the 0.10 noise floor (not a win). ⚠ = winner
differs between the two Jev contracts (MCDA vs IDPS).*

| Query | Keenable | default (exa) | Δ | Mean confidence K / D | IDPS winner |
|---|---|---|---|---|---|
| BI-001 (market sizing) | 1.603 | 1.077 | +0.526 | 0.68 / 0.72 | keenable |
| STRAT-001 (cyber M&A) | 1.774 | 1.692 | +0.082 † | 0.58 / 0.69 | keenable |
| REG-001 (EU AI Act) | 1.839 | 1.668 | +0.171 | 0.77 / 0.74 | keenable |
| IT-002 (vector DB) | 1.472 | 1.341 | +0.131 | 0.66 / 0.77 | keenable |
| FIN-001 (SaaS multiples) | 1.512 | 1.449 | +0.064 † | 0.59 / 0.60 | keenable |
| DEEP-001 (CSRD supply chain) | 1.337 | 1.388 | -0.051 † | 0.69 / 0.71 | default-exa |
| DEEP-002 (GenAI ROI) | 1.554 | 1.028 | +0.525 | 0.79 / 0.84 | keenable |
| DEEP-003 (climate/banking) | 1.548 | 1.466 | +0.081 † | 0.64 / 0.82 | keenable |
| DEEP-004 (post-quantum) | 1.425 | 1.473 | -0.048 † | 0.74 / 0.79 | keenable |
| DEEP-005 (green hydrogen) | 1.623 | 1.581 | +0.043 † | 0.73 / 0.70 | keenable |

Two further cautions on this table:

- **CONTRADICTION: DEEP-004.** The MCDA composite puts Exa ahead (−0.048) while the IDPS
  arbitration puts Keenable ahead. Both are Jev contracts over the same evidence. The gap is
  below the noise floor either way, but the two contracts disagreeing in sign means DEEP-004
  should be read as *no difference detected*, not as a result.
- **PROTOCOL DEVIATION: FIN-001** was captured at `limit=5` while every other query used
  `limit=10`. The relevance anchors are stated as counts out of 10, so FIN-001's scores are not
  comparable. It is **included** in the n=5 headline means quoted in the Verdict, since excluding a
  protocol-deviant case after seeing its result is exactly the kind of selection this report
  should not do. An **n=4 sensitivity check** (dropping FIN-001) is reported alongside: Jev
  +0.227, CI −0.094 to +0.549; grok +0.369, CI +0.281 to +0.457 - the same conclusion).

### Statistical treatment, stated plainly

- Planned in the project rubric: paired test, Cohen's d, 95% intervals. **Run: two-sided
  t-intervals on per-pair differences only.** No paired test statistic, no effect size and no
  multiple-comparison correction were applied.
- The 0.10 floor is a pre-declared pragmatic threshold (roughly 5% of the 0-2 scale), not a
  derived minimum detectable effect.
- Composites remain **ordinal**. Intervals are shown to bound the uncertainty in the ranking
  summary; they do not make the scale interval. Ratios **are** computed in Appendix B
  (frontier-Δ vs Jev-Δ) and are there labelled explicitly as ratios of ordinal composites, not
  as effect sizes, and are not to be read as "Keenable is 1.7× better".

<!-- QUANT_END -->
## Key Differentiators

### Keenable.ai advantages

Ordered by evidential strength, strongest first. Only items 1–2 are supported by all three judges.

1. **Analytical resolution (confirmed).** Revenue-tier ($1–5M / $5–20M / $20–100M / $100M+),
   growth-tier (>20% / 10–20% / <10%) and EBITDA-tier multiples; segment splits rather than a
   single median. Widest agreeing margin in the study.
2. **Deal-level and time-series evidence (confirmed).** Aventis's 64-deal cybersecurity database
   2015–2025; Cogent's eight-quarter EV/Revenue and EV/EBITDA series; per-company multiples with
   margin and Rule-of-40 side by side.
3. **Operator-ready regulatory material.** Day-level effective dates, three-tier penalty
   schedules mapped to article groups, and use-case classification matrices — liftable into an
   exhibit with attribution intact.
4. **Breadth of advisor commentary.** Law-firm analyses (Jones Day, Linklaters, Cooley) alongside
   specialist explainers; note that vendor-authored material (Luware, Zango.ai) is mixed in.
5. **Methodological transparency in technical sources.** Preprints and reproducible benchmark
   suites stating hardware, dataset and recall/precision thresholds. *Preprints, not journal
   peer review.*

### Contested, and not counted as advantages
- **Recency.** See [What changed from v1](#what-changed-from-v1). Not established.
- **Source authority.** Small edge at best (Jev +0.23, grok +0.05).

### Default (exa) Advantages
1. **Regulator Coverage** — BaFin, Eurofi, European Commission, national supervisors, KPMG/Forvis Mazars
2. **Practitioner Perspective** — augustyniak.ai production benchmarks, vendor official benchmarks (Qdrant)
3. **Consistency** — Equally authoritative for well-established topics (public SaaS comps, major regulatory frameworks)
4. **Zero-Key Access** — Works without API key via keyless tier

---

## Recommendations

### Consulting queries (BI / M&A / Finance / IT / Regulatory) — prefer Keenable

On the pre-declared rule (gap ≥ 0.10 and the same winner in both presentation orders) the
record is **Jev 3 of 5 clear wins, frontier judge 5 of 5**. Jev's consulting interval
(−0.041 to +0.430) includes zero, so the direction is consistent but the magnitude is not
established. The gain is concentrated where segmented data matters:

- M&A and valuation work needing multiples split by growth, revenue or EBITDA tier
- Competitive intelligence that depends on deal-level private-market data
- Regulatory tracking that needs effective dates and penalty schedules, not summaries
- Technical due diligence where reproducible benchmarks beat vendor claims

### Multi-hop deep research — do not standardise

+5.5% of scale, mixed winners. **Exa won DEEP-001 outright** (CSRD supply-chain reporting);
Keenable won DEEP-002 decisively; three were splits. Pick per question, or run both.

### Either engine is adequate
- Public market comparables (Bessemer, Meritech, SaaS Capital)
- Major regulatory frameworks (EU AI Act, GDPR, DORA) at overview level
- Historical trend work and vendor benchmark round-ups

### Implementation Note
The default backend in this Hermes configuration falls back to **exa** (keyless tier) when ddgs is unavailable. Results shown for "Default" are exa-backed. A configured Brave/Tavily/Perplexity backend may yield different comparative results.

---

## Appendix: Test Queries Run

The 30 queries are reproduced byte-identically, because a re-worded query is a different
experiment. Canonical machine-readable source: `config/queries.yaml` in the repository. The
abbreviated list that appeared in v1 has been removed.

| ID | Category | Limit | Query (byte-identical to what was executed) |
|---|---|---|---|
| BI-001 | business_intelligence | 10 | `Total Addressable Market B2B SaaS DACH region 2024 2025 forecast` |
| BI-002 | business_intelligence | 10 | `Competitive landscape European neobanks 2024 market share revenue N26 Revolut Bunq Monzo` |
| BI-003 | business_intelligence | 10 | `Enterprise software spending growth trends 2024 Gartner IDC worldwide IT spending forecast` |
| BI-004 | business_intelligence | 10 | `Supply chain management software market size 2024 key vendors SAP Oracle Blue Yonder Manhattan Associates` |
| BI-005 | business_intelligence | 10 | `Generative AI enterprise adoption rates 2024 survey McKinsey BCG Bain Deloitte PwC` |
| STRAT-001 | strategy_ma | 10 | `Technology M&A valuation multiples cybersecurity 2023 2024 EV/Revenue EV/EBITDA` |
| STRAT-002 | strategy_ma | 10 | `Microsoft Activision Blizzard deal structure regulatory approval timeline FTC CMA EU Commission` |
| STRAT-003 | strategy_ma | 10 | `Private equity portfolio value creation levers 2024 operational improvement add-on acquisitions` |
| STRAT-004 | strategy_ma | 10 | `Carve-out separation costs benchmarks IT systems TSAs duration 2023 2024` |
| STRAT-005 | strategy_ma | 10 | `Roll-up strategy success factors fragmentation HVAC dental veterinary 2024 case studies` |
| FIN-001 | finance_markets | 10 | `SaaS valuation benchmarks Series B ARR multiple 2024 public comps private transactions` |
| FIN-002 | finance_markets | 10 | `Private credit direct lending returns vs broadly syndicated loans 2023 2024 IRR MOIC` |
| FIN-003 | finance_markets | 10 | `Venture capital fund performance quartiles vintage 2020 2021 2022 TVPI DPI RVPI` |
| FIN-004 | finance_markets | 10 | `Infrastructure fund returns renewable energy digital infrastructure 2023 2024 benchmarks` |
| FIN-005 | finance_markets | 10 | `SPAC performance post-merger 2021 2022 2023 redemption rates shareholder returns` |
| IT-001 | it_technical | 10 | `Kubernetes adoption enterprise 2024 Gartner CNCF survey production clusters percentage` |
| IT-002 | it_technical | 10 | `Vector database comparison Pinecone Weaviate Chroma Milvus Qdrant performance benchmarks 2024` |
| IT-003 | it_technical | 10 | `LLM inference cost optimization GPU utilization vLLM TensorRT-LLM TGI 2024 benchmarks` |
| IT-004 | it_technical | 10 | `Data mesh architecture implementation patterns Data Contracts governance 2024 case studies` |
| IT-005 | it_technical | 10 | `Observability platform market share Datadog New Relic Dynatrace Grafana Splunk 2024 revenue` |
| REG-001 | regulatory | 10 | `EU AI Act implementation timeline financial services high-risk AI systems 2024 2025` |
| REG-002 | regulatory | 10 | `CSRD ESRS reporting requirements non-EU companies scope 2024 2025 double materiality` |
| REG-003 | regulatory | 10 | `SOX 404 compliance cost benchmarks mid-market companies 2024 external auditor fees internal resources` |
| REG-004 | regulatory | 10 | `DORA Digital Operational Resilience Act financial entities ICT risk management requirements 2025` |
| REG-005 | regulatory | 10 | `GDPR Article 28 DPA requirements international data transfers SCCs 2024 Schrems III implications` |
| DEEP-001 | deep_research | 10 | `Impact of CSRD on non-EU companies supply chain reporting Scope 3 emissions data availability challenges 2024` |
| DEEP-002 | deep_research | 10 | `Generative AI ROI enterprise deployments 2023 2024 measurable productivity gains cost savings case studies` |
| DEEP-003 | deep_research | 10 | `Climate transition risk banking portfolio alignment Paris Agreement NZBA PCAF methodology 2024` |
| DEEP-004 | deep_research | 10 | `Quantum computing threat timeline RSA ECC cryptography migration post-quantum NIST standards 2024 enterprise readiness` |
| DEEP-005 | deep_research | 10 | `Green hydrogen cost parity forecasts 2030 2040 electrolyzer CAPEX renewable LCOE regional analysis Europe Middle East Australia` |

**Scored subset.** Only **10 of these 30** went through the two independent judges
(Appendices A and B): BI-001, STRAT-001, REG-001, IT-002, FIN-001 (one exemplar from each
consulting category) plus DEEP-001..005. The other 20 were captured but **not scored**, so
nothing in this report supports a claim about them.

**Protocol deviation.** FIN-001 was captured at `limit=5`; every other query used `limit=10`.

# Appendix A — Decision-Plane (Jev / System One) Cross-Check

> **What this appendix is.** The body of this report was scored by a single LLM judge —
> DeepSeek-V4.1-Flash, **unblinded**, reading the raw result sets rather than the anonymised
> cards used by the two appendices. It is the weakest of the three layers in evidential terms
> and is reported as narrative, not as measurement. This appendix adds a **second, independent scoring
> layer** — the VWOOSH decision plane, running TypeSafe Jev Cloud (`jev-1.13.0`) over
> two purpose-written MCDA contracts — and reports where the two layers agree and,
> more usefully, where they do not. Nothing here replaces a body finding; the decision
> plane either corroborates it or puts a caveat next to it — and where it disagreed, the
> body above has been changed rather than merely annotated.

## A.1 Why a second layer at all

A single-judge narrative has two known failure modes for this kind of work:

1. **Over-claiming.** A judge that has already formed a thesis writes sweeping criteria
   deltas to support it. The recency gap claimed in the body (Section "Quantitative
   Score Summary", +0.8 of 5) is exactly this shape — and, as shown in A.5, the decision
   plane does *not* reproduce it.
2. **Non-reproducibility.** Prose scores cannot be re-run. A typed contract plus a
   pinned model plus a rubric hash can be.

The decision plane is a *different kind of judge*: ordinal anchors, a fixed rubric
compiled to a typed contract, per-dimension probability distributions over the anchor
set, and an explicit confidence floor that refuses to let a low-confidence call pass
silently as a decision.

## A.2 Execution provenance (verified, not assumed)

The `vwoosh-decision-plane` skill documents a silent-degradation trap: if
`typesafe-sdk` is missing or `TYPESAFE_API_KEY` is unset, the service falls back to a
local LM Studio model and inflates latency while making **zero** cloud calls. Every
call in this appendix was therefore verified against the returned verdict object rather
than trusted from the CLI banner.

| Property | Observed value |
|---|---|
| Backend (all 20 evaluation + 40 arbitration calls) | `typesafe_cloud` |
| Model resolved | `jev-1.13.0` |
| Degradation flag raised | never (`degraded: false` on all 20 evaluations) |
| Live HTTP dispatch | `POST https://api.typesafe.ai/v1/systemone → 200` (e.g. `req_01a1ca3660387c57ba47e1fc6c5d0552`) |
| MCDA rubric hash | `sha256:c6fcbc1048637221244ad5ea9333a306fb4e46b469226316bc4217c0c7c0b6ce` |
| Arbitration rubric hash | `sha256:61fa2cd2beb2d54b660ca0452c975c6abc750218fca29b44a1da9dfcf0793029` |
| `evaluate` latency | n=20, min 198 ms / median 220 ms / max 368 ms |
| `compare` inner-call latency | n=40, median 205 ms / max 269 ms |
| Escalations against the 0.70 floor | 10 of 20 evaluations |

Calls made, counted from the artefact rather than from the plan: **20** `evaluate`
(10 query pairs × 2 engines) + **20** `compare` (10 pairs × 2 presentation orders, each
producing 2 verdicts) = **40 CLI invocations, 60 System One calls**. An earlier draft carried
the five-category arithmetic (10 + 10 = 30 calls); that was the first pass and is superseded.

> **Cost of regeneration.** Jev is priced per call, not per token. Counted from the artefacts:

| Stage | Calls | Observed latency | Basis | Est. cost |
|---|---|---|---|---|
| Capture (2 engines × 30 queries) | 60 HTTP | ~0.5-2 s each | vendor list price | Keenable anonymous tier free; your Exa plan |
| Layer 2 — Jev `evaluate` | 20 | median 220 ms | ~$0.042 / 1k actions | ~$0.0008 |
| Layer 2 — Jev `compare` | 40 | median 205 ms | ~$0.042 / 1k actions | ~$0.0017 |
| Layer 3 — frontier judge | 20 | ~15-120 s each | your model's per-call price | model-dependent |
| **Layer 2 total** | **60** | sub-second | — | **~$0.0025** |

> Jev figures are list-price estimates, not an invoice. The dominant costs are the frontier
> judge and operator time; the System One layer is effectively free at this scale.

## A.3 The two contracts

Both contracts live in `evaluation/contracts/` and are reproduced here in summary.
Note the weight vector deliberately mirrors the human rubric, so a divergence between
layers is *not* an artefact of different weighting.

### `search-engine-mcda-v1` — per-engine scoring

Ordinal anchors 0..2 per dimension; composite is the weight-normalized mean on the 0..2
scale. `relevance_precision` is declared a **critical dimension** (a critical failure
forces REJECT/ESCALATE rather than averaging away).

| Dimension | Weight | Mirrors body criterion (weight) |
|---|---|---|
| `relevance_precision` | 2.5 | Relevance & Precision (25%) |
| `source_authority` | 2.0 | Source Quality & Authority (20%) |
| `analytical_depth` | 2.0 | Depth & Completeness (20%) |
| `recency_freshness` | 1.5 | Recency & Freshness (15%) |
| `structured_extractability` | 1.0 | Structured Data Extraction (10%) |
| `query_understanding` | 1.0 | Query Understanding (10%) |

### `search-engine-arbitration-v1` — head-to-head IDPS arbitration

Companion contract for `vwoosh decision compare`, which resolves two candidates with
zero order-bias (IDPS). Dimensions are framed as *comparative* rather than absolute:
`evidence_sufficiency` (3.0, critical), `dispositive_recency` (2.5),
`decision_granularity` (2.5), `source_authority` (2.0), `deliverable_readiness` (2.0).
`tie_epsilon: 0.03`.

### Evidence cards

Because System One models have a hard input ceiling (~12,000 chars for Jev) and do not
perform arithmetic, each engine's result set was compiled into a bounded evidence card
containing *only* what the engine actually returned — every domain, every figure, and a
**pre-computed facts block** (counts of current-vs-stale results, tables present, tier-1
entities cited) calculated by script, not estimated by the model. Cards are in
`evaluation/evidence/`, named `{query_id}_{A|B}.txt`; A=Keenable, B=default. The engine
identity is **not** stated inside the cards — the judge scores blind.

Scope: the decision plane was run on **all six categories, 10 query pairs** — the five
consulting categories (BI-001, STRAT-001, REG-001, IT-002, FIN-001) and the five
deep-research queries (DEEP-001..005), 20 evaluations and 20 order-swapped arbitrations.
(The deep-research pairs were added after the first drafting pass, which covered only the
five consulting categories; every figure in this appendix reflects the full ten pairs.)

## A.4 Layer 1 result — MCDA scores (0–2, higher is better)

Rebuilt from the single canonical artefact `evaluation/jev/summary.json` (20 evaluations, 20
arbitrations). Figures are quoted to four decimals so that the printed Δ equals the printed
difference of the two columns; an earlier draft rounded to three and the Δ column then
disagreed with its own cells, and carried the five-category run besides.

| Query | Keenable | default (exa) | Δ | Mean confidence K / D | IDPS winner |
|---|---|---|---|---|---|
| BI-001 (market sizing) | 1.6035 | 1.0775 | +0.5260 | 0.68 / 0.72 | keenable |
| STRAT-001 (cyber M&A) | 1.7740 | 1.6920 | +0.0820 † | 0.58 / 0.69 | keenable |
| REG-001 (EU AI Act) | 1.8390 | 1.6685 | +0.1705 | 0.77 / 0.74 | keenable |
| IT-002 (vector DB) | 1.4720 | 1.3405 | +0.1315 | 0.66 / 0.77 | keenable |
| FIN-001 (SaaS multiples) | 1.5125 | 1.4485 | +0.0640 † | 0.59 / 0.60 | keenable |
| DEEP-001 (CSRD supply chain) | 1.3370 | 1.3880 | -0.0510 † | 0.69 / 0.71 | default-exa |
| DEEP-002 (GenAI ROI) | 1.5540 | 1.0285 | +0.5255 | 0.79 / 0.84 | keenable |
| DEEP-003 (climate/banking) | 1.5480 | 1.4665 | +0.0815 † | 0.64 / 0.82 | keenable |
| DEEP-004 (post-quantum) | 1.4255 | 1.4730 | -0.0475 † | 0.74 / 0.79 | keenable |
| DEEP-005 (green hydrogen) | 1.6235 | 1.5805 | +0.0430 † | 0.73 / 0.70 | keenable |

† gap below the 0.10 noise floor — **not a win**. ⚠ the two Jev contracts disagree on the
winner (only DEEP-004).

Ten-pair means: Keenable 1.5689 vs default 1.4163, gap **0.1525** — on the
0–100 presentation scale, 78.4 vs 70.8. See the statistical
cautions in "Quantitative Score Summary" before quoting that as a percentage.

## A.5 Layer 2 result — IDPS arbitration (blind, both orders)

Each pair was arbitrated twice with the candidates swapped. A winner that flips between orders
indicates position bias rather than a real difference. Values read from
`evaluation/jev/summary.json`; an earlier draft of this table carried the five-category run.

| Query | Order | score A | score B | Δ | Winner | Maps to |
|---|---|---|---|---|---|---|
| BI-001 | A=kee / B=def | 1.258 | 0.723 | +0.536 | candidate_a | **Keenable** |
| BI-001 | A=def / B=kee | 0.720 | 1.244 | -0.524 | candidate_b | **Keenable** |
| STRAT-001 | A=kee / B=def | 1.734 | 1.437 | +0.298 | candidate_a | **Keenable** |
| STRAT-001 | A=def / B=kee | 1.427 | 1.728 | -0.301 | candidate_b | **Keenable** |
| REG-001 | A=kee / B=def | 1.857 | 1.504 | +0.353 | candidate_a | **Keenable** |
| REG-001 | A=def / B=kee | 1.501 | 1.886 | -0.385 | candidate_b | **Keenable** |
| IT-002 | A=kee / B=def | 1.341 | 1.045 | +0.296 | candidate_a | **Keenable** |
| IT-002 | A=def / B=kee | 1.052 | 1.330 | -0.277 | candidate_b | **Keenable** |
| FIN-001 | A=kee / B=def | 1.533 | 1.436 | +0.097 | candidate_a | **Keenable** |
| FIN-001 | A=def / B=kee | 1.428 | 1.526 | -0.098 | candidate_b | **Keenable** |
| DEEP-001 | A=kee / B=def | 1.117 | 1.212 | -0.095 | candidate_b | **default** |
| DEEP-001 | A=def / B=kee | 1.200 | 1.124 | +0.076 | candidate_a | **default** |
| DEEP-002 | A=kee / B=def | 1.331 | 0.710 | +0.621 | candidate_a | **Keenable** |
| DEEP-002 | A=def / B=kee | 0.723 | 1.327 | -0.604 | candidate_b | **Keenable** |
| DEEP-003 | A=kee / B=def | 1.274 | 1.201 | +0.073 | candidate_a | **Keenable** |
| DEEP-003 | A=def / B=kee | 1.206 | 1.262 | -0.055 | candidate_b | **Keenable** |
| DEEP-004 | A=kee / B=def | 1.366 | 1.190 | +0.176 | candidate_a | **Keenable** |
| DEEP-004 | A=def / B=kee | 1.195 | 1.379 | -0.185 | candidate_b | **Keenable** |
| DEEP-005 | A=kee / B=def | 1.333 | 1.272 | +0.060 | candidate_a | **Keenable** |
| DEEP-005 | A=def / B=kee | 1.265 | 1.322 | -0.056 | candidate_b | **Keenable** |

**Order-invariance of the winner: PASS, 10/10.** No pair produced a tie (`tie_broken_by` null
throughout), so the `tie_epsilon: 0.03` mechanism never fired.

Arbitration dimension means over all 20 verdicts:

| Dimension | Keenable | default | Δ |
|---|---|---|---|
| `source_authority` | 1.621 | 1.319 | **+0.302** |
| `decision_granularity` | 1.524 | 1.227 | **+0.297** |
| `deliverable_readiness` | 0.979 | 0.739 | **+0.240** |
| `evidence_sufficiency` | 1.274 | 1.076 | **+0.198** |
| `dispositive_recency` | 1.652 | 1.463 | **+0.189** |

## A.6 How the decision plane changed the findings

### (1) It removed the recency over-claim

The body's v1 draft asserted a **+0.8 of 5** recency advantage. Neither Jev contract supports an
effect of that size:

| Layer | Recency gap | As % of its scale | n |
|---|---|---|---|
| Body v1 (single unblinded judge) | +0.8 of 5 | 16.0% | 6 exemplars |
| MCDA contract, all 10 pairs | **+0.042 of 2** | **2.1%** | 20 evaluations |
| MCDA contract, consulting 5 | +0.046 of 2 | 2.3% | 10 evaluations |
| Arbitration (`dispositive_recency`) | +0.280 of 2 | 14.0% | 20 verdicts |

The two Jev contracts disagree with each other *and* with the body — a finding in its own
right. Per-query MCDA recency is not uniform: Keenable leads BI-001 (**1.40 vs
1.11**), **trails** FIN-001 (**1.28 vs 1.56**),
and is essentially level on STRAT-001 (**1.49 vs 1.47**).
Recency is contested and small in aggregate; the v1 +0.8 claim was an overstatement.

### (2) It re-ranked *which* dimension drives the difference

| Dimension | Δ all 10 | Δ consulting 5 |
|---|---|---|
| `analytical_depth` | **+0.308** | **+0.424** |
| `source_authority` | +0.232 | +0.144 |
| `query_understanding` | +0.168 | +0.252 |
| `structured_extractability` | +0.122 | +0.276 |
| `relevance_precision` | +0.037 | +0.086 |
| `recency_freshness` | **+0.042** | +0.046 |

The advantage is in disaggregation, not currency. **Buy Keenable for resolution, not recency.**

### (3) Calibration signal

Escalations against the 0.70 confidence floor: **10 of 20** evaluations across all pairs
(7 of 10 on the consulting five). `recency_freshness` carries the least confidence — mean
**0.483** over all 20, with **15 of 20** below the floor (consulting-only: 0.414, 8 of 10).
Next lowest is `query_understanding` (0.592 all-20). The plane is confident about what it can
count and unsure about what requires judging currency or intent.

### (4) Order bias: winner stable, magnitude not

| Query | \|Δ\| AB | \|Δ\| BA | Asymmetry | As % of Δ | vs `tie_epsilon` 0.03 |
|---|---|---|---|---|---|
| BI-001 | 0.536 | 0.524 | 0.012 | 2.3% | within |
| STRAT-001 | 0.298 | 0.301 | 0.003 | 1.1% | within |
| REG-001 | 0.353 | 0.385 | 0.032 | 8.6% | **exceeds** |
| IT-002 | 0.296 | 0.277 | 0.019 | 6.5% | within |
| FIN-001 | 0.097 | 0.098 | 0.000 | 0.4% | within |
| DEEP-001 | 0.095 | 0.076 | 0.018 | 21.5% | within |
| DEEP-002 | 0.621 | 0.604 | 0.017 | 2.8% | within |
| DEEP-003 | 0.073 | 0.055 | 0.017 | 26.7% | within |
| DEEP-004 | 0.176 | 0.185 | 0.009 | 4.9% | within |
| DEEP-005 | 0.060 | 0.056 | 0.004 | 7.1% | within |

Mean asymmetry **8.2%** of delta magnitude, maximum **26.7%**. Only
REG-001 exceeds the contract's 0.03 absolute `tie_epsilon`. Consequences:

- Rankings from `compare` are trustworthy (**10/10** stable).
- Delta magnitudes should not be quoted to two decimals; for |Δ| < 0.15 the magnitude is not
  reliable at all.

## A.7 Agreement between the layers

| Query | Plane Δ (MCDA, K−D) | Plane winner (IDPS) | Body verdict (1–5) | Agree? |
|---|---|---|---|---|
| BI-001 | +0.526 | Keenable | Keenable (+0.5) | yes |
| STRAT-001 | +0.082 | Keenable | Keenable (+0.6) | yes |
| REG-001 | +0.171 | Keenable | Keenable (+0.3) | yes |
| IT-002 | +0.131 | Keenable | Keenable (+0.2) | yes |
| FIN-001 | +0.064 | Keenable | tie (±0.0) | **no** |

**4 of 5 in direction**; the single disagreement (FIN-001) is about size, not sign.

**Do not compare the layers' absolute numbers.** Different scales, different anchors:

| Layer | Keenable | default | Gap |
|---|---|---|---|
| Body, weighted (1–5) — **withdrawn**, see Quantitative Score Summary | ~~4.56~~ | ~~4.28~~ | ~~0.28~~ |
| MCDA composite (0–2), all 10 pairs | 1.569 | 1.416 | 0.153 |
| MCDA composite (0–100 presentation) | 78.4 | 70.8 | 7.6 |
| MCDA rescaled to 1–5 (`1 + 2 × composite`) | 4.14 | 3.83 | 0.31 |

The 1–5 rescaling is `1 + 2 × composite` (mapping 0–2 onto 1–5). An earlier draft used
`1 + composite`, which maps onto 1–3 and was wrong.

## A.8 Reproducing this appendix

```bash
cd ~/Projects/search-benchmark

# 1. Confirm the cloud backend is live (guards against silent local fallback).
vwoosh decision evaluate \
  --state-file evaluation/jev_probe_state.json \
  --contract ~/.hermes/vwoosh-local/engine/_DEVELOPMENT/00_ADMIN/decisions/dependency-selector-v1.yaml \
  --output evaluation/jev_probe_verdict.json --backend cloud
# expect: Backend: typesafe_cloud / Model: jev-1.13.0

# 2. Re-run both layers (10 evaluate + 10 compare, both orders).
python3 scripts/run_decision_plane.py

# 3. Artefacts
#    evaluation/jev/mcda_scores.csv     per-engine per-dimension scores
#    evaluation/jev/arbitration.csv     both orders, deltas, winners
#    evaluation/jev/summary.json        full raw verdicts incl. probabilities
#    evaluation/jev/mcda_<q>_<A|B>.json individual verdicts
#    evaluation/jev/arb_<q>_<AB|BA>.json individual arbitrations
```

Operational notes worth carrying forward:

- `--backend cloud` must be passed explicitly; `auto` may select local.
- Verify `verdict.backend == "typesafe_cloud"` in the **output JSON**, not the banner —
  the silent-fallback failure mode produces a normal-looking table with zero cloud calls.
- Jev's input ceiling forces summarising before evaluation. Every number in the evidence
  cards was computed by script first and injected as text; System One does not do
  arithmetic, so feeding it raw prose and asking for a rate would have produced invented
  figures.
- Blind labelling is enforced by withholding engine identity inside the cards. Re-running
  `compare` in both orders is the cheap way to check the blind held.

## A.9 Net effect on the report's conclusions

| Body conclusion | After decision-plane cross-check |
|---|---|
| Keenable wins overall | **Upheld, with the margin restated.** **10/10** arbitration wins, both orders, no ties; mean MCDA gap **+0.153** over all 10 pairs (+0.195 on the consulting five). The v1 wording ("5/5 wins, +0.201") was the five-category run. |
| Recency is the largest differentiator | **Revised.** Likely overstated; recency is category-specific and small in aggregate. |
| Depth/granularity is an advantage | **Reinforced.** Largest gap in both contracts. |
| Source authority is a tie | **Not upheld.** MCDA all-10 puts Keenable ahead by **+0.232** (consulting five: +0.144); arbitration agrees (+0.223). Treat as a real but modest edge, not a tie. |
| FIN-001 is a tie | **Upheld in substance.** Plane's +0.069 is within noise. |
| Default wins on regulator coverage | **Not corroborated.** `source_authority` favours Keenable in both contracts. The body's regulator-coverage point stands as a *qualitative* observation but is not reflected in the blind scores. |

**Bottom line of this appendix:** the primary recommendation survives an independent
judge, but the *reasoning* given for it in the body was partly wrong. Keenable's
advantage is in resolution and deliverable-readiness, not primarily in freshness — and
the body's own confidence in the recency claim was too high.

# Appendix B — Third Layer: Frontier-LLM Judge (grok-4.6), All Ten Pairs

## B.1 Purpose and design

Appendix A added one independent judge (Jev) against the single-judge body. Two judges can
only disagree; three can reveal *which* judge is the outlier on *which* dimension. This layer
adds a frontier LLM judge — the tool a consultant would actually reach for — under the same
discipline as the IDPS layer: **blind cards, both presentation orders.**

| Property | Value |
|---|---|
| Model | `grok-4.6` via `custom:vwoosh-foundry` (Azure Foundry, credit-backed) |
| Dimensions | the **same six** and **same ordinal anchors (0..2)** as `search-engine-mcda-v1` |
| Weights | identical (2.5 / 2.0 / 2.0 / 1.5 / 1.0 / 1.0) — composites directly comparable to Jev MCDA |
| Blindness | engine identity withheld inside cards; both presentation orders run |
| Calls | **20** (10 query pairs × 2 orders) |
| Validation | strict-JSON output, integer 0..2 per dimension per candidate, winner ∈ {A,B,tie}, up to 3 retries |

## B.2 Three layers, all ten query pairs

K = Keenable · D = default (exa) · `—` means the judge called it a tie.

| Query | Body (1–5) | Jev MCDA (0–2) | Jev IDPS | grok-4.6 (0–2) | Consensus |
|---|---|---|---|---|---|
| BI-001 | 4.5 / 4.0 → K | 1.603 / 1.077 → K | K | 1.350 / 0.925 → K | **all agree** |
| STRAT-001 | 4.8 / 4.2 → K | 1.774 / 1.692 → K | K | 1.900 / 1.550 → K | **all agree** |
| REG-001 | 4.6 / 4.3 → K | 1.839 / 1.668 → K | K | 1.800 / 1.500 → K | **all agree** |
| IT-002 | 4.7 / 4.5 → K | 1.472 / 1.341 → K | K | 1.800 / 1.400 → K | **all agree** |
| FIN-001 | 4.3 / 4.3 → tie | 1.512 / 1.449 → K | K | 1.750 / 1.250 → K | 3 of 4 say K |
| **DEEP-001** | *aggregate only* | 1.337 / **1.388 → D** | **D** | 1.450 / 1.450 → tie | **default or no difference** |
| **DEEP-002** | *aggregate only* | 1.554 / 1.028 → K | K | 1.800 / 1.300 → K | **all agree: K** |
| **DEEP-003** | *aggregate only* | 1.548 / 1.466 → K | K | 1.500 / **1.550 → D** | split, 2–1 K |
| **DEEP-004** | *aggregate only* | 1.425 / **1.473 → D** | K | 1.750 / 1.450 → K | split, 2–1 K |
| **DEEP-005** | *aggregate only* | 1.623 / 1.581 → K | K | 1.300 / **1.400 → D** | split, 2–1 K |

Tally: **Jev IDPS** Keenable 9/10 · **Jev MCDA** Keenable 8/10 · **grok-4.6** Keenable 7/10,
default 2/10, 1 tie.

## B.3 The headline result: the advantage is category-specific

| Slice | Jev MCDA Δ | as % of scale | grok Δ | as % of scale | Frontier/Jev ratio |
|---|---|---|---|---|---|
| **All 10 pairs** | +0.153 | 7.6% | +0.262 | 13.1% | 1.7× † |
| **Consulting 5** (BI, STRAT, REG, IT, FIN) | +0.195 | 9.7% | +0.395 | 19.8% | **2.0×** † |
| **Deep research 5** (DEEP-001..005) | +0.110 | 5.5% | +0.130 | 6.5% | **1.2×** † |

† Ratios of mean ordinal composites, **not effect sizes**. The scales are not interval and the
confidence intervals in the Verdict overlap. Read the column as "the frontier judge is more
generous to the challenger", not as a measured multiplier: with 95% intervals of −0.041 to +0.430
(Jev consulting) and −0.187 to +0.407 (Jev deep), the two means cannot be separated at n=5.

The direction is consistent across slices, but **the v1 claim that the consulting edge is twice the
deep-research edge is not supported and is withdrawn**. In deep research the three judges agree on
only one of five queries:

- **DEEP-002 (GenAI ROI) — clear Keenable win.** Unanimous, and the largest gap in the whole
  benchmark (Jev 1.554 vs 1.028). The evidence cards explain it: the default engine returned
  five distinct domains with three Microsoft and three Automation Anywhere vendor case studies,
  while the challenger returned nine distinct domains spanning arXiv, Omdia, McKinsey, Deloitte
  and independent research.
- **DEEP-001 (CSRD supply chain) — directional default edge, below the clear-win floor.** The only query where
  two of three judges favour the incumbent, and the only IDPS loss for Keenable (Δ −0.095).
- **DEEP-003, DEEP-004, DEEP-005 — contested 2–1 for Keenable in every case**, but the dissent
  is always the frontier judge, and in two of the three the frontier judge's own verdict flipped
  between presentation orders.

**This materially qualifies the report body's Deep Research row**, which recorded both engines
at 4.2/4.2. That aggregate concealed a genuine win and a genuine loss.

## B.4 The frontier judge polarises more — but the gap depends on the category

All 10 pairs: Jev Δ = +0.153 (7.6% of scale); grok Δ = +0.262 (13.1%). The frontier judge's
mean delta is larger in every slice — by a factor of 1.7 across all pairs, 2.0 on consulting and
1.2 on deep research. **Those factors are ratios of ordinal composites, not effect sizes**, and
the underlying intervals overlap; they indicate direction and rough magnitude only (see the
caveat in §B.3).
Prior conclusion refined: the frontier judge does not simply inflate everything; it inflates
**structured, benchmark-style questions** where there are clear anchors to distinguish, and
behaves more like System One on open-ended synthesis questions.

## B.5 Position stability — and a judge that contradicts itself

Two definitions of "winner" are available here, and they differ. The judge returns a declared
`winner` field *and* six per-dimension scores from which a weighted composite is derived. Both
are reported:

| Definition | Winner stable | Flips |
|---|---|---|
| Declared `winner` field | **8/10** | DEEP-001, DEEP-003 |
| Weighted composite | **7/10** | DEEP-001, DEEP-003, DEEP-005 |

Score drift between orders: grok 0.110 (K) / 0.165 (D), max **0.700**; Jev ≈0.01–0.03, max 0.032.

Under the declared-winner definition, both flips moved from default winning to Keenable winning,
i.e. the **candidate in the second position won in each ordering**:

| Query | Order A=K, B=D | Order A=D, B=K | Declared winner |
|---|---|---|---|
| DEEP-001 | **D** wins (1.400 / 1.800) | **K** wins (1.500 / 1.100) | position B |
| DEEP-003 | **D** wins (1.400 / 1.650) | **K** wins (1.600 / 1.450) | position B |

Two flips is thin evidence, so this is stated as a **suggestive position-B tendency, not an
established bias**: both observed flips favoured the second-shown candidate, and both occurred
where the true difference is small (Jev |Δ| = 0.085 and 0.064, the two smallest in the DEEP set).
On DEEP-001 the incumbent's score moved **0.700** between orders (1.800 → 1.100) while the
challenger moved 0.100 — an asymmetry far larger than any effect being measured.

**DEEP-005 is a separate and more useful defect.** The judge scored Keenable 1.400 vs default
1.250 — a composite margin of +0.15 in the challenger's favour — yet **declared the default engine
the winner**. The stated verdict contradicts the judge's own scores. This is a reminder that a
frontier judge's headline verdict is a holistic judgement, not a derivation from its rubric
outputs, and the two must be cross-checked before either is quoted.

**Operational consequence:** a single-pass frontier judgement of a close comparison is unreliable. Winner stability (8/10 declared, 7/10 by composite) is high enough to trust the direction on clear-cut questions, but the 0.700 worst-case score drift means the magnitudes, and any verdict on a near-tie, should not be quoted without both presentation orders — and should be cross-checked against the IDPS layer, which was stable 10/10 on the same pairs.

## B.6 Where the layers agree and disagree, by dimension

Mean score per dimension over all ten pairs (Keenable / default):

| Dimension | grok Δ | Jev Δ | Reading |
|---|---|---|---|
| `analytical_depth` | **+0.50** | +0.31 | **both: Keenable** — the durable finding |
| `query_understanding` | +0.45 | +0.17 | both: Keenable |
| `recency_freshness` | **+0.60** | **+0.04** | **irreconcilable** |
| `structured_extractability` | +0.05 | +0.12 | both: near-parity on the full set |
| `source_authority` | +0.05 | +0.23 | both: small Keenable edge |
| `relevance_precision` | +0.05 | +0.04 | both: parity |

Two things stand out:

1. **`analytical_depth` is the only dimension where both judges find a large, same-signed
   effect.** This is the defensible core: the challenger disaggregates where the incumbent
   generalises. Every layer agrees.
2. **`recency_freshness` remains irreconcilable** — grok +0.60, Jev +0.04. And
   `recency_freshness` is Jev's lowest-confidence dimension across all 20 evaluations
   (mean confidence **0.483**; 10 of 20 evaluations escalated below the 0.70 floor). The
   dimension the judges fight over is precisely the one System One says it cannot read
   confidently from summarised evidence.

Note also that `structured_extractability` collapses to near-parity (+0.05) once deep-research
queries are included, whereas on the consulting five alone it was +0.30. The Keenable
"lift-ready tables" advantage is concentrated in the consulting categories, not universal.

## B.7 Net effect on the report's conclusions

| Body conclusion | After all three layers |
|---|---|
| Keenable wins overall | **Upheld**, but mostly by the consulting categories (9/10 IDPS wins) |
| Advantage is large and general | **Revised.** Consulting: 9.7% of scale. Deep research: 5.5%, with 1 win, 1 loss, 3 splits |
| Recency is the biggest differentiator | **Rejected.** Both judges put recency at or near zero effect in aggregate (Jev +0.04) |
| Depth/granularity is the advantage | **Reinforced and promoted to the headline finding** (+0.31 Jev / +0.50 grok) |
| Deep Research is a 4.2 / 4.2 tie | **Rejected.** It concealed a clear win (DEEP-002) and a clear loss (DEEP-001) |
| Source authority is a tie | **Narrowed to "small Keenable edge"** (Jev +0.23, grok +0.05) |

## B.8 Limitations

- **n=10 pairs, but NOT 5 per category.** Five pairs are *single exemplars* from five different
  consulting categories, plus five deep-research queries. There is no within-category replication
  anywhere except deep research: a "category" label on a consulting row means one query.
- Differences below ~0.10 on the 0–2 scale are treated as no difference. At that floor the Jev
  consulting tally is 3/5, not 5/5.
- **The layers are not independent instruments.** Layer 1 (body) scored *raw result sets
  unblinded*, and its model is unnamed. Layers 2 and 3 scored *blind evidence cards*. So L2 and
  L3 share a summarisation step (a card-writing bias affects both identically and is invisible
  here), while L1 and L3 may be the same model family. Agreement is reported as agreement, not
  as validation by independent instruments.
- One frontier model only. The polarisation multiple and the two observed position flips are
  measured facts about `grok-4.6`, not about frontier judges in general. Two flips is n=2.
- Prompt sensitivity, temperature effects and rubric-anchor wording were not ablated.
- Query strings: consulting queries ran at `limit=10` **except FIN-001 at `limit=5`** (a protocol
  deviation; excluded from slice means); DEEP queries all at `limit=10`.

## B.9 Reproducing

```bash
cd ~/Projects/search-benchmark
python3 scripts/run_judge_layer.py      # 20 calls, cached/resumable, parallel-safe
python3 scripts/three_way.py            # consolidated three-way + agreement + stability
# artefacts: evaluation/judge/judge_<q>_<AB|BA>.json, evaluation/judge/summary.json,
#            evaluation/three_way.json
```
