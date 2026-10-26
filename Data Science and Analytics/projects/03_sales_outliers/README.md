# 03. The Sales Data Detective

> Find impossible sales values and statistical outliers, repair them, and compare daily with weekly trends.

**Category:** Data Cleaning & Preparation  
**Time:** 35–50 minutes  
**Skills:** IQR rule, median imputation, resampling, before/after charts

## The goal

Three stores report daily sales. The file contains negative revenue, missing days and a few enormous values. Decide what is invalid, repair it carefully, and summarise the business trend.

## What you will learn

- Load and sort
- Describe the values
- Mark negative sales as missing
- Calculate IQR bounds
- Replace outliers with the store median
- Aggregate to weeks
- Save the clean data and report
- Compare before and after
- Chart the trend

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/daily_sales_raw.csv` | 360 rows: 3 stores × 120 days, with injected bad values. |
| `data/clean_daily_sales.csv` | The repaired daily table. |
| `outputs/weekly_sales.csv` | Weekly totals by store. |

`date`, `store`, `sales`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load and sort

```python
raw = pd.read_csv(DATA / "daily_sales_raw.csv")
raw["date"] = pd.to_datetime(raw["date"])
raw = raw.sort_values(["store", "date"])
```

Parse the date, drop unreadable dates, and sort by store and date so the time order is clear.

### Step 2 — Describe the values

```python
print(raw["sales"].describe())
```

`describe()` shows the minimum, maximum and quartiles. A negative minimum or a maximum many times larger than the 75th percentile is a warning sign.

### Step 3 — Mark negative sales as missing

```python
df.loc[df["sales"] < 0, "sales"] = np.nan
```

Revenue cannot be negative in this dataset, so a negative row is not a usable observation.

### Step 4 — Calculate IQR bounds

```python
q1 = df.groupby("store")["sales"].transform(lambda s: s.quantile(0.25))
q3 = df.groupby("store")["sales"].transform(lambda s: s.quantile(0.75))
iqr = q3 - q1
outliers = (df["sales"] < q1 - 1.5 * iqr) | (df["sales"] > q3 + 1.5 * iqr)
```

For each store, Q1 and Q3 split the middle 50% of values. The IQR is Q3 − Q1. Values beyond 1.5 × IQR from the box are flagged.

### Step 5 — Replace outliers with the store median

```python
df.loc[outliers, "sales"] = np.nan
df["sales"] = df["sales"].fillna(df.groupby("store")["sales"].transform("median"))
```

The median is robust: one extreme value does not drag it around. Replace flagged values with the median for that same store.

### Step 6 — Aggregate to weeks

```python
df["week"] = df["date"].dt.to_period("W").dt.start_time
weekly = df.groupby(["week", "store"])["sales"].sum()
```

`dt.to_period('W')` groups dates into weeks. Summing sales per week turns noisy daily data into a smoother business signal.

### Step 7 — Save the clean data and report

```python
df.to_csv(DATA / "clean_daily_sales.csv", index=False)
```

Keep both the cleaned daily rows and the weekly summary. The report records how many values were repaired.

### Step 8 — Compare before and after

```python
sns.boxplot(data=raw, x="store", y="sales")
```

Two boxplots make the effect of the repair visible. The before panel shows the extreme values; the after panel shows a usable range.

### Step 9 — Chart the trend

```python
ax.plot(weekly["week"], weekly["sales"], marker="o")
```

A daily line chart shows seasonality; a weekly line chart shows the bigger direction.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/outlier_report.txt` | Counts of negative, missing and IQR-flagged values plus clean totals. |
| `outputs/outliers_before_after.png` | Side-by-side boxplots before and after repair. |
| `outputs/daily_trend.png` | Daily sales by store after cleaning. |
| `outputs/weekly_trend.png` | Total weekly sales. |
| `outputs/weekly_sales.csv` | Weekly totals by store. |

## Try it yourself

- Change 1.5 × IQR to 3.0 × IQR and count how many outliers remain.
- Compare median imputation with dropping the bad rows. Which changes the weekly total more?
- Add a 7-day rolling average to the daily chart.

## Run it

From the pack root:

```bash
python3 projects/03_sales_outliers/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

Outlier rules are judgement calls. The code documents the rule so a reviewer can disagree with it and re-run the analysis.
