"""
generate_defense_pptx.py
========================
Generates a 16:9 widescreen Canva-ready PowerPoint presentation (.pptx)
matching the authentic Canva mock defense slides from `Thesis 2 - Defense Slides.pdf`.

Key Design Decisions & Protocol Adherence:
1. Title Slide: Exact match to `T2_slide_1.png` (PT Serif centered, white line, Proponents/Adviser, authentic perimeter assets).
2. Pure Subsection Titles: Every slide title is strictly the pure subsection heading (e.g. "Background of the Study", "Stage 1 Retrieval Benchmarks").
3. Clean Paper References: Bottom-left references strictly format as "Page X, §Y.Z" with zero source clutter.
4. Non-Minimal, Zero-Stretching Assets: All 8 perimeter assets placed one-by-one with aspect-ratio locking via PIL and proper rotations.
5. High-Resolution Authentic Figures: Locked aspect ratios, crisp white card backing, zero distortion.
6. Standalone Table Slides: 100% table-only with high-res LaTeX booktabs crops (Tables 4.4, 4.5, 4.7, 4.8) and zero bottom text clutter.
7. Clean Typography: PT Serif for titles/numbers, Poppins for body/metadata, Markdown bold formatting support.
"""

import json
import os
import re
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# --- Color Tokens ---
COLOR_WHITE = RGBColor(255, 255, 255)       # Crisp White (#ffffff)
COLOR_TITLE = RGBColor(242, 183, 5)         # Deep Warm Gold (#f2b705)
COLOR_GOLD = RGBColor(216, 155, 20)         # Darker Gold (#d89b14)
COLOR_ICE = RGBColor(148, 163, 184)         # Ice Blue / Muted Paper Ref (#94a3b8)
COLOR_CARD_BORDER = RGBColor(230, 235, 245) # Subtle Border for Figure/Table Cards


def add_fitted_picture(slide, image_path, left, top, max_width=None, max_height=None, rotation=None):
    """
    Adds a picture strictly preserving its native aspect ratio.
    If both max_width and max_height are provided, scales to fit inside the bounding box.
    Returns the created picture shape along with its actual (w, h).
    """
    if not os.path.exists(image_path):
        print(f"Warning: image not found: {image_path}")
        return None, 0, 0

    with Image.open(image_path) as im:
        orig_w, orig_h = im.size
    orig_ar = orig_w / orig_h

    if max_width is not None and max_height is not None:
        scale = min(max_width / orig_w, max_height / orig_h)
        w = orig_w * scale
        h = orig_h * scale
    elif max_width is not None:
        w = max_width
        h = max_width / orig_ar
    elif max_height is not None:
        h = max_height
        w = max_height * orig_ar
    else:
        raise ValueError("Must specify max_width or max_height")

    pic = slide.shapes.add_picture(image_path, left, top, width=w, height=h)
    if rotation is not None:
        pic.rotation = float(rotation)
    return pic, w, h


def add_bullet_with_formatting(tf, bullet_text, is_first=False, font_size=Pt(20), space_after=Pt(16)):
    """
    Appends a bullet point to a text frame, parsing **bold** markers into distinct bold runs.
    """
    p = tf.paragraphs[0] if is_first else tf.add_paragraph()
    p.space_after = space_after

    # Bullet point marker
    run_marker = p.add_run()
    run_marker.text = "•  "
    run_marker.font.name = "Poppins"
    run_marker.font.size = font_size
    run_marker.font.color.rgb = COLOR_WHITE

    # Parse markdown bold tokens
    tokens = re.split(r'(\*\*.*?\*\*)', bullet_text)
    for tok in tokens:
        if not tok:
            continue
        run = p.add_run()
        run.font.name = "Poppins"
        run.font.size = font_size
        run.font.color.rgb = COLOR_WHITE
        if tok.startswith('**') and tok.endswith('**'):
            run.text = tok[2:-2]
            run.font.bold = True
        else:
            run.text = tok
            run.font.bold = False


def add_slide_background(slide, assets_dir, prs_w, prs_h):
    """Adds the full-bleed authentic dark background texture."""
    bg_path = os.path.join(assets_dir, "background.png")
    if os.path.exists(bg_path):
        slide.shapes.add_picture(bg_path, Inches(0), Inches(0), width=prs_w, height=prs_h)


def add_title_slide_decorations(slide, assets_dir):
    """
    Reconstructs the authentic perimeter asset layout for Slide 1 (matching T2_slide_1.png).
    Zero stretching, exact rotations, and full Davao cultural geometry.
    """
    f_yellow = os.path.join(assets_dir, "four petal yellow.png")
    q_white = os.path.join(assets_dir, "quarter circle white.png")
    s_yellow = os.path.join(assets_dir, "square yellow.png")
    two_white = os.path.join(assets_dir, "two petal white.png")
    two_yellow = os.path.join(assets_dir, "two petal yellow.png")
    s_white = os.path.join(assets_dir, "square white.png")
    c_yellow = os.path.join(assets_dir, "circle yellow.png")
    hammer = os.path.join(assets_dir, "hammer.png")
    f_white = os.path.join(assets_dir, "four petal white.png")

    # 1. Top-Left edge flower
    if os.path.exists(f_yellow):
        add_fitted_picture(slide, f_yellow, Inches(0.1), Inches(0.0), max_width=Inches(1.15), rotation=15)

    # 2. Mid-Left edge quarter circle
    if os.path.exists(q_white):
        add_fitted_picture(slide, q_white, Inches(-0.05), Inches(3.2), max_width=Inches(0.9), rotation=180)

    # 3. Bottom-Left corner yellow square tile
    if os.path.exists(s_yellow):
        add_fitted_picture(slide, s_yellow, Inches(-0.35), Inches(5.6), max_width=Inches(2.35), rotation=-12)

    # 4. Bottom-Left inner white petal fragment
    if os.path.exists(two_white):
        add_fitted_picture(slide, two_white, Inches(2.0), Inches(6.8), max_width=Inches(0.4), rotation=30)

    # 5. Top-Edge center-right yellow petals
    if os.path.exists(two_yellow):
        add_fitted_picture(slide, two_yellow, Inches(9.8), Inches(-0.1), max_width=Inches(1.1), rotation=180)

    # 6. Top-Right corner white square tile
    if os.path.exists(s_white):
        add_fitted_picture(slide, s_white, Inches(11.6), Inches(-0.2), max_width=Inches(1.85), rotation=20)

    # 7. Mid-Right edge yellow circle
    if os.path.exists(c_yellow):
        add_fitted_picture(slide, c_yellow, Inches(12.3), Inches(2.6), max_width=Inches(0.6))

    # 8. Bottom-Right diagonal gavel (un-stretched, native AR 0.832, native Canva tilt)
    if os.path.exists(hammer):
        add_fitted_picture(slide, hammer, Inches(10.5), Inches(4.5), max_width=Inches(2.85))

    # 9. Bottom-Right near gavel: bottom white petal near adviser
    if os.path.exists(two_white):
        add_fitted_picture(slide, two_white, Inches(10.0), Inches(6.75), max_width=Inches(0.65), rotation=30)


def add_content_slide_decorations(slide, assets_dir, slide_num, paper_ref=None):
    """
    Reconstructs the authentic perimeter asset layout for all content slides (matching T2_slide_2.png).
    Places 8 decorative assets, bottom-right slide number, and clean bottom-left paper reference.
    """
    q_yellow = os.path.join(assets_dir, "quarter circle yellow.png")
    two_yellow = os.path.join(assets_dir, "two petal yellow.png")
    s_white = os.path.join(assets_dir, "square white.png")
    c_yellow = os.path.join(assets_dir, "circle yellow.png")
    two_white = os.path.join(assets_dir, "two petal white.png")
    q_white = os.path.join(assets_dir, "quarter circle white.png")

    # 1. Top-Left corner: yellow quarter circle flush to corner
    if os.path.exists(q_yellow):
        add_fitted_picture(slide, q_yellow, Inches(0.0), Inches(0.0), max_width=Inches(1.2))

    # 2. Below top-left arc: small yellow petal
    if os.path.exists(two_yellow):
        add_fitted_picture(slide, two_yellow, Inches(1.8), Inches(0.8), max_width=Inches(0.45), rotation=35)

    # 3. Top-edge center: yellow flower petals
    if os.path.exists(two_yellow):
        add_fitted_picture(slide, two_yellow, Inches(6.5), Inches(0.1), max_width=Inches(0.45), rotation=180)

    # 4. Top-Right corner: white diamond (square rotated 45 deg)
    if os.path.exists(s_white):
        add_fitted_picture(slide, s_white, Inches(11.8), Inches(0.5), max_width=Inches(0.65), rotation=45)

    # 5. Right-edge center: yellow circle
    if os.path.exists(c_yellow):
        add_fitted_picture(slide, c_yellow, Inches(12.7), Inches(2.3), max_width=Inches(0.45))

    # 6. Bottom-Left corner: small yellow petal
    if os.path.exists(two_yellow):
        add_fitted_picture(slide, two_yellow, Inches(0.2), Inches(6.8), max_width=Inches(0.45), rotation=-20)

    # 7. Bottom-edge center: white flower petals
    if os.path.exists(two_white):
        add_fitted_picture(slide, two_white, Inches(6.2), Inches(6.8), max_width=Inches(0.8), rotation=0)

    # 8. Bottom-Right corner: white quarter circle arc
    if os.path.exists(q_white):
        add_fitted_picture(slide, q_white, Inches(12.5), Inches(6.6), max_width=Inches(0.9), rotation=0)

    # 9. Bottom-Right Slide Number (placed above white arc)
    num_box = slide.shapes.add_textbox(Inches(12.0), Inches(6.65), Inches(0.7), Inches(0.45))
    tf_n = num_box.text_frame
    tf_n.margin_left = tf_n.margin_right = tf_n.margin_top = tf_n.margin_bottom = 0
    p_n = tf_n.paragraphs[0]
    p_n.text = str(slide_num)
    p_n.alignment = PP_ALIGN.RIGHT
    p_n.font.name = "PT Serif"
    p_n.font.size = Pt(18)
    p_n.font.bold = True
    p_n.font.color.rgb = COLOR_WHITE

    # 10. Bottom-Left Paper Reference Grounding (Issue 3: pure subsection pointer, e.g. "Page 17, §1.1")
    if paper_ref:
        ref_box = slide.shapes.add_textbox(Inches(1.2), Inches(6.95), Inches(5.0), Inches(0.35))
        tf_r = ref_box.text_frame
        tf_r.word_wrap = True
        tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
        p_r = tf_r.paragraphs[0]
        p_r.text = paper_ref
        p_r.font.name = "Poppins"
        p_r.font.size = Pt(11)
        p_r.font.color.rgb = COLOR_ICE


def add_divider_slide_decorations(slide, assets_dir):
    """Perimeter assets for major transition / closing slides (Slide 7 and Slide 21)."""
    s_yellow = os.path.join(assets_dir, "square yellow.png")
    s_white = os.path.join(assets_dir, "square white.png")

    if os.path.exists(s_yellow):
        add_fitted_picture(slide, s_yellow, Inches(-0.35), Inches(5.6), max_width=Inches(2.35), rotation=-12)
    if os.path.exists(s_white):
        add_fitted_picture(slide, s_white, Inches(11.6), Inches(-0.2), max_width=Inches(1.85), rotation=20)


def build_presentation():
    base_dir = os.path.dirname(__file__)
    assets_dir = os.path.join(base_dir, "thesis slides assets")
    data_path = os.path.join(base_dir, "presentation_deck_data.json")

    with open(data_path, "r", encoding="utf-8") as f:
        deck_data = json.load(f)

    prs = Presentation()
    # 16:9 widescreen dimensions (13.333 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    print(f"Generating 16:9 Canva-ready presentation ({len(deck_data['slides'])} slides)...")

    for slide_info in deck_data["slides"]:
        slide = prs.slides.add_slide(blank_layout)
        slide_num = slide_info["slide_number"]
        stype = slide_info.get("type", "bullets")
        title_text = slide_info.get("title", "")
        paper_ref = slide_info.get("paper_ref", "")

        # 1. Background Image (always full bleed)
        add_slide_background(slide, assets_dir, prs.slide_width, prs.slide_height)

        # -------------------------------------------------------------
        # SLIDE TYPE: TITLE (Slide 1)
        # -------------------------------------------------------------
        if stype == "title":
            add_title_slide_decorations(slide, assets_dir)

            # Header Category: "CS Thesis Writing II"
            header_box = slide.shapes.add_textbox(Inches(1.5), Inches(1.05), Inches(10.333), Inches(0.5))
            tf_h = header_box.text_frame
            p_h = tf_h.paragraphs[0]
            p_h.text = slide_info.get("header_category", "CS Thesis Writing II")
            p_h.alignment = PP_ALIGN.CENTER
            p_h.font.name = "Poppins"
            p_h.font.size = Pt(21)
            p_h.font.color.rgb = COLOR_WHITE

            # Crisp horizontal white divider line
            line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.8), Inches(1.65), Inches(9.733), Inches(0.02))
            line.fill.solid()
            line.fill.fore_color.rgb = COLOR_WHITE
            line.line.color.rgb = COLOR_WHITE

            # Centered 4-line Title in PT Serif Bold
            tbox = slide.shapes.add_textbox(Inches(1.5), Inches(2.15), Inches(10.333), Inches(2.6))
            tf_t = tbox.text_frame
            tf_t.word_wrap = True
            p_t = tf_t.paragraphs[0]
            p_t.text = title_text
            p_t.alignment = PP_ALIGN.CENTER
            p_t.font.name = "PT Serif"
            p_t.font.size = Pt(29)
            p_t.font.bold = True
            p_t.font.color.rgb = COLOR_WHITE

            # Bottom Left: Proponents
            prop_box = slide.shapes.add_textbox(Inches(2.6), Inches(5.1), Inches(3.6), Inches(1.6))
            tf_p = prop_box.text_frame
            tf_p.word_wrap = True
            p_ph = tf_p.paragraphs[0]
            p_ph.text = "Proponents:"
            p_ph.font.name = "Poppins"
            p_ph.font.size = Pt(18)
            p_ph.font.bold = True
            p_ph.font.color.rgb = COLOR_WHITE

            for name in slide_info.get("proponents", []):
                pn = tf_p.add_paragraph()
                pn.text = name
                pn.font.name = "Poppins"
                pn.font.size = Pt(17)
                pn.font.color.rgb = COLOR_WHITE

            # Bottom Right: Adviser
            adv_box = slide.shapes.add_textbox(Inches(7.4), Inches(5.1), Inches(4.5), Inches(1.6))
            tf_a = adv_box.text_frame
            tf_a.word_wrap = True
            p_ah = tf_a.paragraphs[0]
            p_ah.text = "Adviser:"
            p_ah.font.name = "Poppins"
            p_ah.font.size = Pt(18)
            p_ah.font.bold = True
            p_ah.font.color.rgb = COLOR_WHITE

            pa = tf_a.add_paragraph()
            pa.text = slide_info.get("adviser", "")
            pa.font.name = "Poppins"
            pa.font.size = Pt(17)
            pa.font.color.rgb = COLOR_WHITE

        # -------------------------------------------------------------
        # SLIDE TYPE: SECTION HEADER / DIVIDER (Slide 7)
        # -------------------------------------------------------------
        elif stype == "section_header":
            add_divider_slide_decorations(slide, assets_dir)

            tbox = slide.shapes.add_textbox(Inches(1.5), Inches(2.8), Inches(10.333), Inches(1.8))
            tf_t = tbox.text_frame
            tf_t.word_wrap = True
            p_t = tf_t.paragraphs[0]
            p_t.text = title_text
            p_t.alignment = PP_ALIGN.CENTER
            p_t.font.name = "PT Serif"
            p_t.font.size = Pt(54)
            p_t.font.bold = True
            p_t.font.color.rgb = COLOR_WHITE

        # -------------------------------------------------------------
        # SLIDE TYPE: CLOSING (Slide 21)
        # -------------------------------------------------------------
        elif stype == "closing":
            add_divider_slide_decorations(slide, assets_dir)

            tbox = slide.shapes.add_textbox(Inches(1.5), Inches(2.7), Inches(10.333), Inches(2.0))
            tf_t = tbox.text_frame
            tf_t.word_wrap = True
            p_t = tf_t.paragraphs[0]
            p_t.text = title_text
            p_t.alignment = PP_ALIGN.CENTER
            p_t.font.name = "PT Serif"
            p_t.font.size = Pt(44)
            p_t.font.bold = True
            p_t.font.color.rgb = COLOR_WHITE

        # -------------------------------------------------------------
        # SLIDE TYPE: CONCEPTUAL FRAMEWORK (Slide 6)
        # -------------------------------------------------------------
        elif stype == "conceptual_framework":
            # Gavel accent at top-left, matching T2_slide_6.png
            hammer_path = os.path.join(assets_dir, "hammer.png")
            if os.path.exists(hammer_path):
                add_fitted_picture(slide, hammer_path, Inches(0.1), Inches(0.1), max_width=Inches(1.8), rotation=-40)

            # Left side: "Conceptual Framework" in large PT Serif
            tbox = slide.shapes.add_textbox(Inches(1.2), Inches(2.7), Inches(5.8), Inches(2.4))
            tf_t = tbox.text_frame
            tf_t.word_wrap = True
            p_t = tf_t.paragraphs[0]
            p_t.text = "Conceptual\nFramework"
            p_t.font.name = "PT Serif"
            p_t.font.size = Pt(50)
            p_t.font.bold = True
            p_t.font.color.rgb = COLOR_WHITE

            # Right side: Full Conceptual Framework Flowchart
            img_rel_path = slide_info.get("image_path", "")
            img_path = os.path.join(os.path.dirname(base_dir), img_rel_path) if not os.path.isabs(img_rel_path) else img_rel_path
            if not os.path.exists(img_path):
                img_path = os.path.join(base_dir, img_rel_path)

            if os.path.exists(img_path):
                # Clean white backing card
                card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.5), Inches(0.35), Inches(4.7), Inches(6.75))
                card.fill.solid()
                card.fill.fore_color.rgb = COLOR_WHITE
                card.line.color.rgb = COLOR_WHITE

                # Fitted flowchart picture inside the card
                add_fitted_picture(slide, img_path, Inches(7.55), Inches(0.4), max_width=Inches(4.6), max_height=Inches(6.65))

            # Bottom-left paper ref
            ref_box = slide.shapes.add_textbox(Inches(1.2), Inches(6.95), Inches(5.0), Inches(0.35))
            tf_r = ref_box.text_frame
            p_r = tf_r.paragraphs[0]
            p_r.text = paper_ref
            p_r.font.name = "Poppins"
            p_r.font.size = Pt(11)
            p_r.font.color.rgb = COLOR_ICE

            # Bottom-right slide number
            num_box = slide.shapes.add_textbox(Inches(12.0), Inches(6.65), Inches(0.7), Inches(0.45))
            tf_n = num_box.text_frame
            p_n = tf_n.paragraphs[0]
            p_n.text = str(slide_num)
            p_n.alignment = PP_ALIGN.RIGHT
            p_n.font.name = "PT Serif"
            p_n.font.size = Pt(18)
            p_n.font.bold = True
            p_n.font.color.rgb = COLOR_WHITE

        # -------------------------------------------------------------
        # SLIDE TYPE: BULLETS / SOP / OBJECTIVES
        # -------------------------------------------------------------
        elif stype == "bullets":
            add_content_slide_decorations(slide, assets_dir, slide_num, paper_ref)

            # Pure Subsection Title
            tbox = slide.shapes.add_textbox(Inches(1.2), Inches(0.95), Inches(10.5), Inches(0.9))
            tf_t = tbox.text_frame
            tf_t.word_wrap = True
            p_t = tf_t.paragraphs[0]
            p_t.text = title_text
            p_t.font.name = "PT Serif"
            p_t.font.size = Pt(36)
            p_t.font.bold = True
            p_t.font.color.rgb = COLOR_WHITE

            # Bullets
            bbox = slide.shapes.add_textbox(Inches(1.2), Inches(2.15), Inches(10.8), Inches(4.65))
            tf_b = bbox.text_frame
            tf_b.word_wrap = True
            tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0

            points = slide_info.get("talking_points", [])
            # Dynamic font sizing: slightly more compact if bullets are long
            max_len = max(len(p) for p in points) if points else 0
            font_size = Pt(17.5) if max_len > 75 else Pt(20)
            space_after = Pt(13) if max_len > 75 else Pt(16)

            for idx, pt in enumerate(points):
                add_bullet_with_formatting(tf_b, pt, is_first=(idx == 0), font_size=font_size, space_after=space_after)

        # -------------------------------------------------------------
        # SLIDE TYPE: TABLE IMAGE (Slide 13, 14 - Standard Width)
        # -------------------------------------------------------------
        elif stype == "table_image":
            add_content_slide_decorations(slide, assets_dir, slide_num, paper_ref)

            # Pure Subsection Title
            tbox = slide.shapes.add_textbox(Inches(1.2), Inches(0.8), Inches(10.5), Inches(0.85))
            tf_t = tbox.text_frame
            tf_t.word_wrap = True
            p_t = tf_t.paragraphs[0]
            p_t.text = title_text
            p_t.font.name = "PT Serif"
            p_t.font.size = Pt(36)
            p_t.font.bold = True
            p_t.font.color.rgb = COLOR_WHITE

            # Centered Table Image (ZERO bullets below, pure table-only!)
            img_rel_path = slide_info.get("image_path", "")
            img_path = os.path.join(os.path.dirname(base_dir), img_rel_path) if not os.path.isabs(img_rel_path) else img_rel_path
            if not os.path.exists(img_path):
                img_path = os.path.join(base_dir, img_rel_path)

            if os.path.exists(img_path):
                max_w = Inches(10.6)
                max_h = Inches(4.8)

                with Image.open(img_path) as im:
                    orig_w, orig_h = im.size
                scale = min(max_w / orig_w, max_h / orig_h)
                actual_w = orig_w * scale
                actual_h = orig_h * scale

                # Center horizontally and vertically within content area
                actual_left = Inches(1.2) + (max_w - actual_w) / 2
                actual_top = Inches(1.85) + (max_h - actual_h) / 2

                # Crisp white card backing
                card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, actual_left - Inches(0.12), actual_top - Inches(0.12), actual_w + Inches(0.24), actual_h + Inches(0.24))
                card.fill.solid()
                card.fill.fore_color.rgb = COLOR_WHITE
                card.line.color.rgb = COLOR_WHITE

                # Add table picture on top
                slide.shapes.add_picture(img_path, actual_left, actual_top, width=actual_w, height=actual_h)

        # -------------------------------------------------------------
        # SLIDE TYPE: TABLE IMAGE TALL (Slide 16, 17 - Tall 28-Model Tables)
        # -------------------------------------------------------------
        elif stype == "table_image_tall":
            add_content_slide_decorations(slide, assets_dir, slide_num, paper_ref)

            # Tall tables (Table 4.7 and 4.8) contain their own caption at the top of the cropped image
            # and span vertically across the slide for maximum font size and legibility.
            img_rel_path = slide_info.get("image_path", "")
            img_path = os.path.join(os.path.dirname(base_dir), img_rel_path) if not os.path.isabs(img_rel_path) else img_rel_path
            if not os.path.exists(img_path):
                img_path = os.path.join(base_dir, img_rel_path)

            if os.path.exists(img_path):
                max_w = Inches(10.6)
                max_h = Inches(6.5)

                with Image.open(img_path) as im:
                    orig_w, orig_h = im.size
                scale = min(max_w / orig_w, max_h / orig_h)
                actual_w = orig_w * scale
                actual_h = orig_h * scale

                actual_left = Inches(1.2) + (max_w - actual_w) / 2
                actual_top = Inches(0.35) + (max_h - actual_h) / 2

                # Crisp white card backing
                card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, actual_left - Inches(0.12), actual_top - Inches(0.12), actual_w + Inches(0.24), actual_h + Inches(0.24))
                card.fill.solid()
                card.fill.fore_color.rgb = COLOR_WHITE
                card.line.color.rgb = COLOR_WHITE

                slide.shapes.add_picture(img_path, actual_left, actual_top, width=actual_w, height=actual_h)

        # -------------------------------------------------------------
        # SLIDE TYPE: FIGURE (Slide 9, 18)
        # -------------------------------------------------------------
        elif stype == "figure":
            add_content_slide_decorations(slide, assets_dir, slide_num, paper_ref)

            # Pure Subsection Title
            tbox = slide.shapes.add_textbox(Inches(1.2), Inches(0.8), Inches(10.5), Inches(0.85))
            tf_t = tbox.text_frame
            tf_t.word_wrap = True
            p_t = tf_t.paragraphs[0]
            p_t.text = title_text
            p_t.font.name = "PT Serif"
            p_t.font.size = Pt(36)
            p_t.font.bold = True
            p_t.font.color.rgb = COLOR_WHITE

            img_rel_path = slide_info.get("image_path", "")
            img_path = os.path.join(os.path.dirname(base_dir), img_rel_path) if not os.path.isabs(img_rel_path) else img_rel_path
            if not os.path.exists(img_path):
                img_path = os.path.join(base_dir, img_rel_path)

            if os.path.exists(img_path):
                max_w = Inches(10.6)
                max_h = Inches(4.85)

                with Image.open(img_path) as im:
                    orig_w, orig_h = im.size
                scale = min(max_w / orig_w, max_h / orig_h)
                actual_w = orig_w * scale
                actual_h = orig_h * scale

                actual_left = Inches(1.2) + (max_w - actual_w) / 2
                actual_top = Inches(1.85) + (max_h - actual_h) / 2

                # Crisp white card backing
                card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, actual_left - Inches(0.12), actual_top - Inches(0.12), actual_w + Inches(0.24), actual_h + Inches(0.24))
                card.fill.solid()
                card.fill.fore_color.rgb = COLOR_WHITE
                card.line.color.rgb = COLOR_WHITE

                slide.shapes.add_picture(img_path, actual_left, actual_top, width=actual_w, height=actual_h)

    out_pptx = os.path.join(base_dir, "Thesis_2_Defense_Presentation.pptx")
    prs.save(out_pptx)
    print(f"Successfully generated Canva-ready PPTX: {out_pptx}")


if __name__ == "__main__":
    build_presentation()
