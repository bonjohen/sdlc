---
phase: 05
title: "Polish, Accessibility, SEO, and Custom Domain Readiness"
depends_on: "Phase 04"
goal: "The site is production-ready for public sharing. All SEO metadata in place, accessibility audit passes, custom domain config verified, and content accuracy confirmed. This completes the First Full Feature Release."
source_pdr_sections: ["1.2", "5", "6", "7", "8", "11", "14"]
source_user_stories: ["NFR-001", "NFR-003", "NFR-004", "NFR-005", "NFR-006", "NFR-010"]
status: "open"
---

# Phase 05: Polish, Accessibility, SEO, and Custom Domain Readiness

## Tasks

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

## Context

### Files to Create or Modify

- `src/pages/404.astro` — Custom 404 page
- `astro.config.mjs` — Add `@astrojs/sitemap` integration; optionally configure link checking
- `package.json` — Add `@astrojs/sitemap` dependency
- `public/CNAME` — Custom domain file (contains `johnboen.com`)
- `src/layouts/BaseLayout.astro` — Verify/fix OG tags and meta descriptions
- `src/content/commands/*.md` — Fix any content drift found in review
- `src/content/artifacts/*.md` — Fix any content drift found in review
- Various page/component files — Fix accessibility and responsive issues found in audits

### 404 Page Structure

`src/pages/404.astro`:

```astro
---
import ContentLayout from '../layouts/ContentLayout.astro';
---

<ContentLayout title="Page Not Found" description="The requested page does not exist.">
  <h1>Page Not Found</h1>
  <p>The page you're looking for doesn't exist or has been moved.</p>
  <p><a href="/">Return to the homepage</a></p>
</ContentLayout>
```

The 404 page uses the same ContentLayout as all other pages, giving visitors access to the full navigation and footer. GitHub Pages automatically serves `404.html` for unmatched routes.

### Sitemap Integration

Install and configure `@astrojs/sitemap`:

```bash
npm install @astrojs/sitemap
```

Update `astro.config.mjs`:

```javascript
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://bonjohen.github.io',
  base: '/',
  integrations: [sitemap()],
});
```

After build, verify `dist/sitemap-index.xml` and `dist/sitemap-0.xml` exist and include all 6 public pages (404 should be excluded from sitemap).

### Open Graph Tags Checklist

Every page rendered through BaseLayout should have these in `<head>`:

```html
<title>{pageTitle} | I2I — From Idea to Implementation</title>
<meta name="description" content="{page-specific description}" />
<meta property="og:title" content="{pageTitle}" />
<meta property="og:description" content="{page-specific description}" />
<meta property="og:type" content="website" />
<meta property="og:url" content="{canonical URL for this page}" />
```

Each page must have a UNIQUE `title` and `description`. Verify no two pages share the same values.

| Page | Expected Title Prefix | Expected Description (theme) |
|------|-----------------------|------------------------------|
| Homepage | "I2I — From Idea to Implementation" | Prompt-driven SDLC workflow overview |
| Workflow | "The SDLC Pipeline" | All 8 commands and 3 workflow paths explained |
| Education | "Why Stages?" | Rationale for staged document production |
| Getting Started | "Getting Started" | Command sequences to adopt the workflow |
| Portfolio | "About This Project" | Case study of AI workflow design skills |
| Artifacts | "Example Artifacts" | Real prompts and generated documents |
| 404 | "Page Not Found" | Requested page doesn't exist |

### Custom Domain Configuration (from PDR Section 11, NFR-010)

`public/CNAME` contains a single line:

```
johnboen.com
```

When CNAME is present and the domain DNS points to GitHub Pages:
- The `site` in `astro.config.mjs` should be `https://johnboen.com`
- The `base` should be `/` (root domain, no project path)
- All internal links should still work (they use relative paths via Astro)

For this task, verify that:
1. Adding the CNAME file doesn't break the build
2. Changing `site` to `https://johnboen.com` and `base` to `/` still produces valid internal links
3. The sitemap uses the correct domain

After verification, revert to the GitHub Pages configuration (`bonjohen.github.io`) since DNS is not yet configured. The CNAME file can remain in `public/` ready for when DNS is set up, OR be removed and added later — either is acceptable.

### Lighthouse Accessibility Audit

Run Lighthouse CLI on each built page:

```bash
npx lighthouse http://localhost:4321/ --only-categories=accessibility --output=json
```

Or use Chrome DevTools Lighthouse panel on the local dev server.

Target: Accessibility score >= 90 on ALL pages.

Common issues to check and fix:
- Missing `alt` attributes on images (if any images were added)
- Insufficient color contrast (check badges, code blocks, subtle text)
- Missing form labels (hamburger nav checkbox needs an accessible label)
- Heading hierarchy violations (`<h1>` → `<h3>` without `<h2>` between)
- Missing landmark roles (should already be correct from Phase 01 semantic HTML)
- Focus indicators missing on interactive elements (links, nav toggle)
- Missing `lang` attribute on `<html>` (should be set in BaseLayout)

### Responsive Testing Checklist

Test each page at these viewport widths:

| Width | Classification | Key Checks |
|-------|---------------|------------|
| 320px | Small mobile | All content visible, no horizontal overflow, nav is hamburger, WorkflowDiagram stacks vertically |
| 768px | Tablet | Nav may transition between hamburger and inline, content width is comfortable |
| 1440px | Desktop | Full horizontal layout, content doesn't stretch too wide (max-width constraint) |
| 2560px | Large monitor | Content stays centered, doesn't stretch to extreme widths, no layout breaks |

### Link Validation

Astro does not have built-in broken link detection by default. Options:

1. **Build-time:** Configure Astro's build to warn on broken internal links (check Astro 5.x docs for `build.format` and link checking options)
2. **Post-build:** Use a link checker on the built output:
   ```bash
   npx linkinator ./dist --recurse --skip "^(?!file://)"
   ```
3. **CI integration:** Add link checking as a step after build in the GitHub Actions workflow

The goal is that broken internal links are caught before deployment — whether at build time or in CI.

### Design Notes

- **Task ordering matters:** Tasks 05.1–05.4 create new assets and configure tooling. Tasks 05.5–05.8 audit the final state. Task 05.9 tests domain readiness. Task 05.10 reviews content accuracy. Running audits (05.5–05.8) after all asset creation is complete ensures audit results reflect the final state.
- **Lighthouse scores are not pass/fail on first try:** Expect iterative improvement. Run the audit (05.7), find issues, fix them (05.8), re-run to verify. The >= 90 target is the FINAL score after fixes.
- **CNAME and base path interaction (PDR Risk 3):** When serving from a custom domain (root, not a project subdirectory), `base` must be `/`. When serving from `bonjohen.github.io/{repo}`, `base` must be `/{repo}`. These are different deployment configs. Verify BOTH work. In practice, only one will be active at a time.
- **Content review (05.10) is defensive:** The SDLC prompt files in `skill/` may have been updated during the project. The command descriptions and artifact examples in the site must match the current state of those files. This is a quick read-and-compare task, not a rewrite.

### Verification

- [ ] `npm run build` exits 0
- [ ] `dist/404.html` exists with navigation, footer, and link to homepage
- [ ] `dist/sitemap-index.xml` (or `dist/sitemap-0.xml`) exists and lists all 6 public pages
- [ ] Sitemap does NOT include the 404 page
- [ ] Every page has a unique `<title>` tag
- [ ] Every page has a unique `<meta name="description">` tag
- [ ] Every page has `og:title`, `og:description`, `og:type`, `og:url` meta tags
- [ ] No broken internal links in built output (link checker passes)
- [ ] All 7 pages render without horizontal overflow at 320px viewport width
- [ ] All 7 pages render correctly at 768px, 1440px, and 2560px viewport widths
- [ ] All 7 pages are fully readable with JavaScript disabled
- [ ] Lighthouse accessibility score >= 90 on all 7 pages
- [ ] Build succeeds with CNAME file in `public/`
- [ ] Build succeeds with `site: 'https://johnboen.com'` and `base: '/'`
- [ ] All command descriptions in `src/content/commands/` match current `skill/*.md` files
- [ ] All artifact examples in `src/content/artifacts/` match their source files
- [ ] PDR-AC-007 satisfied (Lighthouse >= 90)
- [ ] PDR-AC-008 satisfied (CNAME + DNS is sufficient for custom domain)

## Phase Summary

_To be filled after completion._

- **Changes:** TBD
- **Commit:** TBD
