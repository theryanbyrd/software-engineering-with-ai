# Approved AI Tooling Matrix

Companion to *Software Engineering with AI* by Ryan Byrd · Ch 30

**Owner:** VP Engineering · **Co-signed:** CISO · **Reviewed:** quarterly · **Last reviewed:** _[DATE — UPDATE]_

This is the canonical, agent-readable list of approved tools, their permitted uses, and what they are explicitly restricted from. Replaces the legacy `approved-tooling-matrix-template.xlsx`. Engineers and agents both read from this same file; the spreadsheet was a barrier to that.

## Approved tools

| Tool / Vendor | Category | Plan / Tier | Seats | Approved use | Restricted from | BAA status | Training opt-out | Renewal / Notes |
|---|---|---|---|---|---|---|---|---|
| Claude Code (Anthropic) | Agentic coding | Enterprise | [N] | All code; agentic workflows | Production credentials | Available | Contractual no-train | [Renewal date] |
| Cursor | IDE assistant | Business | [N] | Inner-loop IDE work | Customer PII paths | Available on Enterprise | Contractual no-train | [Renewal date] |
| GitHub Copilot | IDE assistant | Business | [N] | Inline completion | Customer PII paths | N/A | Org opt-out enabled | [Renewal date] |
| Claude API (direct) | API / agentic | Pay-as-you-go | — | Custom internal tools | Customer PII without BAA | Available | Contractual no-train | PAYG, monthly |
| LiteLLM gateway | Cost gateway | OSS / self-host | — | All AI traffic routing | — | N/A | N/A | Internal infra |
| _[Add row for any other approved tool]_ | | | | | | | | |

## Explicitly NOT approved

| Tool | Why not |
|---|---|
| Personal-account ChatGPT | Free tier may train on input. No contractual protections. |
| Personal-account Claude.ai | Same — use Claude Code or Claude API instead. |
| Any tool not on this list | Approval process below. |

## How to add a tool

1. Open an issue tagged `tooling-request` with proposed tool, vendor, use case, alternative considered.
2. CISO reviews vendor terms (training opt-out, BAA if needed, security posture). Returns within 5 business days.
3. VP Engineering reviews use case and budget impact. Returns within 5 business days.
4. If approved, add a row to the table above with all fields filled in. Update `.claude/settings.json` allowlist if applicable.
5. Communicate to engineering team in next all-hands or eng-update channel.
6. Add to quarterly review cycle.

## Audit cadence

The matrix is reviewed quarterly by VP Eng + CISO. Any tool whose terms have changed since the last review (training defaults, pricing, BAA status, ownership) gets a row update or removal in the same review. Vendor-changes log lives in `vendor-procurement-runbook/`.
