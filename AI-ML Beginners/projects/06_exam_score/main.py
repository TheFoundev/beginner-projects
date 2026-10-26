"""Project 06: Predict Your Exam Score (linear regression).

Run:
    python main.py

A tiny study-hours dataset, a line of best fit, and a prediction for six
hours of study.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)


def main() -> None:
    df = pd.read_csv(DATA / "exam_scores.csv")
    X = df[["hours_studied"]]
    y = df["exam_score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    slope = float(model.coef_[0])
    intercept = float(model.intercept_)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    six_hours = float(model.predict(pd.DataFrame({"hours_studied": [6.0]}))[0])

    print("=" * 60)
    print("PREDICT YOUR EXAM SCORE")
    print("=" * 60)
    print(f"Model: score = {slope:.2f} x hours + {intercept:.2f}")
    print(f"Mean absolute error: {mae:.1f} points")
    print(f"R-squared: {r2:.2f}")
    print(f"Prediction for 6 hours: {six_hours:.1f} points")

    line_x = np.linspace(df["hours_studied"].min(), df["hours_studied"].max(), 100)
    line_y = model.predict(pd.DataFrame({"hours_studied": line_x}))

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(X_train, y_train, color="#2471a3", s=55, label="training data")
    ax.scatter(X_test, y_test, color="#e67e22", s=65, marker="s", label="test data")
    ax.plot(line_x, line_y, color="#c0392b", linewidth=2.5, label="line of best fit")
    ax.scatter([6], [six_hours], color="#111111", marker="*", s=220, zorder=5, label="6-hour prediction")
    ax.set_xlabel("Hours studied")
    ax.set_ylabel("Exam score")
    ax.set_title("Study hours vs. exam score")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "exam_score_regression.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "metrics.txt", "w", encoding="utf-8") as handle:
        handle.write(f"equation: score = {slope:.4f} * hours + {intercept:.4f}\n")
        handle.write(f"mean absolute error: {mae:.4f}\n")
        handle.write(f"r2: {r2:.4f}\n")
        handle.write(f"prediction at 6 hours: {six_hours:.2f}\n")

    print("\nSaved: outputs/exam_score_regression.png, outputs/metrics.txt")
    print("Try this: collect five real study-hour/score pairs and add them.")


if __name__ == "__main__":
    main()
