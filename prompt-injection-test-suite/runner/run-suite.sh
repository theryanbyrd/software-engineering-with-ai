#!/usr/bin/env bash
# Prompt Injection Test Suite Runner
# Per Ch 37 of the Software Engineering with AI handbook

set -euo pipefail

SUITE_VERSION="2026.q3"
RESULTS_DIR="${RESULTS_DIR:-./results}"
mkdir -p "$RESULTS_DIR"

TIMESTAMP=$(date -u +"%Y%m%dT%H%M%SZ")
RESULTS_FILE="$RESULTS_DIR/run-$TIMESTAMP.md"

# Tests to run
TESTS=(
    "01-poisoned-issue-body"
    "02-malicious-pr-comment"
    "03-poisoned-web-page"
    "04-poisoned-log-line"
    "05-cross-repo-exfil"
    "06-credential-in-output"
)

cat > "$RESULTS_FILE" <<HEADER
# Prompt Injection Test Suite — Results

**Run:** $TIMESTAMP
**Suite version:** $SUITE_VERSION
**Operator:** $(whoami)
**Host:** $(hostname)

## Summary

| Test | Result | Notes |
|---|---|---|
HEADER

PASS=0
FAIL=0
SKIP=0

for test in "${TESTS[@]}"; do
    test_file="test-cases/$test.md"
    if [[ ! -f "$test_file" ]]; then
        echo "ERROR: test case file not found: $test_file" >&2
        exit 1
    fi
    
    echo ""
    echo "=========================================="
    echo "Test: $test"
    echo "=========================================="
    cat "$test_file" | head -20
    echo ""
    echo "Refer to $test_file for full setup, trigger, and verification steps."
    echo ""
    echo "After running the test, enter result: [P]ass / [F]ail / [S]kip"
    read -r -p "Result: " result
    
    case "$result" in
        [Pp]*)
            STATUS="PASS"
            PASS=$((PASS + 1))
            ;;
        [Ff]*)
            STATUS="FAIL"
            FAIL=$((FAIL + 1))
            ;;
        [Ss]*)
            STATUS="SKIP"
            SKIP=$((SKIP + 1))
            ;;
        *)
            STATUS="UNKNOWN"
            ;;
    esac
    
    echo "Notes (one line; press Enter to skip):"
    read -r notes
    
    echo "| $test | $STATUS | $notes |" >> "$RESULTS_FILE"
done

cat >> "$RESULTS_FILE" <<FOOTER

## Totals

- **Pass:** $PASS / ${#TESTS[@]}
- **Fail:** $FAIL / ${#TESTS[@]}
- **Skip:** $SKIP / ${#TESTS[@]}

## Next steps

$(if [[ $FAIL -gt 0 ]]; then
    echo "**FAILURES DETECTED.** Per Ch 37: 'Treat any pass-to-fail regression as a P1 incident.'"
    echo ""
    echo "1. Open a P1 incident ticket for each failure"
    echo "2. Run the response runbook (\`response-runbook.md\`)"
    echo "3. Do not roll out new agent capabilities until the failures are addressed"
else
    echo "All tests passed. File this run for the quarterly compliance record."
fi)

## Filing

This results file: $RESULTS_FILE

For the quarterly cadence, review the previous run's results to detect regressions.
FOOTER

echo ""
echo "=========================================="
echo "Results saved to: $RESULTS_FILE"
echo "Pass: $PASS | Fail: $FAIL | Skip: $SKIP"

if [[ $FAIL -gt 0 ]]; then
    echo ""
    echo "FAILURES DETECTED. See response-runbook.md."
    exit 1
fi
