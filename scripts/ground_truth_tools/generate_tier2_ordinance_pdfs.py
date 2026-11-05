"""
generate_tier2_ordinance_pdfs.py
================================
Generates authentic Philippine Legal/Folio (8.5 x 13 in) PDFs for the 6 stratified
Tier 2 full-document draft ordinances in `data/tier2_draft_ordinances/`, replicating
the exact visual layout, sans-serif typography, single-column councilor attendance list,
staggered signature blocks, embedded schedule tables, and attached legal instruments
(Memorandum of Agreement, Deed of Usufruct, Notary Acknowledgment, and Secretary's
Certificate) of the Sangguniang Panlungsod of Davao City.

Strict Authenticity Notes:
- NO running page headers or running footers (real Davao City ordinances have neither).
- Clean sans-serif typography (Helvetica / Helvetica-Bold / Helvetica-Oblique).
- Page 1: Republic of the Philippines / City of Davao / Office of the Sangguniang Panlungsod,
  left-aligned council session block, single-column PRESENT / ABSENT list, centered
  ORDINANCE NO. XXXX-26, and block-indented bold all-caps long title.
- Page 2+: Enacting clause, operative sections with bold underlined section titles,
  rendered schedule tables, staggered certification/approval sign-off, and attached
  MOA or Deed of Usufruct where applicable.
"""

import json
import xml.sax.saxutils as saxutils
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)

REPO_ROOT = next((p for p in Path(__file__).resolve().parents if (p / ".git").exists() or (p / "README.md").exists()), Path(__file__).resolve().parents[2])
INPUT_DIR = REPO_ROOT / "data" / "tier2_draft_ordinances"
OUTPUT_DIR = REPO_ROOT / "data" / "tier2_draft_ordinances_pdf"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Philippine Legal / Folio size: 8.5 x 13.0 inches
PAGE_WIDTH = 8.5 * inch
PAGE_HEIGHT = 13.0 * inch
MARGIN_LEFT = 1.15 * inch
MARGIN_RIGHT = 1.0 * inch
MARGIN_TOP = 0.95 * inch
MARGIN_BOTTOM = 0.95 * inch
USABLE_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

# Authentic single-column 20th City Council roster format
COUNCILORS_PRESENT = [
    ("Vice Mayor", "J. Melchor B. Quitain Jr.", "- Presiding Officer"),
    ("Councilor", "Marissa S. Abella", ""),
    ("Councilor", "Nilo M. Abellera Jr.", ""),
    ("Councilor", "Luna Maria Dominique S. Acosta", ""),
    ("Councilor", "Bai Hundra Cassandra Dominique N. Advincula", ""),
    ("Councilor", "Bernard E. Al-ag", ""),
    ("Councilor", "Wilberto E. Al-ag", ""),
    ("Councilor", "Al Ryan S. Alejandre", ""),
    ("Councilor", "Dante L. Apostol Sr.", ""),
    ("Councilor", "Conrado C. Baluran", ""),
    ("Councilor", "Jessica M. Bonguyan", ""),
    ("Councilor", "Louie John J. Bonguyan", ""),
    ("Councilor", "Pilar C. Braga", ""),
    ("Councilor", "Augusto Javier G. Campos III", ""),
    ("Councilor", "Jonard C. Dayap", ""),
    ("Councilor", "Edgar P. Ibuyan Jr.", ""),
    ("Councilor", " Edgar R. Ibuyan Sr.", ""),
    ("Councilor", "Richlyn N. Justol-Baguilod", ""),
    ("Councilor", "Diosdado Angelo Junior R. Mahipus", ""),
    ("Councilor", "Rodolfo M. Mande", ""),
    ("Councilor", "Jaffar U. Marohomsalic", ""),
    ("Councilor", "Bonz Andre A. Militar", ""),
    ("Councilor", "Myrna G. L'Dalodo-Ortiz", ""),
    ("Councilor", "Temujin B. Ocampo", ""),
    ("Councilor", "Jesus Joseph P. Zozobrado III", "")
]

COUNCILORS_ABSENT = [
    ("Councilor", "Alberto T. Ungab", "- On Official Business"),
    ("Councilor", "Lorenzo Benjamin D. Villafuerte", "- On Leave"),
    ("Councilor", "Trisha Ann J. Villafuerte", "- On Official Business")
]


def escape_xml(text: str) -> str:
    return saxutils.escape(text)


def build_markdown_table(table_lines, style_cell, style_header):
    """Converts markdown pipe table lines into a formatted ReportLab Table."""
    rows = []
    for line in table_lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        rows.append(cells)

    if not rows:
        return None

    num_cols = max(len(r) for r in rows)
    formatted_rows = []
    for r_idx, r in enumerate(rows):
        row_cells = []
        for c_idx in range(num_cols):
            val = r[c_idx] if c_idx < len(r) else ""
            val_esc = escape_xml(val)
            if r_idx == 0 or "TOTAL" in val.upper() or val.upper().startswith("FROM:") or val.upper().startswith("TO:"):
                p = Paragraph(f"<b>{val_esc}</b>", style_header if r_idx == 0 else style_cell)
            else:
                p = Paragraph(val_esc, style_cell)
            row_cells.append(p)
        formatted_rows.append(row_cells)

    if num_cols == 3:
        col_widths = [USABLE_WIDTH * 0.48, USABLE_WIDTH * 0.24, USABLE_WIDTH * 0.28]
    elif num_cols == 4:
        col_widths = [USABLE_WIDTH * 0.26, USABLE_WIDTH * 0.24, USABLE_WIDTH * 0.22, USABLE_WIDTH * 0.28]
    else:
        col_widths = [USABLE_WIDTH / num_cols] * num_cols

    tbl = Table(formatted_rows, colWidths=col_widths)
    tbl.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.6, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F2F2F2")),
    ]))
    return tbl


def append_ordinance_signoff(story, prop_no, full_title, styles_dict):
    """Appends the authentic staggered Davao City ordinance sign-off block and bottom title summary."""
    style_enacting = styles_dict["enacting"]
    style_sign_label = styles_dict["sign_label"]
    style_sign_person = styles_dict["sign_person"]
    style_footer_code = styles_dict["footer_code"]

    story.append(Spacer(1, 14))
    story.append(Paragraph(
        "ENACTED, _______________, 2026, by a majority vote of all the Members of the Sanggunian, there being a quorum.",
        style_enacting
    ))
    story.append(Spacer(1, 16))

    sign_data = [
        [
            Paragraph("", style_sign_label),
            Paragraph("CERTIFIED CORRECT:", style_sign_label)
        ],
        [Spacer(1, 22), Spacer(1, 22)],
        [
            Paragraph("", style_sign_person),
            Paragraph(
                "<b>CHARITO N. SANTOS</b><br/>Secretary to the Sangguniang Panlungsod<br/>(City Government Department Head II)",
                style_sign_person
            )
        ],
        [Spacer(1, 14), Spacer(1, 14)],
        [
            Paragraph("ATTESTED:", style_sign_label),
            Paragraph("", style_sign_label)
        ],
        [Spacer(1, 22), Spacer(1, 22)],
        [
            Paragraph(
                "<b>J. MELCHOR B. QUITAIN JR.</b><br/>Vice Mayor<br/>Presiding Officer",
                style_sign_person
            ),
            Paragraph("", style_sign_person)
        ],
        [Spacer(1, 16), Spacer(1, 16)],
        [
            Paragraph("", style_sign_label),
            Paragraph("APPROVED: _______________, 2026", style_sign_label)
        ],
        [Spacer(1, 22), Spacer(1, 22)],
        [
            Paragraph("", style_sign_person),
            Paragraph("<b>SEBASTIAN Z. DUTERTE</b><br/>City Mayor", style_sign_person)
        ],
        [Spacer(1, 14), Spacer(1, 14)],
        [
            Paragraph("ATTESTED:", style_sign_label),
            Paragraph("", style_sign_label)
        ],
        [Spacer(1, 22), Spacer(1, 22)],
        [
            Paragraph(
                "<b>ATTY. FRANCIS MARK H. LAYOG</b><br/>Acting City Administrator",
                style_sign_person
            ),
            Paragraph("", style_sign_person)
        ]
    ]

    sign_table = Table(sign_data, colWidths=[USABLE_WIDTH * 0.50, USABLE_WIDTH * 0.50])
    sign_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    story.append(KeepTogether([
        sign_table,
        Spacer(1, 18),
        Paragraph("cns/jav", style_footer_code),
        Paragraph(f"<b>{escape_xml(prop_no.upper())}</b>", style_footer_code),
        Paragraph(escape_xml(full_title), style_footer_code)
    ]))


def append_section_flowables(story, sec, styles_dict):
    """Renders a section with bold underlined title, paragraphs, and any embedded schedule tables."""
    style_section_body = styles_dict["section_body"]
    style_table_cell = styles_dict["table_cell"]
    style_table_header = styles_dict["table_header"]

    num = sec["sec_num"]
    title = sec.get("sec_title", "").strip()
    text = sec.get("text", "").strip()

    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    if not blocks:
        blocks = [text]

    first_rendered = False
    for b in blocks:
        lines = [ln.strip() for ln in b.split("\n") if ln.strip()]
        if lines and lines[0].startswith("|"):
            tbl = build_markdown_table(lines, style_table_cell, style_table_header)
            if tbl:
                story.append(Spacer(1, 4))
                story.append(tbl)
                story.append(Spacer(1, 6))
        else:
            b_escaped = escape_xml(b).replace("\n", "<br/>")
            if not first_rendered:
                title_esc = escape_xml(title.upper())
                first_p = f"<b>SECTION {num}. <u>{title_esc}</u></b> - {b_escaped}"
                story.append(Paragraph(first_p, style_section_body))
                first_rendered = True
            else:
                story.append(Paragraph(b_escaped, style_section_body))


def append_attachment_pages(story, attachment, attach_sections, styles_dict):
    """Appends the attached MOA or Deed of Usufruct, Party Signatures, Notary Acknowledgment, and Annex A."""
    style_ord_no = styles_dict["ord_no"]
    style_section_body = styles_dict["section_body"]
    style_sign_person = styles_dict["sign_person"]
    style_sign_label = styles_dict["sign_label"]
    style_table_cell = styles_dict["table_cell"]
    style_table_header = styles_dict["table_header"]

    story.append(PageBreak())
    att_type = attachment.get("type", "MEMORANDUM OF AGREEMENT")
    story.append(Paragraph(f"<b>{escape_xml(att_type)}</b>", style_ord_no))
    story.append(Spacer(1, 8))

    for sec in attach_sections:
        append_section_flowables(story, sec, styles_dict)

    story.append(Spacer(1, 10))
    story.append(Paragraph("APPROVED AND EXECUTED by the authorized representatives of the Parties:", style_section_body))
    story.append(Spacer(1, 14))

    party_a_lines = escape_xml(attachment.get("party_a", "")).replace("\n", "<br/>")
    party_b_lines = escape_xml(attachment.get("party_b", "")).replace("\n", "<br/>")
    witnesses = attachment.get("witnesses", ["Witness 1", "Witness 2"])
    w1_lines = escape_xml(witnesses[0]).replace("\n", "<br/>") if len(witnesses) > 0 else ""
    w2_lines = escape_xml(witnesses[1]).replace("\n", "<br/>") if len(witnesses) > 1 else ""

    party_table_data = [
        [Spacer(1, 20), Spacer(1, 20)],
        [Paragraph(f"<b>{party_a_lines}</b>", style_sign_person), Paragraph(f"<b>{party_b_lines}</b>", style_sign_person)],
        [Spacer(1, 16), Spacer(1, 16)],
        [Paragraph("SIGNED IN THE PRESENCE OF:", style_sign_label), Paragraph("", style_sign_label)],
        [Spacer(1, 20), Spacer(1, 20)],
        [Paragraph(w1_lines, style_sign_person), Paragraph(w2_lines, style_sign_person)]
    ]
    party_table = Table(party_table_data, colWidths=[USABLE_WIDTH * 0.50, USABLE_WIDTH * 0.50])
    party_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(KeepTogether([party_table]))

    # Notary Public Acknowledgment
    story.append(Spacer(1, 18))
    notary_header = (
        "<b>ACKNOWLEDGMENT</b><br/><br/>"
        "REPUBLIC OF THE PHILIPPINES)<br/>"
        "CITY OF DAVAO ....................) S.S.<br/><br/>"
        "BEFORE ME, a Notary Public for and in the City of Davao, this ___ day of __________, 2026, "
        "personally appeared the following persons with their respective competent evidence of identity:"
    )
    story.append(Paragraph(notary_header, style_sign_person))
    story.append(Spacer(1, 6))

    appearances = attachment.get("notary_appearances", ["SEBASTIAN Z. DUTERTE", "AUTHORIZED REPRESENTATIVE"])
    id_rows = [
        [Paragraph("<b>Name</b>", style_table_header), Paragraph("<b>Competent Evidence of Identity</b>", style_table_header), Paragraph("<b>Date / Place Issued</b>", style_table_header)]
    ]
    for name in appearances:
        id_rows.append([
            Paragraph(escape_xml(name), style_table_cell),
            Paragraph("Government Official ID /TIN", style_table_cell),
            Paragraph("Davao City, Philippines", style_table_cell)
        ])
    id_tbl = Table(id_rows, colWidths=[USABLE_WIDTH * 0.38, USABLE_WIDTH * 0.34, USABLE_WIDTH * 0.28])
    id_tbl.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(id_tbl)
    story.append(Spacer(1, 6))

    notary_footer = (
        "known to me and to me known to be the same persons who executed the foregoing instrument, "
        "and they acknowledged to me that the same is their free and voluntary act and deed and the "
        "free and voluntary act and deed of the entities they respectively represent.<br/><br/>"
        "WITNESS MY HAND AND NOTARIAL SEAL on the date and at the place first above written.<br/><br/>"
        "Doc. No. _____;<br/>"
        "Page No. _____;<br/>"
        "Book No. _____;<br/>"
        "Series of 2026."
    )
    story.append(Paragraph(notary_footer, style_sign_person))

    # Optional Annex A Corporate Secretary's Certificate (e.g., for Typology 04 Deed of Usufruct)
    sec_cert = attachment.get("secretary_certificate")
    if sec_cert:
        story.append(PageBreak())
        story.append(Paragraph("<b>ANNEX \"A\"</b>", style_ord_no))
        story.append(Paragraph("<b>SECRETARY'S CERTIFICATE</b>", style_ord_no))
        story.append(Spacer(1, 8))
        cert_body = (
            f"REPUBLIC OF THE PHILIPPINES)<br/>"
            f"CITY OF DAVAO ....................) S.S.<br/><br/>"
            f"I, <b>{escape_xml(sec_cert['secretary_name'])}</b>, of legal age, Filipino, and with office address at "
            f"J.P. Laurel Avenue, Davao City, after having been duly sworn in accordance with law, hereby depose and state that:<br/><br/>"
            f"1. I am the duly elected and qualified Corporate Secretary of <b>{escape_xml(sec_cert['corp_name'])}</b>, "
            f"a corporation duly organized and existing under the laws of the Republic of the Philippines.<br/><br/>"
            f"2. At the Regular Meeting of the Board of Directors of the Corporation held on {escape_xml(sec_cert['board_date'])}, "
            f"at which meeting a quorum was present and acting throughout, the following {escape_xml(sec_cert['resolution_no'])} "
            f"was unanimously approved and adopted:<br/><br/>"
            f"<i>\"RESOLVED, AS IT IS HEREBY RESOLVED, that the Corporation be authorized to grant unto the City Government of Davao "
            f"a ten (10) year rent-free Usufruct over a 1,500-square-meter portion of the Ground Floor of Southgate Town Center in "
            f"Barangay Catalunan Grande, Talomo District, Davao City, for the establishment of the Talomo North District Satellite "
            f"Public Library and Civil Registry Desk, and to designate Corporate President {escape_xml(sec_cert['authorized_signatory'])} "
            f"to sign, execute, and deliver the corresponding Deed of Usufruct.\"</i><br/><br/>"
            f"3. The foregoing resolution has not been revoked, amended, or modified and remains in full force and effect.<br/><br/>"
            f"IN WITNESS WHEREOF, I have hereunto affixed my signature this ___ day of __________, 2026 in Davao City, Philippines.<br/><br/><br/>"
            f"<b>{escape_xml(sec_cert['secretary_name'])}</b><br/>Corporate Secretary<br/><br/>"
            f"SUBSCRIBED AND SWORN to before me this ___ day of __________, 2026 in Davao City, affiant exhibiting her Integrated Bar "
            f"of the Philippines (IBP) Roll ID.<br/><br/>"
            f"Doc. No. _____;<br/>Page No. _____;<br/>Book No. _____;<br/>Series of 2026."
        )
        story.append(Paragraph(cert_body, style_sign_person))


def build_ordinance_pdf(json_path: Path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    doc_id = data["doc_id"]
    pdf_path = OUTPUT_DIR / f"{doc_id}.pdf"

    # Setup document without any header or footer callbacks
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM
    )

    styles = getSampleStyleSheet()

    # Authentic Davao City Sans-Serif Typography (Helvetica)
    style_header_top = ParagraphStyle(
        "HeaderTop",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        alignment=1
    )
    style_session_left = ParagraphStyle(
        "SessionLeft",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=12.5,
        alignment=0
    )
    style_roster_header = ParagraphStyle(
        "RosterHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12
    )
    style_roster_item = ParagraphStyle(
        "RosterItem",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=11.5
    )
    style_ord_no = ParagraphStyle(
        "OrdNo",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        alignment=1,
        spaceAfter=2
    )
    style_series = ParagraphStyle(
        "SeriesYear",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        alignment=1,
        spaceAfter=10
    )
    style_title = ParagraphStyle(
        "OrdTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13.5,
        alignment=4,
        leftIndent=0.55 * inch,
        rightIndent=0.55 * inch,
        spaceAfter=14
    )
    style_enacting = ParagraphStyle(
        "EnactingClause",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=0,
        firstLineIndent=0.40 * inch,
        spaceAfter=12
    )
    style_section_body = ParagraphStyle(
        "SectionBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=4,
        firstLineIndent=0.40 * inch,
        spaceAfter=8
    )
    style_sign_label = ParagraphStyle(
        "SignLabel",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=12
    )
    style_sign_person = ParagraphStyle(
        "SignPerson",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=12.5
    )
    style_footer_code = ParagraphStyle(
        "FooterCode",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.5,
        leftIndent=0.35 * inch,
        rightIndent=1.2 * inch
    )
    style_table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11
    )
    style_table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11
    )

    styles_dict = {
        "enacting": style_enacting,
        "section_body": style_section_body,
        "sign_label": style_sign_label,
        "sign_person": style_sign_person,
        "footer_code": style_footer_code,
        "table_header": style_table_header,
        "table_cell": style_table_cell,
        "ord_no": style_ord_no
    }

    story = []

    # 1. Centered Republic / City / Office Header
    story.append(Paragraph("Republic of the Philippines", style_header_top))
    story.append(Paragraph("City of Davao", style_header_top))
    story.append(Paragraph("Office of the Sangguniang Panlungsod", style_header_top))
    story.append(Spacer(1, 12))

    # 2. Left-aligned Council Session Info
    session_lines = data.get("session_info", "20th City Council\n18th Regular Session\nSeries of 2026").split("\n")
    for s_line in session_lines:
        story.append(Paragraph(escape_xml(s_line.strip()), style_session_left))
    story.append(Spacer(1, 10))

    # 3. Single-column Councilor Attendance List (matching authentic Davao City scans)
    story.append(Paragraph("PRESENT:", style_roster_header))
    story.append(Spacer(1, 3))

    present_rows = []
    for title_role, member_name, note in COUNCILORS_PRESENT:
        present_rows.append([
            Paragraph(escape_xml(title_role), style_roster_item),
            Paragraph(escape_xml(member_name.strip()), style_roster_item),
            Paragraph(escape_xml(note), style_roster_item)
        ])
    present_tbl = Table(present_rows, colWidths=[1.15 * inch, 2.75 * inch, USABLE_WIDTH - 3.90 * inch])
    present_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.5),
    ]))
    story.append(present_tbl)
    story.append(Spacer(1, 8))

    story.append(Paragraph("ABSENT:", style_roster_header))
    story.append(Spacer(1, 3))
    absent_rows = []
    for title_role, member_name, note in COUNCILORS_ABSENT:
        absent_rows.append([
            Paragraph(escape_xml(title_role), style_roster_item),
            Paragraph(escape_xml(member_name.strip()), style_roster_item),
            Paragraph(escape_xml(note), style_roster_item)
        ])
    absent_tbl = Table(absent_rows, colWidths=[1.15 * inch, 2.75 * inch, USABLE_WIDTH - 3.90 * inch])
    absent_tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.5),
    ]))
    story.append(absent_tbl)
    story.append(Spacer(1, 18))

    # 4. Centered Bold Ordinance Number & Block-Indented All-Caps Long Title
    prop_no = data.get("proposed_ordinance_no", f"ORDINANCE NO. {doc_id}")
    series_yr = data.get("series_year", "Series of 2026")
    story.append(Paragraph(f"<u>{escape_xml(prop_no.upper())}</u>", style_ord_no))
    story.append(Paragraph(escape_xml(series_yr), style_series))

    full_title = data.get("title", "AN ORDINANCE")
    story.append(Paragraph(escape_xml(full_title), style_title))

    # Page 1 ends after the long title, matching authentic Davao City ordinances
    story.append(PageBreak())

    # 5. Page 2+: Enacting Clause & Operative Sections
    enacting_clause = data.get(
        "enacting_clause",
        "Be it ordained by the Sangguniang Panlungsod of Davao City in session assembled, that:"
    )
    story.append(Paragraph(escape_xml(enacting_clause), style_enacting))

    sections = data.get("sections", [])
    attachment = data.get("attachment")

    if attachment:
        ord_sections = [s for s in sections if s["sec_num"] <= 5]
        attach_sections = [s for s in sections if s["sec_num"] > 5]
    else:
        ord_sections = sections
        attach_sections = []

    for sec in ord_sections:
        append_section_flowables(story, sec, styles_dict)

    # 6. Ordinance Enactment & Sign-Off Block
    append_ordinance_signoff(story, prop_no, full_title, styles_dict)

    # 7. Attached Legal Instrument (MOA / Deed of Usufruct + Secretary's Certificate) if present
    if attachment and attach_sections:
        append_attachment_pages(story, attachment, attach_sections, styles_dict)

    doc.build(story)
    return pdf_path


def main():
    print("=" * 80)
    print("GENERATING 6 AUTHENTIC DAVAO CITY TIER 2 DRAFT ORDINANCE PDFS (NO HEADER/FOOTER)")
    print("=" * 80)

    # Remove old PDFs (e.g., 07-10) so only the 6 stratified ordinances exist
    for old_pdf in OUTPUT_DIR.glob("*.pdf"):
        old_pdf.unlink()

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
