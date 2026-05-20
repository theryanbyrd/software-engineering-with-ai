# Reusable GitHub Actions

The audit and reading-list-staleness workflows wired into this repo live in [`../../.github/workflows/`](../../.github/workflows/). Copy them into your own repo and adjust the threshold/paths.

| Workflow | What it does |
|---|---|
| [`audit.yml`](../../.github/workflows/audit.yml) | Runs the AI-readiness audit against each starter kit on every PR |
| [`reading-list-stale.yml`](../../.github/workflows/reading-list-stale.yml) | Weekly cron — flags stale entries in `reading-list/` |
