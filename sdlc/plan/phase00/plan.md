---
phase: 00
title: "Project Scaffold and Deployment Pipeline"
depends_on: "none"
goal: "The Astro project builds, deploys to GitHub Pages, and the configuration variable system works. No real content yet — just proof that the pipeline is operational."
source_pdr_sections: ["1.2", "1.3", "3"]
source_user_stories: ["US-020"]
status: "completed"
---

# Phase 00: Project Scaffold and Deployment Pipeline

## Tasks

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 00.1 | Completed | 2026-05-21 03:45 PM | 2026-05-21 03:48 PM | Initialize Astro project with static output adapter and TypeScript config. Install `astro` and `sharp`. Create `astro.config.mjs` with `site` and `base` settings (PDR Section 1.3). |
| 00.2 | Completed | 2026-05-21 03:48 PM | 2026-05-21 03:49 PM | Create `src/config.ts` with `repoName`, `repoUrl`, `creatorName`, `creatorGithub`, `siteTitle`, and `siteDescription` variables (PDR Section 1.3). |
| 00.3 | Completed | 2026-05-21 03:49 PM | 2026-05-21 03:49 PM | Create minimal placeholder homepage at `src/pages/index.astro` that renders the site title, one paragraph, and a link generated from `src/config.ts` to verify config propagation. |
| 00.4 | Completed | 2026-05-21 03:50 PM | 2026-05-21 03:50 PM | Create GitHub Actions workflow at `.github/workflows/deploy.yml` for building Astro and deploying to GitHub Pages on push to main (PDR Section 1.2, NFR-008). |
| 00.5 | Completed | 2026-05-21 03:50 PM | 2026-05-21 03:51 PM | Test `base` path configuration: verify build succeeds with `base: "/"` and with `base: "/test-repo"`. Verify internal links and asset paths resolve correctly in both cases (PDR Risk 3). |
| 00.6 | Completed | 2026-05-21 03:51 PM | 2026-05-21 03:52 PM | Verify `npm run build` produces a directory of static HTML with no server-side dependencies (PDR-AC-001). Verify changing `repoName` and rebuilding updates the GitHub link on the placeholder page (PDR-AC-003). |
| 00.7 | Blocked | 2026-05-21 03:52 PM | | Deploy to GitHub Pages and verify the site is accessible at the expected URL (PDR-AC-002). [BLOCKED: No GitHub remote repository configured yet; deployment requires push to a remote repo with GitHub Pages enabled] |

## Context

### Files to Create or Modify

- `package.json` — Astro project manifest with `astro`, `sharp` dependencies and `dev`, `build`, `preview` scripts
- `astro.config.mjs` — Astro configuration with `site`, `base`, and static output mode
- `tsconfig.json` — TypeScript config extending Astro's default (`"extends": "astro/tsconfigs/strict"`)
- `src/config.ts` — Site-wide configuration variables
- `src/pages/index.astro` — Minimal placeholder homepage
- `.github/workflows/deploy.yml` — GitHub Actions workflow for Pages deployment

### Configuration Variables (from PDR Section 1.3)

`src/config.ts` must export these variables:

```typescript
// Site configuration — update these values as the project evolves
export const repoName = "";  // Fill when repository name is chosen
export const repoUrl = repoName
  ? `https://github.com/bonjohen/${repoName}`
  : "https://github.com/bonjohen";
export const creatorName = "John Boen";
export const creatorGithub = "https://github.com/bonjohen";
export const siteTitle = "I2I — From Idea to Implementation";
export const siteDescription = "A prompt-driven SDLC workflow from idea to implementation";
```

`astro.config.mjs` configuration:

```javascript
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://bonjohen.github.io',
  base: '/',  // Update to '/{repo-name}' when repository name is chosen
});
```

### Key Patterns and Imports

Astro project initialization command:

```bash
npm create astro@latest -- --template minimal --typescript strict
```

This creates the minimal Astro project with TypeScript. After initialization, install sharp:

```bash
npm install sharp
```

Astro page file structure (`.astro` files use frontmatter + template):

```astro
---
// Component script (runs at build time)
import { siteTitle, repoUrl } from '../config';
---

<!-- Component template (rendered to HTML) -->
<html>
  <head><title>{siteTitle}</title></head>
  <body>
    <h1>{siteTitle}</h1>
    <a href={repoUrl}>GitHub</a>
  </body>
</html>
```

### GitHub Actions Workflow

The deploy workflow must:
1. Trigger on push to `main`
2. Install Node.js and npm dependencies
3. Run `astro build`
4. Deploy the `dist/` directory to GitHub Pages

Standard Astro GitHub Pages workflow structure:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
      - name: Install dependencies
        run: npm ci
      - name: Build
        run: npm run build
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### Design Notes

- **Base path testing (task 00.5):** The `base` config in `astro.config.mjs` prepends a path to all internal links and asset URLs. When `base: "/"`, the site works at the root (`bonjohen.github.io`). When `base: "/repo-name"`, it works as a project site (`bonjohen.github.io/repo-name`). Test both to ensure links don't break. Astro handles this automatically for internal navigation but verify it for any href values constructed manually in templates.
- **Static output adapter:** Astro 5.x defaults to static output. No adapter package is needed unless switching to SSR later. Verify this by checking that `dist/` contains only `.html`, `.css`, `.js`, and asset files — no `_worker.js`, no `package.json`, no server code.
- **Repo name empty state:** When `repoName` is empty string, `repoUrl` falls back to the profile URL (`github.com/bonjohen`). Templates using `repoUrl` should handle this gracefully — either show the profile link or hide the repo-specific link.

### Verification

- [ ] `npm run build` exits 0 and produces `dist/` directory containing `.html` files
- [ ] `dist/` contains no server-side code (no `_worker.js`, no `server/` directory, no `package.json`)
- [ ] `dist/index.html` contains the text "I2I" and a link to `github.com/bonjohen`
- [ ] Build succeeds with `base: "/"` in `astro.config.mjs`
- [ ] Build succeeds with `base: "/test-repo"` in `astro.config.mjs`
- [ ] Changing `repoName` in `src/config.ts` to `"test-repo"` and rebuilding produces a link to `github.com/bonjohen/test-repo` in `dist/index.html`
- [ ] `.github/workflows/deploy.yml` exists and is valid YAML
- [ ] GitHub Pages deployment succeeds (site accessible at expected URL)

## Phase Summary

- **Changes:** Created `package.json`, `astro.config.mjs`, `tsconfig.json`, `src/config.ts`, `src/pages/index.astro`, `.github/workflows/deploy.yml`. Verified static build produces only HTML (no server code). Verified `base` path works with both `/` and `/test-repo`. Verified `repoName` config propagation to built output.
- **Blocked tasks:** 00.7 — no GitHub remote repository configured yet; deployment verification deferred.
- **Commit:** `Phase 00: Project scaffold — Astro init, config system, GitHub Actions workflow`
