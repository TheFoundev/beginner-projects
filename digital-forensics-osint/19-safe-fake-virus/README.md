# Project 19 — The Safe Fake Virus: Meet the EICAR Test File

**Track:** Digital Forensics & OSINT  
**Type:** Coding (Python) + antivirus lab  
**Time:** ~30 minutes  
**Difficulty:** Beginner

## The concept

How do you know your antivirus is actually working? You could wait for a real
infection, but that would be a terrible plan. Instead, security vendors agreed
on a harmless test string called **EICAR**. It is not malware: it is a short
text file that every major antivirus product is supposed to detect. It is the
fire drill of malware defense.

This project creates, verifies, and cleans up the EICAR test file — and teaches
the first-responder habits you would use for a real suspicious file.

## What the code does

`eicar_lab.py`:

- `create` writes the standard EICAR test file and prints its SHA-256 hash,
- `inspect` confirms whether a file is the real EICAR test string,
- `cleanup` deletes it with a confirmation prompt,
- `demo` does the whole cycle in a temporary folder and prints a first-responder
  checklist.

The script never downloads malware and never executes the test file.

## Run it

```powershell
cd "C:\Foundev\Cybersecurity beginners\digital-forensics-osint\19-safe-fake-virus"

# See the whole safe cycle (nothing is left behind)
py -3 eicar_lab.py demo

# Create the file for an antivirus test
py -3 eicar_lab.py create

# Inspect it (if your antivirus has not quarantined it)
py -3 eicar_lab.py inspect lab/eicar.com.txt

# Clean up
py -3 eicar_lab.py cleanup lab/eicar.com.txt
```

Expected SHA-256 for the standard 68-byte file:

```text
275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f
```

If your editor adds a trailing newline, the file is 69 bytes and the hash is
different. That variant is still harmless; `inspect` accepts it.

If your antivirus immediately quarantines the file, that is a **pass**. Check
your antivirus history/quarantine to confirm the detection.

## What to observe

1. Create the file and watch your antivirus notification.
2. Open your antivirus history. What name did it use for the detection?
3. Run `inspect` before and after the antivirus acts. Did the file disappear?
4. Check the file size and SHA-256. Why is the hash useful in an incident note?
5. Delete the file and confirm it is gone.

## First-responder habits (for a real scare)

If you ever find a genuinely suspicious file:

1. Stop using the device. Do not open the file.
2. Disconnect from Wi-Fi/Ethernet if you suspect real malware.
3. Record the time, file name, source, and SHA-256 hash.
4. Run a full antivirus scan and follow its instructions.
5. Tell your school/workplace IT or security team.
6. Change important passwords from a different, clean device.
7. Do not pay a ransom or install random “cleanup” tools.

For EICAR, an alert is expected and harmless. For real malware, contact a
professional.

## What you learn

- How antivirus detection is tested safely.
- File hashes and evidence notes.
- Calm incident-response habits.
- Why “it is only a text file” can still be useful evidence.

## Safety and ethics

- EICAR is **harmless**. It is the only fake virus used here.
- Do not rename it to pretend it is real malware.
- Do not email it, upload it, or place it on someone else’s computer.
- Do not create or download real malware for “practice.” Use isolated labs and
  professional training platforms instead.
- Antivirus alone is not enough; updates, backups, and safe habits matter too.
