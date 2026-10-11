"""
scripts/tier2_drafts_data_part3.py
==================================
Contains authentic, natural legislative drafts (Drafts 8, 9, and 10)
modeled directly after real Sangguniang Panlungsod regulatory and amendatory
ordinances from the Davao City corpus (e.g., Ord. 0495-21, Ord. 0354-23,
Ord. 000030-07, Ord. 0158-05).

Eliminates unnatural filler and artificial jargon; preserves authentic
municipal phrasing, real administrative bodies, and genuine statutory
preemption defect targets.
"""

def get_draft_08():
    return {
        "doc_id": "DRAFT-ORD-2026-08",
        "title": "AN ORDINANCE REGULATING COMMERCIAL HIGH-RISE BUILDING STRUCTURAL INSPECTIONS, MANDATING PERIODIC SAFETY AUDITS, AND PRESCRIBING PENALTIES FOR NON-COMPLIANCE IN THE CITY OF DAVAO",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-08, Series of 2026",
        "committee": "Committee on Housing, Rural and Urban Development, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Commercial High-Rise Building Structural Safety Ordinance of Davao City'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "Under Section 16 of Republic Act No. 7160 (The Local Government Code of 1991), the City Government of Davao shall promote public safety and protect its inhabitants from hazards.\n\nIt is hereby declared the policy of the City of Davao to ensure the structural integrity, earthquake resilience, and public safety of commercial high-rise buildings and high-occupancy structures by establishing regular structural maintenance requirements and periodic safety inspections by the Office of the City Building Official.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16",
                "legal_rationale": "Valid exercise of general welfare powers under RA 7160 §16."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "As used in this Ordinance, the following terms shall mean:\n\n(a) Commercial High-Rise Building - refers to any commercial, residential, or mixed-use building in Davao City having five (5) storeys or more in height;\n\n(b) Structural Audit - refers to a comprehensive structural safety assessment and engineering inspection of a building's load-bearing columns, beams, foundations, and shear walls;\n\n(c) Building Owner - refers to the registered owner, condominium corporation, or authorized property management administrator of a commercial high-rise building;\n\n(d) OCBO - refers to the Office of the City Building Official of Davao City.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitions modeled after Ord. 0495-21 and building regulations."
            },
            {
                "sec_num": 4,
                "sec_title": "MANDATORY PERIODIC STRUCTURAL SAFETY AUDITS",
                "text": "All owners and property managers of commercial high-rise buildings that have been in continuous occupancy for fifteen (15) years or more shall cause a structural safety audit to be conducted on the building every five (5) years.\n\nThe audit must be performed and certified by a duly licensed civil/structural engineer, certifying that the building remains structurally stable and safe for continued public occupancy.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(4)(iv)",
                "legal_rationale": "Valid municipal building maintenance regulation under local police powers."
            },
            {
                "sec_num": 5,
                "sec_title": "POST-EARTHQUAKE STRUCTURAL INSPECTIONS",
                "text": "Immediately following any earthquake of Intensity VI or higher on the PHIVOLCS Earthquake Intensity Scale affecting Davao City, all building owners must conduct an immediate visual structural inspection of their buildings.\n\nA rapid assessment report must be submitted to the OCBO within forty-eight (48) hours following the seismic event, verifying whether any structural cracking or damage occurred.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16; Presidential Decree No. 1096",
                "legal_rationale": "Harmonious local safety standard protecting public welfare during disaster response."
            },
            {
                "sec_num": 6,
                "sec_title": "SUBMISSION OF STRUCTURAL STABILITY CERTIFICATE",
                "text": "The verified Structural Stability Certificate shall be submitted to the Office of the City Building Official as a mandatory requirement for the renewal of the building's Annual Safety Inspection Certificate and Mayor's Business Permit.\n\nBuildings failing to submit the certified audit report shall be issued a Notice of Non-Compliance by the OCBO.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(3)(iv)",
                "legal_rationale": "Valid municipal licensing requirement."
            },
            {
                "sec_num": 7,
                "sec_title": "AUTHORITY TO GRANT STRUCTURAL WAIVERS",
                "text": "The City Building Official is hereby authorized, upon application and submission of an engineering certification from the project developer, to grant structural code waivers and relax specific seismic design requirements under the National Building Code for specialized commercial and mixed-use high-rise developments within designated commercial growth zones of the city.\n\nUpon approval of such waiver by the City Building Official, the building project shall be deemed compliant with all applicable structural and engineering standards.",
                "label": "Contradiction",
                "target_statute": "Presidential Decree No. 1096 §301; Presidential Decree No. 1096 §302",
                "legal_rationale": "Directly contradicts Presidential Decree No. 1096 §§301 and 302 (The National Building Code of the Philippines). National building standards and seismic design criteria are established exclusively by the Secretary of Public Works and Highways under national law. Local building officials possess no statutory authority to grant waivers or relax structural safety codes under the Magtajas preemption doctrine."
            },
            {
                "sec_num": 8,
                "sec_title": "IMPLEMENTING AGENCY",
                "text": "The Office of the City Building Official (OCBO), in coordination with the City Disaster Risk Reduction and Management Office (CDRRMO), shall be the primary agency responsible for enforcing the provisions of this Ordinance.\n\nOCBO engineers are authorized to conduct on-site verifications of high-rise structures during regular working hours.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard implementing agency clause modeled after Ord. 0495-21."
            },
            {
                "sec_num": 9,
                "sec_title": "NOTICE OF DEFICIENCY AND REPAIR ORDER",
                "text": "Whenever an inspection reveals structural distress, excessive cracking, or uncertified modifications, the OCBO shall issue a written Notice of Deficiency and Repair Order giving the owner sixty (60) calendar days to execute retrofitting works.\n\nDuring retrofitting, hazardous sections of the building must be barricaded to ensure public safety.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard administrative enforcement notice clause."
            },
            {
                "sec_num": 10,
                "sec_title": "REVOCATION OF OCCUPANCY PERMIT",
                "text": "Failure of the building owner to submit the required structural audit or rectify certified structural defects shall be sufficient ground for the City Building Official to revoke the building's Certificate of Occupancy and order the temporary evacuation of the structure until retrofitting is completed.",
                "label": "Entailment",
                "target_statute": "Presidential Decree No. 1096 §306",
                "legal_rationale": "Harmonious local enforcement standard aligned with national building safety powers."
            },
            {
                "sec_num": 11,
                "sec_title": "PENALTIES",
                "text": "Any building owner, property manager, or corporate officer who fails or refuses to comply with this Ordinance shall, upon conviction, be punished by a fine of Three Thousand Pesos (Php 3,000.00) for the first offense; Five Thousand Pesos (Php 5,000.00) or imprisonment of up to six (6) months, or both, for subsequent offenses.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Complies strictly with statutory penalty ceilings under RA 7160 §458."
            },
            {
                "sec_num": 12,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any provision of this Ordinance is held unconstitutional or invalid, the other provisions hereof not affected thereby shall continue in full force and effect.",
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


def get_draft_09():
    return {
        "doc_id": "DRAFT-ORD-2026-09",
        "title": "AN ORDINANCE REGULATING COMMERCIAL SAND, GRAVEL, AND QUARRY EXTRACTION OPERATIONS, PRESCRIBING ENVIRONMENTAL SAFEGUARDS ALONG RIVER SYSTEMS, AND PROVIDING PENALTIES FOR VIOLATIONS THEREOF IN THE CITY OF DAVAO",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-09, Series of 2026",
        "committee": "Committee on Environment and Natural Resources, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the 'Riverbed Sand, Gravel, and Quarry Regulation Ordinance of Davao City'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal title clause."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "Pursuant to Section 16 and Section 138 of Republic Act No. 7160 (The Local Government Code of 1991), the City Government of Davao is authorized to regulate the extraction of quarry resources and protect rivers and natural ecosystems from degradation.\n\nIt is hereby declared the policy of the City of Davao to regulate small-scale quarrying and sand and gravel extraction along river systems to protect riverbanks, prevent flooding, and ensure that commercial extraction complies with environmental laws.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §16; Republic Act No. 7160 §138",
                "legal_rationale": "Valid exercise of delegated quarry regulatory powers under RA 7160."
            },
            {
                "sec_num": 3,
                "sec_title": "DEFINITION OF TERMS",
                "text": "As used in this Ordinance, the following terms shall mean:\n\n(a) Quarry Resources - refers to any common stone, gravel, sand, earth, and volcanic rock extracted for construction purposes;\n\n(b) Commercial Sand and Gravel Permit - refers to an extraction permit issued by the City Mayor for quarry areas not exceeding five (5) hectares pursuant to Section 138 of RA 7160;\n\n(c) Quarry Operator - refers to any individual, cooperative, or enterprise granted a valid quarry extraction permit by the City Government;\n\n(d) CQRB - refers to the City Quarry Regulatory Board of Davao City;\n\n(e) Riverbed - refers to the natural bed and banks of rivers within the city, including the Davao River, Talomo River, and Lasang River.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard definitional section modeled after CQRB rules and RA 7160 §138."
            },
            {
                "sec_num": 4,
                "sec_title": "PERMIT REQUIREMENT AND AREA RESTRICTIONS",
                "text": "No person or entity shall extract, haul, or transport sand, gravel, or quarry materials from any riverbed or public land in Davao City without first securing a Commercial Sand and Gravel Permit issued by the City Mayor upon recommendation of the CQRB.\n\nQuarry permits shall be limited to designated extraction zones and shall not exceed five (5) hectares in area per permit.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §138",
                "legal_rationale": "Harmonious local permitting standard adhering strictly to the 5-hectare limit under RA 7160 §138."
            },
            {
                "sec_num": 5,
                "sec_title": "GRANT OF LONG-TERM QUARRY AND MINERAL CONCESSIONS",
                "text": "The City Mayor, upon recommendation of the City Quarry Regulatory Board (CQRB) and approval of the Sangguniang Panlungsod, is hereby authorized to grant twenty-five (25) year mineral extraction concessions and agreements for the commercial extraction of sand, gravel, and associated metallic mineral ores along major river systems in Davao City.\n\nSuch municipal mineral concessions shall confer exclusive commercial exploration and mining rights over mineralized riverbeds, and holders thereof shall be exempt from securing national mineral agreements from the Department of Environment and Natural Resources.",
                "label": "Contradiction",
                "target_statute": "1987 Constitution, Art. XII §2; Republic Act No. 7942 §27",
                "legal_rationale": "Directly contradicts Article XII, Section 2 of the 1987 Constitution and Section 27 of Republic Act No. 7942 (The Philippine Mining Act of 1995). Under constitutional and statutory law, all mineral resources are owned by the State, and large-scale, long-term 25-year mineral agreements and metallic mining concessions can only be entered into by the National Government through the President and DENR. Local governments are restricted to small-scale sand and gravel permits up to 5 hectares under RA 7160 §138."
            },
            {
                "sec_num": 6,
                "sec_title": "RIVERBANK BUFFER AND DEPTH RESTRICTIONS",
                "text": "To prevent riverbank erosion, all extraction activities shall maintain an inviolable setback of not less than twenty (20) meters from the natural riverbank, dikes, and flood control structures.\n\nExcavation depth shall not exceed two (2) meters below the natural water level of the river, and the use of heavy suction dredgers without special environmental permits is strictly prohibited.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(vi); Presidential Decree No. 1067",
                "legal_rationale": "Valid municipal environmental protection standard preserving riverbanks."
            },
            {
                "sec_num": 7,
                "sec_title": "HAULING DELIVERY RECEIPTS AND TARPAULIN COVERS",
                "text": "All dump trucks and transport vehicles hauling sand and gravel on public roads in Davao City must possess official Delivery Receipts (DR) issued by the City Treasurer's Office.\n\nTruck beds containing sand and gravel must be fully covered with sturdy tarpaulins or canvas sheets to prevent spillage and flying dust while traversing public thoroughfares.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §138; Republic Act No. 4136",
                "legal_rationale": "Valid municipal transport and safety regulation."
            },
            {
                "sec_num": 8,
                "sec_title": "IMPLEMENTING AND MONITORING AGENCIES",
                "text": "The City Quarry Regulatory Board (CQRB) and the City Environment and Natural Resources Office (City ENRO) shall oversee the enforcement of this Ordinance.\n\nCity ENRO checkpoint personnel and CTTMO inspectors are authorized to inspect hauling trucks and verify valid delivery receipts at city monitoring stations.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard implementing agency clause."
            },
            {
                "sec_num": 9,
                "sec_title": "SUSPENSION AND CANCELLATION OF PERMITS",
                "text": "Any permit holder who violates riverbank buffer restrictions or operates outside their permitted boundary shall be issued a Cease and Desist Order by the City Mayor and their permit suspended for thirty (30) days for the first offense, and cancelled for subsequent offenses.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §138",
                "legal_rationale": "Valid municipal administrative authority regulating local quarry permits."
            },
            {
                "sec_num": 10,
                "sec_title": "PENALTIES FOR ILLEGAL EXTRACTION",
                "text": "Any person or operator engaging in unauthorized sand and gravel extraction without a valid permit shall, upon conviction, be punished by a fine of Five Thousand Pesos (Php 5,000.00) or imprisonment for six (6) months, or both, at the discretion of the court.\n\nIn addition, all extracted minerals, heavy equipment, and hauling trucks used in illegal quarrying operations shall be subject to impoundment by the City Government.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Complies strictly with statutory penalty ceilings under RA 7160 §458."
            },
            {
                "sec_num": 11,
                "sec_title": "APPROPRIATION",
                "text": "The City Government of Davao shall allocate sufficient funds in its annual budget to support riverbed environmental monitoring, drone surveillance, and CQRB operational activities.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard appropriation clause."
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


def get_draft_10():
    return {
        "doc_id": "DRAFT-ORD-2026-10",
        "title": "AN ORDINANCE AMENDING CERTAIN PROVISIONS OF THE 2005 REVENUE CODE OF DAVAO CITY, ADJUSTING REGULATORY FEES, LEVYING TAXES ON CERTAIN CORPORATE ACTIVITIES AND PROPERTIES, AND FOR OTHER PURPOSES",
        "proposed_ordinance_no": "Proposed Ordinance No. 2026-10, Series of 2026",
        "committee": "Committee on Ways and Means, Sangguniang Panlungsod",
        "sections": [
            {
                "sec_num": 1,
                "sec_title": "TITLE",
                "text": "This Ordinance shall be known and cited as the '2026 Omnibus Revenue Code Amendments Ordinance of Davao City'.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard municipal title clause modeled after Ord. 000030-07."
            },
            {
                "sec_num": 2,
                "sec_title": "DECLARATION OF POLICY",
                "text": "Under Section 129 and Section 151 of Republic Act No. 7160 (The Local Government Code of 1991), the City of Davao is authorized to create its own sources of revenues, levy taxes, fees, and charges for public purposes, and adjust its revenue schedules to finance basic public services.\n\nIt is the policy of the City Government of Davao to maintain an equitable, progressive, and efficient revenue collection system that supports infrastructure and social development while remaining strictly within the statutory taxing powers granted by law.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §129; Republic Act No. 7160 §151",
                "legal_rationale": "Valid exercise of local taxing authority under RA 7160 §129 and §151."
            },
            {
                "sec_num": 3,
                "sec_title": "AMENDMENT TO FIXED REGULATORY PERMIT FEES",
                "text": "Section 45 of the 2005 Revenue Code of Davao City is hereby amended to adjust the annual regulatory permit fees on commercial establishments to reflect the reasonable administrative cost of regulation and inspection:\n\n(a) Wholesale and retail merchants with capital of more than P500,000: One Thousand Pesos (Php 1,000.00);\n\n(b) Manufacturing and industrial processing plants: Two Thousand Five Hundred Pesos (Php 2,500.00);\n\n(c) Commercial banks and financial intermediaries: Three Thousand Pesos (Php 3,000.00).",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §147",
                "legal_rationale": "Valid adjustment of municipal regulatory fees under RA 7160 §147."
            },
            {
                "sec_num": 4,
                "sec_title": "ADJUSTMENT OF SANITATION AND HEALTH INSPECTION FEES",
                "text": "Section 52 of the 2005 Revenue Code of Davao City is hereby amended to prescribe updated annual sanitary inspection fees for all food handling and hospitality businesses operating in the city.\n\nAll food establishments, restaurants, and bakeries shall pay an annual sanitary inspection fee of Three Hundred Pesos (Php 300.00) to cover the cost of hygiene certification by the City Health Office.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §147",
                "legal_rationale": "Valid municipal inspection fee under RA 7160 §147."
            },
            {
                "sec_num": 5,
                "sec_title": "MAYOR'S PERMIT ON SPECIAL BUSINESS OCCUPATIONS",
                "text": "Section 61 of the 2005 Revenue Code of Davao City is hereby amended to require individuals engaged in specialized commercial trades, security agency operations, and private warehouse leasing to secure an annual Mayor's Permit clearance prior to operation in Davao City.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §151",
                "legal_rationale": "Valid exercise of municipal licensing powers."
            },
            {
                "sec_num": 6,
                "sec_title": "LEVY ON CORPORATE DIVIDENDS",
                "text": "Section 68 of the 2005 Revenue Code of Davao City is hereby amended to levy an annual business tax of two percent (2%) on the gross amount of dividends and investment yields distributed by corporations and holding companies maintaining their principal office or branch in Davao City.\n\nThe City Treasurer is authorized to assess and collect this tax from corporate entities at the end of each fiscal dividend declaration period.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 7160 §133(a)",
                "legal_rationale": "Directly violates Section 133(a) of Republic Act No. 7160 (The Local Government Code of 1991), which expressly prohibits local government units from levying income tax of any kind, including taxes on corporate dividends and investment returns. Struck down under the Magtajas preemption doctrine."
            },
            {
                "sec_num": 7,
                "sec_title": "REAL PROPERTY TAX ON PENSION ASSETS",
                "text": "Section 112 of the 2005 Revenue Code of Davao City is hereby amended to provide that real properties, commercial lands, and investment assets situated within Davao City belonging to or held in trust by national pension and social security institutions, including the Government Service Insurance System (GSIS) and the Social Security System (SSS), shall be subject to the basic real property tax and special education fund tax levied by the City Government.\n\nAll previous local tax exemptions granted to such statutory pension properties are hereby revoked.",
                "label": "Contradiction",
                "target_statute": "Republic Act No. 8291 §39; Republic Act No. 7160 §133(o)",
                "legal_rationale": "Directly contradicts Republic Act No. 8291 §39 (GSIS Act of 1997) and Republic Act No. 7160 §133(o). National law explicitly exempts GSIS and statutory pension reserve assets and properties from all local taxes, charges, and assessments under the doctrine of sovereign and statutory exemption affirmed in GSIS v. City Assessor of Iloilo (2006)."
            },
            {
                "sec_num": 8,
                "sec_title": "DELINQUENCY SURCHARGE AND INTEREST",
                "text": "Section 125 of the 2005 Revenue Code is amended to provide that failure to pay any local tax or fee on or before the twentieth (20th) day of January of each calendar year shall subject the taxpayer to a surcharge of twenty-five percent (25%) of the amount due, plus interest at the rate of two percent (2%) per month until paid, up to a maximum period of thirty-six (36) months.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §168",
                "legal_rationale": "Harmonious local tax delinquency surcharge adhering strictly to Section 168 of the Local Government Code."
            },
            {
                "sec_num": 9,
                "sec_title": "IMPLEMENTING OFFICE",
                "text": "The City Treasurer's Office, in coordination with the City Assessor's Office and the Business Bureau, shall implement and administer the collection of taxes, fees, and charges prescribed under this Ordinance.\n\nThe City Treasurer shall formulate administrative guidelines for tax assessments.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard implementing agency clause assigning duties to the City Treasurer."
            },
            {
                "sec_num": 10,
                "sec_title": "PENAL SANCTIONS",
                "text": "Any person who willfully violates any provision of this Ordinance, or fails to pay assessed local taxes within the prescribed period, shall, upon conviction, be punished by a fine of Five Thousand Pesos (Php 5,000.00) or imprisonment of up to six (6) months, or both, at the discretion of the court.",
                "label": "Entailment",
                "target_statute": "Republic Act No. 7160 §458(a)(1)(iii)",
                "legal_rationale": "Complies strictly with statutory penalty ceilings under RA 7160 §458."
            },
            {
                "sec_num": 11,
                "sec_title": "SEPARABILITY CLAUSE",
                "text": "If any section, subsection, or provision of this Ordinance is declared unconstitutional or invalid by a court of competent jurisdiction, the remaining sections and provisions hereof not affected thereby shall continue in full force and effect.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard separability clause modeled after Ord. 000030-07."
            },
            {
                "sec_num": 12,
                "sec_title": "REPEALING CLAUSE",
                "text": "All city ordinances, executive orders, or rules and regulations inconsistent with the provisions of this Ordinance are hereby repealed or modified accordingly.",
                "label": "Neutral",
                "target_statute": None,
                "legal_rationale": "Standard repealing clause."
            },
            {
                "sec_num": 13,
                "sec_title": "EFFECTIVITY",
                "text": "This Ordinance shall take effect on January 1, 2027, following its approval and complete publication in a newspaper of local circulation in Davao City.",
                "label": "Neutral",
                "target_statute": "Republic Act No. 7160 §59",
                "legal_rationale": "Standard effectivity clause."
            }
        ]
    }
