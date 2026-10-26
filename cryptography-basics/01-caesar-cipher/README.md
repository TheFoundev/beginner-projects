# Project 01 — Secret Agent Starter Kit

**Track:** Cryptography Basics  
**Type:** Coding (Python)  
**Time:** ~45 minutes  
**Difficulty:** Beginner

## The concept

A cipher is a recipe for scrambling a message. The Caesar cipher is one of the
oldest recipes: move every letter forward by the same number of steps. With a
shift of 3, `HELLO` becomes `KHOOR`. It is a fun first look at **symmetric
encryption**, where the same secret (the shift) locks and unlocks the message.

## What the code does

`caesar_cipher.py` can:

- encode a message with any shift from 0 to 25,
- decode a message when you know the shift,
- brute-force all 26 shifts (a lesson in why simple ciphers are weak),
- run an interactive prompt or a zero-setup demo.

## Run it

```powershell
cd "C:\Foundev\Cybersecurity beginners\cryptography-basics\01-caesar-cipher"

# Encode
py -3 caesar_cipher.py --message "HELLO WORLD" --shift 3

# Decode
py -3 caesar_cipher.py --message "KHOOR ZRUOG" --shift 3 --decode

# Watch it break instantly
py -3 caesar_cipher.py --message "KHOOR ZRUOG" --brute-force

# No arguments? Get an interactive prompt.
py -3 caesar_cipher.py

# Zero-setup demonstration
py -3 caesar_cipher.py --demo
```

Expected first result:

```text
Encoded (shift 3): KHOOR ZRUOG
```

## Challenge

1. Encode a short message with a shift of 7.
2. Give the result to a classmate **without telling them the shift**.
3. Ask them to use `--brute-force` and find the readable line.
4. Discuss: why does trying only 26 possibilities make this cipher unsafe?

## What you learn

- How symmetric encryption uses one key to lock and unlock data.
- Why short keys and simple algorithms are easy to break.
- How a tiny Python program can automate a repetitive task.

## Safety

This is a historical learning cipher, not real protection. Never use it for
passwords, private messages, or anything that actually needs to stay secret.
