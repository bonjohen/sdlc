---
phase: 20
title: "Hook & Sentinel"
depends_on: "none"
goal: "A working PreToolUse hook blocks source file edits when no task is marked Started in the active phase plan. The sentinel-based activation mechanism is operational."
source_pdr_sections: ["4.1", "2.1", "6.1"]
source_user_stories: ["US-005", "US-006", "US-007", "NFR-001", "NFR-002", "NFR-003"]
status: "open"
---

# Phase 20: Hook & Sentinel

## Tasks

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 20.1 | Completed | 2026-05-27 01:15 PM | 2026-05-27 01:18 PM | Create `~/.claude/hooks/pre-implement-status-guard.py` with the decision tree from PDR 4.1: parse stdin JSON, normalize path, check plan file pattern, read sentinel, check project membership, parse task table, allow or block. All error paths exit 0 (fail open). |
| 20.2 | Completed | 2026-05-27 01:18 PM | 2026-05-27 01:19 PM | Implement task table parsing per PDR 4.1: find header row with `Status` column, identify column index, scan data rows for `Started` value. Handle multiple tables, malformed tables (fail open), empty files. |
| 20.3 | Completed | 2026-05-27 01:19 PM | 2026-05-27 01:19 PM | Implement plan file detection: paths matching `*/plan/phase*/plan.md`, `*/docs/final.plan.md`, `*/docs/draft.*.md` are always allowed (exit 0). |
| 20.4 | Completed | 2026-05-27 01:19 PM | 2026-05-27 01:20 PM | Implement path normalization for Windows (NFR-003): replace backslashes with forward slashes, handle both `C:\` and `/c/` prefixes, resolve to absolute path. |
| 20.5 | Completed | 2026-05-27 01:20 PM | 2026-05-27 01:21 PM | Register the hook in `~/.claude/settings.json` with `Edit` and `Write` matchers per PDR 4.1. Two new PreToolUse entries pointing to `python C:/Users/boen3/.claude/hooks/pre-implement-status-guard.py`. **Note: writes to `~/.claude/settings.json` (outside project directory) — authorized by user.** |
| 20.6 | Completed | 2026-05-27 01:21 PM | 2026-05-27 01:25 PM | Manual test: (a) no sentinel, edit a `.py` file, allowed; (b) create sentinel pointing to a plan with a `Started` task, edit source, allowed; (c) create sentinel pointing to a plan with no `Started` task, edit source, blocked with error message; (d) edit `phase{NN}/plan.md`, allowed regardless; (e) malformed sentinel JSON, allowed (fail open); (f) sentinel for different project, allowed. |

## Context

### Files to Create or Modify

- `~/.claude/hooks/pre-implement-status-guard.py` — **Create.** New PreToolUse hook script. Follows the same pattern as the existing push guard at `~/.claude/hooks/pre-bash-git-push-guard.py` (sentinel-based, JSON stdin, exit 0/2).
- `~/.claude/settings.json` — **Modify.** Add two new entries to the `hooks.PreToolUse` array: one with matcher `Edit`, one with matcher `Write`, both pointing to the same script.

### Key Patterns and Imports

**Existing push guard pattern** (`~/.claude/hooks/pre-bash-git-push-guard.py`):

```python
import sys
import json
import os

# Read JSON from stdin
data = json.loads(sys.stdin.read())
tool_name = data.get("tool_name", "")
tool_input = data.get("tool_input", {})

# Decision logic...

# Allow:
sys.exit(0)

# Block:
print("BLOCKED: ...", file=sys.stderr)
sys.exit(2)
```

The new hook follows this exact pattern but checks:
1. `tool_input.file_path` (for Edit) or `tool_input.file_path` (for Write)
2. Whether the path is a plan file (always allow)
3. Whether the sentinel exists (if not, allow — not in implement mode)
4. Whether the file is under the sentinel's `project_root`
5. Whether any task in the phase plan has `Status = "Started"`

**Sentinel file format** (`~/.claude/state/sdlc-implement.json`):

```json
{
  "project_root": "C:/Projects/chatbot-factory",
  "phase_plan": "sdlc/plan/phase03/plan.md",
  "started_at": "2026-05-27 02:30 PM"
}
```

**Hook decision tree (8 steps):**

```
1. Parse stdin JSON → on failure: exit 0
2. Extract file_path from tool_input
3. Normalize: backslashes → forward slashes, resolve absolute
4. Plan file check: matches */plan/phase*/plan.md, */docs/final.plan.md,
   */docs/draft.*.md → exit 0
5. Read sentinel → missing: exit 0; parse fail: exit 0
6. Is file under sentinel.project_root? → NO: exit 0
7. Read phase plan, parse task table → parse fail: exit 0
8. Any task Started? → YES: exit 0; NO: exit 2 + error
```

**Task table parsing algorithm:**

1. Read the phase plan file line by line.
2. Find lines starting with `|` that contain the word `Status` (case-insensitive) — this is the header row.
3. Split the header on `|`, strip whitespace from each cell, find the index of `Status`.
4. Skip the next line (separator row: `|---|---|...`).
5. For each subsequent row starting with `|`, split on `|` and read the cell at the Status column index.
6. If any cell value (stripped, case-insensitive) equals `started`, return true.
7. If the file has multiple tables, parse all of them — any `Started` anywhere satisfies.
8. On any parse error (missing columns, broken pipes, empty file): return true (fail open).

**Error message format (exit 2):**

```
BLOCKED: No task is marked 'Started' in the active phase plan.

The implement workflow requires updating the phase plan BEFORE editing
source files. Mark the next task as 'Started' in:
    {sentinel.project_root}/{sentinel.phase_plan}

Then retry this edit. This hook enforces US-005 from the user requirements.

To disable this hook (not recommended during /sdlc implement):
    rm ~/.claude/state/sdlc-implement.json
```

**settings.json registration** — add to existing `hooks.PreToolUse` array:

```json
{
  "matcher": "Edit",
  "hooks": [
    {
      "type": "command",
      "command": "python C:/Users/boen3/.claude/hooks/pre-implement-status-guard.py"
    }
  ]
},
{
  "matcher": "Write",
  "hooks": [
    {
      "type": "command",
      "command": "python C:/Users/boen3/.claude/hooks/pre-implement-status-guard.py"
    }
  ]
}
```

### Design Notes

- **Fail-open is non-negotiable (NFR-002).** Every error path — stdin parse failure, sentinel missing, sentinel malformed, plan file missing, table parse failure — must exit 0. The only exit 2 path is: sentinel exists AND file is under project_root AND file is not a plan file AND no task has Status = `Started`.
- **Performance budget (NFR-001): < 200ms.** Non-implement path (sentinel absent) is ~3ms. Full implement path (sentinel + table parse) is < 20ms. No regex compilation per invocation; simple string splitting only.
- **The sentinel file lives outside the project directory** (`~/.claude/state/`). This is intentional — it's per-user session state, not project data. The implement prompt manages its lifecycle; the hook only reads it.
- **Windows path normalization (NFR-003):** The hook receives paths from Claude Code that may use either `\` or `/`. Normalize to forward slashes before all matching. Handle both `C:\Projects\...` and `/c/Projects/...` (Git Bash style).
- **Plan file detection uses glob-style matching**, not regex. Patterns: `*/plan/phase*/plan.md`, `*/docs/final.plan.md`, `*/docs/draft.*.md`. These must match regardless of path separator.
- **The hook script uses only Python standard library**: `sys`, `json`, `os`, `pathlib`. No external dependencies.
- **Task 20.5 writes to `~/.claude/settings.json`**, which is outside the project directory. The user has authorized this as part of the implement hardening project scope.

### Verification

- [ ] With no sentinel file: `Edit` a `.py` file — hook exits 0, edit proceeds
- [ ] With sentinel + `Started` task: `Edit` a source file — hook exits 0, edit proceeds
- [ ] With sentinel + no `Started` task: `Edit` a source file — hook exits 2, error message on stderr
- [ ] `Edit` `phase{NN}/plan.md` with sentinel + no `Started` task — hook exits 0, plan file edit allowed
- [ ] Malformed sentinel JSON — hook exits 0 (fail open)
- [ ] Sentinel pointing to different `project_root` — hook exits 0 (not our project)
- [ ] Empty phase plan file — hook exits 0 (fail open)
- [ ] `~/.claude/settings.json` contains two new PreToolUse entries (Edit matcher, Write matcher)
- [ ] Hook completes in < 200ms for all test cases (use `time python ...` to verify)

## Phase Summary

- **Changes:** Created `~/.claude/hooks/pre-implement-status-guard.py` with 8-step decision tree (parse stdin, normalize path, plan file detection, sentinel read, project membership, task table parsing, allow/block). Registered hook in `~/.claude/settings.json` with Edit and Write matchers. All error paths fail open. Verified with 6 manual test scenarios.
- **Commit:** `Phase 20: Hook & Sentinel — implement status guard hook with fail-open design`
