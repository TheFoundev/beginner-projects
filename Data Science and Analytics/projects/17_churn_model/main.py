"""Project 17 - The Churn Early-Warning System.

Goal: train a logistic regression model that estimates each customer's chance
of churning, then evaluate it with a confusion matrix and ROC curve.

Run from the pack root:
    python3 projects/17_churn_model/main.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")


def main() -> None:
    print("=" * 70)
    print("PROJECT 17 - THE CHURN EARLY-WARNING SYSTEM")
    print("=" * 70)

    # STEP 1 - Load the customer data.
    df = pd.read_csv(DATA / "churn.csv")
    print(f"\nSTEP 1: loaded {len(df)} customers")
    print(df.head(3).to_string(index=False))

    # STEP 2 - Check the target and missing values.
    print("\nSTEP 2: quality check")
    print("Missing values:", int(df.isna().sum().sum()))
    print(f"Churn rate: {df['churned'].mean():.1%}")
    print(df.groupby("churned").size().to_string())

    # STEP 3 - Separate features (X) from the target (y).
    # customer_id is an identifier, not a useful predictor, so we drop it.
    feature_cols = [
        "tenure_months",
        "monthly_charges",
        "support_calls",
        "late_payments",
        "usage_hours",
    ]
    X = df[feature_cols]
    y = df["churned"]
    print("\nSTEP 3: features and target")
    print("Features:", feature_cols)
    print("Target: churned (1 = left, 0 = stayed)")

    # STEP 4 - Split into training and test sets.
    # The model learns on 70% of customers and is judged on the unseen 30%.
    # stratify=y keeps the churn rate similar in both sets.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )
    print(f"\nSTEP 4: train rows = {len(X_train)}, test rows = {len(X_test)}")

    # STEP 5 - Scale the features.
    # Fit the scaler on the training data only, then apply it to the test data.
    # This avoids leaking information from the test set into training.
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # STEP 6 - Fit logistic regression.
    # Logistic regression predicts a probability, then classifies at 0.5 by default.
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_scaled, y_train)
    print("\nSTEP 5-6: model trained")

    # STEP 7 - Make predictions on the test set.
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    # STEP 8 - Evaluate the model.
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    auc = roc_auc_score(y_test, y_prob)
    baseline = max(y_test.mean(), 1 - y_test.mean())
    cm = confusion_matrix(y_test, y_pred)
    print("\nSTEP 8: test-set metrics")
    print(f"Accuracy:  {accuracy:.3f}  (majority-class baseline: {baseline:.3f})")
    print(f"Precision: {precision:.3f}")
    print(f"Recall:    {recall:.3f}")
    print(f"F1 score:  {f1:.3f}")
    print(f"ROC-AUC:   {auc:.3f}")
    print("\nConfusion matrix:")
    print(cm)

    # STEP 9 - Explain the coefficients as odds ratios.
    # A positive coefficient means the feature is associated with more churn.
    # exp(coefficient) is the odds ratio: >1 means higher odds, <1 means lower odds.
    coef_table = pd.DataFrame(
        {
            "feature": feature_cols,
            "coefficient": model.coef_[0],
            "odds_ratio": np.exp(model.coef_[0]),
        }
    ).sort_values("coefficient", ascending=False)
    coef_table.to_csv(OUT / "churn_coefficients.csv", index=False)
    print("\nSTEP 9: coefficients and odds ratios")
    print(coef_table.round(3).to_string(index=False))

    # STEP 10 - Save a plain-English results report.
    results = [
        "CHURN MODEL RESULTS",
        "=" * 60,
        f"Customers: {len(df)}",
        f"Training rows: {len(X_train)}",
        f"Test rows: {len(X_test)}",
        f"Churn rate: {df['churned'].mean():.1%}",
        "",
        f"Accuracy:  {accuracy:.3f}",
        f"Precision: {precision:.3f}",
        f"Recall:    {recall:.3f}",
        f"F1 score:  {f1:.3f}",
        f"ROC-AUC:   {auc:.3f}",
        f"Majority-class baseline: {baseline:.3f}",
        "",
        "Confusion matrix (rows = actual, columns = predicted):",
        pd.DataFrame(cm, index=["Actual stayed", "Actual churned"],
                     columns=["Predicted stayed", "Predicted churned"]).to_string(),
        "",
        "Coefficients (positive = more churn, negative = less churn):",
        coef_table.round(3).to_string(index=False),
        "",
        "Metric reminders:",
        "- Precision: of customers flagged as churners, how many really churned?",
        "- Recall: of customers who really churned, how many did we catch?",
        "- ROC-AUC: ability to rank churners above stayers; 0.5 is random.",
        "",
        "This is a teaching model, not a production decision system.",
    ]
    (OUT / "results.txt").write_text("\n".join(results), encoding="utf-8")
    print("\nSTEP 10: results saved")
    print("\n".join(results))

    # STEP 11 - Plot the most important coefficients.
    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = ["#d95f02" if value > 0 else "#1b9e77" for value in coef_table["coefficient"]]
    ax.barh(coef_table["feature"], coef_table["coefficient"], color=colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_title("Logistic regression coefficients")
    ax.set_xlabel("Coefficient (positive = more churn)")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(OUT / "churn_coefficients.png", dpi=140)
    plt.close(fig)

    # STEP 12 - Plot the confusion matrix.
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["Predicted stayed", "Predicted churned"],
                yticklabels=["Actual stayed", "Actual churned"], ax=ax)
    ax.set_title("Confusion matrix on the test set")
    fig.tight_layout()
    fig.savefig(OUT / "confusion_matrix.png", dpi=140)
    plt.close(fig)

    # STEP 13 - Plot the ROC curve.
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.plot(fpr, tpr, color="#1b9e77", linewidth=2, label=f"AUC = {auc:.3f}")
    ax.plot([0, 1], [0, 1], linestyle="--", color="grey", label="Random guess")
    ax.set_title("ROC curve")
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(OUT / "roc_curve.png", dpi=140)
    plt.close(fig)

    print("\nDONE. Check outputs/results.txt, the coefficient chart and the ROC curve.")


if __name__ == "__main__":
    main()
