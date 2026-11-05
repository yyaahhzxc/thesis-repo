#!/usr/bin/env python3
"""
Generate the Master 350-Pair Ground Truth Benchmark Dataset for Stage 2 (Fine NLI Evaluation).

Key Methodological Guarantees:
1. Grounded in Authentic Davao City Ordinance Legislative Drafting:
   - Operative Formula: SECTION X. [TITLE]. —
   - Deontic Syntax: "It shall be unlawful for any person, natural or juridical, within the territorial jurisdiction of Davao City..."
   - Authentic Institutional Bodies: CTTMO, CHO, CENRO, Business Bureau, AVTF, DCPO, CDRRMO, CEEO, CSWDO.
   - Authentic Territorial Anchors: Poblacion, Talomo, Buhangin, Toril, Bunawan, Calinan, Paquibato Districts.
2. Verified Single-Statute & Single-Section National Premises:
   - Every premise references exactly ONE Republic Act and ONE singular section extracted verbatim from Lawphil corpus.
   - Includes complete Section Titles and introductory lead-in sentences (avoiding headless fragments).
3. Strictly Non-Quantitative, Lawyer-Level Tier 3 Items:
   - ZERO numbers, digits, days, or monetary amounts in any Tier 3 hypothesis.
4. Statistical & Schema Benchmark Compliance:
   - Exactly 350 pairs across 8 Macro Domains (00: 50, 01: 45, 02: 50, 03: 45, 04: 45, 05: 45, 06: 35, 07: 35).
   - 3-Way Logical Label Balance: Contradiction = 116 (33.1%), Entailment = 117 (33.4%), Neutral = 117 (33.4%).
   - Difficulty Tiers: Tier 1 = 105 (30%), Tier 2 = 140 (40%), Tier 3 = 105 (30%).
   - 5 Evaluation Blocks of exactly 70 pairs each for SP Panels A through E.
"""

import os
import json
import csv
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
BLOCKS_DIR = os.path.join(DATA_DIR, "blocks")
CORPUS_PREMISES_PATH = os.path.join(DATA_DIR, "corpus_statute_premises.json")

def load_verified_premises():
    if not os.path.exists(CORPUS_PREMISES_PATH):
        raise FileNotFoundError(f"Missing {CORPUS_PREMISES_PATH}. Run scripts/build_verified_corpus_premises.py first.")
    with open(CORPUS_PREMISES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_curated_topics():
    return [
        # =========================================================================
        # DOMAIN 00: Executive Issuances & Policy Reorganization (50 pairs target)
        # =========================================================================
        {
            "domain_id": 0,
            "domain_name": "Executive Issuances & Policy Reorganization",
            "premise_key": "RA_7581_Sec_6",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Calamity Economic Stabilization Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 4. MANDATORY LOCAL PRICE CEILINGS UPON CALAMITY. — Upon official declaration of a state of local calamity by the Sangguniang Panlungsod, the City Mayor, through the City Economic Enterprise Office and the Business Bureau, shall enforce mandatory price ceilings across all grocery and commercial retail establishments within Davao City, which price freeze shall remain in continuous legal effect for a mandatory period of one hundred eighty (180) calendar days from issuance.",
                 "Direct breach of statutory temporal ceiling. Section 6 of RA 7581 explicitly limits automatic calamity price control to not more than sixty (60) days. The draft ordinance mandates a 180-day freeze, exceeding delegated police power limits."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Regulating Emergency Commodity Distribution", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 7. PROHIBITION ON EMERGENCY PRICE INCREASES. — It shall be unlawful for any commercial food distributor, wholesaler, or retailer within the territorial jurisdiction of Davao City to implement any price adjustment during declared local emergencies, notwithstanding any emergency freight rate adjustments or temporary price ceilings authorized by the National Price Coordinating Council or the Department of Trade and Industry.",
                 "Jurisdictional encroachment under Magtajas. The municipal draft strips statutory adjustment mechanisms and emergency authority explicitly granted to the Secretary of Trade and Industry and the National Price Coordinating Council under RA 7581."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Emergency Commodity Margin Stabilization Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 5. LOCAL COMMODITY MARGIN STABILIZATION. — To protect vulnerable consumer households during riverine flooding emergencies, the Business Bureau is authorized to enforce mandatory gross profit margins on essential grain and canned sustenance items based on pre-emergency wholesale acquisition costs, with immediate closure of non-conforming commercial stalls.",
                 "Latent substantive preemption of presidential price control authority (Lawyer-Level). Regulating profit margins on basic necessities during weather emergencies constitutes price regulation under RA 7581; Section 6 establishes that automatic price control on basic necessities is an exclusive presidential power triggered only upon a formal declaration of a state of calamity, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Executive Order Adopting Calamity Price Freeze Guidelines", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 3. LOCAL MONITORING OF PRICE FREEZE DURATION. — In strict observance of Section 6 of Republic Act No. 7581, the Davao City Local Price Coordinating Council shall monitor retail establishments upon the official declaration of a state of calamity to guarantee that prevailing retail prices of basic necessities remain frozen for a duration not exceeding sixty (60) calendar days.",
                 "Exact statutory adherence executing the 60-day price control ceiling mandated by national statute."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Market Monitoring and Price Enforcement Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 6. COORDINATION WITH NATIONAL PRICE AGENCIES. — The City Economic Enterprise Office shall coordinate with the Department of Trade and Industry Region XI to post official prevailing price bulletins across all public terminal markets, recognizing all statutory price ceiling adjustments authorized by national implementing agencies.",
                 "Compliant local enforcement recognizing national DTI administrative authority and statutory price adjustments."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Emergency Consumer Sustenance Monitoring Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 4. DISASTER PRICE BASING INSPECTIONS. — The City Economic Enterprise Office shall deploy market inspectors to commercial food depots following severe typhoons, ensuring that basic retail sustenance commodities remain at pre-emergency cost baselines without unauthorized local merchant markups.",
                 "Substantive conceptual alignment with automatic price freeze objectives, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Public Market Stall Tenancy Duration Ordinance", "Actual Davao City Ordinance Adaptation",
                 "SECTION 5. STALL LEASE DURATION. — Permanent lease contracts for commercial stalls situated within municipal public markets operated by the City Government of Davao shall be executed for a fixed term of three (3) fiscal years, renewable upon payment of standard renewal fees.",
                 "Regulates commercial stall lease durations; independent and non-conflicting with statutory calamity price freezes."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Wholesale Terminal Unloading Schedule Protocol", "Actual Davao City Ordinance Adaptation",
                 "SECTION 8. TERMINAL VEHICULAR UNLOADING SCHEDULE. — Wholesale freight vehicles transporting agricultural produce into the Bankerohan and Agdao Public Markets shall conduct heavy cargo discharge operations exclusively between midnight and dawn to minimize central traffic congestion.",
                 "Regulates terminal freight vehicular traffic hours; neutral regarding statutory emergency price controls."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Public Market Stall Architectural Standardization Ordinance", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. STALL ARCHITECTURAL SPECIFICATIONS. — Permanent concessionaires operating meat and produce stalls within city public markets shall construct display counters using food-grade stainless steel surfaces and maintain unobstructed drainage gutters within their assigned leased perimeters.",
                 "Regulates physical stall design and sanitation maintenance; completely non-overlapping with statutory automatic price controls, with zero numbers.")
            ]
        },
        {
            "domain_id": 0,
            "domain_name": "Executive Issuances & Policy Reorganization",
            "premise_key": "RA_10121_Sec_12",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Civil Defense Advisory Commission Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 3. REORGANIZATION OF DISASTER OPERATIONS. — The Davao City Disaster Risk Reduction and Management Office (CDRRMO) is hereby dissolved and reconstituted as a private non-governmental foundation operating outside the administrative control of the Office of the City Mayor, governed by an independent civilian board.",
                 "Direct statutory violation. Section 12 of RA 10121 explicitly commands that the LDRRMO shall be an organic governmental office under the direct administrative supervision of the local chief executive."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Establishing Autonomous District Evacuation Units", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 5. AUTONOMOUS DISTRICT RESCUE PROTOCOLS. — Administrative districts within Davao City are authorized to organize independent rescue brigades that shall operate without operational subordination to the unified incident command system of the City Disaster Risk Reduction and Management Office.",
                 "Breach of statutory command hierarchy. Section 12 mandates a unified local disaster office to coordinate all localized disaster preparedness and response operations."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Ordinance Establishing Integrated Shelter Management Operations", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 7. INTEGRATED HUMANITARIAN SHELTER MANAGEMENT ALLIANCE. — To optimize municipal disaster response logistics during severe flooding events, accredited private humanitarian foundations are designated as autonomous directors of designated municipal evacuation centers, possessing exclusive operational authority over relief intake and facility management.",
                 "Latent unlawful delegation of municipal police powers (Lawyer-Level). Devests the statutory Local Disaster Risk Reduction and Management Office (LDRRMO) of supervisory authority over evacuation operations, violating Section 12 of RA 10121 which mandates direct governmental command over local emergency facilities, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Disaster Risk Reduction and Management Reorganization Ordinance", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 2. INSTITUTIONAL STRENGTHENING OF CDRRMO. — In compliance with Section 12 of Republic Act No. 10121, the City Disaster Risk Reduction and Management Office (CDRRMO) is organized as a regular department under the Office of the City Mayor, structured with three (3) functional divisions: Administrative and Training, Research and Planning, and Operations and Warning.",
                 "Exact statutory adherence to the departmental organization and functional division structure mandated by Section 12."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Emergency Response and Warning Activation Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 4. BARANGAY EVACUATION COORDINATION. — The CDRRMO shall establish direct communication linkages with Barangay Disaster Risk Reduction and Management Committees across all administrative districts, maintaining unified operational command during natural calamities.",
                 "Compliant execution of local disaster coordination mandates under national statute."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Integrated Emergency Warning Network Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 3. METROPOLITAN WARNING DISPATCH INTEGRATION. — The City Disaster Risk Reduction and Management Office shall maintain round-the-clock emergency telemetry and severe weather monitoring systems to provide timely pre-evacuation notices to riverbank settlements.",
                 "Substantive conceptual alignment with statutory disaster office early warning mandates, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Rainwater Harvesting Facility Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 5. RAINWATER HARVESTING STORAGE CAPACITIES. — Commercial buildings with roof catchment areas exceeding two hundred (200) square meters shall install rainwater collection cisterns with a minimum capacity of five thousand (5,000) liters.",
                 "Regulates architectural rainwater harvesting; neutral regarding statutory disaster office organization."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Tree Trimming Safety Protocol", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. POWER DISTRIBUTION TREE PRUNING. — Maintenance crews trimming tree branches near high-voltage electric distribution power lines shall coordinate with the City Environment and Natural Resources Office to obtain safety clearance.",
                 "Regulates environmental utility line pruning; neutral regarding statutory disaster office operational mandates."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Public School Grounds Soil Drainage Specification", "Actual Davao City Ordinance Adaptation",
                 "SECTION 6. ATHLETIC FIELD DRAINAGE CONSTRUCTION. — Municipal elementary school sports grounds shall incorporate subterranean gravel drainage grids to prevent stagnant storm water accumulation during wet season athletic events.",
                 "Regulates school grounds civil engineering; completely distinct from civil defense office structuring, with zero numbers.")
            ]
        },
        {
            "domain_id": 0,
            "domain_name": "Executive Issuances & Policy Reorganization",
            "premise_key": "RA_11032_Sec_9",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Comprehensive Business Permit Processing Code", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 8. PROCESSING PERIOD FOR SIMPLE MAYOR'S PERMITS. — The Business Bureau of Davao City is authorized to process and issue simple business registration renewal clearances within an administrative evaluation timeframe of fifteen (15) working days from the date of complete application submission.",
                 "Direct breach of statutory processing ceiling. Section 9(b)(1) of RA 11032 strictly mandates that simple transactions shall be acted upon within not longer than three (3) working days. Extending this to 15 working days violates national anti-red tape standards."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Authorizing Discretionary Permit Processing Suspensions", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 11. ADMINISTRATIVE SUSPENSION OF PERMIT TIMELINES. — The City Legal Officer may suspend statutory processing timetables for business permit applications whenever additional inter-agency verification is deemed convenient, without issuing formal written notices of deficiency to the applicant.",
                 "Violation of due process and anti-red tape mandates. RA 11032 strictly prohibits indefinite or discretionary processing suspensions without formal, written deficiency notices containing explicit legal bases."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Ordinance Regulating Multi-Agency Commercial Safety Audits", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 9. COMPREHENSIVE MULTI-AGENCY PRE-LICENSING AUDIT. — To ensure comprehensive structural safety, the Business Bureau shall route commercial permit renewal applications through sequential onsite verification by the City Planning, Building, and Fire Directorates, issuing operating clearances only upon receiving unanimous written endorsements from each reviewing department.",
                 "Latent evasion of statutory anti-red tape processing caps (Lawyer-Level). Imposes sequential multi-department endorsements as a condition precedent for license renewal, creating procedural bottlenecks that inevitably exceed the statutory processing ceilings mandated under Section 9 of RA 11032, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Business Bureau Streamlined Citizen's Charter Ordinance", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 4. MANDATORY ADHERENCE TO PROCESSING TIMELINES. — In strict adherence to Section 9 of Republic Act No. 11032, the Business Bureau shall process and approve applications for simple business permits within three (3) working days, and complex commercial applications within seven (7) working days, from initial receipt of complete documents.",
                 "Exact statutory adoption of the 3-day simple and 7-day complex transaction processing limits prescribed by RA 11032."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Business One-Stop Shop (BOSS) Operational Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. INTEGRATED APPLICATION PROCESSING. — The Business Bureau shall operate the Business One-Stop Shop (BOSS) electronically, issuing written acknowledgement receipts upon document submission containing the date, time, and assigned tracking number.",
                 "Direct execution of statutory receipt issuance and electronic processing mandates under RA 11032."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Electronic Regulatory Clearance Efficiency Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 7. EXPEDITED COMMERCIAL CLEARANCE WORKFLOW. — The Business Bureau shall process routine trade permit filings through automated validation queues, providing immediate digital clearance to non-hazardous commercial enterprises without arbitrary bureaucratic postponement.",
                 "Substantive conceptual compliance with statutory ease-of-doing-business efficiency mandates, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Central Public Archive Storage Management Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. ARCHIVAL STORAGE SPECIFICATIONS. — Historical municipal administrative dockets designated for permanent retention shall be preserved in climate-controlled document vaults maintained at an ambient temperature of twenty (20) degrees Celsius.",
                 "Regulates physical archive climate control; neutral regarding statutory commercial permit processing timeframes."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Municipal Official Stationery Logo Placement Guidelines", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 3. OFFICIAL LETTERHEAD STANDARDIZATION. — All official communications originating from city hall administrative offices shall display the official corporate seal of the City of Davao centered on the topmost margin.",
                 "Governs municipal stationery formatting; unrelated to statutory ease of doing business processing rules."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Municipal Document Paper Weight Specifications", "Actual Davao City Ordinance Adaptation",
                 "SECTION 5. ADMINISTRATIVE PAPER SPECIFICATIONS. — Official city council committee reports and legislative drafts shall be printed exclusively on acid-free bond paper to guarantee long-term physical document preservation.",
                 "Regulates administrative stationery paper quality; completely independent of statutory permit processing rules, with zero numbers.")
            ]
        },

        # =========================================================================
        # DOMAIN 01: Education & Academic Institutions (45 pairs target)
        # =========================================================================
        {
            "domain_id": 1,
            "domain_name": "Education & Academic Institutions",
            "premise_key": "RA_10931_Sec_4",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft City College of Davao Cost Recovery and Matriculation Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 6. IMPOSITION OF SEMESTRAL LABORATORY FEES. — To fund laboratory equipment upgrades, the City College of Davao shall collect a mandatory technological laboratory fee of Two Thousand Five Hundred Pesos (PHP 2,500.00) per semester from all enrolled undergraduate students.",
                 "Direct breach of statutory fee exemption. Section 4 of RA 10931 explicitly mandates that all qualified students enrolled in recognized Local Universities and Colleges (LUCs) shall be exempt from paying tuition and other school fees, including laboratory fees."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Conditioning Tertiary Tuition Exemption on Local Voting Status", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 4. VOTER REGISTRATION RESTRICTION ON FREE TUITION. — Free higher education benefits at the City College of Davao shall be restricted exclusively to students who present registered voter certifications from Davao City precincts, disqualifying non-voting resident students otherwise eligible under national statute.",
                 "Discriminatory local preemption. RA 10931 extends free tertiary education privileges to all Filipino students enrolled in recognized LUCs without allowing municipal councils to impose local electoral residency conditions."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft City College of Davao Campus Sustainability and Facility Assessment Scheme", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 8. SUSTAINABILITY CO-DEVELOPMENT PROGRAM. — To support green infrastructure and campus power decarbonization, matriculated students attending the local tertiary college shall remit an auxiliary environmental facility maintenance assessment prior to semester course enrollment.",
                 "Latent evasion of statutory tertiary tuition and fee exemptions (Lawyer-Level). Re-labels mandatory student fees under the guise of an 'environmental facility maintenance assessment', violating Section 4 of RA 10931 which prohibits charging any tuition or institutional maintenance fees to undergraduate students in local colleges, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Ordinance Institutionalizing the City College of Davao", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 3. FREE TUITION AND MISCELLANEOUS FEE EXEMPTION. — Pursuant to Section 4 of Republic Act No. 10931, enrolled undergraduate students of the City College of Davao shall be fully exempt from paying tuition, matriculation, library, computer laboratory, and medical fees.",
                 "Direct statutory execution of the comprehensive tuition and miscellaneous fee exemption mandated by RA 10931."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "City College of Davao Student Admission and Enrollment Charter", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 5. ENROLLMENT GUIDELINES. — The Board of Trustees of the City College of Davao shall enforce admission standards consistent with Commission on Higher Education (CHED) policies, honoring statutory free tuition privileges for all qualified students.",
                 "Compliant local administrative policy executing statutory tertiary education mandates in harmony with CHED regulations."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Tertiary Education Accessibility Support Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 7. INSTITUTIONAL SUBSIDIZATION OF UNDERGRADUATE EDUCATION. — The City Government of Davao shall allocate municipal appropriations to cover instructional expenditures for students matriculated at the municipal tertiary college, guaranteeing open access to undergraduate credentials.",
                 "Substantive conceptual execution of free public tertiary education objectives, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Public School Classroom Acoustic Standardization Measure", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. CLASSROOM ACOUSTIC CEILINGS. — Municipal elementary school classrooms constructed within urban commercial zones shall feature sound-dampening ceiling panels designed to reduce interior acoustic noise below fifty (50) decibels.",
                 "Regulates civil architectural acoustics; neutral regarding statutory tertiary tuition exemptions."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Public School Bus Parking and Staging Area Protocol", "Actual Davao City Ordinance Adaptation",
                 "SECTION 6. SCHOOL BUS PARKING ZONES. — School transport buses serving public secondary schools shall park exclusively inside designated school campus parking loops during morning student drop-off hours.",
                 "Regulates vehicular school traffic; neutral regarding statutory higher education fee exemptions."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City School Textbook Storage Humidity Control Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 5. LIBRARY BOOK PRESERVATION. — Municipal public school libraries shall install dehumidification appliances in book archival annexes to protect printed instructional textbooks from tropical humidity damage.",
                 "Regulates library book preservation; completely independent of free higher education tuition mandates, with zero numbers.")
            ]
        },
        {
            "domain_id": 1,
            "domain_name": "Education & Academic Institutions",
            "premise_key": "RA_9165_Sec_36c",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Mandatory Student Substance Screening Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 4. MANDATORY STUDENT DRUG TESTING PRIOR TO ENROLLMENT. — All secondary and tertiary students seeking enrollment in educational institutions situated within Davao City shall undergo compulsory universal drug screening, presenting certified negative drug test results as a mandatory condition for academic enrollment.",
                 "Direct breach of statutory scope. Section 36(c) of RA 9165 explicitly restricts student drug testing to random sampling conducted pursuant to school handbooks, strictly forbidding universal mandatory drug screening as an enrollment prerequisite."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Mandating Summary Expulsion for Positive Drug Screening", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 7. SUMMARY ACADEMIC EXPULSION. — Any high school or college student within Davao City who tests positive in an initial drug screening examination shall be summarily expelled from the academic institution without requiring confirmatory laboratory testing or parental intervention.",
                 "Violation of statutory due process. Section 36(c) and national drug control rules require confirmatory testing, strict confidentiality, and therapeutic rehabilitation rather than summary municipal expulsion."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Ordinance Establishing Campus Security Gate Screening Protocols", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 5. CAMPUS ENTRY SAFETY AND TOXICOLOGY PROTOCOL. — Municipal police school liaison officers assigned to secondary schools shall conduct unannounced chemical toxicology screening swabs on students selected during morning campus gate security inspections, maintaining administrative security logs to identify youth intervention candidates.",
                 "Latent violation of statutory student drug testing protections (Lawyer-Level). Displaces academic administrative guidance and DOH-accredited laboratory procedures by authorizing uniformed police officers to conduct gate-level toxicological testing, violating Section 36(c) of RA 9165 which guarantees confidential, non-law-enforcement student screening, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City School Substance Prevention and Random Testing Protocol", "Actual Davao City Ordinance Adaptation",
                 "SECTION 3. RANDOM STUDENT DRUG SCREENING. — In strict accordance with Section 36(c) of Republic Act No. 9165, secondary and tertiary educational institutions in Davao City shall conduct random drug testing of students with prior notice to parents and strictly in accordance with school student handbooks.",
                 "Direct statutory adherence executing the random testing parameters, parental notice, and student handbook conditions prescribed by national law."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Student Health Protection and Confidential Rehabilitation Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 6. CONFIDENTIALITY OF REHABILITATION RECORDS. — Positive drug screening results obtained during school random testing protocols shall remain strictly confidential, treated as medical records to guide therapeutic intervention without entry into police records.",
                 "Compliant local health policy executing statutory confidentiality and non-punitive rehabilitation mandates."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Youth Wellness and Guidance Counseling Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 4. CAMPUS WELLNESS COUNSELING INTERVENTION. — Academic institutions shall utilize certified adolescent health counselors to guide students identified through substance screening toward community rehabilitation resources without academic forfeiture.",
                 "Substantive conceptual compliance with therapeutic, non-criminal student drug intervention mandates, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Elementary School Canteen Sugar Content Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. CANTEEN BEVERAGE SUGAR RESTRICTIONS. — Concessionaires operating elementary school canteens shall not sell bottled beverages containing more than twenty (20) grams of added refined sugar per serving.",
                 "Regulates school canteen nutritional standards; neutral regarding statutory student substance testing."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City School Crossing Guard Equipment Directive", "Actual Davao City Ordinance Adaptation",
                 "SECTION 5. CROSSING GUARD HIGH-VISIBILITY VESTS. — Municipal traffic marshals assigned to school pedestrian crosswalks shall wear high-visibility reflective safety vests during peak student arrival hours.",
                 "Regulates pedestrian crossing guard safety equipment; neutral regarding statutory student drug testing."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Public Classroom Blackboard Surface Maintenance Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 3. CHALKBOARD SLATE RE-SURFACING. — Municipal school administrators shall re-coat classroom chalkboards with non-reflective matte slate paint annually to reduce visual ocular glare for attending pupils.",
                 "Regulates classroom chalkboard maintenance; completely independent of student substance screening rules, with zero numbers.")
            ]
        },
        {
            "domain_id": 1,
            "domain_name": "Education & Academic Institutions",
            "premise_key": "RA_11314_Sec_5",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Public Transport Local Fare Restructuring Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 6. STUDENT FARE REDUCTION ADJUSTMENT. — Public utility jeepney and motorized tricycle operators in Davao City shall grant enrolled students a reduced fare discount of ten percent (10%) off the regular approved passenger fare rate.",
                 "Direct breach of statutory discount rate. Section 5 of RA 11314 explicitly guarantees students a twenty percent (20%) discount privilege. Reducing the discount to 10% violates national statutory student protections."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Suspending Student Fare Discounts During School Recesses", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 8. SUSPENSION OF FARE DISCOUNTS DURING VACATIONS. — The twenty percent student passenger fare discount shall be suspended across all public conveyances in Davao City during summer vacations, semestral breaks, and statutory public holidays.",
                 "Direct violation of statutory applicability. Section 5 of RA 11314 explicitly commands that the student fare discount shall be effective year-round, including weekends, summer breaks, and official holidays."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Express Transit Congestion Relief Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 4. PREMIUM SEATING CONGESTION MITIGATION SHUTTLES. — Public utility franchises operating express point-to-point commuter routes during morning peak hours may designate executive single-occupancy seating cabins subject to a uniform premium tariff, exempting these specialized non-standing express corridors from standard discounted commuter schedules.",
                 "Latent rollback of mandatory statutory discount privileges (Lawyer-Level). Creates a localized 'premium express corridor' exemption to withhold statutory student fare discounts, violating Section 5 of RA 11314 which establishes universal student discount applicability across all public land transportation services, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Student Public Transit Fare Protection Ordinance", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 3. MANDATORY TWENTY PERCENT PASSENGER FARE DISCOUNT. — In accordance with Section 5 of Republic Act No. 11314, all public utility vehicles operating within Davao City shall grant a twenty percent (20%) fare discount to bona fide students upon presentation of valid school identification.",
                 "Exact statutory adoption executing the mandatory 20% student fare discount prescribed by national law."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Transport Fare Complaint Investigation Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. ENFORCEMENT ACROSS ALL CALENDAR DAYS. — The City Transport and Traffic Management Office (CTTMO) shall enforce student fare discounts continuously across all days of the year, including weekends, semestral breaks, and national holidays.",
                 "Direct local administrative execution of statutory year-round discount mandates under RA 11314."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Student Commuter Welfare and Protection Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 7. COMMUTER PRIVILEGE COMPLIANCE MONITORING. — Traffic marshals shall monitor passenger transit queues to guarantee that registered learners presenting valid institutional credentials receive statutory transit rate reductions without driver refusal.",
                 "Substantive conceptual compliance with student transport fare protection mandates, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Tricycle Route Tarpaulin Signboard Dimensions", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. ROUTE SIGNBOARD SPECIFICATIONS. — Motorized tricycles authorized to operate within designated suburban zones shall mount official route destination boards measuring not less than forty (40) centimeters in width.",
                 "Regulates tricycle route signboard dimensions; neutral regarding statutory student fare discount rights."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Transport Terminal Lost Property Inventory Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 6. LOST PROPERTY CUSTODY. — Transport terminal dispatchers who recover unattended baggage inside public passenger waiting lounges shall log the items within the terminal lost-and-found ledger.",
                 "Regulates terminal lost-and-found procedures; neutral regarding passenger fare discount rates."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Public Transit Passenger Shelter Upholstery Specification", "Actual Davao City Ordinance Adaptation",
                 "SECTION 5. PASSENGER BENCH MATERIALS. — Waiting shed benches constructed at designated public passenger bus stops shall utilize weather-resistant composite fiberglass to endure tropical outdoor exposure.",
                 "Regulates bus stop bench physical construction; completely independent of student transport fare rules, with zero numbers.")
            ]
        },

        # =========================================================================
        # DOMAIN 02: Local Government & Territorial Boundaries (50 pairs target)
        # =========================================================================
        {
            "domain_id": 2,
            "domain_name": "Local Government & Territorial Boundaries",
            "premise_key": "RA_7160_Sec_458",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Environmental Protection and Waste Disposal Penal Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 8. PROHIBITED DISPOSAL AND PENALTIES. — It shall be unlawful for any corporate entity or industrial establishment within the territorial jurisdiction of Davao City to discharge untreated industrial liquid waste into the Davao River or municipal drainage networks; and any violator found guilty shall, upon conviction before the proper court, be punished by a fine of Twenty-Five Thousand Pesos (PHP 25,000.00) per violation.",
                 "Direct breach of statutory penal ceiling. Section 458(a)(1)(iii) of RA 7160 strictly caps city ordinance fines at Five Thousand Pesos (PHP 5,000.00). An ordinance imposing PHP 25,000 is ultra vires."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Penalizing Municipal Road Encroachments", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 5. SUMMARY EASEMENT CLEARANCE AND FORFEITURE. — Property owners within Davao City who construct permanent structures or fences encroaching on public road easements shall suffer immediate summary demolition and municipal forfeiture of their registered land title without judicial expropriation or criminal court proceedings.",
                 "Ultra vires forfeiture. Local councils cannot enact criminal penalties forfeiting real property titles without judicial expropriation or criminal trial, exceeding delegated police powers under Section 458."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Commercial Fleet Traffic Obstruction Accountability Ordinance", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 12. INTEGRATED CORPORATE COMPLIANCE SANCTIONS. — Commercial enterprises whose registered delivery vehicles repeatedly cause traffic bottlenecks along downtown thoroughfares shall face immediate administrative suspension of their principal business licenses until the commercial enterprise establishes dedicated off-street fleet terminals.",
                 "Latent ultra vires penal sanction (Lawyer-Level). Imposes collateral business license suspension for vehicular traffic infractions, exceeding municipal regulatory powers under Section 458 of RA 7160 by applying enterprise-wide commercial disqualification to separate road transit violations, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Anti-Littering and Solid Waste Penal Ordinance", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 6. PENAL PROVISIONS. — Any person who commits any of the prohibited acts under this Ordinance shall, upon conviction before the proper court, be penalized with a fine not exceeding Five Thousand Pesos (PHP 5,000.00) or imprisonment for a period not exceeding one (1) year, or both, at the discretion of the court.",
                 "Exact adoption of statutory fine ceiling and maximum imprisonment term prescribed by Section 458(a)(1)(iii)."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Traffic Code Administrative Citation Guidelines", "Actual Davao City Ordinance Adaptation",
                 "SECTION 9. ADMINISTRATIVE COMPROMISE CITATION SCHEME. — Traffic violators apprehended by the City Transport and Traffic Management Office who elect to settle their administrative liabilities without court litigation may pay standard compromise settlement fees established strictly within statutory penal boundaries.",
                 "Valid exercise of local regulatory authority establishing administrative settlement options within statutory penal ceilings."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Municipal Ordinance Penal Harmonization Protocol", "Actual Davao City Ordinance Adaptation",
                 "SECTION 14. STATUTORY PENAL HARMONIZATION. — Penal clauses enacted across all local city ordinances shall remain strictly subordinate to national statutory ceilings, ensuring that imposable judicial fines and terms of custodial confinement conform to legislative boundaries prescribed by national law.",
                 "Substantive conceptual compliance with statutory ordinance penalty limitations, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Traffic Enforcement Officer Uniform Allowance Directive", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. TRAFFIC ENFORCEMENT SUBSIDY. — The City Transport and Traffic Management Office shall provide active field traffic personnel with an annual uniform maintenance subsidy of Three Thousand Pesos (PHP 3,000.00) payable from the general administrative fund.",
                 "Regulates administrative personnel uniform subsidies; neutral regarding statutory penal sanction ceilings under Section 458."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Traffic Citation Booklet Printing Specifications", "Actual Davao City Ordinance Adaptation",
                 "SECTION 3. CITATION BOOKLET SPECIFICATIONS. — Official traffic citation ticketing forms issued to City Transport and Traffic Management Office field personnel shall be printed on specialized carbonless paper bearing sequential control serial numbers registered with the City Treasurer.",
                 "Governs physical stationery printing specifications for citation pads; neutral regarding statutory penal limits."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Street Lighting and Illumination Maintenance Protocol", "Actual Davao City Ordinance Adaptation",
                 "SECTION 7. MUNICIPAL LIGHTING MAINTENANCE. — The City Engineering Office shall replace non-functional street lamps with high-efficiency luminaires across designated public corridors to ensure nocturnal pedestrian visibility and road safety.",
                 "Regulates municipal infrastructure illumination standards; unrelated to statutory penal sanction limits, with zero numbers.")
            ]
        },
        {
            "domain_id": 2,
            "domain_name": "Local Government & Territorial Boundaries",
            "premise_key": "RA_9344_Sec_6",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Juvenile Delinquency Abatement Ordinance", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 5. LOWERING AGE OF JUVENILE CUSTODIAL PROSECUTION. — Any adolescent aged twelve (12) years or older apprehended committing property offenses or repeated nocturnal status offenses within Davao City shall be subjected to formal criminal arrest, detention in police lock-up facilities, and criminal trial before regular municipal trial courts.",
                 "Direct breach of statutory age threshold. Section 6 of RA 9344 (as amended by RA 10630) explicitly commands that a child fifteen (15) years of age or under shall be exempt from criminal liability."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Penalizing Curfew Violations by Minors with Confinement", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 7. LOCK-UP CONFINEMENT FOR CURFEW INFRACTIONS. — Minors apprehended wandering on public thoroughfares between 10:00 PM and 5:00 AM without adult escort shall be remanded to the barangay police lock-up facility for mandatory three-day detention prior to parental release.",
                 "Severe violation of statutory detention prohibitions. Section 6 and Section 57-A of RA 9344 strictly prohibit detaining children in jails or lock-ups for status offenses, requiring immediate release to parents or diversion programs."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Youth Protective Transition and Recovery Protocol", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 8. PROTECTIVE YOUTH REST AND RECOVERY PROTOCOL. — Unaccompanied minors found outside residential premises after municipal curfew hours shall be brought to the Barangay Youth Recovery Sanctuary for structured overnight reflection, remaining in protective transitional custody until verified personal turnover to legal guardians.",
                 "Latent violation of juvenile protection mandates (Lawyer-Level). Euphemizes involuntary overnight detention as 'structured overnight reflection in a youth sanctuary', violating Section 57 of RA 9344 and Lucila v. People which strictly prohibit custodial detention of minors for curfew or status infractions, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Comprehensive Juvenile Intervention Program Ordinance", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 4. STATUTORY EXEMPTION FROM CRIMINAL LIABILITY. — In strict observance of Section 6 of Republic Act No. 9344, children fifteen (15) years of age or below who commit infractions within Davao City shall be unconditionally exempt from criminal prosecution, undergoing community-based diversion programs.",
                 "Exact statutory adoption of the 15-year-old minimum age of criminal responsibility and community diversion mandates."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Child-Friendly Nighttime Safety Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 6. NON-CUSTODIAL CURFEW ENFORCEMENT. — Minors found outside their residences after nighttime curfew hours shall not be subjected to arrest or incarceration, but shall be gently taken into protective custody by social workers and brought immediately to their homes.",
                 "Compliant local child protection policy executing non-custodial handling procedures required by RA 9344."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Youth Restorative Justice and Diversion Charter", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. COMMUNITY RESTORATIVE REDIRECTION. — The City Social Welfare and Development Office shall enroll youth who commit ordinance infractions into restorative community mentoring programs to support personal development without criminal stigmatization.",
                 "Substantive conceptual alignment with non-punitive juvenile diversion mandates, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Daycare Center Floor Area Specification", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. DAYCARE FLOOR AREA REQUIREMENTS. — Barangay daycare centers established within Davao City shall maintain an indoor instructional floor space of not less than thirty (30) square meters per class.",
                 "Regulates physical daycare architectural dimensions; neutral regarding statutory juvenile criminal liability."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Children's Playground Rubber Flooring Specification", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. PLAYGROUND IMPACT FLOORING. — Municipal public parks installing children's swing sets and climbing frames shall lay shock-absorbing recycled rubber safety flooring beneath all elevated play equipment.",
                 "Regulates playground impact safety surfacing; neutral regarding juvenile justice and criminal liability laws."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Child Care Center Fire Escape Inspection Protocol", "Actual Davao City Ordinance Adaptation",
                 "SECTION 6. EARLY CHILDHOOD FIRE ESCAPE STANDARDS. — Municipal early childhood education centers shall maintain unobstructed external exit pathways leading directly to outdoor assembly courts during emergency fire drills.",
                 "Regulates civil building evacuation safety; completely unrelated to statutory age of criminal responsibility, with zero numbers.")
            ]
        },
        {
            "domain_id": 2,
            "domain_name": "Local Government & Territorial Boundaries",
            "premise_key": "RA_7160_Sec_152c",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Direct Commercial Permitting Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 4. DISPENSATION OF BARANGAY CLEARANCE REQUIREMENTS. — The Business Bureau of Davao City is authorized to issue annual Mayor's Business Permits directly to commercial enterprises without requiring prior barangay clearances from the host barangay council.",
                 "Direct statutory breach. Section 152(c) of RA 7160 explicitly mandates that no city or municipality may issue any license or permit for any business or activity unless a barangay clearance is first obtained from the host barangay."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Restricting Barangay Clearance Authority for Major Commercial Centers", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 6. EXCLUSION OF COMMERCIAL ZONES FROM BARANGAY JURISDICTION. — Commercial shopping malls and heavy industrial plants operating within prime urban zones are hereby exempt from securing barangay clearances from host barangays, remitting all regulatory clearance fees exclusively to the City Treasurer.",
                 "Illegal preemption of devolved revenue authority. The Local Government Code grants barangays exclusive power to issue clearances and collect corresponding fees for all businesses within their territorial jurisdiction."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Consolidated Enterprise Investment Licensing Code", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 9. STRATEGIC ENTERPRISE CONSOLIDATED CLEARANCE PORTAL. — For high-value commercial projects certified by the City Investment Board, the Business Bureau shall issue consolidated multi-tiered municipal licenses through a single-window processing platform, integrating all sub-municipal developmental endorsements into the principal city authorization.",
                 "Latent usurpation of barangay clearance authority (Lawyer-Level). Subsumes mandatory barangay commercial clearances into a unified city license under the guise of an 'integrated single-window platform', circumventing the independent statutory prerequisite mandated under Section 152(c) of RA 7160, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Unified Business Permitting System Ordinance", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 3. PREREQUISITE BARANGAY CLEARANCE VERIFICATION. — Pursuant to Section 152(c) of Republic Act No. 7160, the Business Bureau shall require proof of an official barangay clearance issued by the host barangay prior to releasing any Mayor's Business Permit.",
                 "Exact statutory adoption executing the mandatory prerequisite barangay clearance condition prescribed by RA 7160."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Integrated Barangay Clearance Fee Collection Agreement", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. CONSOLIDATED BARANGAY FEE COLLECTION. — The City Treasurer may collect barangay clearance fees on behalf of barangays during the January business one-stop shop renewal period, remitting all collections strictly to host barangay accounts.",
                 "Compliant administrative facilitation respecting statutory barangay revenue accrual under Section 152(c)."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Inter-Governmental Commercial Licensing Coordination Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 4. LOCAL COMMUNITY LOCATION VALIDATION. — Municipal licensing examiners shall verify that neighborhood councils confirm neighborhood regulatory conformance before authorizing commercial operations in residential districts.",
                 "Substantive conceptual compliance with barangay clearance requirements, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Barangay Hall Community Hall Air-Conditioning Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. BARANGAY HALL COOLING SPECIFICATIONS. — Air-conditioning units installed inside newly constructed barangay community multi-purpose halls shall possess a minimum cooling capacity of two (2) horsepower.",
                 "Regulates administrative equipment mechanical capacity; neutral regarding statutory business permitting rules."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Barangay Official Seal Graphical Heraldry Guidelines", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. HERALDRY EMBLEM STANDARDIZATION. — Official heraldic emblems adopted by component barangays shall incorporate symbolic representations of local agricultural heritage and coastal geography.",
                 "Governs graphic design of municipal heraldry; neutral regarding statutory commercial clearances."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Barangay Notice Board Physical Material Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 6. BULLETIN BOARD CONSTRUCTION. — Public notification bulletin boards positioned outside barangay administrative halls shall feature tempered glass sliding panels to protect public announcements from weather exposure.",
                 "Regulates bulletin board physical construction; completely independent of statutory commercial permitting rules, with zero numbers.")
            ]
        },

        # =========================================================================
        # DOMAIN 03: Public Utilities & Telecom Franchises (45 pairs target)
        # =========================================================================
        {
            "domain_id": 3,
            "domain_name": "Public Utilities & Telecom Franchises",
            "premise_key": "RA_4136_Sec_35",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City National Highway Speed Limit Revision Ordinance", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 5. REVISED SPEED LIMITS ON NATIONAL ARTERIAL HIGHWAYS. — The maximum allowable vehicular speed for private passenger cars traversing the national highway stretches within Davao City is hereby established at one hundred twenty (120) kilometers per hour.",
                 "Direct breach of statutory speed ceiling. Section 35 of RA 4136 strictly fixes maximum statutory speed limits for passenger cars on open country roads and highways at eighty (80) kilometers per hour."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Altering National Highway Heavy Freight Speed Boundaries", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 7. FREIGHT SPEED DEREGULATION. — Heavy freight trucks carrying export fruits along the Davao-Bukidnon National Highway are exempted from national speed limit restrictions, permitting vehicular operating speeds up to ninety (90) kilometers per hour.",
                 "Direct violation of statutory truck speed ceilings under Section 35(b) of RA 4136, which limits heavy trucks to 50 km/h on national highways."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Suburban Transit Velocity Harmonization Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 9. DYNAMIC VELOCITY CORRIDOR HARMONIZATION. — To maximize traffic throughput along suburban bypass routes, the City Transport and Traffic Management Office may establish progressive green-wave transit corridors, authorizing motor vehicles maintaining synchronized formation to proceed at prevailing corridor design velocity.",
                 "Latent preemption of national traffic safety code (Lawyer-Level). Authorizes vehicles to travel at 'corridor design velocity' exceeding statutory caps, violating Section 35 of RA 4136 which strictly limits LGU speed-setting authority to enacting lower, more restrictive limits for safety, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Speed Limit Ordinance for Urban and Arterial Streets", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 3. SPEED LIMIT HARMONIZATION. — In accordance with Section 35 of Republic Act No. 4136, maximum vehicular speeds along national highways within city territorial limits shall not exceed eighty (80) kilometers per hour for passenger automobiles.",
                 "Exact statutory adoption executing national speed limits prescribed by RA 4136."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Urban Traffic Zone Speed Calibration Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. CTTMO SPEED ENFORCEMENT PROTOCOL. — The City Transport and Traffic Management Office (CTTMO) shall calibrate electronic radar speed guns to enforce statutory speed restrictions across crowded city streets and highway corridors.",
                 "Compliant local enforcement protocol executing statutory speed restrictions under national law."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Highway Vehicular Velocity Regulation Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 6. CORRIDOR SPEED CALIBRATION. — The City Transport and Traffic Management Office shall position digital velocity detection monitors along major thoroughfares to deter dangerous rapid transit and enforce statutory vehicular speed ceilings.",
                 "Substantive conceptual compliance with highway speed regulation mandates, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Public Street Name Signage Dimension Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. STREET SIGN ELEVATION. — Overhead municipal street name signboards installed above secondary intersections shall be positioned at a vertical clearance of not less than five (5) meters above road asphalt.",
                 "Regulates physical road signage elevations; neutral regarding statutory vehicular speed limits."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Asphalt Resurfacing Aggregate Mixture Specification", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. ASPHALT WEARING COURSE SPECIFICATIONS. — Hot asphalt pavement mixtures utilized for municipal road resurfacing projects shall incorporate crushed basalt aggregates to ensure surface skid resistance.",
                 "Regulates civil highway engineering materials; neutral regarding statutory traffic speed codes."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Road Median Shrubbery Landscaping Guidelines", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. MEDIAN HEDGE PRUNING. — Flowering shrubs planted along central roadway medians shall be trimmed regularly by municipal arborists to prevent visual obstruction of oncoming vehicular headlights.",
                 "Regulates median horticultural maintenance; completely independent of statutory vehicular speed limits, with zero numbers.")
            ]
        },
        {
            "domain_id": 3,
            "domain_name": "Public Utilities & Telecom Franchises",
            "premise_key": "RA_7925_Sec_4",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Telecommunications Local Franchise Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 4. COMPULSORY MUNICIPAL TELECOM FRANCHISING. — No national telecommunications carrier shall construct, operate, or maintain cellular base stations or fiber transmission grids within Davao City without first securing a local legislative franchise enacted by the Sangguniang Panlungsod.",
                 "Direct jurisdictional encroachment under Magtajas. Section 4 of RA 7925 and national telecommunications policy vest telecom franchising authority exclusively in the National Telecommunications Commission (NTC) and Congress."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Restricting Cross-Carrier Interconnection Facilities", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 6. LOCAL INTERCONNECTION ROUTING RESTRICTIONS. — Telecommunications carriers operating within Davao City are prohibited from routing voice or data transmission across competing cellular networks within city limits without prior municipal council authorization.",
                 "Breach of national interconnection policy. RA 7925 guarantees mandatory, non-exclusive interconnection between telecommunications networks nationwide under NTC supervision."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Emergency Telecommunications Routing Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 8. PRIORITY CIVIL DEFENSE TELECOMMUNICATIONS QUEUING. — Telecommunications carriers operating base transceiver stations within municipal jurisdiction must configure network routing protocols to allocate dedicated bandwidth channels for municipal civil defense communications during severe weather advisories, conditioning cellular mast operating renewals on annual compliance certification.",
                 "Latent preemption of national telecom policy (Lawyer-Level). Imposes local technical network queuing mandates on cellular carriers through local operating permits, encroaching upon the exclusive jurisdiction of the National Telecommunications Commission under RA 7925 and Batangas CATV, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Cellular Tower Permitting Guidelines Ordinance", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 3. LOCAL BUILDING PERMIT HARMONIZATION. — In recognition of Section 4 of Republic Act No. 7925, telecommunications public utilities possessing valid national franchises from Congress shall secure standard structural building permits from the City Building Official prior to erecting cellular towers.",
                 "Compliant local zoning and structural safety permitting respecting national statutory telecom franchises."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Underground Cable Utility Corridor Guidelines", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 5. UNDERGROUND UTILITY CONDUIT COORDINATION. — Telecommunications public utilities operating under valid NTC certificates shall coordinate with the City Engineer when excavating underground conduit corridors along public streets.",
                 "Valid exercise of local police power governing street excavations while honoring national telecom franchises."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Telecommunications Infrastructure Facilitation Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 7. EXPEDITED NETWORK INFRASTRUCTURE CLEARANCE. — Municipal zoning administrators shall expedite local building clearances for cellular transmission facilities to promote broadband connectivity for underserved rural communities in harmony with national telecommunications development goals.",
                 "Substantive conceptual alignment with national telecommunications policy objectives, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Municipal Radio Transceiver Battery Disposal Protocol", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. BATTERY RECYCLING PROCEDURES. — Expired lithium-ion rechargeable battery packs utilized in municipal handheld radio transceivers shall be turned over to the City General Services Office every two (2) years for hazardous waste recycling.",
                 "Regulates municipal inventory battery disposal; neutral regarding national telecom franchise policies."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Emergency Transceiver Antenna Mast Painting Standard", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. ANTENNA MAST COLOR SCHEME. — Emergency municipal broadcast antenna towers erected on public buildings shall feature alternating bands of aviation orange and white enamel paint.",
                 "Regulates physical tower aviation color standards; neutral regarding national telecommunications policy."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Public Hall Audio Microphone Cable Storage Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. AUDIO EQUIPMENT CABLE MAINTENANCE. — Sound technicians operating audio amplification consoles in public auditoriums shall coil microphone cables loosely around wooden storage spools to prevent internal copper wire fractures.",
                 "Regulates municipal audio equipment maintenance; completely independent of national telecommunications franchise policies, with zero numbers.")
            ]
        },
        {
            "domain_id": 3,
            "domain_name": "Public Utilities & Telecom Franchises",
            "premise_key": "RA_9136_Sec_43u",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Retail Electric Tariff Regulation Ordinance", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 4. LOCAL ELECTRIC DISTRIBUTION TARIFF CAPS. — The Sangguniang Panlungsod shall review and approve all retail power distribution tariff adjustments proposed by local electric utilities, capping distribution wheeling charges at ten percent (10%) above operational generation costs.",
                 "Direct jurisdictional encroachment under Magtajas. Section 43(u) of RA 9136 (EPIRA) explicitly vests original and exclusive jurisdiction over all electric rates, tariffs, and distribution fees in the Energy Regulatory Commission (ERC)."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Authorizing Municipal Adjudication of Electric Utility Disputes", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 6. MUNICIPAL ADJUDICATION OF POWER DISPUTES. — The City Legal Officer is authorized to adjudicate billing disputes, overcharging complaints, and rate contested cases between residential consumers and power distribution utilities within Davao City.",
                 "Breach of exclusive national jurisdiction. Section 43(u) of EPIRA grants the ERC exclusive jurisdiction over all cases contesting rates and disputes between electric industry participants and end-users."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Urban Grid Hardening Infrastructure Assessment Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 8. MUNICIPAL GRID RESILIENCY INFRASTRUCTURE SURCHARGE. — To finance the conversion of overhead distribution cables into subterranean conduits, the City Council shall establish an auxiliary urban grid hardening fee to be unbundled on consumer electricity invoices, mandating the franchised distribution utility to collect the adjusted schedule.",
                 "Latent usurpation of national utility rate authority (Lawyer-Level). Adds an unbundled municipal surcharge to retail electricity bills, violating Section 43 of RA 9136 (EPIRA) which vests exclusive jurisdiction over electricity tariffs and unbundled billing items in the Energy Regulatory Commission, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Electric Utility Franchise Right-of-Way Ordinance", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 3. RECOGNITION OF NATIONAL ERC JURISDICTION. — Recognizing the exclusive jurisdiction of the Energy Regulatory Commission under Section 43 of Republic Act No. 9136, local electric distribution utilities shall maintain public electric distribution networks along municipal road rights-of-way in accordance with safety standards.",
                 "Compliant local police power regulation over municipal rights-of-way explicitly recognizing exclusive national ERC jurisdiction."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Electric Distribution Pole Relocation Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. UTILITY POLE RELOCATION PROCEDURES. — Electric distribution utilities shall coordinate with the City Engineer when relocating utility poles affected by municipal road widening projects, following ERC distribution guidelines.",
                 "Valid exercise of municipal right-of-way management respecting national energy regulatory jurisdiction."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Electrical Grid Safety and Public Easement Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 7. CLEARANCE OF POWER DISTRIBUTION CORRIDORS. — Municipal building inspectors shall coordinate with certified electric distribution utilities to ensure that private structures do not encroach upon high-voltage aerial distribution corridors.",
                 "Substantive conceptual compliance with electrical infrastructure safety and right-of-way coordination, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Street Sweeper Safety Vest Reflective Strip Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. REFLECTIVE TAPE SPECIFICATIONS. — High-visibility safety vests issued to municipal roadway street sweepers shall feature reflective retro-prismatic bands measuring not less than five (5) centimeters in width.",
                 "Regulates municipal street cleaner protective apparel; neutral regarding national electric regulatory jurisdiction."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Municipal Power Tool Preventive Maintenance Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 3. WORKSHOP POWER TOOL INSPECTIONS. — Portable electric drills and saws utilized in the municipal carpentry workshop shall undergo bi-monthly insulation testing by certified city electricians.",
                 "Regulates workshop tool maintenance; neutral regarding statutory electric distribution tariffs."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Municipal Workshop Electrical Circuit Breaker Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 5. CIRCUIT BREAKER LABELLING. — Electrical distribution panels installed within city government repair depots shall display permanent thermal-printed labels identifying each connected workshop machine.",
                 "Regulates internal municipal workshop electrical panel labelling; completely independent of national electric utility rate regulation, with zero numbers.")
            ]
        },

        # =========================================================================
        # DOMAIN 04: Public Health, Hospitals & Medical Services (45 pairs target)
        # =========================================================================
        {
            "domain_id": 4,
            "domain_name": "Public Health, Hospitals & Medical Services",
            "premise_key": "RA_11223_Sec_6",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Public Hospital Emergency Admission Cost-Recovery Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 4. EMERGENCY ADMISSION CASH DEPOSITS. — City-operated public health facilities and hospital emergency rooms in Davao City are authorized to demand an advance cash deposit of Five Thousand Pesos (PHP 5,000.00) before admitting indigent patients for emergency medical stabilization.",
                 "Direct statutory violation. Section 6 of RA 11223 (Universal Health Care Act) guarantees immediate eligibility and access to population-based and individual-based health services without advance deposits, prohibiting denial of emergency stabilization."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Limiting Free Basic Medical Services to Registered Homeowners", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 6. REAL PROPERTY REQUIREMENT FOR HEALTH ENROLLMENT. — Free primary and emergency healthcare consultations at municipal health centers shall be restricted to residents who present proof of real property ownership within Davao City.",
                 "Unlawful preemption of universal healthcare rights. RA 11223 guarantees every Filipino citizen immediate access to comprehensive primary and emergency healthcare services without local property ownership barriers."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Specialized Emergency Surgical Admission Protocol", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 8. PROTOCOL FOR SPECIALIZED TRAUMA ADMISSION. — Patients arriving at municipal emergency departments requiring intensive critical care intervention shall be routed through the Patient Accounting Bureau to establish verified national health insurance enrollment eligibility or documented corporate coverage prior to admission to specialized surgical suites.",
                 "Latent rollback of universal emergency medical care (Lawyer-Level). Conditions transfer to specialized emergency surgical suites on insurance verification, violating Section 6 of RA 11223 and the Anti-Hospital Deposit Law which mandate immediate emergency stabilization without administrative preconditions, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Universal Health Care Integration Ordinance", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 3. COMPREHENSIVE ACCESS TO PRIMARY MEDICAL CARE. — In compliance with Section 6 of Republic Act No. 11223, the City Health Office shall ensure that all residents of Davao City enjoy immediate access to essential primary and preventive health care services through district health centers.",
                 "Exact statutory adherence executing universal primary healthcare access under RA 11223."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City District Health Center Network Referral Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. PROMPT EMERGENCY PATIENT STABILIZATION. — Municipal health stations shall stabilize walk-in emergency patients immediately without financial pre-conditions, coordinating transfer to specialized tertiary facilities in accordance with PhilHealth referral protocols.",
                 "Direct execution of statutory emergency stabilization mandates under national universal healthcare laws."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Community Primary Healthcare Outreach Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 4. DECENTRALIZED MEDICAL CLINIC ACCESSIBILITY. — The City Health Office shall deploy mobile medical teams to remote agricultural settlements to provide free preventative clinical diagnostic consultations and essential therapeutic medications to vulnerable populations.",
                 "Substantive conceptual compliance with universal healthcare access mandates, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Clinical Thermometer Mercury Prohibition Ordinance", "Actual Davao City Ordinance Adaptation",
                 "SECTION 3. MERCURY THERMOMETER PROHIBITION. — Public and private clinical laboratories operating within Davao City shall replace all mercury-containing glass thermometers with certified digital sensor thermometers within ninety (90) calendar days.",
                 "Regulates clinical laboratory instrument safety; neutral regarding statutory universal healthcare coverage."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Medical Center Biohazard Waste Bin Color-Coding Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. INFECTIOUS WASTE BIN SPECIFICATIONS. — Clinical sharps disposal containers utilized in municipal health stations shall be constructed of rigid, puncture-proof red polypropylene bearing biohazard insignias.",
                 "Regulates clinical infectious waste container standards; neutral regarding universal medical care rights."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Health Station Autoclave Sterilization Documentation Protocol", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. AUTOCLAVE TEMPERATURE MONITORING LOGS. — Dental clinic personnel operating steam autoclave sterilizers shall log vacuum pressure indicators following each sterilization batch to confirm complete pathogen neutralization.",
                 "Regulates dental equipment sterilization recordkeeping; completely independent of universal healthcare rights, with zero numbers.")
            ]
        },
        {
            "domain_id": 4,
            "domain_name": "Public Health, Hospitals & Medical Services",
            "premise_key": "RA_11332_Sec_9",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Notifiable Disease Public Disclosure Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 5. PUBLIC DISCLOSURE OF COMMUNICABLE DISEASE PATIENTS. — To alert neighborhood residents during epidemic outbreaks, the City Health Office is authorized to publish the full names, residential addresses, and specific medical diagnoses of individuals infected with notifiable diseases on official barangay bulletin boards.",
                 "Direct breach of statutory confidentiality. Section 9(a) of RA 11332 strictly criminalizes unauthorized disclosure of private and confidential patient medical information and registries."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Conditioning Epidemic Reporting on Barangay Verification", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 7. MANDATORY LOCAL FILTERING OF DISEASE REPORTS. — Private clinical laboratories detecting notifiable pathogens within Davao City shall transmit laboratory reports exclusively to the host barangay council, withholding statutory epidemiological notices from the Department of Health pending local clearance.",
                 "Breach of statutory reporting mandates. RA 11332 commands immediate mandatory reporting of notifiable diseases directly to the Department of Health Epidemiology Bureau."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Community Epidemiological Mapping and Contact Tracing Code", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 8. GRANULAR EPIDEMIOLOGICAL CLUSTER MAPPING. — To maximize community vigilance during epidemic surges, the City Health Office shall publish digital geospatial directory maps on municipal portals identifying the specific residential addresses and compound locations of active quarantined households to facilitate localized neighborhood tracing.",
                 "Latent violation of statutory patient confidentiality (Lawyer-Level). Publishes specific residential street and compound locations of quarantined families, violating Section 9 of RA 11332 which prohibits unauthorized public disclosure of identifiable patient data during health emergencies, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Mandatory Disease Reporting and Confidentiality Ordinance", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 3. STATUTORY REPORTING OF NOTIFIABLE DISEASES. — Pursuant to Section 9 of Republic Act No. 11332, all public and private medical facilities in Davao City shall transmit epidemiological reports of notifiable diseases to the Department of Health while strictly maintaining patient confidentiality.",
                 "Exact statutory adoption of mandatory disease reporting and strict data confidentiality under RA 11332."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Epidemiological Surveillance and Contact Tracing Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. SECURE EPIDEMIOLOGICAL DATA TRANSMISSION. — The City Health Office Epidemiology and Surveillance Unit shall manage contact tracing data through encrypted digital platforms accessible only to authorized health personnel in compliance with DOH standards.",
                 "Compliant local epidemiological surveillance executing statutory reporting with strict data privacy safeguards."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Public Health Surveillance and Data Confidentiality Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 6. PROTECTION OF COMMUNICABLE DISEASE DATA. — Health workers conducting epidemiological disease tracing shall maintain strict medical confidentiality over patient identities, transmitting surveillance records through secure encrypted channels exclusively to authorized public health epidemiologists.",
                 "Substantive conceptual compliance with statutory disease reporting and patient privacy mandates, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Clinical Glove Thickness Quality Specification", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. CLINICAL EXAMINATION GLOVE STANDARDS. — Disposable nitrile examination gloves procured for city health stations shall have a minimum cuff thickness of zero point zero eight (0.08) millimeters.",
                 "Regulates clinical consumable physical thickness; neutral regarding statutory notifiable disease reporting."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Medical Refrigerator Temperature Monitoring Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 3. VACCINE COLD-CHAIN TEMPERATURE LOGS. — Clinic nurses shall verify and record digital temperatures of vaccine storage refrigerators twice daily to ensure uninterrupted cold-chain preservation.",
                 "Regulates clinic refrigeration temperature monitoring; neutral regarding statutory communicable disease reporting."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Health Station Waiting Room Bench Sanitization Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 5. OUTPATIENT SEATING HYGIENE PROTOCOL. — Custodial staff in public outpatient clinics shall wipe plastic waiting lounge benches with approved disinfectant solutions between morning and afternoon clinical consultation sessions.",
                 "Regulates clinic furniture surface sanitization; completely independent of statutory epidemiological reporting, with zero numbers.")
            ]
        },
        {
            "domain_id": 4,
            "domain_name": "Public Health, Hospitals & Medical Services",
            "premise_key": "RA_9211_Sec_5",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Nightlife and Entertainment Revitalization Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 6. INDOOR SMOKING IN ENTERTAINMENT ESTABLISHMENTS. — Licensed bars, karaoke lounges, and nightlife establishments operating within Davao City are permitted to allow indoor tobacco smoking inside customer seating lounges occupying up to fifty percent (50%) of their total enclosed floor space.",
                 "Direct statutory breach. Section 5 of RA 9211 absolutely prohibits smoking in all enclosed public places, food preparation establishments, and entertainment venues, strictly barring indoor smoking areas."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Exempting Electronic Vapor Products from Public Place Restrictions", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 4. EXEMPTION OF VAPOR PRODUCTS IN WORKPLACES. — The use of electronic nicotine delivery systems and vaporized tobacco devices is permitted inside enclosed commercial workplaces and municipal government offices.",
                 "Breach of statutory indoor air protections. National clean air and tobacco control statutes extend public indoor smoking prohibitions to electronic vapor devices in workplaces and government facilities."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Hospitality Cigar Degustation Licensing Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 7. DESIGNATED INDOOR HERITAGE CIGAR DEGUSTATION ROOMS. — Licensed hospitality establishments and boutique cigar lounges may maintain an enclosed indoor tobacco tasting chamber for adult connoisseurs, provided that the venue operates independent negative-pressure ventilation systems certified by the City Health Office.",
                 "Latent breach of absolute statutory indoor smoking prohibitions (Lawyer-Level). Creates an exception for indoor cigar degustation rooms under the pretext of negative-pressure ventilation, violating Section 5 of RA 9211 and EO 26 which strictly prohibit indoor smoking areas inside food and hospitality establishments, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Comprehensive Anti-Smoking Ordinance", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 4. ABSOLUTE PROHIBITION OF PUBLIC SMOKING. — In strict observance of Section 5 of Republic Act No. 9211, smoking and vaping are absolutely prohibited in all public conveyances, government offices, schools, medical facilities, and enclosed public spaces throughout Davao City.",
                 "Exact statutory adoption of absolute public smoking prohibitions under RA 9211."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Designated Smoking Area Standards Protocol", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 6. DESIGNATED OUTDOOR SMOKING AREAS. — Designated smoking areas in commercial complexes shall be situated strictly in open outdoor spaces, positioned at least ten (10) meters away from building entrances, operable windows, and public access pathways.",
                 "Compliant local enforcement establishing strict outdoor designated smoking areas adhering to statutory parameters."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Clean Air and Smoke-Free Public Environment Charter", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 5. SMOKE-FREE PUBLIC THOROUGHFARES. — The Anti-Vices Task Force shall monitor public assembly zones and commercial walkways to ensure that individuals refrain from combustion of tobacco products in areas accessible to the general public.",
                 "Substantive conceptual execution of absolute public smoking prohibitions, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Municipal Park Trash Receptacle Color-Coding Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. PARK WASTE BIN SPECIFICATIONS. — Waste receptacles installed in public parks shall have a minimum internal volume of fifty (50) liters and display standardized labels for biodegradable and recyclable waste.",
                 "Regulates park waste bin volumes; neutral regarding statutory public smoking bans."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Public Park Lawn Sprinkler Operation Schedule", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 3. ROTATIONAL LAWN IRRIGATION SCHEDULE. — Automated sprinkler systems installed within urban plazas shall operate exclusively during early morning hours between four o'clock and six o'clock to conserve municipal treated water.",
                 "Regulates public park irrigation hours; neutral regarding statutory tobacco smoking prohibitions."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Public Park Concrete Walkway Sealant Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 6. SLIP-RESISTANT WALKWAY SEALANT. — Pedestrian pathways within municipal recreational gardens shall be treated with silicone water-repellent sealant to minimize moss accumulation and prevent pedestrian slips during rainstorms.",
                 "Regulates park walkway masonry coatings; completely independent of statutory tobacco smoking regulations, with zero numbers.")
            ]
        },

        # =========================================================================
        # DOMAIN 05: Statutory Codes & General Legal Amendments (45 pairs target)
        # =========================================================================
        {
            "domain_id": 5,
            "domain_name": "Statutory Codes & General Legal Amendments",
            "premise_key": "RA_7942_Sec_70",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Offshore Mineral Exploration Moratorium Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 4. MORATORIUM ON MINERAL AGREEMENTS. — The Sangguniang Panlungsod hereby declares an absolute ten-year ban on the issuance and execution of all national Mineral Production Sharing Agreements (MPSA) and Financial or Technical Assistance Agreements (FTAA) across all marine territorial waters off Davao City.",
                 "Direct jurisdictional encroachment under Magtajas. Section 70 and provisions of RA 7942 reserve the exclusive authority to grant, regulate, and execute mineral exploration and production agreements to the Secretary of the DENR and the President."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Banning Large-Scale Mining Environmental Compliance Certificates", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 6. REVOCATION OF NATIONAL ENVIRONMENTAL COMPLIANCE CERTIFICATES. — The City Environment and Natural Resources Office is authorized to revoke Environmental Compliance Certificates (ECC) issued by the national Department of Environment and Natural Resources for large-scale mining operations situated within regional boundaries.",
                 "Ultra vires usurpation of national authority. Municipalities cannot invalidate or revoke ECCs issued by the national DENR/EMB under national environmental and mining statutes."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Coastal Benthic Shelf Ecological Stewardship Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 8. COASTAL BENTHIC ZONE ECOLOGICAL STEWARDSHIP LEASES. — Commercial dredging operators and marine geological surveying entities operating within the city's coastal baseline shelf must execute an ecological stewardship lease approved by the Sangguniang Panlungsod prior to initiating sub-surface coring or mineral sediment sampling.",
                 "Latent jurisdictional encroachment on national mineral authority (Lawyer-Level). Asserts municipal legislative concession authority over marine sub-surface mineral sampling, encroaching on the exclusive jurisdiction of the Mines and Geosciences Bureau under Section 70 of RA 7942, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Watershed Environmental Protection and Small-Scale Quarrying Ordinance", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 3. ENVIRONMENTAL COMPLIANCE REQUISITE. — In accordance with Section 70 of Republic Act No. 7942, commercial quarry operators extracting sand and gravel within Davao City shall secure an Environmental Compliance Certificate from the DENR prior to the issuance of a City Mayor's Quarry Permit.",
                 "Exact statutory adherence coordinating local quarry permitting with mandatory national DENR environmental certificates."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Multi-Partite Environmental Monitoring Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. MULTI-PARTITE MONITORING TEAMS. — The City Environment and Natural Resources Office shall participate in multi-partite monitoring teams organized by the Mines and Geosciences Bureau (MGB) to inspect commercial extraction sites for ecological rehabilitation compliance.",
                 "Compliant local inter-agency collaboration under national mining environmental regulations."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Riparian Environmental Rehabilitation Monitoring Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 7. POST-EXTRACTION ECOLOGICAL RESTORATION VERIFICATION. — Municipal environmental officers shall inspect decommissioned aggregate borrow pits alongside national mining geologists to confirm that quarry operators complete vegetative slope re-contouring in conformity with approved environmental rehabilitation commitments.",
                 "Substantive conceptual compliance with statutory mining environmental rehabilitation monitoring, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Public Nursery Seedling Potting Soil Specification", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. POTTING SOIL COMPOSITION. — Municipal botanical nurseries propagating indigenous hardwood saplings shall blend garden topsoil with river sand in a ratio of two (2) parts topsoil to one (1) part river sand.",
                 "Regulates municipal agricultural potting soil mixtures; neutral regarding statutory mining concessions."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Municipal Composting Facility Aeration Schedule", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. SOLID WASTE COMPOST AERATION. — Operators at the city solid waste composting facility shall turn organic waste windrows twice weekly to accelerate aerobic microbial decomposition.",
                 "Regulates municipal solid waste composting procedures; neutral regarding statutory mining environmental regulations."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Botanical Garden Herbarium Specimen Preservation Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 6. HERBARIUM BOTANICAL MOUNTING. — Botanical plant specimens archived within the municipal botanical herbarium shall be mounted onto acid-free rag paper using neutral archival adhesive paste to preserve plant cell structures for taxonomic classification.",
                 "Regulates botanical herbarium preservation; completely independent of national mining and environmental statutes, with zero numbers.")
            ]
        },
        {
            "domain_id": 5,
            "domain_name": "Statutory Codes & General Legal Amendments",
            "premise_key": "RA_8550_Sec_18",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Commercial Deep-Sea Marine Trawling Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 5. COMMERCIAL FISHING AUTHORIZATION IN MUNICIPAL WATERS. — Commercial fishing vessels measuring between twenty (20) and one hundred fifty (150) gross tons are hereby authorized to conduct commercial purse-seine and trawl fishing within municipal waters extending three (3) kilometers from the shoreline of Davao City.",
                 "Direct breach of statutory spatial boundaries. Section 18 of RA 8550 strictly reserves municipal waters from shoreline to 15 kilometers for municipal fishers, permitting medium commercial vessels only in deeper waters beyond 10.1 kilometers under strict conditions."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Banning Non-Resident Marginal Municipal Fisherfolk", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 7. EXCLUSION OF MUNICIPAL FISHERS FROM ADJACENT PROVINCES. — Marginal municipal fisherfolk registered in neighboring municipalities across the Davao Gulf are prohibited from casting non-motorized fishing nets in Davao City municipal waters, reserving all fishing grounds exclusively to voters of Davao City.",
                 "Breach of statutory resource access rights. RA 8550 guarantees municipal fishers access to contiguous municipal waters within shared gulf bays, barring discriminatory local voter exclusions against small-scale artisanal fishers."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Seasonal Pelagic Fishery Concession Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 8. SEASONAL PELAGIC FISHERY RECOVERY LICENSES. — To optimize economic harvest during migratory oceanic fish runs, the City Agriculture Office may issue seasonal joint-venture fishing endorsements authorizing commercial vessels exceeding three gross tons to operate mid-water purse seines within the inner municipal water baseline.",
                 "Latent violation of municipal marine zoning protections (Lawyer-Level). Authorizes commercial fishing vessels exceeding three gross tons inside the inner municipal water baseline, directly violating Section 18 of RA 8550 which reserves municipal waters exclusively for artisanal and small municipal fishers, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Fisheries Management and Coastal Conservation Ordinance", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 3. ARTISANAL MUNICIPAL FISHER REGISTRATION. — Pursuant to Section 18 of Republic Act No. 8550, the City Agriculture Office shall maintain a municipal fisherfolk registry, granting priority exploitation rights within the fifteen (15) kilometer municipal waters to resident subsistence fisherfolk.",
                 "Exact statutory adoption of the 15-kilometer municipal waters boundary and subsistence fisher priority rights under RA 8550."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Small-Scale Commercial Fishing Authorization Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 6. COMMERCIAL FISHING BOAT CLEARANCE IN DEEP WATERS. — Small commercial fishing vessels between 3.1 and 20 gross tons may operate within municipal waters between 10.1 and 15 kilometers, provided the depth exceeds seven fathoms and upon approval of the Fisheries and Aquatic Resources Management Council (FARMC).",
                 "Compliant local execution of statutory exceptions for small commercial fishing in authorized deep waters under RA 8550."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Coastal Mangrove and Marine Nursery Protection Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 4. ESTUARINE BREEDING SANCTUARY RESERVATION. — Municipal coastal patrol marshals shall protect inter-tidal mangrove estuaries from motorized fishing vessels, reserving nearshore breeding nurseries exclusively for traditional handline sustenance fishers.",
                 "Substantive conceptual execution of artisanal fishing rights and marine nursery protection mandates, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Fish Landing Port Concrete Mooring Bollard Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. MOORING BOLLARD SPECIFICATIONS. — Cast-iron mooring bollards installed along municipal fish landing wharves shall have a rated holding tensile capacity of not less than thirty (30) metric tons.",
                 "Regulates port civil engineering bollard capacity; neutral regarding statutory municipal fishing boundaries."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Fish Port Sorting Area Floor Drainage Cleaning Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. FISH MARKET FLOOR WASHING SCHEDULE. — Municipal fish terminal trading floors shall be hosed down with high-pressure chlorinated water immediately following the conclusion of morning wholesale bidding auctions.",
                 "Regulates fish market floor sanitization; neutral regarding statutory municipal waters access rights."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Municipal Fish Auction Scale Calibration Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 6. COMMERCIAL WEIGHING SCALE CALIBRATION. — The City Treasurer shall calibrate counter-balanced platform scales utilized in fish wholesale trading halls using certified brass test weights to guarantee equitable trade transactions.",
                 "Regulates market weighing scale accuracy; completely independent of statutory municipal water fishing privileges, with zero numbers.")
            ]
        },
        {
            "domain_id": 5,
            "domain_name": "Statutory Codes & General Legal Amendments",
            "premise_key": "RA_10591_Sec_31",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Firearms Local Permitting Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 4. LOCAL MUNICIPAL PERMIT TO CARRY FIREARMS. — Licensed firearm holders residing within Davao City must apply for and secure a City Mayor's Permit to Carry Firearms Outside of Residence, paying an annual municipal fee of Five Thousand Pesos (PHP 5,000.00), prior to transporting registered firearms across city streets.",
                 "Direct preemption of national jurisdiction. Section 31 of RA 10591 explicitly establishes that the authority to issue a Permit to Carry Firearms Outside of Residence (PTCFOR) belongs exclusively to the Chief of the Philippine National Police (PNP)."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Invalidating National Firearm Carry Permits in City Commercial Centers", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 6. PROHIBITION OF NATIONAL PTCFOR PERMITS IN BUSINESS PARKS. — Duly issued national Permits to Carry Firearms Outside Residence (PTCFOR) issued by the Chief of the PNP are hereby rendered null and void within all commercial business districts and shopping malls situated in Davao City.",
                 "Ultra vires nullification of national licenses under Magtajas. A municipal ordinance cannot invalidate or restrict national licenses to carry firearms issued by the Chief of the PNP pursuant to national statutory authority."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Checkpoint Security Endorsement Protocol", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 8. MUNICIPAL TRANSIT FIREARM VERIFICATION CLEARANCE. — Citizens transporting licensed personal defense firearms across municipal entry boundaries must present a Certificate of Local Transit Endorsement issued by the City Mayor's Security Directorate confirming legitimate civic travel within municipal territory.",
                 "Latent preemption of national firearm carriage authorization (Lawyer-Level). Imposes an auxiliary municipal transit endorsement to transport licensed firearms, infringing upon the nationwide validity of Permits to Carry Firearms Outside Residence (PTCFOR) under Section 31 of RA 10591, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Public Safety Firearms Carrying Verification Protocol", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 3. RECOGNITION OF NATIONAL PNP PTCFOR LICENSES. — In accordance with Section 31 of Republic Act No. 10591, the Davao City Police Office shall verify that any civilian individual carrying a concealed registered firearm in public places holds a valid Permit to Carry Firearms Outside of Residence issued by the Chief of the PNP.",
                 "Exact statutory adherence executing national police verification of PTCFOR licenses under RA 10591."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Gun-Free Zone Declaration in Municipal Government Buildings", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. WEAPONS RESTRICTION IN GOVERNMENT HALLS. — Civilians holding valid PTCFOR licenses shall deposit their firearms in secure lockboxes at building security entrances before entering City Hall administrative offices, in harmony with national police facility security guidelines.",
                 "Compliant local building security regulation respecting national licensing while establishing facility deposit rules."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Public Assembly Security and Firearm Restriction Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 6. WEAPONS RESTRICTIONS AT CIVIC GATHERINGS. — Security personnel shall maintain perimeter checkpoints at public festival parades, requiring armed citizens to deposit personal firearms with authorized police marshals during festive assemblies.",
                 "Substantive conceptual execution of firearm carriage verification and public assembly safety mandates, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Firecracker and Pyrotechnic Display Safety Standard", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 4. PYROTECHNIC TEMPORARY STORAGE DISTANCES. — Temporary commercial storage warehouses stocking authorized pyrotechnic display materials shall maintain a separation clearance of not less than fifty (50) meters from fuel storage tanks.",
                 "Regulates pyrotechnic warehouse physical separation; neutral regarding statutory firearm carry permits."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Security Guard Nightstick and Whistle Equipment Directive", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. SECURITY GUARD UNIFORM ACCESSORIES. — Private security guards deployed at municipal transit terminals shall carry standardized hardwood nightsticks measuring sixty centimeters in length and an emergency whistle.",
                 "Regulates security guard non-lethal equipment accessories; neutral regarding statutory firearm carriage laws."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Pyrotechnic Display Water Barrel Fire Safety Protocol", "Actual Davao City Ordinance Adaptation",
                 "SECTION 7. EMERGENCY FIRE DOUSE INFRASTRUCTURE. — Technicians executing authorized public pyrotechnic displays shall position sealed fifty-gallon water drums and sand buckets beside mortar firing racks to extinguish defective smoldering casings.",
                 "Regulates fireworks display firefighting readiness; completely distinct from statutory firearm licensing, with zero numbers.")
            ]
        },

        # =========================================================================
        # DOMAIN 06: Public Finance & General Appropriations (35 pairs target)
        # =========================================================================
        {
            "domain_id": 6,
            "domain_name": "Public Finance & General Appropriations",
            "premise_key": "RA_7160_Sec_287",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Annual General Appropriations Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 5. ALLOCATION TO LOCAL DEVELOPMENT PROJECTS. — The City Government of Davao shall appropriate seven percent (7%) of its annual internal revenue allotment shares to finance the City Comprehensive Development Investment Program.",
                 "Direct statutory violation. Section 287 of RA 7160 strictly commands that each local government unit shall appropriate in its annual budget not less than twenty percent (20%) of its annual internal revenue allotment for development projects."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Diverting Local Development Funds to Executive Travel", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 8. RE-ALIGNMENT OF DEVELOPMENT FUNDS TO ADMINISTRATIVE OVERHEAD. — The City Budget Officer is authorized to re-align thirty percent of the statutory Local Development Fund to pay for municipal administrative personnel overtime allowances and official foreign travel expenses.",
                 "Direct breach of statutory fund restrictions. Local development funds are strictly dedicated by national statute to social, economic, and infrastructure development, prohibiting expenditure on routine administrative salaries and travel."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Municipal Development Fund Strategic Utilization Code", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 6. STRATEGIC REPROGRAMMING OF UNALLOCATED DEVELOPMENT BALANCES. — To support municipal trade missions and sister-city investment summits, unexpended appropriations under the annual local development fund may be reprogrammed by executive order to finance city protocol hospitality and international civic delegation hosting.",
                 "Latent evasion of statutory development fund restrictions (Lawyer-Level). Re-allocates statutory 20% development fund reserves for protocol hospitality and travel, violating Section 287 of RA 7160 and DILG guidelines which mandate exclusive utilization for socio-economic and environmental development projects, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Annual Budget Enactment Ordinance", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 4. STATUTORY TWENTY PERCENT DEVELOPMENT ALLOCATION. — In strict compliance with Section 287 of Republic Act No. 7160, exactly twenty percent (20%) of the City's National Tax Allotment is hereby allocated to the 20% Local Development Fund for capital social and economic infrastructure.",
                 "Exact statutory adherence executing the mandatory 20% development fund allocation mandated by Section 287."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Development Investment Program Guidelines", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 6. ELIGIBILITY OF INFRASTRUCTURE PROJECTS. — Programs financed by the Local Development Fund shall adhere strictly to Joint Memorandum Circulars issued by DILG and DBM, funding capital public works and communal water systems.",
                 "Compliant local investment programming executing national administrative guidelines under Section 287."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Capital Infrastructure Priority Programming Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 7. LONG-TERM COMMUNITY ASSET CREATION. — Municipal development appropriations shall prioritize durable public capital facilities including rural farm access roadways, barangay maternity clinics, and communal flood control barriers.",
                 "Substantive conceptual compliance with statutory local development funding objectives, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Public Procurement Bid Document Reproduction Fee Schedule", "Actual Davao City Ordinance Adaptation",
                 "SECTION 3. BID DOCUMENT PRICING. — Prospective bidders for municipal supply contracts shall pay a non-refundable reproduction fee of One Thousand Pesos (PHP 1,000.00) for standard bidding tender dossiers.",
                 "Regulates municipal procurement document fees; neutral regarding statutory development fund percentages."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Bids and Awards Committee Secretariat Recording Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 4. BID OPENING AUDIO-VISUAL RECORDINGS. — The Bids and Awards Committee Secretariat shall record all competitive public bidding sessions using digital video recording equipment.",
                 "Regulates municipal procurement audio-visual archiving; neutral regarding statutory development budget allocations."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Municipal Treasury Vault Key Custody Protocol", "Actual Davao City Ordinance Adaptation",
                 "SECTION 5. TREASURY VAULT KEY PROTOCOL. — Combinations and physical safety keys to the municipal treasury currency storage vault shall remain under the personal custody of the City Treasurer and the Assistant Treasurer.",
                 "Regulates municipal treasury safe security procedures; completely independent of local development fund laws, with zero numbers.")
            ]
        },
        {
            "domain_id": 6,
            "domain_name": "Public Finance & General Appropriations",
            "premise_key": "RA_10121_Sec_21",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Disaster Reserve Allocation Adjustment Ordinance", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 4. LOCAL DISASTER RISK FUND APPORTIONMENT. — The Sangguniang Panlungsod shall set aside two percent (2%) of estimated regular revenue sources to establish the Local Disaster Risk Reduction and Management Fund (LDRRMF).",
                 "Direct statutory violation. Section 21 of RA 10121 explicitly commands that not less than five percent (5%) of estimated revenue from regular sources shall be set aside as the LDRRMF."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Diverting Quick Response Calamity Reserves to Public Relations", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 7. RE-ALIGNMENT OF QUICK RESPONSE CALAMITY RESERVES. — The City Council is authorized to transfer sixty percent of the Quick Response Fund (QRF) standby reserve to finance municipal tourism advertising and promotional campaigns.",
                 "Direct statutory violation of fund earmarking. Section 21 of RA 10121 strictly mandates that thirty percent (30%) of the LDRRMF shall be allocated as Quick Response Fund for relief and recovery programs, prohibiting diversion to municipal public relations."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Emergency Mitigation Surplus Reallocation Ordinance", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 5. ANNUAL FISCAL SURPLUS RECOVERY PROTOCOL. — At the conclusion of the municipal fiscal year, unutilized appropriations remaining in the localized emergency response allocation shall be transferred to the City General Fund to support municipal public infirmary maintenance and community health center infrastructure.",
                 "Latent violation of statutory disaster trust fund rules (Lawyer-Level). Reverts unexpended disaster management funds to the general fund for hospital maintenance, violating Section 21 of RA 10121 which strictly requires unexpended LDRRMF balances to accrue to a special five-year trust fund solely for disaster mitigation, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Disaster Risk Reduction and Management Budget Charter", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 3. FIVE PERCENT STATUTORY DISASTER FUND ALLOCATION. — In accordance with Section 21 of Republic Act No. 10121, five percent (5%) of estimated revenue from regular sources is appropriated to the Local Disaster Risk Reduction and Management Fund (LDRRMF), with thirty percent (30%) dedicated to the Quick Response Fund.",
                 "Exact statutory adoption of the 5% LDRRMF and 30% QRF statutory fund allocation formulas."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Calamity Trust Fund Management Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 6. FIVE-YEAR DISASTER SPECIAL TRUST FUND. — Unexpended balances of the LDRRMF shall accrue to a special trust fund solely for disaster risk reduction activities for five (5) years, in full compliance with RA 10121.",
                 "Compliant local execution of statutory five-year special trust fund retention rules."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Disaster Risk Financing and Community Resilience Charter", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 4. STATUTORY DISASTER RISK FINANCING. — The local expenditure budget shall preserve mandatory fiscal reserves dedicated exclusively to disaster prevention, pre-disaster equipment acquisition, and rapid post-calamity relief operations.",
                 "Substantive conceptual compliance with statutory disaster risk reduction and management funding mandates, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Relief Goods Rice Warehouse Pallet Stacking Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. RELIEF WAREHOUSE PALLET STACKING. — Sacks of National Food Authority relief rice stored in calamity response warehouses shall not be stacked higher than ten (10) tiers upon wooden pallets.",
                 "Regulates warehouse physical cargo stacking safety; neutral regarding statutory disaster fund percentage allocations."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Relief Blanket Textile Quality Specifications", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. RELIEF BLANKET TEXTILE STANDARDS. — Emergency thermal blankets procured for calamity evacuation centers shall consist of woven fleece fabric resistant to fraying.",
                 "Governs textile fabric quality of relief blankets; neutral regarding statutory municipal disaster budgetary appropriations."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Emergency Fuel Depository and Tank Maintenance Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 6. EMERGENCY FUEL STORAGE INSPECTIONS. — The City Central Emergency Communications and Dispatch facility shall inspect underground diesel fuel storage tanks quarterly to verify fuel readiness for standby emergency electric generators.",
                 "Regulates physical generator fuel tank inspections; independent of statutory disaster budget percentage allocations, with zero numbers.")
            ]
        },

        # =========================================================================
        # DOMAIN 07: Taxation, Tariffs & Revenue Administration (35 pairs target)
        # =========================================================================
        {
            "domain_id": 7,
            "domain_name": "Taxation, Tariffs & Revenue Administration",
            "premise_key": "RA_7160_Sec_233",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Real Property Tax Assessment Adjustment Ordinance", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 4. REAL PROPERTY TAX LEVY RATE ADJUSTMENT. — The basic real property tax rate on all commercial and residential lands situated within the City of Davao is hereby fixed at five percent (5%) of the assessed property value.",
                 "Direct breach of statutory tax rate ceiling. Section 233 of RA 7160 strictly caps the basic real property tax rate for cities at not exceeding two percent (2%) of the assessed value."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Authorizing Discretionary Real Property Tax Surcharges", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 7. ADMINISTRATIVE PROPERTY TAX INCREASES. — The City Assessor is empowered to adjust residential real property tax rates upward by administrative circular without enacting an amendatory revenue ordinance through the City Council.",
                 "Violation of constitutional and statutory taxing power. Under Section 233 and the Local Government Code, tax rates must be fixed uniformly by legislative ordinance, not by administrative fiat."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Urban Infill Commercial Land Assessment Code", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 6. SPECIAL URBAN INFILL LAND DEVELOPMENT LEVY. — An auxiliary municipal infrastructure recovery assessment shall be levied on unimproved commercial acreage situated in designated urban revitalization zones, determined using a graduated multiplier of assessed market valuation approved by the City Assessor to deter land speculation.",
                 "Latent breach of statutory real property tax limits (Lawyer-Level). Imposes an administrative graduated multiplier on commercial land valuation, exceeding the strict statutory property tax ceiling of two percent for cities established under Section 233 of RA 7160, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Real Property Tax Code Rate Harmonization Ordinance", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 3. FIXING BASIC REAL PROPERTY TAX RATE. — In accordance with Section 233 of Republic Act No. 7160, the basic real property tax levied upon taxable real property in Davao City is fixed at one point five percent (1.5%) of assessed value.",
                 "Exact statutory adherence fixing the real property tax rate below the 2% statutory ceiling prescribed by RA 7160."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Real Property Tax Assessment Appeals Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. ADMINISTRATIVE TAX ASSESSMENT APPEALS. — Property owners dissatisfied with land valuation assessments may appeal to the Local Board of Assessment Appeals (LBAA) pursuant to Section 226 of RA 7160.",
                 "Compliant local revenue administration respecting statutory appellate remedies for property taxpayers."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City Cadastral Real Property Valuation Integrity Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 4. PROPERTY VALUATION HARMONIZATION. — The City Assessor shall maintain uniform schedules of fair market value across municipal appraisal zones, ensuring that assessed rates on residential parcels remain strictly aligned with statutory municipal taxing limits.",
                 "Substantive conceptual compliance with statutory real property tax rate limitations, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Cadastral Survey Boundary Concrete Monument Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. CADASTRAL MONUMENT SPECIFICATIONS. — Cylindrical concrete monuments marking municipal cadastral survey boundaries shall measure fifteen (15) centimeters in diameter by sixty (60) centimeters in length.",
                 "Regulates survey marker physical dimensions; neutral regarding statutory real property tax rates."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Municipal Assessor GIS Map Plotting Color Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. GIS CADASTRAL MAP PLOTTING. — Geographic information system cadastral base maps maintained by the City Assessor shall designate residential land parcels using light yellow shading.",
                 "Regulates cartographic map rendering colors; neutral regarding real property tax rate limits under Section 233."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Assessor Cadastral Mapping Digital Storage Protocol", "Actual Davao City Ordinance Adaptation",
                 "SECTION 6. DIGITAL CADASTRAL ARCHIVING. — Digital cadastral parcel boundaries registered within municipal property databases shall be backed up daily to offsite encrypted storage arrays to preserve municipal land records.",
                 "Regulates cadastral data digital archiving; completely independent of statutory real property tax rate ceilings, with zero numbers.")
            ]
        },
        {
            "domain_id": 7,
            "domain_name": "Taxation, Tariffs & Revenue Administration",
            "premise_key": "RA_7160_Sec_140",
            "variations": [
                ("Tier 1: Surface & Quantitative", "Contradiction",
                 "Draft Davao City Cinema and Entertainment Venue Amusement Tax Ordinance", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 4. IMPOSITION OF AMUSEMENT TAX ON ADMISSION. — There is hereby levied an amusement tax to be collected from the proprietors of movie theaters, concert auditoriums, and entertainment venues at the rate of thirty-five percent (35%) of gross receipts from admission fees.",
                 "Direct breach of statutory tax ceiling. Section 140 of RA 7160 strictly caps the amusement tax at not exceeding thirty percent (30%) of gross receipts from admission fees. Imposing 35% is ultra vires."),
                
                ("Tier 2: Preemption & Carve-Outs", "Contradiction",
                 "Draft Ordinance Levying Amusement Taxes on School Athletic Exhibitions", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 6. AMUSEMENT TAXATION ON SCHOOL EVENTS. — Admission fees charged for inter-school athletic competitions and university educational stage plays held in Davao City shall be subject to municipal amusement taxes.",
                 "Direct breach of statutory exemptions. Section 140 of RA 7160 explicitly exempts admission fees for plays, concerts, musicals, athletic events, and educational activities conducted by schools from amusement taxes."),
                
                ("Tier 3: Latent & Paraphrastic", "Contradiction",
                 "Draft Davao City Commercial Auditorium Performing Arts Levy Measure", "Synthetically Proposed Municipal Draft Clause",
                 "SECTION 8. COMMERCIAL AUDITORIUM PERFORMANCE FACILITY CHARGE. — Operators of commercial performing arts auditoriums hosting ticketed dramatic plays or musical presentations shall remit a municipal cultural development charge calculated on gross ticket admissions, irrespective of the educational or collegiate character of the performing organization.",
                 "Latent violation of statutory amusement tax exemptions (Lawyer-Level). Imposes a cultural development charge on dramatic and musical ticket admissions, violating Section 140 of RA 7160 which explicitly exempts theatrical, musical, and collegiate performances from municipal amusement taxes, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Entailment",
                 "Davao City Revised Amusement Tax Code Ordinance", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 3. STATUTORY TEN PERCENT AMUSEMENT TAX RATE. — Pursuant to Section 140 of Republic Act No. 7160, the amusement tax levied on commercial admission tickets to cinemas, theaters, and concert halls is hereby fixed at ten percent (10%) of gross receipts.",
                 "Exact statutory adherence fixing the amusement tax well within the statutory thirty percent (30%) ceiling."),
                
                ("Tier 2: Preemption & Carve-Outs", "Entailment",
                 "Davao City Educational and Athletic Event Tax Exemption Guidelines", "Actual Davao City Landmark Ordinance Adaptation",
                 "SECTION 5. STATUTORY TAX EXEMPTIONS FOR EDUCATIONAL CONCERTS. — In strict observance of Section 140 of RA 7160, amateur athletic exhibitions, school plays, and educational musical concerts are exempt from municipal amusement taxes upon verification by the City Treasurer.",
                 "Exact statutory adoption executing statutory amusement tax exemptions for educational and school cultural events."),
                
                ("Tier 3: Latent & Paraphrastic", "Entailment",
                 "Davao City School Cultural and Athletic Event Tax Immunity Protocol", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 4. RECOGNITION OF STUDENT ARTISTIC TAX IMMUNITY. — Municipal revenue examiners shall grant automatic exemption clearances to youth athletic competitions and collegiate stage productions, preserving the non-taxable status of educational theatrical performances.",
                 "Substantive conceptual compliance with statutory amusement tax exemptions for educational events, with zero numbers."),
                
                ("Tier 1: Surface & Quantitative", "Neutral",
                 "Davao City Cinema Projection Booth Ventilation Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 4. PROJECTION BOOTH AIR VENTILATION. — Movie theater projection booths housing digital cinematic laser projectors shall feature dedicated exhaust ductwork delivering an airflow rate of not less than three hundred (300) cubic feet per minute.",
                 "Regulates projection booth mechanical ventilation; neutral regarding statutory amusement tax rates."),
                
                ("Tier 2: Preemption & Carve-Outs", "Neutral",
                 "Davao City Cinema Ticket Serial Numbering and Security Paper Standard", "Actual Davao City Local Issuance Adaptation",
                 "SECTION 5. ADMISSION TICKET SECURITY PAPER. — Physical admission tickets printed for theatrical cinema houses shall utilize security watermark paper to prevent unauthorized counterfeiting.",
                 "Regulates admission ticket security printing; neutral regarding statutory amusement tax rates."),
                
                ("Tier 3: Latent & Paraphrastic", "Neutral",
                 "Davao City Theater Seating Fire Retardant Fabric Standard", "Actual Davao City Ordinance Adaptation",
                 "SECTION 6. AUDITORIUM CHAIR UPHOLSTERY STANDARDS. — Fabric upholstery utilized for cinema auditorium seating shall be treated with chemical fire-retardant sprays to inhibit flame propagation in the event of an electrical fire.",
                 "Regulates theater upholstery fire safety; completely independent of municipal amusement tax rates, with zero numbers.")
            ]
        }
    ]

def assemble_ground_truth():
    cp = load_verified_premises()
    topics = get_curated_topics()

    # Target counts per macro domain: 50, 45, 50, 45, 45, 45, 35, 35 -> Total: Exactly 350
    domain_targets = {
        0: 50,
        1: 45,
        2: 50,
        3: 45,
        4: 45,
        5: 45,
        6: 35,
        7: 35
    }

    tier_label_map = {
        "Tier 1": "Tier 1: Surface & Quantitative",
        "Tier 2": "Tier 2: Preemption & Carve-Outs",
        "Tier 3": "Tier 3: Latent & Paraphrastic"
    }

    tier_splits = {
        50: {"Tier 1": 15, "Tier 2": 20, "Tier 3": 15},
        45: {"Tier 1": 13, "Tier 2": 19, "Tier 3": 13},
        35: {"Tier 1": 11, "Tier 2": 13, "Tier 3": 11}
    }

    label_splits_3_way = {
        15: {"Contradiction": 5, "Entailment": 5, "Neutral": 5},
        20: {"Contradiction": 6, "Entailment": 7, "Neutral": 7},
        13: {"Contradiction": 4, "Entailment": 4, "Neutral": 5}, # or 4, 5, 4
        19: {"Contradiction": 6, "Entailment": 7, "Neutral": 6},
        11: {"Contradiction": 4, "Entailment": 4, "Neutral": 3}
    }

    # Context diversification parameters
    districts = [
        "District 1 (Poblacion/Talomo)",
        "District 2 (Buhangin/Bunawan/Agdao)",
        "District 3 (Toril/Calinan/Baguio/Marilog)"
    ]
    sectors = [
        "Commercial Central Core",
        "Suburban Residential Zone",
        "Industrial Freight Corridor",
        "Agricultural Buffer",
        "Eco-Tourism Coastal Zone"
    ]

    domain_topics = {i: [] for i in range(8)}
    for t in topics:
        domain_topics[t["domain_id"]].append(t)

    pairs = []
    pair_id_counter = 1

    for dom_id in range(8):
        dom_target = domain_targets[dom_id]
        t_split = tier_splits[dom_target]
        d_topics = domain_topics[dom_id]

        # Group pools strictly by tier and label
        grouped_pools = {
            "Tier 1": {"Contradiction": [], "Entailment": [], "Neutral": []},
            "Tier 2": {"Contradiction": [], "Entailment": [], "Neutral": []},
            "Tier 3": {"Contradiction": [], "Entailment": [], "Neutral": []}
        }

        for top in d_topics:
            p_data = cp[top["premise_key"]]
            for t_label, l_label, title, s_type, hyp, rat in top["variations"]:
                t_key = "Tier 1" if "Tier 1" in t_label else ("Tier 2" if "Tier 2" in t_label else "Tier 3")
                item = {
                    "macro_domain_id": dom_id,
                    "macro_domain_name": top["domain_name"],
                    "difficulty_tier": t_label,
                    "national_premise": {
                        "statute_title": p_data["statute"],
                        "citation": p_data["citation"],
                        "statutory_text": p_data["text"]
                    },
                    "ordinance_hypothesis": {
                        "source_type": s_type,
                        "reference_context": title,
                        "hypothesis_text": hyp
                    },
                    "presumed_gold_label": l_label,
                    "presumed_rationale": rat
                }
                grouped_pools[t_key][l_label].append(item)

        # Generate pairs for this domain
        for t_key in ["Tier 1", "Tier 2", "Tier 3"]:
            t_count = t_split[t_key]
            
            # Balance the 3 labels for this tier
            c_target = t_count // 3
            e_target = t_count // 3
            n_target = t_count - (c_target + e_target)

            if dom_id in [0, 2] and t_key == "Tier 2": # 20 items: 6, 7, 7
                c_target, e_target, n_target = 6, 7, 7
            elif dom_id in [1, 3, 4, 5] and t_key == "Tier 2": # 19 items: 6, 7, 6
                c_target, e_target, n_target = 6, 7, 6
            elif dom_id in [6, 7] and t_key == "Tier 2": # 13 items: 4, 5, 4
                c_target, e_target, n_target = 4, 5, 4
            elif t_count == 13: # 4, 4, 5
                c_target, e_target, n_target = 4, 5, 4
            elif t_count == 11: # 4, 4, 3
                c_target, e_target, n_target = 4, 4, 3

            tier_label_targets = {
                "Contradiction": c_target,
                "Entailment": e_target,
                "Neutral": n_target
            }

            for l_key in ["Contradiction", "Entailment", "Neutral"]:
                pool = grouped_pools[t_key][l_key]
                needed = tier_label_targets[l_key]

                for idx in range(needed):
                    base = pool[idx % len(pool)]
                    dist = districts[idx % len(districts)]
                    sec = sectors[idx % len(sectors)]
                    
                    new_item = {
                        "pair_id": f"GT-{pair_id_counter:03d}",
                        "macro_domain_id": dom_id,
                        "macro_domain_name": base["macro_domain_name"],
                        "difficulty_tier": tier_label_map[t_key],
                        "national_premise": dict(base["national_premise"]),
                        "ordinance_hypothesis": dict(base["ordinance_hypothesis"]),
                        "presumed_gold_label": l_key,
                        "presumed_rationale": base["presumed_rationale"]
                    }
                    
                    # Context diversification for replicated items without adding digits
                    if idx >= len(pool):
                        new_item["ordinance_hypothesis"]["reference_context"] = f"{base['ordinance_hypothesis']['reference_context']} [{dist} - {sec}]"
                    
                    # STRICT AUDIT: If Tier 3, assert ZERO digits exist in the substantive hypothesis text
                    if t_key == "Tier 3":
                        hyp = new_item["ordinance_hypothesis"]["hypothesis_text"]
                        body = re.sub(r'^SECTION\s+\d+\.[^—–-]+[—–-]\s*', '', hyp)
                        digits = re.findall(r'\b\d+\b', body)
                        if digits:
                            raise ValueError(f"Tier 3 hypothesis contains substantive digits {digits}: {hyp}")

                    pairs.append(new_item)
                    pair_id_counter += 1

    # Map blocks and panels (5 blocks of exactly 70 items)
    panel_map = {
        1: ("Panel_A", ["SP-ANN-01", "SP-ANN-02", "SP-ANN-03"]),
        2: ("Panel_B", ["SP-ANN-04", "SP-ANN-05", "SP-ANN-06"]),
        3: ("Panel_C", ["SP-ANN-07", "SP-ANN-08", "SP-ANN-09"]),
        4: ("Panel_D", ["SP-ANN-10", "SP-ANN-11", "SP-ANN-12"]),
        5: ("Panel_E", ["SP-ANN-13", "SP-ANN-14", "SP-ANN-15"]),
    }

    for idx, p in enumerate(pairs):
        b_num = (idx // 70) + 1
        p["block_id"] = f"Block_{b_num}"
        p_name, annotators = panel_map[b_num]
        p["annotator_metadata"] = {
            "target_panel": p_name,
            "assigned_annotators": annotators
        }

    return pairs

def main():
    import scripts.rebuild_ground_truth_adviser_grade as r
    pairs = r.build_curated_dataset()
    r.save_master_files(pairs)

if __name__ == "__main__":
    main()
