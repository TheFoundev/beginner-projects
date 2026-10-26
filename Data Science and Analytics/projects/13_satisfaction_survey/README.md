# 13. The Customer Satisfaction Survey

> Compare satisfaction across segments and test whether recommendation is associated with segment.

**Category:** Statistics & Experiments  
**Time:** 35–50 minutes  
**Skills:** confidence intervals, chi-square test, Cramér's V, stacked bars

## The goal

New, returning and VIP customers rated satisfaction and answered whether they would recommend the service. Compare the groups and test the recommendation pattern.

## What you will learn

- Load and check groups
- Summarise satisfaction
- Build a contingency table
- Run the chi-square test
- Calculate Cramér's V
- Write the result
- Plot satisfaction with error bars
- Plot recommendation shares

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/satisfaction_survey.csv` | 300 respondents with segment, satisfaction, recommendation and age. |

`respondent_id`, `segment`, `satisfaction`, `would_recommend`, `age`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load and check groups

```python
df = pd.read_csv(DATA / "satisfaction_survey.csv")
print(df.groupby("segment").size())
```

Count respondents per segment and inspect the satisfaction range.

### Step 2 — Summarise satisfaction

```python
summary = df.groupby("segment").agg(
    respondents=("respondent_id", "count"),
    avg_satisfaction=("satisfaction", "mean"),
    sd_satisfaction=("satisfaction", "std"),
    recommend_rate=("would_recommend", "mean"),
)
```

For each segment, calculate the mean, standard deviation, recommendation rate and a 95% margin of error.

### Step 3 — Build a contingency table

```python
table = pd.crosstab(df["segment"], df["would_recommend"])
```

`pd.crosstab` counts how many respondents in each segment said yes versus no. This is the input for the chi-square test.

### Step 4 — Run the chi-square test

```python
chi2, p_value, dof, expected = chi2_contingency(table)
```

The null hypothesis is independence: recommendation does not depend on segment. A small p-value suggests an association.

### Step 5 — Calculate Cramér's V

```python
cramers_v = np.sqrt(chi2 / (n * (min(table.shape) - 1)))
```

Cramér's V turns chi-square into an effect size between 0 and 1. It helps distinguish a real association from a trivial one with a large sample.

### Step 6 — Write the result

```python
print(f"chi-square={chi2:.3f}, p={p_value:.5f}, V={cramers_v:.2f}")
```

Report the average satisfaction, recommendation rate, chi-square, p-value, Cramér's V and the expected counts.

### Step 7 — Plot satisfaction with error bars

```python
ax.bar(summary.index, summary["avg_satisfaction"],
       yerr=summary["margin_of_error"], capsize=8)
```

A bar chart with error bars shows both the average and the uncertainty around it.

### Step 8 — Plot recommendation shares

```python
rec_share = pd.crosstab(df["segment"], df["would_recommend"], normalize="index")
```

A 100% stacked bar shows the yes/no mix within each segment. It is easier to compare composition than raw counts.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/segment_summary.csv` | Satisfaction and recommendation metrics by segment. |
| `outputs/results.txt` | Chi-square result, effect size and expected counts. |
| `outputs/satisfaction_by_segment.png` | Average satisfaction with 95% error bars. |
| `outputs/recommend_by_segment.png` | Recommendation mix by segment. |

## Try it yourself

- Run the chi-square test with age groups instead of segments.
- Compare average satisfaction for recommenders versus non-recommenders.
- Check whether the expected counts are all at least 5, a common rule of thumb for chi-square.

## Run it

From the pack root:

```bash
python3 projects/13_satisfaction_survey/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

Satisfaction is ordinal (1–5). Treating the average as a number is common but loses some information; always look at the full distribution too.
