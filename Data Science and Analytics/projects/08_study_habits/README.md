# 08. The Study Habits Explorer

> Describe distributions, measure relationships, and compare exam scores across study methods.

**Category:** Exploratory Analysis & Visualization  
**Time:** 35–50 minutes  
**Skills:** distributions, correlation, scatterplots, boxplots

## The goal

A group of students reports study hours, sleep, attendance, screen time and exam scores. Explore the data before making any claims about what “causes” a better score.

## What you will learn

- Load and inspect
- Select numeric columns
- Calculate the correlation matrix
- Summarise study methods
- Plot distributions
- Plot the correlation heatmap
- Plot study hours against score
- Compare methods with a boxplot
- Write the findings

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/study_habits.csv` | 220 students with five numeric measures and a study-method label. |

`student_id`, `study_hours`, `sleep_hours`, `attendance_percent`, `screen_time_hours`, `exam_score`, `study_method`, `year`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load and inspect

```python
df = pd.read_csv(DATA / "study_habits.csv")
print(df.describe())
```

Start with the shape, missing values and descriptive statistics. This tells you whether the data is plausible before you plot it.

### Step 2 — Select numeric columns

```python
numeric_cols = ["study_hours", "sleep_hours", "attendance_percent",
                "screen_time_hours", "exam_score"]
```

Correlation only works on numbers. Keep the five numeric measures in a list so the analysis is explicit.

### Step 3 — Calculate the correlation matrix

```python
corr = df[numeric_cols].corr().round(2)
```

Each cell is a Pearson correlation between two columns. Values near +1 move together; values near -1 move in opposite directions.

### Step 4 — Summarise study methods

```python
summary = df.groupby("study_method").agg(
    avg_exam_score=("exam_score", "mean"),
    avg_study_hours=("study_hours", "mean"),
)
```

Grouping compares average exam score and average habits for solo, group and online study.

### Step 5 — Plot distributions

```python
sns.histplot(df["exam_score"], bins=14, kde=True)
```

Histograms with a KDE curve show the shape: symmetric, skewed, or clustered. A 2×2 grid keeps four variables comparable.

### Step 6 — Plot the correlation heatmap

```python
sns.heatmap(corr, annot=True, cmap="RdBu_r", vmin=-1, vmax=1)
```

The heatmap makes the strongest relationships jump out. Read the `exam_score` row first.

### Step 7 — Plot study hours against score

```python
sns.regplot(data=df, x="study_hours", y="exam_score")
```

`regplot` adds a straight trend line. It helps you see direction, but it does not prove that studying more causes a higher score.

### Step 8 — Compare methods with a boxplot

```python
sns.boxplot(data=df, x="study_method", y="exam_score")
```

A boxplot shows the median, middle 50% and potential outliers for each method.

### Step 9 — Write the findings

```python
strongest = corr["exam_score"].drop("exam_score").abs().idxmax()
```

Report the strongest correlation, the best average method and the correlation warning in plain English.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/correlation_matrix.csv` | The numeric correlation table. |
| `outputs/method_summary.csv` | Average score and habits by study method. |
| `outputs/study_distributions.png` | Histograms of study, sleep, attendance and score. |
| `outputs/correlation_heatmap.png` | The full correlation matrix. |
| `outputs/study_vs_score.png` | Study hours versus exam score with a trend line. |
| `outputs/method_boxplot.png` | Exam score by study method. |
| `outputs/insights.txt` | Plain-English findings and the correlation caveat. |

## Try it yourself

- Filter to students with attendance above 80% and recompute the correlation.
- Compare the mean score for first-year versus final-year students.
- Use `sns.pairplot` on the numeric columns and explain what it adds.

## Run it

From the pack root:

```bash
python3 projects/08_study_habits/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

Correlation measures association, not causation. A hidden variable such as motivation could affect both study time and score.
