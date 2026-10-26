"""Project 12 - The Study Break Experiment.

Goal: compare exam scores for students who took a short break versus students
who studied straight through, using an independent t-test and an effect size.

Run from the pack root:
    python3 projects/12_study_break/main.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")


def main() -> None:
    print("=" * 70)
    print("PROJECT 12 - THE STUDY BREAK EXPERIMENT")
    print("=" * 70)

    # STEP 1 - Load the experiment data.
    df = pd.read_csv(DATA / "study_break.csv")
    print(f"\nSTEP 1: loaded {len(df)} students")
    print(df.head(3).to_string(index=False))

    # STEP 2 - Check group sizes and missing values.
    print("\nSTEP 2: experiment quality check")
    print("Missing values:", int(df.isna().sum().sum()))
    print(df.groupby("group")["score"].agg(["count", "mean", "std"]).round(2).to_string())

    # STEP 3 - Separate the two groups.
    break_scores = df.loc[df["group"] == "break", "score"]
    no_break_scores = df.loc[df["group"] == "no_break", "score"]
    n1, n2 = len(break_scores), len(no_break_scores)
    mean1, mean2 = break_scores.mean(), no_break_scores.mean()
    sd1, sd2 = break_scores.std(ddof=1), no_break_scores.std(ddof=1)
    print("\nSTEP 3: group separation")
    print(f"Break group: n={n1}, mean={mean1:.1f}, sd={sd1:.1f}")
    print(f"No-break group: n={n2}, mean={mean2:.1f}, sd={sd2:.1f}")

    # STEP 4 - Run an independent-samples t-test.
    # H0: the two groups have the same average score.
    # Welch's version (equal_var=False) does not assume equal variances.
    t_stat, p_value = stats.ttest_ind(break_scores, no_break_scores, equal_var=False)
    print("\nSTEP 4: independent t-test (Welch)")
    print(f"t-statistic: {t_stat:.3f}")
    print(f"p-value: {p_value:.5f}")

    # STEP 5 - Estimate the size of the difference.
    # Cohen's d: small ~0.2, medium ~0.5, large ~0.8.
    pooled_sd = np.sqrt(((n1 - 1) * sd1**2 + (n2 - 1) * sd2**2) / (n1 + n2 - 2))
    cohens_d = (mean1 - mean2) / pooled_sd
    print(f"Cohen's d: {cohens_d:.2f}")

    # STEP 6 - Calculate a 95% confidence interval for the mean difference.
    se = np.sqrt(sd1**2 / n1 + sd2**2 / n2)
    welch_df = (sd1**2 / n1 + sd2**2 / n2) ** 2 / (
        (sd1**2 / n1) ** 2 / (n1 - 1) + (sd2**2 / n2) ** 2 / (n2 - 1)
    )
    t_critical = stats.t.ppf(0.975, welch_df)
    diff = mean1 - mean2
    ci_low, ci_high = diff - t_critical * se, diff + t_critical * se
    print(f"95% CI for mean difference: [{ci_low:.2f}, {ci_high:.2f}]")

    # STEP 7 - Save the results.
    verdict = "statistically significant" if p_value < 0.05 else "not statistically significant"
    results = [
        "STUDY BREAK EXPERIMENT RESULTS",
        "=" * 60,
        f"Break group: n={n1}, mean={mean1:.1f}, sd={sd1:.1f}",
        f"No-break group: n={n2}, mean={mean2:.1f}, sd={sd2:.1f}",
        f"Mean difference: {diff:.2f} points",
        f"t-statistic: {t_stat:.3f}",
        f"p-value: {p_value:.5f}",
        f"Cohen's d: {cohens_d:.2f}",
        f"95% CI for difference: [{ci_low:.2f}, {ci_high:.2f}]",
        "",
        f"At the 5% level, the difference is {verdict}.",
        "A p-value is not the same as the size of the effect; report both.",
    ]
    (OUT / "results.txt").write_text("\n".join(results), encoding="utf-8")
    print("\nSTEP 7: results saved")
    print("\n".join(results))

    # STEP 8 - Plot the two score distributions.
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.boxplot(data=df, x="group", y="score", palette="Set2", width=0.5, ax=ax)
    sns.stripplot(data=df, x="group", y="score", color="black", alpha=0.45, jitter=0.12, ax=ax)
    ax.set_title("Exam scores by study-break group")
    ax.set_xlabel("")
    ax.set_ylabel("Exam score")
    fig.tight_layout()
    fig.savefig(OUT / "study_break_boxplot.png", dpi=140)
    plt.close(fig)

    # STEP 9 - Plot group means with 95% confidence intervals.
    fig, ax = plt.subplots(figsize=(7, 4))
    means = [mean1, mean2]
    errors = [1.96 * sd1 / np.sqrt(n1), 1.96 * sd2 / np.sqrt(n2)]
    ax.bar(["break", "no_break"], means, yerr=errors, capsize=8, color=["#1b9e77", "#d95f02"])
    ax.set_title("Average exam score with 95% error bars")
    ax.set_ylabel("Average score")
    ax.set_xlabel("")
    for i, mean in enumerate(means):
        ax.text(i, mean + 0.8, f"{mean:.1f}", ha="center", fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "group_means.png", dpi=140)
    plt.close(fig)

    print("\nDONE. Check outputs/results.txt and the two charts.")


if __name__ == "__main__":
    main()
