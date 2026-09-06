import os
import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
user_data_dir = os.path.join(BASE_DIR, "browser_session_acc2")
local_image_path = os.path.abspath(os.path.join(BASE_DIR, "images_indian", "day_002.png"))

print("Testing exact modal header Share button click...")
with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,
        viewport={"width": 1280, "height": 800}
    )
    page = browser.new_page()

    page.goto("https://www.instagram.com/", wait_until="domcontentloaded")
    time.sleep(5)

    for text in ["Not Now", "Not now", "Save Info", "Save info"]:
        try:
            btn = page.get_by_text(text, exact=True)
            if btn.count() > 0 and btn.first.is_visible():
                btn.first.click(force=True)
                time.sleep(2)
        except Exception:
            pass

    create_icon = page.locator("svg[aria-label='New post'], svg[aria-label='New Post']").first
    if create_icon.is_visible():
        print("Clicking Create icon...")
        create_icon.click(force=True)
        time.sleep(2)

    post_sub = page.get_by_text("Post", exact=True)
    if post_sub.count() > 0 and post_sub.first.is_visible():
        print("Clicking Post option...")
        post_sub.first.click(force=True)
        time.sleep(3)

    file_input = page.locator("input[type='file']")
    if file_input.count() > 0:
        print(f"Uploading image: {local_image_path}")
        file_input.first.set_input_files(local_image_path)
        time.sleep(4)

    for step in range(2):
        next_btn = page.locator("div[role='button']:has-text('Next'), button:has-text('Next')").first
        if next_btn.is_visible():
            print(f"Clicking Next step {step+1}...")
            next_btn.click(force=True)
            time.sleep(3)

    caption_area = page.locator("div[aria-label='Write a caption...'], textarea[aria-label='Write a caption...']").first
    if caption_area.is_visible():
        print("Filling caption...")
        caption_area.fill("✨ Day 2: Indian Culture & Traditions\n\nTrue friends don't judge your past; they stand beside you to build your future.\n\n#IndianTraditions #VedicWisdom #Culture")
        time.sleep(2)

    # TARGET THE EXACT MODAL HEADER SHARE BUTTON
    # Look for button or div inside div[role='dialog'] header area
    print("Finding exact top-right header Share button in upload dialog...")
    dialog = page.locator("div[role='dialog']")
    
    # Try finding top header button directly
    share_btn = dialog.locator("header div[role='button']:has-text('Share'), header button:has-text('Share'), div[role='button']:has-text('Share')").last
    if share_btn.is_visible():
        print("Found modal header Share button! Clicking...")
        share_btn.click(force=True)
        time.sleep(12)
        page.screenshot(path=os.path.join(BASE_DIR, "exact_share_success.png"))
        print("Saved exact_share_success.png screenshot!")

    browser.close()
