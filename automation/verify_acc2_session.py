import os
import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")

def get_credentials():
    username = os.getenv("INSTA_USERNAME_2", "")
    password = os.getenv("INSTA_PASSWORD_2", "")
    if not username and os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    if k == "INSTA_USERNAME_2" and not username:
                        username = v.strip()
                    elif k == "INSTA_PASSWORD_2" and not password:
                        password = v.strip()
    return username, password

def run_verification():
    username, password = get_credentials()
    user_data_dir = os.path.join(BASE_DIR, "browser_session_acc2")

    print(f"==================================================")
    print(f"🔑 Verifying & Saving Session for @{username}")
    print(f"==================================================")

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

        user_field = page.locator("input[name='email'], input[name='username']")
        if user_field.count() > 0 and user_field.first.is_visible():
            print(f"🔑 Entering login credentials for @{username}...")
            user_field.first.fill(username)
            time.sleep(1)
            pass_field = page.locator("input[name='pass'], input[name='password']").first
            pass_field.fill(password)
            time.sleep(1)
            pass_field.press("Enter")
            time.sleep(8)

        print("\n" + "="*60)
        print("ACTION REQUIRED:")
        print("Look at the Chrome browser window on your screen.")
        print("If Instagram asks for a 6-digit code, check your email (b*******u@gmail.com),")
        print("type the 6-digit code into the browser window, and click 'Continue'.")
        print("Waiting up to 3 minutes for login to complete...")
        print("="*60 + "\n")

        # Wait loop to detect successful login
        logged_in = False
        start_time = time.time()
        while time.time() - start_time < 180:
            current_url = page.url
            
            # Dismiss any 'Save Info' or 'Not Now' prompts
            for text in ["Save Info", "Save info", "Not Now", "Not now"]:
                try:
                    btn = page.get_by_text(text, exact=True)
                    if btn.count() > 0 and btn.first.is_visible():
                        print(f"Clicking '{text}' button...")
                        btn.first.click()
                        time.sleep(2)
                except Exception:
                    pass

            # Check if logged in (New post icon or user profile or homepage elements)
            if "instagram.com" in current_url and "auth_platform" not in current_url and "login" not in current_url and "accounts/onetap" not in current_url:
                create_icon = page.locator("svg[aria-label='New post'], svg[aria-label='New Post']")
                if create_icon.count() > 0 or "instagram.com/direct/" in current_url or page.locator("svg[aria-label='Home']").count() > 0:
                    print("✅ SUCCESS! Instagram login verified and session active!")
                    logged_in = True
                    break

            page.screenshot(path=os.path.join(BASE_DIR, "acc2_verification_status.png"))
            time.sleep(5)

        if logged_in:
            print("💾 Saving session data... (waiting 10 seconds)")
            time.sleep(10)
            page.screenshot(path=os.path.join(BASE_DIR, "acc2_verified_logged_in.png"))
            print("🎉 Browser session successfully saved in browser_session_acc2!")
        else:
            print("⚠️ Timeout reached (3 mins). Please check acc2_verification_status.png for current screen.")

        browser.close()

if __name__ == "__main__":
    run_verification()
