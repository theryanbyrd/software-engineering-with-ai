# The Five Building Blocks (and the Sixth Thing)

A loop needs five capabilities and then one place to remember things. The names differ slightly between Claude Code and the Codex app, but the capability is the same, so the design transfers regardless of which tool you're sitting in.

## 1. Automations — the heartbeat

What makes a loop a loop instead of one run you did once.

- **Claude Code:** scheduling + hooks. Run a prompt/command on an interval, fire a cron task, attach shell commands to points in the agent lifecycle, or push to GitHub Actions so it keeps running after you close the laptop.
- **Codex:** the Automations tab — pick a project, prompt, cadence, and whether it runs on your checkout or a background worktree; findings route to a triage inbox, empty runs archive themselves.

Two in-session primitives are the heart of the whole thing:

- **`/loop`** — re-runs a task on a cadence (e.g. every 5 or 15 minutes) to keep it alive.
- **`/goal`** (both tools) — keeps working across turns until a condition *you wrote* is actually true (`"all tests in test/auth pass and lint is clean"`). Critically, a **separate small model** checks after each turn whether the condition holds. The agent that wrote the code is not the one that decides it's done. That maker-checker split applied to the stop condition is what lets you walk away and trust the word "done."

## 2. Worktrees — parallel without chaos

The moment you run more than one agent, files collide. Two agents editing the same file is two engineers committing to the same lines with no coordination.

A git worktree is a separate working directory on its own branch sharing the same repo history, so one agent's edits cannot touch another's checkout.

- **Claude Code:** `git worktree`, a `--worktree` flag, and `isolation: worktree` on a sub-agent so each helper gets a fresh self-cleaning checkout.
- **Codex:** worktree support built in.

The worktrees remove the collisions. They do **not** remove you — your review bandwidth is still the ceiling on how many parallel agents you can actually run.

## 3. Skills — stop re-explaining the project

A folder with a `SKILL.md` (instructions + metadata) plus optional scripts, references, assets. Runs when called explicitly or when the task matches its description — which is why a **tight, boring description beats a clever one**.

Inside a loop, skills are load-bearing in a way they aren't in interactive use: without them the loop re-derives your conventions, build steps, and hard-won "we don't do it this way because of that one incident" from zero **every cycle**. With them, that intent is written down once on the outside where the agent reads it every run, and the loop compounds instead of resetting.

*Keep the distinction straight:* the skill is the authoring format; a **plugin** is how you ship and share it across repos.

## 4. Plugins & connectors — the loop touches your real tools

A loop that can only see the filesystem is a tiny loop. Connectors (built on MCP) let the agent read your issue tracker, query a database, hit a staging API, drop a message in Slack. Claude Code and Codex both speak MCP, so a connector written for one generally works in the other. Plugins bundle connectors + skills so a teammate installs your whole setup in one step.

This is the difference between an agent that says "here is the fix" and a loop that opens the PR, links the ticket, and pings the channel once CI is green.

*Governance:* a loop with write access to your tracker and cloud can do damage on a schedule. Scope its credentials with the least-privilege discipline of Ch 35.

## 5. Sub-agents — keep the maker away from the checker

The single most useful structural choice. The model that wrote the code is far too generous grading its own homework; a second agent with different instructions and often a different model catches what the first talked itself into.

- Agent definitions as files: TOML in `.codex/agents/`, the equivalent in `.claude/agents/` — each with name, description, instructions, and optional model + reasoning effort. Your security reviewer can be a strong model on high effort; your explorer a fast read-only one.
- Usual division: one explores, one implements, one verifies against the spec.

It matters more inside a loop than in interactive work because the loop runs while you're not watching, so a verifier you actually trust is the only thing that makes walking away defensible. Sub-agents burn more tokens — spend them where a second opinion is worth paying for, which is anything that writes code.

## The sixth thing — memory

A markdown file, a Linear board, anything that lives outside a single conversation and holds what's done and what's next. Sounds too dumb to matter; it's the part everything else depends on. The model forgets everything between runs, so the state has to live **on disk, not in the context window.** The agent forgets; the repo doesn't.

---

## What one loop looks like

> An automation runs every morning against the repo. Its prompt calls a triage skill that reads yesterday's CI failures, the open issues, and recent commits, and writes findings into a state file or Linear board. For each finding worth doing, the thread opens an isolated worktree and sends a sub-agent to draft the fix while a second sub-agent reviews that draft against the project's skills and existing tests. Connectors let the loop open the PR and update the ticket; anything it can't handle lands in the triage inbox for you. The state file is the spine — it remembers what was tried, what passed, what's still open, so tomorrow's run picks up where today's stopped.

You designed that once. You didn't prompt any individual step. Same loop in Claude Code or Codex, because the pieces are the same pieces.
