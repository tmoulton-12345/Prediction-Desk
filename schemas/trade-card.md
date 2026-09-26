# Immutable Tim-approve trade card

Every proposed live order must show all fields below. One Tim yes per order. Then return to read-only.

1. Venue (Polymarket US or Novig)
2. Market id and/or URL and question text
3. Side (Yes/No or named outcome)
4. Size in dollars and in contracts (state the unit: Novig API ≈ 1¢ payout unit; Help Center often $1)
5. Order type (limit price or market) and expected fee that day
6. One-sentence reason (events + price, not "Jev said so")
7. Risks / rules caveat (settlement source, geo, age floor)
8. Forecast + interval (model or desk estimate; confidence is a process label)
9. Skeptic / counter-case
10. Fee assumed + de-vig / EV snapshot (from deterministic code when available)
11. Settlement / resolution source named
12. Arb gate fields if arb: same event, same line, OT/void rules, settlement match
13. Photo confirmation table if source was a photo list
14. Paper log id linking to append-only ledger row

Do not mutate a card after Tim sees it. If inputs change, mint a new card id.
