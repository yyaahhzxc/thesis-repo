# Manuscript audit and chapter-by-chapter sweep

One command audits the whole thesis against the four `paper-*.md` rules and then sweeps every chapter slice by slice,
applying fixes in place. Reusable: run it again any time the manuscript changes.

## Run it

From an Antigravity chat (the `run_workflow` tool), using the model you want for the sweep agents
(`model="inherit"` means the active chat model; Claude Sonnet 5.5 High is the recommended balance):

```
run_workflow(ScriptPath="<repo>/scripts/workflows/paper_sweep/workflow.py",
             Description="Full manuscript audit and sweep",
             Args={"mode": "apply"})
```

| Arg | Default | Meaning |
| :-- | :-- | :-- |
| `mode` | `apply` | `apply` edits files in place; `audit_only` edits nothing and reports proposed edits |
| `only_units` | all | any of `introduction`, `literature_review`, `methodology`, `results_and_discussion`, `conclusions`, `abstract`, `appendices_and_bib` |
| `slice_kb` | `80` | target prose-slice size; slices split only before headings |
| `build` | `true` | run `scripts/build_paper.py` (+ one auto-fix attempt) in Phase 3; ignored in `audit_only` |
| `mechanical_model` | `flash` | tier for the read-only appendix/bib structural auditor |
| `dry_run` | `false` | Phase 0 and the slice plan only; spends no LLM tokens |

Before an `apply` run: `git add -A; git commit -m "checkpoint before paper sweep"` so `git diff` shows exactly what the sweep changed.

## Phases

1. **Phase 0 (no tokens)**: `scripts/audit/pre_audit_paper.py` scans every active `.tex` file, `references.bib` and `main.log`
   (prose bans, anonymity, LaTeX/table hygiene, heading structure, stale corpus counts, undefined refs/cites, BibTeX completeness,
   paragraph cadence, plus the `declauding` linter). Output: `output/paper_sweep/<run>/pre_audit.json`.
2. **Phase 1 (read-only, parallel)**: a cross-chapter auditor (RQ/objective mapping, hindsight leakage, canonical counts, abstract anchors)
   and an appendix/bib auditor.
3. **Phase 2 (sequential)**: Chapter 1, 2, 3, 4, 5, abstract, then appendices and bibliography. Each chapter is split into ~80 KB slices
   at heading boundaries; each slice gets a fresh agent that loads all four rule files, reads its whole line range, edits, re-runs the audit
   on its range, and hands a short note to the next slice. Boundaries are re-located by heading text so earlier edits never shift a slice.
4. **Phase 3**: re-audit, full 4-pass build, one build-fixer pass if needed, and `output/paper_sweep_report.md`
   (edits by rule family, CITE/DATA/CONSISTENCY/HUMAN flags, before/after candidate counts, build telemetry).

## Helpers (usable on their own)

```
python scripts/audit/pre_audit_paper.py                              # full deterministic audit -> output/paper_pre_audit.json (+ .md)
python scripts/audit/pre_audit_paper.py --slice chapters/methodology.tex 1 400
python scripts/audit/pre_audit_paper.py --outline
python scripts/audit/pre_audit_paper.py --compare output/a.json output/b.json
python scripts/audit/ref_grep.py ablazo2019designing "batch" "kappa"   # does the cited PDF literally contain this?
```

## Notes

- The auditor reports candidates, not verdicts; agents judge each in context.
- Anything needing a human (unverifiable citation, number that disagrees with a table) is left alone, marked with a `% [CITE|DATA|HUMAN: ...]`
  comment above the paragraph (invisible in the PDF) and listed in the report.
- Rules live in `.agents/rules/paper-*.md`; if the rules change, the sweep follows them automatically because agents read them at the start of every slice.
