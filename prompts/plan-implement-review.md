# Pattern: Plan → Implement → Review

**When to use:** The core loop for any change beyond a trivial edit (Ch 20). Keep the
human owning intent, architecture, and the merge gate.

**Template — Plan:**

```
Read <relevant files>. Produce a plan for <task> before writing any code:
- the approach and why
- the files you'll change and how
- the tests you'll add
- the edge cases and risks
- anything you'd need clarified
Do not edit yet. Wait for my approval of the plan.
```

**Template — Implement (after you approve the plan):**

```
Implement the approved plan. Keep the diff small and scoped (<~400 lines). Follow the
conventions in the surrounding code. Run verify and report the actual output.
```

**Template — Review (independent):** use
[`independent-verification.md`](independent-verification.md) and
[`slop-review.md`](slop-review.md). Then read the diff yourself.

**References:** Ch 20 (Plan → Implement → Review Loop); merge gate stays human (Ch 2 §2.4).
