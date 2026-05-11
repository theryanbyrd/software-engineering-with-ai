# Agent guidance — LEGACY CODEBASE

This file is the cross-vendor (Claude Code, Cursor, Codex, others) version of `CLAUDE.md`. The full content is there; this is the summary.

## Read CLAUDE.md first

Before doing any work, read the full `CLAUDE.md`. The legacy version is significantly more restrictive than greenfield. Most paths are restricted by default.

## Quick reference

- **Verify:** `bash legacy-bridge-scripts/legacy-verify.sh <module>` — adapts to what's available
- **Discovery:** `bash legacy-bridge-scripts/discover.sh` — auto-detect what's in this repo
- **Default autonomy in legacy:** L1 (suggest only) or L2 (single-file edits with review)
- **Default PR size cap:** 100 lines (stricter than greenfield's 400)
- **Forbidden:** see `CLAUDE.md` § Forbidden — list is longer than greenfield

## The seven brownfield principles (Ch 11 §11.6)

1. Pick 1-2 high-leverage services
2. Establish a golden master
3. Build verify around the golden master
4. Strangler-pattern the AI work
5. Read-only AI for legacy first
6. AI-assisted documentation as side effect
7. Strict autonomy ceiling

If you find yourself violating any of these, stop and ask.
