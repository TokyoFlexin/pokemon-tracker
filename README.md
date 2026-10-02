# The Pokémon Price Guide

A free website for tracking what your Pokémon TCG collection is worth, in Australian dollars.

**Live site:** https://tokyoflexin.github.io/pokemon-tracker/

- **Binder:** add your singles and see each card's market value, plus how much it has moved since you added it.
- **Price history:** a small trend line on every item. Tap it for a full chart with daily prices.
- **Sealed:** add booster packs, boxes, bundles, ETBs, tins and collections, enter what you paid, and see your return in dollars and percent.
- **Release calendar:** upcoming Pokémon TCG release dates for Australia.

There's no account to sign up for, nothing to install, and no ads.

---

## Using the site

### Add a card
1. Open the **Binder** tab.
2. Start typing a card name or number, e.g. `Lugia 149` or `Pikachu ex 053`.
3. Pick the right card from the suggestions and press **Add to binder**.

Each suggestion shows the card number and rarity, because some names appear more than once in a set. For example, `Lugia #121/128 · Rare` is worth well under a dollar, while `Lugia #149/147 · Classic Collection` is worth hundreds. Adding a card you already have increases its quantity.

### Add sealed product
1. Open the **Sealed** tab.
2. Search for the product, e.g. `30th Celebration Booster Bundle`, and press **Add sealed**.
3. Type what you paid per item into **MSRP each (A$)**.

The **Return** column then shows your profit or loss. The total row at the bottom adds up every item that has an MSRP entered.

### See price history
Every card and sealed item has a **Price history** line under its price. Once there are two or more days of data it shows a small trend line and the % change. Tap it to open a full chart:
- Hover over or drag across the chart to read the price on any day. On a keyboard, click the chart and use ← →.
- **Show as a table** lists every daily price.

History started recording on **1 October 2026**, so charts fill in one point per day from then on. Older prices aren't available: tcgcsv's free archive is offline, and the other sources are paid or private.

### Change or remove items
- Change **Qty** on any card or product to set how many you own.
- **Remove** deletes an item. It asks you to confirm first.

### Back up your collection
Your collection is saved **in your browser on this device only**. It isn't sent anywhere, and it won't appear on your other devices automatically.

- **Export backup** downloads a `pokemon-collection.json` file.
- **Import backup** loads that file on another device or browser. It **replaces** whatever collection is there.

Export a backup now and then. Clearing your browser data or using a private window will lose your collection.

---

## How the numbers work

| What you see | How it's calculated |
|---|---|
| Card / product value | TCGplayer **market price** (USD) × the current USD→AUD exchange rate × quantity |
| "since added" | Today's price compared with the price on the day you added the card |
| Return (sealed) | `market value − (MSRP × qty)`, and that amount as a % of what you paid |
| Collection value | Every card and sealed item added together (items with no price count as $0) |
| Price history | One TCGplayer market price per day, converted at that day's exchange rate |

The exchange rate and the time of the last update are shown under the collection value at the top of the page.

**What to keep in mind:**
- **These are US prices converted to AUD, not Australian sale prices.** Prices on Australian eBay or in local shops can be higher or lower, especially for brand-new releases.
- **Prices update about once a day.** The site checks for new data every 3 hours, but TCGplayer's market prices only change roughly daily.
- **"No sales yet" / "No price yet"** means TCGplayer doesn't have a market price for that item yet. This is common for very new or very rare items.
- This is a tracking tool, not financial advice.

### What's covered
- **Singles:** **30th Celebration** (including the Classic Collection) and **Pitch Black**.
- **Sealed:** every Scarlet & Violet and Mega Evolution era product on TCGplayer, from 2023 onwards.
- **Release calendar:** upcoming Australian release dates from [cardtracker.au](https://cardtracker.au/releases).

---

## Where the data comes from

| Data | Source | Notes |
|---|---|---|
| Card and sealed prices | [tcgcsv.com](https://tcgcsv.com), a free daily copy of TCGplayer's price data | Market price in USD |
| USD → AUD rate | [Frankfurter](https://frankfurter.dev) (European Central Bank rates) | Updated each working day |
| Release dates | [cardtracker.au/releases](https://cardtracker.au/releases) | Read from their public page |
| Card and product images | TCGplayer and cardtracker.au | Loaded straight from their servers |

Browsers can't load these sources directly, so a scheduled GitHub Action ([`update.yml`](.github/workflows/update.yml)) runs [`scripts/update.py`](scripts/update.py) every 3 hours. It saves the results to [`data/`](data/), and the website reads those files every time you open it. Each run also saves that day's prices into `data/history/`, which is what the charts are drawn from. Files are only committed when TCGplayer's data or the exchange rate actually changes, which is about once a day.

---

## Run your own copy

You can have your own copy that updates itself, for free.

1. **Fork** this repo on GitHub.
2. In your fork, go to **Settings → Pages** and set **Source** to `Deploy from a branch`, branch `main`, folder `/ (root)`.
3. Go to the **Actions** tab and click **I understand my workflows, go ahead and enable them**. GitHub turns off scheduled workflows in forks until you do this.
4. Open **Update prices & releases** and click **Run workflow** to get fresh data straight away.

Your site will be at `https://<your-username>.github.io/pokemon-tracker/`.

### Run it on your computer

You need Python 3.9 or newer. There's nothing else to install.

```bash
python3 scripts/update.py
```

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000. Opening `index.html` directly from your files won't work, because browsers block the data files when a page is opened that way.

---

## Customising

All the settings are at the top of [`scripts/update.py`](scripts/update.py).

| To… | Change |
|---|---|
| Track singles from more sets | Add part of the TCGplayer set name to `CARD_SETS`, e.g. `("30th Celebration", "Pitch Black", "Prismatic Evolutions")` |
| Track sealed product from other eras | Add to `SEALED_PREFIXES`. It matches the start of TCGplayer set names, e.g. `"SWSH"` for Sword & Shield |
| Change how often prices refresh | Edit the `cron` line in [`.github/workflows/update.yml`](.github/workflows/update.yml) |
| Use another currency | Change `to=AUD` in `update.py`, then the `"AUD"` / `"A$"` formatting in the `aud()` function in `index.html` |

To see TCGplayer's exact set names, open https://tcgcsv.com/tcgplayer/3/groups.

---

## Project layout

```
index.html                     The whole website (HTML, CSS and JavaScript in one file)
scripts/update.py              Fetches prices, exchange rate and release dates (Python standard library only)
data/prices.json               Latest prices, written by the script
data/releases.json             Latest release calendar, written by the script
data/history/YYYY-MM.json      Daily prices for one month, used by the charts
.github/workflows/update.yml   Runs the script every 3 hours and commits any changes
PROGRESS.md                    What's been built and ideas for later
```

### Data formats

`data/prices.json`
```json
{
  "updated": "2026-10-02T02:53:45+00:00",
  "usdToAud": 1.4388,
  "cards":  [{ "id": 714386, "name": "Lugia", "number": "149/147", "rarity": "Classic Collection",
               "set": "ME: 30th Celebration Classic Collection", "img": "…", "url": "…",
               "prices": { "Holofoil": 272.91 } }],
  "sealed": [{ "id": 704171, "name": "30th Celebration Booster Bundle", "set": "ME: 30th Celebration",
               "img": "…", "url": "…", "prices": { "Normal": 88.99 } }]
}
```
`prices` holds USD market prices for each print variant (Normal, Holofoil, Reverse Holofoil…). It's empty when there's no market price yet.

`data/history/2026-10.json` holds one entry per day, mapping `"productId|variant"` to that day's AUD price:
```json
{ "2026-10-01": { "714386|Holofoil": 392.66, "704171|Normal": 128.04 } }
```

The **backup file** (`pokemon-collection.json`) is a list of your items:
```json
[
  { "kind": "card",   "id": 714386, "variant": "Holofoil", "qty": 1, "addedAud": 392.66 },
  { "kind": "sealed", "id": 704171, "variant": "Normal",   "qty": 1, "addedAud": 128.04, "msrp": 54.95 }
]
```
`id` is the TCGplayer product ID, `addedAud` is the price per item on the day you added it, and `msrp` is what you paid per item in AUD.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| My collection disappeared | It's stored in the browser. If you cleared site data, used a private window or switched browsers, use **Import backup** with your last export. |
| A chart only shows one dot | History started on 1 October 2026 and adds one point per day. Come back tomorrow. |
| A card I own isn't in the search | Singles only cover the sets listed in `CARD_SETS`. Brand-new cards can also take a day or two to appear on TCGplayer. |
| "Updated" time is more than a day old | Open the repo's **Actions** tab. If the workflow failed, open the run to see the error. If it shows as disabled, enable it again: GitHub turns off scheduled workflows in public repos after 60 days with no activity. |
| Release calendar looks out of date | It only changes when cardtracker.au updates their page. If their page layout changes and the reader fails, the last good calendar is kept and the workflow log shows `releases failed`. |
| A price looks wrong | Click the card or product name to open its TCGplayer page and compare. New releases often swing a lot in their first few weeks. |

---

Not affiliated with The Pokémon Company, Nintendo, TCGplayer or cardtracker.au. Pokémon and all related names are trademarks of their respective owners.
