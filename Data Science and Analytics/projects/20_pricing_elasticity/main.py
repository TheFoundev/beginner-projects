"""Project 20 - The Pricing & Demand Analyzer.

Goal: estimate price elasticity with a log-log regression and simulate how
demand changes when a product's price moves up or down.

Run from the pack root:
    python3 projects/20_pricing_elasticity/main.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")


def main() -> None:
    print("=" * 70)
    print("PROJECT 20 - THE PRICING & DEMAND ANALYZER")
    print("=" * 70)

    # STEP 1 - Load the pricing data.
    df = pd.read_csv(DATA / "pricing_data.csv")
    print(f"\nSTEP 1: loaded {len(df)} product-month rows")
    print(df.head(3).to_string(index=False))

    # STEP 2 - Check the values before taking logs.
    # Logs are only defined for positive numbers, so price and quantity must be > 0.
    print("\nSTEP 2: quality check")
    print("Missing values:", int(df.isna().sum().sum()))
    print(f"Rows with price <= 0: {int((df['price'] <= 0).sum())}")
    print(f"Rows with quantity <= 0: {int((df['quantity'] <= 0).sum())}")
    print(df[["price", "quantity", "competitor_price"]].describe().round(2).to_string())

    # STEP 3 - Create log variables.
    # In a log-log model, the coefficient on log(price) is the price elasticity:
    # a 1% increase in price is associated with an elasticity% change in quantity.
    df["log_quantity"] = np.log(df["quantity"])
    df["log_price"] = np.log(df["price"])
    df["log_competitor_price"] = np.log(df["competitor_price"])
    print("\nSTEP 3: created log(quantity), log(price) and log(competitor price)")

    # STEP 4 - Fit the main log-log regression.
    # We control for promotion and competitor price so the price coefficient is
    # not simply picking up those effects.
    X = sm.add_constant(df[["log_price", "promotion", "log_competitor_price"]])
    y = df["log_quantity"]
    model = sm.OLS(y, X).fit()
    print("\nSTEP 4: OLS regression summary")
    print(model.summary().tables[1])

    elasticity = model.params["log_price"]
    elasticity_p = model.pvalues["log_price"]
    r_squared = model.rsquared
    print(f"\nEstimated price elasticity: {elasticity:.3f}")
    print(f"p-value: {elasticity_p:.5f}")
    print(f"R-squared: {r_squared:.3f}")
    print("Interpretation: a 1% price increase is associated with a "
          f"{elasticity:.2f}% change in quantity.")

    # STEP 5 - Estimate elasticity separately for each product.
    # Pooling all products can hide very different customer responses.
    rows = []
    for product, group in df.groupby("product"):
        X_p = sm.add_constant(group[["log_price", "promotion", "log_competitor_price"]])
        m_p = sm.OLS(group["log_quantity"], X_p).fit()
        rows.append(
            {
                "product": product,
                "elasticity": m_p.params["log_price"],
                "p_value": m_p.pvalues["log_price"],
                "r_squared": m_p.rsquared,
                "observations": len(group),
            }
        )
    elasticity_table = pd.DataFrame(rows).sort_values("elasticity")
    elasticity_table.to_csv(OUT / "elasticity_by_product.csv", index=False)
    print("\nSTEP 5: elasticity by product")
    print(elasticity_table.round(3).to_string(index=False))

    # STEP 6 - Simulate demand for one product at different prices.
    # Hold promotion off and competitor price at its average, then change only price.
    product = "Coffee"
    product_df = df[df["product"] == product].copy()
    X_product = sm.add_constant(product_df[["log_price", "promotion", "log_competitor_price"]])
    product_model = sm.OLS(product_df["log_quantity"], X_product).fit()

    mean_price = product_df["price"].mean()
    mean_log_competitor = product_df["log_competitor_price"].mean()
    price_grid = np.linspace(mean_price * 0.75, mean_price * 1.25, 25)
    simulation = pd.DataFrame(
        {
            "price": price_grid,
            "promotion": 0,
            "log_price": np.log(price_grid),
            "log_competitor_price": mean_log_competitor,
        }
    )
    sim_X = sm.add_constant(
        simulation[["log_price", "promotion", "log_competitor_price"]],
        has_constant="add",
    )
    simulation["predicted_quantity"] = np.exp(product_model.predict(sim_X))
    simulation["price_change_pct"] = simulation["price"] / mean_price - 1
    simulation.to_csv(OUT / "coffee_price_simulation.csv", index=False)
    print(f"\nSTEP 6: simulated {len(simulation)} price points for {product}")
    print(simulation[["price", "predicted_quantity"]].head(5).round(2).to_string(index=False))

    # STEP 7 - Save the regression results.
    results = [
        "PRICING AND DEMAND RESULTS",
        "=" * 60,
        f"Rows analysed: {len(df)}",
        f"Products: {df['product'].nunique()}",
        "",
        "Main log-log regression:",
        f"Price elasticity: {elasticity:.3f}",
        f"Elasticity p-value: {elasticity_p:.5f}",
        f"R-squared: {r_squared:.3f}",
        "",
        "Coefficients:",
        model.params.round(4).to_string(),
        "",
        "Elasticity by product:",
        elasticity_table.round(3).to_string(index=False),
        "",
        "Interpretation guide:",
        "- Elasticity below -1: demand is elastic; a price rise tends to reduce revenue.",
        "- Elasticity between -1 and 0: demand is inelastic; a price rise may increase revenue.",
        "- Elasticity near 0: price changes barely affect quantity.",
        "",
        "This is an observational model. It shows association, not proof of causation,",
        "and a real pricing decision should also consider costs, competitors and experiments.",
    ]
    (OUT / "results.txt").write_text("\n".join(results), encoding="utf-8")
    print("\nSTEP 7: results saved")

    # STEP 8 - Plot the simulated demand curve.
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.plot(simulation["price"], simulation["predicted_quantity"], color="#1b9e77", linewidth=2,
            label="Predicted demand")
    ax.scatter(product_df["price"], product_df["quantity"], color="#d95f02", alpha=0.65,
               label="Observed months")
    ax.axvline(mean_price, color="grey", linestyle=":", label="Average price")
    ax.set_title(f"Demand curve for {product}")
    ax.set_xlabel("Price ($)")
    ax.set_ylabel("Quantity sold")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "demand_curve.png", dpi=140)
    plt.close(fig)

    # STEP 9 - Plot elasticity by product.
    fig, ax = plt.subplots(figsize=(8, 4.2))
    colors = ["#d95f02" if value < -1 else "#1b9e77" for value in elasticity_table["elasticity"]]
    ax.barh(elasticity_table["product"], elasticity_table["elasticity"], color=colors)
    ax.axvline(-1, color="grey", linestyle="--", label="Elastic = -1")
    ax.set_title("Estimated price elasticity by product")
    ax.set_xlabel("Elasticity (more negative = more price-sensitive)")
    ax.set_ylabel("")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "elasticity_by_product.png", dpi=140)
    plt.close(fig)

    print("\n" + "\n".join(results))
    print("\nDONE. Check outputs/results.txt and the demand curve.")


if __name__ == "__main__":
    main()
