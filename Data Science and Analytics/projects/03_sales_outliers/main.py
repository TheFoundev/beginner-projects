"""Project 03 - The Sales Data Detective.

Goal: find impossible sales values and statistical outliers, repair them, and
compare daily versus weekly patterns.

Run from the pack root:
    python3 projects/03_sales_outliers/main.py
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
    print("PROJECT 03 - THE SALES DATA DETECTIVE")
    print("=" * 70)

    # STEP 1 - Load the raw daily sales table.
    raw = pd.read_csv(DATA / "daily_sales_raw.csv")
    raw["date"] = pd.to_datetime(raw["date"], errors="coerce")
    raw = raw.dropna(subset=["date"]).sort_values(["store", "date"]).reset_index(drop=True)
    print(f"\nSTEP 1: loaded {len(raw)} daily store rows")
    print(raw.head(3).to_string(index=False))

    # STEP 2 - Describe the values and look for impossible numbers.
    print("\nSTEP 2: sales summary before cleaning")
    print(raw["sales"].describe().round(2).to_string())
    negative_count = int((raw["sales"] < 0).sum())
    missing_count = int(raw["sales"].isna().sum())
    print(f"Negative sales rows: {negative_count}")
    print(f"Missing sales rows: {missing_count}")

    # STEP 3 - Mark negative sales as missing.
    # A negative sale is not a valid revenue value, so we cannot average it with real sales.
    df = raw.copy()
    df.loc[df["sales"] < 0, "sales"] = np.nan

    # STEP 4 - Detect outliers with the IQR rule, separately for each store.
    # IQR = Q3 - Q1. Values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR are flagged.
    q1 = df.groupby("store")["sales"].transform(lambda s: s.quantile(0.25))
    q3 = df.groupby("store")["sales"].transform(lambda s: s.quantile(0.75))
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outlier_mask = (df["sales"] < lower) | (df["sales"] > upper)
    outlier_count = int(outlier_mask.sum())
    print(f"\nSTEP 3-4: flagged {negative_count} negative rows and {outlier_count} statistical outliers")
    print("Outlier examples:")
    print(df.loc[outlier_mask, ["date", "store", "sales"]].head(8).to_string(index=False))

    # STEP 5 - Replace flagged values with the median for that store.
    # We use the median because it is not pulled around by extreme values.
    df.loc[outlier_mask, "sales"] = np.nan
    store_median = df.groupby("store")["sales"].transform("median")
    df["sales"] = df["sales"].fillna(store_median).round(2)
    print("\nSTEP 5: replaced invalid/outlier values with each store's median")

    # STEP 6 - Save the clean daily table and a weekly summary.
    clean_path = DATA / "clean_daily_sales.csv"
    df.to_csv(clean_path, index=False)
    df["week"] = df["date"].dt.to_period("W").dt.start_time
    weekly = (
        df.groupby(["week", "store"], as_index=False)["sales"]
        .sum()
        .sort_values(["week", "store"])
    )
    weekly.to_csv(OUT / "weekly_sales.csv", index=False)
    print(f"\nSTEP 6: clean data saved to {clean_path}")
    print(f"Weekly summary saved to {OUT / 'weekly_sales.csv'}")

    # STEP 7 - Compare the before/after distributions.
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    sns.boxplot(data=raw, x="store", y="sales", color="#d95f02", ax=axes[0])
    axes[0].set_title("Before cleaning (note the extreme values)")
    axes[0].set_ylabel("Daily sales ($)")
    sns.boxplot(data=df, x="store", y="sales", color="#1b9e77", ax=axes[1])
    axes[1].set_title("After cleaning")
    axes[1].set_ylabel("Daily sales ($)")
    fig.tight_layout()
    fig.savefig(OUT / "outliers_before_after.png", dpi=140)
    plt.close(fig)

    # STEP 8 - Show the cleaned trend and the weekly totals.
    fig, ax = plt.subplots(figsize=(10, 4))
    for store, group in df.groupby("store"):
        ax.plot(group["date"], group["sales"], label=f"Store {store}", linewidth=1.2)
    ax.set_title("Daily sales after outlier repair")
    ax.set_ylabel("Sales ($)")
    ax.set_xlabel("Date")
    ax.legend(title="Store", ncol=3)
    fig.tight_layout()
    fig.savefig(OUT / "daily_trend.png", dpi=140)
    plt.close(fig)

    weekly_total = weekly.groupby("week", as_index=False)["sales"].sum()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(weekly_total["week"], weekly_total["sales"], marker="o", color="#7570b3")
    ax.set_title("Total weekly sales")
    ax.set_ylabel("Sales ($)")
    ax.set_xlabel("Week starting")
    fig.tight_layout()
    fig.savefig(OUT / "weekly_trend.png", dpi=140)
    plt.close(fig)

    report = [
        "SALES OUTLIER REPORT",
        "=" * 50,
        f"Rows loaded: {len(raw)}",
        f"Negative values repaired: {negative_count}",
        f"IQR outliers repaired: {outlier_count}",
        f"Missing values repaired: {missing_count}",
        f"Clean total sales: ${df['sales'].sum():,.2f}",
        f"Clean daily average: ${df['sales'].mean():,.2f}",
        "",
        "Clean summary by store:",
        df.groupby("store")["sales"].agg(["mean", "min", "max"]).round(2).to_string(),
    ]
    (OUT / "outlier_report.txt").write_text("\n".join(report), encoding="utf-8")
    print("\n" + "\n".join(report))
    print("\nDONE. Check outputs for the before/after chart and reports.")


if __name__ == "__main__":
    main()
