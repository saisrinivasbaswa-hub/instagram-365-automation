import os
import sys
import subprocess
from flask import Flask, jsonify, request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_script(script_name):
    script_path = os.path.join(BASE_DIR, script_name)
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=300
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.route("/")
def home():
    day_acc1 = "N/A"
    day_acc2 = "N/A"
    
    acc1_file = os.path.join(BASE_DIR, "current_day.txt")
    acc2_file = os.path.join(BASE_DIR, "current_day_indian.txt")
    
    if os.path.exists(acc1_file):
        with open(acc1_file, "r") as f:
            day_acc1 = f.read().strip()
            
    if os.path.exists(acc2_file):
        with open(acc2_file, "r") as f:
            day_acc2 = f.read().strip()

    return jsonify({
        "status": "online",
        "service": "Instagram 365 Auto-Poster",
        "account_1_day": day_acc1,
        "account_2_day": day_acc2,
        "endpoints": {
            "trigger_all": "/trigger",
            "trigger_acc1": "/trigger_acc1",
            "trigger_acc2": "/trigger_acc2"
        }
    })

@app.route("/trigger", methods=["GET", "POST"])
def trigger_all():
    print("🚀 Triggering auto-post for Account 1 & Account 2...")
    res1 = run_script("post_via_browser.py")
    res2 = run_script("post_account_2.py")
    return jsonify({
        "account_1_result": res1,
        "account_2_result": res2
    })

@app.route("/trigger_acc1", methods=["GET", "POST"])
def trigger_acc1():
    print("🚀 Triggering auto-post for Account 1...")
    res = run_script("post_via_browser.py")
    return jsonify({"account_1_result": res})

@app.route("/trigger_acc2", methods=["GET", "POST"])
def trigger_acc2():
    print("🚀 Triggering auto-post for Account 2...")
    res = run_script("post_account_2.py")
    return jsonify({"account_2_result": res})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
