# AI Tooling Fluency by Level

The specific AI-tooling expectations at each level. Per Ch 42 §42.1, AI tooling fluency is one of the five high-value engineer properties; this file makes it explicit at each level so calibration committees can apply it consistently.

The dimension is: how does the engineer use, shape, and reason about AI tooling at this level?

The progression goes from **uses fluently** (L3) → **contributes to harness** (L4) → **owns major surfaces** (L5) → **shapes the company's stack** (L6) → **shapes the industry conversation** (L7).

## Why this dimension needs to be explicit

Some legacy engineering ladders don't have AI tooling fluency anywhere. Engineers who go deep on AI tooling — building skills, hooks, subagents — get evaluated on the work they're NOT doing (lines of feature code) rather than the work they ARE doing (org-multiplying harness investment).

Calibration committees without explicit AI-tooling criteria default to "lines of code shipped" as the proxy for impact. Engineers who built a skill that 100 other engineers use weekly can be rated below engineers who shipped a moderate feature. That's the ladder failing the engineer.

This dimension forces the question: at this level, what's the AI tooling expectation, and is the engineer meeting it?

---

## L3 — Engineer (mid-level)

### Expected fluency

- **Uses skills fluently.** Knows when to invoke which skill. Reports skill bugs back with concrete repros.
- **Runs productive Claude Code or Cursor sessions** on real work. Sessions produce shipped code; the engineer can articulate what worked and what didn't.
- **Recognizes when the agent is wrong.** Doesn't accept agent output uncritically. Pushes back, redirects, or escapes when needed.
- **Configures their environment.** CLAUDE.md / AGENTS.md at the repo level is something they can read and modify; they don't need senior help for routine config.

### NOT expected

- Building new skills from scratch
- Designing subagents
- Configuring the team's harness for them
- Shaping vendor selection

### Calibration anchors
- "Engineer asks reasonable questions in office hours; doesn't burn through token budget on confused agent loops."
- "Engineer's PR's, when AI-assisted, are clean and ship-quality. They don't need rework."

### Common gaps at this level
- Engineer has been told "use AI" but doesn't have a stable workflow
- Engineer is using a personal-account version of a tool the team has procured (a security/governance issue, not a fluency one)
- Engineer's agent sessions produce code that other engineers have to clean up

### How to develop fluency at this level
- Pair-driving with an L4 or L5 in the team's primary AI tool (per `junior-trajectory/pair-driving-guide.md`)
- Reading the team's existing skills before each session
- Cost dashboard visibility on their own usage; coaching on cost-aware tool selection

---

## L4 — Senior Engineer

### Expected fluency

- **Contributes to the harness.** Has shipped at least one skill, hook, or substantial CLAUDE.md addition used by other engineers.
- **Pairs effectively in pair-driving sessions** as the senior engineer.
- **Reasons about model selection.** Knows when to use Sonnet vs. Haiku vs. Opus for the task at hand. Cost-aware.
- **Configures the harness for their team's specific patterns.** Repo-level CLAUDE.md, AGENTS.md, llms.txt — they don't depend on platform team for these.
- **Catches AI-induced bugs in code review.** Per Ch 22 §22.2, the seven slop signatures are recognizable.
- **Knows the limits.** Articulates which tasks AI does well at, which it doesn't, with specifics.

### NOT expected

- Owning major harness surfaces (skill families, hook categories)
- Shaping the team's vendor relationships
- Designing complex multi-agent workflows

### Calibration anchors
- "Engineer has shipped a skill that other engineers use; if removed, the team would feel it."
- "Engineer can articulate a recent case where they pushed back on AI output with substantive technical reasoning."
- "Engineer's PR reviews catch slop signatures other engineers miss."

### Common gaps at this level
- Engineer uses AI tooling well personally but hasn't contributed to the team's harness
- Engineer doesn't pair-drive (or refuses to)
- Engineer's contributions to CLAUDE.md / AGENTS.md are absent

### How to develop fluency at this level
- Owning a specific harness component for a quarter (the named owner)
- Leading 2-3 pair-driving sessions per quarter as the senior partner
- Reading the platform team's roadmap; commenting substantively

---

## L5 — Staff Engineer

### Expected fluency

- **Owns major harness surfaces.** A skill family, a hook category, a subagent class — the engineer is the named owner that other engineers consult.
- **Designs subagents** when needed. Understands when a subagent is the right answer vs. a hook vs. a skill.
- **Shapes the team's tooling decisions.** When the team is choosing between AI tools or vendors, the engineer's input carries weight.
- **Designs complex multi-agent workflows** for high-blast-radius work.
- **Mentors L4 and L3 engineers** on AI tooling fluency. Their mentorship is substantive; engineers who work with them get better.
- **Calibrates autonomy levels** appropriately. Knows when a task is L1 / L2 / L3 / L4 autonomy work and articulates why.
- **Recognizes harness gaps.** When something doesn't work, names the gap; opens a specific issue or makes the harness change.

### NOT expected

- Shaping the company-wide tooling stack (that's L6+)
- Leading vendor relationships at the contract level
- Industry-level voice

### Calibration anchors
- "Engineer owns a major harness surface; the surface has measurable adoption metrics."
- "Engineer's subagent designs are reused by other teams."
- "Engineer's input is sought when the team is making AI tooling decisions."

### Common gaps at this level
- Engineer is a strong contributor but hasn't taken named ownership of a major surface
- Engineer's harness work is internal-only (their team) and doesn't generalize
- Engineer's mentorship is informal; doesn't show up in others' growth

### How to develop fluency at this level
- Becoming the named owner of a major surface on the platform team's roadmap (or with the platform team's blessing if on a stream-aligned team)
- Designing and shipping at least one subagent
- Authoring a specific CLAUDE.md or AGENTS.md design pattern that the wider org adopts

---

## L6 — Senior Staff / Principal Engineer

### Expected fluency

- **Shapes the company's tooling stack.** Vendor selection, model strategy, harness investment direction — the engineer's perspective shapes leadership decisions.
- **Partners with the platform team** on strategic decisions, not just tactical ones.
- **Designs cross-team or cross-org tooling work.** Work that affects multiple teams' workflows.
- **Articulates the technical strategy** for AI tooling at the company. Writes documents that engineering leadership reads and acts on.
- **Mentors L5 engineers** on AI tooling depth. Their mentorship is shaping a generation of senior engineers.
- **Recognizes structural gaps.** Not just "this hook is missing" but "we have a structural pattern of [gap]; here's the company-level investment that fixes it."
- **Engages with the AI tooling vendors** at a strategic level. Not the procurement runbook execution (that's the platform team's role), but the strategic conversations about feature direction, escalation, and partnership.

### NOT expected

- Industry-level voice (that's L7)
- Public writing or speaking necessarily (welcome but not required)

### Calibration anchors
- "Engineer's recommendation on AI tooling strategy was the input that shaped the company's [specific decision]."
- "Engineer mentors L5s; multiple L5s are visibly stronger because of this engineer's investment."
- "Engineer's writing on AI tooling shapes the company's posture."

### Common gaps at this level
- Engineer is strong technically but doesn't engage with strategic / vendor / leadership conversations
- Engineer's work is high-quality but inward-facing; doesn't multiply other engineers
- Engineer's perspective on AI tooling is dated (e.g., based on vendor demos rather than current operational reality)

### How to develop fluency at this level
- Authoring and presenting a quarterly AI tooling strategy review
- Owning a partnership with one specific AI tooling vendor at the strategic level
- Mentoring 2-3 L5 engineers on AI tooling depth, with explicit growth metrics

---

## L7 — Distinguished Engineer / Engineering Fellow

### Expected fluency

- **Industry-recognized voice on AI tooling.** Public writing, speaking, OSS contribution, conference engagement — at least one substantive form.
- **Shapes the broader conversation.** Not just within the company; within the industry. Engineers at other companies cite this engineer's work.
- **Strategic vendor relationships.** When the company is in a strategic conversation with a major AI tool vendor (e.g., model partnership, custom feature work), this engineer is in the room with executives.
- **Multi-year strategic foresight.** Knows where AI tooling is going; calibrates the company's investment posture against what will matter in 2-5 years.
- **Genuine multiplication.** L7s in this space have specific multipliers — engineers, teams, or companies that operate measurably better because of this engineer's influence.

### What it looks like

- Original research or insight that shapes how the field thinks about AI tooling
- A book, a substantial body of public writing, or a comparable contribution
- Industry roles (advisor, board, conference chair) related to AI engineering
- Mentorship of senior engineers (L5 and L6) at scale

### Common reality check

L7 is rare. Most companies don't have one. If your company doesn't have an L7 in AI tooling fluency yet, that's not a gap; it's a statistical norm. Don't promote into L7 to fill a slot; promote because the engineer has demonstrated the bar.

### How to develop toward L7

L7 development is not a one-quarter-at-a-time journey. It's the result of years of sustained L6 work that's gradually become external-facing. The path:

- Start writing publicly about the work
- Engage with the industry at conferences, podcasts, OSS
- Mentor outside the company
- Build a body of work that's recognized

Most engineers at L6 won't progress to L7. That's fine. L6 is a great place to spend a career.

---

## Cross-cutting principles

### AI tooling fluency is necessary but not sufficient for leveling

An engineer can be at L5 fluency in AI tooling but L4 in code review judgment, L3 in spec clarity, etc. The leveling is across all dimensions, not just AI tooling.

### AI tooling fluency is not optional

Per Ch 42 §42.1:

> Treat 'AI tooling fluency' as a hiring signal at every level. The company that hires great engineers who refuse to engage with AI tooling is hiring engineers who will be 30% less productive than their peers.

The same logic applies to leveling. An engineer who refuses to engage with AI tooling can't be at L4+. The dimension can't be skipped; engineers who don't develop fluency cap at L3.

### What the rubric does NOT measure

- **Velocity of token usage.** Heavy users aren't necessarily fluent.
- **Volume of skills shipped.** Quality and adoption matter more.
- **Self-reported fluency.** "I'm great with AI" without specific examples doesn't count.

### What about engineers who came in pre-AI?

Engineers with 10+ years pre-AI experience may have had 18-36 months to develop fluency. Most have. Those who haven't, in 2026, have an explicit gap to close.

The path: pair-driving with engineers who are fluent. Investment in the team's harness. Active engagement with the team's AI tooling, not delegated to others. The fluency is learnable; refusal to learn is the issue, not the starting point.

## What this dimension will NOT do

- Will not eliminate disagreements about whether an engineer "is fluent." Some judgment is irreducible.
- Will not work without consistent calibration. Two managers with different fluency standards will produce inconsistent levels.
- Will not capture every dimension of AI tooling fluency. New tools, new workflows, new failure modes will surface; the rubric needs annual updates.

## Companion artifacts

- [`level-rubric.md`](level-rubric.md) — the broader leveling
- [`promotion-conversation-script.md`](promotion-conversation-script.md) — how to communicate
- [`calibration-committee-structure.md`](calibration-committee-structure.md) — how to apply consistently
- `junior-trajectory/pair-driving-guide.md` — adjacent
- `platform-team-charter/platform-engineer-jd.md` — platform-specific level criteria
- Ch 42 §42.1 — source
