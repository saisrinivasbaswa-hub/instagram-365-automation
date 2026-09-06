import os
import sys
import time
import schedule
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def job():
    print(f"\n==========================================")
    print(f"⏰ Scheduled Daily Auto-Post Triggered at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"==========================================")
    
    print("🚀 Running Account 1 poster...")
    p1 = subprocess.run([sys.executable, os.path.join(BASE_DIR, "post_via_browser.py")], capture_output=True, text=True)
    print(p1.stdout)
    if p1.stderr:
        print(p1.stderr)
        
    time.sleep(10)
    
    print("🚀 Running Account 2 poster...")
    p2 = subprocess.run([sys.executable, os.path.join(BASE_DIR, "post_account_2.py")], capture_output=True, text=True)
    print(p2.stdout)
    if p2.stderr:
        print(p2.stderr)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--now":
        print("⚡ Running immediate post now...")
        job()
    else:
        print("📅 Starting 365-Day Instagram Auto-Poster Background Loop...")
        print("⏰ Scheduled daily posting time: 23:00 (11:00 PM)")
        schedule.every().day.at("23:00").do(job)
        
        while True:
            schedule.run_pending()
            time.sleep(30)
