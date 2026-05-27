---
document: "User Requirements"
version: "1.0"
status: "final"
source: "sdlc/docs/draft.user.md"
finalized_date: "2026-05-27"
---

# SDLC Implement Hardening — User Requirements

## Gaps in Source Document

### Notable

- **Edit tool failure during status updates.** The draft does not address what happens if an Edit tool call fails when writing a `Started` or `Completed` marker to the phase plan. The agent has either started or finished implementation work but the plan file doesn't reflect it. This is an edge case — Edit failures are rare — but the recovery protocol (FR-12) should handle it as a variant of "work exists, status doesn't."
- **Plan file format validation.** The draft assumes plan files are well-formed markdown tables. No requirement addresses malformed plan files (missing columns, broken table syntax, manual edits that broke parsing). The hook (FR-20) and the implement prompt both need to parse plan files — the PDR must define what happens when parsing fails.
- **`_standards.md` does not exist.** Both `implement.md` and `expand.md` reference `sdlc/prompts/_standards.md` for phase table standards and commit protocol. This file is missing from disk. The PDR should decide whether to create it or inline the relevant standards into each prompt.

---

## 1. Overview

The SDLC prompt pipeline includes an `implement` stage that directs an AI agent to execute phased implementation plans — reading task tables, writing code, running tests, and committing per phase. In practice, three failure modes have repeatedly destroyed work during multi-phase runs:

1. **Lost status.** The agent completes tasks but defers or skips plan file updates. When the session crashes or compacts, there is no record of what was done. The next session restarts from scratch. This was observed during chatbot-factory Phase 02, where 14 of 15 tasks were completed with no plan file updates before context was lost.

2. **Context waste.** The agent pre-reads future phase plans and launches exploratory scans before writing code, consuming context on information it doesn't need yet. Observed during chatbot-factory Phase 03, where the agent read phases 04–05 and launched a full project explorer before starting phase 03 work.

3. **Context exhaustion.** Multi-phase runs accumulate file reads, narration, and tool output until compaction forces a lossy reset mid-work. By phase 3 or 4, the agent is working with a heavily loaded context and critical details are lost during compaction.

This project hardens the implement stage by making plan file updates non-negotiable (enforced by both prompt instructions and a runtime hook), isolating each phase's context, and managing the context lifecycle across phase boundaries. The changes touch three pipeline artifacts: `implement.md`, `expand.md`, and `SKILL.md`.

## 2. Personas

### 2.1 Human Operator

- **Role:** Software developer using the SDLC pipeline to build software with AI assistance. Invokes `/sdlc implement`, monitors progress, intervenes when the agent goes off-track, and recovers from interrupted sessions.
- **Goals:** Observe real-time progress at two granularities (phase-level in the master plan, step-level in phase plans). Recover from any interruption by re-invoking the implement command. Trust that the agent won't waste context or lose track of completed work.
- **Technical level:** Expert. Understands the prompt pipeline, plan file format, Claude Code's context model, and Git.

### 2.2 AI Agent (Claude Code)

- **Role:** The execution engine. Reads plan files, implements tasks, updates status, manages its own context lifecycle, and commits completed phases.
- **Goals:** Complete all tasks in a phase without violating status update rules, without reading unnecessary files, and without exhausting context before the phase is done.
- **Technical level:** Expert. Operates within the constraints of the implement prompt, the hook system, and the Claude Code runtime.

### 2.3 PreToolUse Hook

- **Role:** Runtime enforcement mechanism. Intercepts tool calls during `/sdlc implement` and verifies that the agent has updated the phase plan before writing source files.
- **Goals:** Block source file edits when no task is marked `Started` in the active phase plan. Never block plan file edits themselves. Never block non-implement work.
- **Technical level:** System actor. Python script registered in `~/.claude/settings.json`.

## 3. User Stories

### 3.1 Status Update Enforcement

| ID | As a... | I want to... | So that... | Priority | Acceptance Criteria |
|----|---------|-------------|-----------|----------|-------------------|
| US-001 | Human Operator | see each task's `Started` timestamp in the phase plan before the agent writes any code for that task | I know the exact moment work began and can detect if the agent is skipping updates | Must | Given a phase with Open tasks, when the agent begins task N, then `phase{NN}/plan.md` shows task N as `Started` with a PST timestamp before any source file is created or modified for that task |
| US-002 | Human Operator | see each task's `Completed` timestamp in the phase plan immediately after the agent finishes its implementation work | I can track completion in real-time and detect stalled tasks | Must | Given a task marked `Started`, when the agent finishes its implementation work, then `phase{NN}/plan.md` shows the task as `Completed` with a PST timestamp as the very next action — before verification, before the next task |
| US-003 | Human Operator | see the master plan updated once per phase with status, timestamp, and commit hash | I have a dashboard view of overall progress without noise from individual task transitions | Must | Given a completed phase, when the agent finishes verification and writes the phase summary, then `final.plan.md` shows the phase as `complete` with completion timestamp and commit hash |
| US-004 | Human Operator | know that batching, skipping `Started`, and deferring updates are explicitly prohibited | the agent has clear rules and I have clear violations to diagnose when something goes wrong | Must | Given the implement prompt, then the prompt text contains explicit prohibitions for: batching updates across tasks, skipping `Started` state, and deferring updates to after verification |

### 3.2 Hook-Based Enforcement

| ID | As a... | I want to... | So that... | Priority | Acceptance Criteria |
|----|---------|-------------|-----------|----------|-------------------|
| US-005 | Human Operator | have a runtime hook that blocks source file edits when no task is marked `Started` | the agent cannot silently skip status updates even under context pressure | Must | Given no task marked `Started` in the active phase plan, when the agent attempts to Edit/Write a source file, then the hook returns exit code 2 with an error message directing the agent to update the phase plan first |
| US-006 | Human Operator | have the hook distinguish source files from plan files | the hook never blocks plan file updates themselves | Must | Given the agent is editing `phase{NN}/plan.md` or `final.plan.md`, when the hook intercepts the tool call, then the hook allows it regardless of task status |
| US-007 | Human Operator | have the hook be inactive during non-implement work | the hook doesn't interfere with normal development, other `/sdlc` commands, or ad-hoc edits | Should | Given the agent is not executing `/sdlc implement`, when the agent edits any file, then the hook does not intercept or block |

### 3.3 Phase Isolation

| ID | As a... | I want to... | So that... | Priority | Acceptance Criteria |
|----|---------|-------------|-----------|----------|-------------------|
| US-008 | AI Agent | read only the current phase's `plan.md` during implementation | I don't waste context on future phases or drift toward over-engineering | Must | Given the agent is executing phase N, then no Read tool call targets `phase{M}/plan.md` where M > N before phase N is committed |
| US-009 | AI Agent | read the next phase's plan only after committing the current phase | phase boundaries are clean and context from phase N doesn't bleed into phase N+1 | Must | Given phase N is committed, when the agent proceeds to phase N+1, then the first Read of `phase{N+1}/plan.md` occurs after the phase N commit |
| US-010 | AI Agent | not launch exploratory agents before implementation begins | I don't waste context on project-wide scans when the phase plan's Context section provides everything I need | Should | Given the agent begins a phase, then no Explore subagent or project-wide scan is launched before the first task's implementation work begins |

### 3.4 Context Lifecycle

| ID | As a... | I want to... | So that... | Priority | Acceptance Criteria |
|----|---------|-------------|-----------|----------|-------------------|
| US-011 | AI Agent | run `/compact` with an aggressive focus phrase after each phase commit in multi-phase mode | accumulated context from the completed phase is shed before starting the next | Must | Given phase N is committed in "all" mode, then `/compact` runs with a focus phrase naming the completed phase and the next phase before any phase N+1 file reads |
| US-012 | AI Agent | re-read `final.plan.md` after compaction to confirm state | I don't proceed based on stale or compacted-away state | Must | Given `/compact` has run after phase N, then `final.plan.md` is re-read and the phase N completion is verified before phase N+1 begins |
| US-013 | AI Agent | self-compact at 50% context usage during multi-phase runs | I compact proactively before lossy auto-compaction hits | Must | Given context usage exceeds 50% during a multi-phase run, then the agent runs `/compact` before continuing work |
| US-014 | AI Agent | stop cleanly when context remains above 50% after compaction | the user can `/clear` and re-invoke rather than losing work to forced compaction | Should | Given context remains above 50% after a `/compact`, then the agent stops and outputs instructions for the user to `/clear` and re-invoke with the next phase number |

### 3.5 Crash Recovery

| ID | As a... | I want to... | So that... | Priority | Acceptance Criteria |
|----|---------|-------------|-----------|----------|-------------------|
| US-015 | Human Operator | recover from any session interruption by re-invoking `/sdlc implement` | I never need to manually audit which tasks were completed | Must | Given a session was interrupted mid-phase, when the user invokes `/sdlc implement` in a new session, then the agent reads the phase plan, identifies `Started` tasks, verifies on-disk work, and continues without re-doing verified completed work |
| US-016 | Human Operator | see recovery annotations in the plan file | I know which tasks were recovered vs. executed normally | Should | Given a task is recovered from an interrupted session, then the plan file shows `[recovered from interrupted session]` in the completion record |
| US-017 | AI Agent | never mark a task `Completed` without verifying its work exists on disk | I don't create false completion records that hide missing implementation | Must | Given a `Started` task during recovery, when the agent checks for its described work, then the task is only marked `Completed` if the files, functions, or tests described by the task actually exist |

### 3.6 Dispatcher Enhancements

| ID | As a... | I want to... | So that... | Priority | Acceptance Criteria |
|----|---------|-------------|-----------|----------|-------------------|
| US-018 | Human Operator | invoke `/sdlc implement phase NN all` to start at a specific phase and continue through remaining phases | I can resume multi-phase execution from a known point after a manual `/clear` | Must | Given the user runs `/sdlc implement phase 03 all`, then the agent starts at phase 03 and continues through all remaining phases autonomously |
| US-019 | Human Operator | pass a plan file path as an argument (e.g., `sdlc/plan/phase03/plan.md`) | I can use tab-completion or paste a path instead of remembering the phase number | Should | Given the user runs `/sdlc implement sdlc/plan/phase03/plan.md`, then the dispatcher extracts phase 03 and executes it |
| US-020 | Human Operator | append continuation language to a path argument (e.g., `sdlc/plan/phase03/plan.md and proceed with remaining phases`) | I can start-at-and-continue using a pasted path | Should | Given the user appends "and proceed with remaining phases" to a path argument, then the dispatcher treats it as `phase 03 all` mode |
| US-021 | Human Operator | have the dispatcher inject status monitoring and phase isolation reminders when routing to implement | the instructions arrive even in fresh contexts that haven't read the full prompt carefully | Must | Given the dispatcher routes to `implement.md`, then it prepends context about real-time status updates and phase isolation |

### 3.7 Plan File Structure

| ID | As a... | I want to... | So that... | Priority | Acceptance Criteria |
|----|---------|-------------|-----------|----------|-------------------|
| US-022 | Human Operator | have the `expand` stage move detailed task tables out of `final.plan.md` into phase plans | the master plan stays concise and readable as a dashboard | Must | Given `expand` has run, then `final.plan.md` contains a phase status table (Phase ID, path, status, timestamps, commit hash) but no individual task rows — those are in `phase{NN}/plan.md` only |
| US-023 | Human Operator | see phase summaries accumulate in the master plan as phases complete | the master plan grows into a history of what was built, with links to details | Must | Given phase N is completed, then `final.plan.md` contains a summary block for phase N below the status table |
| US-024 | Human Operator | have phase plans be the authoritative source for step-level status | there is one place to look for task status, not two competing sources | Must | Given a phase is in progress, then `phase{NN}/plan.md` is the only file with task-level status. `final.plan.md` shows only phase-level status |

## 4. Non-Functional Requirements

| ID | Category | Requirement | Target | Priority |
|----|----------|------------|--------|----------|
| NFR-001 | Latency | The PreToolUse hook must not add perceptible delay to tool calls | < 200ms per invocation | Must |
| NFR-002 | Reliability | The hook must fail open (allow the action) if it encounters an error parsing the plan file or determining context | Exit 0 on internal error; never block legitimate work due to a hook bug | Must |
| NFR-003 | Portability | The hook must work on Windows (the primary development platform) with both forward and backslash path separators | Correctly identify plan files and source files regardless of path separator | Must |
| NFR-004 | Context efficiency | A 3-phase multi-phase run must complete without hitting the context limit | Context usage after each phase transition should drop below 50% of window | Should |
| NFR-005 | Idempotency | Re-running `/sdlc implement` on a fully completed plan must be safe | Agent reads plan, finds no Open/Started tasks, reports "all phases complete" — no modifications | Must |
| NFR-006 | Backward compatibility | Projects that have not run `expand` with the new format must still work with the existing implement prompt | The implement prompt must handle both old-format (task tables in master plan) and new-format (task tables in phase plans only) master plans | Should |

## 5. Constraints and Assumptions

- **Single-session execution.** Only one Claude Code session operates on the plan files at a time. Concurrent session support is out of scope.
- **Interactive Claude Code mode only.** This work targets the interactive CLI. Agent SDK integration (programmatic checkpointing, session management) is a separate future effort.
- **`/compact` is the only programmatic context reset.** The agent cannot invoke `/clear` or `/rewind` programmatically — those are user commands. Context management between phases uses `/compact` with a fallback instruction to the user.
- **Plan files are valid markdown.** The implement prompt and hook assume plan files are well-formed markdown tables with the expected columns. The PDR should define graceful degradation for malformed files, but the requirement set does not mandate a validation step.
- **`scripts/sdlc-plan-state.py` may or may not exist.** The current implement prompt references this script as optional (with manual fallback). The requirements do not mandate the script — the prompt and hook must work without it.
- **PST timestamps.** All Started/Completed timestamps use Pacific Standard Time, format `YYYY-MM-DD HH:MM AM/PM`. This is an existing convention, not a new requirement.
- **Windows is the primary platform.** Path handling must support both `\` and `/` separators. The hook and dispatcher receive user input that may use either style.

## 6. Out of Scope

- **Changing the plan file format.** Markdown tables, status values (`Open`, `Started`, `Completed`, `Blocked`), and PST timestamp format remain as-is within phase plans.
- **Changing the one-commit-per-phase rule.** Each phase still produces exactly one commit.
- **Changing the task execution order.** Tasks within a phase are still executed top-to-bottom.
- **Modifying upstream pipeline prompts.** `draft-user`, `draft-pdr`, `draft-plan`, `gen-user`, `gen-pdr`, `gen-plan`, and `finalize` are not affected.
- **Automated `/clear` or `/rewind`.** The agent cannot invoke these programmatically.
- **Agent SDK integration.** The checkpoint research (`docs/checkpoint.md`) explored SDK-level file checkpointing, but this work targets interactive mode only.
- **Concurrent session support.** Single-session execution is assumed.
- **Creating `_standards.md`.** Referenced by prompts but missing from disk. Creating it is a separate housekeeping task.

## 7. Concerns for Physical Design

1. **FR-20 / US-005 hook design.** The PDR must define: which tool calls the hook intercepts (Edit, Write, Bash, or all three), how it identifies "source files" vs plan files, how it locates the active phase plan, and how it determines whether a `Started` task exists. The hook follows the pattern of the existing push guard (`~/.claude/hooks/pre-bash-git-push-guard.py`) — block and explain, never silently pass. It must also define how the hook knows it's in an `/sdlc implement` context vs. normal development (US-007).

2. **US-011 / FR-8: `/compact` effectiveness.** The quality of context shedding after `/compact` varies — the compaction model may retain more phase N context than desired. The PDR should define what "successful compaction" looks like and whether the 50% threshold needs tuning based on observed behavior.

3. **US-022 / FR-17: `expand` restructuring of `final.plan.md`.** The PDR must define the exact post-expand format of `final.plan.md` — column set for the phase status table, where phase summaries accumulate, and how the transition from pre-expand (full task tables) to post-expand (status-only dashboard) works mechanically.

4. **FR-17 new master plan columns.** Commit hash and validation results don't exist in the current format. The PDR must define whether this is a format migration applied to all plans or only to newly generated plans. NFR-006 requires backward compatibility with old-format plans.

5. **US-022 / NFR-006 tension.** The new expand behavior removes task tables from the master plan, but NFR-006 requires the implement prompt to handle both old and new formats. The PDR must define how the implement prompt detects which format it's working with and adjusts behavior accordingly.

6. **US-019 / FR-15: path parsing on Windows.** The dispatcher receives user input that may use either `\` or `/` separators and may include or omit the `sdlc/plan/` prefix. The PDR should specify normalization behavior and the regex or parsing logic for extracting the phase number.

7. **Hook activation scope (US-007).** The hook must distinguish `/sdlc implement` sessions from normal work. Options include: a sentinel file written by the implement prompt, an environment variable, or a convention-based approach (only activate when a phase plan with `Started` tasks exists). The PDR must choose a mechanism that doesn't require the user to manually toggle the hook.
