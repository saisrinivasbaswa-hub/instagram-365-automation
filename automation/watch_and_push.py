import time
import os
import subprocess
import requests

TOKEN = "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"
REPO_NAME = "instagram-365-automation"
OWNER = "saisrinivasbaswa-hub"
URL = f"https://api.github.com/repos/{OWNER}/{REPO_NAME}"
PUSH_URL = f"https://{TOKEN}@github.com/{OWNER}/{REPO_NAME}.git"

print(f"Waiting for GitHub repository '{REPO_NAME}' to be created...")

headers = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}

for attempt in range(60):
    try:
        r = requests.get(URL, headers=headers, timeout=5)
        if r.status_code == 200:
            print("🎉 Repository detected! Pushing codebase now...")
            res = subprocess.run(
                ["git", "push", PUSH_URL, "master", "--force"],
                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                capture_output=True,
                text=True
            )
            print("Git Push Output:", res.stdout, res.stderr)
            if res.returncode == 0:
                print("SUCCESS: Code pushed to GitHub successfully!")
                break
            else:
                print("Push attempt failed, retrying in 3 seconds...")
        else:
            print(f"Attempt {attempt+1}/60: Repo not created yet ({r.status_code}). Waiting 3s...")
    except Exception as e:
        print("Error:", e)
    time.sleep(3)
