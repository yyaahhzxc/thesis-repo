# **Foundational Research Integrity, Data Standards & Collaborative Principles**

**Institution:** Ateneo de Davao University, Department of Computer Science  
**Project:** *"A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference"*  
**Authors / Proponents:** Ralph Paolo Dulce ("Ralph") & Yahyah Odin ("Yah")  
**Thesis Adviser:** Mr. Adrian "Ogs" Ablazo | **Course Professor:** Ma'am Grace Tacadao  

---

## **1. Core Collaborative Co-Author Protocol & Chat Standards**

Both Ralph and Yah are first-class proponents with full, equal access to all Antigravity capabilities (code authoring, script execution, benchmark evaluation, LaTeX manuscript drafting, PDF compilation, task tracking, and administrative routing).

1. **User Identification & Context Grounding:**
   - **When User is Yah ("I'm Yah", "Yah here"):** Recognize Yah immediately. Ground directly into active machine learning modeling, retrieval benchmarking, pipeline automation, and manuscript revisions.
   - **When User is Ralph ("I'm Ralph", "Ralph here"):** Recognize Ralph immediately. Ground directly into local ordinance OCR experiments, human evaluation deployment, administrative routing (HRMO / City Administrator), and collaborative drafting.
   - **When No Name is Specified:** Check `docs/THESIS_MASTER_TASKS.md` immediately, maintain full situational awareness, and execute requests while preserving continuous task synchronization.
2. **Cross-Host Git Synchronization:**
   - Yah operates primarily on **Host A (Desktop)** (Core i3-10105F, Radeon RX 6600, 8 GB RAM, Windows) for LGU edge simulation.
   - Ralph operates primarily on **Host B (GPU Laptop)** (Lenovo Legion 5: Ryzen 7 7435HS, RTX 5050 Laptop GPU, 16 GB RAM, Windows) for deep learning training and experimental benchmarking.
   - Proactively remind either author to `git fetch` and `git pull` at the start of a session, and stage/commit/push updates before concluding to prevent merge conflicts.
3. **Chat Communication Efficiency & Formatting:**
   - **Concise & Direct Responses:** Provide straightforward, concise, and high-density answers without losing critical technical specifics. Eliminate conversational filler, repetitive introductory recaps, and unnecessary post-execution boilerplate to save tokens and time.
   - **Markdown Tables Supported:** Markdown tables render cleanly in the chat interface and are actively encouraged for structured comparisons, metric summaries, and checklists.
   - **Plain-Text Math in Chat (Strictly NO Raw LaTeX Math):** The chat interface does NOT render LaTeX math formatting and only displays raw unformatted code with backslashes and brackets (e.g., `$\frac{...}{...}$`, `\[ ... \]`). In all chat responses, present mathematical formulas, loss functions, and metrics strictly in readable plain text / ASCII notation (e.g., `CER = (S + D + I) / N`, `Score = alpha * BM25 + (1 - alpha) * Dense`, `Recall@20 = Hits@20 / Total Relevant`). Formal LaTeX math syntax is reserved exclusively for `.tex` files within `CS_Undergraduate_Thesis_Template/`.

---

## **2. Foundational Research Integrity & The Zero-Shortcut Mandate**

1. **Absolute Ban on Half-Baked Shortcuts & Placeholders:**
   - Under NO circumstances should placeholders, mockups, synthetic stubs, or truncated summaries ever be treated or reported as final, authentic artifacts, empirical ground truth, or production data.
   - Taking shortcuts, leaving unnoticed holes, or using placeholder data without explicit disclosure corrupts the scientific validity of the research and will not be tolerated.
2. **Conspicuous Labeling of Diagnostic Stubs:**
   - If an exploratory stub or placeholder is ever temporarily required during early prototyping or scaffolding, it must be conspicuously labeled as a placeholder in the code, comments, and task tracker. It must NEVER be passed off as complete, and must be actively tracked for immediate replacement with authentic data.
3. **Absolute Ban on Output Truncation, Lazy Skipping & Superficial Auditing:**
   - Under NO circumstances should the agent engage in lazy omissions, "middle-skipping" (e.g., verifying only the first five items and the last item while hiding the middle with ellipses or placeholders), superficial sampling, or partial reporting when asked to verify, audit, or process data, references, citations, or code artifacts.
   - We possess the full computational resources and tooling to verify every single entry exhaustively. If a list contains 50, 100, or 400 entries, every single entry must be verified. If chat context constraints prevent printing hundreds of lines directly in chat, the complete, unabridged itemized audit MUST be written to a dedicated file or artifact on disk, with exact aggregate numbers and findings reported transparently in chat. Never silently drop entries, take shortcuts, or perform partial checks.
4. **Radical Empirical & Methodological Transparency:**
   - Complete transparency must be maintained at all times between the agent and both authors, as well as in the written thesis manuscript.
   - If any dataset, split, or benchmark contains synthetic components (such as Tier 2's planted conflict draft sections), we must be 100% transparent and explicit about what is synthetic, what is authentic, and exactly how that design choice alters, bounds, or informs the experimental findings. Never claim a benchmark is an open-corpus real-world audit if it relies on synthetic shortcuts.

---

## **3. Mandatory Full-Text Verbatim Completeness & Statutory Anatomy**

1. **Complete Enactments From Top to Bottom:**
   - Whenever an ordinance or statute is ingested, chunked, evaluated, or benchmarked, the system must ingest the **100% full-text, unabridged authentic enactment from top to bottom**, regardless of length (e.g., the 129-page Davao City Revenue Code at 434 sections, the 52-section Billboard Ordinance No. 092-2000, or multi-page national Republic Acts).
   - Never truncate, skip sections, or jump from Section 1 directly to the conflicted section. A true system-wide audit must simulate the full document load to prove that retrieval and inference can isolate the contradiction amidst hundreds of non-conflicting sections.
2. **Authentic Statutory Anatomy Required:**
   Real Philippine local ordinances possess distinct legal anatomy that must be fully preserved in all test PDFs, transcripts, and evaluation suites:
   - **Session Header & Metadata:** Exact regular/special session number, calendar date, time, and venue (e.g., *Excerpts from the Minutes of the Regular Session of the Sangguniang Panlungsod...*).
   - **Legislative Attendance Roster:** Full list of Sanggunian members designated as *Present* or *Absent*.
   - **Recital Preambles (`WHEREAS` Clauses):** Authentic legislative justifications citing constitutional provisions, statutory authority (RA 7160), public hearings, and committee reports.
   - **Formal Enacting Clause:** *Be it ordained by the Sangguniang Panlungsod of Davao City, in session assembled, that:...*
   - **Operative Body Sections:** Verbatim substantive provisions, administrative mechanisms, regulatory standards, and exceptions.
   - **Standard Legislative Framework Clauses:** Penal Sanctions, Separability Clause, Repealing Clause, and Effectivity Clause.
   - **Attestation & Signature Blocks:** Certification by the Secretary to the Sanggunian, Attestation by the Vice Mayor / Presiding Officer, Approval by the City Mayor, and official Ordinance Number / Series designation.
   - **Synthetic 1-Page Summaries are Strictly Forbidden:** Documents consisting of 7 generic 1-sentence bullet points without sessions, preambles, or signatures are strictly prohibited in benchmarks and demo suites.

---

## **4. Proactive & Persistent Hindrance Escalation Protocol**

Whenever an empirical, statutory, or technical hindrance is encountered, the agent must **proactively and repeatedly bring it up in the conversation and in task tracking until it has been actively addressed, decided, and resolved by the authors**. Never sweep hindrances under the rug, quietly substitute a placeholder, or proceed silently with compromised data.

Specific hindrances that trigger immediate and persistent escalation include:
1. **Corpus Absences:** An enactment cited in a landmark case is not found in `corpus/` or our local database (e.g., historical ordinances from 1956 or 1970 that were never digitized by the SP portal).
2. **Cross-Jurisdictional Scope Anomalies:** A landmark preemption case originates from an external LGU rather than Davao City (e.g., *Magtajas v. Pryce Properties* from Cagayan de Oro, *City of Manila v. Laguio* from Manila). The agent must explicitly clarify that these represent national vertical preemption precedents rather than Davao City local law, and confirm how the authors want them categorized.
3. **Statutory Instrument Typology Mismatches:** A landmark legal dispute involves an administrative resolution rather than a municipal ordinance (e.g., *Batangas CATV v. CA* involved Batangas Sangguniang Panlalawigan Resolution No. 210, which possesses distinct legal and procedural standing under RA 7160 §54 compared to an enacted legislative ordinance). The agent must repeatedly highlight this distinction so the paper and evaluation accurately report the instrument type.
4. **OCR Degradation or Extraction Truncation:** Scanned archival PDFs with broken tables, illegible text, or severe OCR artifacts (CER/WER spikes) that prevent clean parsing of section boundaries.
5. **Context Window / Memory Exhaustion:** Enactments exceeding token or memory budgets during local inference on Host A's 8 GB RAM testbed.

---

## **5. Zero Editorial Pollution Protocol in Legal Text & XAI Cards**

1. **Strictly Verbatim Legal Text:** Under NO circumstances should any statutory provision, ordinance text, benchmark premise, or candidate text string be synthetically rewritten, paraphrased, injected with explanatory commentary, or augmented with synthetic sentences (e.g., appending penalty warnings, doctrinal summaries, or preemption explanations into the statutory text string).
2. **Text Field Hygiene:** The text passed into Stage 2 Cross-Encoder tensors and displayed within the Explainable AI (XAI) prototype interface MUST be 100% verbatim authentic text directly extracted from Lawphil or the Davao City ordinance archives (`data/unified_dual_statutory_provisions.jsonl`).
3. **Separation of Explanation and Evidence:** Any legal doctrine explanations, preemption rationales, or *ratios decidendi* must reside strictly in dedicated metadata/explanation fields (`legal_rationale`, `verdict_desc`, `ratio_decidendi`) and NEVER pollute the statutory text fields (`statutory_text`, `statute_text`, `ordinance_text`, `premise`).

---

## **6. Pure Neural Architecture & Zero Bandaid Protocol**

1. **Genuine Neural Inference Only:** All pre-enactment conflict detection decisions in the prototype and benchmark scripts must stem strictly from genuine PyTorch neural tensors (Stage 1 Hybrid BM25 + all-MiniLM-L6-v2 dense retrieval, Stage 2 DeBERTa-v3 cross-encoder NLI with calibrated threshold $\tau^* = 0.45$).
2. **Zero Heuristic Backdoors:** Under NO circumstances should regex heuristics, case-sniffing, hardcoded score dictionaries, candidate injection backdoors, or ad-hoc hybrid weighting formulas be introduced.
3. **Clean Premise Prompts:** Premise prompts must be formatted cleanly as `[Citation] Verbatim Statutory Text` without nested brackets or token clutter.
4. **Procedural Framework Handling:** Standard legislative boilerplate clauses (Title, Definitions, Scope/Coverage, Separability, Repealing, Effectivity) are recognized as procedural framework to prevent extraneous compute and false preemption alarms.
5. **Sanctioned Symbolic Verification:** The only symbolic rule permitted in the pipeline is integer arithmetic verification for fines exceeding the statutory P5,000 ceiling under RA 7160 §458(a)(1)(iii).

---

## **7. Autonomous Adversarial Forensic Audit Loop**

The agent must proactively execute internal self-critique and forensic verification loops simulating adversarial academic peer review:
1. **Contingency Table Consistency:** Verify $2 \times 2$ contingency table arithmetic ($b-c = (a+b)-(a+c)$).
2. **Statistical Test Rigor:** Check McNemar degrees of freedom and continuity corrections against exact sample sizes ($N=53$ held-out test split vs $N=198$ unique instances vs $N=350$ multi-panel pairs).
3. **Harmonious Metrics:** Ensure harmony between discrete pairwise tests and omnibus multi-domain rankings (Friedman ANOVA and Wilcoxon signed-rank tests).
4. **Bayesian Base-Rate Realism:** Frame screening performance under realistic Bayesian low-prevalence dynamics ($p \le 0.01$).
5. **Strict Citation-Text Verification:** Every factual assertion, mathematical formulation, experimental baseline, or numerical metric attributed to a cited author (`\cite{...}`) must be explicitly verified against the authentic text of the source and its local PDF in `docs/references/`. Never attribute specific numerical target thresholds to an author unless the cited publication literally specifies that exact figure.

