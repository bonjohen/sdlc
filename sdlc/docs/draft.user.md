# SDLC Implement Hardening — Draft User Requirements Document

## Gaps Identified During Extraction

### Critical

None. Both source documents (`docs/checkpoint.md` and `docs/refactor.md`) describe the problem, root cause, and proposed solution for each requirement area in detail. The primary actor (AI agent executing `/sdlc implement`), the secondary actor (human user monitoring progress), and concrete user flows are all identifiable.

### Notable

- **No discussion of error behavior during status updates.** What happens if the Edit tool fails when updating a plan file mid-task? The agent has started implementation but can't write the "Started" marker. No fallback was discussed.
- **No discussion of concurrent sessions.** What happens if two Claude Code sessions are running against the same repo and both try to update `final.plan.md`? The documents assume single-session execution.
- **No discussion of plan file format validation.** The documents assume plan files are well-formed markdown tables. No mention of what happens if a plan file is malformed, has missing columns, or has been manually edited into an unparseable state.
- **`_standards.md` referenced by the pipeline but does not exist on disk.** Gap in pipeline infrastructure, not in these requirements.

---

## 1. Product Name

**SDLC Implement Hardening** — a set of changes to the SDLC prompt pipeline's `implement.md` and `SKILL.md` that make multi-phase code generation recoverable, observable, and context-efficient.

## 2. Purpose

When an AI agent executes `/sdlc implement` across multiple phases, three failure modes repeatedly destroy work:

1. **Lost status.** The agent completes tasks but doesn't update plan files. When the session crashes or compacts, there is no record of what was done. The next session restarts from scratch or guesses.
2. **Context waste.** The agent pre-reads future phase plans and launches exploratory scans before writing code, consuming context window on information it doesn't need yet.
3. **Context exhaustion.** Multi-phase runs accumulate file reads, narration, and tool output until compaction forces a lossy reset mid-work.

These are not theoretical — they were observed during chatbot-factory Phase 02 (14/15 tasks completed with no plan updates, then context lost) and Phase 03 (agent pre-read phases 04–05 and launched a full project explorer before starting work).

The purpose of this work is to harden the implement prompt so that plan files are always current, context is managed deliberately, and crash recovery is possible from plan file state alone.

## 3. Core Concept

Two plan files serve different audiences at different granularities. The phase plan (`phase{NN}/plan.md`) is the step-level state machine — every task transition (Open → Started → Completed) must be written to disk before the agent does anything else. The master plan (`final.plan.md`) is the phase-level dashboard — it tracks which phases are not_started, in_progress, complete, or blocked, and accumulates phase summaries as work completes. The master plan is updated once per phase, not per task. Git commits are the durable phase boundary. Context resets between phases are deliberate, not accidental. The agent reads only what it needs for the current phase.

## 4. Primary User Goal

**As the human operator**, I want to monitor AI agent progress in real-time by reading plan files, intervene when the agent goes off-track, and recover from any session interruption by re-invoking `/sdlc implement` — with the agent picking up exactly where it left off based on plan file state.

**As the AI agent**, the implement prompt must make status updates non-negotiable, prevent context waste from future-phase reads, and manage context lifecycle across phase boundaries so multi-phase runs complete without hitting context limits.

## 5. Operating Modes

The implement command operates in three modes (existing) plus one new mode:

| Mode | Invocation | Behavior |
|------|-----------|----------|
| Single phase | `/sdlc implement` | Execute the next incomplete phase, then stop. |
| Specific phase | `/sdlc implement phase NN` | Execute phase NN specifically. |
| All remaining | `/sdlc implement all` | Execute all remaining phases end-to-end. |
| **Start-at phase, continue all** | **`/sdlc implement phase NN all`** | **Start at phase NN, continue through remaining phases autonomously.** |

Additionally, the dispatcher must accept plan file paths as arguments:
- `/sdlc implement sdlc/plan/phase03/plan.md` → parsed as `/sdlc implement phase 03`
- `/sdlc implement sdlc\plan\phase03\plan.md and proceed with remaining phases` → parsed as `/sdlc implement phase 03 all`

## 6. Primary User Flows

### Flow 1: Single-phase execution with status tracking

1. User invokes `/sdlc implement`.
2. Agent reads `final.plan.md`, identifies next incomplete phase.
3. Agent reads `phase{NN}/plan.md` for the target phase.
4. For each task in the phase:
   a. Agent edits `phase{NN}/plan.md`: Status → `Started`, records PST timestamp. **This happens before any implementation work.**
   b. Agent implements the task (writes code, creates files, runs commands).
   c. Agent edits `phase{NN}/plan.md`: Status → `Completed`, records PST timestamp. **This happens immediately after implementation, before moving to next task.**
5. Agent runs validation (tests, lint).
6. Agent updates `final.plan.md`: phase status → `complete`, writes Phase Summary block, records completion timestamp and commit hash.
7. Agent commits all changes for the phase.

### Flow 2: Multi-phase execution with context lifecycle

1. User invokes `/sdlc implement all` or `/sdlc implement phase NN all`.
2. Agent reads bootstrap data: `CLAUDE.md`, project config, `final.plan.md`, `MEMORY.md`.
3. Agent identifies the first target phase.
4. Agent reads ONLY that phase's `plan.md` and the source files listed in its Context section.
5. Agent executes all tasks in the phase (Flow 1, steps 4–7).
6. After phase commit, agent runs `/compact "phase NN complete, starting phase NN+1"` to shed accumulated context.
7. Agent re-reads `final.plan.md` to confirm phase completion and identify next phase.
8. If next phase exists, agent reads its `plan.md` and continues (step 4).
9. If no more phases, agent reports completion summary and stops.
10. If context exceeds 50% after compaction, agent stops and tells user: "Run `/clear` then `/sdlc implement` to continue from phase {next}."

### Flow 3: Crash recovery

1. Session is interrupted (crash, compaction, user abort) mid-phase.
2. User starts new session, invokes `/sdlc implement`.
3. Agent reads `final.plan.md` to find the in-progress phase, then reads that phase's `plan.md`. Finds tasks marked `Started` (in-progress when session died).
4. For each `Started` task: agent verifies work exists on disk (checks files, functions, tests described by the task).
   - If work exists: mark `Completed` with estimated timestamp and note `[recovered from interrupted session]`.
   - If work does not exist: leave as `Started`, redo the task.
5. For each `Open` task after a `Started`/`Completed` task: agent checks for partial work on disk.
   - If partial work exists: mark `Started`, complete it.
   - If no work exists: proceed normally.
6. Agent never marks a task `Completed` without verifying its work exists.

## 7. Functional Requirements

### Status Update Enforcement

**FR-1:** The agent must update task status in `phase{NN}/plan.md` to `Started` with a PST timestamp BEFORE doing any implementation work for that task. No code, file creation, or command execution for the task may occur before the phase plan file shows `Started`.

**FR-2:** The agent must update task status in `phase{NN}/plan.md` to `Completed` with a PST timestamp IMMEDIATELY after finishing the task's implementation work. The update must be the very next action — not deferred to after verification, not batched with other tasks.

**FR-3:** The master plan (`final.plan.md`) is updated once per phase, not per task. At phase completion (after all tasks are done and validation passes), the agent updates the phase's row in `final.plan.md` with: status → `complete`, completion timestamp, commit hash, and appends the phase summary.

**FR-4:** The following are defined status update violations that the implement prompt must explicitly prohibit:
- Batching updates (writing code for multiple tasks before updating the phase plan file)
- Skipping the `Started` state (going directly from `Open` to `Completed`)
- Deferring updates to "after verification"

### Phase Isolation

**FR-5:** During implementation, the agent must read ONLY the current phase's `plan.md`. It must not read future phase plans, the master plan's future phase sections, or any file not directly needed for the current task.

**FR-6:** In multi-phase mode, the agent must read the next phase's `plan.md` ONLY AFTER committing the current phase. The sequence is: implement → commit → context reset → read next phase.

**FR-7:** The agent must not launch exploratory agents (Explore subagent, project scanners) to "understand the project" before implementation begins. The phase plan's Context section provides all necessary context.

### Context Lifecycle

**FR-8:** After committing each phase in multi-phase mode, the agent must run `/compact` with an aggressive focus phrase (e.g., "phase NN complete, starting phase NN+1, preserve only: branch state, plan file path, next phase number") to shed accumulated context.

**FR-9:** After compaction, the agent must re-read `final.plan.md` to confirm phase completion and identify the next phase before proceeding.

**FR-10:** If context usage exceeds 50% at any point during multi-phase execution, the agent must self-compact before continuing. The 50% threshold is lower than the global 65% rule because multi-phase runs accumulate faster.

**FR-11:** If context remains above 50% after compaction, the agent must stop and instruct the user to `/clear` and re-invoke `/sdlc implement`.

### Crash Recovery

**FR-12:** When resuming a phase that was interrupted, the agent must read the phase plan file and verify the on-disk state of every `Started` task before continuing. Tasks with verified work are marked `Completed` with recovery notes. Tasks without verified work are re-implemented.

**FR-13:** The agent must never mark a task `Completed` without verifying its described work exists on disk (files, functions, tests).

### Dispatcher Enhancements

**FR-14:** The `SKILL.md` dispatcher must support a fourth implement mode: `/sdlc implement phase NN all` (start at phase NN, continue through all remaining phases).

**FR-15:** The dispatcher must parse plan file paths in arguments (e.g., `sdlc/plan/phase03/plan.md`) and extract the phase number. Path alone maps to single-phase mode; path with continuation language ("and proceed", "and continue", "all remaining") maps to start-at-all mode.

**FR-16:** When routing to `implement.md`, the dispatcher must inject context about real-time status monitoring and phase isolation rules, ensuring these instructions arrive even in fresh contexts.

### Plan File Structure

**FR-17:** After the `expand` stage generates phase plans, the detailed task tables must be moved out of `final.plan.md` into the respective `phase{NN}/plan.md` files. Post-expand, `final.plan.md` must contain primarily a phase status table (Phase ID, phase plan path, status, started timestamp, completed timestamp, commit hash) and a growing collection of phase summary results appended as phases complete. The master plan is a dashboard, not a task list.

**FR-18:** Each `phase{NN}/plan.md` must contain: phase goal, task list (with full task-level status tracking), acceptance criteria, files expected to change, validation commands, and completion update instructions. The phase plan is the authoritative source for step-level status during implementation.

## 8. Non-Goals

- **Changing the plan file format.** Markdown tables, status values (`Open`, `Started`, `Completed`, `Blocked`), and PST timestamp format remain as-is.
- **Changing the one-commit-per-phase rule.** Each phase still produces exactly one commit.
- **Changing the task execution order.** Tasks within a phase are still executed top-to-bottom.
- **Modifying most pipeline prompts.** `draft-user`, `draft-pdr`, `draft-plan`, `gen-pdr`, `gen-plan`, and `finalize` are not affected. `expand` is affected — it must restructure the master plan when generating phase plans (see FR-17).
- **Automated `/clear` or `/rewind`.** The agent cannot invoke these programmatically in interactive mode. Context management uses `/compact` with fallback to instructing the user to `/clear`.
- **Agent SDK integration.** The checkpoint research (`docs/checkpoint.md`) explored SDK-level file checkpointing, but this work targets interactive Claude Code mode only. SDK integration is a separate future effort.
- **Concurrent session support.** Single-session execution is assumed.

## 9. Privacy and Storage Expectations

No new data storage. All state is written to existing plan file locations (`sdlc/docs/final.plan.md`, `sdlc/plan/phase{NN}/plan.md`) and committed to the project's Git repository. No external services, APIs, or telemetry are involved.

## 10. Acceptance Criteria

- [ ] **AC-1:** During a single-phase run, every task shows a distinct Edit tool call updating the phase plan file BEFORE the task's first implementation action and AFTER the task's last implementation action. The master plan is updated once at phase completion.
- [ ] **AC-2:** If a session is interrupted mid-phase and resumed with `/sdlc implement`, the agent correctly identifies `Started` tasks, verifies on-disk state, and continues without re-doing completed work.
- [ ] **AC-3:** During a 3+ phase "all" run, context usage drops measurably after each phase transition (visible in compact behavior). Phase N+1 starts with only bootstrap data plus phase N+1 plan in context.
- [ ] **AC-4:** The agent never reads a future phase's `plan.md` before committing the current phase.
- [ ] **AC-5:** The agent never launches an Explore subagent or project-wide scan before beginning implementation of the current phase.
- [ ] **AC-6:** `/sdlc implement phase 03 all` is correctly dispatched as "start at phase 03, continue all remaining."
- [ ] **AC-7:** `/sdlc implement sdlc/plan/phase03/plan.md` is correctly parsed and dispatched as phase 03.
- [ ] **AC-8:** The user can observe real-time task progress by reading `phase{NN}/plan.md` (step-level) and phase-level progress by reading `final.plan.md`.
- [ ] **AC-9:** If context exceeds 50% mid-phase, the agent self-compacts before continuing.
- [ ] **AC-10:** If context remains above 50% after compaction, the agent stops cleanly and instructs the user to `/clear` and re-invoke.

## 11. Concerns for Physical Design

1. **FR-1/FR-2 rely on prompt compliance, not enforcement.** The HARD RULE callouts and violation definitions strengthen the instruction, but there is no runtime mechanism to verify the agent actually updated plan files before writing code. The PDR should consider whether a hook-based enforcement is feasible (e.g., a `PreToolUse` hook that checks plan file timestamps).

2. **FR-8 depends on `/compact` effectiveness.** The quality of context shedding after `/compact` varies — the compaction model may retain more phase N context than desired. The PDR should define what "successful compaction" looks like and whether the 50% threshold needs tuning based on observed behavior.

3. **FR-17 requires `expand` to restructure `final.plan.md`** by moving task tables into phase plans and leaving the master plan as a status dashboard. The PDR must define the exact post-expand format of `final.plan.md` — column set for the phase status table, where phase summaries accumulate, and how the transition from pre-expand (full task tables) to post-expand (status table only) works.

4. **FR-17's new master plan columns** (commit hash, validation results) don't exist in the current format. The PDR must define whether this is a format migration applied to all plans or only to newly generated plans.

5. **The two-level monitoring model** (master plan = phase resolution, phase plans = step resolution) eliminates the per-task two-file sync friction from the original refactor analysis. The PDR should confirm that the `expand.md` prompt changes and the `implement.md` master-plan-at-phase-completion rule are sufficient to keep both files consistent without per-task dual updates.

7. **FR-15 path parsing must handle both forward and backslashes** on Windows. The dispatcher receives user input that may use either separator style. The PDR should specify normalization behavior.
