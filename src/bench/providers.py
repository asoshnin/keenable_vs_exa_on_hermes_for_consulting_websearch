"""Direct HTTP clients for the two engines under test.

Deliberately dependency-light (only `requests`) so the benchmark runs anywhere
without the original tooling. Each backend returns a normalised list of hits and
carries explicit provenance metadata so a silently-degraded call cannot be
mistaken for a genuine one.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

import requests

KEENABLE_URL = os.environ.get("KEENABLE_API_URL", "https://api.keenable.ai")
EXA_URL = os.environ.get("EXA_API_URL", "https://api.exa.ai")
TIMEOUT = int(os.environ.get("BENCH_HTTP_TIMEOUT", "40"))


class BackendError(RuntimeError):
    """Raised when a backend fails. Never swallowed: a failed call must not
    silently become a different engine's result."""


@dataclass
class Hit:
    url: str
    title: str
    snippet: str
    rank: int


@dataclass
class Result:
    engine: str
    query: str
    limit: int
    hits: list[Hit]
    served_by: str
    keyless: bool
    meta: dict[str, Any] = field(default_factory=dict)

    def domains(self) -> list[str]:
        out = []
        for h in self.hits:
            d = h.url.replace("https://", "").replace("http://", "").split("/")[0].lower()
            out.append(d)
        return out


# --------------------------------------------------------------------------- #
# Keenable — independent index. Has an anonymous free tier, so it works with
# no credential at all; a key raises rate limits and guarantees service.
# --------------------------------------------------------------------------- #
def search_keenable(query: str, limit: int = 10, api_key: str | None = None) -> Result:
    api_key = api_key if api_key is not None else os.environ.get("KEENABLE_API_KEY", "")
    app_id = os.environ.get("KEENABLE_APP_ID", "search-benchmark")
    headers = {"X-Keenable-Title": app_id}
    if api_key:
        # Keyed tier: higher limits and a service guarantee.
        headers["X-API-Key"] = api_key
        url = f"{KEENABLE_URL}/v1/search"
    else:
        # Documented anonymous tier. Still Keenable's own index.
        url = f"{KEENABLE_URL}/v1/search/public"

    r = requests.post(
        url,
        json={"query": query, "max_results": int(limit)},
        headers=headers,
        timeout=TIMEOUT,
    )
    if r.status_code >= 400:
        raise BackendError(f"Keenable search failed: HTTP {r.status_code}: {r.text[:300]}")
    payload = r.json()
    raw = payload.get("results") or []
    hits = [
        Hit(
            url=x.get("url") or "",
            title=x.get("title") or "",
            snippet=x.get("snippet") or x.get("description") or "",
            rank=i + 1,
        )
        for i, x in enumerate(raw)
    ]
    return Result(
        engine="keenable",
        query=query,
        limit=limit,
        hits=hits,
        served_by="keenable",
        keyless=not bool(api_key),
        meta={"http_status": r.status_code},
    )


# --------------------------------------------------------------------------- #
# Exa — the incumbent side of this benchmark.
# --------------------------------------------------------------------------- #
def search_exa(query: str, limit: int = 10, api_key: str | None = None) -> Result:
    api_key = api_key if api_key is not None else os.environ.get("EXA_API_KEY", "")
    if not api_key:
        raise BackendError(
            "EXA_API_KEY is not set. The incumbent engine needs a credential; "
            "refusing to substitute a different engine silently."
        )
    r = requests.post(
        f"{EXA_URL}/search",
        json={
            "query": query,
            "numResults": int(limit),
            "contents": {"text": {"maxCharacters": 1200}},
        },
        headers={"x-api-key": api_key, "Content-Type": "application/json"},
        timeout=TIMEOUT,
    )
    if r.status_code >= 400:
        raise BackendError(f"Exa search failed: HTTP {r.status_code}: {r.text[:300]}")
    payload = r.json()
    raw = payload.get("results") or []
    hits = []
    for i, x in enumerate(raw):
        snippet = x.get("text") or " ".join(x.get("highlights") or []) or ""
        hits.append(
            Hit(url=x.get("url") or "", title=x.get("title") or "",
                snippet=snippet, rank=i + 1)
        )
    return Result(
        engine="exa", query=query, limit=limit, hits=hits,
        served_by="exa", keyless=False, meta={"http_status": r.status_code},
    )


BACKENDS = {"keenable": search_keenable, "exa": search_exa}


def search(engine: str, query: str, limit: int = 10, **kw) -> Result:
    if engine not in BACKENDS:
        raise ValueError(f"unknown engine {engine!r}; choose from {sorted(BACKENDS)}")
    return BACKENDS[engine](query, limit=limit, **kw)