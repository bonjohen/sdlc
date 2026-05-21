---
name: "finalize"
purpose: "Convert three draft documents into three finalized documents with gap analysis"
input: "sdlc/docs/draft.user.md, sdlc/docs/draft.pdr.md, sdlc/docs/draft.plan.md"
output: "sdlc/docs/final.user.md, sdlc/docs/final.pdr.md, sdlc/docs/final.plan.md"
path: "document"
sortOrder: 6
---

The `finalize` command processes all three draft documents in strict sequence: user requirements, then PDR, then plan. Each finalized document feeds into the next — the final user requirements inform the final PDR, which informs the final plan.

It fills gaps the draft author missed without rewriting their vision. It performs gap analysis, adds traceability IDs (US-NNN, NFR-NNN), and flags any critical issues found. The result is three buildable, internally consistent documents.
