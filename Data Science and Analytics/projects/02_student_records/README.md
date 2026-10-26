# 02. The Student Records Rescue

> Clean two messy tables, join them, and produce one trustworthy gradebook.

**Category:** Data Cleaning & Preparation  
**Time:** 35–50 minutes  
**Skills:** ID normalisation, merge, pivot_table, grade calculation

## The goal

A college has student details in one file and scores in another. Student IDs are written in four different ways, some rows are duplicated, and a few scores are impossible. Build one clean gradebook.

## What you will learn

- Load both tables
- Inspect the join key
- Normalise IDs
- Remove duplicate students
- Clean scores
- Merge the tables
- Reshape to one row per student
- Calculate average and status
- Save and audit
- Visualise

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/students_raw.csv` | About 88 student rows, including duplicate IDs. |
| `data/scores_raw.csv` | About 255 score rows across Math, Science and English. |
| `data/clean_student_scores.csv` | One row per student with subject columns and an average. |

Students: `student_id`, `name`, `program`, `email`. Scores: `score_id`, `student_id`, `subject`, `score`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load both tables

```python
students = pd.read_csv(DATA / "students_raw.csv")
scores = pd.read_csv(DATA / "scores_raw.csv")
```

The two files have different grains: one row per student versus one row per student-subject. A join needs a shared key.

### Step 2 — Inspect the join key

```python
print(students["student_id"].head())
print(scores["student_id"].head())
```

Print the first few IDs. You will see `S001`, `s001`, `S-001` and ` S001 `. A direct merge would treat these as four different students.

### Step 3 — Normalise IDs

```python
def clean_id(series):
    return (series.astype(str).str.strip().str.upper()
            .str.replace("-", "", regex=False)
            .str.replace(" ", "", regex=False))
```

Strip spaces, uppercase everything, and remove hyphens. All four versions become `S001`.

### Step 4 — Remove duplicate students

```python
students = students.drop_duplicates(subset=["student_id"], keep="first")
```

After cleaning the key, repeated student rows become visible. Keep the first record for each ID.

### Step 5 — Clean scores

```python
scores["score"] = pd.to_numeric(scores["score"], errors="coerce").clip(0, 100)
scores["score"] = scores.groupby("subject")["score"].transform(
    lambda s: s.fillna(s.median())
)
```

`pd.to_numeric` converts `"88"` to `88`. Scores outside 0–100 are clipped to the valid range, then missing scores are filled with the median for that subject.

### Step 6 — Merge the tables

```python
merged = students.merge(scores, on="student_id", how="left",
                        validate="one_to_many")
```

`merge(..., how='left')` keeps every student, even if they have no score. `validate='one_to_many'` documents that one student can have several subject rows.

### Step 7 — Reshape to one row per student

```python
wide = merged.pivot_table(index=["student_id", "name", "program"],
                          columns="subject", values="score", aggfunc="mean").reset_index()
```

`pivot_table` turns the long score table into three columns: Math, Science and English.

### Step 8 — Calculate average and status

```python
wide["average_score"] = wide[["Math", "Science", "English"]].mean(axis=1)
wide["status"] = np.where(wide["average_score"] >= 50, "Pass", "Needs support")
```

The average is the mean of the three subject columns. A simple rule labels students at or above 50 as `Pass`.

### Step 9 — Save and audit

```python
wide.to_csv(DATA / "clean_student_scores.csv", index=False)
```

Save the clean gradebook and a report that records duplicate rows, filled scores, unknown IDs and program averages.

### Step 10 — Visualise

```python
sns.histplot(wide["average_score"], bins=12, kde=True)
```

A histogram shows the shape of the average-score distribution. A bar chart compares programs.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/merge_report.txt` | Duplicate counts, missing-score repairs, unmatched IDs and program averages. |
| `outputs/score_distribution.png` | Distribution of average scores. |
| `outputs/program_averages.png` | Average score by program. |

## Try it yourself

- Change the pass mark from 50 to 60 and count how many students move into support.
- Use `how='inner'` in the merge and explain which students disappear.
- Add a `top_subject` column using `idxmax(axis=1)`.

## Run it

From the pack root:

```bash
python3 projects/02_student_records/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

The most important idea is that a merge is only as good as the key you join on.
