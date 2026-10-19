import re
import json
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.pdfgen import canvas

REPO_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = REPO_ROOT / "demo" / "sample_cases"
OUTPUT_DIR_DEMO = REPO_ROOT / "demo" / "sample_cases" / "pdf"
OUTPUT_DIR_TIER3 = REPO_ROOT / "data" / "tier3_landmark_ordinances_pdf"

OUTPUT_DIR_DEMO.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR_TIER3.mkdir(parents=True, exist_ok=True)

PAGE_WIDTH = 8.5 * inch
PAGE_HEIGHT = 13.0 * inch
MARGIN_LEFT = 1.25 * inch
MARGIN_RIGHT = 1.0 * inch
MARGIN_TOP = 1.0 * inch
MARGIN_BOTTOM = 1.0 * inch
USABLE_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

class CleanSPCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        page_num = self._pageNumber
        # Running Header on page 2+ (Authentic Sangguniang Panlungsod format)
        if page_num > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#334155"))
            header_text = getattr(self, "ord_no_header", "CITY OF DAVAO • SANGGUNIANG PANLUNGSOD")
            self.drawString(MARGIN_LEFT, PAGE_HEIGHT - 0.65 * inch, header_text)
            
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, PAGE_HEIGHT - 0.65 * inch, f"Page {page_num} of {total_pages}")
            
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(MARGIN_LEFT, PAGE_HEIGHT - 0.70 * inch, PAGE_WIDTH - MARGIN_RIGHT, PAGE_HEIGHT - 0.70 * inch)

        # Page 1 Bottom Page Number (NO ARCHIVE OR LANDMARK FLUFF)
        if page_num == 1 and total_pages > 1:
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, MARGIN_BOTTOM - 0.35 * inch, f"Page 1 of {total_pages}")


def sanitize_text(text: str) -> str:
    """Sanitize unicode characters for standard ReportLab Helvetica font."""
    if not text:
        return ""
    text = text.replace("\u20b1", "P ") # Philippine Peso sign -> P
    text = text.replace("₱", "P ")
    text = text.replace("—", " &mdash; ")
    text = text.replace("–", " &mdash; ")
    text = text.replace("“", """).replace("”", """)
    text = text.replace("‘", "'").replace("’", "'")
    text = text.replace("\u00a7", "&sect;")
    text = text.replace("&sect;", "Section ")
    return text


def build_markdown_table(table_lines, styles, usable_width=USABLE_WIDTH):
    """Parse markdown table lines into a styled ReportLab Table flowable."""
    rows = []
    for line in table_lines:
        line_clean = line.strip()
        if re.match(r'^\|[\-\:\s\|]+$', line_clean):
            continue
        cols = [c.strip() for c in line_clean.strip('|').split('|')]
        rows.append(cols)

    if not rows:
        return None

    # Determine max columns
    max_cols = max(len(r) for r in rows)
    # Pad rows to max_cols
    for r in rows:
        while len(r) < max_cols:
            r.append("")

    col_w = usable_width / max_cols

    cell_data = []
    for r_idx, r in enumerate(rows):
        row_cells = []
        is_header = (r_idx == 0)
        for c in r:
            c_sanitized = sanitize_text(c)
            cell_style = styles['SPTableHeader'] if is_header else styles['SPTableCell']
            row_cells.append(Paragraph(c_sanitized, cell_style))
        cell_data.append(row_cells)

    t = Table(cell_data, colWidths=[col_w] * max_cols)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    return t


def format_section_paragraphs(sec_num, sec_title, text, styles):
    """
    Format a section's text into clean ReportLab flowables:
    - Extracts trailing CHAPTER or ARTICLE headings
    - Splits text into lead heading, paragraphs, indented list items, and markdown tables
    - Bolds term definitions in list items
    """
    flowables = []
    body_style = styles['SPBody']
    list_style = styles['SPListItem']
    
    clean_text = sanitize_text(text.strip())
    trailing_chapter = None
    
    # 1. Extract trailing CHAPTER / ARTICLE
    m_chap = re.search(r'\n+((?:CHAPTER\s+[0-9IVXLCDM]+[^\n]*|\bARTICLE\s+[0-9IVXLCDM]+[^\n]*)\b.*)$', clean_text, re.IGNORECASE | re.DOTALL)
    if m_chap:
        trailing_chapter = m_chap.group(1).strip()
        clean_text = clean_text[:m_chap.start()].strip()
        
    clean_text = re.sub(r'^[\.\-\:\s\,]+', '', clean_text).strip()
    
    sec_heading = f"<b>SECTION {sec_num}. {sec_title}.</b> &mdash; "
    
    if not clean_text:
        flowables.append(Paragraph(sec_heading.strip(), body_style))
        flowables.append(Spacer(1, 4))
        return flowables, trailing_chapter

    raw_lines = [l.strip() for l in clean_text.split('\n') if l.strip()]
    
    # 2. Check for markdown table blocks
    i = 0
    first_block = True
    while i < len(raw_lines):
        line = raw_lines[i]
        
        # Check if line is start of markdown table
        if line.startswith('|') and line.endswith('|'):
            table_lines = []
            while i < len(raw_lines) and raw_lines[i].startswith('|') and raw_lines[i].endswith('|'):
                table_lines.append(raw_lines[i])
                i += 1
            table_flowable = build_markdown_table(table_lines, styles)
            if table_flowable:
                flowables.append(Spacer(1, 4))
                flowables.append(table_flowable)
                flowables.append(Spacer(1, 6))
            continue
            
        # Check if line is list item
        # Matches: a., b., (a), (b), 1., 2., (1), (2), A., B., - , SECTION 12.1.
        m_item = re.match(r'^([a-z]\.|\([a-z]\)|[a-z]\)|[0-9]+\.|\([0-9]+\)|[0-9]+\)|[A-Z]\.|\([A-Z]\)|\-|\bSECTION\s+[0-9]+\.[0-9]+[\.\:]?)\s*(.*)$', line, re.IGNORECASE)
        
        # Check if line is an authentic signing block element
        m_sign = re.match(r'^(ENACTED[\:\,]|CERTIFIED CORRECT[\:\,]|ATTESTED[\:\,]|APPROVED[\:\,]|FOR AND IN THE ABSENCE OF THE SECRETARY[\:\,])', line, re.IGNORECASE)
        
        if m_sign:
            # Signing block styling
            flowables.append(Spacer(1, 6))
            flowables.append(Paragraph(f"<b>{line}</b>", styles['SPSigningHeader']))
            flowables.append(Spacer(1, 3))
            i += 1
            continue

        if m_item:
            marker = m_item.group(1)
            rest = m_item.group(2)
            # Check if rest has term - definition
            m_term = re.match(r'^([A-Z0-9\s\(\)\'\-]+?)\s*[\-\–\—\:]\s*(.*)$', rest)
            if m_term and len(m_term.group(1).strip()) < 60:
                item_text = f"<b>{marker} {m_term.group(1).strip()}</b> &mdash; {m_term.group(2).strip()}"
            elif rest.startswith("refers to") or rest.startswith("shall refer to"):
                item_text = f"<b>{marker}</b> {rest}"
            else:
                item_text = f"<b>{marker}</b> {rest}"
                
            if first_block:
                flowables.append(Paragraph(f"{sec_heading}<br/>{item_text}", list_style))
                first_block = False
            else:
                flowables.append(Paragraph(item_text, list_style))
            flowables.append(Spacer(1, 3))
        else:
            if first_block:
                flowables.append(Paragraph(f"{sec_heading}{line}", body_style))
                first_block = False
            else:
                flowables.append(Paragraph(line, body_style))
            flowables.append(Spacer(1, 4))
            
        i += 1
        
    return flowables, trailing_chapter


def compile_clean_pdf(json_path: Path, out_path: Path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM
    )

    base_styles = getSampleStyleSheet()
    styles = {
        'SPHeaderCenter': ParagraphStyle(
            'SPHeaderCenter',
            parent=base_styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            alignment=1,
            textColor=colors.HexColor('#1E293B')
        ),
        'SPTitle': ParagraphStyle(
            'SPTitle',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=15,
            alignment=1,
            textColor=colors.HexColor('#0F172A'),
            spaceAfter=12
        ),
        'SPEnacting': ParagraphStyle(
            'SPEnacting',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=13,
            alignment=0,
            textColor=colors.HexColor('#0F172A'),
            spaceBefore=10,
            spaceAfter=10
        ),
        'SPChapterHeading': ParagraphStyle(
            'SPChapterHeading',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=14,
            alignment=1, # Centered
            textColor=colors.HexColor('#1E293B'),
            spaceBefore=12,
            spaceAfter=8
        ),
        'SPBody': ParagraphStyle(
            'SPBody',
            parent=base_styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13.5,
            alignment=4, # Justify
            textColor=colors.HexColor('#1E293B'),
            spaceAfter=6
        ),
        'SPListItem': ParagraphStyle(
            'SPListItem',
            parent=base_styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13.5,
            leftIndent=24,
            firstLineIndent=-14,
            alignment=4, # Justify
            textColor=colors.HexColor('#1E293B'),
            spaceAfter=4
        ),
        'SPTableHeader': ParagraphStyle(
            'SPTableHeader',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=11,
            alignment=0,
            textColor=colors.HexColor('#0F172A')
        ),
        'SPTableCell': ParagraphStyle(
            'SPTableCell',
            parent=base_styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=11,
            alignment=0,
            textColor=colors.HexColor('#1E293B')
        ),
        'SPSigningHeader': ParagraphStyle(
            'SPSigningHeader',
            parent=base_styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=13,
            alignment=0,
            textColor=colors.HexColor('#0F172A'),
            spaceBefore=8,
            spaceAfter=3
        )
    }

    story = []

    # 1. Legislative Letterhead (Official Government of Davao City format)
    story.append(Paragraph("<b>REPUBLIC OF THE PHILIPPINES</b>", styles['SPHeaderCenter']))
    lgu_name = data.get('enacting_lgu', 'CITY OF DAVAO').upper()
    story.append(Paragraph(f"<b>{lgu_name}</b>", styles['SPHeaderCenter']))
    council_name = "CITY COUNCIL OF MANILA" if "MANILA" in lgu_name else "OFFICE OF THE SANGGUNIANG PANLUNGSOD"
    story.append(Paragraph(f"<b>{council_name}</b>", styles['SPHeaderCenter']))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#7F2723'), spaceAfter=14))

    # 2. Ordinance Number & Long Title (NO JUDICIAL CONTEXT!)
    ord_no = sanitize_text(data.get('ordinance_no', ''))
    if ord_no:
        story.append(Paragraph(f"<b>{ord_no}</b>", styles['SPTitle']))
    story.append(Paragraph(f"<b>{sanitize_text(data.get('title', ''))}</b>", styles['SPTitle']))
    story.append(Spacer(1, 10))

    # 3. Enacting Clause
    enacting_clause = sanitize_text(data.get("enacting_clause", "Be it ordained by the Sangguniang Panlungsod of Davao City in session assembled:"))
    story.append(Paragraph(f"<b>{enacting_clause}</b>", styles['SPEnacting']))
    story.append(Spacer(1, 6))

    # 4. Sections with list item formatting, table parsing & chapter separation
    pending_chapter = None
    for s in data.get("sections", []):
        chap = s.get('chapter') or pending_chapter
        if chap:
            story.append(Spacer(1, 6))
            for c_line in chap.split('\n'):
                if c_line.strip():
                    story.append(Paragraph(f"<b>{c_line.strip().upper()}</b>", styles['SPChapterHeading']))
            story.append(Spacer(1, 6))
            pending_chapter = None

        flowables, trailing_ch = format_section_paragraphs(s['sec_num'], s['sec_title'], s['text'], styles)
        story.extend(flowables)
        if trailing_ch:
            pending_chapter = trailing_ch

    # Build document
    canvas_maker = CleanSPCanvas
    canvas_maker.ord_no_header = f"{ord_no} • {lgu_name}" if ord_no else lgu_name
    doc.build(story, canvasmaker=canvas_maker)


def sync_clean_txt_files():
    """
    Synchronize .txt files in demo/sample_cases/ so they contain pure authentic
    legislative text without Judicial Reference, Gold NLI Label, etc.
    """
    for json_file in sorted(INPUT_DIR.glob("*.json")):
        txt_file = json_file.with_suffix(".txt")
        with open(json_file, "r", encoding="utf-8") as f:
            d = json.load(f)
            
        lgu_name = d.get('enacting_lgu', 'City of Davao')
        ord_no = d.get('ordinance_no', '')
        title = d.get('title', '')
        enacting_clause = d.get('enacting_clause', 'Be it ordained by the Sangguniang Panlungsod of Davao City in session assembled:')
        
        lines = []
        lines.append("REPUBLIC OF THE PHILIPPINES")
        lines.append(lgu_name.upper())
        if "MANILA" in lgu_name.upper():
            lines.append("CITY COUNCIL OF MANILA")
        else:
            lines.append("OFFICE OF THE SANGGUNIANG PANLUNGSOD")
        lines.append("")
        if ord_no:
            lines.append(ord_no)
        lines.append(title)
        lines.append("")
        lines.append(enacting_clause)
        lines.append("")
        
        for s in d.get("sections", []):
            lines.append(f"SECTION {s['sec_num']}. {s['sec_title']} - {s['text']}")
            lines.append("")
            
        clean_content = "\n".join(lines).strip() + "\n"
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(clean_content)
        print(f"Cleaned TXT: {txt_file.name}")


if __name__ == "__main__":
    json_files = sorted(INPUT_DIR.glob("*.json"))
    print(f"Compiling {len(json_files)} authentic Sangguniang Panlungsod PDFs...")
    for jf in json_files:
        pdf_name = f"{jf.stem}.pdf"
        out_pdf_demo = OUTPUT_DIR_DEMO / pdf_name
        out_pdf_tier3 = OUTPUT_DIR_TIER3 / pdf_name
        
        # Compile to demo/sample_cases/pdf/
        compile_clean_pdf(jf, out_pdf_demo)
        # Compile to data/tier3_landmark_ordinances_pdf/
        compile_clean_pdf(jf, out_pdf_tier3)
        print(f"Generated clean PDF: {pdf_name}")
        
    print("\nSynchronizing clean authentic TXT files...")
    sync_clean_txt_files()
    print("\nAll 11 landmark ordinance PDFs and TXTs compiled successfully with zero academic fluff!")
