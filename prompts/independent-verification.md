# Pattern: Independent Verification

**When to use:** Whenever you're tempted to ask the agent "are you done?" Don't —
self-assessment is systematically unreliable because agents tend toward
self-congratulation (Ch 2 §2.1a). Verify deterministically instead.

**Order of trust (most → least):**

1. **Deterministic check.** Run `verify` (lint, typecheck, tests) and read the *actual*
   output, not the agent's summary of it.
2. **Read the diff yourself.** Every line your name is on (Ch 2 §2.4).
3. **Pull the trace.** Inspect what the agent actually did, not what it says it did.
4. **Only if you must use an agent to verify:** use a *different* agent, in a *different*
   harness, with a *different* system prompt, ideally a *different* model family — and
   treat its assessment as a single noisy signal, never ground truth.

**Template (for step 4):**

```
You are an independent reviewer. Do NOT assume the previous agent's claims are true.
Here is a diff and the task it claims to complete. Verify against the acceptance
criteria: <criteria>. For each, state PASS/FAIL with the specific line(s) of evidence.
Flag any of the seven slop signatures. Report only what you can substantiate from the
diff and test output.
```

**References:** Ch 2 §2.1a (self-congratulation), Ch 6.6 (harness benchmarks), Ch 7
(verify), Ch 8 (verification pyramid).
