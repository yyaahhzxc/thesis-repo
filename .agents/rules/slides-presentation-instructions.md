---
trigger: model_decision
description: This rule shall be applied when working on presentation slides, defense deck files, slide visual assets, spoken scripts, or slide viewers (docs/presentation/PRESENTATION_SLIDES_MOCK_DEFENSE.md, docs/presentation/defense_presentation_deck.html, docs/presentation/slides_viewer.html, scripts/sync_slides_viewer.py).
---

# **Thesis Defense Presentation Slides & Deck Authoring Protocol**

**Institution:** Ateneo de Davao University, Department of Computer Science  
**Project:** *"A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference"*  
**Authors:** Ralph Paolo Dulce & Yahyah Odin  
**Adviser:** Mr. Adrian "Ogs" Ablazo | **Professor:** Ma'am Grace Tacadao  

---

## **1. Core Visual Rule: Authentic Artifacts Only (No Redundant Text Cards)**

1. **Visual Purpose & Restraint:**
   * Slide visuals must strictly be **authentic artifacts** directly originating from the thesis research:
     * High-resolution manuscript figures (e.g., flowcharts, distribution plots, attention saliency heatmaps, SVD semantic topic spaces).
     * Publication tables formatted cleanly using booktabs (e.g., Table 4.1 OCR sampling, Table 4.2 OCR benchmark, Table 4.4 functional typologies, Table 4.6 dual corpus parameters, Table 4.13 cross-validation benchmark).
     * Authentic archival scans and screenshot plates (e.g., Lawphil interface, modern vs. typewriter ordinance scans, annotator certificates).
     * Live prototype UI screen shares (`http://127.0.0.1:5050`) or UI screenshot panels.
2. **Visual Orientation in Spoken Scripts (Foundational Walkthrough First):**
   * Whenever introducing a visual artifact (table, figure, graph, or distribution plot), the spoken presenter script **must first describe the basic structure of what is being presented** before explaining the findings or takeaways:
     * *For Tables:* State what the table evaluates, followed explicitly by the columns and rows (e.g., *"Table 4.2 evaluates four candidate extraction architectures across eight performance and operational metrics, comparing Gemini Flash 3.8, Surya v0.6+, Tesseract v5.x, and our offline 4-bit Qwen2.5-VL-3B..."*).
     * *For Figures/Graphs:* State the axes, panels, and what is plotted (e.g., *"Figure 4.3 plots the enactment length asymmetry on a logarithmic scale in Panel A, while Panel B plots the subword token density distributions for national and local provisions against the 512-token transformer limit..."*).
   * Only after orienting the audience to the layout and axes should the script explain *what is happening* and deliver the key empirical conclusions.
3. **Strict Nomenclature & Urban Entity Accuracy (City vs. Municipality):**
   * **Never refer to Davao City as a "municipality"!** Davao City is legally and administratively a Highly Urbanized City (HUC) under Republic Act No. 7160.
   * In on-screen bullets, visual graphics, and spoken scripts, use *"city"*, *"local government unit (LGU)"*, *"local legislative typologies"*, or *"local enactments"*. Purge all instances of *"municipal typologies"* or *"municipal archives"* when referring specifically to Davao City enactments.
   * Adhere strictly to the zero-AI-buzzword policy across all slides and spoken presenter scripts.
4. **Strict Alignment with Manuscript Table and Figure Numbers:**
   * Every slide referencing a table or figure must strictly match the canonical numbering in the compiled manuscript (`main.lot` and `main.lof`):
     * Table 4.1: Stratified Reference Sampling Matrix ($N = 60$)
     * Table 4.2: Ordinance OCR and VLM Benchmark Across Candidate Extraction Architectures
     * Table 4.4: Functional Typology of the Davao City Local Legislative Corpus ($N = 1,925$)
     * Table 4.5: Empirical Holdout Validation Metrics for the Local Topic Modeler
     * Table 4.6: Comparative Structural Parameters of the Dual Statutory Search Space ($N = 27,357$)
     * Table 4.13: Out-of-Sample Test and 5-Fold Cross-Validation Performance Comparison
     * Table 4.17: Full-Document Audit Latency and Candidate Scaling on 4-Thread CPU
     * Table 4.20: Tier 2 Typology-Stratified Full-Document Stress Testing Benchmark
     * Table 4.21: Tier 3 Supreme Court Jurisprudential Preemption Benchmark ($N = 11$)
     * Figure 4.1: Two-Dimensional Latent Semantic Topic Space of Local Corpus
     * Figure 4.2: Longitudinal Word Count Evolution and Legislative Volumes
     * Figure 4.3: Enactment Length Asymmetry (Panel A) and Provision-Level Subword Token Densities (Panel B)
     * Figure 4.4: Cumulative Provision Compliance Curves and Attention Window Evaluation (94.75% 512-Token Compliance)
     * Figure 4.5: Stage 1 Candidate Retrieval Performance across Difficulty Tiers
     * Figure 4.6: Stage 2 Cross-Encoder Loss Dynamics and Convergence Trajectories
     * Figure 4.7: Statistical Model Validation and Cross-Validation Performance Comparison
     * Figure 4.8: Pipeline Feature Importance and Token Attention Attribution Map
5. **Strict Prohibition of Text-Duplicate Graphic Cards:**
   * **NEVER** generate artificial matplotlib "card" images that merely duplicate, restate, or mirror the bullet points already written on the slide.

---

## **2. Structural Slide Transitions & Complex Visual Layout Rules**

1. **Mandatory Chapter Transition Slides (Strict Literal Name Only):**
   * Every chapter must be preceded by a **dedicated transitional slide that contains LITERALLY ONLY the name of the chapter and nothing else** (e.g., Slide 2: *Chapter 1: Introduction*, Slide 6: *Chapter 3: Methodology*, Slide 22: *Chapter 4: Results and Discussion*, Slide 29: *Chapter 5: Conclusions and Recommendations*).
   * **Zero on-screen body bullets, zero agendas, zero subtitles, zero roadmap outlines.** The slide canvas displays strictly and solely the chapter title card (e.g. `Chapter 4: Results and Discussion`).

2. **Complex Visuals & Publication Tables (Full Canvas Space Allocation):**
   * When presenting complex publication tables (such as Table 4.1 OCR/VLM benchmark, Table 4.4 local typologies, Table 4.10 cross-validation, or Table 4.18 Supreme Court suite) or high-resolution diagrams, the visual requires the full screen canvas to remain readable. Never squeeze bullets next to or under dense tables.
   * **The Two Permissible Modes for Complex Visuals:**
     * *Mode A (Let the Visual Speak for Itself):* Dedicate the entire 16:9 canvas strictly to the standalone visual/table artifact without any on-screen bullets. The presenter delivers the narrative interpretation using the word-for-word spoken script.
     * *Mode B (Two-Slide Pairing with Preceding Setup Slide):* If contextual bullets are necessary before revealing the visual, place a dedicated setup slide immediately *before* the visual slide containing high-level motivation, objectives, or context bullets (following 7x7 rules). **Do NOT simply repeat or restate what is already inside the table/figure cells**—use the bullets for motivation, methodology context, or key takeaways, then transition to the standalone visual slide.

---

## **3. Ma'am Grace Tacadao's 7x7 Presentation Rule**

1. **The 7x7 Rule Standard:**
   * **Maximum 7 bullet lines** per slide.
   * **Maximum 7 words per line** (target 5 to 7 words).
   * **Zero Jargon & Clean Cadence:** Write punchy, high-impact statements that can be grasped in 3 seconds by panelists.
   * **Single-Line Bullets:** Never allow bullet text to wrap awkwardly across multiple lines.
2. **Explicit Exemptions to the 7x7 Rule:**
   * **Problem Statement (Slide 4):** Verbatim reading of the 5 official Research Questions from Chapter 1.
   * **Objectives of the Study (Slide 5):** Verbatim reading of the 5 official Specific Research Objectives from Chapter 1.
   * **Title & Chapter Divider Cards:** Metadata and chapter title dividers.
   * **Standalone Visual & Table Slides:** Slides dedicated exclusively to full-screen publication tables or high-resolution figures.

---

## **4. Canonical Slide Order & Flow (Methodology Evaluation Sequence)**

Following benchmark dataset construction (Slide 17: Ground Truth Benchmark Construction), the methodology evaluation and optimization sequence must strictly follow this exact 4-part structure:
1. **Stage 1 Evaluation and Optimization (§3.6.1, §3.8.1):**
   * Coarse retrieval screening across 8 candidate bi-encoders vs. BM25 baseline.
   * Ranking metrics: Recall@{5, 10, 20, 50} and Mean Reciprocal Rank (MRR, $1/\text{rank}$).
   * Edge query latency profiling per provision on commodity CPU.
   * High-recall safety buffer prioritizing Stage 1 recall to prevent downstream Stage 2 blind spots.
2. **Stage 2 Evaluation and Optimization (§3.6.2, §3.7.2, §3.8.2):**
   * Three-Stage Screening Funnel:
     * *Step 1:* Rapid zero-shot sweep across 28 candidate models (6 families) to benchmark latency and expose baseline affirmative entailment bias.
     * *Step 2:* Supervised task adaptation ($N_{\text{train}} = 245$, $N_{\text{val}} = 52$) with AdamW ($\lambda = 0.01$), attention dropout ($p = 0.10$), patience $= 4$, and learning rate warmup.
     * *Step 3:* Finalist benchmarking (top 5 validation models + canonical BERT baseline) on the 350-pair ground truth.
   * Cost-sensitive $F_2$-Score ($\beta = 2$) and decision threshold calibration ($\tau^* \in [0.25, 0.50]$) penalizing false negatives 5:1 under the *Magtajas* doctrine.
3. **Statistical Testing (§3.8.3, §3.9):**
   * Justification for non-parametric tests: discrete, non-normal classification errors.
   * Friedman two-way ANOVA by ranks ($\chi_F^2$) across all 8 Macro Legal Domains to verify cross-domain ranking invariance without thematic bias.
   * McNemar's chi-squared test with Edwards' continuity correction on discordant pairs ($b$ vs. $c$) with Bonferroni correction ($\alpha = 0.05$).
4. **System-Level Evaluation (§3.10):**
   * Three-Tier Evaluation Framework:
     * *Tier 1 (Cascaded Pipeline):* Joint FEVER metric ($\text{Hit}_{\text{casc}} = \text{Recall} \times \text{Contradiction}$) on 53 test pairs feeding only draft hypothesis clauses.
     * *Tier 2 (Full-Document Stress Testing):* 6 typology-stratified full-length drafts (52 sections, 740 to 2,464 words) in authentic SP Folio format with attached MOA, Deeds of Usufruct, measuring Section Sensitivity and Specificity.
     * *Tier 3 (Supreme Court Jurisprudential Precedent Suite):* 8 landmark Davao City preemption cases (*Mosqueda*, *Evasco*, *ARC Investors*, *First Meridian*, etc.) replicating authentic judicial reasoning.

---

## **4. Speaker Balance & Word-for-Word Spoken Scripts**

1. **Balanced Proponent Distribution:**
   * Presentation time is strictly budgeted for a 20-minute window (target: ~16 to 17 minutes spoken presentation + buffer for panel Q&A).
   * Spoken time must remain balanced 50/50 between Ralph Paolo Dulce and Yahyah Odin.
2. **Spoken Script Grounding:**
   * Every slide must provide a complete, articulate, word-for-word spoken presenter script.
   * Spoken scripts must explain the *why*, the *how*, and the *what it means* clearly and directly, adopting an articulate undergraduate honors tone (accessible academic language, zero pompous pretension, zero robotic AI fillers).
   * In HTML decks (`defense_presentation_deck.html`), use `<span class="script-anchor">` to highlight visual anchors matching the spoken script with on-screen bullet points.

---

## **5. Companion File Synchronization Protocol**

Whenever slide contents, titles, numbers, visual references, or scripts are modified:
1. **Primary Source:** Update [`docs/PRESENTATION_SLIDES_MOCK_DEFENSE.md`](file:///c:/Users/SHRIMP/Documents/thesis-repo/docs/PRESENTATION_SLIDES_MOCK_DEFENSE.md).
2. **Viewer Synchronization:** Execute `python scripts/sync_slides_viewer.py` to refresh [`docs/slides_viewer.html`](file:///c:/Users/SHRIMP/Documents/thesis-repo/docs/slides_viewer.html).
3. **HTML Deck Synchronization:** Update [`docs/defense_presentation_deck.html`](file:///c:/Users/SHRIMP/Documents/thesis-repo/docs/defense_presentation_deck.html) so all card IDs, Jump select options, bullet lists, script anchors, and timing metadata remain 100% harmonized.
4. **Master Task Log:** Document all updates in [`docs/THESIS_MASTER_TASKS.md`](file:///c:/Users/SHRIMP/Documents/thesis-repo/docs/THESIS_MASTER_TASKS.md).

