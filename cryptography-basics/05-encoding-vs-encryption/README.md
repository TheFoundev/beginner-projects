# Project 05 — The Great Disguise: Encoding vs. Encryption

**Track:** Cryptography Basics  
**Type:** Coding (Python)  
**Time:** ~30 minutes  
**Difficulty:** Beginner

## The concept

Encoding is like putting a letter in a different envelope so it fits through
the mail: it changes the format, not the secrecy. Encryption actually locks the
message. This project shows the difference with three examples: Base64, ROT13,
and AES-256-GCM.

## What the code does

`encoding_vs_encryption.py`:

- Base64-encodes a message and immediately reverses it without a key,
- applies ROT13 twice to show how trivial it is,
- encrypts with AES-256-GCM using a passphrase-derived key,
- demonstrates that a wrong password and a tampered ciphertext are both
  rejected,
- prints a comparison table you can turn into a classroom poster.

## Install

```powershell
py -3 -m pip install -r requirements.txt
```

## Run it

```powershell
cd "C:\Foundev\Cybersecurity beginners\cryptography-basics\05-encoding-vs-encryption"

# Built-in demonstration
py -3 encoding_vs_encryption.py

# Try your own throwaway message (it will ask for a demo passphrase)
py -3 encoding_vs_encryption.py --text "meet me at the library at 4pm"
```

## Experiments to try

1. Run the demo twice. Why does the AES ciphertext change each time while the
   Base64 output stays the same?
2. Decode the Base64 by hand or with another tool. How much effort did it take?
3. Flip one character in the AES ciphertext. What does the program report?
4. Find a website that uses Base64 in a URL or an image. Is that a security
   problem? Why or why not?

## What you learn

- Encoding vs. encryption, and why “looks scrambled” is not security.
- What a salt and nonce do in real encryption.
- How authenticated encryption detects tampering.

## Safety

Everything here is a local demonstration with fake messages. Base64 and ROT13
must never be used to protect passwords or private data. For real encryption,
use a well-reviewed tool such as AES-GCM through a trusted library, and manage
the key carefully.
