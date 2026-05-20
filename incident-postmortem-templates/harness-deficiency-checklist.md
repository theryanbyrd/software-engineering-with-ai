# Harness Deficiency Checklist — Translating Postmortem Findings to Action Items

The structured "what would have caught this earlier?" work. Per Ch 39 §39.3:

> Always pair an incident with a specific harness or process change. "Be more careful" is not an action item.

This checklist walks through the seven harness mechanisms in the postmortem template's "Harness deficiency" section. Use it when filling out that section.

The mechanisms are listed in rough order of mechanical strength — top of the list is most-likely-to-bind, bottom is most-likely-to-be-ignored. When in doubt, prefer the more mechanical mechanism.

## The seven harness mechanisms

### 1. CLAUDE.md / AGENTS.md content

**What it does:** Documents an invariant, convention, or rule the agent should follow.

**Strength:** Soft. The agent has access to the document but compliance is not enforced.

**When it's the right fix:**
- The agent didn't know about a non-obvious convention (context failure)
- The team has a preference that doesn't rise to a hard constraint
- A pattern is preferred but not strictly required
- Updating documentation is faster than building enforcement and the marginal incident risk is low

**When it's the WRONG fix:**
- The agent ignored existing CLAUDE.md content (constraint failure — needs enforcement)
- The convention is critical and recurrence is unacceptable
- Documentation has already been added for similar issues without effect

**Specifics to include in the action item:**
- Exact wording to add (write it; don't say "I'll write it later")
- Which file: CLAUDE.md, AGENTS.md, or a module-level README
- Where in the file: usually under a clear section header

**Example action item:**
- ❌ "Update CLAUDE.md with HTTP client guidance"
- ✅ "Add to CLAUDE.md, under 'HTTP and Networking': 'For all outbound HTTP, use `internal/httpclient` package. Do NOT import `net/http` directly. The package handles retries, circuit breaking, and structured logging.' Owner: @rbyrd, deadline: 2026-05-15"

---

### 2. A hook

**What it does:** A CI gate, pre-commit check, or pre-merge hook that mechanically enforces a rule.

**Strength:** Hard. The check fires automatically; PRs that fail are blocked.

**When it's the right fix:**
- A specific anti-pattern can be detected mechanically (regex, AST analysis, command output)
- The rule must bind even when the agent or human is in a hurry
- The team has tried documentation and the issue recurs

**When it's the WRONG fix:**
- The pattern is too subtle for mechanical detection (would produce too many false positives)
- The check would block legitimate work
- The check requires understanding intent, not just mechanics (use a subagent instead)

**Specifics to include in the action item:**
- What the hook checks (specific regex, command, condition)
- Where it runs (pre-commit, CI, pre-merge)
- What happens when it fails (warning vs. hard block)
- Bypass mechanism if any (with audit trail)

**Example action item:**
- ❌ "Add hook to prevent force pushes"
- ✅ "Add a server-side hook on the `main` and `release/*` branches that rejects all force pushes (`git push --force` and `--force-with-lease` variants). Owner: @platform-team, deadline: 2026-05-15. Link: [hook implementation in `governance/hooks/no-force-push.sh`]"

**Common hook patterns:**
- Slop-detector heuristic in CI (`scripts/slop-detector.py`)
- PR size limit (warns above N lines, blocks above M)
- Required PR labels (`ai:none` / `ai:assisted` / `ai:authored` / `ai:agent` per Ch 31 §31.6)
- Required CODEOWNERS review on sensitive paths
- Bash firewall preventing specific commands the agent might run

---

### 3. A subagent (security-reviewer, performance-reviewer, migration-reviewer)

**What it does:** A specialized agent that reviews PRs for a specific class of issue. Runs as part of the two-tier review (Ch 22 §22.3).

**Strength:** Medium. Catches subtler issues than hooks but is fallible (LLM-based).

**When it's the right fix:**
- Detection requires understanding intent, not just mechanics
- The class of issue is broad enough to justify a dedicated reviewer
- A hook would have unacceptable false-positive rates

**When it's the WRONG fix:**
- The pattern is mechanically detectable (use a hook for cost and reliability)
- The class of issue is so specific it doesn't merit a separate subagent

**Specifics to include in the action item:**
- The subagent's scope (what it reviews, what it doesn't)
- The model tier (Haiku for cheap broad checks; Sonnet for substantive review)
- The integration point (CI step, GitHub action, manual invocation)
- The output format

**Example action item:**
- ❌ "Add a security reviewer"
- ✅ "Build `skills/security-reviewer/SKILL.md` and `governance/subagents/security-reviewer.yaml`. Reviews any PR touching files matching `**/auth/**`, `**/security/**`, `**/*auth*.{py,ts,go}`. Outputs a structured finding list with severity. Runs on Sonnet. Failures of severity HIGH block merge. Owner: @rbyrd, deadline: 2026-05-30"

---

### 4. A skill

**What it does:** A canonical pattern documented in a SKILL.md file that the agent can invoke. Standardizes how a recurring task is done.

**Strength:** Medium. Drives consistent behavior when the agent uses the skill; doesn't bind if the agent doesn't.

**When it's the right fix:**
- A recurring task has a "right way" the team wants done consistently
- The current freedom is producing inconsistent results
- Onboarding new engineers (or new agents) to the convention is high cost

**When it's the WRONG fix:**
- The task is one-off; doesn't recur enough to justify a skill
- The convention is more of a hard rule than a pattern (use AGENTS.md + a hook)

**Specifics to include in the action item:**
- Skill name and location
- Skill scope (when to invoke; when not to)
- Skill content (the canonical pattern)

**Example action item:**
- ❌ "Add a skill for migrations"
- ✅ "Add `skills/db-migration/SKILL.md` covering: forward+backward migration discipline, index addition pattern, the `--reversible` flag check. Use when adding any database migration. Owner: @rbyrd, deadline: 2026-05-22. Reference: `skills/legacy-bridge/characterize-then-refactor/SKILL.md` for shape."

---

### 5. An MCP permission boundary

**What it does:** Restricts the agent's access to certain tools, files, or systems via MCP server configuration.

**Strength:** Hard. The agent literally cannot perform the action.

**When it's the right fix:**
- The agent shouldn't have access to a particular system (database write access, production deploy, secrets)
- The permission was overly broad and an incident exploited the broadness
- A subagent or skill could route around documentation; the boundary is the durable fix

**When it's the WRONG fix:**
- The work legitimately requires the access; restricting it breaks the workflow
- The boundary is too coarse (would block more than it should)

**Specifics to include in the action item:**
- Which tools / paths / systems are restricted
- Which agent contexts the restriction applies to
- The audit log requirement (who can override and how it's logged)

**Example action item:**
- ❌ "Restrict the agent's access to production"
- ✅ "Update MCP server configuration: agent has read-only access to production database; write access requires human approval via `production-write` ticket. Add audit log entry for every write attempt. Owner: @platform-team, deadline: 2026-05-30"

---

### 6. An ADR

**What it does:** An architectural decision record that the agent (and humans) can reference when making related decisions.

**Strength:** Soft, but durable. ADRs are the team's institutional memory.

**When it's the right fix:**
- The bug arose from making a decision the team had already considered and rejected
- A pattern is the team's chosen approach but the reasoning isn't captured anywhere
- Future engineers (or agents) need the rationale, not just the rule

**When it's the WRONG fix:**
- The issue is mechanical (use a hook)
- The ADR would be a one-paragraph after-the-fact rationalization

**Specifics to include in the action item:**
- ADR number and title
- The decision documented
- The alternatives considered and why they were rejected
- Where the ADR lives (`docs/adr/` typically)

**Example action item:**
- ❌ "Write an ADR about HTTP clients"
- ✅ "Add ADR-014: 'HTTP clients standardized on `internal/httpclient`'. Includes: decision (use the internal package), context (multiple incidents from inconsistent retry behavior), alternatives (raw `net/http`, `resty`, `go-resty`), consequences (one consistent pattern; new engineers must learn it). Owner: @rbyrd, deadline: 2026-05-22"

---

### 7. An autonomy level downgrade

**What it does:** Reduces the level of autonomy the agent has for a class of work. From "agent works independently" to "agent proposes, human approves" to "human leads, agent assists."

**Strength:** Hard. Forces human review at the level appropriate to the risk.

**When it's the right fix:**
- The work has high blast radius and the agent isn't reliable enough at the current autonomy level
- A specific task type recurs as a problem despite other harness investment
- The org is in a learning phase and wants more human oversight before relaxing

**When it's the WRONG fix:**
- The autonomy level is correct and the issue is in another mechanism
- The downgrade would slow important work without clear benefit

**Specifics to include in the action item:**
- Which task category the downgrade applies to
- The new autonomy level (specific behavior expected)
- How long the downgrade lasts (often 90 days, with re-evaluation)
- What triggers re-elevation

**Example action item:**
- ❌ "Reduce agent autonomy on database changes"
- ✅ "Database schema changes downgraded from 'agent autonomous' to 'agent proposes, senior engineer approves' for 90 days starting 2026-05-15. After 90 days, review: zero schema-change incidents in the period → restore autonomy. One or more incidents → extend 90 days and address upstream. Owner: @rbyrd"

---

## Picking the right mechanism

The general principle: the most mechanical mechanism that solves the problem.

Decision flow:

1. **Can a hook detect this?** If yes, prefer hook over docs.
2. **Does the agent need access at all?** If no, prefer MCP permission boundary over docs.
3. **Is detection too subtle for a hook?** Use a subagent.
4. **Is the issue about the agent's pattern of work, not a single check?** Use a skill.
5. **Is the issue about the team's chosen approach with reasoning?** Use an ADR.
6. **Is the work too high-stakes for current autonomy?** Use an autonomy level downgrade.
7. **Does the agent just need information?** Use CLAUDE.md / AGENTS.md.

When two mechanisms could each solve the problem, prefer the more mechanical one. Documentation drift is real; hooks don't drift.

## Combining mechanisms

Many incidents call for multiple mechanisms working together. Common combinations:

- **Hook + AGENTS.md content:** the hook enforces; the AGENTS.md content explains why so engineers don't just bypass.
- **Subagent + skill:** the skill defines the pattern; the subagent verifies adherence.
- **MCP boundary + ADR:** the boundary restricts access; the ADR documents why so future engineers don't loosen it without consideration.
- **Autonomy downgrade + skill:** the downgrade forces review; the skill teaches the pattern so future autonomous work goes well.

In the postmortem, mark one mechanism as **[P]rimary** (the one most likely to prevent recurrence) and the others as **[S]econdary** (supportive but not the load-bearing fix).

## What NOT to put in the harness deficiency section

- **"Be more careful."** Not an action item.
- **"Engineers should review more carefully."** Not specific enough.
- **"Train the team on this issue."** Possible, but a training session is a one-time event; harness mechanisms are durable.
- **"We need a culture of more discipline."** True or not, it's not actionable from a postmortem.
- **"Update the documentation."** Which documentation? Documenting which behavior? Be specific.

The action items section in the postmortem should always reduce to specific, named, dated commitments to specific harness changes. If you find yourself writing vague items, push back on yourself and ask: "What would a future engineer specifically do based on this?"

## Companion artifacts

- [`postmortem-template.md`](postmortem-template.md) — the template that uses this checklist
- [`SLOP_SIGNATURE_REFERENCE.md`](SLOP_SIGNATURE_REFERENCE.md) — what to fix
- [`failure-categorization-guide.md`](failure-categorization-guide.md) — why you're fixing it
- `prompt-injection-test-suite/` — adjacent harness discipline
- `skills/` — the skill library this checklist references
- Ch 39 §39.3 — the source
