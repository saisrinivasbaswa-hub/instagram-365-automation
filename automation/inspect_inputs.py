import os
import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
user_data_dir = os.path.join(BASE_DIR, "browser_session")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,
        viewport={"width": 1280, "height": 800}
    )
    page = browser.new_page()
    print("🌐 Navigating to Instagram...")
    page.goto("https://www.instagram.com/accounts/login/", wait_until="networkidle")
    time.sleep(5)

    print("🔎 Searching for input elements...")
    inputs = page.locator("input").all()
    print(f"Found {len(inputs)} input elements:")
    for idx, inp in enumerate(inputs):
        try:
            name = inp.get_attribute("name")
            aria = inp.get_attribute("aria-label")
            type_attr = inp.get_attribute("type")
            print(f"  Input #{idx}: name='{name}', aria-label='{aria}', type='{type_attr}'")
        except Exception as e:
            print(f"  Input #{idx}: error {e}")

    browser.close()
