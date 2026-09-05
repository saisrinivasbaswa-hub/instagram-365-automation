import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")

def update_profile():
    username = ""
    password = ""

    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            for line in f:
                if "=" in line:
                    key, val = line.strip().split("=", 1)
                    if key == "INSTA_USERNAME":
                        username = val
                    elif key == "INSTA_PASSWORD":
                        password = val

    if not username or not password:
        print("❌ Username or password missing in .env file.")
        return

    print(f"🔄 Logging into Instagram as @{username}...")

    try:
        from instagrapi import Client
        cl = Client()
        cl.login(username, password)
        print("✅ Logged in successfully!")

        full_name = "The Logical Mind | Daily Clarity"
        biography = (
            "🧠 1 Logical Truth Every Day\n"
            "⏳ Save 100 hours of overthinking\n"
            "🎯 Master your Focus, Time & Wealth\n"
            "👇 Start your 365-day mindset shift"
        )
        
        print("📝 Updating profile information (Full Name & Bio)...")
        # Edit account details via instagrapi
        cl.account_edit(
            full_name=full_name,
            biography=biography
        )
        print("🎉 Profile updated successfully on Instagram!")
        print(f"   Name: {full_name}")
        print(f"   Bio:\n{biography}")

    except ImportError:
        print("⚠️ 'instagrapi' package not installed. Installing now...")
        os.system("pip install instagrapi pillow")
    except Exception as e:
        print(f"❌ Error updating profile: {e}")

if __name__ == "__main__":
    update_profile()
