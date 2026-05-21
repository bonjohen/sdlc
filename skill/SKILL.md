---
name: sdlc
description: "SDLC document pipeline — generate, finalize, expand, and implement software design documents. Subcommands: draft-user, draft-pdr, draft-plan, gen-pdr, gen-plan, finalize, expand, implement."
argument-hint: "<subcommand> [options]"
---

You are the dispatcher for the SDLC document pipeline. The user invoked `/sdlc $ARGUMENTS`.

## Command Routing

Parse `$ARGUMENTS` to determine the subcommand. The first word is the subcommand name. Remaining words are options passed to that subcommand.

| Subcommand | Prompt File | Description |
|------------|-------------|-------------|
| `draft-user` | `sdlc/prompts/draft-user.md` | Format this conversation into a `sdlc/docs/draft.user.md` |
| `draft-pdr` | `sdlc/prompts/draft-pdr.md` | Format this conversation into a `sdlc/docs/draft.pdr.md` |
| `draft-plan` | `sdlc/prompts/draft-plan.md` | Format this conversation into a `sdlc/docs/draft.plan.md` |
| `gen-pdr` | `sdlc/prompts/gen-pdr.md` | Generate `sdlc/docs/draft.pdr.md` from user requirements docs on disk |
| `gen-plan` | `sdlc/prompts/gen-plan.md` | Generate `sdlc/docs/draft.plan.md` from PDR docs on disk |
| `finalize` | `sdlc/prompts/finalize.md` | Finalize all three drafts into `sdlc/docs/final.*.md` |
| `expand` | `sdlc/prompts/expand.md` | Generate `sdlc/plan/phase{NN}/plan.md` files from final docs |
| `implement` | `sdlc/prompts/implement.md` | Execute the next incomplete phase (see options below) |
| `help` | *(none)* | Show this command list |

If `$ARGUMENTS` is empty or `help`, respond with the command table above and a one-line description of the pipeline. Do not read any files or take any action.

## Global Option: `show prompt`

Any subcommand can be followed by `show prompt` to display the raw prompt text instead of executing it. This is for copying the prompt into a different AI environment.

Examples:
- `/sdlc draft-user show prompt` — prints the contents of `sdlc/prompts/draft-user.md` to the conversation as a fenced code block. Does NOT execute it.
- `/sdlc gen-pdr show prompt` — same, prints `sdlc/prompts/gen-pdr.md`.

When `show prompt` is detected:
1. Read the prompt file for the matched subcommand.
2. Output the full file contents inside a single markdown code fence (` ```markdown ... ``` `).
3. Stop. Do not execute the prompt.

This is especially useful for `draft-user`, `draft-pdr`, and `draft-plan`, which are designed to format AI conversation content — the user may be having that conversation in a different tool and needs the prompt text to paste there.

## Execution

1. Match the first word of `$ARGUMENTS` to a subcommand in the table above.
2. If no match, respond: "Unknown subcommand: `{word}`. Run `/sdlc help` to see available commands."
3. If `$ARGUMENTS` contains `show prompt`, read the prompt file and display it as a code block. Stop.
4. Read the prompt file listed in the table.
5. Follow the instructions in that prompt file completely. The prompt file is the authority — this dispatcher only routes to it.

## Implement Options

The `implement` subcommand accepts additional options that control execution mode:

| Invocation | Behavior |
|------------|----------|
| `/sdlc implement` | Execute the next incomplete phase, then stop. |
| `/sdlc implement all` | Execute all remaining phases end-to-end without pausing between phases. Stop only for destructive actions, errors, or context limits. |
| `/sdlc implement phase NN` | Execute phase NN specifically (e.g., `/sdlc implement phase 03`). Warn if that phase is already complete. |

When routing to `sdlc/prompts/implement.md`:
- For `/sdlc implement` — pass no special instruction. The prompt defaults to single-phase mode.
- For `/sdlc implement all` — after reading the prompt file, add this instruction: "Execute in autonomous mode. Complete each phase, commit, and immediately proceed to the next phase without waiting for user input."
- For `/sdlc implement phase NN` — after reading the prompt file, add this instruction: "Execute phase NN specifically, regardless of which phase the plan considers 'next'."

## Pipeline Summary (for `help` output)

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
