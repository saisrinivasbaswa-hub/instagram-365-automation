import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

niche_seeds = {
    "Mindset": [
        ("Silence is not the absence of sound, but the presence of focus.", "Protect your focus. Silence the noise before it silences your potential."),
        ("You don't need more time. You need fewer distractions.", "Time is abundant. Attention is rare. Direct it wisely."),
        ("Saying no to others is saying yes to your own growth.", "Guard your energy. Every 'yes' to clutter is a 'no' to progress."),
        ("Busy is a decision. So is focused.", "Being busy is easy. Being effective requires ruthless elimination.")
    ],
    "Food": [
        ("Good food takes time. Great food takes respect for ingredients.", "Honor the process of creation. Quality is never a shortcut."),
        ("Cooking is an act of patience; eating together is an act of love.", "Nourish both your body and your relationships."),
        ("Simple ingredients cooked with mastery outshine complex recipes.", "Master the basics before attempting the ornate."),
        ("Flavor comes from heat and time. So does character.", "Let pressure and duration refine your craft.")
    ],
    "Cinema": [
        ("The best movie lines reveal truth without shouting.", "Substance in storytelling always outshines volume."),
        ("Cinema is a mirror reflecting what we fear and what we love.", "Watch stories to understand human nature deeper."),
        ("Great direction is invisible; you only feel the emotion.", "When execution is flawless, the mechanism disappears."),
        ("Every scene must move the story forward or be cut.", "Eliminate filler from your life with cinematic precision.")
    ],
    "Music": [
        ("Music says what words cannot express and silence cannot hide.", "Tune into what resonates below the surface."),
        ("Rhythm is the heartbeat of discipline.", "Find your cadence and maintain it daily."),
        ("Silence between notes gives the melody its beauty.", "Rest is not wasted time; it defines the rhythm of success."),
        ("Mastering an instrument is mastering your own hands and mind.", "Repetition turns raw effort into effortless harmony.")
    ],
    "Wealth": [
        ("True wealth is not owning things, but owning your schedule.", "Financial freedom is the luxury of saying no."),
        ("Value is created by solving problems people ignore.", "Look for friction. Solutions yield compound returns."),
        ("Price is what you pay. Value is what you keep.", "Always seek underlying quality over surface flash."),
        ("Leverage turns effort into wealth. Build code, content, or capital.", "Scale your work so it operates while you sleep.")
    ],
    "Fitness": [
        ("Pain is temporary. Regret lasts forever.", "Suffer the mild pain of discipline today."),
        ("Your body can stand almost anything. It's your mind you must convince.", "Break mental limits before physical ones."),
        ("Consistency beats intensity every single time.", "Show up daily, even when you don't feel like it."),
        ("You do not rise to the level of your goals; you fall to your habits.", "Build unbreakable physical systems.")
    ],
    "Tech": [
        ("Don't just use tools. Build systems that scale.", "Automate repetitive friction to liberate your mind."),
        ("Code is leverage. Content is leverage. Master scalable assets.", "Work smarter by building systems that execute 24/7."),
        ("Simplicity is the ultimate sophistication in software and life.", "Strip away complexity until only core function remains."),
        ("The future belongs to those who build it today.", "Learn to create technology, not just consume it.")
    ],
    "Books": [
        ("A reader lives a thousand lives before he dies.", "Expand your world through the minds of history's greatest thinkers."),
        ("Read what you love until you love to read.", "Obsessive learning is the ultimate unfair advantage."),
        ("Books are quiet friends that never lie.", "Spend time in deep reading to build deep focus."),
        ("Knowledge without execution is just mental clutter.", "Turn raw reading into decisive daily action.")
    ],
    "Peace": [
        ("Peace of mind is the ultimate luxury.", "Protect your inner tranquility above material gain."),
        ("He who anger controls is controlled by others.", "Maintain emotional composure under external noise."),
        ("Solitude is where clarity meets creation.", "Spend quiet time alone to discover your true purpose."),
        ("Not everything deserves a reaction. Master silence.", "Silence is often the most articulate response.")
    ],
    "Productivity": [
        ("Focus on 1 core task for 90 minutes. Eliminate all else.", "Single-task your way to extraordinary momentum."),
        ("If it takes less than 2 minutes, do it now.", "Kill small friction before it snowball into chaos."),
        ("Relying on motivation is amateur. Build daily routines.", "Systems out-execute mood every single day."),
        ("Done is better than perfect.", "Launch, iterate, and refine in the real world.")
    ]
}

hashtags_map = {
    "Mindset": "#mindset #logic #stoicism #discipline #growth",
    "Food": "#culinary #foodie #cooking #artofcooking #recipes",
    "Cinema": "#cinema #moviequotes #film #filmmaking #storytelling",
    "Music": "#music #harmony #lyrics #musician #soundtrack",
    "Wealth": "#wealth #finance #investing #leverage #freedom",
    "Fitness": "#fitness #discipline #workout #gym #bodybuilding",
    "Tech": "#tech #coding #automation #software #systems",
    "Books": "#books #reading #philosophy #wisdom #learning",
    "Peace": "#innerpeace #mindfulness #calm #stoic #meditation",
    "Productivity": "#productivity #focus #habits #efficiency #execution"
}

all_quotes = []
niches_list = list(niche_seeds.keys())

for i in range(1, 366):
    niche = niches_list[(i - 1) % len(niches_list)]
    seeds = niche_seeds[niche]
    seed = seeds[(i - 1) % len(seeds)]
    
    quote_text = seed[0]
    caption_intro = seed[1]
    hashtag = hashtags_map[niche]
    
    item = {
        "day": i,
        "category": niche,
        "quote": quote_text,
        "caption": f"{quote_text}\n\n💡 {caption_intro}\n\nSave this for when you need clarity.\nFollow @the_logical_minds.1 for daily insights.",
        "hashtags": hashtag,
        "image_filename": f"day_{i:03d}.png"
    }
    all_quotes.append(item)

base_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(base_dir)

json_path = os.path.join(base_dir, "posts_365.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(all_quotes, f, indent=2, ensure_ascii=False)

js_path = os.path.join(project_dir, "js", "quotes365.js")
with open(js_path, "w", encoding="utf-8") as f:
    f.write("// 365-Day Multi-Niche Quotes Dataset\n")
    f.write("const QUOTES_DATA = ")
    json.dump(all_quotes, f, indent=2, ensure_ascii=False)
    f.write(";\n")

print(f"✅ Generated 365 multi-niche quotes across all 10 themes!")
