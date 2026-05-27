---
phase: 24
title: "Integration & Polish"
depends_on: "Phases 20-23 (all components must exist before integration verification)"
goal: "End-to-end behavior is verified, backward compatibility confirmed, cross-cutting consistency ensured across all modified artifacts."
source_pdr_sections: ["4.1", "4.2", "4.3", "4.4", "9", "10"]
source_user_stories: ["NFR-005", "NFR-006"]
status: "open"
---

# Phase 24: Integration & Polish

## Tasks

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 24.1 | Open | | | Read the rewritten `implement.md` and verify the old-format code path is complete: if a master plan lacks `format: "dashboard"`, the prompt uses dual-file per-task updates. Verify the new-format code path: phase plan per-task, master plan per-phase. |
| 24.2 | Open | | | Verify the sentinel lifecycle documentation in the hook script's docstring covers: creation, update on phase advance, deletion on completion, crash orphan behavior, manual cleanup instructions. |
| 24.3 | Open | | | Verify path consistency across all modified files: sentinel file path (`~/.claude/state/sdlc-implement.json`), plan file patterns (`*/plan/phase*/plan.md`), status values (`Open`/`Started`/`Completed`/`Blocked` in phase plans; `not_started`/`in_progress`/`complete`/`blocked` in master plan), timestamp format (PST). |
| 24.4 | Open | | | Verify all path references use forward slashes or handle both separators. No file should reference a path using only backslashes. Check: hook script, implement prompt, dispatcher, expand prompt. |
| 24.5 | Open | | | Update the project `CLAUDE.md` to document the new hook (`pre-implement-status-guard.py`): what it does, where it lives, how to disable it, and its relationship to the sentinel file. |

## Context

### Files to Review

- `~/.claude/hooks/pre-implement-status-guard.py` — Created in Phase 20. Verify docstring, sentinel lifecycle docs, path handling.
- `skill/implement.md` — Rewritten in Phase 21. Verify both format code paths, sentinel references, status values.
- `skill/SKILL.md` — Modified in Phase 22. Verify path parsing, context injection, mode routing.
- `skill/expand.md` — Modified in Phase 23. Verify restructuring output format, Phase Status table columns.
- `CLAUDE.md` — Project-level instructions. Needs hook documentation added.

### Cross-Cutting Consistency Checks

**Sentinel file path must be identical in:**
- Hook script (reads from this path)
- Implement prompt (creates/updates/deletes at this path)
- Hook error message (tells user how to disable)

Expected: `~/.claude/state/sdlc-implement.json`

**Plan file patterns must be consistent in:**
- Hook script (plan file detection — always allow)
- Implement prompt (reads phase plans)
- Dispatcher (path argument parsing)
- Expand prompt (generates phase plans, restructures master plan)

Expected patterns: `sdlc/plan/phase{NN}/plan.md`, `sdlc/docs/final.plan.md`

**Status values must be consistent:**

| File type | Status values |
|-----------|--------------|
| Phase plan task tables | `Open`, `Started`, `Completed`, `Blocked` |
| Master plan Phase Status table (new format) | `not_started`, `in_progress`, `complete`, `blocked` |

**Timestamp format:** PST, `YYYY-MM-DD HH:MM AM/PM` — consistent across all files.

**Path separator handling:**
- Hook: normalizes backslashes to forward slashes (step 3)
- Dispatcher: normalizes before regex matching
- Implement prompt: uses forward slashes in all references
- Expand prompt: uses forward slashes in relative links

### CLAUDE.md Update

Add to the project `CLAUDE.md` under a new section (or under an existing relevant section):

```markdown
## Implement Status Guard Hook

A `PreToolUse` hook at `~/.claude/hooks/pre-implement-status-guard.py` enforces
status-before-implementation during `/sdlc implement`. It blocks Edit/Write calls
to source files when no task is marked `Started` in the active phase plan.

- **Activated by:** sentinel file at `~/.claude/state/sdlc-implement.json`
  (created automatically by the implement prompt)
- **Deactivated by:** deleting the sentinel:
  `rm ~/.claude/state/sdlc-implement.json`
- **Behavior:** Blocks source file edits only. Plan file edits always allowed.
  Fails open on all errors (never blocks legitimate work due to a bug).
- **Registered in:** `~/.claude/settings.json` (Edit and Write matchers)
```

### Design Notes

- **This phase is verification, not implementation.** Read files, check consistency, fix discrepancies. The only new content is the CLAUDE.md update.
- **Old-format backward compatibility (NFR-006)** is the highest-risk verification item. The implement prompt must have a complete, working code path for plans without `format: "dashboard"`. This means: per-task updates in both `final.plan.md` and `phase{NN}/plan.md`, phase summary in master plan at phase completion.
- **The hook's docstring is its documentation.** Since the hook lives outside the project directory (`~/.claude/hooks/`), it can't reference project docs. The docstring must be self-contained: what the hook does, how the sentinel works, how to disable it.

### Verification

- [ ] Old-format `final.plan.md` (no `format: "dashboard"`) is correctly described by the implement prompt with dual-file per-task updates
- [ ] New-format `final.plan.md` (with `format: "dashboard"`) is correctly described by the implement prompt with phase plan per-task, master plan per-phase
- [ ] The sentinel file path `~/.claude/state/sdlc-implement.json` is identical in: hook script, implement prompt, hook error message
- [ ] Plan file patterns are consistent across: hook script, implement prompt, dispatcher, expand prompt
- [ ] No file references a path using only backslashes
- [ ] Status values are consistent: `Open`/`Started`/`Completed`/`Blocked` in phase plans; `not_started`/`in_progress`/`complete`/`blocked` in master plan Phase Status table
- [ ] `CLAUDE.md` documents the hook, sentinel, and disable instructions

## Phase Summary

_To be filled after completion._

- **Changes:** TBD
- **Commit:** TBD
