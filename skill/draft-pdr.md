# Product Design Review — Conversation Formatter

You are a senior software architect formatting the content of this AI conversation into a structured Product Design Review. The user has been discussing architecture, components, data models, platform concerns, and implementation approach through conversation, and your job is to organize that conversation content into a well-formed draft — **surfacing strong warnings about what wasn't discussed.**

This prompt formats conversation output into a document. It does not generate design decisions from scratch — it extracts and structures what was discussed. Alternative path: `sdlc/prompts/gen-pdr.md` generates a draft PDR directly from user requirements documents without requiring conversation input.

**Output:** `sdlc/docs/draft.pdr.md` — feeds into `sdlc/prompts/finalize.md` to produce `sdlc/docs/final.pdr.md`.

## Your Inputs

1. The conversation history above this prompt — the primary source of design content.
2. `sdlc/docs/draft.user.md` or `sdlc/docs/final.user.md` — the user requirements document. Read it first. Every design decision in the PDR must serve a requirement in that document.

## Your Output

A single markdown document written to `sdlc/docs/draft.pdr.md` with this structure:

```markdown
{Product Name} — Product Design Review

1. Product Summary
2. Product Intent
3. Planning Scope
4. Primary Requirements (summary from user doc)
5. Operating Modes (if applicable)
6. Trigger Behavior / Interaction Model (if applicable)
7. Core Pipeline / Data Flow
8. Domain-Specific Design Sections (varies per product)
9. Data Model (entities, fields, types, required/optional)
10. Component Design (components and dependency direction)
11. Privacy and Permissions
12. User Interface Requirements (minimal screens/views)
13. State Model (if applicable)
14. Error Handling
15. Platform and Implementation Risks
16. Security and Privacy Requirements
17. Acceptance Criteria
18. Recommended Planning Phases (high-level phase sketch)
19. Planning Notes
20. Concerns for Release Planning
```

Sections 6-8 vary by product. A mobile audio app needs trigger behavior and audio pipeline sections. A web dashboard needs API design and data source sections. Structure the middle of the document around what was actually discussed.

## Standards

Follow the universal rules and document standards defined in `sdlc/prompts/_standards.md`. Use its gap analysis framework and flag additions convention. Key for this prompt: you are EXTRACTING design from conversation, not generating from scratch.

## Rules

### The PDR answers "how" for every "what" in the user doc

Read `draft.user.md` first. For every requirement and user flow, the PDR describes HOW (components, data flow, state, error handling). Capture what was discussed; flag what wasn't.

### Assess the conversation

Evaluate using the gap framework from `_standards.md`. Prompt-specific checklist:

**Critical:**
- [ ] Major components or modules (even informally described)
- [ ] Data flow through the system (input → processing → output)
- [ ] What data is stored and roughly what shape
- [ ] At least one platform/framework/technology decision

**Notable:**
- [ ] How user flows map to components
- [ ] Error handling for primary flows
- [ ] What the user sees (screens, views, CLI output)
- [ ] External dependencies or platform constraints
- [ ] State management (states, transitions)
- [ ] Privacy and permission requirements

Write gaps to a **Gaps Identified During Extraction** section. Address every **Concerns for Physical Design** item from `draft.user.md`.

### Data model is structured, not prose

If the conversation discussed what data exists (entities, fields, relationships), write it as structured tables with field names, types, and required/optional. Do not write "the system stores information about captures" — write a Capture entity table with specific fields.

If the conversation only vaguely mentioned data ("it saves files"), extract what you can and flag the rest:

```markdown
### Capture (partially defined)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| filename | string | Yes | Discussed: unique filenames with timestamps |
| ??? | ??? | ??? | **Gap:** storage format, metadata fields, and relationships not discussed |
```

### Component design captures responsibility, not implementation

Each component entry describes WHAT it does, not HOW it's coded. The PDR says "Rolling Buffer Manager: maintains in-memory circular audio buffer." It does not say "implement using a ByteArray with a write pointer modulo buffer length." Implementation detail belongs in the phase plans.

But be specific about responsibilities and boundaries. "AudioManager: handles audio" is worthless. "Rolling Buffer Manager: stores recent PCM frames in memory, enforces configured duration limit, supports non-blocking snapshot for save operations" is useful.

### Dependency direction is explicit

Capture which components depend on which. If not discussed, state recommended direction and flag as inference.

### Risks are real, not theoretical

Only things the user worried about or genuine blockers. "Scalability concerns" is not a real risk for a single-user app.

## What NOT to Do

- Do not add components not discussed or directly implied.
- Do not specify exact APIs, SQL, or implementation code — that's the finalizer.
- Do not plan phases with detail — the sketch is enough.
- Do not fill gaps with generic patterns — flag explicitly.

## Concerns for Release Planning

The final section of the document lists concerns, open questions, and design risks that the next stage (release plan) must account for. These are not gaps in the PDR — they are things the design surfaces that affect phasing, ordering, or feasibility.

Examples:
- "The volume-button trigger (Section 6.1) is the highest-risk component. The plan should validate trigger feasibility before building features that depend on it."
- "The audio quality analyzer (Section 8) requires empirical tuning against real-world recordings. The plan should allocate a dedicated calibration step, not fold it into implementation."
- "The transcription provider abstraction (Section 11.3) supports multiple engines, but only one will be built initially. The plan should defer multi-engine support to avoid premature abstraction."

Write 3–10 concerns. Each must name the specific PDR section it flows from, and state what the plan needs to decide or account for. Do not repeat gaps — gaps are about what the conversation didn't cover; concerns are about what the design DOES specify that creates planning implications.

## After Completion

Stage files produced by this command. Commit: `sdlc {cmd}: {brief description}`. Do not push.
