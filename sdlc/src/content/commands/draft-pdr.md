---
name: "draft-pdr"
purpose: "Format a conversation into a structured Product Design Review"
input: "Conversation about architecture, components, data models, and implementation approach, plus the user requirements document"
output: "sdlc/docs/draft.pdr.md — draft Product Design Review"
path: "conversation"
sortOrder: 2
---

The `draft-pdr` command takes a conversation where architecture and design decisions have been discussed and formats it into a structured Product Design Review. It extracts component interfaces, data models, dependency choices, and platform decisions from the discussion.

Like `draft-user`, it extracts rather than invents. The alternative document path is `gen-pdr`, which generates a PDR directly from the user requirements document without requiring conversation input.
