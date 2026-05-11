# Level Rubric — L3 through L7 IC Track

The full IC ladder. Each level has expectations across:

- **Scope** — what the engineer owns end-to-end
- **Direction discipline** (Ch 5 §5.2) — vivid spec writing, "what good feels like"
- **Architecture discipline** (Ch 5 §5.2) — encoding constraints into hooks, lints, contracts
- **Evaluation discipline** (Ch 5 §5.2) — feedback loops, mutation testing, slop detection
- **Code review judgment** (Ch 42 §42.1)
- **Harness contribution** (Ch 42 §42.4)
- **AI tooling fluency** (separate file: [`ai-tooling-fluency-by-level.md`](ai-tooling-fluency-by-level.md))
- **Communication and influence**

Per Ch 5 §5.2, engineers at L4+ are expected to have **depth in one** of the three bottleneck disciplines (Direction / Architecture / Evaluation) and **credible competence in the other two**. Below L4, the discipline awareness is forming; at L4 a discipline preference emerges; at L5+ the depth is real and visible.

---

## L3 — Engineer (mid-level)

The end of the apprenticeship. Reliably productive in scoped work; no longer needs senior shepherding.

### Scope

- Owns T1 features (per the tier framework) end-to-end: spec, implementation, tests, deployment, postmortem if needed
- Contributes meaningfully to T2 features with senior collaboration
- Doesn't yet own architectural decisions

### Direction
- Writes agent-ready specs from scratch in <30 minutes for T2 work
- Specs rarely require pre-implementation revision
- Recognizes when a spec is unclear and asks rather than guesses

### Architecture
- Reads existing architecture documents and ADRs; understands constraints
- Doesn't yet propose new constraints

### Evaluation
- Writes tests that actually test (not slop signature S1)
- Owns at least one minor incident's postmortem with structured root-cause analysis
- Recognizes the seven slop signatures in their own work

### Code review judgment
- Identifies obvious slop signatures (S1, S5, S7) in PRs
- Pushes back constructively on AI-authored work
- Does not rubber-stamp; reviews carry weight on T1 work

### Harness contribution
- Uses the team's harness fluently
- Has contributed at least one small improvement (a fix to a hook, a clarification in CLAUDE.md, a SKILL.md draft)

### Communication
- Writes clear PR descriptions
- Participates productively in design conversations led by seniors
- 1:1s with manager are useful for both

### Promotion to L4 requires
- Reliably writes specs that don't need revision
- Reviews stop being double-checked by seniors on T1 work
- Has owned end-to-end at least one substantive piece of work without senior intervention beyond standard review
- A first solo harness contribution (skill, hook, subagent, or substantial CLAUDE.md addition) used by other engineers

---

## L4 — Senior Engineer

The threshold of "this engineer can be trusted with substantial work." A discipline preference (Direction / Architecture / Evaluation) emerges.

### Scope

- Owns T2 features end-to-end without senior intervention
- Contributes to T3 (complex, high-blast-radius) work with senior partnership
- Begins to own a service or substantial module
- Owns the on-call rotation alongside other senior engineers

### Direction depth (if their depth)
- Writes specs that other engineers (and agents) can ship from
- Translates ambiguous product requirements into agent-ready issues
- Says "the spec is unclear" when it is, and helps clarify

### Direction competence (if not their depth)
- Recognizes when Direction work is inadequate
- Doesn't barrel through with implementation when the spec is wrong

### Architecture depth (if their depth)
- Has shipped at least one constraint system: a hook, a CODEOWNERS pattern, a schema discipline that prevents whole classes of error
- Recognizes where to encode constraints mechanically vs. document them
- Reviews architectural changes with credibility

### Architecture competence (if not their depth)
- Reads and understands the team's architectural docs
- Doesn't routinely propose changes that violate constraints

### Evaluation depth (if their depth)
- Has built at least one feedback loop that the team relies on (mutation testing, telemetry, dashboard, postmortem template)
- Triages incidents (Bug / Quality issue / Feature request)
- Designs for observability rather than retrofits it

### Evaluation competence (if not their depth)
- Recognizes when verification is inadequate
- Doesn't accept "tests pass" as sufficient for high-blast-radius work

### Code review judgment
- Reliably finds non-obvious slop signatures (S2, S3, S4, S6) in PRs
- Calibrates diff size and pushes back on scope creep
- Reviews carry weight on T2 work; senior peers route hard PRs to them

### Harness contribution
- Has shipped at least one harness component (skill, hook, subagent) used by multiple engineers
- Maintains the component (responds to bugs, iterates)

### Communication
- Writes design docs (ADRs, technical proposals)
- Mentors L3 engineers
- Influence within the team is real

### Promotion to L5 requires
- Has shipped multiple T2 features and at least one T3 feature with substantial ownership
- Has either led a substantial design or owned a significant harness component
- Mentors actively (newer L3s on the team go to them)
- Calibration committee can name 2-3 specific impactful contributions

---

## L5 — Staff Engineer

The level where the engineer's work meaningfully shapes the team or domain. Real depth in a discipline; substantial scope.

### Scope

- Owns a domain or substantial system end-to-end
- Routinely runs T3 work with peer partnership (not senior partnership)
- Cross-team work: regularly engages with adjacent teams
- May own a small platform-team-equivalent surface (skill family, hook category, subagent class)

### Direction depth (if their depth)
- Writes specs that the entire team (and other teams) ship from
- Translates business requirements into engineering work routinely
- Holds the line on scope when others are pushing for expansion
- The team trusts their judgment on "is this the right thing to build"

### Architecture depth (if their depth)
- Has shipped multiple constraint systems
- Designs new services / systems with appropriate guard rails
- Reviews architectural decisions across the team; senior peers consult them
- Identifies when AI tooling is weak (data complexity, infra interactions, novel cross-system reasoning) and protects those areas with explicit constraint

### Evaluation depth (if their depth)
- Has built the team's observability or quality discipline
- Drives incident response; postmortems they lead produce durable harness changes
- Designs the team's metrics (per Ch 31 §31.1's six)

### Code review judgment
- Reviews carry weight across the team. L4s consult them on hard cases.
- Spots subtle slop signatures (S6 unnecessary abstractions, complex multi-file pattern divergence)
- Calibrates "should this PR exist at all" routinely

### Harness contribution
- Has shipped harness components used across multiple teams
- Often mentors others on harness contribution
- May be the named owner of a major harness surface

### Communication and influence
- Writes documents that shape direction (architecture proposals, technical strategy memos)
- Mentors L3 and L4 engineers; the mentorship is substantive
- Cross-team influence: trusted by adjacent teams for technical input
- Shapes the team's culture around code review, testing, AI tooling discipline

### Promotion to L6 requires
- Sustained pattern of high-leverage work over multiple quarters
- Has shaped or led at least one cross-team initiative
- Mentors visible (engineers grow under their mentorship)
- The team's outcomes are visibly different because of their work
- Calibration committee can name multiple specific high-impact contributions across at least two quarters

---

## L6 — Senior Staff / Principal Engineer

Senior IC. The engineer's work shapes the engineering organization, not just a team.

### Scope

- Owns a major surface of the engineering org's work — a platform, a domain, a long-running initiative
- Cross-org work is routine; trusted by engineering leadership for technical input
- Sets technical direction for multiple teams
- Often the named author of major ADRs or technical strategies

### Direction (depth required at this level if it's their preference; competence at minimum if it isn't)
- Drives company-level Direction discussions for technical work
- Translates company strategy into engineering investment
- Their judgment on "what's worth building" carries across the org

### Architecture (depth at minimum if it's their preference; substantial competence if not)
- Has shaped the org's architectural posture (service boundaries, data ownership, integration patterns)
- Designs systems that other teams adopt as patterns
- Their judgment on "should we build this way" carries across the org

### Evaluation (depth at minimum if it's their preference; substantial competence if not)
- Has shaped the org's evaluation discipline (testing standards, telemetry investments, postmortem culture)
- Their judgment on "is this working" carries across the org

### Code review judgment
- Reviews are the highest-quality bar in the org
- Trusted by senior leadership for "should we ship this" calls
- Spots issues that others miss; absent, fewer issues get caught

### Harness contribution
- Has shaped the org's harness investment strategy
- Owns a major harness surface (or multiple)
- Their architectural decisions shape what other teams build

### Communication and influence
- Writes documents that engineering leadership reads
- Frequently presents technical strategy to engineering leadership and sometimes to executive leadership
- Mentors L4 and L5 engineers; mentorship is a major part of their job
- Shapes the engineering culture; specific values they champion are evident in the org

### Promotion to L7 requires (if your org has L7)
- Sustained company-level impact over years
- Multiple substantial initiatives with org-shaping outcomes
- Industry-recognized expertise (publications, talks, contributions to the field)
- Genuine multiplication of other engineers' impact

---

## L7 — Distinguished Engineer / Engineering Fellow

The rare case. Many engineering orgs do not have an L7. For those that do:

### Scope

- Industry-recognized expertise in some dimension
- Shapes the engineering org's strategic posture
- Cross-company influence (advisor, board, public speaker, OSS contributor with reach)
- Often plays a strategic role in the company beyond pure engineering

### What an L7 looks like in practice

- Has spent years operating at L6 with sustained company-shaping impact
- Has produced work (technical, written, spoken) that's recognized beyond the company
- Often has explicit engagement with the industry — board roles, advising, conference talks, public writing
- Mentors at the L5 and L6 level; their mentees are senior engineers across the org

### What an L7 is NOT

- Not "L6 with more time in seat." Time alone doesn't produce L7; sustained external-facing impact does.
- Not "the most senior engineer on the team" by default. L7 requires industry recognition, not just internal seniority.
- Not a path everyone should pursue. Many engineers cap at L5 or L6, and that's fine. L7 is a specific kind of role with specific demands.

### How L7 differs from senior management

L7 is an IC role. The engineer is not a manager; their leverage comes from their technical and intellectual contributions, not from people management.

If the engineer wants people management, that's a different track (CTO / VP of Engineering / Director track).

---

## Level transitions

### What "ready for promotion" looks like

An engineer is ready for promotion when:

1. They've been operating at the next level's bar for at least 2 quarters consistently
2. The promotion would recognize work already done, not future potential
3. The calibration committee can name specific high-impact contributions
4. The engineer's manager believes they'd hire them at the next level if hiring externally

### What "not ready" looks like

Some patterns that indicate an engineer isn't ready, even if they think they are:

- Self-described impact doesn't match what the team would say
- Strong on one dimension (e.g., AI tooling fluency) but weak on another (e.g., communication)
- Recent shift in scope that hasn't had time to demonstrate consistent operation at the next level
- The "halo" effect — works closely with a senior engineer who carries them, would not perform at the next level alone

### What to do when an engineer disagrees

The promotion conversation script ([`promotion-conversation-script.md`](promotion-conversation-script.md)) handles this. Briefly: explicit named gaps, specific path forward, time-bounded check-in.

---

## Level migration from legacy ladders

If your existing ladder doesn't recognize harness contribution or AI-tooling work, the migration:

1. Map your existing levels onto L3-L7 here
2. For each engineer at each level, assess against this rubric's criteria
3. Identify gaps: which engineers are at the title but not the bar (probably none move down — that's politically corrosive); which engineers are at the bar but below the title (move them up)
4. Rewrite JDs over the next quarter to reflect the new ladder
5. Apply at the next promotion cycle

The migration is iterative; don't try to remap the entire ladder in one cycle.

## What this rubric will NOT do

- Will not work without manager engagement. The criteria require subjective judgment.
- Will not work as a checklist. Engineers who hit every bullet at the next level may still not be ready; engineers who don't hit every bullet may be ready.
- Will not transfer cleanly to non-engineering ladders. SE, TPM have their own (see `solutions-engineer-and-tech-pm/career-path-and-comp.md`).
- Will not eliminate the politics of promotion. Calibration committees produce more consistent decisions but don't eliminate them.

## Companion artifacts

- [`ai-tooling-fluency-by-level.md`](ai-tooling-fluency-by-level.md) — the AI-tooling dimension across levels
- [`promotion-conversation-script.md`](promotion-conversation-script.md) — the conversation
- [`promotion-packet-template.md`](promotion-packet-template.md) — the artifact for calibration
- [`calibration-committee-structure.md`](calibration-committee-structure.md) — the committee discipline
- `junior-trajectory/calibration-rubric.md` — L3 specific
- Ch 5 §5.2, Ch 42 — sources
