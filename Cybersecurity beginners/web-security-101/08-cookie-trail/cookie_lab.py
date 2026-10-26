#!/usr/bin/env python3
"""
Project 08 - Cookie Trail: What Websites Remember About You
==========================================================

A tiny local website that sets cookies with different safety flags so you can
inspect them in DevTools. It also includes an automated demo that prints the
raw Set-Cookie headers and the cookies the server receives.

Run:
    py -3 cookie_lab.py
    py -3 cookie_lab.py --port 8080
    py -3 cookie_lab.py --demo

Then open http://127.0.0.1:8000 and follow the page.

Safety:
    This server listens on 127.0.0.1 only. It uses random fake IDs, stores
    nothing, and is not a real login system.
"""

from __future__ import annotations

import argparse
import html
import secrets
import sys
import threading
import urllib.request
from http.cookiejar import CookieJar
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


PAGE_STYLE = """
body { font-family: system-ui, sans-serif; max-width: 900px; margin: 40px auto;
       padding: 0 20px; line-height: 1.6; color: #172033; background: #f7f7f2; }
h1 { font-size: 2rem; margin-bottom: .2rem; }
code, pre { background: #eef1f5; border-radius: 6px; }
code { padding: 2px 5px; }
pre { padding: 14px; overflow-x: auto; }
table { border-collapse: collapse; width: 100%; margin: 18px 0; background: white; }
th, td { border: 1px solid #d9dee7; padding: 9px 11px; text-align: left; font-size: .92rem; }
th { background: #eef6f5; }
.note { background: #fff8db; border-left: 4px solid #d9a400; padding: 12px 16px; }
.ok { background: #eaf8ef; border-left: 4px solid #1f9d55; padding: 12px 16px; }
a.button { display: inline-block; margin: 4px 6px 4px 0; padding: 9px 14px;
           border: 1px solid #0f766e; border-radius: 999px; color: #0f766e;
           text-decoration: none; font-weight: 700; }
"""


def page(title: str, body: str) -> bytes:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title><style>{PAGE_STYLE}</style></head>
<body>{body}</body></html>""".encode("utf-8")


class CookieHandler(BaseHTTPRequestHandler):
    server_version = "CookieLab/1.0"

    def log_message(self, format: str, *args: Any) -> None:
        # Keep the demo output clean.
        return

    def send_page(self, title: str, body: str, cookies: list[str] | None = None) -> None:
        data = page(title, body)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        for cookie in cookies or []:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if self.path == "/login":
            session_id = secrets.token_hex(12)
            cookies = [
                f"session_id={session_id}; Path=/; HttpOnly; SameSite=Lax",
                "theme=dark; Path=/; Max-Age=3600; SameSite=Lax",
                f"unsafe_pref={secrets.token_hex(4)}; Path=/",
                f"secure_demo={secrets.token_hex(4)}; Path=/; Secure; SameSite=None",
            ]
            body = """
            <h1>Cookies are set</h1>
            <p>This page sent four <code>Set-Cookie</code> headers. Open DevTools
            and inspect them:</p>
            <table>
              <tr><th>Cookie</th><th>Flags</th><th>What to notice</th></tr>
              <tr><td><code>session_id</code></td><td>HttpOnly, SameSite=Lax</td>
                  <td>JavaScript cannot read it, but the server still receives it.</td></tr>
              <tr><td><code>theme</code></td><td>Max-Age=3600, SameSite=Lax</td>
                  <td>A harmless preference with an expiry.</td></tr>
              <tr><td><code>unsafe_pref</code></td><td>none</td>
                  <td>Visible to JavaScript and sent on every request to this site.</td></tr>
              <tr><td><code>secure_demo</code></td><td>Secure, SameSite=None</td>
                  <td>Only sent over HTTPS. Over plain HTTP it may be rejected.</td></tr>
            </table>
            <div class="note"><strong>Try this:</strong> open DevTools →
              Application/Storage → Cookies → <code>http://127.0.0.1</code>.
              Look for the HttpOnly and Secure columns.</div>
            <h2>What JavaScript can see</h2>
            <pre id="jsCookies">Checking...</pre>
            <p><a class="button" href="/report">Server view</a>
               <a class="button" href="/logout">Log out / clear</a>
               <a class="button" href="/">Home</a></p>
            <script>
              document.getElementById('jsCookies').textContent =
                document.cookie || '(no cookies visible to JavaScript)';
            </script>
            """
            self.send_page("Cookies are set", body, cookies)
            return

        if self.path == "/logout":
            cookies = [
                "session_id=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax",
                "theme=; Path=/; Max-Age=0; SameSite=Lax",
                "unsafe_pref=; Path=/; Max-Age=0",
                "secure_demo=; Path=/; Max-Age=0; Secure; SameSite=None",
            ]
            body = """
            <h1>Cookies cleared</h1>
            <p>The server asked the browser to expire all four cookies by setting
            <code>Max-Age=0</code>.</p>
            <p><a class="button" href="/">Home</a>
               <a class="button" href="/login">Set them again</a></p>
            """
            self.send_page("Cookies cleared", body, cookies)
            return

        if self.path == "/report":
            raw_cookie = self.headers.get("Cookie", "")
            rows = []
            for item in raw_cookie.split(";"):
                item = item.strip()
                if not item:
                    continue
                name, _, value = item.partition("=")
                rows.append(f"<tr><td>{html.escape(name)}</td><td>{html.escape(value)}</td></tr>")

            table = (
                "<table><tr><th>Name</th><th>Value</th></tr>" + "".join(rows) + "</table>"
                if rows else "<p><em>No cookies were sent with this request.</em></p>"
            )
            body = f"""
            <h1>What the server sees</h1>
            <p>This is the raw <code>Cookie</code> request header received by the server:</p>
            <pre>{html.escape(raw_cookie or '(empty)')}</pre>
            {table}
            <div class="ok"><strong>Key point:</strong> HttpOnly stops JavaScript from
            reading a cookie. It does <em>not</em> stop the browser from sending that
            cookie to the server.</div>
            <p><a class="button" href="/login">Set cookies</a>
               <a class="button" href="/logout">Clear cookies</a>
               <a class="button" href="/">Home</a></p>
            """
            self.send_page("Server view", body)
            return

        body = """
        <h1>Cookie Trail</h1>
        <p>A local playground for seeing what cookies are, what flags they carry,
        and what the server can see.</p>
        <p><a class="button" href="/login">Set the demo cookies</a>
           <a class="button" href="/report">Server view</a>
           <a class="button" href="/logout">Clear cookies</a></p>
        <h2>Your mission</h2>
        <ol>
          <li>Click “Set the demo cookies.”</li>
          <li>Open DevTools → Application/Storage → Cookies.</li>
          <li>Find <code>session_id</code>, <code>theme</code>,
              <code>unsafe_pref</code>, and <code>secure_demo</code>.</li>
          <li>Record which flags are set on each cookie.</li>
          <li>Open the Server view and compare it with what JavaScript can see.</li>
        </ol>
        <div class="note"><strong>Discussion:</strong> which cookie would you
        remove first if you were designing this site? Why?</div>
        <p>This server binds to 127.0.0.1 only and stores nothing.</p>
        """
        self.send_page("Cookie Trail", body)


def run_demo() -> None:
    """Start the local server, use a cookie jar, and print the raw headers."""
    print("=" * 72)
    print("  COOKIE TRAIL - AUTOMATED DEMO")
    print("=" * 72)

    server = ThreadingHTTPServer(("127.0.0.1", 0), CookieHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    base = f"http://127.0.0.1:{port}"
    jar = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    try:
        print(f"\nLocal server: {base}")
        print("\n1. Requesting /login and reading raw Set-Cookie headers...")
        with opener.open(base + "/login", timeout=5) as response:
            headers = response.headers.get_all("Set-Cookie") or []
        for header in headers:
            print(f"   {header}")

        print("\n2. Cookies stored by the Python cookie jar:")
        for cookie in jar:
            rest = dict(cookie._rest)
            print(f"   {cookie.name}={cookie.value[:12]}...")
            print(f"      domain={cookie.domain} path={cookie.path} secure={cookie.secure}")
            print(f"      expires={cookie.expires} httponly={rest.get('HttpOnly') is not None}")

        print("\n3. Requesting /report. The server receives:")
        with opener.open(base + "/report", timeout=5) as response:
            body = response.read().decode("utf-8", errors="replace")
        for line in body.splitlines():
            if "Cookie" in line or "session_id=" in line:
                print(f"   {line.strip()[:140]}")

        print("\n4. Clearing cookies via /logout...")
        opener.open(base + "/logout", timeout=5).read()
        print(f"   Cookies left in the jar: {len(list(jar))}")

        print("\nWhat this shows:")
        print("  - Cookies are name/value pairs with rules attached.")
        print("  - HttpOnly hides a cookie from JavaScript, not from the server.")
        print("  - Secure limits a cookie to HTTPS connections.")
        print("  - SameSite controls when another site can trigger a request with it.")
        print("  - A cookie is not automatically a tracker, but it can be used to track.")
    finally:
        server.shutdown()
        server.server_close()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="A local cookie inspection lab.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  py -3 cookie_lab.py\n"
            "  py -3 cookie_lab.py --port 8080\n"
            "  py -3 cookie_lab.py --demo\n"
        ),
    )
    parser.add_argument("--port", type=int, default=8000, help="Local port (default: 8000).")
    parser.add_argument("--demo", action="store_true", help="Run the automated demo and exit.")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return 0

    server = ThreadingHTTPServer(("127.0.0.1", args.port), CookieHandler)
    print("=" * 72)
    print("  COOKIE TRAIL")
    print("=" * 72)
    print(f"Open: http://127.0.0.1:{args.port}")
    print("Press Ctrl+C to stop the server.")
    print("This server listens on localhost only and stores nothing.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
