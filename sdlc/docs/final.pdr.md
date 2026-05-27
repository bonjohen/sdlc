---
document: "Physical Design Requirements"
version: "1.0"
status: "final"
source: "sdlc/docs/draft.pdr.md"
user_requirements: "sdlc/docs/final.user.md"
finalized_date: "2026-05-27"
---

# SDLC Implement Hardening — Physical Design Requirements

**Source document:** `sdlc/docs/final.user.md`
**Project root:** `C:\Projects\sdlc`
**Date:** 2026-05-27

## Gaps in Source Document

The draft PDR (`draft.pdr.md`) is thorough. All seven concerns from the user requirements' "Concerns for Physical Design" section are addressed. Two gaps identified:

- **NFR-005 (idempotency) has no explicit design response.** The draft PDR does not describe what happens when `/sdlc implement` is invoked on a fully completed plan. The implement prompt must detect "no Open or Started tasks remain" and exit cleanly without modifications. <!-- Added during finalization: explicit idempotency handling -->
- **`_standards.md` does not exist on disk.** Both `implement.md` and `expand.md` reference it. The draft PDR acknowledges this but does not propose creating it. This PDR treats it as out of scope per the user requirements (Section 6: "Creating `_standards.md`" is out of scope).

---

## 1. System Context

### 1.1 Existing Infrastructure to Reuse

| Asset | Location | Reuse Strategy |
|-------|----------|---------------|
| `skill/implement.md` | `C:\Projects\sdlc\skill\implement.md` | Rewrite in place (173 lines → ~300+ lines) |
| `skill/expand.md` | `C:\Projects\sdlc\skill\expand.md` | Modify — add master plan restructuring step |
| `skill/SKILL.md` | `C:\Projects\sdlc\skill\SKILL.md` | Modify — add dispatch mode, path parsing, context injection |
| Push guard hook | `C:\Users\boen3\.claude\hooks\pre-bash-git-push-guard.py` | Pattern reference — sentinel-based activation, JSON stdin, exit 0/2 |
| `settings.json` | `C:\Users\boen3\.claude\settings.json` | Modify — add Edit and Write hook registrations |
| `~/.claude/state/` directory | `C:\Users\boen3\.claude\state\` | Reuse — sentinel files stored here (same as push guard) |

### 1.2 New Dependencies

| Package | Purpose | Version Constraint | License |
|---------|---------|-------------------|---------|
| Python 3 (system) | Hook script runtime | ≥ 3.8 (already installed) | PSF |

No new dependencies. The hook uses only Python standard library (`sys`, `json`, `os`, `pathlib`).

### 1.3 Configuration

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| Sentinel file path | File path | `~/.claude/state/sdlc-implement.json` | Signals that `/sdlc implement` is active; checked by hook |
| Hook script path | File path | `~/.claude/hooks/pre-implement-status-guard.py` | PreToolUse hook for Edit and Write matchers |
| Plan file pattern | Regex | `*/plan/phase*/plan.md`, `*/docs/final.plan.md`, `*/docs/draft.*.md` | Paths always allowed by the hook (never blocked) |

---

## 2. State Model

This project has no database. All state is stored in markdown plan files (committed to Git) and one ephemeral JSON sentinel file (not committed).

### 2.1 Sentinel File: `sdlc-implement.json`

**Path:** `~/.claude/state/sdlc-implement.json`

```json
{
  "project_root": "C:/Projects/chatbot-factory",
  "phase_plan": "sdlc/plan/phase03/plan.md",
  "started_at": "2026-05-27 02:30 PM"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `project_root` | string | Absolute path to the project root, forward slashes |
| `phase_plan` | string | Relative path from `project_root` to the active phase plan |
| `started_at` | string | PST timestamp when implement mode was activated |

**Lifecycle:**

| Transition | Trigger | Action |
|-----------|---------|--------|
| Absent → Present | Implement prompt starts | Create with project root and first phase plan path |
| Present → Present (updated) | Phase advance in multi-phase mode | Update `phase_plan` to next phase's path |
| Present → Absent | All phases complete, or single-phase stop, or clean stop | Delete the file |
| Present → Orphaned | Session crash | File lingers; next `/sdlc implement` overwrites it |
| Orphaned → Present | Next `/sdlc implement` invocation | Overwrite with current session's data |
| Orphaned → Absent | User manual cleanup | `rm ~/.claude/state/sdlc-implement.json` |

### 2.2 Plan File State

Task states within phase plans (unchanged from existing convention):

```
Open ──> Started ──> Completed
            │
            └──> Blocked ──> Started ──> Completed
```

Phase states in the master plan (new, post-expand dashboard format only):

```
not_started ──> in_progress ──> complete
                    │
                    └──> blocked
```

### 2.3 Implement Session States

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

---

## 3. Package Layout

```
C:\Projects\sdlc\
├── skill/
│   ├── SKILL.md          ← Dispatcher (modify: add phase NN all, path parsing, context injection)
│   ├── implement.md      ← Phase implementor (rewrite: status enforcement, sentinel, recovery)
│   └── expand.md         ← Phase plan expander (modify: master plan restructuring)
│
C:\Users\boen3\.claude\
├── hooks/
│   └── pre-implement-status-guard.py  ← PreToolUse hook (create)
├── settings.json                      ← Hook registration (modify: add Edit/Write entries)
└── state/
    └── sdlc-implement.json            ← Sentinel file (created/deleted at runtime)
```

---

## 4. Component Designs

### 4.1 `pre-implement-status-guard.py` — PreToolUse Hook

- **Purpose:** Block Edit/Write tool calls to source files when no task is marked `Started` in the active phase plan.
- **Location:** `~/.claude/hooks/pre-implement-status-guard.py`
- **Implements:** US-005, US-006, US-007, NFR-001, NFR-002, NFR-003
- **Interface:** Stdin JSON (`tool_name`, `tool_input.file_path`) → exit 0 (allow) or exit 2 + stderr (block)
- **Behavior:**

  **Decision tree:**

  1. Parse stdin JSON. On parse failure → exit 0 (fail open, NFR-002).
  2. Extract `file_path` from `tool_input`.
  3. Normalize `file_path`: replace backslashes with forward slashes, resolve to absolute (NFR-003).
  4. Is `file_path` a plan file? Matches `*/plan/phase*/plan.md`, `*/docs/final.plan.md`, `*/docs/draft.*.md` → exit 0 (always allow plan file edits, US-006).
  5. Read sentinel at `~/.claude/state/sdlc-implement.json`. File doesn't exist → exit 0 (not in implement mode, US-007). Parse failure → exit 0 (fail open, NFR-002).
  6. Is `file_path` under `sentinel.project_root`? NO → exit 0 (different project).
  7. Read `sentinel.phase_plan` (relative to `project_root`). Parse the task table. Parse failure → exit 0 (fail open, NFR-002).
  8. Does any task have Status = `Started`? YES → exit 0 (allow). NO → exit 2 + error message (block).

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

  **Task table parsing algorithm:**

  1. Read the phase plan file. Find lines starting with `|` that contain `Status` (header row).
  2. Split header on `|`, identify the column index of `Status`.
  3. Skip the separator row (`|---|---|...`).
  4. For each data row, split on `|` and read the Status column value.
  5. If any cell contains `Started` (case-insensitive, stripped), return true.
  6. Multiple tables → parse all; any `Started` satisfies. Malformed/empty → fail open.

- **Dependencies:** Reads sentinel file and phase plan file. No external dependencies.
- **Performance (NFR-001):** Non-implement path (sentinel absent): ~3ms. Implement path (sentinel present, table parse): < 20ms. Well under 200ms target.

### 4.2 `skill/implement.md` — Phase Implementor (rewrite)

- **Purpose:** Direct the AI agent to execute implementation phases with enforced status tracking, phase isolation, context lifecycle, crash recovery, and sentinel management.
- **Location:** `C:\Projects\sdlc\skill\implement.md`
- **Implements:** US-001–004, US-008–017, US-024, NFR-004–006
- **Interface:** Read by Claude Code when `/sdlc implement` is invoked. Produces code, plan file updates, Git commits.
- **Behavior:**

  **Prompt structure (rewritten):**

  ```
  1. Prerequisites
     - Verify plan files exist
     - Format detection: frontmatter check for `format: "dashboard"`
  2. Sentinel Management
     - Create sdlc-implement.json at start
     - Update on phase advance
     - Delete on completion or clean stop
  3. Execution Loop
     3.1 Read State (identify active phase and task)
     3.2 Execute Tasks
         a. HARD RULE: Update phase plan → Started (before any work)
         b. Read Context section
         c. Do the work
         d. HARD RULE: Update phase plan → Completed (immediately after)
     3.3 Run Verification
     3.4 Update Master Plan (phase status, summary, commit hash)
     3.5 Commit
     3.6 Context Lifecycle (compact between phases in multi-phase mode)
     3.7 Continue or Stop
  4. Status Update Violations (explicit prohibited behaviors)
     - Batching updates across tasks
     - Skipping Started state
     - Deferring updates to after verification
  5. Crash Recovery Protocol
     - Detect Started tasks on resume
     - Verify on-disk work exists
     - Mark Completed with [recovered from interrupted session] annotation
     - Re-implement if work not found
  6. Phase Isolation Rules
     - Read only current phase plan
     - No future-phase pre-reads
     - No exploratory agents before implementation
  7. Context Lifecycle (multi-phase modes only)
     - /compact with focus phrase after each phase commit
     - Re-read final.plan.md after compaction
     - 50% context threshold for self-compaction
     - Clean stop if compact insufficient
  8. Format Detection
     - Dashboard format: phase plan per-task, master plan per-phase
     - Old format: dual-file per-task updates (backward compatibility)
  9. Idempotency
     - Fully completed plan: report "all phases complete", no modifications
  ```

  **Key behavioral rules:**

  | Rule | Enforcement | Traces to |
  |------|------------|-----------|
  | Started before code | HARD RULE callout + hook blocks violation | US-001, US-005 |
  | Completed immediately after | HARD RULE callout | US-002 |
  | Master plan per-phase only | Two-level monitoring model | US-003, US-024 |
  | No batching, no skipping, no deferring | Explicit violations list | US-004 |
  | Read only current phase | Phase isolation section | US-008–010 |
  | Compact between phases | Context lifecycle section | US-011–013 |
  | Clean stop on compact failure | Stop instruction with user guidance | US-014 |
  | Verify work before completing | Crash recovery protocol | US-015–017 |
  | Detect plan format | Frontmatter check | NFR-006 |

- **Dependencies:** Reads `final.plan.md`, `phase{NN}/plan.md`. Writes sentinel file. Invokes `/compact`. Runs Git commit.
- **Depended on by:** `SKILL.md` (routes to it)

### 4.3 `skill/expand.md` — Phase Plan Expander (modify)

- **Purpose:** Generate per-phase plan files from finalized documents. **New:** Restructure the master plan into a phase-level dashboard after generating phase plans.
- **Location:** `C:\Projects\sdlc\skill\expand.md`
- **Implements:** US-022, US-023, US-024
- **Interface:** Read by Claude Code when `/sdlc expand` is invoked. Produces `phase{NN}/plan.md` files and restructured `final.plan.md`.
- **Behavior:**

  **Existing behavior (preserved):** Copy task tables from `final.plan.md` to `phase{NN}/plan.md` files with full context sections.

  **New behavior (added):**

  After generating all phase plans, restructure `final.plan.md`:

  1. Add `format: "dashboard"` to the YAML frontmatter.
  2. Replace each phase's task table with a row in a new Phase Status table:

     | Phase | Title | Plan | Status | Started | Completed | Commit |
     |-------|-------|------|--------|---------|-----------|--------|
     | 00 | {title} | [plan](../plan/phase00/plan.md) | not_started | | | |

     Column definitions:

     | Column | Values | Updated by |
     |--------|--------|-----------|
     | Phase | Zero-padded phase number | Expand (once) |
     | Title | Phase title | Expand (once) |
     | Plan | Relative link to phase plan | Expand (once) |
     | Status | `not_started` / `in_progress` / `complete` / `blocked` | Implement |
     | Started | PST timestamp | Implement (when first task starts) |
     | Completed | PST timestamp | Implement (when phase commits) |
     | Commit | Short hash (7 chars) | Implement (after commit) |

  3. Preserve: frontmatter (plus new field), title, source references, work queue instructions, technology stack, coverage checklist.
  4. Remove: individual task rows (now in phase plans only).
  5. Add `## Phase Summaries` section at bottom (empty, filled by implement).
  6. Verification: re-read the rewritten file, confirm Phase Status table has one row per phase.

- **Dependencies:** Reads `final.plan.md`, `final.pdr.md`, `final.user.md`.
- **Depended on by:** `implement.md` (reads its output)

### 4.4 `skill/SKILL.md` — Dispatcher (modify)

- **Purpose:** Route `/sdlc <subcommand>` invocations to the correct prompt file.
- **Location:** `C:\Projects\sdlc\skill\SKILL.md`
- **Implements:** US-018, US-019, US-020, US-021
- **Interface:** Read by Claude Code when `/sdlc` is invoked. Routes to prompt files.
- **Behavior changes:**

  1. **New dispatch mode (US-018):** Add `phase NN all` to implement options table:

     | Invocation | Behavior |
     |------------|----------|
     | `/sdlc implement phase NN all` | Start at phase NN, continue through all remaining phases autonomously |

  2. **Path argument parsing (US-019, US-020):**

     If the argument contains a path matching `phase{NN}` (with any separators), extract NN as the target phase number. Normalize backslashes to forward slashes before matching.

     Regex: `phase[/\\]?(\d{2})`

     - Path alone → single-phase mode
     - Path + continuation language ("and proceed", "and continue", "and remaining", "all remaining") → `phase NN all` mode

  3. **Context injection (US-021):** When routing to `implement.md`, prepend:

     > "Update the phase plan file BEFORE starting each task (Started) and IMMEDIATELY after finishing each task (Completed). The master plan is updated once per phase at completion. Read only the current phase's plan — do not read future phase plans until the current phase is committed."

- **Dependencies:** None (entry point).
- **Depended on by:** All prompt files receive routing from it.

---

## 5. API Specification

Not applicable. This project modifies prompt files and creates a hook script. There are no API endpoints, HTTP services, or programmatic interfaces. The "interface" is the `/sdlc` skill invocation in Claude Code.

---

## 6. Security Design

### 6.1 Fail-Open Design (NFR-002)

The hook must never block legitimate work due to a bug. Every error path exits 0 (allow):

| Error | Action |
|-------|--------|
| stdin JSON parse failure | exit 0 |
| Sentinel file missing | exit 0 |
| Sentinel file parse failure | exit 0 |
| Phase plan file not found | exit 0 |
| Phase plan table parse failure | exit 0 |
| File path outside project root | exit 0 |

The only exit 2 (block) path: sentinel exists AND file is under project root AND file is not a plan file AND no task has Status = `Started`.

### 6.2 Sentinel as Single Point of Control

The sentinel file is the sole mechanism for hook activation. Removing it (`rm ~/.claude/state/sdlc-implement.json`) immediately disables enforcement. This is intentional — the user must always be able to escape.

### 6.3 No Secrets

No API keys, tokens, or credentials are involved. The hook reads local files only. The sentinel contains only file paths and a timestamp.

---

## 7. Observability

### 7.1 Hook Error Messages

The hook produces structured error messages on stderr when blocking (exit 2). The message includes:
- What happened ("No task is marked 'Started'")
- What to do ("Mark the next task as 'Started' in: {path}")
- How to disable ("rm ~/.claude/state/sdlc-implement.json")

### 7.2 Plan File as Observability

The plan files themselves are the observability mechanism. The human operator monitors:
- `phase{NN}/plan.md` — step-level progress (per-task Started/Completed timestamps)
- `final.plan.md` — phase-level progress (per-phase status, timestamps, commit hashes)

Both files are committed to Git, providing a durable audit trail.

### 7.3 Sentinel as Session Indicator

The existence of `~/.claude/state/sdlc-implement.json` indicates an active implement session. Its `phase_plan` field shows which phase is in progress. The human operator can inspect it to understand hook state.

---

## 8. Test Strategy

### 8.1 Behavioral Testing

This project has no automated test suite. All artifacts are markdown prompt files consumed by AI agents — their correctness is verified by observing agent behavior during `/sdlc implement` runs.

**Verification approach:** Run `/sdlc expand` then `/sdlc implement` against a real project plan and verify the acceptance criteria from Section 12 of the draft PDR.

### 8.2 Hook Manual Testing

The hook script can be tested directly:

1. **Sentinel absent:** Run any Edit/Write → hook exits 0 (no interference).
2. **Sentinel present, task Started:** Create sentinel pointing to a plan with a `Started` task → Edit source file → hook exits 0 (allowed).
3. **Sentinel present, no Started task:** Create sentinel pointing to a plan with only `Open`/`Completed` tasks → Edit source file → hook exits 2 (blocked).
4. **Plan file edit:** Create sentinel → Edit `phase{NN}/plan.md` → hook exits 0 (plan files always allowed).
5. **Malformed sentinel:** Write invalid JSON to sentinel → Edit source file → hook exits 0 (fail open).
6. **Cross-project:** Create sentinel for project A → Edit file in project B → hook exits 0 (different project).

### 8.3 Prompt Verification Criteria

The rewritten `implement.md` must contain (verifiable by text search):

- HARD RULE callouts for Started and Completed updates
- Explicit violations list (batching, skipping Started, deferring)
- Sentinel create/update/delete instructions
- Format detection logic (frontmatter check)
- Phase isolation rules
- Context lifecycle instructions (compact, 50% threshold, clean stop)
- Crash recovery protocol

---

## 9. Error Handling

| Error | Component | Behavior | Justification |
|-------|-----------|----------|--------------|
| stdin JSON parse failure | Hook | Exit 0 (allow) | NFR-002: fail open |
| Sentinel file parse failure | Hook | Exit 0 (allow) | NFR-002: fail open |
| Phase plan file not found | Hook | Exit 0 (allow) | NFR-002: fail open |
| Phase plan table parse failure | Hook | Exit 0 (allow) | NFR-002: fail open |
| Edit tool fails on plan file update | Implement prompt | Continue with implementation; recovery protocol handles the gap | Edit failures are rare; FR-12 handles work-exists-but-status-doesn't |
| Master plan format unrecognized | Implement prompt | Fall back to old-format behavior (update both files per-task) | NFR-006: backward compatibility |
| Sentinel file write fails | Implement prompt | Warn user; continue without hook enforcement | Hook is defense-in-depth; prompt rules still apply |
| `/compact` doesn't reduce context enough | Implement prompt | Stop and instruct user to `/clear` and re-invoke | US-014 |
| Phase plan missing for target phase | Implement prompt | Stop and tell user to run expand | Existing behavior, preserved |
| All tasks Completed, no Open/Started | Implement prompt | Report "all phases complete" and exit without modifications | NFR-005: idempotency <!-- Added during finalization: explicit idempotency handling --> |

---

## 10. Platform and Implementation Risks

### Risk 1: Prompt Compliance Under Context Pressure

- **What could go wrong:** The agent skips status updates when the context window is nearly full.
- **Threatens:** US-001, US-002, US-004
- **Mitigation:** The hook (US-005) provides runtime enforcement. Crash recovery (US-015–017) handles the aftermath.

### Risk 2: Hook Blocks Legitimate Work

- **What could go wrong:** False positive — hook blocks a non-implement edit due to stale sentinel or parsing error.
- **Threatens:** US-007, NFR-002
- **Mitigation:** Fail-open design on all parse errors. Sentinel-based activation (dormant when absent). User can always `rm` the sentinel.

### Risk 3: `/compact` is Lossy

- **What could go wrong:** Compaction retains too much phase N context or loses branch/plan state.
- **Threatens:** US-011, US-012, NFR-004
- **Mitigation:** Re-read `final.plan.md` after compaction (US-012). Aggressive focus phrase steers compaction. Clean stop if > 50% after compact (US-014).

### Risk 4: Expand Restructuring Corrupts Master Plan

- **What could go wrong:** Expand incorrectly parses or rewrites `final.plan.md`.
- **Threatens:** US-022, US-023
- **Mitigation:** Master plan is committed before expand runs. `git checkout` restores it. Expand re-reads and verifies output.

### Risk 5: Hook Performance on Large Plans <!-- Added during finalization -->

- **What could go wrong:** A phase plan with hundreds of tasks causes the hook to exceed 200ms.
- **Threatens:** NFR-001
- **Mitigation:** The parsing algorithm is simple string splitting — O(n) in the number of lines. Even a 500-line plan file parses in < 50ms. No regex compilation per invocation.

---

## 11. Traceability Matrix

| User Story | PDR Section | Component |
|-----------|-------------|-----------|
| US-001 | 4.2 (Execution Loop 3.2a) | `implement.md` |
| US-002 | 4.2 (Execution Loop 3.2d) | `implement.md` |
| US-003 | 4.2 (Execution Loop 3.4), 4.3 (Phase Status table) | `implement.md`, `expand.md` |
| US-004 | 4.2 (Violations list) | `implement.md` |
| US-005 | 4.1 (Decision tree step 8) | `pre-implement-status-guard.py` |
| US-006 | 4.1 (Decision tree step 4) | `pre-implement-status-guard.py` |
| US-007 | 4.1 (Decision tree step 5), 2.1 (Sentinel lifecycle) | `pre-implement-status-guard.py` |
| US-008 | 4.2 (Phase Isolation Rules) | `implement.md` |
| US-009 | 4.2 (Phase Isolation Rules) | `implement.md` |
| US-010 | 4.2 (Phase Isolation Rules) | `implement.md` |
| US-011 | 4.2 (Context Lifecycle) | `implement.md` |
| US-012 | 4.2 (Context Lifecycle) | `implement.md` |
| US-013 | 4.2 (Context Lifecycle) | `implement.md` |
| US-014 | 4.2 (Context Lifecycle), 9 (Error Handling) | `implement.md` |
| US-015 | 4.2 (Crash Recovery Protocol) | `implement.md` |
| US-016 | 4.2 (Crash Recovery Protocol) | `implement.md` |
| US-017 | 4.2 (Crash Recovery Protocol) | `implement.md` |
| US-018 | 4.4 (New dispatch mode) | `SKILL.md` |
| US-019 | 4.4 (Path argument parsing) | `SKILL.md` |
| US-020 | 4.4 (Path argument parsing) | `SKILL.md` |
| US-021 | 4.4 (Context injection) | `SKILL.md` |
| US-022 | 4.3 (Master plan restructuring) | `expand.md` |
| US-023 | 4.3 (Phase Summaries section), 4.2 (Execution Loop 3.4) | `expand.md`, `implement.md` |
| US-024 | 4.2 (Two-level monitoring model), 4.3 | `implement.md`, `expand.md` |

| NFR | PDR Section | Design Response |
|-----|-------------|----------------|
| NFR-001 | 4.1 (Performance) | Non-implement path ~3ms; implement path < 20ms. Simple string splitting, no regex compilation per invocation. |
| NFR-002 | 4.1 (Decision tree), 6.1, 9 | Every error path exits 0. Only one exit 2 path (sentinel exists + no Started task + source file + same project). |
| NFR-003 | 4.1 (Decision tree step 3) | Backslash → forward slash normalization before all path matching. Plan file patterns use `*` wildcards matching both separators. |
| NFR-004 | 4.2 (Context Lifecycle) | `/compact` with aggressive focus phrase after each phase. 50% threshold. Clean stop fallback. |
| NFR-005 | 4.2 (Idempotency), 9 | Fully completed plan → "all phases complete" report, no modifications. |
| NFR-006 | 4.2 (Format Detection), 4.3 (restructuring is additive) | Frontmatter check: `format: "dashboard"` → new path; else → old path (dual-file per-task). Old plans never migrated automatically. |

---

## 12. Acceptance Criteria

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
| AC-13 | Running `/sdlc implement` on a fully completed plan produces no modifications | NFR-005 <!-- Added during finalization --> |

---

## 13. Recommended Planning Phases

1. **Hook & Sentinel** — Create `pre-implement-status-guard.py`, register in `settings.json`, test sentinel lifecycle and plan file parsing. Foundation for all other changes.

2. **Implement Prompt Rewrite** — Rewrite `skill/implement.md` with status enforcement, sentinel management, crash recovery, format detection, two-level monitoring model, context lifecycle. Largest single artifact.

3. **Dispatcher Enhancements** — Modify `skill/SKILL.md`: add `phase NN all` mode, path argument parsing, context injection.

4. **Expand Restructuring** — Modify `skill/expand.md`: add master plan restructuring step (Phase Status table, `format: "dashboard"` frontmatter, Phase Summaries section).

5. **Integration & Polish** — Verify end-to-end behavior, backward compatibility, cross-cutting consistency.

---

## 14. Concerns for Release Planning

1. **Phase 1 (hook) writes to `~/.claude/hooks/` and `~/.claude/settings.json`, which are outside the project directory.** The user has authorized this work, but phase task descriptions should note it explicitly.

2. **Phase 1 (hook) must be tested against the existing implement prompt before Phase 2 rewrites it.** The hook should work with both the current and rewritten prompt.

3. **Phase 2 (implement rewrite) is the largest single change** — 173 lines → ~300+ lines. The prompt is a single file with no compile/test step, so splitting it would create two half-broken prompts that can't be individually verified.

4. **Phase 4 (expand restructuring) is destructive to `final.plan.md`.** Git commit before expand runs provides the safety net.

5. **NFR-006 carries two code paths** (old-format and new-format) in the implement prompt indefinitely. No deprecation timeline proposed because old-format plans may exist in archived projects.
