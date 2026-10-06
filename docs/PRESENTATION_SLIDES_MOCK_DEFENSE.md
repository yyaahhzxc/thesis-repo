# Presentation Slides: Initial Presentation & Mock Defense
### Computer Studies Cluster, School of Arts and Sciences
### Ateneo de Davao University
**Course:** Bachelor of Science in Computer Science (BS CS)  
**Time Allotted:** 20 Minutes (Strict) | Target Presentation: ~16--17 mins + Q&A Buffer  
**Proponents:** Ralph Paolo Dulce & Yahyah Odin  
**Thesis Adviser:** Mr. Adrian "Ogs" Ablazo | **Professor:** Ma'am Grace Tacadao  

---

## Presentation Flow & Speaking Split

| Slide | Topic | Primary Speaker | Est. Time |
| :---: | :--- | :---: | :---: |
| **1** | Title & Introduction | Ralph | 1.0 min |
| **2** | Background: Legislative Inflation & Local Archives | Ralph | 1.5 mins |
| **3** | Legal Foundation: Magtajas Doctrine & Ex-Ante Auditing | Ralph | 1.5 mins |
| **4** | Statement of the Problem | Ralph | 1.5 mins |
| **5** | Objectives of the Study | Ralph | 1.5 mins |
| **6** | Conceptual Framework: Retrieve-Then-Entail | Ralph | 1.5 mins |
| — | *Speaker Transition Handoff* | Ralph $\rightarrow$ Yah | 10 secs |
| **7** | Methodology: Unified Dual Statutory Knowledge Base | Yah | 1.5 mins |
| **8** | Methodology: Coarse-to-Fine System Architecture | Yah | 1.5 mins |
| **9** | Methodology: Stage 1 Hybrid Retrieval & Rank Fusion | Yah | 1.5 mins |
| **10** | Methodology: Stage 2 NLI Cross-Encoder & XAI | Yah | 1.5 mins |
| **11** | Empirical Progress: Stage 1 Retrieval Benchmarks | Yah | 1.5 mins |
| **12** | Empirical Progress: Stage 2 NLI Screening & Fine-Tuning | Yah | 1.5 mins |
| **13** | **Live Technical System Demonstration** | Yah | 3.5 mins |
| **14** | Current Progress Summary, Administrative Routing & Next Steps | Ralph & Yah | 1.5 mins |

---

## Slide-by-Slide Presentation Content

---

### Slide 1: Title Slide
* **Speaker:** Ralph Paolo Dulce
* **Header:** Computer Studies Cluster, School of Arts and Sciences | Ateneo de Davao University
* **Title:** A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances
* **Subtitle:** Using Information Retrieval and Natural Language Inference
* **Visual:** Ateneo de Davao seal, thesis title banner, author credentials, adviser name

#### On-Screen Slide Content:
* Automated statutory conflict detection for local legislation
* Powered by hybrid information retrieval and cross-encoders
* Proactive **ex-ante evaluation** prior to formal enactment
* **Proponents:** Ralph Paolo Dulce & Yahyah Odin (BS Computer Science)
* **Adviser:** Mr. Adrian "Ogs" Ablazo | **Professor:** Ma'am Grace Tacadao

#### Spoken Script:
> "Good morning to the members of the evaluation panel, our thesis adviser Mr. Adrian Ablazo, and our course professor Ma'am Grace Tacadao. I am Ralph Paolo Dulce, and together with my co-author Yahyah Odin, we present our thesis entitled: *'A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference.'*
> 
> In this presentation, we will walk you through our legal motivation, core objectives, two-stage system architecture, empirical progress so far, and a live demonstration of our working prototype."

---

### Slide 2: Background: Legislative Inflation & Local Archives
* **Speaker:** Ralph Paolo Dulce
* **Header:** Chapter 1: Introduction | Background of the Study
* **Title:** Statutory Growth & Fragmented Local Archives
* **Visual:** Sample scan of a historical typewriter Davao City ordinance with faded ink and official seal stamps (`figs/sample_davao_city_ordinance_scan.png`)

#### On-Screen Slide Content:
* Rapid legislative expansion outpaces manual human review
* Historical local archives exist primarily as physical scans
* Scanner and typewriter noise degrade OCR accuracy
* Typographical errors break standard keyword search queries
* Latent contradictions create invalid local legislation

#### Spoken Script:
> "Every functional legal system requires statutory consistency so citizens clearly understand their obligations. However, the volume of modern legislation has grown so rapidly that human legal staff can no longer manually track every active rule.
> 
> In local government units like Davao City, this challenge is intensified. Historical ordinances dating back to 1950 are preserved mostly as physical typewriter scans. These documents suffer from faded ink, bleed-through, and overlapping seals. These optical errors break traditional keyword search tools. When legal researchers are overwhelmed by manual cross-referencing across multi-volume legal digests, latent conflicts can easily slip through into enacted law."

---

### Slide 3: Legal Foundation: Magtajas Doctrine & Ex-Ante Review
* **Speaker:** Ralph Paolo Dulce
* **Header:** Chapter 1: Introduction | Legal Motivation
* **Title:** The Magtajas Doctrine & Ex-Ante Auditing
* **Visual:** Diagram showing Philippine Legal Hierarchy: Constitution $\rightarrow$ National Statutes (Republic Acts) $\rightarrow$ Local Ordinances

#### On-Screen Slide Content:
* Local governments hold strictly delegated legislative powers
* *Magtajas Doctrine* voids ordinances that contradict national statutes
* An ordinance cannot prohibit what a statute permits
* **Ex-ante auditing** catches legal conflicts before enactment
* Aligns with **RA 11032** preventative regulatory review mandates

#### Spoken Script:
> "Under the Philippine legal system, local government units operate under delegated authority through the Local Government Code. The foundational doctrine established in *Magtajas v. Pryce Properties* dictates that a local ordinance cannot permit what a statute forbids, nor forbid what a statute permits. Any ordinance that contravenes a national statute is ultra vires and legally void.
> 
> Passing an invalid ordinance causes jurisdictional deadlocks, taxpayer lawsuits, and administrative waste. To prevent this, our study introduces an **ex-ante audit**—meaning an audit conducted 'before the event.' By auditing draft ordinances during committee review before their Second Reading, council staff can catch and fix conflicts while the text is still easily editable, fulfilling the preventative mandates of Republic Act 11032."

---

### Slide 4: Statement of the Problem
* **Speaker:** Ralph Paolo Dulce
* **Header:** Chapter 1: Introduction | Problem Statement
* **Title:** Statement of the Problem
* **Visual:** Checkpoint graphic highlighting the 5 research questions

#### On-Screen Slide Content:
* **Q1:** What linguistic parameters define semantic conflicts?
* **Q2:** How can Coarse-to-Fine retrieval scale on LGU hardware?
* **Q3:** Which hybrid IR and NLI combination maximizes accuracy?
* **Q4:** What is the empirical performance on legal ground-truth?
* **Q5:** How usable is the decision-support tool for SP legal staff?

#### Spoken Script:
> "To address these operational challenges, our research answers five specific questions:
> 
> First, what linguistic characteristics and deontic modal verbs define a true legal conflict? Second, how can a decoupled Coarse-to-Fine architecture retrieve relevant laws from tens of thousands of provisions on budget-constrained office hardware? Third, which combination of hybrid retrieval and natural language inference models delivers the highest accuracy? Fourth, what is the system's empirical performance when tested against verified legal conflict pairs? And fifth, how usable is the final decision-support tool for the legal researchers of the Davao City Sangguniang Panlungsod?"

---

### Slide 5: Objectives of the Study
* **Speaker:** Ralph Paolo Dulce
* **Header:** Chapter 1: Introduction | Objectives of the Study
* **Title:** Research Objectives
* **Visual:** Objective matrix showing mapped project deliverables

#### On-Screen Slide Content:
* **Obj 1:** Characterize legislative archive degradation and text noise
* **Obj 2:** Design a decoupled two-stage Coarse-to-Fine architecture
* **Obj 3:** Implement a hybrid IR and NLI system for Philippine law
* **Obj 4:** Evaluate conflict detection accuracy against ground truth
* **Obj 5:** Deploy an interactive decision-support web application

#### Spoken Script:
> "Our objectives directly align with these research questions. We identify the structural constraints and text noise across the local archive; we design an efficient Coarse-to-Fine pipeline that separates broad retrieval from deep inference; we implement and calibrate a hybrid IR and NLI system tailored to Philippine legal language; we evaluate detection reliability against verified ground truth; and finally, we deploy an interactive, user-friendly web interface that alerts legal researchers to potential conflicts in real time."

---

### Slide 6: Conceptual Framework: Retrieve-Then-Entail
* **Speaker:** Ralph Paolo Dulce
* **Header:** Chapter 2: Theoretical Framework | System Conceptualization
* **Title:** The Retrieve-Then-Entail Framework
* **Visual:** Conceptual framework flowchart (`figs/conceptual_framework_flowchart.png`)

#### On-Screen Slide Content:
* Adapts international **COLIEE benchmark** methodologies
* **Pillar 1:** *Magtajas* mapping (Statute = *Premise*, Draft = *Hypothesis*)
* **Pillar 2:** Decoupled Coarse-to-Fine computational pipeline
* **Pillar 3:** Transformer self-attention resolves contextual polysemy
* Delivers explainable, calibrated predictions for decision support

#### Spoken Script:
> "Our conceptual framework adapts the proven 'Retrieve-Then-Entail' methodology from the international Competition on Legal Information Extraction and Entailment (COLIEE). We structure our solution around three core pillars.
> 
> Pillar 1 maps the Magtajas Doctrine directly into Natural Language Inference, where the governing national law serves as the Premise, and the draft local ordinance serves as the Hypothesis. Pillar 2 decouples coarse candidate retrieval from compute-heavy inference so the system runs smoothly on local hardware. Pillar 3 uses Transformer self-attention to replicate Hermeneutic principles, interpreting words in their proper legal context.
> 
> I now hand the floor to my co-author Yahyah Odin to discuss our technical methodology, empirical progress, and live system demonstration."

---

### Slide 7: Methodology: Unified Dual Statutory Knowledge Base
* **Speaker:** Yahyah Odin
* **Header:** Chapter 3: Methodology | Data Pipeline
* **Title:** Unified Dual Statutory Knowledge Base
* **Visual:** Corpus composition and token length compliance chart (`figs/dual_corpus_transformer_compliance.png`)

#### On-Screen Slide Content:
* **27,096 total enactments** containing **176,421 searchable provisions**
* **25,432 national statutes** (1901–2026) from Lawphil
* **1,664 Davao City ordinances** (1950–2026) from Sangguniang Panlungsod
* Supports both **vertical preemption** and **horizontal coherence**
* **94.69% of provisions** comply with 512-token transformer limits

#### Spoken Script:
> "Thank you, Ralph. To evaluate proposed drafts against the full scope of Philippine law, we constructed the first Unified Dual Statutory Knowledge Base. This database compiles 27,096 enactments comprising 176,421 individual searchable provisions in standardized JSONL format.
> 
> This collection integrates 25,432 national statutes from 1901 to 2026 alongside 1,664 digitized Davao City ordinances across four legislative eras. This dual structure allows us to perform both vertical preemption checks against superior national laws and horizontal consistency checks against active city ordinances. Notably, 94.69% of all provisions naturally fit within standard 512-token transformer limits without needing aggressive chunking."

---

### Slide 8: Methodology: Coarse-to-Fine Architecture
* **Speaker:** Yahyah Odin
* **Header:** Chapter 3: Methodology | System Architecture
* **Title:** Decoupled Coarse-to-Fine Pipeline
* **Visual:** System architecture overview (`figs/JNLP_Framework_BW.png`)

#### On-Screen Slide Content:
* Comparing drafts against 176,421 provisions pairwise is intractable
* **Stage 1 (Coarse Retrieval):** High-throughput candidate filtering
* Filters full corpus down to a compact **top-50 shortlist** in milliseconds
* **Stage 2 (Fine Inference):** Deep pairwise cross-encoder evaluation
* Classifies pairs into **Entailment, Neutral, or Contradiction** offline

#### Spoken Script:
> "Evaluating every single provision in a multi-page draft against 176,421 statutory provisions using deep transformers would take hours and crash ordinary office computers.
> 
> To make this feasible on local LGU hardware, we decouple the pipeline into two stages. Stage 1 is Coarse Retrieval: it searches the entire corpus in milliseconds and returns the top-50 candidate provisions most likely to be relevant. Stage 2 is Fine Inference: a dedicated cross-encoder examines only those 50 candidate pairs, performing deep bidirectional attention to classify whether the pair is an Entailment, Neutral, or Contradiction. This two-stage design provides deep neural accuracy with sub-second execution speeds."

---

### Slide 9: Methodology: Stage 1 Hybrid Retrieval & Rank Fusion
* **Speaker:** Yahyah Odin
* **Header:** Chapter 3: Methodology | Retrieval Engine
* **Title:** Hybrid Search & Rank Fusion Algorithm
* **Visual:** Stage 1 retrieval flow diagram (`figs/Phase_1_Retrieval_BW.png`)

#### On-Screen Slide Content:
* **BM25:** Fast sparse search for exact statutory numbers and citations
* **all-MiniLM-L6-v2:** Dense bi-encoder for semantic paraphrasing
* **Reciprocal Rank Fusion ($k=60$):** Combines disparate rankings robustly
* **Hierarchy Priority Safeguard:** Prioritizes primary Republic Acts
* Achieves **1.26 ms mean latency** per query on consumer CPU

#### Spoken Script:
> "In Stage 1, pure keyword matching fails when a draft paraphrases a law, while pure vector embeddings can miss exact Republic Act numbers. We solve this by combining both in a hybrid pipeline.
> 
> We combine sparse BM25 with a lightweight 22-million parameter dense bi-encoder, `all-MiniLM-L6-v2`. Rather than attempting fragile score normalization, we aggregate their outputs using Reciprocal Rank Fusion with $k=60$, followed by a Hierarchy Priority Safeguard that gives precedence to superior Republic Acts. This stage executes in just 1.26 milliseconds on a standard Intel Core i3 CPU, ensuring that relevant governing laws are never missed."

---

### Slide 10: Methodology: Stage 2 NLI Cross-Encoder & XAI
* **Speaker:** Yahyah Odin
* **Header:** Chapter 3: Methodology | Inference & Explainability
* **Title:** Cross-Encoder NLI & Attention Explainability
* **Visual:** Stage 2 inference diagram (`figs/Phase_2_Entailment_BW.png`) showing token attention matrix

#### On-Screen Slide Content:
* Ingests concatenated premise-hypothesis pairs into a single tower
* Enables **full bidirectional cross-attention** between all tokens
* Overcomes affirmative entailment bias through supervised fine-tuning
* Calibrated three-class probability outputs for legal confidence
* Generates **token-level self-attention attribution heatmaps**

#### Spoken Script:
> "In Stage 2, candidate pairs pass into a single-tower Cross-Encoder. Unlike bi-encoders that encode sentences separately, a cross-encoder allows every word in the local draft to directly attend to every word in the statutory premise.
> 
> We fine-tune DeBERTa-v3 with disentangled position embeddings, training the model to overcome the affirmative bias common in general language models. Crucially, to make the system transparent and trustworthy for legal officers, the model extracts self-attention weights to generate token-level attribution heatmaps. This immediately highlights the exact conflicting phrases—such as an unauthorized fine or an absolute prohibition—giving legal staff an immediate, explainable audit trail."

---

### Slide 11: Empirical Progress: Stage 1 Retrieval Benchmarks
* **Speaker:** Yahyah Odin
* **Header:** Chapter 4: Results & Discussion | Retrieval Performance
* **Title:** Stage 1 Full-Corpus Retrieval & Ablation
* **Visual:** Retrieval performance curves across difficulty tiers (`figs/stage1_retrieval_ablation_performance.png`)

#### On-Screen Slide Content:
* Evaluated against full corpus of **25,432 national statutes** ($N=350$)
* Standalone BM25 achieves only **43.14% Recall@50**
* Rigid topic filtering causes catastrophic drop to **13.43% Recall@50**
* **Hybrid RRF ($k=60$)** achieves **100.0% Recall@50**
* Outperforms BM25 by **+17.3% on difficult Tier-3 paraphrased queries**

#### Spoken Script:
> "Looking at our empirical findings so far, our retrieval benchmarks across all 25,432 national statutes reveal important patterns. Traditional BM25 keyword search achieves only 43.14% Recall@50, missing over half of the governing laws due to vocabulary mismatch. Attempting to use rigid topic filters causes recall to collapse to 13.43% because major statutes span multiple legal subjects.
> 
> In contrast, our hybrid approach combining dense embeddings and BM25 via Reciprocal Rank Fusion reaches 100.0% candidate recall at top-50. On difficult Tier-3 queries where local drafts heavily paraphrase national laws, our dense retriever outperforms keyword search by 17.3 percentage points, guaranteeing no preemption candidates are dropped."

---

### Slide 12: Empirical Progress: Stage 2 NLI Screening & Fine-Tuning
* **Speaker:** Yahyah Odin
* **Header:** Chapter 4: Results & Discussion | Inference Performance
* **Title:** Cross-Encoder Fine-Tuning & Convergence
* **Visual:** Validation loss and Macro $F_1$ convergence trajectories (`figs/stage2_loss_dynamics_and_convergence.png`)

#### On-Screen Slide Content:
* Screened **28 scouted transformer architectures** zero-shot
* Fine-tuned **13 shortlisted encoders** across hyperparameter grids
* **DeBERTa-v3-base-NLI** achieves **89.47% Conflict $F_1$** (86.54% Val Acc)
* Statistically outperforms supervised BERT baseline ($p = 0.0388$)
* Stable convergence at **Epoch 3** with low **14.8 ms per pair latency**

#### Spoken Script:
> "In Stage 2, we conducted an empirical screening across 28 scouted transformer models. Unadapted models exhibited strong affirmative bias, frequently defaulting to Entailment or Neutral on direct statutory conflicts.
> 
> We shortlisted thirteen candidate encoders for supervised fine-tuning. DeBERTa-v3-base-NLI emerged as our top workhorse model, achieving an 89.47% Conflict F1 score and 86.54% validation accuracy. McNemar testing confirmed this improvement is statistically significant over the standard BERT baseline. As shown in our training curves, the models converge cleanly at Epoch 3 without overfitting. Running at just 14.8 milliseconds per pair, DeBERTa-v3 provides an ideal balance of high logical accuracy and fast local processing."

---

### Slide 13: Live Technical System Demonstration
* **Speaker:** Yahyah Odin
* **Header:** Prototype Demonstration | Interactive Decision-Support Tool
* **Title:** Live System Demonstration
* **Visual:** **LIVE SCREEN SHARE** of the interactive web prototype (Reddit-style hierarchical view, live retrieval, and XAI heatmap)

#### On-Screen Slide Content:
* Interactive decision-support web app for local LGU deployment
* Parses draft ordinances into **Reddit-style hierarchical section trees**
* Sub-second dual-corpus retrieval surfaces relevant candidate laws
* Real-time cross-encoder classifies normative conflicts
* Visualizes **token-level attention heatmaps** and exports audit reports

#### Live Demo Walkthrough Script:
> 1. **(Upload & Document Parsing - 0:45):**  
>    "Now, we transition directly to our working prototype. What you see on screen is our interactive decision-support application, designed for local deployment within the city council network. We begin by uploading a realistic draft ordinance—here, a proposed measure regulating local public utility tricycles."
> 
> 2. **(Hierarchical Section View - 0:45):**  
>    "The application immediately parses the draft into a structured, Reddit-style hierarchical tree. Legal researchers can collapse, expand, and inspect individual sections, clauses, and penalty provisions, making multi-page legislation effortless to navigate."
> 
> 3. **(Real-Time Audit & Conflict Detection - 1:00):**  
>    "When we initiate the statutory audit, Stage 1 searches across the 176,421 provisions in under 2 milliseconds, surfacing relevant sections from Republic Act 4136 and related city ordinances. Stage 2 immediately evaluates the pairs. Notice Section 5: the draft ordinance imposes an absolute municipal fine of 15,000 pesos. The system immediately flags a High-Confidence Contradiction!"
> 
> 4. **(Explainable Attention Heatmap & Export - 1:00):**  
>    "When we click 'Inspect Rationales,' the system displays the token-level cross-attention heatmap. It highlights the exact conflict: the draft's 15,000-peso fine directly violates Section 458 of Republic Act 7160, which caps municipal ordinance penalties at 5,000 pesos. Drafters can immediately export this finding into a formal Legislative Audit Report for committee review."

---

### Slide 14: Current Progress Summary, Administrative Routing & Next Steps
* **Speaker:** Ralph Paolo Dulce & Yahyah Odin
* **Header:** Project Status & Roadmap | Sangguniang Panlungsod Evaluation
* **Title:** Current Progress Summary & Next Steps
* **Visual:** Administrative routing diagram (Sangguniang Panlungsod $\rightarrow$ HRMO / City Administrator $\rightarrow$ 15 Legal Researchers $\rightarrow$ Civil Service 201 Commendation)

#### On-Screen Slide Content:
* Chapters 1 to 4 fully drafted; dual statutory knowledge base compiled
* Two-stage hybrid IR and cross-encoder pipeline built and benchmarked
* Functional, interactive web prototype completed with live demo
* Sangguniang Panlungsod endorsed study to City Administrator via HRMO
* Preparing human evaluation with 15 legal researchers and Civil Service 201 certs

#### Spoken Script:
> **(Ralph):**  
> "To summarize our progress so far: we have completed the full manuscript draft for Chapters 1 through 4, compiled and verified our dual statutory knowledge base of 27,096 enactments, benchmarked our hybrid retrieval and fine-tuned cross-encoders, and developed a fully functioning interactive web application.
> 
> **(Yah):**  
> As for our immediate next steps: following the favorable endorsement from Sangguniang Panlungsod Acting Department Head Ma. Theresa Reyes, our formal approval request is currently routing through the City Administrator's Office and HRMO. Once cleared, we will conduct our formal evaluation with 15 city legal researchers, measuring usability and inter-annotator agreement, with official commendations awarded for their Civil Service 201 records.
> 
> That concludes our presentation and progress report so far. Thank you very much, and we welcome your guidance and questions."

---

## Panel Q&A Quick Reference (Common General Inquiries)

### 1. "What is your main technical and practical contribution?"
* **Answer:** "Technically, we designed a computationally efficient Coarse-to-Fine pipeline that combines hybrid retrieval with fine-tuned cross-encoders to run deep conflict detection on consumer LGU computers without cloud dependencies. Practically, we built an ex-ante decision-support tool that helps local governments prevent legally void ordinances and protect citizens' constitutional rights before laws are enacted."

### 2. "Why not just use ChatGPT or a commercial cloud API?"
* **Answer:** "In a local government setting, cloud APIs have three major drawbacks: First, data privacy—uploading unapproved government drafts to commercial cloud servers raises compliance concerns under Republic Act 10173. Second, cost—recurring per-page API fees are unsustainable for municipal budgets. Third, reliability—cloud LLMs often suffer from affirmative bias and hallucination. Our open-weight models run 100% offline, cost nothing to operate, and provide transparent attention heatmaps."

### 3. "What is the status of your data and testing with actual legal staff?"
* **Answer:** "We have already compiled and structured 27,096 laws and 1,664 local ordinances. Our models are trained and benchmarked on verified legal ground truth. For the human evaluation, the Sangguniang Panlungsod has endorsed our study and referred it to the City Administrator through HRMO. We have prepared the testing packets and Google Forms, and we are ready to deploy the evaluation with 15 legal researchers as soon as administrative clearance is finalized."
