# Master Defense Presentation & Slide Deck Authoring Guidelines

**Institution:** Ateneo de Davao University, Department of Computer Science  
**Course:** Bachelor of Science in Computer Science (BS CS)  
**Proponents:** Ralph Paolo Dulce ("Ralph") & Yahyah Odin ("Yah")  
**Thesis Adviser:** Mr. Adrian "Ogs" Ablazo | **Professor:** Ma'am Grace Tacadao  

---

## 1. Visual Layout, Branding, & Coordinate Anchors

All slide decks generated for oral presentations and mock defense must strictly conform to the following visual standards:

1. **Aspect Ratio:** Standard 16:9 widescreen (`1920x1080` or `1440x810`).
2. **Color Palette:**
   - **Background:** Authentic dark navy ethnic weave texture (`presentation slide/thesis slides assets/background.png`, RGB `#041530` to `#081d3d`).
   - **Slide Titles:** Warm golden yellow (`#f2b705` or `#d89b14`), rendered in **PT Serif** (bold, with subtle drop-shadow or high legibility contrast).
   - **Body Text:** Crisp white (`#ffffff` / `#f8fafc`) for primary text; ice blue (`#94a3b8` / `#cbd5e1`) for secondary subtext and metadata.
   - **Highlights & Accents:** Gold (`#f2b705`), Emerald Green (`#10b981`) for positive verification, Crimson Red (`#ef4444`) for preemption collisions.
3. **Mandatory 3-Corner Slide Anchors (Every Content Slide):**
   - **Top-Left Header:** `[Chapter Number & Name]` (e.g., `Chapter 1: Background of the Study`, `Chapter 3: Methodology: Knowledge Base`).
   - **Bottom-Left Footer:** `[Paper Reference / Section Grounding]` (e.g., `Manuscript §1.1 | Republic Act No. 7160 §5(a)`, `Manuscript §4.2 | Table 4.4`).
   - **Bottom-Right Footer:** `[Slide Number]` (Clean, high-legibility bold number matching Canva assets).

---

## 2. Text Density & The 7x7 Rule Protocol (Ma'am Grace Directive)

1. **Strict 7x7 Rule:**
   - A maximum of **7 bullet points per slide**.
   - A maximum of **7 words per bullet point** (excluding grammatical particles or standard legal acronyms like RA 7160).
2. **The Only Exceptions:**
   - **Statement of the Problem (SOP):** Research questions Q1–Q5 must be listed fully and accurately to maintain formal academic alignment.
   - **Objectives of the Study:** Objectives 1–5 must be stated clearly and comprehensively as approved in Chapter 1.
3. **Conversational "Dumbed-Down" Talking Points:**
   - Text on slides must be instantly digestible by panelists at a glance.
   - Avoid dense multi-clause academic prose.
   - Each bullet point must represent an **independent, actionable talking point** that acts as the speaker's memory trigger (no verbatim reading of long paragraphs; proponents do not use written scripts).

---

## 3. Visuals, Figures, & Conceptual Framework Guidelines

1. **Zoomed & High-Fidelity Figures:**
   - Never display a full 3,000×5,000 px multi-phase diagram shrunk onto a single slide.
   - Figures must be cropped, zoomed, and sized to fill the content area with crisp, readable text without requiring zooming during the presentation.
2. **Conceptual Framework Segmentation:**
   - Segment the Master Conceptual Framework into 3 distinct logical slides:
     * **Phase 1: Pre-Planning & Knowledge Base:** Offline ingestion, text normalization, and vector store.
     * **Phase 2: Live Coarse-to-Fine Pipeline:** User submission, Stage 1 hybrid retrieval, Stage 2 cross-encoder reasoning.
     * **Phase 3: Decision Engine & XAI Output:** Calibrated thresholding, vertical/horizontal alerts, and clearance certificates.
3. **Simplified Slide-Optimized Figures:**
   - If a manuscript figure has dense micro-text (e.g., complex 28-model scatter plots), provide a presentation-optimized version highlighting the top contenders, Pareto frontier, or primary convergence points.

---

## 4. Empirical Tables Re-Creation (Booktabs Format)

1. **Native Slide Tables (Not Low-Res Screenshots):**
   - Recreate empirical tables directly as native slide elements (in PowerPoint or Web HTML/CSS).
   - Use the academic **Booktabs format**: bold top horizontal line, clean midrule below headers, no vertical grid lines, clean bottom rule, and right-aligned numerical metrics.
2. **Highlighting Findings:**
   - Bold key findings (e.g., `100.0% Recall@20`, `89.47% Conflict F1`, `1.33 ms Latency`).

---

## 5. Dual Antigravity Delivery (Canva PPTX & Interactive Web Deck)

1. **Single Source of Truth:**
   - All slide contents, anchors, notes, and visual mappings reside in `presentation slide/presentation_deck_data.json`.
2. **Canva-Compatible PPTX Export (`presentation slide/generate_defense_pptx.py`):**
   - Uses `python-pptx` to build a clean `.pptx` file.
   - Embeds `background.png` as background on all slides.
   - Creates editable text boxes with PT Serif / Poppins fonts and native booktabs tables so Ralph and Yah can directly upload to Canva and edit.
3. **Interactive Web Presentation Deck (`presentation slide/index.html`):**
   - A standalone web deck for instant mock-defense rehearsal, keyboard navigation (`←`, `→`, `F` for fullscreen), and live demonstration handoff.
