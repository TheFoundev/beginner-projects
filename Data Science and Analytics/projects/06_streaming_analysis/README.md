# 06. The Streaming Showdown

> Compare genres and shows by watch time and completion rate, then show the weekly viewing pattern.

**Category:** Exploratory Analysis & Visualization  
**Time:** 35–50 minutes  
**Skills:** groupby, aggregation, rates, categorical charts

## The goal

A streaming service wants to know which genres hold attention. Total minutes show popularity; completion rate shows whether viewers finish what they start.

## What you will learn

- Load and parse the date
- Check the data
- Add a weekday label
- Summarise by genre
- Summarise by show
- Summarise by weekday
- Chart volume and completion
- Write the insight file

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/streaming_viewing.csv` | 700 viewing records across 120 users, 5 genres and 30 days. |

`user_id`, `date`, `show`, `genre`, `minutes_watched`, `completed`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load and parse the date

```python
df = pd.read_csv(DATA / "streaming_viewing.csv")
df["date"] = pd.to_datetime(df["date"])
```

The date column is text until you convert it with `pd.to_datetime`. After that, `.dt` accessors and weekday grouping work.

### Step 2 — Check the data

```python
print(df.dtypes)
print(df["minutes_watched"].describe())
```

Look at dtypes, missing values and the range of `minutes_watched`. A clean dataset still deserves a quick sanity check.

### Step 3 — Add a weekday label

```python
df["weekday"] = pd.Categorical(df["date"].dt.day_name(), categories=WEEK_ORDER, ordered=True)
```

`dt.day_name()` creates labels such as `Monday`. An ordered category keeps charts in calendar order instead of alphabetical order.

### Step 4 — Summarise by genre

```python
summary = df.groupby("genre").agg(
    total_minutes=("minutes_watched", "sum"),
    avg_minutes=("minutes_watched", "mean"),
    completion_rate=("completed", "mean"),
)
```

`agg` can compute several statistics at once. Total minutes measure volume; mean minutes measure depth; mean of `completed` is a completion rate because the column is 0/1.

### Step 5 — Summarise by show

```python
shows = df.groupby(["genre", "show"]).agg(
    total_minutes=("minutes_watched", "sum"),
    completion_rate=("completed", "mean"),
)
```

A second groupby at the show level finds individual hits that may be hidden inside a genre total.

### Step 6 — Summarise by weekday

```python
weekday = df.groupby("weekday", observed=True).agg(
    total_minutes=("minutes_watched", "sum"),
)
```

Grouping by the ordered weekday category shows whether viewing rises on weekends.

### Step 7 — Chart volume and completion

```python
summary["total_minutes"].sort_values().plot(kind="barh")
```

A horizontal bar chart is easy to read for named categories. A second chart shows that the most-watched genre is not always the most-completed genre.

### Step 8 — Write the insight file

```python
top_genre = summary.index[0]
(OUT / "insights.txt").write_text(f"Most-watched genre: {top_genre}")
```

A short text file forces you to state the finding in plain English, not just produce a chart.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/genre_summary.csv` | Total minutes, average minutes, completion rate and views by genre. |
| `outputs/show_summary.csv` | The same measures at show level. |
| `outputs/weekday_summary.csv` | Viewing volume by weekday. |
| `outputs/genre_watch_time.png` | Genre popularity by total minutes. |
| `outputs/genre_completion.png` | Completion rate by genre. |
| `outputs/weekday_viewing.png` | Viewing by day of week. |
| `outputs/insights.txt` | Plain-English summary of the main findings. |

## Try it yourself

- Find the show with the highest completion rate among shows with at least 30 views.
- Compare average minutes for completed versus unfinished views.
- Add a stacked bar showing minutes by genre for each weekday.

## Run it

From the pack root:

```bash
python3 projects/06_streaming_analysis/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

Popularity and quality are different questions. Always report both volume and rate.
