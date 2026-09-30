# Prediction Desk

Tim Moulton's prediction-market desk seat (Grok Bot org). Research, paper logging, and Tim-approve trade cards for **Polymarket US** and **Novig**. Not financial advice. Not legal advice.

## Locked scope

- New risk venues: Polymarket US (`gateway.polymarket.us`) and Novig only
- Kalshi sports/politics: out while Washington court block holds
- International Polymarket (`polymarket.com`): close-only, no new risk
- Every live order requires Tim's explicit yes in chat (one order per yes)
- Keys via Grok Bot secret form later; never commit secrets here

## Attention rank

CalmBinderPress > Website Landlord > this desk

## Org (proposed)

- Department head: existing Prediction Desk seat `c219d0bb-cfbf-46dd-9d8c-1cdec41ec205`
- Reports to Chief `b78ecace-0af3-4c84-b7ff-31b5bc23f1c9` (proposed). Live line may still be Business Manager until Tim + HR move it.
- Business Manager is a peer department, not owner of this desk.

## Notion merged proposal

https://app.notion.com/p/3e755ddfbc9f81518c1cffa765fab588

## Repo

https://github.com/tmoulton-12345/Prediction-Desk

## This repo

Paper schemas, ops notes, and read-only public-fetch stubs only. No live auto-submit trading code. No secrets.

## NFL paper log (Phase 0)

`scripts/nfl_paper_log.py` scores an NFL paper slate: contract key, fee, de-vigged `p_market`, hit, P/L, Brier, log loss, and CLV when a same-contract close is on file. Stake is a flat `$20`. The script does not submit an order, does not load keys, and does not fetch a scoreboard. CFB, MLB, and CBB are rejected. Field list: `docs/paper-log-schema.md`.

### Score one settled week

Week 3 top-5 locks are `fixtures/nfl/week3-top5-locks.json`. Finals are the ESPN public scoreboard read frozen on 2026-09-30 in `fixtures/nfl/week3-top5-finals.json` (`STATUS_FINAL`, four quarters, no overtime). No close snapshot was stored for that ledger.

```bash
python3 scripts/nfl_paper_log.py week \
  --locks fixtures/nfl/week3-top5-locks.json \
  --finals fixtures/nfl/week3-top5-finals.json \
  --out data/paper/nfl-week3-top5.jsonl \
  --csv data/paper/nfl-week3-top5.csv \
  --scorecard data/paper/nfl-week3-top5-scorecard.md
```

That run grades **2 wins, 3 losses, -$23.64 on $100.00** at -110, completeness 100% because every row is explicitly `close missing`, and mean CLV blank (`n=0`). Market Brier is 0.25 because the devigged `-110/-110` price is 0.5. A worked copy of that scorecard is `data/paper/nfl-week3-top5-scorecard.md`.

### Next NFL slate

1. Copy the Week 3 locks file. Set `week`, `decision_time` (ISO-8601 with offset), `kick_time_pt`, and one object per ticket. `american_odds` is the price you logged. The script computes the fee, `p_market`, Brier, and `ev_usd`.
2. Set `venue` to `polymarket_us` or `novig` when that quote is the one on the ticket. `paper_ledger` is only the historical flat `-110` ledger. Favorites carry a minus on `line` (`-7.5`). A `+3` and a `-3` are different contracts. So are `7.5` and `8`.
3. Before kickoff, write the rows without a grade:

```bash
python3 scripts/nfl_paper_log.py ingest \
  --locks fixtures/nfl/weekN-locks.json \
  --out data/paper/nfl-weekN.jsonl
```

4. For a close, save a JSON object per ticket with the same `market_type`, `side`, `line`, and `period`, plus `close_american` and `close_american_other`. Pass it as `--closes`. A snapshot on a different line is flagged and is not used as CLV.
5. After the game is final, put `away_score`, `home_score`, and `status: STATUS_FINAL` in a finals file (include `overtime: true` when the linescore has an overtime period). The logger grades the numbers in that file. It does not call ESPN.

```bash
python3 scripts/nfl_paper_log.py week \
  --locks fixtures/nfl/weekN-locks.json \
  --finals fixtures/nfl/weekN-finals.json \
  --closes fixtures/nfl/weekN-closes.json \
  --out data/paper/nfl-weekN.jsonl \
  --csv data/paper/nfl-weekN.csv \
  --scorecard data/paper/nfl-weekN-scorecard.md
```

Omit `--closes` when the close was not captured. `week` then stamps `close missing` on every row. Reprint a saved log with `scorecard --log data/paper/nfl-weekN.jsonl`.

The scorecard prints n, completeness, contract mismatches, mean CLV (with n and a standard error), market Brier, the 0.5 Brier floor, log loss, hit rate, paper P/L, and the quarter-Kelly shadow. At -110 the break-even hit rate is 110/210, about 52.38%. The card is a description of the logged tickets.

Re-check fees on the day of a card. Polymarket US standard taker theta `0.0695` is the 2026-09-29 read of `https://docs.polymarket.us/fees`. Novig pregame straights are 0 under charge mode `WHEN_LIVE`; live straights use `0.03` (`https://support.novig.com/en/articles/16195057-fees-on-novig`). Those constants are named in `scripts/math_fees_arb.py`.

```bash
python3 -m unittest discover -s scripts -p 'test_*.py'
```
