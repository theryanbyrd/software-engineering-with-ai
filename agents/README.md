# Subagents — A Small Team Inside the Harness

Companion to *Software Engineering with AI* by Ryan Byrd · Chapter 14 / Appendix F

Subagents are pre-configured roles the main Claude Code session can delegate to. Each has a tight system prompt, an explicit tool allowlist, and a focused output contract. They are not faster than the main session; they are more reliable because the surface area is smaller.

| File | Role | When to invoke |
|---|---|---|
| [`planner.md`](planner.md) | Read-only planner. Produces a step-by-step plan; does not write code. | Start of any T2+ task |
| [`test-writer.md`](test-writer.md) | Writes failing tests from a spec before implementation. | After plan, before code |
| [`reviewer.md`](reviewer.md) | Adversarial reviewer with the seven slop signatures (Ch 2) loaded. | Before opening a PR |

## How to install

Each subagent lives in your repo's `.claude/agents/` directory. Claude Code discovers them automatically.

```bash
mkdir -p .claude/agents
cp /path/to/this/repo/agents/*.md .claude/agents/
```

Working examples wired into starter kits: [`../starter-kits/typescript-monorepo/.claude/agents/`](../starter-kits/typescript-monorepo/.claude/agents/).

## Quality bar for contributing a new subagent

A new subagent PR must include:

1. **Tight role definition.** "You are a senior X engineer specializing in Y." Three sentences max.
2. **Explicit tool allowlist.** Read-only subagents should declare it explicitly (`tools: read, grep, glob`); write-capable ones should justify why.
3. **An "I am done" contract.** What does success look like? What is the subagent forbidden from claiming?
4. **A regression test in `/benchmarks/`.** What task does this subagent get right, and how do we know if it stops getting it right? (See Ch 6.6.)
5. **A no-self-congratulation clause.** Empty findings is a valid output (Ch 2 §2.1a). Required for any reviewer- or auditor-style subagent.
