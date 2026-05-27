---
document: "Implementation Plan"
version: "1.0"
status: "final"
source: "sdlc/docs/draft.plan.md"
pdr: "sdlc/docs/final.pdr.md"
user_requirements: "sdlc/docs/final.user.md"
finalized_date: "2026-05-27"
total_phases: 5
---

# SDLC Implement Hardening — Implementation Plan

**Source PDR:** `sdlc/docs/final.pdr.md`
**Source User Requirements:** `sdlc/docs/final.user.md`

## Work Queue Instructions

### State Transitions

```
Open  ──>  Started  ──>  Completed
              │
              └──>  Blocked  ──>  Started  ──>  Completed
```

- **Open**: Not yet begun.
- **Started**: Actively in progress. Record the start datetime (PST).
- **Completed**: Done and verified. Record the completion datetime (PST).
- **Blocked**: Cannot proceed; note the blocker in the description.

### Commit Protocol

1. Work through all tasks in a phase.
2. When every task reaches Completed, write the Phase Summary.
3. Stage and commit all changes for the phase. Do not push.
4. Proceed immediately to the next phase.

## Technology Stack

| Concern | Choice | Justification |
|---------|--------|--------------|
| Hook runtime | Python 3 (system, ≥ 3.8) | Matches existing push guard pattern; no new dependencies |
| Hook registration | `~/.claude/settings.json` PreToolUse entries | Standard Claude Code hook mechanism |
| State storage | Markdown plan files + Git | Existing convention; no new data stores |
| Session state | `~/.claude/state/sdlc-implement.json` | Ephemeral sentinel, same directory as push guard flag |
| Prompt format | Markdown | Existing convention for all skill prompts |

---

## Phase 00: Hook & Sentinel

**Goal:** A working `PreToolUse` hook blocks source file edits when no task is marked `Started` in the active phase plan. The sentinel-based activation mechanism is operational.
**Depends on:** None (first phase).
**PDR sections:** 4.1 (Hook), 2.1 (Sentinel), 6.1 (Fail-open design)
**User stories:** US-005, US-006, US-007, NFR-001, NFR-002, NFR-003

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 00.1 | Completed | 2026-05-27 01:15 PM | 2026-05-27 01:18 PM | Create `~/.claude/hooks/pre-implement-status-guard.py` with the decision tree from PDR 4.1: parse stdin JSON → normalize path → check plan file pattern → read sentinel → check project membership → parse task table → allow or block. All error paths exit 0 (fail open). |
| 00.2 | Completed | 2026-05-27 01:18 PM | 2026-05-27 01:19 PM | Implement task table parsing per PDR 4.1: find header row with `Status` column, identify column index, scan data rows for `Started` value. Handle multiple tables, malformed tables (fail open), empty files. |
| 00.3 | Completed | 2026-05-27 01:19 PM | 2026-05-27 01:19 PM | Implement plan file detection: paths matching `*/plan/phase*/plan.md`, `*/docs/final.plan.md`, `*/docs/draft.*.md` are always allowed (exit 0). |
| 00.4 | Completed | 2026-05-27 01:19 PM | 2026-05-27 01:20 PM | Implement path normalization for Windows (NFR-003): replace backslashes with forward slashes, handle both `C:\` and `/c/` prefixes, resolve to absolute path. |
| 00.5 | Completed | 2026-05-27 01:20 PM | 2026-05-27 01:21 PM | Register the hook in `~/.claude/settings.json` with `Edit` and `Write` matchers per PDR 4.1. Two new PreToolUse entries pointing to `python C:/Users/boen3/.claude/hooks/pre-implement-status-guard.py`. **Note: writes to `~/.claude/settings.json` (outside project directory) — authorized by user.** |
| 00.6 | Completed | 2026-05-27 01:21 PM | 2026-05-27 01:25 PM | Manual test: (a) no sentinel → edit a `.py` file → allowed; (b) create sentinel pointing to a plan with a `Started` task → edit source → allowed; (c) create sentinel pointing to a plan with no `Started` task → edit source → blocked with error message; (d) edit `phase{NN}/plan.md` → allowed regardless; (e) malformed sentinel JSON → allowed (fail open); (f) sentinel for different project → allowed. |

### Phase 00 Summary

- **Changes:** Created `~/.claude/hooks/pre-implement-status-guard.py` with 8-step decision tree (parse stdin, normalize path, plan file detection, sentinel read, project membership, task table parsing, allow/block). Registered hook in `~/.claude/settings.json` with Edit and Write matchers. All error paths fail open. Verified with 6 manual test scenarios.
- **Commit:** `Phase 20: Hook & Sentinel — implement status guard hook with fail-open design`

---

## Phase 01: Implement Prompt Rewrite

**Goal:** `skill/implement.md` is fully rewritten with enforced status tracking, phase isolation, context lifecycle, crash recovery, sentinel management, and backward-compatible format detection.
**Depends on:** Phase 00 (hook must exist so the prompt can reference it and manage the sentinel).
**PDR sections:** 4.2 (Implement prompt), 2.2 (Plan file state), 2.3 (Session states)
**User stories:** US-001–004, US-008–017, US-024, NFR-004–006

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 01.1 | Completed | 2026-05-27 01:27 PM | 2026-05-27 01:35 PM | Write the Prerequisites section: verify plan files exist, detect master plan format (old vs new via `format: "dashboard"` in frontmatter). Include idempotency check — if no Open/Started tasks remain, report "all phases complete" and exit (NFR-005). |
| 01.2 | Completed | 2026-05-27 01:35 PM | 2026-05-27 01:35 PM | Write the Sentinel Management section: create `~/.claude/state/sdlc-implement.json` at start with `project_root`, `phase_plan`, `started_at`. Update `phase_plan` on phase advance. Delete on completion, single-phase stop, or clean stop. |
| 01.3 | Completed | 2026-05-27 01:35 PM | 2026-05-27 01:35 PM | Write the Execution Loop with HARD RULE callouts: step 3.2a (Started before code — "you MUST update the phase plan to Started before writing any code, creating any file, or running any command for this task") and step 3.2d (Completed after code — "the VERY NEXT action after finishing implementation work is updating the phase plan to Completed"). Include explicit violation list: batching, skipping Started, deferring. |
| 01.4 | Completed | 2026-05-27 01:35 PM | 2026-05-27 01:35 PM | Write the two-level monitoring model: phase plan updated per-task (Started/Completed with PST timestamps), master plan updated once per-phase (status → `in_progress`/`complete`, timestamp, commit hash, summary). For old-format plans, fall back to dual-file per-task updates. |
| 01.5 | Completed | 2026-05-27 01:35 PM | 2026-05-27 01:35 PM | Write the Phase Isolation section: read only current phase plan, no future-phase reads, no exploratory agents. Next phase plan read only after current phase committed. |
| 01.6 | Completed | 2026-05-27 01:35 PM | 2026-05-27 01:35 PM | Write the Context Lifecycle section (multi-phase modes only): `/compact` with focus phrase after each phase commit, re-read `final.plan.md` after compaction to confirm state, 50% threshold for self-compaction, clean stop with user instructions if compact insufficient. |
| 01.7 | Completed | 2026-05-27 01:35 PM | 2026-05-27 01:35 PM | Write the Crash Recovery Protocol: detect Started tasks on resume, verify on-disk work (files, functions, tests), mark Completed with `[recovered from interrupted session]` annotation if work exists, re-implement if work not found. Handle Edit-failure variant (work exists but status doesn't). |
| 01.8 | Completed | 2026-05-27 01:35 PM | 2026-05-27 01:35 PM | Write format detection logic: old-format path (master plan has task tables → dual-file per-task updates) vs new-format path (master plan has `format: "dashboard"` → phase plan per-task, master plan per-phase). |
| 01.9 | Completed | 2026-05-27 01:35 PM | 2026-05-27 01:35 PM | Preserve existing behaviors that don't conflict: blocked task handling, phase dependency checks, never-modify-completed-phases rule, resumption logic, verification commands, commit protocol. Review current `skill/implement.md` (173 lines) and carry forward applicable sections. |

### Phase 01 Summary

- **Changes:** Rewrote `skill/implement.md` from 173 to 361 lines. Added: Prerequisites with format detection and idempotency check, Sentinel Management lifecycle, Execution Loop with HARD RULE callouts for Started/Completed, Status Update Violations list, Crash Recovery Protocol, Phase Isolation Rules, Context Lifecycle (50% threshold, clean stop), Format Detection (dashboard vs old), and preserved existing behaviors (blocked tasks, dependencies, commit protocol, resumption).
- **Commit:** `Phase 21: Implement Prompt Rewrite — status enforcement, sentinel management, crash recovery`

---

## Phase 02: Dispatcher Enhancements

**Goal:** `skill/SKILL.md` supports the new `phase NN all` dispatch mode, plan file path parsing, and context injection when routing to implement.
**Depends on:** Phase 01 (dispatcher routes to implement.md; new modes must match the rewritten prompt's expectations).
**PDR sections:** 4.4 (Dispatcher)
**User stories:** US-018, US-019, US-020, US-021

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 02.1 | Completed | 2026-05-27 01:40 PM | 2026-05-27 01:43 PM | Add `phase NN all` to the Implement Options table in `skill/SKILL.md`: "Start at phase NN, continue through all remaining phases autonomously." Add routing logic: after reading implement.md, inject "Execute in autonomous mode starting at phase NN." |
| 02.2 | Completed | 2026-05-27 01:43 PM | 2026-05-27 01:43 PM | Add Plan File Path Parsing section: regex `phase[/\\]?(\d{2})` to extract phase number from path arguments. Map path-alone to single-phase mode, path + continuation language ("and proceed", "and continue", "and remaining", "all remaining") to `phase NN all` mode. |
| 02.3 | Completed | 2026-05-27 01:43 PM | 2026-05-27 01:43 PM | Implement Windows backslash normalization in path arguments: normalize `sdlc\plan\phase03\plan.md` to `sdlc/plan/phase03/plan.md` before regex matching. |
| 02.4 | Completed | 2026-05-27 01:43 PM | 2026-05-27 01:43 PM | Add context injection block: when routing to `implement.md`, prepend the status monitoring and phase isolation reminders per PDR 4.4. |
| 02.5 | Completed | 2026-05-27 01:43 PM | 2026-05-27 01:44 PM | Update the Pipeline Summary's implement section if needed to reflect the four dispatch modes. |

### Phase 02 Summary

- **Changes:** Modified `skill/SKILL.md`: added `phase NN all` dispatch mode, plan file path parsing, context injection, routing logic for new mode, updated Pipeline Summary.
- **Commit:** `Phase 22: Dispatcher Enhancements — phase NN all mode, path parsing, context injection`

---

## Phase 03: Expand Restructuring

**Goal:** `skill/expand.md` restructures `final.plan.md` into a phase-level dashboard after generating phase plans. The new dashboard format includes `format: "dashboard"` frontmatter and a Phase Status table.
**Depends on:** Phase 01 (implement prompt must have format detection ready to consume the new format).
**PDR sections:** 4.3 (Expand), 2.2 (Plan file state — Phase Status table format)
**User stories:** US-022, US-023, US-024

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 03.1 | Completed | 2026-05-27 01:47 PM | 2026-05-27 01:50 PM | Add the Master Plan Restructuring section to `skill/expand.md`: after generating all phase plans, rewrite `final.plan.md`. Git commit before expand provides the safety net. |
| 03.2 | Completed | 2026-05-27 01:50 PM | 2026-05-27 01:50 PM | Define the Phase Status table format: columns Phase, Title, Plan (relative link), Status (`not_started`), Started, Completed, Commit. One row per phase. |
| 03.3 | Completed | 2026-05-27 01:50 PM | 2026-05-27 01:50 PM | Define the frontmatter addition: add `format: "dashboard"` to existing YAML frontmatter. |
| 03.4 | Completed | 2026-05-27 01:50 PM | 2026-05-27 01:50 PM | Define what is preserved from the pre-expand plan: frontmatter (plus new field), title, source references, work queue instructions, technology stack, coverage checklist. |
| 03.5 | Completed | 2026-05-27 01:50 PM | 2026-05-27 01:50 PM | Define what is removed: individual task rows (now in phase plans only). Phase goal and dependency lines remain as context for the status table. |
| 03.6 | Completed | 2026-05-27 01:50 PM | 2026-05-27 01:50 PM | Add the `## Phase Summaries` section definition: empty on expand, filled by implement as phases complete. Each summary includes changes description and commit reference. |
| 03.7 | Completed | 2026-05-27 01:50 PM | 2026-05-27 01:50 PM | Add verification step: after restructuring, re-read the master plan and confirm the Phase Status table has one row per phase and no individual task rows remain. |

### Phase 03 Summary

- **Changes:** Modified `skill/expand.md` (166 → 237 lines): added Master Plan Restructuring section with restructuring algorithm, Phase Status table format, frontmatter dashboard field, preserved/removed content rules, Phase Summaries section, and verification step.
- **Commit:** `Phase 23: Expand Restructuring — dashboard format, Phase Status table, Phase Summaries`

---

## Phase 04: Integration & Polish

**Goal:** End-to-end behavior is verified, backward compatibility confirmed, cross-cutting consistency ensured across all modified artifacts.
**Depends on:** Phases 00–03 (all components must exist before integration verification).
**PDR sections:** 4.1–4.4 (all components), 9 (Error Handling), 10 (Risks)
**User stories:** NFR-005, NFR-006 (verification), all US (integration check)

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 04.1 | Open | | | Read the rewritten `implement.md` and verify the old-format code path is complete: if a master plan lacks `format: "dashboard"`, the prompt uses dual-file per-task updates. Verify the new-format code path: phase plan per-task, master plan per-phase. |
| 04.2 | Open | | | Verify the sentinel lifecycle documentation in the hook script's docstring covers: creation, update on phase advance, deletion on completion, crash orphan behavior, manual cleanup instructions. |
| 04.3 | Open | | | Verify path consistency across all modified files: sentinel file path (`~/.claude/state/sdlc-implement.json`), plan file patterns (`*/plan/phase*/plan.md`), status values (`Open`/`Started`/`Completed`/`Blocked` in phase plans; `not_started`/`in_progress`/`complete`/`blocked` in master plan), timestamp format (PST). |
| 04.4 | Open | | | Verify all path references use forward slashes or handle both separators. No file should reference a path using only backslashes. Check: hook script, implement prompt, dispatcher, expand prompt. |
| 04.5 | Open | | | Update the project `CLAUDE.md` to document the new hook (`pre-implement-status-guard.py`): what it does, where it lives, how to disable it, and its relationship to the sentinel file. |

### Phase 04 Summary

_To be filled after completion._

- **Changes:** TBD
- **Commit:** TBD

---

## Coverage Checklist

_Every PDR component appears in at least one phase task._

| PDR Section | Component | Phase | Task |
|-------------|-----------|-------|------|
| 4.1 | `pre-implement-status-guard.py` — Hook script | 00 | 00.1, 00.2, 00.3, 00.4 |
| 4.1 | Hook registration in `settings.json` | 00 | 00.5 |
| 4.1 | Hook manual testing | 00 | 00.6 |
| 2.1 | Sentinel file lifecycle | 01 | 01.2 |
| 4.2 | Implement prompt — Prerequisites & format detection | 01 | 01.1, 01.8 |
| 4.2 | Implement prompt — Execution loop & HARD RULE callouts | 01 | 01.3 |
| 4.2 | Implement prompt — Two-level monitoring model | 01 | 01.4 |
| 4.2 | Implement prompt — Phase isolation | 01 | 01.5 |
| 4.2 | Implement prompt — Context lifecycle | 01 | 01.6 |
| 4.2 | Implement prompt — Crash recovery | 01 | 01.7 |
| 4.2 | Implement prompt — Backward compatibility | 01 | 01.8, 01.9 |
| 4.4 | Dispatcher — `phase NN all` mode | 02 | 02.1 |
| 4.4 | Dispatcher — Path argument parsing | 02 | 02.2, 02.3 |
| 4.4 | Dispatcher — Context injection | 02 | 02.4 |
| 4.3 | Expand — Master plan restructuring | 03 | 03.1, 03.2, 03.3, 03.4, 03.5 |
| 4.3 | Expand — Phase Summaries section | 03 | 03.6 |
| 4.3 | Expand — Verification step | 03 | 03.7 |
| 6.1 | Fail-open design verification | 04 | 04.1, 04.2 |
| 9 | Error handling — All paths | 04 | 04.1, 04.2, 04.3 |
| 11 | Traceability — Path consistency | 04 | 04.3, 04.4 |
