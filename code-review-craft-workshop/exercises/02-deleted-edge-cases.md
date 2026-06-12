# Exercise 02 — The Cleaner getUserName

**Primary smell:** S2 (deleted edge cases).
**Secondary smell:** S3 (silent error swallowing).
**Difficulty:** Medium. Drills the "open the original" habit.
**Pacing:** 5 minutes review, 3 minutes debrief.

## Scenario

The PR description:

> **Title:** Refactor `getUserName` for clarity
>
> The old implementation had several defensive branches. Most of them are no longer needed: callers should be using the typed `User` (not `User | null`), and the empty-string check was for legacy seed data that's been cleaned up. Reduces the function from 12 lines to 3.
>
> Tagged: `[AI-authored]`

The issue (one line):

> "Clean up `getUserName` — the defensive branches are leftovers from before we typed the user model."

## The diff

```typescript
// users/display.ts

// BEFORE
- export function getUserName(user: User | null): string {
-   if (user === null) {
-     return "Anonymous";
-   }
-   if (user.name === undefined || user.name === "") {
-     try {
-       return user.email.split("@")[0];
-     } catch (e) {
-       return "Unknown";
-     }
-   }
-   return user.name;
- }

// AFTER
+ export function getUserName(user: User): string {
+   return user.name;
+ }
```

```typescript
// users/display.test.ts

// BEFORE
- describe("getUserName", () => {
-   it("returns the user's name", () => {
-     expect(getUserName({ name: "Alice", email: "alice@example.com" })).toBe("Alice");
-   });
- });

// AFTER (unchanged)
  describe("getUserName", () => {
    it("returns the user's name", () => {
      expect(getUserName({ name: "Alice", email: "alice@example.com" })).toBe("Alice");
    });
  });
```

```typescript
// templates/welcome.tsx — used by getUserName, NOT in this PR but visible via grep
// existing code, unchanged:
export function WelcomeBanner({ user }: { user: User | null }) {
  return <h1>Welcome, {getUserName(user)}</h1>;
}
```

## Trainee task

Review this diff. Write the comments you would leave on the PR. Suggested time: 5 minutes.

Hint that an experienced reviewer would not need: open the file at the previous revision before reading the new code. The diff is small; the question is whether the deletions were safe.

---

## Instructor key

### Planted smells

**S2 (primary).** The new function handles one case (a valid `User` with a non-empty name) and crashes or returns wrong data for three other cases the original handled:

1. `user === null` — the original returned `"Anonymous"`. The new code throws `TypeError: Cannot read property 'name' of null`.
2. `user.name === undefined` or `""` — the original fell back to the email-prefix. The new code returns `undefined` or `""`.
3. `user.email` is missing — the original caught and returned `"Unknown"`. The new code... doesn't get there, because the new code doesn't handle the previous case either.

The PR description claims the callers are now using the typed `User` (not `User | null`). The reviewer can verify by grepping for `getUserName`. The `WelcomeBanner` component still passes `User | null`. The claim in the PR description is false.

**S3 (secondary, subtle).** The original code had a `try/catch` around the email-split that returned `"Unknown"` on failure. This is debatable — it could be argued as defensive null-checking rather than error-swallowing — but a stricter reading would call it S3-adjacent. The deletion of the try/catch removes the safety net, but it's a clean deletion (the whole branch goes), not the canonical S3 pattern (catching and discarding). Reasonable to flag as "S2 with an S3-shaped element," not full S3.

### Reference comments (what the experienced reviewer leaves)

**Inline on the new function:**

> S2: the original function handled three cases — `user === null`, `user.name` empty, and the email-fallback. The new function handles only the happy path. Specifically:
>
> 1. `getUserName(null)` now throws `TypeError`. The original returned `"Anonymous"`.
> 2. `getUserName({ name: "", email: "alice@example.com" })` now returns `""`. The original returned `"alice"`.
>
> The PR description claims callers are now using the typed `User`, but `WelcomeBanner` (`templates/welcome.tsx`) still passes `User | null`. Grep `getUserName` to confirm. Either:
>
> - Update the callers first (separate PR), then make this change. Or
> - Keep the null-check and the empty-name fallback in this function.

**Inline on the test file:**

> The test suite is unchanged. The new behavior — crash on null, return empty string on empty name — is untested. If the goal is to make this function strict, the tests should assert that strictness. Currently the tests would pass against either the old or the new implementation.

**Summary comment:**

> S2 in the function refactor. The PR description claims callers no longer pass null; that's not true (see `WelcomeBanner`). This refactor will produce a runtime error in the welcome banner the moment a logged-out user hits it. Send it back; either change the callers first or preserve the branches.

### Trainee may have also flagged

- **"Why is the test file unchanged?"** Correct concern, but not directly a signature — it's the absence of test coverage for the new strictness. Credit as bonus.
- **"The original `try/catch` swallowed the email-split error."** Technically true; reasonable to mention as S3-adjacent. Don't penalize.
- **"This is fine, types prevent the null case."** Wrong — types prevent the null case *only if all callers respect them*. The reviewer must grep to verify. If the trainee approved without grepping, they failed the exercise.

### What an L2-ready trainee writes

Names S2 explicitly. Opens the original code (or reads the deletion) and lists the branches that disappeared. Greps for callers and finds at least one passing `User | null`. Articulates the runtime consequence (crash in `WelcomeBanner`). Proposes a fix.

### What a not-yet-ready trainee writes

- "Looks cleaner now, +1."
- "The function is shorter; tests still pass."
- "I'd add JSDoc but otherwise LGTM."

These are the responses that ship S2 to production. They're not bad-faith; they're the result of reading the *new* code without comparing to the *old* code. The exercise drills the comparison habit.

## Debrief prompts

For the workshop facilitator running this exercise:

1. **"Who opened the original code (or noted the deletions)?"** Hands. If fewer than half, that's the discipline gap to drill.
2. **"What did the original handle that the new code doesn't?"** Round-robin three answers — null, empty name, email-fallback. Make sure all three surface.
3. **"How did you check whether the PR description's claim was true?"** Looking for: grep for callers; open the welcome component; verify the type at the call site.
4. **"What's the rule?"** Looking for: **when a function shrinks, open the original and count the branches.** This is the discipline this exercise is drilling.

## Why this is exercise 02

S2 is the second-most-common signature (per [`../incident-postmortem-templates/SLOP_SIGNATURE_REFERENCE.md`](../../incident-postmortem-templates/SLOP_SIGNATURE_REFERENCE.md)) and the one with the most expensive failure mode short of S5. A reviewer who can't catch S2 will ship null-pointer bugs on a regular basis once the team's AI authorship rate goes up.

The exercise specifically drills the "open the original" habit. Engineers who pattern-match on "the new code is cleaner" without doing the comparison will fail this exercise. That failure is the data — it tells the manager exactly what muscle needs developing.

## Companion artifacts

- [`../ai-code-smell-checklist.md`](../ai-code-smell-checklist.md#s2) — the deep reference for S2
- [`01-mocked-impl.md`](01-mocked-impl.md) — the previous exercise
- [`03-multi-smell.md`](03-multi-smell.md) — the next exercise
- Ch 2 §2.2 — source
