---
name: "draft-plan"
purpose: "Format a conversation into a structured phased release plan"
input: "Conversation about phasing, priorities, and milestones, plus user requirements and PDR documents"
output: "sdlc/docs/draft.plan.md — draft phased release plan"
path: "conversation"
sortOrder: 3
---

The `draft-plan` command takes a conversation where planning decisions have been discussed — phase boundaries, risk ordering, priorities, milestones — and formats it into a structured phased release plan with task tables.

The alternative document path is `gen-plan`, which generates a plan directly from the PDR document without requiring conversation input.
