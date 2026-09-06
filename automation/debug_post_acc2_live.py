import os
import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
user_data_dir = os.path.join(BASE_DIR, "browser_session_acc2")
local_image_path = os.path.abspath(os.path.join(BASE_DIR, "images_indian", "day_002.png"))

print("Running live visual debug post for @indian.traditions.1...")
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
        caption_area.fill("✨ Day 2: Friendship & Roots\n\nTrue friends don't judge your past; they stand beside you to build your future.\n\n#IndianTraditions #VedicWisdom #Culture #Friendship")
        time.sleep(2)

    # Locate the exact Share button in modal top-right header
    share_btns = page.locator("div[role='button']:has-text('Share'), button:has-text('Share')")
    print(f"Number of Share button elements found: {share_btns.count()}")
    
    # Click the last visible Share button (modal header button)
    share_clicked = False
    for i in range(share_btns.count()):
        btn = share_btns.nth(i)
        if btn.is_visible():
            print(f"Clicking Share button #{i+1}...")
            btn.click(force=True)
            share_clicked = True
            break

    if share_clicked:
        print("Waiting 15 seconds for upload animation and confirmation modal...")
        time.sleep(15)
        page.screenshot(path=os.path.join(BASE_DIR, "acc2_upload_confirmation.png"))
        print("Saved acc2_upload_confirmation.png")

        # Check if 'Your post has been shared' appears
        if page.locator("text='Your post has been shared', svg[aria-label='Animated checkbox']").count() > 0:
            print("🎉 CONFIRMED! Instagram displayed 'Your post has been shared'!")
        else:
            print(f"Page state URL: {page.url}")

    browser.close()
