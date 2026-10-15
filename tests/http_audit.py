"""
MedicalNet HTTP Endpoint & Delivery Test Suite
Tests zero-dependency server (serve.cjs) for status codes, headers, compression, and delivery.
"""
import urllib.request
import urllib.error
import json
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8090"

ENDPOINTS = [
    ("/", 200, "text/html"),
    ("/index.html", 200, "text/html"),
    ("/assets/css/style.css", 200, "text/css"),
    ("/assets/css/rtl-override.css", 200, "text/css"),
    ("/assets/css/medicalnet-components.css", 200, "text/css"),
    ("/assets/js/main.js", 200, "text/javascript"),
    ("/assets/img/hero-bg.webp", 200, "image/webp"),
    ("/assets/img/favicon.svg", 200, "image/svg+xml"),
    ("/assets/img/world-map.svg", 200, "image/svg+xml"),
    ("/assets/fonts/outfit-var.woff2", 200, "font/woff2"),
    ("/assets/fonts/dm-sans-var.woff2", 200, "font/woff2"),
    ("/assets/fonts/inter-var.woff2", 200, "font/woff2"),
    ("/robots.txt", 200, "text/plain"),
    ("/_headers", 200, "application/octet-stream"),
    ("/non-existent-file.xyz", 404, "text/plain")
]

def test_endpoints():
    print(f"Testing server endpoints at {BASE_URL}...")
    success = True
    for path, expected_status, expected_mime in ENDPOINTS:
        url = BASE_URL + path
        try:
            req = urllib.request.Request(url, headers={"Accept-Encoding": "gzip"})
            with urllib.request.urlopen(req) as resp:
                status = resp.status
                ctype = resp.headers.get("Content-Type", "")
                csp = resp.headers.get("Content-Security-Policy", "")
                nosniff = resp.headers.get("X-Content-Type-Options", "")
                encoding = resp.headers.get("Content-Encoding", "")
                data = resp.read()
                
                status_ok = (status == expected_status)
                mime_ok = expected_mime in ctype
                print(f"[{'PASS' if (status_ok and mime_ok) else 'FAIL'}] {path} -> {status} ({ctype}), length={len(data)}, gzip={encoding=='gzip'}")
                if not (status_ok and mime_ok):
                    success = False
        except urllib.error.HTTPError as e:
            status_ok = (e.code == expected_status)
            ctype = e.headers.get("Content-Type", "")
            mime_ok = expected_mime in ctype
            print(f"[{'PASS' if (status_ok and mime_ok) else 'FAIL'}] {path} -> HTTP {e.code} (expected {expected_status})")
            if not (status_ok and mime_ok):
                success = False
        except Exception as e:
            print(f"[FAIL] {path} -> Exception: {e}")
            success = False

    return success

if __name__ == "__main__":
    ok = test_endpoints()
    print("\nHTTP Server Verification:", "ALL PASSED" if ok else "SOME FAILED")
    sys.exit(0 if ok else 1)
