#!/usr/bin/env python3
"""
AI Readiness Audit — companion to "Software Engineering with AI: A Practical
Handbook for the Claude Code Era" by Ryan Byrd.

Scores a repository against ~25 criteria from the book and produces an HTML
report (or JSON) with concrete next actions and chapter references.

Stdlib only. Python 3.9+.

Usage:
    python3 ai-readiness-audit.py /path/to/repo
    python3 ai-readiness-audit.py /path/to/repo -o report.html
    python3 ai-readiness-audit.py /path/to/repo --json
    python3 ai-readiness-audit.py /path/to/repo --threshold 60   # exit 1 if below
"""

import argparse
import datetime
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from html import escape
from pathlib import Path
from typing import Callable, List, Optional

VERSION = "2026.q3"
BOOK_TITLE = "Software Engineering with AI: A Practical Handbook for the Claude Code Era"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class CheckResult:
    name: str
    category: str
    chapter_ref: str
    description: str
    weight: int          # 1 = nice to have, 2 = important, 3 = critical
    status: str          # "pass" | "warn" | "fail"
    details: str = ""
    fix: str = ""

    @property
    def score(self) -> float:
        return self.weight * {"pass": 1.0, "warn": 0.5, "fail": 0.0}[self.status]


# ---------------------------------------------------------------------------
# Filesystem helpers
# ---------------------------------------------------------------------------

def find_first(repo: Path, *names: str) -> Optional[Path]:
    """Return the first existing path among names (case-insensitive at root)."""
    lower_to_actual = {p.name.lower(): p for p in repo.iterdir() if not p.name.startswith(".")} if repo.is_dir() else {}
    # also look at hidden ones explicitly for things like .github
    hidden = {p.name.lower(): p for p in repo.iterdir() if p.name.startswith(".")} if repo.is_dir() else {}
    lower_to_actual.update(hidden)
    for name in names:
        p = repo / name
        if p.exists():
            return p
        actual = lower_to_actual.get(name.lower())
        if actual:
            return actual
    return None


def has_content(p: Optional[Path], min_chars: int = 50) -> bool:
    if not p or not p.is_file():
        return False
    try:
        return len(p.read_text(errors="ignore")) >= min_chars
    except Exception:
        return False


def read(p: Optional[Path]) -> str:
    if not p or not p.is_file():
        return ""
    try:
        return p.read_text(errors="ignore")
    except Exception:
        return ""


def find_glob(repo: Path, pattern: str, max_depth: int = 3) -> List[Path]:
    """Find files matching a glob, limited to max_depth to avoid node_modules etc."""
    results = []
    skip_dirs = {"node_modules", ".git", "dist", "build", ".next", "target",
                 ".venv", "venv", "__pycache__", ".pytest_cache", ".cache"}
    for root, dirs, files in os.walk(repo):
        # prune
        depth = len(Path(root).relative_to(repo).parts)
        if depth >= max_depth:
            dirs.clear()
            continue
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            from fnmatch import fnmatch
            if fnmatch(f, pattern):
                results.append(Path(root) / f)
    return results


def detect_stack(repo: Path) -> List[str]:
    """Detect what stack(s) the repo uses. Affects which checks apply."""
    stacks = []
    if (repo / "package.json").exists():
        stacks.append("javascript")
    if (repo / "tsconfig.json").exists() or list(repo.glob("**/tsconfig*.json"))[:1]:
        stacks.append("typescript")
    if (repo / "pyproject.toml").exists() or (repo / "setup.py").exists() or (repo / "requirements.txt").exists():
        stacks.append("python")
    if (repo / "go.mod").exists():
        stacks.append("go")
    if (repo / "Cargo.toml").exists():
        stacks.append("rust")
    if (repo / "pom.xml").exists() or (repo / "build.gradle").exists() or (repo / "build.gradle.kts").exists():
        stacks.append("java")
    return stacks or ["unknown"]


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_claude_md(repo: Path) -> CheckResult:
    p = find_first(repo, "CLAUDE.md")
    base = dict(name="CLAUDE.md exists at repo root",
                category="Repo legibility",
                chapter_ref="Ch 6, Appendix A",
                description="Project memory file for Claude Code with conventions, commands, and architectural invariants.",
                weight=3)
    if has_content(p, 200):
        return CheckResult(**base, status="pass",
                           details=f"Found ({p.stat().st_size} bytes)")
    if has_content(p, 50):
        return CheckResult(**base, status="warn",
                           details="Exists but minimal content. Should include: commands, conventions, restricted areas, architecture invariants, forbidden patterns.",
                           fix="Expand CLAUDE.md to cover commands, conventions, restricted areas. See templates/CLAUDE.md.")
    return CheckResult(**base, status="fail",
                       fix="Create CLAUDE.md at repo root. Copy templates/CLAUDE.md as a starting point.")


def check_agents_md(repo: Path) -> CheckResult:
    p = find_first(repo, "AGENTS.md")
    base = dict(name="AGENTS.md exists (cross-vendor agent guidance)",
                category="Repo legibility",
                chapter_ref="Ch 6, Appendix B",
                description="Cross-vendor agent guidance file. Recognized by Claude Code, Cursor, Codex, and others.",
                weight=2)
    if has_content(p, 100):
        return CheckResult(**base, status="pass", details=f"Found ({p.stat().st_size} bytes)")
    return CheckResult(**base, status="fail",
                       fix="Create AGENTS.md at repo root. See templates/AGENTS.md. Can mostly mirror CLAUDE.md content.")


def check_llms_txt(repo: Path) -> CheckResult:
    p = find_first(repo, "llms.txt")
    base = dict(name="llms.txt exists (repo route map)",
                category="Repo legibility",
                chapter_ref="Ch 6 §6.5.3",
                description="Plain-text route map of the repo for agents to find their way around.",
                weight=1)
    if has_content(p, 50):
        return CheckResult(**base, status="pass")
    return CheckResult(**base, status="warn",
                       fix="Run scripts/llms-txt-generator.py to generate llms.txt. Optional but recommended for monorepos.")


def check_readme(repo: Path) -> CheckResult:
    p = find_first(repo, "README.md", "README.rst", "README", "README.txt")
    base = dict(name="README.md exists",
                category="Repo legibility",
                chapter_ref="Ch 6 §6.4",
                description="Human-and-agent-readable project overview.",
                weight=2)
    if has_content(p, 200):
        return CheckResult(**base, status="pass")
    return CheckResult(**base, status="fail",
                       fix="Create a README.md describing what the repo is, how to install, how to run, how to test.")


def check_per_package_readmes(repo: Path) -> CheckResult:
    base = dict(name="Per-package READMEs in monorepos",
                category="Repo legibility",
                chapter_ref="Ch 10, Ch 12",
                description="In monorepos, each package/service should have its own README or AGENTS.md.",
                weight=1)
    pkg_dirs = []
    for parent in ("packages", "services", "apps", "libs", "modules"):
        d = repo / parent
        if d.is_dir():
            pkg_dirs.extend([p for p in d.iterdir() if p.is_dir() and not p.name.startswith(".")])
    if not pkg_dirs:
        return CheckResult(**base, status="pass", details="Not a monorepo (no packages/services/apps/libs).")
    with_readme = [p for p in pkg_dirs if (p / "README.md").exists() or (p / "AGENTS.md").exists()]
    ratio = len(with_readme) / len(pkg_dirs)
    if ratio >= 0.8:
        return CheckResult(**base, status="pass",
                           details=f"{len(with_readme)}/{len(pkg_dirs)} packages have a README or AGENTS.md.")
    if ratio >= 0.4:
        return CheckResult(**base, status="warn",
                           details=f"Only {len(with_readme)}/{len(pkg_dirs)} packages documented.",
                           fix="Add README.md or AGENTS.md to each package describing its purpose and entry points.")
    return CheckResult(**base, status="fail",
                       details=f"Only {len(with_readme)}/{len(pkg_dirs)} packages documented.",
                       fix="Add README.md or AGENTS.md to each package describing its purpose and entry points.")


def check_verify_command(repo: Path) -> CheckResult:
    base = dict(name="`verify` command defined",
                category="Verify command",
                chapter_ref="Ch 7",
                description="A single `verify` command that runs lint + typecheck + format + tests. The most important artifact in the harness.",
                weight=3)
    pkg = repo / "package.json"
    makefile = repo / "Makefile"
    verify_sh = (repo / "scripts" / "verify.sh") if (repo / "scripts" / "verify.sh").exists() else None
    pyproject = repo / "pyproject.toml"

    found = []
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text())
            scripts = data.get("scripts", {})
            if "verify" in scripts:
                found.append(f"package.json scripts.verify: `{scripts['verify']}`")
        except Exception:
            pass
    if makefile.exists():
        text = makefile.read_text(errors="ignore")
        if re.search(r"^verify\s*:", text, re.M):
            found.append("Makefile target `verify`")
    if verify_sh:
        found.append("scripts/verify.sh")
    if pyproject.exists():
        text = pyproject.read_text(errors="ignore")
        if "verify" in text.lower():
            found.append("pyproject.toml mentions verify")

    if found:
        return CheckResult(**base, status="pass", details="; ".join(found))
    return CheckResult(**base, status="fail",
                       fix="Define a `verify` script that runs lint, typecheck/format, and tests. "
                           "Add `\"verify\": \"npm run lint && npm run typecheck && npm test\"` to package.json scripts, "
                           "or a `verify:` target to Makefile.")


def _scripts_text(repo: Path) -> str:
    """Concatenate likely places to find verify-related commands."""
    parts = []
    for p in [repo / "package.json", repo / "Makefile", repo / "pyproject.toml",
              repo / "scripts" / "verify.sh", repo / "Taskfile.yml", repo / ".github" / "workflows"]:
        if p.is_file():
            parts.append(p.read_text(errors="ignore"))
        elif p.is_dir():
            for f in p.iterdir():
                if f.is_file():
                    parts.append(f.read_text(errors="ignore"))
    return "\n".join(parts).lower()


def check_verify_includes_lint(repo: Path) -> CheckResult:
    base = dict(name="Verify pipeline includes lint",
                category="Verify command",
                chapter_ref="Ch 7",
                description="Linting catches a class of slop that verify-without-lint misses.",
                weight=2)
    text = _scripts_text(repo)
    indicators = ["eslint", "ruff", "flake8", "pylint", "golangci-lint", "rubocop", "lint", "checkstyle"]
    if any(i in text for i in indicators):
        return CheckResult(**base, status="pass")
    return CheckResult(**base, status="fail",
                       fix="Add a linter (eslint, ruff, golangci-lint, etc.) to your verify pipeline.")


def check_verify_includes_typecheck(repo: Path) -> CheckResult:
    base = dict(name="Verify pipeline includes typecheck/format",
                category="Verify command",
                chapter_ref="Ch 7",
                description="Type checking and format checking are deterministic gates that catch obvious mistakes.",
                weight=2)
    text = _scripts_text(repo)
    indicators = ["tsc", "typecheck", "type-check", "mypy", "pyright", "prettier", "black", "ruff format", "gofmt"]
    if any(i in text for i in indicators):
        return CheckResult(**base, status="pass")
    return CheckResult(**base, status="warn",
                       fix="Add typecheck (tsc/mypy/pyright) and/or format check (prettier/black) to verify.")


def check_verify_includes_tests(repo: Path) -> CheckResult:
    base = dict(name="Verify pipeline includes tests",
                category="Verify command",
                chapter_ref="Ch 7",
                description="The verify command must run tests. Otherwise it's not a verification.",
                weight=3)
    text = _scripts_text(repo)
    indicators = ["jest", "vitest", "mocha", "pytest", "go test", "cargo test", "rspec", "junit", "npm test", "yarn test", "pnpm test"]
    if any(i in text for i in indicators):
        return CheckResult(**base, status="pass")
    return CheckResult(**base, status="fail",
                       fix="Wire your test runner into verify (npm test / pytest / go test / etc.).")


def check_tests_directory(repo: Path) -> CheckResult:
    base = dict(name="Test files exist",
                category="Test discipline",
                chapter_ref="Ch 8",
                description="Tests are how the harness keeps AI changes safe.",
                weight=3)
    test_files = []
    for pattern in ["*test*.py", "*_test.go", "*.test.ts", "*.test.tsx", "*.test.js", "*.spec.ts", "*.spec.js", "*Test.java"]:
        test_files.extend(find_glob(repo, pattern, max_depth=5))
    if len(test_files) >= 5:
        return CheckResult(**base, status="pass", details=f"Found {len(test_files)} test files.")
    if len(test_files) >= 1:
        return CheckResult(**base, status="warn", details=f"Only {len(test_files)} test file(s).",
                           fix="Add more tests. The verify command needs something real to verify.")
    return CheckResult(**base, status="fail",
                       fix="Add tests. Without tests, AI changes go in unverified.")


def check_ci_workflow(repo: Path) -> CheckResult:
    base = dict(name="CI workflow exists",
                category="Test discipline",
                chapter_ref="Ch 8",
                description="CI runs verify on every PR. Otherwise verify is just a local convention.",
                weight=2)
    workflows = [
        repo / ".github" / "workflows",
        repo / ".gitlab-ci.yml",
        repo / "Jenkinsfile",
        repo / ".circleci" / "config.yml",
        repo / "azure-pipelines.yml",
    ]
    for w in workflows:
        if w.exists():
            if w.is_dir() and any(w.iterdir()):
                return CheckResult(**base, status="pass", details=f"{w.relative_to(repo)} present")
            if w.is_file():
                return CheckResult(**base, status="pass", details=f"{w.relative_to(repo)} present")
    return CheckResult(**base, status="fail",
                       fix="Add a CI workflow (.github/workflows/verify.yml) that runs `verify` on every PR.")


def check_claude_dir(repo: Path) -> CheckResult:
    p = repo / ".claude"
    base = dict(name=".claude/ directory exists",
                category="Harness",
                chapter_ref="Ch 13-15",
                description="The harness lives here: skills, hooks, subagents, settings.",
                weight=3)
    if p.is_dir():
        return CheckResult(**base, status="pass")
    return CheckResult(**base, status="fail",
                       fix="Create .claude/ directory with skills/, agents/, hooks/, and settings.json.")


def check_skills(repo: Path) -> CheckResult:
    base = dict(name="At least one skill defined",
                category="Harness",
                chapter_ref="Ch 13, Appendix E",
                description="Skills are reusable playbooks for repeated tasks. Start with 3-5; grow to 12.",
                weight=3)
    skills_dir = repo / ".claude" / "skills"
    if not skills_dir.is_dir():
        return CheckResult(**base, status="fail",
                           fix="Create .claude/skills/ and add at least one skill (see skills/ in companion repo).")
    skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
    if len(skill_dirs) >= 5:
        return CheckResult(**base, status="pass", details=f"{len(skill_dirs)} skills defined.")
    if len(skill_dirs) >= 1:
        return CheckResult(**base, status="warn", details=f"{len(skill_dirs)} skill(s) — aim for 5-12.",
                           fix="Add more skills covering common tasks: code-review, write-tests, refactor-safely, db-migration.")
    return CheckResult(**base, status="fail",
                       fix="Define at least one skill in .claude/skills/<name>/SKILL.md.")


def check_subagents(repo: Path) -> CheckResult:
    base = dict(name="Subagents defined",
                category="Harness",
                chapter_ref="Ch 14, Appendix F",
                description="Standard subagent roster: planner, implementer, reviewer.",
                weight=2)
    agents_dir = repo / ".claude" / "agents"
    if not agents_dir.is_dir():
        return CheckResult(**base, status="fail",
                           fix="Create .claude/agents/ with at least planner.md, reviewer.md, implementer.md.")
    agent_files = list(agents_dir.glob("*.md"))
    if len(agent_files) >= 3:
        return CheckResult(**base, status="pass", details=f"{len(agent_files)} subagents defined.")
    if len(agent_files) >= 1:
        return CheckResult(**base, status="warn", details=f"{len(agent_files)} subagent(s) — aim for 3+.")
    return CheckResult(**base, status="fail",
                       fix="Add subagent definitions to .claude/agents/.")


def check_hooks(repo: Path) -> CheckResult:
    base = dict(name="Hooks configured",
                category="Harness",
                chapter_ref="Ch 15, Appendix G",
                description="Hooks are deterministic enforcement: bash firewall, protected paths, etc.",
                weight=3)
    settings = repo / ".claude" / "settings.json"
    hooks_dir = repo / ".claude" / "hooks"
    has_settings_hooks = False
    if settings.is_file():
        try:
            data = json.loads(settings.read_text())
            has_settings_hooks = bool(data.get("hooks"))
        except Exception:
            pass
    has_hook_scripts = hooks_dir.is_dir() and any(hooks_dir.iterdir())
    if has_settings_hooks and has_hook_scripts:
        return CheckResult(**base, status="pass", details="Settings reference hooks and hook scripts present.")
    if has_settings_hooks or has_hook_scripts:
        return CheckResult(**base, status="warn",
                           fix="Wire .claude/settings.json hooks block to point at .claude/hooks/*.sh scripts.")
    return CheckResult(**base, status="fail",
                       fix="Add at least bash-firewall.sh and protected-paths.sh hooks. See hooks/ in companion repo.")


def check_pr_template(repo: Path) -> CheckResult:
    base = dict(name="PR template exists",
                category="PR discipline",
                chapter_ref="Ch 21, Appendix D",
                description="PR template enforces verification checklist and AI authorship disclosure.",
                weight=2)
    candidates = [
        repo / ".github" / "pull_request_template.md",
        repo / ".github" / "PULL_REQUEST_TEMPLATE.md",
        repo / "PULL_REQUEST_TEMPLATE.md",
        repo / "docs" / "pull_request_template.md",
    ]
    found = next((p for p in candidates if p.exists()), None)
    if has_content(found, 50):
        return CheckResult(**base, status="pass")
    return CheckResult(**base, status="fail",
                       fix="Create .github/pull_request_template.md. See templates/pr-template.md in companion repo.")


def check_pr_template_mentions_ai(repo: Path) -> CheckResult:
    base = dict(name="PR template mentions AI authorship",
                category="PR discipline",
                chapter_ref="Ch 21, Ch 31 §31.6",
                description="PRs should be tagged ai:none / ai:assisted / ai:authored / ai:agent for attribution and measurement.",
                weight=2)
    candidates = [
        repo / ".github" / "pull_request_template.md",
        repo / ".github" / "PULL_REQUEST_TEMPLATE.md",
        repo / "PULL_REQUEST_TEMPLATE.md",
    ]
    found = next((p for p in candidates if p.exists()), None)
    text = read(found).lower()
    if any(tag in text for tag in ["ai:authored", "ai:assisted", "ai-authored", "ai authorship", "ai-assisted"]):
        return CheckResult(**base, status="pass")
    if "ai" in text and ("review" in text or "tag" in text):
        return CheckResult(**base, status="warn",
                           fix="Make AI authorship explicit. Add the four tags from Ch 31 §31.6.")
    return CheckResult(**base, status="fail",
                       fix="Add AI authorship tags to PR template (ai:none / ai:assisted / ai:authored / ai:agent).")


def check_codeowners(repo: Path) -> CheckResult:
    base = dict(name="CODEOWNERS file exists",
                category="PR discipline",
                chapter_ref="Ch 21",
                description="CODEOWNERS routes reviews to the right humans and gates restricted areas.",
                weight=1)
    candidates = [
        repo / ".github" / "CODEOWNERS",
        repo / "CODEOWNERS",
        repo / "docs" / "CODEOWNERS",
    ]
    found = next((p for p in candidates if p.exists()), None)
    if has_content(found, 20):
        return CheckResult(**base, status="pass")
    return CheckResult(**base, status="warn",
                       fix="Add CODEOWNERS to enforce review routing on sensitive paths.")


def check_security_md(repo: Path) -> CheckResult:
    base = dict(name="SECURITY.md exists",
                category="Governance",
                chapter_ref="Ch 30",
                description="Security policy. Should include AI tooling disclosure for customer audits.",
                weight=2)
    p = find_first(repo, "SECURITY.md")
    if has_content(p, 100):
        return CheckResult(**base, status="pass")
    return CheckResult(**base, status="fail",
                       fix="Create SECURITY.md. Include AI tooling disclosure (see exec-kit/security-questionnaire-answers.md).")


def check_forbidden_listed(repo: Path) -> CheckResult:
    base = dict(name="Forbidden patterns listed in CLAUDE.md",
                category="Governance",
                chapter_ref="Ch 6, Ch 33",
                description="Explicit list of what the agent must never do (production credentials, eval, etc.).",
                weight=2)
    text = read(find_first(repo, "CLAUDE.md")).lower()
    indicators = ["forbidden", "must not", "never", "do not", "restricted"]
    matches = sum(1 for i in indicators if i in text)
    if matches >= 2:
        return CheckResult(**base, status="pass")
    if matches >= 1:
        return CheckResult(**base, status="warn",
                           fix="Expand the forbidden / restricted section in CLAUDE.md.")
    return CheckResult(**base, status="fail",
                       fix="Add explicit Forbidden / Restricted sections to CLAUDE.md (see templates/CLAUDE.md).")


def check_invariants_documented(repo: Path) -> CheckResult:
    base = dict(name="Architectural invariants documented",
                category="Governance",
                chapter_ref="Ch 9",
                description="Hard invariants the agent must respect (UI cannot import from db, all auth server-side, etc.).",
                weight=2)
    text = read(find_first(repo, "CLAUDE.md")).lower() + " " + read(find_first(repo, "AGENTS.md")).lower()
    indicators = ["invariant", "must not import", "boundary", "architecture", "never deletes", "idempotent"]
    matches = sum(1 for i in indicators if i in text)
    if matches >= 2:
        return CheckResult(**base, status="pass")
    if matches >= 1:
        return CheckResult(**base, status="warn",
                           fix="Document at least 3 architectural invariants explicitly.")
    return CheckResult(**base, status="fail",
                       fix="Add an 'Architecture invariants' section to CLAUDE.md.")


def check_cost_telemetry_referenced(repo: Path) -> CheckResult:
    base = dict(name="Cost telemetry / token tracking referenced",
                category="Cost & observability",
                chapter_ref="Ch 26, Ch 29",
                description="Reference to cost gateway, LiteLLM, Bifrost, Helicone, or token-budget mechanism.",
                weight=1)
    paths_to_check = [
        find_first(repo, "CLAUDE.md"),
        find_first(repo, "AGENTS.md"),
        find_first(repo, "README.md"),
        find_first(repo, "docs"),
    ]
    text = ""
    for p in paths_to_check:
        if p and p.is_file():
            text += read(p).lower()
        elif p and p.is_dir():
            for f in p.glob("*.md"):
                text += read(f).lower()
    indicators = ["litellm", "bifrost", "helicone", "token budget", "cost gateway", "token spend", "cost dashboard"]
    if any(i in text for i in indicators):
        return CheckResult(**base, status="pass")
    return CheckResult(**base, status="warn",
                       fix="Document the cost gateway / token-tracking mechanism in CLAUDE.md or docs/.")


def check_data_classification(repo: Path) -> CheckResult:
    base = dict(name="Data classification policy referenced",
                category="Governance",
                chapter_ref="Ch 34",
                description="Data classification matrix mapping data types to AI tool permissions.",
                weight=2)
    paths = [find_first(repo, "CLAUDE.md"), find_first(repo, "SECURITY.md"),
             find_first(repo, "docs"), find_first(repo, "governance")]
    text = ""
    for p in paths:
        if p and p.is_file():
            text += read(p).lower()
        elif p and p.is_dir():
            for f in p.rglob("*.md"):
                text += read(f).lower()
    indicators = ["data classification", "data class", "pii", "phi", "customer data", "regulated"]
    matches = sum(1 for i in indicators if i in text)
    if matches >= 2:
        return CheckResult(**base, status="pass")
    if matches >= 1:
        return CheckResult(**base, status="warn",
                           fix="Add a data classification matrix (see exec-kit/data-classification-matrix).")
    return CheckResult(**base, status="fail",
                       fix="Document data classification (public / internal / confidential / customer / regulated) and which AI tools can touch each.")


def check_incident_runbook(repo: Path) -> CheckResult:
    base = dict(name="AI-aware incident response runbook",
                category="Governance",
                chapter_ref="Ch 39",
                description="Postmortem / IR runbook that handles AI-authored code paths.",
                weight=1)
    paths = []
    for d in [repo / "docs", repo / "runbooks", repo / "governance", repo / ".github"]:
        if d.is_dir():
            paths.extend(d.rglob("*.md"))
    text = ""
    for p in paths:
        text += read(p).lower()
    indicators = ["postmortem", "incident", "runbook", "rca"]
    ai_indicators = ["ai", "agent", "claude"]
    has_ir = any(i in text for i in indicators)
    has_ai = any(i in text for i in ai_indicators)
    if has_ir and has_ai:
        return CheckResult(**base, status="pass")
    if has_ir:
        return CheckResult(**base, status="warn",
                           fix="Update postmortem template to include AI-authored-code path (see governance/ in companion repo).")
    return CheckResult(**base, status="fail",
                       fix="Add an incident response runbook with AI-aware procedures.")


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

ALL_CHECKS: List[Callable[[Path], CheckResult]] = [
    check_claude_md,
    check_agents_md,
    check_llms_txt,
    check_readme,
    check_per_package_readmes,
    check_verify_command,
    check_verify_includes_lint,
    check_verify_includes_typecheck,
    check_verify_includes_tests,
    check_tests_directory,
    check_ci_workflow,
    check_claude_dir,
    check_skills,
    check_subagents,
    check_hooks,
    check_pr_template,
    check_pr_template_mentions_ai,
    check_codeowners,
    check_security_md,
    check_forbidden_listed,
    check_invariants_documented,
    check_cost_telemetry_referenced,
    check_data_classification,
    check_incident_runbook,
]


def run_audit(repo: Path) -> List[CheckResult]:
    return [c(repo) for c in ALL_CHECKS]


def category_summary(results: List[CheckResult]) -> dict:
    summary = {}
    for r in results:
        s = summary.setdefault(r.category, {"score": 0.0, "max": 0, "checks": 0,
                                            "pass": 0, "warn": 0, "fail": 0,
                                            "chapter_ref": r.chapter_ref})
        s["score"] += r.score
        s["max"] += r.weight
        s["checks"] += 1
        s[r.status] += 1
    return summary


def overall_score(results: List[CheckResult]) -> tuple:
    score = sum(r.score for r in results)
    max_score = sum(r.weight for r in results)
    return score, max_score


def top_actions(results: List[CheckResult], n: int = 5) -> List[CheckResult]:
    """The N most-impactful failing or warning checks, sorted by weight."""
    needs_action = [r for r in results if r.status in ("fail", "warn") and r.fix]
    return sorted(needs_action, key=lambda r: (-r.weight, r.status != "fail"))[:n]


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

STATUS_BADGE = {"pass": "✅ PASS", "warn": "⚠️ WARN", "fail": "❌ FAIL"}
STATUS_COLOR = {"pass": "#1a7f37", "warn": "#9a6700", "fail": "#cf222e"}
STATUS_BG = {"pass": "#dafbe1", "warn": "#fff8c5", "fail": "#ffebe9"}


def render_text(repo: Path, results: List[CheckResult]) -> str:
    lines = []
    score, max_score = overall_score(results)
    pct = 100 * score / max_score if max_score else 0
    lines.append(f"AI Readiness Audit  —  {repo}")
    lines.append(f"Audit version: {VERSION}    Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 72)
    lines.append(f"Score: {score:.1f} / {max_score}  ({pct:.0f}%)")
    lines.append("")
    summary = category_summary(results)
    for cat, s in summary.items():
        cat_pct = 100 * s["score"] / s["max"] if s["max"] else 0
        bars = int(cat_pct / 10)
        bar = "▓" * bars + "░" * (10 - bars)
        emoji = "✅" if cat_pct >= 80 else ("⚠️ " if cat_pct >= 50 else "❌")
        lines.append(f"  {cat:30s} {bar} {s['score']:.1f}/{s['max']:>3}  {emoji}")
    lines.append("")
    lines.append(f"Top {min(5, len(results))} things to do this week:")
    for i, r in enumerate(top_actions(results, 5), 1):
        lines.append(f"  {i}. {r.name}    ({r.chapter_ref})")
        lines.append(f"     → {r.fix}")
    lines.append("")
    lines.append("Detailed results:")
    for r in results:
        lines.append(f"  [{STATUS_BADGE[r.status]}] {r.name}  ({r.chapter_ref})")
        if r.details:
            lines.append(f"           {r.details}")
        if r.fix and r.status != "pass":
            lines.append(f"           → {r.fix}")
    return "\n".join(lines)


def render_html(repo: Path, results: List[CheckResult]) -> str:
    score, max_score = overall_score(results)
    pct = 100 * score / max_score if max_score else 0
    summary = category_summary(results)
    actions = top_actions(results, 5)
    generated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    stack = ", ".join(detect_stack(repo))

    overall_color = "#1a7f37" if pct >= 80 else ("#9a6700" if pct >= 50 else "#cf222e")

    cat_rows = ""
    for cat, s in summary.items():
        cat_pct = 100 * s["score"] / s["max"] if s["max"] else 0
        cat_color = "#1a7f37" if cat_pct >= 80 else ("#9a6700" if cat_pct >= 50 else "#cf222e")
        cat_rows += f"""
        <tr>
          <td><strong>{escape(cat)}</strong><br><span class="muted">{escape(s["chapter_ref"])}</span></td>
          <td class="num">{s['score']:.1f} / {s['max']}</td>
          <td>
            <div class="bar"><div class="fill" style="width:{cat_pct:.0f}%; background:{cat_color};"></div></div>
            <span class="muted">{cat_pct:.0f}%</span>
          </td>
          <td class="num">
            <span class="pill" style="background:#dafbe1;color:#1a7f37">{s['pass']}</span>
            <span class="pill" style="background:#fff8c5;color:#9a6700">{s['warn']}</span>
            <span class="pill" style="background:#ffebe9;color:#cf222e">{s['fail']}</span>
          </td>
        </tr>"""

    action_rows = ""
    for i, r in enumerate(actions, 1):
        action_rows += f"""
        <li>
          <strong>{escape(r.name)}</strong>
          <span class="muted">({escape(r.chapter_ref)})</span>
          <div class="fix">→ {escape(r.fix)}</div>
        </li>"""

    detail_rows = ""
    for r in results:
        detail_rows += f"""
        <tr class="row-{r.status}">
          <td><span class="badge" style="background:{STATUS_BG[r.status]};color:{STATUS_COLOR[r.status]};">{STATUS_BADGE[r.status]}</span></td>
          <td>
            <strong>{escape(r.name)}</strong>
            <div class="muted">{escape(r.description)}</div>
            <div class="muted">{escape(r.chapter_ref)} · weight {r.weight}</div>
            {f'<div class="details">{escape(r.details)}</div>' if r.details else ''}
            {f'<div class="fix">→ {escape(r.fix)}</div>' if r.fix and r.status != "pass" else ''}
          </td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AI Readiness Audit — {escape(repo.name)}</title>
<style>
  :root {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; }}
  body {{ max-width: 920px; margin: 2rem auto; padding: 0 1rem; color: #1f2328; line-height: 1.5; }}
  h1 {{ font-size: 1.7rem; margin-bottom: 0.25rem; }}
  h2 {{ font-size: 1.2rem; margin-top: 2rem; border-bottom: 1px solid #d0d7de; padding-bottom: 0.4rem; }}
  .muted {{ color: #656d76; font-size: 0.85rem; }}
  .header {{ background: #f6f8fa; padding: 1.2rem; border-radius: 8px; border: 1px solid #d0d7de; }}
  .score {{ font-size: 3rem; font-weight: 700; color: {overall_color}; }}
  .pct {{ font-size: 1.2rem; color: {overall_color}; }}
  table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; }}
  td, th {{ padding: 0.6rem; border-bottom: 1px solid #d0d7de; text-align: left; vertical-align: top; }}
  td.num {{ text-align: right; white-space: nowrap; }}
  .bar {{ display: inline-block; width: 200px; height: 8px; background: #eaeef2; border-radius: 4px; overflow: hidden; vertical-align: middle; }}
  .fill {{ height: 100%; }}
  .pill {{ display: inline-block; padding: 0.1rem 0.45rem; border-radius: 10px; font-size: 0.78rem; margin-left: 0.2rem; }}
  .badge {{ display: inline-block; padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 0.8rem; font-weight: 600; white-space: nowrap; }}
  .row-fail {{ background: #fff5f5; }}
  .fix {{ background: #f6f8fa; padding: 0.4rem 0.6rem; border-left: 3px solid #0969da; margin-top: 0.4rem; font-size: 0.9rem; }}
  .details {{ font-size: 0.85rem; color: #1f2328; margin-top: 0.3rem; font-style: italic; }}
  ol li {{ margin-bottom: 0.8rem; }}
  footer {{ margin-top: 3rem; color: #656d76; font-size: 0.8rem; text-align: center; }}
</style>
</head>
<body>
<div class="header">
  <h1>AI Readiness Audit</h1>
  <div class="muted">{escape(str(repo))} · stack: {escape(stack)} · {generated} · audit v{VERSION}</div>
  <div style="margin-top: 1rem;">
    <span class="score">{score:.1f}<span style="font-size: 1.2rem; color: #656d76;"> / {max_score}</span></span>
    <span class="pct">  ({pct:.0f}%)</span>
  </div>
  <div class="muted">Companion to <em>{escape(BOOK_TITLE)}</em> by Ryan Byrd.</div>
</div>

<h2>By category</h2>
<table>
  <tr><th>Category</th><th>Score</th><th>Progress</th><th>Pass / Warn / Fail</th></tr>
  {cat_rows}
</table>

<h2>Top {min(5, len(actions))} things to do this week</h2>
<ol>
  {action_rows}
</ol>

<h2>Detailed results</h2>
<table>
  {detail_rows}
</table>

<footer>
  Generated by ai-readiness-audit.py · companion to <em>{escape(BOOK_TITLE)}</em>.
  <br>The book and this script are MIT-licensed. Update via <a href="https://github.com/ryanbyrd/ai-engineering-handbook">github.com/ryanbyrd/ai-engineering-handbook</a>.
</footer>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="AI Readiness Audit — score a repo against the book's standards.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("repo", help="Path to repository to audit")
    parser.add_argument("-o", "--output", default="audit-report.html",
                        help="HTML output path (default: audit-report.html)")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of HTML")
    parser.add_argument("--text", action="store_true", help="Print text summary to stdout")
    parser.add_argument("--threshold", type=int, default=None,
                        help="Exit with code 1 if score is below this percentage (for CI use)")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        print(f"error: not a directory: {repo}", file=sys.stderr)
        return 2

    results = run_audit(repo)
    score, max_score = overall_score(results)
    pct = 100 * score / max_score if max_score else 0

    if args.json:
        out = {
            "version": VERSION,
            "repo": str(repo),
            "score": score,
            "max_score": max_score,
            "percentage": round(pct, 1),
            "stack": detect_stack(repo),
            "results": [asdict(r) for r in results],
            "generated": datetime.datetime.now().isoformat(),
        }
        print(json.dumps(out, indent=2))
    else:
        Path(args.output).write_text(render_html(repo, results))
        print(render_text(repo, results))
        print(f"\nFull HTML report: {args.output}")

    if args.threshold is not None and pct < args.threshold:
        print(f"\nFAIL: score {pct:.0f}% is below threshold {args.threshold}%", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
