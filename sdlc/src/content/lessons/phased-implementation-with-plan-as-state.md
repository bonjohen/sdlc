---
title: "Phased Implementation with Plan-as-State"
summary: "Using markdown plan tables as the task state machine with timestamp audit trails."
category: "process"
sortOrder: 4
---

## The Lesson

Using the plan document itself as the task state tracker — with timestamps written directly into markdown tables — enables strict one-commit-per-phase discipline and makes progress machine-readable without requiring external project management tools. The plan is both the specification and the status board.

## Context

A 6-phase implementation of a static site was executed by an AI agent (Claude Code) following a phased release plan. Each phase had 5-8 tasks tracked in a markdown table with Status, Started (PST), and Completed (PST) columns. The same task table existed in two places: the master plan (`final.plan.md`) and the per-phase execution plan (`plan/phase{NN}/plan.md`). The agent updated both as it worked, committed once per phase, and never committed partial work.

## What Happened

1. The finalized plan defined 6 phases with task tables in `final.plan.md`. Each task row had columns: No, Status, Started, Completed, Description.
2. The `expand` step generated per-phase plans with identical task tables plus detailed context (files to create, patterns to follow, import paths).
3. During execution, the agent flipped each task to "Started" with a PST timestamp, did the work, then flipped to "Completed" with another timestamp. Both files were updated.
4. When all tasks in a phase reached Completed, the agent wrote a Phase Summary block, staged all changes (code + updated plan files), and committed with a phase-scoped message.
5. Phase 00 task 00.7 (deploy to GitHub Pages) was marked "Blocked" because no remote repository was configured. The blocked state was recorded in the plan with a note explaining why.

## Key Insights

- **Markdown tables are a surprisingly good state machine.** The Status column with defined transitions (Open -> Started -> Completed, with a Blocked branch) is a finite state machine encoded in a format humans can read and AI agents can parse. No database, no API, no project management tool required.
- **Two-file state with an authority rule prevents drift.** Having the task table in both `final.plan.md` (master) and `plan/phase{NN}/plan.md` (detail) means you can see big-picture progress OR phase-level context. The rule "if they drift, `final.plan.md` is authoritative" prevents ambiguity.
- **PST timestamps create an execution audit trail.** Knowing that task 00.1 started at 3:45 PM and completed at 3:48 PM (3 minutes) vs. task 01.1 taking 12 minutes tells you where complexity actually lives.
- **One commit per phase is enforceable when the plan is the tracker.** The commit protocol says: "stage and commit when every task in the phase is Completed." This is mechanically verifiable by reading the plan.
- **Blocked states with notes prevent false-negative confusion.** Without an explicit Blocked state, a task stuck at Open could mean "not started yet" or "can't proceed." The Blocked state with a note distinguishes intentional deferral from oversight.

## Applicability

This pattern works well for: AI-agent-executed work (agents parse markdown reliably), solo projects without team coordination overhead, and any project where the plan is the only project-management tool.

It does NOT scale to: large teams needing concurrent task assignment (markdown merge conflicts), tasks with complex dependency graphs (the table can't express DAGs), or workflows requiring notifications/integrations.
