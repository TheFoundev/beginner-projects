#!/usr/bin/env python3
"""
Project 09 - Form Fortress: Build a Sign-Up Page That Says "No"
==============================================================

A local sign-up form with both browser-side and server-side validation. The
browser checks are friendly; the server checks are the real gate.

Run:
    py -3 form_fortress.py
    py -3 form_fortress.py --port 8080
    py -3 form_fortress.py --demo

Then open http://127.0.0.1:8000.

Safety:
    This is a local teaching app. It does not create accounts, store data, or
    send anything over the internet. Use fake names and fake passwords.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

NAME_RE = re.compile(r"^[A-Za-z][A-Za-z '\-]{1,49}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")
COMMON_PASSWORDS = {
    "password", "password1", "123456", "123456789", "qwerty", "letmein",
    "welcome", "admin", "iloveyou", "abc123", "passw0rd", "dragon",
}

FORM_STYLE = """
:root { --ink:#172033; --muted:#667085; --line:#d9dee7; --teal:#0f766e; --bad:#b42318; --good:#067647; }
* { box-sizing: border-box; }
body { margin:0; background:#f7f7f2; color:var(--ink); font-family:system-ui,sans-serif; line-height:1.6; }
main { max-width:720px; margin:40px auto; padding:0 20px; }
.card { background:#fff; border:1px solid var(--line); border-radius:16px; padding:28px; box-shadow:0 12px 30px rgba(16,24,40,.06); }
h1 { margin:0 0 8px; font-size:2rem; letter-spacing:-.03em; }
p.lede { margin:0 0 22px; color:var(--muted); }
label { display:block; margin:16px 0 6px; font-weight:700; font-size:.92rem; }
input { width:100%; padding:11px 12px; border:1px solid var(--line); border-radius:9px; font:inherit; }
input:focus { outline:3px solid rgba(15,118,110,.16); border-color:var(--teal); }
.error { margin:6px 0 0; color:var(--bad); font-size:.85rem; }
.field.invalid input { border-color:var(--bad); background:#fffbfa; }
button { margin-top:22px; width:100%; padding:12px 16px; border:0; border-radius:999px; background:var(--teal); color:#fff; font:inherit; font-weight:750; cursor:pointer; }
button:hover { background:#115e59; }
.note { margin-top:20px; padding:12px 14px; border-left:4px solid #d9a400; background:#fff8db; font-size:.9rem; }
.success { border-left:4px solid var(--good); background:#ecfdf3; padding:14px 16px; border-radius:8px; }
ul { margin:8px 0 0; padding-left:20px; }
code { background:#eef1f5; padding:2px 5px; border-radius:5px; }
"""


def first(form: dict[str, list[str]], key: str) -> str:
    return form.get(key, [""])[0]


def validate_form(form: dict[str, list[str]]) -> tuple[dict[str, str], dict[str, str]]:
    """Return cleaned values and a dictionary of error messages."""
    values = {
        "name": first(form, "name").strip(),
        "email": first(form, "email").strip(),
        "password": first(form, "password"),
        "confirm": first(form, "confirm"),
    }
    errors: dict[str, str] = {}

    if not NAME_RE.fullmatch(values["name"]):
        errors["name"] = "Use 2-50 letters, spaces, hyphens, or apostrophes."

    if not EMAIL_RE.fullmatch(values["email"]) or len(values["email"]) > 254:
        errors["email"] = "Enter a simple email address such as student@example.com."

    password = values["password"]
    password_problems: list[str] = []
    if len(password) < 12:
        password_problems.append("at least 12 characters")
    if not any(char.islower() for char in password):
        password_problems.append("a lowercase letter")
    if not any(char.isupper() for char in password):
        password_problems.append("an uppercase letter")
    if not any(char.isdigit() for char in password):
        password_problems.append("a number")
    if not any(not char.isalnum() for char in password):
        password_problems.append("a symbol")
    if password.lower() in COMMON_PASSWORDS:
        password_problems.append("something less common")
    if values["email"] and password.lower() == values["email"].split("@")[0].lower():
        password_problems.append("something different from your email name")

    if password_problems:
        errors["password"] = "Add " + ", ".join(password_problems) + "."
    if values["confirm"] != password:
        errors["confirm"] = "The two passwords do not match."

    return values, errors


def render_form(values: dict[str, str], errors: dict[str, str], status: int = 200) -> tuple[int, bytes]:
    def field(name: str, label: str, input_type: str, hint: str = "", autocomplete: str = "off") -> str:
        css = "field invalid" if name in errors else "field"
        error = f'<p class="error">{html.escape(errors[name])}</p>' if name in errors else ""
        value = "" if name in {"password", "confirm"} else html.escape(values.get(name, ""))
        return f"""
        <div class="{css}">
          <label for="{name}">{html.escape(label)}</label>
          <input id="{name}" name="{name}" type="{input_type}" value="{value}"
                 autocomplete="{autocomplete}" placeholder="{html.escape(hint)}">
          {error}
        </div>"""

    body = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Form Fortress</title><style>{FORM_STYLE}</style></head>
<body><main><div class="card">
  <h1>Form Fortress</h1>
  <p class="lede">A fake sign-up page. Nothing is stored. Use fake details.</p>
  <form method="post" action="/" novalidate id="signupForm">
    {field("name", "Name", "text", "Ada Lovelace")}
    {field("email", "Email", "email", "ada@example.com")}
    {field("password", "Password", "password", "12+ characters, mixed types")}
    {field("confirm", "Confirm password", "password", "Type it again")}
    <button type="submit">Create fake account</button>
  </form>
  <div class="note"><strong>Defender note:</strong> the browser checks below are
  for friendly feedback only. Anyone can bypass them, so the Python server
  repeats every check. Real sites also need HTTPS, rate limiting, CSRF
  protection, and safe password storage such as Argon2 or bcrypt.</div>
  <script>
    const form = document.getElementById('signupForm');
    form.addEventListener('submit', function (event) {{
      const name = form.name.value.trim();
      const email = form.email.value.trim();
      const password = form.password.value;
      const confirm = form.confirm.value;
      const problems = [];

      if (!/^[A-Za-z][A-Za-z '\\-]{{1,49}}$/.test(name)) problems.push('Name looks invalid.');
      if (!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]{{2,}}$/.test(email)) problems.push('Email looks invalid.');
      if (password.length < 12) problems.push('Password needs 12+ characters.');
      if (!/[a-z]/.test(password) || !/[A-Z]/.test(password)) problems.push('Mix upper and lower case.');
      if (!/[0-9]/.test(password)) problems.push('Add a number.');
      if (!/[^A-Za-z0-9]/.test(password)) problems.push('Add a symbol.');
      if (password !== confirm) problems.push('Passwords do not match.');

      if (problems.length) {{
        event.preventDefault();
        alert('Please fix:\\n\\n' + problems.join('\\n'));
      }}
    }});
  </script>
</div></main></body></html>"""
    return status, body.encode("utf-8")


def render_success(values: dict[str, str]) -> bytes:
    body = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Validated</title><style>{FORM_STYLE}</style></head>
<body><main><div class="card">
  <h1>Validation passed</h1>
  <div class="success">
    <p><strong>No account was created.</strong> This is a teaching app.</p>
    <p>Name: {html.escape(values['name'])}<br>
       Email: {html.escape(values['email'])}</p>
  </div>
  <p style="margin-top:20px">The server repeated every check. That is the important
  part: browser-side validation is a convenience, not a security boundary.</p>
  <p><a href="/">Try another fake sign-up</a></p>
</div></main></body></html>"""
    return body.encode("utf-8")


class FormHandler(BaseHTTPRequestHandler):
    server_version = "FormFortress/1.0"

    def log_message(self, format: str, *args: object) -> None:
        return

    def send_html(self, status: int, data: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if self.path != "/":
            self.send_html(404, b"<h1>404</h1><p>Try <a href='/'>/</a>.</p>")
            return
        _, data = render_form({"name": "", "email": "", "password": "", "confirm": ""}, {})
        self.send_html(200, data)

    def do_POST(self) -> None:
        if self.path != "/":
            self.send_html(404, b"<h1>404</h1>")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length <= 0 or length > 10_000:
            self.send_html(400, b"<h1>Bad request</h1><p>Invalid form size.</p>")
            return

        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        form = parse_qs(raw, keep_blank_values=True)
        values, errors = validate_form(form)

        if errors:
            status, data = render_form(values, errors, status=400)
            self.send_html(status, data)
            return

        self.send_html(200, render_success(values))


def run_validation_demo() -> None:
    print("=" * 72)
    print("  FORM FORTRESS - SERVER-SIDE VALIDATION DEMO")
    print("=" * 72)

    cases = [
        ("Empty form", {}),
        ("Bad email", {"name": ["Ada Lovelace"], "email": ["not-an-email"],
                       "password": ["Blue-Coffee-Rocket-42!"], "confirm": ["Blue-Coffee-Rocket-42!"]}),
        ("Weak password", {"name": ["Ada Lovelace"], "email": ["ada@example.com"],
                           "password": ["password123"], "confirm": ["password123"]}),
        ("Mismatch", {"name": ["Ada Lovelace"], "email": ["ada@example.com"],
                      "password": ["Blue-Coffee-Rocket-42!"], "confirm": ["different"]}),
        ("Valid fake sign-up", {"name": ["Ada Lovelace"], "email": ["ada@example.com"],
                                "password": ["Blue-Coffee-Rocket-42!"], "confirm": ["Blue-Coffee-Rocket-42!"]}),
    ]

    for label, form in cases:
        values, errors = validate_form(form)
        if errors:
            print(f"\n[REJECT] {label}")
            for field, message in errors.items():
                print(f"  - {field}: {message}")
        else:
            print(f"\n[ACCEPT] {label} -> {values['name']} <{values['email']}>")

    print("\nNotice: rejecting bad input is not about being unfriendly.")
    print("It is about keeping confusing or dangerous data out of the system.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="A local sign-up form with client-side and server-side validation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  py -3 form_fortress.py\n"
            "  py -3 form_fortress.py --port 8080\n"
            "  py -3 form_fortress.py --demo\n"
        ),
    )
    parser.add_argument("--port", type=int, default=8000, help="Local port (default: 8000).")
    parser.add_argument("--demo", action="store_true", help="Test the validation rules and exit.")
    args = parser.parse_args()

    if args.demo:
        run_validation_demo()
        return 0

    server = ThreadingHTTPServer(("127.0.0.1", args.port), FormHandler)
    print("=" * 72)
    print("  FORM FORTRESS")
    print("=" * 72)
    print(f"Open: http://127.0.0.1:{args.port}")
    print("Use fake details. Nothing is stored. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
