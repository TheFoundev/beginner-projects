"""Project 18 - The Sales Forecast Baseline.

Goal: build a simple, explainable sales forecast with a moving average and a
linear trend, then test it on the last six months.

Run from the pack root:
    python3 projects/18_sales_forecast/main.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")


def main() -> None:
    print("=" * 70)
    print("PROJECT 18 - THE SALES FORECAST BASELINE")
    print("=" * 70)

    # STEP 1 - Load the monthly sales table.
    df = pd.read_csv(DATA / "monthly_sales.csv")
    df["month"] = pd.to_datetime(df["month"] + "-01", errors="coerce")
    df = df.dropna(subset=["month"]).sort_values("month").reset_index(drop=True)
    print(f"\nSTEP 1: loaded {len(df)} months")
    print(df.head(3).to_string(index=False))

    # STEP 2 - Check the series before modelling.
    print("\nSTEP 2: sales summary")
    print(df["sales"].describe().round(2).to_string())

    # STEP 3 - Add a simple time index and a moving average.
    # t = 0, 1, 2 ... lets a linear model learn a trend.
    # rolling(3).mean() smooths short-term noise using the last three months.
    df["t"] = np.arange(len(df))
    df["moving_avg_3"] = df["sales"].rolling(window=3).mean()
    print("\nSTEP 3: added time index and 3-month moving average")

    # STEP 4 - Split into training and test periods.
    # The last six months are held out so we can measure forecast error honestly.
    train = df.iloc[:-6].copy()
    test = df.iloc[-6:].copy()
    print(f"\nSTEP 4: training months = {len(train)}, test months = {len(test)}")
    print(f"Train period: {train['month'].min().date()} to {train['month'].max().date()}")
    print(f"Test period:  {test['month'].min().date()} to {test['month'].max().date()}")

    # STEP 5 - Fit a linear trend on the training period.
    model = LinearRegression()
    model.fit(train[["t"]], train["sales"])
    print(f"\nSTEP 5: fitted linear trend; slope = {model.coef_[0]:.2f} sales per month")

    # STEP 6 - Predict the test period and measure the error.
    test_pred = model.predict(test[["t"]])
    mae = mean_absolute_error(test["sales"], test_pred)
    rmse = np.sqrt(mean_squared_error(test["sales"], test_pred))
    # Naive baseline: predict that next month equals the last training month.
    naive_pred = np.repeat(train["sales"].iloc[-1], len(test))
    naive_mae = mean_absolute_error(test["sales"], naive_pred)
    print("\nSTEP 6: test-set error")
    print(f"Linear trend MAE:  {mae:,.1f}")
    print(f"Linear trend RMSE: {rmse:,.1f}")
    print(f"Naive last-value MAE: {naive_mae:,.1f}")

    # STEP 7 - Forecast the next three months.
    future_t = np.arange(len(df), len(df) + 3).reshape(-1, 1)
    future_pred = model.predict(future_t)
    future_months = pd.date_range(df["month"].max() + pd.DateOffset(months=1), periods=3, freq="MS")
    forecast = pd.DataFrame({"month": future_months, "forecast_sales": future_pred.round(2)})
    forecast.to_csv(OUT / "next_three_months.csv", index=False)
    print("\nSTEP 7: next three months")
    print(forecast.to_string(index=False))

    # STEP 8 - Save the results report.
    results = [
        "SALES FORECAST RESULTS",
        "=" * 60,
        f"Months of history: {len(df)}",
        f"Training months: {len(train)}",
        f"Test months: {len(test)}",
        f"Trend slope: {model.coef_[0]:.2f} sales per month",
        "",
        f"Linear trend MAE:  {mae:,.1f}",
        f"Linear trend RMSE: {rmse:,.1f}",
        f"Naive baseline MAE: {naive_mae:,.1f}",
        "",
        "Next three months:",
        forecast.to_string(index=False),
        "",
        "Why this is a baseline:",
        "A linear trend is simple, fast and easy to explain. It captures direction",
        "but not complex seasonality or sudden changes. A real forecast would be",
        "compared against several baselines and checked with rolling validation.",
    ]
    (OUT / "results.txt").write_text("\n".join(results), encoding="utf-8")
    print("\nSTEP 8: results saved")

    # STEP 9 - Plot history, smoothing and the forecast.
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(df["month"], df["sales"], marker="o", label="Actual sales", color="#1b9e77")
    ax.plot(df["month"], df["moving_avg_3"], linewidth=2, label="3-month moving average", color="#7570b3")
    ax.plot(test["month"], test_pred, marker="o", linestyle="--", label="Linear trend (test)", color="#d95f02")
    ax.plot(forecast["month"], forecast["forecast_sales"], marker="o", linestyle=":", linewidth=2,
            label="Next 3 months", color="#e7298a")
    ax.axvline(test["month"].min(), color="grey", linestyle=":", linewidth=1)
    ax.set_title("Monthly sales and simple forecast")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales ($)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "sales_forecast.png", dpi=140)
    plt.close(fig)

    # STEP 10 - Plot the test-period errors.
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(test["month"], test["sales"], marker="o", label="Actual", color="#1b9e77")
    ax.plot(test["month"], test_pred, marker="o", label="Predicted", color="#d95f02")
    ax.set_title("Actual vs predicted sales in the test period")
    ax.set_xlabel("Month")
    ax.set_ylabel("Sales ($)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT / "test_predictions.png", dpi=140)
    plt.close(fig)

    print("\n" + "\n".join(results))
    print("\nDONE. Check outputs/sales_forecast.png and results.txt.")


if __name__ == "__main__":
    main()
