# SDLC Implement Hardening — Phased Release Plan

## Gaps in Source Document

The draft PDR (`draft.pdr.md`) is thorough. All 5 release planning concerns are addressed.

- **Concern 1 (test hook against current prompt before rewrite):** Addressed — Phase 00 creates the hook and tests it against the existing `implement.md` before Phase 01 rewrites it.
- **Concern 2 (expand restructuring is destructive):** Addressed — Phase 03 includes a Git commit before expand runs, and verification re-reads the rewritten file.
- **Concern 3 (implement rewrite is large):** The PDR estimated 300+ lines. This plan keeps it as a single phase because the prompt is a single file with no compile/test step — splitting it would create two half-broken prompts that can't be individually verified.
- **Concern 4 (sentinel lives outside project directory):** Addressed in the implement prompt's sentinel management section. The hook checks `project_root` to avoid cross-project interference.
- **Concern 5 (backward compatibility carries two code paths):** Addressed — the old-format code path is minimal (a single conditional at the top of the execution loop). No deprecation timeline proposed because old-format plans may exist indefinitely in archived projects.

PDR recommended 6 phases. This plan uses **5 phases** because:
- PDR's "Context lifecycle" phase (Phase 5) is folded into the implement prompt rewrite (Phase 01) — context lifecycle is a section of the implement prompt, not a separate artifact.
- PDR's "Verification" phase (Phase 6) is folded into each phase's acceptance criteria rather than being a standalone phase. Verification against a real project requires a real project, which is outside this repo's scope.

---

## 1. Release Strategy

This project modifies prompt files and creates a hook script. There is no build step, no deployment, no database migration. Each phase produces markdown or Python files that can be immediately tested by invoking `/sdlc implement` in a test project.

**Risk-first ordering:**
1. The hook is the foundation — without it, all other enforcement is advisory.
2. The implement prompt rewrite is the largest change and depends on the hook's sentinel design.
3. The dispatcher feeds into the implement prompt and must match its new modes.
4. The expand restructuring creates the new master plan format that the implement prompt consumes.

## 2. Release Milestones

| Phase | Name | Deliverable | Risk Level |
|-------|------|-------------|------------|
| 00 | Hook & Sentinel | Working `PreToolUse` hook + sentinel lifecycle | High — validates the core enforcement mechanism |
| 01 | Implement Prompt Rewrite | Rewritten `skill/implement.md` with all new behaviors | High — largest single artifact |
| 02 | Dispatcher Enhancements | Updated `skill/SKILL.md` with new modes and path parsing | Low — mechanical routing changes |
| 03 | Expand Restructuring | Updated `skill/expand.md` + dashboard format definition | Medium — destructive rewrite of master plan |
| 04 | Integration & Polish | Cross-cutting fixes, backward compat verification, documentation | Low — cleanup and edge cases |

---

## Phase 00 — Hook & Sentinel

### Purpose

Create the runtime enforcement mechanism that blocks source file edits when no task is marked `Started` in the active phase plan. This is the highest-risk item because it validates a new hook type (Edit/Write matcher, not just Bash) and the sentinel-based activation pattern.

### Scope

- Create `~/.claude/hooks/pre-implement-status-guard.py`
- Register in `~/.claude/settings.json` (Edit and Write matchers)
- Define the sentinel file format (`~/.claude/state/sdlc-implement.json`)
- Implement task table parsing (find Status column, check for `Started`)
- Implement plan file detection (distinguish plan files from source files)
- Fail-open error handling throughout

### Required Work

1. Create `pre-implement-status-guard.py` with the decision tree from PDR Section 6.3: parse stdin JSON → normalize path → check plan file pattern → read sentinel → check project membership → parse task table → allow or block.
2. Implement task table parsing per PDR Section 6.4: find header row with `Status` column, identify column index, scan data rows for `Started` value.
3. Implement plan file detection: paths matching `*/plan/phase*/plan.md`, `*/docs/final.plan.md`, `*/docs/draft.*.md` are always allowed.
4. Implement path normalization for Windows: replace backslashes with forward slashes, handle both `C:\` and `/c/` prefixes.
5. Register the hook in `settings.json` with `Edit` and `Write` matchers per PDR Section 6.5.
6. Create a manual test: create a temporary sentinel file pointing to a test plan, attempt to edit a source file, verify block behavior; delete sentinel, verify allow behavior.

### Deliverables

- `~/.claude/hooks/pre-implement-status-guard.py` — working hook script
- Updated `~/.claude/settings.json` — Edit and Write hook registrations
- Sentinel file format documented in hook script's docstring

### Acceptance Criteria

- The hook blocks an Edit to a `.py` file when the sentinel exists and no task is `Started` in the referenced phase plan.
- The hook allows an Edit to `phase{NN}/plan.md` regardless of task status.
- The hook allows all edits when the sentinel file does not exist.
- The hook exits 0 (allows) when the sentinel file contains malformed JSON.
- The hook exits 0 (allows) when the referenced phase plan file does not exist.
- The hook runs in < 200ms for all paths (sentinel absent, sentinel present with Started task, sentinel present with no Started task).

---

## Phase 01 — Implement Prompt Rewrite

### Purpose

Rewrite `skill/implement.md` with enforced status tracking, phase isolation, context lifecycle, crash recovery, sentinel management, and backward-compatible format detection. This is the core artifact that all other changes support.

### Scope

- Full rewrite of `skill/implement.md` per PDR Section 8.1
- Status enforcement with HARD RULE callouts and violation definitions
- Phase isolation rules (read only current phase)
- Context lifecycle (compact between phases in multi-phase mode, 50% threshold)
- Crash recovery protocol (verify on-disk work for Started tasks)
- Sentinel management (create/update/delete `sdlc-implement.json`)
- Format detection (frontmatter check for `format: "dashboard"`)
- Two-level monitoring model (phase plan per-task, master plan per-phase)

### Required Work

1. Write the Prerequisites section: verify plan files exist, detect master plan format (old vs. new via `format: "dashboard"` in frontmatter).
2. Write the Sentinel Management section: create sentinel at start, update on phase advance, delete on completion or stop.
3. Write the Execution Loop with HARD RULE callouts on steps 2a (Started before code) and 2d (Completed after code). Include the explicit violation list from the user requirements.
4. Write the two-level monitoring model: phase plan updated per-task, master plan updated once per-phase (status, timestamp, commit hash, summary).
5. Write the Phase Isolation section: read only current phase plan, no future-phase reads, no exploratory agents.
6. Write the Context Lifecycle section: `/compact` between phases, 50% threshold, clean stop instructions.
7. Write the Crash Recovery Protocol: detect Started tasks, verify on-disk work, recovery annotations.
8. Write the format detection logic: old-format path (dual-file per-task updates) vs. new-format path (phase plan per-task, master plan per-phase).
9. Preserve existing behaviors that don't conflict: blocked task handling, phase dependency checks, never-modify-completed-phases rule, resumption logic.

### Deliverables

- Rewritten `skill/implement.md`

### Acceptance Criteria

- The prompt text contains HARD RULE callouts for Started and Completed updates.
- The prompt text contains an explicit violations list (batching, skipping Started, deferring).
- The prompt text contains sentinel creation, update, and deletion instructions.
- The prompt text contains format detection logic (frontmatter check).
- The prompt text contains phase isolation rules.
- The prompt text contains context lifecycle instructions (compact, 50% threshold, clean stop).
- The prompt text contains crash recovery protocol.
- An agent reading this prompt would know: (a) when to update which files, (b) how to manage the sentinel, (c) how to handle crashes, (d) how to manage context between phases.

---

## Phase 02 — Dispatcher Enhancements

### Purpose

Update `skill/SKILL.md` to support the new `phase NN all` dispatch mode, plan file path parsing, and context injection when routing to implement.

### Scope

- Add `phase NN all` to the implement options table and routing logic
- Add plan file path argument parsing with regex extraction
- Add context injection for implement routing
- Handle Windows backslash normalization in path arguments

### Required Work

1. Add `phase NN all` to the Implement Options table: "Start at phase NN, continue through all remaining phases autonomously."
2. Add routing logic for `phase NN all`: after reading the implement prompt, inject "Execute in autonomous mode starting at phase NN."
3. Add Plan File Path Parsing section per PDR Section 8.3: regex `phase[/\\]?(\d{2})`, map path-alone to single-phase, path+continuation to phase-NN-all.
4. Add context injection block: when routing to implement.md, prepend the status monitoring and phase isolation reminders from PDR Section 8.3.
5. Update the Pipeline Summary's implement section if needed.

### Deliverables

- Updated `skill/SKILL.md`

### Acceptance Criteria

- The dispatcher recognizes `/sdlc implement phase 03 all` and routes correctly.
- The dispatcher parses `sdlc/plan/phase03/plan.md` and extracts phase 03.
- The dispatcher parses `sdlc\plan\phase03\plan.md` (backslash) and extracts phase 03.
- The dispatcher parses `sdlc/plan/phase03/plan.md and proceed with remaining phases` as phase 03 all.
- The dispatcher injects status and isolation context when routing to implement.

---

## Phase 03 — Expand Restructuring

### Purpose

Modify `skill/expand.md` to restructure `final.plan.md` into a phase-level dashboard after generating phase plans. This creates the new master plan format that the implement prompt's new-format code path consumes.

### Scope

- Add master plan restructuring step to `skill/expand.md`
- Define the post-expand Phase Status table format
- Define the Phase Summaries section
- Add `format: "dashboard"` frontmatter field
- Preserve existing expand behaviors (phase plan generation, context sections)

### Required Work

1. Add the Master Plan Restructuring section to `expand.md` per PDR Section 8.2: after generating all phase plans, rewrite `final.plan.md`.
2. Define the Phase Status table format per PDR Section 7.1: columns Phase, Title, Plan (link), Status, Started, Completed, Commit.
3. Define the frontmatter addition: `format: "dashboard"`.
4. Define the Phase Summaries section: empty on expand, filled by implement.
5. Define what is preserved from the pre-expand plan: frontmatter (plus new field), title, source references, work queue instructions, technology stack, coverage checklist.
6. Define what is removed: individual task rows (now in phase plans only).
7. Add verification step: after restructuring, re-read the master plan and confirm the Phase Status table has one row per phase.

### Deliverables

- Updated `skill/expand.md`

### Acceptance Criteria

- After expand, `final.plan.md` frontmatter contains `format: "dashboard"`.
- After expand, `final.plan.md` contains a Phase Status table with one row per phase and no individual task rows.
- After expand, each phase plan at `sdlc/plan/phase{NN}/plan.md` contains the full task table.
- The Phase Status table includes relative links to phase plan files.
- Work queue instructions, technology stack, and coverage checklist are preserved.
- A `## Phase Summaries` section exists at the bottom (empty, to be filled by implement).

---

## Phase 04 — Integration & Polish

### Purpose

Verify end-to-end behavior, handle edge cases, ensure backward compatibility with old-format plans, and clean up any cross-cutting issues from the previous phases.

### Scope

- Verify NFR-006 (backward compatibility): old-format master plans still work
- Verify the sentinel lifecycle across session crashes (orphan cleanup)
- Verify path normalization across all components (hook, dispatcher, implement prompt)
- Update CLAUDE.md if needed (hook documentation)
- Clean up any issues discovered during Phases 00–03

### Required Work

1. Read the rewritten `implement.md` and verify the old-format code path is complete: if a master plan lacks `format: "dashboard"`, the prompt should use dual-file per-task updates.
2. Verify the sentinel lifecycle documentation in the hook script's docstring covers: creation, update, deletion, crash orphan, manual cleanup.
3. Verify that all path references across all modified files use consistent conventions (forward slashes, `phase{NN}` pattern).
4. Update the project `CLAUDE.md` to document the new hook (`pre-implement-status-guard.py`) if not already documented.
5. Review all modified files for consistency: sentinel file path, plan file paths, status values, timestamp format.

### Deliverables

- Verified and consistent set of modified files
- Updated `CLAUDE.md` if needed

### Acceptance Criteria

- An old-format `final.plan.md` (no `format: "dashboard"`) is correctly handled by the implement prompt with dual-file per-task updates.
- The sentinel file path is consistent across: hook script, implement prompt, error messages.
- All plan file path patterns are consistent across: hook script, implement prompt, dispatcher, expand prompt.
- No file references a path using only backslashes (all use forward slashes or handle both).

---

## Cross-Phase Requirements

### Data Persistence

All state is persisted in markdown plan files and committed to Git. No additional data stores. The sentinel file (`~/.claude/state/sdlc-implement.json`) is ephemeral session state, not project data.

### Performance

The hook must complete in < 200ms for all code paths (NFR-001). This constrains the task table parsing implementation to simple string operations — no regex compilation on every invocation, no external process spawning.

---

## Minimum Useful Release

**Phase 01 complete (Hook + Implement rewrite).** At this point:
- The hook blocks source file edits when no task is Started (runtime enforcement).
- The implement prompt enforces status updates, phase isolation, context lifecycle, and crash recovery.
- The dispatcher has not been enhanced yet (no `phase NN all`, no path parsing), but the three existing modes work.
- The master plan format has not changed (expand restructuring is Phase 03), but the implement prompt's old-format code path handles this.

This is the minimum because: enforcement (hook) + instructions (prompt) together provide the core value. Everything else is ergonomic or structural.

## First Full Feature Release

**Phase 04 complete (all phases).** At this point:
- All four dispatch modes work, including path parsing.
- Expand produces the new dashboard format.
- The implement prompt handles both old and new formats.
- Cross-cutting consistency is verified.

---

## Concerns for Finalization

1. **Phase 00 writes to `~/.claude/hooks/` and `~/.claude/settings.json`, which are outside the project directory.** The project CLAUDE.md says "Never modify files outside the active project unless explicitly requested." The user has already authorized this work, but the plan should call it out in Phase 00's task descriptions.

2. **Phase 01 is the largest phase** (full rewrite of a 173-line prompt into ~300+ lines). The finalizer should consider whether task-level decomposition can be parallelized (e.g., writing the sentinel management section independently from the execution loop).

3. **Phase 03 modifies `final.plan.md` format, which is an output of the finalize step.** If the user runs `finalize` again after `expand`, the re-finalized plan may not have the dashboard format. The expand step's restructuring must be re-run after any re-finalization. The finalizer should note this ordering dependency.

4. **No automated test suite exists for prompts.** Acceptance criteria are behavioral — they require running `/sdlc implement` against a real project. The finalizer may want to define a specific test scenario (e.g., "expand and implement against the I2I project's archived plan files").

5. **The hook script installation (Phase 00) is global** — it affects all Claude Code sessions, not just this project. If the hook has a bug that causes false blocks, it affects all work until fixed. Phase 00's acceptance criteria must include negative testing (verify the hook allows non-implement work).
