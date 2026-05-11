# Contributing

PRs welcome. This repo is the operating layer for [_Software Engineering with AI_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd. Quality bar is high because mid-size teams will fork this and ship it.

## Quality bar

- **New skills** must pass `scripts/skill-linter.py` (TBD) and include a working example invocation in the skill's README.
- **New hooks** must include a `_tests/` file demonstrating both block and pass cases.
- **War stories** follow `war-stories/_TEMPLATE.md` and must be anonymized — strip company names, identifying tech stack details, and any names of individuals.
- **Reading list entries** must include a `last-verified: YYYY-MM-DD` field.
- **Anything that touches a book chapter** cites the chapter (e.g., "implements Ch 11 §11.6").

## Stack support

First-class stacks are TypeScript, Python, and Next.js. CI tests them every release.

Other stacks (Java, Spring Boot, Go, Rust, Ruby, .NET) live in `starter-kits/community/<stack>/` with a named steward responsible for keeping them current. To propose a new community stack: open an issue with the proposed steward and a working starter that scores 80%+ on the audit.

## Release cadence

Quarterly tagged releases (`v2026.q3`, `v2026.q4`). Between releases, only critical fixes go to `main`. This is the cadence a single maintainer can sustain.

## Errata

Found a mistake in the book? Open an issue tagged `errata` with the chapter and the correction. Errata are tracked in `CHANGELOG.md` per release.

## Code of conduct

Be excellent to each other. Disagree about technical things; don't make it personal.
