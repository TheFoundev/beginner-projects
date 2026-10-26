# 11. The A/B Test Lab

> Compare two landing-page variants with a two-proportion z-test and a confidence interval.

**Category:** Statistics & Experiments  
**Time:** 40–55 minutes  
**Skills:** conversion rates, z-test, confidence intervals, practical significance

## The goal

Variant A and variant B were shown to different users. Decide whether B really converts better, or whether the difference could easily be random noise.

## What you will learn

- Load and inspect
- Calculate conversion rates
- Calculate the lift
- Run the z-test
- Build a 95% confidence interval
- Check revenue per user
- Write the decision report
- Plot rates with error bars

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/ab_test.csv` | 3,000 users, split evenly between variants A and B, with conversion and revenue. |

`user_id`, `group`, `converted`, `revenue`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load and inspect

```python
df = pd.read_csv(DATA / "ab_test.csv")
print(df.groupby("group").size())
```

Check group sizes and the conversion column. A balanced experiment is easier to compare.

### Step 2 — Calculate conversion rates

```python
summary = df.groupby("group").agg(
    users=("user_id", "count"),
    conversions=("converted", "sum"),
)
summary["conversion_rate"] = summary["conversions"] / summary["users"]
```

For each group, divide conversions by users. This is the basic metric the test compares.

### Step 3 — Calculate the lift

```python
diff = b["conversion_rate"] - a["conversion_rate"]
relative_lift = diff / a["conversion_rate"]
```

The absolute difference is B minus A. The relative lift divides that difference by A's rate.

### Step 4 — Run the z-test

```python
z_stat, p_value = proportions_ztest(
    [b["conversions"], a["conversions"]],
    [b["users"], a["users"]],
    alternative="two-sided",
)
```

`proportions_ztest` tests the null hypothesis that both groups have the same true conversion rate. The p-value measures how surprising the observed difference would be under that null.

### Step 5 — Build a 95% confidence interval

```python
se = np.sqrt(pA * (1 - pA) / nA + pB * (1 - pB) / nB)
ci_low, ci_high = diff - 1.96 * se, diff + 1.96 * se
```

The interval estimates a plausible range for the true difference. If it excludes zero, the result is statistically significant at the 5% level.

### Step 6 — Check revenue per user

```python
summary["revenue_per_user"] = summary["revenue"] / summary["users"]
```

A higher conversion rate is not automatically better if the revenue per user is worse. Always connect the metric to the business outcome.

### Step 7 — Write the decision report

```python
verdict = "statistically significant" if p_value < 0.05 else "not statistically significant"
```

Save the rates, difference, lift, z-statistic, p-value, confidence interval and a plain-English verdict.

### Step 8 — Plot rates with error bars

```python
ax.bar(groups, rates, yerr=errors, capsize=8)
```

The error bars show uncertainty around each group's conversion rate. Overlapping bars are a visual warning that the difference may be noisy.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/ab_test_results.txt` | Full statistical result and interpretation. |
| `outputs/conversion_rates.png` | Conversion rate by variant with 95% error bars. |
| `outputs/revenue_per_user.png` | Revenue per user by variant. |

## Try it yourself

- Re-run the test with a one-sided alternative and explain when that is appropriate.
- Split the data by revenue quartile and compare conversion within each quartile.
- Change the significance level to 1% and see whether the verdict changes.

## Run it

From the pack root:

```bash
python3 projects/11_ab_test/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

Statistical significance is not the same as business importance. A tiny lift can be significant with a huge sample and still not be worth shipping.
