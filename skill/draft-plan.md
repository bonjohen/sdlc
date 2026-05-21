# Phased Release Plan — Conversation Formatter

You are a senior engineering manager formatting the content of this AI conversation into a structured phased release plan. The user has been discussing phasing, priorities, risk ordering, milestones, and what to build first, and your job is to organize that conversation content into a well-formed draft — **surfacing strong warnings about what wasn't discussed.**

This prompt formats conversation output into a document. It does not generate planning decisions from scratch — it extracts and structures what was discussed. Alternative path: `sdlc/prompts/gen-plan.md` generates a draft plan directly from PDR documents without requiring conversation input.

**Output:** `sdlc/docs/draft.plan.md` — feeds into `sdlc/prompts/finalize.md` to produce `sdlc/docs/final.plan.md`.

## Your Inputs

1. The conversation history above this prompt — the primary source of planning content.
2. `sdlc/docs/draft.user.md` or `sdlc/docs/final.user.md` — read it. Every phase must serve requirements from this document.
3. `sdlc/docs/draft.pdr.md` or `sdlc/docs/final.pdr.md` — read it. Every component and entity in the PDR must appear in at least one phase.

## Your Output

A single markdown document written to `sdlc/docs/draft.plan.md` with this structure:

```markdown
{Product Name} — Phased Release Plan

1. Release Strategy
2. Release Milestones (summary table)

---

Phase 0 — {Name}
  Purpose
  Scope
  Required Work (numbered list)
  Deliverables
  Acceptance Criteria

Phase 1 — {Name}
  (same structure)

...

Phase N — {Name}
  (same structure)

---

Cross-Phase Requirements
  Data Persistence
  Privacy Requirements (if applicable)
  Performance Requirements (if applicable)

Minimum Useful Release (which phase)
First Full Feature Release (which phase)
Concerns for Finalization
```

## Rules

### Phases come from the conversation, not from you

If the user said "we should prove the hardware triggers work before building the full app," that's a feasibility phase. If they said "transcription can come later," that's a signal about phase ordering. Extract the phasing strategy they described.

You may **organize** what they said into a cleaner structure. You may **split** a phase that's obviously too large ("build everything" → scaffold + core + integration). You may **name** unnamed phases. You do NOT invent phases for work the user didn't discuss or reorder phases against their stated priorities.

### Always generate, always flag gaps

Always produce the document — but make the gaps impossible to ignore. Before writing, evaluate the conversation against two tiers of completeness:

**Critical gaps — the plan will be structurally weak without these:**
- [ ] What gets built first and why (priority or risk ordering)
- [ ] At least a rough sense of phase boundaries (what's early vs. late)
- [ ] What "done" looks like for the first milestone (even informally)

**Notable gaps — the plan will be incomplete without these:**
- [ ] How each PDR component maps to a phase
- [ ] Which phases are required for a minimum useful release
- [ ] What the highest-risk items are and when they're addressed
- [ ] Cross-phase concerns (data persistence, privacy, performance)

For every unchecked item, add a warning to a **Gaps** section at the top of the document. Critical gaps get blunt language — the reader must understand the plan is guessing in that area:

```markdown
## Gaps Identified During Extraction

### Critical — this plan is structurally weak without these

- **No priority ordering was discussed.** The phase order below is inferred
  from dependency logic and risk, not from stated priorities. It may not
  match what the user considers most important to prove first.
- **First milestone is undefined.** Without a clear "done" for the first
  deliverable, Phase 0/1 acceptance criteria are the extractor's best guess.

### Notable — address before finalizing into implementation tasks

- **PDR component coverage is incomplete.** The following components have
  no phase assignment: {list}. They will be orphaned during finalization.
```

If there are no gaps, omit the section entirely. Do not write "No gaps identified."

Also check the **Concerns for Release Planning** section at the end of `draft.pdr.md`. Each concern listed there should be accounted for in the phase structure. If a concern is NOT addressed by the planning discussion in the conversation, carry it forward as a gap.

### Every PDR component must land somewhere

After drafting phases, cross-reference against `draft.pdr.md`. Every component, entity, and major design element in the PDR must appear in at least one phase's Required Work. If something from the PDR has no home, either:

1. Add it to the most logical phase and flag it: "Added — not discussed in conversation but required by PDR component X."
2. Or flag it as an uncovered gap in the warnings section.

Do not silently drop PDR components.

### Phase ordering respects dependencies

Phases must be ordered so that foundations come before features that depend on them:
- Data storage before features that read/write data
- Core capture before filtering that operates on captured audio
- Single-item operations before batch operations
- Platform feasibility before platform-dependent features

If the user's stated ordering violates a dependency ("build transcription first, then audio capture"), flag it:

```markdown
## ⚠ Dependency Conflict

The discussed ordering places {Phase X} before {Phase Y}, but {Phase X}
depends on {component/capability} which is built in {Phase Y}. Recommend
reversing these phases or moving {dependency} earlier.
```

### Required Work is specific but not task-level

Each item in Required Work is a concrete deliverable or capability, not a project-management task. Write "Implement rolling in-memory buffer" not "Create Jira ticket for buffer implementation." But also don't go to task-level granularity — "Implement RollingBufferManager.appendFrames() method" is too fine. The finalizer and phase plan generator handle task breakdown.

### Acceptance criteria are phase-level gates

Each phase's acceptance criteria define what must be true before the phase is considered complete. They should be:
- Verifiable (a person can check yes/no)
- Behavioral (what the system does, not what code exists)
- Independent of later phases (Phase 1 criteria don't mention Phase 2 features)

"Code is written" is not an acceptance criterion. "User can manually save the current buffer and the saved file plays back" is.

### Milestones mark external-facing checkpoints

The Minimum Useful Release and First Full Feature Release are not just internal bookkeeping. They mark the phases where the product is usable enough to show to real users. Extract these from the conversation if discussed. If not discussed, infer them and flag your inference:

```markdown
## Minimum Useful Release

**Phase {N}** (inferred — not explicitly discussed).

Rationale: at this point the product can {list of capabilities}, which
is the minimum set for {reason}.
```

### Cross-phase requirements are real constraints

The Cross-Phase Requirements section captures concerns that span multiple phases — data that must persist across the entire app lifecycle, privacy rules that apply everywhere, performance budgets that every phase must respect. Extract these from the conversation. Do not invent generic cross-phase requirements ("code should be clean").

## What NOT to Do

- Do not decompose phases into implementation tasks. Required Work items are deliverables and capabilities, not "create file X" or "write test Y." Task breakdown is the finalizer's and phase plan generator's job.
- Do not add technology stack decisions unless they were discussed. "Use React Native" is a planning decision only if the user said it.
- Do not inflate the number of phases. If the user described 4 phases of work, don't split them into 8 for granularity. The finalizer can add scaffolding and stabilization phases if needed.
- Do not add time estimates or sprint mappings. The plan is scope-ordered, not time-estimated.
- Do not silently resolve conflicts between `draft.user.md` and `draft.pdr.md`. If the user requirements say one thing and the PDR says another, flag it in the warnings section.

## Concerns for Finalization

The final section of the document lists concerns, open questions, and planning risks that the finalization stage (which adds task-level detail, test strategy, and traceability) must account for. These are not gaps in the plan — they are things the plan surfaces that affect how phases get decomposed into tasks.

Examples:
- "Phase 0 is exploratory. The finalizer should not decompose it into rigid implementation tasks — its deliverables are reports and feasibility results, not code artifacts."
- "Phase 3 (audio quality filtering) requires empirical tuning against real-world audio. The finalizer should include explicit calibration and threshold-adjustment tasks, not just implementation tasks."
- "The plan places continuous recording (Phase 5) after the capture library (Phase 4). If the finalizer adds tests for Phase 4, those tests should not assume continuous recording exists."
- "Cross-phase performance requirements (Section: Performance Requirements) need to become concrete verification tasks in the stabilization phase, not just prose constraints."

Write 3–10 concerns. Each must name the specific phase or cross-phase section it flows from, and state what the finalizer needs to handle. Do not repeat gaps — gaps are about what the conversation didn't cover; concerns are about what the plan DOES specify that creates finalization implications.
