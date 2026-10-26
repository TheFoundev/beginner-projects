# Project 03 — Hash Detective: The Digital Fingerprint

**Track:** Cryptography Basics  
**Type:** Coding (Python)  
**Time:** ~45 minutes  
**Difficulty:** Beginner

## The concept

A hash is a digital fingerprint for a file. Feed in the same bytes and you
always get the same fingerprint. Change one character and the fingerprint
changes completely. Security teams compare hashes to check whether a download
is genuine, uncorrupted, or tampered with.

Hashing is **one-way**: you cannot “unhash” a fingerprint back into the file.

## What the code does

`hash_detective.py`:

- calculates the SHA-256 fingerprint of a file or a piece of text,
- compares it with an expected fingerprint,
- demonstrates the “avalanche effect” by changing one character,
- runs entirely offline with Python’s built-in `hashlib`.

## Run it

```powershell
cd "C:\Foundev\Cybersecurity beginners\cryptography-basics\03-hash-detective"

# Fingerprint a file
py -3 hash_detective.py --file README.md

# Fingerprint some text
py -3 hash_detective.py --text "hello"

# Verify a published checksum
py -3 hash_detective.py --file download.zip --expected "paste-the-published-hash-here"

# Watch one character change everything
py -3 hash_detective.py --demo
```

A SHA-256 fingerprint is always 64 hexadecimal characters long.

## Challenge

1. Create a text file with one sentence.
2. Hash it and save the fingerprint.
3. Change one letter.
4. Hash it again and count how many characters changed.
5. Restore the original text and confirm the fingerprint returns to the
   original value.
6. Find a real download page that publishes a SHA-256 checksum and verify a
   file you downloaded. Only download from the official source.

## What you learn

- How hashing supports **file integrity**.
- Why a checksum can detect tampering but cannot hide data.
- How the same input always produces the same hash.

## Safety

Hashing is read-only and safe. Only hash files you own or have permission to
inspect. A hash proves that two sets of bytes match; it does **not** prove the
file is safe or trustworthy. A malicious file can have a perfectly valid hash.
