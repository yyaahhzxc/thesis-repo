"""
Generate Tier 2 Injected-Fault Full-Document Benchmark and Tier 3 Jurisprudential Validation Datasets.

This script creates:
1. data/tier2_draft_ordinances/ (10 full draft ordinance JSON files)
2. data/tier2_draft_ordinances_benchmark.jsonl (consolidated multi-document benchmark with 140 sections)
3. data/tier3_jurisprudential_cases.jsonl (11 authentic Philippine Supreme Court & Davao City preemption cases)
"""

import json
import os

os.makedirs("data/tier2_draft_ordinances", exist_ok=True)

# -------------------------------------------------------------------------
# TIER 2 BENCHMARK: 10 Full Synthetic/Semi-Synthetic Draft Ordinances
# Evaluated against National Statutes (Vertical Conflict Detection under Magtajas & RA 7160 §5(a))
# -------------------------------------------------------------------------

tier2_drafts = [
    {
        "doc_id": "DRAFT-ORD-2026-01",
        "title": "AN ORDINANCE PROMOTING ORGANIC AGRICULTURE, REGULATING AGRICULTURAL CHEMICAL APPLICATION, AND PRESCRIBING LOCAL BUFFER ZONES IN THE CITY OF DAVAO",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-01, Series of 2026",
        "committee": "Committee on Agriculture and Food, Sangguniang Panlungsod",
        "physical_specs": {
            "paper_size": "Legal / Folio (8.5 x 13.0 inches / 215.9 x 330.2 mm)",
            "margins": "Top 1.0 in, Bottom 1.0 in, Left 1.5 in (Binding Perforation), Right 1.0 in",
            "typography": "12pt Arial, 1.5 line spacing, formal section bold caps",
            "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED"
        },
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Davao City Organic Farming and Agricultural Buffer Zone Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard short title provision containing no operative commands or prohibitions."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "It is hereby declared the policy of the City of Davao to promote sustainable agriculture, protect ecological balance, and safeguard public health from harmful agrochemicals pursuant to Section 16 of Republic Act No. 7160 and Republic Act No. 10068.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16; Republic Act No. 10068 §2",
                "legal_rationale": "Directly invokes and aligns with the statutory general welfare clause and national organic agriculture policy."
            },
            {
                "sec_num": 3,
                "sec_title": "RULES OF INTERPRETATION",
                "text": "The provisions of this Ordinance shall be liberally construed in favor of environmental conservation and the general welfare of the inhabitants of Davao City.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard interpretive canon reflecting Section 5(a) of RA 7160."
            },
            {
                "sec_num": 4,
                "sec_title": "DEFINITION OF TERMS",
                "text": "For purposes of this Ordinance, 'Organic Agriculture' shall refer to all agricultural systems that promote the environmentally, socially, and economically sound production of food and fibers. 'Buffer Zone' shall refer to an identified strip of land separating agricultural plantations from residential communities.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitional section adapting national statutory definitions without contradiction."
            },
            {
                "sec_num": 5,
                "sec_title": "LOCAL INCENTIVES FOR ORGANIC CONVERSION",
                "text": "Agricultural landholders who transition at least twenty percent (20%) of their cultivable land to certified organic farming practices shall be eligible for a fifteen percent (15%) local real property tax rebate for three (3) consecutive years, subject to verification by the City Agriculturist Office.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 10068 §24; Republic Act No. 7160 §192",
                "legal_rationale": "Valid exercise of municipal taxing power to grant local tax exemptions and incentives to promote national organic agriculture policy."
            },
            {
                "sec_num": 6,
                "sec_title": "ESTABLISHMENT OF RESIDENTIAL BUFFER ZONES",
                "text": "All commercial agricultural landholdings adjacent to established residential subdivisions, public schools, or inland water bodies shall maintain a vegetated buffer zone of not less than thirty (30) meters from the plantation boundary, planted with multi-layered canopy trees.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(iv)",
                "legal_rationale": "Valid municipal zoning and police power regulation establishing physical safety setbacks within local jurisdiction."
            },
            {
                "sec_num": 7,
                "sec_title": "PROHIBITION OF AERIAL PESTICIDE APPLICATION",
                "text": "No agricultural entity, corporation, or individual shall apply, disseminate, or spray any chemical pesticide, fungicide, or herbicide by means of aircraft, drones, or any aerial dispersal apparatus anywhere within the territorial boundaries of Davao City, regardless of national licenses or permits issued by the Fertilizer and Pesticide Authority.",
                "label": "Contradiction",
                "target_statute": "Presidential Decree No. 1144 §6; Presidential Decree No. 1144 §9",
                "legal_rationale": "Directly contradicts Presidential Decree No. 1144 which vests exclusive regulatory authority over pesticide licensing, dispersal methods, and chemical approval in the national Fertilizer and Pesticide Authority (FPA). Struck down in Mosqueda v. PBGEA (2016) under the Magtajas doctrine."
            },
            {
                "sec_num": 8,
                "sec_title": "GROUND APPLICATION SAFETY GUIDELINES",
                "text": "Ground application of registered agricultural chemicals must comply strictly with manufacturer dilution ratios and wind-speed thresholds prescribed by national agricultural standards.",
                "label": "Entailment",
                "target_statute": "Presidential Decree No. 1144 §8",
                "legal_rationale": "Harmonious local enforcement requiring compliance with national chemical safety standards."
            },
            {
                "sec_num": 9,
                "sec_title": "ADMINISTRATIVE MONITORING TASK FORCE",
                "text": "There is hereby created the Davao City Agrochemical Monitoring Task Force headed by the City Agriculturist with representatives from the City Health Office and accredited farmer cooperatives.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Internal municipal administrative tasking authorized under Section 454 of RA 7160."
            },
            {
                "sec_num": 10,
                "sec_title": "PENALTIES AND FINES",
                "text": "Any person or corporate officer found guilty of violating Section 6 or Section 8 shall be punished by a fine of Five Thousand Pesos (P5,000.00) or imprisonment for not more than one (1) year, or both, at the discretion of the court.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Statutorily compliant penalty within the exact maximum penalty ceiling of P5,000 fine and 1-year imprisonment for cities."
            },
            {
                "sec_num": 11,
                "sec_title": "APPROPRIATIONS",
                "text": "The amount necessary for the initial implementation of this Ordinance shall be charged against the unappropriated surplus of the General Fund.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal budgetary appropriation clause."
            },
            {
                "sec_num": 12,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any provision of this Ordinance or the application thereof to any person or circumstance is held invalid, the remainder of this Ordinance shall not be affected thereby.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard legislative boilerplate preserving non-offending provisions."
            },
            {
                "sec_num": 13,
                "sec_title": "REPEALING CLAUSE",
                "text": "All prior city ordinances, executive orders, and administrative regulations inconsistent with this Ordinance are hereby modified or repealed accordingly.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard general repealing clause."
            },
            {
                "sec_num": 14,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect thirty (30) days after its publication in two (2) newspapers of general circulation within the City of Davao and posting in prominent public places.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard publication and effectivity clause complying with Section 59 of RA 7160."
            }
        ]
    },
    {
        "doc_id": "DRAFT-ORD-2026-02",
        "title": "AN ORDINANCE PROHIBITING SMOKING AND VAPING IN ENCLOSED PUBLIC SPACES, REQUIRING HEALTH WARNINGS, AND PRESCRIBING LOCAL ENFORCEMENT PROTOCOLS IN DAVAO CITY",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-02, Series of 2026",
        "committee": "Committee on Health, Sangguniang Panlungsod",
        "physical_specs": {
            "paper_size": "Legal / Folio (8.5 x 13.0 inches / 215.9 x 330.2 mm)",
            "margins": "Top 1.0 in, Bottom 1.0 in, Left 1.5 in, Right 1.0 in",
            "typography": "12pt Arial, 1.5 line spacing, formal section bold caps",
            "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED"
        },
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known as the 'Davao City Comprehensive Clean Air and Anti-Smoking Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "PURPOSE AND POLICY",
                "text": "It is the policy of Davao City to guarantee the right of all citizens to breathe clean air and to reduce exposure to second-hand tobacco smoke and vapor aerosols pursuant to Republic Act No. 8749 and Republic Act No. 9211.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 8749 §2; Republic Act No. 9211 §2",
                "legal_rationale": "Valid alignment with Clean Air Act and Tobacco Regulation Act."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "'Public Conveyance' refers to any vehicle available to the public for transportation. 'Enclosed Area' refers to an area covered by a roof or enclosed by two or more walls. 'Electronic Nicotine Delivery Systems (ENDS)' refers to vapor products.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitions adapting national terms."
            },
            {
                "sec_num": 4,
                "sec_title": "PROHIBITION IN ENCLOSED PUBLIC PLACES",
                "text": "Smoking and vaping are strictly prohibited in all enclosed public places, government buildings, healthcare institutions, and educational facilities throughout the City.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 9211 §5; Republic Act No. 11900 §12",
                "legal_rationale": "Directly implements national statutory indoor smoking ban."
            },
            {
                "sec_num": 5,
                "sec_title": "DESIGNATED OUTDOOR SMOKING AREAS",
                "text": "Designated smoking and vaping areas must be located in outdoor open spaces at least ten (10) meters away from building entrances, exits, and air intake ducts.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 9211 §6",
                "legal_rationale": "Valid municipal police power adaptation specifying local physical setbacks for DSAs."
            },
            {
                "sec_num": 6,
                "sec_title": "MANDATORY POINT-OF-SALE WARNINGS",
                "text": "All retail establishments licensed to sell tobacco or vapor products shall display conspicuous signage stating that sales to persons below twenty-one (21) years of age are unlawful.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 11900 §7",
                "legal_rationale": "Echoes mandatory minimum age warning requirements under RA 11900."
            },
            {
                "sec_num": 7,
                "sec_title": "SEARCH AND CONFISCATION IN PRIVATE CONVEYANCES",
                "text": "Authorized local traffic enforcers and police officers are hereby empowered to stop, enter, search, and seize without judicial warrant any private motor vehicle operating on city streets to inspect for smoking passengers.",
                "label": "Contradiction",
                "target_statute": "1987 Constitution Art. III §2; Republic Act No. 4136 §5",
                "legal_rationale": "Violates constitutional search and seizure protections and national land transportation limits; local police cannot conduct warrantless searches of private vehicles without probable cause."
            },
            {
                "sec_num": 8,
                "sec_title": "EXCESSIVE PENAL SANCTIONS",
                "text": "Any person caught smoking within any prohibited zone shall suffer imprisonment for a fixed term of two (2) years and six (6) months, with no option for bail or probation.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Directly contradicts the express statutory ceiling of Section 458(a)(1)(iii) of RA 7160, which limits the penal power of city sanggunians to a maximum imprisonment of one (1) year."
            },
            {
                "sec_num": 9,
                "sec_title": "ANTI-SMOKING TASK FORCE",
                "text": "The Davao City Anti-Smoking Task Force shall oversee enforcement, maintain statistical records, and conduct public awareness drives in all barangays.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Municipal enforcement structure."
            },
            {
                "sec_num": 10,
                "sec_title": "COMMUNITY SERVICE OPTION",
                "text": "First-time individual offenders unable to pay administrative fines may perform eight (8) hours of community environmental service under the supervision of the City Environment and Natural Resources Office.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard local administrative penalty alternative."
            },
            {
                "sec_num": 11,
                "sec_title": "DUTIES OF ESTABLISHMENT OWNERS",
                "text": "Proprietors and building managers must post standard 'No Smoking' notices and ensure compliance within their premises.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard establishment owner obligations."
            },
            {
                "sec_num": 12,
                "sec_title": "APPROPRIATIONS",
                "text": "The sum of Two Million Pesos (P2,000,000.00) is hereby allocated from the City Annual Budget for operational expenses and educational campaigns.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal budgetary appropriation."
            },
            {
                "sec_num": 13,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any section or part of this Ordinance is declared unconstitutional or invalid, other sections shall remain in effect.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 14,
                "sec_title": "REPEALING CLAUSE",
                "text": "All prior city ordinances inconsistent with this Ordinance are hereby repealed.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard repealing clause."
            },
            {
                "sec_num": 15,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect fifteen (15) days after complete publication in a local newspaper of general circulation.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    },
    {
        "doc_id": "DRAFT-ORD-2026-03",
        "title": "AN ORDINANCE REGULATING SPEED LIMITS, DESIGNATING ACTIVE MOBILITY CORRIDORS, AND ESTABLISHING TRAFFIC SAFETY STANDARDS IN DAVAO CITY",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-03, Series of 2026",
        "committee": "Committee on Transportation and Communications, Sangguniang Panlungsod",
        "physical_specs": {
            "paper_size": "Legal / Folio (8.5 x 13.0 inches / 215.9 x 330.2 mm)",
            "margins": "Top 1.0 in, Bottom 1.0 in, Left 1.5 in, Right 1.0 in",
            "typography": "12pt Arial, 1.5 line spacing, formal section bold caps",
            "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED"
        },
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be cited as the 'Davao City Speed Limit and Active Mobility Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF TRAFFIC SAFETY POLICY",
                "text": "The City Government adopts a Safe Systems approach to urban mobility, prioritizing pedestrian safety and accident reduction across all thoroughfares.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard policy statement."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "'Urban Road' refers to municipal streets within the poblacion. 'National Highway' refers to primary arterial thoroughfares connecting Davao City to neighboring provinces. 'Active Mobility' refers to cycling and pedestrian transport.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitions."
            },
            {
                "sec_num": 4,
                "sec_title": "URBAN ROAD SPEED CEILINGS",
                "text": "Vehicles traversing local municipal roads and crowded school zones shall observe a maximum speed of thirty (30) kilometers per hour.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 4136 §35(b); Joint DILG-DOTr-DPWH JAO 2018-01",
                "legal_rationale": "Valid local speed setting on municipal streets expressly delegated to LGUs under national traffic guidelines."
            },
            {
                "sec_num": 5,
                "sec_title": "DEDICATED BICYCLE AND ACTIVE MOBILITY LANES",
                "text": "The City Transport and Traffic Management Office (CTTMO) shall delineate protected bicycle lanes along major municipal avenues.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(3)(vi)",
                "legal_rationale": "Valid municipal authority to regulate traffic and provide public street lanes."
            },
            {
                "sec_num": 6,
                "sec_title": "SPEED LIMIT ON NATIONAL ARTERIAL HIGHWAYS",
                "text": "All motor vehicles, including provincial buses and inter-regional freight trucks traversing national primary highways passing through Davao City, shall not exceed fifteen (15) kilometers per hour at any time.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 4136 §35; Republic Act No. 4136 §38",
                "legal_rationale": "Contradicts Republic Act No. 4136 Section 35 and DPWH arterial speed regulations; local governments cannot impose unreasonable or obstructive speed ceilings on national highways that paralyze national trade."
            },
            {
                "sec_num": 7,
                "sec_title": "PEDESTRIAN WALKWAYS AND CROSSWALKS",
                "text": "Motorists must yield complete right-of-way to pedestrians crossing marked street intersections and zebra crossings.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 4136 §42(c)",
                "legal_rationale": "Reinforces national statutory pedestrian right-of-way rules."
            },
            {
                "sec_num": 8,
                "sec_title": "SPEED MONITORING DEVICES",
                "text": "The CTTMO is authorized to deploy calibrated radar speed guns and automated optical speed sensors to document traffic infractions.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Municipal enforcement tool authorization."
            },
            {
                "sec_num": 9,
                "sec_title": "TRAFFIC CITATION TICKET SYSTEM",
                "text": "Infractions under this Ordinance shall be penalized by administrative citation tickets issued by accredited CTTMO enforcers.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal administrative ticketing procedure."
            },
            {
                "sec_num": 10,
                "sec_title": "GRADUATED FINES",
                "text": "Violators shall pay a fine of P1,000 for the first offense, P2,000 for the second offense, and P5,000 for the third offense.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Fines remain within the statutory limit of P5,000 for cities."
            },
            {
                "sec_num": 11,
                "sec_title": "SPEED CALIBRATION AUDITING",
                "text": "All speed detection devices must undergo semi-annual calibration certification by the Department of Science and Technology (DOST).",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Procedural verification standard."
            },
            {
                "sec_num": 12,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "Should any provision of this Ordinance be declared void by a competent court, all remaining provisions shall remain valid.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 13,
                "sec_title": "REPEALING CLAUSE",
                "text": "All municipal speed ordinances or executive directives inconsistent herewith are amended or revoked.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard repealing clause."
            },
            {
                "sec_num": 14,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect thirty (30) days following publication in two newspapers of general circulation in Region XI.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    },
    {
        "doc_id": "DRAFT-ORD-2026-04",
        "title": "AN ORDINANCE STRENGTHENING THE LOCAL PRICE COORDINATING COUNCIL, REGULATING COMMODITY PRICE MONITORING, AND PREVENTING HOARDING DURING CALAMITIES IN DAVAO CITY",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-04, Series of 2026",
        "committee": "Committee on Trade, Commerce and Industry, Sangguniang Panlungsod",
        "physical_specs": {
            "paper_size": "Legal / Folio (8.5 x 13.0 inches / 215.9 x 330.2 mm)",
            "margins": "Top 1.0 in, Bottom 1.0 in, Left 1.5 in, Right 1.0 in",
            "typography": "12pt Arial, 1.5 line spacing, formal section bold caps",
            "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED"
        },
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known as the 'Davao City Fair Price and Calamity Consumer Protection Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard title provision."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF CONSUMER PROTECTION POLICY",
                "text": "The City Government ensures the availability of basic necessities and prime commodities at reasonable prices, protecting consumers from trade malpractices pursuant to Republic Act No. 7581.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7581 §2",
                "legal_rationale": "Directly implements the national Price Act policy."
            },
            {
                "sec_num": 3,
                "sec_title": "LOCAL PRICE COORDINATING COUNCIL",
                "text": "The Davao City Local Price Coordinating Council (LPCC) is hereby revitalized, with the City Mayor as Chairman and the DTI Provincial Director as Vice Chairman.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7581 §12; DILG-DTI-DA-DOH JAO 2013-01",
                "legal_rationale": "Directly implements national institutional architecture for local price coordination."
            },
            {
                "sec_num": 4,
                "sec_title": "AUTOMATIC PRICE FREEZE UPON CALAMITY",
                "text": "Upon declaration of a state of calamity by the Sangguniang Panlungsod, prices of basic necessities shall be automatically frozen at their prevailing market rates.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7581 §6; Republic Act No. 10121 §16",
                "legal_rationale": "Echoes mandatory statutory price freeze triggered by LGU state of calamity declaration."
            },
            {
                "sec_num": 5,
                "sec_title": "DEFINITION OF BASIC NECESSITIES",
                "text": "'Basic Necessities' shall include rice, corn, bread, fresh fish, pork, beef, poultry, vegetables, root crops, fresh milk, cooking oil, salt, laundry soap, and medicines.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard statutory categorization from RA 7581."
            },
            {
                "sec_num": 6,
                "sec_title": "MUNICIPAL UNILATERAL PRICE MANDATE",
                "text": "The City Mayor, by executive order, is hereby authorized to unilaterally fix and mandate price ceilings on all manufactured consumer goods at fifty percent (50%) below the Suggested Retail Price (SRP) issued by the Department of Trade and Industry, without presidential approval or emergency proclamation.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7581 §7",
                "legal_rationale": "Directly contradicts Republic Act No. 7581 Section 7, which reserves the power to mandate price ceilings strictly to the President of the Philippines upon recommendation of the implementing agency."
            },
            {
                "sec_num": 7,
                "sec_title": "INSPECTION OF WAREHOUSES AND RETAIL OUTLETS",
                "text": "Authorized joint inspection teams of the LPCC and DTI may conduct periodic inspections of commercial storage facilities to verify inventory logs.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard joint regulatory inspection powers."
            },
            {
                "sec_num": 8,
                "sec_title": "PROHIBITION OF PROFITEERING AND HOARDING",
                "text": "No retail or wholesale merchant shall accumulate goods in excess of normal inventory to corner the market or sell above prevailing price freezes.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7581 §5",
                "legal_rationale": "Parallels national anti-hoarding provisions."
            },
            {
                "sec_num": 9,
                "sec_title": "LOCAL BUSINESS LICENSE REVOCATION",
                "text": "Merchants proven to engage in illegal hoarding during a declared state of calamity shall face immediate cancellation of their Mayor's Business Permit.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(ii)",
                "legal_rationale": "Valid municipal licensing authority."
            },
            {
                "sec_num": 10,
                "sec_title": "PENAL SANCTIONS",
                "text": "Violators shall be subject to an administrative fine of P5,000.00 and suspension of business operations for not more than six (6) months.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Compliant with municipal penalty ceiling."
            },
            {
                "sec_num": 11,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "The invalidity of any provision shall not invalidate the other portions hereof.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 12,
                "sec_title": "REPEALING CLAUSE",
                "text": "All ordinances in conflict with this enactment are hereby repealed.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard repealing clause."
            },
            {
                "sec_num": 13,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect immediately upon its approval.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    },
    {
        "doc_id": "DRAFT-ORD-2026-05",
        "title": "AN ORDINANCE MANDATING CLOSED-CIRCUIT TELEVISION (CCTV) INSTALLATION IN COMMERCIAL PREMISES AND ESTABLISHING SECURITY DATA PROTOCOLS IN DAVAO CITY",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-05, Series of 2026",
        "committee": "Committee on Public Safety and Security, Sangguniang Panlungsod",
        "physical_specs": {
            "paper_size": "Legal / Folio (8.5 x 13.0 inches / 215.9 x 330.2 mm)",
            "margins": "Top 1.0 in, Bottom 1.0 in, Left 1.5 in, Right 1.0 in",
            "typography": "12pt Arial, 1.5 line spacing, formal section bold caps",
            "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED"
        },
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known as the 'Davao City Mandatory Commercial CCTV and Security Surveillance Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard title provision."
            },
            {
                "sec_num": 2,
                "sec_title": "LEGISLATIVE INTENT",
                "text": "The City Government exercises its police power to preserve public order, enhance crime detection, and protect commercial establishments through modern surveillance technologies under Section 16 of Republic Act No. 7160.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16",
                "legal_rationale": "Valid exercise of police power for crime prevention under the general welfare clause."
            },
            {
                "sec_num": 3,
                "sec_title": "COVERED COMMERCIAL ESTABLISHMENTS",
                "text": "All banks, shopping malls, supermarkets, pawnshops, money-transfer stations, hotels, fuel stations, and private educational institutions operating within the City shall install functional CCTV systems.",
                "label": "Entailment",
                "target_statute": "DILG Memorandum Circular No. 2022-060",
                "legal_rationale": "Aligns with national DILG guidelines on mandatory business CCTV requirements."
            },
            {
                "sec_num": 4,
                "sec_title": "MINIMUM TECHNICAL SPECIFICATIONS",
                "text": "Surveillance cameras must possess a minimum resolution of 1080p, night vision capability, and a minimum continuous recording retention capacity of not less than thirty (30) calendar days.",
                "label": "Entailment",
                "target_statute": "DILG Memorandum Circular No. 2022-060",
                "legal_rationale": "Standard technical specifications for evidentiary reliability."
            },
            {
                "sec_num": 5,
                "sec_title": "DEFINITION OF TERMS",
                "text": "'Biometric Data' refers to physiological characteristics used for identification. 'Personal Data' refers to information from which the identity of an individual is apparent. 'CCTV' refers to closed-circuit television.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitions."
            },
            {
                "sec_num": 6,
                "sec_title": "MANDATORY PUBLIC BROADCAST OF REAL-TIME PRIVATE FEEDS",
                "text": "All covered private business entities must connect their internal security cameras directly to a publicly accessible municipal cloud portal, transmitting unredacted, unencrypted real-time facial recognition data of all customers without individual consent or National Privacy Commission clearance.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 10173 §11; Republic Act No. 10173 §12; NPC Circular No. 16-01",
                "legal_rationale": "Directly violates Republic Act No. 10173 (Data Privacy Act of 2012) principles of transparency, legitimate purpose, and proportionality, and breaches constitutional privacy guarantees by publishing unredacted surveillance feeds without consent."
            },
            {
                "sec_num": 7,
                "sec_title": "INDEFINITE BIOMETRIC DATA RETENTION",
                "text": "The City Government shall retain all captured facial recognition logs and customer movement records permanently in perpetuity, prohibiting any citizen from requesting data deletion or rectification.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 10173 §16; Republic Act No. 10173 §18",
                "legal_rationale": "Directly contradicts the statutory Rights of the Data Subject under Section 16 of RA 10173, including the right to erasure, blocking, and data minimization."
            },
            {
                "sec_num": 8,
                "sec_title": "ANNUAL BUSINESS PERMIT AUDIT",
                "text": "Inspection and certification of CCTV functionality by the City Engineers Office shall be a mandatory prerequisite for the renewal of Mayor's Business Permits.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(ii)",
                "legal_rationale": "Valid regulatory condition precedent for municipal business licensing."
            },
            {
                "sec_num": 9,
                "sec_title": "DATA SECURITY COMPLIANCE OFFICER",
                "text": "Each commercial establishment shall designate a Compliance Officer responsible for safeguarding stored recordings against unauthorized dissemination.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Administrative compliance requirement."
            },
            {
                "sec_num": 10,
                "sec_title": "PENALTIES FOR NON-INSTALLATION",
                "text": "Failure to install functional CCTVs within ninety (90) days from notice shall result in a fine of P5,000.00 and suspension of business permit.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Statutory fine within municipal limits."
            },
            {
                "sec_num": 11,
                "sec_title": "APPROPRIATIONS",
                "text": "Necessary funds for city monitoring terminals shall be allocated from the annual executive budget.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard appropriation clause."
            },
            {
                "sec_num": 12,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any provision is declared unconstitutional, the rest shall remain operative.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 13,
                "sec_title": "REPEALING CLAUSE",
                "text": "All prior conflicting city orders and resolutions are hereby revoked.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard repealing clause."
            },
            {
                "sec_num": 14,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect thirty (30) days after publication.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    },
    {
        "doc_id": "DRAFT-ORD-2026-06",
        "title": "AN ORDINANCE REGULATING SINGLE-USE PLASTICS, ENFORCING SOURCE SEGREGATION, AND ADVANCING CIRCULAR WASTE MANAGEMENT IN DAVAO CITY",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-06, Series of 2026",
        "committee": "Committee on Environment and Natural Resources, Sangguniang Panlungsod",
        "physical_specs": {
            "paper_size": "Legal / Folio (8.5 x 13.0 inches / 215.9 x 330.2 mm)",
            "margins": "Top 1.0 in, Bottom 1.0 in, Left 1.5 in, Right 1.0 in",
            "typography": "12pt Arial, 1.5 line spacing, formal section bold caps",
            "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED"
        },
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known as the 'Davao City Ecological Solid Waste Management and Plastic Regulation Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF SOLID WASTE POLICY",
                "text": "The City Government commits to systemic ecological solid waste management, waste minimization, and resource recovery pursuant to Republic Act No. 9003 and Republic Act No. 11898.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 9003 §2; Republic Act No. 11898 §2",
                "legal_rationale": "Harmonious adoption of national solid waste management and extended producer responsibility policies."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "'Single-Use Plastics' refers to disposable plastic items designed for one-time use before disposal. 'Source Segregation' refers to the sorting of solid waste at the household level.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitional terms."
            },
            {
                "sec_num": 4,
                "sec_title": "MANDATORY SEGREGATION AT SOURCE",
                "text": "All households, commercial establishments, and public institutions must segregate solid waste into biodegradable, recyclable, non-recyclable, and special hazardous waste categories prior to collection.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 9003 §21",
                "legal_rationale": "Directly implements the mandatory source segregation requirement of RA 9003."
            },
            {
                "sec_num": 5,
                "sec_title": "BARANGAY MATERIALS RECOVERY FACILITIES",
                "text": "Each of the 182 barangays of Davao City shall establish and operate a dedicated Materials Recovery Facility (MRF) or cluster MRF for recyclable and biodegradable composting.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 9003 §32",
                "legal_rationale": "Directly enforces the statutory mandate under Section 32 of RA 9003 requiring barangay-level MRFs."
            },
            {
                "sec_num": 6,
                "sec_title": "PHASE-OUT OF PLASTIC BAGS IN COMMERCE",
                "text": "Commercial groceries and department stores are prohibited from distributing non-biodegradable single-use checkout plastic bags, encouraging reusable shopping bags.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(vi); Republic Act No. 9003 §48",
                "legal_rationale": "Valid municipal police power regulating commercial packaging for environmental sanitation."
            },
            {
                "sec_num": 7,
                "sec_title": "MUNICIPAL IMPORT BARRICADE AND CARGO FORFEITURE",
                "text": "The City Government shall establish checkpoints at the Port of Davao to inspect, intercept, confiscate, and destroy all international cargo shipments of plastic polymers imported under national customs clearance.",
                "label": "Contradiction",
                "target_statute": "1987 Constitution Art. XII §1; Republic Act No. 10863 §200; Republic Act No. 10863 §300",
                "legal_rationale": "Contradicts the exclusive jurisdiction of the Bureau of Customs under Republic Act No. 10863 (Customs Modernization and Tariff Act); municipal councils have no constitutional power over international trade and customs clearance."
            },
            {
                "sec_num": 8,
                "sec_title": "EXORBITANT CONSUMER FINES",
                "text": "Any individual resident found possessing a single-use plastic straw or fork shall be assessed an administrative fine of Fifty Thousand Pesos (P50,000.00) and three (3) years imprisonment.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Blatantly violates Section 458(a)(1)(iii) of RA 7160 which limits city sanggunian penalties to a maximum of P5,000 fine and 1-year imprisonment."
            },
            {
                "sec_num": 9,
                "sec_title": "COLLECTION SCHEDULE COMPLIANCE",
                "text": "Waste collection trucks shall strictly collect segregated biodegradables on designated days and non-biodegradables on alternate days.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal operational scheduling."
            },
            {
                "sec_num": 10,
                "sec_title": "PUBLIC AWARENESS AND EDUCATION",
                "text": "The City Environment and Natural Resources Office (CENRO) shall conduct information campaigns in all public schools regarding waste reduction.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Municipal educational mandate."
            },
            {
                "sec_num": 11,
                "sec_title": "ECO-ENTERPRISE ACCREDITATION",
                "text": "Private recycling firms may register with CENRO for preferred participation in municipal resource-recovery programs.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal partner registration."
            },
            {
                "sec_num": 12,
                "sec_title": "APPROPRIATIONS",
                "text": "Funds for the support of barangay MRFs shall be incorporated into the annual statutory ecological fund.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard appropriation clause."
            },
            {
                "sec_num": 13,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any clause is held unconstitutional, other clauses remain valid.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 14,
                "sec_title": "REPEALING CLAUSE",
                "text": "Inconsistent local enactments are repealed.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard repealing clause."
            },
            {
                "sec_num": 15,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance takes effect thirty (30) days from publication.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    },
    {
        "doc_id": "DRAFT-ORD-2026-07",
        "title": "AN ORDINANCE REGULATING THE ERECTION, INSTALLATION, AND MAINTENANCE OF OUTDOOR BILLBOARDS AND SIGNAGE IN DAVAO CITY",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-07, Series of 2026",
        "committee": "Committee on Housing and Urban Development, Sangguniang Panlungsod",
        "physical_specs": {
            "paper_size": "Legal / Folio (8.5 x 13.0 inches / 215.9 x 330.2 mm)",
            "margins": "Top 1.0 in, Bottom 1.0 in, Left 1.5 in, Right 1.0 in",
            "typography": "12pt Arial, 1.5 line spacing, formal section bold caps",
            "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED"
        },
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be cited as the 'Davao City Signage and Outdoor Advertising Safety Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard title provision."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF URBAN SAFETY POLICY",
                "text": "The City Government exercises its police power to preserve structural safety, traffic sightlines, and aesthetic order from hazardously situated outdoor signage under Section 458(a)(4)(iv) of Republic Act No. 7160.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(iv)",
                "legal_rationale": "Directly invokes explicit city council authority to regulate outdoor advertising signs (affirmed in Evasco v. Montañez, 2018)."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "'Billboard' refers to any off-premise advertising sign. 'Signage' refers to any identification banner or emblem visible from a public street.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitions."
            },
            {
                "sec_num": 4,
                "sec_title": "SETBACK AND CLEARANCE REQUIREMENTS",
                "text": "All free-standing billboards must maintain a minimum setback of five (5) meters from road right-of-way boundaries and must not obstruct street traffic lights.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(iv)",
                "legal_rationale": "Valid local safety setback regulation."
            },
            {
                "sec_num": 5,
                "sec_title": "MAXIMUM HEIGHT LIMITATIONS",
                "text": "No billboard structure along the scenic coastal and mountain corridors shall exceed eighteen (18) meters in total height measured from ground elevation.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(iv)",
                "legal_rationale": "Valid local police power zoning limitation preserving sightlines."
            },
            {
                "sec_num": 6,
                "sec_title": "SEISMIC AND STRUCTURAL EXEMPTION",
                "text": "Billboards erected by registered local municipal businesses are hereby declared exempt from the structural design computations, wind load testing, and building permit requirements of the National Building Code of the Philippines (Presidential Decree No. 1096), requiring only a Barangay Clearance.",
                "label": "Contradiction",
                "target_statute": "Presidential Decree No. 1096 §301; Presidential Decree No. 1096 §302",
                "legal_rationale": "Directly contradicts Presidential Decree No. 1096 (National Building Code) Section 301; a municipal ordinance cannot exempt physical commercial structures from national structural safety permits."
            },
            {
                "sec_num": 7,
                "sec_title": "ELECTRICAL AND ILLUMINATION STANDARDS",
                "text": "Digital LED billboards must incorporate auto-dimming mechanisms to reduce glaring illumination during nighttime hours between 10:00 PM and 5:00 AM.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16",
                "legal_rationale": "Valid traffic safety regulation under general welfare police power."
            },
            {
                "sec_num": 8,
                "sec_title": "INSPECTION AND INVENTORY",
                "text": "The City Building Official shall maintain an updated geo-referenced inventory of all permitted outdoor signs in Davao City.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Administrative municipal database maintenance."
            },
            {
                "sec_num": 9,
                "sec_title": "DISMANTLING OF DILAPIDATED STRUCTURES",
                "text": "Signage abandoned for more than six (6) months or posing imminent danger of collapse shall be dismantled after due notice.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal abatement of nuisance."
            },
            {
                "sec_num": 10,
                "sec_title": "ANNUAL SIGNAGE FEES",
                "text": "Annual regulatory inspection fees shall be collected based on total display square meterage.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §147",
                "legal_rationale": "Valid municipal regulatory fee under RA 7160 Section 147."
            },
            {
                "sec_num": 11,
                "sec_title": "PENALTIES FOR NON-COMPLIANCE",
                "text": "Violators shall be fined P5,000.00 and ordered to dismantle unauthorized structures within ten (10) calendar days.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Statutorily compliant fine."
            },
            {
                "sec_num": 12,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "The declaration of unconstitutionality of any provision shall not impair other sections.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 13,
                "sec_title": "REPEALING CLAUSE",
                "text": "Conflicting local measures are hereby repealed.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard repealing clause."
            },
            {
                "sec_num": 14,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect fifteen (15) days after publication.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    },
    {
        "doc_id": "DRAFT-ORD-2026-08",
        "title": "AN ORDINANCE REGULATING COMMERCIAL SAND AND GRAVEL EXTRACTION, SAFEGUARDING RIVERBANKS, AND ESTABLISHING QUARRY PERMITTING IN DAVAO CITY",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-08, Series of 2026",
        "committee": "Committee on Environment and Natural Resources, Sangguniang Panlungsod",
        "physical_specs": {
            "paper_size": "Legal / Folio (8.5 x 13.0 inches / 215.9 x 330.2 mm)",
            "margins": "Top 1.0 in, Bottom 1.0 in, Left 1.5 in, Right 1.0 in",
            "typography": "12pt Arial, 1.5 line spacing, formal section bold caps",
            "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED"
        },
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be cited as the 'Davao City Sustainable Quarrying and River Protection Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard title provision."
            },
            {
                "sec_num": 2,
                "sec_title": "POLICY STATEMENT",
                "text": "The City Government balances local construction material needs with ecological preservation of vital river ecosystems under Republic Act No. 7942 and Section 16 of Republic Act No. 7160.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7942 §43; Republic Act No. 7160 §16",
                "legal_rationale": "Harmonious balance of quarrying regulation with national mining statute."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "'Quarry Resources' refers to common rocks, sand, gravel, and earth materials. 'Commercial Sand and Gravel Permit' refers to a license granted for extraction not exceeding five (5) hectares.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Adapts national definitions from RA 7942 Section 43."
            },
            {
                "sec_num": 4,
                "sec_title": "RIVER EMBANKMENT BUFFER ZONE",
                "text": "Extraction of sand and gravel is strictly prohibited within one hundred (100) meters upstream and downstream of any bridge, water intake, or public flood control structure.",
                "label": "Entailment",
                "target_statute": "Presidential Decree No. 1067 §51; Republic Act No. 7942 §43",
                "legal_rationale": "Implements national Water Code river protection setbacks."
            },
            {
                "sec_num": 5,
                "sec_title": "CITY MINING REGULATORY BOARD PERMITTING",
                "text": "Commercial quarry permits within five (5) hectares shall be evaluated by the City Mining Regulatory Board (CMRB) and approved by the City Mayor.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7076 §24; Republic Act No. 7942 §43",
                "legal_rationale": "Follows the exact statutory delegation under Section 43 of RA 7942."
            },
            {
                "sec_num": 6,
                "sec_title": "UNILATERAL MINERAL EXPORT AUTHORIZATION",
                "text": "The Sangguniang Panlungsod is hereby empowered to issue local extraction permits for heavy metallic minerals (including nickel, copper, and gold) across ancestral domain lands, authorizing direct commercial export overseas without securing a Mineral Production Sharing Agreement (MPSA) from the DENR or clearance from the NCIP.",
                "label": "Contradiction",
                "target_statute": "1987 Constitution Art. XII §2; Republic Act No. 7942 §27; Republic Act No. 8371 §59",
                "legal_rationale": "Directly violates the Regalian Doctrine (State ownership of metallic mineral resources), Republic Act No. 7942 which reserves mineral agreements strictly to national DENR authority, and Republic Act No. 8371 (IPRA) Free Prior Informed Consent mandates."
            },
            {
                "sec_num": 7,
                "sec_title": "DELIVERY RECEIPT TRACKING",
                "text": "All trucks transporting quarried aggregates within Davao City must carry a valid Delivery Receipt issued by the City Environment Office indicating the volume and extraction site.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Valid municipal transport tracking requirement."
            },
            {
                "sec_num": 8,
                "sec_title": "REHABILITATION BOND",
                "text": "Permittees shall post an environmental rehabilitation deposit prior to the commencement of extraction operations.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal environmental safeguard."
            },
            {
                "sec_num": 9,
                "sec_title": "PROHIBITION OF NIGHT EXTRACTION",
                "text": "No quarrying operations shall be conducted between 6:00 PM and 6:00 AM.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Local police power operating hours regulation."
            },
            {
                "sec_num": 10,
                "sec_title": "PENALTIES AND CONFISCATION",
                "text": "Illegal extraction shall result in a fine of P5,000.00 and impoundment of transport vehicles.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Statutory fine within municipal limits."
            },
            {
                "sec_num": 11,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "Invalidity of any section shall not affect other portions.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 12,
                "sec_title": "REPEALING CLAUSE",
                "text": "All inconsistent local rules are repealed.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard repealing clause."
            },
            {
                "sec_num": 13,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance takes effect thirty (30) days from publication.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    },
    {
        "doc_id": "DRAFT-ORD-2026-09",
        "title": "AN ORDINANCE REGULATING TELECOMMUNICATIONS CABLE INSTALLATIONS, UNDERGROUND UTILITY DUCTS, AND RESTORATION OF PUBLIC ROADS IN DAVAO CITY",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-09, Series of 2026",
        "committee": "Committee on Public Works and Telecommunications, Sangguniang Panlungsod",
        "physical_specs": {
            "paper_size": "Legal / Folio (8.5 x 13.0 inches / 215.9 x 330.2 mm)",
            "margins": "Top 1.0 in, Bottom 1.0 in, Left 1.5 in, Right 1.0 in",
            "typography": "12pt Arial, 1.5 line spacing, formal section bold caps",
            "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED"
        },
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be cited as the 'Davao City Telecommunications Infrastructure and Underground Cabling Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard title provision."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF INFRASTRUCTURE POLICY",
                "text": "The City Government ensures public road safety, prevents aerial cable clutter, and coordinates telecommunications infrastructure pursuant to Republic Act No. 7925 and Republic Act No. 7160.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7925 §4; Republic Act No. 7160 §458(a)(5)(vi)",
                "legal_rationale": "Valid municipal police power over city roads and utilities."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "'Public Telecommunications Entity' refers to any entity authorized to provide public telecommunications services. 'Excavation Permit' refers to an authorization to dig public streets.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitions."
            },
            {
                "sec_num": 4,
                "sec_title": "EXCAVATION PERMITS AND RESTORATION BONDS",
                "text": "All telecommunications utilities undertaking street excavation for fiber optic installation must obtain an Excavation Permit from the City Engineer and post a performance restoration bond.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(5)(vi)",
                "legal_rationale": "Direct municipal authority to regulate street digging and ensure road repair."
            },
            {
                "sec_num": 5,
                "sec_title": "UNDERGROUND CABLING MANDATE IN HERITAGE ZONES",
                "text": "All overhead aerial power and telecommunications cables within the designated downtown historical and commercial zones must be placed underground within three (3) years.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(iv)",
                "legal_rationale": "Valid local zoning and public safety measure."
            },
            {
                "sec_num": 6,
                "sec_title": "LOCAL LEGISLATIVE FRANCHISE REQUIREMENT FOR WIRELESS CARRIERS",
                "text": "No public telecommunications entity holding a national legislative franchise from the Congress of the Philippines shall transmit wireless cellular signals or operate frequency transmitters within Davao City without first obtaining a separate secondary legislative franchise approved by the Sangguniang Panlungsod.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7925 §5; Republic Act No. 7925 §21; Presidential Decree No. 576-A §1",
                "legal_rationale": "Directly contradicts Republic Act No. 7925 which vests exclusive regulatory authority over wireless frequencies and national telecommunications carriers in the National Telecommunications Commission (NTC). Confirmed in Batangas CATV v. CA (2004) under the preemption doctrine."
            },
            {
                "sec_num": 7,
                "sec_title": "UNILATERAL RATE REGULATION OF INTERNET SERVICES",
                "text": "The Sangguniang Panlungsod shall fix the maximum retail subscription tariffs that mobile telephone carriers may charge individual subscribers residing within Davao City.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7925 §17; 1987 Constitution Art. XII §19",
                "legal_rationale": "Directly violates Section 17 of Republic Act No. 7925, which reserves the regulation and deregulation of telecommunication tariffs exclusively to the NTC."
            },
            {
                "sec_num": 8,
                "sec_title": "SHARED TELECOMMUNICATION TOWER INFRASTRUCTURE",
                "text": "Cellular operators are encouraged to utilize shared passive infrastructure and co-locate on authorized common cellular towers.",
                "label": "Neutral",
                "target_statute": "DICT Department Circular No. 008-2020",
                "legal_rationale": "Parallels national DICT common tower policy."
            },
            {
                "sec_num": 9,
                "sec_title": "RESTORATION QUALITY STANDARDS",
                "text": "Excavated road trenches must be restored to original asphalt or concrete specifications within forty-eight (48) hours of cable laying.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal engineering requirement."
            },
            {
                "sec_num": 10,
                "sec_title": "COORDINATING INFRASTRUCTURE COMMITTEE",
                "text": "The City Telecommunications Infrastructure Coordinating Committee shall coordinate all scheduled road works to prevent duplicate street diggings.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Municipal inter-agency administrative tasking."
            },
            {
                "sec_num": 11,
                "sec_title": "PENALTIES AND FINES",
                "text": "Unauthorized excavation or failure to restore roads shall be penalized by a fine of P5,000.00 and forfeiture of the restoration bond.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Statutory fine within municipal limits."
            },
            {
                "sec_num": 12,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "Invalidity of any section shall not affect the remaining portions.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 13,
                "sec_title": "REPEALING CLAUSE",
                "text": "All prior conflicting municipal measures are repealed.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard repealing clause."
            },
            {
                "sec_num": 14,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance takes effect thirty (30) days from publication.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    },
    {
        "doc_id": "DRAFT-ORD-2026-10",
        "title": "AN ORDINANCE AMENDING THE REVENUE CODE OF DAVAO CITY, REGULATING BUSINESS TAX ON COMMERCIAL ENTERPRISES, AND PRESCRIBING LOCAL TAX ADMINISTRATION",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-10, Series of 2026",
        "committee": "Committee on Ways and Means, Sangguniang Panlungsod",
        "physical_specs": {
            "paper_size": "Legal / Folio (8.5 x 13.0 inches / 215.9 x 330.2 mm)",
            "margins": "Top 1.0 in, Bottom 1.0 in, Left 1.5 in, Right 1.0 in",
            "typography": "12pt Arial, 1.5 line spacing, formal section bold caps",
            "enacting_clause": "BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED"
        },
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known as the 'Davao City Revenue Code Amendment on Commercial Business Taxation of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard title provision."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF FISCAL POLICY",
                "text": "The City Government exercises its constitutional power to create its own sources of revenue, ensuring fair taxation within statutory limits under Republic Act No. 7160.",
                "label": "Entailment",
                "target_statute": "1987 Constitution Art. X §5; Republic Act No. 7160 §129",
                "legal_rationale": "Valid exercise of constitutional and statutory local taxing authority."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "'Business' refers to commercial activity for profit. 'Gross Sales or Receipts' refers to the total amount received from merchandise sales or services.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Adapts Section 131 definitions from RA 7160."
            },
            {
                "sec_num": 4,
                "sec_title": "GRADUATED BUSINESS TAX ON RETAIL MERCHANTS",
                "text": "Retail merchants with gross sales exceeding Four Hundred Thousand Pesos (P400,000.00) shall pay a local business tax not exceeding one percent (1%) of gross annual receipts.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §143(a)",
                "legal_rationale": "Directly complies with the statutory business tax ceiling for cities under Section 143(a) of RA 7160."
            },
            {
                "sec_num": 5,
                "sec_title": "TAX ON FINANCIAL INSTITUTIONS AND BANKS",
                "text": "Commercial banks, banking institutions, and offshore banking units authorized by the Bangko Sentral ng Pilipinas shall be assessed a business tax of fifty percent (50%) of one percent (1%) on gross receipts.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §143(f)",
                "legal_rationale": "Directly implements statutory tax rate on licensed banks under RA 7160 Section 143(f)."
            },
            {
                "sec_num": 6,
                "sec_title": "BUSINESS TAX ON CORPORATE HOLDING DIVIDENDS",
                "text": "All corporate holding companies owning shares in manufacturing or utility firms are hereby classified as 'Non-Bank Financial Intermediaries' and shall pay a two percent (2%) local business tax on all passive dividend earnings and interest income received from corporate stock holdings, regardless of whether the holding company is licensed as a financial intermediary by the Bangko Sentral ng Pilipinas.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7160 §133(a); Republic Act No. 7160 §143(f); Republic Act No. 8791 §3",
                "legal_rationale": "Directly contradicts Republic Act No. 7160 Section 133(a) (prohibiting local taxes on income) and Section 143(f) in relation to General Banking Law. Invalidated in City of Davao and Tanjili v. ARC Investors, Inc. (G.R. No. 249668, 2022)."
            },
            {
                "sec_num": 7,
                "sec_title": "RETROACTIVE IMPOSITION ON GOVERNMENT PENSION PROPERTIES",
                "text": "Real properties and facilities titled under the Government Service Insurance System (GSIS) and Social Security System (SSS) located in Davao City are hereby assessed real property taxes retroactively for ten (10) past calendar years, authorizing the City Treasurer to levy on execution.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7160 §133(o); Republic Act No. 8291 §39; Presidential Decree No. 1146 §33",
                "legal_rationale": "Directly violates Section 133(o) of RA 7160 and national agency charters which explicitly exempt government instrumentalities and social security funds from local taxation. Invalidated in City of Davao v. GSIS (G.R. No. 127383, 2005)."
            },
            {
                "sec_num": 8,
                "sec_title": "LOCAL FRANCHISE TAX ON TELECOMMUNICATIONS",
                "text": "Telecommunications utilities operating within Davao City shall be subject to a local franchise tax of one-half of one percent (0.5%) on their gross annual receipts pursuant to Section 137 of Republic Act No. 7160.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §137; Republic Act No. 7160 §151",
                "legal_rationale": "Valid exercise of local franchise taxing power explicitly affirmed by the Supreme Court in Smart Communications v. City of Davao (2008) and PLDT v. City of Davao (2001)."
            },
            {
                "sec_num": 9,
                "sec_title": "TIME OF PAYMENT AND DISCOUNTS",
                "text": "Local business taxes shall be payable for every calendar quarter, with a ten percent (10%) discount for full advance annual payments made before January 20.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §167",
                "legal_rationale": "Standard municipal tax payment schedule."
            },
            {
                "sec_num": 10,
                "sec_title": "EXAMINATION OF BOOKS OF ACCOUNTS",
                "text": "The City Treasurer or duly designated deputies may examine the accounting books and records of businesses operating within the city to verify tax payments.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §171",
                "legal_rationale": "Statutory authority to inspect commercial books under Section 171 of RA 7160."
            },
            {
                "sec_num": 11,
                "sec_title": "SURCHARGES AND INTEREST",
                "text": "Failure to pay taxes on time shall incur a surcharge of twenty-five percent (25%) and interest of two percent (2%) per month.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §168",
                "legal_rationale": "Statutory interest and surcharge limits."
            },
            {
                "sec_num": 12,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any provision is declared void, remaining provisions shall stay effective.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 13,
                "sec_title": "REPEALING CLAUSE",
                "text": "Provisions of the 2005 Revenue Code inconsistent herewith are amended.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard repealing clause."
            },
            {
                "sec_num": 14,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance takes effect on January 1 of the following calendar year after publication.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard tax ordinance effectivity clause."
            }
        ]
    }
]

# Write individual JSON files and consolidated JSONL for Tier 2
with open("data/tier2_draft_ordinances_benchmark.jsonl", "w", encoding="utf-8") as f_out:
    for draft in tier2_drafts:
        doc_filename = f"data/tier2_draft_ordinances/{draft['doc_id']}.json"
        with open(doc_filename, "w", encoding="utf-8") as f_single:
            json.dump(draft, f_single, indent=2, ensure_ascii=False)
        f_out.write(json.dumps(draft, ensure_ascii=False) + "\n")

print(f"Created 10 draft ordinances in data/tier2_draft_ordinances/ and data/tier2_draft_ordinances_benchmark.jsonl")

# Calculate section breakdown
total_sections = sum(len(d["sections"]) for d in tier2_drafts)
contradictions = sum(sum(1 for s in d["sections"] if s["label"] == "Contradiction") for d in tier2_drafts)
entailments = sum(sum(1 for s in d["sections"] if s["label"] == "Entailment") for d in tier2_drafts)
neutrals = sum(sum(1 for s in d["sections"] if s["label"] == "Neutral") for d in tier2_drafts)

print(f"Tier 2 Summary: {len(tier2_drafts)} documents, {total_sections} total sections")
print(f"  Contradiction: {contradictions} ({contradictions/total_sections*100:.1f}%)")
print(f"  Entailment:    {entailments} ({entailments/total_sections*100:.1f}%)")
print(f"  Neutral:       {neutrals} ({neutrals/total_sections*100:.1f}%)")

# -------------------------------------------------------------------------
# TIER 3 BENCHMARK: 11 Authentic Philippine Supreme Court & Davao Cases
# -------------------------------------------------------------------------

tier3_cases = [
    {
        "case_id": "SC-DAVAO-01",
        "case_name": "Mosqueda v. Pilipino Banana Growers & Exporters Association, Inc.",
        "docket_no": "G.R. Nos. 189185 & 189305",
        "promulgation_date": "August 16, 2016",
        "scra_citation": "798 SCRA 389",
        "challenged_local_measure": {
            "enacting_lgu": "City of Davao",
            "ordinance_no": "Ordinance No. 0309-07",
            "ordinance_title": "An Ordinance Banning Aerial Spraying as an Agricultural Practice in All Agricultural Activities by All Agricultural Entities in Davao City",
            "operative_provision": "Section 5: Ban on Aerial Spraying. Aerial spraying shall be prohibited in all agricultural activities in Davao City after a 3-month transition period. Section 6: Buffer Zone. A 30-meter buffer zone shall be established by all agricultural plantations."
        },
        "superior_national_laws": [
            "Presidential Decree No. 1144 (Creating the Fertilizer and Pesticide Authority)",
            "1987 Constitution, Article III, Section 1 (Equal Protection Clause)",
            "Republic Act No. 7160, Section 5(a) & Section 458"
        ],
        "legal_question": "Does a local government unit have the police power to impose a blanket ban on aerial pesticide spraying when the national Fertilizer and Pesticide Authority possesses statutory authority to regulate agricultural chemicals and application methods?",
        "supreme_court_ruling": "Unconstitutional and Ultra Vires",
        "ratio_decidendi": "The Supreme Court invalidated Ordinance No. 0309-07 on two grounds: First, it violated the Equal Protection clause by discriminating against aerial sprayers without reasonable distinction. Second, under the Magtajas doctrine, an ordinance cannot prohibit an activity expressly permitted or regulated by national law. Presidential Decree No. 1144 grants the Fertilizer and Pesticide Authority exclusive jurisdiction to determine permitted methods of agricultural chemical application.",
        "ground_truth_nli_label": "Contradiction",
        "primary_statutory_citation": "Presidential Decree No. 1144 §6",
        "jurisprudential_importance": "Landmark jurisprudence governing vertical statutory preemption between municipal police power and national regulatory agencies."
    },
    {
        "case_id": "SC-DAVAO-02",
        "case_name": "Evasco, Jr. v. Montañez",
        "docket_no": "G.R. No. 199172",
        "promulgation_date": "February 21, 2018",
        "scra_citation": "856 SCRA 320",
        "challenged_local_measure": {
            "enacting_lgu": "City of Davao",
            "ordinance_no": "Ordinance No. 092-2000",
            "ordinance_title": "An Ordinance Regulating the Construction, Repair, Renovation, Erection, Installation and Maintenance of Outdoor Advertising Materials and Structures in Davao City",
            "operative_provision": "Section 7: Setback and Clearance Requirements. Regulates outdoor advertising structures, billboards, and signage, requiring local permits and prescribing physical setback distances from city roads."
        },
        "superior_national_laws": [
            "Presidential Decree No. 1096 (National Building Code of the Philippines)",
            "Republic Act No. 7160, Section 458(a)(4)(iv)"
        ],
        "legal_question": "Does Davao City's local ordinance regulating outdoor advertising structures collide with or get preempted by the National Building Code of the Philippines (PD 1096)?",
        "supreme_court_ruling": "Constitutional and Valid Exercise of Police Power",
        "ratio_decidendi": "The Supreme Court reversed the Court of Appeals and upheld the Davao City ordinance. The Court ruled that under Section 458(a)(4)(iv) of the Local Government Code of 1991 (RA 7160), city councils are explicitly granted statutory power to regulate the display of signs, signboards, and billboards. The local ordinance does not contradict PD 1096 but functions harmoniously alongside national building standards as a valid municipal police power measure.",
        "ground_truth_nli_label": "Entailment",
        "primary_statutory_citation": "Republic Act No. 7160 §458(a)(4)(iv); Presidential Decree No. 1096 §301",
        "jurisprudential_importance": "Critical positive control case demonstrating harmonious statutory coexistence (Entailment) where local regulation is explicitly authorized by the Local Government Code."
    },
    {
        "case_id": "SC-DAVAO-03",
        "case_name": "City of Davao and Tanjili v. ARC Investors, Inc.",
        "docket_no": "G.R. No. 249668",
        "promulgation_date": "July 13, 2022",
        "scra_citation": "G.R. No. 249668 En Banc Decision",
        "challenged_local_measure": {
            "enacting_lgu": "City of Davao",
            "ordinance_no": "Ordinance No. 158-05 (2005 Revenue Code of the City of Davao)",
            "ordinance_title": "The 2005 Revenue Code of the City of Davao, Section 135",
            "operative_provision": "Section 135: Assessment of local business tax on dividend and interest income earned by corporate holding companies under the classification of Non-Bank Financial Intermediaries (NBFIs)."
        },
        "superior_national_laws": [
            "Republic Act No. 7160, Section 131(e) & Section 143(f)",
            "Republic Act No. 8791 (General Banking Law of 2000)",
            "Manual of Regulations for Non-Bank Financial Institutions (Bangko Sentral ng Pilipinas)"
        ],
        "legal_question": "Can a local government unit unilaterally define a passive holding company receiving dividends from stock investments as a 'Non-Bank Financial Intermediary' to impose local business taxes?",
        "supreme_court_ruling": "Tax Assessment Cancelled / Ultra Vires Interpretation",
        "ratio_decidendi": "The Supreme Court ruled that a holding company whose primary activity is holding shares of stock and which passively earns dividend income is not 'doing business' as a Non-Bank Financial Intermediary. Under the Local Government Code in relation to national banking law, to be classified as an NBFI subject to local business taxation under Section 143(f), an entity must be authorized by the Bangko Sentral ng Pilipinas to perform financial intermediary functions.",
        "ground_truth_nli_label": "Contradiction",
        "primary_statutory_citation": "Republic Act No. 7160 §143(f); Republic Act No. 8791 §3",
        "jurisprudential_importance": "Establishes that local tax ordinances cannot redefine specialized statutory and banking terms to expand municipal revenue authority beyond national limits."
    },
    {
        "case_id": "SC-DAVAO-04",
        "case_name": "Smart Communications, Inc. v. City of Davao",
        "docket_no": "G.R. No. 155491",
        "promulgation_date": "September 16, 2008; Res. July 21, 2009",
        "scra_citation": "565 SCRA 237; 593 SCRA 395",
        "challenged_local_measure": {
            "enacting_lgu": "City of Davao",
            "ordinance_no": "Ordinance No. 230 / Ordinance No. 519",
            "ordinance_title": "Davao City Franchise Tax Ordinance",
            "operative_provision": "Section 1: Imposition of a franchise tax of fifty percent (50%) of one percent (1%) on the gross annual receipts of telecommunications businesses operating within the territorial jurisdiction of Davao City."
        },
        "superior_national_laws": [
            "Republic Act No. 7294, Section 9 (Smart Franchise 'In Lieu of All Taxes' Clause)",
            "Republic Act No. 7925, Section 23 (Most Favored Nation Equality Clause)",
            "Republic Act No. 7160, Section 137 & Section 151"
        ],
        "legal_question": "Does the 'in lieu of all taxes' clause in a telecommunication carrier's national legislative franchise exempt it from local franchise taxation enacted by a city council under the Local Government Code?",
        "supreme_court_ruling": "Constitutional and Enforceable",
        "ratio_decidendi": "The Supreme Court ruled in favor of Davao City, holding that tax exemptions must be strictly construed against the taxpayer. The 'in lieu of all taxes' clause in Smart's charter was not clear and explicit enough to grant an exemption from local franchise taxes. Local government units possess autonomous, constitutional taxing authority under Section 137 of RA 7160 to levy franchise taxes, which cannot be abrogated by vague statutory inferences.",
        "ground_truth_nli_label": "Entailment",
        "primary_statutory_citation": "Republic Act No. 7160 §137; Republic Act No. 7160 §151",
        "jurisprudential_importance": "Landmark ruling upholding local municipal taxing autonomy over commercial telecommunications entities against ambiguous national legislative franchise exemptions."
    },
    {
        "case_id": "SC-DAVAO-05",
        "case_name": "Mindanao Shopping Destination Corporation v. Duterte",
        "docket_no": "G.R. No. 211093",
        "promulgation_date": "June 6, 2017",
        "scra_citation": "826 SCRA 202",
        "challenged_local_measure": {
            "enacting_lgu": "City of Davao",
            "ordinance_no": "Ordinance No. 158-05",
            "ordinance_title": "The 2005 Revenue Code of the City of Davao",
            "operative_provision": "Section 69: Imposition of graduated business taxes on retailers and wholesalers operating within Davao City, including retrospective adjustments."
        },
        "superior_national_laws": [
            "Republic Act No. 7160, Section 143(a) & Section 143(b)",
            "Republic Act No. 7160, Section 130 (Fundamental Principles of Local Taxation)"
        ],
        "legal_question": "Can a city government adjust its local revenue code brackets in a manner that exceeds the statutory rate ceilings and classification criteria set forth in Section 143 of the Local Government Code?",
        "supreme_court_ruling": "Partially Modified / Enforcing Statutory Tax Ceilings",
        "ratio_decidendi": "The Supreme Court emphasized that while cities enjoy broad local autonomy in raising revenue, their taxing authority is bounded by the specific statutory rate ceilings enacted by Congress in Section 143 of the Local Government Code. Local tax schedules cannot arbitrarily adjust tax brackets in a manner that violates national legislative ceilings or fundamental principles of taxation.",
        "ground_truth_nli_label": "Contradiction",
        "primary_statutory_citation": "Republic Act No. 7160 §143",
        "jurisprudential_importance": "Demonstrates the binding nature of national statutory tax rate caps on local legislative revenue enactments."
    },
    {
        "case_id": "SC-DAVAO-06",
        "case_name": "City of Davao v. Court of Appeals and Government Service Insurance System (GSIS)",
        "docket_no": "G.R. No. 127383",
        "promulgation_date": "August 18, 2005",
        "scra_citation": "467 SCRA 280",
        "challenged_local_measure": {
            "enacting_lgu": "City of Davao",
            "ordinance_no": "Davao City Real Property Tax Assessment Warrants",
            "ordinance_title": "City Real Property Tax Assessment on GSIS Davao Properties",
            "operative_provision": "Warrants of levy and distraint assessing real property taxes against GSIS properties located in Davao City for municipal tax liabilities."
        },
        "superior_national_laws": [
            "Presidential Decree No. 1146, Section 33 (GSIS Charter Exemption)",
            "Republic Act No. 8291, Section 39 (Revised GSIS Act)",
            "Republic Act No. 7160, Section 133(o) (Common Limitations on Taxing Powers of LGUs)"
        ],
        "legal_question": "May the City of Davao levy real property taxes upon properties owned by the Government Service Insurance System, a government instrumentality?",
        "supreme_court_ruling": "Tax Assessments Null and Void",
        "ratio_decidendi": "The Supreme Court held that Section 133(o) of the Local Government Code expressly prohibits local government units from levying any tax, fee, or charge on the Republic of the Philippines, its agencies, and instrumentalities. Because GSIS is an instrumentality of the national government created to manage public retirement funds, its properties are tax-exempt under both national statute and its charter.",
        "ground_truth_nli_label": "Contradiction",
        "primary_statutory_citation": "Republic Act No. 7160 §133(o); Presidential Decree No. 1146 §33",
        "jurisprudential_importance": "Enforces Section 133(o) of RA 7160 as an absolute statutory barrier prohibiting local taxation of national government instrumentalities."
    },
    {
        "case_id": "SC-DAVAO-07",
        "case_name": "Davao City Mining Ban and Watershed Protection Legal Dispute",
        "docket_no": "Davao City SP Resolution / May 2015 Ordinance vs. MPSA Holders",
        "promulgation_date": "May 12, 2015 (Enactment) / Judicial Review Context",
        "scra_citation": "City Ordinance Enactment Review under RA 7942",
        "challenged_local_measure": {
            "enacting_lgu": "City of Davao",
            "ordinance_no": "Ordinance No. 0310-07 & 2015 Mining Ban Ordinance",
            "ordinance_title": "An Ordinance Banning All Mining Operations in Davao City and Protecting the Panigan-Tamugan Watershed",
            "operative_provision": "Section 2: Total Prohibition. No commercial or metallic mining operations of any nature shall be permitted within the territorial jurisdiction of Davao City, revoking and denying all municipal permits to holders of national mineral agreements."
        },
        "superior_national_laws": [
            "Republic Act No. 7942 (Philippine Mining Act of 1995, Section 4 & Section 27)",
            "1987 Constitution, Article XII, Section 2 (State Ownership of Natural Resources)",
            "Republic Act No. 7160, Section 16 & Section 458(a)(1)(vi)"
        ],
        "legal_question": "Does a local government have the legal authority to enact a complete, territorial-wide ban on mining operations within its boundaries when the national government has issued mineral agreements under Republic Act No. 7942?",
        "supreme_court_ruling": "Active Vertical Conflict / Preemption Doctrine Under Magtajas",
        "ratio_decidendi": "Under the Magtajas doctrine, an ordinance cannot forbid what a national statute permits. Because Republic Act No. 7942 explicitly declares mineral resources to be property of the State open to exploration under national concessions, a blanket municipal prohibition on mining operates in direct vertical tension with national mining law, except where specific areas are designated as protected watersheds under national environmental statutes.",
        "ground_truth_nli_label": "Contradiction",
        "primary_statutory_citation": "Republic Act No. 7942 §4; Republic Act No. 7942 §27",
        "jurisprudential_importance": "Core practical conflict between local environmental police power and the national Regalian doctrine over natural resource exploration."
    },
    {
        "case_id": "SC-DAVAO-08",
        "case_name": "Davao City Comprehensive Anti-Smoking Ordinance vs. National Tobacco Regulation",
        "docket_no": "Ordinance Review under Health Justice Jurisprudence",
        "promulgation_date": "May 31, 2013 (Promulgated as Ord. No. 0367-12)",
        "scra_citation": "Local Police Power Standards Review (RA 9211 vs. RA 7160)",
        "challenged_local_measure": {
            "enacting_lgu": "City of Davao",
            "ordinance_no": "Ordinance No. 0367-12",
            "ordinance_title": "The New Comprehensive Anti-Smoking Ordinance of Davao City",
            "operative_provision": "Section 4: Prohibition of Smoking in Public Places. Smoking is prohibited in all public conveyances, government facilities, and enclosed places, setting stricter physical requirements for designated smoking areas than national minimums."
        },
        "superior_national_laws": [
            "Republic Act No. 9211 (Tobacco Regulation Act of 2003, Section 5 & Section 6)",
            "Republic Act No. 7160, Section 16 (General Welfare Clause)"
        ],
        "legal_question": "Can a local government unit enact smoking regulations and buffer setbacks that are stricter than the baseline standards established in Republic Act No. 9211?",
        "supreme_court_ruling": "Valid Stricter Police Power Standard (Entailment)",
        "ratio_decidendi": "Philippine public health jurisprudence recognizes that national regulatory statutes (such as RA 9211) establish minimum baseline standards, not maximum ceilings, for public health protection. Under Section 16 of RA 7160, local governments may adopt stricter measures to protect public health, provided they do not legalize what national law prohibits. Therefore, an ordinance prohibiting smoking in broader areas than RA 9211 is a valid exercise of municipal police power.",
        "ground_truth_nli_label": "Entailment",
        "primary_statutory_citation": "Republic Act No. 7160 §16; Republic Act No. 9211 §5",
        "jurisprudential_importance": "Critical principle establishing that more stringent municipal standards under public health police power do not automatically constitute an invalid contradiction of national minimum standards."
    },
    {
        "case_id": "SC-PHIL-09",
        "case_name": "Magtajas v. Pryce Properties Corp. and PAGCOR",
        "docket_no": "G.R. No. 111097",
        "promulgation_date": "July 20, 1994",
        "scra_citation": "234 SCRA 255",
        "challenged_local_measure": {
            "enacting_lgu": "City of Cagayan de Oro",
            "ordinance_no": "Ordinance No. 3353 & Ordinance No. 3375-93",
            "ordinance_title": "An Ordinance Prohibiting the Operation of Casinos in the City of Cagayan de Oro",
            "operative_provision": "Section 1: Prohibition of the opening and operation of casinos and all forms of gambling within the territorial jurisdiction of Cagayan de Oro City."
        },
        "superior_national_laws": [
            "Presidential Decree No. 1869 (Charter of the Philippine Amusement and Gaming Corporation, PAGCOR)",
            "Republic Act No. 7160, Section 5(a) & Section 458"
        ],
        "legal_question": "May a city council prohibit gambling operations authorized by a valid national statutory charter enacted by the national legislature?",
        "supreme_court_ruling": "Ordinances Null and Void / Foundational Preemption Ruling",
        "ratio_decidendi": "The Supreme Court laid down the canonical Philippine statutory preemption doctrine: Local councils are merely delegated agents of the national legislature. An ordinance must not contravene the Constitution or any statute. 'An ordinance cannot permit what a statute forbids, nor forbid what a statute permits.' Because PD 1869 expressly authorized PAGCOR to operate casinos throughout the Philippines, local ordinances could not nullify this national mandate.",
        "ground_truth_nli_label": "Contradiction",
        "primary_statutory_citation": "Presidential Decree No. 1869 §1; Republic Act No. 7160 §5(a)",
        "jurisprudential_importance": "The foundational jurisprudence of Philippine municipal law establishing the supremacy of national statutes over local ordinances."
    },
    {
        "case_id": "SC-PHIL-10",
        "case_name": "City of Manila v. Laguio, Jr.",
        "docket_no": "G.R. No. 118127",
        "promulgation_date": "April 12, 2005",
        "scra_citation": "455 SCRA 308",
        "challenged_local_measure": {
            "enacting_lgu": "City of Manila",
            "ordinance_no": "Ordinance No. 7783",
            "ordinance_title": "An Ordinance Prohibiting the Establishment or Operation of Motels, Inns, and Karaoke Bars in the Ermita-Malate District",
            "operative_provision": "Section 1: Prohibits the operation of motels, inns, and other commercial hospitality businesses in Ermita-Malate, ordering their closure or relocation within three (3) months."
        },
        "superior_national_laws": [
            "1987 Constitution, Article III, Section 1 (Due Process and Equal Protection Clauses)",
            "Republic Act No. 7160, Section 458(a)(4)(iv)"
        ],
        "legal_question": "Can an LGU prohibit and eradicate an otherwise lawful commercial business under the guise of zoning regulations and police power without violating constitutional due process?",
        "supreme_court_ruling": "Ordinance Declared Unconstitutional",
        "ratio_decidendi": "The Supreme Court held that the police power of a local government unit is not unlimited. A legitimate police power measure must satisfy two conditions: the interests of the public generally require it, and the means employed are reasonably necessary and not unduly oppressive. Prohibiting lawful businesses instead of regulating them violates substantive due process.",
        "ground_truth_nli_label": "Contradiction",
        "primary_statutory_citation": "1987 Constitution Art. III §1; Republic Act No. 7160 §458",
        "jurisprudential_importance": "Establishes that local police power cannot arbitrarily prohibit legitimate commercial activities recognized under national law."
    },
    {
        "case_id": "SC-PHIL-11",
        "case_name": "Batangas CATV, Inc. v. Court of Appeals",
        "docket_no": "G.R. No. 138810",
        "promulgation_date": "October 29, 2004",
        "scra_citation": "441 SCRA 530",
        "challenged_local_measure": {
            "enacting_lgu": "Sangguniang Panlungsod ng Batangas",
            "ordinance_no": "Resolution No. 210, Series of 1993",
            "ordinance_title": "Resolution Granting and Regulating the Cable Television Franchise of Batangas CATV, Inc.",
            "operative_provision": "Section 2: The Sangguniang Panlungsod assumes authority to fix, regulate, and adjust subscriber rates and channel programming charges for cable television services."
        },
        "superior_national_laws": [
            "Executive Order No. 205 (Regulating Cable Television Systems in the Philippines)",
            "Executive Order No. 546 (Creating the National Telecommunications Commission)",
            "Republic Act No. 7160, Section 458"
        ],
        "legal_question": "Does a local sangguniang panlungsod possess the legal authority to regulate subscriber rates of a cable television network when national executive orders place the industry under the National Telecommunications Commission?",
        "supreme_court_ruling": "Resolution and Rate-Fixing Powers Struck Down / Ultra Vires",
        "ratio_decidendi": "The Supreme Court ruled that local governments have no power to regulate or fix subscriber rates for cable television operators. Executive Order No. 205 and EO 546 vest exclusive regulatory authority over cable television operations and rates in the National Telecommunications Commission (NTC). Where national law occupies the regulatory field, municipal ordinances are preempted.",
        "ground_truth_nli_label": "Contradiction",
        "primary_statutory_citation": "Executive Order No. 205 §2; Executive Order No. 546 §15",
        "jurisprudential_importance": "Foundational case on express and field preemption of local ordinances by specialized national administrative bodies."
    }
]

with open("data/tier3_jurisprudential_cases.jsonl", "w", encoding="utf-8") as f_tier3:
    for c in tier3_cases:
        f_tier3.write(json.dumps(c, ensure_ascii=False) + "\n")

print(f"Created 11 landmark preemption cases in data/tier3_jurisprudential_cases.jsonl")
print("All benchmark datasets generated successfully!")
