# Scripts (placeholders)

Phase 0: public fetch stubs and paper helpers only. **No order submit.**

## Planned stubs (not wired to keys)

- `fetch_polymarket_us_public.py` — read-only calls to `gateway.polymarket.us`
- `fetch_novig_public.py` — read-only catalog / `data.novig.com` CSV helpers
- `paper_log_append.py` — append CSV/JSONL rows per `docs/paper-log-schema.md`
- `trade_card_validate.py` — schema check for `schemas/trade-card.md` fields
- `math_devig_ev.py` — deterministic de-vig / EV / fee math unit-tested

## Explicitly out of scope here

- Live order placement
- Blind retry on Novig 201-queued
- Secret loading or `.env` commits
