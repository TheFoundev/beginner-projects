# Project 02 — The Password Power Meter

**Track:** Cryptography Basics  
**Type:** Coding (Python)  
**Time:** ~60 minutes  
**Difficulty:** Beginner

## The concept

Passwords are like house keys: a short, simple key is easy to copy, while a
long, unusual one is much harder. This project scores a password on length,
character variety, and predictable patterns, then gives friendly advice. It
also estimates **entropy** — a rough measure of how many guesses an attacker
might need.

## What the code does

`password_strength.py` asks for a made-up password, hides it while you type,
and prints:

- a score from 0 to 100,
- a rating from “Very weak” to “Very strong,”
- an entropy estimate,
- specific tips for improvement.

It never saves the password, never sends it anywhere, and deliberately has no
command-line password option (so passwords do not end up in shell history).

## Run it

```powershell
cd "C:\Foundev\Cybersecurity beginners\cryptography-basics\02-password-power-meter"

# Interactive: type a fake password
py -3 password_strength.py

# See a full demonstration with sample passwords
py -3 password_strength.py --demo
```

## Experiments to try

1. Compare `password123`, `Summer2026!`, and `Blue-Coffee-Rocket-42!`.
2. Try a 20-character passphrase made of four random words.
3. Add one symbol to a short password. Does the score improve much?
4. Add four characters instead. Which change helps more?
5. Read the advice and explain in your own words why length matters.

## What you learn

- Password strength and entropy in plain language.
- Why predictable patterns (names, years, keyboard runs) are dangerous.
- Why a password manager and unique passwords matter more than complex-looking
  short passwords.

## Safety

Use fake passwords for this exercise. A real password should only go into a
trusted password manager or the real website’s login page. This script runs
locally; that does **not** make every online “password strength” site safe.
