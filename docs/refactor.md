# Refactor: Enforce Real-Time Plan Status Updates

**Date:** 2026-05-27
**Triggered by:** chatbot-factory Phase 02 — agent completed 14/15 tasks without updating plan.md, then lost context on compaction. No recovery point existed because plan files still showed all tasks as "Open."

## Problem

The `implement.md` prompt already instructs the agent to update task status in both `final.plan.md` and `phase{NN}/plan.md` as each task starts and completes (Section 2, steps a and d). In practice, agents batch these updates or skip them entirely when under pressure from large phases with many tasks. The instruction exists, but it isn't enforced strongly enough to survive context pressure.

This creates two failures:

1. **No recovery point.** If the session crashes, compacts, or is interrupted mid-phase, the plan files show all tasks as "Open" even though code was written. The next session has no way to know what was done without reading every file. This is the primary failure — the plan-as-state-machine pattern only works if state is actually written.

2. **No observability.** The user monitors progress by reading plan files. If statuses aren't updated, the user can't tell what's happening, can't redirect, and can't intervene before the agent goes off-track. The user explicitly requested this capability.

## Root Cause

The current instruction in `implement.md` lines 52-55 and 76-79 says to update status but doesn't make it the *first and last* action for each task. The agent treats it as one of many things to do and deprioritizes it when the task itself is complex.

The two-file update requirement (both `final.plan.md` and `phase{NN}/plan.md`) doubles the friction, making agents more likely to defer updates to a batch at the end.

## Proposed Changes

### 1. Strengthen the status update instructions in `implement.md`

**Current (Section 2, step a):**
```markdown
**a. Start the task.**
Update the task row in BOTH `final.plan.md` and `phase{NN}/plan.md`:
- Status: `Open` → `Started`
- Started (PST): current datetime, e.g. `2026-05-21 02:30 PM`
```

**Proposed — add a hard rule callout and reorder to make it non-negotiable:**

```markdown
**a. Start the task — update plan files FIRST.**

> **HARD RULE:** Edit both plan files BEFORE doing any implementation work for
> the task. This is the recovery point. If the session crashes after this edit,
> the next session knows this task was in progress. If you skip this edit,
> crash recovery is impossible.

Update the task row in BOTH `final.plan.md` and `phase{NN}/plan.md`:
- Status: `Open` → `Started`
- Started (PST): current datetime, e.g. `2026-05-21 02:30 PM`

Do not write any code, create any files, or run any commands for this task
until both plan files show the task as `Started`.
```

Apply the same pattern to step d (completion):

```markdown
**d. Complete the task — update plan files IMMEDIATELY.**

> **HARD RULE:** Edit both plan files as the very next action after finishing
> the task's implementation work. Do not move to the next task, do not start
> verification, do not batch updates. The plan file update IS the completion
> signal.

Update the task row in BOTH `final.plan.md` and `phase{NN}/plan.md`:
- Status: `Started` → `Completed`
- Completed (PST): current datetime, e.g. `2026-05-21 02:45 PM`
```

### 2. Add a State Management Violations section

After the existing "State Management Rules" section (line 125), add:

```markdown
### Status update violations

The following are violations that break the plan-as-state-machine contract:

1. **Batching updates.** Writing code for multiple tasks before updating any
   plan file. This is the most common violation and the most damaging — it
   turns a recoverable crash into an unrecoverable one.

2. **Skipping Started.** Going directly from Open to Completed. The Started
   timestamp is the "I'm working on this now" signal. Without it, there is no
   way to distinguish "not yet attempted" from "attempted and crashed."

3. **Updating one file but not the other.** Both files must be updated in the
   same action. If you update `phase{NN}/plan.md` but not `final.plan.md`,
   the master plan drifts and the next session may restart completed work.

4. **Deferring updates to "after verification."** Verification is step 3.
   Task status updates happen in step 2. Do not wait for tests to pass before
   marking a task Completed — the task is complete when its implementation
   work is done. If verification later reveals a bug, you fix it as part of
   verification, not by reopening the task.
```

### 3. Add a recovery protocol

After the existing "Resumption" section (line 151), add:

```markdown
### Recovery after interrupted session

When resuming a phase that was interrupted (context loss, crash, compaction):

1. Read both plan files. Note which tasks are Started, Completed, or Open.
2. For each `Started` task: verify the described work actually exists on disk
   (check for the files, functions, or tests it describes). If the work
   exists, mark it Completed with an estimated timestamp and a note:
   `[recovered from interrupted session]`. If the work does not exist, leave
   it Started and redo it.
3. For each `Open` task after a `Completed` or `Started` task: verify no
   partial work exists. If partial work exists, mark it Started and complete
   it. If no work exists, proceed normally.
4. Never mark a task Completed without verifying its work exists.
```

### 4. Simplify the two-file update

The two-file synchronization requirement is the biggest source of friction. Consider one of these options:

**Option A: Single-file authority, sync at phase boundary.**

Change the rule so the agent only updates `phase{NN}/plan.md` during execution. At phase completion (before commit), sync the phase plan's task table back to `final.plan.md`. This cuts the per-task update cost in half.

Pros: Less friction per task, more likely to actually happen.
Cons: Master plan lags during execution; user monitoring the master plan sees stale data.

**Option B: Keep both files, but use a consistent edit pattern.**

Provide an exact template the agent can copy-paste:

```markdown
When updating task status, always edit the phase plan first, then the master
plan. Use this exact sequence:

1. Edit `sdlc/plan/phase{NN}/plan.md` — change the task row
2. Edit `sdlc/docs/final.plan.md` — change the same task row
3. Continue to the next action

This is two Edit tool calls. Do them back-to-back. Do not interleave other
work between them.
```

**Recommendation: Option B.** The user explicitly said they watch progress in real-time, which means the master plan must be current. The two-edit pattern is mechanical enough to survive prompt pressure if the instruction is clear.

### 5. Add observability guidance to SKILL.md

In the `implement` routing section of SKILL.md (around line 76), add a note that the dispatcher should inject:

```markdown
When routing to `skill/implement.md`, always prepend this context:

"The user monitors plan file status in real-time. Task status updates in both
plan files are the primary progress signal. Update status BEFORE starting
work (Started) and IMMEDIATELY after finishing work (Completed). Never batch
status updates across multiple tasks."
```

This ensures the instruction arrives even when `implement.md` is loaded into a fresh context that hasn't read the full prompt carefully.

## Files to Modify

| File | Change |
|------|--------|
| `skill/implement.md` | Strengthen steps 2a and 2d with HARD RULE callouts; add Status Update Violations section; add Recovery protocol section |
| `skill/SKILL.md` | Add status-update context injection when routing to implement.md |

## What This Does NOT Change

- The plan file format (markdown tables, status values, timestamp format)
- The two-file state model (both files remain authoritative)
- The one-commit-per-phase rule
- The task execution order (still top-to-bottom)
- Any other prompt in the pipeline (draft, gen, finalize, expand)

## Verification

After applying these changes, the next `/sdlc implement` run should show:
1. Each task's plan file update appears as a distinct Edit tool call before/after the task's implementation work
2. If interrupted mid-phase and resumed, the agent correctly identifies which tasks were started/completed by reading the plan files
3. The user can observe real-time progress by reading either plan file during execution

---

# Refactor: Prevent Phase Plan Pre-Reading in Implement Mode

**Date:** 2026-05-27
**Triggered by:** chatbot-factory Phase 03 — agent pre-read phase 04, 05, and launched a full project explorer before starting phase 03 implementation. Wasted context window on plans that weren't needed yet.

## Problem

When given `/sdlc implement sdlc\plan\phase03\plan.md and proceed with remaining phases`, the agent read the phase 03 plan, then immediately read phase 04 and phase 05 plans, and launched an Explore agent to scan the entire project structure — all before writing a single line of code. None of the future-phase reads were needed. The current phase plan and the existing source files it depends on are sufficient to implement it.

This creates two failures:

1. **Context waste.** Each phase plan is 200+ lines. Reading three unnecessary plans consumed ~600 lines of context that could have been used for actual implementation work. In a context-limited environment, this directly reduces the amount of work that can be done before compaction.

2. **Scope drift.** Reading future phases primes the agent to think about future work, increasing the chance of over-engineering the current phase to "prepare" for later phases. Each phase should be implemented against its own spec, not against a mental model of the whole project.

## Root Cause

Two things are missing:

1. **`sdlc/prompts/implement.md` doesn't exist.** The dispatcher routes to this file, but it was never created. Without an implement prompt, the agent has no guardrails on its behavior during implementation. It freelances — and freelancing includes "let me read everything to understand the full picture."

2. **The dispatcher doesn't handle plan-file-path arguments.** The user passed `sdlc\plan\phase03\plan.md` as an argument, but the dispatcher only recognizes `all`, `phase NN`, or no argument. An unrecognized argument is ignored, so the agent doesn't know it's been told to start at phase 03.

## Proposed Changes

### 1. Create `sdlc/prompts/implement.md` with phase-isolation rules

The implement prompt must include an explicit constraint:

```markdown
## Phase Isolation Rule

Read only the current phase's `plan.md`. Do not read future phase plans,
the master plan's future phases, or any file not directly needed for the
current task.

When in "all remaining" mode, read the next phase's plan.md only AFTER
committing the current phase. The sequence is:

1. Read phase N plan.md
2. Implement phase N (all tasks)
3. Commit phase N
4. Read phase N+1 plan.md  ← not before this point
5. Implement phase N+1
6. ...

Do not pre-read. Do not "scan ahead." Do not launch exploratory agents
to understand the full project unless a specific task requires it.
The phase plan's Context section contains all the context you need.
```

### 2. Add a fourth dispatch mode to `SKILL.md`

Current modes:

| Invocation | Behavior |
|---|---|
| `/sdlc implement` | Next incomplete phase, then stop. |
| `/sdlc implement all` | All remaining phases, no pause. |
| `/sdlc implement phase NN` | Specific phase NN. |

Add:

| Invocation | Behavior |
|---|---|
| `/sdlc implement phase NN all` | Start at phase NN, continue through remaining phases autonomously. |

### 3. Parse plan file paths in the dispatcher

When the argument contains a path like `sdlc/plan/phase03/plan.md` or `sdlc\plan\phase03\plan.md`, extract the phase number (`03`) and treat it as `/sdlc implement phase 03`. If followed by "and proceed with remaining phases" or similar continuation language, treat it as `/sdlc implement phase 03 all`.

Add to the dispatcher's argument parsing section:

```markdown
### Plan file path parsing

If the argument contains a path matching `phase{NN}` (e.g.,
`sdlc/plan/phase03/plan.md`, `sdlc\plan\phase05\plan.md`), extract NN
as the target phase number.

- Path alone → `/sdlc implement phase NN`
- Path + continuation language ("and proceed", "and continue",
  "and remaining", "all remaining") → `/sdlc implement phase NN all`
```

### 4. Add context-injection to the dispatcher for all implement modes

When routing to `implement.md`, the dispatcher should always prepend:

```markdown
"Read only the current phase plan. Do not read future phase plans until
the current phase is committed. The phase plan's Context section provides
all schema, imports, and patterns needed for implementation."
```

This ensures the phase-isolation rule arrives even if the implement prompt is long and the agent skims it.

## Files to Modify

| File | Change |
|------|--------|
| `prompts/implement.md` | Add Phase Isolation Rule section (create file if missing) |
| `skill/SKILL.md` | Add `phase NN all` dispatch mode; add plan-file-path parsing; add context injection for phase isolation |

## What This Does NOT Change

- The implement prompt's task execution loop (still top-to-bottom within a phase)
- The plan file format
- The commit-per-phase rule
- The status update rules (covered by the previous refactor entry)

## Verification

After applying these changes:
1. `/sdlc implement phase 03 all` reads only phase 03's plan before starting, not phase 04+
2. After committing phase 03, the agent reads phase 04's plan — not before
3. `/sdlc implement sdlc/plan/phase03/plan.md` is correctly parsed as phase 03
4. No exploratory agents are launched to "understand the project" before implementation begins

---

# Refactor: Context Lifecycle Management for Multi-Phase Implement

**Date:** 2026-05-27
**Triggered by:** Continuation of the phase-isolation refactor. Even with isolation rules, a multi-phase "all" run accumulates context from every phase — old file reads, completed task narration, stale tool output — until it hits the context limit and compacts lossy. The agent needs an explicit context reset between phases.

## Problem

When running `/sdlc implement all` across many phases, the context window fills with:
- File reads from phase N that are irrelevant to phase N+1
- Step-by-step narration of completed work
- Tool output from tests, lint, git commands
- The phase N plan itself (200+ lines, no longer needed)

By phase 3 or 4, the agent is working with a heavily loaded context. Compaction is lossy — it summarizes rather than preserves, and critical details (current branch, task status, file paths) can be lost. The current approach treats context as append-only until compaction forces a reset, which is the worst time to reset because the agent is mid-work.

## Proposed Design: Checkpoint-and-Reset Loop

The implement prompt should manage context as a deliberate lifecycle, not an accident of accumulation. The loop for multi-phase execution:

```
1. /clear — start with empty context
2. Read project bootstrap data:
   - CLAUDE.md, template.toml (project config)
   - final.plan.md (find next open phase)
   - Memory files (MEMORY.md index)
3. Create checkpoint (conversation snapshot before phase work)
4. Read ONLY the current phase's plan.md
5. Read ONLY the source files identified in the phase plan's Context section
6. Execute all tasks in the phase
7. Commit the phase
8. Update the phase summary in final.plan.md
9. Identify the next open phase number
10. /clear — discard all phase N context
11. Restore from checkpoint (project bootstrap data is back)
12. GOTO step 4 with the next phase

On final phase completion:
13. /clear
14. Restore checkpoint
15. No phase to load — done. Report completion summary.
```

### What "checkpoint" means

The checkpoint is not a literal conversation snapshot (Claude Code doesn't support that). It's a **re-read of the minimal bootstrap set** after each `/clear`. The "checkpoint" is the list of files to re-read:

- `CLAUDE.md` (project rules)
- `template.toml` (project state)
- `sdlc/docs/final.plan.md` (master plan — to find next phase and verify previous phase was committed)
- `MEMORY.md` (auto-memory index)

This is ~4 file reads. Compared to the 50+ file reads accumulated during a phase, this is a >90% context reduction.

### What `/clear` means in practice

Claude Code's `/clear` resets the conversation history. The implement prompt can't literally invoke `/clear` — it's a user command. Instead, the implement prompt should instruct:

**Option A: Use `/compact` with aggressive focus.**
After committing phase N, run `/compact "starting phase N+1, discard all phase N context"`. This tells the compaction model to aggressively drop phase N details and preserve only the bootstrap state.

**Option B: Instruct the user to `/clear` between phases.**
The implement prompt tells the agent to stop after each phase commit with: "Phase N complete. Run `/clear` then `/sdlc implement` to continue with phase N+1." This gives the user the cleanest possible context but requires manual intervention between phases.

**Option C: Self-compact via summarization.**
After committing phase N, the agent writes a one-line summary to the plan file, then deliberately forgets phase N details by not referencing them. This is the weakest option — the context is still there, just unused.

**Recommendation: Option A with Option B as fallback.** The agent runs `/compact` with an aggressive focus phrase after each phase commit. If context is still above 50% after compaction, it tells the user to `/clear` and re-invoke.

### Integration with phase-isolation rules

This supersedes the simpler "read next phase only after committing current" rule from the previous refactor. The sequence is now:

1. Commit phase N
2. Update `final.plan.md` with phase N summary
3. `/compact "phase N complete, starting phase N+1, preserve only: branch state, plan file path, next phase number"`
4. Re-read `final.plan.md` to confirm phase N is marked complete
5. Read phase N+1 `plan.md`
6. Begin phase N+1 tasks

### What the implement prompt needs to encode

The implement prompt must include:

```markdown
## Context Lifecycle (multi-phase mode)

When executing multiple phases ("all" or "phase NN all" mode):

### Before each phase:
- Read `sdlc/docs/final.plan.md` to identify the next open phase
- Read `sdlc/plan/phase{NN}/plan.md` for the target phase
- Read only the source files listed in the phase plan's Context section
- Do not read any other phase plans or unrelated source files

### After each phase:
1. Commit the phase (all tasks complete, tests pass, lint clean)
2. Update the phase summary block in `final.plan.md`
3. Run `/compact "phase NN complete, starting phase NN+1"` to shed
   accumulated context from the completed phase
4. Re-read `final.plan.md` to confirm state and find next phase
5. If no more open phases, report completion and stop

### Context budget rule:
If at any point you estimate context usage exceeds 50%, run `/compact`
with a focus phrase describing the current task before continuing.
Do not wait for 65% — multi-phase runs accumulate faster than
single-phase work.

### If `/compact` is insufficient:
If context remains above 50% after compaction, stop and tell the user:
"Context is too full to continue cleanly. Run `/clear` then
`/sdlc implement` to continue from phase {next_phase}."
```

## Files to Modify

| File | Change |
|------|--------|
| `prompts/implement.md` | Add Context Lifecycle section for multi-phase mode |
| `skill/SKILL.md` | Update "all" mode routing to inject context lifecycle instructions |

## What This Does NOT Change

- Single-phase mode (`/sdlc implement` with no `all`) — no context lifecycle needed
- The plan file format
- The commit-per-phase rule
- The status update rules

## Interaction with Previous Refactors

- **Status updates (refactor #1):** Still applies. Status updates happen within each phase, unaffected by context resets between phases.
- **Phase isolation (refactor #2):** Subsumed by this refactor. The isolation rule becomes a natural consequence of the checkpoint-and-reset loop — you can't read future phases if you clear context between them.

## Verification

After applying these changes:
1. A 3-phase "all" run completes without hitting the context limit
2. Context usage drops measurably after each phase transition (visible in `/compact` behavior)
3. Phase N+1 starts with only bootstrap data + phase N+1 plan in context
4. If context exceeds 50% mid-phase, the agent self-compacts before continuing
5. The user is never surprised by a mid-work context loss — resets are deliberate and announced
