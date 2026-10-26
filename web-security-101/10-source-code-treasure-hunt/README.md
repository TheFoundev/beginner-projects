# Project 10 — Source Code Treasure Hunt

**Track:** Web Security 101  
**Type:** Coding (Python + HTML)  
**Time:** ~40 minutes  
**Difficulty:** Beginner

## The concept

Every web page ships with its recipe visible to anyone who looks — HTML,
comments, JavaScript, and sometimes leftover notes. It is like reading the
scraps of paper left on a restaurant counter: usually harmless, occasionally
revealing. This project gives you a fictional site with intentional “leaks,” an
audit script to find them, and a cleaned-up version to compare.

## What the code does

- `vulnerable_site/` contains a fictional company page with:
  - an HTML comment about an old admin area,
  - a fake API key in JavaScript,
  - hidden debug/role fields,
  - a `robots.txt` file that advertises private paths,
  - an old admin page and a backup page.
- `fixed_site/` removes those leftovers.
- `audit_site.py` scans local site folders for comments, suspicious wording,
  hard-coded secrets, hidden fields, and `robots.txt` paths.
- `serve_site.py` hosts either version on `127.0.0.1` so you can inspect it in a
  browser.

Every “secret” in the vulnerable site is intentionally fake.

## Run it

```powershell
cd "C:\Foundev\Cybersecurity beginners\web-security-101\10-source-code-treasure-hunt"

# Compare the leaky site with the cleaned-up site
py -3 audit_site.py --demo

# Audit each one separately
py -3 audit_site.py vulnerable_site
py -3 audit_site.py fixed_site

# Serve the leaky site and inspect it by hand
py -3 serve_site.py --site vulnerable_site
# Open http://127.0.0.1:8000, then press Ctrl+U (View Source)

# Serve the cleaned version
py -3 serve_site.py --site fixed_site --port 8080
```

## Your treasure hunt

With the vulnerable site open, find:

1. the HTML comment that mentions an old admin path,
2. the fake API key in `app.js`,
3. the hidden form fields,
4. the paths listed in `robots.txt`,
5. the old admin page and the backup page.

Then run:

```powershell
py -3 audit_site.py vulnerable_site
```

Compare the findings with your list. Did the script catch everything? Did it
miss context that a human noticed?

## Experiments to try

1. Fix one finding in `vulnerable_site` and re-run the audit. What changes?
2. Add a new HTML comment with the word `TODO` and see how it is classified.
3. Explain why `robots.txt` is **not** an access-control system. It asks polite
   crawlers not to visit a path; it does not stop a human from opening it.
4. Add a security header to the fixed site using Project 07’s knowledge.
5. Write a short “before and after” report for a pretend client.

## What you learn

- Information disclosure and why leftovers matter.
- Secure code review habits.
- The difference between hiding a path and protecting it.

## Safety

Everything runs on `127.0.0.1` with fictional data. Never publish real
credentials, internal URLs, or private notes in a public website, and never
probe someone else’s site without permission.
