---
phase: 01
title: "Homepage and Core Layout"
depends_on: "Phase 00"
goal: "The site has a functional homepage with the workflow-first design, responsive navigation, and all shared layout components. The WorkflowDiagram renders correctly across viewport sizes."
source_pdr_sections: ["4.1", "4.2", "4.3", "4.4", "4.5", "5", "6", "12"]
source_user_stories: ["US-001", "US-002", "US-003", "US-004", "US-022"]
status: "completed"
---

# Phase 01: Homepage and Core Layout

## Tasks

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

## Context

### Files to Create or Modify

- `src/styles/global.css` — Global styles: reset, typography, color tokens, responsive breakpoints
- `src/layouts/BaseLayout.astro` — HTML shell with `<head>` and skip-to-content
- `src/layouts/ContentLayout.astro` — BaseLayout + Nav + main + Footer
- `src/components/Nav.astro` — Responsive navigation bar
- `src/components/Footer.astro` — Site footer
- `src/components/WorkflowDiagram.astro` — Visual SDLC pipeline diagram
- `src/pages/index.astro` — Replace placeholder homepage with full homepage

### Component Interfaces (from PDR Section 4)

**BaseLayout** (`src/layouts/BaseLayout.astro`):

```astro
---
interface Props {
  title: string;
  description: string;
}

const { title, description } = Astro.props;

import { siteTitle } from '../config';
import '../styles/global.css';
---

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title} | {siteTitle}</title>
    <meta name="description" content={description} />
    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:type" content="website" />
    <meta property="og:url" content={Astro.url} />
    <meta http-equiv="Content-Security-Policy"
          content="default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; script-src 'self'; font-src 'self';" />
  </head>
  <body>
    <a href="#main-content" class="skip-link">Skip to content</a>
    <slot />
  </body>
</html>
```

**ContentLayout** (`src/layouts/ContentLayout.astro`):

```astro
---
interface Props {
  title: string;
  description: string;
}

const { title, description } = Astro.props;
---

<BaseLayout title={title} description={description}>
  <Nav />
  <main id="main-content">
    <slot />
  </main>
  <Footer />
</BaseLayout>
```

**Nav** (`src/components/Nav.astro`):

- No props. Reads a static page list.
- Navigation items (initial — only Homepage active in this phase):

```typescript
const pages = [
  { href: "/", label: "Home", order: 1 },
  { href: "/workflow/", label: "Workflow", order: 2 },
  { href: "/why/", label: "Why Stages?", order: 3 },
  { href: "/getting-started/", label: "Getting Started", order: 4 },
  { href: "/portfolio/", label: "Portfolio", order: 5 },
  { href: "/artifacts/", label: "Artifacts", order: 6 },
];
```

- Renders `<nav aria-label="Main navigation">`
- Active page detection: compare `Astro.url.pathname` against each href
- Active link gets `aria-current="page"`
- CSS-only hamburger: `<input type="checkbox" id="nav-toggle">` + `<label for="nav-toggle">` pattern

**Footer** (`src/components/Footer.astro`):

- No props. Imports from `src/config.ts`.
- Renders `<footer role="contentinfo">` with:
  - Link to `creatorGithub`
  - Link to `repoUrl` (only if `repoName` is non-empty)
  - Text: `creatorName`

**WorkflowDiagram** (`src/components/WorkflowDiagram.astro`):

- No props. Self-contained.
- Renders `<div role="img" aria-label="SDLC pipeline diagram showing seven stages: Idea, User Requirements, Product Design Review, Phased Release Plan, Finalized Documents, Phase Execution Plans, and Implementation. Two input paths (conversation and document) converge at finalization.">`
- 7 stages as labeled boxes connected by arrows/connectors
- Two input paths shown:
  - Conversation path: `draft-user` → `draft-pdr` → `draft-plan`
  - Document path: `gen-pdr` → `gen-plan`
- Both converge at `finalize` → `expand` → `implement`
- Responsive breakpoints:
  - >= 1024px: horizontal flow (left-to-right)
  - 768px–1023px: may wrap to 2 rows
  - < 768px: vertical stack (top-to-bottom)

### CSS Design Tokens (for global.css)

```css
:root {
  /* Typography */
  --font-body: system-ui, -apple-system, sans-serif;
  --font-mono: ui-monospace, 'Cascadia Code', 'Fira Code', monospace;
  --font-size-base: 1rem;      /* 16px minimum */
  --font-size-lg: 1.25rem;
  --font-size-xl: 1.5rem;
  --font-size-2xl: 2rem;
  --line-height-body: 1.6;

  /* Colors — must maintain >= 4.5:1 contrast on --color-bg */
  --color-text: #1a1a2e;       /* Body text */
  --color-heading: #0f0f1a;    /* Headings */
  --color-link: #1a56db;       /* Links (4.5:1 on white) */
  --color-link-hover: #1e40af;
  --color-bg: #ffffff;
  --color-bg-alt: #f8f9fa;     /* Cards, code blocks */
  --color-border: #e2e8f0;
  --color-accent: #2563eb;     /* CTAs, badges */

  /* Layout */
  --max-width: 72rem;          /* 1152px */
  --content-width: 48rem;      /* 768px */
  --spacing-page: 2rem;

  /* Breakpoints (used in media queries) */
  /* --bp-mobile: 768px */
  /* --bp-desktop: 1024px */
}

.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
  padding: 0.5rem 1rem;
  background: var(--color-accent);
  color: white;
  z-index: 1000;
}
.skip-link:focus {
  top: 0;
}
```

### Content Security Policy (from PDR Section 6)

```
default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; script-src 'self'; font-src 'self';
```

`'unsafe-inline'` on `style-src` is needed for Astro's scoped component styles.

### Design Notes

- **WorkflowDiagram fallback (PDR Risk 1):** If the HTML/CSS diagram cannot render readably at 320px viewport width after implementation, replace with a static SVG. The component's external interface stays the same (`<WorkflowDiagram />` with no props), only the internal implementation changes. Make this decision in task 01.8.
- **CSS-only hamburger (PDR Section 4.3):** The `<input type="checkbox">` pattern allows toggling the mobile nav without JavaScript. The checkbox is visually hidden; the `<label>` renders as the hamburger icon. Adjacent sibling selector (`input:checked ~ .nav-links`) shows/hides the menu. This satisfies NFR-002 (works without JS).
- **Nav page list:** Define nav items as a static array now. All pages are listed from the start (they'll 404 until built). This avoids modifying Nav.astro in every subsequent phase — only task 00.3's placeholder page routing changes.
- **Homepage CTA links:** Three links go to `/workflow/`, `/artifacts/`, `/portfolio/`. These pages don't exist yet and will 404. That's expected — they're built in later phases. The homepage structure is correct from Phase 01 onward.

### Verification

- [ ] `npm run build` exits 0
- [ ] Homepage at `dist/index.html` contains "I2I — From Idea to Implementation" as heading
- [ ] Homepage contains the WorkflowDiagram (7 labeled stages visible in HTML)
- [ ] Homepage contains 3 CTA links pointing to `/workflow/`, `/artifacts/`, `/portfolio/`
- [ ] Skip-to-content link exists and targets `#main-content`
- [ ] `<nav aria-label="Main navigation">` exists with page links
- [ ] Footer contains a link to `github.com/bonjohen`
- [ ] CSP `<meta>` tag is present in `<head>`
- [ ] Open Graph `og:title` and `og:description` meta tags are present
- [ ] WorkflowDiagram renders readably at 320px viewport width (or SVG fallback is in place)
- [ ] WorkflowDiagram renders readably at 768px and 1440px viewport widths
- [ ] Nav collapses to hamburger below 768px viewport width
- [ ] All content readable with JS disabled (no content hidden behind JS toggles except mobile nav which uses CSS)
- [ ] Keyboard tab reaches: skip link → nav links → CTA links → footer links (in order)

## Phase Summary

- **Changes:** Created `src/styles/global.css`, `src/layouts/BaseLayout.astro`, `src/layouts/ContentLayout.astro`, `src/components/Nav.astro`, `src/components/Footer.astro`, `src/components/WorkflowDiagram.astro`. Rebuilt `src/pages/index.astro` using ContentLayout with workflow diagram and 3 CTA cards. All content renders as static HTML with no JS dependency. CSS-only responsive hamburger nav, skip-to-content link, CSP meta tag, Open Graph tags all in place.
- **Commit:** `Phase 01: Homepage and core layout — BaseLayout, Nav, Footer, WorkflowDiagram, ContentLayout`
