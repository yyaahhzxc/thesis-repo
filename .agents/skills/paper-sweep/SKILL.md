---
name: paper-sweep
description: Run the full thesis manuscript audit and chapter-by-chapter sweep in one command (deterministic pre-audit, cross-chapter audit, sliced chapter edits against the four paper-*.md rules, build check, report). Use when the user asks to sweep, audit, or re-check the paper, a chapter, or the rules compliance of CS_Undergraduate_Thesis_Template/, including after the paper changed.
---

# Paper sweep

Reusable pipeline in `scripts/workflows/paper_sweep/` (see its `README.md` for every argument).

## When to use

- "Sweep / audit the paper", "check the paper against the rules", "run the paper sweep again".
- After large manuscript edits, before a submission, or after changing `.agents/rules/paper-*.md`.
- For one chapter only, pass `only_units`.

## Steps

1. Ask which model to run on only if the user has not said; the workflow's agents inherit the active chat model
   (Claude Sonnet 5.5 High is the agreed quota/quality balance). Optionally check `swarm` action `models` for quota.
2. Confirm a clean checkpoint exists (`git status`); offer `git add -A; git commit -m "checkpoint before paper sweep"` if not.
3. Optional zero-token preview: `run_workflow(ScriptPath=".../scripts/workflows/paper_sweep/workflow.py", Args={"dry_run": true})`.
4. Run: `run_workflow(ScriptPath=".../scripts/workflows/paper_sweep/workflow.py", Description="Full manuscript audit and sweep", Args={"mode": "apply"})`
   (`"audit_only"` for a report without edits; `only_units` / `slice_kb` / `build` as needed).
5. When it finishes, read `output/paper_sweep_report.md`, show the user the CITE/DATA/CONSISTENCY/HUMAN items, check `git diff --stat`,
   and log the session in `docs/THESIS_MASTER_TASKS.md`.

## Standalone helpers

- `python scripts/audit/pre_audit_paper.py` (deterministic audit, `--slice`, `--outline`, `--compare`)
- `python scripts/audit/ref_grep.py <bibkey> "phrase"` (verify a claim or number against `docs/references/<bibkey>.pdf`)

## Guardrails

Never invent citations or numbers, never alter verbatim legal text, never change canonical counts silently; unresolved items go to the report.
