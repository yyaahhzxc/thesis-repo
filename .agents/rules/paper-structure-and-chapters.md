---
trigger: model_decision
description: Apply alongside ALL other paper-*.md rules when drafting, editing, reorganizing, or sweeping thesis chapters, appendices, or front matter in CS_Undergraduate_Thesis_Template/. Covers structural flow, heading caps, Curse of Knowledge chapter boundaries, appendices, abstract limits, and chapter checklists.
---

# **Paper Structure, Chapter Boundaries & Appendix Standards**

**Scope:** Structural rules for `CS_Undergraduate_Thesis_Template/`. When running a **full-paper sweep or major chapter revision**, read and enforce all four rules together: `paper-structure-and-chapters.md`, `paper-voice-and-style.md`, `paper-rigor-and-citations.md`, and `paper-latex-and-visuals.md`.

---

## **1. Operational Editor Discipline**

1. **Direct In-File Action:** Apply edits cleanly and directly to `.tex` files without conversational filler or post-edit recaps.
2. **Preserve Architecture:** Keep existing section hierarchies, `\label{...}`, `\cite{...}`, and `\ref{...}` intact unless structural reorganization is requested.
3. **End-State Integration:** Every edit must read as if conceived in the original draft—eliminate defensive signposting, edit trails, and sudden shifts like *"notably,"* *"specifically,"* or *"as requested"*.
4. **Subfile Root Header:** Every file in `chapters/` and `appendices/` must begin with `% !TeX root = ../main.tex`.
5. **Living Glossary Sync:** Append any newly introduced technical, legal, statistical, or ML terms/metrics/doctrines to `docs/GLOSSARY.md` with plain-language definitions and thesis context.
6. **Ban on Fourth-Wall Breaks:** Never mention course milestones, syllabus requirements, professor instructions, teacher prompts, grading rubrics, or submission deadlines in thesis prose. Frame every methodology and experiment as an intentional scientific decision.

---

## **2. Heading Hierarchy, Titles & Paragraph-Driven Flow**

1. **Maximum 3 Heading Levels:** `\chapter` (0) $\rightarrow$ `\section` (1) $\rightarrow$ `\subsection` (2) $\rightarrow$ `\subsubsection` (3). **NEVER** use `\paragraph` or `\subparagraph` as numbered or level-4 section headers.
2. **Structural Symmetry (No Orphan Subsections):** Whenever a section or subsection is subdivided, it must contain at least two child units (e.g., `\subsubsection{A}` requires `\subsubsection{B}`).
3. **Simplified Single-Line Titles:** Keep section, subsection, and subsubsection titles concise and on a single line (e.g., `\subsection{Candidate Retrieval Ablation}` instead of long multi-clause or parenthetical titles).
4. **Paragraph-Driven Prose (No Unnecessary Inline Headings/Lists):** Eliminate artificial bulleted lists, inline bold subheaders, and heavy `description` environments (`\item[Topic.]`) when not strictly required. Write continuous academic paragraphs and integrate each concept directly into the opening topic sentence.

---

## **3. Chapter Boundaries (Avoiding the "Curse of Knowledge")**

Maintain strict chronological and narrative separation across chapters—never write early chapters with hindsight or leak downstream model winners before they are evaluated:

* **Chapter 1 (Introduction):** Establishes the problem statement, local governance context, ex-ante motivation, research objectives, and high-level scope/limitations without declaring experimental winners, hyperparameters, or hindsight results.
* **Chapter 2 (Review of Related Literature):** Strictly objective scholarly survey of jurisprudence, statutory drafting conventions, IR paradigms, and NLI benchmarks. **NEVER** write with hindsight or announce pipeline choices (avoid *"this has consequences for our pipeline"* or *"the researchers chose Path 1"*). Frame broad computational or document-cleaning implications objectively without assuming downstream implementation knowledge.
* **Chapter 3 (Methodology):** Translates Chapter 2 into an operational research plan—defining system architecture, math formulations, screening protocols, and experimental design strictly in the **planning phase** without reporting actual execution results, finalist rankings, or empirical outcomes.
* **Chapter 4 (Results and Discussion):** Executes the Chapter 3 plan and reports empirical findings, ablation outcomes, loss curves, and error analyses. **Structural Alignment:** Arrange sections in direct correspondence with the Statement of the Problem and Research Objectives in Chapter 1 so every question and objective receives a dedicated empirical answer.

---

## **4. Abstract, Front Matter & Appendix Standards**

1. **Strict Abstract Limit ($\le 250$ Words):** Format as a single cohesive academic paragraph with no bullets or numbered lists. Eliminate parenthetical bloat while keeping essential anchors: research dilemma, Davao City, dual statutory corpus (`27,248` enactments, `177,423` provisions), two-stage architecture, zero-leakage premise-grouped CV accuracy (`86.44% ± 6.05%`) and Conflict $F_1$ (`0.8945`), Host A latency (`12.69 s`), RAM (`1,416.4 MB`), and Tier 2 open-corpus detection (`2` of `7` planted conflicts caught with `6` false alarms, `39` of `45` compliant sections cleared at `86.67%` specificity; `7` of `7` detected under oracle candidates).
2. **Front Matter TOC Registration:** Register Table of Contents, List of Figures, List of Tables, List of Listings, and List of Equations in the TOC with Roman numeral sequencing via `\addcontentsline{toc}{chapter}{...}`.
3. **Appendix Running Header Clearance (+45 pt Rule):** Keep appendix chapter titles concise. If over ~35 characters, supply `\chapter[Short Title]{Full Descriptive Title}` or `\chaptermark{Short Title}` so uppercase `\pagestyle{headings}` headers leave at least **+45 pt** of clear whitespace before the page number.
4. **Appendix Artifacts-Only Format (No Appendix Discussion):** Appendices hold supplementary artifacts (figures, tables, code, notebooks, forms, evaluation catalogs) with brief, factual descriptive captions (`\caption[Short]{Descriptive}`) stating scope/counts only. **NEVER** include analytical discussion, interpretative multi-paragraph narrative, or `\textit{Note:}` blocks inside appendices (all interpretation belongs in Chapters 4 and 5).
5. **Active Appendix Cross-Referencing:** Every active appendix must be cited (`Appendix~\ref{app:...}`) in Chapters 1–5; avoid orphaned appendices.
6. **Institutional AI Disclosure Placement (Appendix R Only):** Embed the verified 2-page university AI disclosure form (`statement_of_authorship_and_ai_disclosure_filled.pdf`) exclusively in the terminal appendix alongside the 5 human oversight pillars and experimental model boundaries. **NEVER** insert a standalone disclosure statement after the Bibliography.

---

## **5. Chapter-Specific Structural Checklists**

* **Chapter 1 (Introduction):** Background (Fuller's consistency, legal inflation, unitary hierarchy, *Magtajas v. Pryce*, ex-ante necessity, LGU OCR noise); 5 formal Research Questions; General + 5 specific Objectives; Significance (SP, LegalNLP research, public); Scope & Limitations (national laws + `1,816` deduplicated Davao City ordinances, English-only, single-premise asymmetric spans, white-box XAI, consumer hardware); Definition of Terms (alphabetical `description` list).
* **Chapter 2 (Literature Review):** Legal Informatics & Conflict Detection $\rightarrow$ Statutory IR $\rightarrow$ NLI & Textual Entailment $\rightarrow$ COLIEE Paradigm $\rightarrow$ Philippine Legal Corpora & OCR Degradation $\rightarrow$ Research Gap & Synthesis; include structured comparative literature tables.
* **Chapter 3 (Methodology):** Conceptual Framework (IPO, Phase 1 Offline vs Phase 2 Live); Research Design; Data Acquisition (Lawphil `25,432` + SP/LISSP `1,816`); Preprocessing (OCR normalization, boundary chunking); Ground Truth (`N = 350`, 8 macro domains, batched SP annotation, Fleiss' $\kappa$); Hardware & Non-Generative Constraints; Candidate Model Specs (`70/15/15` split, premise-grouped CV, two-stage retrieval + cross-encoder); Evaluation Metrics; Prototype GUI & XAI Design.
* **Chapter 4 (Results and Discussion):** Direct alignment to RQ1–RQ5 / Obj 1–5 (Archival OCR/VLM benchmark, Local/Dual Corpus EDA & Topic Modeling, Stage 1 Retrieval Ablation, Stage 2 Zero-Shot & Fine-Tuning + Premise-Grouped CV + Statistical Validation, XAI Attention Saliency, Tier 2 Full-Document & Knowledge Graph Ablation, Tier 3 Supreme Court & Open-Corpus Full-PDF Benchmark, Edge Hardware Profiling).
* **Chapter 5 (Conclusions and Recommendations):** Direct synthesis per RQ/Objective, grounded system/methodological limitations within scope, and concrete technical/institutional recommendations.
