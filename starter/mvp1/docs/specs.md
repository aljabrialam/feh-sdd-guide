# Meeting Action Tracker · MVP 1 Voice Capture — All Specs

Complete set, in execution order. Every block is paste-ready.
FEH requirements: "Meeting Action Tracker: Requirements", 13 Oct 2026.
Governing rules: docs/constitution.md. Data, labels and look:
docs/reference.md. Target screens: docs/mockup/. FEH's sequence:
docs/voice-capture-sequence.mmd; ours, spec by spec:
docs/mvp-sequence.mmd. Sample AI output: docs/sample/.

---

# SETUP — done in Step 1 of the guide

```bash
mkdir -p ~/Desktop/feh-sdd && cd ~/Desktop/feh-sdd   # Windows: see Step 1 in the guide
specify init feh-app --integration copilot
cd feh-app
# docs pack: docs/constitution.md, docs/specs.md, docs/reference.md
git init -b main && git add -A && git commit -m "chore: spec kit and workshop docs"
code .
```

Then open Copilot Chat in **Agent** mode and paste the constitution:

```
/speckit-constitution

Adopt docs/constitution.md as this project's constitution, exactly as
written: every principle, the Technology Standards, the
Development Workflow, the Definition of Done and Governance.
```

---

# WORKING RULES

Everything that produces a file goes through GitHub Copilot, driven by
the Spec Kit cycle. Not hand-edited around it (Principle X).

**Keep it small is not negotiable mid-build.** If a task seems to need
Entra ID, emails, export or Teams, the task is wrong, not the scope
(Principle XI).

**FEH decides business rules.** When clarify asks a business question,
the FEH product owner answers it in the room and everyone uses the same
answer.

Commit after every spec. One spec, one commit, one demonstrable
capability.

---

## How to run each spec

```
/speckit-specify → /speckit-clarify                       G1  FEH approves
/speckit-plan → /speckit-tasks → /speckit-analyze         G2  VISEO approves
/speckit-implement (tests first) → /speckit-converge      G3  FEH and VISEO accept
git commit
```

Day 1 afternoon: draft, compare, specify and clarify 001–006; G1 for
all six. Late Day 1: execute 001. Day 2: execute 002–006 in order;
007 only if time allows. Azure OpenAI is optional: everything runs and
every test passes with AI_PROVIDER=sample (Principle XVI).

---

## Delivery order and stop lines

Build in this order. Each spec is an increment: it builds on the specs
before it and leaves the app working. Each line marks what you have if
you stop there.

| Order | Spec | Builds on | When | If you stop here |
|---|---|---|---|---|
| 1 | 001 Workshop Sign-in and Hotel Access | Nothing | Late Day 1 | People sign in and see only their own hotel. Isolation exists before any data does. |
| 2 | 002 Weekly Meetings | 001 | Day 2, 9:00 | Meetings can be created and listed. The weekly meeting exists in the tracker. |
| 3 | 003 Action Items in a Meeting | 002 | Day 2, 9:45 | Actions are recorded with an owner and a due date. The spreadsheet could be retired. |
| 4 | 004 Record and Transcribe | 003 | Day 2, 10:30 | The meeting can be recorded and turned into text on screen. |
| 5 | 005 Extract Proposed Action Items | 004 | Day 2, 11:30 | The transcript becomes proposed action items, ready for the chair. |
| 6 | 006 Review and Confirm Proposed Items | 005 | Day 2, 1:30 | Speak, review, confirm: the voice-capture MVP is complete. |
| 7 | 007 Carry Forward and Overdue (stretch) | 003 | Day 2 stretch | Open items carry forward and late ones stand out. |

**Minimum viable demonstration: through 006** (speak, review, confirm).
007 is a stretch goal, only after 006 is accepted.

---

# CONNECT AZURE OPENAI (optional, when FEH provides the values)

Create a file named .env in the project root (it is in .gitignore; never
commit it, never paste the key in chat):

```
AI_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://<feh-resource>.openai.azure.com
AZURE_OPENAI_KEY=<key>
AZURE_OPENAI_TRANSCRIBE_DEPLOYMENT=<transcription deployment name>
AZURE_OPENAI_CHAT_DEPLOYMENT=<chat deployment name>
```

Restart the app. To go back to the sample, set AI_PROVIDER=sample.

---

# 001 — Workshop Sign-in and Hotel Access

## Specify and clarify (G1)

```
/speckit-specify

Create a Feature Specification.

Feature ID
001-sign-in-hotel-access

Feature Name
Workshop Sign-in and Hotel Access

Business Goal
Let each person enter the tracker as themselves and see only their
own hotel, standing in for Microsoft Entra ID during the workshop.

Business Value
Every later feature depends on knowing who the person is and which
hotel they belong to. FEH's requirements make hotel isolation a core
rule (NFR-001), so it is built first, before any meeting or action
exists.

Business Actors
Hotel team member

Business Capability
Access and Hotel Isolation

Reference
docs/reference.md "Hotels" and "People". FEH requirements FR-003
(Entra ID, stubbed for the workshop), FR-013, NFR-001.

Builds On
Nothing: this is the foundation. It sets up the project, sign-in and
hotel isolation that every later spec reuses.

Functional Requirements

FR-001 The system shall present a sign-in page that lists every person in
docs/reference.md with their name and hotel; choosing a person signs
them in as that person.

FR-002 The system shall state on the sign-in page that it is a workshop
stand-in and that Microsoft Entra ID replaces it in the real product.

FR-003 The system shall show the signed-in person's name and hotel on every
page, with a way to sign out.

FR-004 The system shall require sign-in for every page except the sign-in
page.

FR-005 The system shall only ever show a person data that belongs to their
own hotel. Anything belonging to another hotel shall behave as if it
does not exist.

Non-Functional Requirements

Isolation shall be enforced in one place, not page by page.

What It Looks Like On Screen
The sign-in page with one button per person; after choosing Mary Tan,
the top bar shows "Mary Tan · Hotel A" and "Sign out".

Out of Scope
Passwords, roles, Microsoft Entra ID, meetings (002).

Label every acceptance criterion AC-001-<nn>.
Generate the specification following the GitHub Spec Kit format.
Do not generate implementation details.
Do not generate source code.
```

```
/speckit-clarify

Review Feature Specification 001-sign-in-hotel-access.

Identify missing requirements, ambiguity, assumptions, missing
validation, missing error handling, missing non-functional
requirements, and missing acceptance criteria.

Give particular attention to:
- A person types the address of a page that belongs to another hotel.
- A person signs out and presses the browser's Back button.
- Someone in the room asks for a person who belongs to two hotels
  (not in the workshop: each person belongs to one hotel).

Review every functional requirement. Suggest improvements. Update the
specification where necessary. Make sure every acceptance criterion has
an ID AC-001-<nn> and describes behaviour a person can observe.

When a question is about a business rule, wait for the answer FEH gives
in the room. Do not invent business rules.

Do not generate implementation. Do not generate source code.
```

## Execute (G2, G3)

```
/speckit-plan

Plan Feature Specification 001-sign-in-hotel-access, following the constitution's
Technology Standards exactly.

This spec is an increment (Principle IX). It builds on: Nothing: this is the foundation. It sets up the project, sign-in and hotel isolation that every later spec reuses.
Reuse what is there; do not rebuild or restructure it. Every earlier
spec's tests must still pass.

This is the first feature, so it includes the project set-up from the
constitution's Technology Standards: manage.py at the repository root,
the Django project "tracker_site" and app "tracker", uv, pytest with
pytest-django, and Playwright in e2e/.
Add hotels and people with seed_demo loading exactly the "Hotels" and
"People" sections of docs/reference.md. Build the "Sign in as" page and
the top bar like the sign-in page of docs/mockup/mvp-app.html, with the labels and look
in docs/reference.md. Put hotel
isolation in one place (a hotel-scoped manager and a view mixin) that
every later feature will reuse.

Check the result against docs/mockup/mvp-app.html, the whole MVP as a
clickable mockup.

Map every acceptance criterion to at least one test whose name
contains its ID. Write data-model.md and the page contract in
contracts/ (each page and form: address, who may use it, what it
shows) before any code.
```

```
/speckit-tasks

Break the plan for 001-sign-in-hotel-access into small tasks, one demonstrable capability
each (Principle IX). In every task, write the tests first and see them
fail (Principle VI). Name every test after the acceptance criterion it
proves. Mark tasks that can run in parallel.
```

```
/speckit-analyze
```

```
/speckit-implement

Implement 001-sign-in-hotel-access task by task. After each task run the tests. When all
tasks are done, run pytest and Playwright, then stop and report what was
built, the test results, and any acceptance criterion you could not
satisfy (Principle XIII). Do not start the next specification.
```

```
/speckit-converge
```

```bash
git add -A
git commit -m "feat: 001-sign-in-hotel-access"
```

---

# 002 — Weekly Meetings

## Specify and clarify (G1)

```
/speckit-specify

Create a Feature Specification.

Feature ID
002-weekly-meetings

Feature Name
Weekly Meetings

Business Goal
Let a team member create the weekly performance meeting for their
hotel and see all of their hotel's meetings.

Business Value
Each action in FEH's spreadsheet belongs to a meeting date. Meetings
are the container every action is raised in.

Business Actors
Hotel team member
Meeting chair

Business Capability
Meeting Management

Reference
docs/reference.md "Meetings in the seed" and "Screens and exact
labels". FEH requirements FR-004, FR-021.

Builds On
001: people sign in and see only their own hotel. Every meeting
belongs to the signed-in person's hotel through 001's isolation.

Functional Requirements

FR-001 The system shall let a person create a meeting for their hotel with a
date, a time, a title (default "Weekly performance meeting"), a chair
and attendees chosen from the hotel's people, and optionally a Teams
meeting link.

FR-002 The system shall allow only one meeting per hotel per date, and shall
tell the person when the date is already taken.

FR-003 The system shall list the hotel's meetings, newest first, each with
its date, title and chair.

FR-004 The system shall show a meeting's title, date and time, chair,
attendees and Teams meeting link when it is opened.

FR-005 The system shall record who created a meeting and every later change
to it (Constitution Principle III).

Non-Functional Requirements

Dates and times shall be shown in the hotel's time zone.

What It Looks Like On Screen
Meetings shows the three seeded Hotel A meetings, newest first. "New
meeting" creates today's meeting, which then opens with its heading
and attendee chips.

Out of Scope
Action items (003), recording (004), completing a meeting.

Label every acceptance criterion AC-002-<nn>.
Generate the specification following the GitHub Spec Kit format.
Do not generate implementation details.
Do not generate source code.
```

```
/speckit-clarify

Review Feature Specification 002-weekly-meetings.

Identify missing requirements, ambiguity, assumptions, missing
validation, missing error handling, missing non-functional
requirements, and missing acceptance criteria.

Give particular attention to:
- A meeting created for a date in the past or far in the future.
- The chair is not one of the attendees.
- A Teams meeting link that is not a web address.
- Two people create a meeting for the same date at the same time.

Review every functional requirement. Suggest improvements. Update the
specification where necessary. Make sure every acceptance criterion has
an ID AC-002-<nn> and describes behaviour a person can observe.

When a question is about a business rule, wait for the answer FEH gives
in the room. Do not invent business rules.

Do not generate implementation. Do not generate source code.
```

## Execute (G2, G3)

```
/speckit-plan

Plan Feature Specification 002-weekly-meetings, following the constitution's
Technology Standards exactly.

This spec is an increment (Principle IX). It builds on: 001: people sign in and see only their own hotel. Every meeting belongs to the signed-in person's hotel through 001's isolation.
Reuse what is there; do not rebuild or restructure it. Every earlier
spec's tests must still pass.

Extend the project from 001; do not change its stack. Add the meeting
with django-simple-history, scoped to the hotel through 001's isolation.
Meetings list and "New meeting" form like the Meetings and New meeting
pages of docs/mockup/mvp-app.html, with the exact labels in docs/reference.md; seed_demo also loads the seeded meetings.

Check the result against docs/mockup/mvp-app.html, the whole MVP as a
clickable mockup.

Map every acceptance criterion to at least one test whose name
contains its ID. Write data-model.md and the page contract in
contracts/ (each page and form: address, who may use it, what it
shows) before any code.
```

```
/speckit-tasks

Break the plan for 002-weekly-meetings into small tasks, one demonstrable capability
each (Principle IX). In every task, write the tests first and see them
fail (Principle VI). Name every test after the acceptance criterion it
proves. Mark tasks that can run in parallel.
```

```
/speckit-analyze
```

```
/speckit-implement

Implement 002-weekly-meetings task by task. After each task run the tests. When all
tasks are done, run pytest and Playwright, then stop and report what was
built, the test results, and any acceptance criterion you could not
satisfy (Principle XIII). Do not start the next specification.
```

```
/speckit-converge
```

```bash
git add -A
git commit -m "feat: 002-weekly-meetings"
```

---

# 003 — Action Items in a Meeting

## Specify and clarify (G1)

```
/speckit-specify

Create a Feature Specification.

Feature ID
003-action-items

Feature Name
Action Items in a Meeting

Business Goal
Let a team member record each action agreed in the meeting, with its
owner, due date and what it is expected to achieve, and change it later.

Business Value
This replaces FEH's spreadsheet columns (issue, action required,
owner, due date, status) and adds market segment, issue category and
priority, so every action has an owner and a due date (FEH success
measure: 100%).

Business Actors
Hotel team member
Action owner

Business Capability
Action Tracking

Reference
docs/reference.md "Lists" and "Action items in the seed";
the meeting screen and Add action form of
docs/mockup/mvp-app.html. FEH requirements FR-007, FR-008,
FR-009, FR-013, FR-014.

Builds On
002: actions are added to a meeting. 001: owners are people of the
same hotel.

Functional Requirements

FR-001 The system shall let a person add an action to a meeting with a market
segment, an issue category, the issue, the action required, an owner
from the same hotel, a priority, a due date, a status and, optionally,
an anticipated result.

FR-002 The system shall require segment, category, issue, action required,
owner and due date, and shall tell the person which is missing. Issue,
action required and anticipated result are at most 300 characters.

FR-003 The system shall default priority to Medium and status to Open, using
the fixed lists in docs/reference.md.

FR-004 The system shall let a person edit any action of their hotel.

FR-005 The system shall list a meeting's actions with all their values, the
owner's name, and the anticipated result as "Expected: <text>".

FR-006 The system shall never delete an action; setting it to Cancelled is
the way to remove it, and every change is recorded (Constitution
Principle III).

Non-Functional Requirements

The meeting page shall stay fast with 100 actions.

What It Looks Like On Screen
On today's meeting, "Add action" records "December corporate pace
behind last year", owner Alex Wong, expected "December corporate pickup
back to last year's pace". It appears in the list with "Expected: …";
"Edit" changes its status to In progress.

Out of Scope
Recording (004), extraction (005), review (006), carry forward and
overdue (007).

Label every acceptance criterion AC-003-<nn>.
Generate the specification following the GitHub Spec Kit format.
Do not generate implementation details.
Do not generate source code.
```

```
/speckit-clarify

Review Feature Specification 003-action-items.

Identify missing requirements, ambiguity, assumptions, missing
validation, missing error handling, missing non-functional
requirements, and missing acceptance criteria.

Give particular attention to:
- The owner is not one of the meeting's attendees.
- The due date is already in the past when the action is created.
- An action is set straight to Done or Cancelled when it is created.
- Two people edit the same action at the same time.

Review every functional requirement. Suggest improvements. Update the
specification where necessary. Make sure every acceptance criterion has
an ID AC-003-<nn> and describes behaviour a person can observe.

When a question is about a business rule, wait for the answer FEH gives
in the room. Do not invent business rules.

Do not generate implementation. Do not generate source code.
```

## Execute (G2, G3)

```
/speckit-plan

Plan Feature Specification 003-action-items, following the constitution's
Technology Standards exactly.

This spec is an increment (Principle IX). It builds on: 002: actions are added to a meeting. 001: owners are people of the same hotel.
Reuse what is there; do not rebuild or restructure it. Every earlier
spec's tests must still pass.

Extend the project; do not change its stack. Add the action item with
django-simple-history, belonging to the meeting it was raised in and
scoped to the hotel through 001's isolation, including the optional
anticipated result. "Add action" and "Edit" are ordinary Django forms
on the meeting page, like docs/mockup/mvp-app.html. Keep the form's
validation in one place: spec 006 reuses it for proposed items.
seed_demo also loads the seeded actions.

Check the result against docs/mockup/mvp-app.html, the whole MVP as a
clickable mockup.

Map every acceptance criterion to at least one test whose name
contains its ID. Write data-model.md and the page contract in
contracts/ (each page and form: address, who may use it, what it
shows) before any code.
```

```
/speckit-tasks

Break the plan for 003-action-items into small tasks, one demonstrable capability
each (Principle IX). In every task, write the tests first and see them
fail (Principle VI). Name every test after the acceptance criterion it
proves. Mark tasks that can run in parallel.
```

```
/speckit-analyze
```

```
/speckit-implement

Implement 003-action-items task by task. After each task run the tests. When all
tasks are done, run pytest and Playwright, then stop and report what was
built, the test results, and any acceptance criterion you could not
satisfy (Principle XIII). Do not start the next specification.
```

```
/speckit-converge
```

```bash
git add -A
git commit -m "feat: 003-action-items"
```

---

# 004 — Record and Transcribe

## Specify and clarify (G1)

```
/speckit-specify

Create a Feature Specification.

Feature ID
004-record-and-transcribe

Feature Name
Record and Transcribe

Business Goal
Let the chair record the discussion in the meeting and get a written
transcript of it, without anyone typing.

Business Value
FEH's voice-capture proof of concept (sequence steps 1 to 5): the
first half of "voice in, action items out". FEH's success measure for
release 1b starts here.

Business Actors
Meeting chair

Business Capability
Voice Capture

Reference
docs/voice-capture-sequence.mmd steps 1 to 5; docs/reference.md
"MVP 1 · Voice capture"; docs/mockup/mvp-app.html Record page;
docs/sample/transcript.txt.

Builds On
003: the meeting screen gains a Record button. 002: the transcript
belongs to the meeting.

Functional Requirements

FR-001 The system shall offer a "Record" button on the meeting screen that
opens the meeting's Record page.

FR-002 The system shall let the chair start and stop recording in the browser,
showing "Recording…" and a running timer while it records.

FR-003 The system shall, when recording stops, send the audio to the
transcription service and show "Transcribing…" until the text returns.

FR-004 The system shall show the transcript on the Record page under the
heading "Transcript", and keep it with the meeting.

FR-005 The system shall work without any AI service connected, returning the
sample transcript in docs/sample/transcript.txt (Constitution Principle
XVI).

FR-006 The system shall tell the chair, in plain words, when recording or
transcription fails, and let them try again.

Non-Functional Requirements

Only people of the meeting's hotel can record or see its transcript.

The service connection details shall never appear on screen or in the
code (Principle XVI).

What It Looks Like On Screen
On today's Hotel A meeting, "Record" opens the Record page; "Start
recording" shows the timer; "Stop recording" shows "Transcribing…" and
then the sample transcript, beginning "John Lim: Next item."

Out of Scope
Extracting action items (005), reviewing them (006), live streaming,
speaker recognition, uploading audio files.

Label every acceptance criterion AC-004-<nn>.
Generate the specification following the GitHub Spec Kit format.
Do not generate implementation details.
Do not generate source code.
```

```
/speckit-clarify

Review Feature Specification 004-record-and-transcribe.

Identify missing requirements, ambiguity, assumptions, missing
validation, missing error handling, missing non-functional
requirements, and missing acceptance criteria.

Give particular attention to:
- The browser blocks the microphone, or there is no microphone.
- The chair records for a few seconds only, or for a long time.
- The chair leaves the page while recording.
- The transcription service is not connected (sample mode) or does not
  answer.

Review every functional requirement. Suggest improvements. Update the
specification where necessary. Make sure every acceptance criterion has
an ID AC-004-<nn> and describes behaviour a person can observe.

When a question is about a business rule, wait for the answer FEH gives
in the room. Do not invent business rules.

Do not generate implementation. Do not generate source code.
```

## Execute (G2, G3)

```
/speckit-plan

Plan Feature Specification 004-record-and-transcribe, following the constitution's
Technology Standards exactly.

This spec is an increment (Principle IX). It builds on: 003: the meeting screen gains a Record button. 002: the transcript belongs to the meeting.
Reuse what is there; do not rebuild or restructure it. Every earlier
spec's tests must still pass.

Extend the project; do not change its stack. The Record page is an
ordinary Django page with a small script that uses the browser's
MediaRecorder and posts the audio to the server when recording stops.
Transcription goes through one adapter, transcribe(audio) -> text,
exactly as the constitution's Technology Standards describe: AI_PROVIDER
"sample" returns docs/sample/transcript.txt; "azure" calls Azure OpenAI
with AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY and
AZURE_OPENAI_TRANSCRIBE_DEPLOYMENT read from the environment (.env, in
.gitignore). Store the transcript with the meeting. Tests use sample.

Check the result against docs/mockup/mvp-app.html, the whole MVP as a
clickable mockup.

Map every acceptance criterion to at least one test whose name
contains its ID. Write data-model.md and the page contract in
contracts/ (each page and form: address, who may use it, what it
shows) before any code.
```

```
/speckit-tasks

Break the plan for 004-record-and-transcribe into small tasks, one demonstrable capability
each (Principle IX). In every task, write the tests first and see them
fail (Principle VI). Name every test after the acceptance criterion it
proves. Mark tasks that can run in parallel.
```

```
/speckit-analyze
```

```
/speckit-implement

Implement 004-record-and-transcribe task by task. After each task run the tests. When all
tasks are done, run pytest and Playwright, then stop and report what was
built, the test results, and any acceptance criterion you could not
satisfy (Principle XIII). Do not start the next specification.
```

```
/speckit-converge
```

```bash
git add -A
git commit -m "feat: 004-record-and-transcribe"
```

---

# 005 — Extract Proposed Action Items

## Specify and clarify (G1)

```
/speckit-specify

Create a Feature Specification.

Feature ID
005-extract-proposed-items

Feature Name
Extract Proposed Action Items

Business Goal
Turn the transcript into proposed action items with the same fields as
the action list, so nobody types them up.

Business Value
FEH's voice-capture proof of concept (sequence steps 6 to 9): the
second half of "voice in, action items out". Release 1b target: proposed
items within 5 minutes of the meeting ending.

Business Actors
Meeting chair

Business Capability
AI Extraction

Reference
docs/voice-capture-sequence.mmd steps 6 to 9; docs/reference.md
"MVP 1 · Voice capture" and "Lists"; docs/sample/items.json.

Builds On
004: the transcript of the meeting. 003: the action fields, lists and
validation that every proposed item must satisfy.

Functional Requirements

FR-001 The system shall, after a transcript is ready, send it to the
extraction service with the action-item fields and show "Extracting
action items…".

FR-002 The system shall save each extracted item as Proposed for that meeting,
with market segment, issue category, issue, action required, owner,
priority, due date and anticipated result.

FR-003 The system shall only accept values from the fixed lists in
docs/reference.md and owners who are people of the meeting's hotel;
anything else is left empty for the chair to fill in.

FR-004 The system shall never add a proposed item to the meeting's action list
by itself (Constitution Principle XV).

FR-005 The system shall work without any AI service connected, returning the
sample items in docs/sample/items.json.

FR-006 The system shall tell the chair when extraction fails, keep the
transcript, and let them try again.

Non-Functional Requirements

Proposed items are kept, never deleted (Principle III).

Due dates are worked out from the meeting date in the hotel's time
zone.

What It Looks Like On Screen
After the sample transcript, "Extracting action items…" turns into
three proposed items: Alex Wong's December corporate review, Priya Rao's
OTA weekend rates, Mary Tan's Company ABC escalation, each marked
"Proposed".

Out of Scope
Editing, removing and confirming proposed items (006).

Label every acceptance criterion AC-005-<nn>.
Generate the specification following the GitHub Spec Kit format.
Do not generate implementation details.
Do not generate source code.
```

```
/speckit-clarify

Review Feature Specification 005-extract-proposed-items.

Identify missing requirements, ambiguity, assumptions, missing
validation, missing error handling, missing non-functional
requirements, and missing acceptance criteria.

Give particular attention to:
- The transcript mentions a person who is not in the hotel.
- A due date is said as "by Monday" or "next week".
- The service returns a segment or category that is not in the list.
- The transcript contains no actions at all.

Review every functional requirement. Suggest improvements. Update the
specification where necessary. Make sure every acceptance criterion has
an ID AC-005-<nn> and describes behaviour a person can observe.

When a question is about a business rule, wait for the answer FEH gives
in the room. Do not invent business rules.

Do not generate implementation. Do not generate source code.
```

## Execute (G2, G3)

```
/speckit-plan

Plan Feature Specification 005-extract-proposed-items, following the constitution's
Technology Standards exactly.

This spec is an increment (Principle IX). It builds on: 004: the transcript of the meeting. 003: the action fields, lists and validation that every proposed item must satisfy.
Reuse what is there; do not rebuild or restructure it. Every earlier
spec's tests must still pass.

Extend the project; do not change its stack. Add a Proposed item model
(with django-simple-history) belonging to the meeting, with the action
fields and a state: Proposed, Confirmed or Removed. Extraction goes
through one adapter, extract(transcript, meeting) -> list of items,
exactly as the constitution's Technology Standards describe: "sample"
returns docs/sample/items.json; "azure" calls the chat deployment with a
JSON response format, the field list, the fixed lists, the hotel's
people and the meeting date. Validate every value against the lists and
the hotel's people before saving; leave invalid ones empty. Tests use
sample.

Check the result against docs/mockup/mvp-app.html, the whole MVP as a
clickable mockup.

Map every acceptance criterion to at least one test whose name
contains its ID. Write data-model.md and the page contract in
contracts/ (each page and form: address, who may use it, what it
shows) before any code.
```

```
/speckit-tasks

Break the plan for 005-extract-proposed-items into small tasks, one demonstrable capability
each (Principle IX). In every task, write the tests first and see them
fail (Principle VI). Name every test after the acceptance criterion it
proves. Mark tasks that can run in parallel.
```

```
/speckit-analyze
```

```
/speckit-implement

Implement 005-extract-proposed-items task by task. After each task run the tests. When all
tasks are done, run pytest and Playwright, then stop and report what was
built, the test results, and any acceptance criterion you could not
satisfy (Principle XIII). Do not start the next specification.
```

```
/speckit-converge
```

```bash
git add -A
git commit -m "feat: 005-extract-proposed-items"
```

---

# 006 — Review and Confirm Proposed Items

## Specify and clarify (G1)

```
/speckit-specify

Create a Feature Specification.

Feature ID
006-review-and-confirm

Feature Name
Review and Confirm Proposed Items

Business Goal
Let the chair check the proposed items, correct or remove them, and
confirm the right ones into the meeting's action list.

Business Value
FEH's voice-capture proof of concept (sequence steps 10 to 13): the
chair stays in control of what the meeting records (Principle XV).
Release 1b target: at least 80% accepted without edits.

Business Actors
Meeting chair

Business Capability
Human Review of AI Output

Reference
docs/voice-capture-sequence.mmd steps 10 to 13; docs/reference.md
"MVP 1 · Voice capture"; docs/mockup/mvp-app.html Review page.

Builds On
005: the proposed items. 003: the action form and its validation,
reused to edit proposed items and to create the confirmed actions.

Functional Requirements

FR-001 The system shall show the meeting's proposed items on a Review page,
each with a checkbox (checked), its fields, a "Proposed" chip, "Edit"
and "Remove", and the note "Proposed by AI. Nothing is added to the
meeting until you confirm."

FR-002 The system shall let the chair edit a proposed item with the same form
and rules as an action (spec 003).

FR-003 The system shall not let an item with a missing required field be
confirmed, and shall say which field is missing.

FR-004 The system shall, on "Confirm selected (n)", add the selected items to
the meeting's action list as Open actions marked "From recording", mark
them Confirmed, and show "<n> actions confirmed.".

FR-005 The system shall mark removed items Removed; they never appear in the
action list.

FR-006 The system shall show, on the meeting screen, "<n> proposed items
waiting for review" with a "Review" link while any are waiting.

Non-Functional Requirements

Confirming is all-or-nothing for the selected items.

Only people of the meeting's hotel can review its proposed items.

What It Looks Like On Screen
With the three sample items, the chair changes Priya Rao's priority,
removes nothing, and presses "Confirm selected (3)": the meeting shows
"3 actions confirmed." and the three actions under "Raised in this
meeting", marked "From recording".

Out of Scope
Carry forward and overdue (007), re-running extraction, bulk editing.

Label every acceptance criterion AC-006-<nn>.
Generate the specification following the GitHub Spec Kit format.
Do not generate implementation details.
Do not generate source code.
```

```
/speckit-clarify

Review Feature Specification 006-review-and-confirm.

Identify missing requirements, ambiguity, assumptions, missing
validation, missing error handling, missing non-functional
requirements, and missing acceptance criteria.

Give particular attention to:
- The chair confirms nothing and leaves.
- Two people review the same proposed items at the same time.
- The chair records again before reviewing the first set.
- An owner was removed from the hotel since extraction.

Review every functional requirement. Suggest improvements. Update the
specification where necessary. Make sure every acceptance criterion has
an ID AC-006-<nn> and describes behaviour a person can observe.

When a question is about a business rule, wait for the answer FEH gives
in the room. Do not invent business rules.

Do not generate implementation. Do not generate source code.
```

## Execute (G2, G3)

```
/speckit-plan

Plan Feature Specification 006-review-and-confirm, following the constitution's
Technology Standards exactly.

This spec is an increment (Principle IX). It builds on: 005: the proposed items. 003: the action form and its validation, reused to edit proposed items and to create the confirmed actions.
Reuse what is there; do not rebuild or restructure it. Every earlier
spec's tests must still pass.

Extend the project; do not change its stack. The Review page is an
ordinary Django page with one form for the selected items; Edit reuses
the action form and validation from 003. Confirming creates the
action items and marks the proposed items Confirmed in one database
transaction. The meeting screen shows the waiting banner, like
docs/mockup/mvp-app.html.

Check the result against docs/mockup/mvp-app.html, the whole MVP as a
clickable mockup.

Map every acceptance criterion to at least one test whose name
contains its ID. Write data-model.md and the page contract in
contracts/ (each page and form: address, who may use it, what it
shows) before any code.
```

```
/speckit-tasks

Break the plan for 006-review-and-confirm into small tasks, one demonstrable capability
each (Principle IX). In every task, write the tests first and see them
fail (Principle VI). Name every test after the acceptance criterion it
proves. Mark tasks that can run in parallel.
```

```
/speckit-analyze
```

```
/speckit-implement

Implement 006-review-and-confirm task by task. After each task run the tests. When all
tasks are done, run pytest and Playwright, then stop and report what was
built, the test results, and any acceptance criterion you could not
satisfy (Principle XIII). Do not start the next specification.
```

```
/speckit-converge
```

```bash
git add -A
git commit -m "feat: 006-review-and-confirm"
```

---

# 007 — Carry Forward and Overdue (stretch)

## Specify and clarify (G1)

```
/speckit-specify

Create a Feature Specification.

Feature ID
007-carry-forward-and-overdue

Feature Name
Carry Forward and Overdue

Business Goal
Make unfinished actions from earlier meetings appear in the next
meeting automatically, and make late actions impossible to miss.

Business Value
FEH: "open items are easy to lose between weeks". Success measure:
open actions from earlier meetings appear in the next meeting, 100%.

Business Actors
Meeting chair
Hotel team member

Business Capability
Meeting Continuity

Reference
FEH requirements FR-006 and FR-009; docs/mockup/mvp-app.html meeting
screen.

Builds On
003: the actions and their statuses (including those confirmed in
006). 002: the meeting dates that decide what is "earlier".

Functional Requirements

FR-001 The system shall show, in every meeting, the hotel's actions from
earlier meetings that are Open, In progress or Blocked, under "Carried
forward from earlier meetings (n)", oldest first; actions raised in this
meeting under "Raised in this meeting (n)".

FR-002 The system shall show an action as overdue when its due date is before
today in the hotel's time zone and its status is Open, In progress or
Blocked, with "Overdue by n days" in red; "Due today" and "Due in n
days" otherwise.

FR-003 The system shall show the counts "Carried forward", "Raised in this
meeting" and "Overdue" at the top of each meeting.

Non-Functional Requirements

Overdue is worked out each time, never stored as a status.

What It Looks Like On Screen
Today's Hotel A meeting shows the seven open seeded actions carried
forward, three of them overdue in red, and the counters 7, 0 and 3.

Out of Scope
Due this week, filters, reminders.

Label every acceptance criterion AC-007-<nn>.
Generate the specification following the GitHub Spec Kit format.
Do not generate implementation details.
Do not generate source code.
```

```
/speckit-clarify

Review Feature Specification 007-carry-forward-and-overdue.

Identify missing requirements, ambiguity, assumptions, missing
validation, missing error handling, missing non-functional
requirements, and missing acceptance criteria.

Give particular attention to:
- An action due today, seen late in the evening.
- Whether actions confirmed from a recording count as raised in this
  meeting.

Review every functional requirement. Suggest improvements. Update the
specification where necessary. Make sure every acceptance criterion has
an ID AC-007-<nn> and describes behaviour a person can observe.

When a question is about a business rule, wait for the answer FEH gives
in the room. Do not invent business rules.

Do not generate implementation. Do not generate source code.
```

## Execute (G2, G3)

```
/speckit-plan

Plan Feature Specification 007-carry-forward-and-overdue, following the constitution's
Technology Standards exactly.

This spec is an increment (Principle IX). It builds on: 003: the actions and their statuses (including those confirmed in 006). 002: the meeting dates that decide what is "earlier".
Reuse what is there; do not rebuild or restructure it. Every earlier
spec's tests must still pass.

Extend the project; do not change its stack. Carry-forward and overdue
are queries on the existing models through 001's isolation; nothing is
copied or stored. Make "today" replaceable in tests.

Check the result against docs/mockup/mvp-app.html, the whole MVP as a
clickable mockup.

Map every acceptance criterion to at least one test whose name
contains its ID. Write data-model.md and the page contract in
contracts/ (each page and form: address, who may use it, what it
shows) before any code.
```

```
/speckit-tasks

Break the plan for 007-carry-forward-and-overdue into small tasks, one demonstrable capability
each (Principle IX). In every task, write the tests first and see them
fail (Principle VI). Name every test after the acceptance criterion it
proves. Mark tasks that can run in parallel.
```

```
/speckit-analyze
```

```
/speckit-implement

Implement 007-carry-forward-and-overdue task by task. After each task run the tests. When all
tasks are done, run pytest and Playwright, then stop and report what was
built, the test results, and any acceptance criterion you could not
satisfy (Principle XIII). Do not start the next specification.
```

```
/speckit-converge
```

```bash
git add -A
git commit -m "feat: 007-carry-forward-and-overdue"
```
