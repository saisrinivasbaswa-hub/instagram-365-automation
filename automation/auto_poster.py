import json
import os
import sys
import time
import datetime
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


# CONFIGURATION
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "YOUR_INSTAGRAM_ACCOUNT_ID")
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "YOUR_META_GRAPH_API_ACCESS_TOKEN")
PUBLIC_IMAGE_SERVER = os.getenv("PUBLIC_IMAGE_SERVER", "https://your-domain-or-gcs.com/images/")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSTS_JSON = os.path.join(BASE_DIR, "posts_365.json")
TRACKER_FILE = os.path.join(BASE_DIR, "current_day.txt")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

def get_current_day():
    """Reads current day index from tracker file or defaults to Day 1."""
    if os.path.exists(TRACKER_FILE):
        try:
            with open(TRACKER_FILE, "r") as f:
                return int(f.read().strip())
        except ValueError:
            return 1
    return 1

def update_current_day(next_day):
    """Saves the next day index to tracker file."""
    with open(TRACKER_FILE, "w") as f:
        f.write(str(next_day))

def post_to_instagram_graph_api(image_url, caption):
    """
    Posts to Instagram using Meta Graph API:
    Step 1: Create Container
    Step 2: Publish Container
    """
    if INSTAGRAM_ACCOUNT_ID == "YOUR_INSTAGRAM_ACCOUNT_ID" or ACCESS_TOKEN == "YOUR_META_GRAPH_API_ACCESS_TOKEN":
        print("⚠️ Instagram API Credentials not configured.")
        print(f"   Simulated Post Successful for Image: {image_url}")
        return True

    # Step 1: Create Media Container
    container_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media"
    container_payload = {
        'image_url': image_url,
        'caption': caption,
        'access_token': ACCESS_TOKEN
    }
    
    response = requests.post(container_url, data=container_payload)
    res_data = response.json()
    
    if 'id' not in res_data:
        print(f"❌ Error creating media container: {res_data}")
        return False
        
    creation_id = res_data['id']
    print(f"📦 Container created with ID: {creation_id}. Waiting for processing...")
    time.sleep(10) # Wait 10 seconds for Meta processing

    # Step 2: Publish Container
    publish_url = f"https://graph.facebook.com/v18.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    publish_payload = {
        'creation_id': creation_id,
        'access_token': ACCESS_TOKEN
    }
    
    pub_response = requests.post(publish_url, data=publish_payload)
    pub_data = pub_response.json()
    
    if 'id' in pub_data:
        print(f"✅ Published successfully! Post ID: {pub_data['id']}")
        return True
    else:
        print(f"❌ Error publishing media: {pub_data}")
        return False

def execute_daily_post():
    day_num = get_current_day()
    if day_num > 365:
        print("🎉 All 365 days of posts have been completed!")
        return

    with open(POSTS_JSON, "r", encoding="utf-8") as f:
        posts = json.load(f)

    post_item = next((p for p in posts if p['day'] == day_num), None)
    if not post_item:
        print(f"Error: Could not find Day {day_num} in posts_365.json")
        return

    print(f"\n==========================================")
    print(f"📅 Executing Scheduled Post: DAY {day_num} / 365")
    print(f"💡 Topic: {post_item['category']}")
    print(f"💬 Quote: {post_item['quote']}")
    print(f"==========================================")

    image_filename = post_item['image_filename']
    local_image_path = os.path.join(IMAGES_DIR, image_filename)

    if not os.path.exists(local_image_path):
        print(f"⚠️ Image file {local_image_path} does not exist. Run generate_all_images.py first!")
        return

    full_caption = f"{post_item['caption']}\n\n{post_item['hashtags']}"
    image_url = f"{PUBLIC_IMAGE_SERVER.rstrip('/')}/{image_filename}"

    success = post_to_instagram_graph_api(image_url, full_caption)
    
    if success:
        next_day = day_num + 1
        update_current_day(next_day)
        print(f"🔄 Progress saved. Tomorrow will post Day {next_day}.\n")

if __name__ == "__main__":
    print(f"🤖 Instagram Auto-Poster Bot initialized at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    execute_daily_post()
