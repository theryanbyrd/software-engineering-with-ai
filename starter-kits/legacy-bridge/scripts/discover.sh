#!/usr/bin/env bash
# discover.sh — auto-detect what tools, languages, and conventions a repo uses.
# Read-only. Outputs a markdown report to stdout.
#
# Usage: bash legacy-bridge-scripts/discover.sh [path]

set -uo pipefail

REPO="${1:-.}"
cd "$REPO" || { echo "Cannot cd to $REPO"; exit 1; }

echo "# Discovery Report — $(basename "$(pwd)")"
echo "_Generated $(date -u +%Y-%m-%dT%H:%M:%SZ)_"
echo ""

# ---- Languages ----
echo "## Languages detected"
echo ""
declare -A langs
for ext in py rb js ts tsx jsx go rs java kt cs cpp c rb php scala swift; do
  count=$(find . -name "*.${ext}" -not -path "*/node_modules/*" -not -path "*/.venv/*" -not -path "*/vendor/*" -not -path "*/.git/*" 2>/dev/null | wc -l)
  if [ "$count" -gt 0 ]; then
    langs["$ext"]=$count
  fi
done
for ext in "${!langs[@]}"; do
  echo "- \`.${ext}\`: ${langs[$ext]} files"
done
echo ""

# ---- Build / package files ----
echo "## Build and package configuration"
echo ""
for f in package.json pyproject.toml setup.py requirements.txt Gemfile go.mod Cargo.toml pom.xml build.gradle build.gradle.kts Makefile CMakeLists.txt composer.json; do
  if [ -f "$f" ]; then
    echo "- \`$f\` exists"
  fi
done
echo ""

# ---- Tests ----
echo "## Tests"
echo ""
for pattern in "tests" "test" "spec" "__tests__"; do
  if [ -d "$pattern" ]; then
    count=$(find "$pattern" -type f 2>/dev/null | wc -l)
    echo "- \`$pattern/\` directory: $count files"
  fi
done
test_files=$(find . \( -name "test_*.py" -o -name "*_test.go" -o -name "*.test.ts" -o -name "*.test.js" -o -name "*.spec.ts" -o -name "*Test.java" \) -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | wc -l)
echo "- Test files (by naming convention): $test_files"
echo ""

# ---- CI ----
echo "## CI configuration"
echo ""
for f in .github/workflows .gitlab-ci.yml .circleci/config.yml Jenkinsfile azure-pipelines.yml .travis.yml; do
  if [ -e "$f" ]; then
    echo "- \`$f\` present"
  fi
done
echo ""

# ---- Existing harness ----
echo "## Existing AI harness"
echo ""
for f in CLAUDE.md AGENTS.md .cursorrules .github/copilot-instructions.md llms.txt .claude .aider .cursor; do
  if [ -e "$f" ]; then
    echo "- \`$f\` exists"
  fi
done
echo ""

# ---- Dead-code signals ----
echo "## Brownfield signals"
echo ""
echo "### Files not modified in 2+ years"
old_count=$(find . -type f -mtime +730 -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/vendor/*" 2>/dev/null | wc -l)
echo "- Count: $old_count"
echo ""

echo "### TODO/FIXME density"
todo_count=$(grep -r --include="*.py" --include="*.ts" --include="*.js" --include="*.rb" --include="*.go" --include="*.java" -E "TODO|FIXME|XXX|HACK" . 2>/dev/null | wc -l)
echo "- Count: $todo_count"
echo ""

echo "### Type-ignore / silenced lints"
ignore_count=$(grep -r --include="*.py" --include="*.ts" --include="*.js" -E "type:\s*ignore|@ts-ignore|// eslint-disable|# noqa" . 2>/dev/null | wc -l)
echo "- Count: $ignore_count"
echo ""

# ---- Documentation ----
echo "## Documentation density"
echo ""
md_count=$(find . -name "*.md" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | wc -l)
echo "- Markdown files: $md_count"
readme_count=$(find . -iname "readme*" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | wc -l)
echo "- READMEs: $readme_count"
echo ""

# ---- Module candidates ----
echo "## Top-level directories (potential modules)"
echo ""
for d in */; do
  d="${d%/}"
  case "$d" in
    node_modules|.git|.venv|vendor|build|dist|coverage|target) continue ;;
  esac
  if [ -d "$d" ]; then
    file_count=$(find "$d" -type f 2>/dev/null | wc -l)
    echo "- \`$d/\`: $file_count files"
  fi
done
echo ""

# ---- Recommendations ----
echo "## Suggested next steps"
echo ""
if [ ! -f "CLAUDE.md" ]; then
  echo "1. Copy this starter's \`CLAUDE.md\` to repo root and customize."
fi
if [ "$test_files" -lt 50 ]; then
  echo "1. Test coverage is low ($test_files files). Golden master tests will be your primary safety net."
fi
if [ "$old_count" -gt 100 ]; then
  echo "1. Many files (>$old_count) haven't been modified in 2+ years — flag the modules these live in as L0 in MVH_LEVELS until characterized."
fi
echo "1. Run \`bash legacy-bridge-scripts/golden-master-record.sh <module>\` for your first chosen module."
echo "1. Read \`BROWNFIELD_PLAN.md\` and start at Day 0."
