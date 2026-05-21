---
name: "implement"
purpose: "Execute phase plans — write code, update task status, verify, and commit"
input: "sdlc/docs/final.plan.md and sdlc/plan/phase{NN}/plan.md for the target phase"
output: "Working code, updated task tables with timestamps, one commit per phase"
path: "document"
sortOrder: 8
---

The `implement` command is the execution engine. It reads the plan state, finds the next incomplete phase, and works through each task: marking it started, doing the implementation work, running verification, and marking it complete with PST timestamps.

It updates both the master plan and the per-phase plan as it goes, writes a phase summary, and commits. It can run in single-phase mode (default) or autonomous mode (all remaining phases end-to-end).
