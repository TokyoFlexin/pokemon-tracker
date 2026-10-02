# Progress

## 2026-10-02 — v5: AU RRP + split Sealed layout
- [x] Australian RRP pre-filled for Mega Evolution ETBs (A$109; 30th Celebration A$100) and Booster Bundles (A$59.99; 30th A$54), marked "AU RRP" and editable
- [x] Sealed tab split in two: list on the left, total-value chart on the right (sticky while scrolling); stacks on phones

## 2026-10-02 — v4: targets + chart ranges
- [x] 7D / 30D / 90D / All range buttons on every chart (remembered, shared across charts)
- [x] Targets tab: watchlist of products to buy (incl. presale, e.g. Delta Reign), MSRP → profit at MSRP, release badge, chart, "I bought one" moves it to Sealed
- [x] Sealed tab: total sealed value chart with a dashed "Paid" line; MSRP line on sealed/target item charts
- [x] Presale release dates captured from TCGplayer (`release` on sealed items)
- [x] Fixed: tab links (#sealed) no longer scroll past the header

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
- More sets for singles: add the set name to `CARD_SETS` in `scripts/update.py`
- Sync collection across devices: right now it lives in each browser (use Export/Import)
