---
title: "Self-Documenting Product via Dogfooding"
summary: "Building a product's site using the product itself: benefits, risks, and circular-reasoning traps."
category: "meta"
sortOrder: 7
---

## The Lesson

Building a product's documentation or marketing site *using the product itself* simultaneously validates the tool, generates authentic example artifacts, and exposes UX friction — but requires discipline to avoid circular reasoning where the product's limitations shape its own requirements.

## Context

A developer built an AI-assisted SDLC pipeline (prompt-driven requirements, design, planning, and implementation). To explain and market the pipeline, they decided to build the marketing website ("I2I — From Idea to Implementation") using the pipeline itself. The website would explain the 8-step workflow while being produced by that exact workflow.

## What Happened

1. Wrote user requirements for the I2I website by having a conversation about what the site should do — this was the `draft-user` step of the pipeline applied to its own marketing.
2. Generated the PDR from those requirements using `gen-pdr` — the pipeline decided on Astro, content collections, and GitHub Pages based on the stated constraints.
3. Generated the release plan from the PDR using `gen-plan` — the pipeline produced 6 phases from scaffold through polish.
4. Finalized all three documents, catching gaps (missing accessibility NFRs, no SEO strategy, no mobile breakpoints).
5. Expanded into per-phase execution plans with full implementation context.
6. Executed phases 00-04, producing working code at each step. The site itself contains examples of pipeline output (generated plan tables, prompt excerpts) as content.
7. The dogfooding revealed that the `expand` prompt needed more context about existing code patterns — phases 02+ had to reference components built in phase 01 but the prompt didn't explicitly support "look at what exists."

## Key Insights

- **Dogfooding generates authentic artifacts.** The I2I site's "Artifacts" page shows real pipeline output because the output *is* real — it was used to build the site. This is more convincing than fabricated examples and costs nothing extra to produce.
- **Friction discovered during dogfooding is high-signal.** When the pipeline struggled to reference previously-built components during later phases, that was a real usability gap — not a hypothetical.
- **Circular reasoning is the main risk.** If the pipeline can't express a requirement, and you're using the pipeline to define the product, that requirement might never surface. The mitigation is: start with external requirements (what do users need?) not internal ones (what can the pipeline produce?).
- **The "works for me" trap is real.** A single developer dogfooding their own tool has deep familiarity that masks onboarding friction.
- **Phased execution is the safest dogfooding structure.** Each phase produces a shippable increment, so if the pipeline breaks at phase 3, you still have phases 0-2 working.

## Applicability

This pattern applies when your product produces artifacts that can be used in its own development or documentation: code generators, design systems, documentation tools, template engines, CI/CD pipelines.

It does NOT apply when the product and its documentation are in fundamentally different domains (e.g., a database engine doesn't write its own docs using SQL queries).
