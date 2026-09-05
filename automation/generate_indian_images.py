import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_FILE = os.path.join(BASE_DIR, "indian_calendar_365.json")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "images_indian")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def text_wrap(text, font, max_width, draw):
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]
        
        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def generate_indian_card(item, output_folder, handle="@indian_mindset_culture"):
    img_size = 1080
    
    # Warm Royal Obsidian Gradient Background
    img = Image.new('RGB', (img_size, img_size), color='#0B0E14')
    draw = ImageDraw.Draw(img)

    # Decorative Royal Golden Border Frame
    draw.rectangle([40, 40, img_size-40, img_size-40], outline='#F5C518', width=3)
    draw.rectangle([50, 50, img_size-50, img_size-50], outline='#D4AF37', width=1)

    # Load Fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 34)
        quote_font = ImageFont.truetype("georgia.ttf", 46)
        footer_font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        title_font = ImageFont.load_default()
        quote_font = ImageFont.load_default()
        footer_font = ImageFont.load_default()

    # Category Tag / Festival Label (Golden Saffron Header)
    tag_text = f"✨ {item.get('category_tag', item['category']).upper()} ✨"
    tag_bbox = draw.textbbox((0, 0), tag_text, font=title_font)
    tag_w = tag_bbox[2] - tag_bbox[0]
    draw.text(((img_size - tag_w) / 2, 120), tag_text, fill='#F5C518', font=title_font)

    # Decorative Line
    draw.line([(img_size//2 - 100, 180), (img_size//2 + 100, 180)], fill='#FF8C00', width=2)

    # Wrapped Quote Text
    quote_text = f"“{item['quote']}”"
    max_text_width = 850
    lines = text_wrap(quote_text, quote_font, max_text_width, draw)

    line_heights = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=quote_font)
        line_heights.append(bbox[3] - bbox[1])
    
    total_text_height = sum(line_heights) + (len(lines) - 1) * 20
    start_y = (img_size - total_text_height) / 2 + 30

    current_y = start_y
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=quote_font)
        line_w = bbox[2] - bbox[0]
        draw.text(((img_size - line_w) / 2, current_y), line, fill='#FFFFFF', font=quote_font)
        current_y += line_heights[i] + 20

    # Footer Watermark & Handle
    footer_text = f"🇮🇳  {handle}"
    foot_bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    foot_w = foot_bbox[2] - foot_bbox[0]
    draw.text(((img_size - foot_w) / 2, 940), footer_text, fill='#D4AF37', font=footer_font)

    # Save PNG
    file_name = f"day_{item['day']:03d}.png"
    file_path = os.path.join(output_folder, file_name)
    img.save(file_path, 'PNG', quality=95)
    return file_path

print("🚀 Batch rendering 365 Indian Festival & Mindset Quote Cards...")
with open(DATASET_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    generate_indian_card(item, OUTPUT_FOLDER)

print(f"🎉 Successfully rendered all 365 Indian Culture post cards into '{OUTPUT_FOLDER}'!")
