import fitz
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

pdf_path = Path("flagged pdfs/Ordinance No. 000123-60.pdf")
doc = fitz.open(pdf_path)

# Render pages at 300 DPI
p0 = doc[0].get_pixmap(dpi=300)
img0 = Image.frombytes("RGB", [p0.width, p0.height], p0.samples)

p1 = doc[1].get_pixmap(dpi=300)
img1 = Image.frombytes("RGB", [p1.width, p1.height], p1.samples)

# Crop Page 0: Top region showing smudge, header, title, hole punches, and Section 1-2
# Page 0 is (2412, 3912)
crop0 = img0.crop((0, 80, 2412, 2300))

# Crop Page 1: Region showing header, faded text, hole punches, and handwritten amendments
# Page 1 is (2541, 3900)
crop1 = img1.crop((0, 100, 2541, 2320))

# Resize both to same height for balanced side-by-side presentation
target_h = 1400
w0 = int(crop0.width * (target_h / crop0.height))
w1 = int(crop1.width * (target_h / crop1.height))
crop0_resized = crop0.resize((w0, target_h), Image.Resampling.LANCZOS)
crop1_resized = crop1.resize((w1, target_h), Image.Resampling.LANCZOS)

# Target layout: side-by-side with padding and title space
title_h = 90
gap = 50
pad = 30
total_w = pad * 2 + w0 + gap + w1
total_h = pad * 2 + title_h + target_h

canvas = Image.new("RGB", (total_w, total_h), (255, 255, 255))
draw = ImageDraw.Draw(canvas)

# Fonts
try:
    font = ImageFont.truetype("arialbd.ttf", 40)
except Exception:
    font = ImageFont.load_default()

# Paste crops
x0 = pad
y_img = pad + title_h
canvas.paste(crop0_resized, (x0, y_img))

x1 = pad + w0 + gap
canvas.paste(crop1_resized, (x1, y_img))

# Draw titles
title_a = "(a) Severe Diagonal Ink Occlusion, Title Smear & Binder Punch Loss (Page 1)"
title_b = "(b) Mechanical Typewriter Degradation & Handwritten Pen Amendments (Page 2)"

draw.text((x0 + 10, pad + 20), title_a, fill=(0, 0, 0), font=font)
draw.text((x1 + 10, pad + 20), title_b, fill=(0, 0, 0), font=font)

# Optional thin divider line between panels
draw.line([(pad + w0 + gap // 2, pad + 10), (pad + w0 + gap // 2, total_h - pad)], fill=(210, 210, 210), width=2)

out_fig = Path("CS_Undergraduate_Thesis_Template/figs/davao_ordinance_scan_extreme_degradation.png")
out_fig.parent.mkdir(parents=True, exist_ok=True)
canvas.save(out_fig, dpi=(300, 300))
print(f"Saved extreme scan figure to {out_fig} (size: {canvas.size})")
