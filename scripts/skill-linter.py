#!/usr/bin/env python3
"""skill-linter.py — lint SKILL.md files against the book's Ch 13 §13.4 shape.

Companion to *Software Engineering with AI*, Ch 13 (Skills as Playbooks) and the repo's
CONTRIBUTING quality bar ("New skills must pass scripts/skill-linter.py"). Checks that
each skill has the required sections so skills stay consistent and agent-usable.

Usage:
  python3 scripts/skill-linter.py skills/            # lint all skills under a dir
  python3 scripts/skill-linter.py skills/code-review/SKILL.md
Exit code: 0 if all pass, 1 if any skill fails.
"""
import sys, pathlib, re

REQUIRED = {
    "name":        r"(?im)^\s*(name\s*:|#\s)",
    "description": r"(?im)^\s*description\s*:|##?\s*description",
    "when-to-use": r"(?i)when to use|when-to-use|## when",
    "procedure":   r"(?i)procedure|## steps|plan first|## process",
    "forbidden":   r"(?i)forbidden|do not|never\b|## don'?t",
    "references":  r"(?i)references|see also|## refs|chapter",
}

def find_skills(target: pathlib.Path):
    if target.is_file(): return [target]
    return sorted(target.rglob("SKILL.md"))

def lint(path: pathlib.Path):
    text = path.read_text(errors="ignore")
    missing = [k for k, pat in REQUIRED.items() if not re.search(pat, text)]
    return missing

def main():
    if len(sys.argv) < 2:
        print("usage: skill-linter.py <skills-dir-or-SKILL.md>"); sys.exit(2)
    target = pathlib.Path(sys.argv[1])
    skills = find_skills(target)
    if not skills:
        print(f"No SKILL.md found under {target}"); sys.exit(1)
    failed = 0
    for s in skills:
        missing = lint(s)
        if missing:
            failed += 1
            print(f"FAIL {s}: missing {', '.join(missing)}")
        else:
            print(f"PASS {s}")
    print(f"\n{len(skills)-failed}/{len(skills)} skills passed.")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
