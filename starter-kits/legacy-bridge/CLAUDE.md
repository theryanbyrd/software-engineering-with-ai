# Project memory — LEGACY CODEBASE

You are working in a legacy codebase. The rules are different from greenfield.

**Read this whole file before doing anything.** If anything is unclear, ask. Do not improvise on legacy code.

## What you are working with

- **Codebase age:** [N] years (replace with your actual age — most legacy repos in this category are 8-15 years old).
- **Primary language:** [REPLACE]
- **Test coverage:** Partial. Some modules have ~80%; others have 0%. The coverage report lies in places — see Module Status below.
- **Build status:** [REPLACE — "fragile / passes most days," "stable on Linux only," whatever is true]
- **Active development:** [REPLACE — bug fixes only / minor features / heavy active development]
- **Engineers who built it:** Mostly gone. Names of remaining knowledge holders: [LIST].

## Commands

- **Verify (run before claiming work is done):** `bash legacy-bridge-scripts/legacy-verify.sh <module>`
- **Golden master record (one-time per module):** `bash legacy-bridge-scripts/golden-master-record.sh <module>`
- **Discover (find your way around):** `bash legacy-bridge-scripts/discover.sh`
- **Build:** [REPLACE — likely Make, Ant, gradle, npm, etc.]
- **Run tests:** [REPLACE]

## Module status — what's safe and what isn't

This section is more important than any other. Update it as you learn.

| Module | Tests | Documented | Last touched | Owner | Safe to AI-edit? |
|---|---|---|---|---|---|
| `core/` | Sparse, mostly outdated | No | 2024 | [name] | **No — read-only first** |
| `api/v1/` | Good | Yes | This quarter | [name] | Yes, with review |
| `api/v2/` | None | No | 2018 | None alive | **No — explore only** |
| `legacy/billing/` | Golden master only | Partial | 2019 | [name] | **No — golden master tests required for any change** |
| `[your modules]` | | | | | |

**Rule:** if a module is not on this list, treat it as `legacy/billing/` until it is.

## Conventions

The conventions in this codebase are inconsistent. Where you see two patterns, prefer the newer one — but do not refactor old code to match unless that refactor is the explicit task.

- **Inconsistent naming:** snake_case in old code, camelCase in `api/v2/`. Match the surrounding code.
- **Mixed paradigms:** classes in old code, functions in new. Match the surrounding code.
- **Dead patterns:** [LIST any patterns the team has agreed to phase out]

## Restricted areas — much larger than greenfield

**The default for any path not explicitly listed below is RESTRICTED.** You may not edit any file unless its directory is on the allowlist.

**Allowlist (you may propose edits, all reviewed):**
- `legacy-bridge-scripts/`
- `tests/legacy-bridge/`
- `[any modules with green-light status above]`
- This `CLAUDE.md` file (with explicit user approval per change)

**Hard-blocked (never edit, no exceptions):**
- `migrations/` — schema changes are out of scope for AI
- `infra/` — production infrastructure
- `legacy/billing/` — financial logic; CODEOWNER review required for any change
- `legacy/auth/` — authentication; security review required
- `core/` — until characterization tests cover it
- `.github/workflows/`
- Any file matching `*.lock`, `Gemfile.lock`, `package-lock.json`, `Cargo.lock`, `poetry.lock`

## Architecture invariants — what we know

The codebase has invariants we know about (and many we don't). When you discover a new invariant in your work, add it here.

- [REPLACE — example: "Database transactions must be wrapped in `with_retry()` because of intermittent connectivity to legacy MSSQL"]
- [REPLACE — example: "All API responses go through `serializers/legacy.py` which has hand-tuned date formatting we cannot change without breaking 14 customers"]
- [Add as you discover them]

## Forbidden — stricter than greenfield

- **No deletion of any file** without explicit user approval. The codebase has dead-looking code that is, in fact, called by long-running batch jobs.
- **No "modernization" refactoring** without an explicit ticket for that refactor. Touching legacy patterns "while you're in there" is the #1 source of legacy regressions.
- **No dependency upgrades.** They cascade. Open a separate ticket.
- **No `# type: ignore` / `// @ts-ignore` etc. anywhere new.** Legacy code has them; new code does not get them.
- **No silencing of failing tests.** If a test is broken, document it and ask. Do not skip, comment out, or delete.
- **No commits that touch more than 100 lines** (legacy mode is stricter than greenfield's 400).
- **No agent runs at L3 autonomy** in legacy modules. L1 (suggest only) or L2 (single-file edits with review). This is enforced by hooks.
- **No use of production credentials, eval, shell-out with user input** — same as greenfield.

## When `legacy-verify` fails

1. Read all of the error output.
2. Run the failing stage in isolation.
3. **If the golden-master diff fails:** the change broke observable behavior. Either fix the change or update the golden master *with explicit user approval*.
4. **If a unit test fails:** check whether the test is correct. Many legacy tests assert on incidental implementation details; they may be wrong rather than the code being wrong.
5. **If you cannot diagnose:** stop and ask. Do not silence, do not skip, do not retry-with-modifications.

## Cost discipline

- Default: Sonnet for tier-2 work in legacy. Haiku for read-only exploration.
- Opus only for the rare T3 architectural exploration question that justifies the cost.
- **Read-only sessions on legacy code can be expensive.** Set token budgets per exploration session and document what you learned at the end.

## Pointers

- Brownfield plan: `BROWNFIELD_PLAN.md`
- MVH levels rubric: `MVH_LEVELS.md`
- Repo map: `llms.txt`
- Strangler pattern guide: `.claude/skills/strangler-pattern/SKILL.md`
- Architecture (what we know): `docs/architecture-as-known.md` (TBD — you may help build this)
- Architecture decision records (ADRs): `docs/adr/` (often empty in legacy; this is a known gap)

## Honest meta-note for the agent

This codebase has parts that nobody alive understands. The code in those parts works in production but no one can tell you why. When you encounter such a part, your job is to:

1. Recognize it (signs: no recent commits, no tests, comments referring to people who left, complex control flow without obvious purpose).
2. Add a note to the Module status table above with what you observed.
3. *Stop and ask the user* before changing anything. Even if the change looks safe.

The fastest path to a production incident in a legacy codebase is an agent that is "confident enough to act, not knowledgeable enough to be right."
