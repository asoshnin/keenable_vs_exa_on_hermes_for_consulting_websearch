"""Blind multi-criteria judging by an LLM, run in BOTH presentation orders.

Why both orders: an LLM judge asked to compare A and B has a measurable position
preference. Running the same pair with the candidates swapped turns an invisible
bias into an observable one — if the winner changes, the comparison is not
trustworthy for that pair, and the report says so instead of quoting a number.

The judge is any OpenAI-compatible chat-completions endpoint, so this works with
OpenAI, Azure OpenAI/Foundry, OpenRouter, vLLM, Ollama, LM Studio, etc.
"""
from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from typing import Any

import requests

from .cards import build_card
from .providers import Result

DEFAULT_RUBRIC_KEYS = [
    "relevance_precision", "source_authority", "analytical_depth",
    "recency_freshness", "structured_extractability", "query_understanding",
]


@dataclass
class JudgeConfig:
    base_url: str
    api_key: str
    model: str
    temperature: float = 0.0
    timeout: int = 300
    retries: int = 3

    @classmethod
    def from_env(cls) -> "JudgeConfig":
        base = os.environ.get("JUDGE_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        key = os.environ.get("JUDGE_API_KEY", "")
        model = os.environ.get("JUDGE_MODEL", "")
        if not model:
            raise RuntimeError("JUDGE_MODEL is not set (e.g. gpt-4o, grok-4, claude-sonnet-4).")
        if not key and "localhost" not in base and "127.0.0.1" not in base:
            raise RuntimeError("JUDGE_API_KEY is not set.")
        return cls(base_url=base, api_key=key, model=model,
                   temperature=float(os.environ.get("JUDGE_TEMPERATURE", "0")))


def build_prompt(query: str, card_a: str, card_b: str, dims: list[dict]) -> str:
    """Assemble the judge prompt.

    NOTE: uses .replace(), not str.format() — the literal JSON schema below would
    otherwise be parsed as format fields and raise KeyError.
    """
    blocks = []
    for d in dims:
        anchors = "\n".join(f"     {i} = {a}" for i, a in enumerate(d["anchors"]))
        blocks.append(f"  {d['key']} — {d['question'].strip()}\n{anchors}")
    rubric = "\n\n".join(blocks)
    schema_keys = ",".join(
        f'"{d["key"]}":{{"A":<0|1|2>,"B":<0|1|2>}}' for d in dims
    )
    prompt = """You are an independent, blind evaluator of web-search result quality. A professional
research team is choosing between two search engines. You will be shown two anonymised result
sets, CANDIDATE A and CANDIDATE B, returned by two different engines for the SAME query.

You do not know which engine produced which. Judge ONLY from the material shown. Do not reward
or punish length. Do not assume either candidate is better.

Score EACH candidate on each dimension using this ordinal scale (integers only):
  0 = worst anchor, 1 = middle anchor, 2 = best anchor

DIMENSIONS AND ANCHORS:

__RUBRIC__

Return ONLY a single JSON object. No prose before or after. No markdown code fences.
Exact schema:
{__SCHEMA__,"winner":"A"|"B"|"tie","rationale":"<one sentence>"}

QUERY: __QUERY__

=== CANDIDATE A ===
__CARD_A__
=== END CANDIDATE A ===

=== CANDIDATE B ===
__CARD_B__
=== END CANDIDATE B ===

JSON:"""
    return (prompt
            .replace("__RUBRIC__", rubric)
            .replace("__SCHEMA__", schema_keys)
            .replace("__QUERY__", query)
            .replace("__CARD_A__", card_a)
            .replace("__CARD_B__", card_b))


def _parse(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError(f"no JSON object in model output: {text[:300]!r}")
    return json.loads(m.group(0))


def _call(cfg: JudgeConfig, prompt: str) -> dict:
    last = None
    for attempt in range(cfg.retries):
        try:
            r = requests.post(
                f"{cfg.base_url}/chat/completions",
                json={
                    "model": cfg.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": cfg.temperature,
                },
                headers={"Authorization": f"Bearer {cfg.api_key}",
                         "Content-Type": "application/json"},
                timeout=cfg.timeout,
            )
            if r.status_code >= 400:
                raise RuntimeError(f"HTTP {r.status_code}: {r.text[:300]}")
            content = r.json()["choices"][0]["message"]["content"]
            return _parse(content)
        except Exception as exc:  # noqa: BLE001 - retried, then surfaced
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"judge failed after {cfg.retries} attempts: {last}")


def _validate(v: dict, dims: list[dict]) -> None:
    for d in dims:
        for side in ("A", "B"):
            s = v[d["key"]][side]
            if not isinstance(s, int) or not 0 <= s <= 2:
                raise ValueError(f"{d['key']}.{side} = {s!r} is not an int in 0..2")
    if v.get("winner") not in ("A", "B", "tie"):
        raise ValueError(f"winner = {v.get('winner')!r} invalid")


def composite(scores: dict[str, int], dims: list[dict]) -> float:
    total = sum(d["weight"] for d in dims)
    return sum(scores[d["key"]] * d["weight"] for d in dims) / total


def judge_pair(cfg: JudgeConfig, query: str, a: Result, b: Result,
               dims: list[dict], sides: tuple[str, str] = ("keenable", "exa")) -> dict:
    """Judge one pair in both presentation orders.

    `sides` names the engine occupying positions (A, B) in the AB run. The BA run
    swaps them, so a position bias becomes visible as a winner flip.
    """
    card_a, card_b = build_card(a, "A"), build_card(b, "B")
    card_a_swapped, card_b_swapped = build_card(b, "A"), build_card(a, "B")

    out = {"query": query, "orders": {}}
    for order, ca, cb in (("AB", card_a, card_b), ("BA", card_a_swapped, card_b_swapped)):
        raw = _call(cfg, build_prompt(query, ca, cb, dims))
        _validate(raw, dims)
        # map positions back to engines
        pos_engine = {"AB": {"A": sides[0], "B": sides[1]},
                      "BA": {"A": sides[1], "B": sides[0]}}[order]
        per_engine = {
            eng: {d["key"]: raw[d["key"]][pos] for d in dims}
            for pos, eng in pos_engine.items()
        }
        declared = raw["winner"]
        out["orders"][order] = {
            "raw": raw,
            "scores": per_engine,
            "composites": {e: composite(s, dims) for e, s in per_engine.items()},
            "declared_winner_engine": pos_engine[declared] if declared in ("A", "B") else "tie",
        }

    ab, ba = out["orders"]["AB"], out["orders"]["BA"]
    out["winner_stable"] = ab["declared_winner_engine"] == ba["declared_winner_engine"]
    out["mean_composite"] = {
        e: (ab["composites"][e] + ba["composites"][e]) / 2 for e in (sides[0], sides[1])
    }
    out["score_drift"] = {
        e: abs(ab["composites"][e] - ba["composites"][e]) for e in (sides[0], sides[1])
    }
    out["declared_consistent_with_composite"] = {
        order: (
            (o["declared_winner_engine"] == "tie")
            or (o["composites"][o["declared_winner_engine"]]
                >= max(o["composites"].values()) - 1e-9)
        )
        for order, o in out["orders"].items()
    }
    return out