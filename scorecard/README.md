# AI Readiness Scorecard (Appendix H)

> Companion to *Software Engineering with AI*, Appendix H. The book points here at
> `/scorecard/ai-readiness.xlsx`.

Two ways to score a repo against the book's standards:

- **`ai-readiness.xlsx`** — the fillable scorecard for a **manual** assessment (a
  workshop, a self-audit, or a vendor review where you can't run a script). One row per
  criterion, weighted, with auto-summed category and total scores and a readiness band.
- **`../scripts/ai-readiness-audit.py`** — the **automated** version. Runs the same
  criteria against a real repo and emits HTML/JSON/text. Prefer this when you have the
  repo on disk:

  ```bash
  python3 ../scripts/ai-readiness-audit.py /path/to/your/repo
  ```

The spreadsheet and the script share the same criteria, categories, weights, and chapter
references, so a manual score and an automated score are comparable. Weights: 1 = nice to
have, 2 = important, 3 = critical. Each criterion scores full (pass), half (partial), or
zero (fail) of its weight.

**Readiness bands** (% of max weighted score): **<40%** not ready — start with CLAUDE.md +
verify + hooks; **40–69%** partial — close the criticals; **70–89%** solid; **90%+**
exemplary (the repo's own starter kits score 88–94%).
