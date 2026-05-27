---
document: "Physical Design Requirements"
version: "1.0"
status: "final"
source: "sdlc/docs/draft.pdr.md"
user_requirements: "sdlc/docs/final.user.md"
finalized_date: "2026-05-21"
---

# I2I — From Idea to Implementation — Physical Design Requirements

**Source document:** `sdlc/docs/final.user.md`
**Project root:** `C:\Projects\sdlc`
**Date:** 2026-05-21

## 1. System Context

### 1.1 Existing Infrastructure to Reuse

| Asset | Location | Reuse Strategy |
|-------|----------|---------------|
| SDLC prompt files | `skill/*.md` | Source content for Command content collection entries (US-006) and for artifact examples (US-018) |
| Draft SDLC documents | `sdlc/docs/draft.*.md` | Example generated artifacts for the Artifacts page |
| Final SDLC documents | `sdlc/docs/final.*.md` | Example generated artifacts for the Artifacts page |
| Pipeline diagram (ASCII) | `skill/prompt-instructions.md` | Reference for WorkflowDiagram component layout — the text pipeline diagram shows the canonical stage ordering |
| SKILL.md command table | `skill/SKILL.md` | Authoritative list of 8 commands with descriptions, used to populate Command content collection entries |

<!-- Added during finalization: the draft PDR references content sourcing from SDLC artifacts but does not enumerate which specific files are reusable. This table makes the source-to-content mapping explicit so implementation tasks can reference concrete files. -->

### 1.2 New Dependencies

| Package | Purpose | Version Constraint | License |
|---------|---------|-------------------|---------|
| `astro` | Static site generator (framework) | `^5.x` | MIT |
| `@astrojs/sitemap` | Auto-generated `sitemap.xml` for SEO (NFR-006) | Compatible with Astro 5 | MIT |
| `sharp` | Image optimization at build time (Astro default dependency) | `^0.33.x` | Apache-2.0 |

No runtime dependencies. All packages are build-time only. The deployed site is static HTML, CSS, and optionally JS — no Node.js server is needed at runtime.

<!-- Added during finalization: the draft PDR names Astro but does not list it as a formal dependency with version constraints. @astrojs/sitemap is required by NFR-006 (auto-generated sitemap) but was not mentioned in the draft. -->

### 1.3 Configuration

| Variable | Location | Type | Default | Description |
|----------|----------|------|---------|-------------|
| `site` | `astro.config.mjs` | string | `"https://bonjohen.github.io"` | Full site URL for canonical links, sitemap, and OG tags |
| `base` | `astro.config.mjs` | string | `"/"` | Base path for GitHub Pages; update to `"/{repo-name}"` when repository name is chosen (FR-005) |
| `repoName` | `src/config.ts` | string | `""` | Repository name for GitHub links; empty until chosen |
| `repoUrl` | `src/config.ts` | string | computed | `https://github.com/bonjohen/${repoName}` — renders as profile link when repoName is empty |
| `creatorName` | `src/config.ts` | string | `"John Boen"` | Creator display name used in footer and portfolio page |
| `creatorGithub` | `src/config.ts` | string | `"https://github.com/bonjohen"` | GitHub profile URL |
| `siteTitle` | `src/config.ts` | string | `"I2I — From Idea to Implementation"` | Site-wide title for `<title>` tag and Open Graph metadata |
| `siteDescription` | `src/config.ts` | string | `"A prompt-driven SDLC workflow from idea to implementation"` | Default `<meta description>` and OG description |

<!-- Added during finalization: siteTitle and siteDescription are needed for BaseLayout's <head> rendering (NFR-006) and Open Graph tags but were not in the draft's config table. -->

## 2. Data Model

This is a static site with no database. The data model is the content structure: page frontmatter and content collection schemas.

### 2.1 Content Collection Schemas

Content collections use Astro's built-in Zod-based schema validation. Schemas are defined in `src/content/config.ts` and enforced at build time — a schema violation fails the build.

**Command collection** (`src/content/commands/*.md`):

```typescript
import { defineCollection, z } from 'astro:content';

const commands = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),           // e.g., "draft-user"
    purpose: z.string(),        // One-line description
    input: z.string(),          // What the command reads
    output: z.string(),         // What the command produces
    path: z.enum(["conversation", "document", "both"]),
    sortOrder: z.number(),      // Display order matching pipeline sequence
  }),
});
```

**Artifact collection** (`src/content/artifacts/*.md`):

```typescript
const artifacts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),          // Display name of the artifact
    type: z.enum(["prompt", "generated"]),
    command: z.string().optional(),  // Which SDLC command produced this
    excerpt: z.boolean().default(false),  // true if truncated
    sortOrder: z.number(),      // Display order on artifacts page
  }),
});

export const collections = { commands, artifacts };
```

<!-- Added during finalization: the draft PDR defines the data model as prose tables. These Zod schemas are the executable equivalent for Astro — they are the actual code that will live in src/content/config.ts. Build-time validation ensures content entries conform to the schema. -->

### 2.2 Page Frontmatter

Pages use Astro's built-in frontmatter (not content collections). Each `.astro` page file defines props passed to its layout:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `title` | string | Yes | Page `<title>` and `<h1>` |
| `description` | string | Yes | `<meta name="description">` and OG description |
| `navOrder` | number | No | Position in navigation bar; omit to exclude from nav (e.g., 404 page) |
| `navLabel` | string | No | Display text in nav; defaults to `title` if omitted |

### 2.3 Seed Data

Content collection entries are populated from the existing SDLC project files, not from placeholder text.

**Command entries** (8 total, one per SDLC command):

| Entry File | `name` | `path` | Source |
|------------|--------|--------|--------|
| `draft-user.md` | `draft-user` | `conversation` | `skill/draft-user.md` header |
| `draft-pdr.md` | `draft-pdr` | `conversation` | `skill/draft-pdr.md` header |
| `draft-plan.md` | `draft-plan` | `conversation` | `skill/draft-plan.md` header |
| `gen-pdr.md` | `gen-pdr` | `document` | `skill/gen-pdr.md` header |
| `gen-plan.md` | `gen-plan` | `document` | `skill/gen-plan.md` header |
| `finalize.md` | `finalize` | `document` | `skill/finalize.md` header |
| `expand.md` | `expand` | `document` | `skill/expand.md` header |
| `implement.md` | `implement` | `document` | `skill/implement.md` header |

**Artifact entries** (minimum 2, sourced from actual SDLC outputs):

| Entry File | `type` | Source |
|------------|--------|--------|
| At least one prompt excerpt | `prompt` | A truncated section from one of `skill/*.md` |
| At least one generated document excerpt | `generated` | A truncated section from one of `sdlc/docs/*.md` |

<!-- Added during finalization: the draft PDR describes what content collections contain but does not map entries to specific source files. This table ensures implementation tasks know exactly where to source each entry. -->

## 3. Package Layout

```
i2i/                              # Project root (repo name TBD)
├── astro.config.mjs              # Astro configuration (site, base, integrations)
├── package.json                  # Dependencies and scripts
├── tsconfig.json                 # TypeScript configuration (Astro default)
├── .github/
│   └── workflows/
│       └── deploy.yml            # GitHub Actions: build + deploy to Pages
├── public/
│   └── favicon.svg               # Site favicon
├── src/
│   ├── config.ts                 # Site-wide configuration variables (Section 1.3)
│   ├── content/
│   │   ├── config.ts             # Content collection schemas (Section 2.1)
│   │   ├── commands/
│   │   │   ├── draft-user.md     # One file per SDLC command
│   │   │   ├── draft-pdr.md
│   │   │   ├── draft-plan.md
│   │   │   ├── gen-pdr.md
│   │   │   ├── gen-plan.md
│   │   │   ├── finalize.md
│   │   │   ├── expand.md
│   │   │   └── implement.md
│   │   └── artifacts/
│   │       ├── prompt-example.md   # At least one prompt excerpt
│   │       └── generated-example.md # At least one generated doc excerpt
│   ├── components/
│   │   ├── Nav.astro             # Responsive navigation bar
│   │   ├── Footer.astro          # Site footer with GitHub link
│   │   ├── WorkflowDiagram.astro # Visual SDLC pipeline diagram
│   │   ├── CommandCard.astro     # Single command display card
│   │   ├── PathDiagram.astro     # Three workflow paths visualization
│   │   └── ArtifactExample.astro # Artifact display with type label
│   ├── layouts/
│   │   ├── BaseLayout.astro      # HTML shell (<html>, <head>, <body>)
│   │   └── ContentLayout.astro   # BaseLayout + Nav + main + Footer
│   ├── pages/
│   │   ├── index.astro           # Homepage — /
│   │   ├── workflow.astro        # Workflow — /workflow/
│   │   ├── why.astro             # Education — /why/
│   │   ├── getting-started.astro # Getting Started — /getting-started/
│   │   ├── portfolio.astro       # Portfolio — /portfolio/
│   │   ├── artifacts.astro       # Artifacts — /artifacts/
│   │   └── 404.astro             # Not Found — /404/
│   └── styles/
│       └── global.css            # Global styles, CSS custom properties, typography
```

<!-- Added during finalization: the draft PDR shows an architectural layers diagram but does not include a file tree. This layout is derived from the draft's component, page, and content collection specifications applied to Astro's conventional directory structure. -->

## 4. Component Designs

### 4.1 BaseLayout

- **Purpose:** HTML shell shared by all pages. Renders `<html>`, `<head>` (with title, meta description, Open Graph tags, canonical URL, Content Security Policy), and `<body>` with skip-to-content link.
- **Location:** `src/layouts/BaseLayout.astro`
- **Implements:** NFR-003 (skip-to-content link, semantic HTML), NFR-006 (meta tags, canonical URL, OG tags)
- **Interface:**
  ```astro
  ---
  interface Props {
    title: string;
    description: string;
  }
  ---
  ```
- **Behavior:** Receives `title` and `description` from the page. Renders `<title>{title} | {siteTitle}</title>`, `<meta name="description" content="{description}">`, Open Graph `og:title`, `og:description`, `og:type="website"`, and `og:url`. Includes `global.css` import. Renders a `<a href="#main-content" class="skip-link">Skip to content</a>` as the first focusable element. Includes CSP `<meta>` tag (see Section 6).
- **Dependencies:** `src/config.ts` for `siteTitle` and `siteDescription`; `src/styles/global.css`.

### 4.2 ContentLayout

- **Purpose:** Wraps BaseLayout with site navigation, main content area, and footer. Used by all content pages.
- **Location:** `src/layouts/ContentLayout.astro`
- **Implements:** US-003 (navigation paths), US-022 (workflow-first nav), US-023 (creator info reachable)
- **Interface:**
  ```astro
  ---
  interface Props {
    title: string;
    description: string;
  }
  ---
  ```
- **Behavior:** Renders `<BaseLayout>` → `<Nav />` → `<main id="main-content">` → `<slot />` → `<Footer />`. The `id="main-content"` on `<main>` is the target of BaseLayout's skip link.
- **Dependencies:** BaseLayout, Nav, Footer.

### 4.3 Nav

- **Purpose:** Persistent top-level navigation bar. Renders links to all top-level pages sorted by `navOrder`. Highlights the current page. Collapses to hamburger menu on mobile.
- **Location:** `src/components/Nav.astro`
- **Implements:** US-003, US-022, US-023, NFR-002 (works without JS), NFR-005 (responsive)
- **Interface:** No props. Reads page navigation data at build time.
- **Behavior:** Navigation links are defined as a static array matching the page table in Section 5. Sort by `navOrder`. Render as `<nav aria-label="Main navigation">` with `<a>` elements. Current page link gets `aria-current="page"`. Mobile hamburger uses a CSS-only `<input type="checkbox">` + `<label>` toggle pattern so it works without JavaScript (NFR-002). Below 768px viewport width, the nav collapses. Above 768px, links display inline.
- **Dependencies:** `src/config.ts` for `creatorGithub` (GitHub nav link).

### 4.4 Footer

- **Purpose:** Site footer with GitHub link, creator attribution, and year.
- **Location:** `src/components/Footer.astro`
- **Implements:** US-015 (GitHub link), US-017 (creator portfolio links)
- **Interface:** No props.
- **Behavior:** Renders `<footer>` with link to `creatorGithub`, link to `repoUrl` (if `repoName` is set), and creator name. Includes `role="contentinfo"` for accessibility.
- **Dependencies:** `src/config.ts` for `creatorGithub`, `repoUrl`, `repoName`, `creatorName`.

### 4.5 WorkflowDiagram

- **Purpose:** Visual representation of the SDLC pipeline from Idea to Implementation, showing the full 7-stage sequence with conversation vs. document paths.
- **Location:** `src/components/WorkflowDiagram.astro`
- **Implements:** US-002 (visual workflow on homepage), NFR-002 (readable without JS), NFR-003 (accessible), NFR-005 (responsive)
- **Interface:** No props. Self-contained.
- **Behavior:** Renders as semantic HTML + CSS. Stages are presented as labeled boxes connected by directional arrows. The diagram shows two input paths (conversation path entering via `draft-*` commands, document path entering via `gen-*` commands) converging at `finalize`, then flowing through `expand` to `implement`. Must be readable without JavaScript. Accessible via `role="img"` and `aria-label` describing the pipeline sequence. Uses CSS Grid or Flexbox for layout.
- **Responsive behavior:** At desktop (>= 1024px), stages flow left-to-right in a horizontal pipeline. At tablet (768px–1023px), stages may wrap into 2 rows. At mobile (< 768px), stages stack vertically. All viewport sizes must show the complete pipeline — no stages hidden behind overflow or scroll.
- **Fallback:** If the HTML/CSS approach fails responsive testing at 320px, replace with a static SVG image. The component interface (`<WorkflowDiagram />` with no props) stays the same either way.
- **Dependencies:** None.

### 4.6 CommandCard

- **Purpose:** Displays a single SDLC command: name, purpose, input, output, and workflow path membership.
- **Location:** `src/components/CommandCard.astro`
- **Implements:** US-006 (explain each command)
- **Interface:**
  ```astro
  ---
  interface Props {
    name: string;
    purpose: string;
    input: string;
    output: string;
    path: "conversation" | "document" | "both";
  }
  ---
  ```
- **Behavior:** Renders as a styled card element (`<article>`) with the command name as heading, purpose as description, and input/output as labeled fields. The `path` field renders as a visual tag or badge indicating which workflow path the command belongs to. Cards are used on the workflow page in pipeline order.
- **Dependencies:** None (receives data as props from the Workflow page).

### 4.7 PathDiagram

- **Purpose:** Shows the three workflow paths (conversation, fast, mixed) as visual flows indicating which commands appear in each path.
- **Location:** `src/components/PathDiagram.astro`
- **Implements:** US-007 (explain the three paths)
- **Interface:** No props. Self-contained.
- **Behavior:** Renders as CSS-styled HTML showing three labeled paths. Each path lists its command sequence. Visual arrows or connectors show flow direction. Conversation path: `draft-user` → `draft-pdr` → `draft-plan` → `finalize` → `expand` → `implement`. Fast path: `draft-user` → `gen-pdr` → `gen-plan` → `finalize` → `expand` → `implement`. Mixed path: any combination. Must be readable without JavaScript.
- **Dependencies:** None.

### 4.8 ArtifactExample

- **Purpose:** Renders a prompt or generated document example with title, type label, and content in a styled block.
- **Location:** `src/components/ArtifactExample.astro`
- **Implements:** US-018 (view example artifacts), US-019 (accessible from deeper pages)
- **Interface:**
  ```astro
  ---
  interface Props {
    title: string;
    type: "prompt" | "generated";
    command?: string;
    excerpt: boolean;
  }
  ---
  ```
- **Behavior:** Renders as a styled block (`<article>`) with the artifact title, a visual type badge ("Prompt" or "Generated Document"), optional command label (e.g., "from `finalize`"), and the artifact content as rendered markdown. If `excerpt` is true, displays a note: "This is an excerpt. See the full document in the repository."
- **Dependencies:** None (receives data as props from the Artifacts page).

## 5. Site Routes

No API endpoints. The site serves only static HTML pages.

| Page | Route | Nav Order | Primary Stories | Purpose |
|------|-------|-----------|----------------|---------|
| Homepage | `/` | 1 | US-001, US-002, US-003, US-004, US-022 | Project name, workflow diagram, navigation CTAs. Workflow-first. |
| Workflow | `/workflow/` | 2 | US-005–US-010 | All 8 commands explained. Three paths shown. Stage-by-stage detail. |
| Education | `/why/` | 3 | US-011 | Why the workflow is staged. Rationale for gap surfacing, traceability, phased execution. |
| Getting Started | `/getting-started/` | 4 | US-012, US-013 | Command sequence for normal workflow. Fast and mixed paths. |
| Portfolio | `/portfolio/` | 5 | US-014–US-017, US-023 | Case study. Creator role. GitHub links. |
| Artifacts | `/artifacts/` | 6 | US-018, US-019 | Example prompts and generated documents. |
| 404 | `/404/` | *(excluded)* | *(inferred)* | Custom 404 page with navigation back to homepage. |

**Page content specifications:**

**Homepage** (`src/pages/index.astro`)
- Project title: "I2I — From Idea to Implementation"
- Subtitle: one sentence explaining the project
- WorkflowDiagram component as the central visual
- Three CTA sections: "Learn the Workflow" → `/workflow/`, "See Examples" → `/artifacts/`, "About the Creator" → `/portfolio/`
- Footer with GitHub link

**Workflow** (`src/pages/workflow.astro`)
- Heading: "The SDLC Pipeline"
- Stage-by-stage explanation with CommandCard components for each of the 8 commands in pipeline order
- PathDiagram showing conversation path, fast path, mixed path
- Sections explaining what finalize, expand, and implement each produce

**Education** (`src/pages/why.astro`)
- Heading: "Why Stages?"
- Sections explaining: gap surfacing (drafts miss things; finalization catches them), traceability (IDs chain from user need to task), phased execution (each phase is independently shippable), human-in-the-loop (AI assists, human reviews)
- Tone: educational, not marketing

**Getting Started** (`src/pages/getting-started.astro`)
- Heading: "Getting Started"
- Step-by-step command sequence for the normal (conversation) workflow
- Alternate sequences for fast path and mixed path
- Expected output at each step

**Portfolio** (`src/pages/portfolio.astro`)
- Heading: "About This Project"
- What the project demonstrates: AI workflow design, SDLC methodology, documentation practice, software planning
- The creator's role and approach
- Links to GitHub profile (`bonjohen`) and repository (once named)
- Optional: links to `johnboen.com` or broader portfolio
- Tone: credible, technical, practical — no exaggerated claims (Constraint: human-in-the-loop framing)

**Artifacts** (`src/pages/artifacts.astro`)
- Heading: "Example Artifacts"
- ArtifactExample components for each artifact content collection entry
- Each labeled by type (prompt vs. generated) and command

**404** (`src/pages/404.astro`)
- "Page not found" message
- Link back to homepage
- Same ContentLayout as other pages (navigation bar and footer present)

## 6. Security Design

The attack surface is minimal — the site accepts no user input, serves no dynamic content, and has no backend.

**HTTPS:** GitHub Pages serves over HTTPS by default. All internal links use relative paths. No `http://` references anywhere.

**Content Security Policy:** Set via `<meta>` tag in BaseLayout:

```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; script-src 'self'; font-src 'self';">
```

`'unsafe-inline'` is required for Astro's scoped styles. If external fonts or scripts are added later, update the CSP to include their origins with Subresource Integrity hashes.

**Subresource Integrity:** If any external CDN resources are used (fonts, scripts), they must include `integrity` and `crossorigin` attributes. Prefer self-hosting to eliminate external dependencies entirely.

**No secrets in the repository.** The site is fully public. No API keys, tokens, or credentials exist in the codebase. If analytics are added later, any analytics ID must be provided via environment variable, not committed to source.

**No user input.** No forms, no file uploads, no query parameters that affect rendering. The XSS and injection attack surface is zero.

## 7. Observability

There is no runtime server to monitor. Observability covers the build and deployment pipeline only.

| Concern | Mechanism |
|---------|-----------|
| Build success/failure | GitHub Actions workflow logs; status check on the deployment branch |
| Deploy status | GitHub Pages deployment status in the repository's Environments tab |
| Broken links | Build-time link validation (Astro warns on broken internal links; configure as build errors) |
| Content schema violations | Astro's content collection validation fails the build if frontmatter doesn't match schema |
| Site availability | Bounded by GitHub Pages SLA (~99.9%). No additional monitoring needed for initial release. |

No client-side error reporting, no analytics, no logging in the initial release. If analytics are added later, use a privacy-respecting, cookieless service (e.g., Plausible or Fathom) per the user requirements (Section 6: Out of Scope, with allowance for future minimal analytics).

<!-- Added during finalization: the draft PDR has no observability section. For a static site, observability is the build/deploy pipeline — these are the things that break and need visibility. -->

## 8. Test Strategy

No traditional unit tests or integration tests are needed — there is no application logic, no API, no database. Testing validates the build output and the deployed site.

| Test Type | What It Validates | When It Runs | Tool |
|-----------|------------------|-------------|------|
| Build verification | `npm run build` completes without errors | Every phase, every CI run | `astro build` (exit code) |
| Content schema validation | Frontmatter in content collection entries conforms to Zod schemas | Build time (automatic) | Astro built-in |
| Internal link validation | No broken internal links in built output | Build time | Astro build warnings configured as errors |
| HTML validation | Valid HTML5 output | Phase 5 (final verification) | W3C Nu HTML Checker or `html-validate` |
| Accessibility audit | Lighthouse accessibility score >= 90 on all pages (NFR-003, NFR-004) | Every UI phase (spot-check), Phase 5 (comprehensive) | Lighthouse CLI or Chrome DevTools |
| Responsive verification | Pages render correctly at 320px, 768px, 1440px, 2560px (NFR-005) | Every UI phase (spot-check) | Browser DevTools responsive mode |
| No-JS verification | Core content readable with JavaScript disabled (NFR-002) | Phases 1–4 (spot-check) | Browser with JS disabled |
| Config propagation | Changing `repoName` updates all GitHub links (PDR-AC-003) | Phase 0 | Manual: change value, rebuild, verify |

**Mocking:** Not applicable. There are no external dependencies to mock.

**Test data:** Content collection entries serve as test data. They are populated from real SDLC artifacts (Section 2.3), not synthetic data.

**CI integration:** The GitHub Actions deploy workflow runs `astro build`. If the build fails (broken links, schema violations, compilation errors), the deployment is blocked. No separate test step is needed — the build IS the test gate for most validations. Lighthouse CI can be added as a separate workflow step in Phase 5.

<!-- Added during finalization: the draft PDR has no test strategy. The draft plan noted this gap. For a static site, the build is the primary test — schema validation and link checking happen at build time. Accessibility and responsive checks are manual during development and automated via Lighthouse CI for ongoing verification. -->

## 9. Error Handling

The error surface for a static site is small:

| Error Scenario | Design Response |
|----------------|----------------|
| Visitor requests a URL that does not exist | Custom 404 page with site navigation and link to homepage |
| Browser does not support modern CSS (Grid, Flexbox) | Graceful degradation: content remains readable in single-column layout. No critical information hidden behind CSS features. |
| JavaScript is disabled | All core content is static HTML. No functionality is lost. (NFR-002) |
| GitHub Pages is down | No mitigation possible. Availability bounded by GitHub Pages SLA. (NFR-007) |
| Broken internal link (build-time) | Astro build warns on broken links. Configure as build error to prevent deployment with broken links. |
| Image or asset fails to load | Semantic `alt` text on all images so content is understandable without images. (NFR-003) |

## 10. Risks

### Risk 1: Workflow diagram complexity

- **What could go wrong:** The HTML/CSS WorkflowDiagram may not render well on all viewport sizes, especially for the full 7-stage pipeline with branching paths.
- **Requirements threatened:** US-002, NFR-005
- **Validation:** Build the component in Phase 1 and test at 320px, 768px, 1440px.
- **Fallback:** Replace HTML/CSS with a static SVG. Component interface (`<WorkflowDiagram />`) is unchanged.

### Risk 2: Content collection schema drift

- **What could go wrong:** As the SDLC pipeline evolves, command descriptions and artifact examples may fall out of sync with actual prompt files.
- **Requirements threatened:** US-006, US-018
- **Validation:** Compare content collection entries against `skill/*.md` files during Phase 5 content review.
- **Fallback:** Add build-time check that validates referenced source files exist.

### Risk 3: GitHub Pages base path configuration

- **What could go wrong:** Until the repo name is chosen, the `base` path is a placeholder. Deploying before updating it breaks all internal links and asset paths.
- **Requirements threatened:** FR-005, NFR-008
- **Validation:** Test build with `base: "/"` (default) and with `base: "/test-repo"` in Phase 0.
- **Fallback:** Default `base` to `"/"` for root deployment, update when name is chosen.

### Risk 4: Markdown rendering fidelity

- **What could go wrong:** SDLC artifact examples contain complex markdown (nested tables, code blocks in blockquotes). Astro's renderer may not handle all edge cases.
- **Requirements threatened:** US-018
- **Validation:** Include one complex artifact example in Phase 4 and verify rendering.
- **Fallback:** Use MDX for artifact pages to allow custom rendering components.

## 11. NFR Design Responses

Each non-functional requirement from `final.user.md` has a specific design mechanism:

| NFR | Requirement | Design Response |
|-----|------------|----------------|
| NFR-001 | LCP < 2.5s on 10 Mbps | Astro ships zero JS by default. Pages are pre-built static HTML. No client-side rendering delay. |
| NFR-002 | Works without JavaScript | All content is static HTML. Nav hamburger uses CSS-only toggle. No JS-dependent layouts or content. |
| NFR-003 | WCAG 2.1 AA — keyboard + screen reader | Skip-to-content link in BaseLayout. Semantic HTML (`<nav>`, `<main>`, `<footer>`, `<article>`). `aria-label` on WorkflowDiagram. `aria-current="page"` on active nav link. |
| NFR-004 | Contrast >= 4.5:1 body, >= 3:1 large | `global.css` defines color tokens with minimum contrast ratios. Verified via Lighthouse accessibility audit. |
| NFR-005 | Responsive 320px–2560px | CSS Grid/Flexbox layouts. WorkflowDiagram responsive breakpoints (Section 4.5). Nav hamburger below 768px. |
| NFR-006 | SEO — title, description, sitemap | BaseLayout renders `<title>`, `<meta description>`, OG tags per page. `@astrojs/sitemap` generates `sitemap.xml`. Semantic headings. |
| NFR-007 | Available when GitHub Pages is available | No additional infrastructure. Bounded by GitHub Pages SLA. |
| NFR-008 | Auto-deploy within 5 min of push | GitHub Actions workflow triggered by push to deployment branch. Astro build + Pages deploy action. |
| NFR-009 | New page <= 2 files | Create `.astro` page file + add entry to Nav's page array. Content collection pages need only an `.md` file. |
| NFR-010 | Custom domain via CNAME + DNS | `public/CNAME` file (added when ready). `base` in `astro.config.mjs` updated to `"/"` for root domain. No structural changes needed. |

<!-- Added during finalization: the draft PDR addresses NFRs implicitly throughout the document but does not provide a consolidated mapping from each NFR to its design mechanism. This table makes the coverage explicit and verifiable. -->

## 12. UI Design Principles

- **Clean and readable.** Generous whitespace, body text >= 16px, high contrast. The site is primarily a reading experience.
- **Credible, not flashy.** Professional and understated. No gratuitous animations or decorative elements. The marketing tone is technical and practical.
- **Workflow-first hierarchy.** The homepage leads with the workflow diagram and explanation. Creator information is reachable but secondary.

## 13. Privacy and Permissions

- No visitor data collected in the initial release. No cookies, no analytics, no forms, no tracking pixels.
- All content is public. No authentication or authorization.
- If analytics are added later, use a privacy-respecting cookieless service, disclosed visibly. Not in scope for initial release.

## 14. PDR Acceptance Criteria

| ID | Criterion |
|----|-----------|
| PDR-AC-001 | `npm run build` produces a directory of static HTML files with no server-side dependencies |
| PDR-AC-002 | The built output deploys to GitHub Pages via a GitHub Actions workflow and the site is accessible at the expected URL |
| PDR-AC-003 | Changing `repoName` in `src/config.ts` and rebuilding updates all GitHub repository links across the site |
| PDR-AC-004 | Adding a new page requires creating at most 2 files (content file + optional nav config update) |
| PDR-AC-005 | The WorkflowDiagram renders correctly at 320px, 768px, and 1440px viewport widths |
| PDR-AC-006 | All pages are readable with JavaScript disabled |
| PDR-AC-007 | Lighthouse accessibility score >= 90 on all pages |
| PDR-AC-008 | A CNAME file addition and DNS update is sufficient to serve the site under `johnboen.com` |

## 15. Traceability Matrix

| User Story | PDR Section | Component | Page/Route |
|-----------|-------------|-----------|------------|
| US-001 | 5 (Homepage) | — | Homepage `/` |
| US-002 | 4.5 (WorkflowDiagram) | WorkflowDiagram | Homepage `/` |
| US-003 | 4.3 (Nav), 5 (Homepage) | Nav | Homepage `/` |
| US-004 | 5 (all pages) | ContentLayout | All pages |
| US-005 | 5 (Workflow) | — | Workflow `/workflow/` |
| US-006 | 4.6 (CommandCard), 2.1 (Command collection) | CommandCard | Workflow `/workflow/` |
| US-007 | 4.7 (PathDiagram) | PathDiagram | Workflow `/workflow/` |
| US-008 | 5 (Workflow) | — | Workflow `/workflow/` |
| US-009 | 5 (Workflow) | — | Workflow `/workflow/` |
| US-010 | 5 (Workflow) | — | Workflow `/workflow/` |
| US-011 | 5 (Education) | — | Education `/why/` |
| US-012 | 5 (Getting Started) | — | Getting Started `/getting-started/` |
| US-013 | 5 (Getting Started) | — | Getting Started `/getting-started/` |
| US-014 | 5 (Portfolio) | — | Portfolio `/portfolio/` |
| US-015 | 4.4 (Footer), 1.3 (Config) | Footer | Portfolio `/portfolio/`, Footer (all pages) |
| US-016 | 5 (Portfolio) | — | Portfolio `/portfolio/` |
| US-017 | 4.4 (Footer) | Footer | Portfolio `/portfolio/`, Footer (all pages) |
| US-018 | 4.8 (ArtifactExample), 2.1 (Artifact collection) | ArtifactExample | Artifacts `/artifacts/` |
| US-019 | 5 (Artifacts) | ArtifactExample | Artifacts `/artifacts/` |
| US-020 | 1.2 (Dependencies), 8 (Test — CI) | — | GitHub Actions workflow |
| US-021 | 2.1 (Content Collections) | — | Build pipeline |
| US-022 | 4.3 (Nav), 5 (Homepage) | Nav | Homepage `/` |
| US-023 | 4.3 (Nav), 5 (Portfolio) | Nav | Portfolio `/portfolio/` |
| NFR-001 | 11 (NFR Design Responses) | — | All pages (Astro zero-JS) |
| NFR-002 | 4.3 (Nav CSS-only), 4.5 (WD no-JS) | Nav, WorkflowDiagram | All pages |
| NFR-003 | 4.1 (BaseLayout skip link), 4.5 (WD ARIA) | BaseLayout, WorkflowDiagram | All pages |
| NFR-004 | 11 (NFR Design Responses), 12 (UI Principles) | — | All pages (global.css tokens) |
| NFR-005 | 4.3 (Nav responsive), 4.5 (WD responsive) | Nav, WorkflowDiagram | All pages |
| NFR-006 | 4.1 (BaseLayout meta), 1.2 (@astrojs/sitemap) | BaseLayout | All pages |
| NFR-007 | 11 (NFR Design Responses) | — | GitHub Pages SLA |
| NFR-008 | 8 (Test — CI) | — | GitHub Actions workflow |
| NFR-009 | 3 (Package Layout) | — | Astro page model |
| NFR-010 | 1.3 (Config — base), 11 (NFR Design Responses) | — | `public/CNAME`, `astro.config.mjs` |
