---
name: "gen-pdr"
purpose: "Generate a Product Design Review from user requirements documents"
input: "sdlc/docs/final.user.md or sdlc/docs/draft.user.md — the user requirements document"
output: "sdlc/docs/draft.pdr.md — draft Product Design Review"
path: "document"
sortOrder: 4
---

The `gen-pdr` command reads a user requirements document and designs the physical system that satisfies it. It makes design decisions — choosing components, defining data models, identifying risks — based on what the requirements ask for and what good engineering practice demands.

This is the fast-path alternative to `draft-pdr`. Instead of formatting conversation content, it generates design decisions directly from the requirements document.
