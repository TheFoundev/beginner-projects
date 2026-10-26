# Project 07 — Security Header Safari

**Track:** Web Security 101  
**Type:** Coding (Python)  
**Time:** ~45 minutes  
**Difficulty:** Beginner

## The concept

When a website replies to your browser, it includes hidden instructions called
response headers — like a bouncer’s checklist for what the browser is allowed
to do. Some headers block sneaky scripts, stop clickjacking, or force a secure
connection. This project fetches those headers and grades a site’s setup.

## What the code does

`header_safari.py` sends one normal GET request and checks:

| Header | What it helps with |
|---|---|
| `Content-Security-Policy` | Limits where scripts and resources can load from |
| `Strict-Transport-Security` | Keeps browsers on HTTPS |
| `X-Content-Type-Options` | Stops MIME-type guessing |
| `X-Frame-Options` | Helps prevent clickjacking |
| `Referrer-Policy` | Limits URL leakage to other sites |
| `Permissions-Policy` | Restricts camera, microphone, location, etc. |

It calculates a score, gives a grade from A to F, and explains every check.

## Run it

```powershell
cd "C:\Foundev\Cybersecurity beginners\web-security-101\07-security-header-safari"

# Check one site
py -3 header_safari.py https://example.com

# Compare several sites
py -3 header_safari.py https://example.com https://python.org

# Built-in demo
py -3 header_safari.py --demo

# JSON for a spreadsheet or dashboard
py -3 header_safari.py https://example.com --json
```

## Experiments to try

1. Check your school’s public homepage. Which headers are present?
2. Compare a large technology company with a small local business.
3. Open DevTools → Network → refresh → click the main document → Response
   Headers. Find the same headers by hand.
4. Add one header to a local page you build (Project 09 or 10) and verify it
   appears.
5. Explain why a missing header is a clue, not proof of a vulnerability.

## What you learn

- HTTP response headers and defense in depth.
- How browsers use server instructions to reduce risk.
- Why security is built from several small layers, not one magic switch.

## Safety

Only perform passive checks on public pages you are allowed to visit. This
tool makes a single request and reads the response headers. It does not fuzz,
scan, or attempt to bypass anything.
