# Project 17 — Metadata Mystery: What Your Photos Reveal

**Track:** Digital Forensics & OSINT  
**Type:** Coding (Python + Pillow)  
**Time:** ~45 minutes  
**Difficulty:** Beginner

## The concept

A photo is more than pixels. Many images carry **EXIF metadata** — a hidden
note card with the camera model, timestamp, editing software, and sometimes GPS
coordinates. Investigators use it to establish timelines and locations. The same
information can expose you when you share a photo online.

This project inspects the note card and creates a cleaned copy with the metadata
removed.

## What the code does

`photo_metadata.py`:

- opens an image and lists its EXIF tags,
- highlights revealing tags such as camera make/model, date, software, artist,
  and GPS,
- converts GPS degrees/minutes/seconds into decimal coordinates,
- creates a new image with EXIF removed (and orientation preserved),
- includes a `demo` command that generates a fictional sample photo, inspects
  it, cleans it, and compares the results.

## Install

```powershell
cd "C:\Foundev\Cybersecurity beginners\digital-forensics-osint\17-metadata-mystery"
py -3 -m pip install -r requirements.txt
```

## Run it

```powershell
# Create a sample, inspect it, strip it, inspect the clean copy
py -3 photo_metadata.py demo

# Inspect any photo you own
py -3 photo_metadata.py inspect "C:\Users\You\Pictures\photo.jpg"

# Machine-readable output
py -3 photo_metadata.py inspect samples/demo_photo.jpg --json

# Remove metadata into a new file (the original is preserved)
py -3 photo_metadata.py strip samples/demo_photo.jpg samples/clean.jpg
```

The demo creates `samples/demo_photo.jpg` and `samples/demo_photo_clean.jpg`.
The original has fake camera tags; the cleaned copy has none.

## Experiments to try

1. Take a photo with your phone and inspect it. Which tags appear?
2. Does your phone record GPS? If yes, view the decimal coordinates on a map —
   **only for your own photo**.
3. Strip the metadata and compare the tag counts.
4. Send a photo to yourself through a chat app, download it, and inspect it
   again. Did the app remove the metadata?
5. Write a short checklist for sharing photos safely.

## What you learn

- EXIF metadata and digital photo forensics.
- How location and device details can leak.
- Why “the image looks harmless” does not mean the file is harmless.
- How to reduce exposure before publishing a photo.

## Safety and ethics

- Inspect only photos you own or have permission to examine.
- GPS data can reveal a home, school, or workplace. Do not publish someone
  else’s location data.
- Stripping metadata does **not** remove what is visible in the image itself
  (street signs, faces, reflections).
- The demo image and its metadata are fictional.
