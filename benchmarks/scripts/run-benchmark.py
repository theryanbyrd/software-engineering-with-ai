#!/usr/bin/env python3
"""
run-benchmark.py — orchestrate golden tasks against an agent and produce
a quarterly regression report.

Companion to Chapter 6 §6.5.2 of "Software Engineering with AI" by Ryan Byrd.

Stdlib only. Python 3.9+.

Modes:
  Default:                  list tasks, prompt for confirmation, then run all
  --tasks <dir>:            run all tasks in a specific directory
  --task <id>:              run a single task by ID
  --tier T1|T2|T3:          run only tasks of a specific tier
  --report:                 read latest results and print the human-readable report
  --compare <baseline.json>: compare a new run against a baseline
  --self-check:             verify task files parse correctly without running

Configuration:
  Define your agent in scripts/adapters/<name>.py implementing the Agent
  protocol (same as the prompt-injection-test-suite runner). Pass --adapter NAME.

Output:
  results/run-YYYY-Q<N>.json    machine-readable
  results/run-YYYY-Q<N>.md      human-readable report
  Exit code 0 always (even on regressions — the grader decides what to do).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

VERSION = "2026.q3"
SCRIPT_DIR = Path(__file__).resolve().parent
BENCHMARK_DIR = SCRIPT_DIR.parent
TASKS_DIR = BENCHMARK_DIR / "tasks"
RESULTS_DIR = BENCHMARK_DIR / "results"


# ---------------------------------------------------------------------------
# Task parsing
# ---------------------------------------------------------------------------

@dataclass
class RubricItem:
    text: str
    weight: int = 1   # T1/T2 default 1; T3 items can be 0-3


@dataclass
class Task:
    task_id: str
    title: str
    tier: str   # T1 | T2 | T3
    estimated_time: str
    surfaces: list[str]
    file_path: Path
    instruction: str
    pass_criterion: str
    rubric: list[RubricItem]
    max_score: int


def parse_task(path: Path) -> Optional[Task]:
    """Parse a task markdown file. Returns None if file is the template
    or not a valid task."""
    if path.name.startswith("_") or not path.name.endswith(".md"):
        return None

    text = path.read_text()

    # task_id from filename
    task_id = path.stem

    # Title
    title_m = re.search(r"^#\s+(.+)$", text, re.M)
    title = title_m.group(1) if title_m else task_id

    # Tier
    tier_m = re.search(r"\*\*Tier:\*\*\s*(T[123])", text)
    tier = tier_m.group(1) if tier_m else "T2"

    # Estimated time
    time_m = re.search(r"\*\*Estimated time[^:]*:\*\*\s*([^\n]+)", text)
    estimated_time = time_m.group(1).strip() if time_m else "unknown"

    # Surfaces
    surf_m = re.search(r"\*\*Surfaces tested:\*\*\s*([^\n]+)", text)
    surfaces = []
    if surf_m:
        surfaces = [s.strip() for s in surf_m.group(1).split("|") if s.strip()]

    # The task instruction (verbatim — first blockquote in "## The task" section)
    task_section = re.search(r"##\s+The task[^\n]*\n([\s\S]+?)(?=^##\s)", text, re.M)
    instruction = ""
    if task_section:
        # Find blockquote
        bq = re.search(r"^>\s*(.+(?:\n>\s*.+)*)", task_section.group(1), re.M)
        if bq:
            instruction = re.sub(r"^>\s*", "", bq.group(1), flags=re.M).strip()

    # Pass criterion
    pass_section = re.search(r"##\s+Pass criterion\n([\s\S]+?)(?=^##\s)", text, re.M)
    pass_criterion = pass_section.group(1).strip() if pass_section else ""

    # Rubric — checkbox lines
    rubric_section = re.search(r"##\s+Rubric[^\n]*\n([\s\S]+?)(?=^##\s|^---|\Z)", text, re.M)
    rubric = []
    max_score = 0
    if rubric_section:
        # Parse weight from header if present (e.g., "max 14" or "max 24")
        max_m = re.search(r"max\s+(\d+)", rubric_section.group(0)[:200])
        if max_m:
            max_score = int(max_m.group(1))
        # Each "- [ ]" or "- [x]" line is a rubric item
        for line in rubric_section.group(1).splitlines():
            m = re.match(r"\s*-\s*\[\s\]\s*(.+)", line)
            if m:
                # T3 tasks have weights 0-3
                weight = 3 if tier == "T3" else 1
                rubric.append(RubricItem(text=m.group(1), weight=weight))
        if max_score == 0 and rubric:
            max_score = sum(item.weight for item in rubric)

    return Task(
        task_id=task_id,
        title=title,
        tier=tier,
        estimated_time=estimated_time,
        surfaces=surfaces,
        file_path=path,
        instruction=instruction,
        pass_criterion=pass_criterion,
        rubric=rubric,
        max_score=max_score,
    )


def discover_tasks(tasks_dir: Path) -> list[Task]:
    tasks = []
    for path in sorted(tasks_dir.glob("*.md")):
        task = parse_task(path)
        if task and task.rubric:
            tasks.append(task)
    return tasks


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class TaskResult:
    task_id: str
    tier: str
    title: str
    pass_criterion_met: bool
    rubric_scores: list[bool]   # one per rubric item (T1/T2)
    rubric_weights: list[int]   # the weight scored 0..weight (T3)
    raw_score: int
    max_score: int
    normalized_score: float     # 0-100
    pass_fail: str               # "pass" | "fail" | "manual-grade"
    duration_seconds: Optional[float]
    token_cost_estimate: Optional[float]
    transcript_path: Optional[str]
    notes: str = ""


@dataclass
class RunResult:
    version: str
    timestamp: str
    quarter: str               # e.g., "2026-Q2"
    agent_adapter: str
    model: str
    task_results: list[TaskResult]

    @property
    def aggregate_score(self) -> float:
        if not self.task_results:
            return 0.0
        return sum(r.normalized_score for r in self.task_results) / len(self.task_results)

    @property
    def by_tier(self) -> dict[str, list[TaskResult]]:
        out: dict[str, list[TaskResult]] = {"T1": [], "T2": [], "T3": []}
        for r in self.task_results:
            out.setdefault(r.tier, []).append(r)
        return out


# ---------------------------------------------------------------------------
# Agent runner — stub adapter for self-check
# ---------------------------------------------------------------------------

class StubAgent:
    """Self-check stub. Real adapters live in scripts/adapters/<name>.py.

    The Agent protocol:
      def run_task(self, task: Task) -> dict
        Returns:
          - "transcript": list of strings or list of dicts (tool calls, edits, etc.)
          - "outcome": dict with grader-relevant signals
          - "duration_seconds": float
          - "token_cost_usd": float
    """
    name = "stub"
    model = "stub-1.0"

    def run_task(self, task: Task) -> dict:
        return {
            "transcript": ["[stub] Would have attempted task: " + task.title],
            "outcome": {"completed": False, "manual_grade_required": True},
            "duration_seconds": 0.0,
            "token_cost_usd": 0.0,
        }


def load_adapter(name: str):
    if name in ("stub", "self-check"):
        return StubAgent()
    adapter_path = SCRIPT_DIR / "adapters" / f"{name}.py"
    if not adapter_path.exists():
        print(f"error: adapter '{name}' not found at {adapter_path}", file=sys.stderr)
        print("Implement the Agent protocol in scripts/adapters/<name>.py and try again.", file=sys.stderr)
        sys.exit(2)
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"adapter_{name}", adapter_path)
    if spec is None or spec.loader is None:
        print(f"error: could not load adapter {name}", file=sys.stderr)
        sys.exit(2)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Adapter()


# ---------------------------------------------------------------------------
# Run orchestrator
# ---------------------------------------------------------------------------

def current_quarter() -> str:
    now = datetime.now()
    q = (now.month - 1) // 3 + 1
    return f"{now.year}-Q{q}"


def run_task(agent, task: Task, transcripts_dir: Path) -> TaskResult:
    """Run a single task and return a result with placeholders for manual grading."""
    print(f"  Running {task.task_id} ({task.tier})...", file=sys.stderr)
    response = agent.run_task(task)

    # Save transcript
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = transcripts_dir / f"{task.task_id}-transcript.txt"
    with transcript_path.open("w") as f:
        f.write(f"# Transcript for {task.task_id}\n\n")
        f.write(f"Task: {task.title}\n")
        f.write(f"Tier: {task.tier}\n")
        f.write(f"Adapter: {getattr(agent, 'name', 'unknown')}\n")
        f.write(f"Model: {getattr(agent, 'model', 'unknown')}\n\n")
        f.write("## Instruction given to agent\n\n")
        f.write(task.instruction + "\n\n")
        f.write("## Response\n\n")
        for entry in response.get("transcript", []):
            f.write(str(entry) + "\n")

    # For automated runs, results are scaffolded for manual grading
    rubric_scores = [False] * len(task.rubric)
    rubric_weights = [0] * len(task.rubric)

    return TaskResult(
        task_id=task.task_id,
        tier=task.tier,
        title=task.title,
        pass_criterion_met=False,   # set by grader
        rubric_scores=rubric_scores,
        rubric_weights=rubric_weights,
        raw_score=0,
        max_score=task.max_score,
        normalized_score=0.0,
        pass_fail="manual-grade",
        duration_seconds=response.get("duration_seconds"),
        token_cost_estimate=response.get("token_cost_usd"),
        transcript_path=str(transcript_path.relative_to(BENCHMARK_DIR)),
        notes="Awaiting manual grading. See score-result.py for grading interface.",
    )


def run_benchmark(agent, tasks: list[Task]) -> RunResult:
    quarter = current_quarter()
    transcripts_dir = RESULTS_DIR / f"transcripts-{quarter}"

    print(f"Running {len(tasks)} tasks against {agent.name} ({getattr(agent, 'model', 'unknown')})", file=sys.stderr)
    print(f"Transcripts will be written to: {transcripts_dir}", file=sys.stderr)

    task_results = []
    for task in tasks:
        result = run_task(agent, task, transcripts_dir)
        task_results.append(result)

    return RunResult(
        version=VERSION,
        timestamp=datetime.now().isoformat(timespec="seconds"),
        quarter=quarter,
        agent_adapter=agent.name,
        model=getattr(agent, "model", "unknown"),
        task_results=task_results,
    )


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def render_report(result: RunResult, baseline: Optional[RunResult] = None) -> str:
    lines = [
        f"# Benchmark Report — {result.quarter}",
        "",
        f"- **Run timestamp:** {result.timestamp}",
        f"- **Adapter:** {result.agent_adapter}",
        f"- **Model:** {result.model}",
        f"- **Tasks run:** {len(result.task_results)}",
        f"- **Aggregate score:** {result.aggregate_score:.1f} / 100",
        "",
    ]

    if baseline:
        delta = result.aggregate_score - baseline.aggregate_score
        sign = "+" if delta >= 0 else ""
        lines.append(f"- **Baseline ({baseline.quarter}):** {baseline.aggregate_score:.1f}")
        lines.append(f"- **Delta:** {sign}{delta:.1f}")
        if abs(delta) >= 5:
            lines.append(f"- **Verdict:** {'IMPROVEMENT' if delta > 0 else 'REGRESSION'} (delta exceeds 5-point noise threshold)")
        else:
            lines.append("- **Verdict:** Within noise threshold (±5 points)")
        lines.append("")

    # Per-tier breakdown
    lines.append("## Per-tier breakdown")
    lines.append("")
    lines.append("| Tier | Tasks | Average | vs. Baseline |")
    lines.append("|---|---|---|---|")
    for tier in ("T1", "T2", "T3"):
        tier_results = [r for r in result.task_results if r.tier == tier]
        if not tier_results:
            continue
        avg = sum(r.normalized_score for r in tier_results) / len(tier_results)
        vs_baseline = "—"
        if baseline:
            base_tier = [r for r in baseline.task_results if r.tier == tier]
            if base_tier:
                base_avg = sum(r.normalized_score for r in base_tier) / len(base_tier)
                d = avg - base_avg
                vs_baseline = f"{'+' if d >= 0 else ''}{d:.1f}"
        lines.append(f"| {tier} | {len(tier_results)} | {avg:.1f} | {vs_baseline} |")
    lines.append("")

    # Per-task table
    lines.append("## Per-task results")
    lines.append("")
    lines.append("| Task | Tier | Score | Status | Transcript |")
    lines.append("|---|---|---|---|---|")
    for r in result.task_results:
        status_icon = {"pass": "✅", "fail": "❌", "manual-grade": "⏳"}.get(r.pass_fail, "?")
        transcript_link = f"[view]({r.transcript_path})" if r.transcript_path else "—"
        lines.append(f"| {r.task_id} | {r.tier} | {r.normalized_score:.0f} | {status_icon} {r.pass_fail} | {transcript_link} |")
    lines.append("")

    # Regression flags
    if baseline:
        regressions = []
        improvements = []
        baseline_by_id = {r.task_id: r for r in baseline.task_results}
        for r in result.task_results:
            if r.task_id in baseline_by_id:
                base_score = baseline_by_id[r.task_id].normalized_score
                delta = r.normalized_score - base_score
                if delta <= -10:
                    regressions.append((r.task_id, base_score, r.normalized_score, delta))
                elif delta >= 10:
                    improvements.append((r.task_id, base_score, r.normalized_score, delta))

        if regressions:
            lines.append("## ⚠ Regressions (delta ≤ -10)")
            lines.append("")
            for task_id, base, curr, delta in regressions:
                lines.append(f"- **{task_id}:** {base:.0f} → {curr:.0f} ({delta:.0f}). Investigate.")
            lines.append("")
        if improvements:
            lines.append("## ✅ Improvements (delta ≥ +10)")
            lines.append("")
            for task_id, base, curr, delta in improvements:
                lines.append(f"- **{task_id}:** {base:.0f} → {curr:.0f} (+{delta:.0f})")
            lines.append("")

    # Cost and time
    total_cost = sum((r.token_cost_estimate or 0) for r in result.task_results)
    total_seconds = sum((r.duration_seconds or 0) for r in result.task_results)
    if total_cost > 0 or total_seconds > 0:
        lines.append("## Run economics")
        lines.append("")
        lines.append(f"- **Total wall-clock time:** {total_seconds/60:.1f} minutes")
        lines.append(f"- **Total token cost (estimated):** ${total_cost:.2f}")
        lines.append("")

    # Manual grading note
    pending = [r for r in result.task_results if r.pass_fail == "manual-grade"]
    if pending:
        lines.append("## Pending manual grading")
        lines.append("")
        lines.append(f"{len(pending)} task(s) await manual grading. Use:")
        lines.append("")
        lines.append("```")
        lines.append("python3 scripts/score-result.py --task <task_id>")
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--tasks", default=str(TASKS_DIR), help="Path to tasks/ directory")
    parser.add_argument("--task", help="Run a single task by ID")
    parser.add_argument("--tier", choices=["T1", "T2", "T3"], help="Run only tasks of one tier")
    parser.add_argument("--adapter", default="stub", help="Agent adapter name")
    parser.add_argument("--self-check", action="store_true",
                        help="Verify task files parse correctly without running")
    parser.add_argument("--list", action="store_true", help="List tasks and exit")
    parser.add_argument("--report", action="store_true",
                        help="Print latest run's report and exit")
    parser.add_argument("--compare", help="Compare against a baseline JSON results file")
    args = parser.parse_args()

    tasks_dir = Path(args.tasks)
    tasks = discover_tasks(tasks_dir)

    if args.list or args.self_check:
        print(f"Discovered {len(tasks)} tasks in {tasks_dir}:")
        for t in tasks:
            print(f"  {t.task_id}  [{t.tier}]  max_score={t.max_score}  rubric_items={len(t.rubric)}")
            if args.self_check:
                if not t.instruction:
                    print(f"    ⚠ no instruction parsed")
                if not t.rubric:
                    print(f"    ⚠ no rubric parsed")
                if t.max_score == 0:
                    print(f"    ⚠ max_score is 0")
        return 0

    if args.report:
        latest = sorted(RESULTS_DIR.glob("run-*.md")) if RESULTS_DIR.exists() else []
        if not latest:
            print("No reports found. Run the benchmark first.", file=sys.stderr)
            return 2
        print(latest[-1].read_text())
        return 0

    # Filter
    if args.task:
        tasks = [t for t in tasks if t.task_id == args.task]
        if not tasks:
            print(f"error: no task with ID {args.task}", file=sys.stderr)
            return 2
    if args.tier:
        tasks = [t for t in tasks if t.tier == args.tier]
        if not tasks:
            print(f"error: no tasks at tier {args.tier}", file=sys.stderr)
            return 2

    # Load baseline if provided
    baseline = None
    if args.compare:
        baseline_path = Path(args.compare)
        if not baseline_path.is_file():
            print(f"error: baseline file not found: {baseline_path}", file=sys.stderr)
            return 2
        baseline_data = json.loads(baseline_path.read_text())
        baseline_results = [TaskResult(**tr) for tr in baseline_data["task_results"]]
        baseline = RunResult(
            version=baseline_data.get("version", "?"),
            timestamp=baseline_data.get("timestamp", "?"),
            quarter=baseline_data.get("quarter", "baseline"),
            agent_adapter=baseline_data.get("agent_adapter", "?"),
            model=baseline_data.get("model", "?"),
            task_results=baseline_results,
        )

    agent = load_adapter(args.adapter)
    result = run_benchmark(agent, tasks)

    # Write artifacts
    RESULTS_DIR.mkdir(exist_ok=True)
    json_path = RESULTS_DIR / f"run-{result.quarter}.json"
    md_path = RESULTS_DIR / f"run-{result.quarter}.md"

    # If a quarterly file already exists, suffix with timestamp
    if json_path.exists():
        ts = datetime.now().strftime("%H%M%S")
        json_path = RESULTS_DIR / f"run-{result.quarter}-{ts}.json"
        md_path = RESULTS_DIR / f"run-{result.quarter}-{ts}.md"

    json_path.write_text(json.dumps({
        "version": result.version,
        "timestamp": result.timestamp,
        "quarter": result.quarter,
        "agent_adapter": result.agent_adapter,
        "model": result.model,
        "task_results": [asdict(r) for r in result.task_results],
    }, indent=2))

    md_path.write_text(render_report(result, baseline))

    # Print summary
    print(render_report(result, baseline))
    print(f"\nResults: {json_path}", file=sys.stderr)
    print(f"Report:  {md_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
