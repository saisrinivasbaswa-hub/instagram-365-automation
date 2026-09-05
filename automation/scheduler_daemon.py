import time
import datetime
import schedule
import auto_poster

def job():
    print(f"⏰ [{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Triggering daily Instagram post...")
    try:
        auto_poster.execute_daily_post()
    except Exception as e:
        print(f"❌ Error during auto-post job: {e}")

# Schedule job every day at 09:00 AM
schedule.every().day.at("09:00").do(job)

print("🤖 Instagram 365-Day Scheduler Service started.")
print("   Will automatically post 1 quote every day at 09:00 AM.")
print("   Press Ctrl+C to stop.")

# Run immediately once on startup for testing
job()

while True:
    schedule.run_pending()
    time.sleep(60)
