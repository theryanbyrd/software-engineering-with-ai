# A Five-Day Plan to Your First Loop

One concrete deliverable per day. Build it rather than read about it.

## Day 1 — Repo memory

- Write the `CLAUDE.md` that captures your **stack, test commands, code style, release rules, and gotchas**.
- Add `.claude/settings.json` listing the shell commands the agent is allowed to run.

## Day 2 — A verification skill

- Pick the **one flow the agent keeps breaking**.
- Put a real browser/API test for it under `.claude/skills/<flow>/scripts/`.
- Make it return a clear **pass/fail, the failing step, and a screenshot or log path**.

## Day 3 — Commands

Add three command files:

- `.claude/commands/babysit.md` — reads your PRs and CI, handles obvious review nits, surfaces design questions.
- `.claude/commands/triage-issues.md` — labels and dedupes new issues, assigns owners.
- `.claude/commands/deploy-watch.md` — checks the live app, reports regressions, **avoids touching production**.

## Day 4 — Turn the commands into loops

```
/loop 5m  /babysit
/loop 15m /triage-issues
/loop 5m  /deploy-watch
```

## Day 5 — Overnight work

- Schedule a `/morning-report` and a `/deep-audit`.
- Write results into `.claude/inbox/`.
- Let the morning loop read from that folder.

---

## The one rule

**Every code-writing loop gets a separate verifier.**

The builder makes the change. The verifier runs the real app. You read the diff.

Skip that and you wake up to fourteen broken PRs with very confident summaries.

> Build the loop — but build it like someone who intends to stay the engineer, not just the person who presses go.
