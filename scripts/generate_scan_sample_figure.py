import fitz
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

pdf_path = Path("corpus/city_ordinances/City Ordinances (2025-2021)/2021/Ordinance No. 000667-21.pdf")
doc = fitz.open(pdf_path)

# Render pages at 300 DPI
p0 = doc[0].get_pixmap(dpi=300)
img0 = Image.frombytes("RGB", [p0.width, p0.height], p0.samples)

p1 = doc[1].get_pixmap(dpi=300)
img1 = Image.frombytes("RGB", [p1.width, p1.height], p1.samples)

# Crop Page 0: Top region showing session attendance roster and header
crop0 = img0.crop((0, 80, 2551, 1420))

# Crop Page 1: Top region showing operative enacting clause, Section 1, and Section 2
crop1 = img1.crop((0, 80, 2551, 1420))

target_w = 2600
h0 = int(crop0.height * (target_w / crop0.width))
h1 = int(crop1.height * (target_w / crop1.width))

crop0_resized = crop0.resize((target_w, h0), Image.Resampling.LANCZOS)
crop1_resized = crop1.resize((target_w, h1), Image.Resampling.LANCZOS)

# Target layout: Top-and-Bottom (Panel A on top, Panel B on bottom)
title_h = 75
gap = 45
pad = 30
total_w = pad * 2 + target_w
total_h = pad * 2 + title_h * 2 + h0 + h1 + gap

canvas = Image.new("RGB", (total_w, total_h), (255, 255, 255))
draw = ImageDraw.Draw(canvas)

# Fonts
try:
    font = ImageFont.truetype("arialbd.ttf", 38)
except Exception:
    font = ImageFont.load_default()

# Titles
title_a = "(a) Modern Electronic Typesetting with Header Scan Noise & Council Roster (Page 1)"
title_b = "(b) Substantive Enacting Sections with OCR Character Corruption & Margin Skew (Page 2)"

# Draw Panel A
y_a_title = pad + 15
draw.text((pad + 10, y_a_title), title_a, fill=(0, 0, 0), font=font)
y_a_img = pad + title_h
canvas.paste(crop0_resized, (pad, y_a_img))

# Divider line
y_div = y_a_img + h0 + gap // 2
draw.line([(pad, y_div), (total_w - pad, y_div)], fill=(210, 210, 210), width=2)

# Draw Panel B
y_b_title = y_a_img + h0 + gap + 15
draw.text((pad + 10, y_b_title), title_b, fill=(0, 0, 0), font=font)
y_b_img = y_a_img + h0 + gap + title_h
canvas.paste(crop1_resized, (pad, y_b_img))

out_fig = Path("CS_Undergraduate_Thesis_Template/figs/davao_ordinance_scan_sample.png")
out_fig.parent.mkdir(parents=True, exist_ok=True)
canvas.save(out_fig, dpi=(300, 300))
print(f"Saved modern scan sample figure to {out_fig} (size: {canvas.size})")

