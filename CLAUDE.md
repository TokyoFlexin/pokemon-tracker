# Pokémon Tracker

Static site (GitHub Pages) + a scheduled GitHub Action that refreshes JSON. No build step, no dependencies.

- `index.html` — whole site: HTML, CSS, JS in one file. Collection lives in `localStorage.collection` (array of `{kind: "card"|"sealed", id, variant, qty, msrp?, addedAud}`).
- `scripts/update.py` — stdlib Python. Writes `data/prices.json` and `data/releases.json`.
- `.github/workflows/update.yml` — runs the script every 3h, commits `data/` if it changed.
- `PROGRESS.md` — what's done, what's pending, ideas.

## Data sources (and why)
- **Prices:** tcgcsv.com (free daily mirror of TCGplayer, category 3 = Pokémon). No CORS, hence the Action. Market price is USD; converted to AUD with frankfurter.dev at fetch time.
  - Singles: only groups whose name contains `CARD_SETS` (currently "30th Celebration" → main set + Classic Collection).
  - Sealed: every group whose name starts with "SV" or "ME". Sealed = product with no `Number` field, excluding "Code Card".
- **Upcoming releases:** scraped from https://cardtracker.au/releases (robots.txt allows it; their `/api` is paid and disallowed). Parser reads the `<article>`s between "Upcoming releases" and "On the watch list". If the parse fails, the last good `releases.json` is kept.

## Run locally
`python3 scripts/update.py` then `python3 -m http.server` and open http://localhost:8000 (fetch doesn't work from file://).

The user is in Australia, so show AUD.
