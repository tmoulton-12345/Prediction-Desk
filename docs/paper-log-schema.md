# Paper log schema

Append-only. One row per decision, including holds.

## CSV / JSONL fields

| Field | Type | Notes |
| --- | --- | --- |
| `ts` | ISO-8601 datetime | Prefer America/Los_Angeles offset or `Z` with explicit zone |
| `venue` | string | `polymarket_us` or `novig` |
| `market_id` | string | Venue market id |
| `side` | string | Yes/No or named outcome |
| `price` | number | Limit or reference price used |
| `fee_assumed` | number | Fee used in EV snapshot that day |
| `size_paper` | number | Paper size in stated unit |
| `reason` | string | One sentence; events + price, not "Jev said so" |
| `settlement_later` | string/null | Filled after resolution |
| `sources` | string | Semicolon-separated URLs or source ids |
| `decision` | string | `propose` / `hold` / `refuse` / `tim_approved` / `tim_rejected` (optional extension) |
| `trade_card_id` | string/null | Links to immutable ticket |
| `counter_case` | string/null | Skeptic note |
| `jev_shadow` | string/null | Optional Jev shadow output |
| `clv` | number/null | Closing line value when known |
| `brier` | number/null | After settlement when binary forecast logged |
| `log_loss` | number/null | After settlement when probability logged |

## Example JSONL

```json
{"ts":"2026-09-25T19:21:00-07:00","venue":"novig","market_id":"example","side":"Yes","price":0.42,"fee_assumed":0.01,"size_paper":10,"reason":"Paper dry-run only","settlement_later":null,"sources":"https://data.novig.com","decision":"hold"}
```
