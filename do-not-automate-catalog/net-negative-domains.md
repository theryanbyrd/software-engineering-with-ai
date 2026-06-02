# Domains Where AI Is Currently a Net Negative (Ch 33.5)

> Companion to *Software Engineering with AI*, Chapter 33.5 — the concrete counterpart to
> the property-based [Do-Not-Automate catalog](README.md) (Ch 33). Ch 33 is a taxonomy of
> *task properties* (irreversibility, blast radius, audit requirements). This is the
> *domain* list: specific areas where, as of mid-2026, the honest accounting says the
> agent's output costs more to repair than the human's costs to write from scratch.

"Adoption advice that doesn't name its exceptions is marketing." A reader should be able
to name where this technology fails. In every domain below the rule is the same: **the
critical path stays human; the agent does the adjacent work** (test harnesses, fuzzing,
docs, fixtures, boilerplate).

| Domain | Why it's net-negative today | Agent is fine for… |
|--------|-----------------------------|--------------------|
| **Hard real-time systems** | Flight control, automotive ECUs, medical infusion pumps, industrial control. Certification regimes (DO-178C, ISO 26262, IEC 62304) demand requirements→code→test traceability the agent loop doesn't produce. The blocker is regulatory pace, not model intelligence. | Test harnesses, simulation, docs, requirements-traceability matrices, boilerplate around the safety-critical core. |
| **Novel cryptographic protocol implementation** | Failure mode is *invisible*: non-constant-time comparisons, weak RNG use, padding oracles, handshake/KDF mistakes — bug classes ordinary tests don't catch, and the slop looks correct to non-specialist reviewers. Training data is full of plausible-but-wrong crypto blog code. | Testing existing impls against known-good vectors, fuzzing harnesses, integrating battle-tested libraries. **Use the libraries specialists wrote; don't let the agent write its own.** |
| **Certain ML research code** | Experiment loops that run, complete, emit a number, and are *numerically* wrong (miswired loss, wrong-axis aggregation, gradient flowing the wrong way). The experiment confirms/denies a hypothesis on wrong numbers. | Data loaders, plotting utilities, experiment boilerplate. (Production ML pipelines/serving/data-eng are fine.) |
| **Certain compiler work** | Optimization passes / register allocators / lowering rules that compile, pass existing tests, and are wrong on edge cases that surface weeks later. The practitioner's "this pass is suspicious" intuition is tacit; the agent produces confidently-wrong passes that cost 30 min to review and reject. | Test generation for existing passes, fuzzing harnesses, IR documentation, bookkeeping code. |
| **Certain database internals** | Query planners, lock managers, WAL, replication, MVCC — correctness boundaries simple tests miss, plus a training set polluted with wrong blog code. **Vector-store internals are particularly bad right now.** | Crash-recovery test harnesses, fuzzing, lock-contention observability, internal-interface docs. |
| **Hardware-adjacent driver code** | Largest gap between "compiles" and "works." Surface API right, lifecycle wrong: refcount leaks on error paths, locks held across sleeps, memory freed while DMA in flight, suspend-resume races. Symptoms (hangs, corruption) don't point at the change. | Userland test programs, docs, regression tests for known bugs. |

## This list will shrink

Most of these are not permanent — they're here because the current combination of
training data, eval harnesses, and verification tooling isn't good enough yet. The
author's end-of-2027 guess:

- **Stay on the list:** hard real-time (certification won't move) and novel cryptography
  (the bug class is structurally invisible to the testing an agent can do).
- **Likely come off:** ML experiment code (better instrumentation + independent numerical
  verification), compilers and database internals (serious domain-specific eval suites +
  the harness work this book is about), and driver code (hardest of the recoverable group;
  needs hardware-in-the-loop testing most teams don't have).

**Related:** [Do-Not-Automate catalog (Ch 33)](README.md) · [autonomy ladder (Ch 32)](../agent-autonomy-levels/) · [net-negative bug classes vs. the seven slop signatures](../checklists/code-smells.md).
