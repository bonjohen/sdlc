# Scaffold-First Static Sites

## The Lesson

When building a static site, the first phase should prove the deployment pipeline works — config system, build command, CI/CD, and hosting — with zero real content. This eliminates deployment uncertainty before any content investment, and means every subsequent phase can be verified end-to-end immediately.

## Context

A marketing/documentation site ("I2I") was built as a 6-phase Astro project deployed to GitHub Pages. The site would eventually have 8 pages with components, content collections, and interactive diagrams. The project was executed by an AI agent following a phased release plan, with one commit per phase. The risk: investing 4 phases of content work before discovering the GitHub Pages deployment config was broken.

## What Happened

1. Phase 00 was explicitly scoped to "scaffold only" — no real content. The goal statement: "The Astro project builds, deploys to GitHub Pages, and the configuration variable system works."
2. Created: `package.json` (Astro + sharp), `astro.config.mjs` (with `site` and `base` settings), `tsconfig.json`, `src/config.ts` (6 site-wide variables), a minimal `index.astro` (renders site title + one link from config), and `.github/workflows/deploy.yml`.
3. Verified the build: `npm run build` produces static HTML with no server dependencies. Verified config propagation: changing `repoName` in `config.ts` updates the link on rebuild.
4. Tested the `base` path configuration with both `"/"` and `"/test-repo"` to ensure asset paths resolve correctly in both cases (a known Astro/GitHub Pages gotcha).
5. Marked the deploy-to-Pages task as Blocked (no remote repo yet) — but every other deployment prerequisite was proven. When the remote is eventually configured, deployment is a single push away.
6. Phases 01–04 then built on a known-good foundation. No phase ever had to debug a build or deployment issue — only content and component bugs.

## Key Insights

- **Deployment uncertainty is the highest-risk unknown in early phases.** Build tools, hosting platforms, and CI/CD configurations have sharp edges that are impossible to predict from documentation alone. Proving them first (with minimal content) means failures are cheap and localized.
- **A config system in the scaffold enables testing without content.** The `src/config.ts` with 6 variables let Phase 00 verify that data flows from config → template → HTML without writing any real pages. This is the static-site equivalent of a "hello world" that exercises the framework.
- **Base path testing catches the most common static-site deployment bug.** Sites that work at `localhost:4321/` but break at `username.github.io/repo-name/` are the #1 deployment failure mode for GitHub Pages + framework combinations. Testing both paths in Phase 00 eliminates this entire class of bug.
- **Blocked tasks are better than skipped tasks.** Marking deploy as "Blocked" with a note preserves the intent and preconditions. If it had been silently omitted, a future developer might not know whether deployment was untested or deliberately deferred.
- **Zero-content phases build in minutes, not hours.** Phase 00 took 7 minutes (6 tasks, 3:45 PM to 3:52 PM). That's the cost of eliminating deployment risk. Phases with real content (01–04) took significantly longer. Front-loading the cheap validation is pure upside.

## Examples

**Good Phase 00 scope:**
```
- Initialize framework ✓
- Config system ✓
- Placeholder page (uses config) ✓
- CI/CD workflow ✓
- Build verification ✓
- Path configuration test ✓
- Deploy verification (blocked — no remote)
```

**Bad Phase 00 scope (too much):**
```
- Initialize framework ✓
- Config system ✓
- Build navigation component  ← content work, belongs in phase 01+
- Write homepage copy  ← content work
- Set up content collections  ← architecture work for phase 02+
```

## Applicability

This pattern applies to any project deployed to a hosting platform: static sites, SPAs, serverless functions, containerized services. The principle is "prove deployment works before investing in features."

It does NOT apply to: local-only tools (no deployment to prove), libraries published to package registries (the "deployment" is `npm publish` which is trivially testable), or projects adding to an already-deployed site (deployment is already proven).

## Related Lessons

- [Phased Implementation with Plan-as-State](phased-implementation-with-plan-as-state.md) — the phased structure that makes scaffold-first natural
- [Self-Documenting Product via Dogfooding](self-documenting-product-via-dogfooding.md) — the scaffold was the first phase of the dogfooding exercise
