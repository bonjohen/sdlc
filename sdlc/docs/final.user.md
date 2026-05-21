---
document: "User Requirements"
version: "1.0"
status: "final"
source: "sdlc/docs/draft.user.md"
finalized_date: "2026-05-21"
---

# I2I — From Idea to Implementation — User Requirements

## 1. Overview

I2I is a multi-page static website that explains, teaches, and markets a prompt-driven software development life cycle (SDLC) workflow. The workflow moves a software idea through structured stages — user requirements, Product Design Review (PDR), phased release plan, finalized documents, per-phase execution plans, and implementation — using AI-assisted prompts at each stage.

The site serves three simultaneous purposes. First, it is an educational resource that teaches developers how the SDLC workflow operates and why each stage exists. Second, it is a marketing page that presents the workflow as a practical, human-in-the-loop approach to AI-assisted software development. Third, it is a portfolio artifact that demonstrates the creator's ability to design AI-assisted development workflows, organize software projects, and communicate reusable engineering processes.

The site targets GitHub Pages deployment, with eventual hosting under `johnboen.com`. All project materials — prompts, generated documents, and workflow artifacts — are treated as safe for public exposure. The initial release is entirely static; no backend, no user accounts, no interactive demo. Future interactivity is allowed but not required.

## 2. Personas

### 2.1 First-Time Visitor

- **Role:** Someone who arrives at the site with no prior knowledge of I2I or the SDLC workflow. May have found it through a link, search engine, or portfolio reference.
- **Goals:** Quickly understand what I2I is, what the workflow does, and whether it is worth exploring further.
- **Technical level:** Varies (novice to expert). The homepage must be understandable without deep technical knowledge.

### 2.2 Software Developer

- **Role:** A practicing developer evaluating whether the SDLC workflow could help structure their own AI-assisted development process.
- **Goals:** Understand each workflow stage, what it consumes and produces, the difference between conversation-driven and generated paths, and how to get started using the pipeline.
- **Technical level:** Intermediate to expert. Comfortable with CLI tools, markdown, and AI-assisted development concepts.

### 2.3 Technical Reviewer / Hiring Manager

- **Role:** Someone evaluating the creator's engineering skills through this project. May be a hiring manager, recruiter, or technical interviewer.
- **Goals:** Determine whether the project demonstrates relevant skills in AI workflow design, SDLC methodology, documentation, and software planning. Find links to GitHub and related materials.
- **Technical level:** Intermediate to expert. Reads for evidence of engineering judgment, not just code output.

### 2.4 Potential Collaborator

- **Role:** A technical peer, open-source contributor, or potential client considering working with the creator.
- **Goals:** Understand the project deeply enough to assess collaboration fit. Review artifacts, source materials, and the creator's broader portfolio.
- **Technical level:** Intermediate to expert.

<!-- Added during finalization: draft Section 3 names these audiences but does not define them as personas with roles, goals, and technical levels. -->

### 2.5 GitHub Pages Build System

- **Role:** Automated system actor. Builds and deploys the static site from the repository.
- **Goals:** Successfully build the site from source, deploy to the GitHub Pages hosting environment.
- **Technical level:** N/A (automated).

<!-- Added during finalization: FR-002 requires GitHub Pages publishing, which implies a system actor for the build/deploy pipeline. -->

## 3. User Stories

### 3.1 First Impression and Orientation

| ID | As a... | I want to... | So that... | Priority | Acceptance Criteria |
|----|---------|-------------|-----------|----------|-------------------|
| US-001 | First-Time Visitor | see the project name and a concise explanation on the homepage | I immediately understand what I2I is without scrolling or clicking | Must | Homepage displays "I2I — From Idea to Implementation" and a 1-3 sentence explanation above the fold |
| US-002 | First-Time Visitor | see a visual workflow diagram on the homepage | I can grasp the full pipeline at a glance | Must | A diagram showing Idea → User Requirements → PDR → Plan → Finals → Phase Plans → Implementation is visible on the homepage |
| US-003 | First-Time Visitor | choose to learn the workflow, review examples, or learn about the creator | I can follow the path most relevant to me | Must | Homepage provides navigation links or calls-to-action for at least these three paths |
| US-004 | First-Time Visitor | understand the project without reading the source repository | I can evaluate I2I on its own merits from the website alone | Must | The site explains the workflow end-to-end; no page requires the visitor to open GitHub to make sense of the content |

### 3.2 Workflow Education

| ID | As a... | I want to... | So that... | Priority | Acceptance Criteria |
|----|---------|-------------|-----------|----------|-------------------|
| US-005 | Software Developer | see all SDLC stages explained in order on a workflow page | I understand the full pipeline sequence | Must | A dedicated page lists each stage with its purpose, input, and output |
| US-006 | Software Developer | understand what each command does (`draft-user`, `draft-pdr`, `draft-plan`, `gen-pdr`, `gen-plan`, `finalize`, `expand`, `implement`) | I know which command to use at each stage | Must | Each of the 8 commands is explained with its role, input, and output |
| US-007 | Software Developer | understand the conversation path, fast path, and mixed path | I know the different ways to move through the pipeline | Must | All three paths are explained, showing when and why to use each |
| US-008 | Software Developer | understand what `finalize` produces and why | I know the role of final documents vs. drafts | Must | The site explains that finalize converts draft.user, draft.pdr, and draft.plan into final versions with gap analysis and traceability |
| US-009 | Software Developer | understand what `expand` produces | I know that per-phase execution plans are self-contained | Must | The site explains that expand generates `sdlc/plan/phase{NN}/plan.md` files, each containing everything needed to implement that phase |
| US-010 | Software Developer | understand what `implement` does | I know how phases are executed, tracked, and committed | Must | The site explains that implement executes phase plans, updates task status, verifies work, writes summaries, and commits completed phases |
| US-011 | Software Developer | read educational content explaining why the workflow is structured in stages | I understand the reasoning, not just the mechanics | Must | An educational section or page explains the rationale for staged document production, gap surfacing, traceability, and phased execution |

### 3.3 Getting Started

| ID | As a... | I want to... | So that... | Priority | Acceptance Criteria |
|----|---------|-------------|-----------|----------|-------------------|
| US-012 | Software Developer | see the command sequence for the normal workflow | I know where to start and what order to run things | Must | A usage or getting-started page shows the step-by-step command sequence |
| US-013 | Software Developer | determine how to begin using the SDLC workflow after reading the site | I can adopt the workflow for my own projects | Must | The site provides enough information for a developer to start a new project using the pipeline without additional documentation |

### 3.4 Portfolio and Case Study

| ID | As a... | I want to... | So that... | Priority | Acceptance Criteria |
|----|---------|-------------|-----------|----------|-------------------|
| US-014 | Technical Reviewer | see a portfolio or case-study section | I can evaluate the creator's engineering ability through this project | Must | A dedicated page or section explains what the project demonstrates and the creator's role |
| US-015 | Technical Reviewer | find links to the creator's GitHub (`bonjohen`) | I can review source code and related projects | Must | At least one link to `github.com/bonjohen` is accessible from the portfolio section |
| US-016 | Technical Reviewer | understand the project's value without opening the GitHub repository | I can form an opinion from the website alone | Must | The portfolio section explains the project's significance, design decisions, and scope without requiring external reading |
| US-017 | Potential Collaborator | follow links to the creator's broader portfolio or website | I can assess collaboration fit beyond this single project | Should | Links to the creator's other public materials are available from deeper pages |

### 3.5 Artifact Exposure

| ID | As a... | I want to... | So that... | Priority | Acceptance Criteria |
|----|---------|-------------|-----------|----------|-------------------|
| US-018 | Software Developer | view examples or excerpts from prompts, generated documents, or workflow artifacts | I can see what the pipeline actually produces | Must | The site includes at least one example of a prompt and at least one example of a generated artifact |
| US-019 | Software Developer | inspect public project materials on deeper pages | I can review the details without them cluttering the main educational flow | Should | Artifact examples are accessible from deeper pages or expandable sections, not embedded inline in the primary workflow explanation |

### 3.6 Content Management

| ID | As a... | I want to... | So that... | Priority | Acceptance Criteria |
|----|---------|-------------|-----------|----------|-------------------|
| US-020 | GitHub Pages Build System | build and deploy the site from the repository automatically | the site is published without manual intervention after each push | Must | A push to the deployment branch triggers a GitHub Pages build that produces the live site |
| US-021 | Software Developer | author content both manually and from project markdown files | the site can include hand-written pages alongside content derived from SDLC artifacts | Should | The site framework supports both hand-authored pages and markdown-sourced content in the same build |

<!-- Added during finalization: FR-002 and FR-024 imply build/deploy automation and dual content sourcing as user-level needs, not just implementation details. -->

### 3.7 Site Navigation and Information Architecture

| ID | As a... | I want to... | So that... | Priority | Acceptance Criteria |
|----|---------|-------------|-----------|----------|-------------------|
| US-022 | First-Time Visitor | find the workflow explanation as the primary focus of the homepage and top-level navigation | I am not distracted by creator biography on first arrival | Must | The homepage leads with the workflow; creator information is reachable through secondary navigation or deeper pages |
| US-023 | Technical Reviewer | find creator information through deeper navigation | I can learn about the person behind the project when I choose to | Must | Creator details are available within 1-2 clicks from the homepage, but do not dominate the homepage or primary navigation |

<!-- Added during finalization: FR-020 and FR-021 define a workflow-first / creator-secondary hierarchy that needs explicit user stories to trace against. -->

## 4. Non-Functional Requirements

| ID | Category | Requirement | Target | Priority |
|----|----------|------------|--------|----------|
| NFR-001 | Performance | Pages shall load quickly on standard broadband connections | Largest Contentful Paint < 2.5s on a 10 Mbps connection | Must |
| NFR-002 | Performance | The site shall function without JavaScript where possible | Core content (text, navigation, diagrams) is readable with JS disabled; progressive enhancement for any interactive features | Should |
| NFR-003 | Accessibility | The site shall be navigable by keyboard and screen reader | WCAG 2.1 Level AA compliance for all pages | Should |
| NFR-004 | Accessibility | Text shall have sufficient contrast against backgrounds | Contrast ratio >= 4.5:1 for body text, >= 3:1 for large text (WCAG AA) | Should |
| NFR-005 | Responsiveness | The site shall be usable on mobile, tablet, and desktop screens | All pages render correctly from 320px to 2560px viewport width | Must |
| NFR-006 | SEO | Pages shall be discoverable by search engines | Each page has a unique `<title>`, `<meta description>`, semantic HTML headings, and an auto-generated sitemap | Should |
| NFR-007 | Availability | The site shall be available whenever GitHub Pages is available | No additional uptime requirement beyond GitHub Pages SLA (~99.9%) | Must |
| NFR-008 | Deployment | The site shall deploy automatically on push to the deployment branch | GitHub Pages build completes and publishes within 5 minutes of push | Must |
| NFR-009 | Maintainability | Adding a new page shall not require modifying more than 2 files | New content page + navigation config update only | Should |
| NFR-010 | Portability | The site shall support custom domain hosting without structural changes | Adding a CNAME file and DNS configuration is sufficient to serve under `johnboen.com` | Must |

<!-- Added during finalization: the draft had no non-functional requirements. These are derived from FR-001 (static site), FR-002 (GitHub Pages), FR-003 (custom domain), FR-005 (repo name flexibility), and standard web accessibility and performance expectations for a public portfolio site. -->

## 5. Constraints and Assumptions

- **Static only.** The initial release has no backend, no server-side processing, and no database. All content is pre-built at deploy time. (FR-001, Non-Goals 2, 8)
- **GitHub Pages hosting.** The site must conform to GitHub Pages build and deployment constraints. If a static site generator is used, it must be one GitHub Pages supports natively or via GitHub Actions. (FR-002)
- **No user-generated content.** The site does not accept uploads, form submissions (beyond a potential contact link), or visitor data. (Non-Goals 3, 4, 5)
- **Repository name TBD.** All repository links must use a configurable placeholder or variable, not a hardcoded repo name. (FR-005)
- **Public materials.** All SDLC project artifacts — prompts, drafts, finals, plan files — are safe for public exposure. No redaction is needed. (FR-023)
- **Human-in-the-loop framing.** All marketing and educational content must present the workflow as AI-assisted with human review, not as fully autonomous. (FR-025, Non-Goal 11)
- **English only.** The initial release assumes English-language content. Internationalization is not in scope.

<!-- Added during finalization: "English only" and "no user-generated content" are implied by the draft but not stated as explicit constraints. -->

## 6. Out of Scope

The following are explicitly excluded from the initial release. They may be considered for future iterations.

- Executing the SDLC workflow from the browser (Non-Goal 1)
- Hosted SaaS version of the workflow (Non-Goal 2)
- User accounts or authentication (Non-Goal 3)
- Visitor data storage or project uploads (Non-Goals 4, 5)
- Running coding agents from the site (Non-Goal 6)
- Repository modification from the site (Non-Goal 7)
- Backend services (Non-Goal 8)
- Interactive demo (Non-Goal 9; FR-026 reserves room for a future demo)
- Analytics or visitor tracking (Section 10 allows minimal analytics later, but not in initial release)
- Multi-language / internationalization support
- Offline or PWA support
- Blog, changelog, or time-series content
- Comments, feedback forms, or visitor interaction beyond outbound links

<!-- Added during finalization: analytics deferral, i18n, offline/PWA, blog, and feedback forms are not mentioned in the draft but are common scope-creep vectors for portfolio sites. Listing them here prevents ambiguity. -->
