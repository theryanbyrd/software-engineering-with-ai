# Performance Review Section — Harness Contribution

Add this section to your performance review template, per Ch 60 §60.3 of _Software Engineering with AI_.

---

## Section: Harness Contribution

### What this measures

The engineer's contribution to the team's AI-native engineering harness — skills, hooks, subagents, MCP integrations, CLAUDE.md/AGENTS.md investments, CI integrations, custom auditors, verify command improvements.

This section explicitly recognizes work that was previously invisible in performance reviews. An engineer who shipped a feature AND contributed to harness has done more work than an engineer who shipped the same feature alone.

### Manager prompt

> "Describe the harness contributions this engineer has made in the review period. Include: what was shipped, who used it, what it enabled, and any tradeoffs."

### Self-assessment prompt for the engineer

> "What did you ship this period that improved how your team or the broader engineering org uses AI tooling? Describe the problem, the design, the trade-offs, and the adoption."

### Grading rubric

Score the engineer's harness contribution on the dimensions below. Use the levels in [`../career-ladder/ic-track-additions.md`](../career-ladder/ic-track-additions.md) for what's expected at each IC level.

| Dimension | What we're looking for |
|---|---|
| **Substance** | Real shipped work, not concept or planning. Implementation level, with bugs hit and patched. |
| **Reach** | Was it used by other engineers? Other teams? Just the engineer themselves? |
| **Design quality** | Did the engineer make defensible trade-offs? Can they articulate alternatives they rejected? |
| **Maintenance posture** | Is the component documented, tested, and supported? Or shipped-and-forgotten? |
| **Mentorship adjacent** | Did the engineer help others contribute to the harness, not just contribute themselves? |

### Common scoring patterns

- **Strong (above expectations):** Multiple harness contributions during the period. Cross-team adoption. Mentorship of more junior engineers in shipping their own harness work.
- **Meeting expectations:** One substantial harness contribution OR multiple smaller improvements. Used by the engineer's own team.
- **Below expectations:** No harness contribution during the period. The engineer's work was entirely product features without harness improvement.

### Calibration notes

- For L3 engineers: "meeting expectations" is one small contribution (a fix, a CLAUDE.md addition, a skill bug report with a clear repro).
- For L4 engineers: "meeting expectations" is one substantive contribution (a working skill, a hook, a subagent).
- For L5+ engineers: "meeting expectations" is contribution that crosses team boundaries OR substantial mentorship of L4s in shipping their first contribution.
- A "no harness contribution" review for a senior engineer should be a coaching moment, not an instant negative score. Some review periods involve heavy product-feature work; the question is the trend over multiple periods.

### What this section will NOT do

- Will not capture every contribution that mattered. An engineer who reviewed a colleague's harness PR carefully and provided substantive feedback contributed; the section may not surface this. Cross-reference with the review-discipline section.
- Will not work in a culture that doesn't celebrate harness contribution publicly. If the org's blog posts and internal recognition only highlight product features, the harness contributors will move to companies that do.

### Tied to retention

Per Ch 60 §60.4, the engineers who contribute most to the harness are also the ones most likely to leave for the market premium. Use this section's findings as input to the retention strategy: the engineer with strong harness contribution should be visible to skip-level leaders, should be considered for public credit (internal blog post, conference talk with company support), and should be on the retention-watch list.
