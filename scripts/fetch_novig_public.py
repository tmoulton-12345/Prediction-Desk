"""Read-only Novig public v3 catalog calls.

GET https://api.novig.us/v3/public/catalog/... only.
No signed trading routes, no order placement.
"""

from __future__ import annotations

import json
import threading
import time
import urllib.error
import urllib.request

HOST = "https://api.novig.us"
USER_AGENT = "PredictionDeskPhase0/1.0 (public read)"


class RateLimit:
    def __init__(self, min_interval: float) -> None:
        self.min_interval = min_interval
        self._lock = threading.Lock()
        self._next = 0.0

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            if now < self._next:
                time.sleep(self._next - now)
                now = time.monotonic()
            self._next = now + self.min_interval


_BOOKS = RateLimit(0.28)


def get_json(url: str, timeout: float = 60.0, attempts: int = 6, paced: bool = False) -> dict:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
    )
    delay = 1.0
    last_error: Exception | None = None
    for _ in range(attempts):
        if paced:
            _BOOKS.wait()
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last_error = exc
            body = exc.read().decode("utf-8", errors="replace")[:400]
            if exc.code != 429:
                raise RuntimeError(f"Novig GET {url} -> {exc.code}: {body}") from exc
            retry_after = exc.headers.get("Retry-After")
            time.sleep(float(retry_after) if retry_after else delay)
            delay = min(delay * 2, 30.0)
        except urllib.error.URLError as exc:
            last_error = exc
            time.sleep(delay)
            delay = min(delay * 2, 30.0)
    raise RuntimeError(f"Novig GET failed: {url}") from last_error


def fetch_events(league: str, starts_after_ms: int, starts_before_ms: int, limit: int = 500) -> dict:
    url = (
        f"{HOST}/v3/public/catalog/events?league={league}"
        f"&startsAfter={starts_after_ms}&startsBefore={starts_before_ms}&limit={limit}"
    )
    return get_json(url)


def fetch_markets(
    league: str,
    market_types: str,
    starts_after_ms: int,
    starts_before_ms: int,
    limit: int = 5000,
) -> dict:
    url = (
        f"{HOST}/v3/public/catalog/markets?league={league}&marketType={market_types}"
        f"&startsAfter={starts_after_ms}&startsBefore={starts_before_ms}&limit={limit}"
    )
    return get_json(url)


def fetch_book(market_id: str) -> dict:
    return get_json(f"{HOST}/v3/public/catalog/markets/{market_id}/book", timeout=30.0, paced=True)
