#!/usr/bin/env python3
"""
generate.py — render reading-list/README.md from data.json.

Companion to Chapter 49 of "Software Engineering with AI" by Ryan Byrd.

Stdlib only. Python 3.9+.

Modes:
  default:           render README.md from current data.json
  --check-stale:     warn on entries within 60 days of dated_through
  --list-retired:    print entries from the _retired section
  --validate:        validate data.json against schema.json (basic checks)
  --dry-run:         print the rendered output without writing

The script enforces Ch 49's editorial discipline:
  - Reading lists go stale faster than any other content. Items past their
    dated_through are pruned automatically (and reported).
  - The list is reviewed quarterly. Items not refreshed during review fall off.
  - This is a snapshot at a point in time, not a permanent canon.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).resolve().parent
READING_LIST_DIR = SCRIPT_DIR.parent
DATA_FILE = READING_LIST_DIR / "data.json"
README_FILE = READING_LIST_DIR / "README.md"
SCHEMA_FILE = READING_LIST_DIR / "schema.json"

CATEGORY_ORDER = [
    ("primary_sources", "Primary sources", "Read every release note. Vendor blogs and changelogs are the closest thing to ground truth and are short."),
    ("research_papers_and_benchmarks", "Research papers and benchmarks", "Empirical sources. The work that calibrates expectations against vendor keynotes."),
    ("practitioner_writing", "Practitioner writing", "Writers whose output has consistently been worth reading in 2025-2026. The list is not exhaustive and will look different in a year."),
    ("podcasts", "Podcasts", "Long-form conversations. Useful for the cross-functional and founder/builder views."),
]

KIND_LABELS = {
    "blog": "Blog",
    "changelog": "Changelog",
    "research": "Research",
    "benchmark": "Benchmark",
    "podcast": "Podcast",
    "newsletter": "Newsletter",
    "book": "Book",
}


# ---------------------------------------------------------------------------
# Loading and validation
# ---------------------------------------------------------------------------

def load_data() -> dict:
    if not DATA_FILE.is_file():
        print(f"error: {DATA_FILE} not found", file=sys.stderr)
        sys.exit(2)
    try:
        return json.loads(DATA_FILE.read_text())
    except json.JSONDecodeError as exc:
        print(f"error: {DATA_FILE} is not valid JSON: {exc}", file=sys.stderr)
        sys.exit(2)


def validate(data: dict) -> list[str]:
    """Basic structural validation. Returns list of error strings (empty = OK)."""
    errors = []
    required_top = ["version", "last_reviewed", "next_review", "maintainer"]
    for key in required_top:
        if key not in data:
            errors.append(f"missing required top-level field: {key}")

    # Check date fields parse
    for date_field in ("last_reviewed", "next_review"):
        if date_field in data:
            try:
                datetime.fromisoformat(data[date_field])
            except (ValueError, TypeError):
                errors.append(f"{date_field} is not a valid ISO 8601 date: {data.get(date_field)!r}")

    # Check entries
    required_entry = {"name", "url", "category", "kind", "why", "added_on", "dated_through"}
    valid_kinds = set(KIND_LABELS.keys())
    valid_cats = {c[0] for c in CATEGORY_ORDER}

    for cat, _, _ in CATEGORY_ORDER:
        if cat not in data:
            continue
        for i, entry in enumerate(data[cat]):
            prefix = f"{cat}[{i}] ({entry.get('name', '<unnamed>')})"
            missing = required_entry - set(entry.keys())
            if missing:
                errors.append(f"{prefix}: missing fields {sorted(missing)}")
                continue
            if entry["category"] != cat:
                errors.append(f"{prefix}: category mismatch (entry says {entry['category']!r}, lives in {cat!r})")
            if entry["category"] not in valid_cats:
                errors.append(f"{prefix}: invalid category {entry['category']!r}")
            if entry["kind"] not in valid_kinds:
                errors.append(f"{prefix}: invalid kind {entry['kind']!r}")
            if not entry["url"].startswith(("http://", "https://")):
                errors.append(f"{prefix}: url must start with http:// or https://")
            if len(entry.get("why", "")) < 20:
                errors.append(f"{prefix}: 'why' is shorter than 20 chars; explain more")
            for date_field in ("added_on", "dated_through"):
                try:
                    datetime.fromisoformat(entry[date_field])
                except (ValueError, TypeError):
                    errors.append(f"{prefix}: {date_field} is not a valid ISO 8601 date")
            # Check dated_through is after added_on
            try:
                added = datetime.fromisoformat(entry["added_on"])
                expires = datetime.fromisoformat(entry["dated_through"])
                if expires <= added:
                    errors.append(f"{prefix}: dated_through must be after added_on")
            except (ValueError, TypeError, KeyError):
                pass  # already reported above

    return errors


# ---------------------------------------------------------------------------
# Pruning
# ---------------------------------------------------------------------------

def partition_entries(data: dict, today: datetime) -> tuple[dict, list[dict], list[dict]]:
    """Split entries into active / expired / approaching-stale.
    Returns (active_data, expired_entries, stale_warnings).
    """
    expired = []
    stale_warnings = []
    active_data = dict(data)

    sixty_days = timedelta(days=60)

    for cat, _, _ in CATEGORY_ORDER:
        if cat not in data:
            continue
        active = []
        for entry in data[cat]:
            try:
                expires = datetime.fromisoformat(entry["dated_through"])
            except (ValueError, KeyError):
                # Malformed; treat as active so it gets fixed
                active.append(entry)
                continue
            if expires < today:
                expired.append(entry)
            else:
                active.append(entry)
                if expires - today <= sixty_days:
                    stale_warnings.append(entry)
        active_data[cat] = active

    return active_data, expired, stale_warnings


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render(data: dict, today: datetime) -> str:
    lines = []

    # Header
    lines.append("# AI Coding Reading List")
    lines.append("")
    lines.append(f"> **Auto-generated from `data.json`. Do not edit this file directly. Run `scripts/generate.py` after editing the source.**")
    lines.append("")
    lines.append(f"A maintained, dated reading list for engineering leaders building AI-native engineering practices. Companion to Chapter 49 of [_Software Engineering with AI: A Practical Handbook for the Claude Code Era_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.")
    lines.append("")

    # Metadata
    lines.append("## Maintenance status")
    lines.append("")
    lines.append(f"- **Version:** `{data.get('version', 'unknown')}`")
    lines.append(f"- **Last reviewed:** {data.get('last_reviewed', 'unknown')}")
    lines.append(f"- **Next review:** {data.get('next_review', 'unknown')}")
    lines.append(f"- **Maintainer:** [@{data.get('maintainer', 'unknown')}](https://www.linkedin.com/in/ryanbyrd)")
    lines.append("")

    # The discipline (Ch 49 §49.4)
    lines.append("## The discipline")
    lines.append("")
    lines.append("Per Ch 49 §49.4 of the handbook:")
    lines.append("")
    lines.append("- Read **one substantive piece per week**.")
    lines.append("- Discuss **one piece per month** with the platform team.")
    lines.append("- Write **one short note per quarter** on what changed in your understanding.")
    lines.append("- The reading list is not the goal. The goal is a calibrated set of expectations built from primary sources, not vendor keynotes.")
    lines.append("")

    # Editorial note
    lines.append("## Why a dated list")
    lines.append("")
    lines.append("Reading lists go stale faster than any other content in this domain. The people writing the most useful work in mid-2026 may not be the same in mid-2027. Each entry has a `dated_through` field; entries past that date fall off the active list automatically during quarterly review. This protects against the canon ossifying around writers who have stopped producing useful work.")
    lines.append("")

    # Categories
    for cat, title, blurb in CATEGORY_ORDER:
        entries = data.get(cat, [])
        if not entries:
            continue
        lines.append(f"## {title}")
        lines.append("")
        lines.append(f"_{blurb}_")
        lines.append("")
        lines.append("| Source | Kind | Why it's worth reading |")
        lines.append("|---|---|---|")
        for entry in sorted(entries, key=lambda e: e["name"].lower()):
            name_link = f"[{entry['name']}]({entry['url']})"
            kind = KIND_LABELS.get(entry["kind"], entry["kind"].title())
            why = entry["why"].replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {name_link} | {kind} | {why} |")
        lines.append("")

    # Footer — contribution and retirement
    lines.append("---")
    lines.append("")
    lines.append("## Contributing")
    lines.append("")
    lines.append("See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the editorial bar, the entry format, and what gets accepted vs. declined. The short version:")
    lines.append("")
    lines.append("- Every entry must have a specific reason it earns a slot. \"It's popular\" is not a reason.")
    lines.append("- No vendor-pitching content. No \"thought leadership\" that's a marketing piece in disguise.")
    lines.append("- Submit by editing `data.json` and opening a PR; the maintainer renders the README during quarterly review or accepts inline as appropriate.")
    lines.append("")

    lines.append("## Retirement criteria")
    lines.append("")
    lines.append("Entries are retired (moved to `_retired` in `data.json`) when:")
    lines.append("")
    lines.append("- The URL is dead and there's no replacement.")
    lines.append("- The author has left the field or stopped publishing.")
    lines.append("- The content is now stale (e.g., a benchmark that's been gamed, a vendor blog that's gone marketing-only).")
    lines.append("- A better alternative has emerged that covers the same ground more sharply.")
    lines.append("")
    lines.append("Retirement is normal and expected. A reading list that doesn't retire entries becomes inaccurate within 12-18 months.")
    lines.append("")

    lines.append("## Generated")
    lines.append("")
    lines.append(f"This file was generated on {today.strftime('%Y-%m-%d')} from `data.json` (version `{data.get('version', 'unknown')}`). Total entries: {sum(len(data.get(c[0], [])) for c in CATEGORY_ORDER)}.")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--check-stale", action="store_true",
                        help="Warn on entries approaching dated_through (within 60 days)")
    parser.add_argument("--list-retired", action="store_true",
                        help="Print entries from the _retired section")
    parser.add_argument("--validate", action="store_true",
                        help="Validate data.json structure")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print rendered output without writing README.md")
    parser.add_argument("--today", help="Override today's date (YYYY-MM-DD) for testing")
    args = parser.parse_args()

    today = datetime.fromisoformat(args.today) if args.today else datetime.now()

    data = load_data()

    # Validate first
    if args.validate:
        errors = validate(data)
        if errors:
            print(f"VALIDATION FAILED: {len(errors)} error(s)")
            for e in errors:
                print(f"  - {e}")
            return 1
        print("VALIDATION OK")
        return 0

    # Always do a quick validation pass before rendering
    errors = validate(data)
    if errors:
        print(f"warning: data.json has {len(errors)} validation issue(s); fix before next quarterly review", file=sys.stderr)
        for e in errors[:5]:
            print(f"  - {e}", file=sys.stderr)
        if len(errors) > 5:
            print(f"  ... and {len(errors) - 5} more (run with --validate to see all)", file=sys.stderr)

    # List retired
    if args.list_retired:
        retired = data.get("_retired", {})
        if not retired or all(k.startswith("_") for k in retired):
            print("No retired entries.")
            return 0
        print("Retired entries:")
        for key, entry in retired.items():
            if key.startswith("_"):
                continue
            print(f"  {entry.get('name', key)} (retired {entry.get('retired_on', '?')}: {entry.get('retired_because', 'no reason given')})")
        return 0

    # Partition
    active_data, expired, stale = partition_entries(data, today)

    if expired:
        print(f"PRUNED: {len(expired)} expired entries (past dated_through):", file=sys.stderr)
        for entry in expired:
            print(f"  - {entry.get('name')} (dated_through {entry.get('dated_through')})", file=sys.stderr)

    if args.check_stale:
        if not stale:
            print("No entries approaching staleness (60-day window).")
        else:
            print(f"APPROACHING STALENESS: {len(stale)} entries within 60 days of dated_through:")
            for entry in stale:
                print(f"  - {entry.get('name')}: dated_through {entry.get('dated_through')}")
        return 0

    # Render
    rendered = render(active_data, today)

    if args.dry_run:
        print(rendered)
        return 0

    README_FILE.write_text(rendered)
    print(f"Wrote {README_FILE}")

    n_entries = sum(len(active_data.get(c[0], [])) for c in CATEGORY_ORDER)
    print(f"Rendered {n_entries} active entries across {len(CATEGORY_ORDER)} categories")
    if expired:
        print(f"Pruned {len(expired)} expired entries (still in data.json; remove during next quarterly review)")
    if stale:
        print(f"Note: {len(stale)} entries approach dated_through within 60 days; review during next cycle")

    return 0


if __name__ == "__main__":
    sys.exit(main())
