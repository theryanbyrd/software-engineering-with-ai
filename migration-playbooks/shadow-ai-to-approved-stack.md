# Shadow AI → Approved Stack Playbook

Per Ch 53 §53.6: forty percent of mid-size companies discover personal-account ChatGPT subscriptions used on company code; smaller fractions discover personal-account Claude.ai subscriptions; smaller still discover Replit, Cody, or v0 used in ways that touch production code. This playbook covers the cleanup.

**The book's editorial stance — and the only one that works:**

> Every tool used on company code goes on the approved tooling matrix or stops being used. There is no third option. The engineers who self-disclose their shadow tools should be praised, not punished; the goal is governance, not enforcement theater.
>
> — Ch 53 §53.6

This playbook covers the discovery → governance transition. The migration here is not tool-to-tool; it's unmanaged-to-managed.

## Who this playbook is for

- VP of Engineering or Engineering Director responsible for the data classification policy
- Security / compliance lead
- Platform team lead
- Department heads whose teams are using shadow AI

## Read first

- Ch 41 §41.x (data classification and AI tooling)
- Ch 53 §53.6
- `executive-strategic-kit/data-classification-matrix.xlsx` — the framework you're enforcing
- `executive-strategic-kit/approved-tooling-matrix-template.xlsx` — what gets added to (or rejected from)

## When this playbook applies

- You suspect or know engineers are using personal AI accounts on company code
- A security review surfaced unauthorized AI tool usage
- A customer security questionnaire is forcing the conversation
- You're rolling out a formal AI tooling governance policy and need to clean up before it lands

## When this playbook does NOT apply

- You're aware of unauthorized usage but don't yet have the appetite to enforce. Address the appetite first. A cleanup that gets reversed mid-stream is worse than no cleanup.
- The unauthorized usage is one engineer using ChatGPT on a personal side project that's adjacent to work. Talk to the engineer; don't run a playbook.

## Phase 0 — Preconditions (Week -4 to 0)

1. **The data classification matrix is current.** What kinds of data exist; which AI tools each class is approved for. Without this, you cannot have the conversation, only enforce arbitrary rules.
2. **The approved tooling matrix is current.** Which tools have been procured, security-reviewed, and approved for which data classes.
3. **Leadership is aligned.** The cleanup will be uncomfortable. Both engineering and legal/compliance leadership have signed off on the approach.
4. **The amnesty framing is decided.** Engineers who self-disclose are praised, not punished. This is non-negotiable; without amnesty, engineers won't disclose and the cleanup fails. See Ch 53 §53.6.

## Phase 1 — Discovery (Weeks 1-4)

The goal is to surface what's being used without enforcement theater.

### Week 1 — All-hands message

See [`team-conversation-scripts.md`](team-conversation-scripts.md) §5 for verbatim. Key elements:

- *"We are formalizing AI tooling governance. We need to know what's being used so we can approve, replace, or restrict appropriately. If you've been using AI tools we haven't formally approved, please tell us — there is no penalty for self-disclosure."*
- *"What we are cleaning up: unauthorized usage on company code. What we are NOT cleaning up: personal-time usage on personal projects."*
- *"The deadline for self-disclosure is [date in 4 weeks]. After that date, discovered unauthorized usage moves into normal disciplinary channels."*

The amnesty is critical. Without it, engineers will not disclose, and you'll discover the usage through audit trails or customer complaints — much worse paths.

### Weeks 2-4 — Self-disclosure intake

Engineers fill out a simple form:
- Tool name
- Account type (personal, company-procured, free tier)
- What kind of work was being done with it (rough categories)
- Approximate frequency

The intake is reviewed by the platform team and the security lead. **No grading of individual engineers happens at this stage.** Aggregate data only.

Common findings:
- Personal-account ChatGPT (most common — appears in 30-50% of mid-size companies' first audit)
- Personal-account Claude.ai (10-20%)
- Free-tier Replit Agents, Cody, Cursor, v0, Perplexity Pro on company laptops (variable)
- Personal Copilot subscription used on company laptops (less common but real)

### Week 4 — Discovery report

The platform team produces a report (anonymized, aggregate):
- N tools discovered
- N engineers using each tool
- Rough work categories these tools touched
- Estimated risk by data class

This report goes to the VP of Engineering, the security lead, and whoever owns the data classification policy. It's the input to the Phase 2 decisions.

## Phase 2 — Categorization (Weeks 5-8)

For each discovered tool, the decision tree:

### Path A — Approve and procure (tool earns its keep, governance achievable)

The tool is broadly useful, the security review can be passed, the company can procure proper Enterprise tier.

Action:
- Procure Enterprise / Business tier with appropriate data handling terms
- Add to the approved tooling matrix
- Migrate engineers from personal accounts to company accounts
- Cancel personal subscriptions (engineers are reimbursed for any unexpired prepaid time)

Timeline: 4-8 weeks from approval to migration complete

### Path B — Approve for restricted use

The tool is useful but only for some data classes. Engineers can use it but only for approved scopes.

Action:
- Document the approved scope in the data classification matrix
- Communicate to engineers: *"You may use [tool] on [data class A and B], but not on [data class C]"*
- Add monitoring or hooks to enforce where possible

### Path C — Replace with an existing approved tool

The tool's use case is covered by something already approved. Engineers should switch.

Action:
- Identify the equivalent approved tool
- Provide migration support (training, harness components for the approved tool)
- Set a timeline for cutover (typically 4-8 weeks)
- Cancel personal subscriptions

### Path D — Block

The tool's use case is not appropriate for any company work, regardless of data class.

Action:
- Communicate the block clearly: *"[Tool] is not approved for company work. If you need similar capabilities, use [approved alternative]."*
- Block via DLP / endpoint controls where possible
- Address with affected engineers individually if the use case is significant

## Phase 3 — Migration (Weeks 9-16)

For each Path B/C/D tool, run the migration. The principles from `cursor-to-claude-code.md` and `copilot-to-mixed-stack.md` apply, scaled down (typically 4-8 weeks rather than 6-9 months because the scope is narrower).

Key disciplines:
- Reimburse engineers for unexpired prepaid time on personal subscriptions; this signals the cleanup is not punitive
- Provide harness investment for the approved tools so the migration doesn't degrade productivity
- Run benchmarks before and after to verify the approved tool covers the use case

## Phase 4 — Steady state (Month 5+)

The cleanup is complete. The ongoing discipline:

### Quarterly check-ins

In each quarterly engineering survey, include the question: *"Are you using any AI tools on company work that aren't on the approved tooling matrix?"* Anonymous response. The number should trend toward zero; the first quarter post-cleanup might show 5-10% (people who used something during the cleanup window and didn't think to disclose).

### Onboarding update

New hires get the approved tooling matrix during onboarding. The conversation is *"Here's what we use; here's what's restricted; here's why."* Not punitive, not surveillance-style — just clear.

### Hiring impact

Some candidates will have used tools your company doesn't approve. Don't penalize. Address during onboarding: *"At this company, [tool] isn't approved for company work; here's what we use instead."*

## What to do if it goes wrong

### Self-disclosure rate is below 20%

Either the message didn't land, or the team doesn't trust the amnesty. Survey anonymously to find out. The fix is rarely "enforce harder"; usually it's clearer communication and visible follow-through on amnesty.

### A senior engineer pushes back on losing their preferred tool

Listen first. The senior engineer who built a workflow on a now-restricted tool has invested real time. The retention play applies: comp parity, public credit, transition support. If the retention conversation is needed, run it; see `people/career-ladder/`.

### Customer security questionnaire arrives mid-cleanup

The honest answer is the right answer: *"We've discovered shadow AI usage and are in the middle of cleanup; expected completion [date]. Here's our remediation plan."* Customers respect this answer; they punish dishonesty.

### A regulator or auditor surfaces the issue before you do

Different scenario; this playbook becomes secondary. The primary work is the regulatory response with legal counsel.

## Common failure modes

- **Punishing the self-discloser.** Catastrophic. The engineer who disclosed becomes a cautionary tale; nobody else will disclose; the cleanup fails. The amnesty is non-negotiable.
- **Making the approved tool list too small.** Engineers will find unapproved tools because their work demands capabilities the approved list doesn't cover. Approve liberally.
- **Treating this as a security incident.** It often isn't (depending on what was used and on what data). Treating routine shadow AI as an incident burns trust.
- **No follow-up.** A cleanup followed by no governance discipline produces the same problem in 12 months.

## Companion artifacts

- `executive-strategic-kit/data-classification-matrix.xlsx`
- `executive-strategic-kit/approved-tooling-matrix-template.xlsx`
- `executive-strategic-kit/security-questionnaire-answers.md`
- [`team-conversation-scripts.md`](team-conversation-scripts.md) §5
- `prompt-injection-test-suite/` — verify any newly approved tool's harness
