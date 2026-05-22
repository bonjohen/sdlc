---
title: "Content Collections for Structured Docs"
summary: "When schema-validated content collections pay off vs. plain HTML."
category: "architecture"
sortOrder: 3
---

## The Lesson

When a static site has reference content with consistent structure (commands, API endpoints, configuration options), modeling it as typed content collections with schema validation catches errors at build time and makes the content queryable — but the abstraction only pays off when you have 5+ items with the same shape.

## Context

A static marketing site ("I2I") needed to display 8 pipeline commands and 3 artifact examples. Each command has the same fields: name, purpose, input, output, workflow path, and sort order. Each artifact has: title, type (prompt vs. generated), optional source command, and sort order. The site uses Astro 5.x, which provides first-class content collections with Zod schema validation at build time.

## What Happened

1. Phase 02 needed to display 8 commands on the workflow page. Initially considered hardcoding them in the page template as HTML.
2. Recognized the pattern: 8 items with identical structure, likely to change as the pipeline evolves. Moved to content collections with individual markdown files per command.
3. Defined a Zod schema enforcing required fields (`name`, `purpose`, `input`, `output`, `path`, `sortOrder`). The `path` field uses `z.enum(["conversation", "document", "both"])` — typos in frontmatter now fail the build.
4. Phase 04 added an `artifacts` collection with a different schema (`title`, `type`, `command`, `excerpt`, `sortOrder`). Reused the same pattern — new collection, new schema, individual markdown files.
5. Build-time validation caught a typo in a command's `path` field during development — the error message pointed to the exact file and field. Without schema validation, this would have been a silent rendering bug.

## Key Insights

- **Schema validation turns runtime bugs into build errors.** A `z.enum()` on the path field means an invalid value fails `npm run build` with a clear error, not a blank or broken page in production.
- **Individual files per item enable git-level tracking.** When each command is its own markdown file, you get per-command history, blame, and diffs. A single JSON array loses this granularity.
- **The break-even point is around 5 items.** With 3 items, the schema definition + collection config + query code is more work than just writing HTML. With 8 items, the abstraction pays for itself in consistency and maintainability.
- **`sortOrder` fields are underrated.** Filesystem sort (alphabetical by filename) rarely matches the desired display order. An explicit numeric `sortOrder` in frontmatter keeps ordering intentional and independent of file naming.
- **Content collections are overkill for pages.** The "Why Stages" and "Getting Started" pages are one-off content without repeated structure. Making them collections would add overhead with no benefit.

## Applicability

Use content collections when: repeated items (5+), consistent structure, likely to grow, benefits from schema enforcement, edited by people who might make typos.

Do NOT use when: one-off pages, content with unique structure per item, fewer than 5 items with no growth trajectory, or when the "content" is really just a page with some frontmatter.
