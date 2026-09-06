import os
import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
user_data_dir = os.path.join(BASE_DIR, "browser_session_acc2")
state_file = os.path.join(BASE_DIR, "session_acc2.json")

def main():
    print("==================================================")
    print("🇮🇳 Account 2 (@indian.traditions.1) - One-Time Session Saver")
    print("==================================================")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            viewport={"width": 1280, "height": 800}
        )
        page = browser.new_page()

        print("🌐 Opening Instagram...")
        page.goto("https://www.instagram.com/", wait_until="domcontentloaded")
        time.sleep(4)

        user_loc = page.locator("input[name='username'], input[name='email'], input[aria-label*='username'], input[aria-label*='email'], input[aria-label*='Mobile']")
        if user_loc.count() > 0 and user_loc.first.is_visible():
            print("Entering credentials for @indian.traditions.1...")
            user_loc.first.fill("indian.traditions.1")
            time.sleep(1)
            pass_loc = page.locator("input[name='password'], input[name='pass'], input[type='password']").first
            pass_loc.fill("Baswa@10081998")
            time.sleep(1)
            submit_btn = page.locator("button[type='submit'], button:has-text('Log in'), div[role='button']:has-text('Log in')").first
            submit_btn.click()

        print("\n" + "🌟 "*15)
        print("INSTRUCTIONS FOR YOU:")
        print("1. Look at the Chrome browser window on your screen.")
        print("2. If Instagram asks for a code, enter the fresh email code.")
        print("3. Click 'Save Info' or 'Not Now' so you reach the Instagram Home Feed.")
        print("The script is watching and will automatically save session_acc2.json as soon as you are logged in!")
        print("🌟 "*15 + "\n")

        while True:
            for text in ["Save Info", "Save info", "Not Now", "Not now"]:
                try:
                    btn = page.get_by_text(text, exact=True)
                    if btn.count() > 0 and btn.first.is_visible():
                        print(f"Dismissing modal: '{text}'...")
                        btn.first.click(force=True)
                        time.sleep(2)
                except Exception:
                    pass

            create_icon = page.locator("svg[aria-label='New post'], svg[aria-label='New Post']").first
            if create_icon.count() > 0 or "instagram.com/direct/" in page.url or page.locator("svg[aria-label='Home']").count() > 0:
                print("\n🎉 SUCCESS! You are logged in!")
                print("💾 Exporting storage state to session_acc2.json...")
                time.sleep(5)
                browser.storage_state(path=state_file)
                print(f"✅ Created {state_file} successfully!")
                break
            time.sleep(3)

        browser.close()

if __name__ == "__main__":
    main()
