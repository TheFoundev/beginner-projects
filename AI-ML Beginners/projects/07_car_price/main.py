"""Project 07: The Used Car Price Whisperer (multiple linear regression).

Run:
    python main.py

Two clues (age and kilometres) are combined into one price estimate.  The
script prints the model's weights so you can see which clue matters more.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)


def main() -> None:
    df = pd.read_csv(DATA / "used_cars.csv")
    X = df[["age_years", "kilometers"]]
    y = df["price_usd"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    age_weight, km_weight = model.coef_
    intercept = model.intercept_

    example = pd.DataFrame([{"age_years": 5, "kilometers": 60_000}])
    example_price = float(model.predict(example)[0])

    print("=" * 60)
    print("THE USED CAR PRICE WHISPERER")
    print("=" * 60)
    print(f"Equation: price = {intercept:,.0f} + ({age_weight:,.0f} x age) + ({km_weight:.2f} x km)")
    print(f"Each extra year is associated with about ${abs(age_weight):,.0f} less value.")
    print(f"Each extra 10,000 km is associated with about ${abs(km_weight) * 10_000:,.0f} less value.")
    print(f"Mean absolute error: ${mae:,.0f}")
    print(f"R-squared: {r2:.2f}")
    print(f"Prediction for a 5-year-old car with 60,000 km: ${example_price:,.0f}")

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(y_test, predictions, color="#2471a3", s=65, alpha=0.85)
    low = min(y_test.min(), predictions.min())
    high = max(y_test.max(), predictions.max())
    ax.plot([low, high], [low, high], color="#c0392b", linestyle="--", label="perfect prediction")
    ax.set_xlabel("Actual price ($)")
    ax.set_ylabel("Predicted price ($)")
    ax.set_title("Actual vs. predicted used-car prices")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "actual_vs_predicted.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "metrics.txt", "w", encoding="utf-8") as handle:
        handle.write(f"intercept: {intercept:.2f}\n")
        handle.write(f"age coefficient: {age_weight:.2f}\n")
        handle.write(f"km coefficient: {km_weight:.6f}\n")
        handle.write(f"MAE: {mae:.2f}\n")
        handle.write(f"R2: {r2:.4f}\n")
        handle.write(f"example prediction: {example_price:.2f}\n")

    print("\nSaved: outputs/actual_vs_predicted.png, outputs/metrics.txt")
    print("Try this: add a 'fuel_type' column (petrol/diesel) and think about encoding it.")


if __name__ == "__main__":
    main()
