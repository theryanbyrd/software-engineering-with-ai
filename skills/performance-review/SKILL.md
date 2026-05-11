---
name: performance-review
description: Use when investigating slow code paths or performance regressions. Profiles, identifies hot paths, proposes changes — but does NOT prematurely optimize. The output is a measurement plus a recommendation, not a code change.
allowed_tools: Read, Bash, Grep
---

# Performance review

## When to use this skill

The user reports slowness, a performance regression, a SLO breach, or asks "is this fast enough?" The deliverable is analysis, not (necessarily) a code change.

## Procedure

1. **Identify the actual hot path.** Do not assume. Use profiling output, traces, or load-test data. If none exist, propose what to measure first.
2. **Read the code in the hot path.** Look for:
   - O(n^2) where O(n) would do (nested loops over the same collection)
   - Unbatched calls in a loop (N+1 queries, sequential HTTP when concurrent would work)
   - Expensive operations in hot loops (regex compile, JSON parse, hashing)
   - Synchronous blocking IO where async would help
   - Cache misses — check for missing memoization on pure functions
3. **Quantify.** "This loop runs 1000x per request and each call takes 5ms" beats "this loop is slow."
4. **Propose changes in priority order:**
   - Highest impact first (the one change that moves the meter most)
   - Cheapest change next (smallest diff for a measurable improvement)
   - Riskier changes last
5. **For each proposed change:** estimate the expected speedup. State the assumption that could make the estimate wrong.
6. **Recommend whether to implement now.** If current performance meets SLO, the answer is often "no, document for later."

## Output

```
## Performance review

**Hot path:** <function/endpoint>
**Current performance:** <measured number — p50, p95, p99 latency or throughput>
**Target / SLO:** <if defined>

## Analysis

(One paragraph per finding, with code references and quantified impact)

## Recommendations (priority order)

1. <change> — expected impact: <estimate> — risk: <low/med/high>
2. ...

## Recommended action now

[ ] Implement #1 — expected to bring p95 from X to Y, low risk
[ ] Defer #2 and #3 — current performance is within SLO
```

## Forbidden

- Do not optimize without measurement. "Speed up the loop" without numbers is premature optimization.
- Do not propose a rewrite. The skill's output is targeted changes, not greenfield rebuilds.
- Do not ignore the simplicity cost. A 5% speedup that doubles complexity is usually a bad trade.
- Do not optimize a path that isn't the bottleneck. If 90% of latency is in a downstream service, optimizing local code won't help.

## References

- Chapter 8 §8.x — performance and observability
- Chapter 22 — but note that "premature optimization" is itself a slop signature
