import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 365-Day Indian Mindset, Festival & Special Days Content Dataset
# Structured with dynamic date matching, rich cultural wisdom, and viral Indian hashtags.

indian_posts = [
    # JANUARY
    {
        "day": 1, "date": "01-01", "category": "New Year",
        "quote": "New year, same focus: Build in silence, let your progress make the noise.",
        "caption": "Wishing everyone a powerful & focused New Year 2026! 🚀 Set clear goals, work consistently, and respect your time.\n\nTag someone you want to achieve great things with this year!",
        "hashtags": "#NewYear2026 #IndianMindset #GoalGetter #Focus2026 #DesiMotivation #BuildInSilence #IndiaGrowth"
    },
    {
        "day": 12, "date": "01-12", "category": "National Youth Day",
        "quote": "Arise, awake, and stop not till the goal is reached. — Swami Vivekananda",
        "category_tag": "Swami Vivekananda Jayanti",
        "caption": "On National Youth Day, let's remember the timeless wisdom of Swami Vivekananda. Focus your energy, discipline your mind, and serve your nation with pride. 🇮🇳\n\nShare this quote with a friend who needs inspiration today!",
        "hashtags": "#SwamiVivekananda #NationalYouthDay #YouthOfIndia #IndianWisdom #MotivationIndia #Inspiration #DesiPower"
    },
    {
        "day": 14, "date": "01-14", "category": "Festival",
        "quote": "As the sun transforms its direction, may your life transform towards light and joy.",
        "category_tag": "Makar Sankranti / Pongal",
        "caption": "Wishing you and your family a very Happy Makar Sankranti, Pongal, Bihu & Uttarayan! 🪁🌾 May this harvest season bring health, happiness, and prosperity to your home.\n\nSend this to your family WhatsApp group!",
        "hashtags": "#MakarSankranti #HappyPongal #Uttarayan #IndianFestivals #FestiveVibes #CultureOfIndia #JoyAndHarvest"
    },
    {
        "day": 26, "date": "01-26", "category": "National Day",
        "quote": "Freedom in mind, strength in words, and pride in our souls. Happy Republic Day!",
        "category_tag": "Republic Day of India",
        "caption": "Saluting the great Constitution and the brave heroes who built our proud nation. Happy 77th Republic Day to every Indian across the globe! 🇮🇳✨\n\nType 'Jai Hind' in the comments to honor our motherland!",
        "hashtags": "#RepublicDay #RepublicDay2026 #JaiHind #ProudIndian #India #IndianHeritage #UnityInDiversity"
    },

    # FEBRUARY
    {
        "day": 14, "date": "02-14", "category": "Love & Respect",
        "quote": "True love in Indian culture is not just a feeling; it is loyalty, respect, and staying together through every storm.",
        "category_tag": "Love & Loyalty",
        "caption": "Real relationships are built on mutual respect, commitment, and unspoken understanding. Respect the ones who stand by you when times get tough. ❤️\n\nTag that special person who is your biggest support system!",
        "hashtags": "#TrueLove #IndianCulture #LoyaltyAndRespect #RelationshipGoals #FamilyValues #DesiLove #Bonding"
    },
    {
        "day": 28, "date": "02-28", "category": "National Science Day",
        "quote": "Never stop asking 'Why'. Curiosity is the mother of all innovation and wisdom.",
        "category_tag": "CV Raman Jayanti",
        "caption": "On National Science Day, celebrating Sir C.V. Raman's discovery of the Raman Effect. Science teaches us to question assumptions and seek truth through logic. 🔬💡\n\nShare with students & tech enthusiasts!",
        "hashtags": "#NationalScienceDay #CVRaman #ScienceIndia #LogicAndReason #Innovation #IndianGenius #Education"
    },

    # MARCH
    {
        "day": 8, "date": "03-08", "category": "Women's Day",
        "quote": "Where women are respected and honored, prosperity and wisdom naturally reside.",
        "category_tag": "International Women's Day",
        "caption": "Happy Women's Day to the mothers, sisters, daughters, and leaders who shape our homes and our nation every day with strength and grace. 💐✨\n\nTag the strongest women in your life to show your appreciation!",
        "hashtags": "#WomensDay #WomenOfIndia #SheInspires #Empowerment #IndianWomen #RespectWomen #FamilyFoundation"
    },
    {
        "day": 15, "date": "03-15", "category": "Festival",
        "quote": "In the silence of Shivratri, conquer your inner noise and awaken your inner power.",
        "category_tag": "Maha Shivratri",
        "caption": "Wishing you and your family a divine Maha Shivratri! May Lord Shiva destroy all negativity in your life and grant you peace, clarity, and strength. 🔱🕉️\n\nComment 'Har Har Mahadev' to spread positive vibrations!",
        "hashtags": "#MahaShivratri #HarHarMahadev #LordShiva #SpiritualIndia #FestiveVibes #InnerPeace #IndianTradition"
    },
    {
        "day": 25, "date": "03-25", "category": "Festival",
        "quote": "Let the colors of Holi wash away old grudges and fill your heart with forgiveness and joy.",
        "category_tag": "Holi — Festival of Colors",
        "caption": "Wishing you a vibrant and Happy Holi! 🎨✨ May your life be filled with the bright colors of happiness, good health, and success.\n\nShare this warm festive wish with your friends and family!",
        "hashtags": "#HappyHoli #Holi2026 #FestivalOfColors #IndianCulture #DesiFestivals #JoyAndColors #FamilyCelebration"
    },

    # APRIL
    {
        "day": 14, "date": "04-14", "category": "New Year & Equality",
        "quote": "Cultivation of mind should be the ultimate aim of human existence. — Dr. B.R. Ambedkar",
        "category_tag": "Ambedkar Jayanti & Regional New Years",
        "caption": "Celebrating Dr. B.R. Ambedkar Jayanti alongside Ugadi, Gudi Padwa, Baisakhi & Vishu! 🌾✨ Education, equality, and new beginnings define our rich Indian heritage.\n\nSending warm festive wishes to everyone!",
        "hashtags": "#AmbedkarJayanti #Ugadi #GudiPadwa #Baisakhi #IndianHeritage #NewBeginnings #EqualOpportunity"
    },

    # MAY
    {
        "day": 10, "date": "05-10", "category": "Family & Motherhood",
        "quote": "A mother is the first teacher, the safest refuge, and the purest form of selfless love.",
        "category_tag": "Mother's Day",
        "caption": "Happy Mother's Day! 💖 No words can ever measure the sacrifices, prayers, and unconditional love of an Indian mother.\n\nTag your mom or share this to honor the amazing mother who built your life!",
        "hashtags": "#MothersDay #MotherLove #Maa #IndianMom #FamilyFirst #UnconditionalLove #Gratitude"
    },

    # JUNE
    {
        "day": 21, "date": "06-21", "category": "Yoga & Fatherhood",
        "quote": "Yoga is not just exercise; it is the science of mastering your breath, mind, and body.",
        "category_tag": "International Yoga Day & Father's Day",
        "caption": "Happy International Yoga Day & Happy Father's Day! 🧘‍♂️👨‍👧 A father works silently in the background so his children can shine out front.\n\nTag your father and share the gift of health today!",
        "hashtags": "#YogaDay #FathersDay #DadMyHero #YogaIndia #HealthAndMind #Fatherhood #IndianValues"
    },

    # AUGUST
    {
        "day": 2, "date": "08-02", "category": "Relationships",
        "quote": "True friends don't judge your past; they stand beside you to build your future.",
        "category_tag": "Friendship Day",
        "caption": "Happy Friendship Day! 🤝 In life, true friends are the family we choose for ourselves.\n\nTag your 3 closest friends in the comments below to let them know they matter!",
        "hashtags": "#FriendshipDay #BestFriends #DesiYaari #FriendshipGoals #TrustAndLoyalty #Yaariyan #TagYourFriends"
    },
    {
        "day": 15, "date": "08-15", "category": "National Day",
        "quote": "Independence is not just a holiday; it is a responsibility to make our nation stronger every day.",
        "category_tag": "Independence Day of India",
        "caption": "Happy 80th Independence Day, India! 🇮🇳 Remembering the sacrifices of our freedom fighters who gave their today for our tomorrow.\n\nComment 'Vande Mataram' to celebrate Indian pride!",
        "hashtags": "#IndependenceDay #IndiaAt80 #VandeMataram #ProudIndian #Freedom #IndianArmy #JaiHind"
    },
    {
        "day": 26, "date": "08-26", "category": "Festival",
        "quote": "A thread of Rakhi carries a lifetime of protection, laughter, and unspoken sibling love.",
        "category_tag": "Raksha Bandhan",
        "caption": "Happy Raksha Bandhan! 🧵✨ Celebrating the unbreakable bond between brothers and sisters.\n\nTag your brother or sister and demand your gift in the comments! 😄",
        "hashtags": "#RakshaBandhan #Rakhi2026 #SiblingLove #BrotherSister #IndianFestivals #FamilyBond #FestiveJoy"
    },

    # SEPTEMBER
    {
        "day": 5, "date": "09-05", "category": "Education & Respect",
        "quote": "A good teacher does not give you answers; they light the candle of curiosity within you.",
        "category_tag": "Teachers' Day",
        "caption": "Happy Teachers' Day! 📚 Dedicated to Dr. Sarvepalli Radhakrishnan and every guru, mentor, and parent who guided us on the right path.\n\nTag a teacher or mentor who changed your life!",
        "hashtags": "#TeachersDay #GuruPranam #Mentorship #RespectGurus #IndianEducation #Guidance #ThankYouTeacher"
    },
    {
        "day": 18, "date": "09-18", "category": "Festival",
        "quote": "May Lord Ganesha remove all obstacles from your path and bless you with wisdom and peace.",
        "category_tag": "Ganesh Chaturthi",
        "caption": "Ganpati Bappa Morya! 🌺🙏 Wishing you and your family a blessed Ganesh Chaturthi. May Bappa fill your home with happiness and prosperity.\n\nComment 'Ganpati Bappa Morya' to welcome Bappa into your heart!",
        "hashtags": "#GaneshChaturthi #GanpatiBappaMorya #BappaVisarjan #IndianFestivals #FestiveVibes #Devotion #Blessings"
    },

    # OCTOBER
    {
        "day": 2, "date": "10-02", "category": "Wisdom & Truth",
        "quote": "Be the change that you wish to see in the world. — Mahatma Gandhi",
        "category_tag": "Gandhi Jayanti & Shastri Jayanti",
        "caption": "Remembering Mahatma Gandhi and Lal Bahadur Shastri on their birth anniversaries. Truth, non-violence, and 'Jai Jawan, Jai Kisan' remain our guiding pillars. 🇮🇳\n\nShare this timeless wisdom with your network!",
        "hashtags": "#GandhiJayanti #MahatmaGandhi #LalBahadurShastri #TruthAndPeace #IndianValues #Inspiration #Simplicity"
    },
    {
        "day": 20, "date": "10-20", "category": "Festival",
        "quote": "Dussehra reminds us that no matter how strong evil or difficulty seems, truth and righteousness always triumph.",
        "category_tag": "Dussehra / Vijayadashami",
        "caption": "Happy Dussehra / Vijayadashami! 🏹✨ May Lord Rama bless you with the courage to conquer your internal doubts, anger, and ego.\n\nSending warm festive wishes to you and your family!",
        "hashtags": "#Dussehra #Vijayadashami #TruthPrevails #LordRama #IndianCulture #FestiveCelebration #GoodOverEvil"
    },

    # NOVEMBER
    {
        "day": 8, "date": "11-08", "category": "Festival of Lights",
        "quote": "May the light of Diwali ignite peace in your mind, health in your body, and prosperity in your home.",
        "category_tag": "Diwali / Deepavali",
        "caption": "Wishing you and your family a very Happy and Prosperous Diwali! 🪔✨ May your life be illuminated with endless joy, wealth, and good fortune.\n\nShare this Diwali blessing with your loved ones and WhatsApp groups!",
        "hashtags": "#HappyDiwali #Diwali2026 #Deepavali #FestivalOfLights #Prosperity #IndianFestivals #FamilyWarmth"
    },
    {
        "day": 14, "date": "11-14", "category": "Children & Innocence",
        "quote": "Never let the child inside you die. Keep your curiosity alive, no matter how old you get.",
        "category_tag": "Children's Day",
        "caption": "Happy Children's Day! 🎈 Children teach us to forgive quickly, love deeply, and laugh without hesitation.\n\nTag your childhood friends and share a fond memory!",
        "hashtags": "#ChildrensDay #ChildhoodMemories #KeepCurious #JoyAndInnocence #DesiNostalgia #Friendship"
    },

    # DECEMBER
    {
        "day": 23, "date": "12-23", "category": "Gratitude & Farming",
        "quote": "Before you complain about food, thank the farmer who labored under the sun to grow it.",
        "category_tag": "Kisan Diwas / Farmers' Day",
        "caption": "On National Farmers' Day, bowing down to the unsung heroes of India — our farmers (Jai Jawan, Jai Kisan). 🌾🚜\n\nType 'Jai Kisan' in the comments to show respect!",
        "hashtags": "#KisanDiwas #FarmersDay #JaiKisan #IndiaAgriculture #Gratitude #RespectFarmers #HeartOfIndia"
    },
    {
        "day": 31, "date": "12-31", "category": "Reflection",
        "quote": "Thank you for the lessons of this year. Step into the next year with a clean heart and a focused mind.",
        "category_tag": "Year-End Reflection",
        "caption": "As we close this year, express gratitude for every win and every struggle that made you stronger. 🌟\n\nComment 3 things you are grateful for this year!",
        "hashtags": "#YearEndReflection #Gratitude #MindsetMatters #GrowthJourney #IndianWisdom #ReadyFor2027 #Peace"
    }
]

# Fill in remaining days up to 365 with highly relatable everyday Indian mindset quotes
topics_cycle = [
    ("Joint Family Values", "Respecting elders is not weakness; it is the root of character and lasting peace."),
    ("Financial Discipline", "Save before you spend. True wealth is not showing off; it is financial freedom."),
    ("Hard Work & Karma", "Do your duty with full dedication; your karma will take care of your destiny."),
    ("Career & Focus", "Stop competing with others. Your only competition is who you were yesterday."),
    ("Middle-Class Pride", "Being raised in a middle-class family gives you the greatest superpower: Resilience."),
    ("Mental Peace", "Do not let someone else's opinion disturb the peace of your own home."),
    ("Respect for Mentors", "A teacher lights the lamp of knowledge. Never forget the hands that helped you rise."),
    ("Discipline", "Motivation gets you started; discipline keeps you going when excitement fades.")
]

current_days_set = {p["day"] for p in indian_posts}
topic_idx = 0

for d in range(1, 366):
    if d not in current_days_set:
        topic_name, quote_text = topics_cycle[topic_idx % len(topics_cycle)]
        topic_idx += 1
        indian_posts.append({
            "day": d,
            "category": "Indian Mindset",
            "category_tag": topic_name,
            "quote": quote_text,
            "caption": f"💡 {topic_name}: {quote_text}\n\nShare this post with your family or friends who believe in strong values! 🧡",
            "hashtags": "#IndianMindset #FamilyValues #DesiWisdom #CultureAndGrowth #LifeLessons #PeaceAndFocus #India"
        })

indian_posts.sort(key=lambda x: x["day"])

output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "indian_calendar_365.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(indian_posts, f, indent=2, ensure_ascii=False)

print(f"🎉 Successfully created 365 Indian Culture & Festival posts in '{output_file}'!")
