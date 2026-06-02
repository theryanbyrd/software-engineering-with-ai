#!/usr/bin/env python3
"""token-cost-estimator.py — rough token/cost estimate for a repo or a chunk of text.

Companion to *Software Engineering with AI*, Ch 26 (Model Selection and Cost Discipline)
and Ch 29 (Token Cost Warning). Estimates are deliberately approximate — token prices are
perishable (Ch 50.5 §50.5.5). Pass --price to override the per-million-token rate.

Usage:
  python3 scripts/token-cost-estimator.py path/to/repo
  python3 scripts/token-cost-estimator.py file.py --price-in 3 --price-out 15
  echo "some prompt" | python3 scripts/token-cost-estimator.py -
Notes:
  ~4 characters per token is the standard heuristic for English/code. This is an
  estimate for budgeting, not billing. Measure against your provider's real usage.
"""
import argparse, sys, pathlib

CHARS_PER_TOKEN = 4
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".venv", "__pycache__", ".next"}
TEXT_EXT = {".py",".js",".ts",".tsx",".jsx",".go",".rs",".java",".rb",".md",".txt",
            ".json",".yaml",".yml",".toml",".sh",".html",".css",".sql"}

def count_chars_in_path(p: pathlib.Path) -> int:
    if p.is_file():
        try: return len(p.read_text(errors="ignore"))
        except Exception: return 0
    total = 0
    for f in p.rglob("*"):
        if any(part in SKIP_DIRS for part in f.parts): continue
        if f.is_file() and f.suffix.lower() in TEXT_EXT:
            try: total += len(f.read_text(errors="ignore"))
            except Exception: pass
    return total

def main():
    ap = argparse.ArgumentParser(description="Rough token/cost estimator (Ch 26, Ch 29).")
    ap.add_argument("target", help="repo dir, file, or - for stdin")
    ap.add_argument("--price-in", type=float, default=3.0, help="$/1M input tokens (default 3.0)")
    ap.add_argument("--price-out", type=float, default=15.0, help="$/1M output tokens (default 15.0)")
    ap.add_argument("--output-ratio", type=float, default=0.3,
                    help="assumed output tokens as fraction of input (default 0.3)")
    a = ap.parse_args()
    if a.target == "-":
        chars = len(sys.stdin.read())
    else:
        chars = count_chars_in_path(pathlib.Path(a.target))
    tok_in = chars / CHARS_PER_TOKEN
    tok_out = tok_in * a.output_ratio
    cost = tok_in/1_000_000*a.price_in + tok_out/1_000_000*a.price_out
    print(f"Characters:        {chars:,}")
    print(f"Est. input tokens: {tok_in:,.0f}  (@ {CHARS_PER_TOKEN} chars/token)")
    print(f"Est. output tokens:{tok_out:,.0f}  (ratio {a.output_ratio})")
    print(f"Est. cost (1 pass): ${cost:,.4f}  (in ${a.price_in}/M, out ${a.price_out}/M)")
    print("Estimate only — prices are perishable (Ch 50.5). Measure real usage.")

if __name__ == "__main__":
    main()
