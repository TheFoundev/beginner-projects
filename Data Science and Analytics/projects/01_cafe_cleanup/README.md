# 01. The Messy Café Menu

> Turn a deliberately messy order log into a clean revenue table.

**Category:** Data Cleaning & Preparation  
**Time:** 30–45 minutes  
**Skills:** pandas, missing values, duplicates, dates, text cleaning

## The goal

A café exports orders from three different systems. Dates, item names, categories, quantities and prices are inconsistent. Your job is to make one clean table that a manager could actually use.

## What you will learn

- Load the raw file
- Measure the mess before changing it
- Standardise text
- Parse the dates
- Rebuild category from item
- Repair quantity
- Repair unit price
- Create the order total
- Remove duplicates and bad dates
- Save and audit
- Visualise the result

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/cafe_orders_raw.csv` | The messy input: 118 rows, 7 columns. |
| `data/cafe_orders_clean.csv` | The cleaned output written by `main.py`. |

`order_id`, `date`, `item`, `category`, `quantity`, `unit_price`, `customer_type`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load the raw file

```python
df = pd.read_csv(DATA / "cafe_orders_raw.csv")
```

`pd.read_csv` turns the CSV into a DataFrame. A DataFrame is a table with named columns and numbered rows.

### Step 2 — Measure the mess before changing it

```python
print(df.isna().sum())
print(df.duplicated(subset=["order_id"]).sum())
```

`isna().sum()` counts empty cells. `duplicated(subset=['order_id']).sum()` counts repeated order IDs. Always record the “before” numbers so you can prove what changed.

### Step 3 — Standardise text

```python
df["item"] = df["item"].str.strip().str.title()
```

`str.strip()` removes accidental spaces. `str.title()` converts `LATTE`, `latte` and ` Latte ` into `Latte`. This makes grouping reliable.

### Step 4 — Parse the dates

```python
df["date"] = pd.to_datetime(df["date"], format="mixed", errors="coerce")
```

The file mixes `2025-01-05`, `Jan 05, 2025` and `05-Jan-2025`. `pd.to_datetime(..., format="mixed")` reads each row in its own format.

### Step 5 — Rebuild category from item

```python
df["category"] = df["item"].map(item_to_category)
```

The original category column is unreliable. A dictionary maps each known item to `Drink` or `Food`, which is a safer rule.

### Step 6 — Repair quantity

```python
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df.loc[df["quantity"] <= 0, "quantity"] = np.nan
df["quantity"] = df["quantity"].fillna(df["quantity"].median()).astype(int)
```

`pd.to_numeric` converts numbers stored as text and turns bad text into `NaN`. A quantity of zero or less is impossible, so it becomes missing and is filled with the median.

### Step 7 — Repair unit price

```python
df["unit_price"] = df["unit_price"].astype(str).str.replace("$", "", regex=False)
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
df["unit_price"] = df.groupby("item")["unit_price"].transform(
    lambda s: s.fillna(s.median())
)
```

Prices arrive as `4.50`, `$4.50` and blank. Remove the dollar sign, convert to a number, then fill each missing price with the median price for that same item.

### Step 8 — Create the order total

```python
df["total"] = (df["quantity"] * df["unit_price"]).round(2)
```

Revenue per row is `quantity × unit_price`. This is called a derived column: it did not exist in the raw file.

### Step 9 — Remove duplicates and bad dates

```python
df = df.dropna(subset=["date"])
df = df.drop_duplicates(subset=["order_id"], keep="first")
```

`drop_duplicates(subset=['order_id'], keep='first')` keeps one row per order. `dropna(subset=['date'])` removes rows with an unreadable date.

### Step 10 — Save and audit

```python
df.to_csv(DATA / "cafe_orders_clean.csv", index=False)
```

Write the clean CSV, then save a text report with row counts, missing counts, revenue and the repair actions.

### Step 11 — Visualise the result

```python
df.groupby("item")["total"].sum().sort_values().plot(kind="barh")
```

A missing-value bar chart documents the starting point. A revenue-by-item chart shows that the clean table is useful.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/cleaning_report.txt` | Before/after row counts, missing cells, duplicate count, total revenue. |
| `outputs/missing_before.png` | Which columns had empty cells before cleaning. |
| `outputs/revenue_by_item.png` | Revenue per menu item after cleaning. |
| `outputs/daily_revenue.png` | Daily revenue over the two-month period. |

## Try it yourself

- Fill missing prices with the mean instead of the median and compare the total revenue.
- Add a `weekday` column with `df['date'].dt.day_name()` and chart revenue by weekday.
- Change `keep='first'` to `keep='last'` and explain why the result might differ.

## Run it

From the pack root:

```bash
python3 projects/01_cafe_cleanup/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

This project intentionally starts with dirty data. The clean file is the deliverable, not the raw file.
