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

def post_account_2():
    username, password = get_credentials()
    day_num = get_current_day()

    if not os.path.exists(POSTS_JSON):
        print(f"Error: Dataset {POSTS_JSON} not found!")
        return

    with open(POSTS_JSON, "r", encoding="utf-8") as f:
        posts = json.load(f)

    post_item = next((p for p in posts if p['day'] == day_num), None)
    if not post_item:
        print(f"Error: Day {day_num} not found in Indian Calendar")
        return

    print(f"==========================================")
    print(f"🇮🇳 Account 2 (@indian.traditions.1) - DAY {day_num} / 365")
    print(f"✨ Category: {post_item.get('category_tag', post_item['category'])}")
    print(f"💬 Quote: {post_item['quote']}")
    print(f"==========================================")

    img_name = f"day_{day_num:03d}.png"
    img_path = os.path.join(IMAGES_DIR, img_name)

    if not os.path.exists(img_path):
        print(f"Error: Image file {img_path} not found!")
        return

    full_caption = f"{post_item['caption']}\n\n{post_item['hashtags']}"

    session_dir = os.path.join(BASE_DIR, "browser_session_acc2")

    with sync_playwright() as p:
        print("🌐 Navigating to Instagram...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=session_dir,
            headless=True,
            viewport={'width': 1280, 'height': 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.pages[0] if context.pages else context.new_page()

        page.goto("https://www.instagram.com/", wait_until="networkidle")
        time.sleep(3)

        if "login" in page.url or page.locator("input[name='username']").is_visible():
            print(f"🔑 Logging into Account 2 (@{username})...")
            page.fill("input[name='username']", username)
            page.fill("input[name='password']", password)
            page.click("button[type='submit']")
            page.wait_for_load_state("networkidle")
            time.sleep(5)

        print("📸 Navigating Create menu...")
        create_btn = page.locator("svg[aria-label='New post'], svg[aria-label='Create']").first
        if create_btn.is_visible():
            create_btn.click()
            time.sleep(2)

        file_input = page.locator("input[type='file']")
        if file_input.is_visible():
            print(f"📁 Uploading image file: {img_path}")
            file_input.set_input_files(img_path)
            time.sleep(3)

        next_btn = page.locator("div[role='button']:has-text('Next'), button:has-text('Next')").first
        if next_btn.is_visible():
            print("➡️ Clicking Next...")
            next_btn.click()
            time.sleep(2)

        next_btn2 = page.locator("div[role='button']:has-text('Next'), button:has-text('Next')").first
        if next_btn2.is_visible():
            print("➡️ Clicking Next...")
            next_btn2.click()
            time.sleep(2)

        caption_area = page.locator("div[aria-label='Write a caption...'], textarea[aria-label='Write a caption...']").first
        if caption_area.is_visible():
            print("✍️ Filling caption...")
            caption_area.fill(full_caption)
            time.sleep(2)

        share_btn = page.locator("div[role='button']:has-text('Share'), button:has-text('Share')").first
        if share_btn.is_visible():
            print("🚀 Clicking Share...")
            share_btn.click()
            time.sleep(8)
            print(f"🎉 SUCCESS! Published Day {day_num} to @indian.traditions.1!")
            update_current_day(day_num + 1)
            print(f"🔄 Day counter updated to Day {day_num + 1}.")
        else:
            print("Warning: Share button not found")

        context.close()

if __name__ == "__main__":
    post_account_2()
