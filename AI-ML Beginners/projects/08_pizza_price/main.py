"""Project 08: The Pizza Price Calculator (linear regression).

Run:
    python main.py

Train a model on a small menu, then use it as a reusable price-quoting
function for any pizza size and topping count.
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
    df = pd.read_csv(DATA / "pizza_menu.csv")
    X = df[["diameter_inches", "toppings"]]
    y = df["price_usd"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    size_weight, topping_weight = model.coef_
    intercept = model.intercept_

    def quote_pizza(diameter_inches: float, toppings: int) -> float:
        """Return the model's price estimate for one pizza."""
        order = pd.DataFrame(
            [{"diameter_inches": diameter_inches, "toppings": toppings}]
        )
        return float(model.predict(order)[0])

    example = quote_pizza(12, 3)

    print("=" * 60)
    print("THE PIZZA PRICE CALCULATOR")
    print("=" * 60)
    print(f"Equation: price = {intercept:.2f} + {size_weight:.2f} x diameter + {topping_weight:.2f} x toppings")
    print(f"Mean absolute error: ${mae:.2f}")
    print(f"R-squared: {r2:.2f}")
    print(f"Quote for a 12-inch pizza with 3 toppings: ${example:.2f}")

    menu = pd.DataFrame(
        [
            {"order": "Small, 8-inch, 1 topping", "diameter": 8, "toppings": 1},
            {"order": "Medium, 12-inch, 3 toppings", "diameter": 12, "toppings": 3},
            {"order": "Large, 16-inch, 5 toppings", "diameter": 16, "toppings": 5},
            {"order": "Party, 18-inch, 5 toppings", "diameter": 18, "toppings": 5},
        ]
    )
    menu["model_quote"] = [
        quote_pizza(row.diameter, row.toppings) for row in menu.itertuples()
    ]
    print("\nPrice list from the model:")
    for row in menu.itertuples():
        print(f"  {row.order:35s} ${row.model_quote:.2f}")

    # ---- Actual vs. predicted -----------------------------------------
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(y_test, predictions, color="#e67e22", s=70, alpha=0.85)
    low = min(y_test.min(), predictions.min())
    high = max(y_test.max(), predictions.max())
    ax.plot([low, high], [low, high], color="#2471a3", linestyle="--", label="perfect prediction")
    ax.set_xlabel("Actual menu price ($)")
    ax.set_ylabel("Model quote ($)")
    ax.set_title("How close are the pizza price quotes?")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "actual_vs_predicted.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "quotes.txt", "w", encoding="utf-8") as handle:
        handle.write(f"equation: price = {intercept:.4f} + {size_weight:.4f}*diameter + {topping_weight:.4f}*toppings\n")
        handle.write(f"MAE: {mae:.4f}\nR2: {r2:.4f}\n\n")
        for row in menu.itertuples():
            handle.write(f"{row.order}: ${row.model_quote:.2f}\n")

    print("\nSaved: outputs/actual_vs_predicted.png, outputs/quotes.txt")
    print("Try this: add a 'stuffed_crust' true/false column and retrain.")


if __name__ == "__main__":
    main()
