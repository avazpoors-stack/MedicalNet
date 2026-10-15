"""
Senior QA, Accessibility, and Verification Auditor Script for MedicalNet
"""
import os
import re
import sys
import json
from html.parser import HTMLParser

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_audit():
    print(f"Starting MedicalNet QA & Verification Audit on: {ROOT}")
    results = {}

    index_html_path = os.path.join(ROOT, "index.html")
    with open(index_html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 1. FILE INTEGRITY & STRUCTURE
    print("\n--- 1. File Integrity & Structure ---")
    files_to_check = [
        "index.html",
        "assets/css/style.css",
        "assets/css/rtl-override.css",
        "assets/css/medicalnet-components.css",
        "assets/js/main.js"
    ]
    file_existence = {}
    for f in files_to_check:
        full_path = os.path.join(ROOT, f)
        exists = os.path.isfile(full_path)
        size = os.path.getsize(full_path) if exists else 0
        file_existence[f] = {"exists": exists, "size_bytes": size}
        print(f"[{'PASS' if exists else 'FAIL'}] {f} ({size:,} bytes)")
    results["core_files"] = file_existence

    # Verify CSS & JS linked in index.html
    css_links = re.findall(r'<link[^>]+rel=[\'"]stylesheet[\'"][^>]+href=[\'"]([^\'"]+)[\'"]', html_content, re.IGNORECASE)
    css_links += re.findall(r'<link[^>]+href=[\'"]([^\'"]+)[\'"][^>]+rel=[\'"]stylesheet[\'"]', html_content, re.IGNORECASE)
    js_scripts = re.findall(r'<script[^>]+src=[\'"]([^\'"]+)[\'"]', html_content, re.IGNORECASE)

    print(f"Found CSS links in index.html: {css_links}")
    print(f"Found JS scripts in index.html: {js_scripts}")

    expected_css = [
        "assets/css/style.css",
        "assets/css/rtl-override.css",
        "assets/css/medicalnet-components.css"
    ]
    missing_css_links = [c for c in expected_css if c not in css_links]
    print(f"Missing CSS links in index.html: {missing_css_links}")
    results["css_links"] = {"found": css_links, "missing": missing_css_links}

    # Verify SVG symbols referenced by <use href="#...">
    use_hrefs = re.findall(r'<use[^>]+href=[\'"]#([a-zA-Z0-9_-]+)[\'"]', html_content)
    symbols = set(re.findall(r'<symbol[^>]+id=[\'"]([a-zA-Z0-9_-]+)[\'"]', html_content))
    missing_symbols = sorted(list(set(use_hrefs) - symbols))
    print(f"Total <use href='#...'> occurrences: {len(use_hrefs)}, Unique: {len(set(use_hrefs))}")
    print(f"Total symbols defined in sprite: {len(symbols)}")
    print(f"Missing symbols: {missing_symbols}")
    results["svg_symbols"] = {
        "total_uses": len(use_hrefs),
        "unique_uses": len(set(use_hrefs)),
        "defined_symbols": len(symbols),
        "missing_symbols": missing_symbols
    }

    # Verify anchor navigation links match existing IDs
    anchor_hrefs = re.findall(r'<a[^>]+href=[\'"]#([a-zA-Z0-9_-]+)[\'"]', html_content)
    all_ids = set(re.findall(r'\bid=[\'"]([a-zA-Z0-9_-]+)[\'"]', html_content))
    missing_anchor_ids = sorted(list(set(anchor_hrefs) - all_ids))
    print(f"Total anchor href='#...': {len(anchor_hrefs)}, Unique: {len(set(anchor_hrefs))}")
    print(f"Total element IDs: {len(all_ids)}")
    print(f"Missing anchor IDs: {missing_anchor_ids}")
    results["anchors"] = {
        "total_anchors": len(anchor_hrefs),
        "unique_anchors": len(set(anchor_hrefs)),
        "defined_ids": len(all_ids),
        "missing_targets": missing_anchor_ids
    }

    # Verify all local asset references (images, fonts, scripts, links)
    all_refs = re.findall(r'(?:src|href)=[\'"]([^\'":#?]+)[\'"]', html_content)
    # Filter out empty, javascript:, mailto:, data:, https:, http:
    local_refs = set()
    for r in all_refs:
        if r.startswith("http:") or r.startswith("https:") or r.startswith("mailto:") or r.startswith("data:") or r.startswith("javascript:") or r.startswith("#"):
            continue
        local_refs.add(r)

    # Also check url(...) in all CSS files
    for css_file in ["assets/css/style.css", "assets/css/rtl-override.css", "assets/css/medicalnet-components.css"]:
        cpath = os.path.join(ROOT, css_file)
        if os.path.exists(cpath):
            with open(cpath, "r", encoding="utf-8") as cf:
                ctext = cf.read()
                css_urls = re.findall(r'url\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)', ctext)
                for u in css_urls:
                    if u.startswith("http:") or u.startswith("https:") or u.startswith("data:") or u.startswith("#"):
                        continue
                    # resolve relative to css directory
                    resolved = os.path.normpath(os.path.join(os.path.dirname(css_file), u)).replace("\\", "/")
                    local_refs.add(resolved)

    missing_local_files = []
    for ref in sorted(list(local_refs)):
        ref_path = os.path.join(ROOT, ref)
        if not os.path.exists(ref_path):
            missing_local_files.append(ref)

    print(f"Total local references checked: {len(local_refs)}")
    print(f"Missing local files: {missing_local_files}")
    results["local_references"] = {
        "total": len(local_refs),
        "missing": missing_local_files
    }

    # 2. SYNTAX AND CODE QUALITY
    print("\n--- 2. Syntax & Code Quality ---")
    # Check for unclosed tags or malformed HTML using standard HTMLParser
    class TagChecker(HTMLParser):
        def __init__(self):
            super().__init__()
            self.tag_stack = []
            self.errors = []
            self.void_tags = {
                'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
                'link', 'meta', 'param', 'source', 'track', 'wbr'
            }

        def handle_starttag(self, tag, attrs):
            if tag.lower() not in self.void_tags:
                self.tag_stack.append((tag.lower(), self.getpos()))

        def handle_endtag(self, tag):
            tag = tag.lower()
            if tag in self.void_tags:
                return
            if not self.tag_stack:
                self.errors.append(f"Unexpected closing tag </{tag}> at line {self.getpos()[0]}")
                return
            last_tag, pos = self.tag_stack.pop()
            if last_tag != tag:
                self.errors.append(f"Mismatched closing tag: expected </{last_tag}> (from line {pos[0]}), got </{tag}> at line {self.getpos()[0]}")

    checker = TagChecker()
    try:
        checker.feed(html_content)
        unclosed = [(t, p) for t, p in checker.tag_stack]
        print(f"HTML Parser validation: {len(checker.errors)} mismatch errors, {len(unclosed)} unclosed tags")
        if checker.errors[:10]:
            print("First 10 HTML parser errors:", checker.errors[:10])
        if unclosed:
            print("Unclosed tags:", unclosed[:10])
        results["html_syntax"] = {
            "errors": checker.errors,
            "unclosed": [f"<{t}> at line {p[0]}" for t, p in unclosed]
        }
    except Exception as e:
        print(f"HTML parsing exception: {e}")
        results["html_syntax"] = {"exception": str(e)}

    # CSS Bracket Balance Check
    for cfile in ["assets/css/style.css", "assets/css/rtl-override.css", "assets/css/medicalnet-components.css"]:
        cpath = os.path.join(ROOT, cfile)
        if os.path.exists(cpath):
            with open(cpath, "r", encoding="utf-8") as cf:
                ccontent = cf.read()
                # remove comments and strings
                clean_css = re.sub(r'/\*.*?\*/', '', ccontent, flags=re.DOTALL)
                clean_css = re.sub(r'"(?:\\.|[^"\\])*"', '""', clean_css)
                clean_css = re.sub(r"'(?:\\.|[^'\\])*'", "''", clean_css)
                open_braces = clean_css.count('{')
                close_braces = clean_css.count('}')
                open_parens = clean_css.count('(')
                close_parens = clean_css.count(')')
                open_brackets = clean_css.count('[')
                close_brackets = clean_css.count(']')
                balanced = (open_braces == close_braces) and (open_parens == close_parens) and (open_brackets == close_brackets)
                print(f"[{'PASS' if balanced else 'FAIL'}] CSS {cfile}: braces {open_braces}/{close_braces}, parens {open_parens}/{close_parens}, brackets {open_brackets}/{close_brackets}")

    # CSP checks: inline scripts, inline event handlers, javascript: URLs, unsafe innerHTML
    inline_scripts = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html_content, re.DOTALL | re.IGNORECASE)
    # Non-empty inline scripts
    non_empty_inline_scripts = [s.strip() for s in inline_scripts if s.strip()]
    inline_events = re.findall(r'\s(on[a-z]+)\s*=\s*[\'"][^\'"]*[\'"]', html_content, re.IGNORECASE)
    js_urls = re.findall(r'(?:href|src)\s*=\s*[\'"]javascript:[^\'"]*[\'"]', html_content, re.IGNORECASE)

    # In JS: innerHTML, eval, Function
    js_path = os.path.join(ROOT, "assets/js/main.js")
    js_security_hits = []
    if os.path.exists(js_path):
        with open(js_path, "r", encoding="utf-8") as jf:
            jlines = jf.readlines()
            for idx, line in enumerate(jlines):
                if re.search(r'\binnerHTML\b|\bouterHTML\b|\bdocument\.write\b', line):
                    js_security_hits.append(f"main.js:{idx+1} DOM mutation API: {line.strip()[:60]}")
                if re.search(r'\beval\s*\(|new\s+Function\s*\(', line):
                    js_security_hits.append(f"main.js:{idx+1} Dynamic execution: {line.strip()[:60]}")

    print(f"Non-empty inline <script> tags: {len(non_empty_inline_scripts)}")
    print(f"Inline event handlers (onclick etc.): {len(inline_events)}")
    print(f"javascript: pseudo-URLs: {len(js_urls)}")
    print(f"JS security hits in main.js: {len(js_security_hits)}")
    for hit in js_security_hits:
        print("  ", hit)

    results["security_csp"] = {
        "non_empty_inline_scripts": len(non_empty_inline_scripts),
        "inline_events": inline_events,
        "javascript_urls": js_urls,
        "js_security_hits": js_security_hits
    }

    # 3. ACCESSIBILITY (WCAG 2.1 AA / 2.2.2)
    print("\n--- 3. Accessibility Checks ---")
    # Skip-to-content
    skip_links = re.findall(r'<a[^>]+class=[\'"][^\'"]*skip-link[^\'"]*[\'"][^>]+href=[\'"]#([^\'"]+)[\'"]', html_content)
    skip_valid = False
    if skip_links:
        target_id = skip_links[0]
        skip_valid = target_id in all_ids
        print(f"[{'PASS' if skip_valid else 'FAIL'}] Skip link found targeting #{target_id} (Exists: {skip_valid})")
    else:
        print("[FAIL] No skip link found!")

    # Landmarks
    landmarks = {
        "header": bool(re.search(r'<header\b', html_content)),
        "main": bool(re.search(r'<main\b', html_content)),
        "footer": bool(re.search(r'<footer\b', html_content)),
        "section": bool(re.search(r'<section\b', html_content)),
        "nav": bool(re.search(r'<nav\b', html_content)),
        "aside": bool(re.search(r'<aside\b', html_content))
    }
    for lm, present in landmarks.items():
        print(f"[{'PASS' if present else 'WARN'}] Landmark <{lm}> present: {present}")

    # ARIA attributes
    aria_expanded = re.findall(r'\baria-expanded=[\'"]([^\'"]+)[\'"]', html_content)
    aria_labels = re.findall(r'\baria-label=[\'"]([^\'"]+)[\'"]', html_content)
    aria_pressed = re.findall(r'\baria-pressed=[\'"]([^\'"]+)[\'"]', html_content)
    aria_current = re.findall(r'\baria-current=[\'"]([^\'"]+)[\'"]', html_content)
    role_region = re.findall(r'\brole=[\'"]region[\'"]', html_content)
    role_dialog = re.findall(r'\brole=[\'"]dialog[\'"]', html_content)

    print(f"ARIA counts: aria-expanded={len(aria_expanded)}, aria-label={len(aria_labels)}, aria-pressed={len(aria_pressed)}, aria-current={len(aria_current)}, role='region'={len(role_region)}, role='dialog'={len(role_dialog)}")

    # WCAG 2.2.2 Pause, Stop, Hide (Marquee/Animation pause button)
    has_marquee_pause = bool(re.search(r'(?:pause|play).*marquee|marquee.*(?:pause|play)|data-marquee-toggle|marquee-btn|data-pause-toggle|wall__toggle|wall-toggle', html_content, re.IGNORECASE))
    print(f"[{'PASS' if has_marquee_pause else 'FAIL'}] Marquee pause/play control in HTML (#wall-toggle): {has_marquee_pause}")

    # Check focus-visible in CSS
    has_focus_visible = False
    for cfile in ["assets/css/style.css", "assets/css/rtl-override.css", "assets/css/medicalnet-components.css"]:
        cpath = os.path.join(ROOT, cfile)
        if os.path.exists(cpath):
            with open(cpath, "r", encoding="utf-8") as cf:
                if ":focus-visible" in cf.read():
                    has_focus_visible = True
                    break
    print(f"[:focus-visible] styles present in CSS: {has_focus_visible}")

    # 4. RTL AND PERSIAN TYPOGRAPHY
    print("\n--- 4. RTL & Persian Typography ---")
    html_tag = re.search(r'<html\b([^>]*)>', html_content)
    html_attrs = html_tag.group(1) if html_tag else ""
    is_lang_fa = 'lang="fa"' in html_attrs or "lang='fa'" in html_attrs
    is_dir_rtl = 'dir="rtl"' in html_attrs or "dir='rtl'" in html_attrs
    print(f"[{'PASS' if is_lang_fa else 'FAIL'}] <html lang='fa'>: {is_lang_fa}")
    print(f"[{'PASS' if is_dir_rtl else 'FAIL'}] <html dir='rtl'>: {is_dir_rtl}")

    # Vazirmatn font-family checks in CSS
    vazirmatn_declared = False
    for cfile in ["assets/css/style.css", "assets/css/rtl-override.css", "assets/css/medicalnet-components.css"]:
        cpath = os.path.join(ROOT, cfile)
        if os.path.exists(cpath):
            with open(cpath, "r", encoding="utf-8") as cf:
                if "Vazirmatn" in cf.read():
                    vazirmatn_declared = True
                    print(f"Vazirmatn referenced in {cfile}: True")
    print(f"[{'PASS' if vazirmatn_declared else 'FAIL'}] Vazirmatn font-family declared: {vazirmatn_declared}")

    # Direction-aware rules
    with open(os.path.join(ROOT, "assets/css/rtl-override.css"), "r", encoding="utf-8") as rf:
        rtl_content = rf.read()
    has_rtl_transforms = "scaleX(-1)" in rtl_content or "margin-inline" in rtl_content
    print(f"Direction-aware transforms in rtl-override.css: {has_rtl_transforms}")

    print("\nAudit check completed successfully.")

if __name__ == "__main__":
    run_audit()
