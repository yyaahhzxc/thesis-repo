"""
scripts/tier2_drafts_data_part2.py
==================================
Contains authentic, natural legislative drafts (Drafts 4, 5, 6, and 7)
modeled directly after real Sangguniang Panlungsod regulatory ordinances
from the Davao City corpus (e.g., Ord. 0270-23, Ord. 0331-23, Ord. 0258-23,
Ord. 0500-21, Ord. 0539-24).

Eliminates unnatural filler and artificial jargon; preserves authentic
municipal phrasing, real administrative bodies, and genuine statutory
preemption defect targets.
"""

def get_draft_04():
    return {
        "doc_id": "DRAFT-ORD-2026-04",
        "title": "AN ORDINANCE REGULATING THE OPERATION OF ELECTRIC BICYCLES, ELECTRIC SCOOTERS, AND LIGHT CONVEYANCES, PRESCRIBING SPEED LIMITS AND SAFETY STANDARDS, AND PROVIDING PENALTIES FOR VIOLATIONS THEREOF IN THE CITY OF DAVAO",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-04, Series of 2026",
        "committee": "Committee on Transportation and Communication, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Electric Mobility and Light Vehicle Regulation Ordinance of Davao City'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "Pursuant to Section 16 of Republic Act No. 7160 (The Local Government Code of 1991), the City Government of Davao is authorized to regulate traffic and the use of streets to protect public safety and general welfare.\n\nIt is hereby declared the policy of the City of Davao to promote active and sustainable transportation by providing guidelines for the safe operation of electric bicycles, e-scooters, and light mobility vehicles, preventing road crashes, and protecting pedestrians and motorists across city streets.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16",
                "legal_rationale": "Valid exercise of local police powers regulating road traffic."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "As used in this Ordinance, the following terms shall mean:\n\n(a) Electric Bicycle (E-Bike) - refers to any two- or three-wheeled vehicle equipped with an electric motor and functional pedals;\n\n(b) Electric Scooter (E-Scooter) - refers to a stand-up or sit-down light two-wheeled vehicle powered by an electric motor;\n\n(c) City Streets - refers to roads and streets within Davao City not designated as national or provincial highways;\n\n(d) Dedicated Bicycle Lanes - refers to designated lanes on public roads reserved for bicycles and light mobility conveyances;\n\n(e) CTTMO - refers to the City Transport and Traffic Management Office of Davao City.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitional section modeled after Ord. 0270-23."
            },
            {
                "sec_num": 4,
                "sec_title": "SCOPE AND COVERAGE",
                "text": "This Ordinance shall apply to all users, riders, and operators of electric bicycles, electric scooters, and light electric conveyances driven on public streets, lanes, and thoroughfares within Davao City.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard coverage clause."
            },
            {
                "sec_num": 5,
                "sec_title": "SAFETY REQUIREMENTS AND PROTECTIVE GEAR",
                "text": "All riders and operators of electric bicycles and e-scooters traversing public roads in Davao City shall observe the following safety requirements:\n\n(a) Mandatory wearing of protective bicycle or motorcycle safety helmets at all times;\n\n(b) Equipping vehicles with operational white front headlights and red rear reflectors or tail lights during nighttime operation from 6:00 PM to 6:00 AM;\n\n(c) Installation of functional mechanical brakes and an audible bell or horn;\n\n(d) Prohibition against carrying passengers beyond the designed manufacturer capacity of the vehicle.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(5)(v)",
                "legal_rationale": "Harmonious local safety standards under municipal traffic powers."
            },
            {
                "sec_num": 6,
                "sec_title": "MAXIMUM SPEED LIMITS ON MAJOR THOROUGHFARES AND HIGHWAYS",
                "text": "To ensure the safety of pedestrians and light vehicle commuters, the maximum allowable speed for all motor vehicles and electric conveyances traversing national highways within Davao City, including Daang Maharlika and the Davao-Cotabato Highway, shall not exceed fifteen (15) kilometers per hour.\n\nAny driver or operator exceeding this uniform fifteen (15) kilometer per hour limit on any national highway within the city shall be cited for reckless driving and penalized accordingly.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 4136 §35; Republic Act No. 4136 §38; Joint Memorandum Circular JAO 2018-01",
                "legal_rationale": "Directly contradicts Republic Act No. 4136 §§35 and 38 (The Land Transportation and Traffic Code) and DOTr-DPWH-DILG Joint Memorandum Circular (JAO 2018-01). National laws establish higher speed classifications for national highways and restrict local governments from imposing blanket 15 km/h restrictions on national highways under the Magtajas preemption doctrine."
            },
            {
                "sec_num": 7,
                "sec_title": "USE OF DESIGNATED BICYCLE LANES",
                "text": "Operators of electric bicycles and e-scooters shall strictly utilize designated bicycle lanes wherever such lanes have been demarcated by the City Government.\n\nWhere no dedicated bike lane exists, light vehicles shall operate along the rightmost lane of the roadway and shall yield the right-of-way to pedestrians crossing at intersections and marked pedestrian lanes.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(5)(vi)",
                "legal_rationale": "Valid exercise of local traffic management powers."
            },
            {
                "sec_num": 8,
                "sec_title": "ENFORCEMENT AND IMPLEMENTATION",
                "text": "The City Transport and Traffic Management Office (CTTMO), in coordination with the Traffic Enforcement Unit of the Davao City Police Office (DCPO), shall be the lead enforcement agency of this Ordinance.\n\nDeputized traffic enforcement personnel are authorized to issue City Traffic Citation Tickets (CTCT) to any rider or operator violating the provisions of this Ordinance.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard enforcement clause assigning duties to CTTMO and DCPO."
            },
            {
                "sec_num": 9,
                "sec_title": "NO-CONTEST ADMINISTRATIVE SETTLEMENT",
                "text": "Any person issued a citation ticket for violation of Section 5 or Section 7 who does not wish to contest the citation may avail of the No-Contest provision by paying an administrative fine to the City Treasurer within seventy-two (72) hours:\n\n(a) First Offense: Three Hundred Pesos (Php 300.00);\n\n(b) Second Offense: Five Hundred Pesos (Php 500.00);\n\n(c) Third Offense: One Thousand Pesos (Php 1,000.00).",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458",
                "legal_rationale": "Valid administrative compromise procedure modeled after Ord. 0270-23."
            },
            {
                "sec_num": 10,
                "sec_title": "PENALTIES",
                "text": "Any person who violates the provisions of this Ordinance and fails to avail of administrative settlement shall, upon conviction before a court of competent jurisdiction, be penalized by a fine of One Thousand Pesos (Php 1,000.00) for the first offense, Three Thousand Pesos (Php 3,000.00) for the second offense, and Five Thousand Pesos (Php 5,000.00) or imprisonment of up to thirty (30) days for subsequent offenses.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Complies strictly with statutory penalty ceilings under RA 7160 §458."
            },
            {
                "sec_num": 11,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any provision of this Ordinance is declared unconstitutional or invalid, the other provisions not affected thereby shall remain in full force and effect.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 12,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect fifteen (15) days after its complete publication in a newspaper of local circulation in Davao City.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    }


def get_draft_05():
    return {
        "doc_id": "DRAFT-ORD-2026-05",
        "title": "AN ORDINANCE PROMOTING STABILITY OF FOOD COMMODITY PRICES, PRESCRIBING MARKET MONITORING PROCEDURES IN PUBLIC AND PRIVATE MARKETS, PROHIBITING HOARDING, AND PROVIDING PENALTIES FOR VIOLATIONS THEREOF IN THE CITY OF DAVAO",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-05, Series of 2026",
        "committee": "Committee on Trade, Commerce and Industry, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Basic Food Commodities and Price Monitoring Ordinance of Davao City'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "Under Section 16 of Republic Act No. 7160 (The Local Government Code of 1991), local government units are authorized to protect public health and safety and promote economic prosperity and general welfare.\n\nIt is the policy of the City Government of Davao to ensure the constant availability of basic food necessities and prime commodities at fair prices, protect consumers from unfair trading practices, and prevent hoarding and artificial price manipulation in public markets and retail establishments throughout the city.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16",
                "legal_rationale": "Valid exercise of general welfare powers under RA 7160 §16."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "As used in this Ordinance, the following terms shall mean:\n\n(a) Basic Necessities - refers to essential food items including rice, corn, fresh milk, fresh eggs, pork, beef, poultry meat, fresh vegetables, root crops, and cooking oil;\n\n(b) Price Gouging - refers to the act of selling basic food necessities at prices significantly higher than the prevailing market price without justifiable economic reason;\n\n(c) Hoarding - refers to the undue accumulation and holding back of basic food items from commercial channels of trade to create an artificial shortage and hike prices;\n\n(d) Public Market - refers to city-owned public markets including Bankerohan, Agdao, Calinan, and Toril, as well as privately operated wet markets in Davao City;\n\n(e) LPCC - refers to the Local Price Coordinating Council of Davao City.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitions modeled after Ord. 0823-21 and national price monitoring statutes."
            },
            {
                "sec_num": 4,
                "sec_title": "SCOPE AND COVERAGE",
                "text": "This Ordinance shall apply to all public and private wet markets, supermarkets, grocery stores, grain wholesalers, meat retailers, and food vendors operating within the territorial jurisdiction of Davao City.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard scope and coverage clause."
            },
            {
                "sec_num": 5,
                "sec_title": "PRICE MONITORING AND DISPLAY OF PRICE TAGS",
                "text": "All retailers, market vendors, and commercial establishments selling basic food commodities shall clearly display price tags or price boards on all goods offered for sale.\n\nPrice tags must be written in legible characters indicating the price per kilogram or standard unit of measure, and goods shall not be sold at prices higher than those indicated on the price tag.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7394 §81",
                "legal_rationale": "Harmonious local consumer protection standard enforcing the Consumer Act (RA 7394)."
            },
            {
                "sec_num": 6,
                "sec_title": "PROHIBITION OF HOARDING AND ARTIFICIAL SHORTAGES",
                "text": "No wholesale dealer, distributor, or market vendor shall hoard, conceal, or withhold basic food necessities from the market, or collude with other traders to restrict supply and artificially inflate prevailing retail prices in the City of Davao.\n\nAny establishment found possessing hoarded basic commodities shall be reported immediately to the City Mayor and the Department of Trade and Industry (DTI).",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7581 §5",
                "legal_rationale": "Harmonious local anti-hoarding rule aligned with the Price Act (RA 7581)."
            },
            {
                "sec_num": 7,
                "sec_title": "MANDATORY CEILING PRICES ON BASIC COMMODITIES",
                "text": "Whenever prevailing market retail prices of basic necessities in Davao City experience sudden price increases or market volatility, the City Mayor, upon recommendation of the Local Price Coordinating Council (LPCC), is hereby authorized to establish, fix, and enforce mandatory maximum ceiling prices across all public markets, supermarkets, and retail stores in Davao City.\n\nAny vendor or merchant who sells basic food items above the municipal ceiling prices fixed by the City Mayor shall be subject to immediate administrative closure and the penalties provided in this Ordinance.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7581 §6; Republic Act No. 7581 §7",
                "legal_rationale": "Directly contradicts Republic Act No. 7581 §§6 and 7 (The Price Act). The statutory power to declare price ceilings and fix maximum prices on basic necessities is exclusively vested by national law in the President of the Philippines upon recommendation of the National Price Coordinating Council. Local government units have no unilateral power to fix price ceilings on basic necessities under the Magtajas preemption doctrine."
            },
            {
                "sec_num": 8,
                "sec_title": "LOCAL PRICE COORDINATING COUNCIL FUNCTIONS",
                "text": "The Local Price Coordinating Council (LPCC) of Davao City, chaired by the City Mayor and co-chaired by the DTI Provincial Director, shall conduct regular weekly market price monitoring across all major trading centers in Davao City.\n\nThe LPCC shall publish weekly Prevailing Price Bulletins to guide consumers and ensure transparent market operations.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard local administrative council functions under national price monitoring guidelines."
            },
            {
                "sec_num": 9,
                "sec_title": "TESTING AND CALIBRATION OF WEIGHING SCALES",
                "text": "All weighing scales used in public and private markets shall be inspected, tested, and sealed annually by the City Treasurer's Office.\n\nThe use of unsealed, defective, or tampered weighing scales is strictly prohibited. The City Economic Enterprise Office shall maintain 'Timbangan ng Bayan' weighing stations in all public markets for consumer verification.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §148; Republic Act No. 7394 §62",
                "legal_rationale": "Valid municipal regulation of weights and measures under RA 7160."
            },
            {
                "sec_num": 10,
                "sec_title": "NOTICE OF VIOLATION",
                "text": "Any vendor found selling without price tags or using uncalibrated scales shall be issued a Notice of Violation by the City Treasurer or market administrator, directing immediate correction.\n\nFailure to correct the infraction within forty-eight (48) hours shall result in confiscation of the defective scale and formal administrative sanctions.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard administrative warning procedure."
            },
            {
                "sec_num": 11,
                "sec_title": "PENALTIES",
                "text": "Any person, merchant, or establishment who violates the provisions of this Ordinance shall, upon conviction, be punished by a fine of One Thousand Pesos (Php 1,000.00) for the first offense; Three Thousand Pesos (Php 3,000.00) for the second offense; and Five Thousand Pesos (Php 5,000.00) or imprisonment of up to six (6) months, or both, for the third offense.\n\nIn addition, the market stall award or Mayor's Business Permit may be revoked for repeated violations.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Complies strictly with statutory penalty ceilings under RA 7160 §458."
            },
            {
                "sec_num": 12,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any section or part of this Ordinance is held unconstitutional or invalid, other sections or provisions hereof not affected thereby shall continue in full force and effect.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 13,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect fifteen (15) days after its complete publication in a newspaper of local circulation in Davao City.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    }


def get_draft_06():
    return {
        "doc_id": "DRAFT-ORD-2026-06",
        "title": "AN ORDINANCE REQUIRING THE INSTALLATION OF CLOSED-CIRCUIT TELEVISION (CCTV) SYSTEMS IN COMMERCIAL AND BUSINESS ESTABLISHMENTS, PRESCRIBING SECURITY ARCHIVING STANDARDS, AND PROVIDING PENALTIES FOR VIOLATIONS THEREOF IN THE CITY OF DAVAO",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-04, Series of 2026",
        "committee": "Committee on Peace and Public Safety, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Enhanced Commercial CCTV Surveillance and Security Records Ordinance of Davao City'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal title clause modeled after Ord. 0331-23."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "Pursuant to Section 16 of Republic Act No. 7160 (The Local Government Code of 1991), the City Government of Davao shall exercise powers essential to the maintenance of peace and order, the protection of life and property, and the promotion of public safety.\n\nIt is hereby declared the policy of the City of Davao to require the installation and maintenance of operational CCTV systems in commercial establishments to assist law enforcement agencies in crime prevention and investigation, while maintaining appropriate standards for the security and protection of recorded information.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16",
                "legal_rationale": "Valid exercise of general welfare powers under RA 7160 §16 modeled after Ord. 0331-23 §2."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "For purposes of this Ordinance, the following terms shall mean:\n\n(a) Closed-Circuit Television (CCTV) System - refers to a video surveillance system in which signals are transmitted to monitors and recording devices within a closed network;\n\n(b) Commercial Establishment - refers to banks, shopping malls, supermarkets, hotels, restaurants, bars, pawnshops, and business establishments operating in Davao City;\n\n(c) Public and Common Areas - refers to entry and exit doors, lobbies, parking areas, and transaction counters accessible to the general public;\n\n(d) PSSO - refers to the Public Safety and Security Office of the City Government of Davao.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitions modeled after Ord. 0331-23 §3."
            },
            {
                "sec_num": 4,
                "sec_title": "COVERAGE",
                "text": "This Ordinance shall apply to all commercial, industrial, and financial establishments operating within Davao City with capital investments of more than One Million Pesos (Php 1,000,000.00), including banks, money changers, supermarkets, convenience stores, and hotels.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard coverage clause modeled after Ord. 0331-23."
            },
            {
                "sec_num": 5,
                "sec_title": "MANDATORY CCTV INSTALLATION AND MINIMUM SPECIFICATIONS",
                "text": "All covered commercial establishments shall install, operate, and maintain CCTV cameras covering all public entry and exit points, cash transaction counters, and parking facilities.\n\nCCTV systems must possess sufficient image resolution to clearly identify individuals and vehicle license plates, equipped with continuous time and date stamping, and backed up with an uninterrupted power supply (UPS).",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(iv)",
                "legal_rationale": "Valid municipal regulation of commercial establishment safety devices."
            },
            {
                "sec_num": 6,
                "sec_title": "NOTICE OF CCTV SURVEILLANCE",
                "text": "Covered establishments shall post conspicuous signage at all entrance doors informing the public that the premises are under 24-hour video surveillance.\n\nSigns must be clearly visible and legible to all entering customers and visitors.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 10173 §11",
                "legal_rationale": "Harmonious local transparency requirement complying with the Data Privacy Act."
            },
            {
                "sec_num": 7,
                "sec_title": "CONFIDENTIALITY AND ACCESS TO FOOTAGE",
                "text": "CCTV recordings shall be treated as confidential and shall not be released, viewed, or published except upon lawful court order, formal subpoena, or official written request by law enforcement authorities conducting a criminal investigation.\n\nUnauthorized disclosure or publication of footage on social media or public platforms is strictly prohibited.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 10173 §12",
                "legal_rationale": "Harmonious local privacy rule protecting data confidentiality."
            },
            {
                "sec_num": 8,
                "sec_title": "RECORD RETENTION AND ARCHIVING",
                "text": "All captured CCTV recordings, video footage, and associated facial recognition logs shall be preserved and retained indefinitely in secure digital archives for public safety and crime investigation purposes.\n\nNo commercial establishment or system administrator shall delete, alter, or purge any stored video footage or facial logs upon the request of any private individual or data subject, in order to protect the integrity of the public safety archive.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 10173 §11; Republic Act No. 10173 §16",
                "legal_rationale": "Directly violates Sections 11 and 16 of Republic Act No. 10173 (The Data Privacy Act of 2012). National law establishes that personal data shall only be retained for as long as necessary for the purpose, and grants data subjects the statutory right to request erasure or blocking of personal information upon justifiable grounds. Blanket perpetual retention and prohibition of deletion violate national privacy statutes under the Magtajas doctrine."
            },
            {
                "sec_num": 9,
                "sec_title": "INSPECTION AND COMPLIANCE VERIFICATION",
                "text": "The Public Safety and Security Office (PSSO), in coordination with the Business Bureau, shall verify CCTV compliance during annual business permit application and renewal inspections.\n\nEstablishments that comply with all technical specifications shall be issued a CCTV Compliance Certificate.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard inspection procedure modeled after Ord. 0331-23."
            },
            {
                "sec_num": 10,
                "sec_title": "NOTICE OF DEFICIENCY",
                "text": "Establishments found with defective, non-operational, or missing CCTV cameras shall be issued a Notice of Deficiency by the PSSO and given thirty (30) calendar days to install or repair the required equipment.\n\nFailure to comply within the grace period shall result in the suspension of the establishment's Mayor's Business Permit.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard administrative compliance notice clause."
            },
            {
                "sec_num": 11,
                "sec_title": "PENALTIES",
                "text": "Any establishment or person violating this Ordinance shall, upon conviction, be penalized as follows:\n\n(a) First Offense: A fine of One Thousand Pesos (Php 1,000.00);\n\n(b) Second Offense: A fine of Three Thousand Pesos (Php 3,000.00);\n\n(c) Third and Subsequent Offenses: A fine of Five Thousand Pesos (Php 5,000.00) and revocation of Mayor's Business Permit until full compliance is certified.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Complies strictly with statutory penalty ceilings under RA 7160 §458."
            },
            {
                "sec_num": 12,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any provision of this Ordinance is declared invalid or unconstitutional, the other provisions not affected thereby shall continue in full force and effect.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 13,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect fifteen (15) days after its complete publication in a newspaper of general circulation in Davao City.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    }


def get_draft_07():
    return {
        "doc_id": "DRAFT-ORD-2026-07",
        "title": "AN ORDINANCE REGULATING WASTE DISCHARGE AND ENVIRONMENTAL SANITATION IN COASTAL WATERS, PORT WHARVES, AND DOCKING FACILITIES, PRESCRIBING PORT SANITATION STANDARDS, AND PROVIDING PENALTIES FOR VIOLATIONS THEREOF IN THE CITY OF DAVAO",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-07, Series of 2026",
        "committee": "Committee on Environment and Natural Resources, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Coastal Port Sanitation and Marine Pollution Prevention Ordinance of Davao City'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "Under Section 16 of Republic Act No. 7160 (The Local Government Code of 1991), local government units shall enhance the right of the people to a balanced ecology and protect the environment within their territorial boundaries.\n\nIt is hereby declared the policy of the City Government of Davao to maintain clean coastal waters, prevent marine pollution, and regulate the disposal of waste from vessels and port docking facilities along the shores and wharves of Davao City.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16",
                "legal_rationale": "Valid exercise of general welfare powers under RA 7160 §16."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "As used in this Ordinance, the following terms shall mean:\n\n(a) Coastal Waters - refers to the municipal waters, foreshore areas, and marine waters within the territorial jurisdiction of Davao City;\n\n(b) Commercial Vessel - refers to motorized cargo ships, passenger vessels, tugboats, and commercial fishing vessels docking in city ports;\n\n(c) Bilge Water - refers to water that collects in the lowest compartment of a ship's hull, frequently containing oil and chemical residues;\n\n(d) Port Wharves - refers to Santa Ana Wharf, Sasa Port, and private docking wharves operating in Davao City;\n\n(e) City ENRO - refers to the City Environment and Natural Resources Office.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitions modeled after Ord. 0539-24 and Ord. 0500-21."
            },
            {
                "sec_num": 4,
                "sec_title": "PROHIBITION OF BILGE WATER AND UNTREATED WASTE DISCHARGE",
                "text": "No commercial vessel, motorboat, barge, or watercraft shall pump, discharge, or dump untreated bilge water, dirty engine oils, sewage, or garbage into the coastal waters, foreshore zones, or harbor waters of Davao City.\n\nAll vessels docked at city wharves must utilize approved shore reception facilities or private waste haulers accredited by the City ENRO for bilge water disposal.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(vi); Presidential Decree No. 979 §4",
                "legal_rationale": "Harmonious local environmental sanitation standard prohibiting water pollution."
            },
            {
                "sec_num": 5,
                "sec_title": "PORT FACILITY WASTE RECEPTACLES AND RECEPTION",
                "text": "All operators of public and private port wharves, landing stages, and ferry terminals shall provide segregated waste collection bins for biodegradable, recyclable, and hazardous waste generated by docking vessels and passengers.\n\nPort operators shall maintain regular collection schedules with City ENRO solid waste collection personnel to prevent trash accumulation.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 9003 §32",
                "legal_rationale": "Harmonious local solid waste management rule under RA 9003."
            },
            {
                "sec_num": 6,
                "sec_title": "MANDATORY HARBOR SANITATION CLEARANCE",
                "text": "Commercial vessels berthing at city wharves for more than twenty-four (24) hours must secure a Harbor Sanitation Clearance from the City ENRO prior to departure, certifying that no illegal discharge of waste occurred during their stay.\n\nA reasonable inspection fee of Five Hundred Pesos (Php 500.00) shall be collected by the City Treasurer for each sanitation inspection.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(3)(iv)",
                "legal_rationale": "Valid municipal inspection and regulatory fee authority."
            },
            {
                "sec_num": 7,
                "sec_title": "IMPLEMENTING AND MONITORING AGENCIES",
                "text": "The City ENRO, in coordination with the Philippine Coast Guard (Coast Guard Station Davao), the PNP Regional Maritime Unit XI, and the City Legal Office, shall be responsible for enforcing the provisions of this Ordinance.\n\nAuthorized inspectors may board vessels docked at wharves to inspect waste storage logs and ensure compliance with environmental regulations.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard institutional coordination clause modeled after Ord. 0539-24."
            },
            {
                "sec_num": 8,
                "sec_title": "SPECIAL SANCTIONS ON COMMERCIAL VESSELS",
                "text": "Any commercial cargo vessel, passenger vessel, or motorized watercraft found discharging untreated bilge water, dirty ballast, or solid waste into the coastal waters, wharves, or docking facilities of Davao City shall be assessed an administrative fine of Fifty Thousand Pesos (Php 50,000.00) per day of continued violation.\n\nThe City Government, through the City Legal Office and port authorities, is hereby authorized to summarily impound and attach the vessel until all assessed fines and clean-up costs are fully paid.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii); Republic Act No. 10863 §1412",
                "legal_rationale": "Directly violates Section 458(a)(1)(iii) of Republic Act No. 7160, which limits municipal fines strictly to P5,000.00, and Republic Act No. 10863 (Customs Modernization and Tariff Act) and maritime admiralty law. Summary administrative attachment, impoundment, and multi-thousand daily fines on commercial vessels exceed municipal authority and usurp national maritime and customs jurisdiction under the Magtajas preemption doctrine."
            },
            {
                "sec_num": 9,
                "sec_title": "CLEAN-UP AND REMEDIATION RESPONSIBILITY",
                "text": "In addition to administrative penalties, the owner or operator of any vessel that discharges oil, bilge, or hazardous pollutants shall be solely responsible for the immediate containment and clean-up of the spilled materials at their own expense.\n\nFailure to perform clean-up operations within twelve (12) hours shall authorize the City to hire emergency response contractors and bill the expenses to the vessel owner.",
                "label": "Entailment",
                "target_statute": "Presidential Decree No. 979 §8",
                "legal_rationale": "Harmonious local polluter-pays requirement under national marine pollution laws."
            },
            {
                "sec_num": 10,
                "sec_title": "PENALTIES FOR INDIVIDUALS AND STEVEDORES",
                "text": "Any individual, passenger, crew member, or port laborer who intentionally throws garbage, plastic waste, or debris into coastal waters or wharves shall be penalized with a fine of One Thousand Pesos (Php 1,000.00) or eight (8) hours of coastal clean-up community service for the first offense, and Three Thousand Pesos (Php 3,000.00) for subsequent offenses.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458; Republic Act No. 9003 §49",
                "legal_rationale": "Valid municipal littering penalty complying with RA 7160."
            },
            {
                "sec_num": 11,
                "sec_title": "APPROPRIATION",
                "text": "The City Government of Davao shall allocate sufficient funds in its annual budget to support coastal water quality monitoring equipment, harbor patrol logistics, and marine sanitation enforcement.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal appropriation clause."
            },
            {
                "sec_num": 12,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any provision of this Ordinance is declared invalid or unconstitutional, the remaining provisions not affected thereby shall continue in full force and effect.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 13,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect fifteen (15) days after its complete publication in a newspaper of local circulation in Davao City.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    }
