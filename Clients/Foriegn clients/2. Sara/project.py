"""
LoopNet Commercial Real Estate Scraper
=======================================
1. Tkinter UI  → user picks country + lease/sale
2. Playwright  → humanized search on LoopNet
3. Scraper     → pulls first listing details
4. CSV         → saves result + compares with previous run

Requirements:
    pip install playwright
    playwright install chromium

Run:
    python loopnet_scraper.py
"""

import asyncio
import csv
import random
import re
import shutil
import tkinter as tk
from datetime import date
from pathlib import Path

from playwright.async_api import async_playwright


# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
LISTINGS_CSV = "listings.csv"
PREVIOUS_CSV = "previous_listings.csv"

COUNTRIES = {
    "1": "USA",
    "2": "France",
    "3": "Spain",
    "4": "United Kingdom",
    "5": "Canada",
}

LISTING_TYPES = {
    "1": "For Lease",
    "2": "For Sale",
}

# ─────────────────────────────────────────────
# XPATHs
# ─────────────────────────────────────────────
XPATH_SEARCH_BOX        = "/html/body/section[1]/main/section/section[1]/div[2]/div/div/form/div/div/div[2]/div[2]/div/input"
XPATH_TYPE_DROPDOWN     = "/html/body/section[1]/main/section[1]/div/div/section[2]/div[1]/div[2]/div/button"
XPATH_OPTION_LEASE      = "/html/body/section[1]/main/section[1]/div/div/section[2]/div[1]/div[2]/div/ul/li[1]/button"
XPATH_OPTION_SALE       = "/html/body/section[1]/main/section[1]/div/div/section[2]/div[1]/div[2]/div/ul/li[2]/button"
XPATH_LISTING_NAME      = "/html/body/section[1]/main/section[1]/div/section/section[1]/div[3]/ul[1]/li[1]/article/header/div[1]/h6/a"
XPATH_LISTING_LOCATION  = "/html/body/section[1]/main/section[1]/div/section/section[1]/div[3]/ul[1]/li[1]/article/header/div[2]"
XPATH_LISTING_PRICE     = "/html/body/section[1]/main/section[1]/div/section/section[1]/div[3]/ul[1]/li[1]/article/div[2]/div[2]/div/ul[1]/li[1]"
XPATH_LISTING_SPACE     = "/html/body/section[1]/main/section[1]/div/section/section[1]/div[3]/ul[1]/li[1]/article/header/div[2]/h4/a"
XPATH_LISTING_PROVINCE  = "/html/body/section[1]/main/section[1]/div/section/section[1]/div[3]/ul[1]/li[1]/article/header/div[2]/h6/a"


# ══════════════════════════════════════════════
# STEP 1 — Tkinter UI  (fixed layout)
# ══════════════════════════════════════════════

def launch_ui() -> dict | None:
    result = {}

    root = tk.Tk()
    root.title("LoopNet Scraper")
    root.resizable(False, False)
    root.configure(bg="#1a1a2e")

    # ── Colours / fonts ──────────────────────────
    BG       = "#1a1a2e"
    CARD_BG  = "#16213e"
    ACCENT   = "#e94560"
    FG       = "#e0e0e0"
    FG_DIM   = "#a0a0b0"
    FONT     = ("Segoe UI", 10)
    FONT_B   = ("Segoe UI", 10, "bold")
    FONT_H   = ("Segoe UI", 14, "bold")

    def card(parent, **kw):
        return tk.Frame(parent, bg=CARD_BG, bd=0, **kw)

    # ── Title bar ────────────────────────────────
    title_bar = tk.Frame(root, bg=ACCENT, height=4)
    title_bar.pack(fill="x")

    tk.Label(root, text="LoopNet Scraper",
             bg=BG, fg=ACCENT, font=FONT_H).pack(pady=(14, 2))
    tk.Label(root, text="Configure your search below",
             bg=BG, fg=FG_DIM, font=("Segoe UI", 9)).pack(pady=(0, 12))

    # ── Country card ─────────────────────────────
    country_card = card(root)
    country_card.pack(fill="x", padx=22, pady=(0, 10))

    tk.Label(country_card, text="  🌍  Select Country",
             bg=CARD_BG, fg=ACCENT, font=FONT_B,
             anchor="w").pack(fill="x", padx=10, pady=(10, 6))

    country_var = tk.StringVar(value="5")

    # Two columns so the card stays compact but nothing is clipped
    grid = tk.Frame(country_card, bg=CARD_BG)
    grid.pack(padx=14, pady=(0, 10))

    rb_cfg = dict(bg=CARD_BG, fg=FG, font=FONT,
                  activebackground=CARD_BG, activeforeground=ACCENT,
                  selectcolor="#0f3460", relief="flat",
                  variable=country_var)

    items = list(COUNTRIES.items())          # [("1","USA"), ...]
    cols  = 2
    for idx, (num, name) in enumerate(items):
        row_i = idx // cols
        col_i = idx % cols
        tk.Radiobutton(grid, text=f"{num}. {name}",
                       value=num, **rb_cfg).grid(
            row=row_i, column=col_i, sticky="w", padx=10, pady=3)

    # ── Listing type card ────────────────────────
    type_card = card(root)
    type_card.pack(fill="x", padx=22, pady=(0, 14))

    tk.Label(type_card, text="  🏷  Listing Type",
             bg=CARD_BG, fg=ACCENT, font=FONT_B,
             anchor="w").pack(fill="x", padx=10, pady=(10, 6))

    type_var  = tk.StringVar(value="1")
    type_row  = tk.Frame(type_card, bg=CARD_BG)
    type_row.pack(padx=14, pady=(0, 10))

    for num, name in LISTING_TYPES.items():
        tk.Radiobutton(type_row, text=f"{num}. {name}",
                       value=num, **{**rb_cfg, "variable": type_var}
                       ).pack(side="left", padx=16)

    # ── Buttons ──────────────────────────────────
    btn_row = tk.Frame(root, bg=BG)
    btn_row.pack(pady=(0, 18))

    def on_start():
        result["country"]      = COUNTRIES[country_var.get()]
        result["listing_type"] = LISTING_TYPES[type_var.get()]
        root.destroy()

    def on_cancel():
        root.destroy()

    tk.Button(btn_row, text="▶  Start Scraping",
              command=on_start,
              bg=ACCENT, fg="white", font=FONT_B,
              relief="flat", cursor="hand2",
              padx=18, pady=8).pack(side="left", padx=8)

    tk.Button(btn_row, text="Cancel",
              command=on_cancel,
              bg="#333355", fg=FG, font=FONT,
              relief="flat", cursor="hand2",
              padx=14, pady=8).pack(side="left", padx=8)

    # Auto-size window to content
    root.update_idletasks()
    root.geometry(f"{root.winfo_reqwidth() + 20}x{root.winfo_reqheight() + 10}")
    root.mainloop()

    return result if result else None


# ══════════════════════════════════════════════
# HUMAN BEHAVIOR HELPERS
# ══════════════════════════════════════════════

async def human_delay(page, min_ms=800, max_ms=2200):
    await page.wait_for_timeout(random.randint(min_ms, max_ms))


async def human_type(page, locator, text: str):
    for char in text:
        await locator.type(char, delay=random.randint(80, 220))
        if random.random() < 0.07:
            await page.wait_for_timeout(random.randint(150, 500))


async def human_move_and_click(page, locator):
    await locator.scroll_into_view_if_needed()
    await locator.hover()
    await page.wait_for_timeout(random.randint(100, 350))
    await locator.click()


async def simulate_human_presence(page):
    vp = page.viewport_size or {"width": 1280, "height": 900}
    w, h = vp["width"], vp["height"]
    for _ in range(random.randint(4, 8)):
        await page.mouse.move(
            random.randint(100, w - 100),
            random.randint(100, h - 100),
            steps=random.randint(10, 25),
        )
        await page.wait_for_timeout(random.randint(80, 220))
    await page.mouse.wheel(0, random.randint(60, 200))
    await page.wait_for_timeout(random.randint(200, 500))
    await page.mouse.wheel(0, -random.randint(30, 100))


# ══════════════════════════════════════════════
# BROWSER — stealth
# ══════════════════════════════════════════════

async def build_browser(pw):
    browser = await pw.chromium.launch(
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-infobars",
            "--disable-extensions",
            "--window-size=1280,900",
        ],
    )
    context = await browser.new_context(
        viewport={"width": 1280, "height": 900},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        ),
        locale="en-US",
        timezone_id="America/Chicago",
        extra_http_headers={
            "Accept-Language":           "en-US,en;q=0.9",
            "Accept-Encoding":           "gzip, deflate, br",
            "Accept":                    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest":            "document",
            "Sec-Fetch-Mode":            "navigate",
            "Sec-Fetch-Site":            "none",
            "Sec-Fetch-User":            "?1",
        },
    )
    await context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver',  { get: () => undefined });
        Object.defineProperty(navigator, 'plugins',    { get: () => [1,2,3,4,5] });
        Object.defineProperty(navigator, 'languages',  { get: () => ['en-US','en'] });
        window.chrome = { runtime: {} };
        const _orig = window.navigator.permissions.query;
        window.navigator.permissions.query = (p) =>
            p.name === 'notifications'
                ? Promise.resolve({ state: Notification.permission })
                : _orig(p);
    """)
    return browser, context


# ══════════════════════════════════════════════
# STEP 2 — Search
# ══════════════════════════════════════════════

async def search_loopnet(page, country: str):
    print(f"\n[2] Navigating to LoopNet …")
    await page.goto("https://www.loopnet.com", wait_until="domcontentloaded")
    await simulate_human_presence(page)
    await human_delay(page, 1800, 3200)

    print(f"[2] Typing '{country}' into search box …")
    search_box = page.locator(f"xpath={XPATH_SEARCH_BOX}")
    await search_box.wait_for(state="visible", timeout=15000)
    await human_move_and_click(page, search_box)
    await human_delay(page, 400, 800)
    await human_type(page, search_box, country)
    await human_delay(page, 600, 1200)

    print("[2] Pressing Enter …")
    await search_box.press("Enter")
    await human_delay(page, 3000, 5000)
    print("[2] ✓ Search submitted")


# ══════════════════════════════════════════════
# STEP 3 — Select Lease / Sale
# ══════════════════════════════════════════════

async def select_listing_type(page, listing_type: str):
    print(f"\n[3] Selecting '{listing_type}' …")
    dropdown_btn = page.locator(f"xpath={XPATH_TYPE_DROPDOWN}")
    await dropdown_btn.wait_for(state="visible", timeout=15000)
    await human_move_and_click(page, dropdown_btn)
    await human_delay(page, 800, 1500)

    option = page.locator(f"xpath={XPATH_OPTION_LEASE if listing_type == 'For Lease' else XPATH_OPTION_SALE}")
    await option.wait_for(state="visible", timeout=10000)
    await human_move_and_click(page, option)
    await human_delay(page, 2500, 4000)
    print(f"[3] ✓ '{listing_type}' selected")


# ══════════════════════════════════════════════
# STEP 4 — Scrape first listing
# ══════════════════════════════════════════════

async def safe_text(page, xpath: str, default="N/A") -> str:
    try:
        el = page.locator(f"xpath={xpath}")
        await el.wait_for(state="visible", timeout=6000)
        return (await el.inner_text()).strip()
    except Exception:
        return default


def extract_sf(raw: str) -> str:
    match = re.search(r"[\d,\s\-\.]+SF", raw)
    return match.group(0).strip() if match else raw


def extract_province(raw: str) -> str:
    match = re.search(r",\s*([A-Z]{2})\b", raw)
    return match.group(1) if match else raw


async def scrape_first_listing(page) -> dict:
    print("\n[4] Scraping first listing …")

    name      = await safe_text(page, XPATH_LISTING_NAME)
    location  = await safe_text(page, XPATH_LISTING_LOCATION)
    price     = await safe_text(page, XPATH_LISTING_PRICE)
    space_raw = await safe_text(page, XPATH_LISTING_SPACE)
    prov_raw  = await safe_text(page, XPATH_LISTING_PROVINCE)

    space    = extract_sf(space_raw)      if space_raw != "N/A" else "N/A"
    province = extract_province(prov_raw) if prov_raw  != "N/A" else "N/A"

    listing = {
        "name":     name,
        "location": location,
        "price":    price,
        "space":    space,
        "province": province,
        "date":     str(date.today()),
    }

    print("\n" + "═" * 48)
    print("  📋  LISTING DETAILS")
    print("═" * 48)
    for k, v in listing.items():
        print(f"  {k:<12}: {v}")
    print("═" * 48)

    return listing


# ══════════════════════════════════════════════
# CSV helpers
# ══════════════════════════════════════════════

FIELDNAMES = ["name", "location", "price", "space", "province", "date"]


def save_csv(listings: list[dict], path: str):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(listings)
    print(f"\n[CSV] Saved {len(listings)} listing(s) → {path}")


def load_csv(path: str) -> list[dict]:
    if not Path(path).exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compare_and_report(previous: list[dict], current: list[dict]):
    prev_map = {r["name"]: r for r in previous}
    print("\n[COMPARE] Checking for changes …")
    for row in current:
        name = row["name"]
        if name not in prev_map:
            print(f"  🆕 NEW LISTING  : {name}")
        else:
            changes = [f for f in FIELDNAMES if f != "date" and prev_map[name].get(f) != row.get(f)]
            if changes:
                print(f"  🔄 CHANGED      : {name}")
                for field in changes:
                    print(f"       {field}: '{prev_map[name].get(field)}' → '{row.get(field)}'")
            else:
                print(f"  ✅ NO CHANGE    : {name}")


# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════

async def run_scraper(country: str, listing_type: str):
    async with async_playwright() as pw:
        browser, context = await build_browser(pw)
        page = await context.new_page()

        await search_loopnet(page, country)
        await select_listing_type(page, listing_type)
        listing = await scrape_first_listing(page)

        await browser.close()

    previous = load_csv(PREVIOUS_CSV)
    save_csv([listing], LISTINGS_CSV)
    compare_and_report(previous, [listing])
    shutil.copy(LISTINGS_CSV, PREVIOUS_CSV)
    print("\n✅ Done. Run again tomorrow to detect changes.")


def main():
    user_input = launch_ui()
    if not user_input:
        print("Cancelled.")
        return

    country      = user_input["country"]
    listing_type = user_input["listing_type"]
    print(f"\n▶ Country: {country}  |  Type: {listing_type}")

    asyncio.run(run_scraper(country, listing_type))


if __name__ == "__main__":
    main()