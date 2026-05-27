# I2I — From Idea to Implementation — Final User Requirements Document

## 1. Product Name

**I2I — From Idea to Implementation**

## 2. Purpose

I2I shall be a multi-page static website that explains, teaches, and markets a prompt-driven software development life cycle workflow.

The website shall present the SDLC workflow as a practical way to move from a software idea to implementation-ready development artifacts. The underlying SDLC project includes prompts and commands for drafting user requirements, drafting or generating a Product Design Review, drafting or generating a phased release plan, finalizing the documents, expanding phase plans, and implementing the work. The prompt inventory identifies the major commands as `draft-user`, `draft-pdr`, `draft-plan`, `gen-pdr`, `gen-plan`, `finalize`, `expand`, and `implement`. 

The website shall also serve as a public portfolio project. It shall demonstrate the creator’s ability to design AI-assisted development workflows, organize software projects, create structured handoff documents, and communicate a reusable engineering process.

## 3. Core Concept

I2I shall explain a simple workflow:

**Idea → User Requirements → Product Design Review → Phased Release Plan → Finalized Documents → Phase Execution Plans → Implementation**

The site shall make the workflow understandable to a software developer, technical reviewer, hiring manager, or potential collaborator.

The site shall focus first on the workflow itself. Personal information about the creator shall be available, but it shall not dominate the initial explanation. Visitors who want more detail about the creator shall be able to find it through deeper pages, links, or portfolio sections.

## 4. Primary User Goal

A visitor shall be able to understand what I2I does, why it is useful, how the workflow operates, and how it reflects the creator’s software engineering and AI workflow design skills.

## 5. Operating Modes

### 5.1 Website Mode

I2I shall operate as a public, static, multi-page website.

### 5.2 Portfolio Mode

I2I shall operate as a personal portfolio artifact that can be shared with hiring managers, clients, collaborators, or technical peers.

### 5.3 Educational Mode

I2I shall operate as an educational guide that teaches how the SDLC workflow works and why each stage exists.

### 5.4 Marketing Mode

I2I shall operate as a marketing page for the workflow, emphasizing usefulness, clarity, repeatability, and human-in-the-loop AI-assisted software development.

## 6. Primary User Flows

### 6.1 First-Time Visitor Understands the Project

1. Visitor arrives at the homepage.
2. Visitor sees the name **I2I — From Idea to Implementation**.
3. Visitor reads a concise explanation of the project.
4. Visitor sees a visual workflow from idea to implementation.
5. Visitor understands that I2I is an automated SDLC workflow supported by structured prompts and generated artifacts.
6. Visitor can choose to learn the workflow, review examples, or learn more about the creator.

### 6.2 Developer Learns the Workflow

1. Developer opens the workflow page.
2. Developer sees the SDLC stages in order.
3. Developer sees what each stage consumes and produces.
4. Developer understands the difference between conversation-driven drafting, generated design/planning, finalization, expansion, and implementation.
5. Developer can decide whether the workflow could help structure their own AI-assisted development process.

### 6.3 Visitor Reviews the Project as Portfolio Evidence

1. Visitor opens a case study or portfolio page.
2. Visitor sees why the project demonstrates practical engineering skill.
3. Visitor sees the creator’s role in designing the workflow.
4. Visitor sees links to GitHub and related public project material.
5. Visitor can determine whether the creator has relevant AI, SDLC, documentation, workflow design, and software planning skills.

### 6.4 Visitor Learns How to Use the SDLC Pipeline

1. Visitor opens a usage or getting-started page.
2. Visitor sees the command sequence for the normal workflow.
3. Visitor sees the fast path and mixed path options.
4. Visitor understands that user requirements start from conversation, while later PDR and plan stages may be drafted from conversation or generated from prior artifacts. The source instructions describe the conversation path, fast path, and mixed path as supported ways to move through the SDLC pipeline. 
5. Visitor understands where final documents and phase plans are produced.

### 6.5 Visitor Reviews Detailed Project Material

1. Visitor opens a deeper documentation or artifact page.
2. Visitor can inspect the public project materials.
3. Visitor can view examples of prompts, generated documents, or workflow artifacts.
4. Visitor can follow links to GitHub.
5. Visitor can optionally follow links to the creator’s broader portfolio or website.

## 7. Functional Requirements

| ID     | Requirement                                                                                                                                                                                         |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FR-001 | I2I shall be a multi-page static website.                                                                                                                                                           |
| FR-002 | I2I shall be publishable through GitHub Pages.                                                                                                                                                      |
| FR-003 | I2I shall eventually support hosting under `johnboen.com`.                                                                                                                                          |
| FR-004 | I2I shall link to the creator’s GitHub account, `bonjohen`.                                                                                                                                         |
| FR-005 | I2I shall allow the repository name to remain unspecified until selected later.                                                                                                                     |
| FR-006 | I2I shall explain the SDLC workflow from idea to implementation.                                                                                                                                    |
| FR-007 | I2I shall include a clear homepage that explains the project name, purpose, and value.                                                                                                              |
| FR-008 | I2I shall include a visual representation of the workflow.                                                                                                                                          |
| FR-009 | I2I shall include a workflow page explaining each major SDLC stage.                                                                                                                                 |
| FR-010 | I2I shall explain `draft-user`, `draft-pdr`, `draft-plan`, `gen-pdr`, `gen-plan`, `finalize`, `expand`, and `implement`.                                                                            |
| FR-011 | I2I shall explain the normal conversation-driven workflow.                                                                                                                                          |
| FR-012 | I2I shall explain the fast path.                                                                                                                                                                    |
| FR-013 | I2I shall explain the mixed path.                                                                                                                                                                   |
| FR-014 | I2I shall explain that `finalize` converts draft documents into final user requirements, final PDR, and final plan documents.                                                                       |
| FR-015 | I2I shall explain that `expand` creates one self-contained phase execution plan per phase after finalization. The corrected expand prompt specifies output files at `sdlc/plan/phase{NN}/plan.md`.  |
| FR-016 | I2I shall explain that `implement` executes phase plans, updates task status, verifies work, writes summaries, and commits completed phases.                                                        |
| FR-017 | I2I shall include an educational section explaining why each SDLC stage exists.                                                                                                                     |
| FR-018 | I2I shall include a marketing section explaining the value of the workflow.                                                                                                                         |
| FR-019 | I2I shall include a portfolio or case-study section showing why the project demonstrates the creator’s engineering ability.                                                                         |
| FR-020 | I2I shall keep the homepage and primary workflow explanation focused on the workflow rather than on the creator.                                                                                    |
| FR-021 | I2I shall expose more information about the creator only when visitors look for more detailed information.                                                                                          |
| FR-022 | I2I shall include public examples or excerpts from the project artifacts.                                                                                                                           |
| FR-023 | I2I shall treat all project materials as safe for public exposure.                                                                                                                                  |
| FR-024 | I2I shall support both manually authored website content and content derived from project markdown files.                                                                                           |
| FR-025 | I2I shall avoid exaggerated claims and keep the marketing tone credible, technical, and practical.                                                                                                  |
| FR-026 | I2I shall leave room for a future interactive demo without requiring one in the initial version.                                                                                                    |
| FR-027 | I2I shall be understandable without requiring the visitor to read the source repository first.                                                                                                      |

## 8. Initial Configuration

| Item                  | Initial Requirement                                                 |
| --------------------- | ------------------------------------------------------------------- |
| Site name             | `I2I — From Idea to Implementation`                                 |
| Site type             | Multi-page static website                                           |
| Publishing target     | GitHub Pages                                                        |
| GitHub account        | `bonjohen`                                                          |
| Repository name       | To be selected later                                                |
| Future domain         | `johnboen.com`                                                      |
| Content exposure      | Entire project may be publicly exposed                              |
| Initial interactivity | Static pages only; future interactive demo allowed but not required |
| Primary positioning   | Workflow first; creator information available in deeper pages       |
| Tone                  | Educational, technical, credible, and practical                     |

## 9. Non-Goals

The initial I2I website shall not:

1. Execute the SDLC workflow from the browser.
2. Provide a hosted SaaS version of the workflow.
3. Require user accounts.
4. Store visitor projects.
5. Accept visitor uploads.
6. Run coding agents.
7. Modify repositories.
8. Require a backend service.
9. Require an interactive demo.
10. Make the creator the dominant focus of the homepage.
11. Present AI-assisted SDLC as fully autonomous software development without human review.
12. Depend on the final GitHub repository name being known before design begins.

## 10. Privacy and Storage Expectations

I2I shall be a public static website.

The initial version shall not collect visitor project ideas, uploaded files, source code, private documents, or personal information.

The project materials themselves may be public. The website may expose prompts, documentation, examples, and generated artifacts from this SDLC project.

If analytics are added later, they should be minimal and disclosed.

## 11. Acceptance Criteria

| ID     | Acceptance Criterion                                                                                                                              |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| AC-001 | The site can be deployed as static pages through GitHub Pages.                                                                                    |
| AC-002 | The site can later be hosted under `johnboen.com`.                                                                                                |
| AC-003 | The homepage clearly identifies the project as **I2I — From Idea to Implementation**.                                                             |
| AC-004 | A first-time visitor can understand that I2I turns software ideas into implementation-ready SDLC artifacts.                                       |
| AC-005 | The site includes a clear visual workflow from idea to implementation.                                                                            |
| AC-006 | The site explains all major SDLC commands: `draft-user`, `draft-pdr`, `draft-plan`, `gen-pdr`, `gen-plan`, `finalize`, `expand`, and `implement`. |
| AC-007 | The site explains the conversation path, fast path, and mixed path.                                                                               |
| AC-008 | The site explains the role of final user requirements, final PDR, final plan, and per-phase execution plans.                                      |
| AC-009 | The site includes educational content explaining why the workflow is structured in stages.                                                        |
| AC-010 | The site includes marketing content explaining why the workflow is useful.                                                                        |
| AC-011 | The site includes a portfolio or case-study section.                                                                                              |
| AC-012 | The site links to `bonjohen` on GitHub.                                                                                                           |
| AC-013 | The site allows the repository name to be filled in later without redesigning the requirements.                                                   |
| AC-014 | The homepage focuses primarily on the workflow.                                                                                                   |
| AC-015 | More detailed creator information is available through deeper navigation or links.                                                                |
| AC-016 | The site does not require a backend service for the initial release.                                                                              |
| AC-017 | The site does not require an interactive demo for the initial release.                                                                            |
| AC-018 | The site presents the workflow as human-in-the-loop and does not overclaim full automation.                                                       |
| AC-019 | A technical reviewer can understand the project’s value without opening the GitHub repository.                                                    |
| AC-020 | A developer can determine how they would begin using the SDLC workflow after reading the site.                                                    |

## 12. Concerns for Physical Design

1. **Static site structure:** FR-001 and FR-002 require a multi-page static website deployable to GitHub Pages. The PDR should choose the specific static site approach and directory structure.

2. **GitHub Pages deployment:** FR-002 requires publishing through GitHub Pages. The PDR should decide whether deployment is manual, GitHub Actions based, or handled by the selected static site framework.

3. **Future custom domain:** FR-003 requires eventual hosting under `johnboen.com`. The PDR should leave room for custom-domain configuration without blocking the first deployment.

4. **Workflow diagram:** FR-008 requires a visual workflow. The PDR should choose an initial diagram implementation and allow later edits.

5. **Content source strategy:** FR-024 allows both manually authored content and content derived from markdown files. The PDR should decide which pages are manually written and which, if any, are generated from source markdown.

6. **Public artifact exposure:** FR-022 and FR-023 allow the project artifacts to be public. The PDR should decide how to expose those artifacts cleanly without overwhelming the main educational flow.

7. **Workflow-first positioning:** FR-020 and FR-021 require the site to focus on the workflow first and expose creator details only for visitors who want more information. The PDR should define navigation and page hierarchy accordingly.

8. **Marketing tone:** FR-018 and FR-025 require useful marketing without hype. The PDR should define page copy style, section headings, and claim boundaries.

9. **Repository link placement:** FR-004 and FR-005 require linking to `bonjohen` while leaving the repo name undecided. The PDR should define placeholders or configuration for repository links.

10. **Future interactivity:** FR-026 allows a later interactive demo. The PDR should avoid design choices that make future interactivity difficult, but the initial release should remain static.
