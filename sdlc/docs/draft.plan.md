# I2I — From Idea to Implementation — Phased Release Plan

## Gaps in Source Document

### Notable

- **No test strategy in the PDR.** This plan includes build verification and accessibility spot-checks per phase as default. The finalizer should define whether additional automated tests (e.g., link checking, HTML validation, Lighthouse CI) belong in individual phases or in a dedicated verification phase.

## 1. Release Strategy

The plan follows risk-first ordering:

1. **Prove the pipeline first.** Phase 0 validates that the build tool (Astro), GitHub Actions, and GitHub Pages deployment work end-to-end with placeholder content. This eliminates the highest-impact blocker before any content work begins. (PDR Concern 1)
2. **Validate the highest-risk UI element next.** Phase 1 builds the homepage with the WorkflowDiagram — the most complex visual component. If it fails responsively, the fallback to SVG happens before other pages depend on it. (PDR Concern 2, PDR Risk 1)
3. **Build content pages in dependency order.** Workflow page (Phase 2) before education and getting-started (Phase 3), because the education page explains *why* the stages exist and the getting-started page references the commands — both depend on the workflow page having established the vocabulary. Portfolio and artifacts (Phase 4) are independent of workflow explanation and can come last among content phases.
4. **Polish and harden last.** Phase 5 handles SEO, accessibility audit, custom domain readiness, and 404 page — all of which require the full site to exist first.

PDR recommended 6 phases. This plan uses the same 6 phases with identical boundaries — the PDR's ordering is already risk-first and dependency-correct.

## 2. Release Milestones

| Milestone | Phase | What the visitor can do |
|-----------|-------|------------------------|
| Minimum Useful Release | Phase 2 | Visitor sees the homepage with workflow diagram, navigates to the workflow page, reads all 8 command explanations, and understands the three workflow paths. The core value proposition — "what I2I is and how the pipeline works" — is demonstrable. |
| First Full Feature Release | Phase 5 | All pages complete: homepage, workflow, education, getting-started, portfolio, artifacts, 404. SEO metadata, accessibility compliance, custom domain readiness. The site is ready for public sharing. |

---

## Phase 0 — Project Scaffold and Deployment Pipeline

### Purpose

Prove that the build/deploy pipeline works before writing any real content. A broken pipeline blocks everything.

### Scope

Initialize the Astro project, configure GitHub Actions for GitHub Pages deployment, set up the configuration variable system (`src/config.ts`), and deploy a placeholder page to verify the full path from push to live site.

### Required Work

1. Initialize Astro project with the static output adapter
2. Create `src/config.ts` with `repoName`, `repoUrl`, `creatorName`, and `creatorGithub` variables (PDR Section 8.3)
3. Create a minimal placeholder homepage that renders the site title and one paragraph
4. Configure GitHub Actions workflow for GitHub Pages deployment (PDR Section 8.1)
5. Deploy to GitHub Pages and verify the site is accessible at the expected URL
6. Test the `base` path configuration with both empty and populated `repoName` values to catch broken link patterns (PDR Risk 3, PDR Concern 1)
7. Verify the build produces static HTML with no server-side dependencies (PDR-AC-001)

### Deliverables

- Working Astro project with `astro.config.mjs` configured for GitHub Pages
- `src/config.ts` with all configuration variables
- GitHub Actions workflow file (`.github/workflows/deploy.yml` or equivalent)
- Live placeholder page on GitHub Pages

### Acceptance Criteria

- A push to the deployment branch triggers a GitHub Actions build that produces a live site
- The deployed site is accessible at the expected GitHub Pages URL
- `npm run build` produces a directory of static HTML with no server-side dependencies
- Changing `repoName` in `src/config.ts` and rebuilding updates the GitHub link in the placeholder page

---

## Phase 1 — Homepage and Core Layout

### Purpose

Build the site shell (layouts, navigation, footer) and the homepage with the workflow diagram. After this phase, the site has one real page with the workflow-first design and a functional navigation bar.

### Scope

Implement BaseLayout, ContentLayout, Nav, Footer, and WorkflowDiagram components. Build the homepage with project title, workflow diagram, and navigation CTAs.

### Required Work

1. Implement BaseLayout with HTML shell, `<head>` meta tags, skip-to-content link (PDR Section 10.2)
2. Implement ContentLayout wrapping BaseLayout with Nav and Footer (PDR Section 10.2)
3. Implement Nav component with responsive hamburger menu — CSS-only toggle for no-JS support (PDR Section 10.3)
4. Implement Footer component with GitHub link and creator attribution (PDR Section 10.3)
5. Implement WorkflowDiagram as HTML/CSS showing the 7-stage pipeline with conversation vs. document paths (PDR Section 10.3) — test at 320px, 768px, and 1440px
6. Build the homepage at `/` with project title, tagline, WorkflowDiagram, and three CTA links (PDR Section 10.4)
7. Verify accessibility: keyboard navigation, skip link works, diagram has appropriate alt text or ARIA labels

### Deliverables

- BaseLayout, ContentLayout, Nav, Footer, WorkflowDiagram components
- Functional homepage with workflow-first design
- Responsive navigation that works without JavaScript

### Acceptance Criteria

- The homepage displays "I2I — From Idea to Implementation" and the workflow diagram
- The workflow diagram renders correctly at 320px, 768px, and 1440px viewport widths (PDR-AC-005)
- Navigation bar is visible on the homepage and collapses to hamburger on mobile
- The site is fully readable with JavaScript disabled (PDR-AC-006)
- Skip-to-content link is present and functional

---

## Phase 2 — Workflow and Command Pages

### Purpose

Build the workflow page that explains all 8 SDLC commands and the three workflow paths. This is the educational core of the site — the page most developers will spend time on.

### Scope

Define the Command content collection schema, populate it with all 8 commands, build CommandCard and PathDiagram components, and assemble the workflow page.

### Required Work

1. Define the Command content collection schema in `src/content/config.ts` (PDR Section 9.3)
2. Create content entries for all 8 commands: `draft-user`, `draft-pdr`, `draft-plan`, `gen-pdr`, `gen-plan`, `finalize`, `expand`, `implement` — sourced from the actual SDLC prompt files, not placeholder text (PDR Concern 3)
3. Implement CommandCard component that renders a single command's name, purpose, input, output, and path membership (PDR Section 10.3)
4. Implement PathDiagram component showing conversation path, fast path, and mixed path as visual flows (PDR Section 10.3)
5. Build the workflow page at `/workflow/` with stage-by-stage explanation, CommandCard components in pipeline order, and PathDiagram (PDR Section 10.4)
6. Add the workflow page to the navigation bar
7. Spot-check accessibility: heading hierarchy, color contrast on command cards, keyboard focus order

### Deliverables

- Command content collection with 8 entries
- CommandCard and PathDiagram components
- Functional workflow page explaining the full pipeline

### Acceptance Criteria

- The workflow page lists all 8 SDLC commands with their purpose, input, and output
- The three workflow paths (conversation, fast, mixed) are visually explained
- The page explains what finalize, expand, and implement each produce
- A developer can read this page and understand the full pipeline sequence
- All content is accurate relative to the current SDLC prompt files

---

## Phase 3 — Education and Getting-Started Pages

### Purpose

Build the "Why Stages?" education page and the getting-started page. After this phase, a developer can both understand *why* the workflow is staged and *how* to start using it.

### Scope

Create two content pages: education (rationale for staged production) and getting-started (command sequences for all three paths).

### Required Work

1. Build the education page at `/why/` explaining rationale for staged document production: gap surfacing, traceability chains, phased execution, human-in-the-loop review (PDR Section 10.4)
2. Build the getting-started page at `/getting-started/` with step-by-step command sequence for the normal (conversation) workflow (PDR Section 10.4)
3. Add alternate sequences for fast path and mixed path on the getting-started page
4. Show expected output at each step on the getting-started page
5. Add both pages to the navigation bar
6. Ensure the getting-started page provides enough information for a developer to adopt the workflow without additional documentation (US-013)
7. Spot-check accessibility: heading hierarchy, readable code blocks, sufficient contrast

### Deliverables

- Education page at `/why/`
- Getting-started page at `/getting-started/`
- Both pages linked in navigation

### Acceptance Criteria

- The education page explains why the workflow uses staged document production rather than jumping straight to code
- The getting-started page shows the full command sequence for the normal workflow path
- The getting-started page shows the fast path and mixed path as alternatives
- A developer reading only the getting-started page can determine how to begin using the SDLC workflow

---

## Phase 4 — Portfolio and Artifacts Pages

### Purpose

Build the portfolio/case-study page and the artifacts page with example prompts and generated documents. After this phase, all content pages exist and the site serves all four audience personas.

### Scope

Create the portfolio page, define the Artifact content collection, populate it with real examples, build the ArtifactExample component, and assemble the artifacts page.

### Required Work

1. Build the portfolio page at `/portfolio/` with case-study content: what the project demonstrates, the creator's role, skills evidenced, links to GitHub profile and repository (PDR Section 10.4)
2. Review portfolio page content for tone: credible, technical, practical — no exaggerated claims (FR-025, PDR Concern 4)
3. Define the Artifact content collection schema in `src/content/config.ts` (PDR Section 9.2)
4. Create artifact content entries with real SDLC examples: at least one prompt excerpt and at least one generated document excerpt (US-018)
5. Implement ArtifactExample component that renders an artifact with title, type label, and content (PDR Section 10.3)
6. Build the artifacts page at `/artifacts/` with ArtifactExample components (PDR Section 10.4)
7. Add both pages to the navigation bar
8. Spot-check accessibility: heading hierarchy, code block readability, link text

### Deliverables

- Portfolio page at `/portfolio/`
- Artifact content collection with real SDLC examples
- ArtifactExample component
- Artifacts page at `/artifacts/`

### Acceptance Criteria

- The portfolio page explains the project's significance and the creator's role without requiring the visitor to open GitHub
- The portfolio page links to `github.com/bonjohen`
- The artifacts page displays at least one prompt example and one generated document example
- Artifact examples are labeled by type (prompt vs. generated) and source command
- The marketing tone is credible and technical, not exaggerated

---

## Phase 5 — Polish, Accessibility, SEO, and Custom Domain Readiness

### Purpose

Harden the site for public release. Add the 404 page, SEO metadata, Open Graph tags, sitemap, comprehensive accessibility audit, and verify custom domain readiness.

### Scope

Final polish pass across all pages. This phase does not add new content pages — it makes the existing site production-ready.

### Required Work

1. Build the custom 404 page at `src/pages/404.astro` with navigation back to homepage (PDR Section 10.4)
2. Add `<title>`, `<meta description>`, and Open Graph tags to all pages via BaseLayout props (NFR-006, PDR Section 10.2)
3. Configure Astro sitemap integration for auto-generated `sitemap.xml` (NFR-006)
4. Add a Content Security Policy `<meta>` tag to BaseLayout (PDR Section 16)
5. Run Lighthouse accessibility audit on all pages — target score >= 90 (PDR-AC-007)
6. Fix any accessibility failures: contrast, heading order, alt text, keyboard focus, ARIA labels
7. Test responsive rendering on all pages at 320px, 768px, 1440px, and 2560px (NFR-005)
8. Verify custom domain readiness: add a CNAME file, confirm it does not break the base-path configuration (NFR-010, PDR Concern 5)
9. Verify broken internal links are caught at build time (PDR Section 14)
10. Final content review pass: verify all command descriptions match current SDLC prompt files (PDR Concern 3)

### Deliverables

- Custom 404 page
- SEO metadata on all pages
- Auto-generated sitemap
- Content Security Policy
- Accessibility audit results with all critical issues resolved
- CNAME configuration tested

### Acceptance Criteria

- All pages have unique `<title>`, `<meta description>`, and Open Graph tags
- `sitemap.xml` is generated and includes all pages
- Lighthouse accessibility score >= 90 on all pages
- All pages render correctly from 320px to 2560px viewport width
- The 404 page displays site navigation and a link to the homepage
- Adding a CNAME file and DNS configuration is sufficient to serve the site under `johnboen.com` (PDR-AC-008)
- All pages are readable with JavaScript disabled
- No broken internal links exist in the built output

---

## Cross-Phase Requirements

### Privacy Requirements

- No phase shall introduce cookies, analytics, tracking pixels, or visitor data collection. The initial release collects zero visitor data. (final.user.md Section 5, PDR Section 11)
- If any phase adds external resources (fonts, scripts), prefer self-hosted assets. If CDN-hosted, use Subresource Integrity hashes. (PDR Section 16)

### Performance Requirements

- Every phase that produces visible pages must verify that those pages load with Largest Contentful Paint < 2.5s on a simulated 10 Mbps connection. (NFR-001)
- No phase shall introduce JavaScript that blocks core content rendering. Astro's zero-JS default must be preserved unless a specific interactive feature requires an island. (NFR-002)

### Accessibility Requirements

- Every phase that produces visible UI must include a spot-check for keyboard navigation, heading hierarchy, and color contrast. (NFR-003, NFR-004, PDR Concern 6)
- Phase 5 performs the comprehensive audit; earlier phases perform incremental checks.

### Content Accuracy

- Command descriptions and artifact examples must be sourced from the actual SDLC prompt files, not invented or paraphrased from memory. (PDR Concern 3)
- If the prompt files change after content is written, a content update pass is needed before release.

---

## Minimum Useful Release

**Phase 2** (after Workflow and Command Pages).

At this point the visitor can:
- See the homepage with the project name, workflow diagram, and navigation
- Navigate to the workflow page and read explanations of all 8 SDLC commands
- Understand the conversation path, fast path, and mixed path
- See the site deployed live on GitHub Pages

This is enough to demonstrate the core value proposition: "I2I explains a structured SDLC workflow from idea to implementation."

## First Full Feature Release

**Phase 5** (after Polish, Accessibility, SEO, and Custom Domain Readiness).

At this point the site has:
- All 7 pages (homepage, workflow, education, getting-started, portfolio, artifacts, 404)
- Full SEO metadata and sitemap
- Accessibility compliance (Lighthouse >= 90)
- Custom domain readiness
- Real SDLC artifact examples
- Portfolio/case-study content

The site is ready for public sharing with hiring managers, developers, and collaborators.

---

## Concerns for Finalization

1. **Phase 0 has no user-facing content to verify visually.** The finalizer should structure Phase 0 tasks around build/deploy verification rather than UI checks. Acceptance criteria are pipeline-level (build succeeds, deploy works, config propagates), not page-level.

2. **Phase 1's WorkflowDiagram has a defined fallback (SVG).** The finalizer should include a decision point: if the HTML/CSS diagram fails responsive testing at 320px, the task switches to SVG implementation. This is not a blocked state — it's a planned alternative within the same phase.

3. **Phase 2 and Phase 4 depend on content collections populated from real SDLC artifacts.** The finalizer should include specific tasks for sourcing content from `skill/*.md` files, not generic "write content" tasks. The content is not creative writing — it's structured extraction from existing prompt files.

4. **Phase 4's portfolio page requires editorial judgment (PDR Concern 4).** The finalizer should include a content review task separate from the build task. The reviewer must check that claims are credible and specific, not boilerplate.

5. **Phase 5 bundles multiple concerns (SEO, accessibility, 404, CNAME, content review).** The finalizer should order tasks so that the accessibility audit runs after all other Phase 5 changes are complete — otherwise the audit results are stale before the phase ends.

6. **Cross-phase accessibility requirements (PDR Concern 6) create per-phase verification tasks.** The finalizer should add a spot-check accessibility task to every phase that produces visible UI (Phases 1–4), not just Phase 5. The spot-check is lightweight (keyboard nav, heading order, contrast) while Phase 5 does the comprehensive Lighthouse audit.
