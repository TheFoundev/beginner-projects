# Project 18 — Digital Footprint Audit: What Can Strangers Learn About You?

**Track:** Digital Forensics & OSINT  
**Type:** Coding (Python) + self-audit  
**Time:** ~60 minutes  
**Difficulty:** Beginner

## The concept

Your **digital footprint** is the trail you leave online: old profiles, public
posts, usernames, email addresses, and photos. OSINT (open-source intelligence)
is the practice of learning from publicly available information. Used on
yourself, it is a privacy check-up. Used on someone else without permission, it
can become harassment or stalking.

This project checks a list of **your own** public URLs and produces a simple
exposure report. It does not search for other people, scrape search engines, or
bypass logins.

## What the code does

`footprint_audit.py`:

- reads a list of your own profile URLs,
- makes one normal GET request per page (plus `robots.txt`),
- records the final URL, HTTP status, HTTPS use, and redirects,
- checks for `noindex` and `robots.txt` disallow rules,
- optionally checks whether your email or phone number is visible on the page,
- lists third-party hosts loaded by the page,
- calculates a simple exposure score,
- writes a CSV report and prints practical next steps.

It also includes a safe demo using reserved example domains.

## Run it

```powershell
cd "C:\Foundev\Cybersecurity beginners\digital-forensics-osint\18-digital-footprint-audit"

# Safe demo
py -3 footprint_audit.py --demo

# Your own profiles
py -3 footprint_audit.py --input my_profiles.txt

# Check whether your public pages expose an email or phone number
py -3 footprint_audit.py --input my_profiles.txt --email "me@example.com"
py -3 footprint_audit.py --input my_profiles.txt --email "me@example.com" --phone "+1 555 0100"
```

Create `my_profiles.txt` by copying `profiles_sample.txt`:

```text
Personal site | https://your-name.example
Photo portfolio | https://photos.example/your-name
Old forum profile | https://forum.example/users/1234
```

## Manual self-audit checklist

Do these steps in a **private browser window**, while signed out:

1. Search your own name and main usernames. Record what a stranger sees.
2. Search your email address. Where does it appear?
3. Check your email on [Have I Been Pwned](https://haveibeenpwned.com/) using
   the official site. Do not enter your password anywhere.
4. Review the privacy settings on your social accounts:
   - Who can see your posts?
   - Can search engines index your profile?
   - Are your phone number and birthday public?
5. Remove or update old accounts you no longer use, starting with the ones that
   expose the most personal data.
6. Turn on two-factor authentication for important accounts.
7. Use a unique password for every account and store them in a password manager.
8. Ask a trusted friend to do the same search and compare notes. They may spot
   something you missed.

## Reading the exposure score

| Score | Meaning | Suggested response |
|---|---|---|
| 0–24 | Lower exposure | Review occasionally |
| 25–49 | Moderate exposure | Remove unnecessary details, check privacy settings |
| 50–100 | High exposure | Act now: remove contact data, fix HTTP, review public posts |

The score is a teaching checklist, not a scientific risk rating. A public
profile that you intentionally use for work may be perfectly fine.

## Experiments to try

1. Which demo page has the highest score? Why?
2. Add your own site with an intentional fake email on a test page. Does the
   script find it?
3. Compare a page served over HTTP with the same page over HTTPS.
4. Add a third-party widget (such as a map) to a test page and see whether the
   third-party host appears.
5. Write a one-page privacy action plan with three changes you will make.

## What you learn

- OSINT concepts applied defensively to yourself.
- How public pages, search indexing, and contact details interact.
- The difference between `robots.txt` (a polite request) and real access
  control (authentication and authorization).

## Safety and ethics

- Audit **only your own** profiles, or profiles you have explicit permission to
  review.
- Do not use this to stalk, harass, dox, or profile another person.
- The tool makes normal public requests. Do not run it aggressively or against
  sites that forbid automated access.
- Never enter real passwords into third-party “footprint” or “breach” sites.
- If you find a data leak involving others, report it to the site or your IT
  team; do not share it.
