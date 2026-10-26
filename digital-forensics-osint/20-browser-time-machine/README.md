# Project 20 — Browser Time Machine: Build a Timeline from Your Own History

**Track:** Digital Forensics & OSINT  
**Type:** Coding (Python + SQLite)  
**Time:** ~60 minutes  
**Difficulty:** Beginner

## The concept

Your browser keeps a small database of where you have been. In digital
forensics, a timeline is one of the most useful tools: it puts events in order
and helps an investigator explain what happened, when, and in what context.

This project reads a **copy** of a Chrome or Edge `History` database, converts
Chrome’s unusual timestamps, and exports a clean CSV timeline. It also includes
a fictional sample database so you can practice without touching your real
history.

## What the code does

`browser_timeline.py`:

- finds Chrome/Edge history on Windows, macOS, or Linux,
- copies the database to a temporary folder before reading it,
- joins the `visits` and `urls` tables,
- converts Chrome timestamps (microseconds since 1601) into normal dates,
- filters by `--since` and `--until`,
- summarizes top domains and busiest hours,
- writes a CSV with UTC and local timestamps.

`make_sample_history.py` creates a fictional Chrome-style database with fake
example domains and timestamps.

## The two tables that matter

Chrome and Edge use SQLite. The important columns are:

| Table | Column | Meaning |
|---|---|---|
| `urls` | `id` | Internal URL id |
| `urls` | `url` | The address |
| `urls` | `title` | Page title |
| `visits` | `url` | Which URL was visited |
| `visits` | `visit_time` | Chrome timestamp |
| `visits` | `transition` | How the visit started (link, typed, reload, etc.) |

A Chrome timestamp counts **microseconds since 1601-01-01 UTC**. That is why raw
values look like very large numbers.

## Run it

```powershell
cd "C:\Foundev\Cybersecurity beginners\digital-forensics-osint\20-browser-time-machine"

# Practice with the fictional database
py -3 browser_timeline.py --demo

# See where this computer keeps browser history
py -3 browser_timeline.py --list

# Close Chrome first, then auto-detect it
py -3 browser_timeline.py --browser chrome

# Point at a copy you made yourself
py -3 browser_timeline.py --db "C:\Users\You\Desktop\HistoryCopy"

# Filter a date range
py -3 browser_timeline.py --demo --since 2026-10-25 --until 2026-10-26

# Print JSON instead of the summary
py -3 browser_timeline.py --demo --json --limit 5
```

The demo writes `samples/demo_timeline.csv`. A normal run writes
`browser_timeline.csv` unless you use `--output` or `--no-csv`. The default
limit is 500 visits; use `--limit 0` to export everything.

## Browser History locations

**Windows**

```text
Chrome: %LOCALAPPDATA%\Google\Chrome\User Data\Default\History
Edge:   %LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History
```

**macOS**

```text
~/Library/Application Support/Google/Chrome/Default/History
~/Library/Application Support/Microsoft Edge/Default/History
```

**Linux**

```text
~/.config/google-chrome/Default/History
~/.config/chromium/Default/History
~/.config/microsoft-edge/Default/History
```

If you use another profile, the folder may be `Profile 1`, `Profile 2`, etc.
Use `--db` to point at that file.

## Copy first, read second

Close the browser, then copy the `History` file somewhere private. On Windows:

```powershell
$source = "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\History"
$dest   = "$env:USERPROFILE\Desktop\HistoryCopy"
Copy-Item $source $dest
py -3 browser_timeline.py --db $dest
Remove-Item $dest
```

The script also copies the database into a temporary folder itself, so its
normal read does not modify the original. That is a forensic habit: **preserve
the evidence, work on a copy.**

## Experiments to try

1. Run the demo and find the busiest hour. What might that tell an investigator?
2. Filter only 2026-10-25. How many visits remain?
3. Open `samples/history_sample.sqlite` in a SQLite viewer (such as DB Browser
   for SQLite) and compare the raw `visit_time` with the CSV’s readable time.
4. Add a fake visit to the sample with `make_sample_history.py --force`, then
   re-export.
5. Explain why a visit record does **not** prove a person read the page.

## What you learn

- How browser history is stored in SQLite.
- How to convert a non-obvious timestamp format.
- Timeline construction and basic forensic preservation.
- How to summarize large sets of events without reading every row.

## Privacy and safety

- Use **your own** browser profile. Do not inspect someone else’s history
  without permission.
- History can reveal health, financial, political, and relationship details.
  Treat the CSV like a private diary.
- Keep the original database unchanged. Work on copies.
- Delete temporary copies and CSV files when you are finished.
- This tool does not bypass passwords, decrypt profiles, or recover deleted
  records from a disk. It only reads a database you can already access.
