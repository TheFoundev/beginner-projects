"""Project 09: How Tall Will You Be? (linear regression).

Run:
    python main.py

This is a teaching model, not a medical prediction.  It shows how a
relationship with plenty of natural noise can still produce a useful trend.
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
    df = pd.read_csv(DATA / "heights.csv")
    df["midparent_cm"] = (df["mother_cm"] + df["father_cm"]) / 2
    X = df[["midparent_cm"]]
    y = df["child_cm"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    slope = float(model.coef_[0])
    intercept = float(model.intercept_)
    example = float(model.predict(pd.DataFrame({"midparent_cm": [170.0]}))[0])

    print("=" * 60)
    print("HOW TALL WILL YOU BE?")
    print("=" * 60)
    print(f"Model: child height = {slope:.2f} x midparent height + {intercept:.2f}")
    print(f"Mean absolute error: {mae:.1f} cm")
    print(f"R-squared: {r2:.2f}")
    print(f"Prediction for midparent height 170 cm: {example:.1f} cm")
    print("\nRemember: nutrition, health, sleep, and chance also matter.")

    line_x = np.linspace(df["midparent_cm"].min(), df["midparent_cm"].max(), 100)
    line_y = model.predict(pd.DataFrame({"midparent_cm": line_x}))

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(X_train, y_train, color="#8e44ad", s=50, alpha=0.8, label="training families")
    ax.scatter(X_test, y_test, color="#16a085", s=60, marker="s", label="test families")
    ax.plot(line_x, line_y, color="#c0392b", linewidth=2.5, label="trend line")
    ax.scatter([170], [example], color="#111111", marker="*", s=220, zorder=5, label="170 cm example")
    ax.set_xlabel("Midparent height (cm)")
    ax.set_ylabel("Child height (cm)")
    ax.set_title("Parent height vs. child height")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "height_regression.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "metrics.txt", "w", encoding="utf-8") as handle:
        handle.write(f"equation: child = {slope:.4f} * midparent + {intercept:.4f}\n")
        handle.write(f"MAE: {mae:.4f} cm\nR2: {r2:.4f}\n")
        handle.write(f"prediction at midparent 170 cm: {example:.2f} cm\n")

    print("\nSaved: outputs/height_regression.png, outputs/metrics.txt")
    print("Try this: add mother and father as separate features and compare.")


if __name__ == "__main__":
    main()
