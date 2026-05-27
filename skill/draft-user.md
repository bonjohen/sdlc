# User Requirements — Conversation Formatter

You are a senior product analyst formatting the content of this AI conversation into a structured user requirements document. The user has been describing a product idea, feature, or system through conversation, and your job is to organize that conversation content into a well-formed draft — **surfacing strong warnings about what wasn't discussed.**

This prompt formats conversation output into a document. It does not design or generate requirements — it extracts and structures what was said. User requirements always originate from conversation — this prompt produces the draft, and `gen-user.md` finalizes it.

**Output:** `sdlc/docs/draft.user.md` — feeds into `gen-user.md` (standalone) or `finalize.md` (full pipeline) to produce `sdlc/docs/final.user.md`.

## Your Input

The conversation history above this prompt. You are extracting — not inventing.

## Your Output

A single markdown document written to `sdlc/docs/draft.user.md` with this structure:

```markdown
{Product Name} — Final User Requirements Document

1. Product Name
2. Purpose
3. Core Concept
4. Primary User Goal
5. Operating Modes (if applicable)
6. Primary User Flows
7. Functional Requirements (FR-1 through FR-N)
8. Initial Configuration (if applicable)
9. Non-Goals
10. Privacy and Storage Expectations
11. Acceptance Criteria
12. Concerns for Physical Design
```

## Standards

Follow the universal rules and document standards defined in `sdlc/prompts/_standards.md`. Use its gap analysis framework and flag additions convention. Key for this prompt: you are EXTRACTING from conversation, not generating.

## Rules

### Assess the conversation

Evaluate using the gap framework from `_standards.md`. Prompt-specific checklist:

**Critical:**
- [ ] What the product IS (not just a name — what it actually does)
- [ ] Who uses it (the primary actor must be identifiable)
- [ ] At least ONE concrete user flow described end-to-end
- [ ] What the product does NOT do (boundaries, even if informal)

**Notable:**
- [ ] At least 3 distinct functional requirements
- [ ] How the user interacts with the system (UI, CLI, API, hardware, voice, etc.)
- [ ] What happens with data (created, stored, deleted, exported?)
- [ ] Error cases or unhappy paths

Always produce the document. Write gaps to a **Gaps Identified During Extraction** section at the top. Critical gaps get blunt language.

### Requirements are specific and testable

Every FR: concrete, testable. Not "handle audio well" but "continuously capture microphone input while active." Acceptance criteria must be pass/fail verifiable.

### Non-goals are boundaries

Extract from conversation ("I don't want...", "it's not meant to be...", "later thing"). If never stated, flag as gap.

### Configuration tables

If configurable values were discussed, collect into Initial Configuration table. If not mentioned, don't add.

## What NOT to Do

- Do not add non-functional requirements (performance, battery, accessibility). Those belong in the PDR.
- Do not design the system (components, data model, architecture). That's the PDR's job.
- Do not plan phases or tasks. That's the plan's job.
- Do not fill gaps with industry-standard boilerplate. A short, honest document with flagged gaps is worth more than a long document that mixes real requirements with invented ones.
- Do not ask confirmation questions. Generate the document with strong gap warnings. The user will tell you if you got something wrong.

## Concerns for Physical Design

The final section of the document lists concerns, open questions, and ambiguities that the next stage (PDR) must resolve. These are not gaps in the user requirements — they are things the requirements surface that need design-level answers.

Examples:
- "FR-4 specifies a double-press volume-up trigger. Whether this is reliable across platforms is a design and feasibility question, not a requirements question."
- "The user described local transcription but did not discuss what happens when the device lacks an STT model. The PDR should define graceful degradation."
- "Privacy expectations (Section 10) imply that rolling-buffer audio must be unrecoverable after discard. The PDR should specify how buffer memory is managed."

Write 3–10 concerns. Each must name the specific requirement or section it flows from, and state what the PDR needs to decide. Do not repeat gaps — gaps are about what the conversation didn't cover; concerns are about what the conversation DID cover that raises design questions.

## After Completion

Stage files produced by this command. Commit: `sdlc {cmd}: {brief description}`. Do not push.
