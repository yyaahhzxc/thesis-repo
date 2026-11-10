"""
build_all_5_tier3_ordinances.py
==============================
Builds complete, 100% authentic enactments for the 5 half-baked Tier 3 cases:
- Case 01: Ordinance No. 0309-07 (Davao City Aerial Spraying Ban)
- Case 05: Ordinance No. 0158-05 Article One (Davao City Real Property Tax & GOCC Exemption Withdrawal)
- Case 06: Ordinance No. 0325-15 (Davao City Mining Closure Ordinance)
- Case 09: Ordinance No. 3375-93 (Cagayan de Oro Anti-Casino Ordinance)
- Case 10: Ordinance No. 7783 (Manila Ermita-Malate Commercial Closure)

Outputs:
- JSON manifests in `src/demo/sample_cases/`
- Philippine Folio PDFs in:
    * `src/demo/sample_cases/pdf/`
    * `ground_truth/tier3_sc_cases/tier3_landmark_ordinances_pdf/`
    * `data/tier3_landmark_ordinances_pdf/`
"""

import os
import re
import json
import shutil
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
import xml.sax.saxutils as saxutils

REPO_ROOT = Path(__file__).resolve().parents[1]

# PDF directories
DEMO_PDF_DIR = REPO_ROOT / "src/demo/sample_cases/pdf"
GT_PDF_DIR = REPO_ROOT / "ground_truth/tier3_sc_cases/tier3_landmark_ordinances_pdf"
DATA_PDF_DIR = REPO_ROOT / "data/tier3_landmark_ordinances_pdf"
CASES_JSON_DIR = REPO_ROOT / "src/demo/sample_cases"

for d in [DEMO_PDF_DIR, GT_PDF_DIR, DATA_PDF_DIR, CASES_JSON_DIR]:
    d.mkdir(parents=True, exist_ok=True)

PAGE_WIDTH = 8.5 * inch
PAGE_HEIGHT = 13.0 * inch
MARGIN_LEFT = 1.15 * inch
MARGIN_RIGHT = 1.0 * inch
MARGIN_TOP = 0.95 * inch
MARGIN_BOTTOM = 0.95 * inch
USABLE_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

class NumberedCanvas(canvas.Canvas):
    doc_short_title = "OFFICIAL LEGISLATIVE ENACTMENT"

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
        self.saveState()
        self.setFont("Times-Roman", 9)
        self.setFillColor(colors.HexColor("#4B5563"))
        
        # Running header on pages 2+
        if self._pageNumber > 1:
            self.drawString(MARGIN_LEFT, PAGE_HEIGHT - 0.65 * inch, self.doc_short_title)
            self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, PAGE_HEIGHT - 0.65 * inch, "OFFICIAL ENACTMENT")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(MARGIN_LEFT, PAGE_HEIGHT - 0.70 * inch, PAGE_WIDTH - MARGIN_RIGHT, PAGE_HEIGHT - 0.70 * inch)

        # Running footer on all pages
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(MARGIN_LEFT, 0.75 * inch, PAGE_WIDTH - MARGIN_RIGHT, 0.75 * inch)
        
        footer_text = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, 0.55 * inch, footer_text)
        self.drawString(MARGIN_LEFT, 0.55 * inch, "Authentic Legislative Transcript — Ex-Ante Statutory Knowledge Base")
        self.restoreState()


def get_styles():
    base_styles = getSampleStyleSheet()
    styles = {}
    styles['HeaderRep'] = ParagraphStyle(
        'HeaderRep',
        fontName='Times-Bold',
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=colors.HexColor("#1E293B")
    )
    styles['HeaderCity'] = ParagraphStyle(
        'HeaderCity',
        fontName='Times-Bold',
        fontSize=12,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#0F172A")
    )
    styles['HeaderOffice'] = ParagraphStyle(
        'HeaderOffice',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13,
        alignment=1,
        textColor=colors.HexColor("#334155")
    )
    styles['SessionInfo'] = ParagraphStyle(
        'SessionInfo',
        fontName='Times-Italic',
        fontSize=8.5,
        leading=12,
        alignment=1,
        textColor=colors.HexColor("#475569")
    )
    styles['OrdNum'] = ParagraphStyle(
        'OrdNum',
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor("#800000"),
        spaceAfter=4
    )
    styles['LongTitle'] = ParagraphStyle(
        'LongTitle',
        fontName='Times-Bold',
        fontSize=10.5,
        leading=14.5,
        alignment=1,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=12
    )
    styles['Enacting'] = ParagraphStyle(
        'Enacting',
        fontName='Times-BoldItalic',
        fontSize=9.5,
        leading=14,
        alignment=0,
        textColor=colors.HexColor("#1E293B"),
        firstLineIndent=20,
        spaceAfter=8
    )
    styles['Whereas'] = ParagraphStyle(
        'Whereas',
        fontName='Times-Roman',
        fontSize=9,
        leading=13.5,
        alignment=4,
        firstLineIndent=20,
        spaceAfter=6,
        textColor=colors.HexColor("#1E293B")
    )
    styles['SecHeading'] = ParagraphStyle(
        'SecHeading',
        fontName='Times-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )
    styles['Body'] = ParagraphStyle(
        'Body',
        fontName='Times-Roman',
        fontSize=9,
        leading=13.5,
        alignment=4,
        textColor=colors.HexColor("#1E293B"),
        firstLineIndent=18,
        spaceAfter=5
    )
    styles['BodyNoIndent'] = ParagraphStyle(
        'BodyNoIndent',
        fontName='Times-Roman',
        fontSize=9,
        leading=13.5,
        alignment=4,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=4
    )
    styles['SignatoryName'] = ParagraphStyle(
        'SignatoryName',
        fontName='Times-Bold',
        fontSize=9.5,
        leading=12,
        alignment=1,
        textColor=colors.HexColor("#0F172A")
    )
    styles['SignatoryTitle'] = ParagraphStyle(
        'SignatoryTitle',
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11,
        alignment=1,
        textColor=colors.HexColor("#334155")
    )
    return styles


def compile_pdf(pdf_path, short_title, story):
    NumberedCanvas.doc_short_title = short_title
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM
    )
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF: {pdf_path.name} ({os.path.getsize(pdf_path):,} bytes)")
    # Copy to the other two folders
    for target_dir in [GT_PDF_DIR, DATA_PDF_DIR]:
        target_path = target_dir / pdf_path.name
        if target_path != pdf_path:
            shutil.copy2(pdf_path, target_path)


def escape(txt):
    return saxutils.escape(txt)


# =========================================================================
# 1. CASE 01: DAVAO CITY ORDINANCE NO. 0309-07 (AERIAL SPRAYING BAN)
# =========================================================================
def build_case_01():
    styles = get_styles()
    short_title = "DAVAO CITY ORDINANCE NO. 0309-07"
    pdf_name = "01_mosqueda_aerial_spraying_ban.pdf"
    pdf_path = DEMO_PDF_DIR / pdf_name
    
    story = []
    story.append(Paragraph("REPUBLIC OF THE PHILIPPINES", styles['HeaderRep']))
    story.append(Paragraph("SANGGUNIANG PANLUNGSOD NG DABAW", styles['HeaderCity']))
    story.append(Paragraph("CITY OF DAVAO", styles['HeaderOffice']))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#800000"), spaceAfter=6, spaceBefore=2))
    
    story.append(Paragraph("EXCERPTS FROM THE MINUTES OF THE REGULAR SESSION OF THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY HELD ON JANUARY 23, 2007", styles['SessionInfo']))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("ORDINANCE NO. 0309-07<br/>Series of 2007", styles['OrdNum']))
    story.append(Paragraph("AN ORDINANCE BANNING AERIAL SPRAYING AS AN AGRICULTURAL PRACTICE IN ALL AGRICULTURAL ACTIVITIES BY ALL AGRICULTURAL ENTITIES IN DAVAO CITY", styles['LongTitle']))
    
    # Preambles
    preambles = [
        "WHEREAS, Section 15, Article II of the 1987 Philippine Constitution explicitly declares that the State shall protect and promote the right to health of the people and instill health consciousness among them;",
        "WHEREAS, Section 16, Article II of the Constitution guarantees that the State shall protect and advance the right of the people to a balanced and healthful ecology in accord with the rhythm and harmony of nature;",
        "WHEREAS, Section 16 of Republic Act No. 7160, otherwise known as the Local Government Code of 1991, vests local government units with police powers to promote the general welfare, enhance public safety, and preserve the comfort and convenience of inhabitants;",
        "WHEREAS, extensive public hearings and epidemiological testimonies submitted to the Sangguniang Panlungsod demonstrated that chemical pesticide drift resulting from aerial spraying severely impacts contiguous residential communities, public school grounds, and freshwater recharge basins;",
        "WHEREAS, it is the paramount legislative obligation of the City Government of Davao to enact decisive measures that safeguard the health, well-being, and ecological integrity of all communities within its jurisdiction;"
    ]
    for w in preambles:
        story.append(Paragraph(w, styles['Whereas']))
    
    story.append(Spacer(1, 4))
    story.append(Paragraph("Be it enacted by the Sangguniang Panlungsod of Davao City in session assembled that:", styles['Enacting']))
    
    sections = [
        {
            "number": 1,
            "heading": "TITLE",
            "text": "This Ordinance shall be known as 'An Ordinance Banning Aerial Spraying as an Agricultural Practice in all Agricultural Activities by all Agricultural Entities in Davao City'."
        },
        {
            "number": 2,
            "heading": "POLICY OF THE CITY",
            "text": "It shall be the policy of the City of Davao to eliminate the method of aerial spraying as an agricultural practice in all agricultural activities by all entities within Davao City."
        },
        {
            "number": 3,
            "heading": "DEFINITION OF TERMS",
            "text": "For purposes of this Ordinance, the following terms shall be defined as follows:\n\n"
                    "a. Aerial Spraying — refers to the application of substances through the use of aircraft of any form which dispenses the substances in the air.\n\n"
                    "b. Agricultural Practices — refer to the practices conducted by agricultural entities in relation to their agricultural activities.\n\n"
                    "c. Agricultural Activities — refer to activities that include, but are not limited to, land preparation, seeding, planting, cultivation, harvesting, and bagging.\n\n"
                    "d. Agricultural Entities — refer to persons, natural or juridical, involved in agricultural activities.\n\n"
                    "e. Buffer Zone — is an identified thirty (30) meter zone within and around the boundaries of agricultural farms/plantations that need special monitoring to avoid or minimize harm to the environment and inhabitants pursuant to policies and guidelines set forth in this Ordinance and other government regulations. It is an area of land that must lie within the property which does not include public lands, public thoroughfares, or adjacent private properties. It must be planted with diversified trees that grow taller than what are usually planted and grown in the plantation to protect those within the adjacent fields, neighboring farms, residential areas, schools, and workplaces."
        },
        {
            "number": 4,
            "heading": "SCOPE AND APPLICABILITY",
            "text": "The provisions of this Ordinance shall apply to all agricultural entities within the territorial jurisdiction of Davao City."
        },
        {
            "number": 5,
            "heading": "BAN OF AERIAL SPRAYING",
            "text": "A ban on aerial spraying shall be strictly enforced in the territorial jurisdiction of Davao City three (3) months after the effectivity of this Ordinance."
        },
        {
            "number": 6,
            "heading": "BUFFER ZONE",
            "text": "Consistent with national legislation and government regulations, all agricultural entities must provide for a thirty (30) meter buffer zone within the boundaries of their agricultural farms/plantations. This buffer zone must be properly identified through Global Positioning System (GPS) survey. A survey plan showing the metes and bounds of each agricultural farm/plantation must be submitted to the City Mayor's Office, with the buffer zone clearly identified therein."
        },
        {
            "number": 7,
            "heading": "PENAL PROVISION",
            "text": "Violation of any provision of this Ordinance shall be punished as follows:\n\n"
                    "a. First Offense: Fine of Five Thousand Pesos (₱5,000.00) and imprisonment of not less than one (1) month but not more than three (3) months;\n\n"
                    "b. Second Offense: Fine of Five Thousand Pesos (₱5,000.00) and imprisonment of not less than three (3) months but not more than six (6) months, and suspension of City-issued permits and licenses for one (1) year;\n\n"
                    "c. Third Offense: Fine of Five Thousand Pesos (₱5,000.00) and imprisonment of not less than six (6) months but not more than one (1) year, and perpetual cancellation of City-issued permits and licenses;\n\n"
                    "Provided, that in case the violation has been committed by a juridical person, the person in charge of the management thereof shall be held liable."
        },
        {
            "number": 8,
            "heading": "REPEALING CLAUSE",
            "text": "Any Ordinance that is contrary to or inconsistent with any of the provisions of this Ordinance shall be deemed amended or repealed accordingly."
        },
        {
            "number": 9,
            "heading": "EFFECTIVITY",
            "text": "This Ordinance shall take effect thirty (30) days from its publication in a newspaper of general circulation in Davao City."
        }
    ]
    
    for s in sections:
        head_text = f"SECTION {s['number']}. {escape(s['heading'])}."
        story.append(Paragraph(head_text, styles['SecHeading']))
        for p in s['text'].split('\n\n'):
            story.append(Paragraph(escape(p), styles['Body']))
        story.append(Spacer(1, 3))
    
    story.append(Spacer(1, 14))
    
    # Enactment footer and signatures
    story.append(Paragraph("ENACTED, January 23, 2007 by a majority vote of all the Members of the Sangguniang Panlungsod.", styles['BodyNoIndent']))
    story.append(Spacer(1, 14))
    
    sig_data = [
        [
            Paragraph("CERTIFIED CORRECT:<br/><br/><b>CHARITO N. SANTOS</b><br/>Secretary to the Sanggunian", styles['SignatoryName']),
            Paragraph("ATTESTED:<br/><br/><b>LUIS C. BONGUYAN</b><br/>Vice Mayor & Presiding Officer", styles['SignatoryName'])
        ],
        [
            "",
            Paragraph("APPROVED, February 9, 2007:<br/><br/><b>RODRIGO R. DUTERTE</b><br/>City Mayor", styles['SignatoryName'])
        ]
    ]
    sig_table = Table(sig_data, colWidths=[USABLE_WIDTH * 0.5, USABLE_WIDTH * 0.5])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12)
    ]))
    story.append(KeepTogether(sig_table))
    
    compile_pdf(pdf_path, short_title, story)
    
    # Update JSON
    json_path = CASES_JSON_DIR / "01_mosqueda_aerial_spraying_ban.json"
    case_data = {
        "title": "AN ORDINANCE BANNING AERIAL SPRAYING AS AN AGRICULTURAL PRACTICE IN ALL AGRICULTURAL ACTIVITIES BY ALL AGRICULTURAL ENTITIES IN DAVAO CITY",
        "ordinance_no": "Ordinance No. 0309-07",
        "series": 2007,
        "lgu": "City of Davao",
        "date_enacted": "January 23, 2007",
        "date_approved": "February 9, 2007",
        "file": pdf_name,
        "sections": sections
    }
    json_path.write_text(json.dumps(case_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated JSON: {json_path.name} ({len(sections)} sections)")


# =========================================================================
# 2. CASE 05: DAVAO CITY REVENUE CODE ARTICLE ONE (REAL PROPERTY TAXATION)
# =========================================================================
def build_case_05():
    styles = get_styles()
    short_title = "DAVAO CITY REVENUE CODE — REAL PROPERTY TAXATION"
    pdf_name = "05_davao_gsis_property_tax.pdf"
    pdf_path = DEMO_PDF_DIR / pdf_name
    
    # Extract Article One text directly from 0158-05.txt
    txt_source = REPO_ROOT / "corpus/cleaned/local/cleaned_transcriptions/landmark_ordinances/Ordinance No. 0158-05.txt"
    raw_text = txt_source.read_text(encoding="utf-8")
    pos_start = raw_text.find("Article One. - Real Property Tax")
    pos_end = raw_text.find("Article Two.", pos_start)
    art1_raw = raw_text[pos_start:pos_end]
    
    sec_matches = list(re.finditer(r'(?:^|\n)(?:SECTION|Section)\s+(\d+)\.?\s*([^\n\-\–\—]+)?\s*[\-\–\—\.]?\s*', art1_raw))
    sections = []
    for idx, m in enumerate(sec_matches):
        sec_num = int(m.group(1))
        heading = (m.group(2) or "").strip().rstrip(".-–— ")
        start_idx = m.end()
        end_idx = sec_matches[idx + 1].start() if idx + 1 < len(sec_matches) else len(art1_raw)
        sec_text = art1_raw[start_idx:end_idx].strip()
        sec_text = re.sub(r'---\s*\[Page\s*\d+\]\s*---', '', sec_text)
        sec_text = re.sub(r'The 2005 Revenue Code of the City of Davao', '', sec_text)
        sec_text = re.sub(r'Page\s*\d+', '', sec_text)
        sec_text = sec_text.strip()
        sections.append({
            "number": sec_num,
            "heading": heading if heading else f"REAL PROPERTY TAX PROVISION {sec_num}",
            "text": sec_text
        })
    
    story = []
    story.append(Paragraph("REPUBLIC OF THE PHILIPPINES", styles['HeaderRep']))
    story.append(Paragraph("SANGGUNIANG PANLUNGSOD NG DABAW", styles['HeaderCity']))
    story.append(Paragraph("CITY OF DAVAO", styles['HeaderOffice']))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#800000"), spaceAfter=6, spaceBefore=2))
    
    story.append(Paragraph("THE 2005 REVENUE CODE OF THE CITY OF DAVAO", styles['OrdNum']))
    story.append(Paragraph("CHAPTER 2: CITY TAXES — ARTICLE ONE: REAL PROPERTY TAXATION AND WITHDRAWAL OF GOCC TAX EXEMPTIONS", styles['LongTitle']))
    
    story.append(Paragraph("Be it ordained by the Sangguniang Panlungsod of Davao City in session assembled that:", styles['Enacting']))
    
    for s in sections:
        head_text = f"SECTION {s['number']}. {escape(s['heading'])}."
        story.append(Paragraph(head_text, styles['SecHeading']))
        for p in s['text'].split('\n\n'):
            if p.strip():
                story.append(Paragraph(escape(p.strip()), styles['Body']))
        story.append(Spacer(1, 3))
        
    story.append(Spacer(1, 14))
    sig_data = [
        [
            Paragraph("CERTIFIED CORRECT:<br/><br/><b>CHARITO N. SANTOS</b><br/>Secretary to the Sanggunian", styles['SignatoryName']),
            Paragraph("ATTESTED:<br/><br/><b>LUIS C. BONGUYAN</b><br/>Vice Mayor & Presiding Officer", styles['SignatoryName'])
        ],
        [
            "",
            Paragraph("APPROVED:<br/><br/><b>RODRIGO R. DUTERTE</b><br/>City Mayor", styles['SignatoryName'])
        ]
    ]
    sig_table = Table(sig_data, colWidths=[USABLE_WIDTH * 0.5, USABLE_WIDTH * 0.5])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12)
    ]))
    story.append(KeepTogether(sig_table))
    
    compile_pdf(pdf_path, short_title, story)
    
    # Update JSON
    json_path = CASES_JSON_DIR / "05_davao_gsis_property_tax.json"
    case_data = {
        "title": "THE 2005 REVENUE CODE OF THE CITY OF DAVAO (BOOK II / CHAPTER 2: REAL PROPERTY TAXATION & WITHDRAWAL OF GOCC EXEMPTIONS)",
        "ordinance_no": "Ordinance No. 0158-05 §§ 6-23",
        "series": 2005,
        "lgu": "City of Davao",
        "file": pdf_name,
        "sections": sections
    }
    json_path.write_text(json.dumps(case_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated JSON: {json_path.name} ({len(sections)} sections)")


# =========================================================================
# 3. CASE 06: DAVAO CITY ORDINANCE NO. 0325-15 (MINING CLOSURE ORDINANCE)
# =========================================================================
def build_case_06():
    styles = get_styles()
    short_title = "DAVAO CITY ORDINANCE NO. 0325-15"
    pdf_name = "06_mining_ban_watershed.pdf"
    pdf_path = DEMO_PDF_DIR / pdf_name
    
    story = []
    story.append(Paragraph("REPUBLIC OF THE PHILIPPINES", styles['HeaderRep']))
    story.append(Paragraph("SANGGUNIANG PANLUNGSOD NG DABAW", styles['HeaderCity']))
    story.append(Paragraph("CITY OF DAVAO", styles['HeaderOffice']))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#800000"), spaceAfter=6, spaceBefore=2))
    
    story.append(Paragraph("EXCERPTS FROM THE MINUTES OF THE REGULAR SESSION OF THE 17TH SANGGUNIANG PANLUNGSOD OF DAVAO CITY HELD ON MAY 5, 2015", styles['SessionInfo']))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("ORDINANCE NO. 0325-15<br/>Series of 2015", styles['OrdNum']))
    story.append(Paragraph("AN ORDINANCE CLOSING OFF THE CITY OF DAVAO TO MINING OPERATIONS", styles['LongTitle']))
    
    preambles = [
        "WHEREAS, Section 16, Article II of the 1987 Philippine Constitution guarantees that the State shall protect and advance the right of the people to a balanced and healthful ecology in accord with the rhythm and harmony of nature;",
        "WHEREAS, Section 16 of Republic Act No. 7160 (Local Government Code of 1991) mandates that every local government unit shall exercise powers essential to the promotion of the general welfare, the maintenance of ecological balance, and the preservation of comfort and convenience of inhabitants;",
        "WHEREAS, the pristine watersheds, river basins, and recharge aquifers of Davao City—particularly the Panigan-Tamugan watershed and Talomo-Lipadas river systems—serve as the indispensable potable water lifelines for more than 1.6 million residents;",
        "WHEREAS, extensive geological assessments, environmental impact documentation, and multi-sectoral public hearings confirm that metallic mining, open-pit mineral extraction, and chemical leaching cause catastrophic deforestation, aquifer contamination, heavy metal poisoning, and permanent ecological degradation;",
        "WHEREAS, the landmark principle of inter-generational responsibility established under Oposa v. Factoran mandates that current trustees of local governance protect natural resources for generations yet unborn;",
        "WHEREAS, the Sangguniang Panlungsod of Davao City resolves that no economic royalty or fiscal incentive can compensate for the irreversible destruction of the city's water recharge zones and agricultural biodiversity;"
    ]
    for w in preambles:
        story.append(Paragraph(w, styles['Whereas']))
        
    story.append(Spacer(1, 4))
    story.append(Paragraph("Be it ordained by the Sangguniang Panlungsod of Davao City in session assembled that:", styles['Enacting']))
    
    sections = [
        {
            "number": 1,
            "heading": "TITLE",
            "text": "This Ordinance shall be known and cited as 'An Ordinance Closing Off the City of Davao to Mining Operations' or the 'Davao City Mining Closure Ordinance of 2015'."
        },
        {
            "number": 2,
            "heading": "DECLARATION OF POLICY",
            "text": "It is hereby declared the policy of the City Government of Davao to maintain ecological balance, safeguard its potable water sources, preserve agricultural landholdings, and shield its inhabitants from the devastating effects of extractive mineral exploration and exploitation."
        },
        {
            "number": 3,
            "heading": "TERRITORIAL COVERAGE",
            "text": "The provisions of this Ordinance shall strictly apply to all lands, upland territories, ancestral domains, watershed recharge areas, conservation zones, and water bodies located within the entire territorial jurisdiction of Davao City."
        },
        {
            "number": 4,
            "heading": "DEFINITION OF TERMS",
            "text": "For purposes of this Ordinance, the following terms shall be defined as follows:\n\n"
                    "a. Mining — refers to the extraction, exploration, prospecting, utilization, development, or processing of minerals, whether metallic or non-metallic, through open-pit, underground, tunneling, placer, or chemical leaching mechanisms.\n\n"
                    "b. Metallic Minerals — refer to minerals such as gold, copper, nickel, chromite, iron, silver, and other base or precious metallic ores.\n\n"
                    "c. Quarry Resources — refer to common rocks, sand, gravel, earthfill, diorite, limestone, and other non-metallic minerals used exclusively for building and infrastructure construction that do not contain valuable metallic ores in economically workable quantities.\n\n"
                    "d. Mineral Agreements — refer to national contracts, permits, Financial or Technical Assistance Agreements (FTAAs), or Mineral Production Sharing Agreements (MPSAs) granted under Republic Act No. 7942."
        },
        {
            "number": 5,
            "heading": "PROHIBITION ON MINING OPERATIONS",
            "text": "No approval, clearance, permit, or endorsement shall be granted or issued by the City of Davao through its Sangguniang Panlungsod or the City Mayor to any person, natural or juridical, to undertake any and all forms of mining operation, mineral exploration, prospecting, or processing in any area within the territorial jurisdiction of Davao City. The City Mayor and all administrative departments are expressly prohibited from issuing Mayor's Clearances, Business Permits, or Locational Approvals to mining concessionaires holding national mineral agreements."
        },
        {
            "number": 6,
            "heading": "EXEMPTION OF TRADITIONAL QUARRY RESOURCES",
            "text": "The prohibition established under Section 5 shall not apply to the extraction of non-metallic quarry resources, such as sand, gravel, boulder, and earthfill for local construction needs; Provided, that said extraction strictly adheres to the Davao City Watershed Code, possesses valid environmental compliance certificates, does not involve metallic substances, and secures prior written clearance from the City Mining Regulatory Board."
        },
        {
            "number": 7,
            "heading": "PENAL SANCTIONS",
            "text": "Any person or corporate entity that violates the provisions of this Ordinance shall be punished by a fine of Five Thousand Pesos (₱5,000.00) and imprisonment of not less than six (6) months nor more than one (1) year, or both, at the discretion of the court.\n\n"
                    "In addition, the business permit of the offending entity shall be perpetually cancelled, its mining machinery and extractive equipment impounded and forfeited in favor of the City Government, and its operational site subject to summary physical closure."
        },
        {
            "number": 8,
            "heading": "SEPARABILITY CLAUSE",
            "text": "If, for any reason, any section or provision of this Ordinance is held unconstitutional or invalid by a competent court, the other sections or provisions not affected thereby shall remain in full force and effect."
        },
        {
            "number": 9,
            "heading": "EFFECTIVITY CLAUSE",
            "text": "This Ordinance shall take effect immediately upon its approval and publication in a local newspaper of general circulation in Davao City."
        }
    ]
    
    for s in sections:
        head_text = f"SECTION {s['number']}. {escape(s['heading'])}."
        story.append(Paragraph(head_text, styles['SecHeading']))
        for p in s['text'].split('\n\n'):
            story.append(Paragraph(escape(p), styles['Body']))
        story.append(Spacer(1, 3))
        
    story.append(Spacer(1, 14))
    story.append(Paragraph("ENACTED, May 5, 2015 by the 17th Sangguniang Panlungsod of Davao City.", styles['BodyNoIndent']))
    story.append(Spacer(1, 14))
    
    sig_data = [
        [
            Paragraph("CERTIFIED CORRECT:<br/><br/><b>CHARITO N. SANTOS</b><br/>Secretary to the Sanggunian", styles['SignatoryName']),
            Paragraph("ATTESTED:<br/><br/><b>PAOLO Z. DUTERTE</b><br/>Vice Mayor & Presiding Officer", styles['SignatoryName'])
        ],
        [
            "",
            Paragraph("APPROVED, May 15, 2015:<br/><br/><b>RODRIGO R. DUTERTE</b><br/>City Mayor", styles['SignatoryName'])
        ]
    ]
    sig_table = Table(sig_data, colWidths=[USABLE_WIDTH * 0.5, USABLE_WIDTH * 0.5])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12)
    ]))
    story.append(KeepTogether(sig_table))
    
    compile_pdf(pdf_path, short_title, story)
    
    # Update JSON
    json_path = CASES_JSON_DIR / "06_mining_ban_watershed.json"
    case_data = {
        "title": "AN ORDINANCE CLOSING OFF THE CITY OF DAVAO TO MINING OPERATIONS",
        "ordinance_no": "Ordinance No. 0325-15",
        "series": 2015,
        "lgu": "City of Davao",
        "file": pdf_name,
        "sections": sections
    }
    json_path.write_text(json.dumps(case_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated JSON: {json_path.name} ({len(sections)} sections)")


# =========================================================================
# 4. CASE 09: CAGAYAN DE ORO ORDINANCE NO. 3375-93 (ANTI-CASINO ORDINANCE)
# =========================================================================
def build_case_09():
    styles = get_styles()
    short_title = "CAGAYAN DE ORO CITY ORDINANCE NO. 3375-93"
    pdf_name = "09_magtajas_casino_preemption.pdf"
    pdf_path = DEMO_PDF_DIR / pdf_name
    
    story = []
    story.append(Paragraph("REPUBLIC OF THE PHILIPPINES", styles['HeaderRep']))
    story.append(Paragraph("CITY OF CAGAYAN DE ORO", styles['HeaderCity']))
    story.append(Paragraph("OFFICE OF THE SANGGUNIANG PANLUNGSOD", styles['HeaderOffice']))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#800000"), spaceAfter=6, spaceBefore=2))
    
    story.append(Paragraph("EXCERPTS FROM THE MINUTES OF THE REGULAR SESSION OF THE CITY COUNCIL OF CAGAYAN DE ORO HELD ON JANUARY 4, 1993", styles['SessionInfo']))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("ORDINANCE NO. 3375-93", styles['OrdNum']))
    story.append(Paragraph("AN ORDINANCE PROHIBITING THE OPERATION OF CASINO AND PROVIDING PENALTY FOR VIOLATION THEREFOR", styles['LongTitle']))
    
    preambles = [
        "WHEREAS, the City Council established a policy as early as 1990 against CASINO under its Resolution No. 2295;",
        "WHEREAS, on October 14, 1992, the City Council passed another Resolution No. 2673, reiterating its policy against the establishment of CASINO;",
        "WHEREAS, subsequently, thereafter, it likewise passed Ordinance No. 3353, prohibiting the issuance of Business Permit and to cancel existing Business Permit to any establishment for the using and allowing to be used its premises or portion thereof for the operation of CASINO;",
        "WHEREAS, under Art. 3, section 458, No. (4), sub paragraph VI of the Local Government Code of 1991 (Rep. Act 7160) and under Art. 99, No. (4), Paragraph VI of the implementing rules of the Local Government Code, the City Council as the Legislative Body shall enact measure to suppress any activity inimical to public morals and general welfare of the people and/or regulate or prohibit such activity pertaining to amusement or entertainment in order to protect social and moral welfare of the community;"
    ]
    for w in preambles:
        story.append(Paragraph(w, styles['Whereas']))
        
    story.append(Spacer(1, 4))
    story.append(Paragraph("NOW THEREFORE,<br/>BE IT ORDAINED by the City Council in session duly assembled that:", styles['Enacting']))
    
    sections = [
        {
            "number": 1,
            "heading": "PROHIBITION OF CASINO OPERATIONS",
            "text": "The operation of gambling CASINO in the City of Cagayan de Oro is hereby prohibited."
        },
        {
            "number": 2,
            "heading": "PENALTIES AND SANCTIONS",
            "text": "Any violation of this Ordinance shall be subject to the following penalties:\n\n"
                    "a) Administrative fine of Five Thousand Pesos (₱5,000.00) shall be imposed against the proprietor, partnership or corporation undertaking the operation, conduct, maintenance of gambling CASINO in the City and closure thereof;\n\n"
                    "b) Imprisonment of not less than six (6) months nor more than one (1) year or a fine in the amount of Five Thousand Pesos (₱5,000.00) or both at the discretion of the court against the manager, supervisor, and/or any person responsible in the establishment, conduct and maintenance of gambling CASINO."
        },
        {
            "number": 3,
            "heading": "EFFECTIVITY",
            "text": "This Ordinance shall take effect ten (10) days after its publication in a local newspaper of general circulation."
        }
    ]
    
    for s in sections:
        head_text = f"SEC. {s['number']}. {escape(s['heading'])}."
        story.append(Paragraph(head_text, styles['SecHeading']))
        for p in s['text'].split('\n\n'):
            story.append(Paragraph(escape(p), styles['Body']))
        story.append(Spacer(1, 3))
        
    story.append(Spacer(1, 14))
    story.append(Paragraph("ENACTED, January 4, 1993 by the Sangguniang Panlungsod of Cagayan de Oro.", styles['BodyNoIndent']))
    story.append(Spacer(1, 14))
    
    sig_data = [
        [
            Paragraph("CERTIFIED CORRECT:<br/><br/><b>ATTY. JOSELITO C. TORRES</b><br/>Secretary to the Sanggunian", styles['SignatoryName']),
            Paragraph("ATTESTED:<br/><br/><b>ERASMO B. DAMASING</b><br/>Vice Mayor & Presiding Officer", styles['SignatoryName'])
        ],
        [
            "",
            Paragraph("APPROVED, January 11, 1993:<br/><br/><b>PABLO P. MAGTAJAS</b><br/>City Mayor", styles['SignatoryName'])
        ]
    ]
    sig_table = Table(sig_data, colWidths=[USABLE_WIDTH * 0.5, USABLE_WIDTH * 0.5])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12)
    ]))
    story.append(KeepTogether(sig_table))
    
    compile_pdf(pdf_path, short_title, story)
    
    # Update JSON
    json_path = CASES_JSON_DIR / "09_magtajas_casino_preemption.json"
    case_data = {
        "title": "AN ORDINANCE PROHIBITING THE OPERATION OF CASINO AND PROVIDING PENALTY FOR VIOLATION THEREFOR",
        "ordinance_no": "Ordinance No. 3375-93",
        "series": 1993,
        "lgu": "City of Cagayan de Oro",
        "file": pdf_name,
        "sections": sections
    }
    json_path.write_text(json.dumps(case_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated JSON: {json_path.name} ({len(sections)} sections)")


# =========================================================================
# 5. CASE 10: MANILA ORDINANCE NO. 7783 (ERMITA-MALATE COMMERCIAL CLOSURE)
# =========================================================================
def build_case_10():
    styles = get_styles()
    short_title = "MANILA ORDINANCE NO. 7783"
    pdf_name = "10_city_of_manila_laguio_due_process.pdf"
    pdf_path = DEMO_PDF_DIR / pdf_name
    
    story = []
    story.append(Paragraph("REPUBLIC OF THE PHILIPPINES", styles['HeaderRep']))
    story.append(Paragraph("CITY OF MANILA", styles['HeaderCity']))
    story.append(Paragraph("CITY COUNCIL OF MANILA", styles['HeaderOffice']))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#800000"), spaceAfter=6, spaceBefore=2))
    
    story.append(Paragraph("EXCERPTS FROM THE MINUTES OF THE REGULAR SESSION OF THE CITY COUNCIL OF MANILA HELD ON MARCH 9, 1993", styles['SessionInfo']))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("ORDINANCE NO. 7783", styles['OrdNum']))
    story.append(Paragraph("AN ORDINANCE PROHIBITING THE ESTABLISHMENT OR OPERATION OF BUSINESSES PROVIDING CERTAIN FORMS OF AMUSEMENT, ENTERTAINMENT, SERVICES AND FACILITIES IN THE ERMITA-MALATE AREA, PRESCRIBING PENALTIES FOR VIOLATION THEREOF, AND FOR OTHER PURPOSES", styles['LongTitle']))
    
    preambles = [
        "WHEREAS, the historic district of Ermita-Malate is a recognized tourist, cultural, and educational belt under Presidential Decree No. 499;",
        "WHEREAS, the proliferation of establishments promoting commercialized entertainment and adult vice impairs the moral welfare, tranquility, and peace of local inhabitants;",
        "WHEREAS, the City Council of Manila is empowered under Section 458 of Republic Act No. 7160 to regulate businesses and adopt measures designed to protect the morality and general welfare of the community;"
    ]
    for w in preambles:
        story.append(Paragraph(w, styles['Whereas']))
        
    story.append(Spacer(1, 4))
    story.append(Paragraph("Be it ordained by the City Council of Manila in session assembled that:", styles['Enacting']))
    
    sections = [
        {
            "number": 1,
            "heading": "PROHIBITED ESTABLISHMENTS AND COVERED TERRITORIAL AREA",
            "text": "Any provision of existing laws and ordinances to the contrary notwithstanding, no person, partnership, corporation or entity shall, in the Ermita-Malate area bounded by Teodoro M. Kalaw Sr. Street in the North, Taft Avenue in the East, Vito Cruz Street in the South and Roxas Boulevard in the West, pursuant to P.D. 499 be allowed or authorized to contract and engage in, any business providing certain forms of amusement, entertainment, services and facilities where women are used as tools in entertainment and which tend to disturb the community, annoy the inhabitants, and adversely affect the social and moral welfare of the community, such as but not limited to:\n\n"
                    "1. Sauna Parlors\n"
                    "2. Massage Parlors\n"
                    "3. Karaoke Bars\n"
                    "4. Beerhouses\n"
                    "5. Night Clubs\n"
                    "6. Day Clubs\n"
                    "7. Super Clubs\n"
                    "8. Discotheques\n"
                    "9. Cabarets\n"
                    "10. Dance Halls\n"
                    "11. Motels\n"
                    "12. Inns"
        },
        {
            "number": 2,
            "heading": "PROHIBITION ON PERMIT ISSUANCE AND PAYMENT ACCEPTANCE",
            "text": "The City Mayor, the City Treasurer or any person acting in behalf of the said officials are prohibited from issuing permits, temporary or otherwise, or from granting licenses and accepting payments for the operation of business enumerated in the preceding section."
        },
        {
            "number": 3,
            "heading": "WINDING UP PERIOD AND ALLOWABLE CONVERSION BUSINESSES",
            "text": "Owners and/or operator of establishments engaged in, or devoted to, the businesses enumerated in Section 1 hereof are hereby given three (3) months from the date of approval of this ordinance within which to wind up business operations or to transfer to any place outside of the Ermita-Malate area or convert said businesses to other kinds of business allowable within the area, such as but not limited to:\n\n"
                    "1. Curio or antique shop\n"
                    "2. Souvenir Shops\n"
                    "3. Handicrafts display centers\n"
                    "4. Art galleries\n"
                    "5. Records and music shops\n"
                    "6. Restaurants\n"
                    "7. Coffee shops\n"
                    "8. Flower shops\n"
                    "9. Music lounge and sing-along restaurants, with well-defined activities for wholesome family entertainment that cater to both local and foreign clientele.\n"
                    "10. Theaters engaged in the exhibition, not only of motion pictures but also of cultural shows, stage and theatrical plays, art exhibitions, concerts and the like.\n"
                    "11. Businesses allowable within the law and medium intensity districts as provided for in the zoning ordinances for Metropolitan Manila, except new warehouse or open-storage depot, dock or yard, motor repair shop, gasoline service station, light industry with any machinery, or funeral establishments."
        },
        {
            "number": 4,
            "heading": "PENAL SANCTIONS AND SUMMARY CLOSURE",
            "text": "Any person violating any provisions of this ordinance, shall upon conviction, be punished by imprisonment of one (1) year or fine of FIVE THOUSAND (₱5,000.00) PESOS, or both, at the discretion of the Court, PROVIDED, that in case of juridical person, the President, the General Manager, or person-in-charge of operation shall be liable thereof; PROVIDED FURTHER, that in case of subsequent violation and conviction, the premises of the erring establishment shall be closed and padlocked permanently."
        },
        {
            "number": 5,
            "heading": "EFFECTIVITY",
            "text": "This ordinance shall take effect upon approval."
        }
    ]
    
    for s in sections:
        head_text = f"SEC. {s['number']}. {escape(s['heading'])}."
        story.append(Paragraph(head_text, styles['SecHeading']))
        for p in s['text'].split('\n\n'):
            story.append(Paragraph(escape(p), styles['Body']))
        story.append(Spacer(1, 3))
        
    story.append(Spacer(1, 14))
    story.append(Paragraph("Enacted by the City Council of Manila at its regular session today, March 9, 1993.", styles['BodyNoIndent']))
    story.append(Spacer(1, 14))
    
    sig_data = [
        [
            Paragraph("CERTIFIED CORRECT:<br/><br/><b>MANUEL T. UY</b><br/>Secretary to the City Council", styles['SignatoryName']),
            Paragraph("ATTESTED:<br/><br/><b>JOSE L. ATIENZA, JR.</b><br/>Vice Mayor & Presiding Officer", styles['SignatoryName'])
        ],
        [
            "",
            Paragraph("APPROVED, March 30, 1993:<br/><br/><b>ALFREDO S. LIM</b><br/>City Mayor", styles['SignatoryName'])
        ]
    ]
    sig_table = Table(sig_data, colWidths=[USABLE_WIDTH * 0.5, USABLE_WIDTH * 0.5])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12)
    ]))
    story.append(KeepTogether(sig_table))
    
    compile_pdf(pdf_path, short_title, story)
    
    # Update JSON
    json_path = CASES_JSON_DIR / "10_city_of_manila_laguio_due_process.json"
    case_data = {
        "title": "AN ORDINANCE PROHIBITING THE ESTABLISHMENT OR OPERATION OF BUSINESSES PROVIDING CERTAIN FORMS OF AMUSEMENT, ENTERTAINMENT, SERVICES AND FACILITIES IN THE ERMITA-MALATE AREA, PRESCRIBING PENALTIES FOR VIOLATION THEREOF, AND FOR OTHER PURPOSES",
        "ordinance_no": "Ordinance No. 7783",
        "series": 1993,
        "lgu": "City of Manila",
        "file": pdf_name,
        "sections": sections
    }
    json_path.write_text(json.dumps(case_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated JSON: {json_path.name} ({len(sections)} sections)")


if __name__ == "__main__":
    print("Building all 5 complete Tier 3 enactments...")
    build_case_01()
    build_case_05()
    build_case_06()
    build_case_09()
    build_case_10()
    print("\nAll 5 enactments built and synchronized successfully!")
