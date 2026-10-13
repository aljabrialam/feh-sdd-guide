# SDD Workshop Guide — FEH × VISEO

A single-page, slide-style guide for the two-day Spec-Driven Development workshop with Far East Hospitality: Day 1 agrees and approves the specs, Day 2 builds a working slice from them. Every prompt and command has a Copy button, and each participant's progress is saved in their own browser.

| File | What it is | Published |
|---|---|---|
| `index.html` | Countdown (announcement page) | now |
| `setup.html` + `check-setup.sh` / `.ps1` | Laptop setup and check scripts | now |
| `mockup/` | Backup app's target screens | now |
| `certificate.html` | Certificate of completion: name, role, PNG/PDF, LinkedIn. Unlocks 16 Oct 4:30 pm SGT (preview: `?preview=feh-sdd`) | now (locked) |
| `badge.html` | Badge maker: name, stickers, doodle, lanyard, PNG and story download | now |
| `guide.html` | Workshop guide (Day 1) | Day 1 morning |
| `day2.html` | Day 2 build slides | Day 2 morning |

No build step and no dependencies.

## Deploy to GitHub Pages

```bash
cd feh-sdd-guide
git init -b main
git add -A
git commit -m "Workshop guide"
gh repo create feh-sdd-guide --public --source=. --push
gh api -X POST repos/{owner}/feh-sdd-guide/pages -f "source[branch]=main" -f "source[path]=/"
```

The site appears at `https://<your-username>.github.io/feh-sdd-guide/` after a minute or two.

Without the `gh` CLI: create the repo on github.com, push, then go to **Settings → Pages → Build and deployment → Deploy from a branch → main / (root)**.

## Laptop setup page

`setup.html` is the participant setup guide: Mac and Windows steps with copy buttons, a saved checklist and troubleshooting. The AI agent is **GitHub Copilot** (Copilot Chat in VS Code, Agent mode) with Spec Kit 1.1+ in its default skills mode: `specify init . --integration copilot`, skills under `.github/skills/`, invoked as `/speckit-specify` etc.

**Check scripts:** `check-setup.sh` (Mac/Linux) and `check-setup.ps1` (Windows) must be uploaded to the repo root next to `setup.html`; participants run them straight from GitHub Pages and send a screenshot. They only read versions and build a throwaway Django project in a temp folder, which they delete.

## Countdown page

`index.html` is the announcement page: a live countdown to Thursday 15 October 2026, 9:00 am Singapore time, with the VISEO × FEH logos. Share `https://aljabrialam.github.io/feh-sdd-guide/`. When the time arrives it switches to "We're live" with a button to the guide.

**Final countdown:** press `L` (the very bottom-right corner is also an invisible click target) for a full-screen 5-4-3-2-1 with sound and confetti, ending on "Let the hackathon begin!". Press `Esc` to go back. Click once on the page first if the browser blocks sound.

## Mockup

`mockup/` holds the backup app's seven target screens: an HTML page and a PNG for each, a gallery (`mockup/index.html`) and a zip of everything. Publish the folder with the guide; the Reference slide links to it. Copy the PNGs into the starter repo's `docs/mockup/` so the agent can use them.

## Releasing Day 2

The Day 2 slides are in `day2.html`, separate from the main page. While that file is missing from the site, the guide shows an "Unlocks on Day 2" slide in its place; once it is published, the Day 2 slides appear automatically.

- **Before and during Day 1:** do not commit `day2.html` to the repo. Anything in a public repo can be read on GitHub even if the page doesn't show it. Keep it in a folder outside the repo.
- **Morning of Day 2:**

```bash
cp ~/workshop-private/day2.html .
git add day2.html
git commit -m "Release Day 2"
git push
```

GitHub Pages updates within a minute or two; participants refresh the page.

**Previewing locally:** opening `guide.html` straight from disk always shows Day 2 as locked. To preview with Day 2, run `python3 -m http.server` in the folder and open `http://localhost:8000/guide.html`.

## Branding

- **Logo:** the white VISEO logo is embedded in `guide.html` (sidebar and first slide). `logo.svg` is the same artwork as a separate file; the page does not need it to run.
- **Colours and font:** edit the `VISEO BRAND TOKENS` block at the top of `guide.html`.

- **FEH logo:** the Far East Hospitality logo is embedded in `index.html` and `day2.html`, shown in white on the dark background. `feh-logo.svg` is the same artwork for reference.

## Share a specific step

Each slide has its own link, for example `.../feh-sdd-guide/#s001` for Spec 001 or `#flow` for the agenda.

## Edit the content

Each slide is a `<section class="slide">` in `index.html`. Any `<pre data-label="...">` block gets a Copy button automatically. Inside a `<pre>`, write `<` as `&lt;`, `>` as `&gt;` and `&` as `&amp;`.

## Always the newest version

Every page carries a build stamp. When a browser opens a cached copy, the page checks the server, and if a newer build exists it loads it once, then tidies the address back to the plain link. Before each commit, run:

```bash
python3 tools/stamp.py
```
