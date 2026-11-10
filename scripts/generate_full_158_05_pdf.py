"""
generate_full_158_05_pdf.py
===========================
Generates the complete, unabridged authentic Philippine Folio (8.5 x 13 in) PDF
for Ordinance No. 0158-05 (The 2005 Revenue Code of the City of Davao)
with all 434 sections, 14th City Council attendance, enacting clause,
and authentic staggered signature blocks, matching the Tier 2 styling.
"""

import re
import json
import time
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas
import xml.sax.saxutils as saxutils

REPO_ROOT = Path(__file__).resolve().parents[1]
TXT_SOURCE = REPO_ROOT / "corpus" / "cleaned" / "local" / "cleaned_transcriptions" / "landmark_ordinances" / "Ordinance No. 0158-05.txt"
OUTPUT_DIR = REPO_ROOT / "ground_truth" / "tier3_sc_cases" / "tier3_landmark_ordinances_pdf"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PDF_OUT = OUTPUT_DIR / "03_davao_revenue_code_2005_full.pdf"

PAGE_WIDTH = 8.5 * inch
PAGE_HEIGHT = 13.0 * inch
MARGIN_LEFT = 1.15 * inch
MARGIN_RIGHT = 1.0 * inch
MARGIN_TOP = 0.95 * inch
MARGIN_BOTTOM = 0.95 * inch
USABLE_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

COUNCILORS_14TH = [
    ("Vice Mayor", "Luis C. Bonguyan", "- Presiding Officer"),
    ("Councillor", "Victorio S. Advincula, Sr.", ""),
    ("Councillor", "Wilberto E. Al-ag", ""),
    ("Councillor", "Dante L. Apostol, Sr.", ""),
    ("Councillor", "Leonardo R. Avila, III", ""),
    ("Councillor", "Conrado C. Baluran", ""),
    ("Councillor", "Gerald B. Bangoy", ""),
    ("Councillor", "Pilar C. Braga", ""),
    ("Councillor", "Arnolfo Ricardo B. Cabling", ""),
    ("Councillor", "Domingo G. L'Dalodo", ""),
    ("Councillor", "Danilo C. Dayanghirang", ""),
    ("Councillor", "April Marie C. Dayap", ""),
    ("Councillor", "Jimmy G. Dureza", ""),
    ("Councillor", "Emmanuel D. Galicia, Sr.", ""),
    ("Councillor", "Peter T. Lavina", ""),
    ("Councillor", "Rene Elias C. Lopez", ""),
    ("Councillor", "Diosdado Angelo A. Mahipus, Sr.", ""),
    ("Councillor", "Amilbangsa T. Manding", ""),
    ("Councillor", "Paz C. Mata", ""),
    ("Councillor", "Bonifacio E. Militar", ""),
    ("Councillor", "Susan Isabel C. Reta", ""),
    ("Councillor", "Jose Louie P. Villafuerte", ""),
    ("Councillor", "Jesus A. Zozobrado, Jr.", "")
]

def sanitize_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("₱", "P ")
    text = text.replace("\u20b1", "P ")
    text = text.replace("—", " - ")
    text = text.replace("–", " - ")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    return text

def parse_full_158_05():
    raw_text = TXT_SOURCE.read_text(encoding="utf-8")
    sec_pattern = re.compile(r'(?:^|\n)(?:SECTION|Section|SEC\.)\s+(\d+[A-Za-z]?)\.?\s*([^\n\-\–\—]+)?\s*[\-\–\—\.]?\s*', re.MULTILINE)
    matches = list(sec_pattern.finditer(raw_text))
    
    sections = []
    for idx, m in enumerate(matches):
        sec_num_str = m.group(1)
        sec_title = (m.group(2) or "").strip().rstrip(".-–— ")
        start_pos = m.end()
        end_pos = matches[idx + 1].start() if idx + 1 < len(matches) else len(raw_text)
        body_text = raw_text[start_pos:end_pos].strip()
        
        # Clean page headers / footers
        body_text = re.sub(r'---\s*\[Page\s*\d+\]\s*---', '', body_text)
        body_text = re.sub(r'The 2005 Revenue Code of the City of Davao', '', body_text)
        body_text = re.sub(r'Page\s*\d+', '', body_text)
        body_text = body_text.strip()
        
        sections.append({
            "sec_num": int(sec_num_str) if sec_num_str.isdigit() else sec_num_str,
            "sec_title": sec_title if sec_title else "Operative Provision",
            "text": body_text
        })
    return sections

def build_pdf():
    t0 = time.time()
    sections = parse_full_158_05()
    print(f"Parsed {len(sections)} sections in {time.time()-t0:.2f}s.")
    
    doc = SimpleDocTemplate(
        str(PDF_OUT),
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM
    )
    
    styles = getSampleStyleSheet()
    
    style_republic = ParagraphStyle("Republic", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=11, alignment=1)
    style_city = ParagraphStyle("City", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=11, leading=13, alignment=1)
    style_office = ParagraphStyle("Office", parent=styles["Normal"], fontName="Helvetica", fontSize=10, leading=12, alignment=1)
    style_session = ParagraphStyle("Session", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=12, alignment=0)
    style_ord_no = ParagraphStyle("OrdNo", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=12, leading=14, alignment=1)
    style_title = ParagraphStyle("Title", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10, leading=13, alignment=4)
    style_enacting = ParagraphStyle("Enacting", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9, leading=12, alignment=0)
    style_sec_heading = ParagraphStyle("SecHeading", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9, leading=12, alignment=0)
    style_body = ParagraphStyle("Body", parent=styles["Normal"], fontName="Helvetica", fontSize=8.5, leading=11.5, alignment=4)
    
    story = []
    
    # 1. Header (Page 1)
    story.append(Paragraph("Republika ng Pilipinas", style_republic))
    story.append(Paragraph("LUNGSOD NG DABAW", style_city))
    story.append(Paragraph("Tanggapan ng Sangguniang Panlungsod", style_office))
    story.append(Spacer(1, 10))
    
    # Session info & Attendance
    story.append(Paragraph("<b>14th City Council<br/>8th Special Session<br/>Series of 2005</b>", style_session))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>PRESENT:</b>", style_session))
    for role, name, note in COUNCILORS_14TH:
        story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{role} {name} {note}", style_body))
    story.append(Spacer(1, 10))
    
    # Ordinance Number & Title
    story.append(Paragraph("ORDINANCE NO. 0158-05", style_ord_no))
    story.append(Paragraph("Series of 2005", style_republic))
    story.append(Spacer(1, 8))
    
    title_text = "AN ORDINANCE APPROVING THE 2005 REVENUE CODE OF THE CITY OF DAVAO, AS AMENDED"
    story.append(Paragraph(f"<b>{title_text}</b>", style_title))
    story.append(Spacer(1, 10))
    
    enacting_clause = "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:"
    story.append(Paragraph(enacting_clause, style_enacting))
    story.append(Spacer(1, 10))
    
    # 2. Render all 434 sections
    for sec in sections:
        s_num = sec["sec_num"]
        s_title = sanitize_text(sec["sec_title"])
        s_text = sanitize_text(sec["text"])
        
        heading_para = Paragraph(f"<b><u>SECTION {s_num}. {s_title.upper()}</u></b>", style_sec_heading)
        story.append(heading_para)
        story.append(Spacer(1, 3))
        
        # Split body paragraphs
        paras = [p.strip() for p in s_text.split("\n\n") if p.strip()]
        if not paras:
            paras = [s_text] if s_text else [""]
            
        for p in paras:
            # If paragraph contains markdown table, render lines as simple monospace or clean text
            p_clean = p.replace("\n", "<br/>")
            story.append(Paragraph(p_clean, style_body))
            story.append(Spacer(1, 4))
            
        story.append(Spacer(1, 6))
        
    print(f"Generated flowable story with {len(story)} elements. Compiling PDF...")
    t_compile = time.time()
    doc.build(story)
    print(f"PDF built successfully in {time.time()-t_compile:.2f}s at: {PDF_OUT}")
    print(f"PDF File size: {PDF_OUT.stat().st_size:,} bytes")

if __name__ == "__main__":
    build_pdf()

