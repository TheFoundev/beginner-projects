# 15. The Delivery Time ANOVA

> Compare delivery times across three warehouses with ANOVA and a Tukey post-hoc test.

**Category:** Statistics & Experiments  
**Time:** 40–55 minutes  
**Skills:** one-way ANOVA, Tukey HSD, eta squared, group comparisons

## The goal

Three warehouses serve the same region. Compare their delivery times, test whether at least one warehouse differs, and identify which pairs differ.

## What you will learn

- Load and check groups
- Summarise the warehouses
- Run one-way ANOVA
- Calculate eta squared
- Run Tukey HSD
- Read the Tukey table
- Write the result
- Plot the distributions
- Plot the means with error bars

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/delivery_times.csv` | 180 orders across warehouses A, B and C. |

`order_id`, `warehouse`, `delivery_days`, `distance_km`, `order_value`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load and check groups

```python
df = pd.read_csv(DATA / "delivery_times.csv")
print(df.groupby("warehouse")["delivery_days"].agg(["count", "mean", "std"]))
```

Count orders and summarise delivery days for each warehouse before testing.

### Step 2 — Summarise the warehouses

```python
summary = df.groupby("warehouse").agg(
    orders=("order_id", "count"),
    avg_delivery_days=("delivery_days", "mean"),
    sd_delivery_days=("delivery_days", "std"),
)
```

A compact table with average delivery time, standard deviation and average distance makes the raw pattern visible.

### Step 3 — Run one-way ANOVA

```python
groups = [g["delivery_days"].values for _, g in df.groupby("warehouse")]
f_stat, p_value = f_oneway(*groups)
```

The null hypothesis is that all three warehouses have the same average delivery time. The F-statistic compares between-group variation with within-group variation.

### Step 4 — Calculate eta squared

```python
eta_squared = ss_between / (ss_between + ss_within)
```

Eta squared is the share of total variation explained by warehouse differences. It is an effect size, not a p-value.

### Step 5 — Run Tukey HSD

```python
tukey = pairwise_tukeyhsd(
    endog=df["delivery_days"], groups=df["warehouse"], alpha=0.05
)
```

ANOVA says “at least one group differs”, not which one. Tukey compares every pair while controlling the family-wise error rate.

### Step 6 — Read the Tukey table

```python
tukey_table = pd.DataFrame(
    tukey.summary().data[1:], columns=tukey.summary().data[0]
)
```

`meandiff` is the difference in means, `p-adj` is the adjusted p-value, and `reject=True` means the pair differs significantly.

### Step 7 — Write the result

```python
print(f"F={f_stat:.3f}, p={p_value:.5f}, eta squared={eta_squared:.3f}")
```

Report F, p, eta squared and the pairwise Tukey comparisons together.

### Step 8 — Plot the distributions

```python
sns.boxplot(data=df, x="warehouse", y="delivery_days")
sns.stripplot(data=df, x="warehouse", y="delivery_days")
```

Boxplots with individual points show the spread, median and outliers for each warehouse.

### Step 9 — Plot the means with error bars

```python
ax.bar(summary.index, summary["avg_delivery_days"],
       yerr=errors, capsize=8)
```

The bar chart summarises the group means and shows uncertainty around each mean.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/warehouse_summary.csv` | Delivery-time summary by warehouse. |
| `outputs/anova_results.txt` | F-test, effect size, Tukey table and interpretation. |
| `outputs/tukey_results.csv` | Pairwise Tukey comparisons. |
| `outputs/delivery_boxplot.png` | Delivery-time distributions by warehouse. |
| `outputs/warehouse_means.png` | Average delivery time with 95% error bars. |

## Try it yourself

- Add `distance_km` as a covariate in a two-way model and see whether the warehouse effect shrinks.
- Compare the ANOVA result with a Kruskal–Wallis test, which does not assume normality.
- Recode delivery time into fast/medium/slow and run a chi-square test by warehouse.

## Run it

From the pack root:

```bash
python3 projects/15_delivery_anova/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

ANOVA assumes independent observations and roughly normal residuals. The boxplot and group sizes help you judge whether that is plausible.
