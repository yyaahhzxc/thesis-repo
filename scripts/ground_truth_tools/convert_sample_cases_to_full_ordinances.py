import json
from pathlib import Path

sample_cases_dir = Path("demo/sample_cases")
sample_cases_dir.mkdir(parents=True, exist_ok=True)

full_ordinances = [
    {
        "filename_prefix": "01_mosqueda_aerial_spraying_ban",
        "case_id": "DAVAO-TIER3-01",
        "case_name": "Mosqueda v. Pilipino Banana Growers & Exporters Association, Inc.",
        "docket_no": "G.R. Nos. 189185 & 189305 (August 16, 2016)",
        "ordinance_no": "Ordinance No. 0309-07",
        "title": "AN ORDINANCE BANNING AERIAL SPRAYING AS AN AGRICULTURAL PRACTICE IN ALL AGRICULTURAL ACTIVITIES BY ALL AGRICULTURAL ENTITIES IN DAVAO CITY",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "sections": [
            {"sec_num": 1, "sec_title": "TITLE", "text": "This Ordinance shall be known as 'An Ordinance Banning Aerial Spraying as an Agricultural Practice in all Agricultural Activities by all Agricultural Entities in Davao City'."},
            {"sec_num": 2, "sec_title": "POLICY", "text": "It is hereby declared the policy of the City of Davao to protect the health of its citizens and promote the ecological balance of the environment from hazardous agricultural pesticide drift."},
            {"sec_num": 3, "sec_title": "DEFINITION OF TERMS", "text": "Aerial Spraying refers to the application of agricultural chemical substances from an aircraft, airplane, or helicopter onto agricultural crops and plantations. Agricultural Entity refers to any natural or juridical person engaged in agricultural production."},
            {"sec_num": 4, "sec_title": "SCOPE", "text": "This Ordinance shall apply to all agricultural activities and all commercial plantations within the territorial jurisdiction of Davao City."},
            {"sec_num": 5, "sec_title": "BAN ON AERIAL SPRAYING", "text": "Aerial spraying shall be strictly prohibited in all agricultural activities in Davao City after a three (3) month transition period from the effectivity of this Ordinance."},
            {"sec_num": 6, "sec_title": "BUFFER ZONE", "text": "All agricultural entities must maintain a mandatory thirty (30) meter buffer zone within the boundaries of their plantations adjacent to residential zones, public thoroughfares, and water bodies."},
            {"sec_num": 7, "sec_title": "PENAL SANCTIONS", "text": "Any person or corporate officer found guilty of violating this Ordinance shall be penalized with a fine of Five Thousand Pesos (P5,000.00) or imprisonment not exceeding one (1) year, or both, at the discretion of the court."},
            {"sec_num": 8, "sec_title": "SEPARABILITY CLAUSE", "text": "If any provision of this Ordinance is declared invalid or unconstitutional, the remaining provisions not affected shall continue in full force."},
            {"sec_num": 9, "sec_title": "REPEALING CLAUSE", "text": "All ordinances, executive orders, and rules contrary to this enactment are repealed or modified accordingly."},
            {"sec_num": 10, "sec_title": "EFFECTIVITY", "text": "This Ordinance shall take effect thirty (30) days after publication in a newspaper of general circulation."}
        ]
    },
    {
        "filename_prefix": "02_evasco_billboard_regulation",
        "case_id": "DAVAO-TIER3-02",
        "case_name": "Hon. Leoncio Evasco, Jr. v. Alex P. Montañez",
        "docket_no": "G.R. No. 199172 (February 21, 2018)",
        "ordinance_no": "Ordinance No. 092-2000",
        "title": "AN ORDINANCE REGULATING THE CONSTRUCTION, REPAIR, RENOVATION, ERECTION, INSTALLATION AND MAINTENANCE OF OUTDOOR ADVERTISING MATERIALS AND STRUCTURES IN DAVAO CITY",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "sections": [
            {"sec_num": 1, "sec_title": "TITLE", "text": "This Ordinance shall be known as the 'Signage and Outdoor Advertising Ordinance of Davao City'."},
            {"sec_num": 2, "sec_title": "DECLARATION OF POLICY", "text": "It is hereby declared the policy of Davao City to regulate commercial signs and outdoor advertising to ensure public safety and preserve urban environmental aesthetics."},
            {"sec_num": 7, "sec_title": "BILLBOARDS AND SIGNAGES", "text": "Outdoor advertising signs and commercial billboards are strictly prohibited in residential zones. Free-standing billboards along public highways must maintain an unobstructed 150-meter line of sight and must be located at least 10 meters away from property lines abutting the road right-of-way."},
            {"sec_num": 8, "sec_title": "REGULATED SCENIC AREAS", "text": "Areas within two hundred (200) meters of scenic bridges, the Davao River, scenic vantage points of Mount Apo, and the city coastal shoreline are declared regulated areas where commercial advertising displays are restricted to preserve environmental aesthetics."},
            {"sec_num": 37, "sec_title": "SIGN PERMIT FEES", "text": "All commercial advertising structures must obtain an annual Sign Permit from the City Building Official and pay the corresponding regulatory inspection fees prescribed herein."},
            {"sec_num": 45, "sec_title": "REMOVAL OF ILLEGAL ADVERTISING MATERIALS", "text": "The City Engineer and Building Official are authorized to summarily dismantle and remove illegal, dilapidated, or hazardously situated outdoor advertising structures after serving thirty (30) days written notice of violation."},
            {"sec_num": 46, "sec_title": "SEPARABILITY CLAUSE", "text": "If any part of this Ordinance is declared invalid, the other provisions not affected shall remain in full force and effect."},
            {"sec_num": 47, "sec_title": "EFFECTIVITY", "text": "This Ordinance shall take effect immediately upon approval."}
        ]
    },
    {
        "filename_prefix": "03_arc_investors_holding_tax",
        "case_id": "DAVAO-TIER3-03",
        "case_name": "City of Davao and Tanjili v. ARC Investors, Inc.",
        "docket_no": "G.R. No. 249668 (July 13, 2022)",
        "ordinance_no": "Ordinance No. 158-05 §135",
        "title": "THE 2005 REVENUE CODE OF THE CITY OF DAVAO (LOCAL BUSINESS TAX ON HOLDING ENTITIES)",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "sections": [
            {"sec_num": 1, "sec_title": "TITLE", "text": "This Ordinance shall be known and cited as the '2005 Revenue Code of the City of Davao'."},
            {"sec_num": 2, "sec_title": "SCOPE AND APPLICATION", "text": "This Code shall govern the levy, assessment, and collection of all city taxes, fees, and other charges within the territorial jurisdiction of Davao City."},
            {"sec_num": 135, "sec_title": "TAX ON FINANCIAL INSTITUTIONS AND HOLDING CORPORATIONS", "text": "There is hereby levied a tax on banks, banking institutions, and holding entities receiving dividend income and investment interest, categorizing corporate holding firms as non-bank financial intermediaries subject to local business taxes."},
            {"sec_num": 136, "sec_title": "PAYMENT AND ASSESSMENT", "text": "The local business taxes imposed under this Chapter shall be payable for every calendar quarter within the first twenty (20) days of January, April, July, and October."},
            {"sec_num": 420, "sec_title": "SEPARABILITY CLAUSE", "text": "If any provision of this Code is held unconstitutional or invalid, other provisions not affected shall continue in full force."},
            {"sec_num": 421, "sec_title": "EFFECTIVITY", "text": "This Code shall take effect upon approval and publication as required by law."}
        ]
    },
    {
        "filename_prefix": "04_first_meridian_payment_under_protest",
        "case_id": "DAVAO-TIER3-04",
        "case_name": "City of Davao and Dureza v. First Meridian Development, Inc.",
        "docket_no": "G.R. No. 240078 (October 19, 2022)",
        "ordinance_no": "Ordinance No. 158-05 §423",
        "title": "THE 2005 REVENUE CODE OF THE CITY OF DAVAO (MANDATORY PAYMENT UNDER PROTEST)",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "sections": [
            {"sec_num": 1, "sec_title": "TITLE", "text": "This Ordinance shall be known and cited as the '2005 Revenue Code of the City of Davao'."},
            {"sec_num": 2, "sec_title": "ADMINISTRATIVE PROVISIONS", "text": "The administration and collection of city taxes shall be under the direct supervision of the City Treasurer."},
            {"sec_num": 423, "sec_title": "PAYMENT UNDER PROTEST", "text": "No protest against an assessment shall be entertained unless the taxpayer first pays under protest the tax assessed, stating the legal grounds within thirty (30) days from payment."},
            {"sec_num": 424, "sec_title": "APPEAL PROCEDURE", "text": "The City Treasurer shall decide the protest within sixty (60) days from receipt. The taxpayer may appeal an adverse decision to the court of competent jurisdiction within thirty (30) days."},
            {"sec_num": 425, "sec_title": "SEPARABILITY CLAUSE", "text": "If any part of this enactment is invalidated, all other parts shall remain in effect."},
            {"sec_num": 426, "sec_title": "EFFECTIVITY", "text": "This Ordinance shall take effect fifteen (15) days after its complete publication."}
        ]
    },
    {
        "filename_prefix": "05_davao_gsis_property_tax",
        "case_id": "DAVAO-TIER3-05",
        "case_name": "City of Davao v. Court of Appeals and GSIS",
        "docket_no": "G.R. No. 127383 (August 18, 2005)",
        "ordinance_no": "Davao City Real Property Tax Assessment on GSIS",
        "title": "DAVAO CITY MUNICIPAL REAL PROPERTY TAX ASSESSMENT ON GSIS PROPERTIES",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "sections": [
            {"sec_num": 1, "sec_title": "TITLE", "text": "This Measure establishes the Municipal Real Property Tax Assessment Mandate on Government-Owned Corporation Assets."},
            {"sec_num": 2, "sec_title": "ASSESSMENT MANDATE ON COMMERCIAL REALTY", "text": "Notices of assessment and warrants of levy are hereby issued imposing municipal real property taxes upon GSIS properties located in Matina and Ulas, Davao City, for outstanding municipal tax liabilities pursuant to the withdrawal of GOCC tax exemptions."},
            {"sec_num": 3, "sec_title": "LEVY AND REMEDIES", "text": "The City Treasurer is instructed to pursue all administrative remedies under the Local Government Code to enforce tax delinquencies against taxable properties."},
            {"sec_num": 4, "sec_title": "EFFECTIVITY", "text": "This Measure takes effect immediately upon passage."}
        ]
    },
    {
        "filename_prefix": "06_mining_ban_watershed",
        "case_id": "DAVAO-TIER3-06",
        "case_name": "Davao City Mining Ban and Panigan-Tamugan Watershed Dispute",
        "docket_no": "SP Resolution / May 2015 Mining Ban Ordinance",
        "ordinance_no": "Ordinance No. 0310-07 & 2015 Mining Ban Ordinance",
        "title": "THE DAVAO CITY WATERSHED PROTECTION AND MINING BAN ORDINANCE",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "sections": [
            {"sec_num": 1, "sec_title": "TITLE", "text": "This Ordinance shall be known as the 'Davao City Watershed Protection and Mining Ban Ordinance'."},
            {"sec_num": 2, "sec_title": "TOTAL MINING BAN", "text": "No mining operations of any nature, whether large-scale or small-scale, shall be permitted anywhere within the territorial jurisdiction of Davao City. The City Mayor shall refuse to issue business permits or Mayor's clearances to any entity holding national mineral agreements (MPSAs) from the national government."},
            {"sec_num": 3, "sec_title": "PROTECTION OF PANIGAN-TAMUGAN WATERSHED", "text": "The Panigan-Tamugan recharge basin is declared an environmentally critical zone closed to all industrial extraction, quarrying, and mineral exploration activities."},
            {"sec_num": 4, "sec_title": "PENAL SANCTIONS", "text": "Violators shall be penalized with a fine of Five Thousand Pesos (P5,000.00) or imprisonment for one (1) year, or both, plus revocation of municipal permits."},
            {"sec_num": 5, "sec_title": "SEPARABILITY AND EFFECTIVITY", "text": "This Ordinance shall take effect immediately upon enactment and publication."}
        ]
    },
    {
        "filename_prefix": "07_davao_anti_smoking_stricter_standard",
        "case_id": "DAVAO-TIER3-07",
        "case_name": "Davao City Comprehensive Anti-Smoking Ordinance vs. National Standards",
        "docket_no": "Promulgated as Ord. No. 0367-12 (May 31, 2013)",
        "ordinance_no": "Ordinance No. 0367-12",
        "title": "THE NEW COMPREHENSIVE ANTI-SMOKING ORDINANCE OF DAVAO CITY",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "sections": [
            {"sec_num": 1, "sec_title": "TITLE", "text": "This Ordinance shall be known as 'The New Comprehensive Anti-Smoking Ordinance of Davao City'."},
            {"sec_num": 2, "sec_title": "POLICY", "text": "It is declared the policy of Davao City to protect the health of its citizens, especially minors and workers, from exposure to secondhand tobacco smoke and aerosol."},
            {"sec_num": 4, "sec_title": "PROHIBITED ACTS", "text": "Smoking any tobacco product or using electronic nicotine delivery systems (ENDS), electronic cigarettes, and shishas is prohibited in all public conveyances, government offices, private workplaces, and enclosed public spaces, except in duly certified Designated Smoking Areas (DSAs)."},
            {"sec_num": 5, "sec_title": "STRICT SPECIFICATIONS FOR DSAS", "text": "Designated smoking areas must be open outdoor spaces situated not less than ten (10) meters away from building entrances, exits, and windows, exceeding national statutory minimums to safeguard citizens from second-hand smoke."},
            {"sec_num": 6, "sec_title": "PENAL SANCTIONS", "text": "First offense: fine of One Thousand Pesos (P1,000.00); Second offense: Two Thousand Pesos (P2,000.00); Third offense: Five Thousand Pesos (P5,000.00) or imprisonment not exceeding one (1) month."},
            {"sec_num": 7, "sec_title": "SEPARABILITY CLAUSE", "text": "If any provision is declared unconstitutional, other provisions shall remain valid."},
            {"sec_num": 8, "sec_title": "EFFECTIVITY", "text": "This Ordinance shall take effect fifteen (15) days after publication."}
        ]
    },
    {
        "filename_prefix": "08_davao_speed_limits_traffic_code",
        "case_id": "DAVAO-TIER3-08",
        "case_name": "Davao City Comprehensive Speed Limit Ordinance under Joint JAO 2018-01",
        "docket_no": "Promulgated as Ord. No. 0270-23 (October 2023)",
        "ordinance_no": "Ordinance No. 0270-23",
        "title": "THE COMPREHENSIVE SPEED LIMIT ORDINANCE OF DAVAO CITY",
        "enacting_lgu": "City of Davao",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED, THAT:",
        "sections": [
            {"sec_num": 1, "sec_title": "TITLE", "text": "This Ordinance shall be known as the 'Comprehensive Speed Limit Ordinance of Davao City'."},
            {"sec_num": 2, "sec_title": "DECLARATION OF POLICY", "text": "It is the policy of Davao City to safeguard public safety and reduce traffic-related fatalities through reasonable and prudent road speed regulation."},
            {"sec_num": 4, "sec_title": "SPEED LIMIT CLASSIFICATION", "text": "Classifies city roads into Open Roads (80 kph private / 50 kph trucks and buses), Through Streets (40 kph / 30 kph), City Streets (30 kph), and Crowded Residential/School Streets (20 kph)."},
            {"sec_num": 6, "sec_title": "SPEED DETECTION MACHINERY", "text": "Authorizes CTTMO to utilize DOST-calibrated radar speed cameras and automated speed enforcement tools."},
            {"sec_num": 7, "sec_title": "PENAL SANCTIONS", "text": "Violators shall be penalized with fines ranging from One Thousand Pesos (P1,000.00) to Five Thousand Pesos (P5,000.00) or driver license referral."},
            {"sec_num": 8, "sec_title": "SEPARABILITY AND REPEALING", "text": "All prior speed regulations contrary hereto are repealed or modified accordingly."},
            {"sec_num": 9, "sec_title": "EFFECTIVITY", "text": "This Ordinance shall take effect thirty (30) days following publication."}
        ]
    },
    {
        "filename_prefix": "09_magtajas_casino_preemption",
        "case_id": "SC-PHIL-09",
        "case_name": "Magtajas v. Pryce Properties Corp. and PAGCOR",
        "docket_no": "G.R. No. 111097 (July 20, 1994; 234 SCRA 255)",
        "ordinance_no": "Cagayan de Oro Ord. No. 3353 & Ord. No. 3375-93",
        "title": "AN ORDINANCE PROHIBITING THE OPERATION OF CASINOS IN THE CITY OF CAGAYAN DE ORO",
        "enacting_lgu": "City of Cagayan de Oro",
        "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF CAGAYAN DE ORO, IN SESSION ASSEMBLED, THAT:",
        "sections": [
            {"sec_num": 1, "sec_title": "TITLE", "text": "This Ordinance shall be known as the 'Anti-Casino Ordinance of the City of Cagayan de Oro'."},
            {"sec_num": 2, "sec_title": "DECLARATION OF MORAL POLICY", "text": "It is hereby declared the policy of the City to protect the morality and public welfare of its citizens from the pernicious influences of legalized gambling."},
            {"sec_num": 3, "sec_title": "PROHIBITION OF CASINOS", "text": "The opening, establishment, and operation of casinos and all forms of gambling are strictly prohibited and banned within the territorial jurisdiction of the City of Cagayan de Oro."},
            {"sec_num": 4, "sec_title": "PENAL SANCTIONS", "text": "Any person or corporate entity operating a casino shall be punished by a fine of Five Thousand Pesos (P5,000.00) and imprisonment of one (1) year, plus immediate closure."},
            {"sec_num": 5, "sec_title": "SEPARABILITY CLAUSE", "text": "If any provision is declared invalid, the remainder shall continue in effect."},
            {"sec_num": 6, "sec_title": "REPEALING CLAUSE", "text": "All resolutions and ordinances inconsistent with this enactment are repealed."},
            {"sec_num": 7, "sec_title": "EFFECTIVITY", "text": "This Ordinance shall take effect immediately upon approval."}
        ]
    },
    {
        "filename_prefix": "10_city_of_manila_laguio_due_process",
        "case_id": "SC-PHIL-10",
        "case_name": "City of Manila v. Laguio, Jr.",
        "docket_no": "G.R. No. 118127 (April 12, 2005; 455 SCRA 308)",
        "ordinance_no": "Manila Ordinance No. 7783",
        "title": "AN ORDINANCE PROHIBITING THE ESTABLISHMENT OR OPERATION OF MOTELS, INNS, AND KARAOKE BARS IN ERMITA-MALATE",
        "enacting_lgu": "City of Manila",
        "enacting_clause": "BE IT ORDAINED BY THE CITY COUNCIL OF MANILA, IN SESSION ASSEMBLED, THAT:",
        "sections": [
            {"sec_num": 1, "sec_title": "TITLE", "text": "This Ordinance shall be known as the 'Ermita-Malate Hospitality Zoning and Moral Rehabilitation Ordinance'."},
            {"sec_num": 2, "sec_title": "DECLARATION OF URBAN POLICY", "text": "It is declared the policy of the City of Manila to revitalize the tourist district of Ermita-Malate and eliminate venues associated with illicit commercial activities."},
            {"sec_num": 3, "sec_title": "CLOSURE OF HOSPITALITY ESTABLISHMENTS", "text": "Prohibits the establishment or operation of motels, inns, and karaoke bars in the Ermita-Malate district, ordering their permanent closure or relocation within three (3) months without just compensation."},
            {"sec_num": 4, "sec_title": "REVOCATION OF BUSINESS LICENSES", "text": "The City Mayor and Bureau of Permits are directed to cancel all business permits previously issued to motels, inns, massage parlors, and sauna baths in the covered area."},
            {"sec_num": 5, "sec_title": "PENAL SANCTIONS", "text": "Failure to comply shall result in a fine of Five Thousand Pesos (P5,000.00) and summary eviction and physical sealing of premises."},
            {"sec_num": 6, "sec_title": "SEPARABILITY CLAUSE", "text": "The provisions of this Ordinance are separable; invalidity of any provision shall not affect the remaining parts."},
            {"sec_num": 7, "sec_title": "EFFECTIVITY", "text": "This Ordinance shall take effect immediately upon enactment."}
        ]
    },
    {
        "filename_prefix": "11_batangas_catv_cable_regulation",
        "case_id": "SC-PHIL-11",
        "case_name": "Batangas CATV, Inc. v. Court of Appeals",
        "docket_no": "G.R. No. 138810 (September 29, 2004; 439 SCRA 326)",
        "ordinance_no": "Batangas SP Resolution No. 210, Series of 1993",
        "title": "RESOLUTION REGULATING THE CABLE TELEVISION FRANCHISE AND SUBSCRIBER RATES OF BATANGAS CATV, INC.",
        "enacting_lgu": "City of Batangas",
        "enacting_clause": "BE IT RESOLVED BY THE SANGGUNIANG PANLUNGSOD OF BATANGAS CITY, IN SESSION ASSEMBLED, THAT:",
        "sections": [
            {"sec_num": 1, "sec_title": "TITLE", "text": "This Resolution shall be known as the 'Batangas City Cable Television Regulatory Resolution of 1993'."},
            {"sec_num": 2, "sec_title": "DECLARATION OF CONSUMER POLICY", "text": "The City declares its duty to protect city residents from excessive monthly charges imposed by commercial telecommunications providers."},
            {"sec_num": 3, "sec_title": "CABLE RATE REGULATION", "text": "The Sangguniang Panlungsod assumes authority to fix, regulate, and adjust subscriber rates and channel programming charges for commercial cable television services."},
            {"sec_num": 4, "sec_title": "MANDATORY RATE SCHEDULE", "text": "All cable TV concessionaires must submit rate adjustment applications to the City Council for public hearing and approval prior to implementation."},
            {"sec_num": 5, "sec_title": "PENALTIES FOR NON-COMPLIANCE", "text": "Unauthorized rate increases shall be subject to a fine of Five Thousand Pesos (P5,000.00) per month of unauthorized collection and revocation of Mayor's Permit."},
            {"sec_num": 6, "sec_title": "SEPARABILITY AND EFFECTIVITY", "text": "This Resolution shall take effect upon approval."}
        ]
    }
]

for ord in full_ordinances:
    prefix = ord["filename_prefix"]
    json_path = sample_cases_dir / f"{prefix}.json"
    txt_path = sample_cases_dir / f"{prefix}.txt"
    
    # 1. Write full structured JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(ord, f, indent=2, ensure_ascii=False)
        
    # 2. Write clean full TXT format
    lines = [
        f"=== {ord['ordinance_no']} ===",
        f"Title: {ord['title']}",
        f"Enacting LGU: {ord['enacting_lgu']}",
        f"Judicial Reference: {ord['case_name']} ({ord['docket_no']})",
        "",
        ord["enacting_clause"],
        ""
    ]
    for s in ord["sections"]:
        lines.append(f"SECTION {s['sec_num']}. {s['sec_title']} - {s['text']}\n")
        
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    print(f"Created: {json_path.name} ({len(ord['sections'])} sections) and {txt_path.name}")

print("\nSuccessfully updated all 11 sample cases to complete multi-section ordinances!")
