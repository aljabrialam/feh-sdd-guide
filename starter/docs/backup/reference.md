# Reference — Guest Service Requests (backup idea)

Only used if the room switches to the backup idea. Its target screens are
in docs/backup/mockup/; replace docs/mockup/ with docs/backup/mockup/ in
the backup prompts.

All names, rooms and accounts below are invented. Use exactly these.

## Seed data
Properties:
- Riverside Suites, code RS
- Garden Residence, code GR

Rooms:
- RS: 0312 0406 0618 0715 0907 1002 1204 1309 1501 1608
- GR: 0205 0301 0410 0512 0607 0709 0803 0911 1004 1106

Guests with a current stay (room, last name):
- RS: 1204 Tan · 0907 Lim · 0312 Kumar · 1501 Wong · 0618 Rahman
- GR: 0205 Lee · 0410 Ng · 0803 Chen

Staff (password for all: demo1234):
- aisyah@riverside.demo  Aisyah  Housekeeping  RS
- ravi@riverside.demo    Ravi    Engineering   RS
- mei@garden.demo        Mei     Housekeeping  GR
- joel@garden.demo       Joel    Engineering   GR

Authentication: JWT. Guest token after "Identify your stay" (8 hours,
that stay only). Staff access token 30 minutes, refreshed silently for
up to 8 hours; "Sign out" ends it.

No service requests in the seed. Reference numbers are the property
code plus a 4-digit sequence per property, starting at 0001: RS-0001.

## Request types and times
Types: Housekeeping, Maintenance, Amenities, Other
Preferred times: Any time · This afternoon (2pm – 5pm) ·
This evening (5pm – 9pm) · Tomorrow morning (9am – 12pm)

## Screens and exact labels
Guest (desktop browser; content centred, at most 720px wide):
1. Identify your stay — fields "Room number", "Last name"; button "Continue"
2. New request — type buttons "Housekeeping", "Maintenance", "Amenities",
   "Other"; field "Describe it in a few words"; select "When suits you?";
   button "Send request"; link "My requests"
3. Request received — shows reference, status, type, description,
   preferred time; buttons "View my requests", "Make another request"
4. My requests — newest first; each shows type, status, description,
   reference, time; button "New request"
5. Request detail (spec 003) — status history, "How did we do?" with
   1–5 stars, field "Comment", button "Send rating"
Staff (desktop browser, full width):
6. Staff sign in — fields "Email", "Password"; button "Sign in";
   wrong details show "Email or password is incorrect."
7. Open requests — oldest first; columns Waiting, Room, Type, Request,
   Preferred, Status; type filter buttons; row buttons "Pick up" and
   "Mark done"; field "Completion note"

## Look
Font: Figtree (Google Fonts). Background #F5F6F3, text #1C2B2A,
secondary text #4A5856, accent #0E6E66, borders #C9D0CE.
Status badges: Submitted #E6ECF7 on #23407A · In progress #FCEFD9 on
#7A4B16 · Done #DFF0EA on #0B5A44. Rounded corners 12–16px.
Buttons and inputs at least 44px tall.
