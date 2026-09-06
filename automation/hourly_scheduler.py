import os
import sys
import time
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_hourly_poster():
    print("==================================================")
    print("⏰ Local Hourly Auto-Poster Active")
    print("==================================================")
    
    while True:
        print(f"\n🚀 Running hourly post for Account 2 (@indian.traditions.1)...")
        try:
            cmd = [sys.executable, os.path.join(BASE_DIR, "post_account_2.py")]
            res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
            print(res.stdout)
            if res.stderr:
                print(f"Error: {res.stderr}")
        except Exception as e:
            print(f"Execution error: {e}")

        print("⏳ Sleeping for 1 hour (3600 seconds) until next post...")
        time.sleep(3600)

if __name__ == "__main__":
    run_hourly_poster()
