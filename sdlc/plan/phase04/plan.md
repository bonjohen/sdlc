---
phase: 04
title: "Portfolio and Artifacts Pages"
depends_on: "Phase 03"
goal: "All content pages exist. The portfolio page demonstrates the creator's skills with credible, specific claims. The artifacts page shows real SDLC prompt and document examples."
source_pdr_sections: ["2.1", "2.3", "4.8", "5"]
source_user_stories: ["US-014", "US-015", "US-016", "US-017", "US-018", "US-019", "US-023"]
status: "completed"
---

# Phase 04: Portfolio and Artifacts Pages

## Tasks

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 04.1 | Completed | 2026-05-21 04:22 PM | 2026-05-21 04:24 PM | Build portfolio page at `src/pages/portfolio.astro` using ContentLayout: heading "About This Project", what the project demonstrates (AI workflow design, SDLC methodology, documentation, planning), creator's role, links to `github.com/bonjohen` and repo (when named) (PDR Section 5 Portfolio). |
| 04.2 | Completed | 2026-05-21 04:24 PM | 2026-05-21 04:25 PM | Review portfolio page content for tone: claims must be credible, technical, and specific. No boilerplate, no exaggerated claims. Verify human-in-the-loop framing (Constraint: human-in-the-loop framing). |
| 04.3 | Completed | 2026-05-21 04:22 PM | 2026-05-21 04:23 PM | Add Artifact content collection schema to `src/content/config.ts`: `title`, `type` (enum: prompt/generated), `command` (optional), `excerpt` (boolean), `sortOrder` (PDR Section 2.1). |
| 04.4 | Completed | 2026-05-21 04:23 PM | 2026-05-21 04:24 PM | Create artifact content entries in `src/content/artifacts/` from actual SDLC files: at least one prompt excerpt (from `skill/*.md`) and at least one generated document excerpt (from `sdlc/docs/*.md`) (PDR Section 2.3). |
| 04.5 | Completed | 2026-05-21 04:24 PM | 2026-05-21 04:25 PM | Implement `src/components/ArtifactExample.astro`: styled block with title, type badge ("Prompt" or "Generated Document"), optional command label, rendered markdown content, excerpt note when applicable (PDR Section 4.8). |
| 04.6 | Completed | 2026-05-21 04:25 PM | 2026-05-21 04:26 PM | Build artifacts page at `src/pages/artifacts.astro` using ContentLayout: heading "Example Artifacts", ArtifactExample components for each artifact entry, labeled by type and command (PDR Section 5 Artifacts). |
| 04.7 | Completed | 2026-05-21 04:26 PM | 2026-05-21 04:26 PM | Add both pages to Nav: Portfolio at `navOrder: 5` with label "Portfolio", Artifacts at `navOrder: 6` with label "Artifacts". |
| 04.8 | Completed | 2026-05-21 04:26 PM | 2026-05-21 04:27 PM | Spot-check accessibility: heading hierarchy, code block readability, artifact type badges have sufficient contrast, all links have descriptive text (NFR-003). |

## Context

### Files to Create or Modify

- `src/pages/portfolio.astro` — Portfolio/case-study page
- `src/pages/artifacts.astro` — Artifacts examples page
- `src/content/config.ts` — Add Artifact collection schema (file already exists from Phase 02 with Command schema)
- `src/content/artifacts/prompt-example.md` — At least one prompt excerpt
- `src/content/artifacts/generated-example.md` — At least one generated document excerpt
- `src/components/ArtifactExample.astro` — Artifact display component

### Artifact Content Collection Schema (from PDR Section 2.1)

Update `src/content/config.ts` to add the artifacts collection:

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

const artifacts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    type: z.enum(["prompt", "generated"]),
    command: z.string().optional(),
    excerpt: z.boolean().default(false),
    sortOrder: z.number(),
  }),
});

export const collections = { commands, artifacts };
```

### Artifact Seed Data (from PDR Section 2.3)

Source real content from the SDLC project files:

**Prompt example** — excerpt from `skill/finalize.md` (or another prompt file):

```markdown
---
title: "Finalize Prompt — Gap Checklist Excerpt"
type: "prompt"
command: "finalize"
excerpt: true
sortOrder: 1
---

The `finalize` command reads three draft documents and produces three final documents.
Each step applies a gap checklist — here's what the User Requirements gap checklist checks:

**Personas and actors**
- Are all user roles identified? (end user, admin, system/cron, API consumer, reviewer)
- Is there a "system" actor for automated processes?
- Are there external systems that act as users?

**Non-functional requirements (almost always missing from drafts)**
- Performance targets — response time, throughput
- Data volume expectations
- Availability requirements
- Security — authentication, authorization, input validation
- Accessibility — WCAG level, keyboard navigation

This is an excerpt. See the full prompt in the repository.
```

**Generated document example** — excerpt from `sdlc/docs/final.plan.md` (or `final.pdr.md`):

```markdown
---
title: "Implementation Plan — Phase Task Table"
type: "generated"
command: "finalize"
excerpt: true
sortOrder: 2
---

The `finalize` command produced this task table as part of the final implementation plan:

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 01.1 | Open | | | Create `src/styles/global.css` with CSS reset, typography... |
| 01.2 | Open | | | Implement `src/layouts/BaseLayout.astro`... |

Each phase has a goal, dependencies, and a table of atomic tasks.
Status transitions: Open → Started → Completed (with PST timestamps).

This is an excerpt. See the full plan in the repository.
```

### ArtifactExample Component Interface (from PDR Section 4.8)

```astro
---
interface Props {
  title: string;
  type: "prompt" | "generated";
  command?: string;
  excerpt: boolean;
}

const { title, type, command, excerpt } = Astro.props;

const typeLabel = type === "prompt" ? "Prompt" : "Generated Document";
---

<article class="artifact-example">
  <header class="artifact-header">
    <h3>{title}</h3>
    <span class="type-badge" data-type={type}>{typeLabel}</span>
    {command && <span class="command-label">from <code>{command}</code></span>}
  </header>
  <div class="artifact-content">
    <slot />
  </div>
  {excerpt && (
    <p class="excerpt-note">
      <em>This is an excerpt. See the full document in the repository.</em>
    </p>
  )}
</article>
```

### Portfolio Page Content Structure

`src/pages/portfolio.astro` — Heading: "About This Project"

Sections:

1. **What This Project Demonstrates**
   - AI workflow design: structured prompts that guide an AI through complex multi-stage processes
   - SDLC methodology: applying formal software engineering discipline to AI-assisted development
   - Documentation practice: producing traceable, cross-referenced documents that bridge requirements to implementation
   - Software planning: breaking large projects into ordered, dependency-aware phases with atomic tasks

2. **The Creator's Role**
   - Designed the pipeline architecture: the stage sequence, document contracts, and gap-surfacing mechanisms
   - Wrote the prompt system: 8 prompts that handle drafting, generation, finalization, expansion, and implementation
   - Applied the workflow to itself: this website was built using the same SDLC pipeline it explains

3. **Why This Matters**
   - AI-assisted development needs structure to be reliable
   - Unstructured AI coding produces inconsistent results
   - This workflow provides the structure: human sets direction, AI handles volume, documents provide accountability
   - The result is reproducible: anyone can follow the same pipeline and get structured, traceable results

4. **Links**
   - GitHub profile: `bonjohen` (from `src/config.ts` → `creatorGithub`)
   - Repository: when named (from `src/config.ts` → `repoUrl`)
   - Creator's website: `johnboen.com` (optional, if available)

### Key Patterns and Imports

Querying the artifacts collection on the artifacts page:

```astro
---
import { getCollection } from 'astro:content';
import ContentLayout from '../layouts/ContentLayout.astro';
import ArtifactExample from '../components/ArtifactExample.astro';

const artifacts = await getCollection('artifacts');
const sorted = artifacts.sort((a, b) => a.data.sortOrder - b.data.sortOrder);
---

<ContentLayout title="Example Artifacts" description="Real prompts and generated documents from the SDLC pipeline.">
  <h1>Example Artifacts</h1>
  <p>These are real excerpts from the SDLC pipeline...</p>

  {sorted.map(async (artifact) => {
    const { Content } = await artifact.render();
    return (
      <ArtifactExample
        title={artifact.data.title}
        type={artifact.data.type}
        command={artifact.data.command}
        excerpt={artifact.data.excerpt}
      >
        <Content />
      </ArtifactExample>
    );
  })}
</ContentLayout>
```

### Design Notes

- **Portfolio tone (PDR Concern 4, Constraint):** The portfolio page must be credible and specific. Bad: "Revolutionary AI-powered development." Good: "A structured prompt pipeline that turns a product conversation into implementation-ready plans with full traceability from user need to code task." Every claim should be demonstrable from the project itself.
- **Human-in-the-loop framing:** The portfolio must not claim full automation. The workflow is explicitly AI-*assisted*: AI handles volume/formatting, humans set direction/review. This is stated in the user requirements constraints.
- **Artifact content is real:** Do not write placeholder text for artifact examples. Extract actual content from `skill/finalize.md` (or another prompt file) and `sdlc/docs/final.plan.md` (or another generated file). The content IS the portfolio evidence.
- **Task 04.2 is editorial:** This is a content review task, not a code task. Read the portfolio page content after writing it and check: Are claims specific? Can each claim be verified by looking at the project? Is the tone technical rather than promotional?

### Verification

- [ ] `npm run build` exits 0 (artifact collection schema validates all entries)
- [ ] Portfolio page at `dist/portfolio/index.html` exists
- [ ] Portfolio page explains what the project demonstrates (minimum 3 skill areas)
- [ ] Portfolio page includes the creator's role and approach
- [ ] Portfolio page links to `github.com/bonjohen`
- [ ] Portfolio page contains no exaggerated claims (no "revolutionary", "game-changing", "unprecedented")
- [ ] Portfolio page presents the workflow as human-in-the-loop, not fully autonomous
- [ ] Artifacts page at `dist/artifacts/index.html` exists
- [ ] Artifacts page displays at least one prompt excerpt
- [ ] Artifacts page displays at least one generated document excerpt
- [ ] Each artifact is labeled with type badge ("Prompt" or "Generated Document")
- [ ] Each artifact shows its source command when applicable
- [ ] Artifact content is real (sourced from actual project files, not placeholder)
- [ ] Navigation links to `/portfolio/` and `/artifacts/` work from any page
- [ ] Heading hierarchy correct on both pages

## Phase Summary

- **Changes:** Added artifacts collection schema to `src/content/config.ts`. Created 3 artifact entries in `src/content/artifacts/` (2 prompt excerpts, 1 generated doc excerpt). Created `src/components/ArtifactExample.astro`, `src/pages/portfolio.astro`, `src/pages/artifacts.astro`. Portfolio page has credible, specific claims with human-in-the-loop framing. Nav already had entries from Phase 01.
- **Commit:** `Phase 04: Portfolio and artifacts pages — ArtifactExample, content entries, portfolio and artifacts pages`
