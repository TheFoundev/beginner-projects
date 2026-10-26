# 09. The City Weather Story

> Turn one year of daily weather into a monthly story about temperature, rain and extreme days.

**Category:** Exploratory Analysis & Visualization  
**Time:** 30–45 minutes  
**Skills:** date grouping, monthly aggregation, time-series charts

## The goal

A city has 365 days of daily weather. Build a monthly summary, identify extreme days, and present the year in a way a non-specialist can understand.

## What you will learn

- Load and parse dates
- Check the ranges
- Create month labels
- Aggregate by month
- Find extreme days
- Plot monthly temperature
- Plot monthly rainfall
- Plot the temperature distribution
- Write the weather story

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/weather_daily.csv` | 365 daily rows with temperature, rainfall, humidity and wind. |

`date`, `temp_max_c`, `temp_min_c`, `rainfall_mm`, `humidity_percent`, `wind_kmh`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load and parse dates

```python
df = pd.read_csv(DATA / "weather_daily.csv")
df["date"] = pd.to_datetime(df["date"])
```

A real date column allows grouping by calendar month and finding extreme days.

### Step 2 — Check the ranges

```python
print(df[["temp_max_c", "rainfall_mm"]].describe())
```

Are temperatures plausible? Is rainfall ever negative? A quick `describe()` catches data-entry problems.

### Step 3 — Create month labels

```python
df["month"] = df["date"].dt.to_period("M")
df["month_label"] = df["date"].dt.strftime("%b")
```

`dt.to_period('M')` groups by calendar month. `dt.strftime('%b')` creates short labels such as `Jan` for charts.

### Step 4 — Aggregate by month

```python
monthly = df.groupby(["month", "month_label"]).agg(
    avg_max_c=("temp_max_c", "mean"),
    total_rain_mm=("rainfall_mm", "sum"),
)
```

For each month, calculate average high, average low, total rain, rainy days and average humidity.

### Step 5 — Find extreme days

```python
hottest = df.loc[df["temp_max_c"].idxmax()]
coldest = df.loc[df["temp_min_c"].idxmin()]
```

`idxmax()` and `idxmin()` return the row labels of the hottest, coldest and wettest days.

### Step 6 — Plot monthly temperature

```python
ax.plot(monthly["month_label"], monthly["avg_max_c"], marker="o")
```

Two lines on one chart show the average high and average low across the year.

### Step 7 — Plot monthly rainfall

```python
ax.bar(monthly["month_label"], monthly["total_rain_mm"])
```

A bar chart is a good choice for totals because each month is a separate quantity.

### Step 8 — Plot the temperature distribution

```python
sns.histplot(df["temp_max_c"], bins=24, kde=True)
```

A histogram shows how many days fell into each temperature band, not just the monthly average.

### Step 9 — Write the weather story

```python
monthly.loc[monthly["avg_max_c"].idxmax(), "month_label"]
```

Save the warmest month, wettest month, hottest day, coldest day and rainy-day count in a text file.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/monthly_weather.csv` | Monthly temperature, rainfall and humidity summary. |
| `outputs/monthly_temperature.png` | Average high and low by month. |
| `outputs/monthly_rainfall.png` | Total rainfall by month. |
| `outputs/temperature_distribution.png` | Distribution of daily high temperatures. |
| `outputs/insights.txt` | Extreme days and the main seasonal findings. |

## Try it yourself

- Add a `season` column using month numbers and compare average rainfall by season.
- Find the longest run of consecutive rainy days.
- Plot humidity against rainfall and describe the relationship.

## Run it

From the pack root:

```bash
python3 projects/09_weather_story/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

Monthly averages hide daily extremes. Report both when the decision depends on unusual days.
