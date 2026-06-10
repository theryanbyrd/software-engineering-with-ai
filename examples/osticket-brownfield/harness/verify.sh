#!/usr/bin/env bash
# verify.sh — the single "is this safe to look at" command for the osTicket harness.
# Ch 7: a green verify is necessary, not sufficient. Read the diff. Pull the trace.
#
# Usage: ./verify.sh /path/to/osticket-src
# Exit non-zero on the first failing gate.
set -euo pipefail

SRC="${1:-./osticket-src}"
HERE="$(cd "$(dirname "$0")" && pwd)"

echo "==> [1/3] PHP lint (syntax) on changed source"
# Lint every PHP file outside vendored libs. Fast, catches the dumbest regressions.
fail=0
while IFS= read -r f; do
  php -l "$f" >/dev/null || fail=1
done < <(find "$SRC/include" "$SRC/scp" "$SRC/api" -name '*.php' \
            -not -path '*/laminas-mail/*' -not -path '*/mpdf/*' -not -path '*/Spyc*' 2>/dev/null)
[ "$fail" -eq 0 ] || { echo "PHP lint failed"; exit 1; }
echo "    lint clean"

echo "==> [2/3] osTicket structural test suite (setup/test)"
if [ -f "$SRC/setup/test/run-tests.php" ]; then
  php "$SRC/setup/test/run-tests.php"
else
  echo "    (setup/test not found — skipping)"
fi

echo "==> [3/3] characterization tests (behavior we are standing next to)"
# These pin EXISTING behavior before we add TOTP. If TOTP work changes any of
# these, that is a regression to explain, not a test to edit away.
php "$HERE/characterization/test.2fa-email.php" "$SRC"

echo "==> verify OK (remember: necessary, not sufficient — now read the diff)"
