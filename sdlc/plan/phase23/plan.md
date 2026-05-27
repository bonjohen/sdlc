---
phase: 23
title: "Expand Restructuring"
depends_on: "Phase 21 (implement prompt must have format detection ready to consume the new format)"
goal: "skill/expand.md restructures final.plan.md into a phase-level dashboard after generating phase plans. The new dashboard format includes format: dashboard frontmatter and a Phase Status table."
source_pdr_sections: ["4.3", "2.2"]
source_user_stories: ["US-022", "US-023", "US-024"]
status: "open"
---

# Phase 23: Expand Restructuring

## Tasks

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 23.1 | Completed | 2026-05-27 01:47 PM | 2026-05-27 01:50 PM | Add the Master Plan Restructuring section to `skill/expand.md`: after generating all phase plans, rewrite `final.plan.md`. Git commit before expand provides the safety net. |
| 23.2 | Completed | 2026-05-27 01:50 PM | 2026-05-27 01:50 PM | Define the Phase Status table format: columns Phase, Title, Plan (relative link), Status (`not_started`), Started, Completed, Commit. One row per phase. |
| 23.3 | Completed | 2026-05-27 01:50 PM | 2026-05-27 01:50 PM | Define the frontmatter addition: add `format: "dashboard"` to existing YAML frontmatter. |
| 23.4 | Completed | 2026-05-27 01:50 PM | 2026-05-27 01:50 PM | Define what is preserved from the pre-expand plan: frontmatter (plus new field), title, source references, work queue instructions, technology stack, coverage checklist. |
| 23.5 | Completed | 2026-05-27 01:50 PM | 2026-05-27 01:50 PM | Define what is removed: individual task rows (now in phase plans only). Phase goal and dependency lines remain as context for the status table. |
| 23.6 | Completed | 2026-05-27 01:50 PM | 2026-05-27 01:50 PM | Add the `## Phase Summaries` section definition: empty on expand, filled by implement as phases complete. Each summary includes changes description and commit reference. |
| 23.7 | Completed | 2026-05-27 01:50 PM | 2026-05-27 01:50 PM | Add verification step: after restructuring, re-read the master plan and confirm the Phase Status table has one row per phase and no individual task rows remain. |

## Context

### Files to Create or Modify

- `skill/expand.md` — **Modify.** Add master plan restructuring step after existing phase plan generation logic. Current file is 166 lines.

### Post-Expand Master Plan Format

**Before expand (current format):**

```markdown
## Phase 03: Build the Service Layer

**Goal:** Working service with CRUD operations.
**Depends on:** Phase 02.

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 03.1 | Open | | | Create service module |
| 03.2 | Open | | | Implement CRUD operations |
| 03.3 | Open | | | Write unit tests |

### Phase 03 Summary
_To be filled after completion._
```

**After expand (new dashboard format):**

```markdown
---
document: "Implementation Plan"
version: "1.0"
status: "final"
format: "dashboard"
...
---

# {Project Name} — Implementation Plan

{Preserved: source references, work queue instructions, technology stack}

## Phase Status

| Phase | Title | Plan | Status | Started | Completed | Commit |
|-------|-------|------|--------|---------|-----------|--------|
| 00 | Project Scaffold | [plan](../plan/phase00/plan.md) | not_started | | | |
| 01 | Data Model | [plan](../plan/phase01/plan.md) | not_started | | | |
| 02 | Core Components | [plan](../plan/phase02/plan.md) | not_started | | | |
| 03 | Service Layer | [plan](../plan/phase03/plan.md) | not_started | | | |

{Preserved: coverage checklist}

## Phase Summaries

_Summaries are appended here as phases complete._
```

### Column Definitions

| Column | Values | Set by |
|--------|--------|--------|
| Phase | Zero-padded number (e.g., `00`, `01`) | Expand (once) |
| Title | Phase title from master plan | Expand (once) |
| Plan | Relative link: `[plan](../plan/phase{NN}/plan.md)` | Expand (once) |
| Status | `not_started` / `in_progress` / `complete` / `blocked` | Implement (at phase start and completion) |
| Started | PST timestamp | Implement (when first task starts) |
| Completed | PST timestamp | Implement (when phase commits) |
| Commit | Short hash (7 chars) | Implement (after commit) |

### Phase Summary Format (filled by implement)

```markdown
### Phase 03 Summary

- **Changes:** Created `app/services/crud.py`, added 12 unit tests in `tests/test_crud.py`.
- **Commit:** `a1b2c3d` — Phase 03: Service layer with CRUD operations
```

### Restructuring Algorithm

Add this to `expand.md` after the phase plan generation section:

```
After generating all phase plans:

1. Re-read final.plan.md in full.
2. Parse all phase sections (## Phase NN: Title).
3. For each phase, extract: number, title.
4. Construct the Phase Status table with one row per phase.
5. Build the new file content:
   a. Preserve frontmatter — add `format: "dashboard"` field
   b. Preserve title and source references
   c. Preserve Work Queue Instructions section
   d. Preserve Technology Stack section
   e. Replace all phase sections (## Phase NN + task tables + summaries)
      with the single Phase Status table
   f. Preserve Coverage Checklist if present
   g. Add ## Phase Summaries section (empty)
6. Write the restructured content to final.plan.md.
7. Re-read final.plan.md and verify:
   - Phase Status table has exactly one row per phase
   - No individual task rows remain (no | NN.N | patterns)
   - frontmatter contains format: "dashboard"
```

### Design Notes

- **This step is destructive to `final.plan.md`.** The task table content is moved to phase plans, not duplicated. If expand fails mid-restructuring, `git checkout sdlc/docs/final.plan.md` restores the original. The master plan was committed by the finalize step, so there's always a clean copy in Git.
- **Relative links use `../plan/` paths** because `final.plan.md` is at `sdlc/docs/final.plan.md` and phase plans are at `sdlc/plan/phase{NN}/plan.md`. The relative path from `docs/` to `plan/` is `../plan/`.
- **The Coverage Checklist is preserved** — it maps PDR components to phase tasks, which is still valuable for tracking even in dashboard format.
- **Work Queue Instructions are preserved** because they define state transitions and commit protocol that the implement prompt references.
- **Phase goals and dependency lines are removed** from the master plan — they now live only in the phase plans. The dashboard is intentionally minimal: status table + summaries.

### Verification

- [ ] After expand, `final.plan.md` frontmatter contains `format: "dashboard"`
- [ ] After expand, `final.plan.md` contains a Phase Status table with one row per phase
- [ ] After expand, `final.plan.md` contains no individual task rows (no `| NN.N |` patterns)
- [ ] After expand, each phase plan at `sdlc/plan/phase{NN}/plan.md` contains the full task table
- [ ] The Phase Status table includes relative links to phase plan files
- [ ] Work queue instructions, technology stack, and coverage checklist are preserved
- [ ] A `## Phase Summaries` section exists at the bottom (empty)
- [ ] Source references and title are preserved

## Phase Summary

- **Changes:** Modified `skill/expand.md` (166 → 237 lines): added Master Plan Restructuring section with restructuring algorithm, Phase Status table format definition, frontmatter dashboard field, preserved/removed content rules, Phase Summaries section, column definitions, and verification step.
- **Commit:** `Phase 23: Expand Restructuring — dashboard format, Phase Status table, Phase Summaries`
