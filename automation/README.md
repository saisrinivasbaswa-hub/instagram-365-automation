# 365-Day Instagram Auto-Posting Suite

Automated system to generate and publish 365 crisp, logical minimalist quote posts (Samya Raine style) to Instagram.

---

## 🚀 Quick Setup Instructions

### 1. Install Dependencies
Run in your terminal:
```bash
pip install -r automation/requirements.txt
```

---

### 2. Generate All 365 Post Images
Generate all 365 high-resolution (1080x1080) PNG image cards in seconds:
```bash
python automation/generate_all_images.py
```
This creates a folder `automation/images/` containing `day_001.png` to `day_365.png`.

---

### 3. Configure Meta Instagram Graph API (or Auto-Scheduler)
Set your environment variables (or update `auto_poster.py`):
```bash
set INSTAGRAM_ACCOUNT_ID=your_instagram_account_id
set INSTAGRAM_ACCESS_TOKEN=your_meta_access_token
set PUBLIC_IMAGE_SERVER=https://your-server-or-gcs.com/images/
```

---

### 4. Schedule Daily Auto-Posting (1 Post / Day)

#### Option A: Windows Task Scheduler (Recommended for Windows)
1. Open **Task Scheduler** on Windows.
2. Click **Create Basic Task** -> Name: `Instagram_365_Poster`.
3. Trigger: **Daily** at `09:00 AM`.
4. Action: **Start a program**.
   - Program: `python.exe`
   - Arguments: `C:\Users\baswa\Documents\antigravity\friendly-heisenberg\automation\auto_poster.py`
5. Click **Finish**. Your account will automatically post 1 quote every day!

#### Option B: GitHub Actions / Cloud Cron (Free 24/7 Cloud Execution)
Set up a daily GitHub Action `.github/workflows/post_daily.yml` to trigger `auto_poster.py` at `09:00 AM UTC` every single day automatically without keeping your PC powered on.

---

## 📁 File Structure
- `posts_365.json` — Complete database of all 365 quotes, captions, and hashtag bundles.
- `generate_all_images.py` — Python Pillow script to render images.
- `auto_poster.py` — Automated publisher script.
- `current_day.txt` — Tracker file keeping track of the current day index (1 - 365).
