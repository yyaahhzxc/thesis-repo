---
trigger: model_decision
description: This rule shall be applied when working on the prototype demo site, web interface, full-document audit engine, or local neural inference pipeline (demo/, scripts/, src/).
---

# **Ex-Ante Prototype Demo Site & Local Neural Engine Instructions**

**Institution:** Ateneo de Davao University, Department of Computer Science  
**Project:** *"A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference"*  
**Authors / Proponents:** Ralph Paolo Dulce & Yahyah Odin  
**Adviser:** Mr. Adrian "Ogs" Ablazo | **Professor:** Ma'am Grace Tacadao  
**System Target:** Local LGU Edge Simulation Testbed (Host A: Intel Core i3-10105F, Radeon RX 6600, 8 GB RAM, Windows)  

---

## **1. Architectural Foundation & Core Principles**

The prototype demonstration system (`demo/app.py`, `demo/static/index.html`) is an interactive, explainable, and production-faithful deployment of the thesis research system designed for presentation to thesis defense panelists, university faculty, and Sangguniang Panlungsod (SP) legal officers.

### **1.1. 100% Commitment to Option 2 (Pure Transformer Cross-Encoder NLI Architecture)**
1. **Pure Neural Generalization:** All semantic preemption conflict decisions must stem directly from genuine PyTorch neural tensors evaluated through DeBERTa-v3 (`models/nli-deberta-v3-base/`) with the calibrated decision threshold `tau* = 0.45` (Chapter 3 §3.3 & §3.7.2).
2. **Strict Prohibition of Bandaids, Regex Heuristics & Artificial Overrides:**
   - **No Regex Pattern Matching:** Never inject ad-hoc regex scoring (e.g. `compute_generalized_deontic_score()`) or hybrid weighting formulas (`0.40 * p_c + 0.60 * d_score`).
   - **No Case Sniffing:** Never write code that checks file names, case IDs, or keyword tags to trigger special-case execution (e.g., `if "mosqueda" in filename:`, `if "DRAFT-01" in doc_id:`).
   - **No Candidate Injection Backdoors:** Candidates evaluated by Stage 2 must be organically retrieved by Stage 1 hybrid retrieval from the authentic 176,421-provision knowledge base (`output/dual_corpus_embeddings_minilm.npy` and `output/dual_corpus_bm25.pkl`). Never hardcode or manually prepend target statutes into candidate lists.
   - **No Hardcoded Score Dictionaries:** Never substitute neural forward passes with lookup dictionaries of precomputed or fabricated confidence percentages.
3. **The Solitary Symbolic Exception (Integer Penalty Ceiling):**
   The only non-neural rule permitted in the entire pipeline is a pure integer arithmetic validator (`check_statutory_penalty_ceiling()`): extracting numerical fine amounts in Philippine Pesos from draft penalty clauses and verifying whether the fine exceeds the statutory ₱5,000 ceiling prescribed for city ordinances under Republic Act No. 7160 Section 458(a)(1)(iii).

---

## **2. Natural Language Inference & Sequence Construction Protocol**

### **2.1. Canonical Sequence Prompt Formatting**
To avoid attention dilution, token bloat, and sequence truncation within DeBERTa's 512-token context window:
1. **Premise Sequence (Text A - Controlling Statute):**
   Must be formatted concisely as:
   ```python
   premise = f"[{cand['citation']}] {raw_text.lstrip('- \r\n')}".strip()
   ```
   - **Do NOT inject verbose Act titles or multi-sentence metadata:** Never use raw `prepended_text` containing 30--50 words of legislative enactment titles into the Cross-Encoder premise, as this dilutes attention weights on operative verbs and duty standards.
   - **Do NOT create nested brackets:** Never wrap `cand['citation']` in brackets if the following text already begins with citation brackets.
2. **Hypothesis Sequence (Text B - Proposed Ordinance Provision):**
   Must be formatted cleanly as:
   ```python
   hypothesis = f"[{header_title}] {clause_text}".strip()
   ```
   Where `header_title` is `SECTION X: TITLE` or `SECTION X`.

### **2.2. Strict Zero Editorial Pollution Protocol**
Under NO circumstances should any statutory provision, ordinance text, benchmark premise, or candidate text string displayed in the UI or fed to tensors be synthetically rewritten, paraphrased, injected with explanatory commentary, or augmented with synthetic sentences:
1. All statutory text displayed in the Existing Provision card must be 100% verbatim authentic text extracted from Lawphil or the Davao City ordinance archives (`data/unified_dual_statutory_provisions.jsonl`).
2. Legal doctrine explanations, preemption rationales, and *ratios decidendi* must reside strictly in dedicated metadata/explanation fields (`legal_rationale`, `verdict_desc`, `ratio_decidendi`) and NEVER pollute the statutory text fields (`statutory_text`, `statute_text`, `ordinance_text`, `premise`).

---

## **3. Legislative Anatomy & Procedural Boilerplate Classification**

In accordance with Philippine statutory drafting standards (Sangguniang Panlungsod Legislative Manual and National Legislative Drafting Rules), every municipal ordinance contains formal administrative clauses that establish legal context but do not impose operative prohibitions or regulatory mandates.

### **3.1. Standard Procedural Boilerplate Categories**
The section chunker (`chunk_ordinance_sections()`) must recognize the following standard procedural clauses as neutral legislative boilerplate:
- **Title / Short Title**
- **Definition of Terms / Definitions**
- **Scope and Applicability / Coverage** *(territorial reach statements, not operative restrictions)*
- **Rules of Interpretation**
- **Funding / Appropriations**
- **Implementing Rules and Regulations (IRR)**
- **Separability Clause**
- **Repealing Clause**
- **Effectivity Clause**

### **3.2. Boilerplate Handling Behavior**
1. Standard procedural boilerplate clauses are recognized as `is_boilerplate: True` and assigned `NEUTRAL (98.0%)` with standard drafting rationale.
2. This prunes non-regulatory clauses from expensive Stage 2 cross-encoder forward passes on edge hardware, cutting audit latency by >50% without discarding substantive regulatory obligations.
3. Substantive provisions (prohibitions, permits, conditions, fees, administrative inspections, and penal sanctions) are always classified as `is_boilerplate: False` and undergo full Stage 1 retrieval and Stage 2 neural cross-encoder evaluation.

---

## **4. Multi-Stage Pipeline Execution Standards**

### **4.1. Stage 1 Hybrid Retrieval (BM25 + Dense Bi-Encoder)**
- **Embedder:** `all-MiniLM-L6-v2` (`models/all-MiniLM-L6-v2/`, 384 dimensions).
- **Index:** Unified dual statutory corpus containing 176,421 searchable provisions (`dual_corpus_embeddings_minilm.npy` and `dual_corpus_bm25.pkl`).
- **Scoring Formulation:** Calibrated linear combination:
  `Score = 0.50 * Normalized_BM25 + 0.50 * Dense_Cosine_Similarity`
- **Scope Filtering:** When auditing local drafts for vertical statutory preemption, filter query scope to national positive law (`scope="national"`, provisions 0..164,620) and exclude obsolete pre-LGC colonial enactments (Act No. and Commonwealth Act) and superseded charters (RA 4354).
- **Evaluation Depth:** Evaluate the Top 8 retrieved statutory candidates per substantive section through Stage 2.

### **4.2. Stage 2 Flattened Batch Cross-Encoder Inference**
- **Model:** `nli-deberta-v3-base` (`models/nli-deberta-v3-base/`, 86M parameters).
- **Decision Threshold:** Calibrated threshold `tau* = 0.45` on contradiction probability `P(Contradiction)`.
- **Optimization Standards (Host A CPU Acceleration):**
  - **Dynamic Token Padding:** Batch sequence length clamped to max length of active mini-batch (rather than static 512).
  - **Vectorized Flattened Batching:** Vectorized PyTorch forward pass across candidate pairs to leverage Intel AVX2 SIMD instructions.
  - **Per-Pair Latency Telemetry:** Log execution latency in milliseconds and report seq_len for total transparency.

---

## **5. UI / UX Standards & Wireframe Fidelity (`demo/static/index.html`)**

The user interface must strictly preserve the visual aesthetics, layout balance, and interaction patterns designed in collaboration with Yah:

1. **Brand Identity & Aesthetic Theme:**
   - Primary Accent: Official Ateneo / SP Maroon (`#7F2723`).
   - Clean Modern Card System: Rounded gray containers (`border-radius: 28px`, `background: #D4D4D8`).
   - Thick Structural Dividers: `3.5px solid #000000` separating hierarchical card elements.
2. **Top Main Split Layout:**
   - **Left Column (410px):** Stage 1 Candidate Shortlist table (BM25 + all-MiniLM-L6-v2) with sticky headers, scrollable rows, Lawphil links, and color-coded Stage 2 confidence badges.
   - **Right Column (1fr):** Stage 2 Results Card.
3. **Stage 2 Conflict Header & Decision Diamond:**
   - Top-right confidence gauge box with mathematical caret pointer `▲` centered at the exact calibrated `45.0% DECISION THRESHOLD` line.
   - Left metadata panel: `POTENTIAL CONFLICT #X` badge, doctrine pill (`Direct Statutory Preemption (LGC §5(a))`), operative draft section heading, and concise preemption summary.
4. **Nested Interactive Accordions:**
   - **Existing Provision (Left Card):** Bold uppercase statute header (`REPUBLIC ACT NO. 7296...`), collapsible parent context, and verbatim operative statutory text.
   - **Proposed Ordinance (Right Card):** Bold draft enactment header, collapsible parent section, and verbatim proposed draft text.
   - Highlight conflicting keywords dynamically.
5. **Real-Time Telemetry & Progress Streaming:**
   - Navbar status badge: `🟢 Live Neural (CPU: DeBERTa-v3 & MiniLM)`.
   - Real-time audit progress via Server-Sent Events (`/api/audit-document-stream`), reporting active section name, percentage complete, and live progress bar.

---

## **6. Multi-Document Verification & Non-Regression Protocol**

Whenever modifications are made to `demo/app.py` or the underlying inference pipeline:
1. **Never Validate on a Single File Alone:** A fix that resolves one file must never degrade or alter performance across the remaining test suites.
2. **Standard Cross-Act Verification Suite:** Always verify against diverse statutory domains:
   - **Landmark Supreme Court Jurisprudence (`demo/sample_cases/`):** Mosqueda (aerial spraying ban), Batangas CATV (cable rates), Magtajas (casino preemption), Evasco (billboards).
   - **Authentic Davao City Enactments (`corpus/davao_city_tier3_ordinances/`):** Anti-Smoking (Ord. 0367-12), Speed Limits (Ord. 0270-23).
   - **Tier 2 Synthetic Draft Ordinances (`data/tier2_draft_ordinances/`):** 10 authentic municipal drafts (115 sections) with planted statutory defects.
3. **Execution Environment:** Keep the demo server running as a persistent background daemon on `http://127.0.0.1:5050` (`.\venv\Scripts\python.exe demo/app.py`).

---

## **7. Sangguniang Panlungsod (SP) Legal Drafter & Reviewer Mindset Protocol**

Whenever authoring, parsing, chunking, testing, or formatting ordinances, sample case PDFs, or demo site inputs:

### **7.1. Adopting the SP Legal Mindset**
1. **The SP Legislative Drafter Perspective:**
   Always place yourself in the exact mindset of an actual Sangguniang Panlungsod (SP) legal officer, committee secretary, or legislative researcher drafting or reviewing an ordinance for the City Council of Davao.
2. **The Demo Site User Perspective:**
   Alternatively, imagine yourself as that SP legal researcher actively using the ex-ante semantic conflict detection system to audit an incoming draft prior to committee hearings or 2nd reading. Ask yourself: *Would an authentic legislative staff member ever encounter or include this text in a municipal enactment?*

### **7.2. Zero Academic / Judicial Meta Fluff in Documents**
Under NO circumstances should any ordinance document (PDF, TXT, or JSON section text) contain academic test fixture labels, benchmark ground truth tags, or judicial ruling commentaries:
1. **No Judicial Context under Titles:** Never append `Judicial Context: Case Name (G.R. No. ...)` beneath the long title. An ordinance is an enactment of local positive law, not a law school case brief.
2. **No Landmark Branding in Headers:** Never stamp `LANDMARK ORDINANCE` or research category tags in running page headers. Running headers must strictly display `[Ordinance No.] • [LGU]` and page numbers.
3. **No Project Footers:** Never stamp `OFFICIAL LEGISLATIVE RECORD • EX-ANTE LEGAL ARCHIVES REVIEW` or research project watermarks onto legislative pages. Footers must remain clean with authentic page numbers (`Page X of Y`).
4. **No Test Fixture Lines in Text Bodies:** Never include `Judicial Reference:`, `Judicial Ruling:`, `Gold NLI Label:`, or `Superior National Law:` in `.txt` or `.json` legislative text bodies. Judicial case references and benchmark ground truths belong strictly in backend scoring metadata (`case_id`, `case_name`, `docket_no`, `legal_rationale`), completely isolated from the legislative text.

### **7.3. Authentic Legislative Typography, Structure & Hierarchy**
1. **Official Letterhead:** Page 1 must feature the authentic letterhead (`REPUBLIC OF THE PHILIPPINES`, `CITY OF DAVAO`, `OFFICE OF THE SANGGUNIANG PANLUNGSOD` or respective LGU/Council) and official legislative divider line.
2. **Definition of Terms & Enumerated Lists:**
   - Alphanumeric list items (`(a)`, `(b)`, `(c)`, `a.`, `b.`, `c.`, `1.`, `2.`, `3.`, `(1)`, `(2)`, `(3)`) must NEVER be squished together into a single continuous wall of text.
   - Each item must be formatted as an individual indented line with hanging indents (`leftIndent=24`, `firstLineIndent=-14`).
   - Defined terms must be bolded (`<b>a. DEFINED TERM</b> &mdash; definition`).
3. **Chapter & Article Separation:**
   - Legislative chapters and articles must be cleanly spaced and centered as distinct headings between operative sections (`CHAPTER X`, `ARTICLE Y`), never lumped into the trailing sentences of preceding sections.
4. **Structured Legislative Tables:**
   - Graduated penalty schedules, fee matrices, and speed limit tables must be rendered as clean, formatted tables with light-shaded header rows and crisp borders, never left as raw markdown pipe text.
5. **Authentic Signing & Attestation Blocks:**
   - Preserve authentic municipal signing structures (Enactment date, Secretary certification, Vice Mayor / Presiding Officer attestation, Mayor approval).
6. **Robust Font & Currency Glyphs:**
   - Never allow unrenderable unicode currency signs (`₱`) to generate missing glyph black boxes (`■`) in ReportLab; sanitize all Philippine Peso amounts to `P` or `Php`.


