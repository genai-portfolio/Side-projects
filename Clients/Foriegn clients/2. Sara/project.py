"""
LoopNet Commercial Real Estate Scraper
=======================================
- Per-country CSV files, rows updated in-place
- Country-aware card parser (UK has different XPaths)
- Autocomplete-safe search (no crash if Enter times out)
- 3-second countdown, no second dialog

Requirements:
    pip install playwright
    playwright install chromium
"""

import asyncio
import csv
import random
import re
import subprocess
import sys
import tkinter as tk
from datetime import date
from pathlib import Path

from playwright.async_api import async_playwright, TimeoutError as PWTimeout


# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
CDP_URL          = "http://localhost:9222"
CHROME_PATH      = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_DEBUG_DIR = r"C:\chrome-debug"
MAX_LISTINGS     = 5
CHROME_WAIT_SEC  = 3

COUNTRIES     = {"1": "USA", "2": "France", "3": "Spain", "4": "United Kingdom", "5": "Canada"}
LISTING_TYPES = {"1": "For Lease", "2": "For Sale"}

def csv_path(country: str) -> str:
    return f"listings_{country.lower().replace(' ', '_')}.csv"


# ─────────────────────────────────────────────
# BASE XPATH
# ─────────────────────────────────────────────
BASE = "/html/body/section[1]/main/section[1]/div/section/section[1]/div[3]"

def card(ul, li):
    return f"{BASE}/ul[{ul}]/li[{li}]/article"


# ─────────────────────────────────────────────
# STANDARD CARD XPATHS  (USA, France, Spain, Canada)
# ─────────────────────────────────────────────
def std_name(ul, li):     return f"{card(ul,li)}/header/div[1]/h4/a"
def std_size(ul, li):     return f"{card(ul,li)}/header/div[2]/h4/a"
def std_state(ul, li):    return f"{card(ul,li)}/header/div[2]/h6/a"

def std_price_li(ul, li, sub, alt=False):
    mid = "div[2]/div" if alt else "div[2]/div[2]/div"
    return f"{card(ul,li)}/{mid}/ul[1]/li[{sub}]"

def std_broker(ul, li, b):
    base = f"{card(ul,li)}/div[2]/div[2]/ul/li[{b}]/a/span[2]"
    return f"{base}/span[1]", f"{base}/span[2]"


# ─────────────────────────────────────────────
# UK CARD XPATHS  (different structure)
# ─────────────────────────────────────────────
# Name:   header/div[1]              (whole div, no inner anchor)
# Size:   div[2]/div[2]/div[1]/ul[1]/li[1]   "12,101 - 290,202 SF"
# Price:  div[2]/div[2]/div[1]/ul[1]/li[2]   "$17.69 - $20.36 SF/YR"
# Spaces: div[2]/div[2]/div[1]/ul[1]/li[3]   "3 Spaces Available Now"
# State:  header/div[2]/h6/a                 (same as standard)
# Space-uses: header/div[2]/h4/a             "290,202 SF Industrial Available"
# Broker first: div[2]/div[2]/div[2]/div[1]/div/div[N]/div/a/span[3]/span[1]
# Broker last:  div[2]/div[2]/div[2]/div[1]/div/div[N]/div/a/span[3]/span[2]

def uk_name(ul, li):   return f"{card(ul,li)}/header/div[1]"
def uk_size(ul, li):   return f"{card(ul,li)}/div[2]/div[2]/div[1]/ul[1]/li[1]"
def uk_price(ul, li):  return f"{card(ul,li)}/div[2]/div[2]/div[1]/ul[1]/li[2]"
def uk_state(ul, li):  return f"{card(ul,li)}/header/div[2]/h6/a"

def uk_broker(ul, li, n):
    # n = 1-based broker slot (div[1], div[2], ...)
    base = f"{card(ul,li)}/div[2]/div[2]/div[2]/div[1]/div/div[{n}]/div/a/span[3]"
    return f"{base}/span[1]", f"{base}/span[2]"


# ─────────────────────────────────────────────
# PRICE CLASSIFIER
# ─────────────────────────────────────────────
CURRENCY_RE = re.compile(
    r"(\$|€|£|price\s+upon\s+request|upon\s+request|contact\s+for\s+price|negotiable)",
    re.IGNORECASE
)
REJECT_RE = re.compile(
    r"(\d+\s+space|\d+\s+unit|\d+\s+suite|available\s+(now|soon))",
    re.IGNORECASE
)

def is_price(text: str) -> bool:
    if not text: return False
    if REJECT_RE.search(text): return False
    return bool(CURRENCY_RE.search(text))


# ══════════════════════════════════════════════
# CHROME LAUNCHER
# ══════════════════════════════════════════════

def launch_chrome():
    if not Path(CHROME_PATH).exists():
        print(f"❌  Chrome not found at: {CHROME_PATH}")
        sys.exit(1)
    subprocess.Popen([
        CHROME_PATH,
        "--remote-debugging-port=9222",
        f"--user-data-dir={CHROME_DEBUG_DIR}",
        "--no-first-run",
        "--no-default-browser-check",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("[chrome] ✓ Chrome launched")


# ══════════════════════════════════════════════
# TKINTER UI
# ══════════════════════════════════════════════

def launch_ui() -> dict | None:
    result = {}
    root = tk.Tk()
    root.title("LoopNet Scraper")
    root.resizable(False, False)
    root.configure(bg="#1a1a2e")

    BG, CARD_BG     = "#1a1a2e", "#16213e"
    ACCENT          = "#e94560"
    FG, FG_DIM      = "#e0e0e0", "#a0a0b0"
    FONT   = ("Segoe UI", 10)
    FONT_B = ("Segoe UI", 10, "bold")
    FONT_H = ("Segoe UI", 14, "bold")

    def cf(p): return tk.Frame(p, bg=CARD_BG)

    tk.Frame(root, bg=ACCENT, height=4).pack(fill="x")
    tk.Label(root, text="LoopNet Scraper",
             bg=BG, fg=ACCENT, font=FONT_H).pack(pady=(14, 2))
    tk.Label(root, text="Configure your search",
             bg=BG, fg=FG_DIM, font=("Segoe UI", 9)).pack(pady=(0, 12))

    # Country
    cc = cf(root); cc.pack(fill="x", padx=22, pady=(0, 10))
    tk.Label(cc, text="  🌍  Select Country",
             bg=CARD_BG, fg=ACCENT, font=FONT_B, anchor="w").pack(fill="x", padx=10, pady=(10, 6))
    country_var = tk.StringVar(value="1")
    rb = dict(bg=CARD_BG, fg=FG, font=FONT, activebackground=CARD_BG,
              activeforeground=ACCENT, selectcolor="#0f3460", relief="flat",
              variable=country_var)
    cg = tk.Frame(cc, bg=CARD_BG); cg.pack(padx=14, pady=(0, 10))
    for idx, (num, name) in enumerate(COUNTRIES.items()):
        tk.Radiobutton(cg, text=f"{num}. {name}", value=num, **rb).grid(
            row=idx // 2, column=idx % 2, sticky="w", padx=10, pady=3)

    # Listing type
    tc = cf(root); tc.pack(fill="x", padx=22, pady=(0, 14))
    tk.Label(tc, text="  🏷  Listing Type",
             bg=CARD_BG, fg=ACCENT, font=FONT_B, anchor="w").pack(fill="x", padx=10, pady=(10, 6))
    type_var = tk.StringVar(value="1")
    tr = tk.Frame(tc, bg=CARD_BG); tr.pack(padx=14, pady=(0, 10))
    for num, name in LISTING_TYPES.items():
        tk.Radiobutton(tr, text=f"{num}. {name}", value=num,
                       **{**rb, "variable": type_var}).pack(side="left", padx=16)

    # Status bar
    status_var = tk.StringVar(value="")
    tk.Label(root, textvariable=status_var,
             bg=BG, fg="#2ecc71", font=FONT_B).pack(pady=(0, 6))

    btn_frame = tk.Frame(root, bg=BG); btn_frame.pack(pady=(0, 18))
    start_btn = tk.Button(btn_frame, text="▶  Start Scraping",
                          bg=ACCENT, fg="white", font=FONT_B,
                          relief="flat", cursor="hand2", padx=18, pady=8)
    start_btn.pack(side="left", padx=8)
    tk.Button(btn_frame, text="Close", command=root.destroy,
              bg="#333355", fg=FG, font=FONT,
              relief="flat", cursor="hand2", padx=14, pady=8).pack(side="left", padx=8)

    result["_root"]            = root
    result["_status_var"]      = status_var
    result["_start_btn"]       = start_btn
    result["_country_var"]     = country_var
    result["_type_var"]        = type_var
    result["_chrome_launched"] = False

    def set_busy(busy):
        s  = "disabled" if busy else "normal"
        bg = "#888"     if busy else ACCENT
        start_btn.config(state=s, bg=bg)
        for w in cg.winfo_children(): w.config(state=s)
        for w in tr.winfo_children(): w.config(state=s)

    result["_set_busy"] = set_busy

    def tick(n, country, listing_type):
        if n > 0:
            status_var.set(f"⏳  Chrome opening … starting in {n}s")
            root.after(1000, tick, n - 1, country, listing_type)
        else:
            status_var.set("🔗  Connecting to Chrome …")
            import threading
            threading.Thread(
                target=lambda: asyncio.run(run(country, listing_type, result)),
                daemon=True
            ).start()

    def on_start():
        import threading
        country      = COUNTRIES[country_var.get()]
        listing_type = LISTING_TYPES[type_var.get()]
        set_busy(True)
        if not result["_chrome_launched"]:
            launch_chrome()
            result["_chrome_launched"] = True
            tick(CHROME_WAIT_SEC, country, listing_type)
        else:
            status_var.set("🔗  Connecting to Chrome …")
            threading.Thread(
                target=lambda: asyncio.run(run(country, listing_type, result)),
                daemon=True
            ).start()

    start_btn.config(command=on_start)
    root.update_idletasks()
    root.geometry(f"{root.winfo_reqwidth()+20}x{root.winfo_reqheight()+10}")
    root.mainloop()   # stays open until user clicks Close or X


# ══════════════════════════════════════════════
# HUMAN HELPERS
# ══════════════════════════════════════════════

async def human_delay(page, mn=800, mx=2200):
    await page.wait_for_timeout(random.randint(mn, mx))

async def human_type(page, loc, text):
    for ch in text:
        await loc.type(ch, delay=random.randint(80, 220))
        if random.random() < 0.07:
            await page.wait_for_timeout(random.randint(150, 500))

async def human_click(page, loc):
    await loc.scroll_into_view_if_needed()
    await loc.hover()
    await page.wait_for_timeout(random.randint(100, 350))
    await loc.click()

async def human_presence(page):
    vp = page.viewport_size or {"width": 1280, "height": 900}
    for _ in range(random.randint(3, 6)):
        await page.mouse.move(random.randint(100, vp["width"]-100),
                              random.randint(100, vp["height"]-100),
                              steps=random.randint(8, 20))
        await page.wait_for_timeout(random.randint(80, 200))
    await page.mouse.wheel(0, random.randint(60, 180))
    await page.wait_for_timeout(200)
    await page.mouse.wheel(0, -random.randint(30, 90))


# ══════════════════════════════════════════════
# CONNECT
# ══════════════════════════════════════════════

async def connect(pw):
    print(f"\n[browser] Connecting to Chrome at {CDP_URL} …")
    try:
        browser = await pw.chromium.connect_over_cdp(CDP_URL)
        print("[browser] ✓ Connected")
    except Exception as e:
        print(f"❌  Could not connect: {e}")
        raise
    ctx  = browser.contexts[0] if browser.contexts else await browser.new_context()
    page = await ctx.new_page()
    return browser, page


# ══════════════════════════════════════════════
# SEARCH  — autocomplete-safe
# ══════════════════════════════════════════════

XPATH_SEARCH = "/html/body/section[1]/main/section/section[1]/div[2]/div/div/form/div/div/div[2]/div[2]/div/input"
XPATH_DD     = "/html/body/section[1]/main/section[1]/div/div/section[2]/div[1]/div[2]/div/button"
XPATH_LEASE  = "/html/body/section[1]/main/section[1]/div/div/section[2]/div[1]/div[2]/div/ul/li[1]/button"
XPATH_SALE   = "/html/body/section[1]/main/section[1]/div/div/section[2]/div[1]/div[2]/div/ul/li[2]/button"

def is_on_results_page(url: str) -> bool:
    """Return True if LoopNet already navigated to a search/results page."""
    return "/search/" in url or "/commercial-real-estate/" in url

async def do_search(page, country):
    print(f"\n[2] Navigating to LoopNet …")
    await page.goto("https://www.loopnet.com", wait_until="domcontentloaded")
    await human_presence(page)
    await human_delay(page, 1800, 3200)

    print(f"[2] Typing '{country}' …")
    sb = page.locator(f"xpath={XPATH_SEARCH}")
    await sb.wait_for(state="visible", timeout=15000)
    await human_click(page, sb)
    await human_delay(page, 400, 800)
    await human_type(page, sb, country)
    await human_delay(page, 800, 1400)

    # Check if autocomplete already navigated us to results
    if is_on_results_page(page.url):
        print(f"[2] ✓ Autocomplete navigated to results — skipping Enter")
    else:
        print(f"[2] Pressing Enter …")
        try:
            await sb.press("Enter", timeout=10000)
            await human_delay(page, 3000, 5000)
        except PWTimeout:
            # Enter timed out — check if we landed on results anyway
            if is_on_results_page(page.url):
                print(f"[2] ✓ Already on results page (Enter timeout ignored)")
            else:
                print(f"[2] ⚠ Waiting extra time for navigation …")
                await human_delay(page, 4000, 6000)

    print(f"[2] ✓ On: {page.url}")

async def do_select_type(page, listing_type):
    print(f"\n[3] Selecting '{listing_type}' …")
    btn = page.locator(f"xpath={XPATH_DD}")
    await btn.wait_for(state="visible", timeout=15000)
    await human_click(page, btn)
    await human_delay(page, 800, 1500)
    opt = page.locator(f"xpath={XPATH_LEASE if listing_type == 'For Lease' else XPATH_SALE}")
    await opt.wait_for(state="visible", timeout=10000)
    await human_click(page, opt)
    await human_delay(page, 2500, 4000)
    print(f"[3] ✓ '{listing_type}' selected")


# ══════════════════════════════════════════════
# SAFE TEXT GETTER
# ══════════════════════════════════════════════

async def get_text(page, xpath, timeout=4000) -> str:
    try:
        el = page.locator(f"xpath={xpath}")
        await el.wait_for(state="visible", timeout=timeout)
        return (await el.inner_text()).strip()
    except Exception:
        return ""


# ══════════════════════════════════════════════
# FIELD EXTRACTORS — standard countries
# ══════════════════════════════════════════════

async def std_get_price(page, ul, li) -> str:
    all_c = []
    for alt in [False, True]:
        for sub in range(1, 8):
            t = await get_text(page, std_price_li(ul, li, sub, alt), timeout=2000)
            if not t: break
            all_c.append(t)
    seen, candidates = set(), []
    for t in all_c:
        if t not in seen:
            seen.add(t); candidates.append(t)
    for t in candidates:
        if is_price(t): return t
    if candidates:
        print(f"         [price] no currency in: {candidates}")
    return "N/A"

async def std_get_brokers(page, ul, li) -> str:
    names = []
    for b in range(2, 10):
        fx, lx = std_broker(ul, li, b)
        f = await get_text(page, fx, timeout=2000)
        l = await get_text(page, lx, timeout=2000)
        full = f"{f} {l}".strip()
        if not full: break
        names.append(full)
    return ", ".join(names) if names else "N/A"

def clean_size_std(raw: str) -> str:
    """'50,675 SF Office Available' → '50,675 SF'"""
    if not raw: return "N/A"
    m = re.search(r"[\d,\s\-\.]+SF", raw)
    return m.group(0).strip() if m else raw

def clean_state(raw: str) -> str:
    if not raw: return "N/A"
    m = re.search(r",\s*([A-Z]{2})\b", raw)
    return m.group(1) if m else raw.strip()


# ══════════════════════════════════════════════
# FIELD EXTRACTORS — UK
# ══════════════════════════════════════════════

async def uk_get_price(page, ul, li) -> str:
    """UK: price is always at li[2] in div[1]/ul[1]."""
    t = await get_text(page, uk_price(ul, li), timeout=4000)
    if is_price(t):
        return t
    # fallback: scan li[1..5]
    for sub in range(1, 6):
        t = await get_text(
            page,
            f"{card(ul,li)}/div[2]/div[2]/div[1]/ul[1]/li[{sub}]",
            timeout=2000
        )
        if is_price(t): return t
    print(f"         [price-uk] not found")
    return "N/A"

async def uk_get_size(page, ul, li) -> str:
    """UK: size is at div[1]/ul[1]/li[1] e.g. '12,101 - 290,202 SF'"""
    raw = await get_text(page, uk_size(ul, li), timeout=4000)
    if not raw: return "N/A"
    m = re.search(r"[\d,\s\-\.]+SF", raw)
    return m.group(0).strip() if m else raw

async def uk_get_name(page, ul, li) -> str:
    """
    UK name div contains multiple text nodes.
    We grab the whole div text and take only the first non-empty line.
    """
    raw = await get_text(page, uk_name(ul, li), timeout=4000)
    if not raw: return "N/A"
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    return lines[0] if lines else raw.strip()

async def uk_get_brokers(page, ul, li) -> str:
    """
    UK broker structure:
      div[2]/div[2]/div[2]/div[1]/div/div[N]/div/a/span[3]/span[1 or 2]
    Loop div[1], div[2], div[3] …
    """
    names = []
    for n in range(1, 8):
        fx, lx = uk_broker(ul, li, n)
        f = await get_text(page, fx, timeout=2000)
        l = await get_text(page, lx, timeout=2000)
        full = f"{f} {l}".strip()
        if not full: break
        names.append(full)
    return ", ".join(names) if names else "N/A"


# ══════════════════════════════════════════════
# COUNTRY-AWARE CARD SCRAPER
# ══════════════════════════════════════════════

async def scrape_one(page, ul, li, country: str) -> dict:
    """Scrape a single card using the correct XPath strategy for the country."""

    if country == "United Kingdom":
        name    = await uk_get_name(page, ul, li)
        size    = await uk_get_size(page, ul, li)
        state   = clean_state(await get_text(page, uk_state(ul, li)))
        price   = await uk_get_price(page, ul, li)
        brokers = await uk_get_brokers(page, ul, li)
    else:
        name    = await get_text(page, std_name(ul, li))
        size    = clean_size_std(await get_text(page, std_size(ul, li)))
        state   = clean_state(await get_text(page, std_state(ul, li)))
        price   = await std_get_price(page, ul, li)
        brokers = await std_get_brokers(page, ul, li)

    return {
        "name":    name    or "N/A",
        "size":    size    or "N/A",
        "state":   state   or "N/A",
        "price":   price,
        "brokers": brokers,
        "date":    str(date.today()),
    }


# ══════════════════════════════════════════════
# MAIN SCRAPE LOOP
# ══════════════════════════════════════════════

async def scrape_listings(page, count: int, country: str) -> list[dict]:
    print(f"\n[4] Scraping first {count} listings for {country} …\n")

    # Detect ul[1] size
    probe_xpath = uk_name if country == "United Kingdom" else std_name
    ul1_size = 0
    for probe in range(1, 20):
        if await get_text(page, probe_xpath(1, probe), timeout=2000):
            ul1_size = probe
        else:
            break
    print(f"      ul[1] contains {ul1_size} listing(s)\n")

    listings = []
    for n in range(1, count + 1):
        ul, li = (1, n) if n <= ul1_size else (2, n - ul1_size)
        print(f"  [{n}/{count}] ul[{ul}] li[{li}]")

        item = await scrape_one(page, ul, li, country)

        w = 12
        print(f"       {'Name':<{w}}: {item['name']}")
        print(f"       {'Size':<{w}}: {item['size']}")
        print(f"       {'State':<{w}}: {item['state']}")
        print(f"       {'Price':<{w}}: {item['price']}")
        print(f"       {'Brokers':<{w}}: {item['brokers']}\n")

        listings.append(item)
        await human_delay(page, 400, 900)

    return listings


# ══════════════════════════════════════════════
# PER-COUNTRY CSV — in-place row updates
# ══════════════════════════════════════════════

FIELDNAMES = ["name", "size", "state", "price", "brokers", "last_seen", "first_seen"]
TRACK      = ["size", "state", "price", "brokers"]

def load_csv(path: str) -> dict:
    if not Path(path).exists(): return {}
    with open(path, newline="", encoding="utf-8") as f:
        return {row["name"]: row for row in csv.DictReader(f)}

def save_csv(rows: dict, path: str):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        w.writerows(rows.values())

def merge_and_report(existing: dict, scraped: list[dict], country: str) -> dict:
    today   = str(date.today())
    updated = dict(existing)

    print(f"\n[COMPARE] {country} — checking for changes …")
    for item in scraped:
        name = item["name"]
        if name == "N/A": continue

        if name not in updated:
            updated[name] = {
                "name":       name,
                "size":       item["size"],
                "state":      item["state"],
                "price":      item["price"],
                "brokers":    item["brokers"],
                "last_seen":  today,
                "first_seen": today,
            }
            print(f"  🆕 NEW    : {name}")
        else:
            row     = updated[name]
            changes = []
            for field in TRACK:
                old, new = row.get(field, "N/A"), item.get(field, "N/A")
                if old != new:
                    changes.append((field, old, new))
                    row[field] = new
            row["last_seen"] = today

            if changes:
                print(f"  🔄 CHANGED: {name}")
                for field, old, new in changes:
                    print(f"       {field:<10}: '{old}'  →  '{new}'")
            else:
                print(f"  ✅ SAME   : {name}")

    return updated


# ══════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════

def set_status(ui: dict, msg: str):
    """Push a status message into the Tkinter label from any thread."""
    sv = ui.get("_status_var")
    root = ui.get("_root")
    if sv and root:
        try:
            sv.set(msg)
            root.update_idletasks()
        except Exception:
            pass   # window may have been closed manually


async def run(country: str, listing_type: str, ui: dict):
    set_status(ui, "🔗  Connecting to Chrome …")
    async with async_playwright() as pw:
        browser, page = await connect(pw)

        set_status(ui, f"🔍  Searching for {country} …")
        await do_search(page, country)

        set_status(ui, f"🏷  Applying filter: {listing_type} …")
        await do_select_type(page, listing_type)

        set_status(ui, f"📋  Scraping listings …")
        scraped = await scrape_listings(page, MAX_LISTINGS, country)
        await page.close()

    set_status(ui, "💾  Saving to CSV …")
    path     = csv_path(country)
    existing = load_csv(path)
    updated  = merge_and_report(existing, scraped, country)
    save_csv(updated, path)

    print(f"\n[CSV] ✓ {path}  ({len(updated)} total rows)")
    set_status(ui, f"✅  Done! {len(scraped)} listings saved → {path}")

    # Close the window cleanly after a short pause so user sees the done message
    root = ui.get("_root")
    if root:
        try:
            root.after(2000, root.destroy)
            root.mainloop()   # re-enter mainloop for the 2s pause + destroy
        except Exception:
            pass

    print("✅ Done.")


def main():
    ui = launch_ui()
    if not ui:
        print("Cancelled.")
        return
    country      = ui["country"]
    listing_type = ui["listing_type"]
    print(f"\n▶  Country: {country}  |  Type: {listing_type}  |  Max: {MAX_LISTINGS}")
    asyncio.run(run(country, listing_type, ui))

if __name__ == "__main__":
    main()