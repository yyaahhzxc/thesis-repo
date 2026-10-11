"""
scripts/build_full_length_tier2_drafts.py
=========================================
Generates 10 full-length, highly authentic synthetic draft ordinances modeled
directly after the empirical depth, vocabulary, and paragraph structure of
substantive regulatory ordinances in Davao City Sangguniang Panlungsod archives.

Each draft features:
- Word count: 1,800 to 3,200 words (matching authentic corpus distribution: mean 2,247 words)
- Sections: 12 to 16 exhaustive sections
- Multi-paragraph substantive provisions with subsections (a), (b), (c), sub-items (1), (2), (3)
- Realistic institutional bodies: CTTMO, CENRO, CAO, CHO, PSSCC, Business Bureau, City Treasurer
- Authentic enforcement mechanisms: Ordinance Violation Receipts (Citation Tickets),
  No-Contest voluntary settlement within 72 hours, community service options
- Exact planted preemption conflicts rigorously maintained for empirical benchmark evaluation
"""

import json
from pathlib import Path

REPO_ROOT = Path(".").resolve()
OUTPUT_DIR = REPO_ROOT / "data" / "tier2_draft_ordinances"
BENCHMARK_PATH = REPO_ROOT / "data" / "tier2_draft_ordinances_benchmark.jsonl"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# We will build all 10 draft objects with authentic multi-paragraph depth.

def get_draft_01():
    return {
        "doc_id": "DRAFT-ORD-2026-01",
        "title": "AN ORDINANCE PROMOTING SUSTAINABLE ORGANIC AGRICULTURE, REGULATING AGROCHEMICAL DISPERSAL, PRESCRIBING RESIDENTIAL BUFFER SETBACKS, PROHIBITING AERIAL DISPERSAL, AND ESTABLISHING THE INTEGRATED CROP PROTECTION MONITORING COUNCIL IN THE CITY OF DAVAO",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-01, Series of 2026",
        "committee": "Committee on Agriculture and Food, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Davao City Sustainable Organic Agriculture, Agrochemical Drift Containment, and Agricultural Buffer Zone Regulation Ordinance of 2026'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal short title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF PRINCIPLES AND POLICIES",
                "text": "It is hereby declared the fundamental policy of the City Government of Davao to promote, institutionalize, and expand ecologically sustainable, socially equitable, and economically viable agricultural systems across all agricultural districts of the city, pursuant to the General Welfare clause under Section 16 of Republic Act No. 7160 (The Local Government Code of 1991), Republic Act No. 10068 (The Organic Agriculture Act of 2010), and Republic Act No. 11511.\n\nThe Sangguniang Panlungsod recognizes that while commercial export plantations contribute significantly to rural employment, agribusiness investments, and municipal tax revenues, the unmitigated drift and atmospheric dispersion of synthetic agricultural chemicals, toxic fungicides, and chemical ripener formulations pose acute and chronic health hazards to nearby residents, farm laborers, primary school children, rural water catchment systems, and organic farming enterprises.\n\nIn furtherance of constitutional guarantees securing a balanced and healthful ecology and public health, the City Government establishes mandatory physical buffer setbacks and strict operational parameters for chemical dispersal, striking an equitable balance between commercial productivity and community welfare.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16; Republic Act No. 10068 §2",
                "legal_rationale": "Valid exercise of local general welfare powers aligned with national organic agriculture statutory mandates."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "For the purposes of this Ordinance, the following terms, words, and phrases shall be construed as defined hereunder:\n\n(a) 'Agricultural Chemical' or 'Agrochemical' refers to any chemical compound, chemical mixture, synthetic substance, fertilizer, pesticide, insecticide, nematicide, fungicide, herbicide, defoliant, or chemical ripening agent utilized in agricultural production, soil conditioning, or crop protection;\n\n(b) 'Aerial Spraying' refers to the application, dissemination, atomization, or discharge of agricultural chemicals from an airplane, helicopter, ultralight aircraft, unmanned aerial vehicle (drone), or any airborne mechanical conveyance operating above crop canopy level;\n\n(c) 'Chemical Drift' refers to the unintended airborne physical movement of chemical droplets, aerosols, dusts, or vapors beyond the intended cultivation target boundary by action of ambient wind, atmospheric convection, or thermal inversion;\n\n(d) 'Commercial Agricultural Plantation' refers to any contiguous landholding, agricultural estate, or corporate farm aggregation comprising ten (10) hectares or more dedicated to the commercial monoculture cultivation of export crops including bananas, pineapples, oil palm, cacao, or citrus;\n\n(e) 'Mandatory Buffer Zone' refers to a designated physical setback corridor of land of specified minimum width established along the outermost perimeter boundary of an agricultural plantation, planted with permanent multi-layered vegetative barrier species capable of physical particulate interception;\n\n(f) 'Vegetative Barrier' refers to dense, multi-tiered evergreen plantings consisting of outer tall bamboo hedgerows, intermediate non-deciduous broadleaf canopy trees, and ground-level shrubbery planted at high density to intercept airborne aerosol droplets;\n\n(g) 'Participatory Guarantee System (PGS)' refers to a locally focused quality assurance system certified pursuant to Republic Act No. 11511 wherein smallholder farmers and community consumers evaluate organic compliance.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Comprehensive technical definitional section adopting accepted statutory terms without creating substantive legal conflicts."
            },
            {
                "sec_num": 4,
                "sec_title": "MANDATORY THIRTY-METER PHYSICAL VEGETATIVE BUFFER SETBACKS",
                "text": "All owners, operators, agricultural corporations, corporate lessees, and plantation administrators managing commercial agricultural plantations within Davao City shall establish, maintain, and preserve an inviolable physical vegetated buffer zone of not less than thirty (30) linear meters measured from the outermost plantation boundary line inward, wherever said plantation abuts residential settlements, public highways, schools, healthcare centers, religious structures, rivers, creeks, or declared organic farming parcels.\n\n(a) The vegetative buffer zone must feature an engineered, multi-layered bio-shield comprising:\n(1) An outer perimeter barrier planted with dense clumping bamboo species (Bambusa blumeana or Gigantochloa levis) planted at intervals of not more than 1.5 meters to establish a dense ground-to-midstory screen;\n(2) An intermediate canopy belt comprising fast-growing indigenous non-deciduous tree species (such as Acacia mangium, Pterocarpus indicus, or Terminalia microcarpa) reaching a mature foliage height of at least six (6) meters;\n(3) An understory layer of evergreen perennial shrubs planted to prevent low-level laminar wind channeling under tree canopies.\n\n(b) The buffer zone must be fully established within six (6) months from the effectivity of this Ordinance. Commercial plantations failing to establish or maintain compliant vegetative buffers within the prescribed transition period shall be issued an immediate Cease and Desist Order by the City Mayor suspending all chemical application activities on perimeter blocks until compliant bio-shields are certified by the City Agriculturist Office.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(iv)",
                "legal_rationale": "Valid exercise of delegated municipal police power regulating land use setbacks to protect health under RA 7160."
            },
            {
                "sec_num": 5,
                "sec_title": "PARTICIPATORY GUARANTEE SYSTEM AND LOCAL TAX INCENTIVES",
                "text": "In order to vigorously encourage voluntary transition from intensive synthetic agrochemical dependence toward certified ecological and organic farming, smallholder farmers, agrarian reform beneficiaries, and farming cooperatives that convert at least twenty percent (20%) of their contiguous arable lands to certified organic agriculture shall be granted fiscal incentives by the City Government:\n\n(a) Qualified organic farming landholders shall be granted a fifteen percent (15%) local real property tax rebate and assessment discount upon the converted agricultural parcel for three (3) consecutive fiscal years, commencing on the taxable year following formal certification under the Participatory Guarantee System (PGS) pursuant to Republic Act No. 11511;\n\n(b) Applications for organic tax incentives shall be submitted to the City Agriculturist Office, supported by PGS certification credentials, soil organic matter test assays conducted by accredited laboratories, and an on-site verification report signed by the City Organic Agriculture Program Coordinator;\n\n(c) The City Treasurer and City Assessor shall process verified applications and implement the certified real property tax credit pursuant to the express statutory authority granted to local legislative bodies under Section 192 of Republic Act No. 7160.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §192; Republic Act No. 10068 §24; Republic Act No. 11511 §14",
                "legal_rationale": "Valid municipal tax incentive program harmonizing with Section 192 of the Local Government Code and national organic farming laws."
            },
            {
                "sec_num": 6,
                "sec_title": "ABSOLUTE BAN ON AERIAL CHEMICAL PESTICIDE APPLICATION",
                "text": "No person, corporation, agricultural plantation, agribusiness cooperative, aerial spraying contractor, or aerial applicator shall apply, disseminate, atomize, or spray any chemical pesticide, fungicide, herbicide, nematicide, or synthetic agricultural chemical by means of airplane, helicopter, ultralight aircraft, unmanned aerial vehicle (drone), or any aerial dispersal apparatus anywhere within the territorial boundaries of Davao City, regardless of any national permit, product license, commercial aerial spraying license, or experimental dispersal authorization issued by the Fertilizer and Pesticide Authority (FPA).\n\n(a) Any commercial agricultural enterprise currently employing aerial dispersal shall completely terminate all aerial spraying flights within three (3) months from the effectivity of this Ordinance;\n\n(b) Ground equipment, including tractor-mounted boom sprayers, power knapsack units, and calibrated mist blowers, shall be the sole permitted mode of agrochemical dispersal within the city, subject to strict boundary setback compliance;\n\n(c) Any aircraft or unmanned drone caught discharging chemical agents within Davao City airspace shall be impounded by the City Government, and the pilot and corporate officers shall be subject to immediate summary arrest.",
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
                "sec_title": "COMMUNITY CITATION TICKETS AND VOLUNTARY COMPROMISE SETTLEMENT",
                "text": "Deputized agricultural inspectors of the City Agriculturist Office and City ENRO are authorized to issue official Ordinance Violation Receipts (Citation Tickets) to any individual, supervisor, or plantation manager observed violating the provisions of Section 4 or Section 7 of this Ordinance.\n\n(a) Any person or establishment issued a Citation Ticket who does not wish to contest the violation before the courts may avail of the No-Contest Clause by voluntarily paying an administrative compromise penalty to the City Treasurer within seventy-two (72) hours from the issuance of the citation:\n(1) First Offense: Administrative penalty of One Thousand Pesos (P1,000.00);\n(2) Second Offense: Administrative penalty of Two Thousand Five Hundred Pesos (P2,500.00);\n(3) Third Offense: The No-Contest provision shall no longer apply, and formal criminal charges shall be filed.\n\n(b) Individual farmworkers and knapsack sprayers unable to pay the administrative compromise penalty may, in lieu thereof, perform eight (8) to sixteen (16) hours of community service under the supervision of the City Agriculturist Office.",
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
    }

print("Draft 1 defined.")
