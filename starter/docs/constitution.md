# Meeting Action Tracker Constitution

Workshop MVP for Far East Hospitality (FEH), built with Spec-Driven
Development during the two-day session, 15–16 October 2026. One
constitution for both workshop tracks: MVP 1 (voice capture) and MVP 2
(meeting action tracker). What each track builds is in its run sheet,
docs/specs.md.
Source requirements: FEH "Meeting Action Tracker: Requirements",
13 Oct 2026. Data, labels and look: docs/reference.md.

## Core Principles

### I. Specification First

No code MUST be written without an approved specification.
Every acceptance criterion MUST have an ID of the form AC-<spec>-<nn> and
MUST describe behaviour a user can observe.
Specifications MUST NOT contain technology choices.

**Rationale**: FEH approves what is built before it is built. A
specification that names tables or frameworks hides the business decision
behind a technical one.

### II. Hotel Isolation

All meetings and action items MUST belong to exactly one hotel.
A person MUST only see and change data of the hotel they belong to.
Isolation MUST be enforced in one place, so no page, form or query can
return another hotel's data. Another hotel's data MUST behave as if it
does not exist.

**Rationale**: FEH NFR-001. Each property's data is separate; one
leaking query would break that promise for every hotel.

### III. Nothing Disappears

Action items MUST NOT be deleted; they are cancelled.
Every change to a meeting or an action item MUST be recorded with who,
when, the old value and the new value, from the first model onwards.
The record of changes MUST NOT be editable by users.

**Rationale**: FEH FR-014 and NFR-002. Any member can edit any item, so
the change record is the safeguard that makes open editing safe.

### IV. Synthetic Data Only

All hotels, people and actions MUST come from docs/reference.md.
No real FEH data, rates, forecasts or credentials MUST be used.

**Rationale**: The workshop runs on laptops outside FEH's environment.
Rate and forecast data is commercially sensitive even when invented.

### V. End-to-End Traceability

Every requirement MUST have acceptance criteria.
Every acceptance criterion MUST map to one or more automated tests whose
name contains its ID.
Traceability, not coverage percentage, is the test-sufficiency gate.

**Rationale**: At the demo FEH can point at any screen and ask "which
requirement is this, and what proves it?". The answer must be one click
away.

### VI. Test-First Development

Within each task, tests MUST be written before the code that satisfies
them, and MUST be seen to fail first.
Red → Green → Refactor.

**Rationale**: Tests written after the code tend to describe the code,
not the requirement.

### VII. Testing Pyramid

Most tests MUST be fast unit and integration tests (pytest).
End-to-end browser tests (Playwright) MUST be reserved for the main
meeting journey.

**Rationale**: Fast feedback during a one-day build; full-stack
confidence only where FEH will look.

### VIII. AI-Assisted Development Under Human Review

GitHub Copilot MAY generate specifications, plans, tasks and code.
A person MUST review every result before it is committed.
No task SHALL be phrased as "build the application".

**Rationale**: The agent is fast and confident, and sometimes wrong.
Review is where the participant adds value.

### IX. Single Capability Principle

Each specification, task and commit MUST deliver exactly one
demonstrable capability.
One spec = one commit = one capability on screen.
Each specification MUST be an increment on the ones before it in the
delivery order: it MUST state what it builds on, extend the working app
without rebuilding or restructuring what earlier specs delivered, and
leave every earlier acceptance test passing.

**Rationale**: Small capabilities can be approved, built, demonstrated
and rolled back one at a time, which is what lets the workshop stop at
any spec and still have something working. Building each spec on the
last means the app works after every spec, never only at the end.

### X. Built Through Spec Kit and GitHub Copilot

Every file MUST be produced through the Spec Kit cycle in GitHub Copilot
Agent mode.
Hand-written patches around the cycle are not permitted; if something is
wrong, the spec, plan or task is corrected and the agent re-runs it.

**Rationale**: The workshop is about the process. Hand fixes hide where
the specification was unclear.

### XI. Keep It Small

Only what an approved acceptance criterion asks for MUST be built. The
scope of each track is the approved specifications in its run sheet.
Microsoft Entra ID, emails, export, Teams transcripts, Databricks and
Azure hosting are out of scope for both tracks and MUST NOT be started.

**Rationale**: FEH's full requirements do not fit in two days. Each MVP
is chosen so it can be finished.

### XII. Change Through the Spec

When behaviour needs to change, the specification MUST be amended and
re-approved first, then the plan, tasks and code.
Code that does something no specification asks for is a defect.

**Rationale**: FEH stays in control of what the tracker does, even
mid-build.

### XIII. Stop and Report

After implementing a specification, the agent MUST stop and report what
was built, the test results, and any acceptance criterion it could not
satisfy.
It MUST NOT start the next specification unprompted.

**Rationale**: Each gate is a human decision.

### XIV. Demonstrability

Every specification MUST state what it looks like on screen.
A capability that cannot be shown in the final demo earns nothing.

**Rationale**: FEH judges the workshop by what it sees working.

### XV. AI Proposes, a Person Confirms

Anything an AI service produces in the app (a transcript, an extracted
action item) MUST be saved as Proposed and shown to a person.
Only a person MUST be able to confirm it; nothing becomes Confirmed
without that action.
The app MUST say which items came from AI until they are confirmed.

**Rationale**: AI extraction is fast and usually right, and sometimes
confidently wrong. The chair stays accountable for every action the
meeting records. Applies wherever the app calls an AI service.

### XVI. Secrets Stay Out of the Code

Keys and endpoints MUST only be read from environment variables (a
.env file that is listed in .gitignore).
Keys MUST NOT be committed, written in a spec, pasted in a chat, or
shown on screen.
The app MUST run, and every test MUST pass, with no keys at all.

**Rationale**: A leaked key is a security incident and a bill. A
workshop app that only runs with keys cannot be demonstrated when the
network or the key fails.

## Technology Standards

### Application

- **Framework**: Python 3.12+ with Django 5. Server-rendered Django
  templates and plain CSS. No React, no separate frontend, no REST API.
- **Interactivity**: HTMX only for spreadsheet-style editing (MVP 2,
  spec 006), following FEH's architecture. Served from the project's
  static files, never a CDN. Recording in MVP 1 uses the browser's own
  MediaRecorder in a small script on the Record page.
- **AI services (MVP 1)**: Azure OpenAI, called only behind two
  adapters: transcribe(audio) returns text, and extract(transcript)
  returns action items as JSON. AI_PROVIDER selects the implementation:
  "sample" (default; returns docs/sample/transcript.txt and
  docs/sample/items.json) or "azure" (uses AZURE_OPENAI_ENDPOINT,
  AZURE_OPENAI_KEY, AZURE_OPENAI_TRANSCRIBE_DEPLOYMENT and
  AZURE_OPENAI_CHAT_DEPLOYMENT). Tests always use "sample".
- **Database**: SQLite (stands in for Azure Database for PostgreSQL).
- **Dependencies**: managed with uv.
- **Change record**: django-simple-history on every tracked model.
- **Sign-in**: Django authentication behind a "Sign in as" page that
  stands in for Microsoft Entra ID, kept in one place so Entra ID can
  replace it.
- **Time**: stored in UTC, shown in the hotel's time zone.
- **Layout**: manage.py at the repository root, Django project
  "tracker_site", one app "tracker", Playwright tests in e2e/.
- **Seed**: a management command, seed_demo, clears the database and
  loads exactly the data in docs/reference.md that the built specs need.

### Visual Design

The look follows FEH's own screen mockups (docs/mockup/). Screens are
built to VISEO's HTML mockups of the MVP (docs/mockup/mvp-app.html, the
whole MVP as one clickable app, and mvp-*.html), which use exactly these
tokens. Palette is fixed; colour carries meaning, never
decoration.

| Token        | Hex     | Meaning                         |
|--------------|---------|---------------------------------|
| Page         | #F3F5F7 | Page background                 |
| Card         | #FFFFFF | Card and table surface          |
| Top bar      | #0E2A33 | Top bar, white text             |
| Ink          | #14202B | Primary text                    |
| Muted        | #5B6670 | Secondary text                  |
| Primary      | #0F6B6B | Primary buttons                 |
| Overdue      | #B42318 | Overdue text only               |
| Carried row  | #EAF0F3 | "Carried forward" group heading |
| Raised row   | #E3F1F0 | "Raised in this meeting" heading |

Font: Inter. Buttons and inputs at least 40px tall. Exact labels are in
docs/reference.md.

### Testing Tools

- **Rules, pages and forms**: pytest with pytest-django.
- **Journey**: Playwright (TypeScript) in e2e/, against the running
  server with seed_demo loaded. HTML report and screenshots.

## Development Workflow

```
FEH requirement
  → Specification   (/speckit-specify)
  → Clarify         (/speckit-clarify)        → G1  FEH approves the spec
  → Plan            (/speckit-plan)
  → Tasks           (/speckit-tasks)
  → Analyze         (/speckit-analyze)        → G2  VISEO approves plan and tasks
  → Implement       (/speckit-implement, tests first)
  → Converge        (/speckit-converge)       → G3  FEH and VISEO accept
  → Commit          (one spec, one commit)
```

## Definition of Done

A specification is complete only when all of the following are true:

- [ ] Specification approved at G1 by the FEH product owner
- [ ] Plan and tasks approved at G2 by the VISEO technical lead
- [ ] All tasks completed
- [ ] Every earlier specification's tests still pass
- [ ] pytest passes
- [ ] Playwright passes for any journey the spec touches
- [ ] Every acceptance criterion has a test whose name contains its ID
- [ ] The capability was shown on screen and accepted at G3
- [ ] Committed as one commit for the spec

## Governance

This constitution supersedes all other practices for this project.
Amendments require a stated reason, a version bump (MAJOR for removed or
redefined principles, MINOR for added principles or sections, PATCH for
wording), and agreement of FEH and VISEO in the room before they are
committed.

All specifications, plans, tasks and code are subject to this
constitution. Non-compliance found during review MUST be raised before
the artefact is committed.

**Version**: 1.2.0 | **Ratified**: 2026-10-15 | **Last Amended**: 2026-10-15
