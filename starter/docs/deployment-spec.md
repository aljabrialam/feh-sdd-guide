# Deployment Spec — 008 Online Demo on Vercel

Spec Kit run sheet for putting the workshop MVP online, so FEH can open it
from any laptop or phone without installing anything. It works for either
track: it builds on the last spec the room accepted at G3 (006 for MVP 1,
005 for MVP 2).

| | |
|---|---|
| Feature ID | `008-online-demo-vercel` |
| Builds on | The last accepted spec (MVP 1: 006 · MVP 2: 005) |
| When | After the workshop, or Day 2 stretch once the MVP is accepted |
| Gates | Constitution amendment → G1 (FEH) → G2 (VISEO) → G3 (both) |
| Result | A private demo link FEH can open; same app, same tests, invented data only |

---

## Before you start · accounts and access (facilitator, about 15 minutes)

Do these once, before G1, so the deploy steps at the end just work.
Copilot does none of this: accounts and keys are a person's job
(Principle XVI).

### 1. Put the project on GitHub

Vercel deploys from a GitHub repository.

1. Sign in at **github.com** with the GitHub account you use for Copilot.
2. Click **+ → New repository**. Name it, for example, `feh-app-demo`.
   Choose **Private**. Leave "Add a README" unticked. Click
   **Create repository**.
3. In the terminal, inside `feh-app`, connect and push every branch:

   ```
   git remote add origin https://github.com/<your-username>/feh-app-demo.git
   git push -u origin --all
   ```

   ✓ You should see: the branches (`main`, `001-…`, `002-…`, …) listed on
   the repository page.

   Before pushing, check that `.env` is in `.gitignore` and not in the
   repository: `git ls-files .env` must print nothing.

### 2. Create the Vercel account

1. Go to **vercel.com/signup**.
2. Choose **Continue with GitHub** and sign in with the same GitHub
   account. This links the two, so Vercel can see your repositories.
3. Pick a plan:
   - **Hobby** (free) is for personal, non-commercial projects.
   - A demo for a client is commercial use, so use **Pro**, which has a
     free trial, or a VISEO team account if one exists. Ask Tony which
     VISEO uses.
4. Name the team (for example "VISEO SDD Demo") and finish sign-up.
5. When Vercel asks to install the **Vercel GitHub app**, choose
   **Only select repositories** and pick `feh-app-demo`. Vercel then
   sees only this repository.

   ✓ You should see: the Vercel dashboard, with "Import Git Repository"
   listing `feh-app-demo`.

### 3. Sign in to Vercel from the terminal

Node is already installed from the laptop setup, so no extra install is
needed:

```
npx vercel login
```

Choose **Continue with GitHub**; the browser opens, confirm, and come
back to the terminal.

✓ You should see: "Congratulations! You are now signed in."

### 4. Agree with FEH

- **The access code** for the demo, and who receives it (asked again in
  clarify).
- **The Azure OpenAI values** (MVP 1 only), if the demo should use real
  AI. Without them it runs on the sample transcript.

---

## Step 0 · Amend the constitution first (Principle XII, Governance)

The constitution today says SQLite only and puts "Azure hosting" out of
scope (Principle XI). Hosting a demo is a scope change, so it is amended and
agreed **before** `/speckit-specify`. Paste into Copilot Chat:

```
/speckit-constitution

Amend the constitution to version 1.3.0 (MINOR: added scope and a
technology standard). Reason: FEH wants to open the MVP online as a
private demo after the workshop.

1. Principle XI. Keep It Small: add one sentence:
   "A private online demo of the accepted MVP on Vercel is in scope
   (spec 008). Production hosting on Azure stays out of scope."

2. Technology Standards: add a bullet:
   "- **Online demo**: Vercel (Python runtime), region Singapore.
     PostgreSQL from the Vercel Marketplace when DATABASE_URL is set;
     SQLite locally and in every test. Keys and the demo access code
     only in Vercel environment variables (Principle XVI)."

3. Principle IV (Synthetic Data Only) applies to the online demo too:
   add "This includes the online demo."

Update the Sync Impact Report, the version line and Last Amended date.
Change nothing else.
```

FEH and VISEO agree in the room, then commit:

```
git add -A
git commit -m "docs: constitution 1.3.0 - online demo in scope"
```

---

## Specify and clarify (G1)

```
/speckit-specify

Create a Feature Specification.

Feature ID
008-online-demo-vercel

Feature Name
Online Demo

Business Goal
Let FEH open the accepted MVP from any laptop or phone through a private
web address, without installing anything, so people who were not in the
workshop can try it.

Business Value
The MVP currently runs only on participants' laptops. A shared online
demo lets FEH show it to stakeholders, collect feedback and decide the
next phase with everyone looking at the same app.

Business Actors
FEH stakeholder (opens the demo)
Workshop facilitator (shares the link, resets the demo)

Business Capability
Demo Access

Reference
docs/constitution.md (Principles II, IV, XI, XVI). docs/reference.md
"Hotels" and "People".

Builds On
The last accepted spec of the chosen track (MVP 1: 006, MVP 2: 005).
The app's screens, rules and tests stay exactly as accepted; this spec
only makes the same app reachable online.

Functional Requirements

FR-001 The system shall be reachable at a secure web address (https)
that opens on a laptop or phone browser.

FR-002 The system shall ask for a demo access code before showing any
page. Without the right code, nothing from the app is shown.

FR-003 The system shall show a visible "Demo · invented data" label on
every page.

FR-004 The system shall start with exactly the demo data in
docs/reference.md, and shall keep changes made in the demo between
visits.

FR-005 The facilitator shall be able to reset the demo to the starting
data in docs/reference.md.

FR-006 Every capability accepted at G3 shall behave online exactly as it
does locally, including "Sign in as" and hotel isolation.

FR-007 (MVP 1 only) Recording shall work in the browser online. When the
AI service is not connected, the app shall use the sample transcript and
say so on screen.

FR-008 No key, password or access code shall appear in the code, the
repository, a spec or on screen.

Non-Functional Requirements

The first page shall appear within 5 seconds on a normal connection.
Data shall only ever be the invented data from docs/reference.md.

What It Looks Like On Screen
Opening the link shows "Enter the demo access code". After the right
code, the usual "Sign in as" page appears, with "Demo · invented data"
in the top bar. Everything after that looks like the accepted MVP.

Out of Scope
Microsoft Entra ID, Azure hosting, a custom domain, real FEH data,
emails, backups, monitoring, more than one demo environment.

Label every acceptance criterion AC-008-<nn>.
Generate the specification following the GitHub Spec Kit format.
Do not generate implementation details.
Do not generate source code.
```

```
/speckit-clarify

Review Feature Specification 008-online-demo-vercel.

Identify missing requirements, ambiguity, assumptions, missing
validation, missing error handling, missing non-functional
requirements, and missing acceptance criteria.

Give particular attention to:
- Who gets the access code, and how long it stays valid.
- Someone types a wrong access code several times.
- Two people use the demo at the same time and change the same item.
- The demo is reset while someone is using it.
- (MVP 1) The browser blocks the microphone, or the recording is very
  long.
- What FEH should see if the online demo is down.

Review every functional requirement. Suggest improvements. Update the
specification where necessary. Make sure every acceptance criterion has
an ID AC-008-<nn> and describes behaviour a person can observe.

When a question is about a business rule, wait for the answer FEH gives
in the room. Do not invent business rules.

Do not generate implementation. Do not generate source code.
```

**G1:** FEH approves. Record it with the gate prompt (`specs/008-online-demo-vercel/gates/G1.md`) and commit.

### Answer key · acceptance criteria to expect

Compare what Copilot writes with this list:

| ID | Acceptance criterion |
|---|---|
| AC-008-01 | Opening the demo link on a laptop and on a phone shows the access-code page over https. |
| AC-008-02 | A wrong code shows "That code is not right" and nothing from the app; the right code opens "Sign in as". |
| AC-008-03 | Every page shows "Demo · invented data" in the top bar. |
| AC-008-04 | After a reset, the meetings and items match docs/reference.md exactly. |
| AC-008-05 | A change made in the demo is still there when the page is reopened later. |
| AC-008-06 | Signed in as Grace Teo (Hotel B), no Hotel A data can be opened, even by typing its address. |
| AC-008-07 | (MVP 1) With no AI keys set, recording and stopping shows the sample transcript and a note that the sample is in use. |
| AC-008-08 | Searching the repository finds no key, password or access code. |

---

## Execute (G2, G3)

Switch to the spec's branch and bring in the accepted MVP first:

```
git checkout 008-online-demo-vercel
git merge <last accepted branch, e.g. 006-review-and-confirm>
```

```
/speckit-plan

Plan Feature Specification 008-online-demo-vercel, following the
constitution's Technology Standards exactly (version 1.3.0).

This spec is an increment (Principle IX). It builds on the last accepted
spec. Reuse what is there; do not rebuild or restructure it. Every
earlier spec's tests must still pass, locally on SQLite.

Hosting: Vercel, Python runtime. Vercel detects manage.py at the
repository root and uses WSGI_APPLICATION = "tracker_site.wsgi.application".
Dependencies come from pyproject.toml (uv). Add vercel.json with
"regions": ["sin1"] and a functions entry for tracker_site/wsgi.py with
"maxDuration": 60 (MVP 1 transcription can take several seconds).

Settings, all from environment variables, with local defaults unchanged:
- SECRET_KEY from DJANGO_SECRET_KEY; DEBUG off when VERCEL is set.
- ALLOWED_HOSTS includes ".vercel.app"; CSRF_TRUSTED_ORIGINS includes
  "https://*.vercel.app".
- Database: PostgreSQL from DATABASE_URL when it is set (Vercel
  Marketplace Postgres, e.g. Neon), otherwise SQLite. Add psycopg.
  Tests always use SQLite.
- STATIC_ROOT set; Vercel runs collectstatic and serves static files
  from its CDN. HTMX stays a static file, never a CDN link.

Database set-up: a build script in [tool.vercel.scripts] runs
"python manage.py migrate --noinput". seed_demo is run by the
facilitator from a laptop against DATABASE_URL (vercel pull), and the
same command is the reset (FR-005).

Access code (FR-002): one middleware in the tracker app that, before
anything else, asks for the code in DEMO_ACCESS_CODE and remembers it in
the session. When DEMO_ACCESS_CODE is not set (local, tests), the gate
is off. Wrong codes never reveal anything from the app.

Demo label (FR-003): shown in the top bar when VERCEL is set.

MVP 1 only: keep the request under Vercel's 4.5 MB body limit by
limiting a recording to 5 minutes and saying so on the Record page.
AI_PROVIDER stays "sample" unless the Azure values are set in Vercel's
environment variables.

Add tests for: the access gate (on, off, wrong code), the demo label,
and settings reading DATABASE_URL. No test may need the network or keys.

Check the result against docs/mockup/mvp-app.html: apart from the code
page and the demo label, nothing on screen changes.
```

```
/speckit-tasks

Generate tasks for 008-online-demo-vercel from the plan. Tests first for
each task (Principle VI). Keep one task per capability: settings,
access gate, demo label, Vercel configuration, database and seed,
documentation of the deploy steps in quickstart.md.
```

```
/speckit-analyze
```

**G2 checks (VISEO):**
- Every AC-008 criterion maps to at least one test
- No secret in any file; every key is an environment variable
- Local run and every earlier test unchanged (`uv run pytest`)
- Nothing planned beyond the spec: no Entra ID, no Azure, no custom domain

Record G2 with the gate prompt, then:

```
git add -A
git commit -m "plan: 008-online-demo-vercel"
```

```
/speckit-implement

Implement 008-online-demo-vercel task by task, tests first. Stop after
the last task and report what was built, the test results, and any
acceptance criterion you could not satisfy (Principle XIII). Do not
deploy, and do not create any account or key.
```

```
/speckit-converge
```

---

## Deploy (facilitator, once)

Done by a person, not by Copilot. Needs the accounts from
"Before you start": the project on GitHub, a Vercel account linked to
it, and `npx vercel login` done.

First push the accepted spec: `git push origin 008-online-demo-vercel`.

1. **Import the project:** in the Vercel dashboard, **Add New → Project**,
   find `feh-app-demo` and click **Import**. Vercel shows "Django"
   as the framework; keep the detected settings and don't click Deploy
   yet. Open **Environment Variables** first (step 3), or deploy and
   redeploy after setting them.
2. **Add the database:** in the project, **Storage → Marketplace →
   Postgres** (for example Neon) and connect it. This sets `DATABASE_URL`.
3. **Set the environment variables.** These are the app's settings and
   secrets. They live only in Vercel, never in the code, a commit, a
   spec or a chat (Principle XVI). `DATABASE_URL` is already there from
   step 2; don't add it yourself.

   **a. Prepare the values first**, in a private note you delete
   afterwards:

   | Name | Value | Where it comes from |
   |---|---|---|
   | `DJANGO_SECRET_KEY` | a long random string | Generate it with the command below |
   | `DEMO_ACCESS_CODE` | the code FEH agreed | Clarify. At least 8 characters, not a word anyone would guess |
   | `AI_PROVIDER` | `sample` | Use `azure` only when all four Azure values below are set |
   | `AZURE_OPENAI_ENDPOINT` | `https://<feh-resource>.openai.azure.com` | MVP 1 only, from FEH |
   | `AZURE_OPENAI_KEY` | the key | MVP 1 only, from FEH |
   | `AZURE_OPENAI_TRANSCRIBE_DEPLOYMENT` | transcription deployment name | MVP 1 only, from FEH |
   | `AZURE_OPENAI_CHAT_DEPLOYMENT` | chat deployment name | MVP 1 only, from FEH |

   Generate the secret key in the terminal, inside `feh-app`:

   ```
   uv run python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

   ✓ You should see: one line of about 67 random characters. Copy it as
   the value of `DJANGO_SECRET_KEY`.

   **b. Add them in the Vercel dashboard**, one at a time:

   1. Open the project, then **Settings → Environment Variables**.
   2. Under **Key**, type the name exactly as in the table, in capitals
      with underscores, for example `DJANGO_SECRET_KEY`.
   3. Under **Value**, paste the value, with no spaces or quotes around it.
   4. Under **Environments**, tick **Production** and **Preview**. Leave
      **Development** unticked unless you use `vercel dev`.
   5. For `DJANGO_SECRET_KEY`, `DEMO_ACCESS_CODE` and `AZURE_OPENAI_KEY`,
      switch on **Sensitive**, so the value can't be read back later.
   6. Click **Save**. Repeat for the next variable.

   ✓ You should see: the list shows every name from the table plus
   `DATABASE_URL`, with sensitive values hidden.

   **Or add them from the terminal**, one command per variable. Each
   command asks for the value, so it never appears on screen or in the
   terminal history:

   ```
   npx vercel env add DJANGO_SECRET_KEY production
   npx vercel env add DEMO_ACCESS_CODE production
   npx vercel env add AI_PROVIDER production
   ```

   Run the same commands with `preview` instead of `production` for the
   preview builds. For MVP 1 with real AI, add the four `AZURE_OPENAI_…`
   variables the same way, then change `AI_PROVIDER` to `azure`.

   **c. Apply them.** Vercel only uses new or changed variables in the
   next build. After any change, open **Deployments**, click **⋯** on the
   latest one and choose **Redeploy**.

   **Never:** put these values in `.env` files you commit, in
   `vercel.json`, in a screenshot, or in the Teams chat. If a key leaks,
   ask FEH to rotate it, update it here and redeploy.

4. **Deploy:** push the `008-online-demo-vercel` branch (Vercel builds a
   preview), or merge to `main` for the production address.
5. **Load the demo data** from your laptop, in the project folder:

   ```
   npx vercel link
   npx vercel env pull .env.local
   uv run --env-file .env.local python manage.py seed_demo
   ```

   Run the same last line to reset the demo (FR-005).
6. **Share:** send FEH the address and the access code separately.

## G3 · FEH and VISEO accept

- On a phone and a laptop: the code page, then "Sign in as", then the MVP
- Every AC-008 criterion has a passing test whose name contains its ID
- All earlier specs' tests still pass locally
- Grace Teo still sees no Hotel A data online
- (MVP 1) Record → transcript → proposed items → confirm works online
- No key or code anywhere in the repository

Record G3, then:

```
git add -A
git commit -m "feat: 008-online-demo-vercel"
```

---

## Risks and notes

- **Data resets only when you run seed_demo.** The demo keeps changes
  until then; reset before each stakeholder session.
- **Anyone with the link and code can sign in as anyone.** "Sign in as"
  is a workshop stand-in; Microsoft Entra ID replaces it in production.
  Keep the code to the people FEH names.
- **Synthetic data only** (Principle IV): never load real FEH data into
  the demo, even briefly.
- **Cost:** the demo fits Vercel's Hobby plan and a free Postgres tier for
  light use; check current limits before sharing widely. Vercel's own
  password protection for deployments is a paid feature, which is why
  the access code is built into the app.
- **Production is a different spec:** Azure hosting, Azure Database for
  PostgreSQL and Entra ID stay out of scope and start from FEH's
  requirements, not from this demo.
