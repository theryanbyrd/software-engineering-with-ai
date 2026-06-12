# Prompt Injection Test Suite

Six red-team test cases for AI agents that handle untrusted inputs. Direct implementation of Chapter 37 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.

**Run all six quarterly. Treat any pass-to-fail regression as a P1 incident.**

## What this is

A standardized test harness for the six exercises in chapter 37. Each exercise is realized as:

1. A markdown file in `cases/` describing the test scenario, the pass criterion, and the threat model
2. A fixture in `fixtures/` containing the actual injection payload
3. An entry in the `runner.py` that orchestrates the test against your agent
4. Expected behavior documented in machine-readable form (`expected.json`)

The suite is **agent-agnostic by design.** It tests the harness — your hooks, your network egress controls, your output filters, your token scoping — not the model. A passing model with a weak harness still fails.

## What this is NOT

- A penetration test. The cases here are surface-level; a determined attacker will go deeper.
- A substitute for a real security review. Use this as a continuous-integration baseline, not a final word.
- A jailbreak benchmark. We are testing operational defenses, not model alignment.

## The six cases

| # | Case | Tests | Where the defense lives |
|---|---|---|---|
| 1 | [Poisoned issue body](test-cases/01-poisoned-issue-body.md) | Instruction injection in user-supplied text | Agent prompt isolation, output filtering |
| 2 | [Malicious PR comment](test-cases/02-malicious-pr-comment.md) | Shell command injection from comment | Bash firewall, network egress allow-list |
| 3 | [Poisoned web page](test-cases/03-poisoned-web-page.md) | Hidden directives in fetched content | Content sanitization, system-prompt isolation |
| 4 | [Poisoned log line](test-cases/04-poisoned-log-line.md) | Log-line injection during summarization | Input parsing discipline |
| 5 | [Cross-repo exfil attempt](test-cases/05-cross-repo-exfil.md) | Token over-scoping | MCP token least-privilege |
| 6 | [Credential in output](test-cases/06-credential-in-output.md) | Secrets leaking through the agent's output | Output-filtering hook |

## Quickstart

```bash
# 1. Install (stdlib only — no dependencies)
cd prompt-injection-test-suite

# 2. Configure your agent endpoint and credentials in a local .env
cp .env.example .env
# edit .env to add ANTHROPIC_API_KEY or your custom agent endpoint

# 3. Run all six cases
python3 scripts/runner.py

# 4. Run a single case
python3 scripts/runner.py --case 01

# 5. Generate the quarterly report
python3 scripts/runner.py --report
```

## Output

The runner writes:

- `results/run-YYYY-MM-DD.json` — machine-readable results for CI / dashboards
- `results/run-YYYY-MM-DD.md` — human-readable summary
- Exit code 0 if all six pass; 1 if any fail

Wire `runner.py` into your CI on a quarterly schedule. The summary should land in front of the security team and the platform-team lead within 24 hours of completion.

## When a case fails

A failure is a P1 incident. The standard response:

1. **Reproduce.** The test runner records the full transcript; reproduce in a controlled environment.
2. **Identify the missing defense.** Each case's markdown identifies *where the defense should live* — bash firewall, output filter, token scoping. If your harness lacks the relevant control, that's a defense gap, not just a test failure.
3. **Patch the harness.** Add the missing hook, tighten the token scope, add the output filter. Patch the harness, not the test.
4. **Re-run the suite.** Confirm the fix and that nothing else regressed.
5. **Document.** Add an entry to your security runbook describing the gap, the patch, and how it was verified.

## Adapting for your agent

The runner ships with a default Claude API adapter. To test a different agent, implement the `Agent` protocol in `scripts/runner.py`:

```python
class Agent(Protocol):
    def run_with_input(self, system: str, user: str, context: dict) -> AgentResponse: ...
```

A `Cursor`, `Codex`, or in-house agent can plug in with ~20 lines of adapter code. See `scripts/adapters/` for examples.

## What the suite cannot test

These six cases cover the most common attack vectors. They do not cover:

- **Multi-step social engineering.** A patient attacker building trust over multiple sessions.
- **Supply-chain attacks.** A compromised dependency injecting at install time.
- **Insider threats.** An authorized user abusing legitimate access.
- **Model-level jailbreaks.** Persuading the model to violate its training.

For those, you need a real security review and a red-team engagement. This suite is the floor, not the ceiling.

## Contributing new cases

We welcome additions, particularly for attack vectors not covered above. Open a PR with:

1. A new file `cases/NN-your-case-name.md` following the template in `cases/_TEMPLATE.md`
2. A fixture in `fixtures/` if needed
3. An entry in `scripts/runner.py`
4. A passing test against a known-good harness, plus a known-failing test against a known-bad harness

The bar: the case must test a defense that lives in the harness (a hook, a filter, a scope), not in the model.
