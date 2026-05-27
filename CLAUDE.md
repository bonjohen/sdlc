# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

This is the **SDLC prompt pipeline** — a set of structured markdown prompts that drive an AI-assisted software development lifecycle. It is not a codebase with build/test/lint tooling. It is a prompt engineering project whose artifacts are markdown files consumed by AI agents (Claude Code, ChatGPT, Gemini, etc.).

The pipeline turns a software idea into implementation-ready plans and then into working code, through a sequence of document stages. The current project using this pipeline is **I2I — From Idea to Implementation**, a static website that explains and markets the SDLC workflow itself.

## Repository Layout

```
├── skill/              ← Prompt files (the pipeline itself)
│   ├── SKILL.md        ← /sdlc skill dispatcher (routes subcommands to prompts)
│   ├── prompt-instructions.md  ← Pipeline overview, file layout, usage paths
│   ├── draft-user.md   ← Conversation → draft user requirements
│   ├── draft-pdr.md    ← Conversation → draft Product Design Review
│   ├── draft-plan.md   ← Conversation → draft release plan
│   ├── gen-pdr.md      ← User requirements doc → draft PDR (no conversation needed)
│   ├── gen-plan.md     ← PDR doc → draft release plan (no conversation needed)
│   ├── finalize.md     ← Three drafts → three finals (gap analysis, traceability)
│   ├── expand.md       ← Final plan → per-phase execution plans
│   └── implement.md    ← Execute phases, update task state, write code, commit
├── docs/lessons/       ← Reusable patterns extracted from this project
├── sdlc/               ← I2I marketing site (Astro) + SDLC docs for this project
│   ├── docs/           ← Generated documents (drafts and finals)
│   │   ├── draft.user.md / draft.pdr.md / draft.plan.md
│   │   └── final.user.md / final.pdr.md / final.plan.md
│   ├── plan/           ← Per-phase execution plans
│   │   └── phase{NN}/plan.md
│   └── src/            ← Astro site source
└── .github/workflows/  ← GitHub Pages deployment
```

## The Pipeline

Eight prompts form a linear pipeline. Each prompt reads prior-stage artifacts and produces the next stage:

```
Conversation path:              Document path:
  conversation                    prior-stage docs
       |                               |
  draft-user ─┐                  gen-pdr ──┐
  draft-pdr ──┤ → drafts         gen-plan ─┤ → drafts
  draft-plan ─┘                            ┘
                    |
               finalize → finals
                    |
                 expand → phase plans
                    |
               implement → code
```

Three workflow paths exist:
- **Conversation path** (happy path): Have a conversation about each stage, then use `draft-*` to format it into a document.
- **Fast path**: Conversation for user requirements only, then `gen-pdr` and `gen-plan` auto-generate design and plan from docs.
- **Mixed path**: Any combination — e.g., conversation for requirements, generated PDR, conversation for plan.

User requirements always start from conversation (`draft-user`). There is no `gen-user` — requirements must come from a human.

## Skill Installation

The pipeline is invoked as a Claude Code skill via `/sdlc <subcommand>`:

```bash
mkdir -p ~/.claude/skills/sdlc
ln -s "$(pwd)/skill/SKILL.md" ~/.claude/skills/sdlc/SKILL.md
```

## Project Boundary

**Never create, modify, or delete files outside of this project (`C:\Projects\sdlc`) unless the user explicitly requests it in the current message.** The additional working directories (`D:\Archive`, `C:\Users\boen3`) are available for reading/reference only. Other projects under `C:\Projects\` (e.g., `C:\Projects\template`) are separate repositories — do not write to them even if the SDLC pipeline references them.

## Key Conventions

- **Document cascade**: Each prompt reads the best available prior-stage doc (`final.*` preferred over `draft.*`). The finalize step processes all three drafts sequentially — each final feeds into the next.
- **Gap surfacing**: Every prompt is required to flag gaps in its input documents. Critical gaps get blunt warnings at the top of the output. The pipeline never silently fills gaps — it warns and proceeds.
- **Extract, don't invent**: `draft-*` prompts extract and structure conversation content. They do not add features or requirements the user didn't discuss. `gen-*` prompts make engineering decisions but flag assumptions.
- **Traceability chain**: User stories get `US-NNN` IDs, NFRs get `NFR-NNN`. PDR sections reference user story IDs. Plan tasks reference PDR sections. The chain must be unbroken from user need to implementation task.
- **Two-file state**: During implementation, task status is tracked in both `final.plan.md` and `plan/phase{NN}/plan.md`. Both must match. If they drift, `final.plan.md` is authoritative.
- **One commit per phase**: Implementation commits after each phase completes (all tasks done, verification green). Never commits partial phases or batches multiple phases.
- **PST timestamps**: All Started/Completed timestamps use Pacific Standard Time, format `YYYY-MM-DD HH:MM AM/PM`.

## Implement Status Guard Hook

A `PreToolUse` hook at `~/.claude/hooks/pre-implement-status-guard.py` enforces status-before-implementation during `/sdlc implement`. It blocks Edit/Write calls to source files when no task is marked `Started` in the active phase plan.

- **Activated by:** sentinel file at `~/.claude/state/sdlc-implement.json` (created automatically by the implement prompt)
- **Deactivated by:** deleting the sentinel: `rm ~/.claude/state/sdlc-implement.json`
- **Behavior:** Blocks source file edits only. Plan file edits always allowed. Fails open on all errors (never blocks legitimate work due to a bug).
- **Registered in:** `~/.claude/settings.json` (Edit and Write matchers)

## When Editing Prompts

The prompts in `skill/` are the core product. When modifying them:

- Each prompt has a defined input/output contract (documented in its header and in `prompt-instructions.md`). Changes must preserve these contracts or update all downstream consumers.
- The `finalize.md` prompt is the most complex — it processes three documents sequentially where each output feeds the next. Changes here cascade to `expand.md` and `implement.md`.
- `SKILL.md` is a pure dispatcher. It routes subcommands to prompt files and handles `show prompt` (prints raw prompt text for copy/paste into other AI tools). Routing logic lives here; execution logic lives in the individual prompts.
- The `show prompt` feature exists because `draft-*` prompts format conversation content — the conversation may be happening in a different AI tool. Users grab the prompt text via `/sdlc draft-user show prompt` to paste into that tool.
