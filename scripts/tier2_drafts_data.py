"""
scripts/tier2_drafts_data.py
============================
Contains authentic, natural legislative drafts (Drafts 1, 2, and 3)
modeled directly after real Sangguniang Panlungsod regulatory ordinances
from the Davao City corpus (e.g., Ord. 0309-07, Ord. 0897-22, Ord. 048-22,
Ord. 0495-21, Ord. 000078-00).

Eliminates unnatural filler and artificial jargon; preserves authentic
municipal phrasing, real administrative bodies, and genuine statutory
preemption defect targets.
"""

def get_draft_01():
    return {
        "doc_id": "DRAFT-ORD-2026-01",
        "title": "AN ORDINANCE REGULATING THE USE OF AGRICULTURAL CHEMICALS, ESTABLISHING BUFFER ZONES AROUND COMMERCIAL PLANTATIONS, PROHIBITING AERIAL SPRAYING, AND PROVIDING PENALTIES FOR VIOLATIONS THEREOF IN THE CITY OF DAVAO",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-01, Series of 2026",
        "committee": "Committee on Agriculture and Food, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Agricultural Chemical Regulation and Buffer Zone Ordinance of Davao City'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "Pursuant to Section 16 of Republic Act No. 7160, otherwise known as the Local Government Code of 1991, the City Government of Davao shall ensure and support the promotion of health and safety, enhance the right of the people to a balanced ecology, and preserve the comfort and convenience of its inhabitants.\n\nIt is hereby declared the policy of the City of Davao to regulate the application of agricultural chemicals in commercial crop plantations and farmlands in order to protect residential communities, schools, and water sources from the hazards of chemical drift, while supporting sustainable agricultural productivity across the city.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16",
                "legal_rationale": "Valid exercise of general welfare powers under RA 7160 §16."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "As used in this Ordinance, the following terms shall be construed to mean:\n\n(a) Agricultural Chemical - refers to any fertilizer, pesticide, fungicide, herbicide, insecticide, or other chemical substance utilized in agricultural production and crop protection;\n\n(b) Aerial Spraying - refers to the application, spraying, or dispersion of agricultural chemicals from an airplane, helicopter, drone, or any airborne aircraft;\n\n(c) Commercial Plantation - refers to any agricultural land or farm holding dedicated to the commercial cultivation of export crops such as bananas, pineapples, or oil palm;\n\n(d) Buffer Zone - refers to a physical setback area of land established between a commercial plantation boundary and adjoining residential areas, public roads, or bodies of water;\n\n(e) Ground Spraying - refers to the manual or mechanized application of agricultural chemicals using tractor-mounted boom sprayers, power sprayers, or knapsack sprayers operated from the ground.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitional section modeled after Ord. 0309-07 and Ord. 0897-22."
            },
            {
                "sec_num": 4,
                "sec_title": "SCOPE AND COVERAGE",
                "text": "This Ordinance shall apply to all commercial plantations, agricultural corporate farms, agricultural landowners, farm operators, and spraying contractors operating within the territorial jurisdiction of the City of Davao.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard scope and coverage clause."
            },
            {
                "sec_num": 5,
                "sec_title": "MANDATORY BUFFER ZONE",
                "text": "All owners, operators, and managers of commercial agricultural plantations within Davao City shall establish and maintain a mandatory thirty (30) meter buffer zone along the perimeter boundary of their plantations adjacent to residential zones, schools, public roads, and natural water bodies.\n\nThe buffer zone must be planted with appropriate trees, bamboo, and tall vegetative barriers capable of minimizing and intercepting chemical drift from field operations. Plantations shall be given a period of six (6) months from the effectivity of this Ordinance to fully establish compliant buffer zones.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(iv)",
                "legal_rationale": "Valid municipal land use setback regulation modeled after Ord. 0309-07 §6."
            },
            {
                "sec_num": 6,
                "sec_title": "BAN ON AERIAL SPRAYING",
                "text": "Aerial spraying shall be strictly prohibited in all agricultural activities and commercial crop plantations within the territorial jurisdiction of Davao City after a three (3) month transition period from the effectivity of this Ordinance.\n\nAll agricultural entities and plantation operators currently employing aerial spraying shall shift to ground-based application methods. Any person or entity found applying or causing the application of agricultural chemicals through aerial spraying shall be subject to the penalties provided in this Ordinance.",
                "label": "Contradiction",
                "target_statute": "Presidential Decree No. 1144 §6; Presidential Decree No. 1144 §8",
                "legal_rationale": "Directly contradicts Presidential Decree No. 1144 §§6 and 8, which vest exclusive national regulatory and licensing authority over pesticide application methods in the Fertilizer and Pesticide Authority (FPA). Struck down in Mosqueda v. PBGEA (2016) under the Magtajas preemption doctrine."
            },
            {
                "sec_num": 7,
                "sec_title": "REGULATION OF GROUND SPRAYING OPERATIONS",
                "text": "All ground-based chemical spraying operations within commercial plantations shall be subject to the following regulations:\n\n(a) Spraying operations shall not be conducted during periods of heavy wind or adverse weather conditions that cause excessive drift toward neighboring communities;\n\n(b) Plantation operators shall provide all farm sprayers and agricultural workers with appropriate personal protective equipment (PPE), including protective clothing, gloves, and respirators;\n\n(c) Spraying personnel must undergo proper safety training in chemical handling and application approved by the City Agriculturist's Office;\n\n(d) Chemical storage and mixing areas must be situated away from residential settlements and drainage channels.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16; Presidential Decree No. 856",
                "legal_rationale": "Harmonious local safety standards promoting agricultural worker health."
            },
            {
                "sec_num": 8,
                "sec_title": "IMPLEMENTING OFFICES AND MONITORING",
                "text": "The City Agriculturist's Office (CAO), in coordination with the City Environment and Natural Resources Office (City ENRO) and the City Health Office (CHO), shall be the primary implementing agencies of this Ordinance.\n\nThe implementing offices shall conduct periodic inspections of commercial plantations, verify the establishment of required buffer zones, investigate community complaints regarding chemical drift, and submit regular compliance reports to the City Mayor and the Sangguniang Panlungsod.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard institutional implementation clause assigning duties to CAO, CENRO, and CHO."
            },
            {
                "sec_num": 9,
                "sec_title": "NOTICE OF VIOLATION AND REMEDIATION",
                "text": "Upon discovery of any violation of Section 5 or Section 7 of this Ordinance, the City Agriculturist's Office shall immediately issue a written Notice of Violation directing the owner or operator of the plantation to institute corrective measures within fifteen (15) working days.\n\nFailure to rectify the violation within the prescribed period shall result in the filing of appropriate administrative and judicial charges against the non-compliant entity.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard administrative enforcement notice modeled after Ord. 0495-21 and Ord. 0354-23."
            },
            {
                "sec_num": 10,
                "sec_title": "PENALTIES",
                "text": "Any person, plantation operator, manager, or corporate officer who violates the provisions of this Ordinance shall, upon conviction, be penalized as follows:\n\n(a) First Offense: A fine of One Thousand Pesos (Php 1,000.00);\n\n(b) Second Offense: A fine of Three Thousand Pesos (Php 3,000.00);\n\n(c) Third and Subsequent Offenses: A fine of Five Thousand Pesos (Php 5,000.00) or imprisonment for a period of six (6) months, or both such fine and imprisonment at the discretion of the court.\n\nIn addition to the foregoing penalties, the business permit of the commercial plantation may be suspended or revoked upon recommendation of the City Legal Officer.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Strictly complies with the statutory penalty ceiling of P5,000 fine and 1-year imprisonment under RA 7160 §458."
            },
            {
                "sec_num": 11,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If, for any reason, any section or provision of this Ordinance is declared unconstitutional or invalid, other sections or provisions hereof not affected thereby shall continue to be in full force and effect.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 12,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect fifteen (15) days after its complete publication in a newspaper of general circulation in the City of Davao.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    }


def get_draft_02():
    return {
        "doc_id": "DRAFT-ORD-2026-02",
        "title": "AN ORDINANCE ENHANCING PUBLIC SAFETY AND SECURITY MEASURES IN OVERLAND TRANSPORT TERMINALS, MANDATING PASSENGER AND BAGGAGE SCREENING, PRESCRIBING TERMINAL REGULATIONS, AND PROVIDING PENALTIES FOR VIOLATIONS THEREOF IN THE CITY OF DAVAO",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-02, Series of 2026",
        "committee": "Committee on Transportation and Communication, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Overland Transport Terminal Safety and Security Ordinance of Davao City'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "Under Section 16 of Republic Act No. 7160 (The Local Government Code of 1991), the City Government of Davao is authorized to exercise powers essential to the promotion of general welfare, maintenance of peace and order, and protection of public safety.\n\nIt is hereby declared the policy of the City of Davao to promote the safety, comfort, and security of passengers, commuters, and transport workers using overland transport terminals by establishing comprehensive security standards and regulating terminal operations throughout the city.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16",
                "legal_rationale": "Valid exercise of general welfare powers under RA 7160 §16."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "For purposes of this Ordinance, the following terms shall be defined as follows:\n\n(a) Overland Transport Terminal - refers to the Davao City Overland Transport Terminal (DCOTT) and all public and private bus depots, van terminals, and public utility staging areas within Davao City;\n\n(b) Terminal Operator - refers to any government office, private corporation, or person operating or managing a public transport terminal;\n\n(c) Security Personnel - refers to organic security guards, members of the Public Safety and Security Office (PSSO), and police officers assigned to maintain order within terminal compounds;\n\n(d) Passenger Baggage - refers to luggage, backpacks, packages, and parcels brought into terminal premises by traveling passengers;\n\n(e) Public Utility Vehicle (PUV) - refers to buses, passenger vans, and jeepneys duly authorized by the LTFRB to transport passengers for compensation.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitions modeled after Ord. 048-22 and Ord. 000102-03."
            },
            {
                "sec_num": 4,
                "sec_title": "MANDATORY PASSENGER AND BAGGAGE SCREENING",
                "text": "All terminal operators shall install, operate, and maintain electronic security screening equipment at all primary passenger entrance gates:\n\n(a) Walk-through metal detectors and hand-held metal detector wands for screening passengers entering passenger waiting areas;\n\n(b) Baggage inspection tables or conveyorized X-ray machines for non-intrusive examination of passenger luggage, backpacks, and large parcels;\n\n(c) Closed-Circuit Television (CCTV) cameras installed at strategic locations including entry gates, ticket counters, and boarding bays, conforming to the provisions of the Davao City CCTV Ordinance;\n\n(d) Adequate physical signage informing passengers of security regulations and prohibited items posted in prominent areas.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(iv)",
                "legal_rationale": "Valid exercise of local police powers regulating terminal safety infrastructure."
            },
            {
                "sec_num": 5,
                "sec_title": "MANDATORY VEHICLE AND CARGO INSPECTION",
                "text": "In the interest of public safety and crime prevention, security personnel, terminal marshals, and law enforcement officers deployed at terminal checkpoints are authorized to stop and conduct thorough physical inspections of all motor vehicles, delivery vans, and private conveyances entering or utilizing terminal staging areas, including opening and inspecting luggage compartments, trunks, and enclosed cargo spaces, and to seize any unauthorized or suspicious articles found therein.\n\nAny driver, owner, or passenger who refuses to permit the opening and inspection of vehicle compartments shall be denied entry, held for police investigation, and cited for an ordinance violation.",
                "label": "Contradiction",
                "target_statute": "1987 Constitution, Art. III §2; Republic Act No. 4136 §5",
                "legal_rationale": "Violates Article III, Section 2 of the 1987 Constitution (guarantee against unreasonable searches and seizures) and RA 4136. Routine administrative entry into public terminals permits visual exterior checkpoints, but local ordinances cannot authorize mandatory warrantless interior searches, trunk inspections, and detention without judicial warrants or probable cause."
            },
            {
                "sec_num": 6,
                "sec_title": "COMMUTER AMENITIES AND SANITARY STANDARDS",
                "text": "All terminal operators shall provide clean, dignified, and functional amenities for traveling passengers without charging comfort room user fees:\n\n(a) Separate, clean toilet facilities for male and female passengers with continuous running water and hand soap;\n\n(b) Adequate and well-lit waiting areas with comfortable seating and natural or mechanical ventilation;\n\n(c) Clear priority assistance lanes and accessible facilities for senior citizens, persons with disabilities (PWDs), and pregnant women pursuant to Batas Pambansa Blg. 344;\n\n(d) Clean drinking water stations accessible to commuters within waiting lounges.",
                "label": "Entailment",
                "target_statute": "Presidential Decree No. 856; Batas Pambansa Blg. 344",
                "legal_rationale": "Harmonious local sanitation and accessibility standards under national public health and accessibility laws."
            },
            {
                "sec_num": 7,
                "sec_title": "VEHICULAR ROUTING AND TRAFFIC MANAGEMENT",
                "text": "The City Transport and Traffic Management Office (CTTMO) shall formulate and enforce traffic routing, loading and unloading schedules, and designated vehicle bays within and surrounding all terminal premises.\n\nNo public utility vehicle shall pick up or drop passengers along public streets or thoroughfares within one hundred (100) meters of any terminal entrance or exit gate, except at designated CTTMO passenger stops.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(5)(v)",
                "legal_rationale": "Valid municipal authority regulating vehicular traffic routing under RA 7160."
            },
            {
                "sec_num": 8,
                "sec_title": "IMPLEMENTING AND MONITORING AGENCIES",
                "text": "The Public Safety and Security Office (PSSO), in coordination with the City Transport and Traffic Management Office (CTTMO) and the Davao City Police Office (DCPO), shall oversee the implementation and enforcement of this Ordinance.\n\nSaid agencies shall conduct regular safety audits of transport terminals and ensure that security standards and passenger protections are strictly observed.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard implementing agency clause assigning duties to PSSO, CTTMO, and DCPO."
            },
            {
                "sec_num": 9,
                "sec_title": "NOTICE OF DEFICIENCY",
                "text": "Whenever a terminal operator fails to maintain required screening equipment or sanitary standards, the PSSO shall issue a written Notice of Deficiency requiring the operator to rectify the deficiency within ten (10) calendar days from receipt thereof.\n\nFailure to comply with the directive within the prescribed period shall subject the operator to the penalties herein provided.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard administrative enforcement notice clause."
            },
            {
                "sec_num": 10,
                "sec_title": "PENALTIES",
                "text": "Any terminal operator, manager, or person who violates the provisions of this Ordinance shall, upon conviction, be punished as follows:\n\n(a) First Offense: A fine of One Thousand Pesos (Php 1,000.00);\n\n(b) Second Offense: A fine of Three Thousand Pesos (Php 3,000.00);\n\n(c) Third and Subsequent Offenses: A fine of Five Thousand Pesos (Php 5,000.00) or imprisonment for a period of up to six (6) months, or both such fine and imprisonment at the discretion of the court.\n\nFor repeated non-compliance by private terminal operators, the City Mayor may revoke the business permit of the terminal facility upon recommendation of the City Legal Officer.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Complies strictly with the statutory penalty bounds under RA 7160 §458."
            },
            {
                "sec_num": 11,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any provision or part of this Ordinance is declared invalid or unconstitutional by a competent court, the remaining provisions not affected thereby shall continue in full force and effect.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 12,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect fifteen (15) days following its complete publication in a newspaper of local circulation in Davao City.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    }


def get_draft_03():
    return {
        "doc_id": "DRAFT-ORD-2026-03",
        "title": "AN ORDINANCE REGULATING INDUSTRIAL AIR EMISSIONS, MANDATING POLLUTION CONTROL MEASURES IN MANUFACTURING AND COMMERCIAL ESTABLISHMENTS, AND PRESCRIBING PENALTIES FOR VIOLATIONS THEREOF IN THE CITY OF DAVAO",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-03, Series of 2026",
        "committee": "Committee on Environment and Natural Resources, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Industrial Air Quality and Emission Regulation Ordinance of Davao City'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "In accordance with Section 16 of Republic Act No. 7160 (The Local Government Code of 1991), local government units are mandated to enhance the right of the people to a balanced ecology and promote public health and safety.\n\nIt is hereby declared the policy of the City Government of Davao to maintain clean air and regulate stationary sources of air pollution, ensuring that industrial and commercial operations do not discharge harmful smoke, fumes, or particulate matter that endanger the health and welfare of Davao City residents.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16",
                "legal_rationale": "Valid exercise of general welfare powers under RA 7160 §16."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "As used in this Ordinance, the following terms shall mean:\n\n(a) Stationary Source - refers to any industrial plant, factory, boiler, generator, furnace, or commercial facility that emits smoke, gas, or particulate matter into the atmosphere;\n\n(b) Air Pollution - refers to any alteration of the physical, chemical, or biological properties of the atmosphere that endangers health or creates a public nuisance;\n\n(c) Pollution Control Facility - refers to any baghouse filter, electrostatic precipitator, wet scrubber, or cyclone separator designed to reduce industrial air emissions;\n\n(d) Dark Smoke - refers to smoke emissions that equal or exceed Ringelmann Chart density standards for excessive atmospheric obscurity;\n\n(e) Industrial Establishment - refers to factories, mills, batching plants, and processing plants situated within the industrial and commercial zones of Davao City.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitions modeled after Ord. 000078-00 and national clean air standards."
            },
            {
                "sec_num": 4,
                "sec_title": "SCOPE AND COVERAGE",
                "text": "This Ordinance shall apply to all industrial plants, manufacturing factories, commercial boiler facilities, and stationary emission sources operating within the territorial jurisdiction of Davao City.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard scope and coverage clause."
            },
            {
                "sec_num": 5,
                "sec_title": "MANDATORY POLLUTION CONTROL EQUIPMENT",
                "text": "All industrial and commercial establishments operating fuel-burning equipment, boilers, or furnaces shall install, operate, and properly maintain appropriate air pollution control equipment, such as wet scrubbers, dust collectors, or fabric filters, to minimize atmospheric emissions.\n\nIndustrial establishments shall be given a period of ninety (90) calendar days from the effectivity of this Ordinance to install or upgrade compliant emission control devices.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(iv)",
                "legal_rationale": "Valid municipal regulation requiring installation of environmental safety devices."
            },
            {
                "sec_num": 6,
                "sec_title": "PROHIBITION OF DARK SMOKE AND NOXIOUS FUMES",
                "text": "No industrial or commercial establishment shall cause, allow, or permit the emission of dark smoke, toxic chemical fumes, or noxious particulate matter from any chimney, smoke stack, or exhaust vent in such quantities as to cause a public nuisance or endanger the health of surrounding communities.\n\nAll smoke stacks and exhaust vents shall be constructed at a height sufficient to ensure proper atmospheric dispersion as determined by the City Environment and Natural Resources Office (City ENRO).",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16; Presidential Decree No. 856",
                "legal_rationale": "Harmonious local air sanitation standard prohibiting public nuisances."
            },
            {
                "sec_num": 7,
                "sec_title": "PERMIT TO OPERATE AND ANNUAL ENVIRONMENTAL INSPECTION",
                "text": "All industrial establishments covered by this Ordinance must secure an annual Environmental Clearance from the City ENRO prior to the issuance or renewal of their Mayor's Business Permit.\n\nThe City ENRO shall conduct regular on-site inspections of stationary emission sources and verify the operational efficiency of all pollution control equipment.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(3)(iv)",
                "legal_rationale": "Valid exercise of municipal licensing and inspection powers."
            },
            {
                "sec_num": 8,
                "sec_title": "IMPLEMENTING AGENCY",
                "text": "The City Environment and Natural Resources Office (City ENRO), in coordination with the City Health Office (CHO) and the Department of Environment and Natural Resources (DENR-EMB Region XI), shall be the lead implementing agency of this Ordinance.\n\nCity ENRO environmental inspectors are authorized to enter industrial premises during regular operating hours to inspect emission sources and examine pollution control logs.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard implementing agency clause assigning duties to City ENRO and CHO."
            },
            {
                "sec_num": 9,
                "sec_title": "NOTICE OF VIOLATION AND CORRECTIVE ORDER",
                "text": "Whenever an inspection reveals that an establishment has discharged excessive smoke or failed to maintain required pollution control equipment, the City ENRO shall issue a written Notice of Violation.\n\nThe establishment shall be given fifteen (15) working days to institute corrective engineering measures and submit a compliance report to the City ENRO.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard administrative notice procedure modeled after Ord. 0495-21."
            },
            {
                "sec_num": 10,
                "sec_title": "CEASE AND DESIST ORDER",
                "text": "If an industrial establishment fails to comply with the corrective order within the prescribed period and continues to discharge dangerous air contaminants threatening public health, the City Mayor, upon recommendation of the City ENRO and City Legal Officer, may issue a Cease and Desist Order temporarily suspending the operation of the non-compliant emission source.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §455(b)(2)",
                "legal_rationale": "Valid exercise of local executive power abating public health hazards."
            },
            {
                "sec_num": 11,
                "sec_title": "PENALTIES",
                "text": "Any person, factory owner, plant manager, or corporate officer who violates any provision of this Ordinance shall, upon conviction, be punished by a fine of Twenty-Five Thousand Pesos (Php 25,000.00) or imprisonment of three (3) years, or both such fine and imprisonment at the discretion of the court.\n\nIn addition to the penal sanctions herein provided, the Mayor's Business Permit of the non-compliant establishment shall be revoked and the facility subject to permanent closure.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Directly violates Section 458(a)(1)(iii) of Republic Act No. 7160 (The Local Government Code of 1991), which strictly limits municipal ordinance penalties to a fine not exceeding Five Thousand Pesos (P5,000.00) and imprisonment not exceeding one (1) year. Penalties exceeding these statutory thresholds are ultra vires and void under the Magtajas doctrine."
            },
            {
                "sec_num": 12,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any provision of this Ordinance or the application thereof to any person or circumstance is held invalid, the remainder of this Ordinance shall not be affected thereby.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 13,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect fifteen (15) days after its publication in a newspaper of general circulation in Davao City.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    }
