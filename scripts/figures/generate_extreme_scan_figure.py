import fitz
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

pdf_path = Path("data/flagged_scans_pdf/Ordinance No. 000123-60.pdf")
if not pdf_path.exists():
    pdf_path = Path("flagged pdfs/Ordinance No. 000123-60.pdf")
doc = fitz.open(pdf_path)

# Render pages at 300 DPI
p0 = doc[0].get_pixmap(dpi=300)
img0 = Image.frombytes("RGB", [p0.width, p0.height], p0.samples)

p1 = doc[1].get_pixmap(dpi=300)
img1 = Image.frombytes("RGB", [p1.width, p1.height], p1.samples)

# Crop Page 0: Top region showing smudge, header, title, hole punches, and Section 1-2
# Page 0 is (2412, 3912)
crop0 = img0.crop((0, 80, 2412, 1330))

# Crop Page 1: Region showing header, faded text, hole punches, and handwritten amendments
# Page 1 is (2541, 3900)
crop1 = img1.crop((0, 100, 2541, 1350))

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
title_a = "(a) Severe Diagonal Ink Occlusion, Title Smear & Binder Punch Loss (Page 1)"
title_b = "(b) Mechanical Typewriter Degradation & Handwritten Pen Amendments (Page 2)"

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

out_fig = Path("CS_Undergraduate_Thesis_Template/figs/davao_ordinance_scan_extreme_degradation.png")
out_fig.parent.mkdir(parents=True, exist_ok=True)
canvas.save(out_fig, dpi=(300, 300))
print(f"Saved extreme scan figure to {out_fig} (size: {canvas.size})")
