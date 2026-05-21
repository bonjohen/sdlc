---
title: "Finalize Prompt — Gap Checklist"
type: "prompt"
command: "finalize"
excerpt: true
sortOrder: 1
---

The `finalize` command reads three draft documents and produces three final documents. Each step applies a gap checklist to catch what the draft author missed. Here is the User Requirements gap checklist from the actual prompt:

**Personas and actors**
- Are all user roles identified? (end user, admin, system/cron, API consumer, reviewer)
- Is there a "system" actor for automated processes (scheduled imports, background jobs, migrations)?
- Are there external systems that act as users? (webhooks, CI/CD, monitoring)

**Non-functional requirements (almost always missing from drafts)**
- Performance targets — response time, throughput, batch size limits
- Data volume expectations — how many records in year 1? Year 3?
- Availability — is downtime acceptable? For how long?
- Security — authentication, authorization, input validation, secrets management
- Accessibility — WCAG level, keyboard navigation, screen reader support

**Edge cases and error states**
- What happens when an external API is down?
- What happens when the database is full or corrupt?
- What happens when two users edit the same thing?
- What happens on first run with no data?
