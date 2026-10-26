# 07. The Coffee Shop Morning Rush

> Find the busiest hours, compare channels, and measure average order value.

**Category:** Exploratory Analysis & Visualization  
**Time:** 35–50 minutes  
**Skills:** derived revenue, pivot_table, heatmaps, AOV

## The goal

A café wants to staff the right hours and understand whether mobile orders are worth the same as walk-in orders. Build an hourly and channel view of the business.

## What you will learn

- Load and parse timestamps
- Check quantity and price
- Create revenue and time fields
- Summarise by hour
- Compare channels
- Build an hour × weekday table
- Plot the hourly revenue
- Plot the heatmap
- Write the staffing insight

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/coffee_orders.csv` | 800 orders over 14 days, with item, price, channel and timestamp. |

`order_id`, `timestamp`, `item`, `category`, `quantity`, `unit_price`, `channel`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load and parse timestamps

```python
df = pd.read_csv(DATA / "coffee_orders.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
```

The timestamp is text until parsed. Sorting and hour extraction require a real datetime.

### Step 2 — Check quantity and price

```python
print(df[["quantity", "unit_price"]].describe())
```

A quick `describe()` catches impossible values before they affect revenue.

### Step 3 — Create revenue and time fields

```python
df["total"] = df["quantity"] * df["unit_price"]
df["hour"] = df["timestamp"].dt.hour
df["weekday"] = df["timestamp"].dt.day_name()
```

`total = quantity × unit_price` is the order line value. `dt.hour` and `dt.day_name()` create the grouping keys.

### Step 4 — Summarise by hour

```python
hourly = df.groupby("hour").agg(
    orders=("order_id", "count"),
    revenue=("total", "sum"),
)
```

Count orders and sum revenue per hour. Average order value is total revenue divided by order count.

### Step 5 — Compare channels

```python
channel = df.groupby("channel").agg(
    orders=("order_id", "count"),
    revenue=("total", "sum"),
    avg_order_value=("total", "mean"),
)
```

The same aggregation by channel answers whether mobile customers spend more or less per order.

### Step 6 — Build an hour × weekday table

```python
heat = df.pivot_table(index="weekday", columns="hour",
                       values="total", aggfunc="sum", fill_value=0)
```

`pivot_table` makes a two-dimensional table: weekdays as rows, hours as columns, revenue as the cell value. That is exactly the shape a heatmap needs.

### Step 7 — Plot the hourly revenue

```python
ax.plot(hourly["hour"], hourly["revenue"], marker="o")
```

The line chart makes the morning peak and afternoon dip easy to see.

### Step 8 — Plot the heatmap

```python
sns.heatmap(heat, cmap="YlGnBu")
```

Colour intensity shows the strongest weekday-hour combinations. This is useful for shift planning.

### Step 9 — Write the staffing insight

```python
peak_hour = hourly.sort_values("revenue", ascending=False).iloc[0]
```

State the peak hour, the best channel and the overall average order value in a text file.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/hourly_summary.csv` | Orders, revenue and AOV for each hour. |
| `outputs/channel_summary.csv` | Orders, revenue and AOV by channel. |
| `outputs/hour_weekday_heatmap.csv` | The revenue table behind the heatmap. |
| `outputs/hourly_revenue.png` | Revenue by hour. |
| `outputs/hour_weekday_heatmap.png` | Weekday × hour revenue heatmap. |
| `outputs/channel_aov.png` | Average order value by channel. |
| `outputs/insights.txt` | Peak hour and channel findings. |

## Try it yourself

- Add a `is_weekend` flag and compare average order value on weekdays versus weekends.
- Find the top three items by revenue, not by order count.
- Create a second heatmap using order count instead of revenue.

## Run it

From the pack root:

```bash
python3 projects/07_coffee_rush/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

A heatmap is just a table with colour. Always keep the underlying CSV so the chart can be checked.
