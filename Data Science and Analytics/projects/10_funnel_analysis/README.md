# 10. The E-Commerce Funnel

> Measure how visitors move from a visit to a purchase, then compare acquisition channels.

**Category:** Exploratory Analysis & Visualization  
**Time:** 35–50 minutes  
**Skills:** funnel conversion, rates, grouped aggregation, charts

## The goal

An online store records visits, product views, add-to-carts and purchases by channel. Find where the biggest drop-off happens and which channel converts best.

## What you will learn

- Load and parse the date
- Check the funnel order
- Calculate step conversion rates
- Build the overall funnel
- Compare channels
- Chart the funnel
- Chart final conversion by channel
- Plot the daily trend
- Write the funnel insight

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/funnel_events.csv` | 360 rows: 90 days × 4 acquisition channels. |

`date`, `channel`, `visits`, `product_views`, `add_to_carts`, `purchases`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load and parse the date

```python
df = pd.read_csv(DATA / "funnel_events.csv")
df["date"] = pd.to_datetime(df["date"])
```

The daily table is already aggregated by channel, so each row is a day-channel combination rather than a single user.

### Step 2 — Check the funnel order

```python
ordered = ((df["visits"] >= df["product_views"]) &
           (df["product_views"] >= df["add_to_carts"]) &
           (df["add_to_carts"] >= df["purchases"]))
```

Each stage should be no larger than the previous one. A broken order means the data needs investigation.

### Step 3 — Calculate step conversion rates

```python
df["view_rate"] = df["product_views"] / df["visits"]
df["cart_rate"] = df["add_to_carts"] / df["product_views"]
df["purchase_rate"] = df["purchases"] / df["add_to_carts"]
```

A conversion rate is the next stage divided by the previous stage. Keep the overall visit-to-purchase rate as a separate measure.

### Step 4 — Build the overall funnel

```python
overall = df[STAGES].sum()
```

Sum each stage across every day and channel. The share of visits shows how much of the original audience remains.

### Step 5 — Compare channels

```python
channel = df.groupby("channel")[STAGES].sum()
```

Group by channel and recompute the rates. A channel can bring many visits but convert poorly, or bring few visits and convert well.

### Step 6 — Chart the funnel

```python
ax.barh(overall_table["stage"], overall_table["count"])
```

A horizontal bar chart with four stages makes the drop-off visible. Label each bar with the count.

### Step 7 — Chart final conversion by channel

```python
channel["visit_to_purchase"].sort_values().plot(kind="barh")
```

A sorted bar chart makes the best and worst channels easy to compare.

### Step 8 — Plot the daily trend

```python
daily["visit_to_purchase"] = daily["purchases"] / daily["visits"]
```

A line chart checks whether conversion is stable over time or driven by a few unusual days.

### Step 9 — Write the funnel insight

```python
biggest_drop = overall_table.loc[overall_table["step_conversion"].idxmin(), "stage"]
```

Identify the smallest step conversion and the best final channel in a text file.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/overall_funnel.csv` | Stage counts, share of visits and step conversion. |
| `outputs/channel_funnel.csv` | The same funnel metrics by channel. |
| `outputs/funnel_chart.png` | Overall funnel with labelled counts. |
| `outputs/channel_conversion.png` | Visit-to-purchase rate by channel. |
| `outputs/daily_conversion.png` | Daily conversion trend. |
| `outputs/insights.txt` | Biggest drop-off and best channel. |

## Try it yourself

- Calculate revenue per visit if you add an `average_order_value` column.
- Compare weekday and weekend conversion rates.
- Find the channel with the largest absolute drop from product view to cart.

## Run it

From the pack root:

```bash
python3 projects/10_funnel_analysis/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

A high final conversion rate can still mean few purchases if the channel brings very little traffic. Always show volume next to rate.
