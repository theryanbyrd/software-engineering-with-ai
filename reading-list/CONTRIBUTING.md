# Contributing to the Reading List

This list is opinionated. Entries earn slots based on signal-to-noise, not popularity. The editorial bar is the same as the book's: empirical, specific, no marketing language.

## How to contribute

1. **Edit `data.json`.** Don't edit `README.md` directly — it's auto-generated and your changes will be overwritten on the next render.
2. **Validate locally:**
   ```bash
   python3 scripts/generate.py --validate
   ```
3. **Render to preview:**
   ```bash
   python3 scripts/generate.py --dry-run | head -80
   ```
4. **Open a PR.** Include a brief reason for the entry in the PR description (not just in the `why` field).

## Entry format

Every entry in `data.json` requires:

```json
{
  "name": "Sean Goedecke",
  "url": "https://www.seangoedecke.com/",
  "category": "practitioner_writing",
  "kind": "blog",
  "why": "1-2 sentences on why this earns a slot. Specific, not marketing.",
  "added_on": "2026-05-04",
  "dated_through": "2027-05-04"
}
```

- **`category`** must be one of: `primary_sources`, `research_papers_and_benchmarks`, `practitioner_writing`, `podcasts`.
- **`kind`** must be one of: `blog`, `changelog`, `research`, `benchmark`, `podcast`, `newsletter`, `book`.
- **`why`** must be at least 20 characters and ideally 1-2 sentences. "Worth reading" is not a why; "Strong on evaluations and the operational side of running models in production" is.
- **`added_on`** is the date the entry was added. Use today's date.
- **`dated_through`** is the date after which the entry auto-prunes unless renewed during the next quarterly review. Default: 12 months from `added_on`. Vendor blogs may warrant 18 months; volatile newsletters may warrant 6.

## What gets accepted

### ✅ Primary sources

- Vendor blogs and changelogs that publish substantive (non-marketing) content
- Vendor docs that genuinely change as the product changes
- Standards bodies and reference implementations

**Editorial bar:** the source publishes fact, not advertising. A vendor blog with one substantive technical post per month qualifies; a vendor blog with monthly customer testimonials does not.

### ✅ Research papers and benchmarks

- Papers from research labs (Anthropic, DeepMind, OpenAI, METR, Stanford NLP, etc.) on coding-agent capabilities
- Empirical reports with disclosed methodology (DORA, DX, GitClear, Sonar, Faros)
- Benchmarks with published methodology and reproducible runs
- Survey reports with disclosed sample size, methodology, and limitations

**Editorial bar:** methodology is disclosed and the conclusions are calibrated to the evidence. Vendor research that's actually marketing in research clothing does not qualify even if it has a footer of citations.

### ✅ Practitioner writing

- Engineers actively building with AI tooling and writing publicly
- Output that explains things rather than just announcing them
- Sustained track record (5+ substantive posts in the past 12 months)

**Editorial bar:** the writing teaches rather than promotes. Posts that read like "here's how I built X with Y" usually qualify; posts that read like "here's why my company's product is great" do not.

### ✅ Podcasts and newsletters

- Long-form conversations with practitioners
- Newsletters with disclosed editorial perspective

**Editorial bar:** signal density. A podcast where 80% of episodes are vendor pitches does not qualify even if 20% are substantive.

## What does NOT get accepted

### ❌ Vendor-pitching content disguised as editorial

If the writer is the vendor's CEO/CMO and the content is structurally a pitch, it doesn't qualify. Even if the pitch is well-written.

### ❌ "Thought leadership" without substance

Posts that gesture at the importance of AI without saying anything specific. Posts whose claims could not be falsified by any evidence. Posts that are entirely about the writer's personal brand.

### ❌ Aggregator content

Content that summarizes other people's work without adding analysis. Newsletters that round up vendor announcements without commentary. The original sources go on the list, not the aggregator.

### ❌ Generic AI commentary

Writers whose AI commentary is a small fraction of their output and isn't differentiated from a thousand similar takes. The bar for "practitioner writing" is sustained substantive output specifically about AI engineering.

### ❌ Twitter / X / social-only accounts

Slot is for content that lives somewhere durable. If a writer's substantial work is on social media only, link the social account in the `_review_note` field but don't make it a top-level entry.

### ❌ Walled-garden content behind paywalls without preview

A few paid newsletters qualify if they offer enough free content to evaluate. Pure paywalled content does not — readers can't validate the recommendation.

### ❌ Books

Books go stale at the worst rate of any medium and most are out of date by the time they're published. Use the `book` kind only for books with sustained relevance (foundational ML/SE texts). The book this companion repo accompanies is itself an exception, but Ryan's bias is to keep the list focused on faster-moving formats.

## Retirement

Entries are retired (moved to `_retired` in `data.json`) when:

- **The URL is dead** and there's no replacement.
- **The author has left the field** or stopped publishing for 12+ months.
- **The content is now stale.** A benchmark that's been gamed. A vendor blog that's gone marketing-only. A practitioner who pivoted to a different domain.
- **A better alternative emerged** that covers the same ground more sharply.

To retire an entry, move it from its category array to the `_retired` object. Add `retired_on` and `retired_because` fields:

```json
"_retired": {
  "old-entry-name": {
    "name": "Old Entry Name",
    "url": "https://...",
    "retired_on": "2026-09-15",
    "retired_because": "Author stopped publishing in late 2025; last post 14 months ago."
  }
}
```

The `_retired` section is not rendered in the README. It exists for the maintainer's reference.

## Quarterly review

The maintainer runs a full review every quarter, on or near the `next_review` date in `data.json`. The review:

1. Run `python3 scripts/generate.py --check-stale` to surface entries near expiration.
2. For each near-expiry entry: renew (extend `dated_through`) or retire (move to `_retired`).
3. Review proposed additions accumulated since the last review.
4. Update the `version`, `last_reviewed`, and `next_review` fields.
5. Re-render the README.
6. Open a PR with the diff.

The discipline matters. A reading list that doesn't get reviewed quarterly accumulates dead links and stale recommendations within 12-18 months.

## What gets gamed (and how to prevent)

- **Self-nominations.** Common. Authors nominate themselves. Treat this as neutral — quality is the bar — but the maintainer should not be the same person as a heavy nominator. If the maintainer is also a nominator, a different reviewer should evaluate their entries.
- **Network effects.** "X recommended Y who recommended Z" can lead to a closed circle. Check for diversity of perspective, geography, and stage. The bar is signal, not insider status.
- **Recency bias.** Recent entries feel exciting and may not have a sustained track record. The "12+ months of substantive output" rule guards against this.
- **Slot inflation.** Easy to add an entry; hard to remove one. Quarterly review must include "what should we cut" as a real question, not just "what should we add."

## When to disagree with this list

If you think a category is wrong, an entry shouldn't be there, or a missing entry should be — open an issue. The list is opinionated but it's not infallible. Disagreement is welcome; the editorial bar is just disagreement with substance.

## Maintainer

Currently maintained by Ryan Byrd ([LinkedIn](https://www.linkedin.com/in/ryanbyrd)). To take over maintenance, open an issue.
