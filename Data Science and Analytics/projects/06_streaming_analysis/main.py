"""Project 06 - The Streaming Showdown.

Goal: compare genres and shows by watch time and completion rate, then show
how viewing changes across the week.

Run from the pack root:
    python3 projects/06_streaming_analysis/main.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")
WEEK_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def main() -> None:
    print("=" * 70)
    print("PROJECT 06 - THE STREAMING SHOWDOWN")
    print("=" * 70)

    # STEP 1 - Load the viewing log.
    df = pd.read_csv(DATA / "streaming_viewing.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    print(f"\nSTEP 1: loaded {len(df)} viewing records")
    print(df.head(3).to_string(index=False))

    # STEP 2 - Check the basic shape and quality.
    # This is a clean dataset, but we still verify types, missing values and ranges.
    print("\nSTEP 2: quality check")
    print(df.dtypes.to_string())
    print("Missing values:", int(df.isna().sum().sum()))
    print(df[["minutes_watched", "completed"]].describe().round(2).to_string())

    # STEP 3 - Add a weekday label.
    # day_name() turns a date into "Monday", "Tuesday", etc.
    df["weekday"] = df["date"].dt.day_name()
    df["weekday"] = pd.Categorical(df["weekday"], categories=WEEK_ORDER, ordered=True)

    # STEP 4 - Summarise each genre.
    # total minutes shows popularity; mean minutes shows depth of engagement;
    # completion_rate shows how often viewers finished what they started.
    genre_summary = (
        df.groupby("genre")
        .agg(
            total_minutes=("minutes_watched", "sum"),
            avg_minutes=("minutes_watched", "mean"),
            completion_rate=("completed", "mean"),
            views=("user_id", "count"),
        )
        .sort_values("total_minutes", ascending=False)
        .round(2)
    )
    genre_summary.to_csv(OUT / "genre_summary.csv")
    print("\nSTEP 4: genre summary")
    print(genre_summary.to_string())

    # STEP 5 - Summarise each show.
    show_summary = (
        df.groupby(["genre", "show"])
        .agg(total_minutes=("minutes_watched", "sum"), completion_rate=("completed", "mean"))
        .sort_values("total_minutes", ascending=False)
        .round(2)
    )
    show_summary.to_csv(OUT / "show_summary.csv")
    print("\nSTEP 5: top 5 shows by total watch time")
    print(show_summary.head(5).to_string())

    # STEP 6 - Summarise viewing by weekday.
    weekday_summary = (
        df.groupby("weekday", observed=True)
        .agg(total_minutes=("minutes_watched", "sum"), views=("user_id", "count"))
        .reset_index()
    )
    weekday_summary.to_csv(OUT / "weekday_summary.csv", index=False)
    print("\nSTEP 6: weekday viewing")
    print(weekday_summary.to_string(index=False))

    # STEP 7 - Chart the genre totals.
    fig, ax = plt.subplots(figsize=(8, 4))
    genre_summary["total_minutes"].sort_values().plot(kind="barh", color="#1b9e77", ax=ax)
    ax.set_title("Total watch time by genre")
    ax.set_xlabel("Minutes watched")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(OUT / "genre_watch_time.png", dpi=140)
    plt.close(fig)

    # STEP 8 - Chart completion rates.
    fig, ax = plt.subplots(figsize=(8, 4))
    genre_summary["completion_rate"].sort_values().plot(kind="barh", color="#7570b3", ax=ax)
    ax.set_title("Completion rate by genre")
    ax.set_xlabel("Share of views completed")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    fig.tight_layout()
    fig.savefig(OUT / "genre_completion.png", dpi=140)
    plt.close(fig)

    # STEP 9 - Chart the weekday pattern.
    fig, ax = plt.subplots(figsize=(9, 4))
    sns.barplot(data=weekday_summary, x="weekday", y="total_minutes", color="#d95f02", ax=ax)
    ax.set_title("Watch time by day of week")
    ax.set_xlabel("")
    ax.set_ylabel("Minutes watched")
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    fig.savefig(OUT / "weekday_viewing.png", dpi=140)
    plt.close(fig)

    # STEP 10 - Write a plain-English insight file.
    top_genre = genre_summary.index[0]
    best_completion = genre_summary["completion_rate"].idxmax()
    busiest_day = weekday_summary.sort_values("total_minutes", ascending=False).iloc[0]
    insights = [
        "STREAMING INSIGHTS",
        "=" * 50,
        f"Most-watched genre: {top_genre} ({genre_summary.loc[top_genre, 'total_minutes']:,.0f} minutes)",
        f"Highest completion rate: {best_completion} ({genre_summary.loc[best_completion, 'completion_rate']:.1%})",
        f"Busiest weekday: {busiest_day['weekday']} ({busiest_day['total_minutes']:,.0f} minutes)",
        f"Total watch time: {df['minutes_watched'].sum():,.0f} minutes",
        "",
        "Full genre summary:",
        genre_summary.to_string(),
    ]
    (OUT / "insights.txt").write_text("\n".join(insights), encoding="utf-8")
    print("\n" + "\n".join(insights))
    print("\nDONE. Check outputs for three charts and the insight summary.")


if __name__ == "__main__":
    main()
