# Meeting Action Tracker: Requirements

13 Oct 2026

## Overview

The Meeting Action Tracker records every action agreed in the weekly performance meeting, who owns it, when it is due and whether it worked. It replaces the current spreadsheet with a shared record of actions and outcomes across the hotels in the group.

**Context.** Each week, team leaders review performance and react to market conditions. Each issue is assigned an action and a responsible person. Today this lives in a spreadsheet with five columns (issue, action required, owner, due date, status) and a meeting date. Results are not recorded, and open items are easy to lose between weeks.

**What changes.** The tracker adds market segment, issue category, anticipated and actual results (text and numbers), an update history and an audit trail. In the final product, it listens to the meeting and proposes the action items, so no one types them up.

**Scope.** Hotel industry; multi-property; each property’s data is separate. Built on Django and Python, hosted on Azure Container Apps.

**Out of scope for now.** Raising items across properties; group-level meetings; attachments; revenue-impact estimates; writing back to Databricks or the property management system.

**Success measures (proposed targets, to be confirmed).**

- Every action has an owner and a due date: 100%.
- Open actions from earlier meetings appear automatically in the next meeting: 100%.
- Actions with an actual result recorded within 14 days of the stay period ending: 80% or more.
- Release 1b: proposed action items available within 5 minutes of the meeting ending, with at least 80% accepted by the chair without edits.

## Release plan

The tracker ships in five steps. The data-entry screen (1a) ships first and is not held up by the AI work (1b). Live microphone audio is the first listening source; Teams transcripts replace it in the final product.

| Release | What it delivers                                                                                                                   | Outcome                                        |
|---------|------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------|
| MVP 1a  | Data-entry and tracking: properties, meetings, inline action grid, carry-forward, audit trail, reminders, export, basic group view | The spreadsheet is retired                     |
| MVP 1b  | Listen from live microphone: record, transcribe, extract proposed items, review queue                                              | Items are drafted from the meeting             |
| Phase 2 | Databricks connector for actual results, dashboards, recurring-issue detection, escalation, result-review prompts, weekly digest   | Results are measured, not typed                |
| Final   | Teams transcript ingestion via Microsoft Graph, update detection, automatic meeting summary, Teams notifications                   | Hands-free capture, including remote attendees |
| Later   | Group-level meetings, attachments, revenue impact, export of tracker data to Databricks                                            | Wider reporting                                |

## Users, roles and permissions

Access is strictly within a property. A user sees and edits items only for properties where they are a member, and any member can edit any item in that property. Because editing is open, the audit trail and owner notifications are core features.

| Role           | Scope          | Can do                                                                                                             |
|----------------|----------------|--------------------------------------------------------------------------------------------------------------------|
| Member         | One property   | Create meetings; create and edit all action items; add updates; record results; export                             |
| Property admin | One property   | Everything a member can do, plus manage the property’s members and settings (meeting day and time, reminder rules) |
| Read-only      | One property   | View items, meetings and exports                                                                                   |
| Group viewer   | All properties | Read-only roll-up across properties; cannot open or edit items                                                     |
| Group admin    | All properties | Maintain properties, segments, issue categories, statuses and metric definitions                                   |

A person can hold a different role in each property, for example Property admin at Hotel A and Read-only at Hotel B. Sign-in uses Microsoft Entra ID single sign-on.

## Information captured

The tracker stores a meeting with many action items, and each item has a running log of updates. The spreadsheet’s single table becomes the following records.

| Record                       | Purpose                                                                         |
|------------------------------|---------------------------------------------------------------------------------|
| Property                     | A hotel: name, code, currency, time zone, meeting day and time, Databricks code |
| Membership                   | Links a user to a property with a role                                          |
| Meeting                      | One weekly meeting for one property: date, attendees, Teams link, transcript    |
| Action item                  | The issue, the action, the owner, the due date and the result                   |
| Action update                | A dated comment or status change on an item                                     |
| Segment                      | Shared market segment, with its Databricks code                                 |
| Issue category               | Shared list, such as pace or rate                                               |
| Metric definition            | A measurable result (room nights, ADR, RevPAR) and where Databricks holds it    |
| Transcript and proposed item | Meeting text and the AI-suggested items awaiting review (1b onward)             |
| Audit entry                  | Who changed what, when, with old and new values                                 |

**Action item fields**

| Field                                | Description                                                                                                                    | Release                         |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|---------------------------------|
| Meeting raised in                    | The meeting where the item was created                                                                                         | 1a                              |
| Market segment                       | Dropdown from the shared segment list (Corporate, MICE/Groups, Leisure/Transient, OTA, Wholesale, Government, Airline, Direct) | 1a                              |
| Issue category                       | Pace/pickup, Rate/ADR, Mix, Cancellations/wash, Competitor, Event/compression, Distribution, Service                           | 1a                              |
| Issue                                | Free text                                                                                                                      | 1a                              |
| Action                               | Free text                                                                                                                      | 1a                              |
| Owner                                | One primary owner (a user), plus optional supporting owners                                                                    | 1a                              |
| Priority                             | High, Medium, Low                                                                                                              | 1a                              |
| Due date                             | Date                                                                                                                           | 1a                              |
| Status                               | Open, In progress, Blocked, Done, Cancelled; Overdue is calculated                                                             | 1a                              |
| Date raised, closed date, closed by  | Stamped automatically                                                                                                          | 1a                              |
| Stay period affected                 | Start and end date the issue relates to                                                                                        | 1a                              |
| Anticipated result                   | Free text                                                                                                                      | 1a                              |
| Target metric                        | Room nights, ADR, Revenue, Occupancy, RevPAR, Pickup, Group conversion                                                         | 1a                              |
| Baseline and target value            | Numbers, with the property’s currency where relevant                                                                           | 1a                              |
| Actual result                        | Free text                                                                                                                      | 1a                              |
| Actual value                         | Number, with value source (Manual or System), as-of time and override reason                                                   | 1a (System values from Phase 2) |
| Outcome rating                       | Achieved, Partially achieved, Not achieved, Not measurable                                                                     | 1a                              |
| Source                               | Manual, AI-captured or Imported                                                                                                | 1a                              |
| Transcript snippet and AI confidence | Where in the transcript the item came from                                                                                     | 1b                              |
| Linked reference                     | Group, company or booking ID, for example Company ABC                                                                          | Phase 2                         |
| Carry-over count                     | How many meetings the item has rolled through                                                                                  | Phase 2                         |
| Revenue impact, attachments          | Estimated and actual value; supporting files                                                                                   | Later                           |

## MVP 1a: data entry and tracking

MVP 1a replaces the spreadsheet. The IDs below match the SpecKit file.

| ID     | Requirement                                                                                                                                                   |
|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FR-001 | A group admin creates and edits properties: name, code, currency, time zone, meeting day and time, reminder settings, Databricks property code.               |
| FR-002 | A user can be a member of several properties, with a separate role in each.                                                                                   |
| FR-003 | Users sign in with Microsoft Entra ID single sign-on. There are no local passwords.                                                                           |
| FR-004 | A member creates a meeting for a property with a date, title and attendees, and optionally a Teams meeting link.                                              |
| FR-005 | The meeting screen shows an inline grid in which items are added and edited like a spreadsheet, with keyboard navigation and autosave.                        |
| FR-006 | A new meeting opens with all open items from earlier meetings of the same property already listed.                                                            |
| FR-007 | Each item holds the fields listed under Information captured.                                                                                                 |
| FR-008 | An item has one primary owner chosen from the property’s members, plus optional supporting owners.                                                            |
| FR-009 | Status moves through Open, In progress, Blocked, Done and Cancelled. Overdue is calculated from the due date. Closing an item records who closed it and when. |
| FR-010 | Each item has an update log of dated comments and status changes, showing who made them.                                                                      |
| FR-011 | Anticipated and actual results are captured as text and as numbers (baseline, target, actual) against a chosen metric, with an outcome rating.                |
| FR-012 | Every actual value records its source (Manual or System), an as-of time and, if overridden, a reason.                                                         |
| FR-013 | Any member of a property can create and edit any item in that property. No one can see or edit another property’s items.                                      |
| FR-014 | Every change is audited with who, when, old value and new value. Items are never hard-deleted.                                                                |
| FR-015 | The owner is notified when another person changes their item.                                                                                                 |
| FR-016 | Users filter by segment, owner, status, category, priority, due date and stay period. Ready-made views: My actions, Overdue, Due this week.                   |
| FR-017 | Owners receive email reminders for items due soon and overdue. Timing is set per property.                                                                    |
| FR-018 | A meeting’s action list exports to Excel and PDF for circulating minutes.                                                                                     |
| FR-019 | A group admin maintains segments, issue categories and metric definitions without a developer.                                                                |
| FR-020 | Group viewers see a read-only roll-up of open and overdue items by property and segment.                                                                      |
| FR-021 | A meeting can store the Teams meeting link and ID for later transcript matching.                                                                              |

## MVP 1b: listen from live microphone

The app records the meeting through the browser microphone, turns speech into text and proposes action items. A person always confirms an item before it enters the record. Only people in the room are heard, so remote attendees are captured only if their audio plays through the room speakers. This limitation goes away when Teams transcripts arrive in the final product.

| ID     | Requirement                                                                                                                                                                                                   |
|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FR-030 | A Record meeting button on the meeting screen starts and stops microphone capture. The screen shows a clear recording indicator and a consent notice.                                                         |
| FR-031 | Speech is transcribed in near real time with Azure AI Speech, using a custom vocabulary of hotel terms (wash, pickup, rooming list, ADR, RevPAR, block, cut-off, pace).                                       |
| FR-032 | The transcript is stored with the meeting. The extraction pipeline accepts any transcript with optional speaker labels, so the source can change later without rework.                                        |
| FR-033 | When the meeting ends, or on demand, Azure OpenAI extracts proposed items: segment, issue, action, owner, due date and anticipated result, each with a confidence score and a link to the transcript snippet. |
| FR-034 | Spoken names are matched to the property’s attendees and relative dates (for example, next Friday) are resolved against the meeting date. Ambiguous matches are flagged for the reviewer.                     |
| FR-035 | A review queue lets the chair accept, edit, reject or merge each proposed item. Only accepted items become action items. The AI never writes to the record directly.                                          |
| FR-036 | Audio is deleted once the transcript is confirmed, and no later than 7 days after the meeting (to be confirmed). The transcript is kept under the retention policy.                                           |
| FR-037 | If the connection drops, audio is buffered and the meeting can be extracted later from the stored transcript.                                                                                                 |

## Phase 2 and final product

Phase 2 makes results measurable and adds insight. The final product makes capture hands-free.

| ID     | Release | Requirement                                                                                                                                                                                               |
|--------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FR-040 | Phase 2 | A read-only connector fills actual values from Azure Databricks after the stay period ends, and stamps them as System with an as-of time. A manual override requires a reason and keeps the system value. |
| FR-041 | Phase 2 | Baseline and target values are pre-filled from Databricks budget, forecast or last-year data where available.                                                                                             |
| FR-042 | Phase 2 | Dashboards show completion rate by owner and segment, average days to close, anticipated versus actual hit rate and recurring issues.                                                                     |
| FR-043 | Phase 2 | Recurring issues are flagged when the same segment and category reappear across meetings.                                                                                                                 |
| FR-044 | Phase 2 | Escalation rules notify the chair when an item is overdue by a set number of days.                                                                                                                        |
| FR-045 | Phase 2 | When a stay period passes, the owner is prompted to record or confirm the actual result.                                                                                                                  |
| FR-046 | Phase 2 | A weekly digest of open items is sent before each meeting.                                                                                                                                                |
| FR-047 | Phase 2 | Items gain a carry-over count and a linked reference (group, company or booking ID).                                                                                                                      |
| FR-050 | Final   | Transcripts and attendee lists are retrieved from Teams through Microsoft Graph after each meeting, replacing the microphone as the main source.                                                          |
| FR-051 | Final   | Spoken updates in later meetings (for example, the ABC group wash was resolved) are matched to existing items and proposed as updates, not duplicates.                                                    |
| FR-052 | Final   | A meeting summary is generated alongside the action list.                                                                                                                                                 |
| FR-053 | Final   | Reminders and digests can be delivered in Teams as well as email.                                                                                                                                         |
| Later  | Later   | Group-level meetings, attachments, estimated and actual revenue impact, and a nightly export of tracker data to Databricks for BI.                                                                        |

## Integrations

**Azure Databricks (Phase 2).** Databricks holds the performance data, so the tracker reads actual results from it and never writes back.

- The tracker connects through a SQL Warehouse with a read-only Entra ID service principal.
- It reads curated gold-layer views, not raw tables, so the data team can change internals without breaking the tracker. Each metric definition stores the view, column, aggregation and filter.
- Each property and each segment stores its Databricks code, so one shared segment mapping serves every hotel.
- A scheduled job pulls values in one batch after a stay period closes (and nightly for periods in progress) and caches them in the tracker’s database. Pages never query Databricks directly.
- To confirm with the data team: granularity (segment by stay date by property), data latency, who owns the curated views, and whether budget and forecast figures are available.

**Microsoft Teams (final product).** Teams is the long-term meeting source because some participants join remotely.

- After a meeting ends, the app retrieves the transcript and attendee list through Microsoft Graph, matched by the stored Teams meeting ID.
- Teams provides speaker-attributed text, so owner matching uses real attendee identities.
- Assumed available for now. IT must confirm that transcription is enabled in the tenant and that Graph transcript permissions can be granted with an application access policy. If not, microphone capture stays the permanent source.

**Microsoft Entra ID.** Single sign-on for all users, from MVP 1a.

## Non-functional requirements and architecture

| ID      | Requirement                                                                                                                                        |
|---------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| NFR-001 | Property isolation is enforced in one place in the data layer, so no query can return another property’s items.                                    |
| NFR-002 | The audit trail is complete and cannot be edited by users.                                                                                         |
| NFR-003 | Available during business hours at 99.5% or better (proposed).                                                                                     |
| NFR-004 | The meeting screen loads in under 2 seconds for 100 items, and an inline edit saves in under 1 second.                                             |
| NFR-005 | Secrets are held in Azure Key Vault; services use managed identity where possible.                                                                 |
| NFR-006 | Transcripts and rate or forecast data are treated as commercially sensitive: encrypted at rest and in transit, access limited to property members. |
| NFR-007 | Dates and times are stored in UTC and shown in the property’s time zone. Actual values record their currency.                                      |
| NFR-008 | The interface works on current desktop browsers and tablets, and meets WCAG 2.1 AA.                                                                |
| NFR-009 | Logs, metrics and alerts are available for the web app, scheduled jobs and the extraction pipeline.                                                |
| NFR-010 | The listening pipeline is built as three swappable stages: Source, Transcript, Extraction.                                                         |

**Azure design**

- **Web app:** Django on Azure Container Apps, with HTMX for the inline grid. In 1b, the transcription connection (WebSocket) needs a longer ingress timeout and a minimum of one replica so it does not scale to zero during a meeting.
- **Database:** Azure Database for PostgreSQL Flexible Server.
- **Scheduled work:** Azure Container Apps Jobs run Django management commands for reminders and the Databricks pull. Extraction runs on a worker once 1b ships.
- **Email:** Azure Communication Services Email.
- **Speech and AI:** Azure AI Speech and Azure OpenAI.
- **Storage:** Blob Storage for temporary audio, and later attachments.
- **Audit:** django-simple-history on every tracked model.
- **Sign-in:** Entra ID through OpenID Connect.

## Decisions, assumptions and open items

**Decisions made**

- Multi-property from day one; all data is scoped to a property.
- Any property member can edit any item in that property; the audit trail is the safeguard.
- Actual results are entered manually first, then pulled from Azure Databricks.
- Anticipated and actual results are captured as both text and numbers.
- Segments are one shared global list. Items are raised and visible only within a property.
- Teams is the final meeting source. Live microphone audio is used first.

**Assumptions to confirm**

- Issue categories are also a shared global list maintained by the group admin.
- Statuses are a fixed list, because overdue and closing logic depends on them. Segments, categories and metrics are admin-maintained.
- The data-entry screen (1a) ships before the microphone feature (1b).
- “Some participants can be removed” was read as “some participants join remotely”.
- Audio is kept at most 7 days; transcripts are kept 12 months. Both figures are proposals.
- Teams transcript access is assumed to be allowed by IT.

**Open items**

- Databricks: available granularity, latency and owner of the curated views.
- IT: Teams transcription policy and Microsoft Graph permissions.
- Does the chair or the owner confirm the outcome rating?
- Audio and transcript retention periods, and any legal or privacy review needed for recording meetings.
