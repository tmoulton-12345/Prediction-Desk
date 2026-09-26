# AGENTS.md — Cursor / cloud build brief

## Hard rules

1. Paper first. Public reads and paper logs before any live keys.
2. No auto-submit. No unsupervised order loops. No market-order auto fire.
3. No secrets in this repo (no `.env`, API keys, session cookies, private keys).
4. Tim-approve every live trade. One explicit yes per order.
5. Deterministic quant (odds, EV, fees, de-vig, arb math) belongs in code, not LLM prose.
6. Jev (`typesafe/jev-1.13`) is a typed completeness / risk / reversibility gate after packed state. Not a sports oracle. Not a sole trade picker.
7. Cursor cloud is an engineering bench (connectors, tests, PRs), not a production executor.
8. Venues for new risk: Polymarket US + Novig only. Kalshi sports/politics out. International Polymarket close-only.
9. Novig QA: HTTP 201 queued is not filled. No blind retry.
10. Attention: CalmBinderPress > Website Landlord > this desk.

## Allowed in Phase 0

- Public fetch stubs
- Paper log writers (CSV/JSONL)
- Trade-card validators (schema only)
- Unit tests for fee/de-vig/arb math
- Docs and schemas

## Forbidden

- Live order submit modules wired to keys
- Withdraw / management key handling in code paths used by agents
- VPN / geo-spoof helpers
- CreateAgent or org changes from this repo
