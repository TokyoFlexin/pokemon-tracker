# Progress

## 2026-10-02 — v3: price history + Pitch Black
- [x] Pitch Black singles added (all 120 cards, with Normal / Holofoil / Reverse Holofoil prices); search labels now include the set
- [x] Daily price history saved to data/history/YYYY-MM.json, starting 1 Oct 2026 (no free backfill exists)
- [x] Sparkline + % change on every card and sealed item; tap for a full chart (crosshair tooltip, arrow keys, table view)
- [x] Data only committed when tcgcsv or the FX rate changes (was every 3h because of the timestamp)

## 2026-10-02 — v2: redesign + data fixes
- [x] Rebuilt in the "Price Guide Binder" style (cream paper, serif, singles shown in a leather binder, sealed as a ledger)
- [x] Collection starts empty; user adds everything themselves (new storage key, old seeded item ignored)
- [x] Search labels show card number + rarity (fixes the two-Lugia mix-up), items with no price are marked
- [x] Release parser: "Delta Reign" no longer reads "Delta Reign ME06"; set code moved to tags
- [x] Sealed totals row (paid vs worth), signed returns, remove asks to confirm, tab kept in URL (#sealed)
- [x] Verified every displayed number against data/prices.json
- [x] README.md: how to use the site, how numbers are calculated, data sources, run your own copy, customising, troubleshooting

## 2026-10-02 — v1
- [x] Cards tab: search + add any 30th Celebration single, qty, value in AUD, % change since added
- [x] Sealed tab: any SV/ME-era booster pack, box, bundle, ETB, tin, collection — market price vs your MSRP, profit in $ and %
- [x] Upcoming tab: Australian release dates scraped from cardtracker.au/releases
- [x] Header shows total collection value
- [x] GitHub Action refreshes data every 3 hours; site always loads the newest snapshot
- [x] Export / import collection backup

## Decisions
- US→AUD conversion is fine (no paid cardtracker.au API)
- User adds their own cards and sealed product on the site


## Ideas / not built yet
- Chart range presets (7d / 30d / 90d) once there's enough history to need them
- More sets for singles: add the set name to `CARD_SETS` in `scripts/update.py`
- Sync collection across devices: right now it lives in each browser (use Export/Import)
