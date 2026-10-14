#!/usr/bin/env python3
"""Stamp every page with a new build id so browsers fetch the newest version.
Run before each commit:  python3 tools/stamp.py"""
import re, time, pathlib
BUILD = time.strftime('%Y%m%d%H%M%S')
SNIP = '''<meta name="build" content="%s">
<meta http-equiv="Cache-Control" content="no-cache">
<script>/* always show the newest version: if the server has a newer build than this cached copy, load it once */
(function(){try{var me=document.querySelector('meta[name=build]').content,u=new URL(location.href);
if(u.searchParams.get('r')){u.searchParams.delete('r');history.replaceState(null,'',u.pathname+u.search+u.hash);return;}
fetch(location.pathname+'?_='+Date.now(),{cache:'no-store'}).then(function(r){return r.text();}).then(function(t){
var m=t.match(/<meta name="build" content="(\\d+)"/);if(m&&m[1]!==me){u.searchParams.set('r',m[1]);location.replace(u.toString());}}).catch(function(){});}catch(e){}})();
</script>
<!--/build-->'''
for f in ['index.html', 'guide.html', 'day2.html', 'guide-mvp1.html', 'day2-mvp1.html', 'setup.html', 'badge.html', 'certificate.html']:
    p = pathlib.Path(f)
    if not p.exists(): continue
    s = p.read_text()
    s = re.sub(r'<meta name="build".*?<!--/build-->\n?', '', s, flags=re.S)
    s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n' + SNIP % BUILD, 1)
    p.write_text(s)
    print('stamped', f, BUILD)
