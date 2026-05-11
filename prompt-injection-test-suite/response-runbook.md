# Response Runbook — When Prompt Injection Is Detected

What to do when prompt injection is detected — either in the test suite (a test failure) OR in production (a real incident).

The two cases differ in urgency but share most of the response.

## Case A — Prompt injection detected in the test suite

Per Ch 37: "Treat any pass-to-fail regression as a P1 incident."

### Immediate (within 30 minutes)

1. **Confirm the failure.** Re-run the failed test to confirm it's not a flake.
2. **Pause new agent capability rollouts.** Anything in progress that would expand agent permissions is paused until the failure is addressed.
3. **Notify the security team.** Specifically, the platform team lead and security lead.

### Short-term (within 24 hours)

4. **Identify the root cause.** Why did the test fail now? What changed?
5. **Determine if production is exposed.** A test failure in the sandbox doesn't always mean production is vulnerable, but assume it does until proven otherwise.
6. **Assess existing exposure.** If the vulnerability has been live for any period, what's the potential exposure?

### Medium-term (within 1 week)

7. **Implement the fix.** Per the test case's "Common failure modes and remediation" section.
8. **Verify the fix.** Re-run the test; confirm it passes.
9. **Run the full suite.** Confirm no other tests have regressed alongside this one.
10. **Document the incident.** Postmortem per `incident-postmortem-templates/`. The "harness deficiency" section is the durable artifact.

### Long-term (within 30 days)

11. **Extend the suite.** If the failure mode wasn't covered by an existing test in detail, add a more specific test.
12. **Update the autonomy ladder.** If the failure suggests current operations are at too high an autonomy level, lower per `agent-autonomy-levels/raising-and-lowering-autonomy.md`.
13. **Review the certification gates.** If engineers were certified at levels they couldn't safely operate at given the harness gap, address.

## Case B — Prompt injection detected in production

Higher urgency. The defense layers failed; an attacker may have succeeded.

### Phase 1 — Stop the bleeding (within 60 minutes)

1. **Disable the affected agent capability immediately.** Whatever path was exploited — disable.
2. **Rotate any credentials that may have been exposed.** Per the exposure assessment, anything the agent could have read with the compromised tool surface gets rotated.
3. **Notify security team.** This is a security incident, not just a test failure.
4. **Notify legal / compliance team if customer data may be exposed.** Per `customer-facing-ai-disclosure/status-page-language.md`, customer notification SLAs may apply.

### Phase 2 — Assess the impact (within 4 hours)

5. **Determine the scope of exposure.** What did the agent read? What did it write? What did it post?
6. **Determine the duration.** How long has the vulnerability been live?
7. **Identify affected customers.** If customer data was exposed, who?
8. **Review audit logs.** Specifically:
   - Agent transcripts during the incident window
   - Output channels (PR comments, chat, files modified)
   - Network egress logs
   - File access logs

### Phase 3 — Communicate (within 8 hours)

9. **Prepare customer communication if needed.** Per `customer-facing-ai-disclosure/`.
10. **Status page entry if production was affected.**
11. **Internal communication.** Engineering leadership; affected teams; on-call.

### Phase 4 — Investigate root cause (within 48 hours)

12. **How did the injection succeed?**
    - Which defensive layer failed?
    - What other layers should have caught it?
    - Why didn't the test suite catch this?

13. **Reconstruct the timeline.**
    - When was the change that introduced the vulnerability?
    - When was the first known exploitation attempt?
    - When did the team detect?

### Phase 5 — Remediate and prevent (within 1 week)

14. **Implement specific harness improvements** that close the gap.
15. **Extend the test suite** with a specific test case for this attack pattern.
16. **Update CLAUDE.md / AGENTS.md** with relevant guardrails.
17. **Review the autonomy ladder** — should we operate at a lower level until the discipline is restored?

### Phase 6 — Postmortem (within 2 weeks)

18. **Complete the postmortem** per `incident-postmortem-templates/`.
19. **Specific harness deficiency** documented per `incident-postmortem-templates/harness-deficiency-checklist.md`.
20. **30-day follow-up** scheduled.

## Common patterns of vulnerability

### Pattern 1 — Token scope too broad

The agent had a token that gave access to more than the specific task required. Cross-repo exfil (test case 5) succeeds.

Fix: per-task tokens; token scoping reviewed quarterly.

### Pattern 2 — Output filtering missing or too narrow

Credentials appear in output (test case 6) because the filter doesn't catch the specific format.

Fix: comprehensive credential pattern list; subagent review of security-sensitive output; output filtering applies to all channels including logs.

### Pattern 3 — System prompt doesn't treat fetched content as data

Tests 1, 3, 4 — the agent treats issue bodies, web pages, or logs as instructions.

Fix: explicit system prompt treatment; HTML/log sanitization; content classification before passing to the agent.

### Pattern 4 — Bash firewall missing or has gaps

Test 2 succeeds because curl-and-pipe wasn't blocked.

Fix: comprehensive bash firewall; specific patterns enumerated (per `governance/hooks/`); allow-list approach for safe commands.

### Pattern 5 — Network egress not controlled

Tests 1, 2, 3 — even when the agent attempts something it shouldn't, network egress should block external requests.

Fix: network egress allow-list at the host or container level; specifically restrict outbound HTTP to known-safe domains.

## What NOT to do

### Don't blame engineers

Per `incident-postmortem-templates/`, the postmortem is harness-focused, not engineer-focused. Engineers using the agent didn't introduce the vulnerability; the harness has a gap.

### Don't hide the incident

A prompt injection incident is a security incident. Customers and regulators may need to know. Hiding it is worse than disclosing.

### Don't roll back without addressing the gap

Reverting the change that introduced the vulnerability is necessary but not sufficient. The gap that the change exposed needs to be closed.

### Don't run the suite once and call it fixed

Verify with the suite; verify in production with monitoring; verify across the next quarter that the regression doesn't return.

### Don't assume a single fix is comprehensive

Most prompt injection vulnerabilities have multiple contributing factors. Address them all, not just the most visible one.

## What this runbook will NOT do

- Will not eliminate prompt injection. The threat is real and ongoing; the discipline is to catch and remediate.
- Will not work without the test suite. The runbook is for what to do when the tests fail; it requires the tests.
- Will not work without leadership backing. P1 designation has cost (paused rollouts, engineering time); without backing, the discipline erodes.

## Companion artifacts

- [`README.md`](README.md) — suite overview
- [`ci-integration.md`](ci-integration.md) — automation and cadence
- [`extending-the-suite.md`](extending-the-suite.md) — new test cases
- `incident-postmortem-templates/` — postmortem framework
- `agent-autonomy-levels/raising-and-lowering-autonomy.md` — autonomy response
- `customer-facing-ai-disclosure/status-page-language.md` — customer communication
- Ch 36, Ch 37 — sources
