"""Project 11 - The A/B Test Lab.

Goal: compare two landing-page variants with conversion rates, a two-proportion
z-test, a confidence interval and revenue per user.

Run from the pack root:
    python3 projects/11_ab_test/main.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from statsmodels.stats.proportion import proportions_ztest

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")


def main() -> None:
    print("=" * 70)
    print("PROJECT 11 - THE A/B TEST LAB")
    print("=" * 70)

    # STEP 1 - Load the experiment data.
    df = pd.read_csv(DATA / "ab_test.csv")
    print(f"\nSTEP 1: loaded {len(df)} users")
    print(df.head(3).to_string(index=False))

    # STEP 2 - Check the groups and the outcome column.
    print("\nSTEP 2: experiment quality check")
    print("Missing values:", int(df.isna().sum().sum()))
    print(df.groupby("group").size().to_string())
    print("Conversion values:", sorted(df["converted"].unique()))

    # STEP 3 - Calculate conversion rates.
    # A conversion rate is the number of conversions divided by the group size.
    summary = (
        df.groupby("group")
        .agg(users=("user_id", "count"), conversions=("converted", "sum"), revenue=("revenue", "sum"))
        .assign(
            conversion_rate=lambda x: x["conversions"] / x["users"],
            revenue_per_user=lambda x: x["revenue"] / x["users"],
        )
        .round(4)
    )
    print("\nSTEP 3: group summary")
    print(summary.to_string())

    a = summary.loc["A"]
    b = summary.loc["B"]
    diff = b["conversion_rate"] - a["conversion_rate"]
    relative_lift = diff / a["conversion_rate"]
    print(f"\nDifference (B - A): {diff:.2%}")
    print(f"Relative lift: {relative_lift:.1%}")

    # STEP 4 - Run a two-proportion z-test.
    # Null hypothesis: both variants have the same conversion rate.
    # A small p-value means the observed difference is unlikely under that null.
    count = np.array([b["conversions"], a["conversions"]])
    nobs = np.array([b["users"], a["users"]])
    z_stat, p_value = proportions_ztest(count, nobs, alternative="two-sided")
    print("\nSTEP 4: two-proportion z-test")
    print(f"z-statistic: {z_stat:.3f}")
    print(f"p-value: {p_value:.5f}")

    # STEP 5 - Build a 95% confidence interval for the difference.
    # The standard error measures how much the difference could vary by chance.
    se = np.sqrt(
        a["conversion_rate"] * (1 - a["conversion_rate"]) / a["users"]
        + b["conversion_rate"] * (1 - b["conversion_rate"]) / b["users"]
    )
    ci_low = diff - 1.96 * se
    ci_high = diff + 1.96 * se
    print(f"95% CI for the difference: [{ci_low:.2%}, {ci_high:.2%}]")

    # STEP 6 - Save the statistical results in plain English.
    verdict = "statistically significant" if p_value < 0.05 else "not statistically significant"
    results = [
        "A/B TEST RESULTS",
        "=" * 60,
        f"Group A: {int(a['users']):,} users, {int(a['conversions']):,} conversions, "
        f"conversion rate {a['conversion_rate']:.2%}",
        f"Group B: {int(b['users']):,} users, {int(b['conversions']):,} conversions, "
        f"conversion rate {b['conversion_rate']:.2%}",
        "",
        f"Absolute difference (B - A): {diff:.2%}",
        f"Relative lift: {relative_lift:.1%}",
        f"z-statistic: {z_stat:.3f}",
        f"p-value: {p_value:.5f}",
        f"95% confidence interval: [{ci_low:.2%}, {ci_high:.2%}]",
        "",
        f"At the 5% significance level, the result is {verdict}.",
        f"Revenue per user: A = ${a['revenue_per_user']:.2f}, B = ${b['revenue_per_user']:.2f}",
        "",
        "Rule of thumb: a p-value below 0.05 is often treated as evidence of a real difference,",
        "but always consider sample size, practical impact and how the experiment was run.",
    ]
    (OUT / "ab_test_results.txt").write_text("\n".join(results), encoding="utf-8")
    print("\nSTEP 6: results saved")
    print("\n".join(results))

    # STEP 7 - Plot conversion rates with 95% error bars.
    fig, ax = plt.subplots(figsize=(7, 4.5))
    groups = ["A", "B"]
    rates = [a["conversion_rate"], b["conversion_rate"]]
    errors = [
        1.96 * np.sqrt(a["conversion_rate"] * (1 - a["conversion_rate"]) / a["users"]),
        1.96 * np.sqrt(b["conversion_rate"] * (1 - b["conversion_rate"]) / b["users"]),
    ]
    ax.bar(groups, rates, yerr=errors, capsize=8, color=["#7570b3", "#1b9e77"])
    ax.set_title("Conversion rate by variant (95% error bars)")
    ax.set_ylabel("Conversion rate")
    ax.set_xlabel("Variant")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    for i, rate in enumerate(rates):
        ax.text(i, rate + 0.002, f"{rate:.2%}", ha="center", fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "conversion_rates.png", dpi=140)
    plt.close(fig)

    # STEP 8 - Plot revenue per user.
    fig, ax = plt.subplots(figsize=(7, 4))
    summary["revenue_per_user"].plot(kind="bar", color=["#7570b3", "#1b9e77"], ax=ax)
    ax.set_title("Revenue per user by variant")
    ax.set_ylabel("Revenue per user ($)")
    ax.set_xlabel("Variant")
    plt.xticks(rotation=0)
    fig.tight_layout()
    fig.savefig(OUT / "revenue_per_user.png", dpi=140)
    plt.close(fig)

    print("\nDONE. Check outputs/ab_test_results.txt and the two charts.")


if __name__ == "__main__":
    main()
