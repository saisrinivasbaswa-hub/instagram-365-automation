import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")
SESSION_FILE = os.path.join(BASE_DIR, "session.json")

def test_login():
    username = ""
    password = ""

    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            for line in f:
                if "=" in line:
                    key, val = line.strip().split("=", 1)
                    if key == "INSTA_USERNAME":
                        username = val.strip()
                    elif key == "INSTA_PASSWORD":
                        password = val.strip()

    print(f"🔑 Testing Instagram connection for @{username}...")

    try:
        from instagrapi import Client
        cl = Client()

        # Load session if exists
        if os.path.exists(SESSION_FILE):
            print("Session file found. Loading session...")
            cl.load_settings(SESSION_FILE)

        # Login
        cl.login(username, password)
        cl.dump_settings(SESSION_FILE)
        print("✅ LOGIN SUCCESSFUL! Session saved.")

        # Print basic profile status
        user_info = cl.user_info_by_username(username)
        print(f"👤 Account Name: {user_info.full_name}")
        print(f"📝 Current Bio: {user_info.biography}")
        print("🚀 Account is fully connected and ready for auto-posting!")

    except Exception as e:
        print(f"⚠️ Notice: {e}")
        print("\n💡 Instagram is protecting new accounts from automated API logins.")
        print("   Simply open instagram.com on your phone/browser once to establish your normal session.")

if __name__ == "__main__":
    test_login()
