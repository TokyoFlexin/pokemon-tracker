"""Refresh data/prices.json and data/releases.json. Stdlib only; run by the GitHub Action."""
import html
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

TCGCSV = "https://tcgcsv.com/tcgplayer/3"  # 3 = Pokemon
CARD_SETS = ("30th Celebration", "Pitch Black")  # groups whose singles we track; add more set names here
SEALED_PREFIXES = ("SV", "ME")  # Scarlet & Violet + Mega Evolution era sealed product
OUT = Path(__file__).resolve().parent.parent / "data"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "pokemon-tracker (github action)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode()


def prices():
    groups = json.loads(get(f"{TCGCSV}/groups"))["results"]
    cards, sealed = [], []
    for g in groups:
        is_card_set = any(s in g["name"] for s in CARD_SETS)
        if not (is_card_set or g["name"].startswith(SEALED_PREFIXES)):
            continue
        products = json.loads(get(f"{TCGCSV}/{g['groupId']}/products"))["results"]
        market = {}
        for p in json.loads(get(f"{TCGCSV}/{g['groupId']}/prices"))["results"]:
            if p["marketPrice"] is not None:
                market.setdefault(p["productId"], {})[p["subTypeName"]] = p["marketPrice"]
        for p in products:
            ext = {e["name"]: e["value"] for e in p.get("extendedData", [])}
            item = {"id": p["productId"], "name": p["name"], "set": g["name"], "img": p["imageUrl"],
                    "url": p["url"], "prices": market.get(p["productId"], {})}
            if "Number" in ext:
                if is_card_set:
                    cards.append(item | {"number": ext["Number"], "rarity": ext.get("Rarity", "")})
            elif not p["name"].startswith("Code Card"):
                sealed.append(item)
    fx = json.loads(get("https://api.frankfurter.dev/v1/latest?from=USD&to=AUD"))["rates"]["AUD"]
    # tcgcsv's own refresh time, so the file only changes when prices or the rate actually change
    updated = datetime.strptime(get("https://tcgcsv.com/last-updated.txt").strip(), "%Y-%m-%dT%H:%M:%S%z")
    return {"updated": updated.isoformat(), "usdToAud": fx, "cards": cards, "sealed": sealed}


def record_history(p):
    """Add today's AUD prices to data/history/YYYY-MM.json as {date: {"id|variant": aud}}."""
    day = p["updated"][:10]
    path = OUT / "history" / f"{day[:7]}.json"
    path.parent.mkdir(exist_ok=True)
    month = json.loads(path.read_text()) if path.exists() else {}
    month[day] = {f"{i['id']}|{v}": round(usd * p["usdToAud"], 2)
                  for i in p["cards"] + p["sealed"] for v, usd in i["prices"].items()}
    path.write_text(json.dumps(month, separators=(",", ":"), sort_keys=True))


def text(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def releases(page):
    """Parse the 'Upcoming releases' articles from cardtracker.au/releases."""
    section = page.split("Upcoming releases", 1)[1].split("On the watch list", 1)[0]
    out = []
    for art in re.findall(r"(?s)<article.*?</article>", section):
        date = re.search(r">\s*Expected ([^<]+)<", art)
        products = re.search(r"(?s)Products:</b>(.*?)</p>", art)
        note = re.search(r'(?s)<p class="text-\[13px\][^"]*">(.*?)</p>', art)
        img = re.search(r'<img src="([^"]+)"', art)
        link = re.search(r'<h3.*?href="([^"]+)"', art, re.S)
        spans = re.findall(r"(?s)Expected [^<]+</span>(.*?)</div>", art)
        h3 = re.search(r"(?s)<h3.*?</h3>", art).group(0)
        code = re.search(r"(?s)<span[^>]*>(.*?)</span>", h3)  # set code, e.g. "ME06"
        out.append({
            "name": text(re.sub(r"(?s)<span.*?</span>", "", h3)),
            "date": date.group(1).strip() if date else "",
            "tags": ([text(code.group(1))] if code else []) + ([text(t) for t in re.findall(r"<span>(.*?)</span>", spans[0])] if spans else []),
            "products": text(products.group(1)) if products else "",
            "note": text(note.group(1)) if note else "",
            "img": img.group(1) if img else "",
            "url": "https://cardtracker.au" + link.group(1) if link else "https://cardtracker.au/releases",
        })
    return out


def write(name, data):
    (OUT / name).write_text(json.dumps(data, separators=(",", ":")))


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    try:
        rel = releases(get("https://cardtracker.au/releases"))
        assert rel and all(r["name"] and r["date"] for r in rel), "release parse came back empty"
        write("releases.json", {"updated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "releases": rel})
    except Exception as e:  # keep last good releases.json if their HTML changes
        print("releases failed:", e)
    p = prices()
    assert p["cards"] and p["sealed"], "price fetch came back empty"
    write("prices.json", p)
    record_history(p)
    print(f"{len(p['cards'])} cards, {len(p['sealed'])} sealed, fx {p['usdToAud']}")
