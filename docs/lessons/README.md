# Lessons Learned

Reusable patterns and insights extracted from the SDLC prompt pipeline project.

## Architecture & Design

- [Prompt Pipeline as Product](prompt-pipeline-as-product.md) — treating AI prompts as versioned software with I/O contracts and dispatch routing
- [Document Cascade Architecture](document-cascade-architecture.md) — sequential document generation with explicit gap surfacing over silent interpolation
- [Content Collections for Structured Docs](content-collections-for-structured-docs.md) — when schema-validated content collections pay off vs. plain HTML

## Process & Methodology

- [Phased Implementation with Plan-as-State](phased-implementation-with-plan-as-state.md) — using markdown plan tables as the task state machine with timestamp audit trails
- [Draft-to-Final Document Pipeline](draft-to-final-document-pipeline.md) — separating intent capture from quality gates with structured gap analysis between stages
- [Scaffold-First Static Sites](scaffold-first-static-sites.md) — proving deployment works with zero content before investing in features

## Meta

- [Self-Documenting Product via Dogfooding](self-documenting-product-via-dogfooding.md) — building a product's site using the product itself: benefits, risks, and circular-reasoning traps
