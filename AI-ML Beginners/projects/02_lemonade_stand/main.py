"""Project 02: The Lemonade Stand Fortune Teller (linear regression).

Run:
    python main.py

The model learns the relationship between temperature and cups sold, then
predicts sales for a 35 degree Celsius day.
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
    df = pd.read_csv(DATA / "lemonade_days.csv")
    X = df[["temperature_c"]]
    y = df["cups_sold"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    test_predictions = model.predict(X_test)

    slope = float(model.coef_[0])
    intercept = float(model.intercept_)
    mae = mean_absolute_error(y_test, test_predictions)
    r2 = r2_score(y_test, test_predictions)

    hot_day = pd.DataFrame({"temperature_c": [35.0]})
    hot_prediction = float(model.predict(hot_day)[0])

    print("=" * 60)
    print("THE LEMONADE STAND FORTUNE TELLER")
    print("=" * 60)
    print(f"Model: cups = {slope:.2f} x temperature + {intercept:.2f}")
    print(f"Meaning: each extra 1 C is associated with about {slope:.2f} more cups.")
    print(f"Mean absolute error: {mae:.2f} cups")
    print(f"R-squared: {r2:.2f}")
    print(f"Prediction for 35 C: {hot_prediction:.1f} cups")

    # ---- Plot the data and the learned line ---------------------------
    line_x = np.linspace(df["temperature_c"].min(), df["temperature_c"].max(), 100)
    line_y = model.predict(pd.DataFrame({"temperature_c": line_x}))

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(X_train, y_train, color="#e67e22", label="training days", s=55)
    ax.scatter(X_test, y_test, color="#2c3e50", label="test days", s=55, marker="s")
    ax.plot(line_x, line_y, color="#16a085", linewidth=2.5, label="learned trend line")
    ax.scatter([35], [hot_prediction], color="#c0392b", s=140, marker="*", zorder=5, label="35 C prediction")
    ax.set_xlabel("Temperature (C)")
    ax.set_ylabel("Cups sold")
    ax.set_title("Lemonade sales vs. temperature")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "lemonade_regression.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "prediction.txt", "w", encoding="utf-8") as handle:
        handle.write(f"Equation: cups = {slope:.4f} * temperature + {intercept:.4f}\n")
        handle.write(f"Prediction at 35 C: {hot_prediction:.2f} cups\n")
        handle.write(f"Mean absolute error: {mae:.2f}\n")
        handle.write(f"R-squared: {r2:.2f}\n")

    print("\nSaved: outputs/lemonade_regression.png, outputs/prediction.txt")
    print("Try this: add a rainy-day column and see whether the line changes.")


if __name__ == "__main__":
    main()
