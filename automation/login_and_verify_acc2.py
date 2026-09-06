import os
import sys
import json
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_JSON = os.path.join(BASE_DIR, "indian_calendar_365.json")
TRACKER_FILE = os.path.join(BASE_DIR, "current_day_indian.txt")
IMAGES_DIR = os.path.join(BASE_DIR, "images_indian")
ENV_FILE = os.path.join(BASE_DIR, ".env")

CODE_TO_ENTER = "011729"

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

def get_current_day():
    if os.path.exists(TRACKER_FILE):
        try:
            with open(TRACKER_FILE, "r") as f:
                return int(f.read().strip())
        except ValueError:
            return 1
    return 1

def update_current_day(next_day):
    with open(TRACKER_FILE, "w") as f:
        f.write(str(next_day))

def main():
    username, password = get_credentials()
    user_data_dir = os.path.join(BASE_DIR, "browser_session_acc2")

    print(f"==================================================")
    print(f"🚀 Account 2 (@{username}) Automated Login & Verification")
    print(f"==================================================")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            viewport={"width": 1280, "height": 800}
        )
        page = browser.new_page()

        print("🌐 Step 1: Navigating to Instagram...")
        page.goto("https://www.instagram.com/", wait_until="domcontentloaded")
        time.sleep(4)

        user_loc = page.locator("input[name='username'], input[name='email'], input[aria-label*='username'], input[aria-label*='email'], input[aria-label*='Mobile']")
        if user_loc.count() > 0 and user_loc.first.is_visible():
            print(f"🔑 Step 2: Entering username '@{username}'...")
            user_loc.first.fill(username)
            time.sleep(1)

            pass_loc = page.locator("input[name='password'], input[name='pass'], input[type='password']").first
            print("🔑 Entering password...")
            pass_loc.fill(password)
            time.sleep(1)

            submit_loc = page.locator("button[type='submit'], button:has-text('Log in'), div[role='button']:has-text('Log in')").first
            print("⏳ Submitting login form...")
            submit_loc.click()
            time.sleep(8)

        page.screenshot(path=os.path.join(BASE_DIR, "acc2_login_status.png"))
        print(f"Current page URL: {page.url}")

        # Handle Verification Code Screen
        code_input = page.locator("input[name='verificationCode'], input[placeholder='Code'], input[aria-label='Code'], input[type='text'], input").first
        if "codeentry" in page.url or "challenge" in page.url or (code_input.count() > 0 and code_input.is_visible()):
            print(f"📥 Step 3: Entering 6-digit code '{CODE_TO_ENTER}'...")
            if code_input.is_visible():
                code_input.fill(CODE_TO_ENTER)
                time.sleep(1)
                
                cont_btn = page.locator("button:has-text('Continue'), div[role='button']:has-text('Continue'), button:has-text('Confirm')").first
                if cont_btn.is_visible():
                    print("Clicking Continue...")
                    cont_btn.click()
                else:
                    code_input.press("Enter")
                time.sleep(8)

        page.screenshot(path=os.path.join(BASE_DIR, "acc2_status_2.png"))

        # Handle modals ("Save Info", "Not Now")
        for text in ["Save Info", "Save info", "Not Now", "Not now"]:
            try:
                btn = page.get_by_text(text, exact=True)
                if btn.count() > 0 and btn.first.is_visible():
                    print(f"Dismissing modal: {text}")
                    btn.first.click()
                    time.sleep(2)
            except Exception:
                pass

        # Check if logged in
        create_icon = page.locator("svg[aria-label='New post'], svg[aria-label='New Post']").first
        if create_icon.is_visible() or "instagram.com/direct/" in page.url or page.locator("svg[aria-label='Home']").count() > 0:
            print("✅ SUCCESS! Instagram Login & Session Verified!")
        else:
            print(f"Page state URL: {page.url}")

        # Post Day 2
        day_num = get_current_day()
        print(f"\n==========================================")
        print(f"🇮🇳 Account 2 (@{username}) - DAY {day_num} / 365 POSTING")
        print(f"==========================================")

        with open(POSTS_JSON, "r", encoding="utf-8") as f:
            posts = json.load(f)

        post_item = next((p for p in posts if p['day'] == day_num), None)
        if not post_item:
            print(f"Error: Day {day_num} not found in JSON")
            browser.close()
            return

        img_name = f"day_{day_num:03d}.png"
        local_image_path = os.path.abspath(os.path.join(IMAGES_DIR, img_name))

        if not os.path.exists(local_image_path):
            print(f"Error: Image {local_image_path} not found")
            browser.close()
            return

        full_caption = f"{post_item['caption']}\n\n{post_item['hashtags']}"

        try:
            if not create_icon.is_visible():
                page.goto("https://www.instagram.com/", wait_until="domcontentloaded")
                time.sleep(4)
                create_icon = page.locator("svg[aria-label='New post'], svg[aria-label='New Post']").first

            if create_icon.is_visible():
                print("➕ Clicking '+' Create icon...")
                create_icon.click()
                time.sleep(2)
        except Exception as e:
            print(f"Create icon interaction error: {e}")

        try:
            post_sub = page.get_by_text("Post", exact=True)
            if post_sub.count() > 0 and post_sub.first.is_visible():
                print("🖼️ Clicking 'Post' submenu option...")
                post_sub.first.click()
                time.sleep(3)
        except Exception:
            pass

        file_input = page.locator("input[type='file']")
        if file_input.count() > 0:
            print(f"📁 Uploading image file: {local_image_path}")
            file_input.first.set_input_files(local_image_path)
            time.sleep(4)

        for step in range(2):
            next_btn = page.locator("div[role='button']:has-text('Next'), button:has-text('Next')").first
            if next_btn.is_visible():
                print(f"➡️ Clicking Next ({step+1}/2)...")
                next_btn.click()
                time.sleep(3)

        caption_area = page.locator("div[aria-label='Write a caption...'], textarea[aria-label='Write a caption...']").first
        if caption_area.is_visible():
            print("✍️ Filling caption...")
            caption_area.fill(full_caption)
            time.sleep(2)

        share_btn = page.locator("div[role='button']:has-text('Share'), button:has-text('Share')").first
        if share_btn.is_visible():
            print("🚀 Clicking Share...")
            share_btn.click()
            time.sleep(10)
            print(f"🎉 SUCCESS! Published Day {day_num} to @{username}!")
            update_current_day(day_num + 1)
            print(f"🔄 Day counter updated to Day {day_num + 1}.")
            page.screenshot(path=os.path.join(BASE_DIR, "acc2_final_status.png"))
        else:
            print("Warning: Share button not found")
            page.screenshot(path=os.path.join(BASE_DIR, "acc2_final_status.png"))

        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    main()
