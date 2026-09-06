import os
import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
user_data_dir = os.path.join(BASE_DIR, "browser_session_acc2")

print("Launching Playwright Chrome for Account 2...")
with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,
        viewport={"width": 1280, "height": 800}
    )
    page = browser.new_page()
    
    print("Step 1: Navigating to instagram.com...")
    page.goto("https://www.instagram.com/", wait_until="domcontentloaded")
    time.sleep(5)
    page.screenshot(path=os.path.join(BASE_DIR, "step1_home.png"))
    print(f"URL: {page.url}")

    user_field = page.locator("input[name='username']")
    if user_field.count() > 0 and user_field.first.is_visible():
        print("Step 2: Entering username and password...")
        user_field.first.fill("indian.traditions.1")
        time.sleep(1)
        pass_field = page.locator("input[name='password']").first
        pass_field.fill("Baswa@10081998")
        time.sleep(1)
        
        login_btn = page.locator("button[type='submit']").first
        if login_btn.is_visible():
            print("Clicking Log in button...")
            login_btn.click()
        else:
            pass_field.press("Enter")
            
        time.sleep(10)
        page.screenshot(path=os.path.join(BASE_DIR, "step2_after_submit.png"))
        print(f"URL after submit: {page.url}")
    else:
        print("Username input not visible. Already logged in?")

    time.sleep(5)
    browser.close()
