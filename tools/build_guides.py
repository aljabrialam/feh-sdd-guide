#!/usr/bin/env python3
"""Keep both workshop tracks' guides in step.

MVP 2 (meeting action tracker) is the hand-edited guide: guide.html and day2.html.
This script
  1. refreshes the files embedded in guide.html (constitution, reference) and its
     delivery-order table from the docs and tools/runsheet.py;
  2. derives MVP 1 (voice capture): guide-mvp1.html and day2-mvp1.html, from the MVP 2
     pages plus tools/runsheet_mvp1.py. Shared Day 1 teaching stays identical.

Run after editing the docs, the run sheets or the MVP 2 pages:
    python3 tools/runsheet.py && python3 tools/runsheet_mvp1.py
    python3 tools/build_guides.py && python3 tools/build_docs.py && python3 tools/stamp.py
"""
import os, re, sys, html
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
sys.path.insert(0, HERE)
import runsheet as R2
import runsheet_mvp1 as R1
E = html.escape


def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)
def bounds(s, sid):
    i = s.index('<section class="slide" id="%s"' % sid)
    return i, s.index('</section>', i) + len('</section>')
def get(s, sid):
    i, j = bounds(s, sid); return s[i:j]
def replace(s, sid, new):
    i, j = bounds(s, sid); return s[:i] + new.strip() + s[j:]
def remove(s, sid):
    i, j = bounds(s, sid); return s[:i] + s[j:]
def rep(s, a, b, count=1):
    assert a in s, 'not found: ' + a[:90]
    return s.replace(a, b) if count == 0 else s.replace(a, b, count)
def pre(label, text, tall=False):
    return '<pre%s data-label="%s">\n%s</pre>' % (' class="tall"' if tall else '', label, E(text))
def catch(path, what):
    return ('<div class="note"><b>Match the room before moving on</b>Compare your %s with the approved version on the big screen. '
            'Different, or fell behind? The facilitator posts the approved file in the Teams chat. Paste this into Copilot Chat, then paste the approved file underneath:</div>\n'
            '  <pre data-label="Prompt · catch up to the room\'s approved version">\n'
            'Replace the contents of %s with the approved\n'
            'version below, exactly as written. Do not change any other file.</pre>') % (what, path)
def embed(s, label, text):
    a = s.index('data-label="%s">' % label) + len('data-label="%s">' % label)
    b = s.index('</pre>', a)
    return s[:a] + '\n' + E(text.rstrip()) + s[b:]
def order_table(specs):
    rows = '\n'.join('    <tr><td>%d</td><td><b>%s</b> %s%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
        i + 1, s['n'], E(s['name']), ' <span class="muted">stretch</span>' if s.get('stretch') else '', E(s['builds'].split(':')[0]), E(s['when']), E(s['stop']))
        for i, s in enumerate(specs))
    return '<table>\n    <tr><th>Order</th><th>Spec</th><th>Builds on</th><th>When</th><th>If you stop here</th></tr>\n%s\n  </table>' % rows
def set_order_table(s, specs):
    i = s.index('<section class="slide" id="idea"')
    a = s.index('<table>', s.index('Answer key: VISEO', i)); b = s.index('</table>', a) + len('</table>')
    return s[:a] + order_table(specs) + s[b:]


# ---------------------------------------------------------------- slide builders
GATES = {
    'G1': ('Specification approval', 'spec.md', "the FEH product owner's name", 'Product owner, Far East Hospitality',
           "one line per answer FEH gave in clarify (the Clarifications section of spec.md)"),
    'G2': ('Plan approval', 'plan.md', "the VISEO technical lead's name", 'Technical lead, VISEO',
           "one line per main technical choice in plan.md (for example where hotel isolation is enforced)"),
    'G3': ('Acceptance', 'spec.md', "the FEH product owner's name and the VISEO technical lead's name", 'FEH and VISEO',
           "what was shown on screen, and how many pytest and Playwright tests passed"),
}
def gate_prompt_text(sid, g):
    title, doc, who, role, dec = GATES[g]
    return ('Create the file specs/%(id)s/gates/%(g)s.md with the content below.\n'
            'Fill in each part in round brackets, then remove the brackets.\n'
            'Do not change any other file.\n\n'
            '# %(g)s — %(title)s\n\n'
            'Spec: specs/%(id)s/%(doc)s\n'
            'Approved by: (%(who)s), %(role)s\n'
            'Date: (today\'s date)\n'
            'Decision: Approved\n\n'
            'Business decisions made at this gate:\n'
            '- (%(dec)s)\n\n'
            'Conditions:\n'
            '- None\n\n'
            'Deferred to a later spec:\n'
            '- (anything spec.md lists as out of scope, or None)') % dict(id=sid, g=g, title=title, doc=doc, who=who, role=role, dec=dec)
def gate_steps(sid, g, commit=True):
    who = {'G1': 'the FEH product owner says', 'G2': 'the VISEO technical lead says', 'G3': 'FEH and VISEO both say'}[g]
    out = ('<p><b>Record the decision.</b> When %s "approved", paste this into Copilot Chat (Agent mode). '
           'Before you press Enter, replace the name in brackets with the name on the big screen. '
           'What a gate record is: <button class="link" data-goto="gates">Gate record</button>.</p>\n  %s\n'
           '  <p class="expect">✓ You should see: a new file <code>specs/%s/gates/%s.md</code> open in the editor. Read it; if Copilot shows <b>Keep</b>, click it.</p>\n') % (
        who, pre('Prompt · paste into Copilot Chat', gate_prompt_text(sid, g)), sid, g)
    if commit:
        out += '  %s\n' % pre('Terminal or PowerShell · save it in Git', 'git add -A\ngit commit -m "gate: %s approved %s"' % (g, sid))
    return out

def spec_slide(s, time, full, sources='<code>docs/feh-requirements.md</code> and <code>docs/voice-capture-sequence.mmd</code>'):
    draft = ('  <h3><span class="ph">1 · Draft</span> yourself first · %s</h3>\n'
             '  <p>%s Use the <button class="link" data-goto="spec101">spec template</button> and ask Copilot to review your draft. Don\'t run <code>/speckit-specify</code> yet.</p>\n') % (
        '15 min' if full else '5 min',
        'Write the whole block for this spec from %s, including what it builds on.' % sources if full else
        'Write only the Business Goal and the functional requirements (FR-001…) for this spec.')
    return '''
<section class="slide" id="s%(n)s" data-group="Day 1 · Spec" data-title="Spec %(n)s · %(short)s">
  <p class="eyebrow">Spec %(n)s · Day 1, %(t)s · draft, compare, specify, clarify, G1</p>
  <h2>%(n)s — %(name)s</h2>
  <p class="lead">%(goal)s</p>
  <p class="muted"><b>Builds on:</b> %(builds)s<br><b>If you stop here:</b> %(stop)s</p>
%(draft)s  <h3><span class="ph">2 · Compare</span> with the answer key, as a room</h3>
  <p>What did your draft have that ours doesn't? What did you miss? FEH confirms anything that is a business decision. The facilitator edits the agreed block on the big screen.</p>
  <details><summary>Answer key: VISEO's specify block for %(n)s</summary>
  %(spec)s
  </details>
  <h3><span class="ph">3 · Specify</span> run the room's agreed block</h3>
  <p>Copy the answer-key block above (with any changes the room agreed) into Copilot Chat. Everyone runs the same block, so everyone builds the same thing. When Copilot asks to run a script, click <b>Allow</b>.</p>
  <div class="note"><b>This step creates the spec's branch for you</b>You don't type any Git command here. <code>/speckit-specify</code> creates a new Git branch named <code>%(id)s</code> (a separate working copy of the project for this spec), switches to it, and writes <code>specs/%(id)s/spec.md</code>. Everything you do for this spec from now on, including the G1 commit below, is saved on that branch.</div>
  <p class="expect">✓ You should see: Copilot reports the branch <code>%(id)s</code> and the file <code>specs/%(id)s/spec.md</code>, and the bottom-left corner of VS Code shows <code>%(id)s</code>. To check in the terminal, run <code>git branch</code>: the line with <code>*</code> is the branch you're on.</p>
  <p class="muted"><b>If it fails:</b> the branch has a slightly different name: that's fine, use yours wherever the guide says <code>%(id)s</code>. No branch at all: tell the facilitator before you continue.</p>
  <h3><span class="ph">4 · Clarify</span> FEH answers</h3>
  %(clar)s
  <div class="note"><b>One answer for the whole room</b>When Copilot asks a business question, the FEH product owner answers it once, out loud. The facilitator types it on the big screen and everyone gives Copilot the same answer. Add your own edge cases to "Give particular attention to:" before you paste.</div>
  <h3><span class="ph gate">G1</span> FEH approves the spec</h3>
  %(gate)s
  %(catch)s
</section>''' % dict(n=s['n'], short=E(s['short']), t=time, name=E(s['name']), goal=E(' '.join(s['goal'].split())),
                     stop=E(s['stop']), builds=E(' '.join(s['builds'].split())), draft=draft, spec=pre('Prompt · paste into Copilot Chat', R2.specify_block(s), True),
                     clar=pre('Prompt · paste into Copilot Chat', R2.clarify_block(s)), id=s['id'],
                     catch=catch('specs/%s/spec.md' % s['id'], '<code>spec.md</code>'), gate=gate_steps(s['id'], 'G1'))

RUN_FULL = '''  <h3><span class="ph">Run it</span></h3>
  <pre data-label="Terminal 1 · the app">
uv sync
uv run python manage.py migrate
uv run python manage.py seed_demo
uv run python manage.py runserver</pre>
  <p>Open <code>http://localhost:8000</code> in Chrome.</p>
  <pre data-label="Terminal 2 · the tests">
uv run pytest
cd e2e
npm install
npx playwright test</pre>'''
RUN_SHORT = '''  <h3><span class="ph">Run it</span></h3>
  <pre data-label="Terminal">
uv run python manage.py migrate
uv run python manage.py seed_demo
uv run python manage.py runserver</pre>
  <p>Then <code>uv run pytest</code>, and <code>npx playwright test</code> in <code>e2e/</code>.</p>'''
AI_NOTE = ('  <div class="note"><b>No keys needed</b>This spec runs with <code>AI_PROVIDER=sample</code>: the app uses '
           '<code>docs/sample/</code> instead of Azure OpenAI, and every test uses the sample too (Principle XVI). '
           'Connect Azure later, on the <button class="link" data-goto="azure">Connect Azure OpenAI</button> slide.</div>\n')

def exec_slide(s, group, eyebrow, prev=None, with_specify=False, full_run=False, mock='mvp1/', ai=False):
    top = ''
    if with_specify:
        top = ('  <h3><span class="ph">1 · Specify</span></h3>\n  %s\n  <p class="expect">✓ You should see: <code>/speckit-specify</code> creates and switches to a new branch for this spec (its name is in the bottom-left corner of VS Code) and writes its <code>spec.md</code>. You don\'t type any Git command for this.</p>\n  <h3><span class="ph">2 · Clarify</span> FEH answers</h3>\n  %s\n'
               '  <h3><span class="ph gate">G1</span> FEH approves</h3>\n  %s') % (
            pre('Prompt · paste into Copilot Chat', R2.specify_block(s), True), pre('Prompt · paste into Copilot Chat', R2.clarify_block(s)), gate_steps(s['id'], 'G1'))
    switch = ''
    if prev:
        switch = ('  <h3><span class="ph">Switch</span> to spec %s</h3>\n'
                  '  <p>Spec Kit works on the spec whose branch you are on. The first line moves to this spec\'s branch; the second brings in everything built so far (the previous spec\'s branch).</p>\n'
                  '  %s\n'
                  '  <p>✓ You should see: "Switched to branch …", then "Fast-forward" or "Merge made". If the names differ, run <code>git branch</code> and use yours.</p>\n') % (
            s['n'], pre('Terminal or PowerShell', 'git checkout %s\ngit merge %s' % (s['id'], prev)))
    return '''
<section class="slide" id="x%(n)s" data-group="%(group)s" data-title="Execute %(n)s · %(short)s">
  <p class="eyebrow">%(eb)s</p>
  <h2>Execute %(n)s — %(name)s</h2>
  <p class="lead"><b>Builds on:</b> %(builds)s<br><b>If you stop here:</b> %(stop)s</p>
%(ai)s%(top)s  <div class="flow"><span>plan</span><span>tasks</span><span>analyze</span><span class="g">G2</span><span>implement</span><span>converge</span><span class="g">G3</span><span>commit</span></div>
%(switch)s  <h3><span class="ph">Plan</span></h3>
  %(plan)s
  <h3><span class="ph">Tasks</span></h3>
  %(tasks)s
  <h3><span class="ph">Analyze</span> before any code</h3>
  <pre data-label="Prompt">/speckit-analyze</pre>
  <h3><span class="ph gate">G2</span> VISEO approves plan and tasks</h3>
  <ul class="checks">
    <li>Every acceptance criterion maps to at least one test</li>
    <li>The plan follows the constitution's Technology Standards and <code>docs/reference.md</code></li>
    <li>Nothing is planned that no criterion asks for</li>
    <li><code>/speckit-analyze</code> reports no critical issues</li>
  </ul>
  %(g2)s  %(catch)s
  <h3><span class="ph">Implement</span> tests first</h3>
  %(impl)s
  <pre data-label="Prompt · then compare with the spec">/speckit-converge</pre>
%(run)s
  <h3><span class="ph gate">G3</span> FEH and VISEO accept</h3>
  <ul class="checks">
    <li>On screen: %(screen)s</li>
    <li>It matches the <a href="%(mock)s" target="_blank" rel="noopener">interactive mockup</a> for this spec's screens</li>
    <li>Every AC-%(n)s criterion has a passing test whose name contains its ID</li>
    <li>All earlier specs' tests still pass</li>
    <li><code>/speckit-converge</code> reports no gaps</li>
  </ul>
  %(g3)s  %(commit)s
</section>''' % dict(n=s['n'], group=group, short=E(s['short']), eb=eyebrow, name=E(s['name']), stop=E(s['stop']), builds=E(' '.join(s['builds'].split())),
                     ai=AI_NOTE if ai else '', top=top, switch=switch, mock=mock,
                     plan=pre('Prompt · paste into Copilot Chat', R2.plan_block(s), True),
                     tasks=pre('Prompt · paste into Copilot Chat', R2.tasks_block(s)),
                     impl=pre('Prompt · paste into Copilot Chat', R2.implement_block(s)),
                     run=RUN_FULL if full_run else RUN_SHORT, screen=E(' '.join(s['screen'].split())),
                     catch=catch('specs/%s/plan.md' % s['id'], '<code>plan.md</code>'),
                     commit=pre('Terminal · one spec, one commit', R2.commit_block(s)),
                     g2=gate_steps(s['id'], 'G2'), g3=gate_steps(s['id'], 'G3', commit=False))


# ---------------------------------------------------------------- 1. MVP 2 refresh
CONST = rd('starter/docs/constitution.md')
REF = rd('starter/docs/reference.md')
g2 = rd('guide.html')
g2 = embed(g2, 'File · docs/constitution.md', CONST)
g2 = embed(g2, 'File · docs/reference.md', REF)
g2 = set_order_table(g2, R2.SPECS)
g2 = g2.replace('<div><b>MVP 1b</b>Listen to the meeting and propose actions. Needs Azure AI: not in the workshop.</div>',
                '<div><b>MVP 1b</b>Listen to the meeting and propose actions. Built in the other track, <a href="guide-mvp1.html">MVP 1 · Voice capture</a>.</div>')
S2 = {s['n']: s for s in R2.SPECS}
T2 = {'001': ('1:50', True), '002': ('2:30', False), '003': ('2:50', True), '004': ('3:15', False), '005': ('3:30', False)}
i, _ = bounds(g2, 's001'); _, j = bounds(g2, 's005')
g2 = g2[:i] + '\n\n'.join(spec_slide(S2[n], *T2[n], sources='<code>docs/feh-requirements.md</code>').strip() for n in ['001', '002', '003', '004', '005']) + g2[j:]
wr('guide.html', g2)
d2 = rd('day2.html')
X2 = [exec_slide(S2['002'], 'Day 2 · Execute', 'Day 2 · 9:00 · execute (finish 001 first if needed: steps 7–10 of Create the app)', prev='001-sign-in-hotel-access', full_run=True, mock='mvp/'),
      exec_slide(S2['003'], 'Day 2 · Execute', 'Day 2 · 10:00 · execute', prev='002-weekly-meetings', mock='mvp/'),
      exec_slide(S2['004'], 'Day 2 · Execute', 'Day 2 · 11:30 · execute', prev='003-action-items', mock='mvp/'),
      exec_slide(S2['005'], 'Day 2 · Execute', 'Day 2 · 1:30 · execute · completes the MVP', prev='004-carry-forward', mock='mvp/'),
      exec_slide(S2['006'], 'Day 2 · Stretch', 'Day 2 · 2:30 · stretch, only after 005 is accepted', with_specify=True, mock='mvp/'),
      exec_slide(S2['007'], 'Day 2 · Stretch', 'Day 2 · stretch, after 006 or instead of it', with_specify=True, mock='mvp/')]
i, _ = bounds(d2, 'x002'); _, j = bounds(d2, 'x007')
d2 = d2[:i] + '\n\n'.join(x.strip() for x in X2) + d2[j:]
wr('day2.html', d2)

# ---------------------------------------------------------------- 2. MVP 1 guide
S1 = {s['n']: s for s in R1.SPECS}
g = g2
g = rep(g, "var KEY = 'feh-sdd-guide-v1';", "var KEY = 'feh-sdd-guide-mvp1';")
g = rep(g, "fetch('day2.html', { cache: 'no-store' })", "fetch('day2-mvp1.html', { cache: 'no-store' })")
g = rep(g, '<title>SDD Workshop Guide · MVP 2 Meeting action tracker — FEH × VISEO</title>', '<title>SDD Workshop Guide · MVP 1 Voice capture — FEH × VISEO</title>')
g = rep(g, '<small>FEH × VISEO workshop · MVP 2</small>', '<small>FEH × VISEO workshop · MVP 1</small>')
g = g.replace('href="mvp/"', 'href="mvp1/"')
g = g.replace('href="guide-mvp1.html">MVP 1 · Voice capture</a>.</div>', 'href="mvp1/">the interactive mockup</a>.</div>')
i = g.index('<div class="note" id="track-note">'); j = g.index('</div>', i) + 6
g = g[:i] + ('<div class="note" id="track-note"><b>Two tracks, one method</b>You are in <b>MVP 1 · Voice capture</b>: record the meeting, '
             'AI proposes the action items, the chair confirms them. The room may instead build <a href="guide.html">MVP 2 · Meeting action tracker</a>. '
             'Same constitution, same Day 1 teaching; only the specs differ.</div>') + g[j:]

# Step 1: the MVP 1 docs pack
g = g.replace('starter/feh-sdd-docs.zip', 'starter/feh-sdd-docs-mvp1.zip')
rep_pairs = [
    ("├── mockup/              ← our MVP mockups: mvp-app.html (the whole MVP, interactive) and mvp-1 to mvp-5;\n        │                          FEH's original screens 01 and 03",
     "├── mockup/              ← mvp-app.html: the whole MVP 1 as an interactive mockup;\n        │                          FEH's original screens 01 and 03\n        ├── voice-capture-sequence.mmd ← FEH's happy-path sequence: what MVP 1 builds\n        ├── sample/              ← the sample transcript and items the app uses without Azure keys"),
    ("        ├── specs.md             ← answer key for the specs: the run sheet\n        └── backup/              ← the backup idea, only if the room switches",
     "        └── specs.md             ← answer key for the specs: the MVP 1 run sheet"),
    ("our MVP mockups in <code>mockup/</code> (<code>mvp-app.html</code> is the whole MVP as an interactive mockup), FEH's requirements (<code>feh-requirements.md</code>) with FEH's original screens in <code>mockup/</code>, and <code>backup/</code>.",
     "the MVP 1 mockup in <code>mockup/</code> (<code>mvp-app.html</code> is the whole MVP 1 as an interactive mockup), FEH's requirements (<code>feh-requirements.md</code>) with FEH's original screens in <code>mockup/</code>, FEH's voice-capture sequence (<code>voice-capture-sequence.mmd</code>) and the sample AI data in <code>sample/</code>."),
    ("<code>ls docs</code> lists <code>backup</code>, <code>constitution.md</code>, <code>feh-requirements.md</code>, <code>mockup</code>, <code>reference.md</code> and <code>specs.md</code>.",
     "<code>ls docs</code> lists <code>constitution.md</code>, <code>feh-requirements.md</code>, <code>mockup</code>, <code>reference.md</code>, <code>sample</code>, <code>specs.md</code> and <code>voice-capture-sequence.mmd</code>."),
]
for a, b in rep_pairs:
    g = rep(g, a, b)
g = re.sub(r"and <code>mockup</code> has our <code>mvp-app\.html</code> and <code>mvp-\*</code> mockups plus FEH's screens 01 and 03",
           "and <code>mockup</code> has <code>mvp-app.html</code> plus FEH's screens 01 and 03, and <code>sample</code> has the sample transcript", g)

# Agenda
fl = get(g, 'flow')
for a, b in [
    ('<td>Finish 001 · execute 002</td>', '<td>Finish 001 · execute 002 · meetings</td>'),
    ('<tr><td>10:00</td><td></td><td>Execute 003 · action items</td></tr>', '<tr><td>9:45</td><td></td><td>Execute 003 · action items</td></tr>'),
    ('<tr><td>10:30</td><td>How we build a constitution</td><td></td></tr>', '<tr><td>10:30</td><td>How we build a constitution</td><td>Execute 004 · record and transcribe</td></tr>'),
    ('<tr><td>11:30</td><td></td><td>Execute 004 · carry forward</td></tr>', '<tr><td>11:30</td><td></td><td>Execute 005 · extract proposed items</td></tr>'),
    ('<tr><td>1:30</td><td></td><td>Execute 005 · overdue and counts · <b>MVP complete</b></td></tr>', '<tr><td>1:30</td><td></td><td>Execute 006 · review and confirm · <b>MVP complete</b></td></tr>'),
    ('<td>Specs 001–005: draft, compare, specify, clarify with FEH</td>', '<td>Specs 001–006: draft, compare, specify, clarify with FEH</td>'),
    ('<tr><td>2:30</td><td></td><td>Stretch: 006, 007</td></tr>', '<tr><td>2:30</td><td></td><td>Connect Azure OpenAI (if FEH provides it) · stretch 007</td></tr>'),
    ('<b>G1: FEH approves 001–005</b>', '<b>G1: FEH approves 001–006</b>')]:
    fl = rep(fl, a, b)
g = replace(g, 'flow', fl)

# Outcomes
oc = get(g, 'outcomes')
for a, b in [
    ("Approved specifications for a small MVP of FEH's Meeting Action Tracker, and that MVP working, built from those specs.",
     "Approved specifications for MVP 1 of FEH's Meeting Action Tracker, voice capture, and that MVP working, built from those specs."),
    ("<li>A constitution and specs 001–005 written by the participants from FEH's requirements, agreed with FEH and approved at G1</li>",
     "<li>A constitution and specs 001–006 written by the participants from FEH's requirements and voice-capture sequence, agreed with FEH and approved at G1</li>"),
    ("<li>The MVP running locally: sign-in, weekly meetings, action items, carry-forward and overdue flags</li>",
     "<li>The MVP running locally: sign-in, weekly meetings, action items, record and transcribe, AI-proposed items, and the chair's review and confirm</li>"),
    ("<li>Spreadsheet-style editing and comments, if time allows</li>",
     "<li>Live with Azure OpenAI if FEH provides access; otherwise on the sample transcript. Carry forward and overdue if time allows</li>"),
    ("where the parts we stubbed (Entra ID sign-in, emails, Azure) are specified next.",
     "where the parts we stubbed (Entra ID sign-in, Teams transcripts, emails, Azure hosting) are specified next.")]:
    oc = rep(oc, a, b)
g = replace(g, 'outcomes', oc)

# FEH's brief
idea = get(g, 'idea')
idea = rep(idea, "Each week, team leaders at every hotel review performance and agree actions. Today those actions live in a spreadsheet, results are never recorded, and open items get lost between weeks. FEH's requirements describe the full Meeting Action Tracker; two days can't cover all of it, so we propose an MVP that can realistically be finished in the session.",
           "Each week, team leaders at every hotel review performance and agree actions, and someone types them into a spreadsheet afterwards. FEH's MVP 1b asks for the tracker to listen instead: record the meeting, turn it into text, and propose the action items for the chair to confirm. FEH has given us the happy path as a sequence diagram. MVP 1 builds exactly that, on top of the meetings and action list it needs.")
idea = rep(idea, "shows the whole workshop MVP working: sign in, meetings, the meeting screen with carry-forward and overdue, add and edit actions.",
           "shows the whole of MVP 1 working: sign in, meetings, add actions, Record, the transcript, the proposed items and the chair's review.")
idea = rep(idea, '<div><b>MVP 1a</b>Data entry and tracking. <em>Our MVP is the core of this.</em></div>',
           '<div><b>MVP 1a</b>Data entry and tracking. <em>We build the part voice capture needs: meetings and the action list.</em></div>')
idea = rep(idea, '<div><b>MVP 1b</b>Listen to the meeting and propose actions. Built in the other track, <a href="mvp1/">the interactive mockup</a>.</div>',
           '<div><b>MVP 1b</b>Listen to the meeting and propose actions. <em>This is MVP 1: FEH\'s happy path, with Azure OpenAI or the sample data.</em></div>')
seq = '''  <h3><span class="ph">FEH's happy path</span> <code>docs/voice-capture-sequence.mmd</code></h3>
  <ol>
    <li>The chair presses <b>Record</b>; the browser captures the microphone while the team discusses an issue and agrees an action.</li>
    <li>The chair presses <b>Stop</b>; the audio goes to the Django app.</li>
    <li>The app sends the audio to the transcription service and gets the <b>transcript</b> back.</li>
    <li>The app sends the transcript and the action-item fields to the language model and gets <b>structured action items</b> back: segment, issue, action, owner, due date, anticipated result.</li>
    <li>The app saves them as <b>Proposed</b> and shows the to-do table.</li>
    <li>The chair <b>reviews and accepts</b>; the items become <b>Confirmed</b> actions of the meeting.</li>
  </ol>
'''
fig1 = """<!--seq-->
  <h3><span class="ph">How it works</span> FEH's happy path, spec by spec</h3>
  <p>FEH's sequence (<code>docs/voice-capture-sequence.mmd</code>) with the meetings and action list it needs, each numbered step belonging to one spec. Source for Copilot: <code>docs/mvp-sequence.mmd</code> in your project.</p>
  <a href="img/sequence-mvp1.svg" target="_blank" rel="noopener"><img src="img/sequence-mvp1.svg" alt="Sequence diagram of MVP 1: sign in and open the meeting, record and transcribe, extract proposed items, review and confirm" loading="lazy" style="display:block;width:100%;max-width:980px;border-radius:12px;border:1px solid var(--line)"></a>
  <!--/seq-->"""
idea = re.sub(r'<!--seq-->.*?<!--/seq-->', lambda m: fig1, idea, flags=re.S)
idea = rep(idea, "Read docs/feh-requirements.md and docs/constitution.md. Propose an MVP\nthat a developer can build with GitHub Copilot in about one and a half\ndays.",
           "Read docs/voice-capture-sequence.mmd, docs/feh-requirements.md and\ndocs/constitution.md. Propose an MVP of FEH's voice-capture happy path\nthat a developer can build with GitHub Copilot in about one and a half\ndays, including the meetings and action list it needs.")
idea = rep(idea, '<p style="margin-top:10px"><b>Minimum viable demonstration: through 005.</b></p>', '<p style="margin-top:10px"><b>Minimum viable demonstration: through 006</b> (speak, review, confirm).</p>')
idea = rep(idea, '<tr><td>Teams transcripts, microphone and AI extraction (Final, MVP 1b)</td><td>Left out: IT approval and Azure AI services. Only GitHub Copilot is used, for building.</td></tr>',
           '<tr><td>Transcription and extraction (MVP 1b)</td><td>Built, behind two adapters: Azure OpenAI when FEH provides an endpoint and key, otherwise the sample transcript and items. GitHub Copilot is only used for building.</td></tr>\n    <tr><td>Teams transcripts (Final)</td><td>Left out: needs IT approval. The browser microphone is the source, as in FEH\'s sequence.</td></tr>')
idea = rep(idea, '<tr><td>Results, targets, change-history screen, My actions, reminders, export, Databricks, Azure</td><td>Backlog for after the workshop.</td></tr>',
           '<tr><td>Carry forward and overdue (MVP 1a)</td><td>Stretch spec 007.</td></tr>\n    <tr><td>Actual results, targets, change-history screen, My actions, reminders, export, Databricks, Azure hosting</td><td>Backlog for after the workshop.</td></tr>')
idea = re.sub(r'\s*<div class="note"><b>Backup</b>.*?</div>', '', idea, flags=re.S)
g = replace(g, 'idea', idea)
g = set_order_table(g, R1.SPECS)

# Spec slides: 001-006
TIMES = {'001': ('1:50', True), '002': ('2:20', False), '003': ('2:35', False), '004': ('2:55', True), '005': ('3:15', False), '006': ('3:30', False)}
i, _ = bounds(g, 's001')
_, j = bounds(g, 's005')
g = g[:i] + '\n\n'.join(spec_slide(S1[n], *TIMES[n]).strip() for n in ['001', '002', '003', '004', '005', '006']) + g[j:]

# Create the app (execute 001): MVP 1 has six specs on Day 1
g = rep(g, 'The constitution is adopted and specs 001–005 are approved at G1 and committed.', 'The constitution is adopted and specs 001–006 are approved at G1 and committed.')
g = rep(g, '<code>001-sign-in-hotel-access</code> … <code>005-overdue-and-counts</code>', '<code>001-sign-in-hotel-access</code> … <code>006-review-and-confirm</code>')
g = rep(g, 'git merge 005-overdue-and-counts', 'git merge 006-review-and-confirm')
g = g.replace('the <b>005</b> branch has all five specs', 'the <b>006</b> branch has all six specs')
g = g.replace('brings all five approved specs onto it', 'brings all six approved specs onto it')
g = g.replace('<code>ls specs</code> shows all five spec folders', '<code>ls specs</code> shows all six spec folders')

# Quality checks
g = rep(g, '''/speckit-checklist Check specs 001 to 005 for hotel isolation, required
fields, the carry-forward and overdue rules, and the constitution's
"Nothing Disappears" principle. Focus on gaps a hotel team leader would
notice.''', '''/speckit-checklist Check specs 001 to 006 for hotel isolation, required
fields, what happens when recording, transcription or extraction fails,
and the constitution's "AI Proposes, a Person Confirms" and "Secrets
Stay Out of the Code" principles. Focus on gaps a meeting chair would
notice.''')
g = rep(g, '<li>Specs 001–005 are approved at G1, with gate records committed</li>', '<li>Specs 001–006 are approved at G1, with gate records committed</li>')
g = g.replace('Day 2 continues the run sheet: finish 001, then 002 to 005.', 'Day 2 continues the run sheet: finish 001, then 002 to 006.')

# Backup idea slides are MVP 2's fallback only
for sid in ['bref', 'b001', 'b002', 'b003']:
    if '<section class="slide" id="%s"' % sid in g:
        g = remove(g, sid)
g = g.replace('<!-- ======================= BACKUP IDEA ======================= -->', '')
wr('guide-mvp1.html', g)

# ---------------------------------------------------------------- 3. MVP 1 Day 2
d = d2
d = d.replace('href="mvp/"', 'href="mvp1/"').replace('guide.html#x002', 'guide-mvp1.html#x002')
AZURE = '''
<section class="slide" id="azure" data-group="Day 2 · Execute" data-title="Connect Azure OpenAI">
  <p class="eyebrow">Day 2 · when FEH provides the values · 15 minutes</p>
  <h2>Connect Azure OpenAI</h2>
  <p class="lead">Until now the app has used the sample transcript and items. If FEH has provided an Azure OpenAI endpoint, switching to it is configuration only: no spec, plan or code changes (Principle XVI).</p>
  <h3><span class="ph">1</span> What FEH provides</h3>
  <ul class="checks">
    <li>An Azure OpenAI endpoint and key</li>
    <li>A transcription deployment (Whisper or gpt-4o-transcribe) and a chat deployment (e.g. GPT-4o)</li>
    <li>Confirmation that the endpoint is reachable from the venue network</li>
  </ul>
  <h3><span class="ph">2</span> Create <code>.env</code> in the project root</h3>
  <p>In VS Code: File → New File, save it as <code>.env</code> next to <code>manage.py</code>. The facilitator shares the values privately, never in the group chat.</p>
  <pre data-label="File · .env (never commit it)">
AI_PROVIDER=azure
AZURE_OPENAI_ENDPOINT=https://&lt;feh-resource&gt;.openai.azure.com
AZURE_OPENAI_KEY=&lt;key&gt;
AZURE_OPENAI_TRANSCRIBE_DEPLOYMENT=&lt;transcription deployment name&gt;
AZURE_OPENAI_CHAT_DEPLOYMENT=&lt;chat deployment name&gt;</pre>
  <h3><span class="ph">3</span> Check it's safe before you run it</h3>
  <pre data-label="Prompt · paste into Copilot Chat">
Do not print, repeat or log any key. Check that .env is listed in
.gitignore, that git status does not show .env, that the app reads the
AZURE_OPENAI_* values only from the environment, and that no key appears
in any tracked file. Report only yes or no for each check.</pre>
  <h3><span class="ph">4</span> Restart and try it</h3>
  <p>Stop the server (Ctrl + C), run <code>uv run python manage.py runserver</code> again, open today's meeting, press <b>Record</b>, and say: <em>"Alex, please review the December corporate pipeline with sales by the twenty-third."</em></p>
  <p class="expect">✓ You should see: your own words in the transcript, then a proposed item for Alex Wong due 23 Oct.</p>
  <p class="muted"><b>If it fails:</b> the Terminal 1 error names the problem. 401: wrong key. 404: wrong endpoint or deployment name. A timeout: the network blocks Azure. Set <code>AI_PROVIDER=sample</code> and restart to carry on.</p>
  <div class="note"><b>The tests don't change</b>The tests always use the sample (Principle XVI), so <code>uv run pytest</code> passes with or without Azure. Real AI is checked by people, at the Review page: that's Principle XV.</div>
</section>'''
X = [exec_slide(S1['002'], 'Day 2 · Execute', 'Day 2 · 9:00 · execute (finish 001 first if needed: steps 7–10 of Create the app)', prev='001-sign-in-hotel-access', full_run=True),
     exec_slide(S1['003'], 'Day 2 · Execute', 'Day 2 · 9:45 · execute', prev='002-weekly-meetings'),
     exec_slide(S1['004'], 'Day 2 · Execute', 'Day 2 · 10:30 · execute', prev='003-action-items', ai=True),
     exec_slide(S1['005'], 'Day 2 · Execute', 'Day 2 · 11:30 · execute', prev='004-record-and-transcribe', ai=True),
     exec_slide(S1['006'], 'Day 2 · Execute', 'Day 2 · 1:30 · execute · completes the MVP', prev='005-extract-proposed-items'),
     AZURE,
     exec_slide(S1['007'], 'Day 2 · Stretch', 'Day 2 · stretch, only after 006 is accepted', with_specify=True)]
i, _ = bounds(d, 'x002')
_, j = bounds(d, 'x007')
d = d[:i] + '\n\n'.join(x.strip() for x in X) + d[j:]
d = re.sub(r'<nav class="jump" aria-label="Day 2 sections">.*?</nav>',
           '<nav class="jump" aria-label="Day 2 sections"><a href="mvp1/" target="_blank" rel="noopener">MVP 1 mockup</a><a href="#x002">002</a><a href="#x003">003</a><a href="#x004">004</a><a href="#x005">005</a><a href="#x006">006</a><a href="#azure">Azure</a><a href="#x007">007 stretch</a><a href="#change">Change</a><a href="#demo">Demo</a><a href="#gotchas">Gotchas</a><a href="guide-mvp1.html">Full guide</a></nav>', d, flags=re.S)
d = d.replace('<title>', '<title>MVP 1 · ', 1)
DEMO = '''
<section class="slide" id="demo" data-group="Day 2 · Build" data-title="Final demo">
  <p class="eyebrow">Day 2 · 3:45</p>
  <h2>Final demo: trace it back</h2>
  <p class="lead">Each participant has 5 minutes. FEH asks the questions.</p>
  <h3><span class="ph">1</span> Show it running</h3>
  <p>Open the <a href="mvp1/" target="_blank" rel="noopener">interactive mockup</a> next to your app: the mockup was the target, your app is the production MVP built from the specs. Then run a short "weekly meeting": sign in as Mary Tan, create today's meeting, press <b>Record</b>, talk through an issue (or use the sample), and stop. Show the transcript and the proposed items, correct one, and confirm. The actions appear in the meeting, marked "From recording".</p>
  <h3><span class="ph">2</span> Show the chair stays in control</h3>
  <p>Before confirming, show that nothing was added to the meeting: that is Principle XV, and the test whose name contains its acceptance criterion proves it.</p>
  <h3><span class="ph">3</span> FEH picks any screen</h3>
  <p>The participant names the acceptance criterion behind it, opens it in <code>spec.md</code>, and shows the test whose name contains that ID.</p>
  <h3><span class="ph">4</span> Show a decision</h3>
  <p>Open a <code>G1.md</code> and read one business decision FEH made during clarify, for example what happens to a field the transcript doesn't give. That decision is now in the code and covered by a test.</p>
  <h3><span class="ph">5</span> Show isolation</h3>
  <p>Sign in as Grace Teo (Hotel B) and paste the address of a Hotel A meeting's review page. It doesn't exist for her.</p>
  <h3><span class="ph">6</span> Ask the agent</h3>
  <pre data-label="Prompt · paste into Copilot Chat">
List every acceptance criterion in specs/, and for each one the test
that proves it and whether that test currently passes. Show the result
as a table. Do not change anything.</pre>
</section>'''
d = replace(d, 'demo', DEMO)
gt = get(d, 'gotchas')
gt = re.sub(r'\s*<tr><td><b>A grid cell doesn\'t save</b>.*?</tr>', '', gt, flags=re.S)
gt = re.sub(r'\s*<tr><td><b>Overdue counts look wrong</b>.*?</tr>', '', gt, flags=re.S)
gt = rep(gt, '    <tr><td><b>Spec Kit commands vanish or change</b>', '''    <tr><td><b>The browser won't record</b></td><td>Allow the microphone when Chrome asks (or in the site settings by the address bar). Recording only works on <code>http://localhost</code> or https, so open the app as <code>localhost:8000</code>, not by IP address.</td></tr>
    <tr><td><b>"Transcribing…" never finishes</b></td><td>Look at Terminal 1. With <code>AI_PROVIDER=azure</code>, a wrong value or a blocked network shows there. Set <code>AI_PROVIDER=sample</code> and restart to carry on.</td></tr>
    <tr><td><b>A proposed item has empty fields</b></td><td>That's the spec working: values not in the fixed lists, or owners not in the hotel, are left empty for the chair. The item can't be confirmed until it's edited.</td></tr>
    <tr><td><b>A key appears in code, a commit or the chat</b></td><td>Stop. Remove it, tell the facilitator so FEH can rotate the key, and keep it only in <code>.env</code> (Principle XVI).</td></tr>
    <tr><td><b>Spec Kit commands vanish or change</b>''')
d = replace(d, 'gotchas', gt)
if '<section class="slide" id="bbuild"' in d:
    d = remove(d, 'bbuild')
wr('day2-mvp1.html', d)
print('guide.html refreshed; wrote guide-mvp1.html and day2-mvp1.html')
