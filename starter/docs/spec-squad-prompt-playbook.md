# The Spec Squad Prompt Playbook

**How the whole workshop was built with an AI agent, prompt by prompt.**

The guide site, the constitution, the run sheets, the clickable mockups, the
setup checks, the QR page, the badge maker, the certificate, the facilitator
script and the social posts were all built by one facilitator working with
an AI agent, in conversation, over a few days. This playbook gives you that
conversation as a reusable series of prompts, in order, so you can run your
own Spec-Driven Development workshop or project the same way.

Two AI roles, two kinds of prompt:

| | The agent that builds the **material** | The agent that builds the **app** |
|---|---|---|
| Tool | A general AI agent (Claude, in our case) | GitHub Copilot in Agent mode with Spec Kit |
| Builds | Constitution, specs, mockups, guide, scripts, graphics | The working MVP, spec by spec |
| Prompts | This playbook | The `/speckit-*` blocks in the guide |

Replace everything in `<angle brackets>`. Paste one prompt, read the result,
then send the next. The quality comes from the review between prompts, not
from the prompts alone.

---

## The rules we prompted by

1. **Give context once, up front.** Who it's for, when, how long, what tools they have, what they are not allowed to do.
2. **Ask for a plan before changes.** "Review first, don't change anything yet" saved hours.
3. **One request per message.** Small asks are easy to check and easy to undo.
4. **Say who reads it.** "Participants are beginners and may not be developers" changed every page for the better.
5. **When you don't understand something, say exactly that,** and paste the confusing text. That is the most useful prompt in this playbook.
6. **Make it check its own work.** Open the page, click through it, run the commands, test on a phone.
7. **Protect the client.** Synthetic data only, no keys in chat, no client name on personal posts, temporary files removed afterwards.

---

## Phase 0 · Frame the engagement

```
I'm running a <2>-day hands-on Spec-Driven Development workshop for
<CLIENT> on <DATES> in <CITY>, co-facilitated with <NAME>.
Audience: <N> people from <CLIENT>, mixed developers and non-developers,
many using AI coding tools for the first time.
Tools they will have: VS Code, GitHub Copilot (Agent mode, <N> AI credits
each), GitHub Spec Kit. Stack for the app: <e.g. Django + SQLite>.
Goal: by the end of Day 2 every participant has the same small MVP running
locally, built from specs the client approved, with tests.
Constraints: synthetic data only, no client systems, keys never in code
or chat.

Before building anything, propose: the outcome of each day, the
deliverables (site, docs, mockups, scripts), and the risks. Don't create
files yet.
```

```
Give me a brief summary again: what is the expected outcome of each day?
```

---

## Phase 1 · From the client's requirements to a scope

```
Here are <CLIENT>'s requirements: <attach or paste>. Read them first and
don't change anything. What does the client actually want, and what can a
room of beginners realistically build and demo in two days?
Propose an MVP scope we can suggest to them, with what we leave out and why.
```

When the client sends their own idea (a diagram, a sketch):

```
This is a <sequence diagram / sketch> the client sent: <attach>.
Read it first, don't change anything yet. What does the client want, and
is it achievable within the session? What do we need from them to make
it work (access, keys, data)?
```

```
Draft a short email to <CONTACT>. We propose the features; we don't ask
them to choose from scratch. Highlight exactly what we need from them:
<e.g. AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, deployment names>.
Keep it short.
```

```
Let's run two tracks with the same method:
- MVP 1 · <new idea>: its own guide, mockup and run sheet.
- MVP 2 · <original plan>: its own guide, mockup and run sheet.
They share ONE constitution. Show me your plan first, don't change
anything yet.
```

---

## Phase 2 · The constitution

```
Write the project constitution in GitHub Spec Kit format: Core Principles,
Technology Standards, Development Workflow (with gates G1 client approves
the spec, G2 tech lead approves plan and tasks, G3 both accept), Definition
of Done, Governance with versioning.
Every principle must be testable: something a reviewer could reject a pull
request for, with a Rationale that cites the client's requirement ID.
Include: <client-specific rules, e.g. hotel isolation, nothing deleted>,
synthetic data only, test-first, traceability (every acceptance criterion
has a test whose name contains its ID), keep it small, change through the
spec, stop and report, and secrets stay out of the code.
```

```
Add a principle: each spec is an increment on the one before. It states
what it builds on, extends the app without rebuilding it, and every
earlier spec's tests must still pass. Bump the version and update the
Definition of Done.
```

---

## Phase 3 · The run sheet: specs in order

```
Split the MVP into 5–7 specs. One spec = one capability you can see on
screen = one commit. For each spec give: ID, name, business goal, what it
builds on, functional requirements, what it looks like on screen, out of
scope, and a "stop line" (if the room stops here, what works?).
Mark the minimum viable demo and the stretch specs.
Then write, for every spec, the exact blocks participants paste:
/speckit-specify, /speckit-clarify (with "give particular attention to"
edge cases), /speckit-plan, /speckit-tasks, /speckit-implement.
Specify blocks contain no technology; the plan blocks follow the
constitution's Technology Standards.
```

```
Make sure each spec is clearly an incremental feature on the previous
one, and say so in every spec and every plan prompt.
```

```
Are tests included? Show me where each acceptance criterion gets its test.
```

```
Write a reference file with the invented data everyone builds with:
<organisations, people, sample records, labels, colours>, so every
participant's app looks and behaves the same.
```

---

## Phase 4 · Mockups the agent can build from

```
Where is the mockup design based on the client's screens? Create HTML
versions first, so the AI agent can easily refer to them.
```

```
Make it one clickable MVP app, not separate pages: every screen in the
run sheet, working navigation, the invented data from the reference file,
and the exact labels. No backend; plain HTML, CSS and a little JavaScript.
```

```
Publish it on the site as an "interactive mockup" with a clear banner:
this is the target, we build the production MVP from it in the workshop.
Update every guide page that should link to it, and point every plan
prompt at it.
```

---

## Phase 5 · Diagrams

```
For each track, add a Mermaid sequence diagram of the MVP, spec by spec,
render it as SVG for the site, and keep the .mmd source in the docs pack.
```

---

## Phase 6 · The guide site

```
Build the workshop guide as a static site on GitHub Pages
(repo <owner>/<repo>): a slide-per-step guide with a sidebar of steps,
progress saved in the browser, Back / Done → next buttons, and a Copy
button on every prompt and command.
Day 1: why SDD, Spec Kit anatomy, who writes what, the constitution,
the client's brief, how to write a spec, each spec slide (draft, compare
with the answer key, specify, clarify, G1).
Day 2: one Execute slide per spec (switch branch, plan, tasks, analyze,
G2, implement, converge, run it, G3, commit).
Every step shows "You should see:" and "If it fails:".
```

```
Generate the MVP 1 guide from the MVP 2 guide with a build script, so the
shared Day 1 teaching stays identical and I only edit one source.
```

```
Make the guide available only from <TIME, DATE, TIMEZONE>. Before then the
links show "Guide opens at <TIME>". No push needed at that time.
```

```
Add a button to export the whole guide as PDF: every slide, light theme,
answer keys expanded.
```

---

## Phase 7 · Laptop setup that people can do alone

```
Create a laptop setup page for Mac and Windows: Git, VS Code with the
code command, Python, uv, Node, Spec Kit, GitHub Copilot Chat, and a
company-network (certificate) fix. Each step: what it is for, the
command, what you should see, what to do if it fails.
Add one-line check scripts (bash and PowerShell) that print OK or FAIL
per tool and name the step to redo.
```

```
Step 1 · Set up your workspace: be specific, not "create your project".
Every command in order, from opening a terminal to Copilot listing the
/speckit commands. Create the folder on the Desktop so people can find it.
```

---

## Phase 8 · Beginner-proofing (the most valuable phase)

These are the prompts we sent after reading our own guide as a
first-timer. Use them on every page.

```
I don't understand this: "<paste the confusing text>".
Be specific: it will be read by someone trying Spec Kit for the first time.
```

```
You didn't explain how to open Copilot Chat in VS Code, or what to do if
the extension isn't installed. Add it to <page/step>.
```

```
"<paste the slide>". Participants are beginners and may not be
developers. Rewrite it in plain words: what you do, what happens, what you
check. Keep the commands, explain the words.
```

```
When is the Git branch created? Is it per spec? Show it on each spec
slide, and how to see which branch you're on.
```

When something doesn't behave as the guide says, paste what you saw:

```
The folder is created, but not the Git branch. Here is the output:
<paste>. Find out why from the tool's current documentation and fix the
guide.
```

```
So you updated everything, including the guide? Check every page, the run
sheets and the docs packs, and confirm what's live.
```

---

## Phase 9 · The room on the day

```
Create a page with tabs of QR codes for the room: countdown, MVP 1 guide,
MVP 2 guide, badge maker, certificate (unlocks at the end of Day 2), and
Wi-Fi. Show the full URL under each code; clicking a code opens it.
```

```
Make a badge maker: participants add their name, role and stack, pick a
look, download a badge and a 1080×1920 story, with a caption to copy and
the facilitators' LinkedIn to tag.
```

```
Make a certificate page that unlocks at <TIME, DATE> with the
participant's name, downloadable as PDF and easy to add to LinkedIn.
```

```
Give me the spiel I need to follow as facilitator: for every time slot,
what to say, what to show, what the room does, and what usually goes
wrong. Add answers to likely questions. I'll read it on my phone.
```

---

## Phase 10 · Sharing the story

```
What graphic or video should I post on social media for Day <N>?
No client name, logo or screens on my personal posts.
```

```
Make a 5-slide carousel (1080×1350) on how Spec-Driven Development works:
the cycle, the three gates, increments, and the Day 2 outcome. Put both
facilitators' profiles on it. Add it to my "<canvas name>" design canvas.
```

```
Turn the carousel into an animated video for mobile, 4:5 for the feed and
9:16 for stories, for LinkedIn and Facebook.
```

```
Add a Day 2 teaser for the facilitators, with a quote. Then write a short
Taglish caption for Facebook.
```

---

## Phase 11 · After the workshop

```
Create a deployment spec to put the MVP online on Vercel as a private
demo, in the same Spec Kit format: constitution amendment first, then
specify, clarify, plan, tasks, implement, gates. Put it in a Markdown file.
```

```
Add the steps for creating the accounts (GitHub repository, Vercel
account), and setting each environment variable:
<list the variables>. Never put a value in code, a commit or a chat.
```

```
Add it to the guide for both tracks, titled "Deployment spec", and add a
slide on how to clone the guide repository:
https://github.com/<owner>/<repo>.git
```

```
Extract the series of prompts that built all of this into a Markdown
file I can share with participants.
```

---

## Prompts for when the agent goes wrong

```
Stop. That's not what I asked. I asked for <X>. Undo <Y> and do only <X>.
```

```
It doesn't work: <what you clicked, what you expected, what happened>.
```

```
Check your work: open the page, click through it, and show me a screenshot
before you tell me it's done.
```

```
Don't do the change yet. Tell me your plan and what it will affect.
```

And for Copilot while building the app (from the guide's Gotchas slide):

```
Stop. Constitution Principle XI, Keep It Small: nothing is built that an
approved acceptance criterion doesn't ask for. List anything you added
beyond the spec, remove it, confirm all tests still pass, then stop and
report.
```

```
Stop. Constitution Principle XII, Change Through the Spec: do not change
the code for this yet. Amend the specification with new acceptance
criteria for the change, show me the changed criteria, and wait for G1
re-approval.
```

---

## What made it work

- **Specs before code, for the material too.** We asked for plans before changes, the same way the workshop asks for specs before code.
- **Small asks, checked every time.** Most prompts above are one or two lines.
- **"I don't understand" is a feature request.** Every confusing line we pasted back became a clearer slide.
- **Humans decide.** The agent drafted everything; the facilitators approved every page, as FEH and VISEO approved every spec.

*AI builds. Humans decide.* Welcome to the Spec Squad.
