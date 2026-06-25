# Incident Response Runbook (python-service)

> Incident response and postmortem runbook for a codebase where some changes are
> authored by AI agents (Claude Code and similar). It extends a normal IR process
> with the questions you only need to ask once an agent is in the loop.

## When to use this

Open an incident when a change causes (or threatens) customer-visible breakage,
data loss, a security exposure, or a failed deploy that cannot be rolled forward
quickly. The process is the same whether a human or an AI agent wrote the code —
the goal is restore first, explain later, blame never.

## Roles

- **Incident commander (IC):** owns the response, coordinates, makes the call to
  roll back. Always a human.
- **Scribe:** keeps a timestamped log in the incident channel.
- **Subject-matter responders:** pulled in as needed.

## The loop (mitigate → diagnose → resolve)

1. **Declare.** State impact, start time, and severity in one sentence.
2. **Mitigate first.** Roll back or feature-flag off before root-causing. A green
   `verify` on the previous commit is the fastest proof a rollback is safe.
3. **Diagnose.** Find the change that introduced the regression (`git bisect`,
   deploy logs, error tracker).
4. **Resolve.** Land a fix through the normal review + `verify` path. Incidents do
   not get to skip the harness.
5. **Postmortem.** Blameless RCA within 3 business days (see template below).

## AI-authored-code procedures

When the offending change was written or substantially edited by an AI agent, the
RCA must additionally answer:

- **Provenance.** Which agent/session produced it? Was it committed under the
  agent trailer, and did a human approve the PR?
- **Harness gap.** Why did `verify` (lint, typecheck, tests) not catch it? An
  AI-introduced defect that passed CI is a missing test or a missing lint rule —
  add the check as part of the fix so the same class of bug can't recur.
- **Scope drift.** Did the agent touch files outside the ticket's stated scope?
  If so, tighten `.claude/settings.json` permissions or a protected-paths hook.
- **Prompt/context cause.** Was the root cause a stale or ambiguous instruction in
  `CLAUDE.md` or a spec? Fix the instruction, not just the code.
- **Confident-wrong failure.** Did the agent assert the work was done without
  evidence? Reinforce "demand evidence, not assertions" in the relevant skill.

The deliverable of every AI-related incident is at least one durable harness
change — a new test, lint rule, hook, or `CLAUDE.md` edit — not just a patch.

## Blameless postmortem template

```
# Postmortem: <short title>
- Date / duration:
- Severity / customer impact:
- Author of the change (human / AI agent / pair):
- Detection (how we found out, and how long it took):

## Timeline (UTC)
- hh:mm  ...

## Root cause (RCA)
What actually happened, mechanism not symptom.

## Why the harness missed it
Which verify layer should have caught this and didn't.

## AI-specific factors
Provenance, scope drift, prompt/context cause (delete if not AI-authored).

## Action items (owner, due date)
- [ ] Durable check added (test / lint / hook / CLAUDE.md):
- [ ] ...
```
