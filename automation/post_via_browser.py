import os
import sys
import json
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_JSON = os.path.join(BASE_DIR, "posts_365.json")
TRACKER_FILE = os.path.join(BASE_DIR, "current_day.txt")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
ENV_FILE = os.path.join(BASE_DIR, ".env")

def get_credentials():
    username = os.getenv("INSTA_USERNAME", "")
    password = os.getenv("INSTA_PASSWORD", "")
    if not username and os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    if k == "INSTA_USERNAME" and not username:
                        username = v.strip()
                    elif k == "INSTA_PASSWORD" and not password:
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

def post_via_playwright():
    username, password = get_credentials()
    day_num = get_current_day()

    with open(POSTS_JSON, "r", encoding="utf-8") as f:
        posts = json.load(f)

    post_item = next((p for p in posts if p['day'] == day_num), None)
    if not post_item:
        print(f"Error: Day {day_num} not found")
        return

    print(f"==========================================")
    print(f"📅 Browser Auto-Poster: DAY {day_num} / 365")
    print(f"💡 Topic: {post_item['category']}")
    print(f"💬 Quote: {post_item['quote']}")
    print(f"==========================================")

    local_image_path = os.path.abspath(os.path.join(IMAGES_DIR, post_item['image_filename']))
    full_caption = f"{post_item['caption']}\n\n{post_item['hashtags']}"

    user_data_dir = os.path.join(BASE_DIR, "browser_session")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            viewport={"width": 1280, "height": 800}
        )
        page = browser.new_page()

        print("🌐 Navigating to Instagram...")
        for attempt in range(3):
            try:
                page.goto("https://www.instagram.com/", wait_until="domcontentloaded", timeout=30000)
                time.sleep(4)
                break
            except Exception as e:
                print(f"  Retry #{attempt+1} navigating to Instagram: {e}")
                time.sleep(3)

        # Fill Login Credentials if needed
        user_field = page.locator("input[name='email'], input[name='username']").first
        if user_field.count() > 0 and user_field.is_visible():
            print(f"🔑 Logging in as @{username}...")
            user_field.fill(username)
            time.sleep(1)
            
            pass_field = page.locator("input[name='pass'], input[name='password']").first
            pass_field.fill(password)
            time.sleep(1)

            print("⏳ Submitting login form via Enter key...")
            pass_field.press("Enter")
            time.sleep(10)

        print("📸 Navigating Create menu...")
        for text in ["Not Now", "Not now", "Save Info", "Save info"]:
            try:
                btn = page.get_by_text(text, exact=True)
                if btn.count() > 0 and btn.first.is_visible():
                    print(f"Dismissing modal: {text}")
                    btn.first.click()
                    time.sleep(2)
            except Exception:
                pass

        try:
            create_icon = page.locator("svg[aria-label='New post'], svg[aria-label='New Post']").first
            if create_icon.is_visible():
                print("➕ Clicking '+' Create icon...")
                create_icon.click(force=True)
                time.sleep(2)
        except Exception:
            pass

        try:
            post_sub = page.get_by_text("Post", exact=True)
            if post_sub.count() > 0 and post_sub.first.is_visible():
                print("🖼️ Clicking 'Post' submenu option...")
                post_sub.first.click(force=True)
                time.sleep(3)
        except Exception:
            pass

        file_input = page.locator("input[type='file']")
        if file_input.count() > 0:
            print(f"📁 Uploading image file: {local_image_path}")
            file_input.first.set_input_files(local_image_path)
            time.sleep(4)

            # Click 'Next' twice with force=True
            for step in range(2):
                next_btn = page.locator("div[role='button']:has-text('Next'), button:has-text('Next')").first
                if next_btn.is_visible():
                    print(f"➡️ Clicking Next ({step+1}/2)...")
                    next_btn.click(force=True)
                    time.sleep(3)

            # Write Caption
            print("✍️ Filling caption...")
            caption_area = page.locator("div[aria-label='Write a caption...'], textarea[aria-label='Write a caption...']").first
            if caption_area.is_visible():
                caption_area.fill(full_caption)
                time.sleep(2)

            # Click Share with force=True
            print("🚀 Clicking Share...")
            share_btn = page.locator("div[role='button']:has-text('Share'), button:has-text('Share')").first
            if share_btn.is_visible():
                share_btn.click(force=True)
                print("⏳ Publishing post to Instagram...")
                time.sleep(12)

                print(f"🎉 SUCCESS! Published Day {day_num} successfully to Instagram!")
                next_day = day_num + 1
                update_current_day(next_day)
                print(f"🔄 Day counter updated to Day {next_day}.\n")
            else:
                print("Warning: Share button not found")
        else:
            print("⚠️ Uploader modal did not open. Saving final screenshot...")
            page.screenshot(path=os.path.join(BASE_DIR, "final_status.png"))

        browser.close()

if __name__ == "__main__":
    post_via_playwright()
