"""Build the docs packs participants download in Step 1.
MVP 2 (meeting action tracker): starter/docs/            -> starter/feh-sdd-docs.zip
MVP 1 (voice capture):          shared files from starter/docs/ + starter/mvp1/docs/
                                                           -> starter/feh-sdd-docs-mvp1.zip
Run:  python3 tools/build_docs.py"""
import os, zipfile
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(here, '..', 'starter')

def add_tree(z, src, arc_root, skip=()):
    for d, _, files in sorted(os.walk(src)):
        for f in sorted(files):
            p = os.path.join(d, f)
            rel = os.path.relpath(p, src)
            if any(rel == s or rel.startswith(s + os.sep) for s in skip):
                continue
            z.write(p, os.path.join(arc_root, rel))

# MVP 2: the whole shared docs folder
out2 = os.path.join(root, 'feh-sdd-docs.zip')
with zipfile.ZipFile(out2, 'w', zipfile.ZIP_DEFLATED) as z:
    add_tree(z, os.path.join(root, 'docs'), 'docs')

# MVP 1: shared constitution, reference, FEH requirements and FEH screens, plus the MVP 1 files
shared = os.path.join(root, 'docs')
out1 = os.path.join(root, 'feh-sdd-docs-mvp1.zip')
with zipfile.ZipFile(out1, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in ['constitution.md', 'reference.md', 'feh-requirements.md', 'deployment-spec.md',
              'mockup/01-meeting-screen.png', 'mockup/03-item-detail.png']:
        z.write(os.path.join(shared, f), 'docs/' + f)
    add_tree(z, os.path.join(root, 'mvp1', 'docs'), 'docs')
for o in (out2, out1):
    print(os.path.basename(o), len(zipfile.ZipFile(o).namelist()), 'files')
