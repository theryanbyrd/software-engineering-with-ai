# Pattern: Information Requirements (the "inverted brief")

**When to use:** Before finalizing any non-trivial spec. Instead of guessing what context
the agent needs, make the agent tell you (Ch 19 §"information requirements").

**Template:**

```
Here is the task I want to delegate:

<paste the draft spec / issue>

Don't start the work yet. First give me your information requirements: what context,
examples, conventions, files, contracts, edge cases, or constraints would you need to
do this well? List them as questions or gaps. I'll fill them in before you begin.
```

**Why it works:** It surfaces the gaps in your spec while they are cheap to fix (before a
branch exists) rather than expensive (after a wrong implementation). Run it in plan mode.

**References:** Ch 19; pairs with [`agent-ready-issue.md`](agent-ready-issue.md).
