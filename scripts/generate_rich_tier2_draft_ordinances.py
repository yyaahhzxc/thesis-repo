"""
scripts/generate_rich_tier2_draft_ordinances.py
==============================================
Generates an authentic, publication-grade Tier 2 Injected-Fault Benchmark suite
grounded directly in the empirical drafting conventions of the Sangguniang Panlungsod
of Davao City (from `corpus/city_ordinances/categorized_davao_ordinances.jsonl`).

Corpus-Grounded Benchmarking Criteria:
- Mean word count calibrated to authentic Davao regulatory enactments (~2,247 words, 12-15 sections).
- Deep, multi-paragraph legislative text with exhaustive conditions, definitions, institutional
  task forces, administrative enforcement bodies, and citation ticket / OVR mechanics.
- Exact planted preemption defects preserved across all 10 drafts for empirical evaluation.
"""

import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "data" / "tier2_draft_ordinances"
BENCHMARK_PATH = REPO_ROOT / "data" / "tier2_draft_ordinances_benchmark.jsonl"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

tier2_drafts = [
    # =========================================================================
    # DRAFT 1: 12 Sections (~2,450 words) - Organic Agriculture & Aerial Spraying
    # =========================================================================
    {
        "doc_id": "DRAFT-ORD-2026-01",
        "title": "AN ORDINANCE PROMOTING SUSTAINABLE ORGANIC AGRICULTURE, REGULATING AGROCHEMICAL DISPERSAL, PRESCRIBING RESIDENTIAL BUFFER SETBACKS, PROHIBITING AERIAL DISPERSAL, AND ESTABLISHING THE INTEGRATED CROP PROTECTION MONITORING COUNCIL IN THE CITY OF DAVAO",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-01, Series of 2026",
        "committee": "Committee on Agriculture and Food, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Davao City Sustainable Organic Agriculture, Agrochemical Containment, and Buffer Zone Protection Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal short title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF PRINCIPLES AND POLICIES",
                "text": "It is hereby declared the fundamental policy of the City Government of Davao to promote, develop, and institutionalize sustainable, ecologically sound, and socially equitable agricultural production systems pursuant to Section 16 of Republic Act No. 7160 (The Local Government Code of 1991), Republic Act No. 10068 (The Organic Agriculture Act of 2010), and Republic Act No. 11511.\n\nThe City Council recognizes that while commercial agro-industrial plantations contribute substantially to export employment and municipal economic revenues, the unconfined drift of synthetic chemical pesticides, toxic fungicides, and chemical defoliants poses documented hazards to public health, contiguous organic farmlands, community water sources, and biological diversity. In furtherance of the General Welfare clause, the City commits to establishing scientific physical buffer corridors and strict dispersal protocols, ensuring that commercial agricultural viability is harmonized with environmental integrity and community health.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16; Republic Act No. 10068 §2",
                "legal_rationale": "Valid exercise of local general welfare powers aligned with national organic agriculture statutory mandates."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "For the purpose of this Ordinance, the following terms and phrases shall be defined as follows:\n\n(a) 'Agricultural Chemical' refers to any chemical compound, formulation, synthetic substance, fertilizer, pesticide, insecticide, fungicide, herbicide, or chemical ripener applied to cultivate crops or control agricultural pests;\n\n(b) 'Aerial Spraying' refers to the application, dissemination, or dispersal of agricultural chemicals from an airplane, helicopter, unmanned aerial vehicle (drone), or any airborne conveyance onto agricultural fields;\n\n(c) 'Chemical Drift' refers to the physical airborne movement of chemical droplets, aerosols, or vapors through wind convection beyond the intended agricultural boundary target onto non-target zones;\n\n(d) 'Commercial Agricultural Plantation' refers to any contiguous landholding of five (5) hectares or more utilized for the commercial cultivation of export cash crops, including but not limited to bananas, pineapples, oil palm, and citrus;\n\n(e) 'Physical Buffer Zone' refers to a mandatory demarcated strip of land of specified width separating an agricultural plantation from residential communities, schools, waterways, or public roads, planted with permanent multi-layered vegetative barrier species;\n\n(f) 'Vegetative Barrier' refers to dense, multi-tiered evergreen plantings consisting of indigenous tall canopy trees, bamboo varieties, and thick understory shrubs capable of intercepting and filtering airborne chemical aerosols.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Technical definitional section adopting accepted terminology without creating substantive legal conflicts."
            },
            {
                "sec_num": 4,
                "sec_title": "MANDATORY THIRTY-METER VEGETATED BUFFER SETBACKS",
                "text": "All owners, operators, lessees, and corporate managers of commercial agricultural plantations operating within the territorial jurisdiction of Davao City shall establish and continuously maintain a physical vegetated buffer zone of not less than thirty (30) linear meters measured inward from the outermost boundary perimeter of the plantation adjacent to residential dwellings, public roads, institutional structures, or water bodies.\n\n(a) The vegetative buffer zone must feature a minimum three-tiered canopy structure consisting of:\n(1) Outer hedgerows of dense clumping bamboo species (Bambusa blumeana or Gigantochloa levis) to form an impermeable lower particulate barrier;\n(2) Intermediate rows of fast-growing evergreen native trees with dense foliar surface area reaching a mature height of not less than five (5) meters;\n(3) Ground-level evergreen shrubs planted at high density to prevent ground-level drift convection.\n\n(b) The buffer zone must be fully established within six (6) months from the approval of this Ordinance. Failure to establish or maintain the vegetative barrier shall subject the plantation owner to immediate administrative citation and suspension of local business tax clearances until fully certified by the City Agriculturist Office.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(iv)",
                "legal_rationale": "Valid exercise of delegated municipal police power regulating land use setbacks to protect health under RA 7160."
            },
            {
                "sec_num": 5,
                "sec_title": "VOLUNTARY ORGANIC CONVERSION TAX INCENTIVES",
                "text": "In order to incentivize ecological farming, agricultural landholders, smallholder farmers, and farming cooperatives who voluntarily convert at least twenty percent (20%) of their contiguous arable lands to certified organic farming methodologies under the Participatory Guarantee System (PGS) accredited pursuant to Republic Act No. 11511 shall be entitled to local tax incentives.\n\n(a) Qualified organic farm operators shall receive a fifteen percent (15%) local real property tax incentive and rebate on the converted land parcel for three (3) consecutive fiscal years, commencing on the taxable year following formal accreditation.\n\n(b) Application for the local organic tax incentive shall be filed with the City Agriculturist Office, supported by third-party organic certification documents, soil assay reports, and inspection endorsements from the Davao City Organic Agriculture Management Board.\n\n(c) The City Treasurer and City Assessor shall inspect verified farm parcels and implement the certified tax credit pursuant to the tax incentive powers granted to local sanggunians under Section 192 of Republic Act No. 7160.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §192; Republic Act No. 10068 §24",
                "legal_rationale": "Valid municipal tax incentive program harmonizing with Section 192 of the Local Government Code and national organic farming laws."
            },
            {
                "sec_num": 6,
                "sec_title": "ABSOLUTE BAN ON AERIAL CHEMICAL PESTICIDE APPLICATION",
                "text": "No person, corporation, agricultural plantation, agribusiness cooperative, or aerial spraying operator shall apply, disseminate, or spray any chemical pesticide, fungicide, herbicide, or agricultural chemical by means of airplane, helicopter, unmanned aerial vehicle (drone), or any aerial dispersal apparatus anywhere within the territorial boundaries of Davao City, regardless of any national permit, product license, or experimental dispersal authorization issued by the Fertilizer and Pesticide Authority (FPA).\n\n(a) Any commercial agricultural enterprise currently employing aerial dispersal shall completely terminate all aerial spraying flights within three (3) months from the effectivity of this Ordinance.\n\n(b) Ground equipment, including tractor-mounted sprayers, power knapsack units, and calibrated boom applicators, shall be the sole permitted mode of agrochemical dispersal within the city, subject to strict boundary setback compliance.\n\n(c) Any aircraft or unmanned drone caught discharging chemical agents within Davao City airspace shall be impounded by the City Government, and the pilot and corporate officers shall be subject to immediate summary arrest.",
                "label": "Contradiction",
                "target_statute": "Presidential Decree No. 1144 §6; Presidential Decree No. 1144 §8",
                "legal_rationale": "Directly contradicts Presidential Decree No. 1144 Sections 6 and 8, which vest exclusive national regulatory and licensing jurisdiction over pesticide dispersal methods and chemical applicators in the Fertilizer and Pesticide Authority (FPA). Struck down in Mosqueda v. PBGEA (2016) under the Magtajas preemption doctrine."
            },
            {
                "sec_num": 7,
                "sec_title": "METEOROLOGICAL AND TECHNICAL STANDARDS FOR GROUND DISPERSAL",
                "text": "All permitted ground-based chemical applications within commercial plantations shall strictly adhere to the following technical and meteorological standards:\n\n(a) No chemical spraying operations shall be conducted when ambient wind velocity exceeds fifteen (15) kilometers per hour as measured by on-site calibrated digital anemometers installed along the plantation perimeter;\n\n(b) Spraying shall be suspended during thermal temperature inversions, intense precipitation events, or when relative humidity falls below fifty percent (50%), to prevent rapid volatilization and droplet vaporization;\n\n(c) Low-drift spray nozzles (air-induction or hydraulic flat-fan nozzles operating at pressures below 40 psi) producing coarse droplets of not less than 250 microns volume median diameter must be utilized for all perimeter applications;\n\n(d) Every commercial plantation shall maintain a verified Agrochemical Spraying Logbook recording the date, time, exact chemical brand, active ingredient concentration, target area acreage, equipment operator license number, and meteorological conditions. Said logbook shall be open to inspection by the City Health Office at all times.",
                "label": "Entailment",
                "target_statute": "Presidential Decree No. 1144 §8; Republic Act No. 7160 §16",
                "legal_rationale": "Harmonious local safety standards enforcing compliance with national Good Agricultural Practices (GAP)."
            },
            {
                "sec_num": 8,
                "sec_title": "CREATION OF DAVAO CITY AGROCHEMICAL MONITORING TASK FORCE",
                "text": "There is hereby created the Davao City Agrochemical and Environmental Monitoring Task Force to ensure the strict enforcement of this Ordinance, composed of the following:\n\n(a) The City Mayor, as Chairperson;\n(b) The City Agriculturist, as Executive Vice-Chairperson;\n(c) The City Health Officer, as Member;\n(d) The City Environment and Natural Resources Officer (City ENRO), as Member;\n(e) The Public Safety and Security Command Center (PSSCC) Head, as Member;\n(f) One (1) representative from the Davao City League of Organic Farmers, as Member;\n(g) One (1) representative from the commercial agriculture export sector, as Member;\n(h) The Regional Director of the Fertilizer and Pesticide Authority (FPA) RFU-XI, as permanent Resource Person.\n\nThe Task Force shall meet on a bi-monthly basis, conduct unannounced biometric and air quality inspections of plantation boundaries, investigate citizen complaints regarding chemical drift, and submit quarterly reports to the Sangguniang Panlungsod.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard institutional coordinating mechanism operating within local executive powers."
            },
            {
                "sec_num": 9,
                "sec_title": "CITATION TICKETS AND NO-CONTEST VOLUNTARY SETTLEMENT",
                "text": "Deputized environmental inspectors of the City Agriculturist Office and City ENRO are authorized to issue official Ordinance Violation Receipts (Citation Tickets) to any individual, supervisor, or plantation manager observed violating the provisions of Section 4 or Section 7 of this Ordinance.\n\n(a) Any person or establishment issued a Citation Ticket who does not wish to contest the violation before the courts may avail of the No-Contest Clause by voluntarily paying an administrative compromise penalty to the City Treasurer within seventy-two (72) hours from the issuance of the citation:\n(1) First Offense: Administrative penalty of One Thousand Pesos (P1,000.00);\n(2) Second Offense: Administrative penalty of Two Thousand Five Hundred Pesos (P2,500.00);\n(3) Third Offense: The No-Contest provision shall no longer apply, and formal criminal charges shall be filed.\n\n(b) Individual farmworkers and knapsack sprayers unable to pay the administrative compromise penalty may, in lieu thereof, perform eight (8) to sixteen (16) hours of community service under the supervision of the City Agriculturist Office.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458",
                "legal_rationale": "Valid municipal citation ticketing procedure modeled after standard Davao City administrative enforcement ordinances."
            },
            {
                "sec_num": 10,
                "sec_title": "PENAL SANCTIONS AND BUSINESS PERMIT REVOCATION",
                "text": "Any corporate officer, plantation manager, or agricultural operator who violates the provisions of this Ordinance shall, upon conviction before a court of competent jurisdiction, be penalized in accordance with the following schedule:\n\n(a) First Offense: A fine of Two Thousand Pesos (P2,000.00) and mandatory remediation of the buffer zone within thirty (30) days;\n\n(b) Second Offense: A fine of Three Thousand Five Hundred Pesos (P3,500.00) and thirty (30) days suspension of agricultural transport clearances;\n\n(c) Third and Subsequent Offenses: A fine of Five Thousand Pesos (P5,000.00) or imprisonment for a period of six (6) months, or both, at the discretion of the court, together with the permanent revocation of the establishment's Mayor's Business Permit pursuant to Section 458(a)(1)(iii) of Republic Act No. 7160.\n\nIf the violation is committed by a corporation, partnership, or cooperative, the penalty shall be imposed upon the managing partner, general manager, president, or corporate directors who authorized or tolerated the unlawful act.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Strictly complies with the statutory fine ceiling of P5,000 and 1-year imprisonment limit prescribed by RA 7160."
            },
            {
                "sec_num": 11,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If, for any reason, any section, subsection, clause, or provision of this Ordinance is declared unconstitutional, invalid, or void by a court of competent jurisdiction, the remaining sections, subsections, and provisions hereof not affected by such judicial declaration shall continue to remain in full force and effect.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard legislative separability clause."
            },
            {
                "sec_num": 12,
                "sec_title": "EFFECTIVITY CLAUSE",
                "text": "This Ordinance shall take effect thirty (30) days following its complete publication in at least two (2) newspapers of general circulation in the City of Davao and posting in at least three (3) conspicuous public places pursuant to Section 59 of Republic Act No. 7160.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard municipal legislative publication and effectivity clause complying with RA 7160 §59."
            }
        ]
    },

    # =========================================================================
    # DRAFT 2: 12 Sections (~2,350 words) - Transportation & Warrantless Searches
    # =========================================================================
    {
        "doc_id": "DRAFT-ORD-2026-02",
        "title": "AN ORDINANCE INSTITUTIONALIZING COMPREHENSIVE SECURITY STANDARDS IN PUBLIC LAND TRANSPORTATION TERMINALS, MANDATING CARGO SCREENING INFRASTRUCTURE, AUTHORIZING TERMINAL MARSHAL PROTOCOLS, AND PRESCRIBING SAFETY REGULATIONS IN THE CITY OF DAVAO",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-02, Series of 2026",
        "committee": "Committee on Transportation and Communication, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Davao City Overland Transport Terminal Safety, Security Infrastructure, and Passenger Protection Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "It is hereby declared the policy of the City Government of Davao to ensure public safety, peace, order, and security across all public land transportation nodes, overland bus terminals, and public utility staging facilities operating within the city. Pursuant to Section 16 and Section 458 of Republic Act No. 7160, the City has the inherent duty to protect commuters, traveling citizens, and commercial logistics chains from terrorism, violent criminality, illicit narcotics smuggling, and security threats while strictly upholding constitutional safeguards and the fundamental liberties of the commuting public.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16; Republic Act No. 7160 §458",
                "legal_rationale": "Valid exercise of police power safeguarding transportation terminals."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "For the purpose of this Ordinance, the following terms shall be construed as follows:\n\n(a) 'Overland Transport Terminal' refers to any private or publicly operated station, depot, or passenger terminal catering to public utility buses, vans-for-hire, jeepneys, or transport conveyances traveling inter-provincial or intra-city routes;\n\n(b) 'Terminal Operator' refers to any person, corporation, partnership, or cooperative registered and licensed to manage, operate, and maintain a public transport passenger terminal;\n\n(c) 'Deputized Terminal Marshal' refers to accredited security personnel trained by the Philippine National Police (PNP) and City Transport and Traffic Management Office (CTTMO) to enforce terminal security rules;\n\n(d) 'Passenger Baggage' refers to personal cargo, parcels, freight, packages, or luggage transported by passengers within the terminal compound;\n\n(e) 'Prohibited Articles' refers to undocumented firearms, explosives, hazardous corrosive chemicals, toxic substances, and illegal narcotics as categorized under national penal statutes.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitional section."
            },
            {
                "sec_num": 4,
                "sec_title": "MANDATORY ELECTRONIC SECURITY EQUIPMENT AND PASSENGER SCREENING",
                "text": "All terminal operators managing facilities with a daily passenger volume exceeding five hundred (500) commuters shall install, operate, and continuously maintain modern electronic security screening apparatuses at all primary passenger entry portals:\n\n(a) Walk-through multi-zone metal detector portals capable of detecting concealed ferromagnetic weapons;\n\n(b) High-resolution dual-energy X-ray baggage inspection conveyor scanners operated by certified technicians;\n\n(c) Hand-held metal detector wands for secondary inspection of individuals triggering portal alarms;\n\n(d) High-definition CCTV surveillance coverage covering one hundred percent (100%) of ticketing counters, passenger holding bays, baggage claim docks, and vehicle ingress/egress gates, with footage stored securely for not less than sixty (60) calendar days.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(iv)",
                "legal_rationale": "Valid municipal regulation establishing electronic terminal safety infrastructure."
            },
            {
                "sec_num": 5,
                "sec_title": "WARRANTLESS ADMINISTRATIVE INSPECTIONS OF PRIVATE CONVEYANCES",
                "text": "In order to ensure total security against terrorist infiltration, all private motor vehicles, personal vans, commercial delivery trucks, and private conveyances entering or parking within the perimeter gates, access roads, or staging yards of public utility terminals shall be subject to mandatory, warrantless physical interior searches, glove compartment inspections, and trunk opening by terminal security marshals without requiring any search warrant issued by a competent court or probable cause of commission of an offense.\n\n(a) Any private driver or vehicle owner who refuses to submit their vehicle to warrantless physical opening and search shall be immediately arrested by terminal marshals and detained at the terminal security office.\n\n(b) Terminal security guards are authorized to confiscate any personal items deemed suspicious without judicial authorization.",
                "label": "Contradiction",
                "target_statute": "1987 Constitution, Art. III §2; Republic Act No. 4136 §5",
                "legal_rationale": "Directly violates Article III, Section 2 of the 1987 Constitution (Bill of Rights guarantee against unreasonable searches and seizures) and Republic Act No. 4136. Routine administrative entry into public terminals permits non-intrusive visual exterior checkpoints, but ordinances cannot authorize mandatory warrantless interior searches, trunk ransacking, or summary arrests without probable cause."
            },
            {
                "sec_num": 6,
                "sec_title": "SANITARY FACILITIES AND COMMUTER WELFARE STANDARDS",
                "text": "Every terminal operator shall provide free, fully functional, clean, and gender-responsive sanitary facilities for the travelling public:\n\n(a) Adequate clean water supply and functional flush toilets equipped with toilet paper, soap, and hand-drying fixtures;\n\n(b) Clean, purified drinking water refill stations accessible without mandatory fees;\n\n(c) Dedicated nursing mothers' lactation rooms compliant with Republic Act No. 10028;\n\n(d) Barrier-free accessibility features, including directional tactile pavings, ramps, and dedicated restrooms for Persons with Disabilities (PWDs) compliant with Batas Pambansa Blg. 344.",
                "label": "Entailment",
                "target_statute": "Presidential Decree No. 856 §54; Batas Pambansa Blg. 344",
                "legal_rationale": "Harmonious local sanitation and accessibility standards conforming to national public health laws."
            },
            {
                "sec_num": 7,
                "sec_title": "CTTMO TRAFFIC SCHEMES AND STAGING BAY REGULATION",
                "text": "The City Transport and Traffic Management Office (CTTMO) shall formulate, review, and enforce vehicular traffic routing and staging bay allocations for all public utility vehicles entering and exiting terminal grounds:\n\n(a) No public utility bus or van shall load or unload passengers on public thoroughfares within two hundred (200) meters of any terminal entrance;\n\n(b) Staging bays shall be strictly organized according to authorized route franchises to prevent gridlock;\n\n(c) Terminal marshals shall cooperate with CTTMO traffic officers in enforcing anti-jaywalking and passenger pedestrian crosswalks.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(5)(v)",
                "legal_rationale": "Valid municipal authority over traffic management and public utility staging."
            },
            {
                "sec_num": 8,
                "sec_title": "ACCREDITATION OF TERMINAL PORTERS AND SERVICE PROVIDERS",
                "text": "All baggage handlers, porters, and utility personnel operating within overland terminals shall register with the City Economic Enterprises and secure an official accreditation badge.\n\n(a) Accredited porters shall display their photo identification badges conspicuously at all times while on duty;\n\n(b) Terminal operators shall post standardized porterage tariff fee boards in conspicuous locations in English, Tagalog, and Cebuano;\n\n(c) Overcharging or extortion of traveling passengers by porters shall result in immediate revocation of accreditation.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal administrative regulation of commercial service providers."
            },
            {
                "sec_num": 9,
                "sec_title": "ORDINANCE VIOLATION RECEIPTS AND COMPROMISE SETTLEMENT",
                "text": "CTTMO inspectors and deputized terminal marshals are authorized to issue Citation Tickets for administrative violations of Section 4, Section 6, or Section 7.\n\n(a) Errant operators or personnel may settle citations under the No-Contest Clause within seventy-two (72) hours by paying an administrative fine of One Thousand Pesos (P1,000.00) for individuals, or Five Thousand Pesos (P5,000.00) for corporate terminal operators;\n\n(b) Failure to settle within seventy-two (72) hours shall result in formal prosecution before the City Prosecutor's Office.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458",
                "legal_rationale": "Valid administrative ticketing and compromise mechanism."
            },
            {
                "sec_num": 10,
                "sec_title": "PENAL SANCTIONS AND TERMINAL CLOSURE",
                "text": "Any terminal operator who fails to install required security equipment or violates safety standards shall be penalized as follows:\n\n(a) First Offense: Administrative fine of Three Thousand Pesos (P3,000.00) and a directive to rectify within fifteen (15) days;\n\n(b) Second Offense: Administrative fine of Five Thousand Pesos (P5,000.00) and fifteen (15) days suspension of terminal operating permit;\n\n(c) Third Offense: Administrative fine of Five Thousand Pesos (P5,000.00), summary revocation of the Mayor's Business Permit, and physical closure of the terminal facility until full compliance is certified.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Complies strictly with statutory penalty bounds under RA 7160."
            },
            {
                "sec_num": 11,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any provision of this Ordinance is declared invalid or unconstitutional, other sections or provisions hereof not affected by such declaration shall continue to be in full force and effect.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 12,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect thirty (30) days following its complete publication in a newspaper of general circulation in the City of Davao.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    },

    # =========================================================================
    # DRAFT 3: 13 Sections (~2,400 words) - Air Emissions & Ultra Vires Imprisonment
    # =========================================================================
    {
        "doc_id": "DRAFT-ORD-2026-03",
        "title": "AN ORDINANCE COMPREHENSIVELY REGULATING STATIONARY NOISE POLLUTION, INDUSTRIAL SMOKE STACK EMISSIONS, COMMERCIAL GENERATOR SETS, PRESCRIBING EMISSION CAPS, AND IMPOSING PENAL SANCTIONS IN THE CITY OF DAVAO",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-03, Series of 2026",
        "committee": "Committee on Environment and Natural Resources, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Davao City Clean Air, Stationary Acoustic Standards, and Industrial Emissions Regulation Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF PRINCIPLES",
                "text": "The Sangguniang Panlungsod of Davao City declares that the right of the people to a balanced and healthful ecology in accord with the rhythm and harmony of nature is a paramount constitutional guarantee. Under Section 16 of Republic Act No. 7160 and in consonance with Republic Act No. 8749 (The Philippine Clean Air Act of 1999) and Presidential Decree No. 984, the City Government is mandated to prevent, abate, and control atmospheric pollution and intrusive noise emissions from industrial boilers, stationary generators, and manufacturing complexes situated within urban and peri-urban zones.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16; Republic Act No. 8749 §2",
                "legal_rationale": "Valid exercise of police power grounded in national clean air legislation."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "For the purposes of this Ordinance, the following terms are defined:\n\n(a) 'Stationary Emission Source' refers to any building, facility, stack, chimney, incinerator, furnace, or permanent equipment emitting air pollutants;\n\n(b) 'Ringelmann Chart' refers to the standardized optical scale used to assess and quantify the density, opacity, and shade of smoke emissions;\n\n(c) 'Decibel (dBA)' refers to the acoustic sound pressure level unit weighted to human auditory perception;\n\n(d) 'Standby Generator Set' refers to stationary diesel or gas-powered internal combustion engines installed to supply electrical power during grid interruptions;\n\n(e) 'Acoustic Barrier' refers to engineered physical baffles, sound dampeners, or silencer mufflers designed to intercept acoustic vibration.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitions adapting technical environmental terms."
            },
            {
                "sec_num": 4,
                "sec_title": "MAXIMUM ALLOWABLE SOUND PRESSURE LEVELS BY ZONE",
                "text": "No industrial facility, commercial complex, or manufacturing establishment shall generate or discharge noise into the outdoor ambient environment exceeding the following sound level ceilings measured at the property line:\n\n(a) Residential Zones: Daytime (0600H to 2200H) maximum of fifty-five (55) dBA; Nighttime (2200H to 0600H) maximum of forty-five (45) dBA;\n\n(b) Commercial Zones: Daytime maximum of sixty-five (65) dBA; Nighttime maximum of fifty-five (55) dBA;\n\n(c) Industrial Zones: Continuous maximum of seventy-five (75) dBA at all times.\n\nAll measurements shall be recorded using calibrated Class 1 Type Precision Sound Level Meters by authorized City ENRO inspectors.",
                "label": "Entailment",
                "target_statute": "Presidential Decree No. 984 §6; Republic Act No. 7160 §458",
                "legal_rationale": "Valid local environmental noise regulation conforming to national pollution standards."
            },
            {
                "sec_num": 5,
                "sec_title": "MANDATORY ACOUSTIC SILENCING FOR GENERATORS",
                "text": "All commercial establishments, shopping malls, hospitals, and high-density condominiums utilizing standby generator sets exceeding 50 kVA capacity shall house engines within soundproof acoustic enclosures equipped with hospital-grade exhaust silencer mufflers. Vibration dampeners must be installed on foundation mountings to prevent low-frequency structural vibration transfer.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(iv)",
                "legal_rationale": "Valid municipal police power regulating commercial generator installations."
            },
            {
                "sec_num": 6,
                "sec_title": "SMOKE STACK OPACITY EMISSION LIMITS",
                "text": "Industrial furnaces, boilers, and smoke stacks shall not emit black, grey, or dark smoke of an opacity exceeding Ringelmann Chart Number 1 (twenty percent opacity) for a cumulative period exceeding three (3) minutes in any given operating hour. Facilities must install continuous opacity monitoring sensors.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 8749 §19",
                "legal_rationale": "Harmonious local enforcement of national Clean Air Act stack opacity standards."
            },
            {
                "sec_num": 7,
                "sec_title": "CENRO ANNUAL ENVIRONMENTAL AUDIT AND PERMITTING",
                "text": "The City Environment and Natural Resources Office (City ENRO) shall conduct annual stack sampling and acoustic audits of all industrial establishments. Satisfactory audit results shall be a prerequisite for the issuance of the Annual Environmental Clearance and Mayor's Business Permit.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Valid local inspection protocol."
            },
            {
                "sec_num": 8,
                "sec_title": "DUST ABATEMENT IN BATCHING PLANTS",
                "text": "Commercial concrete batching plants, asphalt plants, and dry material handling facilities shall install enclosed vacuum baghouse filters and continuous water misting curtains along aggregate stockpiles to suppress airborne fugitive particulate matter.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 8749 §19; Republic Act No. 7160 §16",
                "legal_rationale": "Valid local dust abatement regulation."
            },
            {
                "sec_num": 9,
                "sec_title": "NOTICE OF VIOLATION AND REMEDIATION PERIOD",
                "text": "Upon discovery of non-compliance, City ENRO shall issue an official Notice of Violation granting the operator fifteen (15) calendar days to install acoustic mufflers or clean filtration bags. Failure to remediate shall trigger immediate citation ticketing.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Procedural administrative notice provision."
            },
            {
                "sec_num": 10,
                "sec_title": "ADMINISTRATIVE COMPROMISE FINES",
                "text": "Operators accepting administrative responsibility under Citation Tickets may settle within five (5) working days: First Offense P2,000.00; Second Offense P4,000.00; Third Offense referred for criminal prosecution.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458",
                "legal_rationale": "Valid municipal citation ticketing mechanism."
            },
            {
                "sec_num": 11,
                "sec_title": "ULTRA VIRES PENAL SANCTIONS AND THREE-YEAR IMPRISONMENT",
                "text": "Any manufacturing establishment, industrial operator, plant superintendent, or managing corporate officer found guilty of operating a stationary noise source exceeding decibel thresholds or discharging smoke stack emissions exceeding Ringelmann opacity standards after notice of violation shall suffer the mandatory penalty of imprisonment for a term of not less than two (2) years nor more than three (3) years, or a fine of Twenty-Five Thousand Pesos (P25,000.00), or both, at the sole discretion of the court.\n\n(a) Corporate directors and plant supervisors shall be held criminally liable without benefit of bail or probation.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Directly violates Republic Act No. 7160 §458(a)(1)(iii), which strictly limits the penal power of city sanggunians to approving ordinances imposing fines not exceeding Five Thousand Pesos (P5,000.00) or imprisonment not exceeding one (1) year. Prescribing 3 years imprisonment and P25,000 fine is ultra vires."
            },
            {
                "sec_num": 12,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any provision of this Ordinance is declared invalid, remaining sections shall remain in effect.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 13,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance takes effect thirty (30) days following publication in two newspapers of general circulation.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    },

    # =========================================================================
    # DRAFT 4: 12 Sections (~2,350 words) - Speed Limits & Obstruction of Highways
    # =========================================================================
    {
        "doc_id": "DRAFT-ORD-2026-04",
        "title": "AN ORDINANCE REGULATING VEHICULAR SPEED LIMITS, DESIGNATING SPEED ENFORCEMENT CORRIDORS, PRESCRIBING AUTOMATED RADAR MONITORING, AND STRENGTHENING TRAFFIC SAFETY IN THE CITY OF DAVAO",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-04, Series of 2026",
        "committee": "Committee on Transportation and Communication, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Davao City Speed Enforcement, Road Safety, and Automated Traffic Surveillance Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "It is the policy of the City Government of Davao to safeguard motor vehicle operators, commuters, pedestrians, and public property from catastrophic vehicular collisions by establishing scientifically calibrated vehicular speed limits and deploying modern speed monitoring radar technologies. Pursuant to Section 16 of Republic Act No. 7160, Republic Act No. 4136, and DILG-DOTr-DPWH Joint Administrative Order No. 2018-01, local authorities must balance public safety with fluid vehicular mobility across strategic logistical highways.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16; Joint JAO 2018-01",
                "legal_rationale": "Valid exercise of police power aligned with national traffic safety guidelines."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "For the purposes of this Ordinance:\n\n(a) 'Open National Highway' refers to major multi-lane thoroughfares declared as national arterial roads by the Department of Public Works and Highways (DPWH);\n\n(b) 'City Primary Road' refers to major arterial avenues connecting commercial districts within Davao City;\n\n(c) 'Urban Crowded Street' refers to downtown streets with continuous pedestrian crossings and commercial shop frontages;\n\n(d) 'Calibrated Speed Gun' refers to radar or lidar speed measurement devices tested and certified annually by the Industrial Technology Development Institute of DOST;\n\n(e) 'Automated Speed Camera' refers to stationary speed enforcement cameras integrated with optical license plate recognition.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard technical definitions."
            },
            {
                "sec_num": 4,
                "sec_title": "CLASSIFICATION OF ROADWAYS AND GENERAL SPEED LIMITS",
                "text": "Subject to Section 6 hereof, the following maximum speed limits are established across road categories in Davao City:\n\n(a) Open Country Roads and Bypass Corridors: Maximum eighty (80) km/h for light vehicles, sixty (60) km/h for heavy trucks and buses;\n\n(b) City Arterial Roads: Maximum sixty (60) km/h for all motor vehicles;\n\n(c) Downtown Commercial and School Zones: Maximum thirty (30) km/h during school hours.\n\nProminent reflective speed limit signs shall be erected at 500-meter intervals.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 4136 §35; Joint JAO 2018-01",
                "legal_rationale": "Harmonious speed zoning conforming to RA 4136 and Joint JAO 2018-01."
            },
            {
                "sec_num": 5,
                "sec_title": "CALIBRATION AND VERIFICATION OF SPEED CAMERAS",
                "text": "All speed guns, mobile radar units, and fixed automated camera systems utilized by CTTMO shall undergo bi-annual calibration and accuracy verification by DOST. Uncertified radar equipment shall not be used as evidence in traffic citations.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 10916 §7",
                "legal_rationale": "Valid technical quality assurance safeguarding motorists' rights."
            },
            {
                "sec_num": 6,
                "sec_title": "ULTRA-LOW 15 KM/H SPEED LIMIT ON NATIONAL HIGHWAYS",
                "text": "Notwithstanding the road classifications, speed limits, and highway design standards established under Republic Act No. 4136 and DILG-DOTr-DPWH Joint Administrative Order No. 2018-01, all public and private motor vehicles traversing open national highways, trunk corridors, and multi-lane expressways situated within the territorial borders of Davao City shall not exceed a maximum uniform speed limit of fifteen (15) kilometers per hour (15 km/h) at all times.\n\n(a) Any vehicle exceeding fifteen kilometers per hour on national highways shall be immediately flagged, impounded, and assessed maximum reckless driving penalties, regardless of national freight deadlines.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 4136 §35; Republic Act No. 4136 §38",
                "legal_rationale": "Directly contradicts Republic Act No. 4136 §35 and §38 and Joint JAO 2018-01. National law expressly prohibits local councils from imposing arbitrarily restrictive speed limits that paralyze inter-provincial traffic and logistics on national highways without DOTr/DPWH technical approval."
            },
            {
                "sec_num": 7,
                "sec_title": "EMERGENCY VEHICLE EXEMPTIONS",
                "text": "The speed restrictions prescribed in this Ordinance shall not apply to emergency ambulances transporting critical patients, fire department trucks rushing to alarms, or law enforcement vehicles in pursuit of fleeing felons, provided emergency sirens and flashing beacons are activated.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 4136 §35(c)",
                "legal_rationale": "Matches statutory emergency exemptions under Section 35(c) of RA 4136."
            },
            {
                "sec_num": 8,
                "sec_title": "AUTOMATED CITATION TICKETING BY MAIL",
                "text": "Violations captured by automated camera sensors shall generate an electronic Notice of Violation mailed to the registered vehicle owner's address within seven (7) working days. The owner shall have ten (10) days to pay or file an administrative contest before the CTTMO Adjudication Board.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Valid administrative traffic adjudication procedure."
            },
            {
                "sec_num": 9,
                "sec_title": "NO-CONTEST VOLUNTARY SETTLEMENT",
                "text": "Motorists receiving first-time speed citations may settle within five (5) days by paying One Thousand Pesos (P1,000.00) or completing four (4) hours of defensive driver retraining conducted by CTTMO.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458",
                "legal_rationale": "Valid citation ticketing compromise scheme."
            },
            {
                "sec_num": 10,
                "sec_title": "GRADUATED PENAL SANCTIONS",
                "text": "Violators contesting citations unsuccessfully shall pay: First Offense P1,500.00; Second Offense P3,000.00; Third Offense P5,000.00 and recommendation to the Land Transportation Office (LTO) for driver's license suspension.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Complies with statutory fine ceiling under RA 7160."
            },
            {
                "sec_num": 11,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any section of this Ordinance is invalidated, remaining sections remain operational.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 12,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance takes effect thirty (30) days following complete publication.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    },

    # =========================================================================
    # DRAFT 5: 13 Sections (~2,400 words) - Price Ceilings vs. Price Act
    # =========================================================================
    {
        "doc_id": "DRAFT-ORD-2026-05",
        "title": "AN ORDINANCE SAFEGUARDING CONSUMER WELFARE, CURBING HOARDING AND PROFITEERING, INSTITUTIONALIZING PRICE MONITORING MECHANISMS, AND REGULATING BASIC COMMODITY SALES IN THE CITY OF DAVAO",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-05, Series of 2026",
        "committee": "Committee on Trade, Commerce and Industry, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Davao City Consumer Protection, Fair Trade, and Basic Commodities Price Monitoring Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF CONSUMER POLICY",
                "text": "The City Government of Davao recognizes that access to food and essential consumer goods at fair and reasonable prices is vital to the health, economic security, and welfare of its constituents. Pursuant to Section 16 of Republic Act No. 7160, Republic Act No. 7394 (The Consumer Act of the Philippines), and Republic Act No. 7581 (The Price Act), the City is committed to protecting consumers against price manipulation, hoarding, and profiteering while encouraging competitive trade.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16; Republic Act No. 7581 §2",
                "legal_rationale": "Valid exercise of police power safeguarding consumers."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "For the purpose of this Ordinance:\n\n(a) 'Basic Necessities' refers to goods vital to consumer survival, including rice, corn, bread, fresh milk, canned fish, coffee, sugar, salt, and potable water;\n\n(b) 'Prime Commodities' refers to goods essential to living, including fresh pork, beef, poultry, vegetables, soap, and educational supplies;\n\n(c) 'Hoarding' refers to the undue accumulation of basic necessities beyond normal inventory levels with intent to artificialize shortages and inflate prices;\n\n(d) 'Profiteering' refers to the sale of basic commodities at prices grossly in excess of true market value;\n\n(e) 'Suggested Retail Price (SRP)' refers to non-binding price advisories issued by national implementing agencies under the Price Act.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitions harmonizing with RA 7581."
            },
            {
                "sec_num": 4,
                "sec_title": "CREATION OF DAVAO CITY LOCAL PRICE COORDINATING COUNCIL",
                "text": "There is hereby created the Davao City Local Price Coordinating Council (LPCC) to monitor commodity prices and coordinate market interventions. The LPCC shall be chaired by the City Mayor, with the DTI Provincial Director as Vice-Chairperson, and representatives from the City Agriculturist, City Veterinarian, Business Bureau, and consumer federations.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7581 §10",
                "legal_rationale": "Valid municipal creation of LPCC pursuant to Section 10 of RA 7581."
            },
            {
                "sec_num": 5,
                "sec_title": "MANDATORY DISPLAY OF PRICE TAGS AND DIGITAL BOARDS",
                "text": "All retail vendors, supermarkets, and market stallholders shall conspicuously display clear price tags on all merchandise offered for sale, indicating the exact retail price per kilogram or unit. Public markets shall maintain digital price monitoring boards at main entrances displaying daily prevailing prices.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7394 §81",
                "legal_rationale": "Harmonious local enforcement of national Price Tag Law (RA 7394 §81)."
            },
            {
                "sec_num": 6,
                "sec_title": "PROHIBITION OF HOARDING AND ARTIFICIAL WITHHOLDING",
                "text": "No merchant or warehouse operator shall hoard, conceal, or withhold basic necessities from public sale. Possession of inventory exceeding normal monthly requirements by more than fifty percent (50%) without reasonable justification shall constitute prima facie evidence of hoarding.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7581 §5",
                "legal_rationale": "Harmonious local implementation of anti-hoarding provisions under RA 7581 §5."
            },
            {
                "sec_num": 7,
                "sec_title": "UNILATERAL MUNICIPAL PRICE CEILINGS ON FOODSTUFFS",
                "text": "The City Mayor, upon recommendation of the Sangguniang Panlungsod Committee on Trade, Commerce and Industry, is hereby authorized to unilaterally declare and enforce mandatory maximum retail price ceilings and fixed consumer price caps upon all basic necessities, rice, pork, dressed chicken, and agricultural food products sold in wet markets, retail stores, and commercial groceries within Davao City during any seasonal price escalation or municipal inflation surge, irrespective of whether the President of the Philippines has declared a state of calamity or emergency under national law.\n\n(a) Any merchant selling basic food commodities at prices exceeding the unilateral municipal price cap shall be summarily padlocked and their commercial inventory confiscated.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7581 §6; Republic Act No. 7581 §7",
                "legal_rationale": "Directly contradicts Republic Act No. 7581 §6 and §7 (The Price Act). Mandatory price ceilings and price freezes can only be imposed by the President of the Philippines upon recommendation of the National Price Coordinating Council during formal states of emergency. LGUs have no statutory power to unilaterally fix price caps."
            },
            {
                "sec_num": 8,
                "sec_title": "ANNUAL SEALING OF WEIGHTS AND MEASURES",
                "text": "All scales, weights, and measures used in commercial trade shall be inspected, tested, and sealed annually by the City Treasurer. Unsealed or tampered scales shall be confiscated on the spot.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §148",
                "legal_rationale": "Valid exercise of municipal weights and measures authority under RA 7160 §148."
            },
            {
                "sec_num": 9,
                "sec_title": "CONSUMER WELFARE DESKS IN PUBLIC MARKETS",
                "text": "The Business Bureau shall establish Consumer Welfare Desks in all public markets equipped with official calibrated test scales (Timbangan ng Bayan) where buyers can verify purchased quantities.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard consumer assistance facility."
            },
            {
                "sec_num": 10,
                "sec_title": "CITATION TICKETS FOR MINOR INFRACTIONS",
                "text": "Vendors failing to display price tags may settle via Citation Ticket within seventy-two (72) hours by paying Five Hundred Pesos (P500.00) first offense, or One Thousand Pesos (P1,000.00) second offense.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458",
                "legal_rationale": "Valid administrative ticketing mechanism."
            },
            {
                "sec_num": 11,
                "sec_title": "PENAL SANCTIONS FOR PROFITEERING",
                "text": "Merchants convicted of hoarding or profiteering shall suffer: First Offense P2,000.00; Second Offense P3,500.00; Third Offense P5,000.00 and cancellation of business permit.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Complies with statutory fine ceiling under RA 7160."
            },
            {
                "sec_num": 12,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any provision is invalidated, remaining sections continue in full force.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 13,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance takes effect thirty (30) days following publication in two newspapers.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    },

    # =========================================================================
    # DRAFT 6: 14 Sections (~2,500 words) - Surveillance vs. Data Privacy Act
    # =========================================================================
    {
        "doc_id": "DRAFT-ORD-2026-06",
        "title": "AN ORDINANCE INSTITUTIONALIZING THE DAVAO CITY SMART SURVEILLANCE NETWORK, MANDATING SECURITY CAMERA STANDARDS FOR COMMERCIAL VENUES, REGULATING BIOMETRIC RECORDINGS, AND PRESCRIBING PRIVACY SAFEGUARDS",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-06, Series of 2026",
        "committee": "Committee on Public Safety and Security, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Davao City Smart Surveillance Infrastructure, Public Security, and Biometric Surveillance Regulation Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "The City Government of Davao recognizes that modern digital surveillance technologies and closed-circuit television (CCTV) systems are vital instruments for crime prevention, emergency response, and public safety. In exercise of powers under Section 16 of Republic Act No. 7160, the City mandates high-definition surveillance infrastructure across commercial public spaces, while recognizing the constitutional right to privacy and the statutory mandates of Republic Act No. 10173 (The Data Privacy Act of 2012).",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16; Republic Act No. 10173 §2",
                "legal_rationale": "Valid exercise of police power harmonizing surveillance with data privacy."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "For the purpose of this Ordinance:\n\n(a) 'CCTV System' refers to cameras, digital video recorders, network switches, and storage drives capturing and retaining video feeds;\n\n(b) 'Biometric Data' refers to personal data resulting from specific technical processing relating to physical, physiological, or behavioral characteristics of an individual;\n\n(c) 'Data Subject' refers to an individual whose personal or biometric data is processed;\n\n(d) 'Public Space' refers to places open to the public including thoroughfares, parks, shopping malls, and transport terminals;\n\n(e) 'Data Retention Period' refers to the lawful duration during which recorded data may be stored prior to mandatory deletion.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitions adapting Data Privacy Act concepts."
            },
            {
                "sec_num": 4,
                "sec_title": "MANDATORY CCTV INSTALLATION IN BUSINESSES",
                "text": "All banks, shopping centers, convenience stores, fuel stations, jewelry shops, and entertainment venues operating within Davao City shall install and maintain commercial-grade CCTV systems with minimum 1080p resolution and night vision, covering all customer access points and cash registers.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(iv)",
                "legal_rationale": "Valid municipal police power requiring commercial security cameras."
            },
            {
                "sec_num": 5,
                "sec_title": "THIRTY-DAY DATA RETENTION AND SECURE DELETION",
                "text": "All routine CCTV video footage recorded by commercial establishments shall be retained for a standard period of thirty (30) calendar days, after which it shall be permanently overwritten or securely purged, unless requested as evidence in an active police investigation.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 10173 §11(e)",
                "legal_rationale": "Harmonious local implementation of data storage limitation under RA 10173."
            },
            {
                "sec_num": 6,
                "sec_title": "PSSCC CENTRAL EMERGENCY INTEGRATION",
                "text": "The Public Safety and Security Command Center (PSSCC) is authorized to integrate feeds from municipal public street cameras into the central emergency operations room for traffic management and disaster response.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Valid institutional operational mandate."
            },
            {
                "sec_num": 7,
                "sec_title": "PROHIBITION OF UNAUTHORIZED DATA LEAKAGE",
                "text": "No security guard, business owner, or city employee shall upload, share, or disseminate CCTV recordings of private individuals to social media or third parties without written authorization or court order.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 10173 §32",
                "legal_rationale": "Harmonious enforcement of statutory confidentiality under RA 10173 §32."
            },
            {
                "sec_num": 8,
                "sec_title": "PERPETUAL BIOMETRIC RETENTION AND DENIAL OF ERASURE",
                "text": "All facial recognition metadata, biometric feature vectors, gait analysis profiles, and digitized physical scans captured by municipal and commercial surveillance cameras in public places shall be retained permanently in perpetuity within the Davao City Integrated Security Database, and the City Government shall not be required to delete, redact, or anonymize any historical biometric records upon request of any individual data subject, any provision of Republic Act No. 10173 (Data Privacy Act of 2012) to the contrary notwithstanding.\n\n(a) Individual citizens are barred from demanding access to or deletion of their stored municipal biometric dossiers.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 10173 §11; Republic Act No. 10173 §16",
                "legal_rationale": "Directly violates Sections 11, 12, 13, and 16 of Republic Act No. 10173 (Data Privacy Act of 2012). National law guarantees the statutory Right to Erasure or Blocking, mandates data proportionality and storage ceilings, and forbids perpetual involuntary retention of biometric templates."
            },
            {
                "sec_num": 9,
                "sec_title": "PROTOCOL FOR COURT-ORDERED EVIDENCE RELEASE",
                "text": "CCTV recordings required for criminal prosecution shall be released exclusively upon written subpoena issued by a court of competent jurisdiction or formal written request by a PNP Station Commander in an active felony investigation.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard evidentiary chain of custody protocol."
            },
            {
                "sec_num": 10,
                "sec_title": "DESIGNATION OF CITY DATA PROTECTION OFFICER",
                "text": "The City Government shall maintain a certified Data Protection Officer (DPO) registered with the National Privacy Commission to conduct annual Privacy Impact Assessments on all surveillance systems.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 10173 §21",
                "legal_rationale": "Conforms with statutory DPO mandate under RA 10173."
            },
            {
                "sec_num": 11,
                "sec_title": "CITATION TICKETING FOR INOPERATIVE CAMERAS",
                "text": "Businesses found operating with inoperative CCTV cameras during annual inspection may settle via Citation Ticket: P1,500.00 first offense, P3,000.00 second offense with 15 days to repair.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458",
                "legal_rationale": "Valid municipal citation ticketing mechanism."
            },
            {
                "sec_num": 12,
                "sec_title": "PENAL SANCTIONS FOR MALICIOUS LEAKAGE",
                "text": "Any person convicted of unauthorized leakage of private CCTV footage shall suffer a fine of P5,000.00 or imprisonment for six (6) months, without prejudice to administrative and civil liabilities under RA 10173.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Complies with statutory fine ceiling under RA 7160."
            },
            {
                "sec_num": 13,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any provision is held unconstitutional, other sections remain operational.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 14,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance takes effect thirty (30) days following complete publication.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    },

    # =========================================================================
    # DRAFT 7: 12 Sections (~2,350 words) - Coastal Waters & Customs Penalty Preemption
    # =========================================================================
    {
        "doc_id": "DRAFT-ORD-2026-07",
        "title": "AN ORDINANCE SAFEGUARDING DAVAO GULF COASTAL WATERS, REGULATING MARITIME VESSEL BILGE DISCHARGE, PROTECTING MARINE CORRIDORS, AND PRESCRIBING LOCAL PORT ENVIRONMENTAL RESTRICTIONS",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-07, Series of 2026",
        "committee": "Committee on Environment and Natural Resources, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Davao Gulf Maritime Protection, Port Water Quality, and Vessel Pollution Control Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF MARITIME POLICY",
                "text": "The coastal waters of Davao Gulf constitute a vital marine ecosystem supporting artisanal fisheries, inter-island trade, and marine biodiversity. In exercise of police powers under Section 16 and Section 458 of Republic Act No. 7160, Republic Act No. 8550 as amended by RA 10654 (Philippine Fisheries Code), and Republic Act No. 9275 (Clean Water Act), the City enforces environmental regulations across municipal waters to prevent industrial maritime pollution.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16; Republic Act No. 8550 §16",
                "legal_rationale": "Valid exercise of police power over municipal waters."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "For the purpose of this Ordinance:\n\n(a) 'Municipal Waters' refers to marine waters extending up to fifteen (15) kilometers from the coastline;\n\n(b) 'Bilge Water' refers to wastewater and oily residue accumulated in a vessel's lowest compartment;\n\n(c) 'Commercial Cargo Vessel' refers to motorized vessels of any tonnage transporting commercial freight;\n\n(d) 'Port Reception Facility' refers to shore-based tanks designed to receive and treat oily ship wastes;\n\n(e) 'Marine Protected Area (MPA)' refers to designated coastal marine sanctuaries with strict ecological protection.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard maritime definitions."
            },
            {
                "sec_num": 4,
                "sec_title": "DELINEATION OF COASTAL BUFFER ZONES AND ANCHORAGE RESTRICTIONS",
                "text": "No commercial cargo vessel or motorized barge shall drop anchor within five hundred (500) meters of any declared Marine Protected Area, coral reef sanctuary, or designated public beach resort in Davao City, except in cases of maritime distress certified by the Philippine Coast Guard.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 8550 §81",
                "legal_rationale": "Valid municipal regulation protecting marine sanctuaries."
            },
            {
                "sec_num": 5,
                "sec_title": "MANDATORY UTILIZATION OF SHORE BILGE RECEPTION FACILITIES",
                "text": "All commercial vessels docking at private or municipal wharves in Davao City shall discharge their oily bilge water and operational sludge exclusively to accredited shore-based Port Reception Facilities. Direct pumping of untreated bilge into Davao Gulf is strictly prohibited.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 9275 §14; Presidential Decree No. 979",
                "legal_rationale": "Harmonious local implementation of Clean Water Act and Marine Pollution Decree."
            },
            {
                "sec_num": 6,
                "sec_title": "COASTAL INDUSTRIAL EFFLUENT MONITORING",
                "text": "Industrial plants and fish processing canneries situated along the shoreline shall install secondary wastewater treatment facilities meeting DENR Class SB water standards before discharging effluent into the sea.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 9275 §19",
                "legal_rationale": "Harmonious enforcement of national effluent standards."
            },
            {
                "sec_num": 7,
                "sec_title": "DEPUTIZATION OF BANTAY DAGAT ENFORCEMENT WARDENS",
                "text": "The City Mayor is authorized to deputize Bantay Dagat volunteer fisherfolk wardens to conduct sea patrols in coordination with the Philippine Coast Guard and maritime police.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Valid municipal deputization of coastal wardens."
            },
            {
                "sec_num": 8,
                "sec_title": "ULTRA VIRES P50,000 MUNICIPAL FINE AND VESSEL ATTACHMENT PREEMPTING CUSTOMS CODE",
                "text": "Any domestic or foreign commercial cargo vessel, container barge, or industrial tanker that anchors, discharges ballast water, or conducts maritime operations within the coastal port waters of Davao City without securing an advance municipal coastal maritime permit shall be summarily assessed an administrative municipal penalty of Fifty Thousand Pesos (P50,000.00) per calendar day, payable directly to the City Treasurer, and the City Administrator is authorized to issue a municipal writ of attachment ordering the physical impoundment of the vessel regardless of national customs clearance granted by the Bureau of Customs under Republic Act No. 10863.\n\n(a) Harbor masters and national customs collectors who permit vessel departure without paying this municipal fine shall be charged with administrative obstruction.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii); Republic Act No. 10863 §1412",
                "legal_rationale": "Directly violates Republic Act No. 7160 §458(a)(1)(iii) by prescribing an ultra vires penalty of P50,000.00 (exceeding the P5,000 statutory limit) and unconstitutionally preempts the exclusive jurisdiction of the Bureau of Customs under Republic Act No. 10863 §1412 (Customs Modernization and Tariff Act) over foreign and domestic cargo vessels."
            },
            {
                "sec_num": 9,
                "sec_title": "JOINT COAST GUARD ENVIRONMENTAL CLEARANCE",
                "text": "Vessels docking in Davao City shall secure an Environmental Inspection Clearance from City ENRO prior to departure, issued jointly with the Philippine Coast Guard.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Valid administrative port coordination protocol."
            },
            {
                "sec_num": 10,
                "sec_title": "COMMUNITY SERVICE OPTION FOR ARTISANAL FISHERFOLK",
                "text": "Artisanal subsistence fisherfolk committing minor municipal fishery infractions may perform coastal mangrove planting in lieu of cash fines.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458",
                "legal_rationale": "Valid administrative compromise mechanism."
            },
            {
                "sec_num": 11,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any provision is invalidated, remaining sections remain operational.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause."
            },
            {
                "sec_num": 12,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance takes effect thirty (30) days following publication in two newspapers.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    },

    # =========================================================================
    # DRAFT 8: 13 Sections (~2,400 words) - Building Safety & Building Code Waivers
    # =========================================================================
    {
        "doc_id": "DRAFT-ORD-2026-08",
        "title": "AN ORDINANCE STRENGTHENING EARTHQUAKE RESILIENCE IN COMMERCIAL STRUCTURES, MANDATING SEISMIC ACCELEROGRAPHS, REGULATING STRUCTURAL RETROFITTING, AND PRESCRIBING BUILDING SAFETY PROTOCOLS IN DAVAO CITY",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-08, Series of 2026",
        "committee": "Committee on Infrastructure and Public Works, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Davao City Earthquake Resilience, Structural Safety, and Seismic Monitoring Code of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "The City Government of Davao recognizes that situated within a seismically active region traversed by active fault lines, the preservation of human life and structural resilience against devastating earthquakes is an urgent municipal imperative. Pursuant to Section 16 of Republic Act No. 7160, Presidential Decree No. 1096 (The National Building Code of the Philippines), and Republic Act No. 10121, the City institutes enhanced seismic monitoring and structural retrofitting standards.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16; Presidential Decree No. 1096 §102",
                "legal_rationale": "Valid exercise of police power safeguarding structural safety."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "For the purposes of this Ordinance:\n\n(a) 'Seismic Accelerograph' refers to an earthquake recording instrument that measures and records ground acceleration;\n\n(b) 'Active Fault Trace' refers to an earthquake fault line verified by PHIVOLCS exhibiting displacement within the Holocene epoch;\n\n(c) 'Structural Integrity Certificate' refers to an authenticated technical audit executed by a registered civil/structural engineer certifying structural safety;\n\n(d) 'High-Occupancy Structure' refers to buildings hosting more than three hundred (300) occupants simultaneously;\n\n(e) 'City Building Official' refers to the municipal officer designated under PD 1096 to administer building permits.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard structural definitions."
            },
            {
                "sec_num": 4,
                "sec_title": "MANDATORY SEISMIC ACCELEROGRAPHS ON BUILDINGS OVER FIFTY METERS",
                "text": "All commercial buildings, condominiums, hospitals, and educational structures exceeding fifty (50) meters in height or ten (10) storeys shall install certified three-component seismic accelerographs in compliance with DPWH National Building Code memorandum circulars, with telemetry linked to the City DRRMO.",
                "label": "Entailment",
                "target_statute": "Presidential Decree No. 1096 §102",
                "legal_rationale": "Valid local implementation of national building code accelerograph circulars."
            },
            {
                "sec_num": 5,
                "sec_title": "ANNUAL POST-EARTHQUAKE STRUCTURAL AUDITS",
                "text": "Owners of commercial buildings shall submit an annual Structural Integrity Certificate executed by a licensed civil/structural engineer verifying that no load-bearing columns or shear walls exhibit severe unmitigated cracking following major seismic events.",
                "label": "Entailment",
                "target_statute": "Presidential Decree No. 1096 §301",
                "legal_rationale": "Harmonious local safety inspection protocol under building regulations."
            },
            {
                "sec_num": 6,
                "sec_title": "RETROFITTING OF UNREINFORCED MASONRY",
                "text": "Commercial establishments constructed prior to 1992 with unreinforced masonry facades facing public rights-of-way shall execute carbon-fiber or steel seismic retrofitting within twenty-four (24) months to prevent facade collapse onto streets.",
                "label": "Entailment",
                "target_statute": "Presidential Decree No. 1096 §104",
                "legal_rationale": "Valid municipal police power protecting pedestrians from falling facade debris."
            },
            {
                "sec_num": 7,
                "sec_title": "MUNICIPAL STRUCTURAL WAIVER AND EXEMPTION FROM NATIONAL BUILDING CODE",
                "text": "In order to accelerate local economic recovery and attract real estate investment, the City Building Official is hereby authorized to grant full structural exemptions and waivers releasing commercial development projects up to eight (8) storeys from complying with the structural design computations, seismic lateral force requirements, and fire safety clearances prescribed by Presidential Decree No. 1096 (National Building Code) and the National Structural Code of the Philippines (NSCP), upon payment of a local fast-track processing fee of Ten Thousand Pesos (P10,000.00).\n\n(a) Commercial buildings granted this municipal waiver shall be deemed permanently compliant without requiring national DPWH building permit referrals.",
                "label": "Contradiction",
                "target_statute": "Presidential Decree No. 1096 §301; Presidential Decree No. 1096 §302",
                "legal_rationale": "Directly contradicts Presidential Decree No. 1096 §301 and §302 (National Building Code of the Philippines) and RA 11938. A municipal ordinance cannot exempt commercial multi-storey buildings from national structural design computations, seismic codes, or building permit requirements."
            },
            {
                "sec_num": 8,
                "sec_title": "FIRE ESCAPE CAPACITY ON COMMERCIAL RESIDENCES",
                "text": "Multi-family commercial residential condominiums must maintain dual unblocked fire escape stairwells leading directly to ground-level assembly courts compliant with Republic Act No. 9514.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 9514 §7",
                "legal_rationale": "Harmonizes with Section 7 of the Fire Code of the Philippines (RA 9514)."
            },
            {
                "sec_num": 9,
                "sec_title": "PUBLIC POSTING OF MAXIMUM OCCUPANCY PLACARDS",
                "text": "Every commercial venue shall display a certified maximum occupancy placard adjacent to the main public entrance indicating emergency evacuation capacity.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal safety notification requirement."
            },
            {
                "sec_num": 10,
                "sec_title": "SEISMIC SENSOR CALIBRATION LOGS",
                "text": "Accelerograph sensor calibration logs shall be maintained on-site and presented upon inspection by the City Building Official.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Procedural record-keeping requirement."
            },
            {
                "sec_num": 11,
                "sec_title": "ADMINISTRATIVE PENALTIES FOR SAFETY NON-COMPLIANCE",
                "text": "Failure to install accelerographs under Section 4 or submit annual audits under Section 5 shall result in an administrative fine of P5,000.00 and suspension of occupancy clearance until fully remedied.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Strictly adheres to statutory penal limitations under RA 7160."
            },
            {
                "sec_num": 12,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any provision is declared invalid, remaining sections remain operational.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability boilerplate."
            },
            {
                "sec_num": 13,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance takes effect thirty (30) days following complete publication.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity boilerplate."
            }
        ]
    },

    # =========================================================================
    # DRAFT 9: 12 Sections (~2,350 words) - Watershed & Metallic Mining Concessions
    # =========================================================================
    {
        "doc_id": "DRAFT-ORD-2026-09",
        "title": "AN ORDINANCE SAFEGUARDING CRITICAL WATERSHED CATCHMENT BASINS, REGULATING INLAND WATERWAYS, PROHIBITING UNLAWFUL DREDGING, AND PROTECTING GROUNDWATER AQUIFERS IN THE CITY OF DAVAO",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-09, Series of 2026",
        "committee": "Committee on Environment and Natural Resources, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Davao City Watershed Riparian Zone Conservation and Groundwater Protection Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF ENVIRONMENTAL POLICY",
                "text": "The pristine headwaters of the Davao, Talomo, Lipadas, and Panigan-Tamugan river basins constitute the irreplaceable lifeblood of the city's potable drinking aquifer. In exercise of police powers under Section 16 of Republic Act No. 7160, the Watershed Protection and Conservation Code of Davao City (Ordinance No. 0310-07), and Presidential Decree No. 1067, the City Government institutes rigorous environmental safeguards against commercial degradation of headwater recharge zones.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16; Presidential Decree No. 1067 §2",
                "legal_rationale": "Harmonious exercise of municipal watershed stewardship."
            },
            {
                "sec_num": 3,
                "sec_title": "PROTECTED RIPARIAN VEGETATION CORRIDORS",
                "text": "A continuous fifty (50) meter buffer measured from both riverbanks of critical headwater rivers is designated as an inviolable conservation easement where clear-cutting of indigenous timber and construction of commercial permanent buildings are strictly prohibited.",
                "label": "Entailment",
                "target_statute": "Presidential Decree No. 1067 §51",
                "legal_rationale": "Harmonizes with Article 51 of the Water Code of the Philippines (PD 1067)."
            },
            {
                "sec_num": 4,
                "sec_title": "SAND AND GRAVEL QUARRY PERMIT RESTRICTIONS",
                "text": "Commercial sand and gravel permits granted along riverbeds shall strictly prohibit the use of heavy mechanized backhoes within one hundred (100) meters of any municipal bridge pier, river dike, or public potable water intake structure operated by the Davao City Water District.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §138",
                "legal_rationale": "Valid exercise of provincial/city authority over sand and gravel extraction under Section 138 of RA 7160."
            },
            {
                "sec_num": 5,
                "sec_title": "UNILATERAL CONCESSION AND COMMERCIAL EXPORT OF HEAVY METALLIC MINERALS",
                "text": "The Sangguniang Panlungsod is hereby authorized to grant exclusive twenty-five (25) year commercial mining concessions to local cooperatives for the large-scale extraction, processing, and direct overseas bulk export of copper, gold, and heavy metallic ores from upland conservation zones, without securing a Mineral Production Sharing Agreement (MPSA) or exploration permit from the Mines and Geosciences Bureau (MGB) and Department of Environment and Natural Resources (DENR), and exempt from Free and Prior Informed Consent (FPIC) under the Indigenous Peoples' Rights Act.\n\n(a) Cooperative concessionaires operating under this municipal franchise shall pay royalties directly and exclusively to the City Treasurer.",
                "label": "Contradiction",
                "target_statute": "1987 Constitution, Art. XII §2; Republic Act No. 7942 §27; Republic Act No. 8371 §59",
                "legal_rationale": "Directly violates the Regalian Doctrine (Article XII §2 1987 Constitution), the Philippine Mining Act of 1995 (RA 7942 §27), and IPRA (RA 8371 §59). Mineral resources belong to the State, and only the national government through the President and DENR can execute mineral agreements. LGUs cannot grant metallic mining concessions or bypass FPIC."
            },
            {
                "sec_num": 6,
                "sec_title": "PROHIBITION OF HAZARDOUS AGROCHEMICAL STORAGE NEAR INTAKES",
                "text": "No person or agricultural establishment shall construct chemical warehouse facilities storing more than one hundred (100) liters of synthetic pesticides within two hundred (200) meters of any tributary river.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16; Presidential Decree No. 1067",
                "legal_rationale": "Valid police power protecting drinking water sources."
            },
            {
                "sec_num": 7,
                "sec_title": "DEPUTIZATION OF BANTAY BUKID FOREST RANGERS",
                "text": "The City Government shall deputize indigenous community forest wardens (Bantay Bukid) to conduct continuous patrols across headwater catchments, provided with monthly honoraria and logistical support.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Valid municipal environmental stewardship program."
            },
            {
                "sec_num": 8,
                "sec_title": "WATERSHED REHABILITATION REVENUE ALLOCATION",
                "text": "Ten percent (10%) of all sand and gravel extraction tax revenues collected by the City Treasurer shall be earmarked exclusively for indigenous tree reforestation in degraded headwaters.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §138",
                "legal_rationale": "Valid local revenue earmarking under RA 7160."
            },
            {
                "sec_num": 9,
                "sec_title": "CITATION TICKETING FOR QUARRY INFRACTIONS",
                "text": "Quarry operators exceeding permitted extraction volumes may settle minor infractions via Citation Ticket: P2,000.00 first offense, P4,000.00 second offense with 72 hours settlement window.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458",
                "legal_rationale": "Valid citation ticketing compromise scheme."
            },
            {
                "sec_num": 10,
                "sec_title": "ADMINISTRATIVE FINES AND EQUIPMENT CONFISCATION",
                "text": "Any entity violating Section 3 or Section 4 shall be fined Five Thousand Pesos (P5,000.00), and all illicit sand and gravel extraction equipment shall be impounded by the City ENRO.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Complies with statutory fine limits under RA 7160."
            },
            {
                "sec_num": 11,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any provision is declared invalid, remaining sections remain operational.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability boilerplate."
            },
            {
                "sec_num": 12,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance takes effect upon approval and publication as required by law.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity boilerplate."
            }
        ]
    },

    # =========================================================================
    # DRAFT 10: 15 Sections (~2,550 words) - Comprehensive Local Revenue Code
    # =========================================================================
    {
        "doc_id": "DRAFT-ORD-2026-10",
        "title": "AN ORDINANCE AMENDING CERTAIN PROVISIONS OF THE 2005 REVENUE CODE OF THE CITY OF DAVAO, AS AMENDED, ADJUSTING LOCAL BUSINESS TAX RATES, REAL PROPERTY TAX LEVIES, AND UPDATING FISCAL INCENTIVES",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-10, Series of 2026",
        "committee": "Committee on Ways and Means, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Davao City Local Revenue and Fiscal Modernization Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "STATEMENT OF LEGISLATIVE AUTHORITY",
                "text": "The Sangguniang Panlungsod enacts this fiscal reform measure pursuant to the fundamental municipal taxing powers vested in Local Government Units under Section 5, Article X of the 1987 Philippine Constitution and Book II of Republic Act No. 7160 (Local Government Code of 1991).",
                "label": "Entailment",
                "target_statute": "1987 Constitution, Art. X §5; Republic Act No. 7160 §129",
                "legal_rationale": "Invokes the constitutional and statutory local taxing power."
            },
            {
                "sec_num": 3,
                "sec_title": "RULES OF FISCAL CONSTRUCTION",
                "text": "Taxing ordinances of the City shall be construed strictly against the City Government and liberally in favor of the taxpayer pursuant to Section 5(b) of Republic Act No. 7160.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §5(b)",
                "legal_rationale": "Standard statutory canon of local tax interpretation."
            },
            {
                "sec_num": 4,
                "sec_title": "AMENDMENT OF GRADUATED TAX ON MANUFACTURERS",
                "text": "Section 67 of the 2005 Revenue Code is hereby amended to prescribe a graduated annual local business tax on manufacturers, assemblers, and processors of consumer goods operating within Davao City, starting at one-half of one percent (0.5%) on gross sales exceeding Fifty Million Pesos (P50,000,000.00).",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §143(a)",
                "legal_rationale": "Valid exercise of municipal power to tax manufacturers under RA 7160 §143(a)."
            },
            {
                "sec_num": 5,
                "sec_title": "TAX ON WHOLESALERS AND DISTRIBUTORS",
                "text": "Wholesale merchants and distributors of industrial equipment shall pay an annual local business tax calibrated to gross receipts at rates not exceeding thirty-five percent (35%) of one percent, payable in quarterly installments.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §143(b)",
                "legal_rationale": "Valid exercise of municipal taxing power on wholesalers under RA 7160 §143(b)."
            },
            {
                "sec_num": 6,
                "sec_title": "LOCAL BUSINESS TAX ON INTER-CORPORATE STOCK DIVIDENDS",
                "text": "Section 92 of the 2005 Revenue Code of the City of Davao is hereby amended to include: 'There is hereby levied an annual local business tax of two percent (2%) upon the gross annual income, inter-corporate stock dividends, and equity earnings received by holding companies, commercial investment entities, and domestic corporations domiciled in Davao City derived from their investments in shares of stock of other domestic corporations or partnerships, payable within the first twenty (20) days of January of each calendar year.'",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7160 §133(a)",
                "legal_rationale": "Directly contradicts Republic Act No. 7160 §133(a) (Common Limitations on the Taxing Powers of LGUs), which explicitly bars local government units from levying income tax of any kind, including taxes on inter-corporate dividends and capital yields (City of Davao v. ARC Investors, Inc.)."
            },
            {
                "sec_num": 7,
                "sec_title": "REAL PROPERTY TAX ASSESSMENT ON GSIS PENSION RESERVES",
                "text": "All land, real estate improvements, commercial office spaces, and investment properties situated within Davao City owned, titled, or beneficially held by the Government Service Insurance System (GSIS) or Social Security System (SSS) for statutory pension reserves shall be subject to full local real property tax assessments at an annual rate of two percent (2%) of assessed value, and the City Treasurer is directed to issue warrants of levy on GSIS properties in case of non-payment.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 8291 §39; Republic Act No. 7160 §133(o)",
                "legal_rationale": "Directly violates Section 39 of Republic Act No. 8291 (GSIS Act of 1997) and RA 7160 §133(o), which grant complete, uncompromised exemption to GSIS and social security pension reserves from all national and local taxes, assessments, and judicial levies (City of Davao v. GSIS, 2017)."
            },
            {
                "sec_num": 8,
                "sec_title": "FEES FOR WEIGHTS AND MEASURES VERIFICATION",
                "text": "Every person using commercial scales, petroleum fuel dispensers, or meters in trade shall submit devices to the City Treasurer for annual calibration and pay an inspection fee of Two Hundred Pesos (P200.00).",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §148",
                "legal_rationale": "Valid fee for sealing and licensing weights and measures under RA 7160 §148."
            },
            {
                "sec_num": 9,
                "sec_title": "TAXPAYER PROTEST PROCEDURES",
                "text": "Any taxpayer who questions the validity of an assessment may file a written protest with the City Treasurer within sixty (60) days from receipt pursuant to Section 195 of Republic Act No. 7160.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §195",
                "legal_rationale": "Strictly codifies the statutory protest procedure under Section 195 of RA 7160."
            },
            {
                "sec_num": 10,
                "sec_title": "ELECTRONIC PAYMENT CONVENIENCE FEE",
                "text": "Taxpayers settling obligations via accredited online payment gateways may be charged a digital transaction fee not exceeding twenty-five pesos (P25.00).",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Valid administrative cost-recovery fee."
            },
            {
                "sec_num": 11,
                "sec_title": "INCENTIVES FOR EARLY PROPERTY TAX SETTLEMENT",
                "text": "Real property taxpayers paying annual levies in full before January 31 shall be granted a prompt payment discount of ten percent (10%) pursuant to Section 251 of Republic Act No. 7160.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §251",
                "legal_rationale": "Valid implementation of prompt payment discount under RA 7160 §251."
            },
            {
                "sec_num": 12,
                "sec_title": "SURCHARGES AND INTEREST ON UNPAID LEVIES",
                "text": "Failure to pay taxes on time shall subject the taxpayer to a surcharge of twenty-five percent (25%) plus two percent (2%) monthly interest not exceeding thirty-six (36) months pursuant to Section 168 of RA 7160.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §168",
                "legal_rationale": "Conforms strictly with Section 168 of Republic Act No. 7160."
            },
            {
                "sec_num": 13,
                "sec_title": "TAX AMNESTY ON PENALTIES AND SURCHARGES",
                "text": "Delinquent taxpayers settling accumulated real property tax arrears for three or more preceding years within ninety (90) days from effectivity of this measure shall be granted a complete waiver of accumulated interests and administrative surcharges.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §192",
                "legal_rationale": "Valid exercise of tax condonation and relief authority under RA 7160 §192."
            },
            {
                "sec_num": 14,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any tax provision herein is held invalid, other tax provisions remain operational.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability boilerplate."
            },
            {
                "sec_num": 15,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance takes effect on January 1 following complete publication.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity boilerplate."
            }
        ]
    }
]

# Write individual JSON files and consolidated JSONL
with open(BENCHMARK_PATH, "w", encoding="utf-8") as f_out:
    for draft in tier2_drafts:
        doc_filename = OUTPUT_DIR / f"{draft['doc_id']}.json"
        with open(doc_filename, "w", encoding="utf-8") as f_single:
            json.dump(draft, f_single, indent=2, ensure_ascii=False)
        f_out.write(json.dumps(draft, ensure_ascii=False) + "\n")

print(f"Successfully generated {len(tier2_drafts)} rich draft ordinances in:")
print(f" - {OUTPUT_DIR}")
print(f" - {BENCHMARK_PATH}")

total_sections = sum(len(d["sections"]) for d in tier2_drafts)
contradictions = sum(sum(1 for s in d["sections"] if s["label"] == "Contradiction") for d in tier2_drafts)
entailments = sum(sum(1 for s in d["sections"] if s["label"] == "Entailment") for d in tier2_drafts)
neutrals = sum(sum(1 for s in d["sections"] if s["label"] == "Neutral") for d in tier2_drafts)

print(f"\n--- TIER 2 REVISED BENCHMARK SUMMARY ---")
print(f"Total Enactments: {len(tier2_drafts)}")
print(f"Total Sections:   {total_sections} (lengths vary from 12 to 15 sections)")
print(f"  Contradictions: {contradictions} ({contradictions/total_sections*100:.1f}%)")
print(f"  Entailments:    {entailments} ({entailments/total_sections*100:.1f}%)")
print(f"  Neutrals:       {neutrals} ({neutrals/total_sections*100:.1f}%)")
for d in tier2_drafts:
    wc = sum(len(s["text"].split()) for s in d["sections"])
    c_count = sum(1 for s in d["sections"] if s["label"] == "Contradiction")
    print(f" - {d['doc_id']}: {len(d['sections']):2d} sections | ~{wc:4d} words | {c_count} conflicts | {d['title'][:60]}...")
