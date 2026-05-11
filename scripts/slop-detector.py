#!/usr/bin/env python3
"""
Slop Detector — heuristic checks for the seven slop signatures from Chapter 22
of "Software Engineering with AI" by Ryan Byrd.

This script analyzes a set of files (typically a git diff) and flags patterns
that match the seven slop signatures. It is heuristic. False positives are
expected; the goal is to raise things for human review, not to gate PRs
automatically.

Stdlib only. Python 3.9+.

The seven signatures from Ch 22:
  S1 — Imaginary APIs            (mostly: lint/typecheck catches these)
  S2 — Confidently wrong         (mostly: cannot detect statically)
  S3 — Repetitive boilerplate    (heuristic via duplicate n-grams)
  S4 — Vestigial code            (TODOs, dead branches, unused stuff)
  S5 — Tests that pass without testing  (no assertions, mock-only)
  S6 — Comment drift             (limited static detection)
  S7 — Scope creep               (diff-level: file count, size)

Plus two diff-level checks:
  D1 — PR size > 400 lines
  D2 — Code added without tests
  D3 — Missing AI authorship tag in PR description (when --pr-body provided)

This script is honest about what it cannot detect and explains why. It is a
companion to human review, not a substitute.

Usage:
    # Analyze a git diff vs HEAD~1
    slop-detector.py

    # Analyze a diff vs main
    slop-detector.py --base main

    # Analyze specific files (no git context)
    slop-detector.py --files src/foo.py tests/test_foo.py

    # JSON output for CI
    slop-detector.py --json

    # Set a severity threshold (exit 1 if any blocking findings)
    slop-detector.py --fail-on blocking

    # Pass PR body to check for AI authorship tag
    slop-detector.py --pr-body "$(cat pr-description.md)"
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, Optional

VERSION = "2026.q3"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    signature: str           # "S3", "S4", "D1", etc.
    severity: str            # "blocking", "major", "minor", "nit"
    file: str
    line: int                # 0 for diff-level findings
    snippet: str             # short excerpt, max ~80 chars
    message: str
    fix_hint: str = ""
    chapter_ref: str = "Ch 22"


SEVERITY_ORDER = {"blocking": 0, "major": 1, "minor": 2, "nit": 3}


# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------

CODE_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
             ".go", ".rs", ".java", ".kt", ".rb", ".cs"}
TEST_NAME_PATTERNS = (
    re.compile(r"^test_.*\.py$"),
    re.compile(r".*_test\.py$"),
    re.compile(r".*\.test\.[jt]sx?$"),
    re.compile(r".*\.spec\.[jt]sx?$"),
    re.compile(r".*Test\.java$"),
    re.compile(r".*_test\.go$"),
)


def is_code_file(path: Path) -> bool:
    return path.suffix in CODE_EXTS


def is_test_file(path: Path) -> bool:
    name = path.name
    return any(p.match(name) for p in TEST_NAME_PATTERNS) or "/tests/" in str(path) or "/test/" in str(path)


def read_text(path: Path) -> str:
    try:
        return path.read_text(errors="ignore")
    except OSError:
        return ""


def trim(s: str, n: int = 80) -> str:
    s = s.strip()
    return s if len(s) <= n else s[: n - 1] + "…"


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def git_diff_name_only(base: str, repo: Path) -> list[Path]:
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", base, "HEAD"],
            cwd=repo, text=True, stderr=subprocess.DEVNULL,
        )
        return [repo / line.strip() for line in out.splitlines() if line.strip()]
    except subprocess.CalledProcessError:
        return []


def git_diff_text(base: str, repo: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "diff", base, "HEAD", "--unified=0"],
            cwd=repo, text=True, stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return ""


# ---------------------------------------------------------------------------
# S3 — Repetitive boilerplate
# ---------------------------------------------------------------------------

def detect_s3_repetitive_boilerplate(file: Path, content: str) -> list[Finding]:
    """Detect duplicated 5+-line blocks within a file."""
    findings: list[Finding] = []
    lines = content.split("\n")
    if len(lines) < 10:
        return findings

    seen: dict[str, int] = {}
    for i in range(len(lines) - 4):
        block_lines = lines[i : i + 5]
        meaningful = [l.strip() for l in block_lines if l.strip() and len(l.strip()) > 8]
        if len(meaningful) < 4:
            continue  # mostly empty/short, skip
        # also skip blocks that are just imports
        if all(re.match(r"^\s*(import|from)\s", l) for l in block_lines if l.strip()):
            continue
        key = "\n".join(meaningful)
        prev = seen.get(key)
        if prev is not None and i - prev > 5:  # don't flag overlapping windows
            findings.append(Finding(
                signature="S3",
                severity="minor",
                file=str(file),
                line=i + 1,
                snippet=trim(lines[i]),
                message=f"Block of 5 lines duplicates lines {prev + 1}-{prev + 5}",
                fix_hint="Extract to a shared function, parametrized helper, or fixture.",
                chapter_ref="Ch 22 §22.3 (S3)",
            ))
            # don't re-flag the same duplicate further down
            seen[key] = i
        else:
            seen.setdefault(key, i)

    return findings


# ---------------------------------------------------------------------------
# S4 — Vestigial code
# ---------------------------------------------------------------------------

def detect_s4_vestigial_code(file: Path, content: str) -> list[Finding]:
    """TODO/FIXME, dead branches, leftover debug prints, etc."""
    findings: list[Finding] = []
    lines = content.split("\n")

    for i, line in enumerate(lines):
        stripped = line.strip()
        # skip blank lines fast
        if not stripped:
            continue

        # TODO / FIXME / XXX in comments
        if re.search(r"(?:#|//|/\*)\s*(TODO|FIXME|XXX|HACK)\b", line, re.I):
            findings.append(Finding(
                signature="S4",
                severity="minor",
                file=str(file),
                line=i + 1,
                snippet=trim(line),
                message="TODO/FIXME comment may indicate unfinished work or AI leaving notes",
                fix_hint="Resolve or convert to a tracked issue with a link.",
                chapter_ref="Ch 22 §22.4 (S4)",
            ))

        # if True: / if False: / if (true) { / if (false) {
        if re.search(r"\bif\s+(True|False)\b\s*:", line) or re.search(r"\bif\s*\(\s*(true|false)\s*\)", line):
            findings.append(Finding(
                signature="S4",
                severity="major",
                file=str(file),
                line=i + 1,
                snippet=trim(line),
                message="Constant-condition branch — dead code",
                fix_hint="Remove the dead branch or replace with the actual condition.",
                chapter_ref="Ch 22 §22.4 (S4)",
            ))

        # Trivially-tautological conditions
        if re.search(r"\b(\w+)\s*==\s*\1\b", line) and "==" in line:
            # rough heuristic: x == x
            findings.append(Finding(
                signature="S4",
                severity="major",
                file=str(file),
                line=i + 1,
                snippet=trim(line),
                message="Self-comparison (x == x) is always true",
                fix_hint="Likely a copy-paste or refactor error. Check the intended comparison.",
                chapter_ref="Ch 22 §22.4 (S4)",
            ))

        # Leftover prints/console.log in non-test files (heuristic — exclude logging.* calls)
        if not is_test_file(file):
            if re.search(r"^\s*print\s*\(", line) and file.suffix == ".py":
                # exclude obvious CLI tools (top-of-file scripts with __main__)
                if "__main__" not in content:
                    findings.append(Finding(
                        signature="S4",
                        severity="minor",
                        file=str(file),
                        line=i + 1,
                        snippet=trim(line),
                        message="`print()` in non-CLI code — possible debug leftover",
                        fix_hint="Use the logger or remove if debugging.",
                        chapter_ref="Ch 22 §22.4 (S4)",
                    ))
            if re.search(r"console\.(log|debug)\s*\(", line) and file.suffix in {".ts", ".tsx", ".js", ".jsx"}:
                findings.append(Finding(
                    signature="S4",
                    severity="minor",
                    file=str(file),
                    line=i + 1,
                    snippet=trim(line),
                    message="`console.log/debug` in code — likely debug leftover",
                    fix_hint="Use the logger or remove.",
                    chapter_ref="Ch 22 §22.4 (S4)",
                ))

    return findings


# ---------------------------------------------------------------------------
# S5 — Tests that pass without testing
# ---------------------------------------------------------------------------

def detect_s5_fake_tests(file: Path, content: str) -> list[Finding]:
    """Tests that don't actually verify anything."""
    findings: list[Finding] = []
    if not is_test_file(file):
        return findings

    lines = content.split("\n")

    # Trivially-true assertions
    for i, line in enumerate(lines):
        if re.search(r"\bassert\s+True\b", line):
            findings.append(Finding(
                signature="S5",
                severity="blocking",
                file=str(file),
                line=i + 1,
                snippet=trim(line),
                message="`assert True` — test always passes",
                fix_hint="Replace with an actual assertion on observable behavior.",
                chapter_ref="Ch 22 §22.5 (S5)",
            ))
        if re.search(r"\bassert\s+1\s*==\s*1\b", line):
            findings.append(Finding(
                signature="S5", severity="blocking",
                file=str(file), line=i + 1, snippet=trim(line),
                message="`assert 1 == 1` — test always passes",
                fix_hint="Replace with a real assertion.",
                chapter_ref="Ch 22 §22.5 (S5)",
            ))
        if re.search(r"expect\(\s*true\s*\)\.toBe\(\s*true\s*\)", line, re.I):
            findings.append(Finding(
                signature="S5", severity="blocking",
                file=str(file), line=i + 1, snippet=trim(line),
                message="`expect(true).toBe(true)` — test always passes",
                fix_hint="Replace with a real assertion.",
                chapter_ref="Ch 22 §22.5 (S5)",
            ))
        if re.search(r"expect\(\s*1\s*\)\.toBe\(\s*1\s*\)", line):
            findings.append(Finding(
                signature="S5", severity="blocking",
                file=str(file), line=i + 1, snippet=trim(line),
                message="`expect(1).toBe(1)` — test always passes",
                fix_hint="Replace with a real assertion.",
                chapter_ref="Ch 22 §22.5 (S5)",
            ))

    # Test functions with no assertions (Python only — most reliable to detect)
    if file.suffix == ".py":
        findings.extend(_find_python_tests_without_assertions(file, lines))

    # JS/TS test functions with no assertions (it/test blocks)
    if file.suffix in {".ts", ".tsx", ".js", ".jsx"}:
        findings.extend(_find_js_tests_without_assertions(file, content))

    return findings


_PY_TEST_DEF = re.compile(r"^(\s*)(?:async\s+)?def\s+(test_\w+)\s*\(")
_PY_ASSERTIONLIKE = re.compile(
    r"\b("
    r"assert\b|raises\b|pytest\.raises|self\.assert\w+|self\.fail|"
    r"approx|warns\("
    r")"
)


def _find_python_tests_without_assertions(file: Path, lines: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    in_test = False
    test_start = -1
    test_name = ""
    test_indent = -1
    has_assertion = False

    def flush() -> None:
        nonlocal in_test
        if in_test and not has_assertion:
            findings.append(Finding(
                signature="S5",
                severity="major",
                file=str(file),
                line=test_start + 1,
                snippet=f"def {test_name}",
                message=f"Test function `{test_name}` has no assertions",
                fix_hint="Add an assertion that verifies observable behavior.",
                chapter_ref="Ch 22 §22.5 (S5)",
            ))
        in_test = False

    for i, line in enumerate(lines):
        m = _PY_TEST_DEF.match(line)
        if m:
            flush()
            in_test = True
            test_start = i
            test_name = m.group(2)
            test_indent = len(m.group(1))
            has_assertion = False
            continue

        if in_test:
            stripped = line.lstrip()
            if not stripped:
                continue
            current_indent = len(line) - len(stripped)
            # Ended the function — back to <= test_indent and not blank
            if current_indent <= test_indent:
                flush()
                # also check this line as a possible new test
                m2 = _PY_TEST_DEF.match(line)
                if m2:
                    in_test = True
                    test_start = i
                    test_name = m2.group(2)
                    test_indent = len(m2.group(1))
                    has_assertion = False
                continue
            # Strip line comments so "# no assert here" doesn't fool us
            code_part = stripped.split("#", 1)[0]
            if _PY_ASSERTIONLIKE.search(code_part):
                has_assertion = True

    flush()
    return findings


def _find_js_tests_without_assertions(file: Path, content: str) -> list[Finding]:
    """Find `it("...", () => { ... })` and `test("...", () => { ... })` blocks
    that contain no `expect(`, `assert(`, or `chai.` calls.

    Uses brace-depth tracking; not a full JS parser, but catches the common case.
    """
    findings: list[Finding] = []
    block_re = re.compile(r"\b(it|test)\s*\(\s*['\"`]([^'\"`]+)['\"`]\s*,\s*(?:async\s*)?(?:function\s*\([^)]*\)\s*|\([^)]*\)\s*=>\s*)\{")
    lines = content.split("\n")
    line_starts = [0]
    for ln in lines:
        line_starts.append(line_starts[-1] + len(ln) + 1)

    def offset_to_line(off: int) -> int:
        # binary-search-like; small files so linear is fine
        for idx, start in enumerate(line_starts):
            if start > off:
                return idx
        return len(lines)

    for m in block_re.finditer(content):
        name = m.group(2)
        start = m.end() - 1  # at the `{`
        depth = 1
        i = start + 1
        while i < len(content) and depth > 0:
            c = content[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            i += 1
        body = content[start + 1 : i - 1]
        if not re.search(r"\b(expect|assert|chai|should)\s*[\.(]", body):
            findings.append(Finding(
                signature="S5",
                severity="major",
                file=str(file),
                line=offset_to_line(m.start()),
                snippet=trim(f"{m.group(1)}('{name}', ...)"),
                message=f"Test block `{name}` has no expect/assert calls",
                fix_hint="Add an expectation that verifies behavior.",
                chapter_ref="Ch 22 §22.5 (S5)",
            ))

    return findings


# ---------------------------------------------------------------------------
# S6 — Comment drift (limited; deep version requires AST + symbol tracking)
# ---------------------------------------------------------------------------

def detect_s6_comment_drift(file: Path, content: str) -> list[Finding]:
    """Limited static detection. The deep version requires symbol tracking
    across versions. Here we flag obvious red flags only:

    - Docstring/comment mentions a function or parameter name that does not
      exist in the surrounding scope (heuristic; many false positives).
    - Comment says "TODO: rename this" or similar self-aware drift markers.
    """
    findings: list[Finding] = []
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if re.search(r"(?:#|//|/\*).*\b(rename|refactor|move|deprecated|outdated)\b.*\bthis\b", line, re.I):
            findings.append(Finding(
                signature="S6",
                severity="nit",
                file=str(file),
                line=i + 1,
                snippet=trim(line),
                message="Comment self-identifies as outdated",
                fix_hint="Either do the work or convert to an issue with a link.",
                chapter_ref="Ch 22 §22.6 (S6)",
            ))
    return findings


# ---------------------------------------------------------------------------
# Diff-level: D1 (size), D2 (tests-with-code), D3 (AI authorship tag)
# ---------------------------------------------------------------------------

def detect_d1_pr_size(diff_text: str) -> list[Finding]:
    if not diff_text:
        return []
    added = sum(1 for line in diff_text.split("\n") if line.startswith("+") and not line.startswith("+++"))
    removed = sum(1 for line in diff_text.split("\n") if line.startswith("-") and not line.startswith("---"))
    total = added + removed
    if total <= 400:
        return []
    severity = "major" if total < 800 else "blocking"
    return [Finding(
        signature="D1",
        severity=severity,
        file="<diff>",
        line=0,
        snippet=f"+{added} / -{removed} = {total} lines",
        message=f"PR has {total} lines changed (over 400-line threshold)",
        fix_hint="Decompose into smaller PRs. Most agent-generated diffs are larger than they need to be.",
        chapter_ref="Ch 21, Ch 44 §44.5",
    )]


def detect_d2_test_ratio(changed_files: list[Path]) -> list[Finding]:
    code_files = [f for f in changed_files if is_code_file(f) and not is_test_file(f)]
    test_files = [f for f in changed_files if is_test_file(f)]
    if code_files and not test_files:
        return [Finding(
            signature="D2",
            severity="major",
            file="<diff>",
            line=0,
            snippet=f"{len(code_files)} code files, 0 test files",
            message="Code changed but no tests added or modified",
            fix_hint="Add tests or modify existing tests to cover the new behavior. If genuinely test-not-applicable (config, docs), note it in the PR description.",
            chapter_ref="Ch 8",
        )]
    return []


def detect_d3_ai_authorship_tag(pr_body: Optional[str]) -> list[Finding]:
    if pr_body is None:
        return []
    body_lower = pr_body.lower()
    tags = ["ai:none", "ai:assisted", "ai:authored", "ai:agent"]
    if any(tag in body_lower for tag in tags):
        return []
    return [Finding(
        signature="D3",
        severity="minor",
        file="<pr-body>",
        line=0,
        snippet="(none of the four tags found)",
        message="PR body does not include an AI authorship tag",
        fix_hint="Add one of: ai:none / ai:assisted / ai:authored / ai:agent (Ch 31 §31.6).",
        chapter_ref="Ch 31 §31.6",
    )]


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def analyze_files(files: Iterable[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for f in files:
        if not f.is_file() or not is_code_file(f):
            continue
        content = read_text(f)
        if not content:
            continue
        findings.extend(detect_s3_repetitive_boilerplate(f, content))
        findings.extend(detect_s4_vestigial_code(f, content))
        findings.extend(detect_s5_fake_tests(f, content))
        findings.extend(detect_s6_comment_drift(f, content))
    return findings


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

SIG_LABELS = {
    "S1": "Imaginary APIs",
    "S2": "Confidently wrong",
    "S3": "Repetitive boilerplate",
    "S4": "Vestigial code",
    "S5": "Tests pass without testing",
    "S6": "Comment drift",
    "S7": "Scope creep",
    "D1": "PR size",
    "D2": "Code without tests",
    "D3": "AI authorship tag",
}


def render_text(findings: list[Finding], scope_desc: str) -> str:
    lines = [f"Slop Detector  —  {scope_desc}", "=" * 72]
    if not findings:
        lines.append("No findings. (Heuristic — false negatives are still possible.)")
        return "\n".join(lines)

    by_sev: dict[str, list[Finding]] = {"blocking": [], "major": [], "minor": [], "nit": []}
    for f in findings:
        by_sev[f.severity].append(f)

    counts = "  ".join(f"{s}: {len(by_sev[s])}" for s in ["blocking", "major", "minor", "nit"])
    lines.append(f"Findings: {len(findings)}    [{counts}]")
    lines.append("")

    sig_counts: dict[str, int] = {}
    for f in findings:
        sig_counts[f.signature] = sig_counts.get(f.signature, 0) + 1
    lines.append("By signature:")
    for sig in sorted(sig_counts, key=lambda s: (s[0], int(s[1:]) if s[1:].isdigit() else 99)):
        lines.append(f"  {sig} ({SIG_LABELS.get(sig, sig)}): {sig_counts[sig]}")
    lines.append("")

    for sev in ["blocking", "major", "minor", "nit"]:
        if not by_sev[sev]:
            continue
        lines.append(f"--- {sev.upper()} ---")
        for f in sorted(by_sev[sev], key=lambda f: (f.file, f.line)):
            loc = f"{f.file}:{f.line}" if f.line else f.file
            lines.append(f"  [{f.signature}] {loc}")
            lines.append(f"      {f.message}")
            if f.snippet:
                lines.append(f"      > {f.snippet}")
            if f.fix_hint:
                lines.append(f"      → {f.fix_hint}")
            lines.append(f"      ({f.chapter_ref})")
        lines.append("")

    lines.append("This script is heuristic and limited:")
    lines.append("  · S1 (imaginary APIs) is best caught by typecheck/lint, not this script.")
    lines.append("  · S2 (confidently wrong) cannot be detected statically — that's the human's job.")
    lines.append("  · S6 (comment drift, deep version) requires symbol tracking across versions.")
    lines.append("  · S7 (scope creep) needs a PR description for ground truth on intended scope.")
    return "\n".join(lines)


def render_json(findings: list[Finding], scope_desc: str) -> str:
    return json.dumps({
        "version": VERSION,
        "scope": scope_desc,
        "findings": [asdict(f) for f in findings],
        "counts": {
            sev: sum(1 for f in findings if f.severity == sev)
            for sev in ("blocking", "major", "minor", "nit")
        },
    }, indent=2)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Heuristic slop detector for the seven slop signatures from Ch 22.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--base", default=None, help="Git base ref (default: HEAD~1 if in a git repo)")
    g.add_argument("--files", nargs="+", help="Specific files to analyze (skip git)")
    parser.add_argument("--repo", default=".", help="Repo root (default: cwd)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--pr-body", default=None, help="PR description text (for AI-tag check)")
    parser.add_argument("--fail-on", choices=["blocking", "major", "minor", "nit"], default=None,
                        help="Exit non-zero if any finding at or above this severity")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()

    findings: list[Finding] = []

    if args.files:
        files = [Path(f).resolve() for f in args.files]
        scope_desc = f"{len(files)} files"
        findings.extend(analyze_files(files))
        # diff-level checks require git context; only D2 (test ratio) makes sense here.
        findings.extend(detect_d2_test_ratio(files))
    else:
        base = args.base or "HEAD~1"
        changed = git_diff_name_only(base, repo)
        if not changed:
            print(f"No changes detected vs {base} (or not a git repo).", file=sys.stderr)
            return 0
        scope_desc = f"diff vs {base} — {len(changed)} files"
        findings.extend(analyze_files(changed))
        findings.extend(detect_d1_pr_size(git_diff_text(base, repo)))
        findings.extend(detect_d2_test_ratio(changed))

    findings.extend(detect_d3_ai_authorship_tag(args.pr_body))

    # Sort: severity, then file, then line
    findings.sort(key=lambda f: (SEVERITY_ORDER[f.severity], f.file, f.line))

    if args.json:
        print(render_json(findings, scope_desc))
    else:
        print(render_text(findings, scope_desc))

    if args.fail_on:
        threshold = SEVERITY_ORDER[args.fail_on]
        if any(SEVERITY_ORDER[f.severity] <= threshold for f in findings):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
