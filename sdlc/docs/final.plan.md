---
document: "Implementation Plan"
version: "1.0"
status: "final"
source: "sdlc/docs/draft.plan.md"
pdr: "sdlc/docs/final.pdr.md"
user_requirements: "sdlc/docs/final.user.md"
finalized_date: "2026-05-21"
total_phases: 6
---

# I2I — From Idea to Implementation — Implementation Plan

**Source PDR:** `sdlc/docs/final.pdr.md`
**Source User Requirements:** `sdlc/docs/final.user.md`

## Work Queue Instructions

### State Transitions

```
Open  ──>  Started  ──>  Completed
              │
              └──>  Blocked  ──>  Started  ──>  Completed
```

- **Open**: Not yet begun.
- **Started**: Actively in progress. Record the start datetime (PST).
- **Completed**: Done and verified. Record the completion datetime (PST).
- **Blocked**: Cannot proceed; note the blocker in the description.

### Commit Protocol

1. Work through all tasks in a phase.
2. When every task reaches Completed, write the Phase Summary.
3. Stage and commit all changes for the phase. Do not push.
4. Proceed immediately to the next phase.

## Technology Stack

| Concern | Choice | Justification |
|---------|--------|--------------|
| Static site generator | Astro 5.x | Zero-JS default, first-class markdown + content collections, GitHub Pages deployment support (PDR Section 4.5 framework choice) |
| Sitemap generation | @astrojs/sitemap | NFR-006 requires auto-generated `sitemap.xml` |
| Content management | Astro Content Collections (Zod) | Type-safe markdown frontmatter, build-time schema validation (PDR Section 2.1) |
| Styling | CSS custom properties (no framework) | NFR-002 requires no-JS; PDR UI principles specify clean/understated design |
| Deployment | GitHub Actions + GitHub Pages | NFR-008 (auto-deploy on push), FR-002 (GitHub Pages publishing) |
| Image optimization | sharp (Astro default) | Build-time optimization for any images added later |

## Phase 00: Project Scaffold and Deployment Pipeline

**Goal:** The Astro project builds, deploys to GitHub Pages, and the configuration variable system works. No real content yet — just proof that the pipeline is operational.
**Depends on:** None (first phase).
**PDR sections:** 1.2 (Dependencies), 1.3 (Configuration), 3 (Package Layout)
**User stories:** US-020 (auto-deploy on push)

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 00.1 | Completed | 2026-05-21 03:45 PM | 2026-05-21 03:48 PM | Initialize Astro project with static output adapter and TypeScript config. Install `astro` and `sharp`. Create `astro.config.mjs` with `site` and `base` settings (PDR Section 1.3). |
| 00.2 | Completed | 2026-05-21 03:48 PM | 2026-05-21 03:49 PM | Create `src/config.ts` with `repoName`, `repoUrl`, `creatorName`, `creatorGithub`, `siteTitle`, and `siteDescription` variables (PDR Section 1.3). |
| 00.3 | Completed | 2026-05-21 03:49 PM | 2026-05-21 03:49 PM | Create minimal placeholder homepage at `src/pages/index.astro` that renders the site title, one paragraph, and a link generated from `src/config.ts` to verify config propagation. |
| 00.4 | Completed | 2026-05-21 03:50 PM | 2026-05-21 03:50 PM | Create GitHub Actions workflow at `.github/workflows/deploy.yml` for building Astro and deploying to GitHub Pages on push to main (PDR Section 1.2, NFR-008). |
| 00.5 | Completed | 2026-05-21 03:50 PM | 2026-05-21 03:51 PM | Test `base` path configuration: verify build succeeds with `base: "/"` and with `base: "/test-repo"`. Verify internal links and asset paths resolve correctly in both cases (PDR Risk 3). |
| 00.6 | Completed | 2026-05-21 03:51 PM | 2026-05-21 03:52 PM | Verify `npm run build` produces a directory of static HTML with no server-side dependencies (PDR-AC-001). Verify changing `repoName` and rebuilding updates the GitHub link on the placeholder page (PDR-AC-003). |
| 00.7 | Blocked | 2026-05-21 03:52 PM | | Deploy to GitHub Pages and verify the site is accessible at the expected URL (PDR-AC-002). [BLOCKED: No GitHub remote repository configured yet; deployment requires push to a remote repo with GitHub Pages enabled] |

### Phase 00 Summary

- **Changes:** Created `package.json`, `astro.config.mjs`, `tsconfig.json`, `src/config.ts`, `src/pages/index.astro`, `.github/workflows/deploy.yml`. Verified static build produces only HTML (no server code). Verified `base` path works with both `/` and `/test-repo`. Verified `repoName` config propagation to built output.
- **Blocked tasks:** 00.7 — no GitHub remote repository configured yet; deployment verification deferred.
- **Commit:** `Phase 00: Project scaffold — Astro init, config system, GitHub Actions workflow`

---

## Phase 01: Homepage and Core Layout

**Goal:** The site has a functional homepage with the workflow-first design, responsive navigation, and all shared layout components. The WorkflowDiagram renders correctly across viewport sizes.
**Depends on:** Phase 00.
**PDR sections:** 4.1 (BaseLayout), 4.2 (ContentLayout), 4.3 (Nav), 4.4 (Footer), 4.5 (WorkflowDiagram), 5 (Homepage), 6 (CSP), 12 (UI Principles)
**User stories:** US-001, US-002, US-003, US-004, US-022

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 01.1 | Completed | 2026-05-21 03:55 PM | 2026-05-21 03:56 PM | Create `src/styles/global.css` with CSS reset, typography (body text >= 16px), color custom properties with minimum 4.5:1 contrast ratios (NFR-004), and responsive foundation (PDR Section 12). |
| 01.2 | Completed | 2026-05-21 03:56 PM | 2026-05-21 03:57 PM | Implement `src/layouts/BaseLayout.astro`: HTML shell with `<title>`, `<meta description>`, Open Graph tags, CSP `<meta>` tag (PDR Section 6), skip-to-content link, and `global.css` import (PDR Section 4.1). |
| 01.3 | Completed | 2026-05-21 03:57 PM | 2026-05-21 03:58 PM | Implement `src/components/Nav.astro`: responsive navigation bar with page links sorted by `navOrder`, `aria-current="page"` on active link, CSS-only hamburger toggle below 768px (PDR Section 4.3, NFR-002). |
| 01.4 | Completed | 2026-05-21 03:58 PM | 2026-05-21 03:59 PM | Implement `src/components/Footer.astro`: GitHub profile link, repo link (when `repoName` set), creator name, `role="contentinfo"` (PDR Section 4.4). |
| 01.5 | Completed | 2026-05-21 03:59 PM | 2026-05-21 03:59 PM | Implement `src/layouts/ContentLayout.astro`: wraps BaseLayout with Nav, `<main id="main-content">`, and Footer (PDR Section 4.2). |
| 01.6 | Completed | 2026-05-21 04:00 PM | 2026-05-21 04:02 PM | Implement `src/components/WorkflowDiagram.astro`: HTML/CSS 7-stage pipeline diagram with conversation and document path branches, `role="img"` and `aria-label`, responsive layout (PDR Section 4.5). |
| 01.7 | Completed | 2026-05-21 04:02 PM | 2026-05-21 04:03 PM | Build homepage at `src/pages/index.astro` using ContentLayout: project title, tagline, WorkflowDiagram, three CTA links to `/workflow/`, `/artifacts/`, `/portfolio/` (PDR Section 5 Homepage). |
| 01.8 | Completed | 2026-05-21 04:03 PM | 2026-05-21 04:04 PM | Test WorkflowDiagram at 320px, 768px, and 1440px viewport widths. If HTML/CSS fails at 320px, switch to static SVG fallback (PDR Risk 1, PDR-AC-005). |
| 01.9 | Completed | 2026-05-21 04:04 PM | 2026-05-21 04:05 PM | Spot-check accessibility: verify skip-to-content link works, keyboard can reach all nav links and CTAs, WorkflowDiagram has appropriate ARIA, heading hierarchy is correct (NFR-003). |
| 01.10 | Completed | 2026-05-21 04:05 PM | 2026-05-21 04:05 PM | Verify all homepage content is readable with JavaScript disabled (NFR-002, PDR-AC-006). |

### Phase 01 Summary

- **Changes:** Created `src/styles/global.css`, `src/layouts/BaseLayout.astro`, `src/layouts/ContentLayout.astro`, `src/components/Nav.astro`, `src/components/Footer.astro`, `src/components/WorkflowDiagram.astro`. Rebuilt `src/pages/index.astro` using ContentLayout with workflow diagram and 3 CTA cards.
- **Commit:** `Phase 01: Homepage and core layout — BaseLayout, Nav, Footer, WorkflowDiagram, ContentLayout`

---

## Phase 02: Workflow and Command Pages

**Goal:** The workflow page explains all 8 SDLC commands and shows the three workflow paths. Content is sourced from actual SDLC prompt files, not placeholder text. This completes the Minimum Useful Release.
**Depends on:** Phase 01.
**PDR sections:** 2.1 (Command collection schema), 2.3 (Command seed data), 4.6 (CommandCard), 4.7 (PathDiagram), 5 (Workflow page)
**User stories:** US-005, US-006, US-007, US-008, US-009, US-010, US-021

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 02.1 | Completed | 2026-05-21 04:07 PM | 2026-05-21 04:08 PM | Create `src/content/config.ts` with Command content collection schema: `name`, `purpose`, `input`, `output`, `path` (enum), `sortOrder` (PDR Section 2.1). |
| 02.2 | Completed | 2026-05-21 04:08 PM | 2026-05-21 04:10 PM | Create 8 command content entries in `src/content/commands/` sourced from `skill/*.md` and `skill/SKILL.md` — one `.md` file per command with accurate purpose, input, and output descriptions (PDR Section 2.3). |
| 02.3 | Completed | 2026-05-21 04:10 PM | 2026-05-21 04:11 PM | Implement `src/components/CommandCard.astro`: card displaying command name, purpose, input, output, and path badge (PDR Section 4.6). |
| 02.4 | Completed | 2026-05-21 04:11 PM | 2026-05-21 04:12 PM | Implement `src/components/PathDiagram.astro`: visual flow showing conversation path, fast path, and mixed path with their respective command sequences (PDR Section 4.7). |
| 02.5 | Completed | 2026-05-21 04:12 PM | 2026-05-21 04:14 PM | Build workflow page at `src/pages/workflow.astro` using ContentLayout: heading "The SDLC Pipeline", stage-by-stage explanation, CommandCard components in pipeline order, PathDiagram, sections on what finalize/expand/implement produce (PDR Section 5 Workflow). |
| 02.6 | Completed | 2026-05-21 04:14 PM | 2026-05-21 04:14 PM | Add workflow page to Nav component page list with `navOrder: 2` and label "Workflow". |
| 02.7 | Completed | 2026-05-21 04:14 PM | 2026-05-21 04:15 PM | Spot-check accessibility: verify heading hierarchy (`h1` > `h2` > `h3`), color contrast on command cards, keyboard focus order through cards (NFR-003). |
| 02.8 | Completed | 2026-05-21 04:15 PM | 2026-05-21 04:15 PM | Verify all 8 command descriptions are accurate by comparing each content entry against the corresponding `skill/*.md` file header and behavior. |

### Phase 02 Summary

- **Changes:** Created `src/content/config.ts`, 8 command entries in `src/content/commands/`, `src/components/CommandCard.astro`, `src/components/PathDiagram.astro`, `src/pages/workflow.astro`.
- **Commit:** `Phase 02: Workflow and command pages — content collections, CommandCard, PathDiagram, workflow page`

---

## Phase 03: Education and Getting-Started Pages

**Goal:** A developer can understand *why* the workflow is staged and *how* to start using it. Both pages are complete and linked in navigation.
**Depends on:** Phase 02.
**PDR sections:** 5 (Education page, Getting Started page)
**User stories:** US-011, US-012, US-013

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 03.1 | Completed | 2026-05-21 04:16 PM | 2026-05-21 04:18 PM | Build education page at `src/pages/why.astro` using ContentLayout: heading "Why Stages?", sections on gap surfacing, traceability chains, phased execution, human-in-the-loop review. Educational tone, not marketing (PDR Section 5 Education). |
| 03.2 | Completed | 2026-05-21 04:18 PM | 2026-05-21 04:20 PM | Build getting-started page at `src/pages/getting-started.astro` using ContentLayout: heading "Getting Started", step-by-step command sequence for the normal (conversation) workflow path (PDR Section 5 Getting Started). |
| 03.3 | Completed | 2026-05-21 04:18 PM | 2026-05-21 04:20 PM | Add fast path and mixed path command sequences to the getting-started page, clearly labeled as alternatives to the normal path. |
| 03.4 | Completed | 2026-05-21 04:18 PM | 2026-05-21 04:20 PM | Add expected output descriptions at each step on the getting-started page (e.g., "After `draft-user`: a structured `draft.user.md` file appears in `sdlc/docs/`"). |
| 03.5 | Completed | 2026-05-21 04:20 PM | 2026-05-21 04:20 PM | Add both pages to Nav: Education at `navOrder: 3` with label "Why Stages?", Getting Started at `navOrder: 4`. |
| 03.6 | Completed | 2026-05-21 04:20 PM | 2026-05-21 04:21 PM | Spot-check accessibility: heading hierarchy, code block readability (sufficient contrast, monospace font), keyboard navigation (NFR-003). |
| 03.7 | Completed | 2026-05-21 04:21 PM | 2026-05-21 04:21 PM | Verify the getting-started page provides enough information for a developer to start using the SDLC pipeline without requiring additional documentation (US-013 acceptance criteria). |

### Phase 03 Summary

- **Changes:** Created `src/pages/why.astro` and `src/pages/getting-started.astro`. Both pages use ContentLayout and are linked in navigation.
- **Commit:** `Phase 03: Education and getting-started pages — Why Stages and Getting Started`

---

## Phase 04: Portfolio and Artifacts Pages

**Goal:** All content pages exist. The portfolio page demonstrates the creator's skills with credible, specific claims. The artifacts page shows real SDLC prompt and document examples.
**Depends on:** Phase 03 (for full navigation context). Phases 02 and 03 are not strict technical dependencies — portfolio and artifacts don't import from education/getting-started — but navigation ordering requires all prior pages to be in place.
**PDR sections:** 2.1 (Artifact collection schema), 2.3 (Artifact seed data), 4.8 (ArtifactExample), 5 (Portfolio page, Artifacts page)
**User stories:** US-014, US-015, US-016, US-017, US-018, US-019, US-023

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 04.1 | Open | | | Build portfolio page at `src/pages/portfolio.astro` using ContentLayout: heading "About This Project", what the project demonstrates (AI workflow design, SDLC methodology, documentation, planning), creator's role, links to `github.com/bonjohen` and repo (when named) (PDR Section 5 Portfolio). |
| 04.2 | Open | | | Review portfolio page content for tone: claims must be credible, technical, and specific. No boilerplate, no exaggerated claims. Verify human-in-the-loop framing (Constraint: human-in-the-loop framing). |
| 04.3 | Open | | | Add Artifact content collection schema to `src/content/config.ts`: `title`, `type` (enum: prompt/generated), `command` (optional), `excerpt` (boolean), `sortOrder` (PDR Section 2.1). |
| 04.4 | Open | | | Create artifact content entries in `src/content/artifacts/` from actual SDLC files: at least one prompt excerpt (from `skill/*.md`) and at least one generated document excerpt (from `sdlc/docs/*.md`) (PDR Section 2.3). |
| 04.5 | Open | | | Implement `src/components/ArtifactExample.astro`: styled block with title, type badge ("Prompt" or "Generated Document"), optional command label, rendered markdown content, excerpt note when applicable (PDR Section 4.8). |
| 04.6 | Open | | | Build artifacts page at `src/pages/artifacts.astro` using ContentLayout: heading "Example Artifacts", ArtifactExample components for each artifact entry, labeled by type and command (PDR Section 5 Artifacts). |
| 04.7 | Open | | | Add both pages to Nav: Portfolio at `navOrder: 5` with label "Portfolio", Artifacts at `navOrder: 6` with label "Artifacts". |
| 04.8 | Open | | | Spot-check accessibility: heading hierarchy, code block readability, artifact type badges have sufficient contrast, all links have descriptive text (NFR-003). |

### Phase 04 Summary

_To be filled after completion._

- **Changes:** TBD
- **Commit:** TBD

---

## Phase 05: Polish, Accessibility, SEO, and Custom Domain Readiness

**Goal:** The site is production-ready for public sharing. All SEO metadata in place, accessibility audit passes, custom domain config verified, and content accuracy confirmed. This completes the First Full Feature Release.
**Depends on:** Phase 04 (all pages must exist before comprehensive audit and polish).
**PDR sections:** 1.2 (@astrojs/sitemap), 5 (404 page), 6 (Security — CSP verification), 7 (Observability — link validation), 8 (Test Strategy — Lighthouse, HTML validation), 11 (NFR Design Responses — all), 14 (PDR-AC-001 through PDR-AC-008)
**User stories:** NFR-001, NFR-003, NFR-004, NFR-005, NFR-006, NFR-010

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 05.1 | Open | | | Build custom 404 page at `src/pages/404.astro` using ContentLayout: "Page not found" message, link back to homepage, same navigation and footer as other pages (PDR Section 5, 404 page). |
| 05.2 | Open | | | Install `@astrojs/sitemap` and add to `astro.config.mjs` integrations. Verify `sitemap.xml` is generated in build output and includes all pages (NFR-006, PDR Section 1.2). |
| 05.3 | Open | | | Audit all pages for unique `<title>`, `<meta description>`, and Open Graph tags (`og:title`, `og:description`, `og:type`, `og:url`). Fix any pages with missing or duplicate metadata (NFR-006). |
| 05.4 | Open | | | Configure Astro build to treat broken internal links as errors. Verify no broken links exist in built output (PDR Section 7, 9 Error Handling). |
| 05.5 | Open | | | Test responsive rendering on all 7 pages at 320px, 768px, 1440px, and 2560px viewport widths. Fix any layout issues (NFR-005). |
| 05.6 | Open | | | Verify all pages are readable with JavaScript disabled. Test CSS-only hamburger nav, WorkflowDiagram, PathDiagram (NFR-002, PDR-AC-006). |
| 05.7 | Open | | | Run Lighthouse accessibility audit on all 7 pages. Target score >= 90 on each (NFR-003, NFR-004, PDR-AC-007). |
| 05.8 | Open | | | Fix any accessibility failures identified by Lighthouse: contrast issues, heading order, alt text, keyboard focus, ARIA labels. |
| 05.9 | Open | | | Verify custom domain readiness: add `CNAME` file to `public/`, confirm build succeeds, confirm base-path configuration is compatible with root-domain hosting (NFR-010, PDR-AC-008, PDR Risk 3). |
| 05.10 | Open | | | Final content review: compare all command descriptions in `src/content/commands/` against current `skill/*.md` files. Compare artifact examples against their source files. Fix any drift. |

<!-- Added during finalization: the draft plan's Phase 5 lists 10 items of required work but does not distinguish between tasks that create new assets (404 page, sitemap) and verification/audit tasks. This task table sequences asset creation (05.1–05.4) before audits (05.5–05.8) so audit results reflect the final state, not a partial state. The draft plan's concern #5 specifically called for this ordering. -->

### Phase 05 Summary

_To be filled after completion._

- **Changes:** TBD
- **Commit:** TBD

---

## Cross-Phase Requirements

These apply to every phase and must be verified before marking a phase complete:

- **No visitor data collection.** No cookies, analytics, tracking pixels, or forms. (final.user.md Section 6, PDR Section 13)
- **No external CDN dependencies without SRI.** Prefer self-hosted assets. If CDN resources are used, include `integrity` and `crossorigin` attributes. (PDR Section 6)
- **Zero-JS default preserved.** Do not add JavaScript that blocks core content rendering. Astro's static HTML output must remain the default. (NFR-002)
- **Performance spot-check.** Visible pages should load with LCP < 2.5s on simulated 10 Mbps. (NFR-001)
- **Accessibility spot-check.** Each phase producing visible UI must verify keyboard navigation, heading hierarchy, and color contrast. Phase 05 performs the comprehensive Lighthouse audit. (NFR-003, NFR-004)
- **Content from source files.** Command descriptions and artifact examples must be sourced from actual `skill/*.md` and `sdlc/docs/*.md` files, not paraphrased from memory. (PDR Section 2.3)

## Release Milestones

| Milestone | Phase | What the Visitor Can Do |
|-----------|-------|------------------------|
| Minimum Useful Release | Phase 02 | See the homepage with workflow diagram, navigate to the workflow page, read all 8 command explanations, understand the three workflow paths. The core value proposition is demonstrable. |
| First Full Feature Release | Phase 05 | All 7 pages complete. SEO metadata, accessibility compliance (Lighthouse >= 90), custom domain readiness. The site is ready for public sharing. |

## Coverage Checklist

_Every component and asset in the PDR must appear in at least one phase task._

| PDR Section | Component/Asset | Phase | Task |
|-------------|----------------|-------|------|
| 1.2 | Astro project initialization | 00 | 00.1 |
| 1.2 | @astrojs/sitemap integration | 05 | 05.2 |
| 1.3 | `src/config.ts` | 00 | 00.2 |
| 2.1 | Command collection schema | 02 | 02.1 |
| 2.1 | Artifact collection schema | 04 | 04.3 |
| 2.3 | Command seed data (8 entries) | 02 | 02.2 |
| 2.3 | Artifact seed data (>= 2 entries) | 04 | 04.4 |
| 3 | Package layout (Astro init) | 00 | 00.1 |
| 3 | `src/styles/global.css` | 01 | 01.1 |
| 3 | `.github/workflows/deploy.yml` | 00 | 00.4 |
| 4.1 | BaseLayout | 01 | 01.2 |
| 4.2 | ContentLayout | 01 | 01.5 |
| 4.3 | Nav | 01 | 01.3 |
| 4.4 | Footer | 01 | 01.4 |
| 4.5 | WorkflowDiagram | 01 | 01.6 |
| 4.6 | CommandCard | 02 | 02.3 |
| 4.7 | PathDiagram | 02 | 02.4 |
| 4.8 | ArtifactExample | 04 | 04.5 |
| 5 | Homepage `/` | 01 | 01.7 |
| 5 | Workflow `/workflow/` | 02 | 02.5 |
| 5 | Education `/why/` | 03 | 03.1 |
| 5 | Getting Started `/getting-started/` | 03 | 03.2 |
| 5 | Portfolio `/portfolio/` | 04 | 04.1 |
| 5 | Artifacts `/artifacts/` | 04 | 04.6 |
| 5 | 404 `/404/` | 05 | 05.1 |
| 6 | CSP `<meta>` tag | 01 | 01.2 |
| 7 | Build-time link validation | 05 | 05.4 |
| 8 | Lighthouse accessibility audit | 05 | 05.7 |
| 11 | NFR-006 SEO metadata | 05 | 05.3 |
| 11 | NFR-010 CNAME / custom domain | 05 | 05.9 |
| 14 | PDR-AC-001 (static build) | 00 | 00.6 |
| 14 | PDR-AC-002 (deploy to Pages) | 00 | 00.7 |
| 14 | PDR-AC-003 (repoName propagation) | 00 | 00.6 |
| 14 | PDR-AC-005 (diagram responsive) | 01 | 01.8 |
| 14 | PDR-AC-006 (no-JS readable) | 01 | 01.10 |
| 14 | PDR-AC-007 (Lighthouse >= 90) | 05 | 05.7 |
| 14 | PDR-AC-008 (custom domain ready) | 05 | 05.9 |
