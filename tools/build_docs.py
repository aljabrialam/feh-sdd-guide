"""Build starter/feh-sdd-docs.zip (the docs pack participants download in Step 1) from starter/docs/."""
import os, zipfile
root = os.path.join(os.path.dirname(__file__), '..', 'starter')
src = os.path.join(root, 'docs')
out = os.path.join(root, 'feh-sdd-docs.zip')
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for d, _, files in sorted(os.walk(src)):
        for f in sorted(files):
            p = os.path.join(d, f)
            z.write(p, os.path.relpath(p, root))
print('\n'.join(zipfile.ZipFile(out).namelist()))
