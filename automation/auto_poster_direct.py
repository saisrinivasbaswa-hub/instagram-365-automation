import json
import os
import sys
import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_JSON = os.path.join(BASE_DIR, "posts_365.json")
TRACKER_FILE = os.path.join(BASE_DIR, "current_day.txt")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
ENV_FILE = os.path.join(BASE_DIR, ".env")

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

def post_direct_to_instagram():
    """Direct post using instagrapi library (Username & Password)"""
    username = os.getenv("INSTA_USERNAME", "")
    password = os.getenv("INSTA_PASSWORD", "")

    # Read from local .env if available
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            for line in f:
                if "=" in line:
                    key, val = line.strip().split("=", 1)
                    if key == "INSTA_USERNAME":
                        username = val
                    elif key == "INSTA_PASSWORD":
                        password = val

    day_num = get_current_day()
    if day_num > 365:
        print("🎉 All 365 days completed!")
        return

    with open(POSTS_JSON, "r", encoding="utf-8") as f:
        posts = json.load(f)

    post_item = next((p for p in posts if p['day'] == day_num), None)
    if not post_item:
        print(f"Error: Day {day_num} not found")
        return

    print(f"\n==========================================")
    print(f"📅 Executing Post: DAY {day_num} / 365")
    print(f"💡 Topic: {post_item['category']}")
    print(f"💬 Quote: {post_item['quote']}")
    print(f"==========================================")

    local_image_path = os.path.join(IMAGES_DIR, post_item['image_filename'])
    full_caption = f"{post_item['caption']}\n\n{post_item['hashtags']}"

    if not username or not password or username == "your_username":
        print("⚠️ Missing Instagram Login Credentials.")
        print(f"   Please add your INSTA_USERNAME and INSTA_PASSWORD in: {ENV_FILE}")
        print(f"   Simulated execution successful for Day {day_num}.")
        return

    try:
        from instagrapi import Client
        cl = Client()
        cl.login(username, password)
        media = cl.photo_upload(local_image_path, caption=full_caption)
        print(f"✅ Published directly to Instagram! Media ID: {media.pk}")
        
        next_day = day_num + 1
        update_current_day(next_day)
        print(f"🔄 Day counter updated to Day {next_day}.\n")
    except ImportError:
        print("⚠️ 'instagrapi' package not installed. Run: pip install instagrapi pillow")
    except Exception as e:
        print(f"❌ Instagram login error: {e}")

if __name__ == "__main__":
    post_direct_to_instagram()
