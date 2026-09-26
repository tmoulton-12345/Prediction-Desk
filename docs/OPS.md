# Prediction Desk ops brief

**Owner:** Prediction Desk (department head). Reports to Chief (proposed). Live reporting may still be Business Manager until Tim + HR move the line. Business Manager is a peer, not owner.
**Seat id:** `c219d0bb-cfbf-46dd-9d8c-1cdec41ec205`
**Chief:** `b78ecace-0af3-4c84-b7ff-31b5bc23f1c9`
**Status:** Live seat. Read paths on. Trading keys not connected yet.
**HR ownership:** Durable profile owned by dr eggbot. Future creates go through HR.

## Locked scope (Tim 2026-09-25)

- Venues for new risk: **Polymarket US** and **Novig** only.
- Tim has small deposits on both and wants trading enabled with **Tim approving every trade**.
- Scope is any market on those venues (sports and non-sports), not sports-only.
- Capabilities: current events vs market prices; cross-venue compare / arb flags; recommendations from spreads, odds, or photo lists.
- Kalshi sports and politics: out while court block holds.
- International Polymarket (polymarket.com): no new risk (US close-only).

## Trade card (required before any order)

See `schemas/trade-card.md` for the expanded immutable ticket fields. Wait for Tim's explicit yes in that same chat. One order per yes. Then read-only again.

## Read paths (Phase 0)

- Polymarket US: `https://gateway.polymarket.us` (public)
- Novig: v3 public catalog; historical CSVs at `https://data.novig.com`

## Keys (later)

- Never paste into chat or commit to git.
- Tim loads via Grok Bot secure secret form when ready.
- Prefer read-only keys first. Trading key only when Tim wants API submit after approve.
- Management / withdraw keys stay offline. Prefer withdraw disabled / IP-bound when venue allows.

## Refuse list

VPN / proxy / Tor / location spoof; auto-submit loops; wash or self-match; other people's money; edge / profit / legal-blessing claims; Kalshi sports-politics while blocked; international Polymarket new risk; blind retry on Novig queued responses.

## Rank and spend

CalmBinderPress > Website Landlord > this desk for attention. New tool spend stays light.
