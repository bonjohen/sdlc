---
phase: 10
title: "Design Refresh — Visual Identity and Marketing Clarity"
depends_on: "Phase 04 (all content pages exist)"
goal: "The site has a distinctive visual identity (dark slate/accent color theme), a compelling hero section, clickable workflow stage cards, a Without/With comparison table, and sharper marketing copy. The site feels like a polished technical product, not a README rendered as pages."
source_pdr_sections: ["4.5", "5", "12"]
source_user_stories: ["US-001", "US-002", "US-003", "US-004"]
source_document: "sdlc/plan/phase10/first-review-feedback.md"
status: "completed"
---

# Phase 10: Design Refresh — Visual Identity and Marketing Clarity

## Tasks

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 10.1 | Completed | 2026-05-21 04:50 PM | 2026-05-21 04:53 PM | Redesign `src/styles/global.css`: replace plain white background with deep slate (`#1a1f2e`) / off-white (`#f8f9fa`) palette, add electric blue accent color (`#3b82f6`), update typography to modern sans-serif stack, increase spacing scale, add card/shadow/border utility classes. Preserve existing 4.5:1 contrast ratios (NFR-004). |
| 10.2 | Completed | 2026-05-21 04:53 PM | 2026-05-21 04:56 PM | Redesign hero section in `src/pages/index.astro`: large bold title "I2I — From Idea to Implementation", subtitle "A prompt-driven SDLC workflow for turning rough software ideas into buildable plans", three CTA buttons (Explore Workflow → /workflow/, View Artifacts → /artifacts/, Case Study → /portfolio/). Replace generic layout with prominent visual treatment. |
| 10.3 | Completed | 2026-05-21 04:53 PM | 2026-05-21 04:56 PM | Add "Without I2I / With I2I" comparison section to `src/pages/index.astro` below the hero: two-column table contrasting vague prompts vs. requirements-first workflow, lost context vs. persistent artifacts, one giant request vs. phased execution, hard-to-review vs. traceable criteria, project drift vs. stage gates. Style as a visually distinct card/panel. |
| 10.4 | Completed | 2026-05-21 04:53 PM | 2026-05-21 04:56 PM | Add problem/solution messaging block to `src/pages/index.astro` between hero and workflow diagram: "Most AI coding failures start before code is written" problem statement, "I2I creates durable SDLC artifacts before implementation begins" solution statement. Styled as a callout panel with accent color. |
| 10.5 | Completed | 2026-05-21 04:56 PM | 2026-05-21 04:59 PM | Redesign `src/components/WorkflowDiagram.astro` as clickable stage cards: 7 cards (Idea, Requirements, PDR, Plan, Finalize, Expand, Implement) each with a one-line description. Cards link to relevant sections of /workflow/. Add hover states, accent-color borders, and subtle shadows. Preserve `role="img"` and `aria-label` for accessibility. |
| 10.6 | Completed | 2026-05-21 04:53 PM | 2026-05-21 04:56 PM | Add "Human-in-the-loop" trust section to `src/pages/index.astro` after comparison: "I2I is not an attempt to remove human judgment from software development. It is designed to preserve it." Explain clear review points between stages. |
| 10.7 | Completed | 2026-05-21 04:59 PM | 2026-05-21 05:02 PM | Redesign `src/components/CommandCard.astro`: update to match new visual identity — dark card background, accent-color top border, increased padding, subtle shadow on hover. Ensure keyboard focus styles are visible against new palette. |
| 10.8 | Completed | 2026-05-21 04:59 PM | 2026-05-21 05:02 PM | Update `src/components/Nav.astro` to match new palette: dark background nav bar, light text, accent-color active indicator. Verify hamburger toggle still works at mobile breakpoints. |
| 10.9 | Completed | 2026-05-21 04:59 PM | 2026-05-21 05:02 PM | Update `src/components/Footer.astro` to match new palette: dark background, subtle top border, light text with accent-color links. |
| 10.10 | Completed | 2026-05-21 05:02 PM | 2026-05-21 05:04 PM | Update `src/pages/portfolio.astro`: restructure as "What This Project Demonstrates" with bullet list (AI-assisted SDLC, prompt pipeline engineering, requirements-to-plan traceability, human-in-the-loop workflow, developer automation, practical AI coding agents). Move personal bio lower. Add links to GitHub profile and future johnboen.com. |
| 10.11 | Completed | 2026-05-21 05:04 PM | 2026-05-21 05:07 PM | Update `src/pages/artifacts.astro` and `src/components/ArtifactExample.astro`: style artifact previews as code-document cards with filename headers (e.g., `draft.user.md`), one-line descriptions, and styled borders matching the new palette. |
| 10.12 | Completed | 2026-05-21 05:07 PM | 2026-05-21 05:09 PM | Full visual QA pass: verify all 7 pages render correctly with new palette at 320px, 768px, 1440px viewpoints. Verify no-JS readability preserved (NFR-002). Verify contrast ratios meet 4.5:1 minimum on all text (NFR-004). Fix any issues found. |

## Context

### Source Document

This phase implements the design feedback from `sdlc/docs/first-review-feedback.md`, which identified the site as visually bland and recommended:
- A workflow-first landing page (not documentation-first)
- Stronger visual identity (dark/accent palette, cards, shadows, spacing)
- Clickable workflow stage cards as the main visual object
- "Without I2I / With I2I" comparison section (identified as highest-value addition)
- Sharper marketing copy with problem/solution framing
- Human-in-the-loop trust messaging

### Design Decisions

- **Color palette:** Deep slate (#1a1f2e) background with electric blue (#3b82f6) accent. This matches the "engineering portfolio" recommendation and provides strong contrast for accessibility.
- **No new pages:** The feedback suggests /how-it-works/, /case-study/, /roadmap/, /about/ but these overlap significantly with existing pages (/workflow/, /portfolio/). This phase enhances existing pages rather than creating redundant routes.
- **No JavaScript added:** All visual enhancements use CSS only. Clickable cards use `<a>` tags, not JS event handlers. Preserves NFR-002.
- **Incremental approach:** Tasks 10.1–10.4 establish the new visual foundation. Tasks 10.5–10.9 update components. Tasks 10.10–10.11 update content pages. Task 10.12 is the verification pass.

### Files to Modify

- `src/styles/global.css` — complete palette and spacing overhaul
- `src/pages/index.astro` — hero redesign, comparison table, problem/solution, trust section
- `src/components/WorkflowDiagram.astro` — clickable stage cards
- `src/components/CommandCard.astro` — new card styling
- `src/components/Nav.astro` — dark palette
- `src/components/Footer.astro` — dark palette
- `src/pages/portfolio.astro` — content restructure
- `src/pages/artifacts.astro` — card styling
- `src/components/ArtifactExample.astro` — card styling

### Existing Patterns to Follow

- Layout: All pages use `ContentLayout.astro` which wraps `BaseLayout.astro` + Nav + Footer
- Styling: CSS custom properties in `global.css`, component-scoped `<style>` blocks
- Accessibility: `role`, `aria-label`, heading hierarchy, keyboard focus, 4.5:1 contrast
- No-JS: All interactions CSS-only (hamburger toggle uses checkbox hack)

### Cross-Phase Requirements Still Apply

- No visitor data collection (no analytics, tracking, cookies)
- No external CDN dependencies without SRI
- Zero-JS default preserved
- Performance: LCP < 2.5s on 10 Mbps
- Content from source files where applicable

## Phase Summary

- **Changes:** Redesigned `global.css` with dark slate palette (#0f172a bg, #60a5fa accent), new typography scale, card/shadow utilities. Rebuilt homepage with hero section, problem/solution callout, comparison table, trust section, and CTA cards. Redesigned WorkflowDiagram as 7 clickable stage cards. Updated CommandCard, Nav, Footer, PathDiagram, and ArtifactExample to match dark palette. Restructured portfolio page with skill bullet list. All 8 pages build, zero JS, correct heading hierarchy, WCAG contrast ratios preserved.
- **Commit:** `Phase 10: Design refresh — visual identity and marketing clarity`
