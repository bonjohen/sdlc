---
name: "draft-user"
purpose: "Format a conversation into structured user requirements"
input: "Conversation about the product idea, goals, and requirements"
output: "sdlc/docs/draft.user.md — draft user requirements document"
path: "conversation"
sortOrder: 1
---

The `draft-user` command takes an ongoing conversation about a product idea and extracts user requirements into a structured document. It identifies user stories, functional requirements, acceptance criteria, and constraints from the natural-language discussion.

It extracts and structures what was said — it does not invent requirements. User requirements always start from conversation; there is no `gen-user` because requirements must come from a human.
