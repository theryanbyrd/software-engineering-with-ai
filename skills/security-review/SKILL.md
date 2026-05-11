---
name: security-review
description: Use when reviewing a diff for security issues. Applies an adversarial reviewer's posture. Looks for: removed validation, swallowed errors, weakened tests, secret exposure, injection vectors, auth/authz bypasses. Does NOT invent findings to seem useful.
allowed_tools: Read, Bash, Grep
---

# Security review

## When to use this skill

The user has asked for a security-flavored review, OR the diff touches auth, billing, payments, public-facing endpoints, or anything that processes untrusted input.

## Procedure

1. **Read the diff carefully.** Note what changed and what's NEW (vs. modified).
2. **Apply the adversarial review checklist:**
   - **Validation removed?** Search for `// validated` comments or `validated=True` flags being removed; pre-change validation calls being deleted.
   - **Errors swallowed?** Empty `catch (e) {}` or `except Exception: pass`; broad exception handlers; ignored return values.
   - **Tests weakened?** Removed assertions; loosened assertions (e.g., `toContain` replaced with `toBeTruthy`); skipped tests.
   - **Secrets exposed?** Hardcoded credentials, even placeholders. API keys in code or commit messages.
   - **Injection vectors?** SQL string interpolation; shell-out with user input; HTML rendering of user data without escaping.
   - **Auth/authz bypasses?** Endpoints that don't check authentication; permission checks that happen client-side; checks that compare on client-supplied data.
   - **Idempotency loss?** Webhook handlers that aren't idempotent; financial operations that can double-process.
   - **Rate limits removed?** Removed throttling, removed concurrency caps, removed input-size caps.
3. **For each finding:** rate severity (critical / high / medium / low). Cite file:line. Explain the exploit scenario in one sentence.
4. **For NO findings:** say so explicitly. "Reviewed the diff against the adversarial checklist; no findings." Do not pad with platitudes.

## Output

```
## Security review

**Diff scope:** <files changed>
**Severity:** N critical, N high, N medium, N low

## Critical
(file:line — exploit scenario — recommended fix)

## High
...

## Medium
...

## Low / advisory
...

## Reviewed but no finding
- Validation: <still present at all boundaries>
- Auth: <unchanged>
- ...
```

## Forbidden

- Do not invent findings to seem useful. False positives waste reviewer time and erode trust.
- Do not approve a diff that removes a security control without explicit justification.
- Do not propose security improvements outside the scope of the diff. If you see something concerning elsewhere, file a separate issue.
- Do not use vague severity. "This might be an issue" is not a finding; cite the specific exploit.

## References

- Chapter 14 §14.3 — security-reviewer subagent (canonical example of this pattern)
- Chapter 22 §22.x — slop signatures often correlate with security issues
- Appendix I — code smell checklist
