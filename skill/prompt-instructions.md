# SDLC Prompt Pipeline — Instructions

## Prompt Inventory

| Prompt | Purpose | Input | Output |
|--------|---------|-------|--------|
| `draft-user.md` | Format an AI conversation about a product idea into a structured user requirements document | Conversation history | `sdlc/docs/draft.user.md` |
| `draft-pdr.md` | Format an AI conversation about system design into a structured Product Design Review | Conversation history + user requirements doc | `sdlc/docs/draft.pdr.md` |
| `draft-plan.md` | Format an AI conversation about phasing and priorities into a structured release plan | Conversation history + user requirements doc + PDR | `sdlc/docs/draft.plan.md` |
| `gen-pdr.md` | Generate a PDR directly from a user requirements document (no conversation needed) | `draft.user.md` or `final.user.md` | `sdlc/docs/draft.pdr.md` |
| `gen-plan.md` | Generate a release plan directly from a PDR (no conversation needed) | `draft.pdr.md` or `final.pdr.md` | `sdlc/docs/draft.plan.md` |
| `finalize.md` | Finalize all three draft documents — fill gaps, add traceability, produce executable schema | `draft.user.md` + `draft.pdr.md` + `draft.plan.md` | `final.user.md` + `final.pdr.md` + `final.plan.md` |
| `expand.md` | Generate per-phase execution plans with full implementation context from the finalized plan | `final.user.md` + `final.pdr.md` + `final.plan.md` | `sdlc/plan/phase{NN}/plan.md` files |
| `implement.md` | Execute phases — read plan state, write code, update task status, commit per phase | `final.plan.md` + `plan/phase{NN}/plan.md` | Working code + updated plan files |

## Using the `/sdlc` Skill

When installed as a Claude Code skill (see `SKILL.md`), the entire pipeline is available through a single command:

```
/sdlc <subcommand> [options]
```

| Command | What it does |
|---------|-------------|
| `/sdlc help` | Show available commands and pipeline diagram |
| `/sdlc draft-user` | Format this conversation into `draft.user.md` |
| `/sdlc draft-pdr` | Format this conversation into `draft.pdr.md` |
| `/sdlc draft-plan` | Format this conversation into `draft.plan.md` |
| `/sdlc gen-pdr` | Generate `draft.pdr.md` from user requirements docs |
| `/sdlc gen-plan` | Generate `draft.plan.md` from PDR docs |
| `/sdlc finalize` | Finalize all three drafts into `final.*.md` |
| `/sdlc expand` | Generate per-phase `plan/phase{NN}/plan.md` files |
| `/sdlc implement` | Execute the next incomplete phase, then stop |
| `/sdlc implement all` | Execute all remaining phases without pausing |
| `/sdlc implement phase 03` | Execute a specific phase |

### Show Prompt (for use in other AI environments)

Any subcommand can be followed by `show prompt` to display the raw prompt text instead of executing it. This prints the full prompt as a code block so you can copy it into ChatGPT, Gemini, or any other AI tool where the conversation is happening.

```
/sdlc draft-user show prompt     → prints draft-user.md for copy/paste
/sdlc draft-pdr show prompt      → prints draft-pdr.md for copy/paste
/sdlc draft-plan show prompt     → prints draft-plan.md for copy/paste
/sdlc gen-pdr show prompt        → works on any subcommand
```

This is especially useful for `draft-user`, `draft-pdr`, and `draft-plan` — since these format conversation content, the conversation may be happening in a different AI tool. Use `show prompt` to grab the prompt text, paste it into that tool, and get a properly formatted draft document back.

### Installation

Copy or symlink `SKILL.md` into your Claude Code skills directory:

```bash
# Symlink (stays in sync with the repo)
mkdir -p ~/.claude/skills/sdlc
ln -s "$(pwd)/sdlc/prompts/SKILL.md" ~/.claude/skills/sdlc/SKILL.md

# Or copy
mkdir -p ~/.claude/skills/sdlc
cp sdlc/prompts/SKILL.md ~/.claude/skills/sdlc/SKILL.md
```

## When to Use Each Prompt

### `draft-user.md` — "I just finished describing my idea"

Use after you've had a conversation with an AI about what your product should do. The conversation should cover what the product is, who uses it, how it works, and what it doesn't do. This prompt reads the conversation and formats it into a `draft.user.md`.

There is no `gen-user.md` equivalent. User requirements always come from conversation — they are the starting point of the pipeline.

### `draft-pdr.md` — "I just finished discussing the system design"

Use after you've had a conversation with an AI about how to build the system — components, data model, architecture layers, platform decisions, risks. This prompt reads the conversation and formats it into a `draft.pdr.md`.

Requires a user requirements document to already exist (draft or final).

### `draft-plan.md` — "I just finished discussing the release phases"

Use after you've had a conversation with an AI about what to build first, how to phase the work, what the milestones are, and what the risks dictate about ordering. This prompt reads the conversation and formats it into a `draft.plan.md`.

Requires both a user requirements document and a PDR to already exist.

### `gen-pdr.md` — "I have user requirements, generate the design"

Use when you have a user requirements document but don't want to (or haven't yet) discussed the design in conversation. This prompt reads the requirements and generates a PDR using engineering judgment. Useful when you want to move quickly from requirements to design without a separate design conversation.

Produces the same `draft.pdr.md` as `draft-pdr.md` — both feed into `finalize.md`.

### `gen-plan.md` — "I have a PDR, generate the release plan"

Use when you have a PDR but don't want to (or haven't yet) discussed phasing in conversation. This prompt reads the PDR and generates a risk-ordered release plan. Useful when you want to move quickly from design to planning without a separate planning conversation.

Produces the same `draft.plan.md` as `draft-plan.md` — both feed into `finalize.md`.

### `finalize.md` — "I have all three drafts, make them production-ready"

Use when `draft.user.md`, `draft.pdr.md`, and `draft.plan.md` all exist (from any combination of conversation formatting and document generation). This prompt processes them sequentially:

1. `draft.user.md` → `final.user.md` (adds personas, NFRs, acceptance criteria, IDs)
2. `draft.pdr.md` + `final.user.md` → `final.pdr.md` (adds executable schema, component interfaces, traceability matrix, test strategy)
3. `draft.plan.md` + `final.pdr.md` → `final.plan.md` (adds numbered task tables, phase dependencies, coverage checklist)

Each step fills gaps the drafts missed, flags additions with HTML comments, and produces documents with full cross-reference traceability.

### `expand.md` — "I have finalized docs, generate the phase execution plans"

Use after `finalize.md` has produced all three final documents. This prompt reads them and generates a standalone plan file for each phase at `sdlc/plan/phase{NN}/plan.md`. Each phase plan contains:

- The task table (same as in `final.plan.md`)
- A Context section with file paths, schema, patterns, imports, and design notes
- Verification criteria

Phase plans are self-contained — an implementer can execute a phase holding only its plan file and the codebase.

### `implement.md` — "Execute the plan"

Use after `expand.md` has generated phase plans. This prompt is the main workflow engine:

- Reads `final.plan.md` to find the next incomplete phase
- Reads `plan/phase{NN}/plan.md` for implementation context
- Executes tasks in order, updating status and timestamps in both files
- Runs verification, writes phase summaries, commits per phase

Two modes:
- **Single phase** (default): executes one phase and stops
- **Autonomous**: executes all remaining phases end-to-end (must be explicitly requested)

## The Happy Path

This is the full pipeline from idea to implementation, using the conversation path at every stage.

### Step 1: Describe the product idea

Start a conversation with an AI. Describe what you want to build, who it's for, what it does, how the user interacts with it, and what it explicitly does NOT do. Cover at least one complete user flow end-to-end.

When the conversation has covered enough ground, run `draft-user.md`.

```
sdlc/docs/draft.user.md  ← created
```

### Step 2: Discuss the system design

Continue the conversation (or start a new one with the draft in context). Discuss architecture: what components exist, how data flows, what the data model looks like, what platform you're targeting, what the risks are, what the state machine looks like.

When the conversation has covered enough ground, run `draft-pdr.md`.

```
sdlc/docs/draft.pdr.md  ← created
```

### Step 3: Discuss the release plan

Continue the conversation. Discuss what to build first and why, how to phase the work, what the milestones are, where the risk-first boundaries fall.

When the conversation has covered enough ground, run `draft-plan.md`.

```
sdlc/docs/draft.plan.md  ← created
```

### Step 4: Finalize all three documents

Run `finalize.md`. It processes all three drafts sequentially, filling gaps and adding structure.

```
sdlc/docs/final.user.md  ← created (from draft.user.md)
sdlc/docs/final.pdr.md   ← created (from draft.pdr.md + final.user.md)
sdlc/docs/final.plan.md  ← created (from draft.plan.md + final.pdr.md)
```

### Step 5: Generate phase execution plans

Run `expand.md`. It reads the three final documents and generates a standalone plan for each phase.

```
sdlc/plan/phase00/plan.md  ← created
sdlc/plan/phase01/plan.md  ← created
...
sdlc/plan/phase08/plan.md  ← created
```

### Step 6: Implement

Run `implement.md`. It picks up the first incomplete phase and starts executing.

```
sdlc/plan/phase00/plan.md  ← task statuses updated
sdlc/docs/final.plan.md   ← task statuses updated
src/...                    ← code written
(commit after phase completes)
```

Repeat `implement.md` for each subsequent phase, or request autonomous mode to run all remaining phases end-to-end.

## The Fast Path

If you don't want three separate conversations, use the generators to skip the conversation steps for design and planning:

```
Step 1: Conversation → draft-user.md → draft.user.md
Step 2: gen-pdr.md                   → draft.pdr.md    (no conversation needed)
Step 3: gen-plan.md                  → draft.plan.md   (no conversation needed)
Step 4: finalize.md                  → final.*.md
Step 5: expand.md                    → phase plans
Step 6: implement.md                 → code
```

The fast path always starts with a conversation (Step 1) — user requirements must come from a human describing what they want. But the PDR and plan can be generated directly from the requirements without additional conversation.

## The Mixed Path

You can mix conversation and generation freely. For example:

- Use `draft-user.md` to format requirements from conversation
- Use `gen-pdr.md` to generate a PDR from those requirements
- Have a conversation about the generated PDR to refine phasing decisions
- Use `draft-plan.md` to format the plan from that conversation

Any combination works as long as the inputs exist when you run each prompt.

## File Layout

```
sdlc/
  prompts/
    prompt-instructions.md    ← this file
    SKILL.md                  ← /sdlc skill dispatcher (install to ~/.claude/skills/sdlc/)
    draft-user.md             ← conversation → draft user requirements
    draft-pdr.md              ← conversation → draft PDR
    draft-plan.md             ← conversation → draft release plan
    gen-pdr.md                ← user requirements → draft PDR
    gen-plan.md               ← PDR → draft release plan
    finalize.md               ← drafts → finals (gap analysis, traceability)
    expand.md                 ← final plan → per-phase execution plans
    implement.md              ← execute phases, update state, write code
  docs/
    draft.user.md             ← draft user requirements
    draft.pdr.md              ← draft Product Design Review
    draft.plan.md             ← draft release plan
    final.user.md             ← finalized user requirements
    final.pdr.md              ← finalized PDR
    final.plan.md             ← finalized release plan
  plan/
    phase00/plan.md           ← Phase 0 execution plan
    phase01/plan.md           ← Phase 1 execution plan
    ...
```
