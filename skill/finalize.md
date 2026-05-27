# Draft-to-Final SDLC Document Finalizer

Follow the universal rules and document standards defined in `sdlc/prompts/_standards.md`. Use its gap analysis framework, document structures, and phase table standard throughout all three steps.

You are a senior software architect finalizing three SDLC documents from their drafts. Process in strict sequence (each feeds the next). Fill gaps the draft missed — don't rewrite their vision, make it buildable.

## Inputs

Three draft documents at the project root:

| Document | Path | Contains |
|----------|------|----------|
| Draft User Requirements | `sdlc/docs/draft.user.md` | User stories, personas, acceptance criteria (may be incomplete) |
| Draft PDR | `sdlc/docs/draft.pdr.md` | Physical design — data model, packages, dependencies, components (may be incomplete) |
| Draft Plan | `sdlc/docs/draft.plan.md` | Phased implementation plan with task tables (may be incomplete) |

Also read the existing codebase to understand what already exists. Do not propose rebuilding things that work.

## Outputs

Three finalized documents, produced in this exact sequence:

```
sdlc/docs/final.user.md    (step 1)
sdlc/docs/final.pdr.md     (step 2)
sdlc/docs/final.plan.md    (step 3)
```

Each step depends on the previous. Do not parallelize.

---

## Step 1: draft.user.md → final.user.md

Follow the instructions in `sdlc/prompts/gen-user.md` completely. That prompt contains the full process, gap checklist, output format, and rules for producing `sdlc/docs/final.user.md` from `sdlc/docs/draft.user.md`.

Read and execute `gen-user.md` as if its instructions were written inline here. Do not skip any of its rules or gap analysis steps. When it completes, `sdlc/docs/final.user.md` must exist before proceeding to Step 2.

---

## Step 2: draft.pdr.md + final.user.md → final.pdr.md

### Process

1. Read `final.user.md` (the output of Step 1).
2. Read `draft.pdr.md` in full.
3. Read the existing codebase for current schema, patterns, dependencies.
4. Cross-reference: for every user story and NFR in `final.user.md`, verify the PDR has a corresponding design element. Flag gaps.
5. Identify gaps using the checklist below.
6. Write `final.pdr.md`.

### Gap Checklist: What Draft PDRs Commonly Miss

**Data model gaps**
- [ ] Are all foreign keys and indexes defined? (not just tables and columns)
- [ ] Are ON DELETE/ON UPDATE cascades specified?
- [ ] Are NOT NULL, UNIQUE, CHECK constraints specified?
- [ ] Is there a migration strategy for schema changes?
- [ ] Are soft deletes needed? Is there a `deleted_at` column?
- [ ] Are audit columns present? (`created_at`, `updated_at`, `created_by`)
- [ ] Is there a versioning or history table for entities that need audit trails?

**API design gaps**
- [ ] Are all endpoints listed with method, path, request body, response shape, and status codes?
- [ ] Are error response formats consistent and documented?
- [ ] Is pagination specified (offset vs cursor, default page size, max page size)?
- [ ] Are rate limits specified per endpoint or globally?
- [ ] Is authentication/authorization specified per endpoint?

**Component design gaps**
- [ ] Are retry policies defined for external API calls? (max retries, backoff strategy, circuit breaker)
- [ ] Are timeout values specified? (request timeout, source timeout, batch timeout)
- [ ] Are batch sizes and concurrency limits specified?
- [ ] Is graceful degradation defined? (what happens when a dependency is down)
- [ ] Are idempotency guarantees specified for write operations?

**Infrastructure gaps**
- [ ] Are configuration values documented? (env vars, settings file, defaults)
- [ ] Are file system paths and permissions documented?
- [ ] Are log levels and log formats specified?
- [ ] Is the health check contract defined? (what it checks, what "healthy" means)
- [ ] Are backup procedures specified?

**Security gaps**
- [ ] Are secrets management practices defined? (no hardcoded keys, env var names, rotation)
- [ ] Is input validation specified at system boundaries?
- [ ] Are CORS, CSP, and other HTTP security headers addressed?
- [ ] Is credential redaction in logs addressed?

**Testing gaps**
- [ ] Is the test strategy defined? (unit, integration, e2e, smoke)
- [ ] Are test fixtures and factories specified?
- [ ] Are mocking strategies specified for external dependencies?
- [ ] Is test data management addressed? (seeding, cleanup, isolation)

### final.pdr.md Format

```markdown
---
document: "Physical Design Requirements"
version: "1.0"
status: "final"
source: "sdlc/docs/draft.pdr.md"
user_requirements: "sdlc/docs/final.user.md"
finalized_date: "{YYYY-MM-DD}"
---

# {Project Name} — Physical Design Requirements

**Source document:** `sdlc/docs/final.user.md`
**Project root:** `{absolute path}`
**Date:** {YYYY-MM-DD}

## 1. System Context

### 1.1 Existing Infrastructure to Reuse
| Asset | Location | Reuse Strategy |
|-------|----------|---------------|

### 1.2 New Dependencies
| Package | Purpose | Version Constraint | License |
|---------|---------|-------------------|---------|

### 1.3 Configuration
| Variable | Type | Default | Description |
|----------|------|---------|-------------|

## 2. Data Model

### 2.1 Schema
{Full CREATE TABLE statements with constraints, indexes, triggers.}

### 2.2 Migrations
{Migration strategy and numbered migration files.}

### 2.3 Seed Data
{What data is pre-loaded and from where.}

## 3. Package Layout
```
project/
  module/
    __init__.py
    ...
```

## 4. Component Designs

### 4.N {Component Name}
- **Purpose:** {one sentence}
- **Location:** `path/to/module.py`
- **Implements:** US-001, US-002, NFR-003
- **Interface:**
  ```python
  class ComponentName:
      async def method(self, arg: Type) -> ReturnType: ...
  ```
- **Behavior:** {how it works, error handling, edge cases}
- **Dependencies:** {what it calls, what calls it}

## 5. API Specification

| Method | Path | Auth | Request | Response | Status Codes |
|--------|------|------|---------|----------|-------------|

## 6. Security Design
{Authentication, authorization, input validation, secrets management.}

## 7. Observability
{Logging, health checks, metrics, error reporting.}

## 8. Test Strategy
{Test types, fixtures, mocking approach, coverage targets.}

## 9. Traceability Matrix

| User Story | PDR Section | Component | Endpoint |
|-----------|-------------|-----------|----------|
| US-001 | 4.1 | SignalService | POST /api/signals |
```

### Type-Aware Enrichment (Step 2)

If the draft PDR contains a "Detected project type" note (added by gen-pdr's type detection):

1. **Locate the template root** using the same convention as gen-pdr:
   - If current project root has `data/types/*.yaml` → template root is `.`
   - Else if `$TEMPLATE_ROOT` is set → use that
   - Else default: `C:\Projects\template`
   
   If the template root cannot be resolved or has no `examples/` directory, skip this enrichment.

2. **Read TYPE_INFO.md** for the detected type from `{template_root}/examples/{type_id}/TYPE_INFO.md`

3. **Cross-reference** the PDR's component designs against the example repo's structure:
   - Where the PDR's components align with example patterns, add concrete implementation notes: directory paths matching the type's conventions, configuration patterns the type uses, testing patterns from the example
   - Where the PDR intentionally diverges from the example, leave it alone — the PDR author's choices take precedence

4. **Check anti-patterns.** Read the type definition's `anti_patterns` field and verify the PDR doesn't exhibit them. If it does, add a warning note.

If no type was detected in the draft PDR, skip this enrichment entirely. No error.

### Template Recommendation

After writing all other PDR sections, check for template manifests:

1. Look for `~/.sdlc/repo/examples/*/template.yaml` files. If `~/.sdlc/repo` does not exist
   (no SDLC CLI cache), skip this section entirely — do not mention templates at all.

2. If template manifests are found, read each manifest's `type_id`, `name`, `description`,
   and `layers` fields. Compare the detected project type (from type enrichment above)
   against each template's `type_id`.

3. Write a `## Recommended Template` section at the end of `final.pdr.md`:

   **If a template matches with high or medium confidence:**

   ```markdown
   ## Recommended Template

   **Template:** {template name}
   **Confidence:** {High|Medium}
   **Layers:** {comma-separated layer list}

   **Reasoning:** {1-2 sentences explaining why this template matches the project's
   intent, architecture, and stack.}

   **To apply:**
   ```
   sdlc pull {template_id} [--var KEY=VALUE ...]
   ```

   Review the template contents with `sdlc list --format json` before pulling.
   ```

   **If no template matches:**

   ```markdown
   ## Recommended Template

   No template match found for this project's characteristics.
   Browse available templates with `sdlc list`.
   ```

4. **Critical:** This section is informational only. The finalize prompt does NOT execute
   `sdlc pull`. It recommends; the user decides and acts.

5. **Backward compatibility (NFR-008):** If no `~/.sdlc/repo` directory exists, omit the
   `## Recommended Template` section entirely. Do not print an error or warning about
   missing templates. The pipeline must work identically to before for users who haven't
   set up the SDLC CLI.

### Rules for Step 2

- **Every user story must trace to at least one component.** The traceability matrix (Section 9) is not optional. If a user story has no corresponding design, either add the design or flag it as deferred with a reason.
- **Every NFR must have a design response.** "P95 < 500ms" needs an explanation of how the design achieves it (indexes, caching, pagination limits, etc.).
- **Schema is executable SQL.** Not pseudocode, not prose descriptions of tables. Actual `CREATE TABLE` statements that can run.
- **Preserve existing patterns.** If the codebase already has a pattern (e.g., service layer, adapter pattern, Pydantic models), the PDR must follow it. Do not introduce new architectural patterns without justification.
- **Flag what you added.** Same convention as Step 1: `<!-- Added during finalization: [brief reason] -->`

---

## Step 3: draft.plan.md + final.pdr.md → final.plan.md

### Process

1. Read `final.pdr.md` (the output of Step 2).
2. Read `draft.plan.md` in full.
3. Cross-reference: for every component and endpoint in the PDR, verify the plan has a task that creates it. Flag gaps.
4. Identify gaps using the checklist below.
5. Write `final.plan.md`.

### Gap Checklist: What Draft Plans Commonly Miss

**Phase structure**
- [ ] Is there a Phase 0 for project scaffolding, configuration, and CI setup?
- [ ] Is there a final phase for documentation, cleanup, and deployment prep?
- [ ] Are database migrations in an early phase before the code that depends on them?
- [ ] Are test fixtures and factories created in the same phase as the code they test?

**Task completeness**
- [ ] Does every CREATE TABLE in the PDR have a corresponding migration task?
- [ ] Does every component in the PDR have creation, wiring, and test tasks?
- [ ] Does every API endpoint have a route task, a test task, and a UI task (if applicable)?
- [ ] Are seed data tasks included?
- [ ] Are configuration/environment setup tasks included?

**Dependency ordering**
- [ ] Are schema migrations before service layer code?
- [ ] Are service layer modules before route handlers?
- [ ] Are base classes and utilities before the things that inherit/use them?
- [ ] Are external API integrations before the orchestrators that call them?
- [ ] Is authentication before endpoints that require it?

**Verification tasks**
- [ ] Does every phase end with a verification task (tests pass, lint clean)?
- [ ] Are integration tests in a later phase than unit tests?
- [ ] Is there an end-to-end smoke test in the final phase?

**Operational tasks often missing**
- [ ] Health check endpoint
- [ ] Database backup mechanism
- [ ] Log configuration
- [ ] Error handling middleware
- [ ] Configuration validation on startup
- [ ] Graceful shutdown handling

### final.plan.md Format

Use the Phase Table Standard from `_standards.md` for state transitions, columns, and commit protocol.

```markdown
---
document: "Implementation Plan"
version: "1.0"
status: "final"
source: "sdlc/docs/draft.plan.md"
pdr: "sdlc/docs/final.pdr.md"
user_requirements: "sdlc/docs/final.user.md"
finalized_date: "{YYYY-MM-DD}"
total_phases: {N}
---

# {Project Name} — Implementation Plan

**Source PDR:** `sdlc/docs/final.pdr.md`
**Source User Requirements:** `sdlc/docs/final.user.md`

## Work Queue Instructions

### State Transitions

Open  ──>  Started  ──>  Completed
              │
              └──>  Blocked  ──>  Started  ──>  Completed

(See _standards.md Phase Table Standard for state definitions and commit protocol.)

## Technology Stack

| Concern | Choice | Justification |
|---------|--------|--------------|
| {concern} | {technology} | {why this choice — from PDR} |

## Phase 00: {Title}

**Goal:** {What is true after this phase completes.}
**Depends on:** None (first phase).
**PDR sections:** {which PDR sections this implements}
**User stories:** {which user story IDs this satisfies}

| No | Status | Started (PST) | Completed (PST) | Description |
|----|--------|---------------|------------------|-------------|
| 00.1 | Open | | | {task description} |
| 00.2 | Open | | | {task description} |

### Phase 00 Summary

_To be filled after completion._

- **Changes:** TBD
- **Commit:** TBD

## Phase 01: {Title}

**Goal:** {goal}
**Depends on:** Phase 00.
...

## Coverage Checklist

_Verify every PDR component appears in at least one phase task._

| PDR Section | Component | Phase | Task |
|-------------|-----------|-------|------|
| 4.1 | SignalService | 02 | 02.3 |
| ... | ... | ... | ... |
```

### Type-Aware Phase Guidance (Step 3)

If a project type was detected (noted in the final PDR from Step 2):

1. Read the example repo's directory structure to understand the typical build order for this type
2. Verify the draft plan's phase ordering is compatible with the type's typical dependencies (e.g., a FastAPI service should set up routes before AI adapter integration)
3. If the type's TYPE_INFO.md describes anti-patterns, verify the plan doesn't repeat them (e.g., if the type avoids "infrastructure overengineering", ensure early phases focus on core value not scaffolding)

This is guidance, not override. The plan author's structure takes precedence. If no type was detected, skip entirely.

### Rules for Step 3

- **Every PDR component gets at least one task.** The Coverage Checklist at the bottom must show complete coverage. If a PDR component has no task, add one to the appropriate phase.
- **Phase boundaries are shippable.** After each phase completes, the system should be in a working state. No phase should leave the codebase in a broken state.
- **Tasks are atomic.** One task = one thing to do. "Create the service layer and write all the tests" is two tasks. Split them.
- **Dependencies flow downward.** Phase N should never depend on Phase N+1. If it does, reorder.
- **Preserve the draft's phasing unless it's wrong.** If the draft has a reasonable phase structure, keep it. Only restructure if there are dependency violations or phases that would leave the system broken.
- **Flag what you added.** Same convention: `<!-- Added during finalization -->`

---

## General Rules (All Steps)

The universal rules in `_standards.md` apply to all three steps. Additionally:

- **Be concrete.** "Handle errors" → "Return HTTP 503 with `{error, retry_after}` when API returns 5xx."
- **Cross-reference everything.** Unbroken traceability: user story IDs → PDR sections → plan tasks.
- **Read the existing codebase.** Don't redesign working patterns.

## After Completion

Stage files produced by this command. Commit: `sdlc {cmd}: {brief description}`. Do not push.
