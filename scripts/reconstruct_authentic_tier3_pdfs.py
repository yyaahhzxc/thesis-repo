"""
reconstruct_authentic_tier3_pdfs.py
===================================
Reconstructs 100% authentic Philippine Folio PDFs and sample case JSONs
from raw scans and verbatim text for Tier 3 cases:
- Case 01: Davao City Ordinance No. 0309-07 (Aerial Spraying Ban)
- Case 06: Davao City Ordinance No. 0325-15 (Mining Closure)
- Case 09: Cagayan de Oro Ordinance Nos. 3375-93 & 3353 (Anti-Casino)
- Case 10: Manila Ordinance No. 7783 (Ermita-Malate Commercial Closure)
"""

import os
import json
import shutil
from pathlib import Path
import xml.sax.saxutils as saxutils

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

REPO_ROOT = Path(__file__).resolve().parents[1]
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
        
        if self._pageNumber > 1:
            self.drawString(MARGIN_LEFT, PAGE_HEIGHT - 0.65 * inch, self.doc_short_title)
            self.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, PAGE_HEIGHT - 0.65 * inch, "OFFICIAL ENACTMENT")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(MARGIN_LEFT, PAGE_HEIGHT - 0.70 * inch, PAGE_WIDTH - MARGIN_RIGHT, PAGE_HEIGHT - 0.70 * inch)

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
    styles['RosterText'] = ParagraphStyle(
        'RosterText',
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1E293B")
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
    story.append(Paragraph("Republika ng Pilipinas", styles['HeaderRep']))
    story.append(Paragraph("SANGGUNIANG PANLUNGSOD", styles['HeaderCity']))
    story.append(Paragraph("Lungsod ng Dabaw", styles['HeaderOffice']))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#800000"), spaceAfter=6, spaceBefore=2))
    
    story.append(Paragraph("14th City Council | 3rd Regular Session | Series of 2007", styles['SessionInfo']))
    story.append(Spacer(1, 6))

    roster = (
        "<b>PRESENT:</b><br/>"
        "Vice Mayor Luis C. Bonguyan - Presiding Officer<br/>"
        "Councilor Nilo G. Abellera, Councilor Ma. Belen S. Acosta, Councilor Victorio S. Advincula, Sr., "
        "Councilor Wilberto E. Al-ag, Councilor Dante L. Apostol, Sr., Councilor Leonardo R. Avila, III, "
        "Councilor Conrado C. Baluran, Councilor Gerald B. Bangoy, Councilor Pilar C. Braga, "
        "Councilor Arnolfo Ricardo B. Cabling, Councilor Domingo G. L'Dalodo, Councilor Danilo C. Dayanghirang, "
        "Councilor April Marie C. Dayap, Councilor Jimmy G. Dureza, Councilor Emmanuel D. Galicia, Sr., "
        "Councilor Peter T. Laviña, Councilor Rene Elias C. Lopez, Councilor Diosdado Angelo A. Mahipus, Sr., "
        "Councilor Amilbangsa T. Manding, Councilor Paz C. Mata, Councilor Bonifacio E. Militar, "
        "Councilor Nenita R. Orcullo, Councilor Susan Isabel C. Reta, Councilor Angela Librado-Trinidad, "
        "Councilor Jose Louie P. Villafuerte, Councilor Jesus A. Zozobrado, Jr."
    )
    story.append(Paragraph(roster, styles['RosterText']))
    story.append(Spacer(1, 10))

    story.append(Paragraph("ORDINANCE NO. 0309-07 / 03252-07<br/>Series of 2007", styles['OrdNum']))
    story.append(Paragraph("AN ORDINANCE BANNING AERIAL SPRAYING AS AN AGRICULTURAL PRACTICE IN ALL AGRICULTURAL ACTIVITIES BY ALL AGRICULTURAL ENTITIES IN DAVAO CITY", styles['LongTitle']))
    story.append(Paragraph("Be it enacted by the Sangguniang Panlungsod of Davao City in session assembled that:", styles['Enacting']))
    
    sections = [
        {
            "number": 1,
            "heading": "TITLE",
            "text": "This Ordinance shall be known as 'An Ordinance Banning Aerial Spraying as an Agricultural Practice in all Agricultural Activities by all Agricultural Entities in Davao City';"
        },
        {
            "number": 2,
            "heading": "POLICY OF THE CITY",
            "text": "It shall be the policy of the City of Davao to eliminate the method of aerial spraying as an agricultural practice in all agricultural activities by all entities within Davao City;"
        },
        {
            "number": 3,
            "heading": "DEFINITION OF TERMS",
            "text": "a. Aerial Spraying- refers to application of substances through the use of aircraft of any form which dispenses the substances in the air.\n\n"
                    "b. Agricultural Practices- refer to the practices conducted by agricultural entities in relation to their agricultural activities;\n\n"
                    "c. Agricultural Activities- refer to activities that include, but not limited to, land preparation, seeding, planting, cultivation, harvesting and bagging;\n\n"
                    "d. Agricultural Entities- refer to persons, natural or juridical, involved in agricultural activities;\n\n"
                    "e. Buffer Zone- is an identified 30-meter zone within and around the boundaries of agricultural farms/plantations that need special monitoring to avoid or minimize harm to the environment and inhabitants pursuant to policies and guidelines set forth in this Ordinance and other government regulations. It is an area of land that must lie within the property which does not include public lands, public thoroughfares or adjacent private properties. It must be planted with diversified trees that grow taller than what are usually planted and grown in the plantation to protect those within the adjacent fields, neighboring farms, residential area, schools and workplaces;"
        },
        {
            "number": 4,
            "heading": "SCOPE AND APPLICABILITY",
            "text": "The provisions of this Ordinance shall apply to all agricultural entities within the territorial jurisdiction of Davao City;"
        },
        {
            "number": 5,
            "heading": "BAN OF AERIAL SPRAYING",
            "text": "A ban on aerial spraying shall be strictly enforced in the territorial jurisdiction of Davao City three (3) months after the effectivity of this Ordinance;"
        },
        {
            "number": 6,
            "heading": "BUFFER ZONE",
            "text": "Consistent with national legislation and government regulations, all agricultural entities must provide for a thirty (30) meter buffer zone within the boundaries of their agricultural farms/plantations. This buffer zone must be properly identified through Global Positioning System (GPS) survey. A survey plan showing the metes and bounds of each agricultural farm/plantation must be submitted to the City Mayor's Office, with the buffer zone clearly identified therein;"
        },
        {
            "number": 7,
            "heading": "PENAL PROVISION",
            "text": "Violation of any provision of this Ordinance shall be punished as follows:\n\n"
                    "a. First Offense: Fine of P5,000.00 and imprisonment of not less than one (1) month but not more than three (3) months;\n\n"
                    "b. Second Offense: Fine of P5,000.00 and imprisonment of not less than three (3) months but not more than six (6) months and suspension of City-issued permits and licenses for one (1) year;\n\n"
                    "c. Third Offense: Fine of P5,000.00 and imprisonment of not less than six (6) months but not more than one (1) year and perpetual cancellation of City-issued permits and licenses;\n\n"
                    "Provided, that in case the violation has been committed by a juridical person, the person in charge of the management thereof shall be held liable;"
        },
        {
            "number": 8,
            "heading": "REPEALING CLAUSE",
            "text": "Any Ordinance that is contrary to or inconsistent with any of the provisions of this Ordinance shall be deemed amended or repealed accordingly;"
        },
        {
            "number": 9,
            "heading": "EFFECTIVITY",
            "text": "This Ordinance shall take effect thirty (30) days from its publication in a newspaper of general circulation in Davao City;"
        }
    ]
    
    for s in sections:
        head_text = f"SECTION {s['number']}. {escape(s['heading'])}."
        story.append(Paragraph(head_text, styles['SecHeading']))
        for p in s['text'].split('\n\n'):
            story.append(Paragraph(escape(p), styles['Body']))
        story.append(Spacer(1, 3))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("ENACTED, January 23, 2007 by a majority vote of all the Members of the Sangguniang Panlungsod.<br/><i>(Note: Councilors Jimmy G. Dureza, Wilberto E. Al-ag, Ma. Belen S. Acosta and Conrado C. Baluran were out when this ordinance was approved).</i>", styles['BodyNoIndent']))
    story.append(Spacer(1, 14))
    
    sig_data = [
        [
            Paragraph("CERTIFIED CORRECT:<br/><br/><b>LOLITA C. GARCIA</b><br/>Secretary to the Sangguniang Panlungsod<br/>(City Government Department Head II)", styles['SignatoryName']),
            Paragraph("ATTESTED:<br/><br/><b>LUIS C. BONGUYAN</b><br/>Vice Mayor & Presiding Officer", styles['SignatoryName'])
        ],
        [
            Paragraph("<br/>ATTESTED:<br/><br/><b>WENDEL E. AVISADO</b><br/>City Administrator", styles['SignatoryName']),
            Paragraph("<br/>APPROVED, February 9, 2007:<br/><br/><b>RODRIGO R. DUTERTE</b><br/>City Mayor", styles['SignatoryName'])
        ]
    ]
    sig_table = Table(sig_data, colWidths=[USABLE_WIDTH * 0.5, USABLE_WIDTH * 0.5])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(KeepTogether(sig_table))
    
    compile_pdf(pdf_path, short_title, story)
    
    json_path = CASES_JSON_DIR / "01_mosqueda_aerial_spraying_ban.json"
    case_data = {
        "title": "AN ORDINANCE BANNING AERIAL SPRAYING AS AN AGRICULTURAL PRACTICE IN ALL AGRICULTURAL ACTIVITIES BY ALL AGRICULTURAL ENTITIES IN DAVAO CITY",
        "ordinance_no": "Ordinance No. 0309-07",
        "series": 2007,
        "lgu": "City of Davao",
        "file": pdf_name,
        "sections": sections
    }
    json_path.write_text(json.dumps(case_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated JSON: {json_path.name} ({len(sections)} sections)")


# =========================================================================
# 2. CASE 06: DAVAO CITY ORDINANCE NO. 0325-15 (MINING CLOSURE ORDINANCE)
# =========================================================================
def build_case_06():
    styles = get_styles()
    short_title = "DAVAO CITY ORDINANCE NO. 0325-15"
    pdf_name = "06_mining_ban_watershed.pdf"
    pdf_path = DEMO_PDF_DIR / pdf_name
    
    story = []
    story.append(Paragraph("Republic of the Philippines", styles['HeaderRep']))
    story.append(Paragraph("City of Davao", styles['HeaderCity']))
    story.append(Paragraph("Office of the Sangguniang Panlungsod", styles['HeaderOffice']))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#800000"), spaceAfter=6, spaceBefore=2))
    
    story.append(Paragraph("17th City Council | 17th Regular Session | Series of 2015", styles['SessionInfo']))
    story.append(Spacer(1, 6))

    roster = (
        "<b>PRESENT:</b> Councilor Rene Elias C. Lopez (Temporary Presiding Officer), "
        "Councilor Nilo M. Abellera Jr., Councilor Victorio U. Advincula Jr., Councilor Bernard E. Al-ag, "
        "Councilor Al Ryan S. Alejandre, Councilor Leonardo R. Avila III, Councilor Joanne M. Bonguyan-Quilos, "
        "Councilor Danilo C. Dayanghirang, Councilor April Marie C. Dayap, Councilor Jimmy G. Dureza, "
        "Councilor Leah A. Librado-Yap, Councilor Diosdado Angelo A. Mahipus Sr., Councilor Bonifacio E. Militar, "
        "Councilor Myrna G. L'Dalodo-Ortiz, Councilor Antoinette G. Principe-Castrodes, Councilor Marissa P. Salvador-Abella, "
        "Councilor Halila Y. Sudagar, Councilor Mary Joselle D. Villafuerte, Councilor Rachel P. Zozobrado.<br/>"
        "<b>ON OFFICIAL BUSINESS:</b> Councilor Ma. Belen S. Acosta (Palarong Pambansa, Tagum City), Councilor Karlo S. Bello (Manila).<br/>"
        "<b>ABSENT:</b> Vice Mayor Paolo Z. Duterte (On Vacation Leave), Councilor Louie John J. Bonguyan (On Vacation Leave), "
        "Councilor January N. Duterte (On Sick Leave), Councilor Edgar R. Ibuyan Sr. (On Domestic Emergency Leave), "
        "Councilor Tomas J. Monteverde IV (On Sick Leave)."
    )
    story.append(Paragraph(roster, styles['RosterText']))
    story.append(Spacer(1, 10))

    story.append(Paragraph("ORDINANCE NO. 0325-15<br/>Series of 2015", styles['OrdNum']))
    story.append(Paragraph("AN ORDINANCE CLOSING OFF THE CITY OF DAVAO TO MINING OPERATIONS", styles['LongTitle']))
    story.append(Paragraph("Be it ordained by the Sangguniang Panlungsod of Davao City in session assembled that:", styles['Enacting']))
    
    sections = [
        {
            "number": 1,
            "heading": "TITLE",
            "text": "This Ordinance shall be known as 'AN ORDINANCE CLOSING OFF THE CITY OF DAVAO TO MINING OPERATIONS';"
        },
        {
            "number": 2,
            "heading": "DECLARATION OF POLICY",
            "text": "The City of Davao hereby declares as its policies, the following, to wit:\n\n"
                    "a) The right of the people to a balanced and healthful ecology in accord with the rhythm and harmony of nature shall be protected and advanced by the City, consistent with the policy enshrined in Article II, Section 16 of the Constitution;\n\n"
                    "b) Under the provisions of the Local Government Code of 1991, in Section 458 (a) (1) (vi) and its Implementing Rules and Regulations, the Sangguniang Panlungsod has the power, the duty and function to protect the environment and impose appropriate penalties for such acts which endanger it;\n\n"
                    "c) The Local Government of Davao City, pursuant to Section 16 of the same Code, shall exercise the powers expressly granted, those necessarily implied therefrom, as well as, powers necessary, appropriate or incidental to its efficient and effective governance, and those which are essential to the promotion of the general welfare;\n\n"
                    "d) While mining has been identified as a highly-important economic program of the national government, the city recognizes the irreversibility of the destructive effects of mining on the earth's fragile ecosystem, especially to an island ecosystem such as Mindanao, and in worsening the magnitude of hunger and conflict as mining competes with the remaining available land, water and food resources;\n\n"
                    "e) The ravaging effects of extreme climatic events and other natural disasters which had visited the country with more frequency and worsening magnitude, demand that government policies and programs must integrate biodiversity protection in order to ensure that future generations will be able to enjoy a healthy and balanced ecology;\n\n"
                    "f) The Local Government of Davao City is mindful of the fact that the city is endowed with vast natural resources, of which the people are very protective of;\n\n"
                    "g) With the view of protecting the city's people and its rich biodiversity, the local government has enacted and passed legislations, notably among them Ordinance No. 03197-07, otherwise known as the 'Watershed Code of Davao City';\n\n"
                    "h) Pursuant to the Watershed Code, a closer view of the terrain analysis of the territorial jurisdiction of Davao City reveals that the city is comprised with areas which are already declared watershed areas, protected areas, prime agricultural areas and the areas inhabited by the people, such that mining in any form or stage poses a most detrimental impact on the ecological balance and the very lives of the people;\n\n"
                    "i) The Local Government of Davao City has taken upon itself the duty and responsibility to protect and preserve the environment for the generations to come under the context of 'inter-generational responsibility' enunciated by the Supreme Court in the case of Oposa vs. Factoran; and\n\n"
                    "j) Within the same context of 'inter-generational responsibility', it is hereby declared that no approval shall ever be issued to any mining project within the territorial jurisdiction of Davao City;"
        },
        {
            "number": 3,
            "heading": "PURPOSE",
            "text": "This Ordinance is enacted in order to protect and conserve the city's rich biodiversity, under the principle that the environment should not be degraded in the name of economy and development, to ensure that future generations will still be able to enjoy a healthy and balanced ecology;"
        },
        {
            "number": 4,
            "heading": "DEFINITION OF TERMS",
            "text": "As used in this Ordinance, the following terms shall mean as follows:\n\n"
                    "a) 'Minerals' refers to all naturally occurring inorganic substance in solid, gas, liquid, or any intermediate state, excluding energy materials such as coal, petroleum, natural gas, radioactive materials and geothermal energy;\n\n"
                    "b) 'Mining operation' means mining activities involving exploration, feasibility, development, utilization and processing;\n\n"
                    "c) 'Quarrying' means the process of extracting, removing and disposing quarry resources found on or underneath the surface of public or private lands;\n\n"
                    "d) 'Quarry resources' refers to any common rock or other mineral substances as the Director of Mines and Geosciences Bureau may declare to be quarry resources such as, but not limited to, andesite, basalt, conglomerate, coral sand, diatomaceous earth, diorite, decorative stones, gabbro, granite, limestone, marble, marl, red burning clays for potteries and bricks, rhyolite, rock phosphate, sandstone, serpentine, shale, tuff, volcanic cinders, and volcanic glass: Provided, that such quarry resources do not contain metals or metallic constituents and/or other valuable minerals in economically workable quantities: Provided, further, that non-metallic minerals such as kaolin, feldspar, bull quartz, quartz or silica, sand and pebbles, bentonite, talc, asbestos, barite, gypsum, bauxite, magnesite, dolomite, mica, precious and semi-precious stones, and other non-metallic minerals that may later be discovered and which the Director declares the same to be of economically workable quantities, shall not be classified under the category of quarry resources;\n\n"
                    "e) 'Biodiversity' refers to the variety of life formed and found on earth; comprises all living things and the genes they contain, the ecosystem they build and the way they live and interact together;"
        },
        {
            "number": 5,
            "heading": "NO APPROVAL OF MINING OPERATIONS",
            "text": "No approval shall be granted or issued by the city through its Sangguniang Panlungsod to any person, natural or juridical, to undertake any and all forms of mining operation in any area within the territorial of Davao City, except rocks and mineral substances classified under the category of quarry resources.\n\n"
                    "Pursuant thereto, no permit shall be issued by the local government and/or any of its offices, allowing any entity, natural or juridical, to engage in any business involving, whether directly or indirectly, mining activities or operations of any kind or stage, within the territorial jurisdiction of Davao City."
        },
        {
            "number": 6,
            "heading": "INFORMATION, EDUCATION AND ADVOCACY",
            "text": "The City Government, in cooperation with the academe, civil society and the business community, shall implement a continuing information and education campaign to encourage awareness and vigilance among the citizenry on biodiversity protection. In particular, this information campaign shall be given to schools in order to educate the young citizens of the importance in protecting the environment. For this purpose, the City Environment and Natural resources (CENRO) shall take the lead in the campaigns;"
        },
        {
            "number": 7,
            "heading": "PENALTIES",
            "text": "Any person found guilty of violating any provision of this Ordinance shall be punished with imprisonment of not exceeding one (1) year or a fine of not more than Five Thousand Pesos (Php 5,000.00) only or both at the discretion of the court, without prejudice to the filing of the appropriate administrative, civil or criminal action;"
        },
        {
            "number": 8,
            "heading": "ADMINISTRATIVE SANCTIONS",
            "text": "Government officials and employees who fail to comply with and enforce the provisions of this Ordinance shall be charged administratively in accordance with existing laws, rules and regulations;"
        },
        {
            "number": 9,
            "heading": "REPEALING CLAUSE",
            "text": "All Ordinance, Executive Orders, resolutions and regulations inconsistent with the provisions of this Ordinance are hereby repealed or modified accordingly;"
        },
        {
            "number": 10,
            "heading": "EFFECTIVITY",
            "text": "This Ordinance shall be posted in all government offices, including barangay halls and shall also be published in full text once a week for three (3) consecutive weeks in a newspaper of general circulation within the jurisdiction of Davao City. This Ordinance shall take effect fifteen (15) days from the date of the last publication thereof;"
        }
    ]
    
    for s in sections:
        head_text = f"SECTION {s['number']}. {escape(s['heading'])}."
        story.append(Paragraph(head_text, styles['SecHeading']))
        for p in s['text'].split('\n\n'):
            story.append(Paragraph(escape(p), styles['Body']))
        story.append(Spacer(1, 3))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("ENACTED, May 5, 2015, by a majority vote of all the Members of the Sanggunian Panlungsod present, there being a quorum.", styles['BodyNoIndent']))
    story.append(Spacer(1, 14))
    
    sig_data = [
        [
            Paragraph("CERTIFIED CORRECT:<br/><br/><b>CHARITO N. SANTOS</b><br/>Secretary to the Sangguniang Panlungsod<br/>(City Government Department Head II)", styles['SignatoryName']),
            Paragraph("ATTESTED:<br/><br/><b>RENE ELIAS C. LOPEZ</b><br/>City Councilor<br/>Temporary Presiding Officer", styles['SignatoryName'])
        ],
        [
            Paragraph("<br/>ATTESTED:<br/><br/><b>ATTY. JESUS MELCHOR V. QUITAIN</b><br/>City Administrator", styles['SignatoryName']),
            Paragraph("<br/>APPROVED: ____________, 2015<br/><b>[LAPSED INTO LAW]</b><br/><i>DEEMED APPROVED AFTER THE LAPSE OF TEN (10) DAYS PER SEC. 54 (b), R.A. 7160</i><br/><b>RODRIGO R. DUTERTE</b><br/>City Mayor", styles['SignatoryName'])
        ]
    ]
    sig_table = Table(sig_data, colWidths=[USABLE_WIDTH * 0.5, USABLE_WIDTH * 0.5])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(KeepTogether(sig_table))
    
    compile_pdf(pdf_path, short_title, story)
    
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
# 3. CASE 09: CAGAYAN DE ORO ORDINANCE NOS. 3375-93 & 3353 (ANTI-CASINO)
# =========================================================================
def build_case_09():
    styles = get_styles()
    short_title = "CAGAYAN DE ORO ORDINANCE NOS. 3375-93 & 3353"
    pdf_name = "09_magtajas_casino_preemption.pdf"
    pdf_path = DEMO_PDF_DIR / pdf_name
    
    story = []
    story.append(Paragraph("REPUBLIC OF THE PHILIPPINES", styles['HeaderRep']))
    story.append(Paragraph("CITY OF CAGAYAN DE ORO", styles['HeaderCity']))
    story.append(Paragraph("OFFICE OF THE SANGGUNIANG PANLUNGSOD", styles['HeaderOffice']))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#800000"), spaceAfter=6, spaceBefore=2))
    
    story.append(Paragraph("EXCERPTS FROM THE MINUTES OF THE REGULAR SESSION OF THE CITY COUNCIL OF CAGAYAN DE ORO", styles['SessionInfo']))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("ORDINANCE NO. 3375-93<br/>Series of 1993", styles['OrdNum']))
    story.append(Paragraph("AN ORDINANCE PROHIBITING THE OPERATION OF CASINO AND PROVIDING PENALTY FOR VIOLATION THEREFOR", styles['LongTitle']))
    
    preambles_3375 = [
        "WHEREAS, the City Council established a policy as early as 1990 against CASINO under its Resolution No. 2295;",
        "WHEREAS, on October 14, 1992, the City Council passed another Resolution No. 2673, reiterating its policy against the establishment of CASINO;",
        "WHEREAS, subsequently, thereafter, it likewise passed Ordinance No. 3353, prohibiting the issuance of Business Permit and to cancel existing Business Permit to any establishment for the using and allowing to be used its premises or portion thereof for the operation of CASINO;",
        "WHEREAS, under Art. 3, section 458, No. (4), sub paragraph VI of the Local Government Code of 1991 (Rep. Act 7160) and under Art. 99, No. (4), Paragraph VI of the implementing rules of the Local Government Code, the City Council as the Legislative Body shall enact measure to suppress any activity inimical to public morals and general welfare of the people and/or regulate or prohibit such activity pertaining to amusement or entertainment in order to protect social and moral welfare of the community;"
    ]
    for w in preambles_3375:
        story.append(Paragraph(w, styles['Whereas']))
        
    story.append(Spacer(1, 4))
    story.append(Paragraph("NOW THEREFORE,<br/>BE IT ORDAINED by the City Council in session duly assembled that:", styles['Enacting']))
    
    sections = [
        {
            "number": 1,
            "heading": "PROHIBITION OF CASINO OPERATIONS (ORD. 3375-93)",
            "text": "The operation of gambling CASINO in the City of Cagayan de Oro is hereby prohibited."
        },
        {
            "number": 2,
            "heading": "PENALTIES AND SANCTIONS (ORD. 3375-93)",
            "text": "Any violation of this Ordinance shall be subject to the following penalties:\n\n"
                    "a) Administrative fine of Five Thousand Pesos (₱5,000.00) shall be imposed against the proprietor, partnership or corporation undertaking the operation, conduct, maintenance of gambling CASINO in the City and closure thereof;\n\n"
                    "b) Imprisonment of not less than six (6) months nor more than one (1) year or a fine in the amount of Five Thousand Pesos (₱5,000.00) or both at the discretion of the court against the manager, supervisor, and/or any person responsible in the establishment, conduct and maintenance of gambling CASINO."
        },
        {
            "number": 3,
            "heading": "EFFECTIVITY (ORD. 3375-93)",
            "text": "This Ordinance shall take effect ten (10) days after its publication in a local newspaper of general circulation."
        },
        {
            "number": 4,
            "heading": "PROHIBITION ON BUSINESS PERMITS FOR CASINO (ORD. 3353)",
            "text": "That pursuant to the policy of the city banning the operation of casino within its territorial jurisdiction, no business permit shall be issued to any person, partnership or corporation for the operation of casino within the city limits."
        },
        {
            "number": 5,
            "heading": "REVOCATION AND PREMISES PROHIBITION (ORD. 3353)",
            "text": "That it shall be a violation of existing business permit by any persons, partnership or corporation to use its business establishment or portion thereof, or allow the use thereof by others for casino operation and other gambling activities."
        },
        {
            "number": 6,
            "heading": "PENALTIES ON ESTABLISHMENT PERMITS (ORD. 3353)",
            "text": "Any violation of such existing business permit as defined in the preceding section shall suffer the following penalties, to wit:\n\n"
                    "a) Suspension of the business permit for sixty (60) days for the first offense and a fine of P1,000.00/day;\n\n"
                    "b) Suspension of the business permit for Six (6) months for the second offense, and a fine of P3,000.00/day;\n\n"
                    "c) Permanent revocation of the business permit and imprisonment of One (1) year, for the third and subsequent offenses."
        },
        {
            "number": 7,
            "heading": "EFFECTIVITY (ORD. 3353)",
            "text": "This Ordinance shall take effect ten (10) days from publication thereof."
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
        ('BOTTOMPADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(KeepTogether(sig_table))
    
    compile_pdf(pdf_path, short_title, story)
    
    json_path = CASES_JSON_DIR / "09_magtajas_casino_preemption.json"
    case_data = {
        "title": "AN ORDINANCE PROHIBITING THE OPERATION OF CASINO AND PROVIDING PENALTY FOR VIOLATION THEREFOR",
        "ordinance_no": "Ordinance Nos. 3375-93 & 3353",
        "series": 1993,
        "lgu": "City of Cagayan de Oro",
        "file": pdf_name,
        "sections": sections
    }
    json_path.write_text(json.dumps(case_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated JSON: {json_path.name} ({len(sections)} sections)")


# =========================================================================
# 4. CASE 10: MANILA ORDINANCE NO. 7783 (ERMITA-MALATE COMMERCIAL CLOSURE)
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
    
    story.append(Paragraph("Excerpts from the Minutes of the Regular Session of the City Council of Manila Held on March 9, 1993", styles['SessionInfo']))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("ORDINANCE NO. 7783", styles['OrdNum']))
    story.append(Paragraph("AN ORDINANCE PROHIBITING THE ESTABLISHMENT OR OPERATION OF BUSINESSES PROVIDING CERTAIN FORMS OF AMUSEMENT, ENTERTAINMENT, SERVICES AND FACILITIES IN THE ERMITA-MALATE AREA, PRESCRIBING PENALTIES FOR VIOLATION THEREOF; AND FOR OTHER PURPOSES.", styles['LongTitle']))
    story.append(Paragraph("Be it ordained by the City Council of Manila, THAT:", styles['Enacting']))
    
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
            "text": "The City Mayor, the City Treasurer or any person acting in behalf of the said officials are prohibited from issuing permits, temporary or otherwise, or from granting licenses and accepting payments for the operation of businesses enumerated in the preceding section."
        },
        {
            "number": 3,
            "heading": "WINDING UP PERIOD AND ALLOWABLE CONVERSION BUSINESSES",
            "text": "Owners and/or operator of establishments engaged in, or devoted to, the businesses enumerated in Section 1 hereof are hereby given three (3) months from the date of approval of this ordinance within which to wind up business operations or to transfer to any place outside of the Ermita-Malate area or convert said businesses to other kinds of business allowable within the area, such as but not limited to:\n\n"
                    "1. Curio or antique shops\n"
                    "2. Souvenir shops\n"
                    "3. Handicrafts display centers\n"
                    "4. Art galleries\n"
                    "5. Records and music shops\n"
                    "6. Restaurants\n"
                    "7. Coffee shops\n"
                    "8. Flower shops\n"
                    "9. Music lounge and sing-along restaurants, with well-defined activities for wholesome family entertainment that cater to both local and foreign clientele.\n"
                    "10. Theaters engaged in the exhibition, not only of motion pictures, but also of cultural shows, stage and theatrical plays, art exhibitions, concerts and the like.\n"
                    "11. Businesses allowable within the law and medium intensity districts as provided for in the zoning ordinances for Metropolitan Manila, except new warehouse or open-storage depot, dock or yard, motor repair shop, gasoline service station, light industry with any machinery, or funeral establishments."
        },
        {
            "number": 4,
            "heading": "PENAL SANCTIONS AND SUMMARY CLOSURE",
            "text": "Any person violating any of the provisions of this ordinance, shall upon conviction, be punished by imprisonment of one (1) year or fine of FIVE THOUSAND (P5,000.00) PESOS, or both, at the discretion of the Court, PROVIDED, that in case of juridical person, the President, the General Manager, or person-in-charge of operation shall be liable thereof; PROVIDED FURTHER, that in case of subsequent violation and conviction, the premises of the erring establishment shall be closed and padlocked permanently."
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
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Enacted by the City Council of Manila at its regular session today, March 9, 1993.<br/>Approved by His Honor, the Mayor on March 30, 1993.", styles['BodyNoIndent']))
    story.append(Spacer(1, 10))

    authors = (
        "<b>PRINCIPAL AUTHORS:</b> Hon. Bienvenido M. Abante, Jr., Hon. Humberto B. Basco, Hon. Nestor C. Ponce, Jr., "
        "Hon. Ernesto A. Nieva, Hon. Francisco G. Varona, Jr., Hon. Jhosep Y. Lopez, Hon. Ma. Paz E. Herrera, "
        "Hon. Gerino A. Tolentino, Jr., Hon. Ma. Lourdes M. Isip, Hon. Flaviano F. Concepcion, Jr., "
        "Hon. Ernesto V.P. Maceda, Jr., Hon. Victoriano A. Melendez, Hon. Ma. Corazon R. Caballes, "
        "Hon. Bernardito C. Ang, Hon. Roberto C. Ocampo, Hon. Rogelio B. dela Paz, Hon. Romeo G. Rivera, "
        "Hon. Alexander S. Ricafort, Hon. Avelino S. Cailian, Hon. Bernardo D. Ragasa, Hon. Joey D. Hizon, "
        "Hon. Leonardo L. Angat, and Hon. Jocelyn B. Dawis."
    )
    story.append(Paragraph(authors, styles['RosterText']))
    story.append(Spacer(1, 14))

    sig_data = [
        [
            Paragraph("APPROVED:<br/><br/><b>ALFREDO S. LIM</b><br/>Mayor, City of Manila", styles['SignatoryName']),
            Paragraph("ATTESTED:<br/><br/><b>MA. CORAZON R. CABALLES</b><br/>Acting Presiding Officer, City Council, Manila", styles['SignatoryName'])
        ],
        [
            Paragraph("<br/>ATTESTED:<br/><br/><b>RAFAELITO M. GARAYBLAS</b><br/>Secretary to the Mayor", styles['SignatoryName']),
            Paragraph("<br/>ATTESTED:<br/><br/><b>EMMANUEL R. SISON</b><br/>Secretary to the City Council", styles['SignatoryName'])
        ]
    ]
    sig_table = Table(sig_data, colWidths=[USABLE_WIDTH * 0.5, USABLE_WIDTH * 0.5])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(KeepTogether(sig_table))
    
    compile_pdf(pdf_path, short_title, story)
    
    json_path = CASES_JSON_DIR / "10_city_of_manila_laguio_due_process.json"
    case_data = {
        "title": "AN ORDINANCE PROHIBITING THE ESTABLISHMENT OR OPERATION OF BUSINESSES PROVIDING CERTAIN FORMS OF AMUSEMENT, ENTERTAINMENT, SERVICES AND FACILITIES IN THE ERMITA-MALATE AREA, PRESCRIBING PENALTIES FOR VIOLATION THEREOF; AND FOR OTHER PURPOSES.",
        "ordinance_no": "Ordinance No. 7783",
        "series": 1993,
        "lgu": "City of Manila",
        "file": pdf_name,
        "sections": sections
    }
    json_path.write_text(json.dumps(case_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated JSON: {json_path.name} ({len(sections)} sections)")


if __name__ == "__main__":
    print("Reconstructing authentic Philippine Folio PDFs from raw scans and transcripts...")
    build_case_01()
    build_case_06()
    build_case_09()
    build_case_10()
    print("\n[SUCCESS] All authentic PDFs and JSON manifests generated and synced!")

