# 20. The Pricing & Demand Analyzer

> Estimate price elasticity with a log-log regression and simulate how demand changes when price moves.

**Category:** Business Analytics & Prediction  
**Time:** 45–60 minutes  
**Skills:** log-log regression, elasticity, OLS, simulation, causal caution

## The goal

A business has monthly price, quantity, promotion and competitor-price data for five products. Estimate how sensitive demand is to price and simulate a price change.

## What you will learn

- Load and check positivity
- Create log variables
- Fit the main regression
- Read the elasticity
- Check significance and fit
- Fit separate models per product
- Simulate a demand curve
- Plot the demand curve
- Plot elasticity by product
- Write the causal caveat

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/pricing_data.csv` | 120 product-month rows: 5 products × 24 months. |

`product`, `month`, `price`, `quantity`, `promotion`, `competitor_price`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load and check positivity

```python
df = pd.read_csv(DATA / "pricing_data.csv")
print((df["price"] <= 0).sum(), (df["quantity"] <= 0).sum())
```

Logs require positive values. Check price and quantity before transforming them.

### Step 2 — Create log variables

```python
df["log_quantity"] = np.log(df["quantity"])
df["log_price"] = np.log(df["price"])
df["log_competitor_price"] = np.log(df["competitor_price"])
```

`np.log` compresses multiplicative relationships into additive ones. In a log-log model, the price coefficient is an elasticity.

### Step 3 — Fit the main regression

```python
X = sm.add_constant(df[["log_price", "promotion", "log_competitor_price"]])
model = sm.OLS(df["log_quantity"], X).fit()
```

`sm.add_constant` adds the intercept. Control for promotion and competitor price so the price coefficient is not contaminated by those effects.

### Step 4 — Read the elasticity

```python
elasticity = model.params["log_price"]
```

The coefficient on `log_price` is the estimated percentage change in quantity for a 1% change in price. Values below -1 are elastic; between -1 and 0 are inelastic.

### Step 5 — Check significance and fit

```python
print(model.pvalues["log_price"], model.rsquared)
```

The p-value tests whether the elasticity is different from zero. R-squared shows how much of the variation the model explains.

### Step 6 — Fit separate models per product

```python
for product, group in df.groupby("product"):
    m = sm.OLS(group["log_quantity"], sm.add_constant(
        group[["log_price", "promotion", "log_competitor_price"]]
    )).fit()
```

Pooling products can hide different customer responses. A per-product loop estimates a separate elasticity for each one.

### Step 7 — Simulate a demand curve

```python
simulation["predicted_quantity"] = np.exp(product_model.predict(sim_X))
```

Hold promotion off and competitor price at its average, then vary price across a range. `exp(prediction)` converts log quantity back to units.

### Step 8 — Plot the demand curve

```python
ax.plot(simulation["price"], simulation["predicted_quantity"])
ax.scatter(product_df["price"], product_df["quantity"])
```

The observed points show the raw months; the line shows the model's predicted demand at each price.

### Step 9 — Plot elasticity by product

```python
ax.axvline(-1, color="grey", linestyle="--")
```

A sorted bar chart with a reference line at -1 makes it easy to see which products are most price-sensitive.

### Step 10 — Write the causal caveat

```python
results.append("This is an observational model, not a pricing experiment.")
```

The regression is observational. It describes association, not proof that changing price will cause exactly that quantity change.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/results.txt` | Regression coefficients, elasticity, p-values and interpretation. |
| `outputs/elasticity_by_product.csv` | Elasticity, p-value and R-squared for each product. |
| `outputs/coffee_price_simulation.csv` | Predicted quantity at 25 simulated coffee prices. |
| `outputs/demand_curve.png` | Observed coffee points plus the simulated demand curve. |
| `outputs/elasticity_by_product.png` | Elasticity comparison with the -1 reference line. |

## Try it yourself

- Add `month` as a categorical control and see whether the elasticity changes.
- Simulate a 10% price increase and calculate the predicted revenue change.
- Run the model without `log_competitor_price` and explain why the price coefficient may shift.

## Run it

From the pack root:

```bash
python3 projects/20_pricing_elasticity/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

The cleanest way to learn the causal effect of price is a controlled experiment or a natural experiment, not a single observational regression.
