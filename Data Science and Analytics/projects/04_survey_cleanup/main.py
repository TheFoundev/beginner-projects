"""Project 04 - The Survey Cleanup Crew.

Goal: turn inconsistent survey answers into clean numeric fields and summarise
what respondents actually said.

Run from the pack root:
    python3 projects/04_survey_cleanup/main.py
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
    print("PROJECT 04 - THE SURVEY CLEANUP CREW")
    print("=" * 70)

    # STEP 1 - Load the raw survey.
    raw = pd.read_csv(DATA / "survey_raw.csv")
    print(f"\nSTEP 1: loaded {len(raw)} survey rows")
    print(raw.head(3).to_string(index=False))

    # STEP 2 - Look at the inconsistency before fixing it.
    print("\nSTEP 2: raw answer values")
    print("gender:", sorted(raw["gender"].astype(str).unique())[:12])
    print("would_recommend:", sorted(raw["would_recommend"].astype(str).unique()))
    print("satisfaction:", sorted(raw["satisfaction"].astype(str).unique()))

    # STEP 3 - Remove duplicate respondents.
    df = raw.copy()
    duplicates = int(df.duplicated(subset=["respondent_id"]).sum())
    df = df.drop_duplicates(subset=["respondent_id"], keep="first").copy()
    print(f"\nSTEP 3: removed {duplicates} duplicate respondent rows")

    # STEP 4 - Clean age.
    # 999 is a placeholder used for "prefer not to say"; it is not a real age.
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df.loc[df["age"] > 100, "age"] = np.nan
    age_missing = int(df["age"].isna().sum())
    df["age"] = df["age"].fillna(df["age"].median())
    print(f"\nSTEP 4: cleaned age and filled {age_missing} missing/placeholder ages with the median")

    # STEP 5 - Standardise gender labels.
    gender_map = {
        "m": "Male", "male": "Male",
        "f": "Female", "female": "Female",
        "other": "Other",
    }
    df["gender"] = (
        df["gender"].astype(str).str.strip().str.lower().map(gender_map).fillna("Unknown")
    )
    print("\nSTEP 5: standardised gender labels")
    print(df["gender"].value_counts().to_string())

    # STEP 6 - Extract the number from satisfaction answers.
    # "5 - Very satisfied" becomes "5"; blank answers become NaN.
    df["satisfaction"] = (
        df["satisfaction"].astype(str).str.extract(r"(\d)", expand=False)
    )
    df["satisfaction"] = pd.to_numeric(df["satisfaction"], errors="coerce").clip(1, 5)
    satisfaction_missing = int(df["satisfaction"].isna().sum())
    df["satisfaction"] = df["satisfaction"].fillna(df["satisfaction"].median())
    print(f"\nSTEP 6: extracted satisfaction scores and filled {satisfaction_missing} missing values")

    # STEP 7 - Convert yes/no answers to 1/0.
    yes_no_map = {
        "yes": 1, "y": 1, "1": 1,
        "no": 0, "n": 0, "0": 0,
    }
    df["would_recommend"] = (
        df["would_recommend"].astype(str).str.strip().str.lower().map(yes_no_map)
    )
    recommend_missing = int(df["would_recommend"].isna().sum())
    # A blank recommendation is treated as "not a yes" for this simple dataset.
    df["would_recommend"] = df["would_recommend"].fillna(0).astype(int)
    print(f"\nSTEP 7: converted recommendations to 1/0 and handled {recommend_missing} blanks")

    # STEP 8 - Save the clean table and a summary.
    clean_path = DATA / "clean_survey.csv"
    df.to_csv(clean_path, index=False)
    summary = [
        "SURVEY CLEANING REPORT",
        "=" * 50,
        f"Rows before cleaning: {len(raw)}",
        f"Rows after de-duplication: {len(df)}",
        f"Duplicate rows removed: {duplicates}",
        f"Missing ages filled: {age_missing}",
        f"Missing satisfaction values filled: {satisfaction_missing}",
        f"Blank recommendation answers treated as 0: {recommend_missing}",
        f"Average satisfaction: {df['satisfaction'].mean():.2f} / 5",
        f"Recommendation rate: {df['would_recommend'].mean():.1%}",
        "",
        "Average satisfaction by gender:",
        df.groupby("gender")["satisfaction"].mean().round(2).to_string(),
    ]
    (OUT / "survey_summary.txt").write_text("\n".join(summary), encoding="utf-8")
    print(f"\nSTEP 8: clean survey saved to {clean_path}")

    # STEP 9 - Visualise the cleaned answers.
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.countplot(data=df, x="satisfaction", color="#1b9e77", ax=ax)
    ax.set_title("Satisfaction scores after cleaning")
    ax.set_xlabel("Satisfaction (1 = low, 5 = high)")
    ax.set_ylabel("Respondents")
    fig.tight_layout()
    fig.savefig(OUT / "satisfaction_distribution.png", dpi=140)
    plt.close(fig)

    gender_recommend = pd.crosstab(df["gender"], df["would_recommend"], normalize="index")
    fig, ax = plt.subplots(figsize=(8, 4))
    gender_recommend.plot(kind="bar", stacked=True, color=["#d95f02", "#1b9e77"], ax=ax)
    ax.set_title("Recommendation rate by gender")
    ax.set_xlabel("Gender")
    ax.set_ylabel("Share of respondents")
    ax.legend(["No", "Yes"], title="Recommend?")
    plt.xticks(rotation=0)
    fig.tight_layout()
    fig.savefig(OUT / "recommend_by_gender.png", dpi=140)
    plt.close(fig)

    print("\n" + "\n".join(summary))
    print("\nDONE. Check outputs/survey_summary.txt and the charts.")


if __name__ == "__main__":
    main()
