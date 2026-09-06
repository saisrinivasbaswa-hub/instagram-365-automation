import os
import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def export_state(session_dir, output_json):
    print(f"Extracting session state from {session_dir}...")
    user_data_dir = os.path.join(BASE_DIR, session_dir)
    out_file = os.path.join(BASE_DIR, output_json)

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=True,
            viewport={"width": 1280, "height": 800}
        )
        page = browser.new_page()
        page.goto("https://www.instagram.com/", wait_until="domcontentloaded")
        
        # Export state JSON
        browser.storage_state(path=out_file)
        print(f"✅ Successfully exported storage state to: {out_file}")
        browser.close()

if __name__ == "__main__":
    if os.path.exists(os.path.join(BASE_DIR, "browser_session")):
        export_state("browser_session", "session_acc1.json")
