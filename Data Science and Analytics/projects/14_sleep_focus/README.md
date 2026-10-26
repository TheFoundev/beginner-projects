# 14. The Sleep & Focus Correlation

> Measure whether sleep, caffeine and screen time move together with focus.

**Category:** Statistics & Experiments  
**Time:** 30–45 minutes  
**Skills:** Pearson correlation, Spearman correlation, regression plots

## The goal

Students recorded sleep, caffeine, screen time and focus. Measure the relationships, separate correlation from causation, and present the evidence honestly.

## What you will learn

- Load and inspect
- Calculate the correlation matrix
- Test sleep versus focus
- Add Spearman correlation
- Check the other variables
- Interpret the strength
- Plot sleep versus focus
- Plot the correlation heatmap
- Write the caveat

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/sleep_focus.csv` | 150 students with sleep, focus, caffeine and screen time. |

`student_id`, `sleep_hours`, `focus_score`, `caffeine_mg`, `screen_time_hours`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load and inspect

```python
df = pd.read_csv(DATA / "sleep_focus.csv")
print(df.describe())
```

Check ranges and missing values. Correlations can be distorted by impossible values such as 30 hours of sleep.

### Step 2 — Calculate the correlation matrix

```python
corr = df.drop(columns=["student_id"]).corr(method="pearson")
```

A matrix shows every pairwise Pearson correlation at once. Read the `focus_score` column for the main relationships.

### Step 3 — Test sleep versus focus

```python
r_value, p_value = pearsonr(df["sleep_hours"], df["focus_score"])
```

`pearsonr` returns the correlation and a p-value for the null hypothesis of no linear relationship.

### Step 4 — Add Spearman correlation

```python
rho_value, rho_p = spearmanr(df["sleep_hours"], df["focus_score"])
```

Spearman works on ranks. It is useful when the relationship is monotonic but not perfectly linear, or when there are outliers.

### Step 5 — Check the other variables

```python
for column in ["caffeine_mg", "screen_time_hours"]:
    r, p = pearsonr(df[column], df["focus_score"])
```

Repeat the Pearson test for caffeine and screen time. Report all relationships, not just the one that supports your story.

### Step 6 — Interpret the strength

```python
strength = "strong" if abs(r_value) >= 0.7 else "moderate" if abs(r_value) >= 0.4 else "weak"
```

A rough guide: |r| below 0.4 is weak, 0.4–0.7 is moderate, and above 0.7 is strong. The sign gives the direction.

### Step 7 — Plot sleep versus focus

```python
sns.regplot(data=df, x="sleep_hours", y="focus_score")
```

`regplot` adds a linear trend line to the scatterplot. It makes the direction visible without hiding the individual points.

### Step 8 — Plot the correlation heatmap

```python
sns.heatmap(corr, annot=True, cmap="RdBu_r", vmin=-1, vmax=1)
```

The heatmap gives a quick overview of all pairwise relationships and makes the strongest cells easy to spot.

### Step 9 — Write the caveat

```python
results.append("Correlation does not prove causation.")
```

State the correlation, the p-value and the fact that correlation does not prove causation.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/correlation_matrix.csv` | Pearson correlations for all numeric columns. |
| `outputs/results.txt` | Pearson and Spearman results plus interpretation and caveats. |
| `outputs/sleep_focus_scatter.png` | Sleep hours versus focus with a trend line. |
| `outputs/correlation_heatmap.png` | Full correlation heatmap. |
| `outputs/screen_focus_scatter.png` | Screen time versus focus. |

## Try it yourself

- Filter to students with less than 200 mg of caffeine and recompute the sleep correlation.
- Compare Pearson and Spearman results and explain any difference.
- Add a simple linear regression with `scipy.stats.linregress` and interpret the slope.

## Run it

From the pack root:

```bash
python3 projects/14_sleep_focus/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

A third variable such as stress or workload could influence both sleep and focus. The analysis cannot rule that out.
