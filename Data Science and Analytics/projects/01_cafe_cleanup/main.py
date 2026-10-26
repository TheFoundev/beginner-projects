"""Project 01 - The Messy Cafe Menu.

Goal: turn a deliberately messy cafe order log into a clean, analysis-ready table.

Run from the pack root:
    python3 projects/01_cafe_cleanup/main.py

Every STEP below explains what the code is doing and why.
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
    print("PROJECT 01 - THE MESSY CAFE MENU")
    print("=" * 70)

    # STEP 1 - Load the raw file.
    # read_csv turns the file into a DataFrame: rows are orders and columns are fields.
    raw_path = DATA / "cafe_orders_raw.csv"
    df = pd.read_csv(raw_path)
    rows_before = len(df)
    print(f"\nSTEP 1: loaded {rows_before} rows and {df.shape[1]} columns from {raw_path.name}")
    print(df.head(3).to_string(index=False))

    # STEP 2 - Inspect data quality before changing anything.
    # isna().sum() counts empty cells in each column. duplicated() finds repeated order IDs.
    print("\nSTEP 2: data-quality check")
    print("Missing values per column:")
    print(df.isna().sum().to_string())
    print(f"Duplicate order IDs: {df.duplicated(subset=['order_id']).sum()}")

    missing_before = df.isna().sum()
    fig, ax = plt.subplots(figsize=(7, 4))
    missing_before.plot(kind="bar", color="#d95f02", ax=ax)
    ax.set_title("Missing values before cleaning")
    ax.set_ylabel("Number of empty cells")
    ax.set_xlabel("Column")
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    fig.savefig(OUT / "missing_before.png", dpi=140)
    plt.close(fig)

    # STEP 3 - Standardise text columns.
    # strip() removes accidental spaces; title() makes LATTE, latte and " Latte " all become "Latte".
    df["date"] = pd.to_datetime(
        df["date"].astype(str).str.strip(),
        format="mixed",
        errors="coerce",
    )
    df["item"] = df["item"].astype(str).str.strip().str.title()
    df["customer_type"] = df["customer_type"].astype(str).str.strip().str.title()
    print("\nSTEP 3: standardised item names, customer types and dates")
    print(df["item"].value_counts().to_string())

    # STEP 4 - Rebuild category from the item.
    # The original category column is inconsistent, but the item name is reliable.
    item_to_category = {
        "Latte": "Drink",
        "Cappuccino": "Drink",
        "Muffin": "Food",
        "Sandwich": "Food",
    }
    df["category"] = df["item"].map(item_to_category)
    print("\nSTEP 4: rebuilt category from item name")
    print(df.groupby(["item", "category"]).size().to_string())

    # STEP 5 - Repair numeric columns.
    # to_numeric converts text such as "4.50" to a number and turns bad text into NaN.
    # A quantity of zero or less is invalid for an order, so we mark it missing first.
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df.loc[df["quantity"] <= 0, "quantity"] = np.nan
    quantity_median = df["quantity"].median()
    df["quantity"] = df["quantity"].fillna(quantity_median).astype(int)

    price_text = (
        df["unit_price"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["unit_price"] = pd.to_numeric(price_text, errors="coerce")
    # Fill a missing price with the median price for that same item.
    df["unit_price"] = df.groupby("item")["unit_price"].transform(
        lambda series: series.fillna(series.median())
    )
    df["unit_price"] = df["unit_price"].round(2)
    df["total"] = (df["quantity"] * df["unit_price"]).round(2)
    print(f"\nSTEP 5: numeric repair complete (median quantity used: {quantity_median:g})")
    print(df[["item", "quantity", "unit_price", "total"]].head().to_string(index=False))

    # STEP 6 - Remove duplicate order IDs and impossible dates.
    # keep="first" keeps the first clean record for each order_id.
    duplicates_removed = int(df.duplicated(subset=["order_id"]).sum())
    bad_dates = int(df["date"].isna().sum())
    df = df.dropna(subset=["date"])
    df = df.drop_duplicates(subset=["order_id"], keep="first")
    df = df.sort_values("date").reset_index(drop=True)
    print(f"\nSTEP 6: removed {duplicates_removed} duplicate order rows and {bad_dates} invalid dates")
    print(f"Clean shape: {df.shape[0]} rows x {df.shape[1]} columns")

    # STEP 7 - Save the clean dataset and a short audit report.
    clean_path = DATA / "cafe_orders_clean.csv"
    df.to_csv(clean_path, index=False)

    report_lines = [
        "CAFE CLEANING REPORT",
        "=" * 50,
        f"Rows before cleaning: {rows_before}",
        f"Rows after cleaning: {len(df)}",
        f"Duplicate order rows removed: {duplicates_removed}",
        f"Invalid dates removed: {bad_dates}",
        f"Missing cells before: {int(missing_before.sum())}",
        f"Missing cells after: {int(df.isna().sum().sum())}",
        f"Total revenue: ${df['total'].sum():,.2f}",
        f"Average order value: ${df['total'].mean():,.2f}",
        "",
        "Revenue by item:",
        df.groupby("item")["total"].sum().sort_values(ascending=False).round(2).to_string(),
    ]
    (OUT / "cleaning_report.txt").write_text("\n".join(report_lines), encoding="utf-8")
    print(f"\nSTEP 7: clean data saved to {clean_path}")
    print(f"Audit report saved to {OUT / 'cleaning_report.txt'}")

    # STEP 8 - Visualise the result so the cleaning work is easy to see.
    revenue_by_item = df.groupby("item")["total"].sum().sort_values()
    fig, ax = plt.subplots(figsize=(8, 4))
    revenue_by_item.plot(kind="barh", color="#1b9e77", ax=ax)
    ax.set_title("Revenue by menu item after cleaning")
    ax.set_xlabel("Revenue ($)")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(OUT / "revenue_by_item.png", dpi=140)
    plt.close(fig)

    daily = df.set_index("date")["total"].resample("D").sum()
    fig, ax = plt.subplots(figsize=(10, 4))
    daily.plot(ax=ax, color="#7570b3", linewidth=1.8)
    ax.set_title("Daily cafe revenue after cleaning")
    ax.set_ylabel("Revenue ($)")
    ax.set_xlabel("Date")
    fig.tight_layout()
    fig.savefig(OUT / "daily_revenue.png", dpi=140)
    plt.close(fig)

    print("\nDONE. Check the outputs folder for charts and the cleaning report.")


if __name__ == "__main__":
    main()
