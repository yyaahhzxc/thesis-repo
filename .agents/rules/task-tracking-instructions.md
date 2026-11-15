# **Master Task Tracking & Cross-Session Continuity Protocol**

**Project:** *"A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference"*  
**Authors:** Ralph Paolo Dulce ("Ralph") & Yahyah Odin ("Yah")  
**Adviser:** Mr. Adrian "Ogs" Ablazo | **Course Professor:** Ma'am Grace Tacadao  

> [!IMPORTANT]
> Foundational research integrity, user greeting, plain-text math formatting, Zero Editorial Pollution, Pure Neural Architecture, and Adversarial Forensic Audit rules are governed by [`.agents/rules/general-instructions.md`](file:///c:/Users/SHRIMP/Documents/thesis-repo/.agents/rules/general-instructions.md). Manuscript writing and sweep rules are modularized under `.agents/rules/paper-*.md` and [`CS_Undergraduate_Thesis_Template/AGENTS.md`](file:///c:/Users/SHRIMP/Documents/thesis-repo/CS_Undergraduate_Thesis_Template/AGENTS.md).

---

## **1. Living Source of Truth & Continuity Mandate**

1. **Mandatory Check on Conversation Start:** Before starting work or proposing priorities, read [`docs/THESIS_MASTER_TASKS.md`](file:///c:/Users/SHRIMP/Documents/thesis-repo/docs/THESIS_MASTER_TASKS.md) to ground in the active milestone, recent session journal, open blockers, and pending deliverables.
2. **Atomic Task Updates:** Whenever a task, script, benchmark, or LaTeX revision completes, immediately update `docs/THESIS_MASTER_TASKS.md` (`[ ]` $\rightarrow$ `[x]` or `[-]`), log file/commit references, and update the `Last Updated` date and Chronological Session Progress Journal.
3. **Verbatim Milestone Preservation:** Record any new professor milestone instructions verbatim in `docs/THESIS_MASTER_TASKS.md` under their dedicated milestone section.
4. **Living Glossary Synchronization:** Whenever new technical, legal, statistical, or ML terms, metrics, algorithms, or doctrines enter the manuscript or codebase, append plain-language definitions and thesis context to [`docs/GLOSSARY.md`](file:///c:/Users/SHRIMP/Documents/thesis-repo/docs/GLOSSARY.md).

---

## **2. Author Action Routing & Re-Run Triggers**

* **Yahyah Odin ("Yah", Host A Desktop):** ML modeling, retrieval benchmarking, pipeline automation, manuscript synthesis, and full-document audits. Always surface the top pending priority from `docs/THESIS_MASTER_TASKS.md` upon greeting.
* **Ralph Paolo Dulce ("Ralph", Host B GPU Laptop):** Local ordinance OCR experiments, Chapters 4–5 defense slides (`docs/PRESENTATION_SLIDES_MOCK_DEFENSE.md` synced via `scripts/sync_slides_viewer.py`), Reference PDF collection (`docs/ref_auditor.html`, `docs/flagged_references.json`), HRMO/City Administrator routing (`docs/annotation/hrmo_city_admin_approval_request_letter.md`), and annotator Civil Service 201 certificates.
* **Ordinance Text Update & Empirical Re-Run Trigger:** Whenever updates land in `cleaned_transcriptions/`, `corpus/city_ordinances/`, or `data/unified_dual_statutory_provisions.jsonl`, immediately re-run affected EDA, word/token counts (`scripts/figures/generate_word_count_temporal_figure.py`), dual-corpus token compliance metrics, and downstream retrieval/NLI evaluations, then verify and sync shifted tables/figures in Chapters 3 and 4.

---

## **3. Canonical Standing Context (Current State)**

* **Canonical Dual Statutory Corpus:** `25,432` national laws (Lawphil) + `1,816` deduplicated Davao City ordinances = **`27,248` unique enactments** and **`177,423` unique provisions** (live demo serialized index in `src/demo/app.py` indexes `176,421` provisions).
* **Dual Conflict Scope:** Vertical preemption (*Magtajas*, RA 7160 §5(a)) + Horizontal intra-jurisdictional coherence across fellow Davao City ordinances.
* **Standing Institutional Decisions:**
  * Problem Statement 5 / Objective 5 modification (15 SP legal researchers evaluation) remains subject to formal adviser and defense panel sign-off; SP referred approval to the City Administrator via HRMO.
  * Official Certificate of Contribution & Commendation approved by Ma'am Grace Tacadao for SP legal researchers' Civil Service 201 records (70-pair workload).

---

## **4. Master Document Structure & Agent Updating Protocol**

`docs/THESIS_MASTER_TASKS.md` maintains: (1) Executive Status & Active Milestone Banner, (2) Canonical Hardware & Software Reference, (3) Repository & Git Sync Details, (4) Verbatim Milestone Archive, (5) Granular Task Checklists (`[x]` Completed, `[-]` In Progress, `[ ]` Pending, `[?]` Needs Verification), and (6) Chronological Session Progress Journal.

* **Keep Synchronized with Git:** Commit and push `docs/THESIS_MASTER_TASKS.md` alongside associated code or manuscript edits.
* **Preserve Completed History:** Never purge completed milestones or historical journal entries; mark completed items `[x]` with links/notes.
* **Proactive Next-Step Signaling:** Close responses by referencing the next active pending item in `docs/THESIS_MASTER_TASKS.md`.
