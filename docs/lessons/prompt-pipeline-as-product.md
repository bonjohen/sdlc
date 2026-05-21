# Prompt Pipeline as Product

## The Lesson

A set of AI prompts can be engineered as a product with defined I/O contracts, versioned files, routing dispatch, and a cascade architecture — not just ad-hoc text pasted into chat windows. Treating prompts as software artifacts with interfaces unlocks composition, reuse, and quality gates.

## Context

A solo developer built an AI-assisted software development lifecycle (SDLC) tool. The tool is a set of 8 markdown prompts that take a software idea through requirements, design, planning, and implementation. The prompts are consumed by multiple AI agents (Claude Code, ChatGPT, Gemini) and need to work reliably across all of them. The pipeline produces ~3,000 lines of structured output documents from a single conversation about a product idea.

## What Happened

1. Started with a single monolithic prompt that tried to do everything — gather requirements, design the system, plan phases, and execute. It was 2,000+ lines and broke constantly when AI tools hit context limits.
2. Decomposed into 8 discrete prompts, each with a defined input (prior-stage documents or conversation) and output (a specific markdown file at a known path).
3. Added a dispatcher (`SKILL.md`) that routes subcommands to prompt files — giving the pipeline a CLI-like interface (`/sdlc draft-user`, `/sdlc gen-pdr`).
4. Defined explicit I/O contracts in a manifest (`prompt-instructions.md`) so each prompt's dependencies are documented and machine-inspectable.
5. Added a `show prompt` feature so prompts could be extracted and used in other AI tools where the conversation was happening — acknowledging the pipeline doesn't own the execution environment.
6. Built the I2I marketing site *using* the pipeline itself, validating the contracts end-to-end.

## Key Insights

- **Prompts have interfaces just like functions.** Defining input documents, output paths, and expected formats lets you compose prompts into pipelines the same way you compose software modules. Without contracts, prompts are black boxes that can't be reliably chained.
- **A dispatcher pattern makes prompt sets usable.** A single routing file that maps commands to prompts gives users a discoverable entry point. Without it, users must know which of 8 files to open and how to invoke each one.
- **"Show prompt" is the escape hatch for multi-tool workflows.** Prompts that format conversation content may need to run in tools other than where they're installed. Printing the raw prompt text for copy/paste acknowledges that the pipeline doesn't control the runtime.
- **Prompt files should be versioned in git like source code.** This gives you diff, blame, history, and branch — the same tools that make code maintainable. Ad-hoc prompts stored in notes apps or clipboard managers lose all of this.
- **Contracts enable independent prompt evolution.** When each prompt's I/O is defined, you can rewrite `finalize.md` without touching `expand.md`, as long as the output schema stays stable. Monolithic prompts can't evolve incrementally.

## Applicability

This pattern applies whenever you have more than 2-3 prompts that work together. It does NOT apply to one-off prompts for simple tasks (summarization, translation, Q&A) — the overhead of contracts and dispatch isn't justified for standalone operations.

The dispatcher pattern specifically helps when prompts will be invoked from a CLI or tool integration. If your prompts only run via copy/paste into a chat window, the routing layer adds no value.

## Related Lessons

- [Document Cascade Architecture](document-cascade-architecture.md) — the cascade is the composition model that prompt-as-product enables
- [Draft-to-Final Document Pipeline](draft-to-final-document-pipeline.md) — the quality-gate pattern that sits between pipeline stages
