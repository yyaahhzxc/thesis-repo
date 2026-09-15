---
trigger: always_on
description: This rule mandates that the agent must always inspect, maintain, and update the master thesis task tracking document (docs/THESIS_MASTER_TASKS.md) to preserve cross-session continuity, track progress across both the LaTeX manuscript and Python codebase, and ensure all milestone requirements are rigorously fulfilled.
---

# **Master Task Tracking & Cross-Session Continuity Protocol**

**Institution:** Ateneo de Davao University, Department of Computer Science  
**Project:** *"A Coarse-to-Fine Semantic Conflict Detection System for Ex-Ante Davao City Ordinances Using Information Retrieval and Natural Language Inference"*  
**Authors:** Ralph Paolo Dulce & Yahyah Odin  
**Adviser:** Mr. Adrian "Ogs" Ablazo | **Professor:** Ma'am Grace Tacadao  

---

## **1. Author Identity & Collaborative Multi-User Handling**

**Thesis Proponents:**
* **Yahyah Odin ("Yah")**: Primary technical lead on machine learning modeling, retrieval benchmarking, paper drafting, and script automation.
* **Ralph Paolo Dulce ("Ralph")**: Co-author leading human evaluation deployment (Google Forms, annotator coordination, Sangguniang Panlungsod administrative communication, annotator guidebook).

**Operational Greeting & Execution Behavior:**
1. **When User is Identified as Yah ("I'm Yah", "Yah here", etc.):**
   - Immediately recognize Yah as the lead author.
   - Ground directly into `docs/THESIS_MASTER_TASKS.md`, execute tasks with precision, and update the master task tracking checklist as work progresses.
2. **When User is Identified as Ralph ("I'm Ralph", "Ralph here", etc.):**
   - Recognize Ralph and present a collaborative status briefing:
     > *"Welcome Ralph! Here is the current progress briefing and task status based on the latest updates logged by Yah in `docs/THESIS_MASTER_TASKS.md`: [brief bullet summary of recent progress].*  
     > *Here are your primary active action items:*
     > *- [ ] Create Google Forms for Ground Truth evaluation (5 panels, 70 pairs each)*
     > *- [ ] Draft official Sangguniang Panlungsod annotator engagement email*
     > *- [ ] Compile the Annotator Guidebook PDF*
     > *How can we assist you today?"*
3. **When No Name is Specified:**
   - Default to checking `docs/THESIS_MASTER_TASKS.md` immediately, maintain full situational awareness, and execute requests while preserving continuous task synchronization.

---

## **2. Core Principle & Agent Operational Mandate**

To ensure seamless progress across multiple conversations and prevent repetitive context re-prompting:
1. **Living Source of Truth:** The file [`docs/THESIS_MASTER_TASKS.md`](file:///c:/Users/SHRIMP/Documents/thesis-repo/docs/THESIS_MASTER_TASKS.md) serves as the persistent, centralized record of all completed, active, and pending tasks across the thesis manuscript, codebase, empirical benchmarks, and milestone submissions.
2. **Mandatory Check on Conversation Start:** At the beginning of any new conversation or before undertaking major additions or revisions, the agent must check `docs/THESIS_MASTER_TASKS.md` to ground itself in the active milestone, recent progress, open questions, and pending deliverables.
3. **Atomic Task Updates:** Whenever any task, code implementation, empirical experiment, or LaTeX revision is completed, the agent must immediately update `docs/THESIS_MASTER_TASKS.md`, changing status indicators (`[ ]` $\rightarrow$ `[x]` or `[-]`), logging relevant commit/file references, and updating the progress timestamp.
4. **Verbatim Instruction Preservation:** Whenever the user provides instructions for a new milestone (e.g., Milestone 2, Milestone 3, Final Defense), the agent must record the full, unabridged instructions verbatim in `docs/THESIS_MASTER_TASKS.md` under a dedicated milestone section to preserve complete contextual fidelity for future turns.

---

## **2. Master Tracking Document Structure (`docs/THESIS_MASTER_TASKS.md`)**

The master tracking document must maintain the following core sections:
1. **Executive Status & Active Milestone Banner:** High-level summary of active focus, deadlines, and current system status.
2. **Exact Hardware & Software Environment Reference:** Canonical specifications of the local LGU simulation testbed (CPU, GPU, RAM, OS, Python version, key library versions).
3. **Repository & Version Control Details:** Canonical repository URL, branch structure, and reproducibility setup.
4. **Verbatim Milestone Instructions Archive:** Complete, unedited milestone prompts provided by the course professor.
5. **Milestone-by-Milestone Audit & Task Checklist:** Granular, checkable action items categorized by:
   * **LaTeX Thesis Manuscript (`CS_Undergraduate_Thesis_Template/`)**
   * **Core Engine, Models & Scripts (`src/`, `scripts/`)**
   * **Evaluation Benchmark & Human Annotation (`data/`, `docs/annotation/`)**
   * **Documentation, Reproducibility & Build Validation (`README.md`, `requirements.txt`)**
6. **Task Status Legend:**
   * `[x]` **Completed**: Fully implemented, documented, and verified.
   * `[-]` **In Progress**: Actively being drafted, coded, or benchmarked.
   * `[ ]` **Pending**: Planned work scheduled for the active or upcoming milestone.
   * `[?]` **Requires Verification / Consultation**: Awaiting user, adviser, or professor decision.
7. **Change Log / Chronological Milestone Journal:** Brief date-stamped summaries of what was accomplished in each session.

---

## **3. Agent Updating Protocol**

* **Keep It Synchronized with Git:** All updates to `docs/THESIS_MASTER_TASKS.md` must be committed and pushed alongside the associated code or manuscript edits.
* **Never Delete Completed History:** When tasks are finished, mark them as `[x]` with a brief note or link to the corresponding file/section. Do not purge completed milestones, as they provide critical traceability and defense review records.
* **Proactive Next-Step Signaling:** At the conclusion of each response, the agent should briefly reference the next pending item from `docs/THESIS_MASTER_TASKS.md` to maintain momentum.
