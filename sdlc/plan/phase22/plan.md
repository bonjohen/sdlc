---
phase: 22
title: "Dispatcher Enhancements"
depends_on: "Phase 21 (dispatcher routes to implement.md; new modes must match the rewritten prompt's expectations)"
goal: "skill/SKILL.md supports the new phase NN all dispatch mode, plan file path parsing, and context injection when routing to implement."
source_pdr_sections: ["4.4"]
source_user_stories: ["US-018", "US-019", "US-020", "US-021"]
status: "open"
---

# Phase 22: Dispatcher Enhancements

## Tasks

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 22.1 | Open | | | Add `phase NN all` to the Implement Options table in `skill/SKILL.md`: "Start at phase NN, continue through all remaining phases autonomously." Add routing logic: after reading implement.md, inject "Execute in autonomous mode starting at phase NN." |
| 22.2 | Open | | | Add Plan File Path Parsing section: regex `phase[/\\]?(\d{2})` to extract phase number from path arguments. Map path-alone to single-phase mode, path + continuation language ("and proceed", "and continue", "and remaining", "all remaining") to `phase NN all` mode. |
| 22.3 | Open | | | Implement Windows backslash normalization in path arguments: normalize `sdlc\plan\phase03\plan.md` to `sdlc/plan/phase03/plan.md` before regex matching. |
| 22.4 | Open | | | Add context injection block: when routing to `implement.md`, prepend the status monitoring and phase isolation reminders per PDR 4.4. |
| 22.5 | Open | | | Update the Pipeline Summary's implement section if needed to reflect the four dispatch modes. |

## Context

### Files to Create or Modify

- `skill/SKILL.md` — **Modify.** Add new dispatch mode, path parsing logic, and context injection. Current file has ~114 lines with three implement modes in the options table.

### Current Implement Options Table (in `skill/SKILL.md`)

```markdown
| Invocation | Behavior |
|------------|----------|
| `/sdlc implement` | Execute the next incomplete phase, then stop. |
| `/sdlc implement all` | Execute all remaining phases end-to-end... |
| `/sdlc implement phase NN` | Execute phase NN specifically... |
```

**Add this row:**

```markdown
| `/sdlc implement phase NN all` | Start at phase NN, continue through all remaining phases autonomously. |
```

### Path Argument Parsing Logic

Add a new section to the dispatcher (before the routing logic):

```markdown
### Plan file path parsing

If the argument contains a file path rather than a keyword:

1. Normalize backslashes to forward slashes.
2. Match against regex: `phase[/\\]?(\d{2})`
3. Extract the two-digit phase number as NN.

Dispatch rules:
- Path alone → `/sdlc implement phase NN` (single-phase)
- Path + continuation language → `/sdlc implement phase NN all`

Continuation language (case-insensitive):
- "and proceed with remaining phases"
- "and continue"
- "all remaining"
- "and remaining"
```

**Examples:**

| User input | Parsed as |
|-----------|-----------|
| `/sdlc implement sdlc/plan/phase03/plan.md` | `/sdlc implement phase 03` |
| `/sdlc implement sdlc\plan\phase03\plan.md` | `/sdlc implement phase 03` |
| `/sdlc implement sdlc/plan/phase03/plan.md and proceed with remaining phases` | `/sdlc implement phase 03 all` |
| `/sdlc implement phase03/plan.md all remaining` | `/sdlc implement phase 03 all` |

### Context Injection

When routing to `implement.md` (any mode), prepend this context block:

```markdown
**Status monitoring reminders:**
- Update the phase plan file BEFORE starting each task (Started) and
  IMMEDIATELY after finishing each task (Completed).
- The master plan is updated once per phase at completion.
- Read only the current phase's plan — do not read future phase plans
  until the current phase is committed.
```

This injection ensures the critical rules arrive even in fresh contexts that haven't read the full implement prompt carefully.

### Routing Logic for New Mode

After reading `implement.md`, add this instruction for `phase NN all`:

```markdown
"Execute in autonomous mode starting at phase NN. Complete phase NN, commit,
compact, and immediately proceed to phase NN+1. Continue through all remaining
phases without waiting for user input. Stop only for destructive actions,
errors, or context limits."
```

### Design Notes

- **Path parsing is best-effort.** If the regex doesn't match, fall back to treating the argument as a keyword (existing behavior). Don't error on unrecognized path formats.
- **Windows backslash normalization** happens before regex matching, so `phase[/\\]?(\d{2})` needs to handle both separators in the raw input (before normalization) for robustness.
- **Context injection is additive** — it prepends reminders, it doesn't replace the implement prompt's own instructions. If the implement prompt is read carefully, the reminders are redundant. If context pressure causes the agent to skim, the reminders catch the critical points.
- **The Pipeline Summary diagram** in SKILL.md may need a note about the four implement modes, but the diagram itself doesn't need structural changes.

### Verification

- [ ] `skill/SKILL.md` contains four implement modes in the options table (was three)
- [ ] The dispatcher recognizes `/sdlc implement phase 03 all` and routes correctly
- [ ] The dispatcher parses `sdlc/plan/phase03/plan.md` and extracts phase 03
- [ ] The dispatcher parses `sdlc\plan\phase03\plan.md` (backslash) and extracts phase 03
- [ ] The dispatcher parses `sdlc/plan/phase03/plan.md and proceed with remaining phases` as phase 03 all
- [ ] The dispatcher injects status and isolation context when routing to implement
- [ ] Unrecognized path formats fall back gracefully (no error, treated as keyword)

## Phase Summary

_To be filled after completion._

- **Changes:** TBD
- **Commit:** TBD
