# Reference — Meeting Action Tracker (workshop MVP)

Source: FEH "Meeting Action Tracker: Requirements" (13 Oct 2026) and its
screen mockups in docs/mockup/. This file fixes the data, labels and look
for the two-day workshop. All hotels, people and text below are invented.
Use exactly these.

## Workshop scope
A small MVP from MVP 1a, in two specs:
- 001 Meetings and the action list (carry-forward, overdue): built on Day 2
- 002 Updates and results (update log, result, outcome, change history):
  built only if time allows

Kept deliberately simple for the workshop:
- Each person belongs to one hotel and can do everything there. No roles,
  no read-only users, no group view.
- Sign-in: a "Sign in as" page lists the people below (stand-in for
  Microsoft Entra ID). No passwords.
- Results are text plus an outcome rating. No metrics, baselines,
  targets or currencies.
- One owner per item. No supporting owners, stay periods or linked
  references.
Not built in the workshop: My actions, email reminders, export, group roll-up,
microphone and AI (MVP 1b), Teams transcripts, Databricks, Azure hosting.

## Hotels
| Name    | Code | Time zone      |
|---------|------|----------------|
| Hotel A | HTA  | Asia/Singapore |
| Hotel B | HTB  | Asia/Singapore |

## People
| Name      | Email              | Hotel   |
|-----------|--------------------|---------|
| Mary Tan  | mary@tracker.demo  | Hotel A |
| John Lim  | john@tracker.demo  | Hotel A |
| Alex Wong | alex@tracker.demo  | Hotel A |
| Sam Ng    | sam@tracker.demo   | Hotel A |
| Priya Rao | priya@tracker.demo | Hotel A |
| Grace Teo | grace@tracker.demo | Hotel B |
| Lee Chen  | lee@tracker.demo   | Hotel B |

## Lists (fixed; seed exactly these)
Market segments: Corporate · MICE / Groups · Leisure / Transient · OTA ·
Wholesale · Government · Airline · Direct
Issue categories: Pace / pickup · Rate / ADR · Mix · Cancellations / wash ·
Competitor · Event / compression · Distribution · Service
Priority: High · Medium · Low (default Medium)
Status: Open · In progress · Blocked · Done · Cancelled (default Open).
"Overdue" is not a status: an item is overdue when its due date is before
today and its status is Open, In progress or Blocked.
Outcome rating: Not rated (default) · Achieved · Partially achieved ·
Not achieved · Not measurable

## Meetings in the seed
Hotel A, "Weekly performance meeting", chair John Lim, attendees Mary Tan,
John Lim, Alex Wong, Sam Ng, Priya Rao: Tue 29 Sep 2026 · Tue 6 Oct 2026 ·
Tue 13 Oct 2026, each at 10:00.
Hotel B, "Weekly performance meeting", chair Grace Teo, attendees Grace
Teo, Lee Chen: Wed 7 Oct 2026, 09:30.

## Action items in the seed
Hotel A (raised in the meeting on the date shown):
1. 29 Sep · MICE / Groups · Cancellations / wash · "Group wash risk for
   Company ABC" · "Contact company organizer for rooming list update" ·
   Mary Tan · Medium · due 16 Oct · Blocked · anticipated "Updated rooming
   list received and wash held under 10% of the block"
2. 29 Sep · OTA · Rate / ADR · "Parity gap on weekend rates" · "Adjust
   weekend rates on OTA channels" · Alex Wong · Medium · due 11 Oct ·
   In progress · anticipated "Weekend ADR 5% higher"
3. 29 Sep · MICE / Groups · Service · "Breakfast queue complaints from
   group" · "Open second breakfast station for groups over 40" · Sam Ng ·
   Medium · due 6 Oct · Done (closed 6 Oct by Sam Ng) · outcome Achieved ·
   actual "No complaints in the next two group stays"
4. 6 Oct · Corporate · Pace / pickup · "Corporate segment below forecast" ·
   "Review upcoming opportunities for sales" · John Lim · High · due
   10 Oct · In progress · anticipated "Corporate pickup back on forecast"
5. 6 Oct · Government · Pace / pickup · "Forecast not submitted" · "Send Q4
   forecast to regional office" · Mary Tan · Medium · due 9 Oct ·
   In progress · anticipated "Forecast submitted"
6. 13 Oct · Leisure / Transient · Event / compression · "Concert on 14 Nov
   compresses demand" · "Set minimum stay for 13 to 15 Nov" · Sam Ng ·
   High · due 20 Oct · Open · anticipated "ADR higher on 14 Nov"
7. 13 Oct · Airline · Distribution · "Crew block release date not
   confirmed" · "Confirm release date with airline contact" · Priya Rao ·
   Low · due 23 Oct · Open · anticipated "Block confirmed"
8. 13 Oct · Wholesale · Pace / pickup · "Wholesale pickup behind forecast"
   · "Call top three wholesale partners" · Mary Tan · Medium · due 20 Oct ·
   Open
Hotel B:
9. 7 Oct · Corporate · Pace / pickup · "Two key accounts slowing" · "Meet
   both accounts' travel managers" · Grace Teo · High · due 12 Oct ·
   In progress
10. 7 Oct · Leisure / Transient · Competitor · "New hotel opening nearby" ·
   "Prepare rate response plan" · Lee Chen · Medium · due 21 Oct · Open

Update log for item 1 (spec 002): 29 Sep 10:40 John Lim "Item raised. Mary
to contact the organizer for an updated rooming list." · 9 Oct 15:20 Alex
Wong changed status In progress → Blocked · 13 Oct 10:12 Mary Tan
"Organizer has not replied to two emails. Raised again in today's meeting."

Provide a management command, seed_demo, that clears the database and
loads exactly this data. Store dates and times in UTC; show them in the
hotel's time zone.

## Screens and exact labels
Desktop browser. Follow the images in docs/mockup/, leaving out anything
this file says is not built.
Top bar (all screens): "Action Tracker" · "Meetings" · the person's name
and hotel · "Sign out".
- Sign in as: heading "Sign in", one button per person showing name and
  hotel; note "Workshop sign-in. Microsoft Entra ID replaces this page in
  the real product."
- Meetings (spec 001): the hotel's meetings, newest first, each with date,
  title, chair and number of open items; button "New meeting". New meeting
  form: "Date", "Time", "Title" (default "Weekly performance meeting"),
  "Chair", "Attendees", "Teams meeting link" (optional); button
  "Create meeting".
- Meeting screen (spec 001): docs/mockup/01-meeting-screen.png. Counters
  "Carried forward", "Raised in this meeting", "Overdue". Columns
  "Market segment", "Issue category", "Issue", "Action required", "Owner",
  "Priority", "Due", "Status". Group headings "Carried forward from earlier
  meetings (n)" and "Raised in this meeting (n)". Under each issue "Raised
  <date>". Due cell shows the date and "Overdue by n days" (red),
  "Due today" or "Due in n days". A blank entry row at the bottom. Save
  status "All changes save automatically. Saved just now." Not built:
  "Record meeting", "Export Excel / PDF", "Complete meeting", "Due this
  week", filters, "Anticipated / actual" column.
- Item detail (spec 002): docs/mockup/03-item-detail.png, simplified to
  sections "Issue and action", "Ownership and timing" (owner, due date,
  status, priority), "Result" (fields "What we expect", "What happened",
  "Outcome rating"), "Update log" (field "Add a comment", button "Post
  comment"), "Change history". Buttons "Cancel item", "Mark as done".

## Look (sampled from FEH's mockups)
Font: Inter (Google Fonts). Page background #F3F5F7, cards #FFFFFF with
a 1px border #DDE3E8 and 8px corners. Top bar #0E2A33 with white text.
Text #14202B, secondary text #5B6670. Primary button #0F6B6B with white
text; secondary buttons white with a #C9D2D9 border.
Overdue text #B42318. Group rows: carried forward #EAF0F3, raised in
this meeting #E3F1F0.
Priority chips: High #FDECEC on #B42318 · Medium #FDF3DC on #8A5200 ·
Low #EEF1F4 on #34454F.
Status dots: Open #4A5A68 · In progress #1F4F99 · Blocked #8A5200 ·
Done #0B7A55 · Cancelled #9AA3AB.
Owner shown as initials in a circle (#E3EAEE) followed by the name.
Buttons and inputs at least 40px tall.
