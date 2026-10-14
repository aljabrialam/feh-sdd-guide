# Meeting Action Tracker — All Specs (workshop MVP)

Complete set, in execution order. Every block is paste-ready.
FEH requirements: "Meeting Action Tracker: Requirements", 13 Oct 2026.
Governing rules: docs/constitution.md. Data, labels and look:
docs/reference.md. Target screens: docs/mockup/.

---

# SETUP — done in Step 1 of the guide

```bash
mkdir -p ~/feh-sdd && cd ~/feh-sdd
specify init feh-app --integration copilot
cd feh-app
# docs pack: docs/constitution.md, docs/specs.md, docs/reference.md
# from Teams (feh-workshop-files.zip): docs/feh-requirements.md, docs/mockup/
git init -b main && git add -A && git commit -m "chore: spec kit and workshop docs"
code .
```

Then open Copilot Chat in **Agent** mode and paste the constitution:

```
/speckit-constitution

Adopt docs/constitution.md as this project's constitution, exactly as
written: all fourteen principles, the Technology Standards, the
Development Workflow, the Definition of Done and Governance.
```

---

# WORKING RULES

Everything that produces a file goes through GitHub Copilot, driven by
the Spec Kit cycle. Not hand-edited around it (Principle X).

**Keep it small is not negotiable mid-build.** If a task seems to need
Entra ID, emails, export, Teams or AI, the task is wrong, not the scope
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

Day 1 afternoon: draft, compare, specify and clarify 001–005; G1 for
all five. Late Day 1: execute 001. Day 2: execute 002–005 in order;
006 and 007 only if time allows.

---

## Delivery order and stop lines

Build in this order. Each line marks what you have if you stop there.

| Order | Spec | When | If you stop here |
|---|---|---|---|
| 1 | 001 Workshop Sign-in and Hotel Access | Late Day 1 | People sign in and see only their own hotel. Isolation exists before any data does. |
| 2 | 002 Weekly Meetings | Day 2, 9:00 | Meetings can be created and listed. The weekly meeting exists in the tracker. |
| 3 | 003 Action Items in a Meeting | Day 2, 10:00 | Actions are recorded with an owner and a due date. The spreadsheet could be retired. |
| 4 | 004 Carry Forward Open Items | Day 2, 11:30 | Open items are never lost between weeks: FEH's main pain is solved. |
| 5 | 005 Overdue Flags and Meeting Counts | Day 2, 1:30 | The meeting shows what is late at a glance. The MVP is complete. |
| 6 | 006 Spreadsheet-style Editing (stretch) | Day 2 stretch | The action list feels like FEH's spreadsheet. |
| 7 | 007 Comments and Mark as Done (stretch) | Day 2 stretch | Follow-up between meetings is recorded, and actions can be closed properly. |

**Minimum viable demonstration: through 005.** 006 and 007 are stretch
goals, only after 005 is accepted.

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

This is the first feature, so it includes the project set-up from the
constitution's Technology Standards: manage.py at the repository root,
the Django project "tracker_site" and app "tracker", uv, pytest with
pytest-django, and Playwright in e2e/.
Add hotels and people with seed_demo loading exactly the "Hotels" and
"People" sections of docs/reference.md. Build the "Sign in as" page and
the top bar like docs/mockup/mvp-1-sign-in.html, with the labels and look
in docs/reference.md. Put hotel
isolation in one place (a hotel-scoped manager and a view mixin) that
every later feature will reuse.

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
Action items (003), carry-forward (004), completing a meeting.

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

Extend the project from 001; do not change its stack. Add the meeting
with django-simple-history, scoped to the hotel through 001's isolation.
Meetings list and "New meeting" form like docs/mockup/mvp-2-meetings.html
and mvp-3-new-meeting.html, with the exact labels in docs/reference.md; seed_demo also loads the seeded meetings.

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
owner and due date, and change it later.

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
docs/mockup/mvp-4-meeting-screen.html and mvp-5-add-action.html. FEH requirements FR-007, FR-008,
FR-009, FR-013, FR-014.

Functional Requirements

FR-001 The system shall let a person add an action to a meeting with a market
segment, an issue category, the issue, the action required, an owner
from the same hotel, a priority, a due date and a status.

FR-002 The system shall require segment, category, issue, action required,
owner and due date, and shall tell the person which is missing. Issue
and action required are at most 300 characters.

FR-003 The system shall default priority to Medium and status to Open, using
the fixed lists in docs/reference.md.

FR-004 The system shall let a person edit any action of their hotel.

FR-005 The system shall list a meeting's actions with all their values and
the owner's name.

FR-006 The system shall never delete an action; setting it to Cancelled is
the way to remove it, and every change is recorded (Constitution
Principle III).

Non-Functional Requirements

The meeting page shall stay fast with 100 actions.

What It Looks Like On Screen
On today's meeting, "Add action" records "December corporate pace
behind last year", owner Alex Wong. It appears in the list; "Edit"
changes its status to In progress.

Out of Scope
Actions from earlier meetings (004), overdue (005), editing in place
(006), comments and closing (007).

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

Extend the project; do not change its stack. Add the action item with
django-simple-history, belonging to the meeting it was raised in and
scoped to the hotel through 001's isolation. "Add action" and "Edit"
are ordinary Django forms on the meeting page, laid out like
docs/mockup/mvp-4-meeting-screen.html and mvp-5-add-action.html. seed_demo also loads the seeded actions.

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

# 004 — Carry Forward Open Items

## Specify and clarify (G1)

```
/speckit-specify

Create a Feature Specification.

Feature ID
004-carry-forward

Feature Name
Carry Forward Open Items

Business Goal
Make every unfinished action from earlier meetings appear in the next
meeting automatically, so nothing is lost between weeks.

Business Value
FEH: "open items are easy to lose between weeks". Success measure:
open actions from earlier meetings appear in the next meeting, 100%.

Business Actors
Meeting chair
Hotel team member

Business Capability
Meeting Continuity

Reference
FEH requirement FR-006; docs/mockup/01-meeting-screen.png group
headings.

Functional Requirements

FR-001 The system shall show, in every meeting, the hotel's actions from
earlier meetings that are Open, In progress or Blocked, under the
heading "Carried forward from earlier meetings (n)", oldest first.

FR-002 The system shall show the actions raised in this meeting under
"Raised in this meeting (n)", below the carried-forward group.

FR-003 The system shall show under each action "Raised <date>", the date of
the meeting it was raised in.

FR-004 The system shall not carry forward Done or Cancelled actions.

FR-005 The system shall treat a carried-forward action as the same action,
not a copy: a change made in any meeting shows everywhere.

Non-Functional Requirements

Carry-forward shall need no manual step by anyone.

What It Looks Like On Screen
Creating today's Hotel A meeting shows the seven open seeded
actions under "Carried forward from earlier meetings (7)"; "Breakfast
queue complaints" (Done) is not there.

Out of Scope
Overdue flags and counts (005).

Label every acceptance criterion AC-004-<nn>.
Generate the specification following the GitHub Spec Kit format.
Do not generate implementation details.
Do not generate source code.
```

```
/speckit-clarify

Review Feature Specification 004-carry-forward.

Identify missing requirements, ambiguity, assumptions, missing
validation, missing error handling, missing non-functional
requirements, and missing acceptance criteria.

Give particular attention to:
- A meeting is created for a date earlier than the latest meeting.
- An action raised in a meeting is later Cancelled, then set back to
  Open.
- What "earlier" means when two meetings are on the same day at
  different hotels.

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

Plan Feature Specification 004-carry-forward, following the constitution's
Technology Standards exactly.

Extend the project; do not change its stack. Carry-forward is a query
on the existing models through the hotel isolation from 001, not a
copy of any data. Show the two groups with the headings and colours in
docs/reference.md and the constitution.

Map every acceptance criterion to at least one test whose name
contains its ID. Write data-model.md and the page contract in
contracts/ (each page and form: address, who may use it, what it
shows) before any code.
```

```
/speckit-tasks

Break the plan for 004-carry-forward into small tasks, one demonstrable capability
each (Principle IX). In every task, write the tests first and see them
fail (Principle VI). Name every test after the acceptance criterion it
proves. Mark tasks that can run in parallel.
```

```
/speckit-analyze
```

```
/speckit-implement

Implement 004-carry-forward task by task. After each task run the tests. When all
tasks are done, run pytest and Playwright, then stop and report what was
built, the test results, and any acceptance criterion you could not
satisfy (Principle XIII). Do not start the next specification.
```

```
/speckit-converge
```

```bash
git add -A
git commit -m "feat: 004-carry-forward"
```

---

# 005 — Overdue Flags and Meeting Counts

## Specify and clarify (G1)

```
/speckit-specify

Create a Feature Specification.

Feature ID
005-overdue-and-counts

Feature Name
Overdue Flags and Meeting Counts

Business Goal
Make late actions impossible to miss, and give the meeting a
one-glance summary.

Business Value
In the weekly meeting the chair needs to see immediately what is
overdue. FEH's mockup shows this as red "Overdue by n days" and three
counters at the top.

Business Actors
Meeting chair
Action owner

Business Capability
Follow-up Visibility

Reference
FEH requirement FR-009 (overdue is calculated, not a status);
docs/mockup/01-meeting-screen.png counters and due-date cell.

Functional Requirements

FR-001 The system shall show an action as overdue when its due date is
before today in the hotel's time zone and its status is Open, In
progress or Blocked, with "Overdue by n days" in red.

FR-002 The system shall show "Due today" for an action due today, and "Due
in n days" for a later due date.

FR-003 The system shall show at the top of each meeting the counts "Carried
forward", "Raised in this meeting" and "Overdue".

FR-004 The system shall never store "overdue" as a status; it is worked out
from the due date each time.

Non-Functional Requirements

The flags and counts shall be correct on the day of the demo without re-seeding.

What It Looks Like On Screen
Today's Hotel A meeting shows "Overdue by n days" in red on the seeded
actions due 9, 10 and 11 Oct, and the counters Carried forward 7,
Raised in this meeting 0, Overdue 3.

Out of Scope
Due this week, filters, reminders.

Label every acceptance criterion AC-005-<nn>.
Generate the specification following the GitHub Spec Kit format.
Do not generate implementation details.
Do not generate source code.
```

```
/speckit-clarify

Review Feature Specification 005-overdue-and-counts.

Identify missing requirements, ambiguity, assumptions, missing
validation, missing error handling, missing non-functional
requirements, and missing acceptance criteria.

Give particular attention to:
- An action due today, seen late in the evening in the hotel's time
  zone.
- A Blocked action whose due date has passed.
- Whether Done or Cancelled actions count in "Raised in this meeting".

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

Plan Feature Specification 005-overdue-and-counts, following the constitution's
Technology Standards exactly.

Extend the project; do not change its stack. Work out overdue, due
today and the counts from the due date and today's date in the hotel's
time zone; nothing is stored. Make "today" replaceable in tests so the
tests do not depend on the real date.

Map every acceptance criterion to at least one test whose name
contains its ID. Write data-model.md and the page contract in
contracts/ (each page and form: address, who may use it, what it
shows) before any code.
```

```
/speckit-tasks

Break the plan for 005-overdue-and-counts into small tasks, one demonstrable capability
each (Principle IX). In every task, write the tests first and see them
fail (Principle VI). Name every test after the acceptance criterion it
proves. Mark tasks that can run in parallel.
```

```
/speckit-analyze
```

```
/speckit-implement

Implement 005-overdue-and-counts task by task. After each task run the tests. When all
tasks are done, run pytest and Playwright, then stop and report what was
built, the test results, and any acceptance criterion you could not
satisfy (Principle XIII). Do not start the next specification.
```

```
/speckit-converge
```

```bash
git add -A
git commit -m "feat: 005-overdue-and-counts"
```

---

# 006 — Spreadsheet-style Editing (stretch)

## Specify and clarify (G1)

```
/speckit-specify

Create a Feature Specification.

Feature ID
006-spreadsheet-style-editing

Feature Name
Spreadsheet-style Editing

Business Goal
Let a team member change any value directly in the meeting's action
list, saved straight away, like the spreadsheet they use today.

Business Value
FEH's requirement FR-005: an inline grid with autosave, so the
meeting is not slowed down by opening a form for every change.

Business Actors
Hotel team member

Business Capability
Fast Data Entry

Reference
FEH requirement FR-005; docs/mockup/01-meeting-screen.png; the
constitution's Technology Standards (HTMX for this spec only).

Functional Requirements

FR-001 The system shall let a person change any value of an action directly in
the meeting's list, saved without pressing a save button.

FR-002 The system shall show "All changes save automatically. Saved just
now." after each save.

FR-003 The system shall keep the last saved value and show the reason next
to the value when a change is not accepted.

FR-004 The system shall offer a blank row at the bottom of the list to add
an action in place.

FR-005 The system shall update the counts from 005 after each change.

Non-Functional Requirements

A change shall save in under one second (FEH NFR-004).

What It Looks Like On Screen
Changing Alex Wong's status in the list saves at once, the "Saved just
now" line appears, and the Overdue count changes when a due date moves.

Out of Scope
Keyboard shortcuts beyond normal Tab order.

Label every acceptance criterion AC-006-<nn>.
Generate the specification following the GitHub Spec Kit format.
Do not generate implementation details.
Do not generate source code.
```

```
/speckit-clarify

Review Feature Specification 006-spreadsheet-style-editing.

Identify missing requirements, ambiguity, assumptions, missing
validation, missing error handling, missing non-functional
requirements, and missing acceptance criteria.

Give particular attention to:
- A person changes a value, then changes it back before it saves.
- The connection drops while a value is saving.

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

Plan Feature Specification 006-spreadsheet-style-editing, following the constitution's
Technology Standards exactly.

Extend the project; do not change its stack. Use HTMX, served from
static files, for this list only: each change posts one value and
re-renders that row and the counts. Reuse the validation and the
change record from 003.

Map every acceptance criterion to at least one test whose name
contains its ID. Write data-model.md and the page contract in
contracts/ (each page and form: address, who may use it, what it
shows) before any code.
```

```
/speckit-tasks

Break the plan for 006-spreadsheet-style-editing into small tasks, one demonstrable capability
each (Principle IX). In every task, write the tests first and see them
fail (Principle VI). Name every test after the acceptance criterion it
proves. Mark tasks that can run in parallel.
```

```
/speckit-analyze
```

```
/speckit-implement

Implement 006-spreadsheet-style-editing task by task. After each task run the tests. When all
tasks are done, run pytest and Playwright, then stop and report what was
built, the test results, and any acceptance criterion you could not
satisfy (Principle XIII). Do not start the next specification.
```

```
/speckit-converge
```

```bash
git add -A
git commit -m "feat: 006-spreadsheet-style-editing"
```

---

# 007 — Comments and Mark as Done (stretch)

## Specify and clarify (G1)

```
/speckit-specify

Create a Feature Specification.

Feature ID
007-comments-and-done

Feature Name
Comments and Mark as Done

Business Goal
Let a team member follow an action up between meetings and close it
properly.

Business Value
FEH requirements FR-009 and FR-010: an update log of dated comments,
and closing that records who closed it and when.

Business Actors
Action owner
Hotel team member

Business Capability
Action Follow-up

Reference
docs/mockup/03-item-detail.png (simplified as in docs/reference.md).

Functional Requirements

FR-001 The system shall give each action its own page showing its details and
an update log.

FR-002 The system shall let a person post a comment of 1 to 500 characters,
shown with who posted it and when; comments cannot be edited or
removed.

FR-003 The system shall add a line to the update log automatically whenever
the status changes.

FR-004 The system shall let a person mark an action as done, recording who
closed it and when.

FR-005 The system shall let a person cancel an action only with a short
reason, which is posted to the update log.

Non-Functional Requirements

Every post goes through the same hotel isolation as 001.

What It Looks Like On Screen
Opening "Group wash risk for Company ABC" shows its update log; Mary
posts a comment, then "Mark as done" closes it with her name and the
time.

Out of Scope
Results and outcome ratings, the change-history screen.

Label every acceptance criterion AC-007-<nn>.
Generate the specification following the GitHub Spec Kit format.
Do not generate implementation details.
Do not generate source code.
```

```
/speckit-clarify

Review Feature Specification 007-comments-and-done.

Identify missing requirements, ambiguity, assumptions, missing
validation, missing error handling, missing non-functional
requirements, and missing acceptance criteria.

Give particular attention to:
- A Done action is set back to In progress: what happens to who closed
  it and when.
- Who may mark an action as done: anyone at the hotel, or only the
  owner.

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

Plan Feature Specification 007-comments-and-done, following the constitution's
Technology Standards exactly.

Extend the project; do not change its stack. The action page is an
ordinary Django page; comments and closing are ordinary form posts
through 001's isolation. Update seed_demo with the update log in
docs/reference.md.

Map every acceptance criterion to at least one test whose name
contains its ID. Write data-model.md and the page contract in
contracts/ (each page and form: address, who may use it, what it
shows) before any code.
```

```
/speckit-tasks

Break the plan for 007-comments-and-done into small tasks, one demonstrable capability
each (Principle IX). In every task, write the tests first and see them
fail (Principle VI). Name every test after the acceptance criterion it
proves. Mark tasks that can run in parallel.
```

```
/speckit-analyze
```

```
/speckit-implement

Implement 007-comments-and-done task by task. After each task run the tests. When all
tasks are done, run pytest and Playwright, then stop and report what was
built, the test results, and any acceptance criterion you could not
satisfy (Principle XIII). Do not start the next specification.
```

```
/speckit-converge
```

```bash
git add -A
git commit -m "feat: 007-comments-and-done"
```
