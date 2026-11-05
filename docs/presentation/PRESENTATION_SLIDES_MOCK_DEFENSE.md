# Presentation Slides: Initial Presentation & Mock Defense
### Computer Studies Cluster, School of Arts and Sciences
### Ateneo de Davao University
**Course:** Bachelor of Science in Computer Science (BS CS)  
**Time Allotted:** 20 Minutes (Strict) | Target Presentation: ~16--17 mins + Q&A Buffer  
**Proponents:** Ralph Paolo Dulce & Yahyah Odin  
**Thesis Adviser:** Mr. Adrian "Ogs" Ablazo, MSIT | **Professor:** Ma'am Grace Tacadao, MSIT  

---

## Presentation Flow & Speaking Split

| Slide | Topic | Primary Speaker | Slide Visual Type | Est. Time |
| :---: | :--- | :---: | :--- | :---: |
| **1** | Title Slide | Ralph | Metadata Banner & University Seal | 1.0 min |
| **2** | Background of the Study | Ralph | **Side-by-Side:** Authentic Scan (`figs/sample_davao_city_ordinance_scan.png`) + 7x7 Bullets | 1.5 mins |
| **3** | Objectives of the Study | Ralph to Yah | Bold Highlights (5 Specific Research Objectives) & Handoff | 1.0 min |
| **4** | Conceptual Framework | Yah | **Full Flowchart:** Complete System Architecture (`figs/conceptual_framework_flowchart.png`) | 1.0 min |
| **5** | Descriptive Analysis: Search Spaces | Yah | Text Layout: National Lawphil Baseline & 8 Legal Domains | 0.75 min |
| **6** | Model Design: Coarse-to-Fine Pipeline | Yah | Two-Column Text Layout: Stage 1 RRF & Stage 2 Cross-Encoder NLI | 1.0 min |
| **7** | Experimental Setup: Validation Design | Yah | Four-Pillar Grid: OCR vs VLM, Stage 1, Stage 2 Funnel & System Tiers | 1.0 min |
| **8** | Evaluation Metrics: Decision Criteria | Yah | Structured Matrix: Extraction, IR Ranking, NLI & Non-Parametric Tests | 0.75 min |
| **9** | Archival OCR & Local VLM Benchmark | Ralph | **Standalone Full-Screen Table 4.1:** Multi-Dimensional Benchmark (`figs/slide21_table4_1_ocr_benchmark.png`) | 1.5 mins |
| **10** | Dual Statutory Corpus Composition | Yah | **Parameters Table 4.6:** Comparative Search Spaces (`figs/slide26_dual_corpus_length_and_tokens.png`) | 1.0 min |
| **11** | Full-Corpus Candidate Retrieval | Yah | **Standalone Table 4.7:** Baseline Keyword Search across 25,432 Statutes | 0.75 min |
| **12** | Dense Bi-Encoder Selection | Yah | **Standalone Table 4.8:** Semantic Retrieval on 350 Ground-Truth Pairs | 0.75 min |
| **13** | Retrieval Architecture Ablation | Yah | **Standalone Table 4.9:** Hybrid Fusion Strategy Comparison | 0.75 min |
| **14** | Stage 2 Cross-Encoder NLI Benchmark | Yah | **Standalone Table 4.11 & 4.13:** Supervised Training & Validation F1 | 1.0 min |
| **15** | Decision Threshold & Statistical Rigor | Yah | **Statistical Validation:** Table 4.14 ($\\tau^* = 0.45$) & Friedman ANOVA (`figs/statistical_validation_model_comparison.png`) | 1.0 min |
| **16** | Real-World Jurisprudence & Edge Latency | Ralph | **Case Matrix Table 4.18:** 8 Supreme Court Decisions & Host A Latency (`figs/slide25_table4_17_latency_scaling.png`) | 1.0 min |
| **17** | **Live Technical System Demonstration** | Ralph & Yah | **Interactive Walkthrough:** Live Screen Share (`http://127.0.0.1:5050`) (`figs/prototype_conflict_accordion.png`) | 2.5 mins |
| **18** | Chapter 5: Conclusions & Synthesis | Ralph | **Scorecard Table:** Objectives 1 to 5 Completion Verification | 1.0 min |
| **19** | Recommendations of the Study | Ralph | Text Layout: 7 Actionable Technical & Institutional Directives | 1.0 min |
| **20** | Administrative Adoption & Next Steps | Ralph & Yah | **Routing Card:** SP Referral, HRMO Clearance & Civil Service 201 Commendation | 1.0 min |

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
* **Adviser:** Mr. Adrian "Ogs" Ablazo, MSIT | **Professor:** Ma'am Grace Tacadao, MSIT

#### Spoken Script:
> "Good morning to the members of the evaluation panel, our thesis adviser Mr. Adrian Ablazo, and our course professor Ma'am Grace Tacadao. I am Ralph Paolo Dulce, and together with my co-author Yahyah Odin, we present our undergraduate thesis entitled: *'A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference.'*
> 
> In this presentation, we will walk you through our legal motivation, research objectives, our unified conceptual framework, experimental methodology, and empirical experimental results."

---

### Slide 2: Background of the Study
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 1. Introduction
* **Bottom-Left Paper Ref:** §1.1
* **Bottom-Right Slide:** Slide 2
* **Title:** Background of the Study
* **Visual:** Side-by-Side: Authentic Archival Typewriter Scan (`figs/sample_davao_city_ordinance_scan.png`) on the left, 7x7 Motivation Bullets on the right

#### On-Screen Slide Content:
* Local ordinances cannot contradict national statutes
* Overlooked legal conflicts make ordinances void
* Thousands of laws overwhelm manual review
* Scanned local archives suffer OCR noise
* Missed conflicts trigger costly legal disputes
* Ex-ante auditing prevents invalid enacted laws

#### Spoken Script:
> "To understand why we built this system, imagine what happens when a city council drafts a new ordinance—for example, regulating local transportation, environmental protection, or setting municipal revenue fees.
> 
> Under Philippine constitutional law and the *Magtajas Doctrine*, local government units only possess delegated powers. An ordinance cannot permit what a national law prohibits, nor can it forbid what a national law allows. If a conflict slips through committee review, that local enactment is legally void from the moment it is signed.
> 
> But here is the operational dilemma: how can city legal officers verify that a new draft is completely compliant? Today, legal researchers must manually cross-reference thousands of pages of national codes dating back to 1901 alongside local city archives. And as shown on screen, historical ordinances exist as degraded scanned PDFs—full of typewriter noise, faded ribbons, and ink bleed that break standard search engines. When conflicts are missed, the result is costly court annulments. This motivates an **ex-ante audit**—evaluating drafts during First Reading to catch conflicts before enactment, leading directly into our five specific research objectives."

---

### Slide 3: Objectives of the Study
* **Speaker:** Ralph Paolo Dulce → Yahyah Odin
* **Top-Left Header:** Chapter 1. Introduction
* **Bottom-Left Paper Ref:** §1.3
* **Bottom-Right Slide:** Slide 3
* **Title:** Objectives of the Study
* **Visual:** Objectives Matrix with Bold Highlights and Speaker Handoff

#### On-Screen Slide Content:
The primary goal of this research is to develop a computationally efficient, two-stage semantic conflict detection system for proposed Davao City ordinances.

Specifically, this study aims to:
* **Objective 1:** **Investigate linguistic characteristics and structural constraints** of Davao City's legislative archive that contribute to semantic ambiguity and retrieval failure;
* **Objective 2:** **Design a Coarse-to-Fine computational pipeline** that decouples document retrieval from logical inference to optimize resource usage for local deployment;
* **Objective 3:** **Implement a hybrid Information Retrieval (IR) algorithm and Natural Language Inference (NLI)** system specifically calibrated for the Philippine legal hierarchy;
* **Objective 4:** **Evaluate system accuracy and computational efficiency** using domain-specific benchmarks and expert legal annotations; and
* **Objective 5:** **Develop a functional web application prototype** to support ex-ante legislative scrutiny within the Davao City Sangguniang Panlungsod.

#### Spoken Script:
> **(Ralph):**
> "To address these legal and computational challenges, this study formulates five specific research objectives:
> 
> First, **Objective 1 investigates the linguistic characteristics and structural constraints** of Davao City's legislative archive that contribute to retrieval failure on degraded historical scans.
> 
> Second, **Objective 2 designs a sovereign Coarse-to-Fine pipeline** that decouples high-throughput candidate retrieval from deep logical inference to run efficiently on commodity local government hardware.
> 
> Third, **Objective 3 implements a hybrid IR and cross-encoder NLI system** specifically calibrated for the Philippine legal hierarchy and the Magtajas preemption doctrine.
> 
> Fourth, **Objective 4 evaluates system reliability against a verified ground truth** of known legal conflicts to measure contradiction detection accuracy.
> 
> Finally, **Objective 5 develops a user-friendly decision-support web interface** for the Davao City Sangguniang Panlungsod to provide real-time conflict alerts.
> 
> **(Yah):**
> Thank you, Ralph. We now present the technical blueprint of our system, starting with our overall conceptual framework."

---

### Slide 4: Conceptual Framework
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.1
* **Bottom-Right Slide:** Slide 4
* **Title:** Conceptual Framework
* **Subtitle:** Two-Phase Retrieve-Then-Entail Architecture
* **Visual:** Full-Slide Display: Complete Conceptual Framework Flowchart (`figs/conceptual_framework_flowchart.png`) showing Phase 1 (Offline Foundation) and Phase 2 (Live Retrieve-Then-Entail Pipeline)

#### On-Screen Slide Content:
* Operationalizes the 'Retrieve-Then-Entail' legal AI framework
* **Phase 1 (Offline Foundation):**
  * Assembles dual statutory knowledge base (national & local)
  * Pre-computes hybrid BM25 and dense embedding indexes
  * Calibrates neural models and decision thresholds offline
* **Phase 2 (Live System Workflow):**
  * Stage 1: Fast hybrid retrieval narrows corpus to top-50 candidates
  * Stage 2: Deep cross-encoder NLI detects legal contradictions
  * Delivers token-level attention heatmaps & explainable verdicts

#### Spoken Script:
> "Moving to Chapter 3, our system operationalizes the 'Retrieve-Then-Entail' framework shown in our Conceptual Framework flowchart on screen.
> 
> Evaluating a proposed draft ordinance against hundreds of thousands of laws using deep transformers would crash standard office computers. To make automated conflict detection feasible for local government units, we decouple our workflow into two distinct operational phases.
> 
> On the left, **Phase 1 represents our Offline Foundation**. Here, we ingest and preprocess the dual statutory knowledge base—combining national statutes from Lawphil and 75 years of scanned Davao City ordinances—pre-compute hybrid search indexes, and benchmark neural models to establish optimal weights and thresholds.
> 
> On the right, **Phase 2 represents our Live System Workflow**. When a drafter inputs a proposed ordinance, the system extracts operative text, applies Stage 1 coarse retrieval to filter the search space down to the top-50 candidate provisions in milliseconds, and passes those pairs to Stage 2 cross-encoder inference for deep contradiction detection. Finally, it delivers transparent, token-level explainability to city council researchers before the draft is enacted into law."

---

### Slide 5: Descriptive Analysis: Statutory Search Spaces
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.2, §3.3, §3.4
* **Bottom-Right Slide:** Slide 5
* **Title:** Descriptive Analysis: Statutory Search Spaces
* **Subtitle:** Dual Corpus Acquisition, Lawphil Baseline, & Preliminary Parameters
* **Visual:** Clean 7x7 Text Layout (Search Space Scope & Methodological Rules)

#### On-Screen Slide Content:
* Compiles 25,432 national statutory enactments (1901–2025)
* Decomposes acts into 164,620 section-level provisions
* Partitions positive law into eight substantive legal domains
* Ingests 1,664 authentic Davao City enactments (SP & LISSP)
* Digitizes 75 years of municipal governance archives
* Detailed local distributions deferred to Chapter 4
* Unified search space ($N = 27,357$) established in Table 4.6

#### Spoken Script:
> "Moving from our conceptual framework to our descriptive analysis, we evaluate the statutory search spaces forming the foundation of our conflict detection pipeline.
> 
> For superior positive law, we acquired the Lawphil national archive, compiling **25,432 national statutory enactments**. Segmenting these acts at the natural section level yields **164,620 section-level national provisions**. Using TF-IDF and K-Means topic modeling, we **partition positive law into eight domains**—such as public finance, taxation, and general welfare—to ensure stratified coverage across all legislative areas.
> 
> In parallel, on the local level, we **ingest 1,664 authentic Davao City enactments** **sourced from Sanggunian portal and LISSP** archives spanning 75 years of municipal governance. Because our local digitizations underwent multi-era OCR cleaning and functional clustering under Objective 1, the **detailed local distributions are deferred to Chapter 4**, where the **final unified search space in Table 4.6** establishes our 27,357-enactment search corpus."

---

### Slide 6: Model Design: Two-Stage Coarse-to-Fine Pipeline
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.1, §3.6, §3.7
* **Bottom-Right Slide:** Slide 6
* **Title:** Model Design: Coarse-to-Fine Architecture
* **Subtitle:** Stage 1 Hybrid Retrieval & Stage 2 Cross-Encoder Inference
* **Visual:** Two-Column Architecture Comparison (Clean Text Layout)

#### On-Screen Slide Content:
* **Stage 1: Dual-Stream Hybrid Retrieval:**
  * Fuses Sparse BM25 (exact citations/fines) + Dense all-MiniLM-L6-v2
  * Merges rank lists via Reciprocal Rank Fusion ($k = 60$)
  * Filters 178k provisions down to top-50 candidates in 14.8 ms
  * Enforces statutory hierarchy safeguard under *Magtajas* doctrine
* **Stage 2: Cross-Encoder Natural Language Inference:**
  * Executes deep bidirectional token-to-token cross-attention
  * Fine-tuned DeBERTa-v3 cross-encoder running CPU inference
  * Calibrated threshold ($	au^* = 0.45$) penalizes false negatives 5:1
  * Symbolic integer rule enforces P5,000 fine ceiling (RA 7160 §458)

#### Spoken Script:
> "Next, we present our Model Design, which formalizes the two-stage Coarse-to-Fine retrieve-then-entail architecture shown on screen.
> 
> To circumvent the quadratic attention overhead that prevents full-corpus transformer evaluation, the system **decouples candidate retrieval from cross-attention inference**. In Stage 1, the pipeline **combines BM25 and all-MiniLM**: BM25 captures exact statutory citations and penalty numbers, while all-MiniLM captures latent semantic intent. The system **merges sparse-dense rankings via Reciprocal Rank Fusion**, rapidly **filtering 178k provisions down to top-50** candidate laws in under 15 milliseconds on a commodity 4-thread CPU.
> 
> In Stage 2, the pipeline **executes deep bidirectional cross-attention** over each candidate pair. It **employs DeBERTa-v3 with calibrated threshold** of tau equals 0.45, penalizing false negative conflicts 5-to-1 to protect the city against unlawful enactments under the *Magtajas* doctrine. Finally, Stage 2 **integrates a symbolic penalty integer ceiling checker** to guarantee 100% precision on local fines exceeding the statutory 5,000-peso cap under Section 458 of Republic Act 7160."

---

### Slide 7: Experimental Setup: Four-Pillar Validation Design
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.5, §3.6, §3.7, §3.10
* **Bottom-Right Slide:** Slide 7
* **Title:** Experimental Setup: Four-Pillar Validation Design
* **Subtitle:** Archival OCR, Stage 1 Retrieval, Stage 2 Inference, & System-Wide Tiers
* **Visual:** Four-Pillar Validation Grid (Clean Text Layout)

#### On-Screen Slide Content:
* **Pillar 1: Archival Document Ingestion:**
  * Compares Tesseract, Surya, Google Cloud Vision, and local 4-bit Qwen2.5-VL-3B
* **Pillar 2: Stage 1 Candidate Retrieval:**
  * Evaluates lexical search vs. dense bi-encoders across 350 ground-truth pairs
* **Pillar 3: Stage 2 Cross-Encoder Screening:**
  * 3-Level Funnel: Zero-Shot (28 models) → Supervised training (245 pairs) → 5-Fold Cross-Validation (105 test pairs)
* **Pillar 4: System-Wide Auditing Tiers:**
  * 3-Tier Suite: Tier 1 (350-pair cascaded FEVER) → Tier 2 (6 full draft ordinances) → Tier 3 (8 Supreme Court cases)

#### Spoken Script:
> "To ensure rigorous evaluation, our Experimental Setup is structured across four distinct experimental pillars.
> 
> In Pillar 1, our **OCR benchmark evaluates candidate extraction engines**, comparing Tesseract, Surya, and Google Cloud Vision against our offline 4-bit Qwen2.5-VL-3B on degraded historical scans. In Pillar 2, **Stage 1 retrieves over 350 pairs** across the entire dual statutory search space, evaluating raw lexical search against candidate bi-encoders.
> 
> In Pillar 3, Stage 2 follows a three-level screening funnel: **Stage 2 Level 1 tests zero-shot** inference across 28 pretrained models; **Stage 2 Level 2 trains cross-encoders** on 245 training pairs using AdamW and learning rate warmup; and **Stage 2 Level 3 executes cross-validation** with 5-fold testing on held-out test splits.
> 
> Finally, in Pillar 4, our system-wide evaluation operates across three tiers: **System Tier 1 measures cascaded FEVER** joint accuracy on 350 pairs; **System Tiers 2-3 audit full documents** across six typology-stratified draft ordinances with attached MOAs and Deeds, alongside eleven landmark Supreme Court jurisprudential cases."

---

### Slide 8: Evaluation Metrics: Quantitative Decision Criteria
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 3. Methodology
* **Bottom-Left Paper Ref:** §3.8, §3.9, §3.10
* **Bottom-Right Slide:** Slide 8
* **Title:** Evaluation Metrics: Quantitative Decision Criteria
* **Subtitle:** Extraction Fidelity, IR Ranking, Cost-Sensitive NLI, & Non-Parametric Tests
* **Visual:** Multi-Stage Metrics Matrix (Clean Text Layout)

#### On-Screen Slide Content:
* **Document Extraction Fidelity:**
  * Character Error Rate (CER), Word Error Rate (WER), Citation Entity Accuracy
* **Stage 1 Candidate Retrieval:**
  * Recall@k ($k \in \{5, 10, 20, 50\}$), Mean Reciprocal Rank (MRR), Query Latency (ms)
* **Stage 2 Cross-Encoder Classification:**
  * Validation Loss, Macro $F_1$, Contradiction $F_1$, Cost-Sensitive $F_2$ ($eta = 2.0$)
* **Statistical Significance Validation:**
  * Friedman Two-Way ANOVA by Ranks, Pairwise McNemar $\chi^2$ tests ($p < 0.05$)
* **System-Wide End-to-End Metrics:**
  * Joint FEVER Accuracy, Multi-Section Triage Specificity, Judicial Alignment Rate

#### Spoken Script:
> "Our Evaluation Metrics establish quantitative, objective criteria for each stage of the pipeline.
> 
> For archival extraction, our **OCR uses character and word errors** alongside cosine semantic fidelity, while verifying legal citation entity accuracy to ensure statutory numbers and section references remain uncorrupted.
> 
> For coarse retrieval, **Stage 1 measures recall and MRR** across depths k equals 5, 10, 20, and 50, alongside per-query CPU inference latency in milliseconds.
> 
> For fine inference, **Stage 2 measures cross-entropy loss** during training, evaluating macro and conflict F1 alongside cost-sensitive F2 to penalize preemption false negatives. To ensure algorithmic validity, **non-parametric tests verify cross-domain significance** using Friedman two-way ANOVA and pairwise McNemar chi-squared tests.
> 
> Finally, at the system level, our **system evaluation measures specificity and alignment**, evaluating full-document triage specificity on multi-section drafts and judicial ruling alignment on authentic Supreme Court cases."

---

### Slide 9: Archival OCR & Local VLM Benchmark
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 4. Results and Discussion
* **Bottom-Left Paper Ref:** §4.1, Table 4.1
* **Bottom-Right Slide:** Slide 9
* **Title:** Archival Ingestion: OCR & Local VLM Benchmark
* **Visual:** **Standalone Full-Screen Table 4.1** (`figs/slide21_table4_1_ocr_benchmark.png`) (Multi-Dimensional Extraction Benchmark)

#### On-Screen Slide Content:
* Table 4.1 compares extraction across degraded municipal archives
* Tesseract v5: 18.4% CER, 14.2% citation entity error
* Surya v0.6+: 8.1% CER, 4.3% citation entity error
* Cloud Vision: 2.15% CER, but incurs recurring API costs & cloud privacy risk
* Qwen2.5-VL-3B (4-bit NF4): 3.12% CER, 98.4% legal entity fidelity
* 100% offline edge deployment preserves sensitive government drafts

#### Spoken Script:
> "Moving to Chapter 4, Table 4.1 presents our empirical benchmark comparing four document extraction architectures on authentic Davao City archival scans.
> 
> Historical ordinances suffer from severe physical degradation—typewriter strike-throughs, carbon bleed, and manual rubber stamps. Standard open-source engines like Tesseract v5 struggle significantly, posting an 18.4 percent Character Error Rate and dropping 14.2 percent of statutory citations.
> 
> In contrast, our locally hosted 4-bit Qwen2.5-VL-3B-Instruct model achieves performance rivaling commercial cloud platforms—delivering a 3.12 percent CER, 98.4 percent legal entity accuracy, and 98.1 percent penalty accuracy. Crucially, by running locally in 4-bit precision within 2.8 GB of memory, it complies with Republic Act 10173 data privacy mandates and eliminates recurring cloud API fees."

---

### Slide 10: Dual Statutory Corpus Composition
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 4. Results and Discussion
* **Bottom-Left Paper Ref:** §4.1.10, Table 4.6
* **Bottom-Right Slide:** Slide 10
* **Title:** Unified Statutory Search Space
* **Subtitle:** Dual-Corpus Inventory & Structural Token Compliance
* **Visual:** **Standalone Table 4.6** (`figs/slide26_dual_corpus_length_and_tokens.png`) (Dual Corpus Search Space & Compliance Parameters)

#### On-Screen Slide Content:
* National Statutes (Lawphil): 25,432 enactments, 164,620 section provisions
* Davao City Ordinances: 1,925 enactments (1950–2025), 18,466 section provisions
* Complete Knowledge Base: 27,357 enactments, 183,086 searchable provisions
* Average provision length: 112.4 words (National) vs. 94.6 words (Local)
* **94.75% of provisions strictly comply with the 512-token transformer ceiling**
* Eliminates document truncation and prevents quadratic attention bottlenecks

#### Spoken Script:
> "Table 4.6 summarizes our unified dual statutory knowledge base, integrating 25,432 national statutes with 1,925 Davao City local ordinances spanning 1950 to 2025—totaling 27,357 enactments and 183,086 searchable section provisions.
> 
> As revealed in our document length analysis, legislative enactments exhibit massive structural asymmetry: whole acts span thousands of words, far exceeding transformer memory limits.
> 
> By executing natural section-level decomposition, our provisions achieve an average length of 112 words, with **94.75 percent of all provisions strictly complying with the 512-token context window**. This ensures that both Stage 1 dense encoders and Stage 2 cross-encoders operate without truncation or attention degradation."

---

### Slide 11: Full-Corpus Candidate Retrieval
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 4. Results and Discussion
* **Bottom-Left Paper Ref:** §4.2.1, Table 4.7
* **Bottom-Right Slide:** Slide 11
* **Title:** Stage 1 Full-Corpus Baseline Retrieval
* **Subtitle:** Keyword Search Scaling Across 25,432 Unindexed Statutes
* **Visual:** **Standalone Table 4.7** (Full-Corpus Baseline Retrieval Performance)

#### On-Screen Slide Content:
* Evaluates keyword retrieval across the entire 25,432-enactment statute base
* Raw BM25 baseline: 71.4% Recall@20, MRR = 0.412
* Ingesting entire enactments triggers severe term frequency saturation
* Adding Statutory Hierarchy Safeguard increases MRR to 0.584 (+41.7%)
* Prioritizes superior positive national statutes over historical local texts
* Proves necessity of dense semantic retrieval for non-exact paraphrases

#### Spoken Script:
> "Table 4.7 evaluates Stage 1 keyword search strategies when executed across the entire unindexed database of 25,432 national statutes.
> 
> Standard lexical search achieves 71.4 percent Recall at 20, but suffers from term saturation when legal terms appear across thousands of acts, yielding an MRR of 0.412.
> 
> In contrast, incorporating our **Statutory Hierarchy Safeguard** boosts Mean Reciprocal Rank to 0.584—a 41.7 percent relative improvement. By mathematically prioritizing governing national laws over municipal history, the system ensures preemption candidates surface to the top of the retrieval stack."

---

### Slide 12: Dense Bi-Encoder Selection
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 4. Results and Discussion
* **Bottom-Left Paper Ref:** §4.2.2, Table 4.8
* **Bottom-Right Slide:** Slide 12
* **Title:** Stage 1 Dense Bi-Encoder Selection
* **Subtitle:** Semantic Retrieval Benchmarking Across 350 Verified Legal Pairs
* **Visual:** **Standalone Table 4.8 Simplified** (Dense Retriever Benchmark)

#### On-Screen Slide Content:
* Evaluates 5 core bi-encoder architectures on 350 ground-truth pairs
* Legal-BERT bi-encoder: 88.6% Recall@20, 118 ms query latency
* BGE-Large: 96.0% Recall@20, but requires 1.34 GB RAM and 84 ms latency
* **all-MiniLM-L6-v2 Selected:**
  * **100.0% Recall@20 on clean statutory provisions**
  * **91.3% Recall@20 on Tier 3 semantically obscured conflicts**
  * 14.8 ms CPU latency (8x faster than Legal-BERT)
  * Tiny 80 MB footprint enables smooth deployment on 8 GB LGU desktops

#### Spoken Script:
> "Table 4.8 summarizes our empirical benchmark across candidate dense bi-encoder architectures evaluated on our 350-pair ground truth dataset.
> 
> While domain-specific models like Legal-BERT capture legal terminology, their 110-million-parameter footprint slows search latency to 118 milliseconds per query.
> 
> In contrast, our selected model, **all-MiniLM-L6-v2**, achieves **100 percent Recall at 20 on clean provisions** and **91.3 percent recall on difficult Tier 3 obscured conflicts**. Delivering 14.8-millisecond CPU query latency with an 80 MB memory footprint, all-MiniLM provides the ideal balance of recall and edge throughput."

---

### Slide 13: Retrieval Architecture Ablation
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 4. Results and Discussion
* **Bottom-Left Paper Ref:** §4.2.3, Table 4.9
* **Bottom-Right Slide:** Slide 13
* **Title:** Stage 1 Retrieval Architecture Ablation
* **Subtitle:** Hybrid Fusion Strategy Comparison on 350 Ground-Truth Pairs
* **Visual:** **Standalone Table 4.9 Simplified** (Retrieval Paradigm Ablation)

#### On-Screen Slide Content:
* BM25 Alone: 79.7% Recall@20, MRR = 0.512 (captures exact penalty numbers)
* Dense MiniLM Alone: 91.4% Recall@20, MRR = 0.638 (captures latent semantics)
* Linear Weighted Hybrid: 94.3% Recall@20, but requires ad-hoc score scaling
* **Reciprocal Rank Fusion (RRF, $k = 60$):**
  * **97.1% Overall Recall@20 (+17.4% over BM25)**
  * **MRR = 0.724 (+41.4% over BM25)**
  * Scale-invariant rank fusion eliminates score normalization artifacts

#### Spoken Script:
> "Table 4.9 presents our Stage 1 ablation benchmark, isolating the empirical performance of four distinct retrieval paradigms.
> 
> BM25 alone achieves 79.7 percent Recall at 20, excelling on exact statutory citations but failing on paraphrased concepts. Dense MiniLM alone reaches 91.4 percent recall, excelling on semantics but missing fine-grained numerical penalties.
> 
> Our proposed **Reciprocal Rank Fusion with constant k equal to 60** achieves the highest performance: **97.1 percent Recall at 20 and an MRR of 0.724**. By operating purely on positional ranks rather than unbounded scores, RRF reliably merges both search modalities."

---

### Slide 14: Stage 2 Cross-Encoder NLI Benchmark
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 4. Results and Discussion
* **Bottom-Left Paper Ref:** §4.3.1, §4.3.2, Tables 4.11 & 4.13
* **Bottom-Right Slide:** Slide 14
* **Title:** Stage 2 Cross-Encoder NLI Benchmark
* **Subtitle:** Pretrained Screening & Fine-Tuned Convergence on 350 Ground-Truth Pairs
* **Visual:** **Standalone Tables 4.11 & 4.13** (Model Screening & Supervised Metrics)

#### On-Screen Slide Content:
* Zero-shot foundation LLMs exhibit severe affirmative entailment bias (+39.7%)
* Pretrained MNLI models drop conflict recall below 60% on Philippine statutes
* **Supervised Fine-Tuning Convergence (DeBERTa-v3-base):**
  * Validation Loss decreases smoothly from 0.892 → 0.342 at Epoch 4
  * Macro $F_1$ increases from 0.548 → **0.884**
  * Contradiction $F_1$ achieves **0.916** on held-out test split
  * Outperforms RoBERTa-large, Legal-BERT, and standard MiniLM

#### Spoken Script:
> "In Section 4.3, we address Research Objectives 3 and 4 through our Stage 2 Natural Language Inference benchmark.
> 
> Zero-shot foundation LLMs fail in legal contradiction detection due to affirmative bias—assuming proposed drafts are compliant and missing 40 percent of actual conflicts.
> 
> By fine-tuning **DeBERTa-v3-base** on our verified Philippine legal dataset, validation loss converges smoothly to 0.342, achieving a **Macro F1 of 0.884 and a Contradiction F1 of 0.916**. DeBERTa's disentangled attention mechanism captures subtle semantic inversions between statutory mandates and local draft exceptions."

---

### Slide 15: Decision Threshold & Statistical Rigor
* **Speaker:** Yahyah Odin
* **Top-Left Header:** Chapter 4. Results and Discussion
* **Bottom-Left Paper Ref:** §4.3.3, §4.3.4, Tables 4.14, 4.15 & Figure 4.3
* **Bottom-Right Slide:** Slide 15
* **Title:** Threshold Calibration & Statistical Validation
* **Subtitle:** Cost-Sensitive Asymmetry ($\\tau^* = 0.45$) & Friedman ANOVA
* **Visual:** **Statistical Validation Card** (`figs/statistical_validation_model_comparison.png`) (Table 4.14 Sensitivity Sweep & Friedman Significance Bars)

#### On-Screen Slide Content:
* Standard 0.50 threshold allows 15 false negatives (unlawful ordinances enacted)
* Calibrated threshold **$\\tau^* = 0.45$** reflects 5:1 legal cost ratio ($C_{FN} / C_{FP} = 5.0$)
* Reduces false negatives from 15 → 9, boosting Contradiction Recall to **93.1%**
* Maintains strong 90.2% Precision with minimal false alarm burden
* **Friedman Two-Way ANOVA ($p < 0.001$):** Confirms significant superiority across all 8 legal domains
* Pairwise McNemar tests confirm DeBERTa outperforms all baselines ($p < 0.05$)

#### Spoken Script:
> "Because an undetected conflict results in a void municipal law, false negatives carry catastrophic legal costs compared to manageable false alarms.
> 
> In Table 4.14, lowering the decision threshold to **tau equals 0.45** reduces false negatives from 15 down to 9, increasing **Contradiction Recall to 93.1 percent** while preserving 90.2 percent precision.
> 
> Furthermore, non-parametric Friedman ANOVA across all eight legal domains confirms consistent cross-domain superiority with p less than 0.001, while pairwise McNemar tests confirm that DeBERTa-v3 significantly outperforms all baseline classifiers with p less than 0.05."

---

### Slide 16: Real-World Jurisprudence & Edge Latency
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 4. Results and Discussion
* **Bottom-Left Paper Ref:** §4.4, Tables 4.18, 4.21 & Host A Edge Profiling
* **Bottom-Right Slide:** Slide 16
* **Title:** Real-World Jurisprudence & Edge Profiling
* **Subtitle:** Historical Preemption Suite & Consumer Latency Validation
* **Visual:** **Table 4.18 Case Matrix & Scaling Curve** (`figs/slide25_table4_17_latency_scaling.png`) (8 Landmark Supreme Court Cases & Host A Latency)

#### On-Screen Slide Content:
* Validated against 8 landmark Supreme Court preemption cases
* Successfully detected **100% of historical statutory conflicts**
* Accurately replicates *Magtajas* (gambling), *Aerial Spraying*, and *Mining* rulings
* Evaluated on Host A (consumer LGU desktop: Intel Core i3, 8 GB RAM, no GPU)
* Stage 1 retrieval: 14.8 ms per query | Stage 2 inference: 1.84 s per pair
* Complete full-document audit finishes in **under 15 seconds**

#### Spoken Script:
> "In Section 4.4, we subjected our pipeline to real-world validation against 8 landmark Supreme Court preemption cases including *Magtajas*, *Batangas CATV*, and the *Davao City Aerial Spraying* ban. In all eight landmark decisions, our system successfully flagged the controlling national statutes and correctly identified the legal contradiction.
> 
> To prove municipal feasibility, all latency tests were conducted on Host A—an entry-level LGU desktop with an Intel Core i3 processor and 8 GB of RAM without a discrete GPU. Stage 1 retrieval finishes in 14.8 milliseconds, while Stage 2 cross-encoder classification averages 1.84 seconds per provision pair. A complete legislative draft is audited in under 15 seconds, making real-time screening practical during council committee hearings."

---

### Slide 17: Live Technical System Demonstration
* **Speaker:** Ralph Paolo Dulce & Yahyah Odin
* **Top-Left Header:** Chapter 4. Results and Discussion
* **Bottom-Left Paper Ref:** §4.5, Prototype System Walkthrough
* **Bottom-Right Slide:** Slide 17
* **Title:** Live Technical Demonstration
* **Subtitle:** Web Application Prototype (`http://127.0.0.1:5050`)
* **Visual:** Live Application Screen Share (`figs/prototype_conflict_accordion.png`) (Clean Full-Screen Workflow)

#### On-Screen Slide Content:
* [Interactive Demonstration: Live Browser Interface at `http://127.0.0.1:5050`]
* Ingests draft ordinance with multi-provision sections
* Displays real-time progress bar (Draft Parsing → Stage 1 RRF → Stage 2 NLI)
* Shows comparative side-by-side text accordion
* Highlights verbatim statutory excerpts without synthetic rewriting
* Color-coded verdict badges: Contradiction (Red), Entailment (Green), Neutral (Gray)
* Integrates symbolic penalty ceiling checker (P5,000 fine warning)

#### Spoken Script:
> **(Ralph):**
> "We now transition to a live demonstration of our working web application prototype running locally at port 5050. The interface is tailored specifically for First Reading committee reviews by council researchers.
> 
> As you can see, when a legal officer uploads a new proposed ordinance, the system parses the document into natural section provisions.
> 
> **(Yah):**
> Upon clicking 'Analyze Draft', Stage 1 instantly queries our unified dual corpus, pulling the top candidate statutes using Reciprocal Rank Fusion. Stage 2 cross-encoders then classify the logical relationship, evaluating whether the proposed language permits an act prohibited by national law.
> 
> **(Ralph):**
> Drafters can inspect the side-by-side comparative text accordion, review verbatim statutory provisions without editorial pollution, and inspect token-level attention highlights showing exactly where the conflict originates. This provides council attorneys with instant, explainable decision support."

---

### Slide 18: Chapter 5: Conclusions & Synthesis
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 5. Conclusions and Recommendations
* **Bottom-Left Paper Ref:** §5.1, Table 5.1
* **Bottom-Right Slide:** Slide 18
* **Title:** Conclusions: Research Objectives Synthesis
* **Subtitle:** Empirical Validation of Objectives 1 through 5
* **Visual:** **Objectives Completion Scorecard Table** (Objectives 1–5 Verification)

#### On-Screen Slide Content:
* **Objective 1 (Corpus Constraints):** Characterized 75-year archive; 4-bit VLM achieved 3.12% CER; 94.75% 512-token compliance
* **Objective 2 (Pipeline Design):** Decoupled Coarse-to-Fine architecture; filters 178k provisions down to top-50 in 14.8 ms
* **Objective 3 (Algorithm Implementation):** Hybrid RRF ($k = 60$) achieved 97.1% Recall@20; DeBERTa-v3 achieved 0.916 Contradiction $F_1$
* **Objective 4 (System Accuracy & Efficiency):** 100% replication of Supreme Court landmark cases; sub-15s full-document edge audit
* **Objective 5 (Prototype Deployment):** Operationalized zero-editorial web prototype with XAI attention heatmaps

#### Spoken Script:
> "We conclude our defense with Chapter 5. As synthesized in Section 5.1, our thesis successfully accomplished all five specific research objectives.
> 
> Under Objective 1, we established that section-level decomposition enables 94.75 percent transformer compliance, while local 4-bit VLMs solve historical scan noise. Under Objective 2, our Coarse-to-Fine pipeline decoupled candidate retrieval from deep cross-attention, making municipal scaling computationally possible.
> 
> Under Objectives 3 and 4, our hybrid RRF retriever delivered 97.1 percent candidate recall, while our fine-tuned cross-encoder reached an F1 score of 0.916 and replicated 100 percent of Supreme Court preemption rulings.
> 
> Finally, under Objective 5, we integrated our two-stage architecture into a functional edge web prototype, providing council staff with explainable, real-time legislative decision support."

---

### Slide 19: Recommendations of the Study
* **Speaker:** Ralph Paolo Dulce
* **Top-Left Header:** Chapter 5. Conclusions and Recommendations
* **Bottom-Left Paper Ref:** §5.2
* **Bottom-Right Slide:** Slide 19
* **Title:** Recommendations & Future Technical Roadmap
* **Subtitle:** Concrete Directives for Local Government & AI Research
* **Visual:** Clean 7x7 Technical & Institutional Recommendations Layout

#### On-Screen Slide Content:
* 1. Institutionalize ex-ante semantic conflict screening during First Reading committee reviews
* 2. Mandate local 4-bit vision-language models for historical document digitization
* 3. Integrate automated penalty integer verification to enforce statutory fine ceilings
* 4. Implement dynamic corpus versioning to continuously track statutory repeals and amendments
* 5. Extend conflict detection to horizontal conflicts across neighboring municipal ordinances
* 6. Develop word-level visual conflict heatmaps highlighting problematic phrases in draft text
* 7. Maintain offline-first sovereign edge deployments to protect municipal data privacy

#### Spoken Script:
> "Section 5.2 outlines our study's concrete recommendations for local legislative bodies and technical researchers.
> 
> First, we recommend institutionalizing automated ex-ante conflict screening during First Reading, preventing void measures before significant public funds are committed to legislative debate.
> 
> Second, local government digitization units should adopt 4-bit vision-language models like Qwen2.5-VL to transcribe historical archives accurately without recurring cloud costs.
> 
> Technically, future research should integrate dynamic versioning to track statutory repeals in real time, expand the system to audit horizontal conflicts across neighboring local ordinances, and generate word-level heatmaps directly highlighting problematic text phrases.
> 
> Above all, local government AI deployments should remain strictly offline and on-premise, guaranteeing data sovereignty and privacy compliance under Philippine law."

---

### Slide 20: Administrative Adoption & Next Steps
* **Speaker:** Ralph Paolo Dulce & Yahyah Odin
* **Top-Left Header:** Chapter 5. Conclusions and Recommendations
* **Bottom-Left Paper Ref:** §5.3, Appendix K & Appendix O
* **Bottom-Right Slide:** Slide 20
* **Title:** Administrative Adoption & Institutional Roadmap
* **Subtitle:** Sangguniang Panlungsod Referral & Civil Service 201 Recognition
* **Visual:** **Administrative Routing Card** (`figs/annotator_certificate_of_contribution.png`) & Clearance Protocol

#### On-Screen Slide Content:
* Official SP endorsement received from Acting Department Head II Ma. Theresa A. Reyes
* Clearance packet routed through City Administrator's Office via HRMO
* 15 SP legal researchers prepared to execute 70-pair human evaluation protocol
* Official Certificate of Contribution approved by course professor Ma'am Grace Tacadao
* Formally structured for inclusion in legal staff Civil Service 201 personnel records
* Bridges cutting-edge computer science research with municipal governance empowerment

#### Spoken Script:
> **(Ralph):**
> "Regarding administrative adoption and institutionalization, our study received an official endorsement from Sangguniang Panlungsod Acting Department Head II Ma. Theresa A. Reyes, who recognized the critical need for automated conflict detection. In accordance with city protocol, our formal research clearance packet is currently being routed through the City Administrator's Office via the Human Resource Management Office.
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
