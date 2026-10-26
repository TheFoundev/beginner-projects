# 04. The Survey Cleanup Crew

> Turn inconsistent survey answers into clean numeric fields and summarise what respondents said.

**Category:** Data Cleaning & Preparation  
**Time:** 30–45 minutes  
**Skills:** categorical mapping, regex extraction, duplicates, missing values

## The goal

A survey exports free-text-style answers such as `YES`, `y`, `1`, `5 - Very satisfied` and blank cells. Clean the answers without accidentally changing their meaning.

## What you will learn

- Load and inspect the raw answers
- Remove duplicate respondents
- Clean age
- Map gender labels
- Extract the satisfaction number
- Convert yes/no to 1/0
- Save and report
- Chart the cleaned answers

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/survey_raw.csv` | 290 rows before de-duplication, with inconsistent labels. |
| `data/clean_survey.csv` | 250 unique respondents with numeric fields. |

`respondent_id`, `age`, `gender`, `satisfaction`, `would_recommend`, `comments`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load and inspect the raw answers

```python
raw = pd.read_csv(DATA / "survey_raw.csv")
print(raw["would_recommend"].unique())
```

Print the unique values in the categorical columns. This is how you discover every spelling and format you need to handle.

### Step 2 — Remove duplicate respondents

```python
df = raw.drop_duplicates(subset=["respondent_id"], keep="first")
```

Duplicate `respondent_id` values usually mean the same person submitted twice. Keep one record per ID.

### Step 3 — Clean age

```python
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df.loc[df["age"] > 100, "age"] = np.nan
df["age"] = df["age"].fillna(df["age"].median())
```

`999` is a placeholder for “prefer not to say”, not a real age. Convert to numeric, mark values above 100 as missing, then fill with the median.

### Step 4 — Map gender labels

```python
gender_map = {"m": "Male", "male": "Male", "f": "Female", "female": "Female"}
df["gender"] = df["gender"].str.lower().map(gender_map).fillna("Unknown")
```

A dictionary converts `M`, `male` and `Male` to one label. Anything unrecognised becomes `Unknown` instead of silently disappearing.

### Step 5 — Extract the satisfaction number

```python
df["satisfaction"] = df["satisfaction"].str.extract(r"(\d)", expand=False)
df["satisfaction"] = pd.to_numeric(df["satisfaction"], errors="coerce").clip(1, 5)
```

`str.extract(r'(\d)')` pulls the first digit out of answers such as `5 - Very satisfied`. Blank answers become missing.

### Step 6 — Convert yes/no to 1/0

```python
yes_no = {"yes": 1, "y": 1, "1": 1, "no": 0, "n": 0, "0": 0}
df["would_recommend"] = df["would_recommend"].str.lower().map(yes_no).fillna(0)
```

A second dictionary maps every accepted “yes” spelling to 1 and every “no” spelling to 0. Blanks are treated as 0 for this simple analysis.

### Step 7 — Save and report

```python
df.to_csv(DATA / "clean_survey.csv", index=False)
```

The report records how many duplicates, placeholder ages, missing satisfaction values and blank recommendations were handled.

### Step 8 — Chart the cleaned answers

```python
sns.countplot(data=df, x="satisfaction")
```

A count plot shows the satisfaction distribution. A stacked bar shows the recommendation rate by gender.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/survey_summary.txt` | Cleaning counts, average satisfaction and recommendation rate. |
| `outputs/satisfaction_distribution.png` | How respondents rated satisfaction. |
| `outputs/recommend_by_gender.png` | Recommendation share by gender. |

## Try it yourself

- Treat blank recommendations as missing and drop them instead of coding them as 0. How does the rate change?
- Add a `satisfaction_label` column that maps 1–5 to words such as `Very low` and `Very high`.
- Compare average age for people who recommend versus people who do not.

## Run it

From the pack root:

```bash
python3 projects/04_survey_cleanup/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

Never map unknown categories to a real category silently. `Unknown` is honest; guessing can bias the result.
