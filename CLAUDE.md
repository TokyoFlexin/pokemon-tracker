# Pokémon Tracker

Static site (GitHub Pages) + a scheduled GitHub Action that refreshes JSON. No build step, no dependencies.

- `index.html` — whole site: HTML, CSS, JS in one file. Collection lives in `localStorage["pokemon-tracker"]` (array of `{kind: "card"|"sealed"|"target", id, variant, qty, msrp?, addedAud}`); starts empty. Targets are sealed products on a watchlist: not in the total, and "I bought one" converts them to sealed. Chart range lives in `localStorage["pokemon-tracker-range"]`.
- Section ids are `p-<tab>` on purpose: if they matched the URL hash, the browser would jump past the header.
- AU RRP defaults live in `auRrp(p)` in index.html (ME-era ETB/Booster Bundle only; sourced from cardtracker.au, Oct 2026). They fill `msrp` when an item is added and backfill items with no msrp on load. Retailer sites (JB/Big W) block scripted requests, so there's no live RRP source.
- Sealed tab is a two-column `.split`: table left, sticky total-value chart right; stacks with the chart first under 860px.
- `drawChart(box, pts, ref)` is the one chart renderer (item dialog + Sealed total). Sealed items in `prices.json` carry `release` (US date) when TCGplayer marks them as presale.
- Design: "Price Guide Binder" (user picked a mix of an editorial price-guide look + binder pages, 2026-10-02). Paper `#f6f1e7`, leather binder `#2b241c`, Newsreader + Libre Franklin. Don't drift back to a generic dark dashboard.
- `scripts/update.py` — stdlib Python. Writes `data/prices.json`, `data/releases.json` and `data/history/YYYY-MM.json` (`{date: {"id|variant": aud}}`, keyed by tcgcsv's last-updated date).
- `prices.json` `updated` = tcgcsv's `last-updated.txt`, so files only change (and only get committed) when upstream data changes (~daily).
- Price history can't be backfilled: the tcgcsv archive is offline (403, "temporarily removed"), cardtracker API is paid, and TCGplayer's internal API is off-limits. Recording began 2026-10-01.
- In `index.html` the history object is `priceHistory`. Don't name it `history`: that would shadow `window.history`, which the tabs use.
- `.github/workflows/update.yml` — runs the script every 3h, commits `data/` if it changed.
- `PROGRESS.md` — what's done, what's pending, ideas.

## Data sources (and why)
- **Prices:** tcgcsv.com (free daily mirror of TCGplayer, category 3 = Pokémon). No CORS, hence the Action. Market price is USD; converted to AUD with frankfurter.dev at fetch time.
  - Singles: only groups whose name contains `CARD_SETS` (currently "30th Celebration" → main set + Classic Collection, and "Pitch Black").
  - Sealed: every group whose name starts with "SV" or "ME". Sealed = product with no `Number` field, excluding "Code Card".
- **Upcoming releases:** scraped from https://cardtracker.au/releases (robots.txt allows it; their `/api` is paid and disallowed). Parser reads the `<article>`s between "Upcoming releases" and "On the watch list". If the parse fails, the last good `releases.json` is kept.

## Run locally
`python3 scripts/update.py` then `python3 -m http.server` and open http://localhost:8000 (fetch doesn't work from file://).

The user is in Australia, so show AUD. US→AUD conversion is fine with them (no paid AU price API).
Card search labels include number + rarity because names repeat (e.g. Lugia 121/128 Rare vs Lugia 149/147 Classic Collection).
