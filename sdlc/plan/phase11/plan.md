# Phase 11 — Second Review Feedback

**Source:** `sdlc/plan/phase11/second-review-feedback.md`
**Goal:** Address all 5 recommendations from the second site review. Each task maps to one recommendation.
**Depends on:** Phase 10 (design refresh) completed.

## Work Queue Instructions

### State Transitions

Open  ──>  Started  ──>  Completed
              │
              └──>  Blocked  ──>  Started  ──>  Completed

- **Open**: Not yet begun.
- **Started**: Actively in progress. Record the start datetime (PST).
- **Completed**: Done and verified. Record the completion datetime (PST).
- **Blocked**: Cannot proceed; note the blocker in the description.

### Commit Protocol

1. Work through all tasks in the phase.
2. When every task reaches Completed, write the Phase Summary.
3. Stage and commit all changes for the phase. Do not push.
4. Proceed immediately to the next phase (if any).

## Phase 11 Tasks

| No    | Status | Started (PST) | Completed (PST) | Description |
|-------|--------|---------------|------------------|-------------|
| 11.1  | Open   |               |                  | Set `repoName = "sdlc"` in `src/config.ts` so portfolio "View Repository" link activates; add repo CTA button to homepage hero section |
| 11.2  | Open   |               |                  | Fix Getting Started table stray `<code>` tags — replace `{`{NN}`}` with a plain string expression in `src/pages/getting-started.astro` line 108 |
| 11.3  | Open   |               |                  | Add end-to-end mini-example: new page `src/pages/example.astro` showing a single narrative walkthrough (idea → draft.user → draft.pdr → final.plan → phase plan → code) with pipeline stage labels |
| 11.4  | Open   |               |                  | Promote Lessons page — add Lessons card to homepage CTA grid in `src/pages/index.astro` and add nav link to example page in `src/components/Nav.astro` |
| 11.5  | Open   |               |                  | Add project status badge to homepage — a one-line maturity statement below the hero subtitle in `src/pages/index.astro` |
| 11.6  | Open   |               |                  | Build (`npm run build`), verify 0 errors, spot-check built HTML for stray tags and correct repo links |
| 11.7  | Open   |               |                  | Stage all changes and commit with phase-scoped message |

<details>
<summary>Phase 11 Context</summary>

**Feedback source:** `sdlc/plan/phase11/second-review-feedback.md` — 5 numbered recommendations from external review of live site at `sdlc.johnboen.com`.

### Task 11.1 — Repo CTA

**File:** `sdlc/src/config.ts`
- Change `repoName = ""` to `repoName = "sdlc"`
- This automatically activates the conditional `{repoName && <li><a href={repoUrl}>Project repository</a></li>}` in `src/pages/portfolio.astro` (line 37)
- Also add a "View Repository" secondary button to the hero CTA row in `src/pages/index.astro` (after the existing 3 buttons)

**File:** `sdlc/src/pages/index.astro`
- Import `repoUrl` from config
- Add button: `<a href={repoUrl} class="btn btn-secondary">View Repository</a>` in the `.hero-ctas` div

### Task 11.2 — Getting Started table fix

**File:** `sdlc/src/pages/getting-started.astro` (line 108)

Current (broken):
```astro
<td><code>sdlc/plan/phase{`{NN}`}/plan.md</code></td>
```

The backtick-brace combination generates stray empty `<code>` elements in the built HTML. Fix by using a single JSX expression:
```astro
<td><code>{"sdlc/plan/phase{NN}/plan.md"}</code></td>
```

### Task 11.3 — End-to-end mini-example page

**New file:** `sdlc/src/pages/example.astro`

Content: A single narrative walkthrough. The reviewer suggested "Build a password-protected static page" but any simple, concrete example works. Structure:
1. The Idea (2-3 sentences describing what we want to build)
2. Step 1: Requirements (`/sdlc draft-user`) — show a condensed excerpt of what the output looks like
3. Step 2: Design (`/sdlc gen-pdr`) — show key design decisions
4. Step 3: Plan (`/sdlc gen-plan` + `/sdlc finalize`) — show the phase table
5. Step 4: Expand (`/sdlc expand`) — show a phase plan excerpt
6. Step 5: Implement (`/sdlc implement`) — show the result

Use the existing `.callout` and `.card` CSS classes from `global.css`. Each step should be a visually distinct section with a stage label badge. Keep it concise — the goal is to make the abstract pipeline concrete, not to reproduce full documents.

**File:** `sdlc/src/components/Nav.astro`
- Add `{ href: "/example/", label: "Example", order: 4.5 }` (between Getting Started and Portfolio) or renumber to fit

### Task 11.4 — Promote Lessons

**File:** `sdlc/src/pages/index.astro`

Add a 4th card to the `.cta-grid` at the bottom:
```astro
<a href="/lessons/" class="cta-card">
  <strong>Lessons Learned</strong>
  <span>Reusable patterns extracted from building with the pipeline</span>
</a>
```

The grid uses `grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr))` so a 4th card will auto-flow correctly (2×2 on desktop, stacked on mobile).

### Task 11.5 — Status badge

**File:** `sdlc/src/pages/index.astro`

Add a one-line status indicator below `.hero-subtitle`, above `.hero-ctas`:
```html
<p class="status-badge">Status: working documentation site · SDLC workflow under active refinement</p>
```

Style: small font, muted text, pill-shaped or inline with a subtle border. Use existing CSS vars.

</details>
