# Project 16 — Phishing Autopsy: Dissect a Suspicious Email Safely

**Track:** Digital Forensics & OSINT  
**Type:** Coding (Python)  
**Time:** ~60 minutes  
**Difficulty:** Beginner

## The concept

Phishing is a con game delivered by email: a message pretends to be from
someone you trust and tries to make you click, pay, or type a password. A
forensic analyst treats the email like evidence — read the headers, compare the
domains, inspect the links, and never open the attachment.

This project is the **safe** way to satisfy your curiosity: it parses `.eml`
files offline and never visits a link or launches a file.

## What the code does

`phishing_autopsy.py`:

- reads the visible headers (`From`, `Reply-To`, `Return-Path`, `Subject`),
- checks SPF, DKIM, and DMARC results when present,
- finds links and compares the displayed text with the real destination,
- flags raw IP links, URL shorteners, punycode, suspicious domains, and HTTP,
- lists attachments by name and type **without opening them**,
- detects credential-collecting HTML forms,
- scores the message and explains every point,
- includes three fictional sample emails: one obvious phish, one invoice with an
  archive attachment, and one harmless newsletter.

## Run it

```powershell
cd "C:\Foundev\Cybersecurity beginners\digital-forensics-osint\16-phishing-autopsy"

# Look at all three samples
py -3 phishing_autopsy.py --demo

# One file with full detail
py -3 phishing_autopsy.py samples/01-password-reset.eml

# Several files
py -3 phishing_autopsy.py samples/*.eml

# Machine-readable report
py -3 phishing_autopsy.py samples/01-password-reset.eml --json
```

## How to save a real suspicious email as `.eml`

Use this only for messages you received and have permission to inspect:

- **Outlook (desktop):** drag the message to a folder, or File → Save As → `.msg`
  (this parser expects `.eml`; export from a client that supports it).
- **Thunderbird:** select the message → Ctrl+S → save as `.eml`.
- **Gmail:** open the message → three-dot menu → **Download message** (`.eml`).

Then run the parser on the saved file. Do not forward the original to strangers.

## Reading the sample reports

| Sample | What to notice |
|---|---|
| `01-password-reset.eml` | Failed SPF/DMARC, a different Reply-To domain, an IP-address link, and a password form inside the email |
| `02-invoice-attachment.eml` | Authentication passes, but the message uses invoice pressure and an archive attachment |
| `03-newsletter.eml` | Matching domains, passing authentication, a normal HTTPS link, no form, no attachment |

**Important:** passing SPF/DKIM/DMARC does **not** make an email safe. Those
checks only say the sending domain authorized the message. A real company can
send a legitimate invoice, and an attacker can compromise a legitimate account.

## Experiments to try

1. Which sample has the highest score? List the three findings that added the
   most points.
2. Change one character in a sample link so its domain no longer matches the
   sender. Re-run the parser.
3. Add a fake `Attachment: invoice.pdf.exe` part and see the warning.
4. Remove the `Authentication-Results` header. How does the score change?
5. Write a one-page incident note: what arrived, what you observed, what you
   did **not** click, and who you reported it to.

## What you learn

- Email headers and sender authentication in plain language.
- Link inspection without clicking.
- Attachment risk and safe evidence handling.
- Why “the email looked real” is not a security control.

## Safety and ethics

- This tool is **offline**. It does not fetch remote images, visit links, or run
  attachments.
- Use it only on emails you received or have permission to analyze.
- Never test phishing links against other people.
- If you think you clicked a real phishing link, change the affected password
  from a clean device, enable two-factor authentication, and tell your IT or
  security team.
