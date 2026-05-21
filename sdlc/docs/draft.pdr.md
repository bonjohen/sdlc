# I2I — From Idea to Implementation — Product Design Review

## Gaps in Source Document

### Notable

- **No error states described.** The user requirements cover the happy path only. The error handling section below (Section 14) is this PDR's inference. For a static site the error surface is small (404 pages, broken anchor links, failed asset loads), but the requirements do not specify what the visitor should see in those cases.

## 1. Product Summary

I2I is a multi-page static website that explains, teaches, and markets a prompt-driven SDLC workflow. It is built with a static site generator, deployed to GitHub Pages, and serves educational, marketing, and portfolio purposes simultaneously. It has no backend, no database, no user accounts, and no interactive features in its initial release.

## 2. Product Intent

The site exists to make the SDLC pipeline understandable to four audiences: first-time visitors who need a quick orientation, developers who want to learn or adopt the workflow, technical reviewers evaluating the creator's skills, and potential collaborators assessing fit. The site is the public face of the SDLC prompt pipeline project.

## 3. Planning Scope

The initial release covers:
- A complete multi-page static site with homepage, workflow page, education page, getting-started page, portfolio/case-study page, and artifact examples page
- GitHub Pages deployment via GitHub Actions
- Custom domain readiness (`johnboen.com`)
- Visual workflow diagram
- Content sourced from both hand-authored pages and project markdown files

Not in scope: interactive demos, backend services, analytics, user accounts, i18n.

## 4. Primary Requirements (from final.user.md)

| Category | Key Stories | Summary |
|----------|-----------|---------|
| First Impression | US-001 through US-004 | Homepage shows project name, workflow diagram, navigation paths; self-contained without GitHub |
| Workflow Education | US-005 through US-011 | Dedicated workflow page explaining all 8 commands, 3 paths, and rationale for staged production |
| Getting Started | US-012, US-013 | Usage page with command sequence; enough info to adopt the workflow |
| Portfolio | US-014 through US-017 | Case-study page with creator role, GitHub links, project significance |
| Artifacts | US-018, US-019 | Example prompts and generated artifacts on deeper pages |
| Content Management | US-020, US-021 | Automated deploy on push; dual content sourcing (manual + markdown-derived) |
| Navigation/IA | US-022, US-023 | Workflow-first homepage; creator info reachable but secondary |

## 5. Operating Modes

The site operates in a single mode: a public static website served over HTTPS. The four "modes" described in the user requirements (website, portfolio, educational, marketing) are not runtime modes — they are content perspectives addressed by different pages and sections within the same static site.

## 6. Interaction Model

Visitors interact with the site through standard web browsing:
- Navigate via a persistent top-level navigation bar
- Read content on individual pages
- Follow internal links between pages
- Follow external links to GitHub and the creator's other materials
- View diagrams and code examples inline

There are no forms, no login, no state, no cookies (unless analytics are added later). Every page is a static HTML document.

## 7. Site Architecture and Data Flow

```
Content Sources                    Build Pipeline                    Output
─────────────────                  ──────────────                    ──────
Hand-authored pages (.astro)  ─┐
                                ├──> Astro build ──> Static HTML/CSS/JS ──> GitHub Pages
Markdown content files (.md)  ─┘         │
                                         │
                              astro.config.mjs
                              (site URL, base path,
                               repo name variable)
```

Content flows in one direction: authored source files are processed at build time into static output. There is no runtime data flow. The build reads all content, applies layouts and components, and emits a directory of HTML, CSS, and JS files that GitHub Pages serves as-is.

## 8. Static Site Framework

### 8.1 Framework Choice: Astro

Astro is selected as the static site generator for the following reasons:

| Requirement | How Astro satisfies it |
|-------------|----------------------|
| FR-001: Multi-page static site | Astro's default output mode is static multi-page HTML |
| US-021: Markdown-sourced content | Astro has first-class markdown and MDX support with content collections |
| FR-002: GitHub Pages deployment | Astro has an official GitHub Pages deployment guide and adapter |
| NFR-001: LCP < 2.5s | Astro ships zero JS by default; pages are static HTML with optional islands |
| NFR-002: Works without JS | Static HTML output is fully readable without JavaScript |
| FR-026: Future interactivity | Astro's island architecture allows adding interactive components (React, Svelte, etc.) to specific pages without rebuilding the site |
| NFR-009: Adding a page requires <= 2 files | New `.astro` or `.md` file + optional nav config update |

<!-- Structurally required: no explicit user requirement names Astro, but the combination of static output, markdown content support, GitHub Pages deployment, zero-JS default, and future interactivity support makes Astro the strongest fit among current static site generators. Alternatives considered: Hugo (fast but limited component model), Eleventy (flexible but less integrated markdown pipeline), Next.js (overkill for static-only, ships more JS by default). -->

### 8.2 Content Collections

Astro content collections organize markdown-sourced content:

| Collection | Source Directory | Purpose |
|------------|-----------------|---------|
| `artifacts` | `src/content/artifacts/` | SDLC prompt excerpts and generated document examples (US-018, US-019) |
| `commands` | `src/content/commands/` | Per-command descriptions for `draft-user`, `gen-pdr`, etc. (US-006) |

Hand-authored pages live in `src/pages/` as `.astro` files and are not part of content collections.

### 8.3 Configuration Variables

| Variable | Location | Purpose | Default |
|----------|----------|---------|---------|
| `site` | `astro.config.mjs` | Full site URL for canonical links and sitemap | `https://bonjohen.github.io` |
| `base` | `astro.config.mjs` | Base path for GitHub Pages project site | `/{repo-name}` (placeholder until repo name is chosen) |
| `repoName` | `src/config.ts` | Repository name used in GitHub links throughout the site | `""` (empty string; templates render `github.com/bonjohen` without repo path until set) |
| `repoUrl` | `src/config.ts` | Computed full repository URL | `https://github.com/bonjohen/${repoName}` |
| `creatorName` | `src/config.ts` | Creator display name | `"John Boen"` |
| `creatorGithub` | `src/config.ts` | GitHub profile URL | `https://github.com/bonjohen` |

This addresses Concern 9 (repository link placement) from the draft user requirements. All GitHub links are generated from `src/config.ts` so the repo name can be filled in once and propagate everywhere.

## 9. Data Model

This is a static site with no database. The "data model" is the content structure:

### 9.1 Page

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| title | string | Yes | Page `<title>` and `<h1>` |
| description | string | Yes | `<meta name="description">` content (NFR-006) |
| layout | string | Yes | Which layout template to use |
| slug | string | Yes | URL path segment |
| navOrder | number | No | Position in navigation bar; omit to exclude from nav |
| navLabel | string | No | Display text in nav; defaults to `title` if omitted |

### 9.2 Artifact (content collection)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| title | string | Yes | Display name of the artifact |
| type | enum | Yes | `"prompt"` or `"generated"` |
| command | string | No | Which SDLC command produced this (e.g., `"draft-user"`, `"finalize"`) |
| excerpt | boolean | No | `true` if this is a truncated excerpt rather than a full artifact |
| sortOrder | number | Yes | Display order on the artifacts page |

### 9.3 Command (content collection)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| name | string | Yes | Command name (e.g., `draft-user`, `gen-pdr`) |
| purpose | string | Yes | One-line description |
| input | string | Yes | What the command reads |
| output | string | Yes | What the command produces |
| path | enum | Yes | `"conversation"`, `"document"`, or `"both"` — which workflow path(s) this command belongs to |
| sortOrder | number | Yes | Display order matching pipeline sequence |

## 10. Component Design

### 10.1 Architectural Layers

```
Pages (.astro)  ──>  Layouts  ──>  Components  ──>  Content Collections
      │                 │               │                    │
      │                 │               │                    └── Markdown files + frontmatter schemas
      │                 │               └── Reusable UI pieces (Nav, Footer, Diagram, CommandCard, etc.)
      │                 └── Page shells (BaseLayout, ContentLayout)
      └── Route-level files (index, workflow, education, getting-started, portfolio, artifacts)
```

Dependencies flow left-to-right: pages import layouts, layouts import components, components read content collections. Nothing flows backward.

### 10.2 Layouts

**BaseLayout**
- **Purpose:** HTML shell shared by all pages. Renders `<html>`, `<head>` (with title, meta description, Open Graph tags, canonical URL), and `<body>` with skip-to-content link.
- **Serves:** NFR-003 (accessibility — skip link, semantic HTML), NFR-006 (SEO — meta tags, canonical)
- **Dependencies:** None (leaf layout)
- **Used by:** All pages via ContentLayout or directly

**ContentLayout**
- **Purpose:** Wraps BaseLayout with the site navigation bar, main content area, and footer.
- **Serves:** US-003 (navigation paths), US-022 (workflow-first nav), US-023 (creator info reachable)
- **Dependencies:** BaseLayout, Nav component, Footer component
- **Used by:** All content pages

### 10.3 Components

**Nav**
- **Purpose:** Persistent top-level navigation bar. Renders links to all top-level pages in order. Highlights the current page. Collapses to a hamburger menu on mobile viewports.
- **Serves:** US-003, US-022, US-023, NFR-005 (responsiveness)
- **Dependencies:** Page frontmatter (navOrder, navLabel) for link generation; `src/config.ts` for GitHub link
- **Behavior:** Reads page list at build time, sorts by navOrder, renders as `<nav>` with `<a>` elements. Mobile hamburger uses CSS-only toggle (NFR-002: works without JS) or progressive enhancement.

**Footer**
- **Purpose:** Site footer with GitHub link, creator attribution, and optional copyright.
- **Serves:** US-015 (GitHub link), US-017 (creator portfolio links)
- **Dependencies:** `src/config.ts` for URLs

**WorkflowDiagram**
- **Purpose:** Visual representation of the SDLC pipeline from Idea to Implementation. Renders the full stage sequence with arrows showing flow direction.
- **Serves:** US-002 (visual workflow on homepage), FR-008
- **Dependencies:** None (self-contained)
- **Behavior:** Renders as an inline SVG or CSS-styled HTML diagram. Must be readable without JavaScript (NFR-002) and accessible via alt text or ARIA labels (NFR-003). Initial implementation uses semantic HTML + CSS; can be replaced with a richer SVG later without changing the component interface.
- **Key decision:** HTML/CSS over an image file so the diagram is searchable, accessible, and editable without external tools. Addresses Concern 4 (workflow diagram) from the draft user requirements.

**CommandCard**
- **Purpose:** Displays a single SDLC command with its name, purpose, input, output, and workflow path membership.
- **Serves:** US-006 (explain each command)
- **Dependencies:** Command content collection entries
- **Behavior:** Renders as a styled card element. Used on the workflow page in pipeline order.

**PathDiagram**
- **Purpose:** Shows the three workflow paths (conversation, fast, mixed) as visual flows.
- **Serves:** US-007 (explain the three paths)
- **Dependencies:** None (self-contained)
- **Behavior:** Renders as CSS-styled HTML showing which commands appear in each path and what connects them.

**ArtifactExample**
- **Purpose:** Renders a prompt or generated document example with title, type label, and content in a styled code/prose block.
- **Serves:** US-018 (view example artifacts), US-019 (accessible from deeper pages)
- **Dependencies:** Artifact content collection entries

### 10.4 Pages

| Page | Route | Primary Stories | Purpose |
|------|-------|----------------|---------|
| Homepage | `/` | US-001, US-002, US-003, US-004, US-022 | Project name, workflow diagram, navigation CTAs. Workflow-first. |
| Workflow | `/workflow/` | US-005, US-006, US-007, US-008, US-009, US-010 | All 8 commands explained. Three paths shown. Stage-by-stage detail. |
| Education | `/why/` | US-011 | Why the workflow is staged. Rationale for gap surfacing, traceability, phased execution. |
| Getting Started | `/getting-started/` | US-012, US-013 | Command sequence for normal workflow. Fast path and mixed path. Enough to adopt. |
| Portfolio | `/portfolio/` | US-014, US-015, US-016, US-017, US-023 | Case study. Creator's role. Skills demonstrated. GitHub links. |
| Artifacts | `/artifacts/` | US-018, US-019 | Example prompts and generated documents. Deeper detail. |
| 404 | `/404/` | *(none — inferred)* | Custom 404 page with navigation back to homepage. |

<!-- Structurally required: the 404 page has no user story, but GitHub Pages serves a 404 for any unmatched route. A custom 404 that matches the site's navigation prevents visitors from hitting a dead end. -->

## 11. Privacy and Permissions

- The site collects no visitor data in its initial release. No cookies, no analytics, no forms, no tracking pixels.
- All content is public. No authentication or authorization is needed.
- If analytics are added later (as allowed by the user requirements), they should use a privacy-respecting service, be disclosed in a visible notice, and not require cookie consent banners (prefer cookieless analytics like Plausible or Fathom).

## 12. User Interface Requirements

### 12.1 Design Principles

- **Clean and readable.** Generous whitespace, readable font sizes (16px+ body text), high contrast. The site is primarily a reading experience.
- **Credible, not flashy.** The marketing tone is technical and practical (FR-025, US-025). The visual design should match: professional, understated, no gratuitous animations or decorative elements.
- **Workflow-first hierarchy.** The visual weight of the homepage leads with the workflow diagram and explanation, not with the creator's name or photo (US-022).

### 12.2 Pages (minimal screen descriptions)

**Homepage**
- Project title: "I2I — From Idea to Implementation"
- Subtitle or tagline: one sentence explaining the project
- Workflow diagram (WorkflowDiagram component): the central visual
- Three CTA sections: "Learn the Workflow" → /workflow/, "See Examples" → /artifacts/, "About the Creator" → /portfolio/
- Footer with GitHub link

**Workflow Page**
- Heading: "The SDLC Pipeline"
- Stage-by-stage explanation with CommandCard components for each of the 8 commands
- PathDiagram showing conversation path, fast path, mixed path
- Section explaining what finalize, expand, and implement each produce

**Education Page**
- Heading: "Why Stages?"
- Sections explaining the rationale: gap surfacing, traceability chains, phased execution, human-in-the-loop review
- Tone: educational, not marketing

**Getting Started Page**
- Heading: "Getting Started"
- Step-by-step command sequence for the normal (conversation) workflow
- Alternate sequences for fast path and mixed path
- Expected output at each step

**Portfolio Page**
- Heading: "About This Project" or "Case Study"
- What the project demonstrates (AI workflow design, SDLC methodology, documentation, software planning)
- The creator's role and approach
- Links to GitHub profile (`bonjohen`) and repository (once named)
- Optional: links to creator's broader portfolio or `johnboen.com`

**Artifacts Page**
- Heading: "Example Artifacts"
- List of ArtifactExample components showing prompt excerpts and generated document excerpts
- Each artifact labeled by type (prompt vs. generated) and command

**404 Page**
- "Page not found" message
- Link back to homepage
- Same layout and navigation as other pages

## 13. State Model

Not applicable. The site is stateless. Every page load is independent. There are no sessions, no authentication states, and no client-side state machines. Navigation is standard anchor-link HTTP requests (or prefetching via Astro's optional view transitions, but no state is carried).

## 14. Error Handling

The error surface for a static site is small:

| Error Scenario | Design Response |
|----------------|----------------|
| Visitor requests a URL that does not exist | Custom 404 page with site navigation and link to homepage |
| Visitor's browser does not support modern CSS (grid, flexbox) | Graceful degradation: content remains readable in single-column layout. No critical information is hidden behind CSS features. |
| JavaScript is disabled | All core content is static HTML. No functionality is lost. (NFR-002) |
| GitHub Pages is down | No mitigation possible. Availability is bounded by GitHub Pages SLA. (NFR-007) |
| Broken internal link (build-time) | Astro's build will warn on broken links if configured. The build pipeline should treat broken internal links as build errors. |
| Image or asset fails to load | Use semantic `alt` text on all images so content is understandable even if images fail. (NFR-003) |

## 15. Platform and Implementation Risks

### Risk 1: Workflow diagram complexity

- **What could go wrong:** The HTML/CSS workflow diagram may become hard to maintain or may not render well on all viewport sizes, especially for the full 7-stage pipeline with branching paths (conversation vs. document path).
- **Which requirements it threatens:** US-002 (visual workflow on homepage), NFR-005 (responsive)
- **What to validate:** Build the diagram component in Phase 1 and test across mobile, tablet, and desktop. Verify readability at 320px width.
- **Fallback:** Replace HTML/CSS diagram with a static SVG image. Loses editability but guarantees consistent rendering.

### Risk 2: Content collection schema drift

- **What could go wrong:** As the SDLC pipeline evolves, the command descriptions and artifact examples in content collections may fall out of sync with the actual prompt files.
- **Which requirements it threatens:** US-006 (accurate command explanations), US-018 (accurate artifact examples)
- **What to validate:** Compare content collection entries against the actual skill/ prompt files during a review phase.
- **Fallback:** Add a build-time check that validates content collection entries reference files that exist.

### Risk 3: GitHub Pages base path configuration

- **What could go wrong:** Until the repository name is chosen, the `base` path in `astro.config.mjs` is a placeholder. If someone deploys before updating it, all internal links and asset paths will break.
- **Which requirements it threatens:** FR-005 (repo name TBD), NFR-008 (automated deploy)
- **What to validate:** Test the build with a placeholder base path and with a real one. Ensure the config variable propagates to all internal links.
- **Fallback:** Default `base` to `/` (root deployment) so the site works immediately on `bonjohen.github.io` as a user site, then update to `/{repo-name}` when the name is chosen.

### Risk 4: Markdown content rendering fidelity

- **What could go wrong:** SDLC artifact examples contain complex markdown (nested tables, code blocks inside blockquotes, frontmatter). Astro's markdown renderer may not handle all edge cases identically to how they appear in the source files.
- **Which requirements it threatens:** US-018 (view example artifacts)
- **What to validate:** Include one complex artifact example in Phase 2 and verify rendering.
- **Fallback:** Use MDX for artifact example pages to allow custom rendering components for edge cases.

## 16. Security and Privacy Requirements

- **No secrets in the repository.** The site is public and contains no API keys, tokens, or credentials. If analytics are added later, any analytics ID should be in environment variables, not committed to source.
- **HTTPS only.** GitHub Pages serves over HTTPS by default. All internal links should use relative paths (no `http://` references).
- **No user input.** The site accepts no form data, file uploads, or query parameters that affect content rendering. The XSS and injection attack surface is zero.
- **Subresource integrity.** If external CDN resources are used (fonts, scripts), use SRI hashes. Prefer self-hosted assets to eliminate external dependencies.
- **Content Security Policy.** Set a restrictive CSP via `<meta>` tag: `default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; script-src 'self'`. Relax only if specific features require it.

## 17. Acceptance Criteria

These are design-level acceptance criteria that verify the PDR's decisions, not the user requirements' acceptance criteria (which are in final.user.md).

| ID | Criterion |
|----|-----------|
| PDR-AC-001 | `npm run build` (or equivalent Astro build command) produces a directory of static HTML files with no server-side dependencies |
| PDR-AC-002 | The built output deploys to GitHub Pages via a GitHub Actions workflow and the site is accessible at the expected URL |
| PDR-AC-003 | Changing `repoName` in `src/config.ts` and rebuilding updates all GitHub repository links across the site |
| PDR-AC-004 | Adding a new page requires creating at most 2 files (content file + optional nav config update) |
| PDR-AC-005 | The workflow diagram renders correctly at 320px, 768px, and 1440px viewport widths |
| PDR-AC-006 | All pages are readable with JavaScript disabled |
| PDR-AC-007 | Lighthouse accessibility score is >= 90 on all pages |
| PDR-AC-008 | A CNAME file addition and DNS update is sufficient to serve the site under `johnboen.com` |

## 18. Recommended Planning Phases

1. **Phase 0 — Project scaffold and deployment pipeline.** Initialize Astro project, configure GitHub Actions for Pages deployment, verify deployment works with placeholder content. Proves the build/deploy pipeline before writing real content.

2. **Phase 1 — Homepage and core layout.** Build BaseLayout, ContentLayout, Nav, Footer, and the homepage with WorkflowDiagram. The site has one functional page with the workflow-first design.

3. **Phase 2 — Workflow and command pages.** Build the workflow page with CommandCard components and PathDiagram. Content collection schemas for commands. All 8 commands explained.

4. **Phase 3 — Education and getting-started pages.** Build the "Why Stages?" education page and the getting-started page with command sequences and workflow paths.

5. **Phase 4 — Portfolio and artifacts pages.** Build the portfolio/case-study page and the artifacts page with ArtifactExample components. Content collection for artifacts.

6. **Phase 5 — Polish, accessibility, SEO, and custom domain readiness.** 404 page, meta tags, Open Graph, sitemap, CNAME readiness, accessibility audit, responsive testing.

## 19. Planning Notes

- Phase 0 must prove deployment before any content work. A broken pipeline blocks everything.
- The workflow diagram (Phase 1) is the highest-risk visual component. If it takes too long or renders poorly, the fallback is a static SVG.
- Content collections (Phase 2, 4) should be populated with real SDLC artifacts from this project, not placeholder Lorem Ipsum. The site is a portfolio piece — the content IS the product.
- The repo name placeholder (`repoName` in `src/config.ts`) should be tested in Phase 0 with both empty and populated values to catch broken link patterns early.
- Accessibility (Phase 5) should be checked incrementally during earlier phases, not deferred entirely. But the formal audit and fix pass belongs in Phase 5.

## 20. Concerns for Release Planning

1. **Phase 0 must validate both GitHub Actions and the base-path config (Section 8.3).** The plan should not proceed to content phases until deployment is proven. Risk 3 (base path configuration) is the most likely early blocker.

2. **The WorkflowDiagram component (Section 10.3) is the highest-risk UI element.** It must render a multi-stage pipeline with branching paths responsively. The plan should validate it early (Phase 1) and allocate time for fallback to SVG if the HTML/CSS approach is too fragile.

3. **Content collection population (Sections 9.2, 9.3) depends on the actual SDLC prompt files being stable.** If the prompt pipeline is still being revised, artifact examples and command descriptions may need updates. The plan should sequence content population after the prompt files are finalized, or plan for a content update pass.

4. **The portfolio page (US-014 through US-017) requires editorial judgment about tone and claim boundaries.** FR-025 says "no exaggerated claims." The plan should include a content review step for the portfolio page specifically, not just a build-and-ship task.

5. **Custom domain readiness (NFR-010, Concern 3 from draft.user.md) does not require the domain to be configured during initial development,** but the plan must verify that adding a CNAME file does not break the GitHub Pages base-path configuration. Test this in the final phase.

6. **Accessibility (NFR-003, NFR-004) should be checked incrementally, not batched into a final phase.** The plan should include accessibility checks as verification criteria in every phase that produces visible UI, with a comprehensive audit in the final phase.
