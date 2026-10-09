#!/bin/sh
# adpreview-bookmarklet.js -> adpreview-bookmarklet.html (설치 페이지) 생성
cd "$(dirname "$0")"
python3 - <<'PY'
import re, urllib.parse, html
src = open('adpreview-bookmarklet.js', encoding='utf-8').read()
lines = [l.strip() for l in src.splitlines() if l.strip() and not l.strip().startswith('//')]
code = ' '.join(lines)
url = 'javascript:' + urllib.parse.quote(code, safe="(){}[];,.'=+-*/!?:<>|&$_^~@ ")
tpl = open('adpreview-bookmarklet.template.html', encoding='utf-8').read()
open('adpreview-bookmarklet.html', 'w', encoding='utf-8').write(tpl.replace('%%HREF%%', html.escape(url, quote=True)))
print('built', len(url), 'chars')
PY
