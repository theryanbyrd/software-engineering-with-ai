# Contributing

PRs welcome. This repo is the operating layer for [_Software Engineering with AI_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd. Quality bar is high because mid-size teams will fork this and ship it.

## Where to start — pick the matching template

Every contribution that adds a new artifact starts from a template. The templates capture the conventions that the artifact downstream depends on (naming, sectioning, the `_tests/` requirement, the no-self-congratulation clause for subagents). Find your template, copy it, edit, and open a PR.

| Adding... | Template | What the template enforces |
|---|---|---|
| A new skill | [`skills/_TEMPLATE.md`](skills/_TEMPLATE.md) | SKILL.md structure, working example invocation, the skill-linter pass |
| A new subagent | [`agents/_TEMPLATE.md`](agents/_TEMPLATE.md) *(forthcoming)* | Tight role definition, tool allowlist, "I am done" contract, no-self-congratulation clause |
| A new hook | [`hooks/_TEMPLATE.sh`](hooks/_TEMPLATE.sh) *(forthcoming)* | `_tests/` file, documented threat model, performance budget |
| A new war story | [`war-stories/_TEMPLATE.md`](war-stories/_TEMPLATE.md) | Anonymization checklist, root-cause framing, what-we-changed-after section |
| A new prompt-injection test case | [`prompt-injection-test-suite/test-cases/_TEMPLATE.md`](prompt-injection-test-suite/test-cases/_TEMPLATE.md) | Scenario, fixture, pass criterion, threat model |
| A new reading-list entry | [`reading-list/data.json`](reading-list/data.json) (see `schema.json`) | `last-verified` date, category, `dated_through` for auto-pruning |
| An errata correction | _open an issue tagged `errata`_ | Chapter reference + the correction |

If you do not see your template in the table, ask in an issue before starting — odds are an existing template fits with light modification, and we want to keep the surface area small.

## Quality bar (in detail)

- **New skills** must pass `scripts/skill-linter.py` and include a working example invocation in the skill's README. The skill must be exercised by at least one entry in `benchmarks/` so that a future skill regression is caught.
- **New hooks** must include a `_tests/<hook-name>.test.sh` demonstrating both block and pass cases. Hooks should not add more than 200ms to the edit loop.
- **New subagents** must include the no-self-congratulation clause (Ch 2 §2.1a): "An empty findings list is a valid output. Do not invent findings to seem useful." Reviewer-style subagents in particular will be rejected without it.
- **War stories** follow `war-stories/_TEMPLATE.md` and must be anonymized — strip company names, identifying tech stack details, and any names of individuals. The reviewer will spot-check; a story with identifiable details will be returned with a comment, not closed.
- **Reading list entries** must include a `last-verified: YYYY-MM-DD` field and a `dated_through: YYYY-MM-DD` field. Entries past `dated_through` are auto-pruned (`scripts/generate.py --check-stale`) and the weekly CI workflow opens an issue when this happens.
- **Anything that touches a book chapter** cites the chapter (e.g., "implements Ch 11 §11.6"). PRs without chapter references will be returned with a comment.

## CI is real

Every PR runs:

- [`.github/workflows/audit.yml`](.github/workflows/audit.yml) — the AI-readiness audit against each starter kit, with a comment summary posted to the PR.
- [`.github/workflows/reading-list-stale.yml`](.github/workflows/reading-list-stale.yml) — on schedule, but PRs that touch `reading-list/data.json` should also pass locally: `python3 reading-list/scripts/generate.py --validate`.

If a PR fails the audit threshold for the kit it touches, it cannot merge until the regression is fixed. The kit-specific thresholds are tuned for the kit's purpose (legacy-bridge is intentionally lower than the greenfield kits).

## Stack support

First-class stacks are TypeScript, Python, and Next.js (forthcoming in v2026.q4). CI tests them every release.

Other stacks (Java, Spring Boot, Go, Rust, Ruby, .NET) live in `starter-kits/community/<stack>/` with a named steward responsible for keeping them current. To propose a new community stack: open an issue with the proposed steward and a working starter that scores 80%+ on the audit.

## Release cadence

Quarterly tagged releases (`v2026.q3`, `v2026.q4`). Between releases, only critical fixes go to `main`. This is the cadence a single maintainer can sustain.

## Errata

Found a mistake in the book? Open an issue tagged `errata` with the chapter and the correction. Errata are tracked in `CHANGELOG.md` per release.

## Code of conduct

Be excellent to each other. Disagree about technical things; don't make it personal. See [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) for the long form.
