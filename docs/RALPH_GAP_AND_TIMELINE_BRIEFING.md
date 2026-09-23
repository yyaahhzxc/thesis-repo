# **Quick Briefing for Ralph: Workflow Solutions & Timeline**

**To:** Ralph Paolo Dulce  
**From:** Yahyah Odin  
**Date:** September 22, 2026  

---

Hey Ralph! While reviewing our timeline and connecting Stage 1 and Stage 2 into the complete live pipeline, I spotted 7 simple but crucial operational gaps we needed to solve before defense. I already updated our paper (Chapters 2 and 3) so we’re 100% covered. 

Here is the quick TL;DR of each problem and our solution:

* **The Big Question (How to test the finished system?):** We evaluate the complete pipeline using a **3-Tier Framework**: Tier 1 (blind test on our 53 locked test pairs), Tier 2 (stress-testing full synthetic drafts with deliberate conflict "traps" while checking if innocent sections are left alone), and Tier 3 (running real historical Supreme Court clashes like the Davao aerial spraying ban *Mosqueda v. PBGEA* + SP user study).
* **Gap 1 (Testing full drafts vs OCR noise):** Live drafts submitted by SP drafters are clean Word/PDF files (digital-born), not messy physical scans; our preprocessor tests clean text and automatically skips procedural boilerplate (Title, Separability, Repealing, and Effectivity clauses).
* **Gap 2 (Scoring candidates for whole documents):** We don't cut candidate laws (keeping all 50 to preserve Stage 1 recall); Stage 2 evaluates them in parallel batches in $\approx 4\text{ seconds}$ on GPU, using a Max-Pooling rule to alert on the highest contradiction score per section.
* **Gap 3 (National preemption vs local ordinance amendments):** We separated alerts into two colors—**🔴 Red Alert** for illegal national law preemption (*Magtajas* doctrine), and **🟡 Amber Notice** for older local ordinance updates (reminding the drafter to check their repealing clause).
* **Gap 4 (XAI on the web dashboard):** Keep it clean and practical: the UI will show total contradiction count, a side-by-side view of the draft clause vs governing statute, the confidence percentage, and highlighted clash words (e.g., *prohibited* vs *allowed*).
* **Gap 5 (The 2-Phase SP Evaluation Timeline):** We split SP testing into two separate phases so we don't bottleneck:
  * **Phase 1 (NOW – by 2nd week of October):** 15 SP researchers label the 350 Ground Truth pairs on Google Forms for Fleiss' Kappa (our answer key; does not need the AI to be finished).
  * **Phase 2 (Late October – before mid-Nov defense):** SP researchers test the finished web prototype and answer the 10-question SUS usability survey.
* **Gap 6 (Offline City Hall deployment):** We will permanently download and pin the winning model's weights folder (`local_files_only=True`) so the system runs 100% offline without needing internet during City Hall testing or panel defense.

---

**Immediate Action for Ralph:** Let's finalize the Google Forms and Guidebook PDF and send the official SP endorsement email ASAP for Phase 1!
