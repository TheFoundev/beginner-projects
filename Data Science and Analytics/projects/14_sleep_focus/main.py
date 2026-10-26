"""Project 14 - The Sleep & Focus Correlation.

Goal: measure whether sleep, caffeine and screen time move together with focus,
using Pearson and Spearman correlation.

Run from the pack root:
    python3 projects/14_sleep_focus/main.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import pearsonr, spearmanr

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")


def main() -> None:
    print("=" * 70)
    print("PROJECT 14 - THE SLEEP & FOCUS CORRELATION")
    print("=" * 70)

    # STEP 1 - Load the student data.
    df = pd.read_csv(DATA / "sleep_focus.csv")
    print(f"\nSTEP 1: loaded {len(df)} students")
    print(df.head(3).to_string(index=False))

    # STEP 2 - Check the ranges and missing values.
    print("\nSTEP 2: quality check")
    print("Missing values:", int(df.isna().sum().sum()))
    print(df.describe().round(2).to_string())

    # STEP 3 - Calculate the full correlation matrix.
    # Pearson measures a straight-line relationship; values run from -1 to +1.
    corr = df.drop(columns=["student_id"]).corr(method="pearson").round(2)
    corr.to_csv(OUT / "correlation_matrix.csv")
    print("\nSTEP 3: Pearson correlation matrix")
    print(corr.to_string())

    # STEP 4 - Test the main relationship: sleep hours vs focus score.
    # pearsonr returns r and a p-value for the null hypothesis r = 0.
    r_value, p_value = pearsonr(df["sleep_hours"], df["focus_score"])
    # Spearman works on ranks and is less sensitive to extreme values.
    rho_value, rho_p = spearmanr(df["sleep_hours"], df["focus_score"])
    print("\nSTEP 4: sleep vs focus")
    print(f"Pearson r = {r_value:.3f}, p = {p_value:.5f}")
    print(f"Spearman rho = {rho_value:.3f}, p = {rho_p:.5f}")

    # STEP 5 - Check the other relationships too.
    extra = []
    for column in ["caffeine_mg", "screen_time_hours"]:
        r, p = pearsonr(df[column], df["focus_score"])
        extra.append((column, r, p))
    print("\nSTEP 5: other relationships with focus")
    for column, r, p in extra:
        print(f"{column}: r = {r:.3f}, p = {p:.5f}")

    # STEP 6 - Save the results in plain English.
    strength = "strong" if abs(r_value) >= 0.7 else "moderate" if abs(r_value) >= 0.4 else "weak"
    direction = "positive" if r_value > 0 else "negative"
    results = [
        "SLEEP AND FOCUS RESULTS",
        "=" * 60,
        f"Students analysed: {len(df)}",
        f"Sleep vs focus: Pearson r = {r_value:.3f} (p = {p_value:.5f})",
        f"Sleep vs focus: Spearman rho = {rho_value:.3f} (p = {rho_p:.5f})",
        f"Interpretation: a {strength} {direction} correlation.",
        "",
        "Other relationships with focus:",
    ]
    for column, r, p in extra:
        results.append(f"- {column}: r = {r:.3f}, p = {p:.5f}")
    results += [
        "",
        "Important: correlation does not prove causation.",
        "A third factor (for example, stress or workload) could affect both variables.",
    ]
    (OUT / "results.txt").write_text("\n".join(results), encoding="utf-8")
    print("\nSTEP 6: results saved")
    print("\n".join(results))

    # STEP 7 - Plot sleep against focus with a linear trend line.
    fig, ax = plt.subplots(figsize=(8, 4.8))
    sns.regplot(
        data=df,
        x="sleep_hours",
        y="focus_score",
        scatter_kws={"alpha": 0.6, "color": "#1b9e77"},
        line_kws={"color": "#d95f02"},
        ax=ax,
    )
    ax.set_title(f"Sleep hours vs focus score (r = {r_value:.2f})")
    ax.set_xlabel("Sleep hours")
    ax.set_ylabel("Focus score")
    fig.tight_layout()
    fig.savefig(OUT / "sleep_focus_scatter.png", dpi=140)
    plt.close(fig)

    # STEP 8 - Plot the full correlation heatmap.
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    sns.heatmap(corr, annot=True, cmap="RdBu_r", vmin=-1, vmax=1, linewidths=0.5, ax=ax)
    ax.set_title("Correlation heatmap")
    fig.tight_layout()
    fig.savefig(OUT / "correlation_heatmap.png", dpi=140)
    plt.close(fig)

    # STEP 9 - Plot focus against screen time as a second view.
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.regplot(
        data=df,
        x="screen_time_hours",
        y="focus_score",
        scatter_kws={"alpha": 0.55, "color": "#7570b3"},
        line_kws={"color": "#e7298a"},
        ax=ax,
    )
    ax.set_title("Screen time vs focus score")
    ax.set_xlabel("Screen time (hours)")
    ax.set_ylabel("Focus score")
    fig.tight_layout()
    fig.savefig(OUT / "screen_focus_scatter.png", dpi=140)
    plt.close(fig)

    print("\nDONE. Check outputs/results.txt and the correlation charts.")


if __name__ == "__main__":
    main()
