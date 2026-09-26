"""Read-only Polymarket US public gateway calls.

GET only. No order, cancel, or account routes.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

GATEWAY = "https://gateway.polymarket.us"
USER_AGENT = "PredictionDeskPhase0/1.0 (public read)"


def get_json(url: str, timeout: float = 120.0, attempts: int = 4) -> dict:
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    delay = 1.0
    last_error: Exception | None = None
    for _ in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code != 429:
                body = exc.read().decode("utf-8", errors="replace")[:400]
                raise RuntimeError(f"Polymarket US GET {url} -> {exc.code}: {body}") from exc
            retry_after = exc.headers.get("Retry-After")
            time.sleep(float(retry_after) if retry_after else delay)
            delay = min(delay * 2, 30.0)
        except urllib.error.URLError as exc:
            last_error = exc
            time.sleep(delay)
            delay = min(delay * 2, 30.0)
    raise RuntimeError(f"Polymarket US GET failed: {url}") from last_error


def fetch_nfl_events(limit: int = 100) -> dict:
    return get_json(f"{GATEWAY}/v2/leagues/nfl/events?limit={limit}")


def fetch_market_book(slug: str) -> dict:
    return get_json(f"{GATEWAY}/v1/markets/{slug}/book", timeout=30.0)
