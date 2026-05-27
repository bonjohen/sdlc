---
phase: 21
title: "Implement Prompt Rewrite"
depends_on: "Phase 20 (hook must exist so the prompt can reference it and manage the sentinel)"
goal: "skill/implement.md is fully rewritten with enforced status tracking, phase isolation, context lifecycle, crash recovery, sentinel management, and backward-compatible format detection."
source_pdr_sections: ["4.2", "2.2", "2.3"]
source_user_stories: ["US-001", "US-002", "US-003", "US-004", "US-008", "US-009", "US-010", "US-011", "US-012", "US-013", "US-014", "US-015", "US-016", "US-017", "US-024", "NFR-004", "NFR-005", "NFR-006"]
status: "open"
---

# Phase 21: Implement Prompt Rewrite

## Tasks

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 21.1 | Completed | 2026-05-27 01:27 PM | 2026-05-27 01:35 PM | Write the Prerequisites section: verify plan files exist, detect master plan format (old vs new via `format: "dashboard"` in frontmatter). Include idempotency check — if no Open/Started tasks remain, report "all phases complete" and exit (NFR-005). |
| 21.2 | Completed | 2026-05-27 01:35 PM | 2026-05-27 01:35 PM | Write the Sentinel Management section: create `~/.claude/state/sdlc-implement.json` at start with `project_root`, `phase_plan`, `started_at`. Update `phase_plan` on phase advance. Delete on completion, single-phase stop, or clean stop. |
| 21.3 | Completed | 2026-05-27 01:35 PM | 2026-05-27 01:35 PM | Write the Execution Loop with HARD RULE callouts: step 3.2a (Started before code — "you MUST update the phase plan to Started before writing any code, creating any file, or running any command for this task") and step 3.2d (Completed after code — "the VERY NEXT action after finishing implementation work is updating the phase plan to Completed"). Include explicit violation list: batching, skipping Started, deferring. |
| 21.4 | Completed | 2026-05-27 01:35 PM | 2026-05-27 01:35 PM | Write the two-level monitoring model: phase plan updated per-task (Started/Completed with PST timestamps), master plan updated once per-phase (status to `in_progress`/`complete`, timestamp, commit hash, summary). For old-format plans, fall back to dual-file per-task updates. |
| 21.5 | Completed | 2026-05-27 01:35 PM | 2026-05-27 01:35 PM | Write the Phase Isolation section: read only current phase plan, no future-phase reads, no exploratory agents. Next phase plan read only after current phase committed. |
| 21.6 | Completed | 2026-05-27 01:35 PM | 2026-05-27 01:35 PM | Write the Context Lifecycle section (multi-phase modes only): `/compact` with focus phrase after each phase commit, re-read `final.plan.md` after compaction to confirm state, 50% threshold for self-compaction, clean stop with user instructions if compact insufficient. |
| 21.7 | Completed | 2026-05-27 01:35 PM | 2026-05-27 01:35 PM | Write the Crash Recovery Protocol: detect Started tasks on resume, verify on-disk work (files, functions, tests), mark Completed with `[recovered from interrupted session]` annotation if work exists, re-implement if work not found. Handle Edit-failure variant (work exists but status doesn't). |
| 21.8 | Completed | 2026-05-27 01:35 PM | 2026-05-27 01:35 PM | Write format detection logic: old-format path (master plan has task tables, dual-file per-task updates) vs new-format path (master plan has `format: "dashboard"`, phase plan per-task, master plan per-phase). |
| 21.9 | Completed | 2026-05-27 01:35 PM | 2026-05-27 01:35 PM | Preserve existing behaviors that don't conflict: blocked task handling, phase dependency checks, never-modify-completed-phases rule, resumption logic, verification commands, commit protocol. Review current `skill/implement.md` and carry forward applicable sections. |

## Context

### Files to Create or Modify

- `skill/implement.md` — **Rewrite.** Current file is 173 lines. Rewritten version estimated at ~300+ lines. This is the core artifact of the entire project.

### Current `skill/implement.md` Structure (to preserve what works)

The current prompt has these sections that should be reviewed for carryover:
- Phase identification logic (read `final.plan.md`, find next incomplete phase)
- Task execution order (top-to-bottom within phase)
- Verification step (tests, lint)
- Commit protocol (one commit per phase)
- Blocked task handling (skip, note, continue)
- Phase dependency checks
- Never-modify-completed-phases rule
- References to optional `scripts/sdlc-plan-state.py` (keep as optional)

### Rewritten Prompt Structure

The rewritten prompt must follow this structure (from PDR 4.2):

```
1. Prerequisites
   - Verify plan files exist (final.plan.md, phase{NN}/plan.md)
   - Format detection: read frontmatter of final.plan.md
     If contains `format: "dashboard"` → new format
     Else → old format (legacy dual-file behavior)
   - Idempotency: if no Open/Started tasks in any phase → "all phases complete"

2. Sentinel Management
   - CREATE: ~/.claude/state/sdlc-implement.json
     {
       "project_root": "{absolute path, forward slashes}",
       "phase_plan": "sdlc/plan/phase{NN}/plan.md",
       "started_at": "{PST timestamp}"
     }
   - UPDATE: change phase_plan when advancing to next phase
   - DELETE: when all phases complete, or single-phase stop, or clean stop

3. Execution Loop
   3.1 Read State — identify active phase and next Open task
   3.2 Execute Tasks (for each task, top-to-bottom):
       a. ███ HARD RULE ███ Update phase plan → Started with PST timestamp
          BEFORE any code, file creation, or command for this task.
          This is not optional. This is not deferrable.
       b. Read the phase plan's Context section for this task
       c. Do the implementation work
       d. ███ HARD RULE ███ Update phase plan → Completed with PST timestamp
          IMMEDIATELY after finishing. The VERY NEXT action.
          Not after verification. Not batched with next task.
   3.3 Run Verification (tests, lint, behavioral checks from phase plan)
   3.4 Update Master Plan:
       - New format: update Phase Status table row
         (status → complete, Completed timestamp, Commit hash)
         Append Phase Summary to ## Phase Summaries section
       - Old format: update phase status in master plan task table
         (legacy dual-file per-task behavior)
   3.5 Commit all changes for the phase
   3.6 Context Lifecycle (multi-phase modes only):
       - Run /compact "{phase NN complete, starting phase NN+1}"
       - Re-read final.plan.md after compaction
       - Verify phase completion recorded
   3.7 Continue or Stop:
       - More phases + multi-phase mode → loop to 3.1
       - More phases + single-phase mode → stop
       - No more phases → delete sentinel, report complete

4. Status Update Violations (explicit prohibited behaviors)
   THE FOLLOWING ARE VIOLATIONS:
   - Batching: writing code for tasks 2 and 3 before updating task 1's status
   - Skipping Started: going directly from Open to Completed
   - Deferring: "I'll update the plan after I verify" — NO
   - Grouping: "I'll mark all tasks complete at the end" — NO

5. Crash Recovery Protocol
   When resuming and finding Started tasks:
   - For each Started task: check if described files/functions/tests exist on disk
   - If work exists → mark Completed, add "[recovered from interrupted session]"
   - If work doesn't exist → leave as Started, re-implement
   - For Open tasks after a Started/Completed: check for partial work on disk
   - Never mark Completed without verifying work exists (US-017)

6. Phase Isolation Rules
   - Read ONLY the current phase's plan.md during implementation
   - Do NOT read future phase plans (phase{M}/plan.md where M > current)
   - Do NOT launch Explore subagents or project-wide scans before starting work
   - Do NOT pre-read the master plan's future phase sections
   - Next phase's plan.md: read ONLY after committing current phase

7. Context Lifecycle (multi-phase modes: "all" and "phase NN all")
   - After each phase commit: /compact with aggressive focus phrase
   - After compaction: re-read final.plan.md to confirm state
   - If context > 50%: self-compact before continuing
   - If context > 50% AFTER compaction: stop, instruct user:
     "Run /clear then /sdlc implement phase {next} to continue"

8. Format Detection
   - Dashboard format (frontmatter has format: "dashboard"):
     Phase plan: per-task updates (Started/Completed)
     Master plan: per-phase updates only (status, timestamp, commit, summary)
   - Old format (no format field in frontmatter):
     Both files: per-task updates (legacy dual-file behavior)
     Phase summary: still added to master plan at phase completion

9. Idempotency (NFR-005)
   - Fully completed plan: report "all phases complete", no modifications
   - Partially completed: resume from first incomplete phase
```

### Two-Level Monitoring Model

| File | Update frequency | What gets updated | Who updates |
|------|-----------------|-------------------|-------------|
| `phase{NN}/plan.md` | Per-task | Task Status → Started/Completed with PST timestamp | Agent during execution loop |
| `final.plan.md` (new format) | Per-phase | Phase Status table row: status, Started, Completed, Commit. Phase Summary appended. | Agent at phase completion |
| `final.plan.md` (old format) | Per-task (legacy) | Task rows in both files | Agent during execution loop |

### Sentinel Lifecycle

| Event | Sentinel action |
|-------|----------------|
| `/sdlc implement` starts | Create `~/.claude/state/sdlc-implement.json` |
| Phase advance (multi-phase) | Update `phase_plan` field to next phase |
| All phases complete | Delete sentinel |
| Single-phase mode, phase done | Delete sentinel |
| Clean stop (context > 50% after compact) | Delete sentinel |
| Session crash | Sentinel lingers (orphaned) |
| Next `/sdlc implement` after crash | Overwrite sentinel |

### Design Notes

- **This is the largest single change in the project** — 173 lines → ~300+ lines. The prompt is a single file with no compile/test step, so it cannot be meaningfully split into sub-phases. Each section depends on the others (e.g., sentinel management is referenced by the execution loop, format detection affects the monitoring model, crash recovery depends on the status update rules).
- **HARD RULE callouts must be visually distinct.** Use `███ HARD RULE ███` or similar formatting that stands out when the model reads the prompt. The goal is that these rules survive even under context pressure.
- **The violations list is positive enforcement.** Instead of just saying "update status before code," the prompt explicitly lists what NOT to do. This has proven more effective for AI agent compliance than positive-only instructions (per the refactor analysis in `docs/refactor.md`).
- **Old-format backward compatibility (NFR-006):** The format detection is a single frontmatter check. If `format: "dashboard"` is absent, the entire prompt falls back to the current dual-file per-task behavior. This means the rewritten prompt works immediately with existing projects that haven't re-expanded.
- **Context lifecycle 50% threshold is lower than the global 65% rule** in `~/.claude/CLAUDE.md`. This is intentional — multi-phase runs accumulate context faster, so the implement prompt compacts earlier.

### Verification

- [ ] The rewritten `skill/implement.md` contains `HARD RULE` callouts for Started and Completed updates
- [ ] The prompt contains an explicit violations list (batching, skipping Started, deferring)
- [ ] The prompt contains sentinel create/update/delete instructions with exact file path and JSON format
- [ ] The prompt contains format detection logic (frontmatter check for `format: "dashboard"`)
- [ ] The prompt contains phase isolation rules (read only current phase, no future-phase reads)
- [ ] The prompt contains context lifecycle instructions (compact, 50% threshold, clean stop)
- [ ] The prompt contains crash recovery protocol (verify on-disk work, recovery annotations)
- [ ] The prompt contains idempotency handling (fully completed plan → exit cleanly)
- [ ] The prompt preserves: blocked task handling, phase dependencies, commit protocol, verification step
- [ ] An agent reading this prompt would know: when to update which files, how to manage the sentinel, how to handle crashes, how to manage context between phases

## Phase Summary

- **Changes:** Rewrote `skill/implement.md` from 173 to 361 lines. Added: Prerequisites with format detection and idempotency check, Sentinel Management lifecycle, Execution Loop with HARD RULE callouts for Started/Completed, Status Update Violations list, Crash Recovery Protocol, Phase Isolation Rules, Context Lifecycle (50% threshold, clean stop), Format Detection (dashboard vs old), and preserved existing behaviors (blocked tasks, dependencies, commit protocol, resumption).
- **Commit:** `Phase 21: Implement Prompt Rewrite — status enforcement, sentinel management, crash recovery`
