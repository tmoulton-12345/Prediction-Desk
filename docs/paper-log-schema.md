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

NFL paper-log v1 (`scripts/nfl_paper_log.py`, `schema_version` `nfl-paper-log-v1`) extends this row. The base names stay populated: `ts` = `decision_time`, `price` = `open_price`, `fee_assumed` = `fee_used`, `size_paper` = `stake`, `settlement_later` = `settlement_notes`. Jev is not called.

## Example JSONL

```json
{"ts":"2026-09-25T19:21:00-07:00","venue":"novig","market_id":"example","side":"Yes","price":0.42,"fee_assumed":0.01,"size_paper":10,"reason":"Paper dry-run only","settlement_later":null,"sources":"https://data.novig.com","decision":"hold"}
```

## NFL paper-log v1

One derived row per NFL paper ticket. The locks file is the record. JSONL and CSV are regenerated from it. Sport is `NFL`. Stake is the flat paper unit `$20`. `quarter_kelly_shadow` is computed only when `p_model` is on the lock, and it does not change `stake`.

| Field | Notes |
| --- | --- |
| `sport` | `NFL` |
| `week` | NFL week number |
| `event` | `AWAY @ HOME` |
| `kick_time_pt` | ISO-8601 with a numeric offset |
| `market_type` | `spread`, `total`, or `ml` |
| `side` | Team abbreviation, or `over` / `under` |
| `line` | Signed spread (`-7.5`, `+3`), total points, or `ML` |
| `period` | `FG` is the only period v1 grades. `1H` stays open |
| `venue` | `polymarket_us`, `novig`, or `paper_ledger` |
| `american_odds` | Logged American price. Code does not invent one |
| `stake` | `20` |
| `open_price` | Raw implied probability of `american_odds`, vig still inside |
| `close_price` | Raw implied probability of the close. Null when the close is missing |
| `close_status` | `ok` or `close missing`. Null until a settled run stamps it |
| `p_market` | Devigged probability of the side. `devig_method` is `basic` or `shin` |
| `p_basic`, `p_shin` | Both methods, stored on every two-way row |
| `fee_method`, `fee_coeff`, `fee_used` | See the fee table below |
| `same_contract_key` | `nfl\|week=3\|event=SEA@WAS\|market=spread\|side=SEA\|line=-7.5\|period=FG` |
| `same_contract_mismatch` | True when a compare quote or a close snapshot differs in event, market, side, line, or period |
| `hit` | `hit`, `miss`, `push`. Blank while the game is open |
| `pnl` | `paper_grade.settle` at the logged American price and `$20` |
| `clv` | Devigged close probability of the side, minus `p_market`. Positive means the ticket beat the close |
| `brier` | `(p_market - y)^2` on wins and losses. Pushes are omitted |
| `log_loss` | Natural log, `p` clipped to `[1e-15, 1 - 1e-15]` |
| `settlement_notes` | Final score, margin, overtime flag, decision-time note |
| `decision_time` | ISO-8601 |
| `ev_usd` | Expectation under `p_market` at the logged American price, minus `fee_used` |
| `quarter_kelly_shadow` | `0.25 * (p_model - (1 - p_model) / b)`. Blank when `p_model` is blank |

A spread or total with no `american_odds_other` de-vigs as if the other side were the same American price (`devig_other_side` = `symmetric_same_american`). A moneyline requires the other side.

`paper_ledger` is the historical flat `-110` desk ledger (the Week 3 top-5). It is not a Polymarket US or Novig fill. New quotes use `polymarket_us` or `novig`.

### Fee methods

Coefficients live in `scripts/math_fees_arb.py`. Re-check the venue page on the day of a card. The 2026-09-29 read is:

| `fee_method` | Coefficient | Formula |
| --- | --- | --- |
| `polymarket_us_taker_v20260925` | theta `0.0695` | Banker's cent round of `theta * contracts * p * (1 - p)`, `contracts = stake / open_price`. Source: `https://docs.polymarket.us/fees` (US schedule from 2026-09-25 00:00 ET). |
| `novig_straight_taker_v20260929` | live straight `0.03`; pregame straight `0` | `novig_taker_fee_per_dollar` with charge mode `WHEN_LIVE`. `OPEN_PREGAME` charges 0. `OPEN_INGAME` charges `0.03`. Futures `0.06` is not used on these game tickets. Source: `https://support.novig.com/en/articles/16195057-fees-on-novig`. |
| `american_hold_in_odds` | `0` | `paper_ledger` only. The hold is removed by de-vig. |

`pnl` uses the American settlement. `fee_used` is the taker snapshot beside it.

### De-vig

`scripts/devig.py`. Basic divides each implied probability by the sum. Shin uses the two-outcome closed form and the n-outcome fixed point from `mberk/shin` (Shin 1993). `p_market` follows `devig_method`. The Week 3 ledger uses `basic`. On a symmetric `-110/-110` book both methods are `0.5`.

### Close snapshot

Each close object names `ticket_id`, `market_type`, `side`, `line`, and `period`, plus `close_american` and `close_american_other` (or `close_implied` and `close_implied_other`). A different line is a mismatch: CLV stays blank and `close_status` is `close missing`. Omitting the closes file on `week` stamps every row `close missing`.
