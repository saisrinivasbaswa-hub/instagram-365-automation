import time
import subprocess
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRACKER_FILE = os.path.join(BASE_DIR, "current_day.txt")

def get_current_day():
    if os.path.exists(TRACKER_FILE):
        try:
            with open(TRACKER_FILE, "r") as f:
                return int(f.read().strip())
        except ValueError:
            return 1
    return 1

print("==========================================")
print("🚀 Starting 5-Post Batch Test (1-Min Interval)")
print("==========================================")

for i in range(1, 6):
    current_day = get_current_day()
    print(f"\n📢 [POST {i}/5] Attempting to publish DAY {current_day}...")
    
    # Run browser auto poster script with UTF-8 encoding
    res = subprocess.run([sys.executable, os.path.join(BASE_DIR, "post_via_browser.py")], capture_output=True, text=True, encoding='utf-8', errors='replace')
    print(res.stdout)
    if res.stderr:
        print("Log output:", res.stderr)
        
    if i < 5:
        print(f"⏳ Waiting 60 seconds before Post {i+1}...")
        time.sleep(60)

print("==========================================")
print("🎉 5-Post Batch Test Completed Successfully!")
print("==========================================")
