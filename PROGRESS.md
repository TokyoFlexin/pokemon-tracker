# Progress

## 2026-10-02 — v1 shipped
- [x] Cards tab: search + add any 30th Celebration single (incl. variants like Holofoil / Reverse Holofoil), qty, value in AUD, % change since added
- [x] Sealed tab: any SV/ME-era booster pack, box, bundle, ETB, tin, collection — market price vs your MSRP, profit in $ and %
- [x] Upcoming tab: Australian release dates scraped from cardtracker.au/releases
- [x] Header shows total collection value
- [x] GitHub Action refreshes data every 3 hours; site always loads the newest snapshot
- [x] Export / import collection backup
- [x] Seeded first visit with the 30th Celebration Booster Bundle

## Waiting on Sahel
- [ ] List of the 30th Celebration cards you own (add them on the site, or send me the list)
- [ ] MSRP you paid for the Booster Bundle (type it into the tile)

## Ideas / not built yet
- More sets for singles: add the set name to `CARD_SETS` in `scripts/update.py`
- Real Australian (eBay AU) prices instead of US→AUD conversion: cardtracker.au has an API, but it's paid (info@cardtracker.au)
- Price history charts: would need the Action to append snapshots instead of overwriting
- Sync collection across devices: right now it lives in each browser (use Export/Import)
