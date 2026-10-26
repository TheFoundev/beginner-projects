"""Project 10: The Sleep vs. Screen Time Detective (linear regression).

Run:
    python main.py

A correlation project: the model finds a trend, but the script also reminds
you that a trend is not proof of cause and effect.
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
    df = pd.read_csv(DATA / "sleep_screen.csv")
    X = df[["screen_time_hours"]]
    y = df["sleep_hours"]

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
    correlation = float(df["screen_time_hours"].corr(df["sleep_hours"]))
    example = float(model.predict(pd.DataFrame({"screen_time_hours": [3.0]}))[0])

    print("=" * 60)
    print("THE SLEEP VS. SCREEN TIME DETECTIVE")
    print("=" * 60)
    print(f"Model: sleep = {slope:.2f} x screen time + {intercept:.2f}")
    print(f"Correlation: {correlation:.2f} (negative means they move in opposite directions)")
    print(f"Mean absolute error: {mae:.2f} hours")
    print(f"R-squared: {r2:.2f}")
    print(f"Prediction for 3 hours of screen time: {example:.1f} hours of sleep")
    print("\nImportant: this does not prove that screen time causes less sleep.")

    line_x = np.linspace(df["screen_time_hours"].min(), df["screen_time_hours"].max(), 100)
    line_y = model.predict(pd.DataFrame({"screen_time_hours": line_x}))

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(X_train, y_train, color="#2c3e50", s=55, label="training data")
    ax.scatter(X_test, y_test, color="#e67e22", s=65, marker="s", label="test data")
    ax.plot(line_x, line_y, color="#c0392b", linewidth=2.5, label="trend line")
    ax.scatter([3], [example], color="#111111", marker="*", s=220, zorder=5, label="3-hour example")
    ax.set_xlabel("Screen time before bed (hours)")
    ax.set_ylabel("Sleep (hours)")
    ax.set_title("Screen time vs. sleep duration")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "sleep_regression.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "metrics.txt", "w", encoding="utf-8") as handle:
        handle.write(f"equation: sleep = {slope:.4f} * screen_time + {intercept:.4f}\n")
        handle.write(f"correlation: {correlation:.4f}\n")
        handle.write(f"MAE: {mae:.4f}\nR2: {r2:.4f}\n")
        handle.write(f"prediction at 3 hours: {example:.2f}\n")

    print("\nSaved: outputs/sleep_regression.png, outputs/metrics.txt")
    print("Try this: add 'weekend' as a second feature and see whether it helps.")


if __name__ == "__main__":
    main()
