"""MVP 1 · Voice capture run sheet: one source for the MVP 1 docs pack specs.md and the MVP 1 guide's spec slides.

Run:  python3 tools/runsheet_mvp1.py   -> writes starter/mvp1/docs/specs.md
"""
import os, copy
import runsheet as R

S2 = {s['n']: s for s in R.SPECS}

S001 = copy.deepcopy(S2['001'])
S001['plan'] = S001['plan'].replace('docs/mockup/mvp-1-sign-in.html', 'the sign-in page of docs/mockup/mvp-app.html')
S002 = copy.deepcopy(S2['002'])
S002['when'] = 'Day 2, 9:00'
S002['out'] = 'Action items (003), recording (004), completing a meeting.'
S002['plan'] = S002['plan'].replace('docs/mockup/mvp-2-meetings.html\nand mvp-3-new-meeting.html', 'the Meetings and New meeting\npages of docs/mockup/mvp-app.html')

S003 = copy.deepcopy(S2['003'])
S003.update(
  when='Day 2, 9:45',
  ref=S003['ref'].replace('docs/mockup/mvp-4-meeting-screen.html and mvp-5-add-action.html.', 'the meeting screen and Add action form of\ndocs/mockup/mvp-app.html.'),
  goal='''Let a team member record each action agreed in the meeting, with its
owner, due date and what it is expected to achieve, and change it later.''',
  frs=['''The system shall let a person add an action to a meeting with a market
segment, an issue category, the issue, the action required, an owner
from the same hotel, a priority, a due date, a status and, optionally,
an anticipated result.''',
       '''The system shall require segment, category, issue, action required,
owner and due date, and shall tell the person which is missing. Issue,
action required and anticipated result are at most 300 characters.''',
       '''The system shall default priority to Medium and status to Open, using
the fixed lists in docs/reference.md.''',
       '''The system shall let a person edit any action of their hotel.''',
       '''The system shall list a meeting's actions with all their values, the
owner's name, and the anticipated result as "Expected: <text>".''',
       '''The system shall never delete an action; setting it to Cancelled is
the way to remove it, and every change is recorded (Constitution
Principle III).'''],
  screen='''On today's meeting, "Add action" records "December corporate pace
behind last year", owner Alex Wong, expected "December corporate pickup
back to last year's pace". It appears in the list with "Expected: …";
"Edit" changes its status to In progress.''',
  out='''Recording (004), extraction (005), review (006), carry forward and
overdue (007).''',
  plan='''Extend the project; do not change its stack. Add the action item with
django-simple-history, belonging to the meeting it was raised in and
scoped to the hotel through 001's isolation, including the optional
anticipated result. "Add action" and "Edit" are ordinary Django forms
on the meeting page, like docs/mockup/mvp-app.html. Keep the form's
validation in one place: spec 006 reuses it for proposed items.
seed_demo also loads the seeded actions.''',
)

S004 = dict(n='004', id='004-record-and-transcribe', name='Record and Transcribe', short='Record and transcribe',
  builds='003: the meeting screen gains a Record button. 002: the transcript\nbelongs to the meeting.',
  when='Day 2, 10:30', stop='The meeting can be recorded and turned into text on screen.',
  goal='''Let the chair record the discussion in the meeting and get a written
transcript of it, without anyone typing.''',
  value='''FEH's voice-capture proof of concept (sequence steps 1 to 5): the
first half of "voice in, action items out". FEH's success measure for
release 1b starts here.''',
  actors=['Meeting chair'], cap='Voice Capture',
  ref='''docs/voice-capture-sequence.mmd steps 1 to 5; docs/reference.md
"MVP 1 · Voice capture"; docs/mockup/mvp-app.html Record page;
docs/sample/transcript.txt.''',
  frs=['''The system shall offer a "Record" button on the meeting screen that
opens the meeting's Record page.''',
       '''The system shall let the chair start and stop recording in the browser,
showing "Recording…" and a running timer while it records.''',
       '''The system shall, when recording stops, send the audio to the
transcription service and show "Transcribing…" until the text returns.''',
       '''The system shall show the transcript on the Record page under the
heading "Transcript", and keep it with the meeting.''',
       '''The system shall work without any AI service connected, returning the
sample transcript in docs/sample/transcript.txt (Constitution Principle
XVI).''',
       '''The system shall tell the chair, in plain words, when recording or
transcription fails, and let them try again.'''],
  nfrs=['''Only people of the meeting's hotel can record or see its transcript.''',
        '''The service connection details shall never appear on screen or in the
code (Principle XVI).'''],
  screen='''On today's Hotel A meeting, "Record" opens the Record page; "Start
recording" shows the timer; "Stop recording" shows "Transcribing…" and
then the sample transcript, beginning "John Lim: Next item."''',
  out='''Extracting action items (005), reviewing them (006), live streaming,
speaker recognition, uploading audio files.''',
  attention=['''The browser blocks the microphone, or there is no microphone.''',
             '''The chair records for a few seconds only, or for a long time.''',
             '''The chair leaves the page while recording.''',
             '''The transcription service is not connected (sample mode) or does not
answer.'''],
  plan='''Extend the project; do not change its stack. The Record page is an
ordinary Django page with a small script that uses the browser's
MediaRecorder and posts the audio to the server when recording stops.
Transcription goes through one adapter, transcribe(audio) -> text,
exactly as the constitution's Technology Standards describe: AI_PROVIDER
"sample" returns docs/sample/transcript.txt; "azure" calls Azure OpenAI
with AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY and
AZURE_OPENAI_TRANSCRIBE_DEPLOYMENT read from the environment (.env, in
.gitignore). Store the transcript with the meeting. Tests use sample.''',
)

S005 = dict(n='005', id='005-extract-proposed-items', name='Extract Proposed Action Items', short='Extract proposed items',
  builds='004: the transcript of the meeting. 003: the action fields, lists and\nvalidation that every proposed item must satisfy.',
  when='Day 2, 11:30', stop='The transcript becomes proposed action items, ready for the chair.',
  goal='''Turn the transcript into proposed action items with the same fields as
the action list, so nobody types them up.''',
  value='''FEH's voice-capture proof of concept (sequence steps 6 to 9): the
second half of "voice in, action items out". Release 1b target: proposed
items within 5 minutes of the meeting ending.''',
  actors=['Meeting chair'], cap='AI Extraction',
  ref='''docs/voice-capture-sequence.mmd steps 6 to 9; docs/reference.md
"MVP 1 · Voice capture" and "Lists"; docs/sample/items.json.''',
  frs=['''The system shall, after a transcript is ready, send it to the
extraction service with the action-item fields and show "Extracting
action items…".''',
       '''The system shall save each extracted item as Proposed for that meeting,
with market segment, issue category, issue, action required, owner,
priority, due date and anticipated result.''',
       '''The system shall only accept values from the fixed lists in
docs/reference.md and owners who are people of the meeting's hotel;
anything else is left empty for the chair to fill in.''',
       '''The system shall never add a proposed item to the meeting's action list
by itself (Constitution Principle XV).''',
       '''The system shall work without any AI service connected, returning the
sample items in docs/sample/items.json.''',
       '''The system shall tell the chair when extraction fails, keep the
transcript, and let them try again.'''],
  nfrs=['''Proposed items are kept, never deleted (Principle III).''',
        '''Due dates are worked out from the meeting date in the hotel's time
zone.'''],
  screen='''After the sample transcript, "Extracting action items…" turns into
three proposed items: Alex Wong's December corporate review, Priya Rao's
OTA weekend rates, Mary Tan's Company ABC escalation, each marked
"Proposed".''',
  out='''Editing, removing and confirming proposed items (006).''',
  attention=['''The transcript mentions a person who is not in the hotel.''',
             '''A due date is said as "by Monday" or "next week".''',
             '''The service returns a segment or category that is not in the list.''',
             '''The transcript contains no actions at all.'''],
  plan='''Extend the project; do not change its stack. Add a Proposed item model
(with django-simple-history) belonging to the meeting, with the action
fields and a state: Proposed, Confirmed or Removed. Extraction goes
through one adapter, extract(transcript, meeting) -> list of items,
exactly as the constitution's Technology Standards describe: "sample"
returns docs/sample/items.json; "azure" calls the chat deployment with a
JSON response format, the field list, the fixed lists, the hotel's
people and the meeting date. Validate every value against the lists and
the hotel's people before saving; leave invalid ones empty. Tests use
sample.''',
)

S006 = dict(n='006', id='006-review-and-confirm', name='Review and Confirm Proposed Items', short='Review and confirm',
  builds='005: the proposed items. 003: the action form and its validation,\nreused to edit proposed items and to create the confirmed actions.',
  when='Day 2, 1:30', stop='Speak, review, confirm: the voice-capture MVP is complete.',
  goal='''Let the chair check the proposed items, correct or remove them, and
confirm the right ones into the meeting's action list.''',
  value='''FEH's voice-capture proof of concept (sequence steps 10 to 13): the
chair stays in control of what the meeting records (Principle XV).
Release 1b target: at least 80% accepted without edits.''',
  actors=['Meeting chair'], cap='Human Review of AI Output',
  ref='''docs/voice-capture-sequence.mmd steps 10 to 13; docs/reference.md
"MVP 1 · Voice capture"; docs/mockup/mvp-app.html Review page.''',
  frs=['''The system shall show the meeting's proposed items on a Review page,
each with a checkbox (checked), its fields, a "Proposed" chip, "Edit"
and "Remove", and the note "Proposed by AI. Nothing is added to the
meeting until you confirm."''',
       '''The system shall let the chair edit a proposed item with the same form
and rules as an action (spec 003).''',
       '''The system shall not let an item with a missing required field be
confirmed, and shall say which field is missing.''',
       '''The system shall, on "Confirm selected (n)", add the selected items to
the meeting's action list as Open actions marked "From recording", mark
them Confirmed, and show "<n> actions confirmed.".''',
       '''The system shall mark removed items Removed; they never appear in the
action list.''',
       '''The system shall show, on the meeting screen, "<n> proposed items
waiting for review" with a "Review" link while any are waiting.'''],
  nfrs=['''Confirming is all-or-nothing for the selected items.''',
        '''Only people of the meeting's hotel can review its proposed items.'''],
  screen='''With the three sample items, the chair changes Priya Rao's priority,
removes nothing, and presses "Confirm selected (3)": the meeting shows
"3 actions confirmed." and the three actions under "Raised in this
meeting", marked "From recording".''',
  out='''Carry forward and overdue (007), re-running extraction, bulk editing.''',
  attention=['''The chair confirms nothing and leaves.''',
             '''Two people review the same proposed items at the same time.''',
             '''The chair records again before reviewing the first set.''',
             '''An owner was removed from the hotel since extraction.'''],
  plan='''Extend the project; do not change its stack. The Review page is an
ordinary Django page with one form for the selected items; Edit reuses
the action form and validation from 003. Confirming creates the
action items and marks the proposed items Confirmed in one database
transaction. The meeting screen shows the waiting banner, like
docs/mockup/mvp-app.html.''',
)

S007 = dict(n='007', id='007-carry-forward-and-overdue', name='Carry Forward and Overdue', short='Carry forward and overdue', stretch=True,
  builds='003: the actions and their statuses (including those confirmed in\n006). 002: the meeting dates that decide what is "earlier".',
  when='Day 2 stretch', stop='Open items carry forward and late ones stand out.',
  goal='''Make unfinished actions from earlier meetings appear in the next
meeting automatically, and make late actions impossible to miss.''',
  value='''FEH: "open items are easy to lose between weeks". Success measure:
open actions from earlier meetings appear in the next meeting, 100%.''',
  actors=['Meeting chair', 'Hotel team member'], cap='Meeting Continuity',
  ref='''FEH requirements FR-006 and FR-009; docs/mockup/mvp-app.html meeting
screen.''',
  frs=['''The system shall show, in every meeting, the hotel's actions from
earlier meetings that are Open, In progress or Blocked, under "Carried
forward from earlier meetings (n)", oldest first; actions raised in this
meeting under "Raised in this meeting (n)".''',
       '''The system shall show an action as overdue when its due date is before
today in the hotel's time zone and its status is Open, In progress or
Blocked, with "Overdue by n days" in red; "Due today" and "Due in n
days" otherwise.''',
       '''The system shall show the counts "Carried forward", "Raised in this
meeting" and "Overdue" at the top of each meeting.'''],
  nfrs=['''Overdue is worked out each time, never stored as a status.'''],
  screen='''Today's Hotel A meeting shows the seven open seeded actions carried
forward, three of them overdue in red, and the counters 7, 0 and 3.''',
  out='''Due this week, filters, reminders.''',
  attention=['''An action due today, seen late in the evening.''',
             '''Whether actions confirmed from a recording count as raised in this
meeting.'''],
  plan='''Extend the project; do not change its stack. Carry-forward and overdue
are queries on the existing models through 001's isolation; nothing is
copied or stored. Make "today" replaceable in tests.''',
)

SPECS = [S001, S002, S003, S004, S005, S006, S007]

SCHEDULE = '''Day 1 afternoon: draft, compare, specify and clarify 001–006; G1 for
all six. Late Day 1: execute 001. Day 2: execute 002–006 in order;
007 only if time allows. Azure OpenAI is optional: everything runs and
every test passes with AI_PROVIDER=sample (Principle XVI).'''
MINIMUM = '''**Minimum viable demonstration: through 006** (speak, review, confirm).
007 is a stretch goal, only after 006 is accepted.'''
EXTRA = ''' FEH's sequence:
docs/voice-capture-sequence.mmd; ours, spec by spec:
docs/mvp-sequence.mmd. Sample AI output: docs/sample/.'''

AZURE = '''---

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
'''

def markdown():
    md = R.markdown(SPECS, title='Meeting Action Tracker · MVP 1 Voice Capture — All Specs',
                    schedule=SCHEDULE, minimum=MINIMUM, extra_docs=EXTRA)
    md = md.replace('Entra ID, emails, export, Teams or AI, the task is wrong', 'Entra ID, emails, export or Teams, the task is wrong')
    k = md.index('---\n\n# 001')
    return md[:k] + AZURE + '\n' + md[k:]

if __name__ == '__main__':
    p = os.path.join(os.path.dirname(__file__), '..', 'starter', 'mvp1', 'docs', 'specs.md')
    open(p, 'w').write(markdown())
    print('wrote', os.path.normpath(p))
