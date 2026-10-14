"""The workshop run sheet: one source for docs/specs.md (docs pack) and the guide's spec slides.

Run:  python3 tools/runsheet.py   -> writes starter/docs/specs.md
"""
import os

CLARIFY_TAIL = '''Review every functional requirement. Suggest improvements. Update the
specification where necessary. Make sure every acceptance criterion has
an ID AC-{n}-<nn> and describes behaviour a person can observe.

When a question is about a business rule, wait for the answer FEH gives
in the room. Do not invent business rules.

Do not generate implementation. Do not generate source code.'''

SPECIFY_TAIL = '''Label every acceptance criterion AC-{n}-<nn>.
Generate the specification following the GitHub Spec Kit format.
Do not generate implementation details.
Do not generate source code.'''

SPECS = [
 dict(n='001', id='001-sign-in-hotel-access', name='Workshop Sign-in and Hotel Access', short='Sign-in and hotel access',
  when='Late Day 1', stop='People sign in and see only their own hotel. Isolation exists before any data does.',
  goal='''Let each person enter the tracker as themselves and see only their
own hotel, standing in for Microsoft Entra ID during the workshop.''',
  value='''Every later feature depends on knowing who the person is and which
hotel they belong to. FEH's requirements make hotel isolation a core
rule (NFR-001), so it is built first, before any meeting or action
exists.''',
  actors=['Hotel team member'], cap='Access and Hotel Isolation',
  ref='''docs/reference.md "Hotels" and "People". FEH requirements FR-003
(Entra ID, stubbed for the workshop), FR-013, NFR-001.''',
  frs=['''The system shall present a sign-in page that lists every person in
docs/reference.md with their name and hotel; choosing a person signs
them in as that person.''',
       '''The system shall state on the sign-in page that it is a workshop
stand-in and that Microsoft Entra ID replaces it in the real product.''',
       '''The system shall show the signed-in person's name and hotel on every
page, with a way to sign out.''',
       '''The system shall require sign-in for every page except the sign-in
page.''',
       '''The system shall only ever show a person data that belongs to their
own hotel. Anything belonging to another hotel shall behave as if it
does not exist.'''],
  nfrs=['Isolation shall be enforced in one place, not page by page.'],
  screen='''The sign-in page with one button per person; after choosing Mary Tan,
the top bar shows "Mary Tan · Hotel A" and "Sign out".''',
  out='''Passwords, roles, Microsoft Entra ID, meetings (002).''',
  attention=['''A person types the address of a page that belongs to another hotel.''',
             '''A person signs out and presses the browser's Back button.''',
             '''Someone in the room asks for a person who belongs to two hotels
(not in the workshop: each person belongs to one hotel).'''],
  plan='''This is the first feature, so it includes the project set-up from the
constitution's Technology Standards: manage.py at the repository root,
the Django project "tracker_site" and app "tracker", uv, pytest with
pytest-django, and Playwright in e2e/.
Add hotels and people with seed_demo loading exactly the "Hotels" and
"People" sections of docs/reference.md. Build the "Sign in as" page and
the top bar like docs/mockup/mvp-1-sign-in.png, with the labels and look
in docs/reference.md. Put hotel
isolation in one place (a hotel-scoped manager and a view mixin) that
every later feature will reuse.''',
  ),
 dict(n='002', id='002-weekly-meetings', name='Weekly Meetings', short='Weekly meetings',
  when='Day 2, 9:00', stop='Meetings can be created and listed. The weekly meeting exists in the tracker.',
  goal='''Let a team member create the weekly performance meeting for their
hotel and see all of their hotel's meetings.''',
  value='''Each action in FEH's spreadsheet belongs to a meeting date. Meetings
are the container every action is raised in.''',
  actors=['Hotel team member', 'Meeting chair'], cap='Meeting Management',
  ref='''docs/reference.md "Meetings in the seed" and "Screens and exact
labels". FEH requirements FR-004, FR-021.''',
  frs=['''The system shall let a person create a meeting for their hotel with a
date, a time, a title (default "Weekly performance meeting"), a chair
and attendees chosen from the hotel's people, and optionally a Teams
meeting link.''',
       '''The system shall allow only one meeting per hotel per date, and shall
tell the person when the date is already taken.''',
       '''The system shall list the hotel's meetings, newest first, each with
its date, title and chair.''',
       '''The system shall show a meeting's title, date and time, chair,
attendees and Teams meeting link when it is opened.''',
       '''The system shall record who created a meeting and every later change
to it (Constitution Principle III).'''],
  nfrs=['Dates and times shall be shown in the hotel\'s time zone.'],
  screen='''Meetings shows the three seeded Hotel A meetings, newest first. "New
meeting" creates today's meeting, which then opens with its heading
and attendee chips.''',
  out='''Action items (003), carry-forward (004), completing a meeting.''',
  attention=['''A meeting created for a date in the past or far in the future.''',
             '''The chair is not one of the attendees.''',
             '''A Teams meeting link that is not a web address.''',
             '''Two people create a meeting for the same date at the same time.'''],
  plan='''Extend the project from 001; do not change its stack. Add the meeting
with django-simple-history, scoped to the hotel through 001's isolation.
Meetings list and "New meeting" form like docs/mockup/mvp-2-meetings.png
and mvp-3-new-meeting.png, with the exact labels in docs/reference.md; seed_demo also loads the seeded meetings.''',
  ),
 dict(n='003', id='003-action-items', name='Action Items in a Meeting', short='Action items',
  when='Day 2, 10:00', stop='Actions are recorded with an owner and a due date. The spreadsheet could be retired.',
  goal='''Let a team member record each action agreed in the meeting, with its
owner and due date, and change it later.''',
  value='''This replaces FEH's spreadsheet columns (issue, action required,
owner, due date, status) and adds market segment, issue category and
priority, so every action has an owner and a due date (FEH success
measure: 100%).''',
  actors=['Hotel team member', 'Action owner'], cap='Action Tracking',
  ref='''docs/reference.md "Lists" and "Action items in the seed";
docs/mockup/mvp-4-meeting-screen.png and mvp-5-add-action.png. FEH requirements FR-007, FR-008,
FR-009, FR-013, FR-014.''',
  frs=['''The system shall let a person add an action to a meeting with a market
segment, an issue category, the issue, the action required, an owner
from the same hotel, a priority, a due date and a status.''',
       '''The system shall require segment, category, issue, action required,
owner and due date, and shall tell the person which is missing. Issue
and action required are at most 300 characters.''',
       '''The system shall default priority to Medium and status to Open, using
the fixed lists in docs/reference.md.''',
       '''The system shall let a person edit any action of their hotel.''',
       '''The system shall list a meeting's actions with all their values and
the owner's name.''',
       '''The system shall never delete an action; setting it to Cancelled is
the way to remove it, and every change is recorded (Constitution
Principle III).'''],
  nfrs=['The meeting page shall stay fast with 100 actions.'],
  screen='''On today's meeting, "Add action" records "December corporate pace
behind last year", owner Alex Wong. It appears in the list; "Edit"
changes its status to In progress.''',
  out='''Actions from earlier meetings (004), overdue (005), editing in place
(006), comments and closing (007).''',
  attention=['''The owner is not one of the meeting's attendees.''',
             '''The due date is already in the past when the action is created.''',
             '''An action is set straight to Done or Cancelled when it is created.''',
             '''Two people edit the same action at the same time.'''],
  plan='''Extend the project; do not change its stack. Add the action item with
django-simple-history, belonging to the meeting it was raised in and
scoped to the hotel through 001's isolation. "Add action" and "Edit"
are ordinary Django forms on the meeting page, laid out like
docs/mockup/mvp-4-meeting-screen.png and mvp-5-add-action.png. seed_demo also loads the seeded actions.''',
  ),
 dict(n='004', id='004-carry-forward', name='Carry Forward Open Items', short='Carry forward',
  when='Day 2, 11:30', stop='Open items are never lost between weeks: FEH\'s main pain is solved.',
  goal='''Make every unfinished action from earlier meetings appear in the next
meeting automatically, so nothing is lost between weeks.''',
  value='''FEH: "open items are easy to lose between weeks". Success measure:
open actions from earlier meetings appear in the next meeting, 100%.''',
  actors=['Meeting chair', 'Hotel team member'], cap='Meeting Continuity',
  ref='''FEH requirement FR-006; docs/mockup/01-meeting-screen.png group
headings.''',
  frs=['''The system shall show, in every meeting, the hotel's actions from
earlier meetings that are Open, In progress or Blocked, under the
heading "Carried forward from earlier meetings (n)", oldest first.''',
       '''The system shall show the actions raised in this meeting under
"Raised in this meeting (n)", below the carried-forward group.''',
       '''The system shall show under each action "Raised <date>", the date of
the meeting it was raised in.''',
       '''The system shall not carry forward Done or Cancelled actions.''',
       '''The system shall treat a carried-forward action as the same action,
not a copy: a change made in any meeting shows everywhere.'''],
  nfrs=['Carry-forward shall need no manual step by anyone.'],
  screen='''Creating today's Hotel A meeting shows the seven open seeded
actions under "Carried forward from earlier meetings (7)"; "Breakfast
queue complaints" (Done) is not there.''',
  out='''Overdue flags and counts (005).''',
  attention=['''A meeting is created for a date earlier than the latest meeting.''',
             '''An action raised in a meeting is later Cancelled, then set back to
Open.''',
             '''What "earlier" means when two meetings are on the same day at
different hotels.'''],
  plan='''Extend the project; do not change its stack. Carry-forward is a query
on the existing models through the hotel isolation from 001, not a
copy of any data. Show the two groups with the headings and colours in
docs/reference.md and the constitution.''',
  ),
 dict(n='005', id='005-overdue-and-counts', name='Overdue Flags and Meeting Counts', short='Overdue and counts',
  when='Day 2, 1:30', stop='The meeting shows what is late at a glance. The MVP is complete.',
  goal='''Make late actions impossible to miss, and give the meeting a
one-glance summary.''',
  value='''In the weekly meeting the chair needs to see immediately what is
overdue. FEH's mockup shows this as red "Overdue by n days" and three
counters at the top.''',
  actors=['Meeting chair', 'Action owner'], cap='Follow-up Visibility',
  ref='''FEH requirement FR-009 (overdue is calculated, not a status);
docs/mockup/01-meeting-screen.png counters and due-date cell.''',
  frs=['''The system shall show an action as overdue when its due date is
before today in the hotel's time zone and its status is Open, In
progress or Blocked, with "Overdue by n days" in red.''',
       '''The system shall show "Due today" for an action due today, and "Due
in n days" for a later due date.''',
       '''The system shall show at the top of each meeting the counts "Carried
forward", "Raised in this meeting" and "Overdue".''',
       '''The system shall never store "overdue" as a status; it is worked out
from the due date each time.'''],
  nfrs=['The flags and counts shall be correct on the day of the demo without re-seeding.'],
  screen='''Today's Hotel A meeting shows "Overdue by n days" in red on the seeded
actions due 9, 10 and 11 Oct, and the counters Carried forward 7,
Raised in this meeting 0, Overdue 3.''',
  out='''Due this week, filters, reminders.''',
  attention=['''An action due today, seen late in the evening in the hotel's time
zone.''',
             '''A Blocked action whose due date has passed.''',
             '''Whether Done or Cancelled actions count in "Raised in this meeting".'''],
  plan='''Extend the project; do not change its stack. Work out overdue, due
today and the counts from the due date and today's date in the hotel's
time zone; nothing is stored. Make "today" replaceable in tests so the
tests do not depend on the real date.''',
  ),
 dict(n='006', id='006-spreadsheet-style-editing', name='Spreadsheet-style Editing', short='Spreadsheet-style editing', stretch=True,
  when='Day 2 stretch', stop='The action list feels like FEH\'s spreadsheet.',
  goal='''Let a team member change any value directly in the meeting's action
list, saved straight away, like the spreadsheet they use today.''',
  value='''FEH's requirement FR-005: an inline grid with autosave, so the
meeting is not slowed down by opening a form for every change.''',
  actors=['Hotel team member'], cap='Fast Data Entry',
  ref='''FEH requirement FR-005; docs/mockup/01-meeting-screen.png; the
constitution's Technology Standards (HTMX for this spec only).''',
  frs=['''The system shall let a person change any value of an action directly in
the meeting's list, saved without pressing a save button.''',
       '''The system shall show "All changes save automatically. Saved just
now." after each save.''',
       '''The system shall keep the last saved value and show the reason next
to the value when a change is not accepted.''',
       '''The system shall offer a blank row at the bottom of the list to add
an action in place.''',
       '''The system shall update the counts from 005 after each change.'''],
  nfrs=['A change shall save in under one second (FEH NFR-004).'],
  screen='''Changing Alex Wong's status in the list saves at once, the "Saved just
now" line appears, and the Overdue count changes when a due date moves.''',
  out='''Keyboard shortcuts beyond normal Tab order.''',
  attention=['''A person changes a value, then changes it back before it saves.''',
             '''The connection drops while a value is saving.'''],
  plan='''Extend the project; do not change its stack. Use HTMX, served from
static files, for this list only: each change posts one value and
re-renders that row and the counts. Reuse the validation and the
change record from 003.''',
  ),
 dict(n='007', id='007-comments-and-done', name='Comments and Mark as Done', short='Comments and done', stretch=True,
  when='Day 2 stretch', stop='Follow-up between meetings is recorded, and actions can be closed properly.',
  goal='''Let a team member follow an action up between meetings and close it
properly.''',
  value='''FEH requirements FR-009 and FR-010: an update log of dated comments,
and closing that records who closed it and when.''',
  actors=['Action owner', 'Hotel team member'], cap='Action Follow-up',
  ref='''docs/mockup/03-item-detail.png (simplified as in docs/reference.md).''',
  frs=['''The system shall give each action its own page showing its details and
an update log.''',
       '''The system shall let a person post a comment of 1 to 500 characters,
shown with who posted it and when; comments cannot be edited or
removed.''',
       '''The system shall add a line to the update log automatically whenever
the status changes.''',
       '''The system shall let a person mark an action as done, recording who
closed it and when.''',
       '''The system shall let a person cancel an action only with a short
reason, which is posted to the update log.'''],
  nfrs=['Every post goes through the same hotel isolation as 001.'],
  screen='''Opening "Group wash risk for Company ABC" shows its update log; Mary
posts a comment, then "Mark as done" closes it with her name and the
time.''',
  out='''Results and outcome ratings, the change-history screen.''',
  attention=['''A Done action is set back to In progress: what happens to who closed
it and when.''',
             '''Who may mark an action as done: anyone at the hotel, or only the
owner.'''],
  plan='''Extend the project; do not change its stack. The action page is an
ordinary Django page; comments and closing are ordinary form posts
through 001's isolation. Update seed_demo with the update log in
docs/reference.md.''',
  ),
]

def specify_block(s):
    fr = '\n\n'.join('FR-%03d %s' % (i + 1, t) for i, t in enumerate(s['frs']))
    nfr = '\n\n'.join(s['nfrs'])
    actors = '\n'.join(s['actors'])
    return '''/speckit-specify

Create a Feature Specification.

Feature ID
%s

Feature Name
%s

Business Goal
%s

Business Value
%s

Business Actors
%s

Business Capability
%s

Reference
%s

Functional Requirements

%s

Non-Functional Requirements

%s

What It Looks Like On Screen
%s

Out of Scope
%s

%s''' % (s['id'], s['name'], s['goal'], s['value'], actors, s['cap'], s['ref'], fr, nfr,
         s['screen'], s['out'], SPECIFY_TAIL.format(n=s['n']))

def clarify_block(s):
    att = '\n'.join('- ' + a.replace('\n', '\n  ') for a in s['attention'])
    return '''/speckit-clarify

Review Feature Specification %s.

Identify missing requirements, ambiguity, assumptions, missing
validation, missing error handling, missing non-functional
requirements, and missing acceptance criteria.

Give particular attention to:
%s

%s''' % (s['id'], att, CLARIFY_TAIL.format(n=s['n']))

def plan_block(s):
    return '''/speckit-plan

Plan Feature Specification %s, following the constitution's
Technology Standards exactly.

%s

Map every acceptance criterion to at least one test whose name
contains its ID. Write data-model.md and the page contract in
contracts/ (each page and form: address, who may use it, what it
shows) before any code.''' % (s['id'], s['plan'])

def tasks_block(s):
    return '''/speckit-tasks

Break the plan for %s into small tasks, one demonstrable capability
each (Principle IX). In every task, write the tests first and see them
fail (Principle VI). Name every test after the acceptance criterion it
proves. Mark tasks that can run in parallel.''' % s['id']

ANALYZE = '/speckit-analyze'

def implement_block(s):
    return '''/speckit-implement

Implement %s task by task. After each task run the tests. When all
tasks are done, run pytest and Playwright, then stop and report what was
built, the test results, and any acceptance criterion you could not
satisfy (Principle XIII). Do not start the next specification.''' % s['id']

def commit_block(s):
    return 'git add -A\ngit commit -m "feat: %s"' % s['id']

def markdown():
    out = ['''# Meeting Action Tracker — All Specs (workshop MVP)

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
|---|---|---|---|''']
    for i, s in enumerate(SPECS):
        out.append('| %d | %s %s%s | %s | %s |' % (i + 1, s['n'], s['name'], ' (stretch)' if s.get('stretch') else '', s['when'], s['stop']))
    out.append('''
**Minimum viable demonstration: through 005.** 006 and 007 are stretch
goals, only after 005 is accepted.
''')
    for s in SPECS:
        out.append('---\n\n# %s — %s%s\n' % (s['n'], s['name'], ' (stretch)' if s.get('stretch') else ''))
        out.append('## Specify and clarify (G1)\n')
        out.append('```\n' + specify_block(s) + '\n```\n')
        out.append('```\n' + clarify_block(s) + '\n```\n')
        out.append('## Execute (G2, G3)\n')
        for b in (plan_block(s), tasks_block(s), ANALYZE, implement_block(s), '/speckit-converge'):
            out.append('```\n' + b + '\n```\n')
        out.append('```bash\n' + commit_block(s) + '\n```\n')
    return '\n'.join(out)

if __name__ == '__main__':
    p = os.path.join(os.path.dirname(__file__), '..', 'starter', 'docs', 'specs.md')
    open(p, 'w').write(markdown())
    print('wrote', os.path.normpath(p))
