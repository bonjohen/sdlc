---
name: "gen-plan"
purpose: "Generate a phased release plan from a Product Design Review"
input: "sdlc/docs/final.pdr.md or sdlc/docs/draft.pdr.md — the PDR document, plus user requirements for context"
output: "sdlc/docs/draft.plan.md — draft phased release plan"
path: "document"
sortOrder: 5
---

The `gen-plan` command reads a Product Design Review and decomposes it into a risk-ordered phased release plan. It makes planning decisions — choosing phase boundaries, ordering by risk and dependency, defining per-phase scope — based on the design and what good engineering sequencing demands.

This is the fast-path alternative to `draft-plan`. It generates planning decisions directly from the PDR document without requiring conversation.
