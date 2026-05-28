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

## Context Discipline During Implementation

**Before reaching for any tool — Read, Grep, Glob, Bash, or Agent — check what you already have.** The phase plan files (`sdlc/plan/phase{NN}/plan.md`) are intentionally designed to contain everything needed to implement that phase: file paths, schema definitions, code patterns, imports, design notes, and verification steps. The expand stage puts this information there precisely so that implementation does not require exploratory reads, codebase scans, or research subagents.

When you are executing a phase:

1. **Read the phase plan's Context section first.** It is your implementation guide. If the answer is there, act on it.
2. **Check conversation context second.** Files you have already read this session, plan state you have already parsed, tool output you have already received — do not re-fetch any of it.
3. **Read source files only when the phase plan tells you to** (e.g., "modify `src/foo.py`" means read that file) **or when you are genuinely missing information** that is not in the phase plan, the PDR, or the conversation.
4. **Never launch Explore subagents or project-wide searches before starting implementation work.** The phase plan already scoped what you need. If it didn't, that is a gap to flag — not a license to scan the entire codebase.

Unnecessary lookups waste context window, delay execution, and signal that the phase plan's Context section was ignored. Every Read/Grep/Glob/Agent call that retrieves information already available is a defect in execution, not diligence.

## Hooks & Skills

### SDLC-Specific Hooks

Two hooks enforce the `/sdlc implement` workflow:

**Checkpoint hook** (`~/.claude/hooks/sdlc-implement-checkpoint.py`) — `UserPromptSubmit` hook. Detects `/sdlc implement` in the user's prompt and automatically creates the sentinel file at `~/.claude/state/sdlc-implement.json`. If a sentinel already exists for the same project, it keeps it. This ensures the guard hook is always active during implement — not dependent on prompt compliance.

**Status guard hook** (`~/.claude/hooks/pre-implement-status-guard.py`) — `PreToolUse` hook (Edit/Write matchers). Blocks source file edits when no task is marked `Started` in the active phase plan. Plan file edits are always allowed. Fails open on all errors.

- **Activated by:** sentinel file at `~/.claude/state/sdlc-implement.json` (created by the checkpoint hook)
- **Deactivated by:** deleting the sentinel: `rm ~/.claude/state/sdlc-implement.json`
- **Registered in:** `~/.claude/settings.json`

### Global Hooks That Affect This Project

These hooks fire on every project. Documented in `~/.claude/CLAUDE.md`, registered in `~/.claude/settings.json`:

- **`PreToolUse(Bash)` — `ANTHROPIC_API_KEY` guard.** Blocks bash calls if `ANTHROPIC_API_KEY` is set. Enforces OAuth-only credit routing.
- **`PreToolUse(Bash)` — `git push` guard.** Blocks `git push` unless a single-use sentinel at `~/.claude/state/push-authorized.flag` exists. Each push needs fresh authorization.
- **`SessionStart` — status banner.** Prints branch/ahead-behind/effort level/guardrail reminders at session start.
- **`UserPromptSubmit` — plan-mode reminder.** Fires on design-shaped prompts (design doc, PDR, Stage 1/2), injecting workflow reminders. Always exits 0.

### Installed Skills (`~/.claude/skills/`)

This project defines `/sdlc`. The remaining skills are global utilities available across all projects.

| Skill | Source | Description |
|-------|--------|-------------|
| `/sdlc` | This project (`skill/SKILL.md` → symlinked) | SDLC document pipeline dispatcher. Routes subcommands to prompt files. |
| `/phase` | `~/.claude/skills/phase/` | Execute one phase of a plan (Stage 4 loop). Used by `/sdlc implement`. |
| `/push` | `~/.claude/skills/push/` | Commit, push, monitor GitHub Actions, fix build failures. Handles push sentinel. |
| `/preflight` | `~/.claude/skills/preflight/` | Run CI checks locally before pushing. |
| `/review` | `~/.claude/skills/review/` | Structured codebase review (security, dead code, consistency, drift). |
| `/tidy` | `~/.claude/skills/tidy/` | Repo housekeeping: archive, clean, normalize, verify consistency. |
| `/lessons` | `~/.claude/skills/lessons/` | Discover, write, audit, or repair lessons-learned documents. |
| `/external-lesson` | `~/.claude/skills/external-lesson/` | Research a topic via web and create a lesson markdown file. |
| `/file-pipeline` | `~/.claude/skills/file-pipeline/` | Process inbound lesson files through a state-machine pipeline. |
| `/diagram` | `~/.claude/skills/diagram/` | Generate architecture diagrams from knowledge graph presets. |
| `/healthcheck-machine` | `~/.claude/skills/healthcheck-machine/` | Run health scripts for machine classes (sparkdgx, macmini, etc.). |

## When Editing Prompts

The prompts in `skill/` are the core product. When modifying them:

- Each prompt has a defined input/output contract (documented in its header and in `prompt-instructions.md`). Changes must preserve these contracts or update all downstream consumers.
- The `finalize.md` prompt is the most complex — it processes three documents sequentially where each output feeds the next. Changes here cascade to `expand.md` and `implement.md`.
- `SKILL.md` is a pure dispatcher. It routes subcommands to prompt files and handles `show prompt` (prints raw prompt text for copy/paste into other AI tools). Routing logic lives here; execution logic lives in the individual prompts.
- The `show prompt` feature exists because `draft-*` prompts format conversation content — the conversation may be happening in a different AI tool. Users grab the prompt text via `/sdlc draft-user show prompt` to paste into that tool.
