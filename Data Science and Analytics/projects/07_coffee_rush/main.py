"""Project 07 - The Coffee Shop Morning Rush.

Goal: find the busiest hours, compare weekdays and weekends, and measure the
average order value for each sales channel.

Run from the pack root:
    python3 projects/07_coffee_rush/main.py
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
WEEK_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def main() -> None:
    print("=" * 70)
    print("PROJECT 07 - THE COFFEE SHOP MORNING RUSH")
    print("=" * 70)

    # STEP 1 - Load orders and parse the timestamp.
    df = pd.read_csv(DATA / "coffee_orders.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    print(f"\nSTEP 1: loaded {len(df)} coffee orders")
    print(df.head(3).to_string(index=False))

    # STEP 2 - Check quality and basic ranges.
    print("\nSTEP 2: quality check")
    print("Missing values:", int(df.isna().sum().sum()))
    print(df[["quantity", "unit_price"]].describe().round(2).to_string())

    # STEP 3 - Create revenue and time fields.
    # total is the order line value: quantity bought multiplied by the unit price.
    df["total"] = (df["quantity"] * df["unit_price"]).round(2)
    df["hour"] = df["timestamp"].dt.hour
    df["weekday"] = df["timestamp"].dt.day_name()
    df["weekday"] = pd.Categorical(df["weekday"], categories=WEEK_ORDER, ordered=True)
    df["is_weekend"] = df["weekday"].isin(["Saturday", "Sunday"])
    print(f"\nSTEP 3: added revenue and time fields; total revenue = ${df['total'].sum():,.2f}")

    # STEP 4 - Summarise each hour.
    hourly = (
        df.groupby("hour")
        .agg(orders=("order_id", "count"), revenue=("total", "sum"), avg_order_value=("total", "mean"))
        .reset_index()
        .sort_values("hour")
    )
    hourly.to_csv(OUT / "hourly_summary.csv", index=False)
    print("\nSTEP 4: hourly summary")
    print(hourly.to_string(index=False))

    # STEP 5 - Compare channels and weekday/weekend behaviour.
    channel = (
        df.groupby("channel")
        .agg(orders=("order_id", "count"), revenue=("total", "sum"), avg_order_value=("total", "mean"))
        .round(2)
    )
    channel.to_csv(OUT / "channel_summary.csv")
    day_type = (
        df.groupby("is_weekend")
        .agg(orders=("order_id", "count"), revenue=("total", "sum"), avg_order_value=("total", "mean"))
        .round(2)
    )
    print("\nSTEP 5: channel summary")
    print(channel.to_string())
    print("\nWeekday vs weekend:")
    print(day_type.to_string())

    # STEP 6 - Build an hour-by-weekday revenue table for a heatmap.
    heat = df.pivot_table(
        index="weekday", columns="hour", values="total", aggfunc="sum", fill_value=0, observed=True
    ).reindex(WEEK_ORDER)
    heat.to_csv(OUT / "hour_weekday_heatmap.csv")

    # STEP 7 - Plot hourly revenue.
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(hourly["hour"], hourly["revenue"], marker="o", color="#1b9e77", linewidth=2)
    ax.set_title("Revenue by hour of day")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Revenue ($)")
    ax.set_xticks(hourly["hour"])
    fig.tight_layout()
    fig.savefig(OUT / "hourly_revenue.png", dpi=140)
    plt.close(fig)

    # STEP 8 - Plot the hour/weekday heatmap.
    fig, ax = plt.subplots(figsize=(10, 4.5))
    sns.heatmap(heat, cmap="YlGnBu", linewidths=0.4, ax=ax)
    ax.set_title("Revenue heatmap: weekday vs hour")
    ax.set_xlabel("Hour")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(OUT / "hour_weekday_heatmap.png", dpi=140)
    plt.close(fig)

    # STEP 9 - Plot average order value by channel.
    fig, ax = plt.subplots(figsize=(6, 4))
    channel["avg_order_value"].plot(kind="bar", color="#7570b3", ax=ax)
    ax.set_title("Average order value by channel")
    ax.set_ylabel("Average order value ($)")
    ax.set_xlabel("")
    plt.xticks(rotation=0)
    fig.tight_layout()
    fig.savefig(OUT / "channel_aov.png", dpi=140)
    plt.close(fig)

    # STEP 10 - Write the key findings.
    peak_hour = hourly.sort_values("revenue", ascending=False).iloc[0]
    best_channel = channel["avg_order_value"].idxmax()
    insights = [
        "COFFEE SHOP INSIGHTS",
        "=" * 50,
        f"Total revenue: ${df['total'].sum():,.2f}",
        f"Total orders: {len(df):,}",
        f"Overall average order value: ${df['total'].mean():.2f}",
        f"Peak revenue hour: {int(peak_hour['hour'])}:00 (${peak_hour['revenue']:,.2f})",
        f"Channel with highest average order value: {best_channel} (${channel.loc[best_channel, 'avg_order_value']:.2f})",
        "",
        "Hourly summary:",
        hourly.to_string(index=False),
    ]
    (OUT / "insights.txt").write_text("\n".join(insights), encoding="utf-8")
    print("\n" + "\n".join(insights))
    print("\nDONE. Check outputs for hourly, heatmap and channel charts.")


if __name__ == "__main__":
    main()
