import os
import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
user_data_dir = os.path.join(BASE_DIR, "browser_session_acc2")

print("Checking profile of @indian.traditions.1 live...")
with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,
        viewport={"width": 1280, "height": 800}
    )
    page = browser.new_page()

    page.goto("https://www.instagram.com/indian.traditions.1/", wait_until="domcontentloaded")
    time.sleep(5)
    
    page.screenshot(path=os.path.join(BASE_DIR, "acc2_profile_live.png"))
    print("Saved live profile screenshot: acc2_profile_live.png")
    
    # Check post elements on profile page
    posts = page.locator("article a[href*='/p/'], article a[href*='/reel/']")
    print(f"Number of post links found on profile page: {posts.count()}")
    for i in range(min(posts.count(), 5)):
        print(f"  Post #{i+1} URL: {posts.nth(i).get_attribute('href')}")

    browser.close()
