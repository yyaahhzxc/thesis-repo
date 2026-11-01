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
| **3** | Background of the Study | Ralph | **Side-by-Side:** Scan (`sample_davao_city_ordinance_scan.png`) + 7x7 Bullets | 2.0 mins |
| **4** | Problem Statement | Ralph | Text Layout (Verbatim Reading) | 1.5 mins |
| **5** | Objectives of the Study | Ralph | Text Layout (Verbatim Reading) | 1.5 mins |
| **6** | Chapter 3: Methodology | Ralph $\rightarrow$ Yah | Title-Only Divider & Speaker Handoff | 0.5 min |
| **7** | Conceptual Framework: Overview | Yah | **Full Flowchart:** Bird's-Eye View (`conceptual_framework_flowchart.png`) | 1.0 min |
| **8** | Phase 1: Dual Corpus Ingestion | Yah | **Multi-Panel:** Full Flowchart (Right) + Remade Component (`cf_phase1_ingestion.png`) (Top-Left) + 7x7 Bullets (Bottom-Left) | 0.75 min |
| **9** | Phase 1: Model Benchmarking | Yah | **Multi-Panel:** Full Flowchart (Right) + Remade Component (`cf_phase1_benchmarking.png`) (Top-Left) + 7x7 Bullets (Bottom-Left) | 0.75 min |
| **10** | Phase 2: System Input | Yah | **Multi-Panel:** Full Flowchart (Right) + Remade Component (`cf_phase2_input.png`) (Top-Left) + 7x7 Bullets (Bottom-Left) | 0.75 min |
| **11** | Phase 2: Stage 1 Retrieval | Yah | **Multi-Panel:** Full Flowchart (Right) + Remade Component (`cf_phase2_stage1.png`) (Top-Left) + 7x7 Bullets (Bottom-Left) | 0.75 min |
| **12** | Phase 2: Stage 2 Inference | Yah | **Multi-Panel:** Full Flowchart (Right) + Remade Component (`cf_phase2_stage2.png`) (Top-Left) + 7x7 Bullets (Bottom-Left) | 0.75 min |
| **13** | Phase 2: System Output & Explainability | Yah | **Multi-Panel:** Full Flowchart (Right) + Remade Component (`cf_phase2_output.png`) (Top-Left) + 7x7 Bullets (Bottom-Left) | 0.75 min |
| **14** | Statutory Corpus & Acquisition | Yah | **Multi-Panel:** Figures 3.2, 3.3, 3.4 Scan Quality Composite (`slide14_corpus_acquisition_comparison.png`) | 1.0 min |
| **15** | Ground Truth Benchmark Construction | Yah | **Dual Card:** Curated Benchmark Tiers & 15-Expert Study (`slide15_ground_truth_benchmark_card.png`) | 1.0 min |
| **16** | Two-Stage Algorithmic Architecture | Yah | **Dual Card:** Stage 1 Hybrid Retrieval vs Stage 2 Cross-Encoder NLI (`slide16_two_stage_architecture_card.png`) | 1.0 min |
| **17** | Performance Metrics & Statistical Testing | Yah | **Dual Card:** Performance Standards vs Hypothesis Testing (`slide17_evaluation_and_testing_card.png`) | 1.0 min |
| **18** | **Live Technical System Demonstration** | Yah | Live Screen Share | 3.0 mins |
| **19** | Project Status, Administrative Routing & Next Steps | Ralph & Yah | Workflow Diagram / Next Steps | 1.0 min |

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

### Slide 14: Statutory Corpus & Acquisition
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.3, §3.4
* **Bottom-Right Slide:** Slide 14
* **Title:** Statutory Corpus & Acquisition
* **Visual:** Figures 3.2, 3.3, 3.4 Scan Quality Composite (`CS_Undergraduate_Thesis_Template/figs/slide14_corpus_acquisition_comparison.png`) showing clean Lawphil HTML, modern municipal scan, and pre-LGC typewriter degradation

#### On-Screen Slide Content:
* 25,432 national statutes scraped from Lawphil
* 1,925 local ordinances acquired from SP
* 183,086 provisions compiled into unified dataset
* 8 macro topics extracted via K-Means
* 94.69% provisions fit 512-token transformer limit
* Local full-text EDA deferred to Chapter 4

#### Spoken Script:
> "Moving into the methodology of Chapter 3, our system relies on positive law across both national and local jurisdictions.
> 
> For national legislation, we scraped 25,432 statutes from Lawphil spanning 1901 to 2026. Because national laws arrive in structured HTML, we immediately performed unsupervised topic modeling using TF-IDF, Truncated SVD, K-Means clustering, and class-based TF-IDF. This revealed eight distinct macro domains: Administrative, Revenue, Penal, Public Welfare, Commerce, Natural Resources, Labor, and Infrastructure. We verified this structure through a holdout classification sanity check across 1,600 manually audited provisions, attaining 0.88 Macro F1 and 0.91 Weighted F1.
> 
> For Davao City ordinances, we inventoried 1,925 enacted measures across four historical legislative eras. However, as illustrated in the visual plate on screen comparing Figures 3.2, 3.3, and 3.4, local ordinances present a stark physical contrast. While national laws are clean digital text, our municipal archive consists of scanned paper documents ranging from modern digital scans to heavily degraded pre-1991 typewriter pages with bleed-through, faded ribbons, and dark borders.
> 
> Because extracting text from these noisy scans requires specialized Vision-Language Models—which fulfills Research Objective 1—we report the complete token distributions and full-text exploratory data analysis for local legislation in Chapter 4, immediately after our text extraction benchmark."

---

### Slide 15: Ground Truth Benchmark Construction
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.5
* **Bottom-Right Slide:** Slide 15
* **Title:** Ground Truth Benchmark Construction
* **Visual:** Ground Truth Benchmark & Human Study Card (`CS_Undergraduate_Thesis_Template/figs/slide15_ground_truth_benchmark_card.png`) detailing the 350-pair stratified dataset and 15-expert evaluation framework

#### On-Screen Slide Content:
* 350 curated statutory conflict evaluation pairs
* 70-15-15 train validation test split allocation
* Balanced entailment contradiction and neutral classes
* Adversarial mining defeats affirmative model bias
* Directional framing: statute premise, ordinance hypothesis
* 15 Sangguniang Panlungsod legal researchers study

#### Spoken Script:
> "To train and benchmark our system under Research Objectives 3 and 4, we constructed a rigorous ground-truth evaluation benchmark of 350 statutory conflict pairs.
> 
> First, in Section 3.5.1, we establish a strict directional hypothesis formulation: under the constitutional preemption doctrine of Magtajas v. Pryce Properties, the superior national statute serves as the unchanging Premise, while the subordinate draft ordinance serves as the Hypothesis. Under Section 3.5.2, a formal Cohen power analysis confirms that 350 pairs achieves over 98.5% statistical power to detect medium effect sizes at alpha = 0.05.
> 
> In Section 3.5.3, we split the dataset into 70% training, 15% validation, and 15% test, stratified strictly across all eight legal domains to prevent thematic leakage. In Section 3.5.4, pairs are stratified across three difficulty tiers: Tier 1 covers explicit lexical overlap; Tier 2 covers structural preemption where an ordinance exceeds municipal authority limits; and Tier 3 covers subtle semantic contradictions with zero overlapping keywords. To defeat affirmative classification bias, Section 3.5.5 introduces adversarial near-miss mining—pairing similar legal topics that do not conflict.
> 
> Finally, in Sections 3.5.6 through 3.5.9, we deploy a comprehensive human evaluation study involving 15 legal researchers from the Davao City Sangguniang Panlungsod. Evaluators are divided into five independent review panels of three researchers each, reviewing 70 pairs with three-fold redundancy. We evaluate agreement using Fleiss' Multi-Rater Kappa, measure usability via SUS and PSSUQ instruments, and award participants official Certificates of Commendation for their Civil Service 201 records."

---

### Slide 16: Two-Stage Algorithmic Architecture
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.6, §3.7
* **Bottom-Right Slide:** Slide 16
* **Title:** Two-Stage Algorithmic Architecture
* **Visual:** Two-Stage Architecture Comparison Card (`CS_Undergraduate_Thesis_Template/figs/slide16_two_stage_architecture_card.png`) contrasting Stage 1 coarse hybrid search with Stage 2 deep cross-attention reasoning

#### On-Screen Slide Content:
* Stage 1 combines BM25 and dense retrieval
* Reciprocal Rank Fusion merges candidate lists
* Statutory Hierarchy Safeguard injects controlling statutes
* Stage 2 applies DeBERTa-v3 cross-attention
* Calibrated threshold tau 0.45 prevents errors
* Asymmetric cost penalizes missed conflicts 5-to-1

#### Spoken Script:
> "In Sections 3.6 and 3.7, we formulate our core algorithmic contribution: a decoupled Coarse-to-Fine architecture designed to run on local government desktop computers.
> 
> Comparing a draft ordinance pairwise against all 183,086 provisions using deep neural transformers would require millions of forward passes and take hours. Instead, Stage 1 executes high-throughput coarse retrieval in milliseconds. It merges sparse BM25 search—which catches exact statute numbers and fine quantities—with dense semantic retrieval using all-MiniLM-L6-v2 embeddings. These streams are fused via Reciprocal Rank Fusion with constant k = 60 to eliminate score calibration discrepancies.
> 
> Furthermore, Stage 1 implements our Statutory Hierarchy Safeguard, which automatically injects governing provisions from Republic Act 7160—the Local Government Code—into the candidate pool, guaranteeing that municipal authority boundaries and fine caps are always evaluated even if draft ordinances omit statutory citations.
> 
> In Stage 2, the top 50 shortlisted candidates pass to a fine-tuned DeBERTa-v3 Cross-Encoder. Because premise and hypothesis tokens attend to each other across all transformer layers, the model detects subtle contradictions that bi-encoders miss. We replace the standard 0.50 classification cutoff with a calibrated threshold of tau = 0.45, incorporating a 5-to-1 asymmetric cost penalty against false negatives under Magtajas, because letting an unconstitutional ordinance pass is far more hazardous than reviewing a false flag."

---

### Slide 17: Performance Metrics & Statistical Testing
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.8, §3.9
* **Bottom-Right Slide:** Slide 17
* **Title:** Performance Metrics & Statistical Testing
* **Visual:** Performance Metrics & Statistical Testing Card (`CS_Undergraduate_Thesis_Template/figs/slide17_evaluation_and_testing_card.png`) showing IR/NLI metrics alongside non-parametric hypothesis testing

#### On-Screen Slide Content:
* Recall@k and MRR evaluate retrieval completeness
* Macro F1 and Conflict F1 evaluate inference
* End-to-end recall verifies combined pipeline accuracy
* Throttled 4-thread CPU edge latency profiling
* Friedman ANOVA validates cross-domain performance invariance
* McNemar test confirms pairwise classifier superiority

#### Spoken Script:
> "To validate our system under rigorous computer science standards, Sections 3.8 and 3.9 define our quantitative metrics and non-parametric hypothesis testing procedures.
> 
> In Section 3.8, Stage 1 retrieval is evaluated using Recall at k for k in 5, 10, 20, and 50, alongside Mean Reciprocal Rank, verifying that the governing positive law appears at the very top of the candidate shortlist. For Stage 2 inference, we evaluate Macro F1 and Conflict Class F1, ensuring the model is not artificially inflated by majority neutral pairs. We also compute End-to-End Recall via the FEVER compound metric, requiring both correct statutory retrieval and correct conflict classification.
> 
> To prove deployment feasibility on local government hardware, all inference pipelines undergo throttled 4-thread CPU profiling on Host A, ensuring complete draft audits terminate in under 15 seconds with resident memory capped below 8 gigabytes.
> 
> Finally, in Section 3.9, we enforce non-parametric hypothesis testing. Because legal conflict datasets exhibit skewed distributions, we reject simple accuracy averages. We execute Friedman's Non-Parametric ANOVA across all eight macro legal domains to prove that model performance is invariant and does not overfit to specific domains like taxation. Furthermore, we conduct McNemar's Test with Edwards' Continuity Correction on discordant prediction pairs, applying a strict alpha = 0.05 rejection boundary to confirm the statistical superiority of our fine-tuned cross-encoder over baseline models."

---

### Slide 18: Live Technical System Demonstration
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Interactive Prototype Demonstration
* **Bottom-Left Paper Ref:** Appendix H
* **Bottom-Right Slide:** Slide 18
* **Title:** Live System Demonstration
* **Visual:** **LIVE SCREEN SHARE** of the interactive web prototype (Draft upload, Reddit-style hierarchical tree, real-time audit, and XAI heatmap)

#### On-Screen Slide Content:
* Interactive decision-support tool for local deployment
* Parses draft into hierarchical section trees
* Sub-second retrieval surfaces relevant positive laws
* Real-time cross-encoder classifies normative conflicts
* Visualizes attention heatmaps and exports reports

#### Live Demo Walkthrough Script:
> 1. **(Upload & Document Parsing - 0:45):**  
>    "Now, we transition directly to our working technical prototype. What you see on screen is our interactive decision-support application, designed for local deployment within the city council network. We begin by uploading a draft ordinance—here, a proposed measure regulating public utility tricycles."
> 
> 2. **(Hierarchical Section View - 0:45):**  
>    "The application immediately parses the draft into a structured, Reddit-style hierarchical tree. Legal researchers can collapse, expand, and inspect individual sections, clauses, and penalty provisions, making multi-page legislation effortless to navigate."
> 
> 3. **(Real-Time Audit & Conflict Detection - 0:45):**  
>    "When we initiate the statutory audit, Stage 1 searches across the 183,086 provisions in milliseconds, surfacing relevant sections from Republic Act 4136 and related city ordinances. Stage 2 immediately evaluates the pairs. Notice Section 5: the draft ordinance imposes an absolute municipal fine of 15,000 pesos. The system immediately flags a High-Confidence Contradiction!"
> 
> 4. **(Explainable Attention Heatmap & Export - 0:45):**  
>    "When we click 'Inspect Rationales,' the system displays the token-level cross-attention heatmap. It highlights the exact conflict: the draft's 15,000-peso fine directly violates Section 458 of Republic Act 7160, which caps municipal ordinance penalties at 5,000 pesos. Drafters can immediately export this finding into a formal Legislative Audit Report for committee review."

---

### Slide 19: Project Status, Administrative Routing & Next Steps
* **Speaker:** Ralph Paolo Dulce & Yahyah Odin
* **Top-Left Header:** Project Status & Roadmap
* **Bottom-Left Paper Ref:** §4.5, §5.2
* **Bottom-Right Slide:** Slide 19
* **Title:** Current Progress Summary & Next Steps
* **Visual:** Administrative routing workflow (Sangguniang Panlungsod $\rightarrow$ HRMO / City Administrator $\rightarrow$ 15 Legal Researchers $\rightarrow$ Civil Service 201 Commendation)

#### On-Screen Slide Content:
* Chapters 1 through 3 fully completed
* Dual statutory knowledge base fully assembled
* 183,086 provisions validated for transformer processing
* Two-stage coarse-to-fine architecture formally formulated
* Functional web application prototype completed
* SP endorsement received; routing via HRMO
* Human evaluation prepared with official commendations

#### Spoken Script:
> **(Ralph):**  
> "To summarize our progress: we have completed the full manuscript draft for Chapters 1 through 3, compiled and structured our dual statutory knowledge base of 27,357 enactments, formally defined our two-stage architecture, and developed a fully functioning interactive web prototype.
> 
> **(Yah):**  
> Regarding our immediate next steps: following the favorable endorsement from Sangguniang Panlungsod Acting Department Head Ma. Theresa Reyes, our formal approval packet is currently routing through the City Administrator's Office via HRMO. Once cleared, we will execute our human evaluation with the 15 city legal researchers, measuring usability and inter-annotator agreement, with official commendations awarded for their Civil Service 201 records.
> 
> That concludes our proposal defense presentation. Thank you very much, and we welcome the comments and guidance of our evaluation panel."

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
