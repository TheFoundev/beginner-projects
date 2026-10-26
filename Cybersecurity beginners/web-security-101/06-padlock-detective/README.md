# Project 06 — Padlock Detective: Is That Site Really Secure?

**Track:** Web Security 101  
**Type:** Coding (Python)  
**Time:** ~30 minutes  
**Difficulty:** Beginner

## The concept

The padlock in your browser means you and the website are talking through a
private, locked tunnel called HTTPS. It is like a sealed courier envelope:
strangers cannot read the message, but the envelope does not prove the sender
is honest. This project inspects the certificate behind the padlock and
separates what it proves from what it does not.

## What the code does

`padlock_detective.py` performs a normal, verified TLS handshake with a public
site and prints:

- the TLS version and cipher suite,
- who issued the certificate,
- the domain names it covers,
- when it expires and how many days remain,
- a plain-language “proves / does not prove” summary.

It does not bypass certificate warnings, scan ports, or attack anything.

## Run it

```powershell
cd "C:\Foundev\Cybersecurity beginners\web-security-101\06-padlock-detective"

# Inspect one site
py -3 padlock_detective.py example.com

# Machine-readable output
py -3 padlock_detective.py wikipedia.org --json

# Compare a few public sites
py -3 padlock_detective.py --demo
```

## Experiments to try

1. Compare the certificates for your school website, a bank, and a news site.
2. Find the certificate's expiry date. What happens when it expires?
3. Look at the list of names the certificate covers. Why would a certificate
   for `www.example.com` not automatically cover `mail.example.com`?
4. Open the same site in your browser, click the padlock, and compare the
   browser's certificate view with this report.
5. Find a lookalike domain (for example, a misspelling of a real brand) and
   check whether it has a padlock. What does that tell you?

## What you learn

- HTTPS and TLS basics.
- What a certificate authority actually vouches for.
- The difference between a private connection and a trustworthy website.

## Safety

Only connect to public sites you are allowed to visit. This tool is passive:
it completes a TLS handshake, reads the public certificate, and disconnects.
It does not test for vulnerabilities or interact with accounts.
