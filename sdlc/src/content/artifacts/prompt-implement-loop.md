---
title: "Implement Prompt — Execution Loop"
type: "prompt"
command: "implement"
excerpt: true
sortOrder: 3
---

The `implement` command follows this exact sequence for each phase. This is from the actual prompt that drives phase execution:

**1. Read state** — Read `final.plan.md`, find the active phase, read the phase plan.

**2. Execute tasks in order** — For each task, top to bottom:
- Mark it `Started` with a PST timestamp in both plan files
- Read the phase plan's Context section for implementation guidance
- Do the work (write code, create files, write tests)
- Mark it `Completed` with a PST timestamp

**3. Run verification** — Execute the checks listed in the phase plan (tests, lint, behavioral checks). Fix failures until green.

**4. Write Phase Summary** — Record what was created, modified, or configured.

**5. Commit** — One commit per phase, message reflects the phase scope. Do not push.

The prompt is designed to be run repeatedly — it picks up where it left off by reading plan state.
