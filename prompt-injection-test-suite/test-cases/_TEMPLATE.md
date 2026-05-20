# Case NN — [Short title]

## Threat model

<!-- One paragraph describing the attacker's goal and capabilities. -->

## The injection

<!-- The actual payload. Place complex or multi-line payloads in fixtures/. -->

## Setup

<!-- What the test environment needs. Specific repo state, MCP tokens, etc. -->

## How to run

```bash
python3 scripts/runner.py --case NN
```

## Pass criterion

<!-- Specific, observable behavior the agent must exhibit. -->

## Fail criterion

<!-- Specific, observable behavior that constitutes a failure. -->

## Where the defense lives

<!-- The harness component that should prevent the failure: hook, filter,
     egress allow-list, token scope, etc. NOT "the model should refuse." -->

## If this fails

<!-- Step-by-step remediation. Patch the harness, not the test. -->

## References

- Chapter 37 §37.N of the handbook
- Related cases: NN, NN
