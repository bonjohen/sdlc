---
phase: 03
title: "Education and Getting-Started Pages"
depends_on: "Phase 02"
goal: "A developer can understand *why* the workflow is staged and *how* to start using it. Both pages are complete and linked in navigation."
source_pdr_sections: ["5"]
source_user_stories: ["US-011", "US-012", "US-013"]
status: "completed"
---

# Phase 03: Education and Getting-Started Pages

## Tasks

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 03.1 | Completed | 2026-05-21 04:16 PM | 2026-05-21 04:18 PM | Build education page at `src/pages/why.astro` using ContentLayout: heading "Why Stages?", sections on gap surfacing, traceability chains, phased execution, human-in-the-loop review. Educational tone, not marketing (PDR Section 5 Education). |
| 03.2 | Completed | 2026-05-21 04:18 PM | 2026-05-21 04:20 PM | Build getting-started page at `src/pages/getting-started.astro` using ContentLayout: heading "Getting Started", step-by-step command sequence for the normal (conversation) workflow path (PDR Section 5 Getting Started). |
| 03.3 | Completed | 2026-05-21 04:18 PM | 2026-05-21 04:20 PM | Add fast path and mixed path command sequences to the getting-started page, clearly labeled as alternatives to the normal path. |
| 03.4 | Completed | 2026-05-21 04:18 PM | 2026-05-21 04:20 PM | Add expected output descriptions at each step on the getting-started page (e.g., "After `draft-user`: a structured `draft.user.md` file appears in `sdlc/docs/`"). |
| 03.5 | Completed | 2026-05-21 04:20 PM | 2026-05-21 04:20 PM | Add both pages to Nav: Education at `navOrder: 3` with label "Why Stages?", Getting Started at `navOrder: 4`. |
| 03.6 | Completed | 2026-05-21 04:20 PM | 2026-05-21 04:21 PM | Spot-check accessibility: heading hierarchy, code block readability (sufficient contrast, monospace font), keyboard navigation (NFR-003). |
| 03.7 | Completed | 2026-05-21 04:21 PM | 2026-05-21 04:21 PM | Verify the getting-started page provides enough information for a developer to start using the SDLC pipeline without requiring additional documentation (US-013 acceptance criteria). |

## Context

### Files to Create or Modify

- `src/pages/why.astro` — Education page: "Why Stages?"
- `src/pages/getting-started.astro` — Getting Started page with command sequences
- `src/components/Nav.astro` — Verify nav entries for these pages are active (if not already in the static array from Phase 01)

### Education Page Content Structure

`src/pages/why.astro` — Heading: "Why Stages?"

Sections (educational tone, explain the reasoning):

1. **Gap Surfacing**
   - Drafts miss things. Every document stage has blind spots.
   - The `finalize` step applies a gap checklist: personas, error states, NFRs, edge cases.
   - Catching gaps in documents is cheaper than catching them in code.
   - Example: A draft user requirements doc might describe the happy path but miss what happens when an external API is down.

2. **Traceability Chains**
   - User stories get `US-NNN` IDs. NFRs get `NFR-NNN` IDs.
   - PDR sections reference user story IDs. Plan tasks reference PDR sections.
   - The chain is unbroken from user need → design decision → implementation task.
   - Why this matters: When a requirement changes, you can trace downstream to find every design element and task affected.

3. **Phased Execution**
   - The plan breaks work into ordered phases, each independently shippable.
   - Each phase ends in a working state — no phase leaves the system broken.
   - One commit per phase creates a clean history where every commit is a functional checkpoint.
   - Phases are ordered by risk and dependency: prove infrastructure first, build content later.

4. **Human-in-the-Loop**
   - AI assists at every stage but humans review at every transition.
   - `draft-*` commands extract and structure — they don't invent.
   - `gen-*` commands make engineering decisions but flag assumptions.
   - `finalize` adds what's missing but marks additions visibly.
   - The workflow is AI-assisted, not AI-autonomous.

### Getting-Started Page Content Structure

`src/pages/getting-started.astro` — Heading: "Getting Started"

**Normal (Conversation) Path:**

```
Step 1: Have a conversation about your product idea
Step 2: /sdlc draft-user
        → Produces: sdlc/docs/draft.user.md

Step 3: Have a conversation about physical design
Step 4: /sdlc draft-pdr
        → Produces: sdlc/docs/draft.pdr.md

Step 5: Have a conversation about implementation planning
Step 6: /sdlc draft-plan
        → Produces: sdlc/docs/draft.plan.md

Step 7: /sdlc finalize
        → Produces: sdlc/docs/final.user.md
                    sdlc/docs/final.pdr.md
                    sdlc/docs/final.plan.md

Step 8: /sdlc expand
        → Produces: sdlc/plan/phase00/plan.md
                    sdlc/plan/phase01/plan.md
                    ... (one per phase)

Step 9: /sdlc implement
        → Executes: next incomplete phase
        → Updates: task statuses in plan files
        → Commits: one commit per completed phase
```

**Fast Path:**

```
Step 1: Have a conversation about your product idea
Step 2: /sdlc draft-user
        → Produces: sdlc/docs/draft.user.md

Step 3: /sdlc gen-pdr
        → Produces: sdlc/docs/draft.pdr.md (generated from user requirements)

Step 4: /sdlc gen-plan
        → Produces: sdlc/docs/draft.plan.md (generated from PDR)

Steps 5-7: Same as normal path (finalize → expand → implement)
```

**Mixed Path:**

```
Any combination of conversation (draft-*) and generation (gen-*) for PDR and plan stages.
User requirements always start from conversation (no gen-user exists).

Example: conversation for requirements, generated PDR, conversation for plan
Step 1-2: draft-user (conversation)
Step 3: gen-pdr (from docs)
Step 4-5: Have a conversation about planning, then draft-plan
Steps 6-8: finalize → expand → implement
```

**Expected output at each step:**

| Step | Command | Output File | What It Contains |
|------|---------|-------------|------------------|
| `draft-user` | `/sdlc draft-user` | `sdlc/docs/draft.user.md` | Structured user stories, personas, acceptance criteria |
| `draft-pdr` / `gen-pdr` | `/sdlc draft-pdr` or `/sdlc gen-pdr` | `sdlc/docs/draft.pdr.md` | Physical design: data model, components, packages, config |
| `draft-plan` / `gen-plan` | `/sdlc draft-plan` or `/sdlc gen-plan` | `sdlc/docs/draft.plan.md` | Phased release plan with task tables |
| `finalize` | `/sdlc finalize` | `sdlc/docs/final.*.md` (3 files) | Gap-filled, cross-referenced, ID-traced final documents |
| `expand` | `/sdlc expand` | `sdlc/plan/phase{NN}/plan.md` (N files) | Self-contained phase execution plans |
| `implement` | `/sdlc implement` | Modified source code + updated plans | Working code committed per phase |

### Key Patterns and Imports

Both pages follow the same pattern established in Phases 01-02:

```astro
---
import ContentLayout from '../layouts/ContentLayout.astro';
---

<ContentLayout title="Why Stages?" description="Understanding the rationale behind staged document production in the SDLC workflow.">
  <h1>Why Stages?</h1>
  <!-- Page content -->
</ContentLayout>
```

Code examples on the getting-started page should use `<pre><code>` with appropriate styling from `global.css`. Ensure monospace font and sufficient contrast for code blocks.

### Design Notes

- **Tone distinction:** The education page (`/why/`) is explanatory — it explains rationale and reasoning. It is NOT marketing copy. No "revolutionary" or "game-changing" language. Just clear explanations of why each element of the workflow exists.
- **Getting-started sufficiency (US-013):** The acceptance criteria says "a developer can determine how they would begin using the SDLC workflow after reading the site." The getting-started page must answer: What tool do I need? (Claude Code with the /sdlc skill) What's the first command? What order do things go in? What do I get at the end?
- **Nav entries (task 03.5):** If Nav was implemented in Phase 01 with all page links pre-defined in a static array, both pages' nav entries already exist. Task 03.5 then verifies they work (pages now exist instead of 404ing). If Nav was not implemented with pre-defined links, add the entries.
- **Code blocks need styling:** The getting-started page has significant code/command content. Ensure `global.css` has styles for `<pre>` and `<code>` elements: monospace font, background color (`--color-bg-alt`), padding, appropriate line-height for readability.

### Verification

- [ ] `npm run build` exits 0
- [ ] Education page at `dist/why/index.html` exists
- [ ] Education page has sections covering: gap surfacing, traceability, phased execution, human-in-the-loop
- [ ] Education page tone is educational (no marketing language, no superlatives)
- [ ] Getting-started page at `dist/getting-started/index.html` exists
- [ ] Getting-started page shows the normal (conversation) workflow path step by step
- [ ] Getting-started page shows the fast path as an alternative
- [ ] Getting-started page shows the mixed path as an alternative
- [ ] Getting-started page shows expected output files at each step
- [ ] Navigation links to `/why/` and `/getting-started/` work from any page
- [ ] Heading hierarchy correct on both pages (single `<h1>`, sections `<h2>`)
- [ ] Code blocks use monospace font with sufficient contrast
- [ ] A developer reading only the getting-started page can answer: "What's the first command I run, and what do I get?"

## Phase Summary

- **Changes:** Created `src/pages/why.astro` (education page with gap surfacing, traceability, phased execution, human-in-the-loop sections) and `src/pages/getting-started.astro` (step-by-step guide with conversation path, fast path, mixed path, and expected output table). Nav already had entries for both pages from Phase 01.
- **Commit:** `Phase 03: Education and getting-started pages — Why Stages and Getting Started`
