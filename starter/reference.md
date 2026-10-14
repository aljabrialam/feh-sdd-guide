# Reference — Meeting Action Tracker (workshop build)

Source: FEH "Meeting Action Tracker: Requirements" (13 Oct 2026) and its
five screen mockups in docs/mockup/. This file fixes the data, labels and
look for the two-day workshop. All hotels, people and figures below are
invented. Use exactly these.

## Workshop scope
Built in the workshop: a slice of MVP 1a (specs 001 to 004).
Stubbed for the workshop:
- Microsoft Entra ID sign-in (FR-003): replaced by a "Sign in as" page that
  lists the seeded users. No passwords anywhere.
- Properties, members, segments, categories and metrics (FR-001, FR-019):
  seeded, and editable in the Django admin by the group admin.
Not built in the workshop: email reminders (FR-017), Excel and PDF export
(FR-018), microphone capture and AI extraction (MVP 1b), Databricks and
Teams (Phase 2 and Final), Azure hosting.

## Properties
| Code | Name    | Currency | Time zone      | Weekly meeting   |
|------|---------|----------|----------------|------------------|
| HTA  | Hotel A | SGD      | Asia/Singapore | Tuesday 10:00    |
| HTB  | Hotel B | SGD      | Asia/Singapore | Wednesday 09:30  |
| HTC  | Hotel C | SGD      | Asia/Singapore | Thursday 10:00   |

## People and roles
A person can hold a different role in each property.
| Name       | Email             | Roles                                       |
|------------|-------------------|---------------------------------------------|
| Mary Tan   | mary@tracker.demo | Member at Hotel A                           |
| John Lim   | john@tracker.demo | Property admin at Hotel A (chairs meetings) |
| Alex Wong  | alex@tracker.demo | Member at Hotel A; Read-only at Hotel B     |
| Sam Ng     | sam@tracker.demo  | Member at Hotel A                           |
| Priya Rao  | priya@tracker.demo| Member at Hotel A                           |
| Lee Chen   | lee@tracker.demo  | Member at Hotel A; Member at Hotel B        |
| Grace Teo  | grace@tracker.demo| Property admin at Hotel B                   |
| Ben Tay    | ben@tracker.demo  | Member at Hotel C                           |
| Chris Lau  | chris@tracker.demo| Group viewer (all properties, counts only)  |
| Dana Ong   | dana@tracker.demo | Group admin (Django admin access)           |

Roles: Member · Property admin · Read-only (per property);
Group viewer · Group admin (all properties).

## Shared lists (group admin maintains; seed exactly these)
Market segments: Corporate · MICE / Groups · Leisure / Transient · OTA ·
Wholesale · Government · Airline · Direct
Issue categories: Pace / pickup · Rate / ADR · Mix · Cancellations / wash ·
Competitor · Event / compression · Distribution · Service
Target metrics: Room nights · ADR · Revenue · Occupancy · RevPAR · Pickup ·
Group conversion
Fixed lists (not admin-maintained):
- Status: Open · In progress · Blocked · Done · Cancelled.
  "Overdue" is not a status: an item is overdue when its due date is before
  today and its status is Open, In progress or Blocked.
- Priority: High · Medium · Low (default Medium)
- Outcome rating: Achieved · Partially achieved · Not achieved ·
  Not measurable · (blank = not rated)
- Actual value source: Manual (System arrives in Phase 2)
- Item source: Manual (AI-captured and Imported arrive later)

## Meetings in the seed
Hotel A, "Weekly performance meeting", chair John Lim, attendees Mary Tan,
John Lim, Alex Wong, Sam Ng, Priya Rao, Lee Chen:
Tue 22 Sep 2026 · Tue 29 Sep 2026 · Tue 6 Oct 2026 · Tue 13 Oct 2026
(all Completed).
Hotel B, "Weekly performance meeting", chair Grace Teo, attendees Grace Teo,
Lee Chen: Wed 7 Oct 2026 · Wed 14 Oct 2026 (Completed).
Hotel C, chair Ben Tay: Thu 8 Oct 2026 (Completed).

## Action items in the seed
Hotel A (raised in the meeting on the date shown):
1. 6 Oct · Corporate · Pace / pickup · "Corporate segment below forecast" ·
   "Review upcoming opportunities for sales" · John Lim · High · due 10 Oct ·
   In progress · stay 1–30 Nov · anticipated "Target 4,600 room nights" ·
   Room nights, baseline 4,200, target 4,600
2. 29 Sep · MICE / Groups · Cancellations / wash · "Group wash risk for
   Company ABC" · "Contact company organizer for rooming list update" ·
   Mary Tan (supporting: Alex Wong) · Medium · due 16 Oct · Blocked ·
   stay 22–25 Oct · anticipated "Updated rooming list received and wash
   held under 10% of the block" · Room nights, baseline 80, target 110
3. 22 Sep · OTA · Rate / ADR · "Parity gap on weekend rates" · "Adjust
   weekend rates on OTA channels" · Alex Wong · Medium · due 11 Oct ·
   In progress · stay 16–31 Oct · anticipated "ADR 5% higher" · ADR,
   baseline 210, target 220
4. 6 Oct · Government · Pace / pickup · "Forecast not submitted" · "Send Q4
   forecast to regional office" · Mary Tan · Medium · due 9 Oct ·
   In progress · stay 1 Nov–31 Dec · anticipated "Forecast submitted"
5. 13 Oct · Leisure / Transient · Event / compression · "Concert on 14 Nov
   compresses demand" · "Set minimum stay for 13 to 15 Nov" · Sam Ng · High ·
   due 20 Oct · Open · stay 13–15 Nov · anticipated "ADR higher on 14 Nov" ·
   ADR, baseline 230, target 280
6. 13 Oct · Airline · Distribution · "Crew block release date not confirmed"
   · "Confirm release date with airline contact" · Priya Rao · Low · due
   23 Oct · Open · stay 1–15 Dec · anticipated "Block confirmed"
7. 13 Oct · Wholesale · Pace / pickup · "Wholesale pickup behind forecast" ·
   "Call top three wholesale partners" · Mary Tan · Medium · due 20 Oct · Open
8. 13 Oct · Corporate · Rate / ADR · "Rate sheet expires 31 Oct" · "Refresh
   corporate rate sheet" · Mary Tan · Medium · due 24 Oct · Open
9. 22 Sep · MICE / Groups · Service · "Breakfast queue complaints from group"
   · "Open second breakfast station for groups over 40" · Lee Chen · Medium ·
   due 29 Sep · Done (closed 29 Sep by Lee Chen) · outcome Achieved ·
   actual "No complaints in the next two group stays"
10. 29 Sep · Direct · Distribution · "Website booking engine slow" · "Raise
   ticket with booking engine vendor" · Priya Rao · Low · due 6 Oct ·
   Cancelled (closed 6 Oct by John Lim) · note "Vendor fixed it before
   ticket was raised"
Hotel B:
11. 7 Oct · Corporate · Pace / pickup · "Two key accounts slowing" · "Meet
   both accounts' travel managers" · Grace Teo · High · due 12 Oct ·
   In progress
12. 14 Oct · Leisure / Transient · Competitor · "New hotel opening nearby" ·
   "Prepare rate response plan" · Lee Chen · Medium · due 21 Oct · Open
Hotel C:
13. 8 Oct · OTA · Mix · "OTA share above target" · "Shift budget to direct
   campaigns" · Ben Tay · Medium · due 22 Oct · Open
Update log for item 2: 29 Sep 10:40 John Lim "Item raised. Mary to contact
the organizer for an updated rooming list." · 9 Oct 15:20 Alex Wong status
In progress → Blocked, due 14 Oct → 16 Oct · 13 Oct 10:12 Mary Tan
"Organizer has not replied to two emails. Raised again in today's meeting."

Provide a management command, seed_demo, that clears the database and
loads exactly this data. Store dates and times in UTC; show them in the
property's time zone (NFR-007).

## Screens and exact labels
Desktop and tablet browser. Follow the images in docs/mockup/.
Top bar (all screens): "Action Tracker" · property switcher (only the
properties the user belongs to) · "Meetings" · "My actions" ·
"Group view" (group viewers only) · "Admin" (group admin only) · the user's
name and role at the current property.
- Sign in as (workshop only): heading "Sign in", one button per seeded user
  showing name and roles; footer note "Workshop sign-in. Microsoft Entra ID
  replaces this page in the real product."
- Meetings (spec 001): newest first; button "New meeting". New meeting form:
  "Date", "Title" (default "Weekly performance meeting"), "Chair",
  "Attendees", "Teams meeting link" (optional); button "Create meeting".
- Meeting screen (spec 001): docs/mockup/01-meeting-screen.png. Counters
  "Carried forward", "Raised in this meeting", "Overdue", "Due this week".
  Grid columns "Market segment", "Issue category", "Issue",
  "Action required", "Owner", "Priority", "Due", "Status",
  "Anticipated / actual". Group headings "Carried forward from earlier
  meetings (n)" and "Raised in this meeting (n)". Due cell shows the date
  and "Overdue by n days" (red) or "Due in n days". Hint "Press Tab to move
  to the next cell, Enter to add the next row." Save status "All changes
  save automatically. Saved just now." Buttons "Complete meeting".
  "Record meeting" and "Export Excel / PDF" are not built in the workshop.
- Item detail (spec 002): docs/mockup/03-item-detail.png. Sections
  "Issue and action", "Ownership and timing", "Anticipated result",
  "Actual result", "Update log" (field "Add a comment", button
  "Post comment"), "Change history". Buttons "Cancel item", "Mark as done".
- My actions (spec 003): docs/mockup/02-my-actions.png. Tabs
  "My open actions (n)", "Overdue (n)", "Due this week (n)",
  "All open at <property> (n)", "Done (n)". Panel "Changes by others on
  your items" with an "n new" badge.
- Group roll-up (spec 004): docs/mockup/05-group-rollup.png.
- docs/mockup/04-review-proposed-items.png is MVP 1b: not built.

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
Desktop and tablet browsers; buttons and inputs at least 40px tall.
