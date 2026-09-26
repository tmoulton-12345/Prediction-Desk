# Scripts (placeholders)

Phase 0: public fetch stubs and paper helpers only. **No order submit.**

## Read-only helpers

- `fetch_polymarket_us_public.py` — GET `gateway.polymarket.us` only
- `fetch_novig_public.py` — GET `api.novig.us/v3/public/catalog` only
- `math_fees_arb.py` — taker fee and round-trip cost. Tested by `test_math_fees_arb.py`
- `scan_nfl_week3_arb.py` — Week 3 NFL paper scan. Writes `research/` and `snapshots/`

Still not in this folder:

- `paper_log_append.py` — append CSV/JSONL rows per `docs/paper-log-schema.md`
- `trade_card_validate.py` — schema check for `schemas/trade-card.md` fields

## Explicitly out of scope here

- Live order placement
- Blind retry on Novig 201-queued
- Secret loading or `.env` commits
