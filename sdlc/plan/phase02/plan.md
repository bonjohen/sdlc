---
phase: 02
title: "Workflow and Command Pages"
depends_on: "Phase 01"
goal: "The workflow page explains all 8 SDLC commands and shows the three workflow paths. Content is sourced from actual SDLC prompt files, not placeholder text. This completes the Minimum Useful Release."
source_pdr_sections: ["2.1", "2.3", "4.6", "4.7", "5"]
source_user_stories: ["US-005", "US-006", "US-007", "US-008", "US-009", "US-010", "US-021"]
status: "open"
---

# Phase 02: Workflow and Command Pages

## Tasks

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 02.1 | Completed | 2026-05-21 04:07 PM | 2026-05-21 04:08 PM | Define Command content collection schema in `src/content/config.ts`: `name`, `purpose`, `input`, `output`, `path` (enum), `sortOrder` (PDR Section 2.1). |
| 02.2 | Completed | 2026-05-21 04:08 PM | 2026-05-21 04:10 PM | Create 8 command content entries in `src/content/commands/` sourced from `skill/*.md` and `skill/SKILL.md` — one `.md` file per command with accurate purpose, input, and output descriptions (PDR Section 2.3). |
| 02.3 | Completed | 2026-05-21 04:10 PM | 2026-05-21 04:11 PM | Implement `src/components/CommandCard.astro`: card displaying command name, purpose, input, output, and path badge (PDR Section 4.6). |
| 02.4 | Completed | 2026-05-21 04:11 PM | 2026-05-21 04:12 PM | Implement `src/components/PathDiagram.astro`: visual flow showing conversation path, fast path, and mixed path with their respective command sequences (PDR Section 4.7). |
| 02.5 | Completed | 2026-05-21 04:12 PM | 2026-05-21 04:14 PM | Build workflow page at `src/pages/workflow.astro` using ContentLayout: heading "The SDLC Pipeline", stage-by-stage explanation, CommandCard components in pipeline order, PathDiagram, sections on what finalize/expand/implement produce (PDR Section 5 Workflow). |
| 02.6 | Completed | 2026-05-21 04:14 PM | 2026-05-21 04:14 PM | Add workflow page to Nav component page list with `navOrder: 2` and label "Workflow". |
| 02.7 | Completed | 2026-05-21 04:14 PM | 2026-05-21 04:15 PM | Spot-check accessibility: verify heading hierarchy (`h1` > `h2` > `h3`), color contrast on command cards, keyboard focus order through cards (NFR-003). |
| 02.8 | Completed | 2026-05-21 04:15 PM | 2026-05-21 04:15 PM | Verify all 8 command descriptions are accurate by comparing each content entry against the corresponding `skill/*.md` file header and behavior. |

## Context

### Files to Create or Modify

- `src/content/config.ts` — Create file with Command content collection schema
- `src/content/commands/draft-user.md` — Command entry for draft-user
- `src/content/commands/draft-pdr.md` — Command entry for draft-pdr
- `src/content/commands/draft-plan.md` — Command entry for draft-plan
- `src/content/commands/gen-pdr.md` — Command entry for gen-pdr
- `src/content/commands/gen-plan.md` — Command entry for gen-plan
- `src/content/commands/finalize.md` — Command entry for finalize
- `src/content/commands/expand.md` — Command entry for expand
- `src/content/commands/implement.md` — Command entry for implement
- `src/components/CommandCard.astro` — Command display card component
- `src/components/PathDiagram.astro` — Three workflow paths visualization
- `src/pages/workflow.astro` — Workflow page

### Content Collection Schema (from PDR Section 2.1)

`src/content/config.ts`:

```typescript
import { defineCollection, z } from 'astro:content';

const commands = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),
    purpose: z.string(),
    input: z.string(),
    output: z.string(),
    path: z.enum(["conversation", "document", "both"]),
    sortOrder: z.number(),
  }),
});

export const collections = { commands };
```

### Command Seed Data (from PDR Section 2.3)

Each command entry is a markdown file in `src/content/commands/` with YAML frontmatter + body content. Source the descriptions from these specific files:

| Entry | Source File | `path` | `sortOrder` |
|-------|------------|--------|-------------|
| `draft-user.md` | `skill/draft-user.md` | `conversation` | 1 |
| `draft-pdr.md` | `skill/draft-pdr.md` | `conversation` | 2 |
| `draft-plan.md` | `skill/draft-plan.md` | `conversation` | 3 |
| `gen-pdr.md` | `skill/gen-pdr.md` | `document` | 4 |
| `gen-plan.md` | `skill/gen-plan.md` | `document` | 5 |
| `finalize.md` | `skill/finalize.md` | `document` | 6 |
| `expand.md` | `skill/expand.md` | `document` | 7 |
| `implement.md` | `skill/implement.md` | `document` | 8 |

Example command entry (`src/content/commands/draft-user.md`):

```markdown
---
name: "draft-user"
purpose: "Format a conversation into structured user requirements"
input: "Conversation about the product idea, goals, and requirements"
output: "sdlc/docs/draft.user.md — draft user requirements document"
path: "conversation"
sortOrder: 1
---

The `draft-user` command takes an ongoing conversation about a product idea and extracts user requirements into a structured document. It identifies personas, user stories, functional requirements, acceptance criteria, and constraints from the natural-language discussion.

User requirements always start from conversation — there is no `gen-user` because requirements must come from a human.
```

The body content (below frontmatter) provides additional explanation rendered on the workflow page.

### Component Interfaces (from PDR Section 4.6, 4.7)

**CommandCard** (`src/components/CommandCard.astro`):

```astro
---
interface Props {
  name: string;
  purpose: string;
  input: string;
  output: string;
  path: "conversation" | "document" | "both";
}

const { name, purpose, input, output, path } = Astro.props;
---

<article class="command-card">
  <h3 class="command-name"><code>{name}</code></h3>
  <span class="path-badge" data-path={path}>{path}</span>
  <p class="command-purpose">{purpose}</p>
  <dl>
    <dt>Input</dt>
    <dd>{input}</dd>
    <dt>Output</dt>
    <dd>{output}</dd>
  </dl>
</article>
```

**PathDiagram** (`src/components/PathDiagram.astro`):

- No props. Self-contained.
- Shows three paths with their command sequences:
  - **Conversation path:** `draft-user` → `draft-pdr` → `draft-plan` → `finalize` → `expand` → `implement`
  - **Fast path:** `draft-user` → `gen-pdr` → `gen-plan` → `finalize` → `expand` → `implement`
  - **Mixed path:** `draft-user` → (any combination of draft/gen for PDR and plan) → `finalize` → `expand` → `implement`
- Renders as CSS-styled HTML with labeled sections for each path
- `draft-user` always starts from conversation in all paths (no `gen-user` exists)

### Workflow Page Structure

`src/pages/workflow.astro` should render:

1. **Heading:** "The SDLC Pipeline"
2. **Introduction paragraph:** Brief explanation of the pipeline concept
3. **Stage-by-stage section:** One CommandCard per command in pipeline order (sorted by `sortOrder`)
4. **Three paths section:** PathDiagram component with explanation of when to use each
5. **What finalize produces:** Explanation that finalize converts 3 drafts → 3 finals with gap analysis and traceability
6. **What expand produces:** Explanation that expand generates `sdlc/plan/phase{NN}/plan.md` files, each self-contained
7. **What implement does:** Explanation that implement executes phase plans, updates task status, verifies, commits

### Key Patterns and Imports

Querying content collections in Astro pages:

```astro
---
import { getCollection } from 'astro:content';
import ContentLayout from '../layouts/ContentLayout.astro';
import CommandCard from '../components/CommandCard.astro';
import PathDiagram from '../components/PathDiagram.astro';

const commands = await getCollection('commands');
const sortedCommands = commands.sort((a, b) => a.data.sortOrder - b.data.sortOrder);
---

<ContentLayout title="The SDLC Pipeline" description="...">
  {sortedCommands.map(cmd => (
    <CommandCard
      name={cmd.data.name}
      purpose={cmd.data.purpose}
      input={cmd.data.input}
      output={cmd.data.output}
      path={cmd.data.path}
    />
  ))}
  <PathDiagram />
</ContentLayout>
```

### Design Notes

- **Content sourcing (PDR Concern 3):** Command descriptions must be sourced from reading the actual `skill/*.md` files, not paraphrased from memory. Each skill file has a first-line comment or heading that explains its purpose. Read the file, extract the key information, write the content entry.
- **Task 02.6 (Nav update):** In the Phase 01 design, Nav already has all page links defined in a static array. The workflow page link should already be present. If it is, task 02.6 is verifying it works (the page now exists so the link no longer 404s). If the Nav was implemented differently, add the entry.
- **Path badges on CommandCard:** The `path` field renders as a visual badge indicating "conversation", "document", or "both". Use CSS to color-code: e.g., conversation path = blue badge, document path = green badge. Keep accessible (don't rely on color alone — the text label is the primary indicator).

### Verification

- [ ] `npm run build` exits 0 (content collection schema validates all 8 entries)
- [ ] Workflow page at `dist/workflow/index.html` exists
- [ ] Workflow page contains 8 CommandCard elements (one per command)
- [ ] Each CommandCard shows: name, purpose, input, output, and path badge
- [ ] Commands appear in pipeline order: draft-user, draft-pdr, draft-plan, gen-pdr, gen-plan, finalize, expand, implement
- [ ] PathDiagram shows three distinct paths: conversation, fast, mixed
- [ ] Page explains what `finalize` produces (3 finals from 3 drafts)
- [ ] Page explains what `expand` produces (per-phase plan files)
- [ ] Page explains what `implement` does (execute, track, verify, commit)
- [ ] Heading hierarchy: single `<h1>`, sections use `<h2>`, subsections use `<h3>`
- [ ] Navigation link to `/workflow/` works from homepage
- [ ] Command descriptions match the actual content in `skill/*.md` source files

## Phase Summary

- **Changes:** Created `src/content/config.ts` (Command collection schema), 8 command entries in `src/content/commands/`, `src/components/CommandCard.astro`, `src/components/PathDiagram.astro`, `src/pages/workflow.astro`. Workflow page shows all 8 commands with path badges, three workflow paths diagram, and explanation of finalize/expand/implement stages.
- **Commit:** `Phase 02: Workflow and command pages — content collections, CommandCard, PathDiagram, workflow page`
