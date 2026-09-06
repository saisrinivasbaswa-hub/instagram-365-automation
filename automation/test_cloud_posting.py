import os
import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
state_file = os.path.join(BASE_DIR, "session_acc1.json")

print("🧪 Testing Cloud Runner Execution with session_acc1.json...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(storage_state=state_file, viewport={"width": 1280, "height": 800})
    page = context.new_page()
    page.goto("https://www.instagram.com/", wait_until="domcontentloaded")
    time.sleep(5)

    create_icon = page.locator("svg[aria-label='New post'], svg[aria-label='New Post']")
    if create_icon.count() > 0 or "instagram.com/direct/" in page.url:
        print("🎉 SUCCESS! Cloud storage state session_acc1.json is 100% authenticated and active headlessly!")
    else:
        print(f"⚠️ Page URL: {page.url}")

    browser.close()
