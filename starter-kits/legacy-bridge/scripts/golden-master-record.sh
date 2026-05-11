#!/usr/bin/env bash
# golden-master-record.sh — record the current behavior of a module
# as a set of input/expected-output pairs that can be replayed later.
#
# This is a SCAFFOLD. Real recording depends on what the module does
# (HTTP service vs. batch job vs. UI). Customize the stub functions below.
#
# Usage: bash legacy-bridge-scripts/golden-master-record.sh <module>

set -euo pipefail

MODULE="${1:-}"
if [ -z "$MODULE" ]; then
  echo "Usage: $0 <module>"
  echo ""
  echo "Examples:"
  echo "  $0 api/v1/orders"
  echo "  $0 legacy/billing"
  echo "  $0 core/scheduler"
  exit 1
fi

GOLDEN_DIR="tests/golden/${MODULE}"
mkdir -p "$GOLDEN_DIR/inputs" "$GOLDEN_DIR/expected"

echo "Recording golden master for: $MODULE"
echo "Output directory: $GOLDEN_DIR"
echo ""
echo "This script is a SCAFFOLD. You need to customize it for your module type."
echo ""
echo "## For an HTTP service:"
echo ""
echo "  Replace this script's body with traffic capture (e.g., mitmproxy --mode reverse:http://your-service)"
echo "  Run for 1-2 weeks against production-like traffic"
echo "  Save request/response pairs to \$GOLDEN_DIR"
echo ""
echo "## For a batch job:"
echo ""
echo "  1. Pick representative inputs (small/medium/edge cases)"
echo "  2. Place them in \$GOLDEN_DIR/inputs/"
echo "  3. Run your batch job against each input"
echo "  4. Save the outputs in \$GOLDEN_DIR/expected/"
echo "  5. Verify by running the job again — outputs should match"
echo ""
echo "## For a UI:"
echo ""
echo "  Use Playwright or Cypress to capture screenshots of key flows"
echo "  Save to \$GOLDEN_DIR/screenshots/"
echo ""
echo "## After recording:"
echo ""
echo "  1. Add a 'replay' command to legacy-verify.sh that compares current"
echo "     behavior against the golden master."
echo "  2. Run legacy-verify.sh and confirm it passes against current code."
echo "  3. Run it against a deliberate-breakage version (mutate a function)"
echo "     and confirm it FAILS."
echo "  4. Only then is the golden master 'real.'"
echo ""

# Create a placeholder so the next invocation knows recording was attempted
cat > "$GOLDEN_DIR/RECORDING.md" <<EOF
# Golden Master Recording — $MODULE

Started: $(date -u +%Y-%m-%dT%H:%M:%SZ)
Status: SCAFFOLD — needs customization for module type

See \`legacy-bridge-scripts/golden-master-record.sh\` for guidance.
EOF

echo "Created scaffold at $GOLDEN_DIR/"
echo "Next: customize this script for your module type."
