#!/usr/bin/env python3
"""
MedicalNet — Static site validator.
Checks every generated page for:
  1. balanced HTML tags (HTMLParser, SVG-aware void set)
  2. unique ids per page
  3. internal links: target file exists AND fragment resolves
     (also covers pure-fragment hrefs like href="#f-sos")

Usage:  python3 tools/validate_pages.py   (exit 1 on any problem)
"""
import pathlib
import re
import sys
import urllib.parse
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ['index.html', 'console.html', 'hospital.html', 'technicians.html',
         'marketplace.html', 'students.html', 'odr.html', 'academy.html']

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
        'meta', 'source', 'track', 'wbr',
        # SVG self-closing elements
        'use', 'path', 'circle', 'rect', 'line', 'polyline', 'polygon',
        'ellipse', 'stop'}


class BalanceChecker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errs = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.errs.append('unclosed <%s>' % self.stack.pop())
            self.stack.pop()
        else:
            self.errs.append('stray </%s>' % tag)


def page_ids(html):
    return re.findall(r'\bid="([^"]+)"', html)


def check_page(fname):
    html = (ROOT / fname).read_text(encoding='utf-8')
    problems = []

    v = BalanceChecker()
    v.feed(html)
    problems += v.errs
    if v.stack:
        problems.append('unclosed-at-eof: %s' % v.stack)

    ids = page_ids(html)
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        problems.append('duplicate ids: %s' % dupes)

    for m in re.finditer(r'(?:href|src)="([^"]+)"', html):
        target = m.group(1)
        if target.startswith(('http://', 'https://', 'mailto:', 'tel:', 'data:')):
            continue
        path, _, frag = target.partition('#')
        if path:
            clean = urllib.parse.unquote(path)
            if not ((ROOT / clean).exists() or (ROOT / clean / 'index.html').exists()):
                problems.append('missing file: %s' % target)
        if frag:
            if path and path != fname:
                other_ids = page_ids((ROOT / urllib.parse.unquote(path)).read_text(encoding='utf-8'))
            else:
                other_ids = ids
            if frag not in other_ids:
                problems.append('missing anchor: %s' % target)
    return len(ids), problems


def main():
    ok = True
    for fname in PAGES:
        n_ids, problems = check_page(fname)
        status = 'OK  ' if not problems else 'FAIL'
        print('%s %-18s ids=%3d %s' % (status, fname, n_ids, problems or ''))
        ok = ok and not problems
    print('\nALL PAGES VALID' if ok else '\nPROBLEMS FOUND')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
