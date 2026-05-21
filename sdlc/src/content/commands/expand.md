---
name: "expand"
purpose: "Generate self-contained phase execution plans from finalized documents"
input: "sdlc/docs/final.plan.md, sdlc/docs/final.pdr.md, sdlc/docs/final.user.md"
output: "sdlc/plan/phase{NN}/plan.md — one file per phase"
path: "document"
sortOrder: 7
---

The `expand` command reads the finalized plan, PDR, and user requirements, then produces one standalone plan file per phase. Each phase plan contains everything an implementer needs — task tables, relevant schema, import paths, design notes, and verification criteria — without re-reading the full PDR.

This is the bridge between finalized documentation and implementation. It runs once after `finalize` and before `implement`.
