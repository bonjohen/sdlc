# Phase Plan Expander

Follow the phase table standard and document structures defined in `sdlc/prompts/_standards.md`.

You are generating standalone phase execution plans from finalized SDLC documents. Each phase plan must contain everything an implementer needs to execute that phase without re-reading the full PDR or user requirements.

**Output:** One file per phase at `sdlc/plan/phase{NN}/plan.md`

## Inputs

Read all three finalized documents in full before generating any output:

| Document | Path | What you extract from it |
|----------|------|--------------------------|
| Final Plan | `sdlc/docs/final.plan.md` | Phase structure, task tables, goals, dependencies, PDR section references, user story references |
| Final PDR | `sdlc/docs/final.pdr.md` | Component interfaces, data model (schema), package layout, platform adapters, configuration, test strategy |
| Final User Requirements | `sdlc/docs/final.user.md` | User stories referenced by each phase, acceptance criteria, NFRs |

If any of these files do not exist, stop: "Cannot expand phases. Missing: `{file}`. Run `sdlc/prompts/finalize.md` first."

Also read the existing codebase to understand what already exists. If prior phases have already been implemented, the context sections for later phases should reference the actual code, not just the PDR's design.

## Scaffold Generation

Run `python scripts/phase-template.py` to generate skeleton files for all phases. This creates the frontmatter, task tables, and section headings automatically. Then fill in the **Context** section for each phase — that is where the AI value-add is.

If the script is unavailable, generate files manually using the format below.

## Output Format

For each phase numbered `NN` (zero-padded: `00`, `01`, ... `99`) in `final.plan.md`, generate:

```
sdlc/plan/phase{NN}/plan.md
```

Each file follows this exact structure:

````markdown
---
phase: {NN}
title: "{Phase title from final.plan.md}"
depends_on: "{Dependency from final.plan.md, or 'none'}"
goal: "{Goal statement from final.plan.md}"
source_pdr_sections: ["{PDR section numbers this phase implements}"]
source_user_stories: ["{User story IDs this phase satisfies}"]
status: "open"
---

# Phase {NN}: {Phase Title}

## Tasks

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| {NN}.1 | Open | | | {One-line task description — imperative verb, specific file paths where known} |
| {NN}.2 | Open | | | {Next task} |
| ... | ... | ... | ... | ... |

## Context

{This is the critical section. Everything an implementer needs to complete
this phase WITHOUT reading the full PDR or user doc.}

### Files to Create or Modify

- `path/to/file.ext` — {what to do and why}
- `path/to/other.ext` — {what to modify}

### Data Model

{Only include tables/columns/types relevant to THIS phase.
Copy the exact schema from the PDR — do not paraphrase.}

```sql
-- Only if this phase touches the schema
CREATE TABLE example (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
```

### Key Patterns and Imports

{Actual import paths, class signatures, and patterns the implementer
should follow. Pull from the PDR or from existing code.}

```
class ComponentName:
    method(arg: Type) -> ReturnType
```

### Design Notes

{Non-obvious decisions from the PDR that affect this phase:
- WHY a particular approach was chosen
- Edge cases or gotchas
- Integration points with other phases
- Constraints (rate limits, file size limits, API quirks)}

### Verification

{How to verify this phase is complete. Every item must be runnable or checkable:}

- [ ] `{test command}` passes
- [ ] `{lint command}` clean
- [ ] {Behavioral check — e.g., "app launches and captures audio into buffer"}

## Phase Summary

_To be filled after completion._

- **Changes:** TBD
- **Commit:** TBD
````

## Rules

### 1. Self-contained context

Each phase plan must contain enough context to execute without re-reading the PDR or user stories. Copy relevant schema, component interfaces, patterns, and rationale into the Context section. An implementer holding only the phase plan and the codebase should be able to do the work.

This means the Context section will often be the longest part of the file. A 200-line context section for a complex phase is fine. A 3-line context section is almost certainly insufficient.

### 2. Task tables match the master plan

Copy task tables exactly from `final.plan.md`. Do not adjust tasks. Context section provides detail.

### 3. Concrete, not abstract

File paths, actual SQL, interface signatures, data shapes. If a task says "Implement X," the Context shows the exact interface, location, and configuration from the PDR.

### 4. One task per line, one file per phase

Do not merge or split tasks or phases from the master plan.

### 5. Frontmatter traces lineage

Use exact section numbers and story IDs from `final.plan.md` phase headers.

### 6. Verification is testable

Commands to run or conditions to check. Not "code is clean" — "`ruff check app/` exits 0". For research phases: deliverable existence checks.

### 7. Context references existing code for later phases

Reference actual files, patterns, imports from earlier implemented phases — not just PDR abstractions.

### 8. No implementation

Write what to implement, where, and how to verify — not the actual code.

## Processing Order

Generate sequentially from Phase 00. Later phases may reference earlier plans but don't assume earlier phases are implemented.

## What NOT to Do

- Do not modify final docs (read-only inputs).
- Do not change tasks from master plan — note gaps in Design Notes instead.
- Do not write implementation code.

## Master Plan Restructuring

After generating all phase plans, restructure `final.plan.md` into a phase-level dashboard. The master plan was committed by the finalize step, so `git checkout sdlc/docs/final.plan.md` restores the original if this step fails.

### Restructuring Algorithm

1. Re-read `final.plan.md` in full.
2. Parse all phase sections (`## Phase NN: Title`).
3. For each phase, extract: phase number (zero-padded) and title.
4. Build the restructured file:

   **a. Frontmatter:** Preserve existing YAML frontmatter. Add `format: "dashboard"` field.

   **b. Preserve these sections verbatim:**
   - Title and source references (e.g., `**Source PDR:**`, `**Source User Requirements:**`)
   - `## Work Queue Instructions` (state transitions, commit protocol)
   - `## Technology Stack`
   - `## Coverage Checklist` (if present)

   **c. Replace all phase sections** (each `## Phase NN` block including task tables and summary placeholders) with a single Phase Status table:

   ```markdown
   ## Phase Status

   | Phase | Title | Plan | Status | Started | Completed | Commit |
   |-------|-------|------|--------|---------|-----------|--------|
   | 00 | {title} | [plan](../plan/phase00/plan.md) | not_started | | | |
   | 01 | {title} | [plan](../plan/phase01/plan.md) | not_started | | | |
   ```

   One row per phase. All statuses start as `not_started`. The `Plan` column uses relative links from `sdlc/docs/` to `sdlc/plan/`.

   **d. Add Phase Summaries section** at the bottom (before Coverage Checklist if present):

   ```markdown
   ## Phase Summaries

   _Summaries are appended here as phases complete during `/sdlc implement`._
   ```

   **e. Remove:** Individual task rows (these now live only in phase plans). Phase goal and dependency lines. Phase summary placeholders.

### Phase Status Table Columns

| Column | Values | Set by |
|--------|--------|--------|
| Phase | Zero-padded number (e.g., `00`, `01`) | Expand (once) |
| Title | Phase title from master plan | Expand (once) |
| Plan | Relative link: `[plan](../plan/phase{NN}/plan.md)` | Expand (once) |
| Status | `not_started` / `in_progress` / `complete` / `blocked` | Implement |
| Started | PST timestamp | Implement (when first task starts) |
| Completed | PST timestamp | Implement (when phase commits) |
| Commit | Short hash (7 chars) | Implement (after commit) |

### Phase Summary Format (filled by implement)

```markdown
### Phase 03 Summary

- **Changes:** Created `app/services/crud.py`, added 12 unit tests in `tests/test_crud.py`.
- **Commit:** `a1b2c3d` — Phase 03: Service layer with CRUD operations
```

### Verification

After restructuring, re-read `final.plan.md` and confirm:
- Frontmatter contains `format: "dashboard"`
- Phase Status table has exactly one row per phase
- No individual task rows remain (no `| NN.N |` patterns outside of Coverage Checklist)
- `## Phase Summaries` section exists
- Work Queue Instructions, Technology Stack, and Coverage Checklist are preserved

## After Completion

Stage files produced by this command. Commit: `sdlc {cmd}: {brief description}`. Do not push.
