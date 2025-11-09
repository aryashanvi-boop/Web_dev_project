# generate_gifs.py
# Creates placeholder GIFs for: a–z, hello, thank_you, yes, no

import os
from PIL import Image, ImageDraw, ImageFont
import string

OUT_DIR = os.path.join("static", "asl_gestures")
os.makedirs(OUT_DIR, exist_ok=True)

def make_gif(text, filename, size=(160, 160)):
    img = Image.new("RGB", size, color=(255, 255, 255))
    d = ImageDraw.Draw(img)

    # Try to load a default font; fall back if unavailable
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()

    # Center the label
    w, h = d.textbbox((0,0), text, font=font)[2:]
    d.text(((size[0]-w)//2, (size[1]-h)//2), text, fill=(0,0,0), font=font)
    img.save(os.path.join(OUT_DIR, filename), save_all=True)

# 1) A–Z fingerspelling placeholders: "A" .. "Z"
for ch in string.ascii_lowercase:
    make_gif(ch.upper(), f"{ch}.gif")

# 2) Word placeholders (simple readable tiles)
make_gif("HELLO", "hello.gif")
make_gif("THANK YOU", "thank_you.gif")
make_gif("YES", "yes.gif")
make_gif("NO", "no.gif")

print("✅ Placeholder GIFs generated in static/asl_gestures/")
