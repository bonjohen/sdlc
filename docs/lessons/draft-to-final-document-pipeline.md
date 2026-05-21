# Draft-to-Final Document Pipeline

## The Lesson

Separating document generation into explicit draft and final stages — with a structured gap analysis between them — forces quality gates that prevent the common failure mode of AI-generated documents: looking complete while silently missing critical requirements. The draft captures intent; the finalization adds rigor.

## Context

An AI-driven SDLC pipeline generates three documents: user requirements, PDR, and implementation plan. Each document goes through a draft stage (capturing the user's intent from conversation or auto-generation) and a finalization stage (running gap checklists, adding traceability IDs, and ensuring cross-document consistency). The finalization is a single prompt (`finalize.md`) that processes all three drafts sequentially, with each finalized output feeding the next.

## What Happened

1. Initial pipeline had no draft/final distinction — prompts produced "the document" directly. Results looked polished but frequently missed non-functional requirements, error handling scenarios, and edge cases.
2. Introduced a draft stage focused purely on capturing what the user said or what the generator inferred. Drafts are explicitly allowed to be incomplete.
3. Added a finalization step with a 50-item gap checklist organized by category: personas, functional requirements, non-functional requirements, security, accessibility, error handling, data model completeness.
4. The finalizer processes drafts sequentially: `draft.user.md` → `final.user.md` → (feeds into) → `draft.pdr.md` → `final.pdr.md` → (feeds into) → `draft.plan.md` → `final.plan.md`.
5. Added traceability during finalization: user stories get `US-NNN` IDs, NFRs get `NFR-NNN`, PDR sections reference story IDs, plan tasks reference PDR sections.
6. In the I2I project, finalization caught: missing accessibility NFR (no WCAG mention in drafts), no mobile breakpoint strategy, no error page design, and no SEO metadata requirements. All were added to finals without changing the user's stated intent.

## Key Insights

- **Drafts give humans a checkpoint without forcing completeness.** A draft that says "this is what I understood from our conversation" lets the user verify intent before the system adds engineering rigor. Without this checkpoint, users discover misunderstandings only when looking at generated code.
- **Gap checklists outperform open-ended "find what's missing."** Asking an AI "what's missing from this document?" produces generic suggestions. A structured checklist of 50 specific items (pagination? bulk ops? audit trail? rate limiting?) catches real gaps because it's testing against a known taxonomy of common omissions.
- **Sequential finalization with cross-feeding prevents consistency drift.** Processing user → PDR → plan in sequence means the plan can't reference PDR sections that don't exist, and the PDR can't claim to implement stories that aren't in the user doc. Parallel finalization would let documents diverge.
- **Traceability IDs are cheap to add and expensive to retrofit.** Adding `US-001` through `US-020` during finalization takes seconds. Trying to add them after implementation (to audit coverage) requires re-reading every requirement and mapping to code — a multi-hour task.
- **"Extract, don't invent" is the draft discipline; "surface, don't assume" is the finalization discipline.** These complementary rules prevent both stages from silently adding requirements. Drafts extract from conversation; finals flag gaps and ask rather than fill.

## Examples

**Good finalization (surfaces gap, doesn't fill it):**
```markdown
### Gaps Found in draft.user.md

1. **CRITICAL: No accessibility requirements stated.**
   Added NFR-005: WCAG 2.1 AA compliance for all pages.
   Rationale: Public-facing site, legal and ethical baseline.

2. **MODERATE: No mobile breakpoint strategy.**
   Added NFR-003: Responsive layout, mobile-first.
   Rationale: PDR specifies CSS custom properties; breakpoints
   are an implementation detail but need a stated target.
```

**Bad finalization (silently invents):**
```markdown
## User Management
Users can create accounts, reset passwords, and manage profiles...
```
(Nobody asked for user management. This is invention, not gap-filling.)

## Applicability

This pattern applies to any document generation where quality matters more than speed: specifications, contracts, technical designs, grant proposals, compliance documentation. The two-stage approach adds latency but catches errors that are expensive to fix downstream.

It does NOT apply to: ephemeral content (chat messages, quick notes), creative writing (where "gaps" are subjective), or documents with rapid iteration cycles where the draft/final distinction would be bureaucratic overhead.

## Related Lessons

- [Document Cascade Architecture](document-cascade-architecture.md) — the cascade is the ordering constraint that the draft/final pipeline operates within
- [Prompt Pipeline as Product](prompt-pipeline-as-product.md) — the pipeline that implements this draft/final separation
