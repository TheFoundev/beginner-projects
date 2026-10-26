# 18. The Sales Forecast Baseline

> Build a simple sales forecast with a moving average and a linear trend, then test it on the last six months.

**Category:** Business Analytics & Prediction  
**Time:** 40–55 minutes  
**Skills:** time index, moving average, train/test split, MAE, RMSE

## The goal

A business has 36 months of sales. Build an explainable baseline, measure its error on a holdout period, and forecast the next three months.

## What you will learn

- Load and parse the month
- Create a time index
- Add a moving average
- Hold out the last six months
- Fit a linear trend
- Predict and measure error
- Compare with a naive baseline
- Forecast the next three months
- Plot the forecast
- Explain the limitation

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/monthly_sales.csv` | 36 monthly sales values from 2023 through 2025. |

`month`, `sales`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load and parse the month

```python
df = pd.read_csv(DATA / "monthly_sales.csv")
df["month"] = pd.to_datetime(df["month"] + "-01")
```

The month is stored as `YYYY-MM`. Appending `-01` and parsing gives a real date that can be sorted and plotted.

### Step 2 — Create a time index

```python
df["t"] = np.arange(len(df))
```

A linear model needs a number, not a date. `t = 0, 1, 2, ...` represents the passage of time.

### Step 3 — Add a moving average

```python
df["moving_avg_3"] = df["sales"].rolling(window=3).mean()
```

`rolling(3).mean()` smooths short-term noise using the current month and the two before it.

### Step 4 — Hold out the last six months

```python
train = df.iloc[:-6]
test = df.iloc[-6:]
```

The model trains on the first 30 months and is tested on the last 6. The test period must come after the training period, never before.

### Step 5 — Fit a linear trend

```python
model = LinearRegression()
model.fit(train[["t"]], train["sales"])
```

`LinearRegression` finds the straight line that minimises squared error between the time index and sales.

### Step 6 — Predict and measure error

```python
test_pred = model.predict(test[["t"]])
mae = mean_absolute_error(test["sales"], test_pred)
rmse = np.sqrt(mean_squared_error(test["sales"], test_pred))
```

MAE is the average absolute miss in sales dollars. RMSE penalises larger misses more heavily.

### Step 7 — Compare with a naive baseline

```python
naive_pred = np.repeat(train["sales"].iloc[-1], len(test))
naive_mae = mean_absolute_error(test["sales"], naive_pred)
```

A forecast is only useful if it beats a simple benchmark. The naive forecast repeats the last training value for every future month.

### Step 8 — Forecast the next three months

```python
future_t = np.arange(len(df), len(df) + 3).reshape(-1, 1)
future_pred = model.predict(future_t)
```

Extend the time index beyond the observed data and use the fitted line to predict.

### Step 9 — Plot the forecast

```python
ax.plot(df["month"], df["sales"], label="Actual")
ax.plot(forecast["month"], forecast["forecast_sales"], label="Forecast")
```

The chart shows history, the moving average, the test predictions and the future forecast on the same timeline.

### Step 10 — Explain the limitation

```python
results.append("A linear trend does not capture seasonality.")
```

A linear trend captures direction but not seasonality or sudden shocks. The report states this explicitly.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/results.txt` | MAE, RMSE, naive baseline, trend slope and forecast. |
| `outputs/next_three_months.csv` | Forecast values for the next three months. |
| `outputs/sales_forecast.png` | History, moving average, test predictions and future forecast. |
| `outputs/test_predictions.png` | Actual versus predicted sales in the test period. |

## Try it yourself

- Add month-of-year dummy variables and compare test MAE with the plain trend.
- Use a 6-month moving average instead of 3 and describe the trade-off.
- Evaluate with rolling-origin validation instead of a single holdout.

## Run it

From the pack root:

```bash
python3 projects/18_sales_forecast/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

A more complex model is not automatically better. Always compare against a naive baseline and report the error in the original units.
