"""Project 08 - The Study Habits Explorer.

Goal: describe distributions, measure relationships, and compare exam scores
across study methods.

Run from the pack root:
    python3 projects/08_study_habits/main.py
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
    print("PROJECT 08 - THE STUDY HABITS EXPLORER")
    print("=" * 70)

    # STEP 1 - Load the student survey.
    df = pd.read_csv(DATA / "study_habits.csv")
    print(f"\nSTEP 1: loaded {len(df)} students")
    print(df.head(3).to_string(index=False))

    # STEP 2 - Check the dataset before analysis.
    print("\nSTEP 2: quality check")
    print("Missing values:", int(df.isna().sum().sum()))
    print(df.describe().round(2).to_string())

    # STEP 3 - Choose the numeric columns for correlation analysis.
    # Correlation measures how strongly two numbers move together, from -1 to +1.
    numeric_cols = [
        "study_hours",
        "sleep_hours",
        "attendance_percent",
        "screen_time_hours",
        "exam_score",
    ]
    corr = df[numeric_cols].corr().round(2)
    corr.to_csv(OUT / "correlation_matrix.csv")
    print("\nSTEP 3: correlation matrix")
    print(corr.to_string())

    # STEP 4 - Compare study methods.
    method_summary = (
        df.groupby("study_method")
        .agg(
            students=("student_id", "count"),
            avg_exam_score=("exam_score", "mean"),
            avg_study_hours=("study_hours", "mean"),
            avg_sleep_hours=("sleep_hours", "mean"),
        )
        .round(2)
        .sort_values("avg_exam_score", ascending=False)
    )
    method_summary.to_csv(OUT / "method_summary.csv")
    print("\nSTEP 4: study-method summary")
    print(method_summary.to_string())

    # STEP 5 - Plot the distributions of the four main habits.
    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    plot_specs = [
        ("study_hours", "Study hours per day", "#1b9e77", axes[0, 0]),
        ("sleep_hours", "Sleep hours per night", "#7570b3", axes[0, 1]),
        ("attendance_percent", "Attendance (%)", "#d95f02", axes[1, 0]),
        ("exam_score", "Exam score", "#e7298a", axes[1, 1]),
    ]
    for column, title, color, ax in plot_specs:
        sns.histplot(df[column], bins=14, kde=True, color=color, ax=ax)
        ax.set_title(title)
        ax.set_xlabel("")
        ax.set_ylabel("Students")
    fig.suptitle("Distributions of study habits and exam scores", fontsize=14)
    fig.tight_layout()
    fig.savefig(OUT / "study_distributions.png", dpi=140)
    plt.close(fig)

    # STEP 6 - Plot the correlation heatmap.
    fig, ax = plt.subplots(figsize=(8, 5.5))
    sns.heatmap(corr, annot=True, cmap="RdBu_r", vmin=-1, vmax=1, linewidths=0.5, ax=ax)
    ax.set_title("Correlation between habits and exam score")
    fig.tight_layout()
    fig.savefig(OUT / "correlation_heatmap.png", dpi=140)
    plt.close(fig)

    # STEP 7 - Plot study hours against exam score with a trend line.
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.regplot(data=df, x="study_hours", y="exam_score", scatter_kws={"alpha": 0.55}, ax=ax)
    ax.set_title("Study hours vs exam score")
    ax.set_xlabel("Study hours per day")
    ax.set_ylabel("Exam score")
    fig.tight_layout()
    fig.savefig(OUT / "study_vs_score.png", dpi=140)
    plt.close(fig)

    # STEP 8 - Compare exam scores by study method.
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.boxplot(data=df, x="study_method", y="exam_score", palette="Set2", ax=ax)
    ax.set_title("Exam score by study method")
    ax.set_xlabel("")
    ax.set_ylabel("Exam score")
    fig.tight_layout()
    fig.savefig(OUT / "method_boxplot.png", dpi=140)
    plt.close(fig)

    # STEP 9 - Write the key findings.
    best_method = method_summary.index[0]
    strongest = corr["exam_score"].drop("exam_score").abs().idxmax()
    strongest_value = corr.loc[strongest, "exam_score"]
    insights = [
        "STUDY HABITS INSIGHTS",
        "=" * 50,
        f"Average exam score: {df['exam_score'].mean():.1f}",
        f"Average study time: {df['study_hours'].mean():.1f} hours/day",
        f"Best average score by method: {best_method} ({method_summary.loc[best_method, 'avg_exam_score']:.1f})",
        f"Strongest relationship with exam score: {strongest} (r = {strongest_value:.2f})",
        "Remember: correlation does not prove causation.",
        "",
        "Study-method summary:",
        method_summary.to_string(),
    ]
    (OUT / "insights.txt").write_text("\n".join(insights), encoding="utf-8")
    print("\n" + "\n".join(insights))
    print("\nDONE. Check outputs for distributions, heatmap and comparison charts.")


if __name__ == "__main__":
    main()
