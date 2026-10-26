"""Project 15 - The Delivery Time ANOVA.

Goal: compare delivery times across three warehouses with a one-way ANOVA and
Tukey post-hoc test.

Run from the pack root:
    python3 projects/15_delivery_anova/main.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")


def main() -> None:
    print("=" * 70)
    print("PROJECT 15 - THE DELIVERY TIME ANOVA")
    print("=" * 70)

    # STEP 1 - Load the delivery data.
    df = pd.read_csv(DATA / "delivery_times.csv")
    print(f"\nSTEP 1: loaded {len(df)} orders")
    print(df.head(3).to_string(index=False))

    # STEP 2 - Check groups and missing values.
    print("\nSTEP 2: quality check")
    print("Missing values:", int(df.isna().sum().sum()))
    print(df.groupby("warehouse")["delivery_days"].agg(["count", "mean", "std"]).round(2).to_string())

    # STEP 3 - Summarise each warehouse.
    summary = (
        df.groupby("warehouse")
        .agg(
            orders=("order_id", "count"),
            avg_delivery_days=("delivery_days", "mean"),
            sd_delivery_days=("delivery_days", "std"),
            avg_distance_km=("distance_km", "mean"),
        )
        .round(2)
    )
    summary.to_csv(OUT / "warehouse_summary.csv")
    print("\nSTEP 3: warehouse summary")
    print(summary.to_string())

    # STEP 4 - Run a one-way ANOVA.
    # H0: all three warehouses have the same average delivery time.
    groups = [group["delivery_days"].values for _, group in df.groupby("warehouse")]
    f_stat, p_value = f_oneway(*groups)
    print("\nSTEP 4: one-way ANOVA")
    print(f"F-statistic: {f_stat:.3f}")
    print(f"p-value: {p_value:.5f}")

    # STEP 5 - Calculate eta squared, a simple effect-size measure.
    # It is the share of total variation explained by warehouse differences.
    grand_mean = df["delivery_days"].mean()
    ss_between = sum(len(g) * (g.mean() - grand_mean) ** 2 for g in groups)
    ss_within = sum(((g - g.mean()) ** 2).sum() for g in groups)
    eta_squared = ss_between / (ss_between + ss_within)
    print(f"Eta squared: {eta_squared:.3f}")

    # STEP 6 - Run Tukey's HSD to see which pairs differ.
    # This controls the family-wise error rate when making several comparisons.
    tukey = pairwise_tukeyhsd(endog=df["delivery_days"], groups=df["warehouse"], alpha=0.05)
    tukey_table = pd.DataFrame(
        tukey.summary().data[1:],
        columns=tukey.summary().data[0],
    )
    tukey_table.to_csv(OUT / "tukey_results.csv", index=False)
    print("\nSTEP 6: Tukey HSD")
    print(tukey_table.to_string(index=False))

    # STEP 7 - Save the results.
    verdict = "statistically significant" if p_value < 0.05 else "not statistically significant"
    results = [
        "DELIVERY TIME ANOVA RESULTS",
        "=" * 60,
        f"Orders: {len(df)}",
        f"F-statistic: {f_stat:.3f}",
        f"p-value: {p_value:.5f}",
        f"Eta squared: {eta_squared:.3f}",
        f"At the 5% level, the warehouse difference is {verdict}.",
        "",
        "Warehouse summary:",
        summary.to_string(),
        "",
        "Tukey HSD pairwise comparisons:",
        tukey_table.to_string(index=False),
        "",
        "Tukey column guide: meandiff = difference in means;",
        "p-adj = adjusted p-value; reject = True means the pair differs significantly.",
    ]
    (OUT / "anova_results.txt").write_text("\n".join(results), encoding="utf-8")
    print("\nSTEP 7: results saved")
    print("\n".join(results))

    # STEP 8 - Plot the delivery-time distributions.
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.boxplot(data=df, x="warehouse", y="delivery_days", palette="Set2", width=0.5, ax=ax)
    sns.stripplot(data=df, x="warehouse", y="delivery_days", color="black", alpha=0.4, jitter=0.12, ax=ax)
    ax.set_title("Delivery time by warehouse")
    ax.set_xlabel("Warehouse")
    ax.set_ylabel("Delivery days")
    fig.tight_layout()
    fig.savefig(OUT / "delivery_boxplot.png", dpi=140)
    plt.close(fig)

    # STEP 9 - Plot group means with 95% error bars.
    fig, ax = plt.subplots(figsize=(7, 4))
    errors = 1.96 * summary["sd_delivery_days"] / np.sqrt(summary["orders"])
    ax.bar(summary.index, summary["avg_delivery_days"], yerr=errors, capsize=8,
           color=["#1b9e77", "#7570b3", "#d95f02"])
    ax.set_title("Average delivery time with 95% error bars")
    ax.set_ylabel("Average delivery days")
    ax.set_xlabel("Warehouse")
    for i, value in enumerate(summary["avg_delivery_days"]):
        ax.text(i, value + 0.08, f"{value:.2f}", ha="center", fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "warehouse_means.png", dpi=140)
    plt.close(fig)

    print("\nDONE. Check outputs/anova_results.txt and the two charts.")


if __name__ == "__main__":
    main()
