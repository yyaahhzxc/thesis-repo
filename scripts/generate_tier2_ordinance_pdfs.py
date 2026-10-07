"""
generate_tier2_ordinance_pdfs.py
================================
Generates authentic Philippine Legal/Folio (8.5 x 13 in) PDFs for the 10 synthetic
Tier 2 draft ordinances in `data/tier2_draft_ordinances/`, copying the exact visual
layout, typography, and administrative structure of Sangguniang Panlungsod ng Dabaw.

Authentic Features:
- Legal/Folio Paper Size: 8.5 x 13.0 inches (612 x 936 pt)
- Margins: Left 1.25 in (binding gutter), Right 1.0 in, Top 1.0 in, Bottom 1.0 in
- Page 1 Header: Republic of the Philippines / City of Davao / Office of the Sangguniang Panlungsod
- Session Roster: Two-column Present / Absent councilor list
- Centered Long Title in Bold Caps
- Running Header on Page 2+: 'Page X of Y' and 'Proposed Ord. No. 2026-XX'
- Operational Sections: 'SECTION X. TITLE. - Body text...'
- Official Enactment, Certification, Attestation, and Mayoral Approval Sign-off Block
"""

import os
import json
from pathlib import Path
from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

REPO_ROOT = Path(r"c:\Users\HP\Documents\GitHub\thesis-repo")
INPUT_DIR = REPO_ROOT / "data" / "tier2_draft_ordinances"
OUTPUT_DIR = REPO_ROOT / "data" / "tier2_draft_ordinances_pdf"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Philippine Legal / Folio size: 8.5 x 13.0 inches
PAGE_WIDTH = 8.5 * inch
PAGE_HEIGHT = 13.0 * inch
MARGIN_LEFT = 1.25 * inch
MARGIN_RIGHT = 1.0 * inch
MARGIN_TOP = 1.0 * inch
MARGIN_BOTTOM = 1.0 * inch
USABLE_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

COUNCILORS_PRESENT = [
    ("Vice Mayor J. Melchor B. Quitain Jr.", "- Presiding Officer"),
    ("Councilor Marissa S. Abella", "Councilor Louie John J. Bonguyan"),
    ("Councilor Nilo M. Abellera Jr.", "Councilor Pilar C. Braga"),
    ("Councilor Luna Maria Dominique S. Acosta", "Councilor Jonard C. Dayap"),
    ("Councilor Bernard E. Al-ag", "Councilor Edgar P. Ibuyan Jr."),
    ("Councilor Wilberto E. Al-ag", "Councilor Richlyn N. Justol-Baguilod"),
    ("Councilor Al Ryan S. Alejandre", "Councilor Diosdado Angelo Junior R. Mahipus"),
    ("Councilor Dante L. Apostol Sr.", "Councilor Bonz Andre A. Militar"),
    ("Councilor Conrado C. Baluran", "Councilor Temujin B. Ocampo"),
    ("Councilor Jessica M. Bonguyan", "Councilor Myrna G. L'Dalodo-Ortiz")
]

COUNCILORS_ABSENT = [
    ("Councilor Alberto T. Ungab", "- On Official Business"),
    ("Councilor Lorenzo Benjamin D. Villafuerte", "- On Leave")
]

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print total page count
    and authentic Sangguniang Panlungsod running headers.
    """
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
        # We only draw running headers on Page 2 and above
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Times-Roman", 9)
            
            # Top Running Header
            header_text = f"Page {self._pageNumber} of {total_pages}"
            doc_id_text = getattr(self, "doc_identifier", "Proposed Ordinance")
            self.drawString(MARGIN_LEFT, PAGE_HEIGHT - 0.65 * inch, header_text)
            self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, PAGE_HEIGHT - 0.65 * inch, doc_id_text)
            
            # Subtle ruling line under header
            self.setStrokeColor(colors.HexColor("#777777"))
            self.setLineWidth(0.5)
            self.line(MARGIN_LEFT, PAGE_HEIGHT - 0.72 * inch, PAGE_WIDTH - MARGIN_RIGHT, PAGE_HEIGHT - 0.72 * inch)
            
            # Bottom running folio rule
            self.line(MARGIN_LEFT, 0.75 * inch, PAGE_WIDTH - MARGIN_RIGHT, 0.75 * inch)
            self.setFont("Times-Italic", 8)
            self.drawString(MARGIN_LEFT, 0.60 * inch, "SP Davao Legislative Information Support System (LISSP) - Ex-Ante Review Copy")
            self.restoreState()


def build_ordinance_pdf(json_path: Path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    doc_id = data["doc_id"]
    pdf_filename = f"{doc_id}.pdf"
    pdf_path = OUTPUT_DIR / pdf_filename

    # Setup document
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles matching authentic Davao city ordinances
    style_header_republic = ParagraphStyle(
        "HeaderRepublic",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=10,
        leading=13,
        alignment=1 # Center
    )

    style_sp = ParagraphStyle(
        "HeaderSP",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=12,
        leading=15,
        alignment=1
    )

    style_council = ParagraphStyle(
        "HeaderCouncil",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=10,
        leading=13,
        alignment=1
    )

    style_ord_no = ParagraphStyle(
        "OrdNo",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=13,
        leading=16,
        alignment=1,
        spaceAfter=8
    )

    style_title = ParagraphStyle(
        "OrdTitle",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=10.5,
        leading=14.5,
        alignment=4, # Justify
        spaceAfter=14
    )

    style_enacting = ParagraphStyle(
        "EnactingClause",
        parent=styles["Normal"],
        fontName="Times-Italic",
        fontSize=10,
        leading=14,
        alignment=4,
        spaceAfter=12
    )

    style_section_title = ParagraphStyle(
        "SectionTitle",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=10,
        leading=14,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    style_section_body = ParagraphStyle(
        "SectionBody",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=10,
        leading=14.5,
        alignment=4,
        firstLineIndent=0.35 * inch,
        spaceAfter=6
    )

    style_roster_header = ParagraphStyle(
        "RosterHeader",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=9,
        leading=11
    )

    style_roster_item = ParagraphStyle(
        "RosterItem",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=8.5,
        leading=11
    )

    story = []

    # 1. Page 1 Official Government Header
    story.append(Paragraph("Republic of the Philippines", style_header_republic))
    story.append(Paragraph("City of Davao", style_header_republic))
    story.append(Paragraph("Office of the Sangguniang Panlungsod", style_sp))
    story.append(Paragraph("20th City Council", style_council))
    story.append(Paragraph("Committee Legislative Hearing Draft", style_council))
    story.append(Paragraph("Series of 2026", style_council))
    story.append(Spacer(1, 10))

    # 2. Council Attendance Roster (Two columns, matching raw scans)
    roster_data = [
        [Paragraph("<b>PRESENT:</b>", style_roster_header), Paragraph("", style_roster_header)]
    ]
    for left_mem, right_mem in COUNCILORS_PRESENT:
        roster_data.append([
            Paragraph(left_mem, style_roster_item),
            Paragraph(right_mem, style_roster_item)
        ])
    roster_data.append([Paragraph("<br/><b>ABSENT:</b>", style_roster_header), Paragraph("", style_roster_header)])
    for left_mem, right_mem in COUNCILORS_ABSENT:
        roster_data.append([
            Paragraph(left_mem, style_roster_item),
            Paragraph(right_mem, style_roster_item)
        ])

    roster_table = Table(roster_data, colWidths=[USABLE_WIDTH * 0.52, USABLE_WIDTH * 0.48])
    roster_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    story.append(roster_table)
    story.append(Spacer(1, 14))

    # 3. Proposed Ordinance Number & Title
    prop_no = data.get("proposed_ordinance_no", f"PROPOSED ORDINANCE NO. {doc_id}")
    story.append(Paragraph(prop_no.upper(), style_ord_no))
    story.append(Paragraph("Series of 2026", style_council))
    story.append(Spacer(1, 8))

    full_title = data.get("title", "ORDINANCE")
    story.append(Paragraph(full_title, style_title))
    story.append(Spacer(1, 6))

    # Page break to Page 2 for body sections (following exact Davao city convention)
    story.append(PageBreak())

    # 4. Enacting Clause on Page 2
    story.append(Paragraph("Be it ordained by the Sangguniang Panlungsod of Davao City, in session assembled, that:", style_enacting))

    # 5. Operative Sections
    sections = data.get("sections", [])
    for sec in sections:
        num = sec["sec_num"]
        title = sec.get("sec_title", "")
        text = sec.get("text", "")
        
        sec_header_str = f"SECTION {num}. {title.upper()} - "
        story.append(Paragraph(sec_header_str, style_section_title))
        story.append(Paragraph(text, style_section_body))

    # 6. Formal Closing & Legislative Certification Block
    story.append(Spacer(1, 16))
    story.append(Paragraph("ENACTED on Committee Review, by the Sangguniang Panlungsod of Davao City.", style_enacting))
    story.append(Spacer(1, 14))

    # Two column signature block
    sign_data = [
        [
            Paragraph("CERTIFIED CORRECT:", style_roster_header),
            Paragraph("ATTESTED:", style_roster_header)
        ],
        [
            Spacer(1, 24),
            Spacer(1, 24)
        ],
        [
            Paragraph("<b>CHARITO N. SANTOS</b><br/>Secretary to the Sangguniang Panlungsod<br/><i>(City Government Department Head II)</i>", style_roster_item),
            Paragraph("<b>J. MELCHOR B. QUITAIN JR.</b><br/>Vice Mayor<br/><i>Presiding Officer</i>", style_roster_item)
        ],
        [
            Spacer(1, 18),
            Spacer(1, 18)
        ],
        [
            Paragraph("APPROVED: ____________________, 2026", style_roster_header),
            Paragraph("ATTESTED:", style_roster_header)
        ],
        [
            Spacer(1, 24),
            Spacer(1, 24)
        ],
        [
            Paragraph("<b>SEBASTIAN Z. DUTERTE</b><br/>City Mayor", style_roster_item),
            Paragraph("<b>ATTY. FRANCIS MARK H. LAYOG</b><br/>Acting City Administrator", style_roster_item)
        ]
    ]

    sign_table = Table(sign_data, colWidths=[USABLE_WIDTH * 0.52, USABLE_WIDTH * 0.48])
    sign_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    story.append(KeepTogether([sign_table]))

    # Build the document using NumberedCanvas
    def on_page_setup(canvas_obj, document):
        canvas_obj.doc_identifier = f"Proposed Ord. No. {doc_id}"

    doc.build(story, canvasmaker=NumberedCanvas)
    return pdf_path


def main():
    print("=" * 80)
    print("GENERATING AUTHENTIC DAVAO CITY TIER 2 DRAFT ORDINANCE PDFS")
    print("=" * 80)

    json_files = sorted(list(INPUT_DIR.glob("*.json")))
    print(f"Found {len(json_files)} draft ordinance templates in {INPUT_DIR}")

    generated = []
    for jf in json_files:
        pdf_out = build_ordinance_pdf(jf)
        size_kb = pdf_out.stat().st_size / 1024
        print(f"[*] Generated: {pdf_out.name:<25} ({size_kb:>6.1f} KB)")
        generated.append(pdf_out)

    print(f"\n[OK] Successfully compiled {len(generated)} authentic ordinance PDFs to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
