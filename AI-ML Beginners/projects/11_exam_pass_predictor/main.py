"""Project 11: Will You Pass? (logistic regression).

Run:
    python main.py

Logistic regression predicts a probability, not just a yes/no label.  The
script also shows how changing the cutoff changes the decisions.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay, confusion_matrix
from sklearn.model_selection import train_test_split

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)


def main() -> None:
    df = pd.read_csv(DATA / "student_results.csv")
    X = df[["hours_studied", "attendance_percent"]]
    y = df["passed"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    accuracy = accuracy_score(y_test, predictions)

    print("=" * 60)
    print("WILL YOU PASS?")
    print("=" * 60)
    print(f"Accuracy at 50% cutoff: {accuracy:.1%}")
    print(f"Hours weight: {model.coef_[0, 0]:.2f}")
    print(f"Attendance weight: {model.coef_[0, 1]:.2f}")
    print("\nClassification report:\n")
    print(classification_report(y_test, predictions, zero_division=0))

    examples = pd.DataFrame(
        [
            {"label": "6 hours, 80% attendance", "hours_studied": 6, "attendance_percent": 80},
            {"label": "3 hours, 60% attendance", "hours_studied": 3, "attendance_percent": 60},
            {"label": "8 hours, 95% attendance", "hours_studied": 8, "attendance_percent": 95},
        ]
    )
    example_probs = model.predict_proba(examples[["hours_studied", "attendance_percent"]])[:, 1]
    print("Example probabilities:")
    for label, probability in zip(examples["label"], example_probs):
        print(f"  {label:30s} -> {probability:.0%} chance of passing")

    print("\nChanging the cutoff:")
    for cutoff in (0.5, 0.7):
        cutoff_predictions = (probabilities >= cutoff).astype(int)
        print(
            f"  cutoff {cutoff:.0%}: predicted {cutoff_predictions.sum()} passes "
            f"out of {len(cutoff_predictions)} test students"
        )

    # ---- Decision boundary --------------------------------------------
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    DecisionBoundaryDisplay.from_estimator(
        model,
        X,
        response_method="predict_proba",
        grid_resolution=250,
        cmap="RdYlBu_r",
        alpha=0.35,
        ax=ax,
    )
    scatter = ax.scatter(
        X["hours_studied"],
        X["attendance_percent"],
        c=y,
        cmap="RdYlBu_r",
        edgecolor="black",
        linewidth=0.5,
        s=55,
    )
    handles, _ = scatter.legend_elements()
    ax.legend(handles, ["failed", "passed"], title="actual result", loc="lower right")
    ax.set_xlabel("Hours studied")
    ax.set_ylabel("Attendance (%)")
    ax.set_title("The model learns a boundary between pass and fail")
    fig.tight_layout()
    fig.savefig(OUT / "decision_boundary.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---- Confusion matrix ---------------------------------------------
    cm = confusion_matrix(y_test, predictions, labels=[0, 1])
    fig, ax = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay(cm, display_labels=["failed", "passed"]).plot(
        ax=ax, cmap="Blues", colorbar=False
    )
    ax.set_title("Pass/fail predictions")
    fig.tight_layout()
    fig.savefig(OUT / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "metrics.txt", "w", encoding="utf-8") as handle:
        handle.write(f"accuracy at 0.5 cutoff: {accuracy:.4f}\n\n")
        handle.write(classification_report(y_test, predictions, zero_division=0))
        handle.write("\nExample probabilities:\n")
        for label, probability in zip(examples["label"], example_probs):
            handle.write(f"{label}: {probability:.4f}\n")

    print("\nSaved: outputs/decision_boundary.png, outputs/confusion_matrix.png, outputs/metrics.txt")
    print("Try this: change the cutoff to 0.8 and discuss which mistake is worse.")


if __name__ == "__main__":
    main()
