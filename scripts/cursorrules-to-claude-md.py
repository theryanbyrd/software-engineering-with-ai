#!/usr/bin/env python3
"""
cursorrules-to-claude-md.py — migration helper from Cursor / Windsurf /
Copilot project memory files to CLAUDE.md (and AGENTS.md).

Companion to "Software Engineering with AI: A Practical Handbook for the
Claude Code Era" by Ryan Byrd, particularly Chapter 53 (migration playbooks).

Detects and converts:
  - .cursorrules                    (Cursor — single-file format)
  - .cursor/rules/*.mdc             (Cursor — multi-file format introduced 2024)
  - .windsurfrules                  (Windsurf)
  - .github/copilot-instructions.md (GitHub Copilot)
  - .aider.conf.yml                 (Aider — partial: extracts text rules only)

Stdlib only. Python 3.9+.

Usage:
    cursorrules-to-claude-md.py                       # auto-discover in cwd
    cursorrules-to-claude-md.py --source .cursorrules # explicit source
    cursorrules-to-claude-md.py --output CLAUDE.md    # explicit output
    cursorrules-to-claude-md.py --stdout              # print to stdout
    cursorrules-to-claude-md.py --no-scaffold         # skip empty TODO sections
    cursorrules-to-claude-md.py --merge               # merge with existing CLAUDE.md
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

VERSION = "2026.q3"

# ---------------------------------------------------------------------------
# Source detection
# ---------------------------------------------------------------------------

@dataclass
class Source:
    kind: str          # "cursorrules" | "cursor-mdc" | "windsurf" | "copilot" | "aider"
    paths: list[Path]
    raw: str           # combined raw text


def discover_sources(repo: Path) -> list[Source]:
    """Find all known source files in a repo."""
    sources = []

    # .cursorrules (single file)
    p = repo / ".cursorrules"
    if p.is_file():
        sources.append(Source(kind="cursorrules", paths=[p], raw=p.read_text(errors="ignore")))

    # .cursor/rules/*.mdc
    cursor_rules_dir = repo / ".cursor" / "rules"
    if cursor_rules_dir.is_dir():
        mdc_files = sorted(cursor_rules_dir.glob("*.mdc"))
        if mdc_files:
            combined = "\n\n".join(f"# From {p.name}\n\n{p.read_text(errors='ignore')}" for p in mdc_files)
            sources.append(Source(kind="cursor-mdc", paths=mdc_files, raw=combined))

    # .windsurfrules
    p = repo / ".windsurfrules"
    if p.is_file():
        sources.append(Source(kind="windsurf", paths=[p], raw=p.read_text(errors="ignore")))

    # .github/copilot-instructions.md
    p = repo / ".github" / "copilot-instructions.md"
    if p.is_file():
        sources.append(Source(kind="copilot", paths=[p], raw=p.read_text(errors="ignore")))

    # .aider.conf.yml — partial support (extract any lint/test/instruction text)
    p = repo / ".aider.conf.yml"
    if p.is_file():
        sources.append(Source(kind="aider", paths=[p], raw=p.read_text(errors="ignore")))

    return sources


# ---------------------------------------------------------------------------
# Section classification
# ---------------------------------------------------------------------------

@dataclass
class Sections:
    """Classified content destined for CLAUDE.md sections."""
    commands: list[str] = field(default_factory=list)
    conventions: list[str] = field(default_factory=list)
    restricted: list[str] = field(default_factory=list)
    forbidden: list[str] = field(default_factory=list)
    invariants: list[str] = field(default_factory=list)
    pointers: list[str] = field(default_factory=list)
    cost_discipline: list[str] = field(default_factory=list)
    misc: list[str] = field(default_factory=list)
    untranslatable: list[str] = field(default_factory=list)


def classify_line(line: str) -> str:
    """Classify a rule line into a CLAUDE.md section."""
    low = line.lower().strip(" -*•")

    # Commands — explicit run/build/test mentions
    if re.search(r"\b(run|use|invoke|execute)\b.*\b(npm|pnpm|yarn|pytest|cargo|go test|make|docker|bundle exec)\b", low):
        return "commands"
    if re.match(r"(npm|pnpm|yarn|pytest|cargo|go|make|docker|bundle)\s", low):
        return "commands"
    if "verify" in low and ("command" in low or "script" in low or "run" in low):
        return "commands"

    # Forbidden — never / don't / no / forbidden / banned
    if re.search(r"\b(never|forbidden|banned|disallow|do not|don't|no\s+\w+ing)\b", low):
        return "forbidden"
    if "no eval" in low or "no shell" in low or "no globals" in low:
        return "forbidden"

    # Restricted — paths or modules limited to specific reviewers
    if re.search(r"\b(restrict|protect|gated|codeowner|owner|review required|sensitive)\b", low):
        return "restricted"
    if re.search(r"\b(auth|billing|payments|secrets?|credentials?|production|infra|migrations?)\b", low):
        if "must" in low or "only" in low or "require" in low:
            return "restricted"

    # Architecture invariants — must / always / never (without forbidden context)
    if re.search(r"\b(must always|invariant|cannot import|boundary|architecture|never deletes|idempotent)\b", low):
        return "invariants"

    # Cost / model routing
    if re.search(r"\b(model|opus|sonnet|haiku|gpt-|claude-|cost|token|budget|cheap|expensive)\b", low):
        return "cost_discipline"

    # Pointers — references to docs, ADRs, etc.
    if re.search(r"\b(see|read|reference|adr|docs?/|documentation|@reference)\b", low) and any(
        c in low for c in ("/", "doc", "adr", "readme")
    ):
        return "pointers"

    # Conventions — style, naming, patterns
    if re.search(r"\b(use|prefer|style|naming|format|convention|pattern|always)\b", low):
        return "conventions"

    return "misc"


def parse_rules(raw: str) -> list[str]:
    """Extract rule lines from raw source text. Handles bullets, plain lines, headers."""
    rules: list[str] = []

    for line in raw.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        # Skip markdown headers (we'll regenerate them)
        if stripped.startswith("#"):
            continue
        # Skip code fences and YAML frontmatter
        if stripped.startswith("```") or stripped == "---":
            continue
        # Strip bullet prefixes
        cleaned = re.sub(r"^[-*•]\s+", "", stripped)
        cleaned = re.sub(r"^\d+\.\s+", "", cleaned)  # numbered list
        if not cleaned or len(cleaned) < 3:
            continue
        rules.append(cleaned)

    return rules


def classify_all(rules: list[str]) -> Sections:
    """Classify all rules into sections."""
    sections = Sections()
    for rule in rules:
        category = classify_line(rule)
        getattr(sections, category).append(rule)
    return sections


# ---------------------------------------------------------------------------
# Output generation
# ---------------------------------------------------------------------------

def detect_stack(repo: Path) -> str:
    """Return a short stack description for the generated CLAUDE.md."""
    if (repo / "package.json").exists():
        if (repo / "tsconfig.json").exists():
            return "TypeScript / Node"
        return "JavaScript / Node"
    if (repo / "pyproject.toml").exists() or (repo / "setup.py").exists() or (repo / "requirements.txt").exists():
        return "Python"
    if (repo / "go.mod").exists():
        return "Go"
    if (repo / "Cargo.toml").exists():
        return "Rust"
    if (repo / "Gemfile").exists():
        return "Ruby"
    if (repo / "pom.xml").exists() or (repo / "build.gradle").exists():
        return "Java / JVM"
    return "[REPLACE — describe your stack]"


def detect_verify_command(repo: Path) -> str:
    """Detect a likely verify command from existing tooling."""
    pkg = repo / "package.json"
    if pkg.exists():
        text = pkg.read_text(errors="ignore")
        if '"verify"' in text:
            return "npm run verify"
        return "[CONFIGURE — add `\"verify\": \"npm run lint && npm run typecheck && npm test\"` to package.json]"

    if (repo / "Makefile").exists():
        text = (repo / "Makefile").read_text(errors="ignore")
        if re.search(r"^verify\s*:", text, re.M):
            return "make verify"

    if (repo / "pyproject.toml").exists():
        return "[CONFIGURE — set up `make verify` running ruff + mypy + pytest]"

    return "[CONFIGURE — define a single `verify` command per Ch 7]"


def render_claude_md(sources: list[Source], sections: Sections, repo: Path, scaffold: bool) -> str:
    """Render a CLAUDE.md from classified sections."""
    stack = detect_stack(repo)
    verify_cmd = detect_verify_command(repo)
    source_list = ", ".join(f"`{p.name}`" for s in sources for p in s.paths)

    out: list[str] = []

    # Header
    out.append("# Project memory")
    out.append("")
    out.append(f"_Generated by `cursorrules-to-claude-md.py` from: {source_list}_")
    out.append(f"_Stack detected: {stack}_")
    out.append("_Review every section before relying on it. The migration tool is heuristic._")
    out.append("")

    # Commands
    out.append("## Commands")
    out.append("")
    out.append(f"- **Verify (run before claiming work is done):** `{verify_cmd}`")
    if sections.commands:
        for rule in sections.commands:
            out.append(f"- {rule}")
    elif scaffold:
        out.append("- [TODO — add lint, typecheck, format, test commands here]")
    out.append("")

    # Conventions
    out.append("## Conventions")
    out.append("")
    if sections.conventions:
        for rule in sections.conventions:
            out.append(f"- {rule}")
    elif scaffold:
        out.append("- [TODO — describe your code style, naming, validation conventions]")
    out.append("")

    # Restricted areas
    out.append("## Restricted areas (require CODEOWNER review)")
    out.append("")
    if sections.restricted:
        for rule in sections.restricted:
            out.append(f"- {rule}")
    elif scaffold:
        out.append("- [TODO — list paths that need explicit review (auth, billing, infra, workflows)]")
    out.append("")

    # Architecture invariants
    out.append("## Architecture invariants")
    out.append("")
    if sections.invariants:
        for rule in sections.invariants:
            out.append(f"- {rule}")
    elif scaffold:
        out.append("- [TODO — list 3-5 hard invariants the agent must respect (e.g., 'UI must not import from db', 'all auth server-side', 'webhooks idempotent')]")
    out.append("")

    # Forbidden
    out.append("## Forbidden")
    out.append("")
    if sections.forbidden:
        for rule in sections.forbidden:
            out.append(f"- {rule}")
    else:
        # Always include the standard forbidden list — these are universal
        out.append("- No production credentials in code, fixtures, tests, or commit messages.")
        out.append("- No `eval()`, shell-out with user input, or unsafe deserialization.")
        out.append("- No deletion of tests \"to make CI pass.\"")
        out.append("- No commits that bypass `verify`.")
    out.append("")

    # Pointers
    out.append("## Pointers")
    out.append("")
    if sections.pointers:
        for rule in sections.pointers:
            out.append(f"- {rule}")
    elif scaffold:
        out.append("- [TODO — link to architecture docs, ADRs, repo map (`llms.txt`)]")
    out.append("")

    # Cost discipline (only if there's content)
    if sections.cost_discipline or scaffold:
        out.append("## Cost discipline")
        out.append("")
        if sections.cost_discipline:
            for rule in sections.cost_discipline:
                out.append(f"- {rule}")
        elif scaffold:
            out.append("- Default routing: Sonnet for tier-2 work, Haiku for trivial transformations, Opus only for tier-3 architectural exploration.")
            out.append("- Stop and ask the human if you find yourself in a retry loop. Retry loops are the largest source of wasted cost.")
        out.append("")

    # Misc — anything we couldn't classify confidently
    if sections.misc:
        out.append("## Other rules (review and re-classify)")
        out.append("")
        out.append("_These rules were carried over from the source file but not confidently classified. Review and move to the appropriate section above._")
        out.append("")
        for rule in sections.misc:
            out.append(f"- {rule}")
        out.append("")

    # Untranslatable warnings
    if sections.untranslatable:
        out.append("## Notes — content not migrated")
        out.append("")
        out.append("_The following content was in the source but is platform-specific or could not be translated:_")
        out.append("")
        for rule in sections.untranslatable:
            out.append(f"- {rule}")
        out.append("")

    # Final guidance for the user
    out.append("---")
    out.append("")
    out.append("## Migration notes")
    out.append("")
    out.append("This file was generated by `cursorrules-to-claude-md.py`. Before relying on it:")
    out.append("")
    out.append("1. **Read every section.** The classifier is heuristic; some rules may be in the wrong section.")
    out.append("2. **Replace `[TODO]` markers** with content specific to your codebase.")
    out.append("3. **Verify the verify command actually works.** Run it once to confirm.")
    out.append("4. **Add the missing sections.** A complete CLAUDE.md typically also has: Module Status table (for monorepos), per-package README pointers, and team-specific terminology.")
    out.append("5. **Create AGENTS.md alongside** — usually it's a short cross-vendor mirror of this file.")
    out.append("6. **Keep the source file for now.** Don't delete `.cursorrules` etc. until you've confirmed CLAUDE.md is complete and your team has migrated.")
    out.append("")

    return "\n".join(out)


def render_agents_md() -> str:
    """A minimal AGENTS.md to accompany the generated CLAUDE.md."""
    return """# Agent guidance

This file is the cross-vendor (Claude Code, Cursor, Codex, others) version of `CLAUDE.md`. The full content is there; this is the entry point for tools that look for AGENTS.md by name.

## Read CLAUDE.md first

Before doing any work in this repo, read `CLAUDE.md` for full conventions, commands, restrictions, and architecture invariants.

## Quick reference

- **Verify command:** see CLAUDE.md § Commands
- **Restricted paths:** see CLAUDE.md § Restricted areas
- **Forbidden:** see CLAUDE.md § Forbidden

## Plan-then-implement-then-verify

For any non-trivial change:

1. Read the relevant code and tests.
2. State your plan (what files, what changes, what tests).
3. Get approval (from the human if interactive; from the issue spec if agentic).
4. Implement.
5. Run the verify command.
6. If verify fails, fix and re-verify. Don't claim done with a failing verify.

## Default to small PRs

PRs over 400 lines diff should be decomposed.
"""


def render_merge_with_existing(existing: str, new_sections: Sections) -> str:
    """Append new content to an existing CLAUDE.md without clobbering it."""
    out = [existing.rstrip(), "", ""]
    out.append("---")
    out.append("")
    out.append("## Migrated rules")
    out.append("")
    out.append(f"_Imported by cursorrules-to-claude-md.py v{VERSION} on {Path('.').resolve().name}._")
    out.append("_Review and integrate these into the sections above; this section can be deleted once integration is complete._")
    out.append("")

    for category, items in [
        ("Commands", new_sections.commands),
        ("Conventions", new_sections.conventions),
        ("Restricted", new_sections.restricted),
        ("Architecture invariants", new_sections.invariants),
        ("Forbidden", new_sections.forbidden),
        ("Pointers", new_sections.pointers),
        ("Cost discipline", new_sections.cost_discipline),
        ("Other (unclassified)", new_sections.misc),
    ]:
        if items:
            out.append(f"### {category}")
            out.append("")
            for item in items:
                out.append(f"- {item}")
            out.append("")

    return "\n".join(out)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Migrate Cursor / Windsurf / Copilot project memory to CLAUDE.md.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--repo", default=".", help="Repo root (default: cwd)")
    parser.add_argument("--source", help="Specific source file to convert (overrides auto-discover)")
    parser.add_argument("--output", default="CLAUDE.md", help="Output file (default: CLAUDE.md)")
    parser.add_argument("--stdout", action="store_true", help="Print to stdout instead of writing")
    parser.add_argument("--no-scaffold", action="store_true", help="Don't include [TODO] scaffolding for empty sections")
    parser.add_argument("--merge", action="store_true", help="Merge with existing CLAUDE.md instead of overwriting")
    parser.add_argument("--also-write-agents-md", action="store_true",
                        help="Also write AGENTS.md (minimal cross-vendor mirror)")
    parser.add_argument("--list-sources", action="store_true", help="List detected sources and exit")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        print(f"error: not a directory: {repo}", file=sys.stderr)
        return 2

    # Get sources
    if args.source:
        src_path = Path(args.source)
        if not src_path.is_file():
            print(f"error: source file not found: {src_path}", file=sys.stderr)
            return 2
        # Guess kind from name
        if src_path.name == ".cursorrules":
            kind = "cursorrules"
        elif src_path.name == ".windsurfrules":
            kind = "windsurf"
        elif "copilot" in src_path.name:
            kind = "copilot"
        elif src_path.suffix == ".mdc":
            kind = "cursor-mdc"
        else:
            kind = "unknown"
        sources = [Source(kind=kind, paths=[src_path], raw=src_path.read_text(errors="ignore"))]
    else:
        sources = discover_sources(repo)

    if args.list_sources:
        if not sources:
            print("No sources found.")
            return 0
        for s in sources:
            print(f"{s.kind}:")
            for p in s.paths:
                print(f"  {p}")
        return 0

    if not sources:
        print(f"No source files found in {repo}.", file=sys.stderr)
        print("Looked for: .cursorrules, .cursor/rules/*.mdc, .windsurfrules, .github/copilot-instructions.md, .aider.conf.yml", file=sys.stderr)
        return 1

    # Classify
    sections = Sections()
    for s in sources:
        rules = parse_rules(s.raw)
        partial = classify_all(rules)
        # Merge into combined
        for field_name in ("commands", "conventions", "restricted", "forbidden",
                           "invariants", "pointers", "cost_discipline", "misc",
                           "untranslatable"):
            getattr(sections, field_name).extend(getattr(partial, field_name))

    # Output
    output_path = repo / args.output
    if args.merge and output_path.is_file():
        existing = output_path.read_text()
        result = render_merge_with_existing(existing, sections)
    else:
        result = render_claude_md(sources, sections, repo, scaffold=not args.no_scaffold)

    if args.stdout:
        print(result)
    else:
        output_path.write_text(result)
        print(f"Wrote {output_path}", file=sys.stderr)

        if args.also_write_agents_md:
            agents_path = repo / "AGENTS.md"
            if agents_path.exists():
                print(f"Skipping AGENTS.md ({agents_path} already exists; remove it first to regenerate)", file=sys.stderr)
            else:
                agents_path.write_text(render_agents_md())
                print(f"Wrote {agents_path}", file=sys.stderr)

    # Summary
    print("", file=sys.stderr)
    print("Summary:", file=sys.stderr)
    print(f"  Sources: {len(sources)} file(s)", file=sys.stderr)
    total = sum(len(getattr(sections, f)) for f in ("commands", "conventions", "restricted",
                                                       "forbidden", "invariants", "pointers",
                                                       "cost_discipline", "misc"))
    print(f"  Rules migrated: {total}", file=sys.stderr)
    if sections.misc:
        print(f"  Unclassified (review needed): {len(sections.misc)}", file=sys.stderr)
    print("", file=sys.stderr)
    print("Next steps:", file=sys.stderr)
    print("  1. Read the generated CLAUDE.md — the classifier is heuristic; review every section.", file=sys.stderr)
    print("  2. Replace any [TODO] markers with content specific to your codebase.", file=sys.stderr)
    print("  3. Verify the verify command actually works.", file=sys.stderr)
    print("  4. If --also-write-agents-md was not used, create AGENTS.md as a cross-vendor mirror.", file=sys.stderr)
    print("  5. Run scripts/ai-readiness-audit.py to check the rest of the harness.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
