#!/usr/bin/env python3
"""
Project 20 - Browser Time Machine: Build a Timeline from Your Own History
=======================================================================

Read a copy of a Chrome or Edge History SQLite database and export a clean
timeline. This is a beginner digital-forensics exercise: preserve the original,
work on a copy, and explain what the timestamps mean.

Run:
    py -3 browser_timeline.py --demo
    py -3 browser_timeline.py --browser chrome
    py -3 browser_timeline.py --db "C:\\path\\to\\History"
    py -3 browser_timeline.py --db History --since 2026-10-25 --until 2026-10-26

Safety:
    Use your own browser profile. History contains sensitive data. Close the
    browser before copying, keep the CSV private, and delete it when finished.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import sqlite3
import sys
import tempfile
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


CHROME_EPOCH = datetime(1601, 1, 1, tzinfo=timezone.utc)
TRANSITIONS = {
    0: "link",
    1: "typed",
    2: "bookmark",
    3: "auto subframe",
    4: "manual subframe",
    5: "generated",
    6: "auto top-level",
    7: "form submit",
    8: "reload",
    9: "keyword",
    10: "keyword generated",
}


def from_chrome_time(value: int) -> datetime:
    return CHROME_EPOCH + timedelta(microseconds=int(value))


def to_chrome_time(value: datetime) -> int:
    if value.tzinfo is None:
        value = value.replace(tzinfo=datetime.now().astimezone().tzinfo)
    return int((value.astimezone(timezone.utc) - CHROME_EPOCH).total_seconds() * 1_000_000)


def parse_when(value: str | None, end_of_day: bool = False) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"Use an ISO date such as 2026-10-26 or 2026-10-26T14:30: {value}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=datetime.now().astimezone().tzinfo)
    if end_of_day and len(value) == 10:
        parsed = parsed + timedelta(days=1)
    return parsed


def browser_paths() -> list[tuple[str, Path]]:
    if os.name == "nt":
        local = Path(os.environ.get("LOCALAPPDATA", ""))
        return [
            ("Chrome", local / "Google" / "Chrome" / "User Data" / "Default" / "History"),
            ("Edge", local / "Microsoft" / "Edge" / "User Data" / "Default" / "History"),
        ]
    if sys.platform == "darwin":
        support = Path.home() / "Library" / "Application Support"
        return [
            ("Chrome", support / "Google" / "Chrome" / "Default" / "History"),
            ("Edge", support / "Microsoft Edge" / "Default" / "History"),
        ]
    config = Path.home() / ".config"
    return [
        ("Chrome", config / "google-chrome" / "Default" / "History"),
        ("Chromium", config / "chromium" / "Default" / "History"),
        ("Edge", config / "microsoft-edge" / "Default" / "History"),
    ]


def find_database(explicit: Path | None, browser: str | None, demo: bool, base: Path) -> tuple[str, Path]:
    if demo:
        sample = base / "samples" / "history_sample.sqlite"
        if not sample.exists():
            from make_sample_history import create_sample_db

            create_sample_db(sample)
        return "Fictional sample", sample

    if explicit:
        if not explicit.is_file():
            raise FileNotFoundError(f"History database not found: {explicit}")
        return "Custom database", explicit

    candidates = browser_paths()
    if browser:
        candidates = [(name, path) for name, path in candidates if name.lower() == browser.lower()]

    existing = [(name, path) for name, path in candidates if path.is_file()]
    if not existing:
        raise FileNotFoundError(
            "No browser History database found. Close the browser and pass --db PATH. "
            "Detected locations: " + ", ".join(str(path) for _, path in candidates)
        )
    if len(existing) > 1 and not browser:
        print("[!] Multiple browsers found; using the first. Use --browser chrome or --browser edge.")
    return existing[0]


def history_rows(db_path: Path, since: datetime | None, until: datetime | None, limit: int) -> list[dict[str, Any]]:
    """Copy the database, query it, and return normalized rows."""
    with tempfile.TemporaryDirectory(prefix="browser-timeline-") as temporary:
        copy_path = Path(temporary) / "History"
        try:
            shutil.copy2(db_path, copy_path)
            for suffix in ("-wal", "-shm"):
                companion = db_path.with_name(db_path.name + suffix)
                if companion.exists():
                    shutil.copy2(companion, copy_path.with_name(copy_path.name + suffix))
        except OSError:
            # Last resort: read the original directly. Close the browser first.
            copy_path = db_path

        connection = sqlite3.connect(str(copy_path))
        try:
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                ).fetchall()
            }
            if "urls" not in tables or "visits" not in tables:
                raise ValueError("This does not look like a Chrome/Edge History database.")

            clauses = []
            params: list[Any] = []
            if since:
                clauses.append("v.visit_time >= ?")
                params.append(to_chrome_time(since))
            if until:
                clauses.append("v.visit_time < ?")
                params.append(to_chrome_time(until))
            where = " WHERE " + " AND ".join(clauses) if clauses else ""

            query = (
                "SELECT v.id, v.visit_time, u.url, u.title, v.transition "
                "FROM visits v JOIN urls u ON u.id = v.url"
                + where
                + " ORDER BY v.visit_time ASC"
            )
            if limit > 0:
                query += " LIMIT ?"
                params.append(limit)

            raw_rows = connection.execute(query, params).fetchall()
        finally:
            connection.close()

    records: list[dict[str, Any]] = []
    for visit_id, visit_time, url, title, transition in raw_rows:
        moment = from_chrome_time(visit_time)
        local = moment.astimezone()
        domain = (urlparse(url).hostname or "").lower()
        transition_value = int(transition or 0) & 0xFF
        records.append(
            {
                "visit_id": visit_id,
                "visit_time_utc": moment.isoformat(),
                "visit_time_local": local.isoformat(),
                "url": url,
                "title": title or "",
                "domain": domain,
                "transition": TRANSITIONS.get(transition_value, f"code {transition_value}"),
            }
        )
    return records


def print_summary(
    records: list[dict[str, Any]],
    source: str,
    db_path: Path,
    output: Path,
    limit: int,
    save_csv: bool = True,
) -> None:
    print("=" * 82)
    print("  BROWSER TIME MACHINE")
    print("=" * 82)
    print(f"Source : {source}")
    print(f"Database: {db_path}")
    print(f"Visits : {len(records)}")
    if not records:
        print("\nNo visits matched the date filter.")
        return

    first = records[0]["visit_time_local"]
    last = records[-1]["visit_time_local"]
    print(f"Range  : {first}  ->  {last}")
    print(f"Unique URLs: {len({item['url'] for item in records})}")
    print(f"Unique domains: {len({item['domain'] for item in records if item['domain']})}")

    domains = Counter(item["domain"] for item in records if item["domain"])
    print("\nTop domains:")
    for domain, count in domains.most_common(10):
        print(f"  {domain:<40} {count}")

    hours = Counter(datetime.fromisoformat(item["visit_time_local"]).hour for item in records)
    print("\nBusiest local hours:")
    for hour, count in hours.most_common(5):
        print(f"  {hour:02d}:00-{hour:02d}:59  {count} visits")

    print(f"\nFirst {min(15, len(records))} visits:")
    print(f"  {'Local time':<20} {'Domain':<26} Title")
    for item in records[:15]:
        local = item["visit_time_local"][:19].replace("T", " ")
        print(f"  {local:<20} {item['domain']:<26} {item['title'][:46]}")

    if save_csv:
        print(f"\n[+] Timeline CSV: {output}")
    else:
        print("\n[i] CSV output disabled by --no-csv.")
    print("[!] Browser history is sensitive. Keep the CSV private and delete it when done.")


def write_csv(records: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "visit_id", "visit_time_utc", "visit_time_local", "url",
                "title", "domain", "transition",
            ],
        )
        writer.writeheader()
        writer.writerows(records)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export a timeline from your own Chrome/Edge History database.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  py -3 browser_timeline.py --demo\n"
            "  py -3 browser_timeline.py --browser chrome\n"
            "  py -3 browser_timeline.py --db History --since 2026-10-25 --until 2026-10-26\n"
            "  py -3 browser_timeline.py --list\n"
        ),
    )
    parser.add_argument("--db", type=Path, help="Path to a copy of Chrome/Edge History.")
    parser.add_argument("--browser", choices=["chrome", "edge", "chromium"], help="Auto-detect this browser.")
    parser.add_argument("--since", help="Start date/time (ISO). Date-only means local midnight.")
    parser.add_argument("--until", help="End date/time (ISO). Date-only includes the whole day.")
    parser.add_argument("--limit", type=int, default=500, help="Maximum visits; 0 means all (default: 500).")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("browser_timeline.csv"),
        help="CSV output path.",
    )
    parser.add_argument("--list", action="store_true", help="Show detected browser History paths.")
    parser.add_argument("--json", action="store_true", help="Print records as JSON instead of writing a report.")
    parser.add_argument("--no-csv", action="store_true", help="Do not write the CSV file.")
    parser.add_argument("--demo", action="store_true", help="Use the fictional sample database.")
    args = parser.parse_args()

    if args.list:
        print("Detected browser History locations:")
        for name, path in browser_paths():
            marker = "FOUND" if path.is_file() else "missing"
            print(f"  [{marker}] {name:<8} {path}")
        return 0

    if args.limit < 0:
        print("ERROR: --limit cannot be negative.")
        return 1

    base = Path(__file__).resolve().parent
    try:
        since = parse_when(args.since)
        until = parse_when(args.until, end_of_day=True)
        source, db_path = find_database(args.db, args.browser, args.demo, base)
    except (ValueError, FileNotFoundError) as error:
        print(f"ERROR: {error}")
        return 1

    if args.demo and args.output == Path("browser_timeline.csv"):
        args.output = base / "samples" / "demo_timeline.csv"

    try:
        records = history_rows(db_path, since, until, args.limit)
    except (sqlite3.Error, OSError, ValueError) as error:
        print(f"ERROR: could not read history: {error}")
        print("Close the browser, copy the History file, and use --db to point at the copy.")
        return 1

    if args.json:
        print(json.dumps(records, indent=2))
    else:
        print_summary(records, source, db_path, args.output, args.limit, save_csv=not args.no_csv)

    if records and not args.no_csv:
        write_csv(records, args.output)
        if not args.json:
            print(f"\nWrote {len(records)} rows.")

    if not records:
        print("No matching visits. Try a wider date range or a different browser profile.")
        return 1

    print("\nHow to read this responsibly:")
    print("  - Timestamps are shown in UTC and in your local timezone.")
    print("  - A visit record means the browser opened the URL, not that you read it.")
    print("  - History can be incomplete, synchronized across devices, or deleted.")
    print("  - Treat someone else's history as private data; do not inspect it without")
    print("    permission.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
