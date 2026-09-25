# **Thesis Terminology & Conceptual Glossary**

**Project:** *A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference*  
**Authors:** Ralph Paolo Dulce & Yahyah Odin  
**Adviser:** Mr. Adrian "Ogs" Ablazo | **Professor:** Ma'am Grace Tacadao  
**Institution:** Ateneo de Davao University, Department of Computer Science  

---

## **About This Document**
This glossary provides plain-language definitions, mathematical intuition, and practical thesis context for all technical, legal, statistical, and machine learning terms used across the thesis manuscript and codebase. It is designed to serve as a quick, authoritative reference for the authors during drafting, coding, adviser consultations, and thesis defense.

---

## **Table of Contents**
1. [Legal, Constitutional & Local Government Concepts](#1-legal-constitutional--local-government-concepts)
2. [Stage 1: Information Retrieval (IR) & Coarse Filtering](#2-stage-1-information-retrieval-ir--coarse-filtering)
3. [Stage 2: Natural Language Inference (NLI) & Deep Reasoning](#3-stage-2-natural-language-inference-nli--deep-reasoning)
4. [Machine Learning Training & Optimization (The "Dials")](#4-machine-learning-training--optimization-the-dials)
5. [Evaluation Metrics & Decision Calibration](#5-evaluation-metrics--decision-calibration)
6. [Statistical Hypothesis Testing (Comparing Models)](#6-statistical-hypothesis-testing-comparing-models)
7. [System Architecture, Software Engineering & Reproducibility](#7-system-architecture-software-engineering--reproducibility)
8. [Ground Truth Benchmark & Human Annotation Protocol](#8-ground-truth-benchmark--human-annotation-protocol)

---

## **1. Legal, Constitutional & Local Government Concepts**

### **Ex-Ante vs. Ex-Post**
* **Plain Meaning:** *Before* the fact vs. *after* the fact.
* **In This Thesis:** Our system is strictly **ex-ante**—it evaluates *draft* city ordinances **before** they are enacted into law by the City Council to prevent legal conflicts in advance. This is the opposite of **ex-post** analysis, which happens *after* a law is already enacted (e.g., when citizens challenge it in court years later).

### **Sangguniang Panlungsod (SP)**
* **Plain Meaning:** The City Council (the local legislative body of a city).
* **In This Thesis:** The Davao City Sangguniang Panlungsod is our primary partner and beneficiary. Their 15 legal researchers will provide the human Ground Truth annotations, and their legislative archives (~1,500 local ordinances) form our local dataset.

### **Local Government Code of 1991 (Republic Act No. 7160)**
* **Plain Meaning:** The national law that gives Philippine cities, provinces, and municipalities the authority to govern themselves (devolved autonomy) and pass local ordinances.
* **In This Thesis:** RA 7160 defines what the City Council is allowed to do. However, Section 5(a) also affirms that local laws must remain consistent with national laws.

### **Magtajas v. Pryce Properties Doctrine (1994)**
* **Plain Meaning:** The Supreme Court ruling (*G.R. No. 111097*) establishing the strict hierarchy of Philippine laws.
* **The Rule:** A local city ordinance is subordinate to national statutes passed by Congress. An ordinance **cannot prohibit what a national statute permits**, nor **permit what a national statute prohibits**. If it does, the ordinance is invalid and void (*ultra vires*).

### **Ultra Vires**
* **Plain Meaning:** Latin for "beyond the powers."
* **In This Thesis:** Refers to an ordinance or provision passed by the City Council that exceeds its legal authority because it directly conflicts with a national law or constitutional mandate.

### **Types of Philippine National Statutes**
* **Republic Acts (RA):** Laws passed by the Philippine Congress from 1946–1972 and 1987–present (e.g., RA 7160).
* **Batas Pambansa (BP):** Laws passed by the interim/regular Batasang Pambansa parliament (1978–1986).
* **Presidential Decrees (PD):** Laws enacted by presidential decree during Martial Law (1972–1986), which have the force of national statutes.
* **Commonwealth Acts (CA) & Acts:** Historical statutes passed from 1900–1946 that remain active unless repealed.
* **In This Thesis:** Our national corpus contains **25,432** cleaned national laws spanning all of these statutory categories.

### **Dual Statutory Corpus**
* **Plain Meaning:** A two-part legal dataset combining national laws and local ordinances.
* **In This Thesis:** The national corpus of **25,432** statutes is only one part of the story! The complete knowledge base integrates both the national laws and the **~1,500** Davao City local ordinances (being cleaned and digitized by Ralph), totaling **over 27,000+ legal enactments**. This ensures the system can detect conflicts across both jurisdictional levels.

### **Vertical Conflict Detection (Statutory Preemption)**
* **Plain Meaning:** Checking if a city ordinance clashes with a superior national law passed by Congress or the President.
* **In This Thesis:** Under the *Magtajas v. Pryce Properties* doctrine and RA 7160 §5(a), an ordinance cannot permit what a national statute forbids, or forbid what a national statute permits. Vertical conflict detection ensures local legislation conforms to higher-tier national mandates.

### **Horizontal Conflict Detection (Intra-Jurisdictional Coherence)**
* **Plain Meaning:** Checking if a new draft ordinance clashes with, duplicates, or contradicts an existing local ordinance within the same city.
* **In This Thesis:** A draft ordinance cannot conflict with fellow Davao City ordinances. If the City Council has already enacted a comprehensive ordinance on a subject (e.g., the Davao City Children's Welfare Code or Liquor Ban), a new draft must maintain horizontal coherence to avoid contradictory penalties, overlapping regulations, or unintentional implied repeals.

### **Single-Premise Rule**
* **Plain Meaning:** Evaluating a draft local ordinance provision against **one** statutory provision at a time.
* **In This Thesis:** Instead of asking an AI to simultaneously digest a web of 10 different laws at once (which causes severe hallucinations and requires massive cloud servers), our pipeline pairs each candidate draft section with a single statutory section. This keeps inference fast, mathematically sound, and executable on standard local office hardware.

### **Dual Legislative Heritage (Civil Law Codification & Anglo-American Drafting)**
* **Plain Meaning:** The unique historical blend of Spanish Continental civil law structure (systematic, abstract codification) and American common law legislative drafting (highly technical, verbose, enumerative administrative provisions).
* **In This Thesis:** Philippine statutes inherit both styles. Foundational codes (Civil Code, Local Government Code) use dense, high-level abstract principles, while modern regulatory Republic Acts and municipal ordinances use granular, clause-heavy sentences with multi-condition qualifiers ("Provided, that...", "Notwithstanding..."). Our tokenization, structural section chunking, and cross-attention models are specifically tailored to parse this complex syntactic blend.

---

## **2. Stage 1: Information Retrieval (IR) & Coarse Filtering**

### **Coarse-to-Fine Pipeline**
* **Plain Meaning:** A two-step funnel: first use a fast, broad net to narrow down thousands of documents to a handful (Coarse), then use a slow, highly intelligent model to examine only that handful in extreme detail (Fine).
* **In This Thesis:** 
  * *Stage 1 (Coarse IR):* Rapidly searches 25,432 national laws in seconds to find the **top-$k$** (e.g., top 10) most relevant candidates.
  * *Stage 2 (Fine NLI):* Runs deep neural logic on just those 10 candidates to detect whether any of them contradict the draft ordinance.

### **Information Retrieval (IR)**
* **Plain Meaning:** The science of searching for relevant documents or passages inside a large database based on a user's query (like a search engine).

### **Sparse Retrieval vs. Dense Retrieval**
* **Sparse Retrieval (Keyword-based):** Looks for exact word matches (e.g., searching "tricycle fare" finds texts containing the words "tricycle" and "fare"). High speed, zero GPU required, but fails if different words are used (e.g., "three-wheeled public utility vehicle tariff").
* **Dense Retrieval (Semantic-based):** Converts text into mathematical vectors (embeddings) using neural networks. Matches texts based on conceptual meaning even if they use completely different words. Requires more compute.

### **BM25 (Best Matching 25)**
* **Plain Meaning:** An advanced, industry-standard formula for keyword search. It improves on basic word counts by taking into account document length and word saturation (mentioning a word 20 times isn't 20 times more relevant than mentioning it 5 times).
* **In This Thesis:** BM25 serves as our **Stage 1 baseline retrieval model**.

### **TF-IDF (Term Frequency-Inverse Document Frequency)**
* **Plain Meaning:** A basic statistical score showing how important a word is to a specific document relative to an entire collection. Common words like "the" or "section" get very low scores, while rare words like "curfew" get high scores.

### **SVD (Singular Value Decomposition) & LSA**
* **Plain Meaning:** A mathematical matrix factorization technique that compresses thousands of word counts down into a smaller set of hidden "concepts" (Latent Semantic Analysis).
* **In This Thesis:** Used in our exploratory analysis to discover latent legal topics across the 25,432 national laws. Because factoring a 25,432-document matrix is memory-intensive, we run this in Google Colab Pro.

### **Bi-Encoder (Dual-Encoder)**
* **Plain Meaning:** A neural architecture that encodes the draft ordinance and the national law **separately** into vectors, then compares them using dot product or cosine similarity.
* **In This Thesis:** Used in Stage 1 because you can pre-calculate and store the vectors for all 25,432 national laws ahead of time, allowing instant sub-second searching.

### **Cosine Similarity**
* **Plain Meaning:** A mathematical metric between $-1.0$ and $+1.0$ (or $0.0$ to $1.0$) measuring the angle between two vectors. An angle of 0 degrees ($\text{similarity} = 1.0$) means the two texts have identical semantic direction in embedding space.

### **Hit@$k$ & Recall@$k$**
* **Plain Meaning:** The percentage of test queries where the truly relevant legal statute appeared somewhere in the top-$k$ returned results (e.g., top 5 or top 10).
* **In This Thesis:** If the system achieves Recall@10 = 92%, it means in 92 out of 100 cases, the conflicting national statute was successfully caught in Stage 1's 10-candidate shortlist.

### **MRR@$k$ (Mean Reciprocal Rank)**
* **Plain Meaning:** A metric that rewards the search engine for putting the correct law at the very top of the list. If the correct law is ranked #1, it gets a score of $1/1 = 1.0$. If it is ranked #2, it gets $1/2 = 0.5$. If ranked #5, it gets $1/5 = 0.2$.

### **Statutory Chunking (Provision-Level Granularity)**
* **Plain Meaning:** Splitting massive legal documents into manageable pieces.
* **In This Thesis:** Instead of feeding an entire 100-page Republic Act into the model at once, we split statutes at the **Section / Article level**. In Philippine law, each section acts as a self-contained rule with its own conditions and penalties.

### **Reciprocal Rank Fusion (RRF)**
* **Plain Meaning:** A ranking formula that merges results from multiple search systems (like BM25 keyword search and Bi-Encoder vector search) using only their rank positions rather than arbitrary raw scores: $\text{RRF}(d) = \sum \frac{1}{k_{\text{rrf}} + \text{rank}(d)}$.
* **In This Thesis:** RRF with smoothing constant $k_{\text{rrf}} = 60$ fuses the top-100 BM25 list and the top-100 MiniLM dense vector list into a single unified top-50 shortlist, achieving 100.0% candidate Recall@50 without requiring fragile score normalization.

### **Hierarchy Priority Safeguard ($\beta$ Multiplier)**
* **Plain Meaning:** An algorithmic safeguard that boosts the search rank of primary congressional legislation over subordinate administrative clutter.
* **In This Thesis:** In our 25,432 national corpus, 48% of documents are administrative executive orders that share generic administrative vocabulary. A multiplicative boost factor ($\beta = 1.15$) is applied to primary enactments (Republic Acts), preventing administrative issuances from pushing critical governing codes out of the top-$k$ candidate pool and elevating MRR by +45.8%.

---

## **3. Stage 2: Natural Language Inference (NLI) & Deep Reasoning**

### **Natural Language Inference (NLI)**
* **Plain Meaning:** An NLP task where a model reads two texts—a **Premise ($P$)** and a **Hypothesis ($H$)**—and decides the logical relationship between them.
* **The Three NLI Classes:**
  1. **Entailment:** The premise guarantees the hypothesis is true (the ordinance complies with or aligns with national law).
  2. **Contradiction:** The premise and hypothesis cannot both be true simultaneously (the ordinance conflicts with or violates national law).
  3. **Neutral:** The premise neither confirms nor contradicts the hypothesis (they cover different topics or do not logically clash).

### **Premise and Hypothesis in Our Pipeline**
* **Premise ($P$):** The national statutory provision (the established, supreme law passed by Congress).
* **Hypothesis ($H$):** The draft local ordinance section (the proposed rule whose validity is being tested).

### **Cross-Encoder**
* **Plain Meaning:** A neural architecture that feeds **both the Premise and the Hypothesis together** into the transformer at the exact same time, separated by a `[SEP]` token: `[CLS] Premise [SEP] Hypothesis [SEP]`.
* **Why It Matters:** Unlike Bi-Encoders (which look at texts separately), a Cross-Encoder allows every single word in the ordinance to directly cross-examine every single word in the national statute through all attention layers. This makes it far more accurate at detecting subtle legal contradictions, though it is computationally heavier.

### **Self-Attention & Cross-Attention**
* **Self-Attention:** The transformer mechanism allowing words within the same sentence to connect to one another (e.g., linking the pronoun "it" to the noun "ordinance").
* **Cross-Attention:** When the model compares words between the two different texts (e.g., linking the word "prohibited" in the national statute directly to "permitted" in the ordinance).

### **Token & Subword Tokenization**
* **Plain Meaning:** The basic unit of text that a neural network reads. Words are split into common syllables or words called tokens (e.g., "ordinance" $\rightarrow$ 1 token, "unconstitutional" $\rightarrow$ 3 tokens: "un", "constitut", "ional"). On average, 100 English words $\approx$ 130 tokens.

### **Context Window / Maximum Sequence Length**
* **Plain Meaning:** The maximum number of tokens a model can process at once.
* **In This Thesis:** The standard transformer context limit is **512 tokens**. In our corpus analysis, **94.83%** of all Philippine statutory sections fit within 512 tokens. For the remaining 5.17% unusually long sections, we evaluate **ModernBERT** (which supports up to 8,192 tokens).

### **Candidate Transformer Models**
* **BERT (Devlin et al., 2019):** The foundational bidirectional transformer model.
* **RoBERTa (Liu et al., 2019):** An optimized version of BERT trained on more data with dynamic masking. `roberta-large-mnli` serves as our canonical unadapted zero-shot baseline from COLIEE Task 4 literature (Rabelo et al., 2022).
* **DeBERTa-v3 (He et al., 2021):** Features "disentangled attention" (evaluating a word's meaning and its relative position separately), making it exceptionally strong at subtle grammatical nuances like "shall" vs. "may".
* **ModernBERT (Warner et al., 2024):** A state-of-the-art 2024 architecture featuring FlashAttention-2, native rotary embeddings (RoPE), and support for up to 8,192 tokens.
* **LEGAL-BERT (Chalkidis et al., 2020):** A domain-specific encoder pretrained from scratch on 12GB of European and US legal and statutory corpora with a specialized legal vocabulary.
* **Pile-of-Law BERT (Henderson et al., 2022):** A 340M-parameter model pretrained on a 256GB corpus of administrative codes, statutory enactments, and municipal regulations.
* **BGE-Reranker-v2-m3 (Xiao et al., 2024):** A multilingual cross-encoder supporting 8,192 tokens, pretrained on hard-negative pairs and evaluated in COLIEE 2025/2026.

### **Disentangled Attention (DeBERTa-v3)**
* **Plain Meaning:** Representing each word using two separate vectors: one vector for its semantic content, and a separate vector for its relative position in the sentence.
* **In This Thesis:** Unlike standard BERT which sums word and position vectors into a single vector, DeBERTa-v3 calculates attention using disentangled matrices (content-to-content, content-to-position, and position-to-content). This enables precise sensitivity to legal qualifiers ("provided that", "shall not", "unless otherwise specified") where the relative syntactic position of conditions alters deontic meaning.

### **Unpadded Sequence Packing & FlashAttention-2 (ModernBERT)**
* **Plain Meaning:** Eliminating wasteful padding tokens by concatenating variable-length sentences into a single continuous tensor, and accelerating exact attention computation directly inside GPU SRAM.
* **In This Thesis:** Standard transformers pad shorter statutory sections with dummy `[PAD]` tokens up to the maximum batch length, wasting compute. ModernBERT uses unpadded sequence packing with FlashAttention-2, allowing efficient 8,192-token context windows without quadratic memory spikes.

### **LexGLUE Benchmark (Legal General Language Understanding Evaluation)**
* **Plain Meaning:** The gold-standard collection of legal NLP benchmark datasets (CaseHOLD, SCOTUS, EUR-LEX, ECtHR, etc.) used to evaluate whether language models understand specialized legal and statutory syntax (Chalkidis et al., 2022).

### **NLI Pre-Alignment (Warm Logical Initialization)**
* **Plain Meaning:** Starting fine-tuning from a model checkpoint that was already fine-tuned on large general NLI datasets (MNLI, FEVER, ANLI) rather than starting from raw Masked Language Model (MLM) weights.
* **In This Thesis:** Models like `MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli` already possess pre-trained sensitivity to logical negation and contradiction. Fine-tuning them on our 245-pair Philippine ground truth dataset adapts their logic to statutory vocabulary without requiring the classification head to learn the definition of "contradiction" from scratch.

### **Replaced Token Detection (RTD)**
* **Plain Meaning:** A pretraining objective used by ELECTRA where a generator replaces some words and a discriminator must predict whether each word in the sequence is original or replaced.
* **In This Thesis:** Unlike standard BERT which only learns from 15% masked words per sentence, RTD trains across 100% of tokens in every input, resulting in exceptionally high sample efficiency when fine-tuning on small datasets ($N_{\text{train}} = 245$).

### **Explainable AI (XAI) & Attention Heatmaps**
* **Plain Meaning:** Making the model's inner reasoning transparent to humans without generating hallucinated summaries.
* **In This Thesis:** The system extracts the actual self-attention weights from the final transformer layer and highlights the exact conflicting word spans in yellow/red on the screen (e.g., highlighting *"shall not exceed 5,000 pesos"* in the national law vs. *"fine of 10,000 pesos"* in the draft ordinance).

---

## **4. Machine Learning Training & Optimization (The "Dials")**

### **Fine-Tuning**
* **Plain Meaning:** Taking a model that already knows general English (pre-trained on billions of words) and training it on a smaller, specialized legal dataset so it learns how to identify Philippine statutory conflicts.

### **Loss Function (Cross-Entropy Loss)**
* **Plain Meaning:** The mathematical formula that calculates how wrong the model was on a specific prediction. A loss of $0.0$ means a perfect, 100% confident correct prediction; a high loss means the model was either wrong or very uncertain.

### **Gradient & Backpropagation**
* **Backpropagation:** The process of tracing an error backwards through all layers of the neural network to determine which weights contributed to the mistake.
* **Gradient:** The mathematical direction and steepness indicating how each weight should be adjusted to decrease the loss.

### **Learning Rate ($\eta$)**
* **Plain Meaning:** The multiplier applied to the gradient when updating weights:
  $$\text{new\_weight} = \text{old\_weight} - (\eta \times \text{gradient})$$
* **Why It Matters:** If $\eta$ is too big (e.g., $0.1$), the weights jump violently and the model breaks (`NaN`). If $\eta$ is too small (e.g., $10^{-8}$), the weights barely move and training takes forever. The sweet spot for fine-tuning transformers is typically $\eta = 2 \times 10^{-5}$ ($0.00002$).

### **Weights & Parameters**
* **Plain Meaning:** The millions of numerical values inside a neural network that determine how incoming words influence the final decision.
* **Weight Magnitude:** A large positive weight means a feature strongly triggers a certain label; a large negative weight means it suppresses it.
* **What if weights grow too large?** The model suffers from **hyper-fixation** (overfitting). If a weight balloons to $+50.0$, the model will scream "CONTRADICTION" the moment it sees the word "fine", ignoring whether the ordinance actually complied with the statute. It also causes numerical overflow crashes.

### **Weight Decay (AdamW, $\lambda$)**
* **Plain Meaning:** A built-in stabilizer that slightly shrinks all weights toward zero at every step by multiplying them by $(1 - \eta \lambda)$. This prevents any single weight from becoming an overwhelming tyrant and keeps the model balanced.

### **Epoch**
* **Plain Meaning:** One complete pass through the entire training dataset.
* **In This Thesis:** If our training set has 245 law pairs:
  * When the model has processed all 245 pairs once $\rightarrow$ **1 Epoch**.
  * Looping through them 3 times $\rightarrow$ **3 Epochs**.

### **Batch & Batch Size ($B$)**
* **Plain Meaning:** The number of training pairs fed into the GPU simultaneously before calculating the gradient and updating weights.
* **In This Thesis:** We evaluate batch sizes of $B = 8$ and $B = 16$. Larger batches give smoother gradients but consume more GPU VRAM.

### **Warmup Steps (Linear Warmup)**
* **Plain Meaning:** Starting training with a very small learning rate for the first few hundred steps (e.g., 10% of training), gradually ramping up to the full learning rate. This prevents early, unstable gradients from damaging pre-trained knowledge.

### **Dropout ($p$)**
* **Plain Meaning:** Randomly turning off a certain percentage of neurons (e.g., $p = 0.10$ or 10%) during each training pass. This forces the network to learn redundant, robust patterns rather than relying on a few lucky shortcut connections.

### **Early Stopping & Patience**
* **Plain Meaning:** A safety rule that halts training automatically if performance on the validation set stops improving.
* **Patience:** The number of consecutive epochs the algorithm is willing to wait without seeing a new best validation score before pulling the plug (in our paper, $\text{patience} = 4$).

### **Underfitting vs. Overfitting**
* **Underfitting:** Occurs when the model has not learned enough to capture authentic patterns (both training and validation error remain high). In our paper, this happens when the learning rate is too low ($\eta = 1\times 10^{-5}$) or training is stopped too early.
* **Overfitting:** Occurs when a high-capacity model memorizes the noise, phrasing quirks, or specific wording of the training sample ($N_{\text{train}} = 245$) rather than learning general legal principles. Training loss continues falling, but validation loss starts rising.
* **In This Thesis:** Controlled using the tripartite regularization strategy: AdamW weight decay ($\lambda = 0.01$), dropout ($p = 0.10$), and early stopping validation checkpoints.

### **Loss Dynamics & Inflection Point**
* **Loss Dynamics:** The chronological trajectory of training loss and validation loss across successive training epochs.
* **Inflection Point:** The exact epoch where validation loss reaches its lowest point (minimum) and begins to reverse upward. In our paper, DeBERTa-v3 reaches its inflection point at **Epoch 3** ($\text{Val Loss} = 0.4812$), signaling optimal generalization.

### **Ablation Study**
* **Plain Meaning:** An experimental design where individual features, modules, or filters are systematically removed or swapped to measure their isolated impact on overall system accuracy.
* **In This Thesis:** In Chapter 4 (Section 4.1.2), we conduct an ablation benchmark across 9 candidate Stage 1 retrieval configurations (BM25, Dense Bi-Encoder, Soft Priors, RRF) to prove that Reciprocal Rank Fusion ($k=60$) is optimal.

### **Catastrophic Forgetting**
* **Plain Meaning:** When fine-tuning a neural network on a small specialized dataset causes it to overwrite and "forget" the broad linguistic and grammatical knowledge it acquired during pretraining.
* **In This Thesis:** Prevented by using conservative learning rates ($\eta = 2\times 10^{-5}$), linear warmup, and weight decay so only the necessary classification and cross-attention weights adapt to Philippine statutory preemption.

### **Random Seed**
* **Plain Meaning:** Setting a fixed starting number for the computer's random number generator (e.g., $\text{seed} = 42$).
* **Why It Matters:** Guarantees **scientific reproducibility**. Anyone on any computer running the script with seed 42 will get the exact same dataset splits and initial weight shuffles.

---

## **5. Evaluation Metrics & Decision Calibration**

### **Ground Truth (Gold Standard)**
* **Plain Meaning:** The verified, correct answers established by human experts.
* **In This Thesis:** Our Ground Truth consists of **350 legal pairs** annotated and verified by 15 active Sangguniang Panlungsod legal researchers.

### **The Confusion Matrix**
* **True Positive (TP):** The model correctly detected a real contradiction.
* **False Positive (FP):** False alarm (the model flagged a contradiction where none exists).
* **True Negative (TN):** The model correctly identified that there is no conflict.
* **False Negative (FN):** Missed conflict (the model said the ordinance was fine, but it actually violated national law). **In municipal law, this is the most dangerous error.**

### **Precision, Recall & Accuracy**
* **Precision:** Out of all the contradictions the model flagged, how many were actually real?
  $$\text{Precision} = \frac{TP}{TP + FP}$$
* **Recall:** Out of all real contradictions that exist in the documents, how many did the model catch?
  $$\text{Recall} = \frac{TP}{TP + FN}$$
* **Accuracy:** Overall percentage of correct predictions across all classes. (Can be misleading if 90% of your data is neutral).

### **$F_1$-Score vs. $F_2$-Score**
* **$F_1$-Score:** The balanced harmonic mean of Precision and Recall (gives equal weight to both).
* **$F_2$-Score:** A variation of the F-measure that **weights Recall twice as heavily as Precision**:
  $$F_2 = \frac{5 \times \text{Precision} \times \text{Recall}}{4 \times \text{Precision} + \text{Recall}}$$
* **Why $F_2$ for Our Thesis?** Missing a real statutory conflict (False Negative) can lead to the City Council passing an illegal ordinance that gets struck down by the Supreme Court. A false alarm (False Positive) merely costs a legal researcher 2 minutes to verify and dismiss. Therefore, our conflict threshold is calibrated to maximize $F_2$.

### **Contradiction Decision Threshold ($\tau^*$)**
* **Plain Meaning:** The probability cutoff needed to trigger a "Conflict Detected" warning.
* **In This Thesis:** Standard classifiers use a 50% cutoff ($\tau = 0.50$). We test cutoff values between $0.50$ and $0.90$ on the validation dataset to find the exact optimal value $\tau^*$ that maximizes the $F_2$-score.

### **Macro-Averaging**
* **Plain Meaning:** Calculating the metric (e.g., $F_1$) for each class separately (Entailment, Neutral, Contradiction) and then taking the simple unweighted average. This ensures the minority class (Contradiction) is treated with equal importance as the common class (Neutral).

### **Inter-Annotator Agreement (Fleiss' Kappa, $\kappa$)**
* **Plain Meaning:** A statistical metric that measures how consistently multiple human judges agree with each other, adjusted for how often they might agree by pure luck/chance.
* **In This Thesis:** Bounded between $0.0$ and $1.0$. We target $\kappa \ge 0.61$ ("Substantial Agreement") across the 15 SP legal researchers.

### **Three-Tier System Evaluation Framework**
* **Plain Meaning:** A comprehensive evaluation methodology that validates the system at three complementary operational levels: component/algorithmic, full-document simulation, and real-world judicial/expert application.
* **In This Thesis:** Connects (1) Tier 1: Cascaded End-to-End Benchmark (algorithmic testing on 53 held-out test pairs); (2) Tier 2: Injected-Fault Full-Document Stress Testing (behavioral perturbation testing on full drafts); and (3) Tier 3: Historical Jurisprudential Validation (Supreme Court cases like *Mosqueda v. PBGEA*) and Sangguniang Panlungsod Human Evaluation.

### **Cascaded End-to-End Evaluation (Joint Hit Indicator)**
* **Plain Meaning:** Testing a multi-stage AI pipeline as a unified chain without spoon-feeding intermediate answers.
* **In This Thesis:** Rather than giving Stage 2 the correct national statute, the local draft clause is fed blindly into Stage 1, which searches all 27,000+ laws. A prediction is scored as a true hit ($\text{Hit}_{\text{casc}} = 1$) if and only if Stage 1 retrieved the correct statute in its top-$k$ shortlist AND Stage 2 correctly classified the conflict. Adapting the FEVER benchmark protocol (Thorne et al., 2018), this prevents high Stage 2 accuracy from masking retrieval failures.

### **Injected-Fault Testing (Behavioral Perturbation Testing)**
* **Plain Meaning:** Stress-testing software by deliberately inserting specific bugs or traps into an otherwise clean document to see if the system catches them while ignoring the innocent parts.
* **In This Thesis:** Adapting the CheckList framework (Ribeiro et al., 2020), we take full 8-to-12 section draft ordinances where 80–90% of clauses are standard legal text, and inject deliberate preemption violations into 1 or 2 target sections (e.g., penalty caps under RA 7160 §458). We measure Section-Level Sensitivity (did it catch the trap?) and Section-Level Specificity (did it avoid raising false alarms on compliant sections?).

### **System Usability Scale (SUS)**
* **Plain Meaning:** A standardized 10-item Likert survey used in human-computer interaction to evaluate how easy, intuitive, and usable a software tool is.
* **In This Thesis:** Administered to the 15 Sangguniang Panlungsod legal researchers after using the single-page prototype dashboard during First Reading committee review simulations (Brooke, 1996). A SUS score above 68 represents above-average usability.

### **Digital-Born Document Ingestion**
* **Plain Meaning:** Ingesting newly drafted electronic files exported directly from word processors or digital PDFs, rather than legacy scanned paper images.
* **In This Thesis:** Live ex-ante draft ordinances submitted to the system are digital-born files with clean Unicode text, bypassing the OCR error correction pipeline required for legacy scanned ordinances from the 1970s–2000s.

### **Procedural Boilerplate Filtering**
* **Plain Meaning:** Automatically ignoring formulaic administrative sections of an ordinance that do not contain actual substantive legal rules or prohibitions.
* **In This Thesis:** The regex preprocessor automatically skips Title, Separability, Repealing, and Effectivity clauses during Stage 1 candidate retrieval to prevent search drift and avoid matching irrelevant national administrative statutes.

### **Section-Level Max-Pooling Aggregation**
* **Plain Meaning:** Consolidating multiple candidate prediction scores for a single section into one overall conflict verdict.
* **In This Thesis:** For a section $S_i$, Stage 2 evaluates all $k = 50$ candidate statutory provisions. The section's final conflict probability is the maximum contradiction score across all candidates: $P(\text{Conflict} \mid S_i) = \max_j P(\text{Contradiction} \mid P_j, S_i)$. If this maximum exceeds $\tau^*$, the section is flagged and linked directly to the specific statute that caused the highest contradiction score.

### **Two-Tiered Conflict Categorization (Red vs. Amber)**
* **Plain Meaning:** Distinguishing fatal legal violations against national law from routine municipal updates against older local laws.
* **In This Thesis:**
  1. **Critical Vertical Preemption Alert (Red):** Conflict with a superior Philippine National Statute under the *Magtajas* doctrine (fatal legal defect; *ultra vires*).
  2. **Informational Horizontal Modification Notice (Amber):** Inconsistency with an older Davao City Ordinance (signals an intended legislative amendment or implied repeal, alerting the drafter to verify their repealing clause).

### **Intrinsic Structural Explainability**
* **Plain Meaning:** Explaining an AI decision by directly displaying the exact source texts side-by-side with matched keywords, rather than generating black-box approximations.
* **In This Thesis:** The web dashboard displays the exact draft section side-by-side with the governing national statute, shows the calibrated contradiction probability ($P(\text{Contradiction})$), and highlights overlapping regulated entities and conflicting command words (*shall* vs. *may*, *prohibited* vs. *allowed*).

---

## **6. Statistical Hypothesis Testing (Comparing Models)**

### **Null Hypothesis ($H_0$) & Alternative Hypothesis ($H_1$)**
* **Null Hypothesis ($H_0$):** There is no real difference between Model A and Model B; any difference in score is just random noise or luck.
* **Alternative Hypothesis ($H_1$):** Model A is genuinely, statistically superior to Model B.
* **Goal:** We want to reject $H_0$ with a $p$-value $< 0.05$ (meaning there is less than a 5% chance the result occurred by random luck).

### **Type I Error ($\alpha$) vs. Type II Error ($\beta$)**
* **Type I Error ($\alpha$):** Claiming Model A is better when it actually isn't (False Positive claim).
* **Type II Error ($\beta$):** Failing to recognize that Model A is genuinely better because your test was too weak or conservative (False Negative claim).

### **Contingency Table**
* **Plain Meaning:** A $2 \times 2$ grid comparing where two models agree and disagree on the exact same test items:
  * Cell $a$: Both models were correct.
  * Cell $b$: Model 1 was correct, Model 2 was wrong.
  * Cell $c$: Model 1 was wrong, Model 2 was correct.
  * Cell $d$: Both models were wrong.

### **McNemar's Test (with Edwards' Continuity Correction)**
* **Plain Meaning:** A specialized statistical test designed specifically for comparing two classifiers on the exact same test dataset.
* **How It Works:** It ignores all the cases where both models got the answer right ($a$) or both got it wrong ($d$), and focuses strictly on the discordant cases ($b$ vs. $c$):
  $$\chi^2 = \frac{(|b - c| - 1)^2}{b + c}$$
* **Edwards' Correction (the $-1$ in the formula):** A mathematical adjustment that prevents the test from overestimating significance when the number of discordant pairs ($b + c$) is small.

### **The Multiple Testing Problem & Family-Wise Error Rate (FWER)**
* **The Problem:** If you compare 10 candidate models against each other using pairwise tests, you have to run $\binom{10}{2} = 45$ separate tests!
* **The Risk:** Even if all models are identical, running 45 tests at a 5% error rate gives a **$\sim 90.1\%$ chance of getting at least one false positive**.
* **Bonferroni Correction:** Dividing your significance threshold by the number of tests ($\alpha' = \frac{0.05}{45} = 0.0011$). While safe, this makes the test so strict that you will fail to detect real improvements (high Type II error).

### **The Two-Step Multi-Model Protocol (Demšar, 2006)**
* **Step 1: The Friedman Test ($\chi_F^2$):** A non-parametric ranking test that evaluates all 10 models across the 8 macro legal domains simultaneously. It answers one global question: *"Are all 10 models performing identically, or is at least one significantly different?"* without inflating error rates.
* **Step 2: Post-Hoc Comparison Against Control:** Only if the Friedman test shows a significant difference ($p < 0.05$), we run pairwise comparisons comparing each candidate model **only against the single top-performing "control" model** (e.g., DeBERTa-v3-base). This requires only $10 - 1 = \mathbf{9\text{ tests}}$ instead of 45!
* **Critical Difference (CD) Diagram:** A standard visual chart that plots the average rank of each model along an axis and draws a horizontal bar connecting models whose differences are not statistically significant.

---

## **7. System Architecture, Software Engineering & Reproducibility**

### **Config-Driven Architecture**
* **Plain Meaning:** Separating code from settings.
* **In This Thesis:** Just like a game mod that uses a `settings.json` or `config.ini`, all our model hyperparameters (learning rate, batch size, threshold $\tau^*$, top-$k$) are stored in external configuration files (e.g., `configs/training_config.yaml`). Changing a setting never requires editing Python source code.

### **Minimal Working Example (MWE)**
* **Plain Meaning:** A tiny, self-contained demonstration script that runs in seconds to prove the code works.
* **In This Thesis:** Located at `python scripts/prototype_pipeline.py --demo`. It loads mock statutory samples, executes Stage 1 BM25, passes the candidate to Stage 2 NLI, and outputs an explainability preview in $1.4$ seconds without needing any heavy downloads.

### **Optical Character Recognition (OCR) Noise**
* **Plain Meaning:** Spelling and layout errors created when software reads scanned paper documents (e.g., reading "Section 5" as "Sect10n S" or turning "₱5,000" into "P5.000").
* **In This Thesis:** Davao City ordinances from the 1970s–2000s are scanned PDFs with significant OCR noise, which our preprocessing pipeline cleans using regex and text normalization.

### **Task-Appropriate Workstation Allocation**
* **Plain Meaning:** Assigning each computing task to the hardware environment best suited for it, rather than treating hardware as an artificial hierarchy:
  1. **Workstation A: Primary Ingestion Workstation (Edge Simulation Node - Intel Core i3-10105F, 8GB RAM, RX 6600, Windows 10):** Handled national statute scraping of 25,432 laws from Lawphil, HTML parsing, text normalization, routine maintenance scripts, and serves as our physical LGU consumer desktop simulation testbed.
  2. **Workstation B: Neural Training Workstation (Dedicated GPU Node - Lenovo Legion 5, AMD Ryzen 7 260, 32GB RAM, NVIDIA RTX 5050 Laptop GPU, Windows 11):** Handles scanning and OCR cleaning of ~1,500 local Davao City ordinances from SP archives; executes dedicated Stage 2 Cross-Encoder fine-tuning, hyperparameter sweeps, latency profiling, and final full-system evaluation consistency.
  3. **Cloud Computing Environment (Google Colab Pro):** Utilized opportunistically for heavy exploratory Jupyter notebooks, large-scale SVD matrix factorization over 25,432 documents, and generating notebook visual assets.
---

## **8. Ground Truth Benchmark & Human Annotation Protocol**

### **Ground Truth Partitioning (70/15/15 Split)**
* **Plain Meaning:** Dividing the expert-annotated gold standard into non-overlapping training, validation, and test subsets to train models and assess true generalization without data leakage.
* **In This Thesis:** Our 350 statutory premise–hypothesis pairs are partitioned into a static **70/15/15 split** (245 training, 52 validation, 53 test pairs). This preserves enough validation data for fine decision threshold calibration ($\tau^*$) while satisfying the $N \ge 50$ test size required for reliable Minimum Detectable Effect (MDE) and McNemar's test.

### **Senior Annotator (Hierarchical Adjudicator)**
* **Plain Meaning:** An expert evaluator designated within each annotation sub-panel who acts as panel lead and tie-breaker for ambiguous or disputed items.
* **In This Thesis:** Within each of the five 3-member sub-panels ($k = 3$), the evaluator with the highest educational attainment and longest legislative drafting tenure is designated as the Senior Annotator. When all three panel raters choose different categories (a three-way split of 1 Contradiction, 1 Entailment, 1 Neutral), the item is referred to the Senior Annotator for binding qualitative adjudication against the statutory codebook (Gao et al., 2022; Artstein & Poesio, 2008).

### **Intake Credential Profiling**
* **Plain Meaning:** Systematically collecting objective professional qualifications from domain experts during recruitment before assigning tasks.
* **In This Thesis:** In the initial administrative correspondence transmitting the Guidebook to the Sangguniang Panlungsod Secretariat, the proponents request 15 volunteers and collect two objective metrics: (1) **Highest Educational Attainment** (J.D., LL.B., LL.M., Bar admission); and (2) **Years of Experience** in legislative drafting and statutory review. These metrics are used to stratify panels and objectively select Senior Annotators (Snow et al., 2008; Zheng et al., 2021).

### **Batched Consensus Allocation (Ablazo Framework)**
* **Plain Meaning:** A workload distribution model that achieves multi-rater voting overlap without overloading individual experts.
* **In This Thesis:** Adapted from Ablazo (2019), the 350 pairs $\times$ 3 independent votes ($1,050$ total annotations) are divided among 15 legal researchers organized into five 3-member panels ($P = 15, k = 3$). Each researcher reviews exactly **70 pairs**, taking approximately 60–90 minutes.

### **Annotator Agreement Target & Ceiling**
* **Plain Meaning:** The expected realistic range of human consensus on subjective or complex legal reasoning tasks.
* **In This Thesis:** Measured using Fleiss' Kappa ($\kappa$) across the initial independent votes of the 15 SP legal researchers. The study targets a threshold of $\kappa \ge 0.61$ ("Substantial Agreement" under Landis & Koch, 1977), bounded by the empirical NLI human agreement ceiling established by Bowman et al. (SNLI, $\sim 0.70$). Any residual 3-way discordance is resolved through the Senior Annotator adjudication hierarchy.

---

## **9. System-Level Multi-Tier Evaluation & Landmark Jurisprudence**

### **Cascaded Joint Hit Metric ($\text{Hit}_{\text{casc}}$ - Tier 1)**
* **Plain Meaning:** A strict success indicator that credits the system only if Stage 1 successfully retrieves the relevant governing statute into the top-$k$ shortlist AND Stage 2 correctly classifies the relationship (e.g., Contradiction).
* **Why It Matters:** Adapted from the FEVER fact verification benchmark (Thorne et al., 2018), this prevents Stage 2 from falsely taking credit when Stage 1 fails to find the right law, and isolates exactly which processing stage caused a pipeline failure.

### **Injected-Fault Full-Document Stress Testing (Tier 2)**
* **Plain Meaning:** Testing the pipeline on complete, multi-page draft ordinances containing 10–18 sections rather than isolated sentence pairs, where 85–90% of the sections are benign procedural boilerplate and only 1–2 sections contain deliberate legal violations.
* **In This Thesis:** Comprises 10 full synthetic/semi-synthetic draft ordinances ($N_{\text{sec}} = 140$ total provisions) evaluated against national statutes. It tests whether the system can spot the "needle in the haystack" (Section-Level Sensitivity) without raising annoying false alarms on standard procedural clauses (Section-Level Specificity).

### **Section-Level Specificity ($\text{Specificity}_{\text{sec}}$) & False Alarm Rate ($\text{FAR}$)**
* **Plain Meaning:** The mathematical measure of how well the system resists crying wolf on harmless legislative text:
  $$\text{Specificity}_{\text{sec}} = \frac{TN_{\text{sec}}}{TN_{\text{sec}} + FP_{\text{sec}}}, \quad \text{FAR}_{\text{sec}} = 1 - \text{Specificity}_{\text{sec}}$$
* **Why It Matters:** High specificity protects city council researchers from "alert fatigue." If an AI flags every standard repealing clause or definitions section as a violation, users will quickly turn the system off.

### **Efficient Use of Paper Rule (SC A.M. No. 11-9-4-SC) & LGU Folio Standards**
* **Plain Meaning:** The formal document and typography standards mandated across Philippine legal and governmental drafting.
* **In This Thesis:** Draft ordinances in our Tier 2 benchmark adhere strictly to Philippine Government Legal/Folio size ($8.5 \times 13.0$ inches), 1.5-inch left binding margins (for Sangguniang Panlungsod LISSP archival ring-binders), 1.0-inch top/bottom/right margins, 12pt Arial/Times New Roman font, 1.5 line spacing, and the mandatory Section 54 RA 7160 enacting clause (*"BE IT ORDAINED BY THE SANGGUNIANG PANLUNGSOD OF DAVAO CITY, IN SESSION ASSEMBLED"*).

### **Behavioral Perturbation Testing (CheckList)**
* **Plain Meaning:** A software engineering testing paradigm for AI (Ribeiro et al., 2020) that evaluates models by deliberately introducing specific, targeted linguistic or structural faults to see if the model reliably breaks or succeeds.

### **Historical Judicial Validation Suite (Tier 3)**
* **Plain Meaning:** Testing the system against authentic historical municipal ordinances that were actually litigated and resolved by the Supreme Court of the Philippines or tested under official administrative regulatory preemption boundaries.
* **In This Thesis:** Compiled in `data/tier3_jurisprudential_cases.jsonl` and stored in `corpus/davao_city_tier3_ordinances/`, spanning 10 landmark Davao City municipal enactments:
  1. ***Mosqueda v. PBGEA* (2016):** Davao City Ordinance No. 0309-07 banning aerial pesticide spraying was invalidated for conflicting with the Fertilizer and Pesticide Authority's national regulatory powers under PD 1144 and violating Equal Protection (`Contradiction`).
  2. ***Evasco, Jr. v. Montañez* (2018):** Davao City Ordinance No. 092-2000 regulating outdoor billboards was upheld as a valid police power measure under RA 7160 Section 458 coexisting harmoniously with the National Building Code (`Entailment`).
  3. ***City of Davao and Tanjili v. ARC Investors, Inc.* (2022):** Cancelled Davao City's local business tax assessment on a corporate holding company, ruling that an LGU cannot unilaterally classify a passive dividend-earning company as a financial intermediary without a BSP license (`Contradiction`).
  4. ***Smart Communications, Inc. v. City of Davao* (2008) / *PLDT v. City of Davao* (2001):** Upheld Davao City Ordinance No. 230 / 519 imposing local franchise tax on telecom carriers, ruling that "in lieu of all taxes" franchise clauses must be strictly construed and do not abrogate municipal taxing autonomy under RA 7160 Section 137 (`Entailment`).
  5. ***Mindanao Shopping Destination Corp. v. Duterte* (2017):** Held that Davao City Ordinance No. 158-05 graduated business tax schedules cannot exceed the statutory tax rate ceilings established in RA 7160 Section 143 (`Contradiction`).
  6. ***City of Davao v. GSIS* (2005):** Invalidated real property tax assessments on GSIS facilities under RA 7160 Section 133(o), which strictly prohibits LGUs from taxing national government instrumentalities (`Contradiction`).
  7. ***Davao City Mining Ban Dispute* (2015):** The territorial mining prohibition under Ordinance No. 0310-07 operates in direct vertical tension with State mineral ownership and concessions under RA 7942 (`Contradiction` / Vertical Tension).
  8. ***Davao Anti-Smoking Ordinance* (2012):** Stricter local smoking setbacks under Ordinance No. 0367-12 are valid police power measures because national tobacco law (RA 9211) establishes minimum health baselines, not maximum ceilings (`Entailment`).
  9. ***Davao City Speed Limit Ordinance* (2023):** Davao City Ordinance No. 0270-23 establishing road speed classifications is valid pursuant to delegated authority under RA 4136 §38 and Joint DOTr-DPWH-DILG JAO 2018-01 (`Entailment`).
  10. ***Davao City Firecracker Ban Ordinance* (2002):** Davao City Ordinance No. 060-02 imposing a total ban on pyrotechnics is a valid municipal exercise of general welfare police power to protect life and safety under RA 7160 §16 and §458(a)(1)(vi) (`Entailment`).

---

*This glossary is maintained as a living reference. Whenever new models, metrics, or legal doctrines are introduced to the thesis manuscript, they are immediately added here.*

