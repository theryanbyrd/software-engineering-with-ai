#!/usr/bin/env python3
"""pr-ai-tagger.py — detect AI authorship signals and emit a PR label/marker.

Companion to *Software Engineering with AI*, Ch 21 / Ch 31 §31.6 ("make AI authorship
explicit") and Ch 2 §2.5 ("tooling that hides AI authorship — build the signal yourself").
Scans commit messages and the diff for AI-authorship trailers/markers and prints whether
the PR should be tagged [AI-authored].

Usage (run inside a git repo):
  python3 scripts/pr-ai-tagger.py                 # compare HEAD against origin/main
  python3 scripts/pr-ai-tagger.py --base main --head HEAD
  python3 scripts/pr-ai-tagger.py --github-output  # emit key=value for GitHub Actions
Exit code: 0 always (informational). Prints 'ai-authored: true|false'.
"""
import argparse, subprocess, re, sys, os

SIGNALS = [
    r"Co-authored-by:.*(claude|anthropic|copilot|cursor|gpt|gemini)",
    r"Generated with .*Claude", r"\bAI-authored\b", r"\[AI\]", r"\bvibe-?coded\b",
    r"Assisted-by:.*(claude|copilot|cursor)",
]

def git(args):
    try:
        return subprocess.check_output(["git"]+args, text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return ""

def main():
    ap = argparse.ArgumentParser(description="Tag PRs with AI-authorship signal (Ch 21, Ch 31 §31.6).")
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--head", default="HEAD")
    ap.add_argument("--github-output", action="store_true", help="emit key=value for CI")
    a = ap.parse_args()
    rng = f"{a.base}..{a.head}"
    log = git(["log", rng, "--format=%B%n%an %ae"])
    if not log:
        log = git(["log", "-20", "--format=%B%n%an %ae"])  # fallback
    matched = sorted({re.search(p, log, re.I).group(0).strip()
                      for p in SIGNALS if re.search(p, log, re.I)})
    is_ai = bool(matched)
    print(f"ai-authored: {str(is_ai).lower()}")
    if matched:
        print("signals found:")
        for m in matched: print(f"  - {m}")
    else:
        print("No AI-authorship trailer found. If this PR is AI-assisted, add a")
        print("'Co-authored-by:' trailer or tag the PR [AI-authored] (Ch 2 §2.5).")
    if a.github_output and os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
            fh.write(f"ai_authored={str(is_ai).lower()}\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
