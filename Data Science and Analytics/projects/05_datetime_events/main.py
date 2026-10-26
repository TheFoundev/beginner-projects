"""Project 05 - The Date & Time Fixer.

Goal: parse timestamps written in three different formats, remove duplicate
events, and build hourly and daily activity summaries.

Run from the pack root:
    python3 projects/05_datetime_events/main.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")


def main() -> None:
    print("=" * 70)
    print("PROJECT 05 - THE DATE & TIME FIXER")
    print("=" * 70)

    # STEP 1 - Load the event log.
    raw = pd.read_csv(DATA / "events_raw.csv")
    print(f"\nSTEP 1: loaded {len(raw)} event rows")
    print(raw.head(4).to_string(index=False))

    # STEP 2 - See the mixed timestamp formats.
    print("\nSTEP 2: example raw timestamps")
    print(raw["timestamp"].head(8).tolist())

    # STEP 3 - Parse every timestamp into a real datetime value.
    # format="mixed" tells pandas that different rows may use different formats.
    # errors="coerce" turns anything unparseable into NaT (missing time).
    df = raw.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed", errors="coerce")
    bad_timestamps = int(df["timestamp"].isna().sum())
    print(f"\nSTEP 3: parsed timestamps; unparseable rows: {bad_timestamps}")

    # STEP 4 - Remove duplicate event IDs and invalid timestamps.
    duplicates = int(df.duplicated(subset=["event_id"]).sum())
    df = df.dropna(subset=["timestamp"])
    df = df.drop_duplicates(subset=["event_id"], keep="first").copy()
    df = df.sort_values("timestamp").reset_index(drop=True)
    print(f"\nSTEP 4: removed {duplicates} duplicate events and {bad_timestamps} invalid timestamps")

    # STEP 5 - Create useful time parts.
    # dt accessors pull the date, hour, weekday name and month out of each timestamp.
    df["date"] = df["timestamp"].dt.date
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.day_name()
    df["month"] = df["timestamp"].dt.month_name()

    # STEP 6 - Fill missing durations with the median for the same event type.
    df["duration_min"] = pd.to_numeric(df["duration_min"], errors="coerce")
    duration_missing = int(df["duration_min"].isna().sum())
    df["duration_min"] = df.groupby("event_type")["duration_min"].transform(
        lambda series: series.fillna(series.median())
    )
    print(f"\nSTEP 5-6: added date/hour/weekday fields and filled {duration_missing} missing durations")

    # STEP 7 - Save the clean event table.
    clean_path = DATA / "clean_events.csv"
    df.to_csv(clean_path, index=False)
    print(f"\nSTEP 7: clean events saved to {clean_path}")

    # STEP 8 - Aggregate by hour and by day.
    hourly = df.groupby("hour").size().rename("events").reset_index()
    daily = (
        df.set_index("timestamp")
        .resample("D")
        .agg(events=("event_id", "count"), active_users=("user_id", "nunique"))
        .reset_index()
    )
    hourly.to_csv(OUT / "hourly_activity.csv", index=False)
    daily.to_csv(OUT / "daily_activity.csv", index=False)

    # STEP 9 - Plot hourly activity and daily active users.
    fig, ax = plt.subplots(figsize=(9, 4))
    sns.barplot(data=hourly, x="hour", y="events", color="#1b9e77", ax=ax)
    ax.set_title("Activity by hour of day")
    ax.set_xlabel("Hour (24-hour clock)")
    ax.set_ylabel("Number of events")
    fig.tight_layout()
    fig.savefig(OUT / "hourly_activity.png", dpi=140)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(daily["timestamp"], daily["active_users"], marker="o", color="#7570b3")
    ax.set_title("Daily active users")
    ax.set_xlabel("Date")
    ax.set_ylabel("Unique users")
    fig.tight_layout()
    fig.savefig(OUT / "daily_active_users.png", dpi=140)
    plt.close(fig)

    report = [
        "EVENT TIME CLEANING REPORT",
        "=" * 50,
        f"Rows before cleaning: {len(raw)}",
        f"Rows after cleaning: {len(df)}",
        f"Duplicate events removed: {duplicates}",
        f"Invalid timestamps removed: {bad_timestamps}",
        f"Missing durations filled: {duration_missing}",
        f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}",
        "",
        "Events by type:",
        df["event_type"].value_counts().to_string(),
        "",
        "Busiest hour:",
        hourly.sort_values("events", ascending=False).head(3).to_string(index=False),
    ]
    (OUT / "time_cleaning_report.txt").write_text("\n".join(report), encoding="utf-8")
    print("\n" + "\n".join(report))
    print("\nDONE. Check outputs/hourly_activity.png and daily_active_users.png.")


if __name__ == "__main__":
    main()
