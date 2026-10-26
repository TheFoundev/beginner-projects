# 05. The Date & Time Fixer

> Parse mixed timestamp formats, remove duplicate events, and build hourly and daily activity summaries.

**Category:** Data Cleaning & Preparation  
**Time:** 30–45 minutes  
**Skills:** datetime parsing, dt accessors, resampling, event aggregation

## The goal

An event log contains timestamps in ISO, US-style and ISO-with-T formats. Turn them into real datetime values, then answer: when are users most active?

## What you will learn

- Load the event log
- Look at the formats
- Parse with format='mixed'
- Remove duplicates and bad times
- Create time parts
- Fill missing durations
- Save the clean event table
- Aggregate by hour
- Aggregate by day
- Plot the patterns

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/events_raw.csv` | 420 rows with three timestamp styles and duplicate event IDs. |
| `data/clean_events.csv` | 400 unique events with date, hour, weekday and month columns. |

`event_id`, `user_id`, `timestamp`, `event_type`, `duration_min`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load the event log

```python
raw = pd.read_csv(DATA / "events_raw.csv")
```

Each row is one user action. The raw timestamp is currently text, so it cannot be sorted or grouped by time yet.

### Step 2 — Look at the formats

```python
print(raw["timestamp"].head(8))
```

Print a few raw timestamps. You should see all three styles side by side.

### Step 3 — Parse with format='mixed'

```python
df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed", errors="coerce")
```

Pandas reads each row in its own format. `errors='coerce'` turns a broken timestamp into `NaT` instead of crashing the whole script.

### Step 4 — Remove duplicates and bad times

```python
df = df.dropna(subset=["timestamp"])
df = df.drop_duplicates(subset=["event_id"], keep="first")
```

Drop rows with no valid timestamp, then keep the first event for each `event_id`.

### Step 5 — Create time parts

```python
df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.day_name()
df["date"] = df["timestamp"].dt.date
```

`dt.hour`, `dt.day_name()` and `dt.date` expose the parts you need for grouping and charts.

### Step 6 — Fill missing durations

```python
df["duration_min"] = df.groupby("event_type")["duration_min"].transform(
    lambda s: s.fillna(s.median())
)
```

A missing duration is filled with the median duration for the same event type, so a purchase is not filled with a view median.

### Step 7 — Save the clean event table

```python
df.to_csv(DATA / "clean_events.csv", index=False)
```

The output contains the original columns plus the new time parts.

### Step 8 — Aggregate by hour

```python
hourly = df.groupby("hour").size()
```

Counting event IDs per hour reveals peak activity periods.

### Step 9 — Aggregate by day

```python
daily = df.set_index("timestamp").resample("D").agg(
    events=("event_id", "count"), active_users=("user_id", "nunique")
)
```

Resampling by day lets you count events and unique active users for each date.

### Step 10 — Plot the patterns

```python
sns.barplot(data=hourly, x="hour", y="events")
```

A bar chart shows the busiest hours; a line chart shows daily active users.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/time_cleaning_report.txt` | Parsing counts, date range and busiest hours. |
| `outputs/hourly_activity.csv` | Event count for every hour. |
| `outputs/hourly_activity.png` | Activity by hour of day. |
| `outputs/daily_activity.csv` | Daily events and unique active users. |
| `outputs/daily_active_users.png` | Daily active-user trend. |

## Try it yourself

- Add a `is_weekend` column and compare average hourly activity on weekends.
- Find the top 10 users by number of events.
- Change the resample frequency from daily to weekly and describe the trade-off.

## Run it

From the pack root:

```bash
python3 projects/05_datetime_events/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

The mixed-format parser is convenient for teaching, but production pipelines should enforce one timestamp format at the source.
