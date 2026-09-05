import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

theme_styles = {
    "Mindset": {"bg": "#07090e", "border": "#262d40", "tag": "#8b5cf6", "text": "#f3f4f6", "handle": "#f59e0b"},
    "Food": {"bg": "#231510", "border": "#84a98c", "tag": "#e0a96d", "text": "#fdfbf7", "handle": "#84a98c"},
    "Cinema": {"bg": "#120404", "border": "#e5a93c", "tag": "#e5a93c", "text": "#ffffff", "handle": "#e5a93c"},
    "Music": {"bg": "#0a0714", "border": "#8b5cf6", "tag": "#06b6d4", "text": "#ffffff", "handle": "#8b5cf6"},
    "Wealth": {"bg": "#041d15", "border": "#d4af37", "tag": "#d4af37", "text": "#f4f6f0", "handle": "#d4af37"},
    "Fitness": {"bg": "#111111", "border": "#ff5722", "tag": "#ff5722", "text": "#ffffff", "handle": "#ff5722"},
    "Tech": {"bg": "#09101d", "border": "#10b981", "tag": "#10b981", "text": "#e2e8f0", "handle": "#10b981"},
    "Books": {"bg": "#f4ecd8", "border": "#8c6d1f", "tag": "#8c6d1f", "text": "#1a1a1a", "handle": "#1a1a1a"},
    "Peace": {"bg": "#0b1324", "border": "#f472b6", "tag": "#f472b6", "text": "#f3f4f6", "handle": "#f472b6"},
    "Productivity": {"bg": "#ffffff", "border": "#0f172a", "tag": "#2563eb", "text": "#0f172a", "handle": "#0f172a"}
}

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

def generate_quote_card(item, output_folder, handle="@the_logical_minds.1"):
    category = item.get('category', 'Mindset')
    style = theme_styles.get(category, theme_styles["Mindset"])

    width, height = 1080, 1080
    image = Image.new("RGB", (width, height), style["bg"])
    draw = ImageDraw.Draw(image)

    # Draw Border Frame
    draw.rectangle([60, 60, width - 60, height - 60], outline=style["border"], width=4)

    # Try loading default system fonts
    try:
        font_cat = ImageFont.truetype("arial.ttf", 24)
        font_quote = ImageFont.truetype("georgia.ttf", 46)
        font_handle = ImageFont.truetype("arial.ttf", 26)
        font_day = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font_cat = ImageFont.load_default()
        font_quote = ImageFont.load_default()
        font_handle = ImageFont.load_default()
        font_day = ImageFont.load_default()

    # Draw Category (Top)
    category_str = f"— {category.upper()} —"
    bbox_cat = draw.textbbox((0, 0), category_str, font=font_cat)
    cat_w = bbox_cat[2] - bbox_cat[0]
    draw.text(((width - cat_w) / 2, 130), category_str, fill=style["tag"], font=font_cat)

    # Draw Main Quote Text
    quote_str = f"“{item['quote']}”"
    lines = text_wrap(quote_str, font_quote, width - 240, draw)
    line_height = 60
    total_text_height = len(lines) * line_height
    start_y = (height - total_text_height) / 2 - 20

    for i, line in enumerate(lines):
        bbox_line = draw.textbbox((0, 0), line, font=font_quote)
        line_w = bbox_line[2] - bbox_line[0]
        draw.text(((width - line_w) / 2, start_y + (i * line_height)), line, fill=style["text"], font=font_quote)

    # Draw Handle Watermark (Bottom)
    bbox_h = draw.textbbox((0, 0), handle, font=font_handle)
    h_w = bbox_h[2] - bbox_h[0]
    draw.text(((width - h_w) / 2, height - 140), handle, fill=style["handle"], font=font_handle)

    # Draw Day Tag
    day_str = f"DAY {item['day']} OF 365"
    bbox_d = draw.textbbox((0, 0), day_str, font=font_day)
    d_w = bbox_d[2] - bbox_d[0]
    draw.text(((width - d_w) / 2, height - 95), day_str, fill=style["tag"], font=font_day)

    # Save PNG
    output_filename = f"day_{item['day']:03d}.png"
    filepath = os.path.join(output_folder, output_filename)
    image.save(filepath, "PNG")
    return filepath

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "posts_365.json")
    output_folder = os.path.join(base_dir, "images")
    os.makedirs(output_folder, exist_ok=True)

    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found!")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        posts = json.load(f)

    print(f"🚀 Generating 365 multi-theme quote cards in '{output_folder}'...")
    
    for idx, item in enumerate(posts, 1):
        filepath = generate_quote_card(item, output_folder)
        if idx % 50 == 0 or idx == len(posts):
            print(f"  [✓] Generated {idx}/365 images...")

    print("\n✅ Success! All 365 multi-theme post images have been generated.")

if __name__ == "__main__":
    main()
