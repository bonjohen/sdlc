---
title: "Document Cascade Architecture"
summary: "Sequential document generation with explicit gap surfacing over silent interpolation."
category: "architecture"
sortOrder: 2
---

## The Lesson

When generating a sequence of interdependent documents, process them in strict order where each output feeds the next — and require every stage to surface gaps in its input explicitly rather than silently filling them. Silent interpolation compounds errors; explicit gap warnings let humans intervene at the cheapest possible moment.

## Context

An SDLC pipeline produces three documents in sequence: user requirements, product design review (PDR), and implementation plan. Each document depends on the one before it. The finalization step processes all three drafts sequentially — each finalized document becomes input to the next. A gap in the user requirements (e.g., missing pagination story) cascades into a PDR without pagination design, which cascades into a plan without pagination tasks. The pipeline needed to handle these gaps without inventing requirements the user never stated.

## What Happened

1. Early versions of the pipeline let each stage independently interpret the source material. The PDR would infer requirements not in the user doc; the plan would add tasks not in the PDR. Output quality was unpredictable.
2. Added a strict ordering constraint: `final.user.md` must exist before `final.pdr.md` is produced; `final.pdr.md` must exist before `final.plan.md`. No parallelization.
3. Added explicit gap-surfacing requirements: every finalization step runs a checklist of commonly-missed items (personas, NFRs, error handling, pagination, audit trails) and must emit warnings for anything missing — not silently add it.
4. Introduced a traceability chain: user stories get `US-NNN` IDs, the PDR references those IDs, and plan tasks reference PDR sections. If the chain breaks, the gap is visible.
5. The cascade caught a missing accessibility NFR in the user requirements, which propagated a warning through PDR and plan rather than silently producing inaccessible implementation tasks.

## Key Insights

- **Sequential processing with explicit dependencies prevents hallucinated requirements.** When the PDR can only reference what's in `final.user.md`, it can't invent features. When it spots a gap, it warns rather than fills — giving the human a chance to decide.
- **Gap checklists are more reliable than free-form "check for completeness."** A structured checklist of 20 common omissions (pagination, bulk ops, audit trail, error recovery) catches more gaps than asking an AI to "identify what's missing." The checklist encodes domain knowledge about what drafts typically forget.
- **Traceability IDs make broken chains visible.** When every plan task must cite a PDR section and every PDR section must cite a user story, orphaned tasks and unsupported features become structurally detectable — not just a matter of careful reading.
- **The cheapest place to fix a gap is where it's first detected.** A missing NFR caught during finalization costs one sentence to add. The same gap discovered during implementation costs a redesign. Surfacing gaps early is the cascade's primary value.

## Applicability

This pattern applies to any multi-document generation pipeline where later documents depend on earlier ones — technical specifications, legal document suites, grant applications with multiple sections, curriculum design.

It does NOT apply when documents are genuinely independent (e.g., generating 10 blog posts from 10 topics — no cascade relationship exists).
