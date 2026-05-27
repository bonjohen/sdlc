# SDLC Implement Hardening — Product Design Review

## Gaps in Source Document

The user requirements document (`final.user.md`) is thorough. All seven concerns from its "Concerns for Physical Design" section are addressed below. Notable gaps:

- **No priority ordering among the 24 user stories.** All "Must" stories are treated equally. This PDR proposes a risk-first phase ordering (hook + prompt enforcement first, then expand restructuring, then dispatcher, then context lifecycle) because enforcement must exist before the other features have value.
- **US-007 (hook inactive during non-implement work) is marked "Should."** This PDR treats it as effectively "Must" because a hook that fires during normal development will be disabled by the user immediately, rendering US-005 useless.

---

## 1. Product Summary

Three prompt files (`skill/implement.md`, `skill/expand.md`, `skill/SKILL.md`) and one new Python hook script are modified or created to harden the SDLC pipeline's implement stage against lost status, context waste, and context exhaustion during multi-phase AI agent execution.

## 2. Product Intent

Make it impossible for an AI agent to write source code without first marking a task as `Started` in the phase plan file (enforced by a runtime hook), and make multi-phase runs sustainable by managing context lifecycle across phase boundaries and restructuring the master plan as a phase-level dashboard.

## 3. Planning Scope

| Artifact | Action | Location |
|----------|--------|----------|
| `skill/implement.md` | Rewrite | `C:\Projects\sdlc\skill\implement.md` |
| `skill/expand.md` | Modify | `C:\Projects\sdlc\skill\expand.md` |
| `skill/SKILL.md` | Modify | `C:\Projects\sdlc\skill\SKILL.md` |
| `pre-implement-status-guard.py` | Create | `C:\Users\boen3\.claude\hooks\pre-implement-status-guard.py` |
| `settings.json` | Modify | `C:\Users\boen3\.claude\settings.json` |

No new dependencies. No database. No API. No package layout changes. The "system" is markdown prompt files consumed by Claude Code and a Python hook script that runs on every Edit/Write tool call.

## 4. Primary Requirements Summary

| Area | Key Requirement | User Stories |
|------|----------------|-------------|
| Status enforcement | Phase plan updated per-task (Started before code, Completed after). Master plan updated per-phase. | US-001 – US-004 |
| Hook enforcement | Runtime hook blocks source file edits when no task is `Started` | US-005 – US-007 |
| Phase isolation | Read only current phase plan; no future-phase pre-reads | US-008 – US-010 |
| Context lifecycle | `/compact` between phases; 50% threshold; clean stop on failure | US-011 – US-014 |
| Crash recovery | Verify on-disk work for `Started` tasks; recovery annotations | US-015 – US-017 |
| Dispatcher | `phase NN all` mode; path parsing; context injection | US-018 – US-021 |
| Plan file structure | Expand moves task tables out of master plan; master becomes dashboard | US-022 – US-024 |

## 5. Operating Modes

The implement command operates in four modes. The first three exist today; the fourth is new.

| Mode | Invocation | Context lifecycle | Master plan update |
|------|-----------|------------------|-------------------|
| Single phase | `/sdlc implement` | No compaction | Once at phase end |
| Specific phase | `/sdlc implement phase NN` | No compaction | Once at phase end |
| All remaining | `/sdlc implement all` | Compact between phases | Once per phase |
| Start-at all (new) | `/sdlc implement phase NN all` | Compact between phases | Once per phase |

All modes share the same per-task status update rules (US-001–002) and hook enforcement (US-005). The context lifecycle rules (US-011–014) apply only to multi-phase modes ("all" and "phase NN all").

---

## 6. Hook Architecture

### 6.1 Design Decision: Sentinel-Based Activation (addresses Concern 7)

The hook must distinguish `/sdlc implement` sessions from normal work (US-007). Three options were evaluated:

| Option | Mechanism | Pros | Cons |
|--------|-----------|------|------|
| A. Sentinel file | Implement prompt creates `~/.claude/state/sdlc-implement.json`; hook checks for it | Explicit on/off; fast check; crash-safe | Sentinel lingers on crash; needs cleanup |
| B. Environment variable | Implement prompt sets `SDLC_IMPLEMENT_ACTIVE=1` via `$CLAUDE_ENV_FILE` | No file I/O | Persists across implement/non-implement work in same session |
| C. Convention-based | Hook scans for `phase*/plan.md` with `Started` tasks | No sentinel; always correct | Slow (file scan on every Edit/Write); breaks NFR-001 on large repos |

**Decision: Option A (sentinel file).** Rationale:

- Fast path for non-implement work: check file existence (< 1ms), exit 0 if absent.
- Explicit: the implement prompt controls activation/deactivation.
- Crash-safe enough: if the session crashes, the sentinel lingers, but the hook only blocks source file edits when no task is `Started`. A new session invoking `/sdlc implement` will find the `Started` task from the crashed session and proceed with recovery. For non-implement work after a crash, the user can delete the sentinel (same pattern as the push guard).

### 6.2 Sentinel File

**Path:** `~/.claude/state/sdlc-implement.json`

**Contents:**

```json
{
  "project_root": "C:/Projects/chatbot-factory",
  "phase_plan": "sdlc/plan/phase03/plan.md",
  "started_at": "2026-05-27 02:30 PM"
}
```

| Field | Type | Description |
|-------|------|-------------|
| project_root | string | Absolute path to the project root, forward slashes |
| phase_plan | string | Relative path from project_root to the active phase plan |
| started_at | string | PST timestamp when implement mode was activated |

**Lifecycle:**

1. **Create:** The implement prompt instructs the agent to create the sentinel at step 1 (before reading the phase plan), writing the project root and phase plan path.
2. **Update:** When advancing to the next phase in multi-phase mode, the agent updates `phase_plan` to the new phase's path.
3. **Delete:** The implement prompt instructs the agent to delete the sentinel when: (a) all phases complete, (b) the agent stops in single-phase mode, (c) the agent tells the user to `/clear`.
4. **Crash orphan:** If the session crashes, the sentinel lingers. The next `/sdlc implement` invocation overwrites it. For non-implement work, the sentinel's presence causes the hook to check the phase plan — but if no task is `Started` (because the crash left a task Started and the file still reflects that), the hook allows the edit. The recovery protocol (US-015) handles the stale `Started` task.

### 6.3 Hook Script: `pre-implement-status-guard.py`

**Registered for:** `PreToolUse` with matchers `Edit` and `Write`.

**Input:** JSON on stdin with `tool_name` ("Edit" or "Write") and `tool_input` containing `file_path`.

**Decision tree:**

```
1. Parse stdin JSON. On parse failure → exit 0 (fail open, NFR-002).
2. Extract file_path from tool_input.
3. Normalize file_path: replace backslashes with forward slashes, resolve to absolute.
4. Is file_path a plan file?
   → YES (matches */plan/phase*/plan.md, */docs/final.plan.md, */docs/draft.*.md)
   → exit 0 (always allow plan file edits, US-006).
5. Read sentinel at ~/.claude/state/sdlc-implement.json.
   → File doesn't exist → exit 0 (not in implement mode, US-007).
   → Parse failure → exit 0 (fail open, NFR-002).
6. Is file_path under sentinel.project_root?
   → NO → exit 0 (different project, not our concern).
7. Read sentinel.phase_plan (relative to project_root). Parse the task table.
   → Parse failure → exit 0 (fail open, NFR-002).
8. Does any task in the table have Status = "Started"?
   → YES → exit 0 (a task is active, agent may edit source files).
   → NO → exit 2 + stderr error message (BLOCKED).
```

**Error message (exit 2):**

```
BLOCKED: No task is marked 'Started' in the active phase plan.

The implement workflow requires updating the phase plan BEFORE editing
source files. Mark the next task as 'Started' in:
    {sentinel.project_root}/{sentinel.phase_plan}

Then retry this edit. This hook enforces US-005 from the user requirements.

To disable this hook (not recommended during /sdlc implement):
    rm ~/.claude/state/sdlc-implement.json
```

### 6.4 Task Table Parsing

The hook must parse a markdown table to find the Status column. The table format is:

```markdown
| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 03.1 | Completed | 2026-05-27 02:30 PM | 2026-05-27 02:45 PM | Create the service |
| 03.2 | Started | 2026-05-27 02:46 PM | | Implement the adapter |
| 03.3 | Open | | | Write tests |
```

Parsing algorithm:

1. Read the file. Find lines that start with `|` and contain `Status` (the header row).
2. Identify the column index of `Status` by splitting the header on `|`.
3. Skip the separator row (`|---|---|...`).
4. For each subsequent row, split on `|` and read the Status column.
5. If any cell contains `Started` (case-insensitive, stripped), return true.
6. If no `Started` found, return false.

Edge cases:
- Multiple tables in the file → parse all tables; any `Started` anywhere satisfies the check.
- Malformed table (missing columns, broken pipes) → fail open (exit 0).
- Empty file → fail open.
- `Blocked` status → treated as not-Started (the agent should not be editing source files for a blocked task).

### 6.5 Registration in `settings.json`

Add to the existing `hooks.PreToolUse` array:

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

The same script handles both Edit and Write — the tool_name is used only for logging, not for behavior branching.

### 6.6 Performance (NFR-001)

Critical path for non-implement work: steps 1–5 (parse JSON, normalize path, check plan file pattern, read sentinel file). If the sentinel doesn't exist, this is ~3ms. If it does exist, add ~5ms for JSON parse + file read + table parse. Well under 200ms.

Critical path for implement work: steps 1–8. The phase plan file read and parse add ~10ms for a typical plan file (50–200 lines). Total < 20ms.

---

## 7. Plan File Formats

### 7.1 Post-Expand Master Plan Format (addresses Concern 3)

After `expand` runs, `final.plan.md` is restructured. The task tables are moved into phase plans. What remains is a phase status dashboard.

**Pre-expand format (current):**

```markdown
## Phase 03: Build the Service Layer

**Goal:** Working service with CRUD operations.
**Depends on:** Phase 02.

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 03.1 | Open | | | Create service module |
| 03.2 | Open | | | Implement CRUD operations |
| 03.3 | Open | | | Write unit tests |

### Phase 03 Summary
_To be filled after completion._
```

**Post-expand format (new):**

```markdown
---
document: "Implementation Plan"
version: "1.0"
status: "final"
format: "dashboard"
...
---

# {Project Name} — Implementation Plan

## Phase Status

| Phase | Title | Plan | Status | Started | Completed | Commit |
|-------|-------|------|--------|---------|-----------|--------|
| 00 | Project Scaffold | [plan](../plan/phase00/plan.md) | not_started | | | |
| 01 | Data Model | [plan](../plan/phase01/plan.md) | not_started | | | |
| 02 | Core Components | [plan](../plan/phase02/plan.md) | not_started | | | |
| 03 | Service Layer | [plan](../plan/phase03/plan.md) | not_started | | | |

## Phase Summaries

_Summaries are appended here as phases complete._
```

**Column definitions:**

| Column | Values | Updated by |
|--------|--------|-----------|
| Phase | Zero-padded phase number | Expand (once) |
| Title | Phase title | Expand (once) |
| Plan | Relative link to `phase{NN}/plan.md` | Expand (once) |
| Status | `not_started` / `in_progress` / `complete` / `blocked` | Implement (at phase start and completion) |
| Started | PST timestamp | Implement (when first task starts) |
| Completed | PST timestamp | Implement (when phase commits) |
| Commit | Short hash (7 chars) | Implement (after commit) |

**Phase summaries** are appended below the status table as Markdown sections:

```markdown
### Phase 03 Summary

- **Changes:** Created `app/services/crud.py`, added 12 unit tests in `tests/test_crud.py`.
- **Commit:** `a1b2c3d` — Phase 03: Service layer with CRUD operations
```

### 7.2 Format Detection for Backward Compatibility (addresses Concern 5)

The implement prompt must handle both pre-expand (old) and post-expand (new) master plan formats. Detection:

```
If final.plan.md frontmatter contains `format: "dashboard"`:
    → New format. Task tables are in phase plans only.
    → Update phase status table at phase completion.

Else:
    → Old format. Task tables are in the master plan.
    → Update task rows in BOTH files per-task (legacy behavior).
    → Update phase summary in master plan at phase completion.
```

This is a frontmatter check — one line read, no complex parsing. The implement prompt includes both code paths with the detection logic at the top of the execution loop.

### 7.3 Expand Restructuring Mechanics (addresses Concern 3)

When `expand` generates phase plans, it performs these steps on `final.plan.md`:

1. Read the full master plan and parse all phases, tasks, goals, dependencies.
2. For each phase, generate `sdlc/plan/phase{NN}/plan.md` with the task table (existing behavior).
3. **New step:** Rewrite `final.plan.md`:
   a. Preserve the frontmatter, adding `format: "dashboard"`.
   b. Preserve the header, source references, work queue instructions, and technology stack.
   c. Replace each phase's task table with a single row in the Phase Status table.
   d. Add an empty `## Phase Summaries` section at the bottom.
   e. Preserve the Coverage Checklist if present.

The task table content is not lost — it now lives in the phase plans. The master plan links to them.

### 7.4 New Master Plan Columns (addresses Concern 4)

The `Commit` column is new. It is added by the expand step when restructuring the master plan. For projects that haven't re-expanded, this column doesn't exist — the implement prompt's old-format code path doesn't write to it.

This is not a migration. Old-format plans continue to work as-is. New-format plans get the column automatically when expand runs.

---

## 8. Component Design

### 8.1 `skill/implement.md` — Phase Implementor (rewrite)

- **What it does:** Directs the AI agent to execute implementation phases with enforced status tracking, phase isolation, context lifecycle, and crash recovery.
- **Serves:** US-001–004, US-008–017, US-024
- **Depends on:** `final.plan.md`, `phase{NN}/plan.md`, sentinel file
- **Depended on by:** `SKILL.md` (routes to it)

**Key changes from current `implement.md`:**

| Current behavior | New behavior | Rationale |
|-----------------|-------------|-----------|
| Update both plan files per-task | Update phase plan per-task; master plan per-phase | US-003, US-024 — two-level monitoring model |
| No enforcement language | HARD RULE callouts, violation definitions | US-004 — explicit prohibitions |
| No phase isolation | "Read only current phase" rule | US-008–010 — prevent context waste |
| No context lifecycle | `/compact` between phases, 50% threshold | US-011–014 — prevent context exhaustion |
| No crash recovery protocol | Verify on-disk work for `Started` tasks | US-015–017 — recover from interruptions |
| No sentinel management | Create/update/delete sentinel file | US-005–007 — hook activation |
| Handles one master plan format | Detects old vs new format, adjusts behavior | NFR-006 — backward compatibility |

**Structure of rewritten prompt:**

```
1. Prerequisites (verify plan files exist)
2. Format Detection (frontmatter check for "dashboard" format)
3. Sentinel Management (create/update/delete sdlc-implement.json)
4. Execution Loop
   4.1 Read State (identify active phase and task)
   4.2 Execute Tasks
       a. HARD RULE: Update phase plan → Started (before any work)
       b. Read Context section
       c. Do the work
       d. HARD RULE: Update phase plan → Completed (immediately after)
   4.3 Run Verification
   4.4 Update Master Plan (phase status → complete, summary, commit hash)
   4.5 Commit
   4.6 Context Lifecycle (compact between phases in multi-phase mode)
   4.7 Continue or Stop
5. Status Update Violations (explicit list of prohibited behaviors)
6. Crash Recovery Protocol
7. State Management Rules
8. Resumption
```

### 8.2 `skill/expand.md` — Phase Plan Expander (modify)

- **What it does:** Generates per-phase plan files from finalized documents. **New:** Also restructures the master plan into a phase-level dashboard.
- **Serves:** US-022–024
- **Depends on:** `final.plan.md`, `final.pdr.md`, `final.user.md`
- **Depended on by:** `implement.md` (reads its output)

**Key changes from current `expand.md`:**

| Current behavior | New behavior |
|-----------------|-------------|
| Copies task tables from master plan to phase plans | Same — task tables still go to phase plans |
| Leaves master plan unchanged | **Restructures master plan:** replaces task tables with Phase Status table, adds `format: "dashboard"` to frontmatter |
| No link between master plan and phase plans | Phase Status table includes relative links to phase plans |

**New section added to expand.md:**

```markdown
## Master Plan Restructuring

After generating all phase plans, restructure `final.plan.md`:

1. Add `format: "dashboard"` to the YAML frontmatter.
2. Replace each phase's task table with a row in a new Phase Status table
   (see Section 7.1 of the PDR for exact format).
3. Preserve: frontmatter, title, source references, work queue instructions,
   technology stack, coverage checklist.
4. Remove: individual task rows from the master plan (they now live in phase plans).
5. Add a `## Phase Summaries` section at the bottom (empty, filled by implement).
```

### 8.3 `skill/SKILL.md` — Dispatcher (modify)

- **What it does:** Routes `/sdlc <subcommand>` invocations to the correct prompt file.
- **Serves:** US-018–021
- **Depends on:** Nothing (entry point)
- **Depended on by:** All prompt files (receives routing from it)

**Key changes:**

1. **New dispatch mode (US-018):** Add `phase NN all` to the implement options table and routing logic.

2. **Path argument parsing (US-019, US-020):** Add a section to the dispatcher:

   ```markdown
   ### Plan file path parsing

   If the argument contains a path matching `phase{NN}` (with any separators),
   extract NN as the target phase number. Normalize backslashes to forward
   slashes before matching.

   Regex: `phase[/\\]?(\d{2})`

   - Path alone → `/sdlc implement phase NN`
   - Path + continuation language ("and proceed", "and continue",
     "and remaining", "all remaining") → `/sdlc implement phase NN all`
   ```

3. **Context injection (US-021):** When routing to `implement.md`, prepend:

   ```markdown
   "Update the phase plan file BEFORE starting each task (Started) and
   IMMEDIATELY after finishing each task (Completed). The master plan is
   updated once per phase at completion. Read only the current phase's
   plan — do not read future phase plans until the current phase is committed."
   ```

### 8.4 `pre-implement-status-guard.py` — PreToolUse Hook (create)

- **What it does:** Blocks Edit/Write tool calls to source files when no task is marked `Started` in the active phase plan.
- **Serves:** US-005–007, NFR-001–003
- **Depends on:** Sentinel file (`~/.claude/state/sdlc-implement.json`), phase plan file
- **Depended on by:** Nothing (standalone enforcement mechanism)

Full design in Section 6.3–6.5 above.

---

## 9. State Model

### 9.1 Implement Session States

```
Inactive ──[/sdlc implement]──> Reading State
                                     │
                   ┌─────────────────┘
                   ▼
             Phase Active ──[all tasks done]──> Verifying
                   │                                │
                   │                    ┌───────────┘
                   │                    ▼
                   │              Updating Master ──[commit]──> Phase Complete
                   │                                                 │
                   │                ┌────────────────────────────────┘
                   │                ▼
                   │          ┌── More phases? ──[yes]──> Compacting ──> Reading State
                   │          │
                   │          └── [no] ──> Cleanup ──> Inactive
                   │
                   └──[crash/abort]──> Orphaned ──[next /sdlc implement]──> Recovery
                                                                              │
                                                                    ┌────────┘
                                                                    ▼
                                                              Reading State
```

### 9.2 Task States (unchanged)

```
Open ──> Started ──> Completed
            │
            └──> Blocked ──> Started ──> Completed
```

### 9.3 Phase States in Master Plan (new)

```
not_started ──> in_progress ──> complete
                    │
                    └──> blocked
```

### 9.4 Sentinel States

```
Absent ──[implement starts]──> Present
Present ──[phase advance]──> Present (updated phase_plan)
Present ──[implement completes]──> Absent (deleted)
Present ──[session crash]──> Orphaned (lingers)
Orphaned ──[next /sdlc implement]──> Present (overwritten)
Orphaned ──[user deletes]──> Absent
```

---

## 10. Error Handling

| Error | Component | Behavior | Justification |
|-------|-----------|----------|--------------|
| stdin JSON parse failure | Hook | Exit 0 (allow) | NFR-002: fail open |
| Sentinel file parse failure | Hook | Exit 0 (allow) | NFR-002: fail open |
| Phase plan file not found | Hook | Exit 0 (allow) | NFR-002: fail open |
| Phase plan table parse failure | Hook | Exit 0 (allow) | NFR-002: fail open |
| Edit tool fails on plan file update | Implement prompt | Continue with implementation; recovery protocol handles the gap | Edit failures are rare; the work-exists-but-status-doesn't case is handled by FR-12 |
| Master plan format unrecognized | Implement prompt | Fall back to old-format behavior (update both files per-task) | NFR-006: backward compatibility |
| Sentinel file write fails | Implement prompt | Warn user; continue without hook enforcement | Hook is defense-in-depth; prompt rules still apply |
| `/compact` doesn't reduce context enough | Implement prompt | Stop and instruct user to `/clear` | US-014 |
| Phase plan missing for target phase | Implement prompt | Stop and tell user to run expand | Existing behavior, preserved |

---

## 11. Platform and Implementation Risks

### Risk 1: Prompt compliance under context pressure

- **What could go wrong:** Even with HARD RULE callouts, the agent may skip status updates when the context window is nearly full and the model is under pressure to produce output quickly.
- **Threatens:** US-001, US-002, US-004
- **Validated by:** The hook (US-005) provides runtime enforcement as a safety net.
- **Fallback:** The crash recovery protocol (US-015–017) handles the aftermath.

### Risk 2: Hook blocks legitimate work

- **What could go wrong:** The hook incorrectly blocks an edit that isn't part of `/sdlc implement` (false positive on sentinel detection or plan file parsing).
- **Threatens:** US-007, NFR-002
- **Validated by:** Fail-open design ensures parse failures allow the action. Sentinel-based activation means the hook is dormant during non-implement work.
- **Fallback:** User deletes the sentinel: `rm ~/.claude/state/sdlc-implement.json`.

### Risk 3: `/compact` is lossy

- **What could go wrong:** After `/compact`, the compaction model retains too much phase N context or loses critical state (branch name, plan file path, next phase number).
- **Threatens:** US-011, US-012, NFR-004
- **Validated by:** US-012 requires re-reading `final.plan.md` after compaction to confirm state. The focus phrase in the compact command steers the compaction model.
- **Fallback:** US-014 — if context is still > 50% after compaction, stop and tell the user to `/clear`.

### Risk 4: Expand restructuring corrupts the master plan

- **What could go wrong:** The expand prompt incorrectly parses or rewrites `final.plan.md`, losing content or producing malformed output.
- **Threatens:** US-022, US-023
- **Validated by:** The master plan is committed before expand runs (the finalize step commits it). If expand corrupts it, `git checkout sdlc/docs/final.plan.md` restores it.
- **Fallback:** Git is the safety net. The expand step should verify its output by re-reading the rewritten file.

---

## 12. Acceptance Criteria

Derived from user stories. Each criterion is testable by observing a `/sdlc implement` run.

| ID | Criterion | Traces to |
|----|-----------|----------|
| AC-01 | Every task shows an Edit call to `phase{NN}/plan.md` (Started) before its first source file edit | US-001, US-005 |
| AC-02 | Every task shows an Edit call to `phase{NN}/plan.md` (Completed) immediately after its last source file edit | US-002 |
| AC-03 | `final.plan.md` is updated once per phase (not per task) with status, timestamp, and commit hash | US-003 |
| AC-04 | The hook blocks a source file edit when no task is Started, with an explanatory error message | US-005 |
| AC-05 | The hook allows plan file edits regardless of task status | US-006 |
| AC-06 | The hook does not fire during non-implement work (no sentinel) | US-007 |
| AC-07 | In multi-phase mode, phase N+1's plan is read only after phase N is committed | US-008, US-009 |
| AC-08 | `/compact` runs after each phase commit in multi-phase mode | US-011 |
| AC-09 | After crash recovery, previously-started tasks with verified work are marked Completed with recovery annotation | US-015, US-016 |
| AC-10 | `/sdlc implement phase 03 all` starts at phase 03 and continues autonomously | US-018 |
| AC-11 | Post-expand `final.plan.md` contains a Phase Status table with no individual task rows | US-022 |
| AC-12 | Old-format master plans (no `format: "dashboard"`) still work with the implement prompt | NFR-006 |

---

## 13. Recommended Planning Phases

1. **Hook script + settings registration.** Create `pre-implement-status-guard.py`, register in `settings.json`, test sentinel lifecycle and plan file parsing. This is the foundation — all other changes are prompt-level and unenforceable without the hook.

2. **Implement prompt rewrite.** Rewrite `skill/implement.md` with: status enforcement (HARD RULE callouts, violation definitions), sentinel management, crash recovery protocol, format detection, two-level monitoring model (phase plan per-task, master plan per-phase).

3. **Dispatcher enhancements.** Modify `skill/SKILL.md`: add `phase NN all` mode, path argument parsing, context injection when routing to implement.

4. **Expand restructuring.** Modify `skill/expand.md`: add master plan restructuring step (Phase Status table, `format: "dashboard"` frontmatter, Phase Summaries section).

5. **Context lifecycle.** Add context lifecycle instructions to `implement.md`: `/compact` between phases, 50% threshold, clean stop on failure. This is last because it's prompt-only (no hook or format changes) and benefits from the other changes being in place.

6. **Verification.** End-to-end test: run `/sdlc expand` on the current I2I plan (from archive), then `/sdlc implement phase 01 all` and verify all acceptance criteria.

---

## 14. Concerns for Release Planning

1. **Phase 1 (hook) must be tested against the existing implement prompt before Phase 2 rewrites it.** The hook should work with both the current and rewritten implement prompt. Test with the current prompt first.

2. **Phase 4 (expand restructuring) is destructive to `final.plan.md`.** The plan must ensure Git commits before and after. If expand fails, `git checkout` recovers.

3. **Phase 2 (implement rewrite) is the largest single change** — the prompt goes from 173 lines to an estimated 300+ lines. Consider splitting it into sub-phases if the context budget is tight.

4. **The sentinel file lives outside the project directory** (`~/.claude/state/`). This is intentional (it's per-user, not per-project) but means it's not tracked by Git. If the user works on two projects simultaneously in different terminal tabs, the sentinel from project A could affect project B. The sentinel's `project_root` field mitigates this (the hook checks project membership), but the implement prompt must always overwrite the sentinel when starting, not append to it.

5. **NFR-006 (backward compatibility) means the implement prompt carries two code paths** (old-format and new-format) until all active projects have re-expanded. The plan should include a deprecation notice for the old format with a target date for removal.
