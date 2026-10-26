# Project 04 — The Unbreakable Diary: Encrypt a Folder

**Track:** Cryptography Basics  
**Type:** Tool + Python  
**Time:** ~30 minutes  
**Difficulty:** Beginner

## The concept

Encryption is like putting your diary in a strongbox that opens only with your
secret phrase. Even if someone copies the box, the pages stay unreadable. This
project turns a whole folder into one encrypted `.diary` file using **AES-256**
and a passphrase-derived key.

The code also uses **authenticated encryption** (AES-GCM), which detects
tampering as well as hiding the contents.

## What the code does

`encrypted_diary.py`:

- compresses a folder into an in-memory ZIP,
- derives a 256-bit key from your passphrase with PBKDF2 (600,000 iterations),
- encrypts everything with a random salt and nonce,
- decrypts only with the correct passphrase,
- blocks unsafe archive paths (“zip slip”),
- includes a complete demo that tries a wrong password first.

## Install

```powershell
py -3 -m pip install -r requirements.txt
```

If you prefer a graphical tool, 7-Zip can also create AES-256 encrypted
archives. This project shows what is happening under the hood.

## Run it

```powershell
cd "C:\Foundev\Cybersecurity beginners\cryptography-basics\04-encrypted-diary"

# Watch the full round trip first
py -3 encrypted_diary.py demo

# Encrypt your own folder of fake notes
py -3 encrypted_diary.py encrypt .\my_fake_notes -o .\my_fake_notes.diary

# Decrypt it
py -3 encrypted_diary.py decrypt .\my_fake_notes.diary -o .\restored_notes
```

You will be prompted for a passphrase. Use at least 12 characters. The passphrase
is never written to disk or passed on the command line.

## Experiments to try

1. Encrypt the same folder twice with the same passphrase. The output files
   should be different because the salt and nonce are random.
2. Try decrypting with the wrong passphrase. Read the error message.
3. Change one byte in the middle of the `.diary` file and try again. What
   happens? (Use a copy, never your only file.)
4. Compare AES-GCM with the Caesar cipher from Project 01. Why is one safe and
   the other not?

## What you learn

- Encryption at rest and password-based key derivation.
- Salt, nonce, and authenticated encryption in plain language.
- Key management: losing the key means losing the data.

## Safety

Use fake notes for practice. There is **no password recovery**. Never encrypt
your only copy of important files. Keep backups, and use a trusted password
manager to store the passphrase.
