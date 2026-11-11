"""Offline tests: no network, no API keys.

They cover the three places this harness has actually produced wrong numbers:
composite arithmetic, per-query aggregation that hides a mixed category, and the
provenance guard that stops a failed engine call becoming another engine's data.
"""
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bench.aggregate import slice_by_category, summarise  # noqa: E402
from bench.cards import TIER1, build_card, precomputed_facts  # noqa: E402
from bench.judge import composite  # noqa: E402
from bench.providers import BackendError, Hit, Result, search  # noqa: E402

DIMS = [
    {"key": "relevance_precision", "weight": 2.5, "anchors": ["a", "b", "c"]},
    {"key": "source_authority", "weight": 2.0, "anchors": ["a", "b", "c"]},
    {"key": "analytical_depth", "weight": 2.0, "anchors": ["a", "b", "c"]},
    {"key": "recency_freshness", "weight": 1.5, "anchors": ["a", "b", "c"]},
    {"key": "structured_extractability", "weight": 1.0, "anchors": ["a", "b", "c"]},
    {"key": "query_understanding", "weight": 1.0, "anchors": ["a", "b", "c"]},
]
KEYS = [d["key"] for d in DIMS]


def _res(engine, domains, q="q", limit=10):
    return Result(engine=engine, query=q, limit=limit,
                  hits=[Hit(url=f"https://{d}/x", title=f"{d} title", snippet="snip", rank=i + 1)
                        for i, d in enumerate(domains)],
                  served_by=engine, keyless=(engine == "keenable"))


# --------------------------------------------------------------------------- #
def test_composite_is_weighted_mean_on_0_2():
    scores = {k: 2 for k in KEYS}
    assert composite(scores, DIMS) == pytest.approx(2.0)
    scores = {k: 0 for k in KEYS}
    assert composite(scores, DIMS) == pytest.approx(0.0)
    # weights sum to 10; a dimension maxed at 2 contributes 2*weight/10
    scores = {k: 0 for k in KEYS}
    scores["relevance_precision"] = 2
    assert composite(scores, DIMS) == pytest.approx(2 * 2.5 / 10)


def test_composite_ignores_unweighted_extra_keys():
    scores = {k: 1 for k in KEYS}
    scores["not_a_dimension"] = 2
    assert composite(scores, DIMS) == pytest.approx(1.0)


# --------------------------------------------------------------------------- #
def test_unknown_engine_raises():
    with pytest.raises(ValueError):
        search("nope", "q")


def test_exa_without_key_raises_rather_than_falling_back(monkeypatch):
    monkeypatch.delenv("EXA_API_KEY", raising=False)
    with pytest.raises(BackendError) as e:
        search("exa", "q")
    assert "EXA_API_KEY" in str(e.value)


# --------------------------------------------------------------------------- #
def test_precomputed_facts_counts_tier1_and_repeats():
    r = _res("keenable", ["nist.gov", "nist.gov", "someblog.example", "arxiv.org"])
    f = precomputed_facts(r)
    assert f["n_results"] == 4
    assert f["distinct_domains"] == 3
    assert f["repeat_publishers"] == {"nist.gov": 2}
    assert f["tier1_count"] == 3          # nist x2 + arxiv
    assert "nist.gov" in f["tier1_domains"]


def test_tier1_matching_accepts_subdomains():
    r = _res("keenable", ["nvlpubs.nist.gov"])
    assert precomputed_facts(r)["tier1_count"] == 1


def test_card_is_anonymised():
    r = _res("keenable", ["nist.gov"])
    for side in ("A", "B"):
        card = build_card(r, side)
        assert "keenable" not in card.lower()
        assert "exa" not in card.lower()
        assert "PRE-COMPUTED FACTS" in card


def test_card_respects_char_ceiling():
    from bench.cards import write_cards
    import tempfile
    big = _res("keenable", [f"d{i}.example" for i in range(40)])
    big.hits = [Hit(url=h.url, title="t" * 200, snippet="s" * 900, rank=h.rank) for h in big.hits]
    with tempfile.TemporaryDirectory() as td:
        paths = write_cards({"Q1": {"A": big, "B": big}}, Path(td), max_chars=5000)
        for p in paths:
            assert len(p.read_text()) <= 5000 + 80


# --------------------------------------------------------------------------- #
def _pair(leader_a_rows, leader_b_rows, keys=KEYS):
    """Build a fake judge_pair() output for N queries."""
    judged, cats = {}, {}
    for i, (la, lb) in enumerate(zip(leader_a_rows, leader_b_rows)):
        qid = f"Q{i}"
        cats[qid] = "cat"
        judged[qid] = {
            "mean_composite": {"keenable": la, "exa": lb},
            "winner_stable": True,
            "score_drift": {"keenable": 0.01, "exa": 0.02},
            "orders": {
                "AB": {"declared_winner_engine": "keenable" if la > lb else "exa",
                       "scores": {e: {k: 1 for k in keys} for e in ("keenable", "exa")}},
                "BA": {"declared_winner_engine": "keenable" if la > lb else "exa",
                       "scores": {e: {k: 1 for k in keys} for e in ("keenable", "exa")}},
            },
        }
    return judged, cats


def test_summary_counts_leaders_per_query_not_by_mean():
    judged, cats = _pair([1.9, 1.0], [1.0, 1.9])
    s = summarise(judged, DIMS)
    assert s["n"] == 2
    assert s["leader_counts"] == {"keenable": 1, "exa": 1}
    # the two means are tied, which must NOT be reported as a win for either
    assert math.isclose(s["mean_composite"]["keenable"], s["mean_composite"]["exa"])


def test_category_flags_mixed_winners():
    judged, cats = _pair([1.9, 1.0], [1.0, 1.9])
    s = summarise(judged, DIMS)
    cats_ = slice_by_category(s, cats)
    assert cats_["cat"]["mixed"] is True
    assert cats_["cat"]["leaders"] == {"keenable": 1, "exa": 1}


def test_category_not_mixed_when_one_engine_sweeps():
    judged, cats = _pair([1.9, 1.8], [1.0, 1.1])
    s = summarise(judged, DIMS)
    cats_ = slice_by_category(s, cats)
    assert cats_["cat"]["mixed"] is False
    assert cats_["cat"]["leaders"]["keenable"] == 2