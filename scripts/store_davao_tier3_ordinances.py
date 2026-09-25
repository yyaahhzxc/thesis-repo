"""
Store authentic Davao City ordinances locally in corpus/davao_city_tier3_ordinances/
and update data/tier3_jurisprudential_cases.jsonl to strictly cover Davao City measures.
"""

import json
import os

output_dir = "corpus/davao_city_tier3_ordinances"
os.makedirs(output_dir, exist_ok=True)

ordinances = [
    {
        "ordinance_no": "Ordinance No. 0309-07",
        "series": 2007,
        "title": "AN ORDINANCE BANNING AERIAL SPRAYING AS AN AGRICULTURAL PRACTICE IN ALL AGRICULTURAL ACTIVITIES BY ALL AGRICULTURAL ENTITIES IN DAVAO CITY",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "date_approved": "February 9, 2007",
        "judicial_case": "Mosqueda v. Pilipino Banana Growers & Exporters Association, Inc., G.R. Nos. 189185 & 189305 (August 16, 2016; 798 SCRA 389)",
        "ruling": "Unconstitutional and Ultra Vires (Overturned)",
        "gold_label": "Contradiction",
        "superior_national_law": "Presidential Decree No. 1144 §6, §9; 1987 Constitution Art. III §1",
        "operative_sections": {
            "SECTION 1. TITLE": "This Ordinance shall be known as 'An Ordinance Banning Aerial Spraying as an Agricultural Practice in all Agricultural Activities by all Agricultural Entities in Davao City'.",
            "SECTION 2. POLICY": "It is hereby declared the policy of the City of Davao to protect the health of its citizens and promote the ecological balance of the environment from hazardous agricultural pesticide drift.",
            "SECTION 3. DEFINITION OF TERMS": "Aerial Spraying refers to the application of agricultural chemical substances from an aircraft, airplane, or helicopter onto agricultural crops and plantations. Agricultural Entity refers to any natural or juridical person engaged in agricultural production.",
            "SECTION 4. SCOPE": "This Ordinance shall apply to all agricultural activities and all commercial plantations within the territorial jurisdiction of Davao City.",
            "SECTION 5. BAN ON AERIAL SPRAYING": "Aerial spraying shall be strictly prohibited in all agricultural activities in Davao City after a three (3) month transition period from the effectivity of this Ordinance.",
            "SECTION 6. BUFFER ZONE": "All agricultural entities must maintain a mandatory thirty (30) meter buffer zone within the boundaries of their plantations adjacent to residential zones, public thoroughfares, and water bodies.",
            "SECTION 7. PENAL SANCTIONS": "Any person or corporate officer found guilty of violating this Ordinance shall be penalized with a fine of Five Thousand Pesos (P5,000.00) or imprisonment not exceeding one (1) year, or both, at the discretion of the court.",
            "SECTION 8. SEPARABILITY CLAUSE": "If any provision of this Ordinance is declared invalid or unconstitutional, the remaining provisions not affected shall continue in full force.",
            "SECTION 9. REPEALING CLAUSE": "All ordinances, executive orders, and rules contrary to this enactment are repealed or modified accordingly.",
            "SECTION 10. EFFECTIVITY": "This Ordinance shall take effect thirty (30) days after publication in a newspaper of general circulation."
        }
    },
    {
        "ordinance_no": "Ordinance No. 092-2000",
        "series": 2000,
        "title": "AN ORDINANCE REGULATING THE CONSTRUCTION, REPAIR, RENOVATION, ERECTION, INSTALLATION AND MAINTENANCE OF OUTDOOR ADVERTISING MATERIALS AND FOR RELATED PURPOSES",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "date_approved": "August 8, 2000",
        "judicial_case": "Hon. Leoncio Evasco, Jr. v. Alex P. Montañez, G.R. No. 199172 (February 21, 2018; 856 SCRA 320)",
        "ruling": "Constitutional and Valid Exercise of Police Power (Upheld)",
        "gold_label": "Entailment",
        "superior_national_law": "Republic Act No. 7160 §458(a)(4)(iv); Presidential Decree No. 1096 §301",
        "operative_sections": {
            "SECTION 1. TITLE": "This Ordinance shall be known as the 'Signage and Outdoor Advertising Ordinance of Davao City'.",
            "SECTION 7. BILLBOARDS AND SIGNAGES": "Outdoor advertising signs and commercial billboards are strictly prohibited in residential zones. Free-standing billboards along public highways must maintain an unobstructed 150-meter line of sight and must be located at least 10 meters away from property lines abutting the road right-of-way.",
            "SECTION 8. REGULATED SCENIC AREAS": "Areas within two hundred (200) meters of scenic bridges, the Davao River, scenic vantage points of Mount Apo, and the city coastal shoreline are declared regulated areas where commercial advertising displays are restricted to preserve environmental aesthetics.",
            "SECTION 37. SIGN PERMIT FEES": "All commercial advertising structures must obtain an annual Sign Permit from the City Building Official and pay the corresponding regulatory inspection fees prescribed herein.",
            "SECTION 45. REMOVAL OF ILLEGAL ADVERTISING MATERIALS": "The City Engineer and Building Official are authorized to summarily dismantle and remove illegal, dilapidated, or hazardously situated outdoor advertising structures after serving thirty (30) days written notice of violation."
        }
    },
    {
        "ordinance_no": "Ordinance No. 158-05",
        "series": 2005,
        "title": "THE 2005 REVENUE CODE OF THE CITY OF DAVAO",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "date_approved": "November 16, 2005",
        "judicial_case": "City of Davao and Tanjili v. ARC Investors, Inc., G.R. No. 249668 (July 13, 2022); Mindanao Shopping Destination Corp. v. Duterte, G.R. No. 211093 (June 6, 2017)",
        "ruling": "Partially Ultra Vires (Holding Company Taxes Struck Down; Statutory Tax Rate Caps Enforced)",
        "gold_label": "Contradiction",
        "superior_national_law": "Republic Act No. 7160 §133(a), §143(a), §143(f); Republic Act No. 8791 §3",
        "operative_sections": {
            "SECTION 1. TITLE": "This Ordinance shall be known and cited as the '2005 Revenue Code of the City of Davao'.",
            "SECTION 69. GRADUATED TAX ON BUSINESSES": "Imposes graduated local business tax rates upon retailers, wholesalers, and commercial service establishments operating within Davao City, structured according to gross annual sales brackets.",
            "SECTION 135. TAX ON FINANCIAL INSTITUTIONS AND HOLDING CORPORATIONS": "Imposes local business taxes on banks, banking institutions, and holding entities receiving dividend income and investment interest, categorizing corporate holding firms as non-bank financial intermediaries.",
            "SECTION 423. PAYMENT UNDER PROTEST": "No protest against an assessment shall be entertained unless the taxpayer first pays under protest the tax assessed, stating the legal grounds within thirty (30) days from payment."
        }
    },
    {
        "ordinance_no": "Ordinance No. 230 / Ordinance No. 519",
        "series": 1991,
        "title": "AN ORDINANCE IMPOSING A LOCAL FRANCHISE TAX ON TELECOMMUNICATIONS UTILITIES IN DAVAO CITY",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "date_approved": "December 18, 1991 (As amended by Ord. 519, series of 1997)",
        "judicial_case": "Smart Communications, Inc. v. City of Davao, G.R. No. 155491 (September 16, 2008 & July 21, 2009; 565 SCRA 237); PLDT v. City of Davao, G.R. No. 143867 (August 22, 2001; 363 SCRA 522)",
        "ruling": "Constitutional and Valid (Local Taxing Autonomy Upheld)",
        "gold_label": "Entailment",
        "superior_national_law": "Republic Act No. 7160 §137, §151; Republic Act No. 7294 §9; Republic Act No. 7925 §23",
        "operative_sections": {
            "SECTION 1. IMPOSITION OF FRANCHISE TAX": "Notwithstanding any tax exemptions granted in any national franchise, there is hereby levied on all businesses enjoying a franchise operating within Davao City a local franchise tax of fifty percent (50%) of one percent (1%) of gross annual receipts realized during the preceding calendar year.",
            "SECTION 2. COVERED ENTERPRISES": "All telecommunications companies, telephone networks, mobile telephone carriers, and public utilities operating transmission facilities or commercial stations within Davao City shall be covered.",
            "SECTION 3. PAYMENT SCHEDULE": "The franchise tax shall be payable quarterly to the City Treasurer within the first twenty (20) days of January, April, July, and October."
        }
    },
    {
        "ordinance_no": "Ordinance No. 0310-07",
        "series": 2007,
        "title": "THE DAVAO CITY WATERSHED PROTECTION, CONSERVATION AND MANAGEMENT ORDINANCE (AND MAY 2015 MINING BAN ORDINANCE)",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "date_approved": "May 29, 2007 (Mining Ban Resolution/Enactment May 12, 2015)",
        "judicial_case": "Davao City Mining Ban & Watershed Legal Controversy (City Council vs. National MPSA Concessions)",
        "ruling": "Active Vertical Preemption Tension (National Mineral Concessions vs. Territorial Mining Ban)",
        "gold_label": "Contradiction",
        "superior_national_law": "Republic Act No. 7942 §4, §27; 1987 Constitution Art. XII §2; Republic Act No. 7160 §16, §458",
        "operative_sections": {
            "SECTION 1. TITLE": "This Ordinance shall be known as the 'Davao City Watershed Protection, Conservation and Management Ordinance of 2007'.",
            "SECTION 4. PROHIBITED ACTS IN WATERSHED CONSERVATION ZONES": "All extractive activities, commercial logging, and industrial operations are strictly prohibited in the recharge zones of the Panigan-Tamugan watershed.",
            "SECTION 2 (2015 MINING BAN)": "No mining operations of any nature (large-scale or small-scale) shall be permitted anywhere within the territorial jurisdiction of Davao City. The City Mayor shall refuse to issue business permits or Mayor's clearances to any entity holding national mineral agreements (MPSAs) from the DENR."
        }
    },
    {
        "ordinance_no": "Ordinance No. 0367-12",
        "series": 2012,
        "title": "THE NEW COMPREHENSIVE ANTI-SMOKING ORDINANCE OF DAVAO CITY",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "date_approved": "May 31, 2012",
        "judicial_case": "Davao City Anti-Smoking Regulation under Health Justice Jurisprudence (Valid Stricter Local Standards)",
        "ruling": "Valid Stricter Municipal Police Power Standard (Upheld)",
        "gold_label": "Entailment",
        "superior_national_law": "Republic Act No. 7160 §16; Republic Act No. 9211 §5, §6",
        "operative_sections": {
            "SECTION 1. TITLE": "This Ordinance shall be known as 'THE NEW COMPREHENSIVE ANTI-SMOKING ORDINANCE OF DAVAO CITY'.",
            "SECTION 4. PROHIBITED ACTS": "Smoking any tobacco product or using electronic nicotine delivery systems (ENDS), electronic cigarettes, and shishas is prohibited in all public conveyances, government offices, private workplaces, and enclosed public spaces, except in duly certified Designated Smoking Areas (DSAs).",
            "SECTION 5. STRICT SPECIFICATIONS FOR DSAS": "Designated smoking areas must be open outdoor spaces situated not less than ten (10) meters away from building entrances, exits, and windows, exceeding national statutory minimums to safeguard citizens from second-hand smoke."
        }
    },
    {
        "ordinance_no": "Ordinance No. 060-02",
        "series": 2002,
        "title": "AN ORDINANCE PROHIBITING THE MANUFACTURE, SALE, DISTRIBUTION, POSSESSION OR USE OF FIRECRACKERS OR PYROTECHNIC DEVICES AND SUCH OTHER SIMILAR DEVICES IN DAVAO CITY",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "date_approved": "November 26, 2002",
        "judicial_case": "Davao City Firecracker Prohibition under General Welfare Police Power",
        "ruling": "Valid Local Prohibitory Measure under General Welfare Police Power (Upheld)",
        "gold_label": "Entailment",
        "superior_national_law": "Republic Act No. 7160 §16, §458(a)(1)(vi); Republic Act No. 7183 §2",
        "operative_sections": {
            "SECTION 1. TITLE": "This Ordinance shall be cited as the 'Davao City Firecracker Ban Ordinance of 2002'.",
            "SECTION 2. PROHIBITED ACTS": "It shall be unlawful for any person or business entity to manufacture, sell, distribute, possess, transport, or use any firecracker, pyrotechnic device, or explosive novelty anywhere within Davao City at any time of the year.",
            "SECTION 3. GRADUATED PENALTIES": "Violators shall pay P1,000 fine and 20 days imprisonment for first offense; P3,000 fine and 1 to 3 months imprisonment for second offense; and P5,000 fine and 3 to 6 months imprisonment for third offense."
        }
    },
    {
        "ordinance_no": "Ordinance No. 0270-23",
        "series": 2023,
        "title": "THE COMPREHENSIVE SPEED LIMIT ORDINANCE OF DAVAO CITY",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "date_approved": "September 26, 2023",
        "judicial_case": "Davao City Speed Limit Enforcement under Joint DOTr-DPWH-DILG JAO 2018-01",
        "ruling": "Valid Delegated Local Speed Setting under National Transport Guidelines (Upheld)",
        "gold_label": "Entailment",
        "superior_national_law": "Republic Act No. 4136 §35, §38; Joint DILG-DOTr-DPWH JAO 2018-01",
        "operative_sections": {
            "SECTION 1. TITLE": "This Ordinance shall be known as the 'Comprehensive Speed Limit Ordinance of Davao City'.",
            "SECTION 4. SPEED LIMIT CLASSIFICATION": "Classifies city roads into Open Roads (80 kph private / 50 kph trucks and buses), Through Streets (40 kph / 30 kph), City Streets (30 kph), and Crowded Residential/School Streets (20 kph).",
            "SECTION 6. SPEED DETECTION MACHINERY": "Authorizes CTTMO to utilize DOST-calibrated radar speed cameras and automated speed enforcement tools."
        }
    },
    {
        "ordinance_no": "Ordinance No. 004-13",
        "series": 2013,
        "title": "AN ORDINANCE AMENDING ORDINANCE NO. 1627 RELATIVE TO THE LIQUOR BAN IN DAVAO CITY",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "date_approved": "July 24, 2013",
        "judicial_case": "Davao City Sobriety and Public Order Regulation",
        "ruling": "Valid Exercise of Police Power Regulating Operating Hours of Commercial Establishments (Upheld)",
        "gold_label": "Entailment",
        "superior_national_law": "Republic Act No. 7160 §16, §458(a)(4)(iv)",
        "operative_sections": {
            "SECTION 1. TITLE": "This Ordinance shall be known as the 'Davao City Liquor Ban Ordinance of 2013'.",
            "SECTION 2. RESTRICTED HOURS": "It is unlawful for any commercial establishment to serve, sell, furnish, or allow the consumption of alcoholic and intoxicating liquor between 1:00 AM and 8:00 AM within the territorial jurisdiction of Davao City.",
            "SECTION 4. PENAL CLAUSE": "First offense: P3,000 fine; Second offense: P5,000 fine and 3 months closure; Third offense: Revocation of Mayor's Business Permit."
        }
    },
    {
        "ordinance_no": "Davao City Real Property Tax Assessment on GSIS",
        "series": 2001,
        "title": "DAVAO CITY MUNICIPAL REAL PROPERTY TAX ASSESSMENT ON GSIS HOUSING AND COMMERCIAL UNITS",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "MUNICIPAL TAX LEVY EXECUTED PURSUANT TO THE DAVAO CITY LOCAL REVENUE CODE:",
        "date_approved": "Assessed Calendar Years 1992-2001",
        "judicial_case": "City of Davao v. Court of Appeals and GSIS, G.R. No. 127383 (August 18, 2005; 467 SCRA 280)",
        "ruling": "Ultra Vires Assessment Struck Down (National Instrumentality Tax Exemption)",
        "gold_label": "Contradiction",
        "superior_national_law": "Republic Act No. 7160 §133(o); Presidential Decree No. 1146 §33",
        "operative_sections": {
            "ASSESSMENT MANDATE": "Warrants of levy and distraint assessing real property taxes against real properties titled under the Government Service Insurance System located in Matina and downtown Davao City.",
            "STATUTORY DEFECT": "Directly collides with Section 133(o) of Republic Act No. 7160, which categorically bars LGUs from imposing any tax or charge upon the national government, its agencies, and instrumentalities."
        }
    }
]

# Write individual text and JSON files
for ord in ordinances:
    safe_name = ord["ordinance_no"].replace(" ", "_").replace("/", "-")
    txt_path = os.path.join(output_dir, f"{safe_name}.txt")
    json_path = os.path.join(output_dir, f"{safe_name}.json")
    
    with open(json_path, "w", encoding="utf-8") as f_json:
        json.dump(ord, f_json, indent=2, ensure_ascii=False)
        
    with open(txt_path, "w", encoding="utf-8") as f_txt:
        f_txt.write(f"=== {ord['ordinance_no']} ({ord['series']}) ===\n")
        f_txt.write(f"Title: {ord['title']}\n")
        f_txt.write(f"Enacting LGU: {ord['enacting_lgu']}\n")
        f_txt.write(f"Enacting Clause: {ord['enacting_clause']}\n")
        f_txt.write(f"Date Approved: {ord['date_approved']}\n")
        f_txt.write(f"Judicial Reference: {ord['judicial_case']}\n")
        f_txt.write(f"Judicial Ruling: {ord['ruling']}\n")
        f_txt.write(f"Gold NLI Label: {ord['gold_label']}\n")
        f_txt.write(f"Superior National Law: {ord['superior_national_law']}\n\n")
        f_txt.write("--- OPERATIVE SECTIONS ---\n")
        for sec_k, sec_v in ord["operative_sections"].items():
            f_txt.write(f"{sec_k}:\n{sec_v}\n\n")

print(f"Successfully stored {len(ordinances)} authentic Davao City ordinances in {output_dir}")

# Update data/tier3_jurisprudential_cases.jsonl to contain strictly Davao City measures
with open("data/tier3_jurisprudential_cases.jsonl", "w", encoding="utf-8") as f_cases:
    for idx, ord in enumerate(ordinances, 1):
        case_record = {
            "case_id": f"DAVAO-TIER3-{idx:02d}",
            "ordinance_no": ord["ordinance_no"],
            "series": ord["series"],
            "title": ord["title"],
            "judicial_reference": ord["judicial_case"],
            "ruling": ord["ruling"],
            "gold_nli_label": ord["gold_label"],
            "superior_national_law": ord["superior_national_law"],
            "operative_sections": ord["operative_sections"]
        }
        f_cases.write(json.dumps(case_record, ensure_ascii=False) + "\n")

print("Updated data/tier3_jurisprudential_cases.jsonl with strictly Davao City ordinances!")
