"""Project 13 - The Customer Satisfaction Survey.

Goal: compare satisfaction across customer segments and test whether the
recommendation decision is associated with the segment.

Run from the pack root:
    python3 projects/13_satisfaction_survey/main.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import chi2_contingency

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")


def main() -> None:
    print("=" * 70)
    print("PROJECT 13 - THE CUSTOMER SATISFACTION SURVEY")
    print("=" * 70)

    # STEP 1 - Load the survey.
    df = pd.read_csv(DATA / "satisfaction_survey.csv")
    print(f"\nSTEP 1: loaded {len(df)} respondents")
    print(df.head(3).to_string(index=False))

    # STEP 2 - Check the values and group sizes.
    print("\nSTEP 2: quality check")
    print("Missing values:", int(df.isna().sum().sum()))
    print(df.groupby("segment").size().to_string())
    print("Satisfaction range:", df["satisfaction"].min(), "to", df["satisfaction"].max())

    # STEP 3 - Summarise satisfaction by segment.
    # The 95% margin of error is 1.96 * standard_error.
    summary = (
        df.groupby("segment")
        .agg(
            respondents=("respondent_id", "count"),
            avg_satisfaction=("satisfaction", "mean"),
            sd_satisfaction=("satisfaction", "std"),
            recommend_rate=("would_recommend", "mean"),
        )
        .assign(
            margin_of_error=lambda x: 1.96 * x["sd_satisfaction"] / np.sqrt(x["respondents"])
        )
        .round(2)
    )
    summary.to_csv(OUT / "segment_summary.csv")
    print("\nSTEP 3: segment summary")
    print(summary.to_string())

    # STEP 4 - Build a contingency table for the chi-square test.
    # Rows are segments; columns are recommend (0/1).
    table = pd.crosstab(df["segment"], df["would_recommend"])
    print("\nSTEP 4: contingency table (0 = no, 1 = yes)")
    print(table.to_string())

    # STEP 5 - Run the chi-square test.
    # H0: recommendation is independent of segment.
    # A small p-value suggests the recommendation rate differs by segment.
    chi2, p_value, dof, expected = chi2_contingency(table)
    n = table.values.sum()
    cramers_v = np.sqrt(chi2 / (n * (min(table.shape) - 1)))
    print("\nSTEP 5: chi-square test")
    print(f"chi-square: {chi2:.3f}")
    print(f"degrees of freedom: {dof}")
    print(f"p-value: {p_value:.5f}")
    print(f"Cramer's V: {cramers_v:.2f}")

    # STEP 6 - Save the results.
    verdict = "a statistically significant association" if p_value < 0.05 else "no statistically significant association"
    results = [
        "SATISFACTION SURVEY RESULTS",
        "=" * 60,
        f"Respondents: {len(df)}",
        f"Overall average satisfaction: {df['satisfaction'].mean():.2f} / 5",
        f"Overall recommendation rate: {df['would_recommend'].mean():.2%}",
        "",
        "Average satisfaction by segment:",
        summary.to_string(),
        "",
        f"Chi-square: {chi2:.3f} (df={dof}), p-value={p_value:.5f}",
        f"Cramer's V: {cramers_v:.2f}",
        f"At the 5% level, there is {verdict} between segment and recommendation.",
        "",
        "Expected counts (used by the test):",
        pd.DataFrame(expected, index=table.index, columns=table.columns).round(1).to_string(),
    ]
    (OUT / "results.txt").write_text("\n".join(results), encoding="utf-8")
    print("\nSTEP 6: results saved")
    print("\n".join(results))

    # STEP 7 - Plot average satisfaction with error bars.
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(
        summary.index,
        summary["avg_satisfaction"],
        yerr=summary["margin_of_error"],
        capsize=8,
        color=["#1b9e77", "#7570b3", "#d95f02"],
    )
    ax.set_title("Average satisfaction by segment (95% error bars)")
    ax.set_ylabel("Average satisfaction (1-5)")
    ax.set_xlabel("")
    ax.set_ylim(0, 5.2)
    for i, value in enumerate(summary["avg_satisfaction"]):
        ax.text(i, value + 0.12, f"{value:.2f}", ha="center", fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "satisfaction_by_segment.png", dpi=140)
    plt.close(fig)

    # STEP 8 - Plot recommendation rate by segment.
    rec_share = pd.crosstab(df["segment"], df["would_recommend"], normalize="index")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    rec_share.plot(kind="bar", stacked=True, color=["#d95f02", "#1b9e77"], ax=ax)
    ax.set_title("Recommendation rate by segment")
    ax.set_ylabel("Share of respondents")
    ax.set_xlabel("")
    ax.legend(["No", "Yes"], title="Recommend?")
    plt.xticks(rotation=0)
    fig.tight_layout()
    fig.savefig(OUT / "recommend_by_segment.png", dpi=140)
    plt.close(fig)

    print("\nDONE. Check outputs/results.txt and the two charts.")


if __name__ == "__main__":
    main()
