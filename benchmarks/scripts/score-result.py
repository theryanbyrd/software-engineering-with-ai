#!/usr/bin/env python3
"""
score-result.py — interactive manual grading for benchmark runs.

After run-benchmark.py completes, each task's transcript is captured but
the rubric is unscored (status: manual-grade). This tool walks a grader
through each rubric item and writes the scores back to the results file.

Stdlib only. Python 3.9+.

Usage:
    python3 scripts/score-result.py --task T1-add-field-to-user-model
    python3 scripts/score-result.py --quarter 2026-Q2 --interactive
    python3 scripts/score-result.py --quarter 2026-Q2 --task T2-add-api-endpoint
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BENCHMARK_DIR = SCRIPT_DIR.parent
RESULTS_DIR = BENCHMARK_DIR / "results"
TASKS_DIR = BENCHMARK_DIR / "tasks"


def find_results_file(quarter: str | None) -> Path | None:
    if quarter:
        candidates = list(RESULTS_DIR.glob(f"run-{quarter}*.json"))
    else:
        candidates = list(RESULTS_DIR.glob("run-*.json"))
    if not candidates:
        return None
    return sorted(candidates)[-1]


def parse_rubric_from_task_file(task_id: str) -> list[str]:
    """Re-parse the rubric items from the task markdown file for grading prompts."""
    task_file = TASKS_DIR / f"{task_id}.md"
    if not task_file.is_file():
        return []
    text = task_file.read_text()
    items = []
    in_rubric = False
    for line in text.splitlines():
        if line.startswith("## Rubric"):
            in_rubric = True
            continue
        if in_rubric and line.startswith("##"):
            break
        if in_rubric:
            stripped = line.strip()
            if stripped.startswith("- [ ]"):
                items.append(stripped[5:].strip())
    return items


def grade_task(task_result: dict, tier: str) -> dict:
    """Walk the grader through the rubric. Returns updated task_result."""
    task_id = task_result["task_id"]
    rubric = parse_rubric_from_task_file(task_id)

    if not rubric:
        print(f"[{task_id}] No rubric found in task file; skipping.")
        return task_result

    print(f"\n{'='*72}")
    print(f"Grading: {task_id} ({tier})")
    print(f"Title: {task_result['title']}")
    if task_result.get("transcript_path"):
        print(f"Transcript: {task_result['transcript_path']}")
    print(f"{'='*72}\n")

    # Pass criterion
    pc = input("Pass criterion met? (y/n/skip): ").strip().lower()
    if pc == "skip":
        print(f"  Skipped {task_id}")
        return task_result
    pass_met = pc == "y"

    # Rubric items
    print(f"\nRubric ({len(rubric)} items):")
    if tier == "T3":
        print("Score each item 0-3 (0=absent, 1=weak, 2=adequate, 3=strong)")
        weights = []
        for i, item in enumerate(rubric, 1):
            print(f"\n[{i}/{len(rubric)}] {item}")
            while True:
                resp = input("Score (0/1/2/3): ").strip()
                if resp in ("0", "1", "2", "3"):
                    weights.append(int(resp))
                    break
                print("  Please enter 0, 1, 2, or 3.")
        scores_bool = [w > 0 for w in weights]   # for compatibility with the dataclass
        raw = sum(weights)
        max_score = len(rubric) * 3
    else:
        print("For each item, answer y (achieved) or n (not achieved):")
        scores_bool = []
        for i, item in enumerate(rubric, 1):
            print(f"\n[{i}/{len(rubric)}] {item}")
            while True:
                resp = input("Achieved? (y/n): ").strip().lower()
                if resp in ("y", "n"):
                    scores_bool.append(resp == "y")
                    break
                print("  Please enter y or n.")
        weights = [1 if s else 0 for s in scores_bool]
        raw = sum(weights)
        max_score = len(rubric)

    # Notes
    print()
    notes = input("Notes (optional, one line): ").strip()

    normalized = (raw / max_score) * 100 if max_score > 0 else 0.0

    # Determine pass/fail
    if not pass_met:
        pass_fail = "fail"
    elif normalized >= 70:
        pass_fail = "pass"
    else:
        pass_fail = "fail"

    print(f"\n  Score: {raw}/{max_score} ({normalized:.1f}%) — {pass_fail}")

    # Update result
    task_result["pass_criterion_met"] = pass_met
    task_result["rubric_scores"] = scores_bool
    task_result["rubric_weights"] = weights
    task_result["raw_score"] = raw
    task_result["max_score"] = max_score
    task_result["normalized_score"] = normalized
    task_result["pass_fail"] = pass_fail
    if notes:
        task_result["notes"] = notes

    return task_result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quarter", help="Quarter to grade (e.g., 2026-Q2). Default: latest run.")
    parser.add_argument("--task", help="Grade only this specific task ID")
    parser.add_argument("--list", action="store_true", help="List ungraded tasks and exit")
    args = parser.parse_args()

    results_file = find_results_file(args.quarter)
    if not results_file:
        print("No results file found. Run benchmarks first.", file=sys.stderr)
        return 2

    print(f"Loading results from: {results_file}")
    data = json.loads(results_file.read_text())

    # Show what needs grading
    pending = [r for r in data["task_results"] if r.get("pass_fail") == "manual-grade"]
    if args.list:
        if not pending:
            print("No tasks pending manual grading.")
            return 0
        print(f"\nPending grading ({len(pending)} task(s)):")
        for r in pending:
            print(f"  {r['task_id']} ({r['tier']})")
        return 0

    if not pending:
        print("All tasks already graded. Use --task to re-grade a specific task.")
        if not args.task:
            return 0

    # Grade
    to_grade = data["task_results"]
    if args.task:
        to_grade = [r for r in to_grade if r["task_id"] == args.task]
        if not to_grade:
            print(f"error: no task {args.task} in results", file=sys.stderr)
            return 2
    else:
        to_grade = pending

    print(f"\nGrading {len(to_grade)} task(s). Press Ctrl-C to save and exit.\n")

    try:
        for tr in to_grade:
            tier = tr.get("tier", "T2")
            updated = grade_task(tr, tier)
            # Update in the data structure
            for i, r in enumerate(data["task_results"]):
                if r["task_id"] == updated["task_id"]:
                    data["task_results"][i] = updated
                    break
    except KeyboardInterrupt:
        print("\nInterrupted. Saving partial progress.")

    # Save
    results_file.write_text(json.dumps(data, indent=2))
    print(f"\nSaved to: {results_file}")

    # Recompute aggregate
    scores = [r["normalized_score"] for r in data["task_results"] if r.get("pass_fail") != "manual-grade"]
    if scores:
        agg = sum(scores) / len(scores)
        print(f"Updated aggregate score: {agg:.1f} / 100 (over {len(scores)} graded tasks)")

    print("\nNext: regenerate the report with:")
    print(f"  python3 scripts/run-benchmark.py --report")

    return 0


if __name__ == "__main__":
    sys.exit(main())
