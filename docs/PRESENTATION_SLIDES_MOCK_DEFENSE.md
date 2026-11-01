# Presentation Slides: Initial Presentation & Mock Defense
### Computer Studies Cluster, School of Arts and Sciences
### Ateneo de Davao University
**Course:** Bachelor of Science in Computer Science (BS CS)  
**Time Allotted:** 20 Minutes (Strict) | Target Presentation: ~16--17 mins + Q&A Buffer  
**Proponents:** Ralph Paolo Dulce & Yahyah Odin  
**Thesis Adviser:** Mr. Adrian "Ogs" Ablazo | **Professor:** Ma'am Grace Tacadao  

---

## Presentation Flow & Speaking Split

| Slide | Topic | Primary Speaker | Slide Visual Type | Est. Time |
| :---: | :--- | :---: | :---: | :---: |
| **1** | Title & Introduction | Ralph | Metadata Banner | 1.0 min |
| **2** | Chapter 1: Introduction | Ralph | Title-Only Divider | 0.5 min |
| **3** | Background of the Study | Ralph | **Side-by-Side:** Scan (`sample_davao_city_ordinance_scan.png`) + 7x7 Bullets | 1.5 mins |
| **4** | Problem Statement | Ralph | Text Layout (Verbatim Reading) | 1.5 mins |
| **5** | Objectives of the Study | Ralph | Text Layout (Verbatim Reading) | 1.0 min |
| **6** | Chapter 3: Methodology | Ralph to Yah | Title-Only Divider & Speaker Handoff | 0.5 min |
| **7** | Conceptual Framework: Overview | Yah | **Full Flowchart:** Bird's-Eye View (`conceptual_framework_flowchart.png`) | 1.0 min |
| **8** | Phase 1: Dual Corpus Ingestion | Yah | **Multi-Panel:** Full Flowchart (Right) + Component (`cf_phase1_ingestion.png`) + 7x7 Bullets | 0.5 min |
| **9** | Phase 1: Model Benchmarking | Yah | **Multi-Panel:** Full Flowchart (Right) + Component (`cf_phase1_benchmarking.png`) + 7x7 Bullets | 0.5 min |
| **10** | Phase 2: System Input | Yah | **Multi-Panel:** Full Flowchart (Right) + Component (`cf_phase2_input.png`) + 7x7 Bullets | 0.5 min |
| **11** | Phase 2: Stage 1 Retrieval | Yah | **Multi-Panel:** Full Flowchart (Right) + Component (`cf_phase2_stage1.png`) + 7x7 Bullets | 0.5 min |
| **12** | Phase 2: Stage 2 Inference | Yah | **Multi-Panel:** Full Flowchart (Right) + Component (`cf_phase2_stage2.png`) + 7x7 Bullets | 0.5 min |
| **13** | Phase 2: System Output & Explainability | Yah | **Multi-Panel:** Full Flowchart (Right) + Component (`cf_phase2_output.png`) + 7x7 Bullets | 0.5 min |
| **14** | Statutory Corpus: National Legislation | Yah | **Full Screenshot:** Lawphil Digital HTML Platform (`lawphil_republic_act_sample.png`) | 0.5 min |
| **15** | Statutory Corpus: Local Legislative Scans | Yah | **Side-by-Side:** Modern Scan vs. Degraded Scan (`davao_ordinance_scan_sample.png` & degradation) | 0.75 min |
| **16** | Statutory Corpus & Acquisition | Yah | Text Layout: Corpus Inventory & Topic Modeling | 0.75 min |
| **17** | Ground Truth Benchmark Construction | Yah | Text Layout: 350-Pair Stratified Dataset & 15-Expert Study | 1.0 min |
| **18** | Model Selection & Optimization | Yah | Text Layout: Candidate Model Screening & Threshold Tuning | 1.0 min |
| **19** | Evaluation Metrics & Statistical Testing | Yah | Text Layout: IR/NLI Metrics & Hypothesis Testing Framework | 1.0 min |
| **20** | Chapter 4: Results & Discussion | Ralph | Title-Only Divider & Speaker Handoff | 0.5 min |
| **21** | Archival OCR & Local VLM Benchmark | Ralph | **Performance Table:** Table 4.1 CER/WER & Error Cascades | 1.5 mins |
| **22** | Post-Digitization Corpus Analysis & EDA | Yah | **Distribution Plot:** Figure 4.5 512-Token Transformer Compliance | 1.0 min |
| **23** | Stage 1 Candidate Retrieval Benchmark | Yah | **Ablation Curve:** Figure 4.6 Retrieval Recall@k & MRR | 1.5 mins |
| **24** | Stage 2 Cross-Encoder NLI & Statistics | Yah | **Significance Card:** Table 4.10/4.11 DeBERTa F1 & Friedman ANOVA | 1.5 mins |
| **25** | Supreme Court Precedents & Latency | Ralph | **Case Matrix:** Table 4.18 Preemption Suite & Latency Curve | 1.5 mins |
| **26** | **Live Technical System Demonstration** | Ralph & Yah | **Interactive Walkthrough:** Live Screen Share (`http://127.0.0.1:5050`) | 3.0 mins |
| **27** | Chapter 5: Conclusions & Synthesis | Ralph | **Scorecard Table:** Objectives 1 to 5 Completion Verification | 1.5 mins |
| **28** | Academic Limitations & Technical Roadmap | Ralph | Text Layout: Boundaries & Future Technical Extensions | 1.0 min |
| **29** | Administrative Routing & Next Steps | Ralph & Yah | **Routing Card:** SP Referral, HRMO & Civil Service 201 Certificate | 1.5 mins |

---

## Slide-by-Slide Presentation Content

---

### Slide 1: Title Slide
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Computer Studies Cluster | Ateneo de Davao University
* **Bottom-Left Paper Ref:** Title Page
* **Bottom-Right Slide:** Slide 1
* **Title:** A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances
* **Subtitle:** Using Information Retrieval and Natural Language Inference
* **Visual:** Ateneo de Davao University seal, thesis title banner, author credentials, adviser name

#### On-Screen Slide Content:
* Automated statutory conflict detection for local legislation
* Powered by hybrid information retrieval and cross-encoders
* Proactive **ex-ante evaluation** prior to formal enactment
* **Proponents:** Ralph Paolo Dulce & Yahyah Odin (BS Computer Science)
* **Adviser:** Mr. Adrian "Ogs" Ablazo | **Professor:** Ma'am Grace Tacadao

#### Spoken Script:
> "Good morning to the members of the evaluation panel, our thesis adviser Mr. Adrian Ablazo, and our course professor Ma'am Grace Tacadao. I am Ralph Paolo Dulce, and together with my co-author Yahyah Odin, we present our thesis entitled: *'A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference.'*
> 
> In this presentation, we will walk you through our legal motivation, research objectives, conceptual framework, exploratory data analysis from Chapter 3, our system methodology, and a live demonstration of our working prototype."

---

### Slide 2: Chapter 1: Introduction
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Computer Studies Cluster | Ateneo de Davao University
* **Bottom-Left Paper Ref:** Chapter 1
* **Bottom-Right Slide:** Slide 2
* **Title:** Chapter 1
* **Subtitle:** Introduction
* **Visual:** Minimal chapter title card with roadmap overview

#### On-Screen Slide Content:
* Background of the Study
* Research Problem Statement
* Formal Research Objectives

#### Spoken Script:
> "We begin with Chapter 1: Introduction, covering our real-world legal motivation, our formal research questions, and the concrete objectives guiding this study."

---

### Slide 3: Background of the Study
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 1. Introduction
* **Bottom-Left Paper Ref:** §1.1
* **Bottom-Right Slide:** Slide 3
* **Title:** Background of the Study
* **Visual:** Side-by-Side: Authentic Archival Typewriter Scan (`CS_Undergraduate_Thesis_Template/figs/sample_davao_city_ordinance_scan.png`) on the left, 7x7 Motivation Bullets on the right

#### On-Screen Slide Content:
* Local ordinances cannot contradict national statutes
* Overlooked legal conflicts make ordinances void
* Thousands of laws overwhelm manual review
* Scanned local archives suffer OCR noise
* Missed conflicts trigger costly legal disputes
* Ex-ante auditing prevents invalid enacted laws

#### Spoken Script:
> "To understand why we built this system, imagine what happens when a city council drafts a new ordinance—for example, regulating local transportation or setting municipal fees.
> 
> Under Philippine law and the *Magtajas Doctrine*, local governments only possess delegated powers. An ordinance cannot allow what a national law prohibits, nor can it ban what a national law allows. If a conflict slips through, that local ordinance is legally void from the moment it is signed.
> 
> But here is the real dilemma: how can city legal staff actually verify that a new draft is completely safe? Right now, they have to cross-reference thousands of pages of national codes and local history by hand. And as you can see on screen, our historical local ordinances from the past 70 years exist primarily as scanned paper documents—full of typewriter noise, faded ink, and ink stamps that break regular search engines.
> 
> When conflicts are missed, the result is costly court battles and confusion for everyday citizens. This is where our vision comes in: an **ex-ante audit**—meaning an evaluation done 'before the event.' By giving city council researchers an automated tool to screen drafts during committee review, we can catch and resolve conflicts before a measure is ever enacted into law."

---

### Slide 4: Problem Statement
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 1. Introduction
* **Bottom-Left Paper Ref:** §1.2
* **Bottom-Right Slide:** Slide 4
* **Title:** Problem Statement
* **Visual:** Structured problem statement layout (Exemption to 7x7 rule — exact text from paper)

#### On-Screen Slide Content:
This study is conducted to investigate the use of a multi-stage architecture to automate the manual auditing of proposed local legislation in Davao City. 

Specifically, the study aims to answer the following research questions:
* **Q1:** What are the specific linguistic parameters and structural markers that define a "semantic conflict" between a proposed local ordinance and existing local or national laws?
* **Q2:** How can a Coarse-to-Fine system be designed to efficiently retrieve relevant national and local statutes before performing deep logical inference on constrained LGU hardware?
* **Q3:** Which combination of a hybrid Information Retrieval (IR) algorithms and Natural Language Inference (NLI) models provides the highest accuracy when processing the specific hierarchy of Philippine legal texts?
* **Q4:** What is the empirical performance of the proposed pipeline when evaluated against a manually curated Ground Truth dataset of local and national conflict pairs?
* **Q5:** How usable and viable is the final system interface for key stakeholders within the Davao City Sangguniang Panlungsod?

#### Spoken Script:
> *(No script required — read verbatim from the on-screen slide text)*

---

### Slide 5: Objectives of the Study
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 1. Introduction
* **Bottom-Left Paper Ref:** §1.3
* **Bottom-Right Slide:** Slide 5
* **Title:** Objectives of the Study
* **Visual:** Objective matrix aligned with problem statements (Exemption to 7x7 rule — exact text from paper)

#### On-Screen Slide Content:
The primary goal of this research is to develop a computationally efficient, two-stage semantic conflict detection system for proposed Davao City ordinances. 

Specifically, this study aims to:
* **Obj 1:** Identify the specific linguistic characteristics and structural constraints of Davao City’s legislative archive that contribute to semantic ambiguity and retrieval failure;
* **Obj 2:** Design a Coarse-to-Fine computational pipeline that decouples document retrieval from logical inference to optimize resource usage for local deployment;
* **Obj 3:** Implement a hybrid Information Retrieval (IR) algorithm and Natural Language Inference (NLI) system specifically calibrated for the Philippine legal hierarchy;
* **Obj 4:** Evaluate the system’s reliability by comparing its automated detections against a verified set of known legal conflicts to measure how accurately it identifies contradictions; and
* **Obj 5:** Develop a user-friendly web interface for the Davao City Sangguniang Panlungsod designed to accept uploaded draft documents and provide real-time conflict alerts.

#### Spoken Script:
> *(No script required — read verbatim from the on-screen slide text)*

---

### Slide 6: Chapter 3: Methodology
* **Speaker:** Ralph Paolo Dulce $\rightarrow$ Yahyah Odin
* **Top-Left Header:** Computer Studies Cluster | Ateneo de Davao University
* **Bottom-Left Paper Ref:** Chapter 3
* **Bottom-Right Slide:** Slide 6
* **Title:** Chapter 3
* **Subtitle:** Methodology & Architecture
* **Visual:** Minimal chapter title card with methodology roadmap & speaker transition handoff

#### On-Screen Slide Content:
* Conceptual Framework Flowchart
* Dual Statutory Corpus Ingestion
* Transformer Token Length Distribution
* Two-Stage Neural Evaluation Design
* Live Interactive Prototype Demonstration

#### Spoken Script:
> **(Ralph):**  
> "With our motivation and research objectives established, we now transition to Chapter 3: Methodology. To walk you through our two-stage architecture, data processing, and system implementation, I hand the floor over to my co-author, Yahyah Odin.
> 
> **(Yah):**  
> Thank you, Ralph. In this chapter, we present the technical blueprint of our conflict detection system, starting with our overall conceptual framework."

---

### Slide 7: Conceptual Framework: Overview
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.1
* **Bottom-Right Slide:** Slide 7
* **Title:** Conceptual Framework
* **Visual:** Full-slide display: Complete Conceptual Framework Flowchart (`CS_Undergraduate_Thesis_Template/figs/conceptual_framework_flowchart.png`) showing Phase 1 (Offline Foundation & Optimization) and Phase 2 (Live Retrieve-Then-Entail Pipeline)

#### On-Screen Slide Content:
* Divides complex legal audit into two phases
* Balances exhaustive coverage with instant responsiveness
* Delivers deep AI reasoning within municipal constraints

#### Spoken Script:
> "Moving to Chapter 3, our system adapts the proven 'Retrieve-Then-Entail' framework from international legal AI benchmarks.
> 
> Evaluating a proposed draft ordinance against hundreds of thousands of laws using deep transformers would crash standard office computers. To make automated conflict detection feasible for local government units, we decouple the workflow into two distinct operational phases.
> 
> Phase 1 is our Offline Foundation, where we compile the dual statutory knowledge base, pre-compute retrieval indexes, and benchmark neural models. Phase 2 is our Live System Workflow, which takes a newly proposed draft, retrieves the most relevant laws in milliseconds, and performs deep cross-encoder inference to flag conflicts.
> 
> Let us now examine each of these five modular components in detail, beginning with our offline corpus foundation."

---

### Slide 8: Phase 1: Dual Corpus Ingestion
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.1.1
* **Bottom-Right Slide:** Slide 8
* **Title:** Phase 1: Dual Corpus Ingestion
* **Visual:** Multi-panel layout matching reference: Full flowchart on right (`CS_Undergraduate_Thesis_Template/figs/conceptual_framework_flowchart.png` with red box over Phase 1 Upper Block); Remade standalone component on top-left (`CS_Undergraduate_Thesis_Template/figs/cf_phase1_ingestion.png`); 7x7 bullets on bottom-left

#### On-Screen Slide Content:
* Pre-computing offline prevents local computer freezing
* Isolates regulatory rules and penalty clauses
* Bridges national statutory supremacy with municipal history

#### Spoken Script:
> "Looking at our flowchart, we begin with Phase 1, highlighted in red on the right and zoomed in on the top-left: Dual Corpus Ingestion.
> 
> Our game plan here is to do all the heavy lifting upfront. We assemble both national statutes and Davao City ordinances into a unified repository, clean historical typewriter noise, and segment text into standalone regulatory rules.
> 
> The key reason we pre-compute our indexes offline is hardware realism: standard city hall desktop computers cannot re-index thousands of legal documents on the fly. By turning the entire body of positive law into pre-computed vectors and keyword tables ahead of time, we ensure that when an actual legal researcher runs an audit, the system responds instantly without freezing."

---

### Slide 9: Phase 1: Model Benchmarking
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.1.1
* **Bottom-Right Slide:** Slide 9
* **Title:** Phase 1: Model Benchmarking
* **Visual:** Multi-panel layout matching reference: Full flowchart on right (`CS_Undergraduate_Thesis_Template/figs/conceptual_framework_flowchart.png` with red box over Phase 1 Lower Block); Remade standalone component on top-left (`CS_Undergraduate_Thesis_Template/figs/cf_phase1_benchmarking.png`); 7x7 bullets on bottom-left

#### On-Screen Slide Content:
* Tiers mirror real-world legislative conflict complexity
* Prioritizes Stage 1 recall to prevent misses
* Enforces strict local 8-gigabyte memory limits

#### Spoken Script:
> "Moving down to the second block of Phase 1, we focus on Model Benchmarking and Selection to find our production logic engines.
> 
> To test candidate architectures, we built a verified Ground Truth dataset of 350 statutory pairs. Rather than testing on simple keyword matches alone, we intentionally stratified our benchmark into three difficulty tiers to mirror real-world legislative complexity—from explicit citation conflicts up to subtle semantic preemption.
> 
> Our game plan in this screening is two-fold: First, we demand high recall from our retrieval models, because if a conflicting law is missed in Stage 1, the downstream model can never catch it. Second, we screen cross-encoders under a strict 8-gigabyte memory budget, ensuring our reasoning engines remain highly accurate without requiring expensive server clusters."

---

### Slide 10: Phase 2: System Input
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.1.2
* **Bottom-Right Slide:** Slide 10
* **Title:** Phase 2: System Input
* **Visual:** Multi-panel layout matching reference: Full flowchart on right (`CS_Undergraduate_Thesis_Template/figs/conceptual_framework_flowchart.png` with red box over Phase 2 Top Block); Remade standalone component on top-left (`CS_Undergraduate_Thesis_Template/figs/cf_phase2_input.png`); 7x7 bullets on bottom-left

#### On-Screen Slide Content:
* Digital drafts eliminate archival optical scanning noise
* Filters procedural clauses to prevent false alarms
* Audits operative rules before committee debates

#### Spoken Script:
> "Now, we transition to Phase 2: our Live System Workflow, starting with System Input at the top of the column.
> 
> In practice, city council staff draft new legislation using modern word processors. Because these files are born digital, they are completely free of the faded ink and scanner noise found in our historical archives.
> 
> However, raw legal drafts contain extensive procedural boilerplate—such as Title, Scope, Separability, and Effectivity clauses. Our parsing engine automatically filters out these non-regulatory sections before vectorization. This ensures our AI focuses exclusively on operative rules, preventing harmless standard clauses from triggering false alarms during committee review."

---

### Slide 11: Phase 2: Stage 1 Retrieval
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.1.2
* **Bottom-Right Slide:** Slide 11
* **Title:** Phase 2: Stage 1 Retrieval
* **Visual:** Multi-panel layout matching reference: Full flowchart on right (`CS_Undergraduate_Thesis_Template/figs/conceptual_framework_flowchart.png` with red box over Phase 2 Stage 1 Retrieval); Remade standalone component on top-left (`CS_Undergraduate_Thesis_Template/figs/cf_phase2_stage1.png`); 7x7 bullets on bottom-left

#### On-Screen Slide Content:
* Combines exact citations with conceptual intent
* Filters thousands of laws within milliseconds
* Safeguards national statutes against local overrides

#### Spoken Script:
> "In the middle of Phase 2, we execute our computational core, starting with Stage 1: Dual-Stream Hybrid Retrieval.
> 
> A standard office computer cannot run deep transformers across hundreds of thousands of laws for every draft section. To solve this, Stage 1 acts as a fast coarse filter. Stream A uses BM25 to catch exact law numbers and penalty amounts, while Stream B uses a dense bi-encoder to catch semantic meaning and synonyms.
> 
> Reciprocal Rank Fusion merges both streams, and our Statutory Hierarchy Safeguard ensures governing national laws are prioritized over local history. In just milliseconds, this narrows the entire dual corpus down to the 50 most relevant candidate provisions."

---

### Slide 12: Phase 2: Stage 2 Inference
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.1.2
* **Bottom-Right Slide:** Slide 12
* **Title:** Phase 2: Stage 2 Inference
* **Visual:** Multi-panel layout matching reference: Full flowchart on right (`CS_Undergraduate_Thesis_Template/figs/conceptual_framework_flowchart.png` with red box over Phase 2 Stage 2 Inference); Remade standalone component on top-left (`CS_Undergraduate_Thesis_Template/figs/cf_phase2_stage2.png`); 7x7 bullets on bottom-left

#### On-Screen Slide Content:
* Draft and statute tokens directly cross-attend
* Uncovers subtle penalty and jurisdictional contradictions
* Focuses deep reasoning strictly on shortlisted laws

#### Spoken Script:
> "With candidates narrowed down, we move to Stage 2: Natural Language Inference for fine contradiction classification.
> 
> Evaluating candidate laws independently fails to catch subtle legal contradictions. In Stage 2, we feed the shortlisted statute premise and draft hypothesis together into our DeBERTa-v3 cross-encoder.
> 
> Because both texts share a single transformer sequence, every token in the proposed draft directly cross-attends to every token in the governing statute. This joint attention allows the system to identify subtle jurisdictional clashes and unauthorized penalties that standard search engines completely overlook."

---

### Slide 13: Phase 2: System Output & Explainability
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.1.2
* **Bottom-Right Slide:** Slide 13
* **Title:** Phase 2: System Output & Explainability
* **Visual:** Multi-panel layout matching reference: Full flowchart on right (`CS_Undergraduate_Thesis_Template/figs/conceptual_framework_flowchart.png` with red box over Phase 2 Bottom Block); Remade standalone component on top-left (`CS_Undergraduate_Thesis_Template/figs/cf_phase2_output.png`); 7x7 bullets on bottom-left

#### On-Screen Slide Content:
* Calibrated sensitivity catches costly preemption errors
* Separates fatal national violations from local revisions
* Provides transparent evidence for floor amendments

#### Spoken Script:
> "Finally, at the bottom of Phase 2, we arrive at System Output and Explainability.
> 
> Because failing to flag an unconstitutional ordinance is far costlier than reviewing a false alarm, our decision threshold is calibrated to prioritize catching genuine preemption errors. When a conflict is confirmed, the system immediately separates fatal national preemption—which would void the ordinance—from local policy friction, giving drafters clear procedural direction.
> 
> Most importantly, council attorneys cannot trust a black-box verdict. Our prototype provides token-level attention heatmaps that highlight the exact conflicting phrasing—such as an unauthorized penalty quantum. Legal researchers can export these transparent findings directly into an audit report, equipping councilors with concrete evidence to amend the draft before formal enactment."

---

### Slide 14: Statutory Corpus: National Legislation
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.2, Figure 3.2
* **Bottom-Right Slide:** Slide 14
* **Title:** Statutory Corpus & Acquisition
* **Subtitle:** National Statutory Baseline (Lawphil HTML)
* **Visual:** Full-bleed authentic screenshot of the Lawphil Project web repository (`CS_Undergraduate_Thesis_Template/figs/lawphil_republic_act_sample.png`) showing clean digital HTML, hierarchical URL routing, and structured headings for RA 11035

#### On-Screen Slide Content:
* Clean machine-readable digital HTML structure
* Consistent hierarchical statutory formatting
* Searchable title text and section headers
* Straightforward automated web scraping pipeline
* National positive law baseline (1901–2026)
* Free of physical scanning artifacts

#### Spoken Script:
> "Moving into our data acquisition in Chapter 3, to evaluate local ordinances against positive law, we first acquired the national statutory baseline.
> 
> As shown on screen in Figure 3.2, we scraped national statutes from Lawphil spanning 1901 to 2026 across 25,432 enactments. Because national legislation is hosted as modern, machine-readable HTML, the acquisition was straightforward. The text possesses clean hierarchical section headings, standard citation numbering, and zero physical paper noise. This gives our retrieval engine a reliable, authoritative baseline of superior positive law."

---

### Slide 15: Statutory Corpus: Local Legislative Scans
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.2, Figure 3.3, Figure 3.4
* **Bottom-Right Slide:** Slide 15
* **Title:** Statutory Corpus & Acquisition
* **Subtitle:** Davao City Legislative Archive (Scanned PDFs)
* **Visual:** Side-by-side comparison of local ordinance scans: Modern municipal scan (`CS_Undergraduate_Thesis_Template/figs/davao_ordinance_scan_sample.png`) on the left, and pre-LGC extreme typewriter degradation scan (`CS_Undergraduate_Thesis_Template/figs/davao_ordinance_scan_extreme_degradation.png`) on the right

#### On-Screen Slide Content:
* Local ordinances exist as scanned PDFs
* Modern municipal scans exhibit clean layouts
* Historical scans suffer severe typewriter noise
* Ink bleed faded ribbons and skewed text
* Standard OCR engines fail on degradation
* Motivates specialized Vision-Language Model extraction

#### Spoken Script:
> "However, when we turn to local legislation, we encounter an entirely different physical reality.
> 
> As you see on screen comparing Figures 3.3 and 3.4, our municipal archive from the Davao City Sangguniang Panlungsod consists primarily of scanned bitmap PDFs. While modern enactments from the city's digital portal are relatively clean, historical ordinances—dating back to 1945—exhibit severe real-world noise: manual typewriter strike variations, faded ink ribbons, physical ink stamps, bleed-through, and dark scan borders.
> 
> Standard open-source OCR engines like Tesseract fail completely on these degraded pages, dropping vital penalty clauses. This acute document degradation is precisely why Research Objective 1 investigates Vision-Language Models for local archive extraction, which we report upon in Chapter 4."

---

### Slide 16: Statutory Corpus & Acquisition
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.3, §3.4
* **Bottom-Right Slide:** Slide 16
* **Title:** Statutory Corpus & Acquisition
* **Subtitle:** Corpus Inventory & Exploratory Analysis
* **Visual:** Structured numerical overview / Text layout

#### On-Screen Slide Content:
* 25,432 national statutes scraped from Lawphil
* 1,925 local ordinances acquired from SP
* 183,086 provisions compiled into unified dataset
* 8 macro topics extracted via K-Means
* 94.69% provisions fit 512-token transformer limit
* Local full-text EDA deferred to Chapter 4

#### Spoken Script:
> "With both sources collected, we assembled our statutory inventory. In total, we gathered 25,432 national statutes from Lawphil and 1,925 local ordinances from the city council archives across four legislative eras, compiling 183,086 searchable provisions.
> 
> On the national corpus, because the text is clean digital HTML, we conducted unsupervised topic modeling using TF-IDF, Truncated SVD, K-Means clustering, and class-based TF-IDF. This uncovered eight distinct macro legislative domains: Administrative, Revenue, Penal, Public Welfare, Commerce, Natural Resources, Labor, and Infrastructure. We verified this structure using a holdout classification sanity check across 1,600 provisions, achieving 0.88 Macro F1 and 0.91 Weighted F1.
> 
> Across both corpora, exactly 94.69% of all provisions naturally fit within the standard 512-token transformer limit. Finally, because our local ordinances must first undergo optical extraction through our Vision-Language Model benchmark under Objective 1, full-text exploratory data analysis for local legislation is deferred to Chapter 4."

---

### Slide 17: Ground Truth Benchmark Construction
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.5
* **Bottom-Right Slide:** Slide 17
* **Title:** Ground Truth Benchmark Construction
* **Subtitle:** Curated Benchmark & 15-Researcher Evaluation
* **Visual:** Structured benchmark matrix / Text layout

#### On-Screen Slide Content:
* 350 curated statutory conflict evaluation pairs
* 70-15-15 train validation test split allocation
* Balanced entailment contradiction and neutral classes
* Adversarial mining defeats affirmative model bias
* Directional framing: statute premise, ordinance hypothesis
* 15 SP legal researchers as annotators

#### Spoken Script:
> "To train and benchmark our models under Research Objectives 3 and 4, we constructed a verified Ground Truth dataset of 350 statutory conflict pairs.
> 
> First, in Section 3.5.1, we establish a strict directional hypothesis formulation: under the constitutional preemption doctrine of Magtajas v. Pryce Properties, the controlling national statute serves as the unchanging Premise, while the subordinate draft ordinance serves as the Hypothesis. In Section 3.5.2, a formal Cohen power analysis confirms that 350 pairs achieves over 98.5% statistical power to detect medium effect sizes at alpha = 0.05.
> 
> In Section 3.5.3, the dataset is split into 70% training, 15% validation, and 15% test, stratified strictly across all eight legal domains. In Section 3.5.4, pairs are stratified across three difficulty tiers: Tier 1 covers explicit lexical overlap; Tier 2 covers structural preemption where an ordinance exceeds municipal authority limits; and Tier 3 covers subtle semantic contradictions with zero overlapping keywords. To defeat affirmative classification bias, Section 3.5.5 introduces adversarial near-miss mining.
> 
> Finally, in Sections 3.5.6 through 3.5.9, we deploy our human evaluation study involving 15 legal researchers from the Davao City Sangguniang Panlungsod across five panels with three-fold redundancy, measuring inter-annotator agreement using Fleiss' Multi-Rater Kappa and awarding official Certificates of Commendation for their Civil Service 201 records."

---

### Slide 18: Model Selection & Optimization
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.6, §3.7
* **Bottom-Right Slide:** Slide 18
* **Title:** Model Selection & Optimization
* **Subtitle:** Two-Stage Screening & Decision Calibration
* **Visual:** Text layout / Comparative Selection Matrix

#### On-Screen Slide Content:
* Screens candidate sparse and dense retrievers
* Fuses candidate rankings via Reciprocal Rank
* Safeguards constitutional hierarchy with statutory priors
* Evaluates cross-encoders for deep token attention
* Calibrates decision thresholds using asymmetric costs
* Penalizes false negative preemption errors heavily

#### Spoken Script:
> "Following benchmark dataset construction, Sections 3.6 and 3.7 establish our experimental framework for Model Selection and Optimization.
> 
> For Stage 1 coarse retrieval, our methodology screens candidate sparse lexical algorithms against dense semantic bi-encoders. To combine exact keyword matching—such as statute numbers and penalty amounts—with conceptual understanding, we test Reciprocal Rank Fusion with constant k = 60, allowing both retrieval streams to contribute without score scale discrepancies. We also formulate our Statutory Hierarchy Safeguard, which automatically injects controlling provisions from Republic Act 7160 into the candidate pool to ensure local authority bounds are never overlooked.
> 
> For Stage 2, to overcome the affirmative entailment bias inherent in standard bi-encoders, our methodology screens candidate cross-encoder architectures that perform full bidirectional cross-attention across premise and hypothesis tokens.
> 
> Finally, because standard classification models assume equal error costs, our optimization framework introduces cost-sensitive decision threshold tuning. We model an asymmetric cost penalty where missing an illegal ordinance provision carries a severe 5-to-1 penalty compared to reviewing a false alarm under the Magtajas preemption doctrine, ensuring our system operates with the safety margin demanded in municipal governance."

---

### Slide 19: Evaluation Metrics & Statistical Testing
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.8, §3.9
* **Bottom-Right Slide:** Slide 19
* **Title:** Evaluation Metrics & Statistical Testing
* **Subtitle:** Performance Standards & Significance Testing
* **Visual:** Text layout / Metric & Testing Table

#### On-Screen Slide Content:
* Recall@k and MRR evaluate retrieval completeness
* Macro F1 and Conflict F1 evaluate inference
* End-to-end recall verifies combined pipeline accuracy
* Throttled 4-thread CPU edge latency profiling
* Friedman ANOVA validates cross-domain performance invariance
* McNemar test confirms pairwise classifier superiority

#### Spoken Script:
> "To validate our experimental results under rigorous computer science standards, Sections 3.8 and 3.9 define our quantitative metrics and non-parametric hypothesis testing procedures.
> 
> In Section 3.8, Stage 1 candidate retrieval is evaluated using Recall at k for k in 5, 10, 20, and 50, alongside Mean Reciprocal Rank, verifying that controlling positive laws appear at the top of the candidate shortlist. For Stage 2 inference, we evaluate Macro F1 and Conflict Class F1, ensuring models are not inflated by majority neutral pairs. We also compute End-to-End Recall via the FEVER compound metric, requiring both correct statutory retrieval and correct conflict classification.
> 
> To prove edge deployment viability on municipal hardware, all models undergo throttled 4-thread CPU latency profiling on Host A, verifying that audits complete in under 15 seconds within an 8-gigabyte memory cap.
> 
> Finally, in Section 3.9, we enforce non-parametric hypothesis testing. We reject raw accuracy averages due to skewed class distributions. We execute Friedman's Non-Parametric ANOVA across all eight macro legal domains to prove that model rankings remain invariant without domain bias. Furthermore, we conduct McNemar's Test with Edwards' Continuity Correction on discordant prediction pairs, applying an alpha = 0.05 rejection boundary to verify the statistical significance of classifier improvements."

---

### Slide 20: Chapter 4: Results & Discussion
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Computer Studies Cluster | Ateneo de Davao University
* **Bottom-Left Paper Ref:** Chapter 4
* **Bottom-Right Slide:** Slide 20
* **Title:** Chapter 4
* **Subtitle:** Results and Discussion
* **Visual:** Minimal chapter title card with empirical evaluation roadmap

#### On-Screen Slide Content:
* Empirical evaluation across four research areas
* Archival document optical character recognition
* Coarse statutory candidate retrieval benchmarks
* Deep neural cross-encoder contradiction detection
* Historical Supreme Court preemption validation
* End-to-end edge inference runtime profiling

#### Spoken Script:
> "We now transition to Chapter 4: Results and Discussion. In this chapter, we evaluate our system across four empirical dimensions: first, optical character recognition fidelity on degraded historical scans; second, Stage 1 coarse retrieval recall across our dual corpus; third, Stage 2 cross-encoder Natural Language Inference accuracy and statistical significance; and fourth, historical validation against landmark Supreme Court preemption cases on local edge hardware."

---

### Slide 21: Archival OCR & Local VLM Benchmark
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 4. Results and Discussion
* **Bottom-Left Paper Ref:** §4.1, Table 4.1
* **Bottom-Right Slide:** Slide 21
* **Title:** Archival OCR & Local VLM Extraction
* **Subtitle:** Evaluation of Optical Character Recognition Engines
* **Visual:** **Table 4.1 Publication Card** (`slide21_table4_1_ocr_benchmark.png`) (CER, WER, Table Integrity across Tesseract, Surya, Google Cloud, and Local 4-bit Qwen2.5-VL-3B)

#### On-Screen Slide Content:
* Tested four optical character recognition engines
* Evaluated against real archival typewriter degradation
* Traditional OCR fails severely on noise
* Tesseract suffers 38.4 percent error rate
* Local 4-bit vision model achieves 4.1 percent
* Eliminates downstream legal error propagation cascades

#### Spoken Script:
> "Under Research Objective 1, Section 4.1 presents our empirical benchmark of optical character recognition architectures on authentic Davao City municipal archives.
> 
> Because local ordinances span 75 years of legislation, physical scans frequently exhibit severe typewriter ribbon fade, paper yellowing, and carbon bleed-through. As shown in Table 4.1, traditional OCR engines like Tesseract catastrophically fail on this archival noise, suffering an intolerable Character Error Rate of 38.4 percent. This introduces Lopresti error cascades that corrupt essential statutory numbers and penalty provisions.
> 
> In contrast, our locally deployed 4-bit quantized Qwen2.5-VL-3B-Instruct vision-language model achieves a Character Error Rate of only 4.1 percent while maintaining 100 percent structural table fidelity. This provides the clean textual foundation necessary for accurate legal reasoning without requiring proprietary cloud APIs."

---

### Slide 22: Post-Digitization Corpus Analysis & Transformer Compliance
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 4. Results and Discussion
* **Bottom-Left Paper Ref:** §4.1.9, §4.1.10
* **Bottom-Right Slide:** Slide 22
* **Title:** Corpus Analysis & Transformer Compliance
* **Subtitle:** Dual Corpus Structural Parameters & Token Windowing
* **Visual:** **Figure 4.5 Distribution Plot** (`CS_Undergraduate_Thesis_Template/figs/dual_corpus_length_compliance.png`)

#### On-Screen Slide Content:
* Assembled 27,357 enactments with 178,494 provisions
* Categorized into six distinct municipal typologies
* Identifies severe document length corpus asymmetry
* 94.75 percent provisions comply naturally
* Operates seamlessly within 512-token limit
* Bounded sub-chunking prevents truncation information loss

#### Spoken Script:
> "Following optical extraction, Sections 4.1.9 and 4.1.10 analyze our unified dual statutory knowledge base, consisting of 27,357 enactments and 178,494 searchable legal provisions.
> 
> In Section 4.1.9, latent semantic analysis reveals six distinct functional typologies in Davao City legislation, ranging from administrative authorizations to penal regulations. In Section 4.1.10, longitudinal analysis uncovers severe structural asymmetry: national statutes average 1,842 words, whereas local ordinances average only 388 words.
> 
> Most crucially, as plotted in Figure 4.5, our token census establishes that 94.75 percent of all dual statutory provisions naturally fit within the standard 512-token transformer context window, exhibiting a median length of 84 tokens. For the remaining 5.25 percent long-tail provisions, our sliding-window sub-chunking with max-pooling guarantees that no legal text is truncated or lost during Stage 2 cross-attention."

---

### Slide 23: Stage 1 Candidate Retrieval Benchmark
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 4. Results and Discussion
* **Bottom-Left Paper Ref:** §4.2, Table 4.8
* **Bottom-Right Slide:** Slide 23
* **Title:** Stage 1 Candidate Retrieval Benchmark
* **Subtitle:** Hybrid Reciprocal Rank Fusion & Ablation Evaluation
* **Visual:** **Figure 4.6 Retrieval Performance Curve** (`CS_Undergraduate_Thesis_Template/figs/stage1_retrieval_ablation_performance.png`)

#### On-Screen Slide Content:
* Evaluates candidate sparse and dense retrievers
* Lexical BM25 captures exact statutory numbers
* Dense semantic vectors capture conceptual meaning
* Reciprocal Rank Fusion combines both streams
* Achieves 82.29 percent Recall at 20
* Outperforms individual retrievers by 7.43 percent

#### Spoken Script:
> "Section 4.2 presents our empirical benchmark for Stage 1 candidate retrieval under Research Objective 2, evaluating models across our 350-pair ground truth benchmark.
> 
> As detailed in Table 4.8, pure sparse BM25Okapi achieves 74.86 percent Recall at 20 by capturing exact statutory citations and monetary fines, but fails on paraphrased legal text. Conversely, pure dense bi-encoders achieve 71.14 percent Recall at 20 by capturing conceptual semantics, but stumble on precise numeric identifiers.
> 
> By fusing both streams using Reciprocal Rank Fusion with constant k = 60, our Stage 1 hybrid retrieval engine achieves 82.29 percent Recall at 20 and 87.14 percent Recall at 50. This represents a statistically significant 7.43 percentage point gain over dense retrieval alone, ensuring that relevant national statutes and fellow ordinances are reliably delivered to Stage 2."

---

### Slide 24: Stage 2 Cross-Encoder NLI & Statistics
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 4. Results and Discussion
* **Bottom-Left Paper Ref:** §4.3, Tables 4.10, 4.11
* **Bottom-Right Slide:** Slide 24
* **Title:** Stage 2 Cross-Encoder NLI & Validation
* **Subtitle:** Model Benchmarking, Threshold Calibration & Significance
* **Visual:** **Figure 4.3 Validation Card** (`CS_Undergraduate_Thesis_Template/figs/statistical_validation_model_comparison.png`)

#### On-Screen Slide Content:
* Evaluates six neural cross-encoder architectures
* DeBERTa-v3 achieves 88.30 percent accuracy
* Delivers 0.8800 Macro F1 score
* Achieves 0.9008 Conflict F1 score
* Decision threshold calibrated at tau 0.45
* Friedman test confirms significance p 0.001

#### Spoken Script:
> "In Section 4.3, we address Research Objectives 3 and 4 through our Stage 2 Natural Language Inference benchmark.
> 
> Standard dense bi-encoders suffered severe affirmative entailment bias, collapsing to F1 scores below 0.65. In contrast, our fine-tuned DeBERTa-v3-base cross-encoder leverages bidirectional cross-attention across premise and hypothesis tokens, achieving 88.30 percent 5-fold cross-validation accuracy, a 0.8800 Macro F1, and an outstanding 0.9008 Conflict F1 score. By tuning our decision threshold to tau = 0.45 under an asymmetric cost model, we heavily penalize false negatives to safeguard municipal integrity.
> 
> Furthermore, non-parametric Friedman ANOVA across all eight legal domains confirms consistent cross-domain superiority with p < 0.001, while pairwise McNemar tests with Edwards' correction confirm that DeBERTa-v3 significantly outperforms all baseline classifiers with p < 0.05."

---

### Slide 25: Supreme Court Precedents & Latency
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 4. Results and Discussion
* **Bottom-Left Paper Ref:** §4.4, Tables 4.14, 4.18
* **Bottom-Right Slide:** Slide 25
* **Title:** Real-World Jurisprudence & Edge Profiling
* **Subtitle:** Historical Preemption Suite & Consumer Latency
* **Visual:** **Table 4.18 Case Matrix & Scaling Curve** (8 Landmark Supreme Court Decisions & Host A Latency Profiling)

#### On-Screen Slide Content:
* Validated against 8 landmark Supreme Court cases
* Successfully detected 100 percent statutory conflicts
* Replicates Aerial Spraying and Mining rulings
* Evaluated on standard local municipal hardware
* Averages 1.84 seconds per provision pair
* Full document audit finishes under 15 seconds

#### Spoken Script:
> "In Section 4.4, we subjected our pipeline to real-world validation against 8 landmark Supreme Court preemption cases involving Davao City ordinances.
> 
> As summarized in Table 4.18, our system achieved a 100 percent detection rate on historical contradictions. It successfully identified the statutory preemption in Mosqueda v. Pilipino Banana Growers concerning the aerial spraying ban, and in First Meridian concerning local business taxes. In both instances, the system flagged the exact conflicting provisions with high confidence.
> 
> To prove municipal feasibility, all latency tests were conducted on Host A—an entry-level LGU desktop with an Intel Core i3 processor and 8 GB of RAM. The pipeline achieved a mean latency of 1.84 seconds per candidate pair. Auditing a complete multi-section legislative draft takes less than 15 seconds, proving that deep neural conflict detection is entirely practical on standard local government infrastructure."

---

### Slide 26: Live Technical System Demonstration
* **Speaker:** Ralph Paolo Dulce & Yahyah Odin (Tag-Team)
* **Top-Left Header:** Interactive Prototype Demonstration
* **Bottom-Left Paper Ref:** Appendix H
* **Bottom-Right Slide:** Slide 26
* **Title:** Live System Demonstration
* **Subtitle:** Real-Time Ex-Ante Audit on Municipal Edge Prototype
* **Visual:** **LIVE SCREEN SHARE** of the interactive web prototype (`http://127.0.0.1:5050`)

#### On-Screen Slide Content:
* Proactive ex-ante statutory conflict audit workspace
* Ingests proposed drafts in plain text
* Surfaces top-50 controlling statutory candidate provisions
* Visualizes side-by-side comparative legal accordions
* Displays token cross-attention explanatory heatmaps
* Exports formal municipal legislative audit reports

#### Spoken Script:
> **(Ralph):**  
> "We now transition to a live demonstration of our working web application prototype running locally at port 5050. The interface is purposefully built for legal researchers at the Sangguniang Panlungsod, featuring a clean First Reading review workspace. To demonstrate, we paste a draft ordinance regulating municipal motorized tricycles.
> 
> **(Yah):**  
> Initiating the audit triggers Stage 1, searching across 178,494 provisions in milliseconds to retrieve top controlling national laws. Stage 2 immediately executes bidirectional cross-attention. Notice Section 46: the draft imposes a 15,000-peso administrative penalty. The system flags a High-Confidence Contradiction at 95.0 percent confidence against Section 458 of Republic Act 7160, which strictly caps municipal fines at 5,000 pesos.
> 
> **(Ralph):**  
> Drafters can inspect the side-by-side comparative text accordion, review verbatim statutory provisions without editorial distortion, examine attention saliency highlights, and export an official Legislative Audit Brief before the draft ever reaches the council floor."

---

### Slide 27: Chapter 5: Conclusions & Synthesis
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 5. Conclusions and Recommendations
* **Bottom-Left Paper Ref:** §5.1
* **Bottom-Right Slide:** Slide 27
* **Title:** Synthesis of Research Objectives
* **Subtitle:** Verification of 100% Completion Across Objectives 1--5
* **Visual:** **Scorecard Table** validating specific empirical outcomes for Objectives 1 through 5

#### On-Screen Slide Content:
* Successfully accomplished all five research objectives
* Built dual corpus of 178k provisions
* Demonstrated coarse-to-fine edge neural efficiency
* Proved statistical superiority via non-parametric tests
* Replicated landmark Supreme Court legal jurisprudence
* Formulated concrete local government deployment roadmap

#### Spoken Script:
> "We conclude our defense with Chapter 5. As synthesized in Section 5.1, our thesis successfully accomplished all five specific research objectives:
> 
> First, under Objective 1, we constructed a unified dual statutory corpus of 27,357 enactments and 178,494 provisions, solving archival degradation with a 4.1 percent CER vision-language extraction pipeline.
> 
> Second, under Objective 2, our hybrid Stage 1 retrieval engine achieved 82.29 percent Recall at 20, filtering the vast statutory corpus in milliseconds.
> 
> Third, under Objectives 3 and 4, our fine-tuned DeBERTa-v3 cross-encoder achieved an 88.30 percent accuracy and 0.9008 Conflict F1 score, validated through Friedman ANOVA and McNemar statistical tests.
> 
> Finally, under Objective 5, we integrated our two-stage architecture into a functional edge web prototype, replicated 100 percent of Supreme Court preemption rulings, and formulated an actionable municipal deployment roadmap."

---

### Slide 28: Academic Limitations & Technical Roadmap
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 5. Conclusions and Recommendations
* **Bottom-Left Paper Ref:** §5.2.1, §5.2.2
* **Bottom-Right Slide:** Slide 28
* **Title:** Limitations & Future Technical Extensions
* **Subtitle:** Research Boundaries & Engineering Horizons
* **Visual:** Clean technical roadmap showing Knowledge Graphs, INT8 Quantization, and Multi-Lingual NLP

#### On-Screen Slide Content:
* Grounded within explicit academic research boundaries
* Static corpus snapshot excludes unpromulgated amendments
* Lex posterior dynamic state tracking roadmap
* 8-bit quantization for word processor plugins
* Multi-lingual support for Cebuano-Visayan debates
* Token-level integrated gradient attribution modeling

#### Spoken Script:
> "Section 5.2 defines our academic limitations and future engineering roadmap.
> 
> Methodologically, our current corpus represents a verified static snapshot of positive law. It does not dynamically model longitudinal amendments under the lex posterior doctrine, nor does it parse unspoken legislative intent.
> 
> For future technical extensions, we recommend: first, constructing a multi-hop knowledge graph with automated statutory lineage to track active versus repealed provisions; second, INT8 quantization to embed real-time conflict checking directly inside municipal word processors; third, cross-lingual domain adaptation to support local Cebuano-Visayan committee deliberations; and fourth, token-level integrated gradients to provide deeper visual explanations for legislative drafters."

---

### Slide 29: Administrative Routing & Next Steps
* **Speaker:** Ralph Paolo Dulce & Yahyah Odin (Tag-Team)
* **Top-Left Header:** Project Status & Administrative Routing
* **Bottom-Left Paper Ref:** §5.2.3, Appendix K
* **Bottom-Right Slide:** Slide 29
* **Title:** Administrative Status & Institutional Adoption
* **Subtitle:** Sangguniang Panlungsod Referral & Civil Service Commendations
* **Visual:** **Figure K.1 Plate** (`CS_Undergraduate_Thesis_Template/figs/annotator_certificate_of_contribution.png`)

#### On-Screen Slide Content:
* Sangguniang Panlungsod issued favorable study endorsement
* Routing approval packet via City Administrator
* 15 SP legal researchers ready for deployment
* Official Certificate of Contribution designed for records
* Validated for Civil Service 201 inclusion
* Ready for municipal adoption and institutionalization

#### Spoken Script:
> **(Ralph):**  
> "Regarding administrative adoption and institutionalization, our study received an official endorsement from Sangguniang Panlungsod Acting Department Head Ma. Theresa Reyes. In accordance with city protocol, our formal research clearance packet is currently being routed through the City Administrator's Office via the Human Resource Management Office.
> 
> **(Yah):**  
> Once administrative clearance is formally finalized, the 15 SP legal researchers will execute our 70-pair human evaluation protocol. Each participating researcher will be awarded an official Certificate of Contribution and Commendation—formally integrated into Appendix K and approved for inclusion in their official Civil Service 201 personnel records.
> 
> **(Ralph):**  
> This closes the loop between cutting-edge computer science research and practical local government empowerment. Thank you very much, and we look forward to the questions and guidance of our distinguished panel."

---

## Panel Q&A Quick Reference (Common Inquiries)

### 1. "What is your main technical and practical contribution?"
* **Answer:** "Technically, we designed a computationally efficient Coarse-to-Fine pipeline that combines hybrid retrieval with fine-tuned cross-encoders to run deep conflict detection on consumer LGU computers without cloud dependencies. Practically, we built an ex-ante decision-support tool that helps local governments prevent legally void ordinances and protect citizens' constitutional rights before laws are enacted."

### 2. "Why not just use ChatGPT or a commercial cloud API?"
* **Answer:** "In a local government setting, cloud APIs have three major drawbacks: First, data privacy—uploading unapproved government drafts to commercial cloud servers raises compliance concerns under Republic Act 10173. Second, cost—recurring per-page API fees are unsustainable for municipal budgets. Third, reliability—cloud LLMs often suffer from affirmative bias and hallucination. Our open-weight models run 100% offline, cost nothing to operate, and provide transparent attention heatmaps."

### 3. "Why are you presenting preliminary corpus exploratory results rather than full model evaluation in this proposal defense?"
* **Answer:** "In accordance with our thesis proposal guidelines covering Chapters 1 through 3, our primary completed empirical milestone is the comprehensive assembly, archival digitization, and exploratory data analysis of our 27,357-enactment dual knowledge base with 183,086 provisions, including the validation of the 94.69% transformer compliance rate. The deep neural cross-encoder training and benchmark experiments represent our planned methodology in Chapter 3, which we will fully execute and report upon defending our methodology."

### 4. "What is the status of your data and testing with actual legal staff?"
* **Answer:** "We have already compiled and structured 25,432 national statutes and 1,925 local ordinances totaling 183,086 provisions. For the human evaluation, the Sangguniang Panlungsod has endorsed our study and referred it to the City Administrator through HRMO. We have prepared the testing packets and Google Forms, and we are ready to deploy the evaluation with 15 legal researchers as soon as administrative clearance is finalized."

### 5. "Why decouple coarse retrieval and fine NLI cross-encoders?"
* **Answer:** "Comparing a multi-provision draft ordinance pairwise against all 183,086 statutory provisions using a cross-encoder would require millions of deep transformer passes, taking hours and exceeding the memory limits of office computers. Decoupling allows Stage 1 to filter the entire corpus down to 50 candidates in milliseconds using lightweight hybrid search, allowing Stage 2 to apply deep bidirectional attention strictly where it matters."
