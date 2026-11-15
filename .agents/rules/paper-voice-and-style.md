---
trigger: model_decision
description: Apply alongside ALL other paper-*.md rules when drafting, editing, humanizing, or sweeping thesis prose in CS_Undergraduate_Thesis_Template/. Covers undergraduate CS voice, anonymity, vocabulary calibration, 5-sentence paragraph cadence, and strict anti-AI syntax/buzzword bans.
---

# **Paper Voice, Readability & Anti-AI Style Rules**

**Scope:** Prose style, authorial tone, and register checks for `CS_Undergraduate_Thesis_Template/`. When polishing or sweeping prose, also consult `.agents/skills/declauding/SKILL.md` for final de-clauding passes and enforce all four `paper-*.md` rules together.

---

## **1. Undergraduate Scholarly Voice & Authorial Identity**

1. **The Caucus Principle (Humility & Realism):** The proponents are undergraduate CS students, not lawyers or doctoral scholars. Never adopt an arrogant, all-knowing tone. Frame the system strictly as an **assistive decision-support screening tool** flagging candidate textual tensions for human SP legal researchers—never claim it resolves statutory construction, determines constitutionality, or replaces legal counsel.
2. **Direct Undergraduate Voice & Balanced Softening:** Write clearly and plainly without pompous thesaurus prose. Explain *why* choices were made using concrete reasons (available researchers, fatigue limits, sample power).
   * Avoid over-claiming (*"guarantees zero provision attrition"* $\rightarrow$ *"ensures zero provision attrition across the 350 evaluated queries"*; *"this proves"* $\rightarrow$ *"this evaluates"*; *"indispensable"* $\rightarrow$ *"provides substantial benefits"*; *"universal phenomenon"* $\rightarrow$ *"consistent cross-architectural trend"*).
   * Simultaneously avoid journalistic hedging (*"allegedly," "supposedly," "purportedly"*). Ground claims in verified metrics, *Magtajas*, RA 7160, and peer-reviewed citations.
3. **Strict Academic Anonymity (Zero Personal Names in Chapters 1–5):** Refer to authors strictly as *"the proponents"* or *"the research team"* (avoid *"I"*, *"my"*; use *"we"* very sparingly). Refer to faculty by role (*"the thesis adviser"*, *"the course instructor"*, *"the defense panel"*). **NEVER** write personal names (*Yahyah Odin*, *Ralph Paolo Dulce*, *Sir Ogs*, *Adrian Ablazo*) inside Chapters 1–5; personal names belong only on Title/Approval/Acknowledgement pages.
   * **Citation Exception:** When citing faculty research (e.g., Ablazo's 2019 thesis), cite formally by surname and BibTeX key (`Ablazo~\cite{ablazo2019designing}`).
   * **Hardware Naming:** Use objective platform labels (*Host A (Desktop)*, *Host B (Laptop 1)*) rather than possessive owner names.

---

## **2. Vocabulary Calibration & Literal Naming**

1. **Accessible Baseline (0.5–1.0 Level Below Hyper-Academic Prose):** Match Chapters 1 and 2—clear, direct, and readable. Replace dense Latinate constructions with plain English whenever exact meaning is preserved:
   * *"systematic compilation of text from disparate public repositories"* $\rightarrow$ *"gathering text from different public repositories"*
   * *"syntactically headless and lose their governing institutional actors"* $\rightarrow$ *"separated from their context, making it unclear who must follow or enforce the rule"*
   * *"deontic modality clashes"* $\rightarrow$ *"clashes in mandatory words (such as 'shall' versus 'may')"*
   * *"mitigate cognitive fatigue through a multi-stage cognitive support protocol"* $\rightarrow$ *"reduce reviewer fatigue by providing structured reference guides"*
2. **Preserve Exact Technical & Legal Terms of Art:** Plain phrasing never sacrifices precision. Retain canonical identifiers and formulations: `Cross-Encoder`, `Bi-Encoder`, `BM25`, `ModernBERT`, `DeBERTa-v3`, `TF-IDF`, `SVD`, `c-TF-IDF`, `MiniBatch K-Means`, `AdamW`, `Magtajas v. Pryce Doctrine`, `ultra vires`, `in pari materia`, `ex-ante`, `Republic Act No. 7160`, `Sangguniang Panlungsod`, `Recall@k`, `MRR@k`, `Fleiss' Kappa` ($\kappa$), and benchmark parameters ($N = 350$, $k = 3$, $R = 70$, $P = 15$, static 70/15/15 split).
3. **Canonical Jurisdiction Terms (City vs. Municipal):** Davao City is a Highly Urbanized City (HUC), not a municipality. Refer to Davao enactments as *"local ordinances"* or *"city ordinances."* Reserve *"municipal"* strictly when quoting general statutory language (e.g., RA 7160) or external municipal cases.
4. **Plain, Literal Entity Naming (No AI Epithets):** Name statutes, models, and metrics by their literal identifiers. **NEVER** append dramatic epithets or noun stacks (*"Central Anchor Hub"*, *"Super-Hub"*, *"Core Backbone"*, *"Reasoning Ceiling"*, *"Gold-Standard Pillar"*). Use plain names (`RA 7160`, `DeBERTa-v3-base`, `National Statutes`, `Local Ordinances`), leaving degree or centrality to plain numbers.

---

## **3. Paragraph Cadence & Structural Rhythm**

1. **Target 4–6 Sentences per Paragraph (Target: 5):**
   * **S1 (Topic & Transition):** Direct assertion or thematic link.
   * **S2 (Elaboration & Context):** Theoretical, jurisdictional, or technical qualification.
   * **S3 (Evidence / Data / Citation):** Concrete empirical metric, formula, or verified citation.
   * **S4 (Analytical Bridge):** What the evidence demonstrates and why it matters.
   * **S5 (Implication & Forward Link):** Operational constraint or transition to next point.
2. **Visual Balance:** Eliminate thin 1–3 sentence micro-paragraphs (expand or merge them). Dedicated visual expositions may run 7–8 sentences; split beyond ~10 sentences while keeping the chain of thought intact.

---

## **4. Absolute Structural, Syntax & Vocabulary Bans**

Strictly enforce these invariants during both initial drafting and manuscript sweeps:

1. **ZERO Triplet / Rule-of-Three Cadence:** Ban rhythmic triplets of nouns, adjectives, verbs, or three-clause compounds (e.g., *"enhancing efficiency, fostering collaboration, and driving innovation"*; *"vital, crucial, and indispensable"*). Rewrite into a **binary pair** (*"X and Y"*) or **two distinct declarative sentences**.
2. **ZERO Sentence-Ending Participle Tails:** Ban trailing `, [verb]ing ...` clauses at sentence ends (e.g., *", achieving 100\% recall"*; *", ensuring statutory coherence"*). Cut the tail, make it a separate sentence, or fold it into the main verb (*"processes candidates in 12.69 s and reduces latency by 54.9\%"*).
3. **NO Copula Avoidance:** Use direct *is*, *are*, *has*. Replace *"serves as"*, *"stands as"*, *"acts as"* with *"is"*; replace *"boasts"* with *"has"* or *"achieves"*.
4. **NO Inanimate Subject Agency:** Charts, tables, metrics, and algorithms do not act as human agents. Replace *"Table 4.1 shows/reveals/argues"* or *"the algorithm discovers"* with *"As shown in Table~4.1, ..."*, *"The evaluation demonstrates that ..."*, or *"The proponents observe that ..."*.
5. **NO Staged Reveals / Movie-Trailer Phrasing:** Ban dramatic pacing (*"Here is where it gets interesting:"*, *"What the researchers did not expect was..."*, *"It turns out that..."*, *"The real problem was not X; it was Y."*). State findings directly in SVO order.
6. **NO Flat-Certainty Adverbs:** Ban *"plainly,"* *"merely,"* *"quietly,"* or bare *"empirically"* as evidence substitutes; give the exact metric, $p$-value, or citation instead.
7. **NO "Not Just X, But Y" / Heavy Em-Dashes:** Avoid *"not only X, but also Y"* formulas and frequent dramatic em-dashes (`---`). Prefer commas, semicolons, balanced parentheses, or period breaks.
8. **Banned AI Buzzwords & Overused Jargon:**
   * **Abstract Clichés:** *tapestry, delve, underscore, testament to, beacon, delicate dance, dynamic interplay, cornerstone, multifaceted paradigm, paramount, pivotal, overarching, nuanced, mastery of, vibrant, intricate web, holistic symphony*.
   * **Promotional Hyperbole:** *revolutionary, groundbreaking, remarkable, astounding, paradigm shift* (unless directly quoting literature).
   * **Overused Jargon:** Ban routine *"protocol"* (*chunking/screening/adjudication protocol* $\rightarrow$ *procedure, workflow, process, method, safeguards*); ban reflexive *"bottleneck"* (*quadratic/lexical/review bottleneck* $\rightarrow$ *constraint, memory ceiling, processing delay, review burden, hardware limitation*); ban *"Crucially,"*, *"leverage"* (*use, apply, adopt*), *"utilize"* (*use*), *"foster"* (*support, enable*).
   * **Mechanical Openers:** Ban repetitive *"In addition," "It is worth noting that," "Interestingly," "Importantly."* (*"Furthermore," "Moreover," "Consequently"* are fine when genuinely linking reasoning.)
