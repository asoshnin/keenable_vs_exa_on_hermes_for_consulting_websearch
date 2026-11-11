"""Build blind evidence cards from captured results.

A card is what a judge sees. It deliberately contains:
  * the query and category (so the judge knows the task),
  * a PRE-COMPUTED FACTS block (counts produced by code, not estimated by a model),
  * every returned hit as `domain — title — snippet`.

It deliberately does NOT contain the engine name. That is what makes the judging
blind. Cards are written as `{query_id}_{A|B}.txt`, A = challenger, B = incumbent.
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Iterable

from .providers import Result

# Domains treated as tier-1 primary/authoritative sources. Deliberately
# conservative and public: regulators, statistical agencies, peer-reviewed
# publishers, Big-4 / strategy firms, named M&A advisors.
TIER1 = {
    # regulators / official
    "europa.eu", "ec.europa.eu", "eur-lex.europa.eu", "consilium.europa.eu",
    "eba.europa.eu", "esma.europa.eu", "eiopa.europa.eu", "ecb.europa.eu",
    "nist.gov", "nvlpubs.nist.gov", "csrc.nist.gov", "nccoe.nist.gov",
    "ncsc.gov.uk", "cisa.gov", "bsi.bund.de", "bafin.de", "sec.gov",
    "ftc.gov", "cma.gov.uk", "pcaobus.org", "oecd.org", "imf.org", "bis.org",
    "worldbank.org", "documents1.worldbank.org", "iea.org", "irena.org",
    "europarl.europa.eu", "efrag.org",
    # statistics
    "statista.com", "eurostat.ec.europa.eu",
    # peer-reviewed / academic
    "arxiv.org", "nature.com", "sciencedirect.com", "link.springer.com",
    "pubs.rsc.org", "onlinelibrary.wiley.com", "europepmc.org", "doi.org",
    "ssrn.com", "nber.org", "jstor.org",
    # strategy / Big 4 / advisors
    "mckinsey.com", "bcg.com", "bain.com", "deloitte.com", "kpmg.com",
    "pwc.com", "ey.com", "accenture.com", "oliverwyman.com",
    "gartner.com", "idc.com", "forrester.com",
    "solganick.com", "lincolninternational.com", "aventis-advisors.com",
    "equiteq.com", "clairfield.com", "bdo.de", "cogentvaluation.com",
    "spglobal.com", "pitchbook.com", "preqin.com", "mergermarket.com",
}

YEAR_RE = re.compile(r"\b(20[2-4]\d)\b")
NUM_RE = re.compile(r"\d[\d.,]*\s*(?:%|x\b|USD|EUR|GBP|\$|bn\b|B\b|M\b|GW|GW/yr|kg|ms)")


def _domain(url: str) -> str:
    return url.replace("https://", "").replace("http://", "").split("/")[0].lower()


def _is_tier1(dom: str) -> bool:
    return any(dom == d or dom.endswith("." + d) for d in TIER1)


def precomputed_facts(result: Result) -> dict:
    doms = result.domains()
    t1 = sorted({d for d in doms if _is_tier1(d)})
    text = " ".join(f"{h.title} {h.snippet}" for h in result.hits)
    years = Counter(y for y in YEAR_RE.findall(text))
    return {
        "n_results": len(result.hits),
        "distinct_domains": len(set(doms)),
        "repeat_publishers": {d: n for d, n in Counter(doms).items() if n > 1},
        "tier1_count": sum(1 for d in doms if _is_tier1(d)),
        "tier1_domains": t1,
        "year_mentions": dict(sorted(years.items())),
        "numeric_mentions": len(NUM_RE.findall(text)),
    }


def build_card(result: Result, side: str) -> str:
    f = precomputed_facts(result)
    rep = f["repeat_publishers"]
    lines = [
        "ENGINE RESULT SET — CANDIDATE (blind)",
        f'Query: "{result.query}"',
        f"Retrieved: {f['n_results']} results (requested limit {result.limit}).",
        "",
        "PRE-COMPUTED FACTS (counted programmatically from the result set, not estimated):",
        f"- Distinct domains this result set draws on: {f['distinct_domains']} of {f['n_results']} results",
        f"- Results from tier-1 / primary-source domains (regulators, statistical agencies, "
        f"peer-reviewed, Big 4 / strategy firms): {f['tier1_count']} of {f['n_results']}",
        f"- Tier-1 domains present: {', '.join(f['tier1_domains']) if f['tier1_domains'] else 'none'}",
        f"- Repeat publishers (same domain more than once): "
        f"{', '.join(f'{d}\u00d7{n}' for d, n in rep.items()) if rep else 'none'}",
        f"- Explicit year mentions across titles and snippets: "
        f"{', '.join(f'{y}\u00d7{n}' for y, n in f['year_mentions'].items()) or 'none'}",
        f"- Numeric quantity mentions (%, multiples, currency, physical units): {f['numeric_mentions']}",
        "",
        "SOURCES RETURNED (domain — title — snippet as returned):",
    ]
    for h in result.hits:
        d = _domain(h.url)
        title = re.sub(r"\s+", " ", h.title).strip()[:120]
        snippet = re.sub(r"\s+", " ", h.snippet).strip()[:430]
        lines.append(f"{h.rank}. {d} — {title}")
        if snippet:
            lines.append(f"   {snippet}")
    return "\n".join(lines)


def write_cards(results: dict[str, dict[str, Result]], out_dir: Path,
                max_chars: int = 11000) -> list[Path]:
    """results: {query_id: {"A": Result, "B": Result}} -> card paths.

    `max_chars` guards a judge's input ceiling; cards that overflow are truncated
    on snippet length, never by dropping whole results.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for qid, sides in results.items():
        for side, res in sides.items():
            card = build_card(res, side)
            if len(card) > max_chars:
                card = card[:max_chars] + "\n[... card truncated to fit judge input ceiling ...]"
            p = out_dir / f"{qid}_{side}.txt"
            p.write_text(card)
            written.append(p)
    return written