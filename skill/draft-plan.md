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

## Standards

Follow the universal rules and document standards defined in `sdlc/prompts/_standards.md`. Use its gap analysis framework and phase table standard. Key for this prompt: you are EXTRACTING phasing from conversation, not generating from scratch.

## Rules

### Phases come from the conversation, not from you

Extract the phasing strategy discussed. May organize, split, merge, name — but do NOT invent phases or reorder against stated priorities.

### Assess the conversation

Evaluate using the gap framework from `_standards.md`. Prompt-specific checklist:

**Critical:**
- [ ] What gets built first and why (priority or risk ordering)
- [ ] At least rough phase boundaries (what's early vs. late)
- [ ] What "done" looks like for the first milestone

**Notable:**
- [ ] How each PDR component maps to a phase
- [ ] Which phases are required for minimum useful release
- [ ] Highest-risk items and when they're addressed
- [ ] Cross-phase concerns (data persistence, privacy, performance)

Write gaps to a **Gaps Identified During Extraction** section. Address every **Concerns for Release Planning** item from `draft.pdr.md`.

### Every PDR component must land somewhere

After drafting phases, cross-reference against `draft.pdr.md`. Every component, entity, and major design element in the PDR must appear in at least one phase's Required Work. If something from the PDR has no home, either:

1. Add it to the most logical phase and flag it: "Added — not discussed in conversation but required by PDR component X."
2. Or flag it as an uncovered gap in the warnings section.

Do not silently drop PDR components.

### Phase ordering respects dependencies

Foundations before features. If stated ordering violates a dependency, flag it with a `## ⚠ Dependency Conflict` section explaining the issue.

### Required Work is specific but not task-level

Concrete deliverables, not Jira tickets and not method-level tasks. 5-15 items per phase.

### Acceptance criteria are phase-level gates

Verifiable, behavioral, independent of later phases. "Code is written" fails. "User can save buffer and file plays back" passes.

### Milestones and cross-phase requirements

Extract Minimum Useful Release and First Full Feature Release from conversation (or infer and flag). Extract cross-phase constraints (persistence, privacy, performance) — don't invent generic ones.

## What NOT to Do

- Do not decompose phases into tasks — that's the finalizer's job.
- Do not add tech decisions unless discussed.
- Do not inflate phases — 4 discussed phases ≠ 8 padded ones.
- Do not silently resolve conflicts between user doc and PDR — flag them.

## Concerns for Finalization

Write 3–10 concerns for the finalizer. Each names a phase/section and states what it must handle. Not gaps — things the plan specifies that create finalization implications.

## After Completion

Stage files produced by this command. Commit: `sdlc {cmd}: {brief description}`. Do not push.
