# 12. The Study Break Experiment

> Compare exam scores for students who took a break versus students who studied straight through.

**Category:** Statistics & Experiments  
**Time:** 35–50 minutes  
**Skills:** t-test, Cohen's d, confidence intervals, boxplots

## The goal

Two groups of students studied the same material. One group took a short break; the other did not. Test whether the average scores differ and how large the difference is.

## What you will learn

- Load and check groups
- Separate the two score vectors
- Run Welch's t-test
- Calculate Cohen's d
- Build a 95% confidence interval
- Write the result
- Plot the distributions
- Plot the means with error bars

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/study_break.csv` | 80 students: 40 in the break group and 40 in the no-break group. |

`student_id`, `group`, `score`, `study_minutes`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load and check groups

```python
df = pd.read_csv(DATA / "study_break.csv")
print(df.groupby("group")["score"].agg(["count", "mean", "std"]))
```

Count rows, means and standard deviations for each group. This is the descriptive part before any test.

### Step 2 — Separate the two score vectors

```python
break_scores = df.loc[df["group"] == "break", "score"]
no_break_scores = df.loc[df["group"] == "no_break", "score"]
```

The t-test needs two separate arrays, one per group.

### Step 3 — Run Welch's t-test

```python
t_stat, p_value = stats.ttest_ind(
    break_scores, no_break_scores, equal_var=False
)
```

The null hypothesis is that both groups have the same average score. Welch's version does not assume equal variances.

### Step 4 — Calculate Cohen's d

```python
pooled_sd = np.sqrt(((n1 - 1) * sd1**2 + (n2 - 1) * sd2**2) / (n1 + n2 - 2))
cohens_d = (mean1 - mean2) / pooled_sd
```

A p-value says whether a difference is likely, not how big it is. Cohen's d standardises the mean difference by the pooled standard deviation.

### Step 5 — Build a 95% confidence interval

```python
se = np.sqrt(sd1**2 / n1 + sd2**2 / n2)
ci_low, ci_high = diff - t_critical * se, diff + t_critical * se
```

The interval shows the plausible range for the true mean difference. It is more informative than a bare p-value.

### Step 6 — Write the result

```python
verdict = "statistically significant" if p_value < 0.05 else "not statistically significant"
```

Report the means, difference, t-statistic, p-value, Cohen's d and confidence interval together.

### Step 7 — Plot the distributions

```python
sns.boxplot(data=df, x="group", y="score")
sns.stripplot(data=df, x="group", y="score")
```

A boxplot with individual points shows the median, spread and outliers. The points prevent the box from hiding the raw data.

### Step 8 — Plot the means with error bars

```python
ax.bar(["break", "no_break"], means, yerr=errors, capsize=8)
```

The bar chart summarises the group means, and the error bars show uncertainty around each mean.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/results.txt` | Means, t-test, effect size, confidence interval and verdict. |
| `outputs/study_break_boxplot.png` | Score distributions with individual students shown. |
| `outputs/group_means.png` | Group means with 95% error bars. |

## Try it yourself

- Run the standard Student t-test with `equal_var=True` and compare the p-value.
- Check whether study minutes differ between the groups. If they do, the comparison is confounded.
- Calculate a 99% confidence interval instead of 95%.

## Run it

From the pack root:

```bash
python3 projects/12_study_break/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

A statistically significant result does not prove that breaks caused the score difference. Random assignment and a clean protocol matter.
