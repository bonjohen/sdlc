# I2I — From Idea to Implementation

A prompt-driven SDLC workflow that turns rough software ideas into buildable plans and working code.

**Live site:** [sdlc.johnboen.com](https://sdlc.johnboen.com)

## What This Is

A set of structured markdown prompts that drive an AI-assisted software development lifecycle. The prompts work with Claude Code, ChatGPT, Gemini, or any AI tool that accepts markdown instructions.

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
  draft-user ─┐              gen-user ─→ final.user.md
  draft-pdr ──┤ → drafts     gen-pdr ──┐
  draft-plan ─┘              gen-plan ─┤ → drafts
                                       ┘
                    |
               finalize → finals
                    |
                 expand → phase plans
                    |
               implement → code
```

## Repository Layout

```
├── skill/              ← Prompt files (the pipeline itself)
│   ├── SKILL.md        ← /sdlc skill dispatcher
│   ├── draft-user.md   ← Conversation → draft user requirements
│   ├── draft-pdr.md    ← Conversation → draft Product Design Review
│   ├── draft-plan.md   ← Conversation → draft release plan
│   ├── gen-user.md     ← Finalize draft user requirements into final
│   ├── gen-pdr.md      ← Requirements doc → draft PDR (no conversation needed)
│   ├── gen-plan.md     ← PDR doc → draft release plan (no conversation needed)
│   ├── finalize.md     ← Three drafts → three finals (gap analysis, traceability)
│   ├── expand.md       ← Final plan → per-phase execution plans
│   ├── implement.md    ← Execute phases, write code, commit
│   └── create-repo.md  ← Bootstrap a new project with SDLC prompts
├── hooks/              ← Implement enforcement hooks
│   ├── sdlc-implement-checkpoint.py  ← Creates sentinel on /sdlc implement
│   └── pre-implement-status-guard.py ← Blocks edits when no task is Started
├── docs/lessons/       ← Reusable patterns extracted from this project
├── sdlc/               ← I2I marketing site (built using this pipeline)
│   ├── docs/           ← Generated SDLC documents (drafts and finals)
│   ├── plan/           ← Per-phase execution plans
│   └── src/            ← Astro site source
└── .github/workflows/  ← GitHub Pages deployment
```

## Deploy

Run the deploy script to install the skill and hooks into your Claude Code environment:

```bash
bash deploy.sh
```

This copies:
- `skill/*.md` to `~/.claude/skills/sdlc/skill/` (prompt files)
- `skill/SKILL.md` to `~/.claude/skills/sdlc/SKILL.md` (dispatcher)
- `hooks/*.py` to `~/.claude/hooks/` (implement enforcement)

The hooks also require registration in `~/.claude/settings.json`. Add these entries if not already present:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [{ "type": "command", "command": "python ~/.claude/hooks/pre-implement-status-guard.py" }]
      },
      {
        "matcher": "Write",
        "hooks": [{ "type": "command", "command": "python ~/.claude/hooks/pre-implement-status-guard.py" }]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [{ "type": "command", "command": "python ~/.claude/hooks/sdlc-implement-checkpoint.py", "timeout": 10 }]
      }
    ]
  }
}
```

Start a new Claude Code session after deploying. Existing sessions do not pick up new skill files.

## Quick Start

### Use the pipeline

```
/sdlc draft-user          # Format conversation into user requirements
/sdlc gen-user            # Finalize draft user requirements
/sdlc gen-pdr             # Generate design from requirements
/sdlc gen-plan            # Generate plan from design
/sdlc finalize            # Gap analysis + traceability IDs
/sdlc expand              # Per-phase execution plans
/sdlc implement           # Execute the next phase
/sdlc implement all       # Execute all phases autonomously
/sdlc implement phase 03  # Execute a specific phase
/sdlc create-repo         # Bootstrap a new project
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

## Implement Workflow

The `implement` command uses three mechanisms to enforce disciplined execution:

- **Resume** — Each invocation reads plan state from disk and picks up where the last session left off. No conversation history needed.
- **Rewind** — If a session crashes mid-task, the next run inspects on-disk state against the plan. Work that exists is marked complete; work that doesn't is re-implemented from scratch.
- **Branch** — In multi-phase mode (`implement all`), each phase forks into a new session via `/branch`. Each phase gets a full context window; the completed session is preserved as a restore point.

Two hooks enforce the workflow:
- **Checkpoint hook** creates a sentinel file when `/sdlc implement` is detected, activating the guard.
- **Guard hook** blocks source file edits unless a task is marked `Started` in the active phase plan.

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
