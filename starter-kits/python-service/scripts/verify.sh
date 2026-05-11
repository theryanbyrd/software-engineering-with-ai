#!/usr/bin/env bash
# verify — wrapper for CI. Delegates to Makefile so there's one source of truth.
set -euo pipefail
cd "$(dirname "$0")/.."
exec make verify
