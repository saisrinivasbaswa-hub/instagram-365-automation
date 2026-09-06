import os
import sys
import json
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_JSON = os.path.join(BASE_DIR, "indian_calendar_720.json")
if not os.path.exists(POSTS_JSON):
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
    print(f"🇮🇳 Account 2 (@{username}) - POST #{day_num}")
    print(f"✨ Category: {post_item.get('category_tag', post_item.get('category', 'Culture'))}")
    print(f"💬 Quote: {post_item['quote']}")
    print(f"==========================================")

    img_name = f"day_{day_num:03d}.png"
    local_image_path = os.path.abspath(os.path.join(IMAGES_DIR, img_name))

    # If static PNG image is missing, attempt to generate it on the fly
    if not os.path.exists(local_image_path):
        print(f"Image {local_image_path} missing. Generating on the fly...")
        try:
            from PIL import Image, ImageDraw, ImageFont
            os.makedirs(IMAGES_DIR, exist_ok=True)
            img = Image.new('RGB', (1080, 1080), color=(15, 12, 28))
            draw = ImageDraw.Draw(img)
            # Decorative border
            draw.rectangle([30, 30, 1050, 1050], outline=(245, 158, 11), width=4)
            draw.text((540, 200), "🇮🇳 INDIAN TRADITIONS", fill=(245, 158, 11), anchor="mm")
            draw.text((540, 540), post_item['quote'], fill=(255, 255, 255), anchor="mm")
            img.save(local_image_path)
            print(f"Generated {local_image_path}")
        except Exception as e:
            print(f"Image generation error: {e}")

    full_caption = f"{post_item['caption']}\n\n{post_item['hashtags']}"
    user_data_dir = os.path.join(BASE_DIR, "browser_session_acc2")
    state_file = os.path.join(BASE_DIR, "session_acc2.json")

    with sync_playwright() as p:
        if os.path.exists(user_data_dir):
            print("🖥️ Using local persistent profile browser_session_acc2...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir,
                headless=False,
                viewport={"width": 1280, "height": 800}
            )
            page = browser.new_page()
        elif os.path.exists(state_file):
            print("☁️ Using cloud storage state (session_acc2.json)...")
            headless_browser = p.chromium.launch(headless=True)
            context = headless_browser.new_context(
                storage_state=state_file,
                viewport={"width": 1280, "height": 800}
            )
            page = context.new_page()
        else:
            print("⚠️ Launching fresh context...")
            headless_browser = p.chromium.launch(headless=True)
            context = headless_browser.new_context(viewport={"width": 1280, "height": 800})
            page = context.new_page()

        print("🌐 Navigating to Instagram...")
        for attempt in range(3):
            try:
                page.goto("https://www.instagram.com/", wait_until="domcontentloaded", timeout=30000)
                time.sleep(4)
                break
            except Exception as e:
                print(f"  Retry #{attempt+1} navigating to Instagram: {e}")
                time.sleep(3)

        # Check if login form is present
        user_field = page.locator("input[name='username'], input[name='email'], input[aria-label*='username'], input[aria-label*='email'], input[aria-label*='Mobile']").first
        if user_field.count() > 0 and user_field.is_visible():
            print(f"🔑 Logging in as @{username}...")
            user_field.fill(username)
            time.sleep(1)
            
            pass_field = page.locator("input[name='password'], input[name='pass'], input[type='password']").first
            pass_field.fill(password)
            time.sleep(1)

            print("⏳ Submitting login form...")
            submit_btn = page.locator("button[type='submit'], button:has-text('Log in'), div[role='button']:has-text('Log in')").first
            submit_btn.click(force=True)
            time.sleep(8)

        print("📸 Navigating Create menu...")
        for text in ["Not Now", "Not now", "Save Info", "Save info"]:
            try:
                btn = page.get_by_text(text, exact=True)
                if btn.count() > 0 and btn.first.is_visible():
                    print(f"Dismissing modal: {text}")
                    btn.first.click(force=True)
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

            for step in range(2):
                next_btn = page.locator("div[role='button']:has-text('Next'), button:has-text('Next')").first
                if next_btn.is_visible():
                    print(f"➡️ Clicking Next ({step+1}/2)...")
                    next_btn.click(force=True)
                    time.sleep(3)

            caption_area = page.locator("div[aria-label='Write a caption...'], textarea[aria-label='Write a caption...']").first
            if caption_area.is_visible():
                print("✍️ Filling caption...")
                caption_area.fill(full_caption)
                time.sleep(2)

            share_btn = page.locator("div[role='button']:has-text('Share'), button:has-text('Share')").first
            if share_btn.is_visible():
                print("🚀 Clicking Share...")
                share_btn.click(force=True)
                time.sleep(12)
                print(f"🎉 SUCCESS! Published Post #{day_num} to @{username}!")
                update_current_day(day_num + 1)
                print(f"🔄 Counter updated to Post #{day_num + 1}.")
            else:
                print("Warning: Share button not found")
        else:
            print("⚠️ Upload modal not found.")

        # Save updated state
        if os.path.exists(user_data_dir):
            browser.storage_state(path=state_file)
            print(f"💾 Storage state refreshed in {state_file}")

        browser.close()

if __name__ == "__main__":
    post_account_2()
