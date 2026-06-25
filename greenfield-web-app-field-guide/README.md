# The Greenfield Web App Field Guide

Companion material to *Software Engineering with AI: A Practical Handbook for the Claude Code Era* by Ryan Byrd. This is the greenfield method in a single pass — the field-guide version of the disciplines the book develops chapter by chapter. Cross-references Ch 6 (repo legibility / CLAUDE.md), Ch 7–8 (the single verify command and the verification pyramid), Ch 19–20 (agent-ready issues and the plan → implement → review loop), and Ch 47.6 (the greenfield worked example that applies this method end to end).

> Direct Opus 4.8 like a senior engineer, not a chatbot: **spec first, tickets second, code third, evals always** — with context discipline underneath all of it.

## Start here: what actually changed

You are no longer prompting a chatbot and pasting its answers into an editor. You are directing an agent that reads your files, runs your commands, edits your code, and works through problems while you watch or step away. That shift is the whole game, and almost every technique in this guide follows from two hard constraints of how that agent behaves.

**Constraint 1 — the context window fills up, and quality drops as it does.** Everything the agent sees — your messages, every file it reads, every command's output — lives in one finite context window. A single debugging detour can burn tens of thousands of tokens, and as the window fills, the model starts forgetting earlier instructions and making more mistakes. Context is your scarcest resource. Most of the discipline below exists to spend it well.

**Constraint 2 — "looks done" is the only stop signal unless you give it a real one.** The agent stops when the work looks finished. Without a check it can run itself — a test, a build, a screenshot to diff against a mockup — you become the verification loop, and every defect waits for you to notice it. Give it something that returns pass/fail and the loop closes on its own: it works, runs the check, reads the result, and iterates until the check passes.

The mental model: a brilliant senior engineer with infinite stamina, no memory between sessions, and no instinct for when it's confidently wrong. Your job is to give it tight scope, clean context, and a way to prove its own work.

## 1. Pick a boring, agent-friendly stack

Use a stack the model has seen tens of thousands of times. Density of prior examples matters more than novelty — the agent writes idiomatic, low-surprise code in a popular stack and flails in an exotic one. The legibility of the stack to the agent is itself a feature.

Recommended default:

- **Frontend:** Next.js (App Router), React, TypeScript, Tailwind, shadcn/ui
- **Backend:** Next.js Server Actions / route handlers for most apps; split out a separate NestJS service only when backend complexity genuinely demands it
- **Database / ORM:** Postgres with Prisma or Drizzle
- **Auth:** Clerk, Auth.js, or Supabase Auth
- **Files / jobs:** S3 or R2 for storage; Inngest, Trigger.dev, BullMQ, or SQS for queues
- **Testing:** Vitest (unit), Playwright (E2E), ESLint, TypeScript strict mode
- **Deployment:** Vercel for full-stack Next.js; AWS when you need a VPC or private infra

The App Router gives you Server Components, nested layouts, and first-class loading/error states; Server Actions run mutations on the server without hand-rolling an API. Vercel deploys every push and pull request automatically. None of this is mandatory — the rule is simply: choose tools the agent already knows cold.

## 2. The build packet: CLAUDE.md plus a /docs spec set

Before any code, give the agent persistent context it cannot infer from the codebase. This is two things: a CLAUDE.md that loads on every turn, and a /docs folder of specs it reads on demand.

### CLAUDE.md — the file the agent reads every session

Run `/init` in Claude Code to generate a starter CLAUDE.md from your project, then refine it. (Earlier drafts of this guide called this file `agent-instructions.md`; the real, supported convention is CLAUDE.md, auto-loaded from the repo root, your home folder, and per-directory in monorepos.) It holds commands the agent can't guess, code-style rules that differ from defaults, test instructions, and repo etiquette.

The discipline that matters most: keep it short. A bloated CLAUDE.md causes the agent to ignore your actual instructions, because the real rules drown in noise. For each line ask: "Would removing this cause a mistake?" If not, cut it.

A good starting CLAUDE.md:

```
# Project
Production B2B app. Stack: Next.js App Router, TS strict, Prisma, Postgres.

# Commands
- Typecheck: npm run typecheck
- Lint: npm run lint
- Unit tests: npm run test   (prefer single files: npm run test -- foo)
- E2E: npm run test:e2e

# Workflow
- After a series of edits: typecheck, then run the relevant tests.
- Organize code by feature, not by technical layer.
- IMPORTANT: never modify files outside the ticket's stated scope.

# Conventions
- Validate all inputs with zod at the server boundary.
- No `any` without a one-line comment explaining why.
- Branch naming: feat/<ticket-id>-short-slug
```

Treat it like code: review it when things go wrong, prune it regularly, and confirm a change by watching whether the agent's behavior actually shifts. Knowledge that's only relevant sometimes does not belong here — put it in a skill (a SKILL.md under `.claude/skills/`) so the agent loads it on demand instead of carrying it every turn.

### /docs — the spec set CLAUDE.md points to

Keep the specs that don't need to be in context every turn as files the agent reads when a ticket calls for them:

```
/docs
  product-brief.md      data-model.md      api-contracts.md
  user-stories.md       ux-flows.md        evals.md
  security.md           deployment.md      coding-standards.md
  /mockups              (one image per screen state)
```

## 3. Spec first — and let the agent interview you

The cheapest place to fix a feature is in its spec. Changing a spec costs a sentence; changing shipped code costs hours. For anything non-trivial, don't write the spec alone — have the agent interview you first:

```
I want to build [brief description]. Interview me in detail using the
AskUserQuestion tool. Ask about technical implementation, UI/UX, edge
cases, and tradeoffs. Skip obvious questions; dig into the hard parts
I might not have considered. When we've covered everything, write a
complete, self-contained spec to docs/SPEC-<feature>.md.
```

It surfaces decisions you hadn't made yet. When the spec is solid, start a fresh session to implement it — clean context, focused entirely on the build, with the written spec as the reference. The best specs are self-contained: they name the files and interfaces involved, state what is out of scope, and end with an end-to-end check that proves the feature works.

Each spec answers a specific question:

- **Product brief:** who the users are, the job the app does, what success means, and what is explicitly out of scope.
- **User stories:** "As a [role], I want to [action], so that [outcome]," each with Given/When/Then acceptance criteria.
- **Data model:** entities, fields, ownership, indexes, and lifecycle states.
- **API contracts:** named inputs and outputs even for Server Actions — `CreateProjectInput`, `CreateProjectResult`, `ProjectListItem`, `ProjectDetail`.
- **UX states:** one mock per screen state — empty, loading, error, permission-denied — plus mobile and desktop where it matters.

## 4. The core loop: explore → plan → implement → commit

Letting the agent jump straight to code is how it confidently solves the wrong problem. Separate thinking from doing with plan mode:

- **Explore.** In plan mode, have it read the relevant code and answer questions — no edits. "Read /src/auth and explain how we handle sessions and login."
- **Plan.** Ask for a detailed plan. Demand specifics, or you'll get a paragraph: "List the exact files to change, the functions to modify in each, and the order of operations."
- **Review the plan.** This is the cheap gate — your last chance before code exists. Are the steps ordered correctly? Anything missing or out of scope?
- **Implement, then commit.** Leave plan mode, let it build against the approved plan, run the checks, then commit with a descriptive message and open a PR.

When to skip planning: if you could describe the diff in one sentence — a typo, a log line, a rename — just ask for it directly. Planning earns its overhead when the approach is uncertain, the change spans multiple files, or you don't know the code well.

## 5. Work in small tickets with specific context

Never say "build the dashboard." Hand the agent one tightly scoped ticket at a time, and point it at exact sources rather than describing them. Precision in the prompt is the cheapest way to cut corrections.

A good ticket looks like this:

```
Implement the Project List screen.
  Spec:    docs/user-stories.md US-004
  Mock:    docs/mockups/project-list.png
  Data:    Project (see docs/data-model.md)
  UI:      reuse shadcn/ui; match existing list screens
Requirements:
  - Server-side fetch; search by name; empty + loading states
  - Playwright test for the happy path and the empty state
  - No unrelated refactors
Verify: run npm run test:e2e and show me the output.
```

## 6. Always give it a way to verify its own work

This is the single highest-leverage habit. The check is anything that returns a signal the agent can read: a test suite, a build exit code, a linter, a script that diffs output against a fixture, or a browser screenshot compared to a design.

Demand evidence, not assertions. Have it show the test output, the command it ran and what came back, or a screenshot — not "done ✅." Reviewing evidence is faster than re-running the check yourself, and it's the only thing that works for a session you weren't watching. If you can't verify it, don't ship it.

## 7. Evals: layers of "is it actually working?"

Stack the checks so each layer catches what the one below it can't. One concrete example per layer:

- **Static:** TypeScript compiles, ESLint clean, no unused vars, no circular imports, no forbidden dependencies.
- **Unit:** business rules — pricing math, permission checks, state transitions, validation, date/time handling.
- **Integration:** create user → create project → invite teammate → upload file → run workflow → assert DB state.
- **Browser (Playwright):** sign up, complete onboarding, create/edit/delete an object, see the right error, and confirm an unauthorized user is blocked.
- **Visual:** screenshot against the mockup — layout roughly matches, required text present, primary CTA visible, no overflow, mobile works.
- **AI-assisted:** feed a screenshot and the target mock to a model and ask for missing elements, layout errors, and broken interactions, each rated severity 1–5.

Why a deterministic test suite isn't enough: generative output varies run to run, so ordinary fixed-input/fixed-output tests don't fully cover behavior — hence the layered, partly model-judged approach above.

Caveat on adversarial reviewers: a reviewer told to find gaps will find some even when the work is sound — that's what it was asked to do. Chasing every finding leads to over-engineering. Tell it to flag only gaps that break correctness or a stated requirement, and treat the rest as optional.

## 8. Manage context like the budget it is

Because context is the scarce resource, spending it well is most of the skill. The same long session that feels productive is often the reason quality quietly degrades.

- **Clear between unrelated tasks.** Run `/clear` when you switch problems. A clean window with a sharp prompt beats a long one full of stale file reads.
- **The two-correction rule.** If you've corrected the agent twice on the same issue, the context is polluted with failed approaches. `/clear` and restart with a better prompt that bakes in what you learned.
- **Delegate research to subagents.** "Use subagents to investigate how token refresh works." They read the files in a separate window and report back a summary, keeping your main context clean for implementation.
- **Compact deliberately.** Use `/compact` with instructions ("preserve the list of modified files and the test commands") so the summary keeps what matters.
- **Rewind freely.** Every prompt is a checkpoint. Try something risky; if it fails, rewind conversation and code and take a different line. (Checkpoints track only the agent's edits — they are not a substitute for git.)

## 9. Repository structure

Organize by feature, not only by generic technical buckets. A feature folder keeps its UI, server actions, queries, schema, and tests together so a ticket touches one place.

```
/src
  /app                      route entries, layouts
  /components               shared, cross-feature UI
  /features
    /projects
      components/  actions/  queries/  schema.ts  tests/
  /lib  /server  /db  /auth  /emails
/tests/e2e   /docs   /prisma
```

## 10. Guardrails: advisory rules and hard gates

CLAUDE.md rules are advisory — the agent usually follows them. For things that must happen every time with zero exceptions, use a hook: a script that runs at a fixed point ("run ESLint after every edit," "block writes to the migrations folder") and is deterministic, not a suggestion.

Standing rules worth keeping:

- Never modify files unrelated to the ticket.
- Never change the database schema without a migration.
- Never delete or weaken tests to make the build pass.
- Never hardcode fake data into production paths, or bypass auth for convenience.
- Never introduce `any` without a one-line reason. Never duplicate a component that already exists.

Done means done. A feature is complete only when the UX matches the mock, acceptance criteria pass, typecheck and lint are clean, unit and Playwright tests pass, there are no console errors, and the docs are updated.

## 11. Scale: parallel sessions, writer/reviewer, and headless runs

Once one agent is reliable, multiply throughput — with eyes open about cost, since each parallel context multiplies token usage.

- **Worktrees / parallel sessions:** run separate sessions in isolated git checkouts for unrelated workstreams so edits don't collide.
- **Writer / reviewer:** one session implements; a second, fresh session reviews the diff. The reviewer isn't biased toward code it just wrote, so it catches more.
- **Headless mode:** `claude -p "…"` for CI, pre-commit hooks, and large migrations. Loop it over a file list with `--allowedTools` to scope what it can do unattended.
- **Automate the loop:** once a step is reliable, stop typing it. `/loop <interval> <prompt>` re-runs a prompt on a timer (`/loop 15m run the tests, and if anything fails use /fix-tests`); `/goal` keeps iterating until a condition is true and then stops. Nest them — the timer re-arms the work, the goal defines verified-done. A `/loop` is session-bound by design and auto-expires after a few days, so for anything that must outlive a closed laptop climb the persistence ladder: `/loop` (in-session) → `/schedule` (cloud cron, hourly/daily) → Routines (cloud-hosted, survives the machine being off). See the Loop Engineering chapter for the full treatment.
- **Mind the bill:** subagent- and team-heavy workflows can burn several times the tokens of a single session. The time savings usually justify it on big tasks — but decide on purpose.

```
# Fan out a migration across many files
for f in $(cat files.txt); do
  claude -p "Migrate $f from React to Vue. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)"
done   # test on 2-3 files first, refine the prompt, then run at scale
```

## 12. Deployment and observability

Start simple and let the environments mirror your build loop.

- **Dev:** local Postgres or a Neon/Supabase branch DB, `.env.local`, seed data.
- **Preview:** every PR deploys automatically to its own URL on a branch DB; run Playwright smoke tests against it.
- **Production:** Vercel or AWS, managed Postgres, Sentry for errors, PostHog or Amplitude for product analytics, uptime checks, backups, and alerts.

Vercel fits because pushes and PRs trigger deploys automatically and infra is billed by usage — requests, data transfer, function duration.

## 13. The build sequence

Work in this order, and make the first vertical slice go all the way through before you widen:

1. Repo setup
2. Auth
3. Database schema
4. Design system
5. App shell and navigation
6. First vertical slice: UI → server action → DB → test → deploy
7. CRUD screens
8. Permissions
9. Background jobs
10. Notifications and email
11. Admin tools
12. Eval and test hardening, then observability, then launch

Once that first slice works end to end — from the rendered UI through the server action to the database, with a passing test and a live deploy — you've proven the whole path. Then you just repeat it.

## 14. Common failure patterns

Recognizing these early saves hours:

- **The kitchen-sink session:** one task, then an unrelated detour, then back — now the context is full of noise. Fix: `/clear` between tasks.
- **Correcting in circles:** two failed corrections means the context is polluted. Fix: `/clear` and write a sharper opening prompt.
- **The bloated CLAUDE.md:** too long, so the agent ignores half of it. Fix: prune ruthlessly, or convert a rule into a hook.
- **The trust-then-verify gap:** plausible code that misses edge cases. Fix: always provide a check; if you can't verify it, don't ship it.
- **Infinite exploration:** an unscoped "investigate this" reads hundreds of files. Fix: scope it, or hand it to a subagent.

## 15. The master prompt to kick things off

Run this in plan mode, before any code exists:

```
We are building a production-grade web application. Read these first:
  docs/product-brief.md     docs/architecture.md
  docs/data-model.md        docs/user-stories.md
  docs/ux-flows.md          docs/evals.md  docs/coding-standards.md
Your job, in plan mode (do NOT write code yet):
  1. List every ambiguity or contradiction you find.
  2. Propose the first 10 implementation tickets, smallest first.
  3. For each ticket: files likely touched, tests required, and
     acceptance criteria.
  4. Make ticket 1 a vertical slice: UI -> server action -> DB -> test.
```

Then, per ticket: "Implement ticket N from your plan. Write the tests, run the suite, and show me the output. No unrelated refactors."

And before calling anything done: "Use a subagent to review this diff against the ticket. Confirm every requirement is implemented and tested, and that nothing outside scope changed. Report gaps that affect correctness, not style."

The pattern, start to finish: **spec first, tickets second, code third, evals always** — with context discipline underneath all of it.
