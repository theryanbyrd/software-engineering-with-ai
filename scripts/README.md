# Scripts

Standalone tools referenced throughout the book. All run with `python3 <script> --help` and have no dependencies beyond the standard library unless noted.

| Script | What it does | Book |
|---|---|---|
| [`ai-readiness-audit.py`](ai-readiness-audit.py) | Scores any repo against the book's harness standards; HTML report | Appendix H |
| [`slop-detector.py`](slop-detector.py) | Flags the seven slop signatures in a diff or PR | Ch 2, Ch 22 |
| [`skill-linter.py`](skill-linter.py) | Validates SKILL.md frontmatter and structure | Ch 13, Ch 18 |
| [`pr-ai-tagger.py`](pr-ai-tagger.py) | Tags PRs with AI-authorship metadata for telemetry | Ch 21, Ch 31 |
| [`token-cost-estimator.py`](token-cost-estimator.py) | Models monthly token spend from usage assumptions | Ch 26, Ch 29 |
| [`cursorrules-to-claude-md.py`](cursorrules-to-claude-md.py) | Migrates .cursorrules to CLAUDE.md | Ch 53 |
| [`llms-txt-generator.py`](llms-txt-generator.py) | Generates llms.txt from repo structure | Ch 10 |

Quickstart:

```bash
python3 scripts/ai-readiness-audit.py /path/to/your/repo
open audit-report.html
```
