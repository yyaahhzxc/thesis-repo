"""
build_full_length_tier2_drafts.py
=================================
Constructs the 6 Stratified Tier 2 Full-Document Draft Ordinances (one per functional
legislative typology discovered in Table 4.4 of the Davao City Local Corpus EDA).

Designed to authentically mirror the wording, structural conventions, attached instruments
(MOAs, Deeds of Usufruct, financial reprogramming schedules, TCT zoning tables), and
empirical length variance (from ~480 words to ~3,500 words) of real Davao City Sangguniang
Panlungsod enactments (2021-2025).

Typology Mapping (Table 4.4):
- DRAFT-ORD-2026-01: Typology 01 - Substantive Regulatory & Penal (RA 7160 §458) [~3,400 words, 16 sections]
- DRAFT-ORD-2026-02: Typology 02 - Inter-Agency Agreements / MOA (RA 7160 §§22(c), 455) [~2,400 words, 5 ord sections + full attached MOA]
- DRAFT-ORD-2026-03: Typology 03 - Disaster Relief & QRF Funds (RA 10121 §21) [~880 words, 6 sections + financial schedule]
- DRAFT-ORD-2026-04: Typology 04 - Deeds of Donation & Usufruct (RA 7160 §22(a)(4)) [~1,900 words, 5 ord sections + full attached Deed of Usufruct & Secretary's Certificate]
- DRAFT-ORD-2026-05: Typology 05 - Temporary Road Closures (RA 7160 §21) [~480 words, 6 concise sections]
- DRAFT-ORD-2026-06: Typology 06 - Zoning & Subdivision Permits (RA 7160 §20, BP 220) [~1,250 words, 7 sections + TCT table]
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "data" / "tier2_draft_ordinances"
BENCHMARK_JSONL = REPO_ROOT / "data" / "tier2_draft_ordinances_benchmark.jsonl"

DRAFT_ORDINANCES = [
    # =========================================================================
    # TYPOLOGY 01: SUBSTANTIVE REGULATORY & PENAL (~3,400 words, 16 sections)
    # =========================================================================
    {
        "doc_id": "DRAFT-ORD-2026-01",
        "typology_id": 1,
        "functional_typology": "Substantive Regulatory & Penal",
        "statutory_authority": "RA 7160 §458",
        "proposed_ordinance_no": "ORDINANCE NO. 0114-26",
        "series_year": "Series of 2026",
        "session_info": "20th City Council\n11th Regular Session\nSeries of 2026",
        "committee": "Committee on Health and Committee on Agriculture, Aquaculture and Food",
        "title": "AN ORDINANCE ESTABLISHING THE DAVAO CITY VETERINARY PUBLIC HEALTH, ANIMAL WELFARE, AND RESPONSIBLE PET OWNERSHIP CODE, REGULATING THE OPERATION OF VETERINARY CLINICS, KENNELS, AND ANIMAL SHELTERS, AND PROVIDING PENALTIES FOR VIOLATIONS THEREOF",
        "enacting_clause": "Be it ordained by the Honorable Sangguniang Panlungsod of Davao City, in session assembled, that:",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the \"Davao City Veterinary Public Health and Responsible Pet Ownership Code of 2026\".",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard legislative title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF PRINCIPLES AND POLICIES",
                "text": "1. Pursuant to Section 16 and Section 458(a)(4)(viii) of Republic Act No. 7160, otherwise known as the Local Government Code of 1991, the City Government of Davao is mandated to promote the general welfare, safeguard public health, regulate the keeping of domestic animals, and establish effective measures to prevent and eradicate zoonotic diseases within its territorial jurisdiction.\n\n2. In harmony with Republic Act No. 9482, otherwise known as the Anti-Rabies Act of 2007, and Republic Act No. 8485, as amended by Republic Act No. 10631, otherwise known as the Animal Welfare Act of 1998, it is hereby declared the policy of the City of Davao to protect its residents from the fatal threat of rabies and other animal-borne illnesses while ensuring that all companion animals, livestock, and commercial kennel populations are treated humanely and maintained under sanitary conditions.\n\n3. Towards this end, the City Government shall institutionalize a unified barangay-based pet registration system, enforce mandatory annual anti-rabies immunization, regulate commercial veterinary establishments and breeding facilities, and strengthen the operational capacity of the City Veterinarian's Office (CVO) across all eleven (11) administrative districts of Davao City.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(viii); Republic Act No. 9482 §7",
                "legal_rationale": "Valid exercise of local police power and public health mandate under RA 7160 and RA 9482."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "As used in this Ordinance, the following terms and phrases shall mean and be construed as follows:\n\n1. Animal Shelter or Pound - refers to any public or private facility designated and maintained by the City Veterinarian's Office or an accredited non-governmental animal welfare organization for the temporary custody, quarantine, rehabilitation, and rehoming of stray, abandoned, or impounded domestic animals.\n\n2. Biting Incident - refers to any wound, scratch, abrasion, or mucosal exposure inflicted by a dog, cat, or other warm-blooded mammal upon a human being or another animal that carries a potential risk of rabies virus transmission.\n\n3. Commercial Kennel or Cattery - refers to any establishment, facility, or premises engaged in the commercial breeding, boarding, grooming, training, or retail sale of dogs, cats, or companion animals for fee or profit.\n\n4. City Veterinarian's Office (CVO) - refers to the primary department of the City Government of Davao responsible for veterinary public health, animal disease surveillance, livestock inspection, and the implementation of this Ordinance.\n\n5. Impounding - refers to the lawful seizure and temporary confinement of any stray, unregistered, or unvaccinated dog or cat found roaming at large in any public street, plaza, market, school ground, or common space without a leash or direct supervision of its owner.\n\n6.Leash Control - refers to the physical restraint of a dog in public places using a secure collar or harness attached to a strap, cord, or chain not exceeding two (2) meters in length held by a person of sufficient physical capacity to control the animal.\n\n7. Pet Owner - refers to any natural or juridical person keeping, harboring, or having custody, charge, or control of a dog, cat, or companion animal within the territorial jurisdiction of Davao City.\n\n8. Public Place - refers to any road, sidewalk, alley, park, barangay gym, public market, commercial establishment, transport terminal, or open area accessible to the general public.\n\n9. Stray Animal - refers to any dog or cat leaving its owner's premises or property boundary without being securely leashed or accompanied by its owner or handler.\n\n10. Veterinary Clinic or Hospital - refers to a licensed facility supervised by a duly registered veterinarian engaged in the medical diagnosis, surgical treatment, immunization, and hospitalization of animals.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitional section modeled after Davao City regulatory codes."
            },
            {
                "sec_num": 4,
                "sec_title": "SCOPE AND COVERAGE",
                "text": "The provisions of this Ordinance shall apply to all pet owners, animal handlers, livestock raisers, veterinary clinics, veterinary hospitals, pet grooming salons, commercial breeding kennels, pet shops, and animal welfare organizations residing or operating within the one hundred eighty-two (182) barangays across the First, Second, and Third Congressional Districts of the City of Davao.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard territorial scope and applicability clause."
            },
            {
                "sec_num": 5,
                "sec_title": "MANDATORY RABIES VACCINATION AND PET REGISTRATION",
                "text": "Every owner or custodian of a dog or cat within the City of Davao shall cause the animal to be regularly vaccinated against rabies upon reaching three (3) months of age and every year thereafter by the City Veterinarian's Office, an accredited barangay livestock aide, or a licensed private veterinarian.\n\nUpon vaccination, the pet owner shall register the animal with the Office of the Punong Barangay where the owner resides or directly with the District Veterinary Satellite Office in Poblacion, Talomo, Buhangin, Bunawan, Toril, Tugbok, Calinan, Baguio, Marilog, or Paquibato. The City Veterinarian's Office shall issue an official Certificate of Registration and a serialized metallic or radio-frequency identification (RFID) collar tag, which must be worn by the registered dog at all times when outside the owner's enclosed residential premises.\n\nLicensed private veterinary clinics operating within Davao City shall submit a monthly consolidated registry of all immunized dogs and cats to the City Veterinarian's Office on or before the tenth (10th) day of the succeeding month for inclusion in the Davao City Zoonotic Disease Surveillance Database.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 9482 §5; Republic Act No. 9482 §7",
                "legal_rationale": "Directly implements mandatory dog registration and immunization under RA 9482 §§5 and 7."
            },
            {
                "sec_num": 6,
                "sec_title": "DUTIES AND RESPONSIBILITIES OF PET OWNERS",
                "text": "All pet owners and handlers within the City of Davao shall strictly observe the following obligations:\n\n(a) Maintain their dogs within a securely fenced yard, enclosure, or residential compound so as to prevent the animal from escaping onto public streets or neighboring properties;\n\n(b) Keep their dogs on a secure leash not exceeding two (2) meters in length whenever walking or exercising the animal along public sidewalks, parks, coastal roads, or greenways, and place a humane basket muzzle on dogs with a documented history of aggression;\n\n(c) Immediately collect, bag, and properly dispose of any fecal matter deposited by their pet on any public street, sidewalk, park, or neighbor's property into designated sanitary waste receptacles;\n\n(d) Provide their animals with adequate daily nutrition, clean potable water, ventilated shelter protected from extreme heat and rain, and prompt veterinary care when ill or injured;\n\n(e) Refrain from abandoning any sick, aged, or unwanted domestic animal on public streets, vacant lots, or watershed areas.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 9482 §5; Republic Act No. 8485 §1",
                "legal_rationale": "Complies with statutory pet owner duties under RA 9482 §5 and Animal Welfare Act standards."
            },
            {
                "sec_num": 7,
                "sec_title": "ACCREDITATION OF VETERINARY CLINICS AND KENNELS",
                "text": "No commercial kennel, cattery, pet shop, pet grooming facility, or veterinary clinic shall operate or renew its Mayor's Business Permit through the Business Bureau of Davao City without first securing an Annual Veterinary Sanitary and Welfare Clearance from the City Veterinarian's Office and an Environmental Compliance Certificate from the City Environment and Natural Resources Office (CENRO).\n\nAll commercial kennels and pet shops shall maintain individual cages with impervious, non-slip flooring and sufficient floor space allowing each animal to stand, turn around, and lie down comfortably with limbs extended. Facilities shall install dedicated wastewater septic traps, biological medical waste bins for sharps and pathological tissues in accordance with City Health Office (CHO) infectious waste guidelines, and acoustic baffling to prevent excessive noise nuisance in adjoining residential zones.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 8485 §2; Republic Act No. 7160 §458",
                "legal_rationale": "Valid local licensing and sanitary regulation of commercial animal facilities under RA 8485 §2 and LGC."
            },
            {
                "sec_num": 8,
                "sec_title": "CAPTURE, IMPOUNDING, AND REDEMPTION OF STRAY ANIMALS",
                "text": "The City Veterinarian's Office, in coordination with trained Barangay Animal Control Teams, shall conduct regular humane stray animal capture operations across all barangays using padded capture nets, humane box traps, and ventilated transport vehicles.\n\nImpounded stray dogs and cats shall be brought to the Davao City Central Animal Pound in Barangay Maa or the designated District Impounding Center, where they shall be logged by breed, color, sex, collar tag number, and place of capture. Registered animals bearing valid identification tags shall be traced, and their recorded owners shall be notified via SMS or written barangay notice within twenty-four (24) hours. Unclaimed animals shall be held for a mandatory redemption and adoption period of seventy-two (72) hours from the time of capture, during which the owner may reclaim the animal upon payment of the corresponding impounding and feeding fees and proof of anti-rabies vaccination.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 9482 §7",
                "legal_rationale": "Complies with local impounding and pound management powers under RA 9482 §7."
            },
            {
                "sec_num": 9,
                "sec_title": "POUND DISPOSAL AND COMMERCIAL UTILIZATION OF UNCLAIMED ANIMALS",
                "text": "To minimize municipal pound maintenance expenses and generate supplemental city revenue, any impounded dog or cat that remains unclaimed after twenty-four (24) hours shall be summarily destroyed by high-voltage electrocution, exhaust gas asphyxiation, or mechanical clubbing without requiring veterinary supervision or sedative anesthesia.\n\nFurthermore, the City Veterinarian's Office is hereby authorized to sell unclaimed impounded dogs in bulk to accredited commercial slaughterhouses, public market vendors, and restaurant operators in Davao City for processing and retail sale as dog meat for human consumption, subject to the payment of a municipal slaughter permit fee of Three Hundred Pesos (P300.00) per head.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 8485 §6; Republic Act No. 9482 §7",
                "legal_rationale": "Directly contradicts Section 6 of RA 8485 (Animal Welfare Act, as amended by RA 10631) and Section 7(5)-(6) of RA 9482 (Anti-Rabies Act), which strictly prohibit the torture, electrocution, and commercial trade of dogs for meat and mandate that euthanasia of unclaimed pound animals be performed solely through humane veterinary methods approved by the Bureau of Animal Industry."
            },
            {
                "sec_num": 10,
                "sec_title": "MANDATORY QUARANTINE AND BITE INCIDENT MANAGEMENT",
                "text": "Whenever a dog or cat bites any person within Davao City, the owner or custodian of the animal shall immediately report the incident within twenty-four (24) hours to the Punong Barangay, the nearest District Health Center, or the City Veterinarian's Office, and shall surrender the biting animal for a mandatory fourteen (14) day clinical observation and quarantine period.\n\nThe owner of a biting dog that was unregistered or unvaccinated at the time of the incident, or was allowed to roam loose in a public place in violation of Section 6 hereof, shall be liable to pay for the full cost of post-exposure prophylaxis (PEP) anti-rabies vaccine and immunoglobulin administered to the bite victim at the Davao City Animal Bite Treatment Center or Southern Philippines Medical Center (SPMC). It shall be unlawful for any person to kill, conceal, or transport a biting animal during the fourteen-day observation period.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 9482 §5",
                "legal_rationale": "Harmonious local implementation of bite incident reporting and medical expense liability under RA 9482 §5."
            },
            {
                "sec_num": 11,
                "sec_title": "BARANGAY RABIES SURVEILLANCE AND ANIMAL WELFARE COMMITTEES",
                "text": "There is hereby organized in every barangay of Davao City a Barangay Rabies Surveillance and Animal Welfare Committee (BRSAWC) chaired by the Punong Barangay, with the Barangay Kagawad Chair on Health as Vice Chairperson, and composed of the Barangay Health Worker (BHW) Coordinator, a deputized Barangay Livestock Aide, a representative from the local public elementary or secondary school, and an accredited community animal welfare volunteer.\n\nThe BRSAWC shall maintain the updated Barangay Pet Registry, assist CVO veterinary teams during house-to-house mass vaccination campaigns, mediate neighborhood complaints regarding noise or sanitation involving domestic pets, and immediately report suspected rabid animals to the City Veterinarian's Office.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 9482 §7; Republic Act No. 7160 §389",
                "legal_rationale": "Valid institutionalization of barangay enforcement committees under RA 9482 and RA 7160."
            },
            {
                "sec_num": 12,
                "sec_title": "SCHEDULE OF REGULATORY REGISTRATION AND IMPOUNDING FEES",
                "text": "The City Treasurer's Office, upon assessment by the City Veterinarian's Office, shall collect the following regulatory and service fees, which shall accrue to the Davao City Veterinary Public Health and Rabies Eradication Trust Fund:\n\n| Nature of Regulatory Service / Clearance | Schedule of Fee (Php) | Renewal / Validity Period |\n|---|---|---|\n| Barangay Pet Registration and Metallic Collar Tag | P 100.00 per head | Annual |\n| Replacement of Lost Metallic or RFID Tag | P 150.00 per tag | Per Issuance |\n| Veterinary Sanitary Clearance (Veterinary Clinic / Hospital) | P 1,500.00 | Annual |\n| Veterinary Sanitary Clearance (Commercial Kennel / Pet Shop) | P 2,000.00 | Annual |\n| Daily Pound Maintenance and Subsistence Fee | P 150.00 per day | Per Day of Custody |\n| First Impounding Redemption Fee (Registered Pet) | P 500.00 | Per Redemption |\n| First Impounding Redemption Fee (Unregistered Pet) | P 1,000.00 | Per Redemption |\n\nIndigent pet owners certified by the City Social Welfare and Development Office (CSWDO) shall be exempt from the payment of the annual Pet Registration Fee during scheduled barangay mass immunization drives.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §153; Republic Act No. 9482 §7",
                "legal_rationale": "Reasonable local regulatory and service fees authorized under RA 7160 §153 and RA 9482 §7."
            },
            {
                "sec_num": 13,
                "sec_title": "PENAL PROVISIONS",
                "text": "Any person, pet owner, commercial kennel operator, or corporate officer who violates any provision of this Ordinance shall, upon conviction, be punished in accordance with the following graduated penalty schedule:\n\n(a) First Offense: A fine of Twenty-Five Thousand Pesos (Php 25,000.00) and mandatory community service of forty (40) hours;\n\n(b) Second Offense: A fine of Thirty-Five Thousand Pesos (Php 35,000.00) or imprisonment for a period of one (1) year and six (6) months;\n\n(c) Third and Subsequent Offenses: A fine of Fifty Thousand Pesos (Php 50,000.00) and imprisonment for a fixed term of three (3) years, plus permanent revocation of the Mayor's Business Permit in the case of commercial kennels, pet shops, or veterinary establishments.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Directly violates Section 458(a)(1)(iii) of Republic Act No. 7160 (Local Government Code of 1991), which strictly limits penal sanctions enacted by a Sangguniang Panlungsod to a maximum fine of Five Thousand Pesos (P5,000.00) and a maximum imprisonment of one (1) year."
            },
            {
                "sec_num": 14,
                "sec_title": "IMPLEMENTING RULES AND REGULATIONS",
                "text": "Within sixty (60) days from the approval of this Ordinance, the City Mayor, through a Technical Working Group composed of the City Veterinarian's Office, the City Health Office, the City Legal Office, the City Environment and Natural Resources Office, and the Liga ng mga Barangay - Davao City Chapter, shall formulate and issue the necessary Implementing Rules and Regulations (IRR) for the effective execution of this Code.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard administrative IRR delegation clause."
            },
            {
                "sec_num": 15,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If, for any reason, any section, clause, or provision of this Ordinance is declared unconstitutional or invalid by a court of competent jurisdiction, other sections or provisions hereof which are not affected by such declaration shall continue to be in full force and effect.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard legislative separability clause."
            },
            {
                "sec_num": 16,
                "sec_title": "REPEALING AND EFFECTIVITY CLAUSE",
                "text": "All existing city ordinances, executive orders, resolutions, or local regulations inconsistent with the provisions of this Ordinance are hereby repealed or modified accordingly. This Ordinance shall take effect fifteen (15) days after its complete publication in a newspaper of general circulation in the City of Davao.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard repealing and effectivity clause."
            }
        ],
        "attachment": None
    },

    # =========================================================================
    # TYPOLOGY 02: INTER-AGENCY AGREEMENTS & MOAs (~2,400 words, Ord + Full MOA)
    # =========================================================================
    {
        "doc_id": "DRAFT-ORD-2026-02",
        "typology_id": 2,
        "functional_typology": "Inter-Agency Agreements (MOA/MOU)",
        "statutory_authority": "RA 7160 §§22(c), 455",
        "proposed_ordinance_no": "ORDINANCE NO. 0218-26",
        "series_year": "Series of 2026",
        "session_info": "20th City Council\n14th Regular Session\nSeries of 2026",
        "committee": "Committee on Health and Committee on Information Technology",
        "title": "AN ORDINANCE AUTHORIZING THE CITY MAYOR TO ENTER INTO AND SIGN, FOR AND IN BEHALF OF THE CITY OF DAVAO, THE MEMORANDUM OF AGREEMENT TO BE ENTERED INTO BY AND BETWEEN THE CITY OF DAVAO AND MINDANAO DIGITAL HEALTH SYSTEMS CONSORTIUM, INC. PERTAINING TO THE INTER-HOSPITAL ELECTRONIC MEDICAL RECORD (EMR) AND TELEMEDICINE EXCHANGE NETWORK FOR DAVAO CITY DISTRICT HOSPITALS",
        "enacting_clause": "Be it ordained by the Sangguniang Panlungsod of Davao City in session assembled, that:",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known as \"AN ORDINANCE AUTHORIZING THE CITY MAYOR TO ENTER INTO AND SIGN, FOR AND IN BEHALF OF THE CITY OF DAVAO, THE MEMORANDUM OF AGREEMENT TO BE ENTERED INTO BY AND BETWEEN THE CITY OF DAVAO AND MINDANAO DIGITAL HEALTH SYSTEMS CONSORTIUM, INC. PERTAINING TO THE INTER-HOSPITAL ELECTRONIC MEDICAL RECORD (EMR) AND TELEMEDICINE EXCHANGE NETWORK FOR DAVAO CITY DISTRICT HOSPITALS\".",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard ordinance title clause modeled after Ord. No. 0673-21."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "Section 22 (a) (5) and (c) and Section 455 (b) (1) (vi) of the Local Government Code of 1991 or Republic Act No. 7160 provide that:\n\n\"Corporate Powers (Sec. 22). -\n(a) Every local government unit, as a corporation, shall have the following powers:\n(5) To enter into contracts; and\n(c) Unless otherwise provided in this Code, no contract may be entered into by the local chief executive in behalf of the local government unit without prior authorization by the sanggunian concerned. A legible copy of such contract shall be posted at a conspicuous place in the provincial capitol or the city, municipal or barangay hall.\n\nChief Executive; Powers, Duties and Compensation (Sec. 455). -\n(b) For efficient, effective and economical governance the purpose of which is the general welfare of the city and its inhabitants pursuant to Section 16 of this Code, the city mayor shall:\n(1) Exercise general supervision and control over all programs, projects, services, and activities of the city government, and in this connection, shall:\nxxx xxx xxx\n(vi) Represent the city in all its business transactions and sign in its behalf all bonds, contracts, and obligations, and such other documents upon authority of the sangguniang panlungsod or pursuant to law or ordinance.\"",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §22(c); Republic Act No. 7160 §455(b)(1)(vi)",
                "legal_rationale": "Verbatim statutory authority for council contract authorization under RA 7160 §§22(c) and 455(b)(1)(vi)."
            },
            {
                "sec_num": 3,
                "sec_title": "AUTHORITY",
                "text": "The City Mayor is hereby granted legislative authority to enter into and sign, for and in behalf of the City of Davao, the Memorandum of Agreement (MOA) to be entered into by and between the City of Davao and Mindanao Digital Health Systems Consortium, Inc. pertaining to the establishment, hosting, and operation of the Inter-Hospital Electronic Medical Record (EMR) and Telemedicine Exchange Network linking the City Health Office (CHO), Marilog District Hospital, Paquibato District Hospital, and Bunawan District Hospital for a period of three (3) years, which Memorandum of Agreement is hereto attached and made an integral part of this Ordinance.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §22(c)",
                "legal_rationale": "Valid legislative grant of authority to the City Mayor to execute an inter-agency MOA."
            },
            {
                "sec_num": 4,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If, for any reason, any section or provision of this Ordinance is declared unconstitutional or invalid, other sections or provisions hereof not affected by such declaration shall continue to be in full force and effect.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 5,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect immediately upon approval.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard effectivity clause."
            },
            {
                "sec_num": 6,
                "sec_title": "MOA ARTICLE I (PARTIES, PREMISES, AND PROJECT OBJECTIVES)",
                "text": "KNOW ALL PERSONS BY THESE PRESENTS: This Memorandum of Agreement, made and entered into by and between the CITY OF DAVAO, a local government unit organized and existing by virtue of the laws of the Republic of the Philippines, with official address at City Hall Building, City Hall Drive, Davao City, represented herein by its City Mayor, SEBASTIAN Z. DUTERTE, hereinafter referred to as the \"LGU\"; and MINDANAO DIGITAL HEALTH SYSTEMS CONSORTIUM, INC., a corporation organized and existing under the laws of the Republic of the Philippines, with principal office at Pryce Tower, J.P. Laurel Avenue, Bajada, Davao City, represented herein by its President and Chief Executive Officer, ENGR. LORENZO M. VALDEZ, hereinafter referred to as the \"SYSTEM PROVIDER\".\n\nWITNESSETH: That WHEREAS, Section 16 of Republic Act No. 7160 mandates every local government unit to promote health and safety and preserve the comfort and convenience of its inhabitants; WHEREAS, the LGU operates district hospitals, lying-in clinics, and rural health units serving indigent and geographically isolated communities across Marilog, Paquibato, Baguio, Calinan, Tugbok, and Bunawan Districts; WHEREAS, manual paper-based clinical charting and fragmented diagnostic laboratory records delay urgent patient referrals between peripheral city health facilities and the Southern Philippines Medical Center (SPMC); WHEREAS, the SYSTEM PROVIDER possesses technical expertise and accredited software infrastructure for hospital information management and real-time audio-visual tele-consultation; NOW THEREFORE, for and in consideration of the foregoing premises and the mutual covenants hereinafter set forth, the Parties hereby agree to deploy, operate, and maintain the Davao City Inter-Hospital Electronic Medical Record (EMR) and Telemedicine Exchange Network across participating municipal health facilities for a term of three (3) years commencing upon the signing of this Agreement.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §17; Republic Act No. 11223 §36",
                "legal_rationale": "Compliant health system interoperability and telemedicine partnership under the Local Government Code and Universal Health Care Act."
            },
            {
                "sec_num": 7,
                "sec_title": "MOA ARTICLE II (OBLIGATIONS OF THE PARTIES)",
                "text": "7.1 The SYSTEM PROVIDER shall undertake the following technical and operational obligations:\n(a) Install, configure, and maintain cloud-synchronized Electronic Medical Record (EMR) workstations, digital radiology viewing consoles, and high-definition telemedicine diagnostic terminals at the City Health Office (CHO), Marilog District Hospital, Paquibato District Hospital, and Bunawan District Hospital within forty-five (45) calendar days from the execution of this Agreement;\n(b) Provide twenty-four-hour technical helpdesk support, automated daily backups to redundant domestic servers, disaster recovery failover capability, and quarterly clinical software updates at no additional maintenance cost to the City Government;\n(c) Conduct comprehensive hands-on training workshops for municipal physicians, public health nurses, midwives, pharmacists, and medical technologists on digital admission charting, ICD-10 diagnostic coding, electronic prescription workflows, and remote specialist consultation protocols; and\n(d) Submit monthly system uptime reports, network latency audits, and anonymized epidemiological utilization summaries to the City Health Officer and the City Information Technology Center (CITC).\n\n7.2 The LGU, through the City Health Office and the City Information Technology Center (CITC), shall undertake the following counterpart obligations:\n(a) Designate two (2) permanent hospital information technology focal persons per participating facility to coordinate workstation installation, local area network routing, and role-based user authentication credentials;\n(b) Provide uninterrupted electrical power, uninterruptible power supply (UPS) units, and dedicated fiber-optic internet connectivity at each hospital and district health site;\n(c) Ensure that attending municipal medical personnel encode clinical admission notes, maternal delivery records, and PhilHealth electronic claim forms accurately within the platform; and\n(d) Conduct semi-annual clinical quality assurance reviews to evaluate referral turnaround times for emergency obstetric, pediatric, and trauma cases originating from hinterland barangays.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §17",
                "legal_rationale": "Standard bilateral technical and operational obligations in a municipal health IT agreement."
            },
            {
                "sec_num": 8,
                "sec_title": "MOA ARTICLE III (DATA OWNERSHIP AND COMMERCIAL DISCLOSURE)",
                "text": "In consideration of the software hosting discount granted to the LGU, the SYSTEM PROVIDER is hereby granted full commercial ownership over all patient medical records and is authorized to publish unredacted sensitive personal information—including patient full names, home addresses, psychiatric evaluations, HIV/AIDS test results, and genetic profiles—on a publicly accessible internet marketing directory and to sell such unredacted medical databases to third-party pharmaceutical advertisers and private insurance brokers without notifying or obtaining the consent of the patients.\n\nFurthermore, all patients admitted to Davao City district hospitals shall be permanently barred from exercising any right to access, correct, block, or request the erasure or deletion of their sensitive medical data stored in the commercial database, notwithstanding any privacy complaint.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 10173 §13; Republic Act No. 10173 §16",
                "legal_rationale": "Directly contradicts Section 13 (Sensitive Personal Information) and Section 16 (Rights of the Data Subject) of Republic Act No. 10173 (Data Privacy Act of 2012), as well as RA 11166 (Philippine HIV and AIDS Policy Act), which strictly prohibit the unauthorized processing, public disclosure, or commercial sale of sensitive medical and health records without explicit consent and guarantee the data subject's inalienable right to access, rectification, erasure, and blocking."
            },
            {
                "sec_num": 9,
                "sec_title": "MOA ARTICLE IV (TERM, LIABILITY, AMENDMENTS, AND VENUE)",
                "text": "9.1 This Memorandum of Agreement shall remain in full force and effect for a period of three (3) years from the date of notarization, renewable for another three (3) years upon mutual written agreement of the Parties and subject to prior ratificatory authority from the Sangguniang Panlungsod of Davao City. Either Party may pre-terminate this Agreement upon sixty (60) days prior written notice in the event of a material breach of the obligations stipulated herein.\n\n9.2 The SYSTEM PROVIDER shall hold the LGU, its elective officials, department heads, and medical personnel free and harmless from any third-party claim, civil action, damage, or liability arising from hardware defects, network downtime, or intellectual property infringement attributable to the fault or negligence of the SYSTEM PROVIDER, its officers, or employees.\n\n9.3 No modification, amendment, or supplement to this Agreement shall be valid or binding unless reduced into writing and signed by the duly authorized representatives of both Parties. Any judicial action or dispute arising from the interpretation or implementation of this Agreement that cannot be settled amicably within thirty (30) days shall be filed exclusively before the proper courts of the City of Davao, to the exclusion of all other venues. IN WITNESS WHEREOF, the Parties have hereunto affixed their signatures this ___ day of __________, 2026 in the City of Davao, Philippines.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard contract term, hold-harmless liability, amendment, venue stipulation, and attestation clause."
            }
        ],
        "attachment": {
            "type": "MEMORANDUM OF AGREEMENT",
            "party_a": "CITY OF DAVAO\nLGU\nRepresented by:\nSEBASTIAN Z. DUTERTE\nCity Mayor",
            "party_b": "MINDANAO DIGITAL HEALTH SYSTEMS CONSORTIUM, INC.\nSystem Provider\nRepresented by:\nENGR. LORENZO M. VALDEZ\nPresident & CEO",
            "witnesses": ["ATTY. FRANCIS MARK H. LAYOG\nActing City Administrator", "DR. TOMAS MIGUEL S. ABonado\nCity Health Officer"],
            "notary_appearances": ["SEBASTIAN Z. DUTERTE", "ENGR. LORENZO M. VALDEZ"]
        }
    },

    # =========================================================================
    # TYPOLOGY 03: DISASTER RELIEF & QRF FUNDS (~880 words, 6 sections + Table)
    # =========================================================================
    {
        "doc_id": "DRAFT-ORD-2026-03",
        "typology_id": 3,
        "functional_typology": "Disaster Relief & QRF Funds",
        "statutory_authority": "RA 10121 §21",
        "proposed_ordinance_no": "ORDINANCE NO. 0309-26",
        "series_year": "Series of 2026",
        "session_info": "20th City Council\n16th Regular Session\nSeries of 2026",
        "committee": "Committee on Finance, Ways and Means and Appropriations and Committee on Disaster Risk Reduction and Management",
        "title": "AN ORDINANCE APPROVING AND ADOPTING THE AMENDMENT AND UTILIZATION OF THE CALENDAR YEAR 2026 LOCAL DISASTER RISK REDUCTION AND MANAGEMENT FUND INVESTMENT PLAN (LDRRMFIP) AND QUICK RESPONSE FUND (QRF) OF THE CITY DISASTER RISK REDUCTION AND MANAGEMENT OFFICE (CDRRMO) IN THE TOTAL AMOUNT OF FIFTEEN MILLION PESOS (P15,000,000.00)",
        "enacting_clause": "Be it ordained by the Honorable Sangguniang Panlungsod of Davao City in session assembled, that:",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known as \"AN ORDINANCE APPROVING AND ADOPTING THE AMENDMENT AND UTILIZATION OF THE CALENDAR YEAR 2026 LOCAL DISASTER RISK REDUCTION AND MANAGEMENT FUND INVESTMENT PLAN (LDRRMFIP) AND QUICK RESPONSE FUND (QRF) OF THE CITY DISASTER RISK REDUCTION AND MANAGEMENT OFFICE (CDRRMO) IN THE TOTAL AMOUNT OF FIFTEEN MILLION PESOS (P15,000,000.00)\".",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard ordinance title clause modeled after Ord. No. 0692-21 and Ord. No. 0598-24."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY AND LEGAL BASIS",
                "text": "Section 324 (d) of Republic Act No. 7160 or the Local Government Code of 1991, as amended, and Section 21 of Republic Act No. 10121, otherwise known as the Philippine Disaster Risk Reduction and Management Act of 2010, provide that not less than five percent (5%) of the estimated revenue from regular sources shall be set aside as the Local Disaster Risk Reduction and Management Fund (LDRRMF) to support disaster risk management activities.\n\nOf the amount appropriated for the LDRRMF, thirty percent (30%) shall be allocated as a Quick Response Fund (QRF) or stand-by fund for relief and recovery programs in order that the situation and living conditions of people in communities or areas stricken by disasters, calamities, epidemics, or complex emergencies may be normalized as quickly as possible.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 10121 §21; Republic Act No. 7160 §324(d)",
                "legal_rationale": "Accurately states the statutory mandate governing the 5% LDRRMF and 30% Quick Response Fund under RA 10121 §21."
            },
            {
                "sec_num": 3,
                "sec_title": "AMENDMENT AND SCHEDULE OF FUND UTILIZATION",
                "text": "The Davao City Disaster Risk Reduction and Management Fund Investment Plan (DCDRRMFIP) for Calendar Year 2026 is hereby amended to fund urgent flood relief and rehabilitation operations in Paquibato and Marilog Districts as follows:\n\n| Budget Item / Program Description | Source Allocation | Appropriated Amount (Php) |\n|---|---|---|\n| FROM: Unprogrammed Disaster Mitigation Equipment Reserve | 70% Mitigation Fund | P 15,000,000.00 |\n| TO: 1. Procurement of Modular Family Evacuation Tents and Hygiene Kits for Paquibato District |LDRRMF Relief | P 4,500,000.00 |\n| TO: 2. Deployment of Mobile Potable Water Filtration Units for Marilog District Barangays | LDRRMF Relief | P 1,500,000.00 |\n| TO: 3. Pre-Disaster Administrative Overtime Bonuses and Regular Clerical Salaries | 30% Quick Response Fund | P 9,000,000.00 |\n| TOTAL REPROGRAMMED APPROPRIATION | | P 15,000,000.00 |",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Schedule table of reprogrammed appropriations modeled after Ord. No. 0692-21 §2."
            },
            {
                "sec_num": 4,
                "sec_title": "UTILIZATION OF QUICK RESPONSE FUND FOR REGULAR SALARIES",
                "text": "Notwithstanding the absence of a declared State of Calamity, the City Treasurer and the City Budget Officer are hereby authorized to immediately disburse Nine Million Pesos (P9,000,000.00) or sixty percent (60%) of the thirty percent (30%) Quick Response Fund (QRF) standby allocation to pay regular monthly administrative salaries, year-end productivity bonuses, and office furniture purchases for permanent clerical personnel at City Hall, without requiring any Sangguniang Panlungsod resolution declaring a state of calamity.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 10121 §21; Republic Act No. 7160 §324(d)",
                "legal_rationale": "Directly contradicts Section 21 of Republic Act No. 10121 and Section 324(d) of Republic Act No. 7160, which strictly restrict the 30% Quick Response Fund (QRF) to a standby fund exclusively for post-disaster relief and recovery programs in areas declared under a State of Calamity by the local sanggunian, and prohibit the diversion of calamity funds to regular personnel services (PS) or administrative bonuses."
            },
            {
                "sec_num": 5,
                "sec_title": "ACCOUNTING AND AUDITING RULES",
                "text": "Subject to the provisions of the preceding section, all disbursements and utilization of funds for emergency evacuation kits and mobile water filtration units shall be governed by existing government budgeting, accounting, and auditing rules and regulations of the Department of Budget and Management (DBM), the Commission on Audit (COA), and Republic Act No. 9184, otherwise known as the Government Procurement Reform Act.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 9184 §4",
                "legal_rationale": "Standard fiscal compliance provision modeled after Ord. No. 0692-21 §3."
            },
            {
                "sec_num": 6,
                "sec_title": "SEPARABILITY AND EFFECTIVITY CLAUSE",
                "text": "If, for any reason, any section or provision of this Ordinance is declared unconstitutional or invalid, other sections or provisions hereof which are not affected by such declaration shall continue to be in full force and effect. This Ordinance shall take effect immediately upon approval.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability and effectivity clause."
            }
        ],
        "attachment": None
    },

    # =========================================================================
    # TYPOLOGY 04: DEEDS OF DONATION & USUFRUCT (~1,900 words, Ord + Full Deed)
    # =========================================================================
    {
        "doc_id": "DRAFT-ORD-2026-04",
        "typology_id": 4,
        "functional_typology": "Deeds of Donation & Usufruct",
        "statutory_authority": "RA 7160 §22(a)(4)",
        "proposed_ordinance_no": "ORDINANCE NO. 0412-26",
        "series_year": "Series of 2026",
        "session_info": "20th City Council\n18th Regular Session\nSeries of 2026",
        "committee": "Committee on Finance, Ways and Means and Appropriations and Committee on Education, Science and Technology, Arts and Culture",
        "title": "AN ORDINANCE AUTHORIZING THE CITY MAYOR TO ENTER INTO AND SIGN, FOR AND IN BEHALF OF THE CITY OF DAVAO, THE DEED OF USUFRUCT TO BE ENTERED INTO BY AND BETWEEN THE CITY OF DAVAO AND SOUTHERN MINDANAO COMMERCIAL PROPERTIES, INC. OVER A COMMERCIAL BUILDING SPACE SITUATED AT CATALUNAN GRANDE ROAD, BARANGAY CATALUNAN GRANDE, TALOMO DISTRICT, DAVAO CITY, COVERED BY TRANSFER CERTIFICATE OF TITLE NO. 146-2019004518, FOR THE OPERATION OF A SATELLITE PUBLIC LIBRARY AND CIVIL REGISTRY DESK",
        "enacting_clause": "Be it ordained by the Honorable Sangguniang Panlungsod of Davao City, in session assembled, that:",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known as \"AN ORDINANCE AUTHORIZING THE CITY MAYOR TO ENTER INTO AND SIGN, FOR AND IN BEHALF OF THE CITY OF DAVAO, THE DEED OF USUFRUCT TO BE ENTERED INTO BY AND BETWEEN THE CITY OF DAVAO AND SOUTHERN MINDANAO COMMERCIAL PROPERTIES, INC. OVER A COMMERCIAL BUILDING SPACE SITUATED AT CATALUNAN GRANDE ROAD, BARANGAY CATALUNAN GRANDE, TALOMO DISTRICT, DAVAO CITY, COVERED BY TRANSFER CERTIFICATE OF TITLE NO. 146-2019004518, FOR THE OPERATION OF A SATELLITE PUBLIC LIBRARY AND CIVIL REGISTRY DESK\".",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard title clause modeled after Ord. No. 0485-21."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "Section 22 (a) (4), (5) and (c) and Section 455 (b) (1) (vi) of Republic Act No. 7160 or the \"Local Government Code of 1991\" provide that:\n\n\"Corporate Powers (Sec. 22). -\n(a) Every local government unit, as a corporation, shall have the following powers:\n(4) To acquire and convey real or personal property;\n(5) To enter into contracts; and\n(c) Unless otherwise provided in this Code, no contract may be entered into by the local chief executive in behalf of the local government unit without prior authorization by the sanggunian concerned. A legible copy of such contract shall be posted at a conspicuous place in the provincial capitol or the city, municipal or barangay hall.\n\nChief Executive; Powers, Duties and Compensation (Sec. 455). -\n(b) For efficient, effective and economical governance the purpose of which is the general welfare of the city and its inhabitants pursuant to Section 16 of this Code, the city mayor shall:\n(1) Exercise general supervision and control over all programs, projects, services, and activities of the city government and in this connection, shall:\n(vi) Represent the city in all its business transactions and sign in its behalf all bonds, contracts, and obligations, and such other documents upon authority of the sangguniang panlungsod or pursuant to law or ordinance.\"",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §22(a)(4); Republic Act No. 7160 §22(c)",
                "legal_rationale": "Verbatim corporate and property acquisition powers under RA 7160 §22."
            },
            {
                "sec_num": 3,
                "sec_title": "AUTHORITY",
                "text": "The City Mayor is hereby granted legislative authority to enter into and sign, for and in behalf of the City of Davao, the Deed of Usufruct to be entered into by and between the City of Davao and Southern Mindanao Commercial Properties, Inc. over a one thousand five hundred (1,500) square meter commercial space situated at Ground Floor, Southgate Town Center, Catalunan Grande Road, Barangay Catalunan Grande, Talomo District, this City, embraced in Transfer Certificate of Title No. 146-2019004518, for the operation of the Talomo North District Satellite Public Library, Youth Digital Reading Hub, and Civil Registry Satellite Desk.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §22(c)",
                "legal_rationale": "Valid legislative authorization for the City Mayor to execute a Deed of Usufruct."
            },
            {
                "sec_num": 4,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If, for any reason, any section or provision of this Ordinance is declared unconstitutional or invalid, other sections or provisions hereof not affected by such declaration shall continue to be in full force and effect.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 5,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect immediately upon approval.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard effectivity clause."
            },
            {
                "sec_num": 6,
                "sec_title": "DEED OF USUFRUCT CLAUSE I (PARTIES AND TERM OF GRANT)",
                "text": "KNOW ALL MEN BY THESE PRESENTS: This Deed of Usufruct is executed by and between SOUTHERN MINDANAO COMMERCIAL PROPERTIES, INC., a corporation duly organized and existing under the laws of the Republic of the Philippines, with principal office at J.P. Laurel Avenue, Davao City, represented in this Deed by its Corporate President, ATTY. RICARDO V. MONTEMAYOR, by virtue of Board Resolution No. 08-2026 embodied in the Secretary's Certificate hereto attached as Annex \"A\", hereinafter referred to as the \"OWNER\"; and the CITY OF DAVAO, a local government unit organized and existing under the laws of the Republic of the Philippines, with principal office at City Hall, San Pedro Street, Davao City, represented herein by its City Mayor, SEBASTIAN Z. DUTERTE, hereinafter referred to as the \"USUFRUCTUARY\".\n\nWITNESSETH: WHEREAS, the OWNER is the registered and absolute owner of a commercial complex covered by Transfer Certificate of Title No. 146-2019004518 located in Barangay Catalunan Grande, Talomo District, Davao City; WHEREAS, the USUFRUCTUARY desires to establish a modern Satellite Public Library and Civil Registry Desk accessible to residents and students of Catalunan Grande, Catalunan Pequeño, and Mintal; NOW, THEREFORE, the OWNER hereby grants unto the USUFRUCTUARY the full, rent-free right of usufruct over a 1,500-square-meter portion of the Ground Floor of Southgate Town Center for a period of ten (10) years commencing upon the execution of this Deed.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 386 Art. 562; Republic Act No. 7160 §22(a)(4)",
                "legal_rationale": "Valid constitution of usufructuary rights in favor of a local government unit under the Civil Code and RA 7160."
            },
            {
                "sec_num": 7,
                "sec_title": "DEED OF USUFRUCT CLAUSE II (CARE AND MAINTENANCE)",
                "text": "1. The USUFRUCTUARY shall utilize the Property exclusively for the operation of the District Satellite Public Library, Youth Digital Hub, and Civil Registry Satellite Office, and shall take care of the premises with the diligence of a good father of a family in accordance with Article 589 of the New Civil Code of the Philippines.\n\n2. The USUFRUCTUARY may introduce non-structural interior partitions, bookshelves, computer local-area network cabling, air-conditioning units, and official signage necessary for its public operations, and shall pay for actual monthly consumption of water, electricity, and telecommunications utilities metered separately to the premises.\n\n3. The USUFRUCTUARY shall not sublease, assign, or transfer its right of usufruct over the premises to any third party without the prior written consent of the OWNER.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 386 Art. 589",
                "legal_rationale": "Standard usufructuary maintenance and non-assignment covenants under the Civil Code."
            },
            {
                "sec_num": 8,
                "sec_title": "DEED OF USUFRUCT CLAUSE III (NATIONAL TAX EXEMPTION GRANT)",
                "text": "In consideration of the rent-free usufruct granted herein, the Sangguniang Panlungsod of Davao City and the City Treasurer hereby grant the OWNER, Southern Mindanao Commercial Properties, Inc., and all its subsidiary retail corporations a perpetual and irrevocable exemption from the payment of National Corporate Income Taxes, twelve percent (12%) Value-Added Tax (VAT) under the National Internal Revenue Code, and Bureau of Customs import duties on all imported construction materials and commercial merchandise across the Philippines.\n\nThe City Treasurer of Davao City is hereby authorized to issue binding Certificates of National Tax Immunity barring the Bureau of Internal Revenue (BIR) and the Bureau of Customs (BOC) from assessing or collecting any national internal revenue taxes or customs tariffs from the OWNER.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7160 §133(a); Republic Act No. 7160 §192",
                "legal_rationale": "Directly contradicts Section 133(a) and (d) and Section 192 of Republic Act No. 7160 (Local Government Code of 1991) and the National Internal Revenue Code, which strictly prohibit local government units from levying, altering, or granting exemptions from national internal revenue taxes (Corporate Income Tax and Value-Added Tax) or customs duties administered exclusively by the Bureau of Internal Revenue and Bureau of Customs."
            }
        ],
        "attachment": {
            "type": "DEED OF USUFRUCT",
            "party_a": "SOUTHERN MINDANAO COMMERCIAL PROPERTIES, INC.\nOwner\nRepresented by:\nATTY. RICARDO V. MONTEMAYOR\nCorporate President",
            "party_b": "CITY OF DAVAO\nUsufructuary\nRepresented by:\nSEBASTIAN Z. DUTERTE\nCity Mayor",
            "witnesses": ["ATTY. FRANCIS MARK H. LAYOG\nActing City Administrator", "ENGR. MARITES B. MONTEMAYOR\nCorporate Treasurer"],
            "notary_appearances": ["ATTY. RICARDO V. MONTEMAYOR", "SEBASTIAN Z. DUTERTE"],
            "secretary_certificate": {
                "secretary_name": "ATTY. CLARISSA M. DELGADO",
                "corp_name": "SOUTHERN MINDANAO COMMERCIAL PROPERTIES, INC.",
                "board_date": "January 19, 2026",
                "resolution_no": "Resolution No. 08-2026",
                "authorized_signatory": "Atty. Ricardo V. Montemayor"
            }
        }
    },

    # =========================================================================
    # TYPOLOGY 05: TEMPORARY ROAD CLOSURES (~480 words, 6 concise sections)
    # =========================================================================
    {
        "doc_id": "DRAFT-ORD-2026-05",
        "typology_id": 5,
        "functional_typology": "Temporary Road Closures",
        "statutory_authority": "RA 7160 §21",
        "proposed_ordinance_no": "ORDINANCE NO. 0504-26",
        "series_year": "Series of 2026",
        "session_info": "20th City Council\n19th Regular Session\nSeries of 2026",
        "committee": "Committee on Transportation and Communications",
        "title": "AN ORDINANCE FOR THE TEMPORARY CLOSURE OF ROAD TO VEHICULAR TRAFFIC ALONG A PORTION OF STA. ANA AVENUE AND GUERRERO STREET, BARANGAY 29-C, POBLACION DISTRICT, ON AUGUST 14-16, 2026 IN CONNECTION WITH THE DAVAO CITY AGRO-INDUSTRIAL AND ARTISAN TRADE FAIR, AND IMPOSING A PERMANENT MUNICIPAL HIGHWAY PASSAGE TOLL ON NATIONAL ARTERIAL ROADS",
        "enacting_clause": "Be it ordained by the Sangguniang Panlungsod of Davao City in session assembled, that:",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known as \"AN ORDINANCE FOR THE TEMPORARY CLOSURE OF ROAD TO VEHICULAR TRAFFIC ALONG A PORTION OF STA. ANA AVENUE AND GUERRERO STREET, BARANGAY 29-C, POBLACION DISTRICT, ON AUGUST 14-16, 2026 IN CONNECTION WITH THE DAVAO CITY AGRO-INDUSTRIAL AND ARTISAN TRADE FAIR, AND IMPOSING A PERMANENT MUNICIPAL HIGHWAY PASSAGE TOLL ON NATIONAL ARTERIAL ROADS\".",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard road closure ordinance title modeled after Ord. No. 003-22 and Ord. No. 0197-23."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "Section 21 (c) and (d) of Republic Act No. 7160, otherwise known as the \"Local Government Code of 1991\", provides that any national or local road, alley, park, or square may be temporarily closed during an actual emergency, or fiesta celebrations, public rallies, agricultural or industrial fairs, or the undertaking of public works and highways, Telecommunications, and waterworks projects, the duration of which shall be specified by the local chief executive in a written order.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §21(c); Republic Act No. 7160 §21(d)",
                "legal_rationale": "Quotes the exact statutory basis for temporary road closures under RA 7160 §21(c)-(d)."
            },
            {
                "sec_num": 3,
                "sec_title": "TEMPORARY ROAD CLOSURE SCHEDULE",
                "text": "In connection with the celebration of the Davao City Agro-Industrial and Artisan Trade Fair, the Barangay Council of Barangay 29-C, Poblacion District, in coordination with the City Transport and Traffic Management Office (CTTMO), is hereby authorized to temporarily close the innermost lane of Sta. Ana Avenue corner Guerrero Street to vehicular traffic from 6:00 PM to 11:00 PM on August 14 to 16, 2026, subject to the installation of directional detour signage and emergency vehicle access lanes.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §21(c)",
                "legal_rationale": "Valid temporary street closure for an agricultural and artisan trade fair under RA 7160 §21(c)."
            },
            {
                "sec_num": 4,
                "sec_title": "PERMANENT HIGHWAY TOLL BARRICADES AND PASSAGE TAX",
                "text": "To generate continuing traffic management funds for the Barangay Council and the CTTMO, permanent toll barricades shall be erected along the Pan-Philippine National Highway (Davao-Agusan National Arterial Road) and all national primary highways entering Davao City, and a compulsory Municipal Transit Toll and Commodity Passage Tax of Five Hundred Pesos (P500.00) per trip shall be collected from every inter-provincial cargo truck, agricultural hauler, and public utility bus carrying goods or passengers into or out of the city; any vehicle refusing to pay the highway passage tax shall be impounded without warrant.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7160 §133(e); Republic Act No. 7160 §21",
                "legal_rationale": "Directly contradicts Section 133(e) of Republic Act No. 7160 (Local Government Code of 1991), which expressly prohibits local government units from levying taxes, fees, charges, or tolls on countryside and barangay business enterprises and on any goods or commodities carried into or out of, or passing through, the territorial jurisdictions of local government units in the guise of charges for wharfage, tolls for bridges or highways, or other taxes in any form whatever."
            },
            {
                "sec_num": 5,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If, for any reason, any section or provision of this Ordinance is declared unconstitutional or invalid, other sections or provisions hereof not affected by such declaration shall continue to be in full force and effect.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 6,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect immediately upon approval.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard effectivity clause."
            }
        ],
        "attachment": None
    },

    # =========================================================================
    # TYPOLOGY 06: ZONING & SUBDIVISION PERMITS (~1,250 words, 7 sections + TCT Table)
    # =========================================================================
    {
        "doc_id": "DRAFT-ORD-2026-06",
        "typology_id": 6,
        "functional_typology": "Zoning & Subdivision Permits",
        "statutory_authority": "RA 7160 §20, BP 220",
        "proposed_ordinance_no": "ORDINANCE NO. 0615-26",
        "series_year": "Series of 2026",
        "session_info": "20th City Council\n21st Regular Session\nSeries of 2026",
        "committee": "Committee on Housing, Rural and Urban Development (Low-End Projects) and Committee on Land Use",
        "title": "AN ORDINANCE GRANTING THE APPLICATION OF MINDANAO GREENFIELDS AGRO-INDUSTRIAL DEVELOPMENT CORPORATION FOR THE RECLASSIFICATION AND REZONING OF PARCELS OF LAND CONSISTING OF A TOTAL AREA OF 148,500 SQUARE METERS, COVERED BY TCT NOS. 146-2021008412, 146-2021008413, AND 146-2021008414, FROM PRIME IRRIGATED AGRICULTURAL ZONE TO HEAVY INDUSTRIAL ZONE, LOCATED IN BARANGAY CALLAWA AND BARANGAY MANDUG, BUHANGIN DISTRICT, THIS CITY",
        "enacting_clause": "Be it ordained by the Sangguniang Panlungsod of Davao City in session assembled, that:",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known as \"AN ORDINANCE GRANTING THE APPLICATION OF MINDANAO GREENFIELDS AGRO-INDUSTRIAL DEVELOPMENT CORPORATION FOR THE RECLASSIFICATION AND REZONING OF PARCELS OF LAND CONSISTING OF A TOTAL AREA OF 148,500 SQUARE METERS, COVERED BY TCT NOS. 146-2021008412, 146-2021008413, AND 146-2021008414, FROM PRIME IRRIGATED AGRICULTURAL ZONE TO HEAVY INDUSTRIAL ZONE, LOCATED IN BARANGAY CALLAWA AND BARANGAY MANDUG, BUHANGIN DISTRICT, THIS CITY\".",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard zoning reclassification title modeled after Ord. No. 0707-21 and Ord. No. 0853-22."
            },
            {
                "sec_num": 2,
                "sec_title": "COMMON REGULATIONS FOR GENERAL ZONES",
                "text": "Article V of the Comprehensive Zoning Ordinance of Davao City provides Common Regulations for General Zones:\n\n\"Article V, Paragraph 1 (REVIEW OF GENERAL ZONES). - General zones are subject to review by the Local Zoning Review Committee every five (5) years from the enactment of this Ordinance. Any amendment thereof as recommended by the committee shall be in accordance with the provision of Article XIV Section 14.\n\nArticle V, Paragraph 2 (RECLASSIFICATION AND CHANGE OF ZONE REQUIREMENT). - Reclassification from agricultural zone to non-agricultural use and any change from one general zone to another general zone must be approved by three-fourths (3/4) vote of all the members of the Sangguniang Panlungsod through a resolution and an ordinance. Any change of general zone to another zone shall be considered as an amendment of the zoning ordinance and must comply with the provision of Article XIV, Section 14 hereof.\n\nARTICLE XIV, SECTION 14 (AMENDMENTS TO THE ZONING ORDINANCE). - Changes in the Zoning Ordinance as a result of the review by the Local Zoning Review Committee shall be treated as an amendment, provided that any amendment to the Zoning Ordinance or provision thereof shall be subject to public hearing and sectoral consultation to be conducted by the Local Zoning Review Committee and review evaluation of the said Local Zoning Review Committee and shall be carried out through a resolution/ordinance upon three-fourths (3/4) majority votes of all the members of the Sangguniang Panlungsod.\"",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(2)(vii)",
                "legal_rationale": "Verbatim zoning ordinance amendment rules modeled after Ord. No. 0707-21 §2 and Ord. No. 0853-22 §2."
            },
            {
                "sec_num": 3,
                "sec_title": "COVERAGE AND SCHEDULE OF RECLASSIFIED PARCELS",
                "text": "This Ordinance shall cover the grant of the application of Mindanao Greenfields Agro-Industrial Development Corporation, represented by its Vice President for Operations, Engr. Victoriano S. Alcantara, for the reclassification of properties located in Barangay Callawa and Barangay Mandug, Buhangin District, this City, covered by the following Transfer Certificates of Title, to wit:\n\n| Transfer Certificate of Title Number | Registered Lot Area | Current Zone Classification | Proposed Zonal Classification |\n|---|---|---|---|\n| TCT No. 146-2021008412 | 64,200 sq.m. | Prime Irrigated Agricultural Zone | Heavy Industrial Zone (I-2) |\n| TCT No. 146-2021008413 | 51,800 sq.m. | Prime Irrigated Agricultural Zone | Heavy Industrial Zone (I-2) |\n| TCT No. 146-2021008414 | 32,500 sq.m. | Agricultural Non-Tillage Zone | Commercial-2 / Logistics Zone |\n| Total Reclassified Area | 148,500 sq.m. | | |",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard technical schedule of TCT parcels modeled after Ord. No. 0707-21 §3."
            },
            {
                "sec_num": 4,
                "sec_title": "AGRICULTURAL RECLASSIFICATION CEILING AND CONVERSION",
                "text": "To accelerate industrial warehousing expansion across Buhangin, Calinan, and Tugbok Districts, the Sangguniang Panlungsod hereby authorizes the cumulative reclassification of up to forty-five percent (45%) of the total agricultural land area of Davao City into industrial and commercial zones, expressly superseding the fifteen percent (15%) statutory reclassification ceiling for highly urbanized cities.\n\nFurthermore, prime irrigated agricultural lands serviced by National Irrigation Administration (NIA) communal irrigation systems covered by this Ordinance are hereby summarily converted into Heavy Industrial Zones without securing any Land Use Conversion Order from the Department of Agrarian Reform (DAR) or certification from the Department of Agriculture (DA).",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7160 §20(a); Republic Act No. 6657 §65",
                "legal_rationale": "Directly contradicts Section 20(a)(1) and (b) of Republic Act No. 7160 (Local Government Code of 1991) and Section 65 of Republic Act No. 6657 (Comprehensive Agrarian Reform Law), which strictly limit a highly urbanized city's authority to reclassify agricultural lands to a maximum of fifteen percent (15%) of total agricultural land at the time of the passage of the Code, prohibit the reclassification of irrigated agricultural lands serviced by NIA irrigation systems, and vest exclusive authority to approve actual land use conversion in the Department of Agrarian Reform (DAR)."
            },
            {
                "sec_num": 5,
                "sec_title": "SITE DEVELOPMENT AND DRAINAGE REQUIREMENTS",
                "text": "The applicant developer shall submit a comprehensive Site Development Plan to the City Planning and Development Office (CPDO) and the Office of the City Building Official (OCBO) within ninety (90) days from the effectivity of this Ordinance. The development shall incorporate an on-site stormwater retention basin to prevent surface runoff into the Davao River watershed and maintain a ten (10) meter greenbelt perimeter buffer planted with native tree species along boundaries adjoining residential settlements in Barangay Mandug.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(2)(vi); Presidential Decree No. 1096 §301",
                "legal_rationale": "Valid local site development and drainage engineering conditions."
            },
            {
                "sec_num": 6,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If, for any reason, any section or provision of this Ordinance is declared unconstitutional or invalid, other sections or provisions hereof which are not affected by such declaration shall continue to be in full force and effect.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 7,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect immediately upon approval.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard effectivity clause."
            }
        ],
        "attachment": None
    }
]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # Remove any old files in OUT_DIR
    for old_f in OUT_DIR.glob("*.json"):
        old_f.unlink()

    print("=" * 80)
    print("BUILDING 6 STRATIFIED TIER 2 FULL-DOCUMENT DRAFT ORDINANCES (TABLE 4.4 TYPOLOGIES)")
    print("=" * 80)

    with open(BENCHMARK_JSONL, "w", encoding="utf-8") as bf:
        for doc in DRAFT_ORDINANCES:
            doc_path = OUT_DIR / f"{doc['doc_id']}.json"
            with open(doc_path, "w", encoding="utf-8") as f:
                json.dump(doc, f, indent=2, ensure_ascii=False)
            bf.write(json.dumps(doc, ensure_ascii=False) + "\n")

            sec_words = sum(len(s["text"].split()) for s in doc["sections"])
            conflicts = sum(1 for s in doc["sections"] if s["label"] == "Contradiction")
            print(
                f"[*] {doc['doc_id']} | Typology {doc['typology_id']}: {doc['functional_typology']:<34} | "
                f"Secs: {len(doc['sections']):>2} | Operative Words: {sec_words:>4} | Planted Defects: {conflicts}"
            )

    print(f"\n[OK] Wrote 6 JSON drafts to {OUT_DIR} and consolidated benchmark to {BENCHMARK_JSONL}")


if __name__ == "__main__":
    main()
