"""Project 09 - The City Weather Story.

Goal: turn one year of daily weather into a monthly story about temperature,
rain and extreme days.

Run from the pack root:
    python3 projects/09_weather_story/main.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")


def main() -> None:
    print("=" * 70)
    print("PROJECT 09 - THE CITY WEATHER STORY")
    print("=" * 70)

    # STEP 1 - Load the daily weather table.
    df = pd.read_csv(DATA / "weather_daily.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    print(f"\nSTEP 1: loaded {len(df)} days of weather")
    print(df.head(3).to_string(index=False))

    # STEP 2 - Check the ranges before summarising.
    print("\nSTEP 2: weather-quality check")
    print("Missing values:", int(df.isna().sum().sum()))
    print(df[["temp_max_c", "temp_min_c", "rainfall_mm", "humidity_percent"]].describe().round(1).to_string())

    # STEP 3 - Add month labels.
    # to_period("M") groups dates by calendar month; strftime makes nicer chart labels.
    df["month"] = df["date"].dt.to_period("M")
    df["month_label"] = df["date"].dt.strftime("%b")
    print("\nSTEP 3: grouped dates into calendar months")

    # STEP 4 - Build the monthly summary.
    monthly = (
        df.groupby(["month", "month_label"], as_index=False)
        .agg(
            avg_max_c=("temp_max_c", "mean"),
            avg_min_c=("temp_min_c", "mean"),
            total_rain_mm=("rainfall_mm", "sum"),
            rainy_days=("rainfall_mm", lambda s: int((s > 0).sum())),
            avg_humidity=("humidity_percent", "mean"),
        )
        .round(1)
    )
    monthly.to_csv(OUT / "monthly_weather.csv", index=False)
    print("\nSTEP 4: monthly weather summary")
    print(monthly.to_string(index=False))

    # STEP 5 - Find extreme days.
    hottest = df.loc[df["temp_max_c"].idxmax()]
    coldest = df.loc[df["temp_min_c"].idxmin()]
    wettest = df.loc[df["rainfall_mm"].idxmax()]
    print("\nSTEP 5: extreme days")
    print(f"Hottest: {hottest['date'].date()} at {hottest['temp_max_c']} C")
    print(f"Coldest: {coldest['date'].date()} at {coldest['temp_min_c']} C")
    print(f"Wettest: {wettest['date'].date()} with {wettest['rainfall_mm']} mm")

    # STEP 6 - Plot monthly temperatures.
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(monthly["month_label"], monthly["avg_max_c"], marker="o", label="Average high", color="#d95f02")
    ax.plot(monthly["month_label"], monthly["avg_min_c"], marker="o", label="Average low", color="#1b9e77")
    ax.set_title("Average monthly temperature")
    ax.set_xlabel("")
    ax.set_ylabel("Temperature (C)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "monthly_temperature.png", dpi=140)
    plt.close(fig)

    # STEP 7 - Plot monthly rainfall.
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(monthly["month_label"], monthly["total_rain_mm"], color="#7570b3")
    ax.set_title("Total rainfall by month")
    ax.set_xlabel("")
    ax.set_ylabel("Rainfall (mm)")
    fig.tight_layout()
    fig.savefig(OUT / "monthly_rainfall.png", dpi=140)
    plt.close(fig)

    # STEP 8 - Plot the distribution of daily high temperatures.
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df["temp_max_c"], bins=24, kde=True, color="#e7298a", ax=ax)
    ax.set_title("Distribution of daily high temperatures")
    ax.set_xlabel("Daily high (C)")
    ax.set_ylabel("Days")
    fig.tight_layout()
    fig.savefig(OUT / "temperature_distribution.png", dpi=140)
    plt.close(fig)

    # STEP 9 - Write the weather story.
    insights = [
        "WEATHER STORY",
        "=" * 50,
        f"Days analysed: {len(df)}",
        f"Warmest month on average: {monthly.loc[monthly['avg_max_c'].idxmax(), 'month_label']}",
        f"Wettest month: {monthly.loc[monthly['total_rain_mm'].idxmax(), 'month_label']}",
        f"Hottest day: {hottest['date'].date()} ({hottest['temp_max_c']} C)",
        f"Coldest day: {coldest['date'].date()} ({coldest['temp_min_c']} C)",
        f"Rainy days: {int((df['rainfall_mm'] > 0).sum())} of {len(df)}",
        f"Total rainfall: {df['rainfall_mm'].sum():,.1f} mm",
        "",
        "Monthly summary:",
        monthly.to_string(index=False),
    ]
    (OUT / "insights.txt").write_text("\n".join(insights), encoding="utf-8")
    print("\n" + "\n".join(insights))
    print("\nDONE. Check outputs for temperature, rainfall and distribution charts.")


if __name__ == "__main__":
    main()
