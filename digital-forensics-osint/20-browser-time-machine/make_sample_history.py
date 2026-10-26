#!/usr/bin/env python3
"""
Create a safe, fictional Chrome/Edge-style History database for Project 20.

Run:
    py -3 make_sample_history.py
    py -3 make_sample_history.py --output samples/history_sample.sqlite --force

The database contains only fake URLs and timestamps. It is not copied from a
real browser.
"""

from __future__ import annotations

import argparse
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def to_chrome_time(value: datetime) -> int:
    """Chrome/Edge store microseconds since 1601-01-01 UTC."""
    epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return int((value.astimezone(timezone.utc) - epoch).total_seconds() * 1_000_000)


SAMPLE_URLS = [
    ("https://example.com/", "Example Domain"),
    ("https://en.wikipedia.org/wiki/Phishing", "Phishing - Wikipedia"),
    ("https://www.python.org/doc/", "Python Documentation"),
    ("http://neverssl.com/", "NeverSSL - plain HTTP demo"),
    ("https://haveibeenpwned.com/", "Have I Been Pwned"),
    ("https://example.com/security", "Security notes"),
    ("https://www.youtube.com/watch?v=demo123", "Fictional demo video"),
]

# (url index, UTC datetime, transition code)
SAMPLE_VISITS = [
    (0, datetime(2026, 10, 25, 8, 15, tzinfo=timezone.utc), 1),
    (1, datetime(2026, 10, 25, 8, 31, tzinfo=timezone.utc), 0),
    (2, datetime(2026, 10, 25, 9, 5, tzinfo=timezone.utc), 1),
    (3, datetime(2026, 10, 25, 9, 22, tzinfo=timezone.utc), 7),
    (4, datetime(2026, 10, 25, 10, 2, tzinfo=timezone.utc), 0),
    (1, datetime(2026, 10, 25, 14, 45, tzinfo=timezone.utc), 8),
    (5, datetime(2026, 10, 25, 16, 10, tzinfo=timezone.utc), 0),
    (6, datetime(2026, 10, 26, 7, 50, tzinfo=timezone.utc), 0),
    (0, datetime(2026, 10, 26, 8, 20, tzinfo=timezone.utc), 8),
    (2, datetime(2026, 10, 26, 9, 12, tzinfo=timezone.utc), 0),
]


def create_sample_db(path: Path, force: bool = False) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"File exists: {path} (use --force to overwrite)")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()

    connection = sqlite3.connect(path)
    try:
        cursor = connection.cursor()
        cursor.executescript(
            """
            CREATE TABLE urls (
                id INTEGER PRIMARY KEY,
                url LONGVARCHAR,
                title LONGVARCHAR,
                visit_count INTEGER DEFAULT 0,
                typed_count INTEGER DEFAULT 0,
                last_visit_time INTEGER NOT NULL,
                hidden INTEGER DEFAULT 0
            );
            CREATE TABLE visits (
                id INTEGER PRIMARY KEY,
                url INTEGER NOT NULL,
                visit_time INTEGER NOT NULL,
                from_visit INTEGER,
                transition INTEGER DEFAULT 0,
                segment_id INTEGER,
                visit_duration INTEGER DEFAULT 0
            );
            CREATE INDEX visits_time_idx ON visits(visit_time);
            """
        )

        last_visit: dict[int, int] = {}
        counts: dict[int, int] = {}
        for url_index, when, _ in SAMPLE_VISITS:
            stamp = to_chrome_time(when)
            last_visit[url_index] = max(last_visit.get(url_index, 0), stamp)
            counts[url_index] = counts.get(url_index, 0) + 1

        for index, (url, title) in enumerate(SAMPLE_URLS):
            cursor.execute(
                "INSERT INTO urls (id, url, title, visit_count, typed_count, last_visit_time, hidden) "
                "VALUES (?, ?, ?, ?, ?, ?, 0)",
                (
                    index + 1,
                    url,
                    title,
                    counts.get(index, 0),
                    1 if counts.get(index, 0) else 0,
                    last_visit.get(index, to_chrome_time(datetime(2026, 10, 25, tzinfo=timezone.utc))),
                ),
            )

        for visit_index, (url_index, when, transition) in enumerate(SAMPLE_VISITS, start=1):
            cursor.execute(
                "INSERT INTO visits (id, url, visit_time, from_visit, transition, segment_id, visit_duration) "
                "VALUES (?, ?, ?, 0, ?, 0, 0)",
                (visit_index, url_index + 1, to_chrome_time(when), transition),
            )

        connection.commit()
    finally:
        connection.close()

    print(f"[+] Created fictional browser history: {path}")
    print(f"[+] URLs: {len(SAMPLE_URLS)}  Visits: {len(SAMPLE_VISITS)}")
    print("[!] All entries are fake and use reserved example domains.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a fictional browser History database.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "samples" / "history_sample.sqlite",
        help="Output SQLite file.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite an existing file.")
    args = parser.parse_args()

    try:
        create_sample_db(args.output, force=args.force)
    except (FileExistsError, OSError, sqlite3.Error) as error:
        print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
