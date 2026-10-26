"""Project 02 - The Student Records Rescue.

Goal: clean two messy tables, join them, and produce one trustworthy gradebook.

Run from the pack root:
    python3 projects/02_student_records/main.py
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


def clean_id(series: pd.Series) -> pd.Series:
    """Make S001, s001, S-001 and ' S001 ' all look the same."""
    return (
        series.astype(str)
        .str.strip()
        .str.upper()
        .str.replace("-", "", regex=False)
        .str.replace(" ", "", regex=False)
    )


def main() -> None:
    print("=" * 70)
    print("PROJECT 02 - THE STUDENT RECORDS RESCUE")
    print("=" * 70)

    # STEP 1 - Load both source tables.
    # students_raw has one row per student; scores_raw has one row per student-subject.
    students = pd.read_csv(DATA / "students_raw.csv")
    scores = pd.read_csv(DATA / "scores_raw.csv")
    print(f"\nSTEP 1: loaded {len(students)} student rows and {len(scores)} score rows")
    print(students.head(3).to_string(index=False))
    print(scores.head(3).to_string(index=False))

    # STEP 2 - Inspect the join keys.
    # The same student ID appears in different formats, so a direct merge would fail.
    print("\nSTEP 2: raw ID examples")
    print("students:", students["student_id"].head(6).tolist())
    print("scores:  ", scores["student_id"].head(6).tolist())

    # STEP 3 - Standardise IDs and remove duplicate student rows.
    students["student_id"] = clean_id(students["student_id"])
    scores["student_id"] = clean_id(scores["student_id"])
    students["program"] = students["program"].astype(str).str.strip().str.upper()
    student_duplicates = int(students.duplicated(subset=["student_id"]).sum())
    students = students.drop_duplicates(subset=["student_id"], keep="first")
    print(f"\nSTEP 3: normalised IDs and removed {student_duplicates} duplicate student rows")

    # STEP 4 - Clean the score values.
    # to_numeric turns "88" into 88; impossible values are clipped to the valid 0-100 range.
    scores["score"] = pd.to_numeric(scores["score"], errors="coerce")
    scores["subject"] = scores["subject"].astype(str).str.strip().str.title()
    scores["score"] = scores["score"].clip(lower=0, upper=100)
    missing_scores = int(scores["score"].isna().sum())
    # A missing score is filled with the median for that subject, not the overall median.
    scores["score"] = scores.groupby("subject")["score"].transform(
        lambda series: series.fillna(series.median())
    )
    print(f"\nSTEP 4: cleaned scores and filled {missing_scores} missing values with subject medians")
    print(scores.groupby("subject")["score"].agg(["mean", "min", "max"]).round(1).to_string())

    # STEP 5 - Join the tables.
    # how="left" keeps every student, even if they have no score rows.
    merged = students.merge(scores, on="student_id", how="left", validate="one_to_many")
    unmatched_scores = scores.loc[~scores["student_id"].isin(students["student_id"]), "student_id"].nunique()
    students_without_scores = merged.loc[merged["score"].isna(), "student_id"].nunique()
    print(f"\nSTEP 5: merged table has {len(merged)} rows")
    print(f"Score rows for unknown students: {unmatched_scores} student IDs")
    print(f"Students with no score rows: {students_without_scores}")

    # STEP 6 - Reshape to one row per student.
    # pivot_table turns the three subject rows into three columns: Math, Science and English.
    wide = merged.pivot_table(
        index=["student_id", "name", "program"],
        columns="subject",
        values="score",
        aggfunc="mean",
    ).reset_index()
    wide.columns.name = None
    for subject in ["Math", "Science", "English"]:
        if subject not in wide.columns:
            wide[subject] = np.nan
    wide["average_score"] = wide[["Math", "Science", "English"]].mean(axis=1).round(1)
    wide["status"] = np.where(wide["average_score"] >= 50, "Pass", "Needs support")

    # STEP 7 - Save the clean table and a merge audit.
    clean_path = DATA / "clean_student_scores.csv"
    wide.to_csv(clean_path, index=False)
    report = [
        "STUDENT RECORDS MERGE REPORT",
        "=" * 50,
        f"Student rows before de-duplication: {len(students) + student_duplicates}",
        f"Unique students: {len(students)}",
        f"Score rows before cleaning: {len(scores)}",
        f"Missing scores filled: {missing_scores}",
        f"Score rows for unknown students: {unmatched_scores} IDs",
        f"Students with no scores: {students_without_scores}",
        "",
        "Average score by program:",
        wide.groupby("program")["average_score"].mean().round(1).to_string(),
        "",
        "Pass / support counts:",
        wide["status"].value_counts().to_string(),
    ]
    (OUT / "merge_report.txt").write_text("\n".join(report), encoding="utf-8")
    print(f"\nSTEP 6-7: clean gradebook saved to {clean_path}")

    # STEP 8 - Visualise the score distribution and program averages.
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(wide["average_score"], bins=12, kde=True, color="#1b9e77", ax=ax)
    ax.set_title("Distribution of student average scores")
    ax.set_xlabel("Average score")
    ax.set_ylabel("Number of students")
    fig.tight_layout()
    fig.savefig(OUT / "score_distribution.png", dpi=140)
    plt.close(fig)

    program_means = wide.groupby("program")["average_score"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(7, 4))
    program_means.plot(kind="bar", color="#7570b3", ax=ax)
    ax.set_title("Average score by program")
    ax.set_ylabel("Average score")
    ax.set_xlabel("Program")
    plt.xticks(rotation=0)
    fig.tight_layout()
    fig.savefig(OUT / "program_averages.png", dpi=140)
    plt.close(fig)

    print("\nTop 5 students:")
    print(wide.sort_values("average_score", ascending=False).head(5)[
        ["student_id", "name", "average_score"]
    ].to_string(index=False))
    print("\nDONE. Check outputs/merge_report.txt and the two charts.")


if __name__ == "__main__":
    main()
