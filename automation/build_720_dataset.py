import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_365 = os.path.join(BASE_DIR, "indian_calendar_365.json")
OUTPUT_720 = os.path.join(BASE_DIR, "indian_calendar_720.json")

def generate_720_dataset():
    if not os.path.exists(INPUT_365):
        print(f"Error: {INPUT_365} not found!")
        return

    with open(INPUT_365, "r", encoding="utf-8") as f:
        data_365 = json.load(f)

    hourly_themes = [
        "🌸 Morning Mantra & Prayer",
        "🕉️ Vedic Wisdom",
        "🛕 Temple Architecture & History",
        "🌺 Sacred Ritual Meaning",
        "🧘 Mindset & Inner Peace",
        "🌿 Ayurveda & Healthy Life",
        "📜 Upanishad Quote",
        "🚩 Great Indian Heritage",
        "🪔 Daily Festival Insight",
        "✨ Spiritual Awakening",
        "📚 Bhagavad Gita Lesson",
        "☀️ Midday Positivity",
        "📿 Chanting & Vibration",
        "🌾 Indian Art & Culture",
        "🔱 Devotional Thought",
        "🪷 Karma & Dharma",
        "🌙 Evening Reflection",
        "🧘‍♂️ Silence & Meditation",
        "📜 Sanskrit Sloka & Meaning",
        "🔥 Agni & Sacred Elements",
        "🌸 Compassion & Gratitude",
        "🌌 Cosmic Law & Order",
        "🕯️ Peace & Serenity",
        "🌌 Night Blessing & Gratitude"
    ]

    posts_720 = []
    item_id = 1

    for day in range(1, 31): # 30 days
        for hour in range(24): # 24 hours per day
            source_item = data_365[(item_id - 1) % len(data_365)]
            theme = hourly_themes[hour % len(hourly_themes)]
            
            post_entry = {
                "day": item_id,
                "day_of_month": day,
                "hour": hour,
                "category": f"Day {day} ({hour:02d}:00) - {theme}",
                "quote": source_item["quote"],
                "caption": f"✨ Day {day} | Post #{item_id}/720 ({hour:02d}:00 IST)\n\nCategory: {theme}\n\n\"{source_item['quote']}\"\n\n{source_item['caption']}",
                "hashtags": source_item["hashtags"] + " #IndianCulture #VedicWisdom #DailyBlessings #IndianTraditions",
                "image_filename": f"day_{item_id:03d}.png"
            }
            posts_720.append(post_entry)
            item_id += 1

    with open(OUTPUT_720, "w", encoding="utf-8") as f:
        json.dump(posts_720, f, indent=2, ensure_ascii=False)

    print(f"🎉 Generated {len(posts_720)} posts in {OUTPUT_720} (24 posts/day for 30 days)!")

if __name__ == "__main__":
    generate_720_dataset()
