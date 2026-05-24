# I2I — From Idea to Implementation

A prompt-driven SDLC workflow that turns rough software ideas into buildable plans and working code.

**Live site:** [sdlc.johnboen.com](https://sdlc.johnboen.com)

## What This Is

A set of 8 structured markdown prompts that drive an AI-assisted software development lifecycle. The prompts work with Claude Code, ChatGPT, Gemini, or any AI tool that accepts markdown instructions.

The pipeline takes a software idea through:

1. **Requirements** — Extract structured user stories from conversation
2. **Design** — Generate a Product Design Review with architecture, data model, and technology decisions
3. **Planning** — Break the design into phased, risk-ordered implementation plans
4. **Finalization** — Gap analysis, traceability IDs, cross-document consistency
5. **Expansion** — Per-phase execution plans with full implementation context
6. **Implementation** — Execute phases, track task state, commit per phase

```
Conversation path:          Document path:
  conversation                prior-stage docs
       |                           |
  draft-user ─┐              gen-pdr ──┐
  draft-pdr ──┤ → drafts     gen-plan ─┤ → drafts
  draft-plan ─┘                        ┘
                    |
               finalize → finals
                    |
                 expand → phase plans
                    |
               implement → code
```

## Repository Layout

```
sdlc/
├── skill/              ← Prompt files (the pipeline itself)
│   ├── SKILL.md        ← /sdlc skill dispatcher
│   ├── draft-user.md   ← Conversation → draft user requirements
│   ├── draft-pdr.md    ← Conversation → draft Product Design Review
│   ├── draft-plan.md   ← Conversation → draft release plan
│   ├── gen-pdr.md      ← Requirements doc → draft PDR (no conversation needed)
│   ├── gen-plan.md     ← PDR doc → draft release plan (no conversation needed)
│   ├── finalize.md     ← Three drafts → three finals (gap analysis, traceability)
│   ├── expand.md       ← Final plan → per-phase execution plans
│   └── implement.md    ← Execute phases, write code, commit
└── sdlc/               ← I2I marketing site (built using this pipeline)
    ├── docs/           ← Generated SDLC documents (drafts and finals)
    ├── plan/           ← Per-phase execution plans
    └── src/            ← Astro site source
```

## Quick Start

### Install as a Claude Code skill

```bash
mkdir -p ~/.claude/skills/sdlc
ln -s "$(pwd)/skill/SKILL.md" ~/.claude/skills/sdlc/SKILL.md
```

### Use the pipeline

```
/sdlc draft-user          # Format conversation into user requirements
/sdlc gen-pdr             # Generate design from requirements
/sdlc gen-plan            # Generate plan from design
/sdlc finalize            # Gap analysis + traceability IDs
/sdlc expand              # Per-phase execution plans
/sdlc implement all       # Execute all phases autonomously
```

### Use with other AI tools

Any command + `show prompt` prints the raw prompt for copy/paste:

```
/sdlc draft-user show prompt    # Prints prompt text to paste into ChatGPT, Gemini, etc.
```

## Three Workflow Paths

| Path | Best for | How it works |
|------|----------|-------------|
| **Conversation** | Maximum control | Have a conversation at each stage, then `draft-*` to format it |
| **Fast** | Speed | Conversation for requirements only, then `gen-pdr` and `gen-plan` auto-generate |
| **Mixed** | Balance | Any combination of conversation and generation per stage |

User requirements always start from conversation (`draft-user`). There is no `gen-user` — requirements must come from a human.

## The I2I Site

The `sdlc/` subdirectory contains the I2I marketing site — built using this pipeline as a dogfooding exercise. It's an Astro 5.x static site deployed to GitHub Pages.

```bash
cd sdlc
npm install
npm run dev     # http://localhost:4321
npm run build   # Static output in dist/
```

## Key Design Principles

- **Extract, don't invent.** Draft prompts structure what was said in conversation. They do not add features or requirements.
- **Gap surfacing over silent interpolation.** Every prompt flags what's missing with blunt warnings rather than quietly filling gaps.
- **Traceability chain.** User stories (US-NNN) → PDR sections → plan tasks. The chain must be unbroken.
- **Plan-as-state.** Markdown task tables are the state machine. Status, timestamps, and phase summaries are tracked in the plan files.
- **One commit per phase.** Each phase is independently shippable. No partial commits, no multi-phase batches.

## License

MIT
