# Pattern: Task Decomposition

**When to use:** Breaking a feature into 5–10 agent-ready issues that can run in parallel
without stepping on each other (Ch 20). CODEOWNERS and package boundaries do most of the
conflict prevention.

**Template:**

```
Decompose <feature> into 5–10 agent-ready issues that can be implemented in parallel.
For each issue give: title, scope, the files/packages it touches, and its dependencies
on other issues. Flag any two issues that touch the same files (merge-conflict risk) and
propose a sequencing or boundary change to remove the overlap. Respect existing package
and CODEOWNERS boundaries. Don't write code — produce the issue list.
```

**References:** Ch 20 (task decomposition); each resulting issue should follow
[`agent-ready-issue.md`](agent-ready-issue.md).
