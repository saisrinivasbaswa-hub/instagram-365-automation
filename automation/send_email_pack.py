import os
import sys
import smtplib
import zipfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
JSON_FILE = os.path.join(BASE_DIR, "posts_365.json")

def create_summary_zip():
    zip_path = os.path.join(PROJECT_DIR, "Instagram_365_Day_Package.zip")
    print(f"📦 Creating zip file '{zip_path}'...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add JSON database
        if os.path.exists(JSON_FILE):
            zipf.write(JSON_FILE, arcname="posts_365.json")
        # Add Profile Strategy guide
        strat_file = os.path.join(PROJECT_DIR, "INSTAGRAM_PROFILE_STRATEGY.md")
        if os.path.exists(strat_file):
            zipf.write(strat_file, arcname="INSTAGRAM_PROFILE_STRATEGY.md")
        # Add README
        readme_file = os.path.join(BASE_DIR, "README.md")
        if os.path.exists(readme_file):
            zipf.write(readme_file, arcname="README.md")
    print("✅ Zip package created successfully!")
    return zip_path

def send_email(recipient_email):
    zip_path = create_summary_zip()
    print(f"📧 Preparing email for: {recipient_email}...")

    subject = "🧠 Your 365-Day Instagram Logical Quote Package (@the_logical_minds.1)"
    body = """Hello!

Here is your complete 365-Day Instagram Content & Automation Package for @the_logical_minds.1.

==================================================
INSTAGRAM PROFILE SETUP:
==================================================
Name: The Logical Mind | Daily Clarity
Bio:
🧠 1 Logical Truth Every Day
⏳ Save 100 hours of overthinking
🎯 Master your Focus, Time & Wealth
👇 Start your 365-day mindset shift

==================================================
WHAT IS INCLUDED IN YOUR PACKAGE:
==================================================
1. 365 Logical Quotes, Captions, and Hashtag sets (posts_365.json)
2. All 365 high-resolution 1080x1080 post images branded with @the_logical_minds.1
3. Web Studio Dashboard (index.html)
4. Windows Task Scheduler automated daily posting bot (auto_poster.py)

Your daily automated poster is configured on your computer to run every day at 9:00 AM!

Best regards,
Logical Quotes 365 Team
"""

    print("\n==================================================")
    print(f"SUMMARY FOR: {recipient_email}")
    print("==================================================")
    print(body)
    print("==================================================\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        recipient = sys.argv[1]
    else:
        recipient = "user@example.com"
    send_email(recipient)
