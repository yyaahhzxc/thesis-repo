# SANGGUNIANG PANLUNGSOD LEGAL ANNOTATION GUIDE
## Domain Expert Evaluation Guide for Statutory Consistency Auditing of Municipal Ordinances
**Ateneo de Davao University — Department of Computer Science**  
*In Institutional Collaboration with the Sangguniang Panlungsod of Davao City*

---

### Research Project Metadata
* **Thesis Title:** *“A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference”*
* **Authors / Proponents:** Ralph Paolo Dulce & Yahyah Odin (Department of Computer Science, School of Arts and Sciences)
* **Advisory & Faculty:** Mr. Adrian “Ogs” Ablazo (Thesis Adviser) | Ma’am Grace Tacadao (Thesis Professor)
* **Annotator Cohort:** 15 Legal Researchers & Legislative Officers, Sangguniang Panlungsod of Davao City

---

## 1. Project Purpose & System Context

Welcome! As a legal researcher, legislative committee secretary, or policy staff member of the **Sangguniang Panlungsod (City Council) of Davao City**, your professional diligence ensures that every local ordinance enacted is legally sound, effective, and strictly compliant with higher laws.

In Philippine local governance, Local Government Units (LGUs) exercise delegated police and regulatory powers under **Republic Act No. 7160 (The Local Government Code of 1991)**. However, under the well-settled **Magtajas Doctrine** (*Magtajas v. Pryce Properties*, 234 SCRA 255) and related constitutional jurisprudence, a municipal ordinance is strictly **subordinate** to national statutes passed by Congress. A local ordinance cannot prohibit what national law permits, permit what national law prohibits, or alter statutory ceilings.

Manually auditing proposed ordinances against the entire body of Philippine national statutes (Republic Acts, Presidential Decrees, and national codes) during the **First Reading committee review** is an intensive, time-consuming task prone to cognitive fatigue. To assist legislative staff in this critical oversight function, our undergraduate thesis develops an automated, artificial intelligence-assisted conflict screening system.

> [!NOTE]
> **How the AI System Operates (The Coarse-to-Fine Pipeline):**
> 1. **Stage 1 (Information Retrieval / Coarse Search):** Rapidly scans thousands of national statute provisions using lexical (BM25) and semantic vector search to identify candidate laws governing the subject matter of the draft ordinance.
> 2. **Stage 2 (Natural Language Inference / Fine Audit):** Employs a specialized Transformer Cross-Encoder model to conduct a rigorous sentence-level semantic comparison, predicting whether the draft ordinance **entails (complies with)**, **contradicts (violates/exceeds)**, or remains **neutral toward** the national statute.
>
> **Your Role:** Machine learning models require authoritative domain ground truth to benchmark their accuracy. Your independent legal judgments on these 350 curated text pairs serve as the **gold-standard benchmark** against which the AI system's legal reasoning is evaluated.

---

## 2. Data Privacy, Anonymity & Research Ethics (Republic Act No. 10173)

This evaluation strictly adheres to the ethical guidelines of the Ateneo de Davao University Research Ethics Committee and **Republic Act No. 10173 (The Data Privacy Act of 2012)**. The thesis proponents guarantee full protection of your privacy and intellectual contributions through the following safeguards:

* **Complete Evaluator Anonymization:** You will be assigned a standardized alphanumeric code (e.g., `SP-ANN-01` to `SP-ANN-15`). Your name, position, or personal identifiers will **NEVER** appear in the thesis manuscript, public presentations, or published datasets.
* **Purely Voluntary Participation:** Your participation in this study is completely voluntary. You may pause, request clarifications, or withdraw your participation at any time without any professional or administrative penalty.
* **Restricted Academic Purpose:** All annotations collected will be used solely for academic validation, statistical agreement modeling (Fleiss' Kappa), and machine learning error analysis within this thesis.
* **Aggregated Statistical Reporting:** All findings reported in the thesis will be presented strictly in aggregate form (e.g., cross-domain accuracy, panel agreement rates, confusion matrices). No individual response will be singled out or attributed.

---

## 3. The Core Task & The Single-Premise Rule

In each assigned item, you will be presented with an isolated pair of legal texts:
1. **National Statute (The Premise):** A specific statutory provision extracted from a Philippine Republic Act.
2. **Proposed Local Ordinance (The Hypothesis):** A drafted clause from a proposed Davao City municipal ordinance.

Your guiding evaluative question for every pair is:
> *“Based strictly and solely on this specific national statute provision, does the draft local ordinance contradict it, entail (comply with) it, or govern an independent matter (neutral)?”*

> [!IMPORTANT]
> **CRITICAL EVALUATION RULE: The Strict Single-Premise Constraint**  
> As trained legal professionals, your natural instinct is to evaluate an ordinance against the totality of Philippine jurisprudence—synthesizing constitutional provisions, the Revised Penal Code, and unlisted administrative circulars.  
> **⚠️ FOR THIS AI BENCHMARK, YOU MUST SUPPRESS EXTERNAL SYNTHESIS:** Judge each pair **STRICTLY** against the specific National Statute text provided in that specific row. Even if you know from memory that another unmentioned statute might prohibit the act, if the provided statutory premise does not address it, the pair must be evaluated solely on the relationship between the two texts on screen.

---

## 4. The Three Evaluation Choices Explained

### CHOICE 1: CONTRADICTION (Legal Inconsistency / Ultra Vires Overreach)
**Meaning:** The draft local ordinance violates, overrides, diminishes, or exceeds the mandate, bounds, or prohibitions established in the national statute (*Magtajas Doctrine*). Common manifestations include:
* **Exceeding Penalty Ceilings:** National law (RA 7160 Sec. 458) limits city penalties to a maximum ₱5,000 fine and 1-year imprisonment. A draft imposing ₱25,000 or permanent property forfeiture is an ultra vires contradiction.
* **Breaching Temporal Limitations:** National law (RA 7581 Sec. 6) limits automatic calamity price freezes to 60 days. A local draft extending the freeze to 180 days is a contradiction.
* **Diminishing Guaranteed Statutory Rights:** National law (RA 11314) guarantees a 20% student fare discount year-round. A local draft reducing it to 10% or suspending it on weekends is a contradiction.
* **Usurping Exclusive National Regulatory Jurisdiction:** National law vests exclusive rate-setting authority in the Energy Regulatory Commission (ERC) and telecommunications franchising in Congress/NTC. A city ordinance attempting to fix electric utility rates or issue local cellular franchises is a contradiction.
* **Administrative Euphemisms Concealing Statutory Violations:** National law (RA 9344) forbids detaining minors for curfew violations. An ordinance requiring apprehended minors to undergo mandatory locked overnight stays (euphemistically termed *“protective shelter reflection”*) is a contradiction.

### CHOICE 2: ENTAILMENT (Compliant Adoption / Lawful Execution)
**Meaning:** The draft local ordinance directly executes, adopts, enforces, or lawfully implements the national statute within the delegated authority of the Local Government Code without deviation or conflict. Common manifestations include:
* **Direct Statutory Adoption:** The local draft mirrors national highway speed limits (80 km/h under RA 4136) or statutory health standards.
* **Exact Formula Compliance:** The draft appropriates at least 20% of its National Tax Allotment (NTA) for local development (RA 7160 Sec. 287) or exactly 5% for disaster funds (RA 10121).
* **Preserving Mandatory Procedural Clearances:** The draft requires sand-and-gravel quarry operators to secure a national DENR Environmental Compliance Certificate (ECC) prior to Mayor's Permit issuance.
* **Adhering to Diversion Standards:** The draft channels apprehended youth to accredited community counseling and family reintegration, faithfully adhering to RA 9344 non-custodial mandates.

### CHOICE 3: NEUTRAL (Independent / Non-Conflicting Subject Matter)
**Meaning:** Both laws may belong to the same broad subject domain (e.g., environmental protection, transportation, or public health), but they govern distinct administrative obligations with no mutual legal friction, conflict, or direct derivation. Common manifestations include:
* **Public Health Domain:** National law requires immediate hospital reporting of notifiable infectious diseases to DOH, while the local draft sets hygiene protocols for sanitizing public market meat stalls.
* **Local Governance Domain:** National statute establishes juvenile age exemptions (15 years old under RA 9344), while the local draft regulates minimum floor space dimensions for daycare centers (30 sq.m.).
* **Transportation Domain:** National statute establishes licensing criteria for heavy bus operators, while the local draft specifies reflective paint markings for city center bicycle lanes.

---

## 5. Legal Advisory: Local Autonomy vs. Ultra Vires (Magtajas Doctrine)

As legal advisers to the Sangguniang Panlungsod, evaluators frequently and rightfully champion local autonomy under Section 16 of the Local Government Code (The General Welfare Clause). To ensure inter-rater consistency across our benchmark, please apply the established Supreme Court tests governing the constitutional limits of municipal ordinances:

> [!CAUTION]
> **The Magtajas Test of Ordinance Validity (*Magtajas v. Pryce Properties*, 234 SCRA 255):**  
> Under Philippine constitutional jurisprudence, for an ordinance to be valid, it must satisfy six cardinal tests:
> 1. It must not contravene the Constitution or **ANY statute passed by Congress**.
> 2. It must not be unfair or oppressive.
> 3. It must not be partial or discriminatory.
> 4. It must not prohibit, but may regulate, trade.
> 5. It must be general and consistent with public policy.
> 6. It must not be unreasonable.
>
> **Operational Rule:** Local autonomy cannot be invoked to override an express act of Congress. If an ordinance provision departs from, expands penalties beyond, or removes exceptions guaranteed in a national statute, it is **CONTRADICTION (Ultra Vires)**, regardless of whether the local policy goal is deemed beneficial for Davao City.

---

## 6. Difficulty Stratification & Calibrating Your Attention

The 350-pair ground truth corpus is stratified into three distinct complexity tiers to help you calibrate your mental focus:

| Tier Level | Primary Inconsistency Mechanism | What to Look For |
| :--- | :--- | :--- |
| **Tier 1: Surface & Quantitative (30%)** | Direct statutory & numerical cap violations; modal polarity inversions. | Examine explicit numbers: Fines > ₱5,000, jail terms > 1 year, processing deadlines (3/7/20 days), percentage allocations (<20% dev fund), or *shall* flipped to *may*. |
| **Tier 2: Procedural & Jurisdictional (40%)** | Bypassing mandatory statutory procedures, permits, or agency jurisdiction. | Examine regulatory authority: Bypassing DENR Environmental Clearance Certificates, usurping LTFRB/LTO transit powers, or erasing senior citizen/student exemptions. |
| **Tier 3: Latent & Preemption (30%)** | Substantive field preemption, administrative euphemisms, and structural conflict. | Examine legislative effect: Curfew detention rebranded as "protective reflection", disguised local taxes on national goods, or local bans on activities licensed by national charters. |

---

## 7. Confidence Ratings & Legal Notes Protocol

For each text pair in your evaluation form, you will provide three inputs:
1. **Classification Decision:** Contradiction, Entailment, or Neutral.
2. **Confidence Rating (1 to 3 Stars/Scale):** Reflecting how clear-cut the statutory boundary is:
   * **`3` (High Confidence / Clear-Cut):** Explicit statutory ceiling, verbatim compliance, or obvious subject-matter divergence.
   * **`2` (Moderate Confidence):** Clear legal foundation, but requires interpreting administrative phrasing or regulatory scope.
   * **`1` (Low Confidence / Edge Case):** Borderline interpretation, ambiguous statutory wording, or competing statutory interpretations.
3. **Optional Brief Legal Basis / Note:** If you flag a Contradiction or encounter an edge case, please write a concise 1-sentence note (e.g., *“Exceeds ₱5k penalty cap under RA 7160 Sec. 458”* or *“Encroaches on exclusive LTO driver's license confiscation power”*). These expert notes will provide invaluable qualitative evidence for our thesis discussion and defense.

---

## 8. Quick 3-Step Decision Flowchart Guide

```
[START: Read Premise (National Statute) and Hypothesis (Local Draft)]
                          │
                          ▼
            Does the draft clash with, exceed,
         diminish, or bypass the national rule?
           ├── YES ──► [CONTRADICTION (Ultra Vires)]
           └── NO
                 │
                 ▼
        Does the draft directly execute, adopt,
       or adhere to the statutory mandate/formula?
           ├── YES ──► [ENTAILMENT (Compliant Adoption)]
           └── NO
                 │
                 ▼
       Are both provisions governing separate,
        independent administrative obligations?
           └── YES ──► [NEUTRAL (Independent Subject Matter)]
```

---

## 9. Desk Cheat Sheet: Statutory Baseline Ceilings & Supreme Court Precedents

| Legal Area / Subject | National Statutory Baseline | Red Flag in Draft (Contradiction) |
| :--- | :--- | :--- |
| **Ordinance Penalties** | Max ₱5,000 fine / 1-year imprisonment for cities (RA 7160 Sec. 458(a)(1)(iii)). | Drafts imposing ₱10,000–₱50,000 fines, 2+ years jail, or real property title forfeiture. |
| **Calamity Price Control** | Max 60 calendar days automatic price freeze (RA 7581 Sec. 6 / Price Act). | Drafts establishing 90-day, 120-day, or 180-day local price control periods. |
| **Processing Time (EODB)** | Max 3 days (Simple), 7 days (Complex), 20 days (Highly Tech) (RA 11032). | Drafts setting 15-day simple permit reviews or open-ended administrative holds. |
| **Student Fare Discount** | 20% discount on all public land/water transit, year-round (RA 11314). | Drafts reducing discount to 10%, or suspending discounts during summer breaks/holidays. |
| **Juvenile Justice** | Minors 15 and below exempt from criminal liability; non-custodial diversion (RA 9344). | Drafts subjecting minors to lock-up, holding rooms, or curfew jail sentences. |
| **Real Property Tax** | Basic real property tax capped at max 2% of assessed value for cities (RA 7160 Sec. 233). | Drafts levying 3% to 5% basic RPT, or adjusting assessment levels without statutory authority. |
| **Amusement Tax** | Capped at max 30% of gross receipts; school events exempt (RA 7160 Sec. 140). | Drafts levying 35% amusement tax, or taxing school plays, concerts, and athletic meets. |
| **Local Development Fund** | At least 20% of annual National Tax Allotment (NTA) (RA 7160 Sec. 287). | Drafts appropriating less than 20% (e.g., 10%), or diverting development funds to travel/allowances. |
| **Disaster Fund (LDRRMF)** | At least 5% of estimated regular revenue; 30% allocated to QRF (RA 10121). | Drafts allocating less than 5% (e.g., 2%), or reverting unexpended QRF to the General Fund early. |
| **Driver's License Seizure** | Only LTO and officially deputized agents may confiscate driver's licenses (RA 4136). | Drafts authorizing local traffic enforcers to seize driver's licenses without LTO deputization. |
| **Air Pollution & Waste** | Open burning of municipal/backyard waste (*siga*) strictly prohibited (RA 8749 Sec. 20; RA 9003). | Drafts permitting barangay open burning or unpermitted municipal waste incineration. |
| **Public Utilities / Telecoms** | Exclusive franchising jurisdiction vested in Congress and NTC (*Batangas CATV* doctrine). | Drafts attempting to issue municipal telecom certificates or regulate cell tower radio frequencies. |
| **Double Regulatory Taxation** | LGUs prohibited from taxing goods/services already taxed by national government (RA 7160 Sec. 133). | Drafts imposing local inspection fees duplicating national FDA or DTI regulatory charges. |

---

## 10. Submission Mechanics & Google Forms Allocation

To ensure balanced evaluator workload and prevent cognitive fatigue, the 350-pair ground truth benchmark is partitioned into five distinct evaluation sets of exactly 70 pairs each. Evaluators are organized into five panels with three independent raters per panel ($k=3$), ensuring statistically rigorous multi-rater consensus (with one member per panel designated as Senior Annotator based on credentials collected during intake):

| Panel | Assigned Set | Evaluator ID Allocation | Evaluation Pair IDs |
| :--- | :--- | :--- | :--- |
| **Panel A** | Set A (70 Pairs) | `SP-ANN-01`, `SP-ANN-02`, `SP-ANN-03` | GT-001 to GT-070 |
| **Panel B** | Set B (70 Pairs) | `SP-ANN-04`, `SP-ANN-05`, `SP-ANN-06` | GT-071 to GT-140 |
| **Panel C** | Set C (70 Pairs) | `SP-ANN-07`, `SP-ANN-08`, `SP-ANN-09` | GT-141 to GT-210 |
| **Panel D** | Set D (70 Pairs) | `SP-ANN-10`, `SP-ANN-11`, `SP-ANN-12` | GT-211 to GT-280 |
| **Panel E** | Set E (70 Pairs) | `SP-ANN-13`, `SP-ANN-14`, `SP-ANN-15` | GT-281 to GT-350 |

### Step-by-Step Google Forms Workflow:
1. **Open the Official Link:** Access the evaluation Google Form link provided in your panel email or engagement packet.
2. **Section 1 — Evaluator Verification:** Select your assigned Evaluator ID (e.g., `SP-ANN-01`) and designated Panel/Set from the dropdown. The form will automatically branch into your specific 70-pair block.
3. **Section 2 — Pair Evaluation:** For each item (1 to 70), read the National Statute Premise and Municipal Ordinance Hypothesis, select your classification (Contradiction, Entailment, or Neutral), select your confidence score (1 to 3), and optionally add a brief legal basis note.
4. **Estimated Time & Pacing:** Evaluating 70 items takes approximately 60 to 90 minutes (~1 minute per pair). If logged into your Google account, Google Forms automatically saves draft responses, allowing you to complete the evaluation in 1 or 2 sittings.
5. **Final Submission:** Click **SUBMIT** at the end of the form. A confirmation screen will display: *“Thank you! Your legal evaluation has been recorded.”*

---

## 11. Multi-Rater Consensus & Adjudication Protocol

To alleviate decision fatigue and assure evaluators that individual borderline decisions will not skew the benchmark, our research implements a rigorous statistical consensus protocol adapted from established natural language inference benchmarks (Ablazo, 2019; Bowman et al., 2015):

* **Independent Initial Ratings:** Each pair is evaluated independently by all three legal researchers in the assigned panel without mutual consultation, preserving authentic inter-rater variance.
* **Majority Rule Acceptance:** If at least 2 out of 3 evaluators agree on the label (e.g., Contradiction–Contradiction–Neutral), the majority judgment is accepted directly as the final Ground Truth label.
* **Senior Annotator Role & Purpose:** Within each three-member panel (Panels A through E), one evaluator is designated as the **Senior Annotator** (Panel Lead / Adjudicator). Their core responsibilities include:
  * **Binding Qualitative Adjudication (Tie-Breaking):** In rare instances of a three-way split (1 Contradiction, 1 Entailment, 1 Neutral) where no 2-out-of-3 majority consensus exists, the pair is referred to the Senior Annotator of that specific panel to perform an authoritative qualitative review against the statutory codebook and determine the final Ground Truth label (following hierarchical annotation frameworks; Gao et al., 2022; Artstein & Poesio, 2008).
  * **Resolving Edge Cases & Ambiguities:** When subtle statutory phrasing or administrative euphemisms create uncertainty, the Senior Annotator reviews the pair against the standardized codebook to reconcile whether the discrepancy arose from differing interpretations or an overlooked provisos clause.
  * **Panel Point of Contact & Quality Assurance:** Serving as the primary panel contact for procedural questions regarding the annotation guidelines, while ensuring that all initial round ratings remain completely independent.
* **Senior Annotator Selection & Designation Methodology:** To ensure an objective, transparent, and credential-backed designation process, Senior Annotators are chosen through a four-step intake protocol established during the initial administrative engagement with the Sangguniang Panlungsod:
  * **Initial Administrative Outreach (15 Volunteers):** In the proponents' initial official communication to the Sangguniang Panlungsod transmitting this Legal Annotation Guidebook, the proponents formally request a cohort of 15 volunteer legal researchers and legislative staff across the council offices.
  * **Intake Credential Profiling:** Alongside the volunteer roster, the proponents systematically collect two objective profiling metrics from each participant: (1) **Highest Educational Attainment** (e.g., Juris Doctor [J.D.], Bachelor of Laws [LL.B.], Master of Laws [LL.M.], Philippine Bar admission, or relevant postgraduate legal degrees); and (2) **Years of Professional Experience** in legislative drafting, statutory research, ordinance codification, or legal committee review at the Sangguniang Panlungsod.
  * **Objective Panel Stratification & Designation:** Upon receiving the roster and credentials from the SP Secretariat, the proponents organize the 15 volunteers into the 5 balanced panels (3 members per panel) and objectively designate the evaluator within each panel possessing the highest educational attainment and longest legislative drafting tenure as that panel's Senior Annotator (Snow et al., 2008; Zheng et al., 2021; Chalkidis et al., 2022).
  * **Confirmation & Procedural Readiness:** In the follow-up confirmation email to the SP and the panels, the proponents confirm panel assignments and explicitly communicate who the designated Senior Annotator is for each panel, establishing clear procedural readiness "just in case" qualitative tie-breaking or adjudication is required.
* **Statistical Validation:** Inter-annotator reliability will be formally reported in the thesis using Fleiss' Kappa ($\kappa$) and percent agreement across all initial independent ratings prior to adjudication.

---

### Proponents & Contact Information
*Daghang Kaayong Salamat!* We are deeply grateful for your time, professional dedication, and intellectual contribution to developing AI-assisted legislative consistency tools for the City of Davao.

* **Ralph Paolo Dulce** | Email: `rpdulce@addu.edu.ph`
* **Yahyah Odin** | Email: `ygodin@addu.edu.ph`
* **Mr. Adrian “Ogs” Ablazo (Thesis Adviser)** | Department of Computer Science, Ateneo de Davao University
