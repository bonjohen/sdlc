---
title: "Draft-to-Final Document Pipeline"
summary: "Separating intent capture from quality gates with structured gap analysis between stages."
category: "process"
sortOrder: 5
---

## The Lesson

Separating document generation into explicit draft and final stages — with a structured gap analysis between them — forces quality gates that prevent the common failure mode of AI-generated documents: looking complete while silently missing critical requirements. The draft captures intent; the finalization adds rigor.

## Context

An AI-driven SDLC pipeline generates three documents: user requirements, PDR, and implementation plan. Each document goes through a draft stage (capturing the user's intent from conversation or auto-generation) and a finalization stage (running gap checklists, adding traceability IDs, and ensuring cross-document consistency). The finalization is a single prompt (`finalize.md`) that processes all three drafts sequentially, with each finalized output feeding the next.

## What Happened

1. Initial pipeline had no draft/final distinction — prompts produced "the document" directly. Results looked polished but frequently missed non-functional requirements, error handling scenarios, and edge cases.
2. Introduced a draft stage focused purely on capturing what the user said or what the generator inferred. Drafts are explicitly allowed to be incomplete.
3. Added a finalization step with a 50-item gap checklist organized by category: personas, functional requirements, non-functional requirements, security, accessibility, error handling, data model completeness.
4. The finalizer processes drafts sequentially: `draft.user.md` -> `final.user.md` -> (feeds into) -> `draft.pdr.md` -> `final.pdr.md` -> (feeds into) -> `draft.plan.md` -> `final.plan.md`.
5. Added traceability during finalization: user stories get `US-NNN` IDs, NFRs get `NFR-NNN`, PDR sections reference story IDs, plan tasks reference PDR sections.
6. In the I2I project, finalization caught: missing accessibility NFR, no mobile breakpoint strategy, no error page design, and no SEO metadata requirements. All were added to finals without changing the user's stated intent.

## Key Insights

- **Drafts give humans a checkpoint without forcing completeness.** A draft that says "this is what I understood from our conversation" lets the user verify intent before the system adds engineering rigor.
- **Gap checklists outperform open-ended "find what's missing."** A structured checklist of 50 specific items catches real gaps because it's testing against a known taxonomy of common omissions.
- **Sequential finalization with cross-feeding prevents consistency drift.** Processing user -> PDR -> plan in sequence means the plan can't reference PDR sections that don't exist.
- **Traceability IDs are cheap to add and expensive to retrofit.** Adding `US-001` through `US-020` during finalization takes seconds. Trying to add them after implementation costs hours.
- **"Extract, don't invent" is the draft discipline; "surface, don't assume" is the finalization discipline.** These complementary rules prevent both stages from silently adding requirements.

## Applicability

This pattern applies to any document generation where quality matters more than speed: specifications, contracts, technical designs, grant proposals, compliance documentation.

It does NOT apply to: ephemeral content, creative writing (where "gaps" are subjective), or documents with rapid iteration cycles where the draft/final distinction would be bureaucratic overhead.
