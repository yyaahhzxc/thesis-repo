---
trigger: always_on
description: This rule mandates that the agent must always inspect, maintain, and update the master thesis task tracking document (docs/THESIS_MASTER_TASKS.md) to preserve cross-session continuity, track progress across both the LaTeX manuscript and Python codebase, and ensure all milestone requirements are rigorously fulfilled.
---

# **Master Task Tracking & Cross-Session Continuity Protocol**

**Institution:** Ateneo de Davao University, Department of Computer Science  
**Project:** *"A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference"*  
**Authors:** Ralph Paolo Dulce & Yahyah Odin  
**Adviser:** Mr. Adrian "Ogs" Ablazo | **Professor:** Ma'am Grace Tacadao  

---

## **1. Author Identity & Collaborative Multi-User Handling**

**Thesis Proponents:**
* **Yahyah Odin ("Yah")**: Co-author leading machine learning modeling, retrieval benchmarking, manuscript drafting, and pipeline automation. Operates primarily on **Host A (Desktop)** (Core i3-10105F, Radeon RX 6600, 8 GB RAM, Windows) for LGU edge simulation.
* **Ralph Paolo Dulce ("Ralph")**: Co-author leading local ordinance OCR experiments, human evaluation deployment (Google Forms, 15 SP legal researchers), administrative routing (HRMO / City Administrator), and collaborative manuscript drafting. Operates primarily on **Host B (GPU Laptop)** (Lenovo Legion 5: Ryzen 7 7435HS, RTX 5050 Laptop GPU, 16 GB RAM, Windows) for deep learning training and experimental benchmarking.

**Operational Greeting & Execution Behavior:**
Both Ralph and Yah are first-class proponents with full, equal access to all Antigravity capabilities (code authoring, script execution, benchmark evaluation, LaTeX manuscript drafting, PDF compilation, task tracking, and administrative document preparation).
1. **When User is Identified as Yah ("I'm Yah", "Yah here", etc.):**
   - Immediately recognize Yah as co-author.
   - Ground directly into `docs/THESIS_MASTER_TASKS.md`, provide a rapid progress briefing, execute tasks with precision, and update tracking checklists and journals as work progresses.
2. **When User is Identified as Ralph ("I'm Ralph", "Ralph here", etc.):**
   - Immediately recognize Ralph as co-author.
   - Ground directly into `docs/THESIS_MASTER_TASKS.md`, present a crisp progress briefing on recent manuscript/codebase updates, highlight Ralph's active action items as well as shared tasks, and execute any requested work (coding, OCR experiments, manuscript writing, survey design, or LaTeX compilation) with the exact same technical depth and rigor as for Yah.
   - Proactively suggest Ralph's active action items when he asks what to work on:
     * **Manual Reference PDF Collection & Verification (Collaborative with Yah):** Use the Reference Auditor dashboard (`http://127.0.0.1:8080/docs/ref_auditor.html`) to help collect and drag-and-drop remaining cited reference PDFs into `docs/references/`.
     * **Audit Flagged Sources & Manuscript Text Adjustments:** Review the sources flagged as unobtainable (in `docs/flagged_references.json` or exported via `Export Flagged`), and collaborate on either finding substitute sources or adjusting the manuscript text in Chapters 1--4 to remove or replace citations.
     * **Local Ordinance OCR Empirical Experiments:** Finalize the empirical comparison across Tesseract, Surya, Google Cloud Vision, and local 4-bit Qwen2.5-VL-3B-Instruct.
     * **HRMO / City Administrator Routing & Legal Researchers Certificates:** Advance the administrative routing packet (`docs/annotation/hrmo_city_admin_approval_request_letter.md`) and certificate layout.
3. **When No Name is Specified:**
   - Default to checking `docs/THESIS_MASTER_TASKS.md` immediately, maintain full situational awareness, and execute requests while preserving continuous task synchronization.
4. **Cross-Host Git Synchronization Protocol:**
   - Because Yah and Ralph develop collaboratively on separate machines (Host A and Host B), proactively remind either author to `git fetch` and `git pull` at the start of a session, and stage/commit/push updates before concluding, ensuring working directories remain synchronized without merge conflicts.
5. **Ordinance Text Update & Empirical Re-Run Trigger:**
   - Whenever Ralph pushes updates to ordinance texts (e.g., in `cleaned_transcriptions/`, `corpus/city_ordinances/`, or `data/unified_dual_statutory_provisions.jsonl`) resulting from his manual archival verification and OCR checks, immediately re-run the relevant exploratory data analysis (EDA), word/token counts, temporal distributions (`scripts/generate_word_count_temporal_figure.py`), dual-corpus token compliance metrics, and any downstream retrieval or NLI evaluation scripts affected by the updated text upon pulling.
   - Verify if any reported statistics, tables (e.g., Table 3.2, Table 3.3, Table 4.1, Table 4.3), or figures in Chapters 3 and 4 shift due to the updated text, and synchronize the manuscript accordingly.
6. **Chat Communication Efficiency & Formatting Protocol (Yah & Ralph Directives):**
   - **Concise & Direct Responses:** Provide straightforward, concise, and high-density answers without losing critical technical specifics. Eliminate conversational filler, repetitive introductory recaps, and unnecessary post-execution boilerplate to save tokens and time.
   - **Markdown Tables Supported:** Markdown tables render cleanly in the chat interface and are actively encouraged for structured comparisons, metric summaries, and checklists.
   - **Plain-Text Math (No Raw LaTeX Math in Chat):** The chat interface does NOT render LaTeX math formatting and only shows raw unformatted code with backslashes and brackets (e.g., `$\frac{...}{...}$`, `\[ ... \]`). In all chat responses, present mathematical formulas, loss functions, and metrics strictly in readable plain text / ASCII notation (e.g., `CER = (S + D + I) / N`, `Score = alpha * BM25 + (1 - alpha) * Dense`, `Recall@20 = Hits@20 / Total Relevant`). Reserve formal LaTeX math syntax exclusively for `.tex` files within `CS_Undergraduate_Thesis_Template/`.

---

## **2. Standing Operational Context & External Dependencies**

The agent must maintain awareness of the following operational realities without requiring repeated user updates:
1. **Dual Statutory Corpus Architecture (27,096 Records, 176,421 Provisions):** The complete dual statutory knowledge base combines 25,432 national statutes (Lawphil) and 1,664 Davao City local ordinances (SP portal & LISSP), totaling **27,096 enactments and 176,421 searchable provisions** compiled in `data/unified_dual_statutory_provisions.jsonl`.
2. **Dual Conflict Detection Scope (Vertical & Horizontal):**
   - *Vertical Conflict Detection (Statutory Preemption):* Comparing draft local ordinances against superior national laws under the *Magtajas v. Pryce Properties* doctrine and RA 7160 §5(a) (an ordinance cannot permit what a statute forbids, or forbid what a statute permits).
   - *Horizontal Conflict Detection (Intra-Jurisdictional Coherence):* Comparing draft local ordinances against existing, fellow Davao City ordinances to ensure the draft does not contradict, duplicate, or inadvertently cause implied repeal of active local legislation.
3. **Local Ordinances Digitization & Cleaning (Completed):** Ralph and Yah completed physical/PDF scanning and OCR cleaning of exactly 1,664 Davao City local ordinances (from SP portal and LISSP 2021--2026), compiled to `corpus/city_ordinances/categorized_davao_ordinances.jsonl`.
4. **Local Ordinances EDA (Completed in Chapter 3):** Exploratory Data Analysis—including temporal distribution across four legislative eras, 6-class functional typology, document length asymmetry, and 94.69% 512-token compliance—is fully written into Chapter 3 (§3.2.4 & §3.2.5) with Figures 3.5 & 3.6 and Tables 3.2 & 3.3.
5. **Local Ordinances Empirical Experiments (Ralph Lead):** Ralph leads the empirical experiments comparing traditional scanner OCR vs. local LLM/VLM text extraction fidelity (Character Error Rate, Word Error Rate, structural table preservation).
6. **HRMO & City Administrator Approval Routing (Active):** Sangguniang Panlungsod response received (Sept 28, 2026, signed by Acting Dept. Head II Ma. Theresa A. Reyes) appreciating the study and referring approval of the thesis and 15 legal researchers to the City Administrator's Office via the Human Resource Management Office (HRMO). The formal request packet (`docs/annotation/hrmo_city_admin_approval_request_letter.md`) is drafted and being routed.
7. **Adviser Consultation Pending (Sir Ogs):** The proponents are preparing for a consultation with thesis adviser Mr. Adrian "Ogs" Ablazo for methodology verification and review of recent revisions.
8. **Professor Directive on Formatting (Ma'am Grace Tacadao, Sept 30, 2026):** Eliminate unnecessary inline headings, description lists (`\item[...]`), and enumerated outlines across thesis chapters; format discussions as continuous, cohesive academic paragraphs with topics naturally integrated into topic sentences.
9. **Scope Modification Inquiry (Problem Statement & Objective 5 / Legal Researchers Evaluation):** Proponents inquired with course professor Ma'am Grace Tacadao regarding potentially modifying or relaxing Problem Statement 5 and Research Objective 5 (post-interaction usability and usefulness evaluation with 15 SP legal researchers) due to timeline and administrative routing constraints. Ma'am Grace advised that this modification is possible due to time constraints, but requires formal consultation and written/signed approval from thesis adviser Mr. Adrian "Ogs" Ablazo and the thesis defense panel.
10. **Annotator Recognition Protocol (Civil Service 201 Records):** Course professor Ma'am Grace Tacadao approved providing an official Certificate of Contribution and Commendation to the 15 SP legal researchers who successfully complete their 70-pair annotation workload, structured specifically for inclusion in their official Civil Service 201 personnel records to provide meaningful institutional recognition. Ralph leads certificate visual layout and signature routing (Ma'am Grace, Sir Ogs, Dr. Oneil, Ralph, Yah; defense panelists marked as `[?] Pending Confirmation`).
11. **Instruction & Algorithm Code Grounding (Ma'am Grace Tacadao, Sept 30, 2026):** Only present instructions, pseudocode, and algorithms in the manuscript that are actually implemented, executed, and functional within the project codebase (`src/`, `scripts/`). Never include speculative, unused, or generic textbook algorithms.
12. **Equation-Algorithm Non-Redundancy & List of Equations Integration (Oct 1, 2026):** If an equation is already embedded within an algorithm listing, do not redundantly highlight or isolate it. Formal display equations across the manuscript are titled, captioned via `\eqcaption{...}`, aggregated into the front matter *List of Equations* (`\listofequations`), and formatted with `\noindent Where ...` to eliminate unwanted paragraph indentation on variable breakdowns.


---

## **3. Core Principle & Agent Operational Mandate**

To ensure seamless progress across multiple conversations and prevent repetitive context re-prompting:
1. **Living Source of Truth:** The file [`docs/THESIS_MASTER_TASKS.md`](file:///c:/Users/SHRIMP/Documents/thesis-repo/docs/THESIS_MASTER_TASKS.md) serves as the persistent, centralized record of all completed, active, and pending tasks across the thesis manuscript, codebase, empirical benchmarks, and milestone submissions.
2. **Mandatory Check on Conversation Start:** At the beginning of any new conversation or before undertaking major additions or revisions, the agent must check `docs/THESIS_MASTER_TASKS.md` to ground itself in the active milestone, recent progress, open questions, and pending deliverables.
3. **Atomic Task Updates:** Whenever any task, code implementation, empirical experiment, or LaTeX revision is completed, the agent must immediately update `docs/THESIS_MASTER_TASKS.md`, changing status indicators (`[ ]` $\rightarrow$ `[x]` or `[-]`), logging relevant commit/file references, and updating the progress timestamp.
4. **Verbatim Instruction Preservation:** Whenever the user provides instructions for a new milestone (e.g., Milestone 2, Milestone 3, Final Defense), the agent must record the full, unabridged instructions verbatim in `docs/THESIS_MASTER_TASKS.md` under a dedicated milestone section to preserve complete contextual fidelity for future turns.
5. **Living Glossary Synchronization:** Whenever new technical, legal, statistical, or machine learning terms, metrics, algorithms, or doctrines are introduced to the manuscript or codebase, the agent must immediately append them to [`docs/GLOSSARY.md`](file:///c:/Users/SHRIMP/Documents/thesis-repo/docs/GLOSSARY.md) with an accessible, plain-language definition and practical thesis context.

---

## **4. Master Tracking Document Structure (`docs/THESIS_MASTER_TASKS.md`)**

The master tracking document must maintain the following core sections:
1. **Executive Status & Active Milestone Banner:** High-level summary of active focus, deadlines, and current system status.
2. **Exact Hardware & Software Environment Reference:** Canonical specifications of the local LGU simulation testbed (CPU, GPU, RAM, OS, Python version, key library versions).
3. **Repository & Version Control Details:** Canonical repository URL, branch structure, and reproducibility setup.
4. **Verbatim Milestone Instructions Archive:** Complete, unedited milestone prompts provided by the course professor.
5. **Milestone-by-Milestone Audit & Task Checklist:** Granular, checkable action items categorized by:
   * **LaTeX Thesis Manuscript (`CS_Undergraduate_Thesis_Template/`)**
   * **Core Engine, Models & Scripts (`src/`, `scripts/`)**
   * **Evaluation Benchmark & Human Annotation (`data/`, `docs/annotation/`)**
   * **Documentation, Reproducibility & Build Validation (`README.md`, `requirements.txt`)**
6. **Task Status Legend:**
   * `[x]` **Completed**: Fully implemented, documented, and verified.
   * `[-]` **In Progress**: Actively being drafted, coded, or benchmarked.
   * `[ ]` **Pending**: Planned work scheduled for the active or upcoming milestone.
   * `[?]` **Requires Verification / Consultation**: Awaiting user, adviser, or professor decision.
7. **Change Log / Chronological Milestone Journal:** Brief date-stamped summaries of what was accomplished in each session.

---

## **5. Agent Updating Protocol**

* **Keep It Synchronized with Git:** All updates to `docs/THESIS_MASTER_TASKS.md` must be committed and pushed alongside the associated code or manuscript edits.
* **Never Delete Completed History:** When tasks are finished, mark them as `[x]` with a brief note or link to the corresponding file/section. Do not purge completed milestones, as they provide critical traceability and defense review records.
* **Proactive Next-Step Signaling:** At the conclusion of each response, the agent should briefly reference the next pending item from `docs/THESIS_MASTER_TASKS.md` to maintain momentum.
