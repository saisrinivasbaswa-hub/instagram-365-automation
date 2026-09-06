import os
import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
session_dir = os.path.join(BASE_DIR, "browser_session_acc2")

print("==========================================")
print("🌐 Opening Browser Window for Account 2 Verification...")
print("==========================================")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        session_dir,
        headless=False,
        viewport={"width": 1280, "height": 800}
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://www.instagram.com/")
    time.sleep(3)

    user_field = page.locator("input[name='username'], input[name='email']")
    if user_field.count() > 0 and user_field.first.is_visible():
        print("🔑 Filling username and password...")
        user_field.first.fill("indian.traditions.1")
        time.sleep(1)
        pass_field = page.locator("input[name='password'], input[name='pass']").first
        pass_field.fill("Baswa@10081998")
        time.sleep(1)
        pass_field.press("Enter")
        time.sleep(5)

    print("⏳ Waiting 30 seconds for verification step...")
    time.sleep(30)
    browser.close()
