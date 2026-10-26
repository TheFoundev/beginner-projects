# 20 Beginner-Friendly Data Science & Analytics Projects — Runnable Code Pack

A complete set of **20 real, runnable data projects** for beginners who want to learn by doing.

No GPU. No API keys. No paid accounts. Every project runs on a normal laptop, a college lab machine, or free Google Colab with Python 3.10+.

Each project has its own folder:

- `main.py` — the full, commented project code
- `data/` — the dataset used by the project
- `README.md` — a step-by-step walkthrough of the code
- `outputs/` — charts, CSVs, and text summaries created when you run it

Projects 01–05 start with **deliberately messy raw data** and produce a cleaned dataset. Projects 06–20 start with **clean, tidy data** so you can focus on analysis, statistics, or prediction.

---

## Quick start

```bash
cd "/home/aziz/foundev/Beginners/Data Science and Analytics"
python3 -m pip install -r requirements.txt
python3 projects/01_cafe_cleanup/main.py
```

Or run all 20 projects:

```bash
python3 run_all.py
```

Check that every project has code, data, a README, and outputs:

```bash
python3 verify_projects.py
```

Every script is headless-friendly: it saves figures to `outputs/` instead of opening a window. If you use Google Colab, upload a project folder and run `!python main.py` from inside it.

---

## Project map

| # | Project | Category | Main skill | Code style |
|---|---|---|---|---|
| 01 | [The Messy Café Menu](projects/01_cafe_cleanup/) | Data Cleaning & Preparation | Missing values, duplicates, dates | Python, pandas |
| 02 | [The Student Records Rescue](projects/02_student_records/) | Data Cleaning & Preparation | ID cleaning, merge, pivot | Python, pandas |
| 03 | [The Sales Data Detective](projects/03_sales_outliers/) | Data Cleaning & Preparation | IQR outliers, median repair | Python, pandas |
| 04 | [The Survey Cleanup Crew](projects/04_survey_cleanup/) | Data Cleaning & Preparation | Category mapping, regex | Python, pandas |
| 05 | [The Date & Time Fixer](projects/05_datetime_events/) | Data Cleaning & Preparation | Mixed timestamps, resampling | Python, pandas |
| 06 | [The Streaming Showdown](projects/06_streaming_analysis/) | Exploratory Analysis & Visualization | Groupby, completion rates | Python, seaborn |
| 07 | [The Coffee Shop Morning Rush](projects/07_coffee_rush/) | Exploratory Analysis & Visualization | Heatmaps, hourly revenue | Python, seaborn |
| 08 | [The Study Habits Explorer](projects/08_study_habits/) | Exploratory Analysis & Visualization | Distributions, correlation | Python, seaborn |
| 09 | [The City Weather Story](projects/09_weather_story/) | Exploratory Analysis & Visualization | Monthly aggregation, time series | Python, matplotlib |
| 10 | [The E-Commerce Funnel](projects/10_funnel_analysis/) | Exploratory Analysis & Visualization | Funnel conversion rates | Python, seaborn |
| 11 | [The A/B Test Lab](projects/11_ab_test/) | Statistics & Experiments | Two-proportion z-test, CI | Python, statsmodels |
| 12 | [The Study Break Experiment](projects/12_study_break/) | Statistics & Experiments | Welch t-test, Cohen's d | Python, SciPy |
| 13 | [The Customer Satisfaction Survey](projects/13_satisfaction_survey/) | Statistics & Experiments | Chi-square, Cramér's V | Python, SciPy |
| 14 | [The Sleep & Focus Correlation](projects/14_sleep_focus/) | Statistics & Experiments | Pearson and Spearman | Python, SciPy |
| 15 | [The Delivery Time ANOVA](projects/15_delivery_anova/) | Statistics & Experiments | ANOVA, Tukey HSD | Python, SciPy, statsmodels |
| 16 | [The Customer Segmentation Studio](projects/16_customer_segments/) | Business Analytics & Prediction | RFM, K-Means, silhouette | Python, scikit-learn |
| 17 | [The Churn Early-Warning System](projects/17_churn_model/) | Business Analytics & Prediction | Logistic regression, ROC-AUC | Python, scikit-learn |
| 18 | [The Sales Forecast Baseline](projects/18_sales_forecast/) | Business Analytics & Prediction | Trend, moving average, MAE | Python, scikit-learn |
| 19 | [The Product Recommendation Engine](projects/19_recommendation/) | Business Analytics & Prediction | Cosine similarity, cold start | Python, scikit-learn |
| 20 | [The Pricing & Demand Analyzer](projects/20_pricing_elasticity/) | Business Analytics & Prediction | Log-log regression, elasticity | Python, statsmodels |

---

## What each category teaches

### 1. Data Cleaning & Preparation (Projects 01–05)

Real datasets are rarely ready to analyse. These projects start with messy files and teach the habits that prevent bad analysis:

- inspecting missing values before filling them
- normalising IDs and category labels
- parsing mixed date formats
- detecting impossible values and statistical outliers
- documenting every repair in a report

Each project writes a cleaned CSV to its `data/` folder. That clean file is the deliverable.

### 2. Exploratory Analysis & Visualization (Projects 06–10)

These projects ask questions and answer them with tables and charts:

- Which genre holds attention, not just gets clicks?
- When is the coffee shop actually busy?
- Which habits are associated with exam scores?
- What did the weather do across the year?
- Where do e-commerce visitors drop out of the funnel?

You will use `groupby`, rates, pivots, heatmaps, and time-based charts. Every project saves both the summary table and the chart.

### 3. Statistics & Experiments (Projects 11–15)

These projects move from "what happened in the data" to "is this difference likely to be real?"

- compare two conversion rates
- compare two group means
- test whether two categorical variables are associated
- measure correlation without confusing it with causation
- compare three groups with ANOVA and Tukey HSD

Every project reports an effect size and a plain-English verdict, not just a p-value.

### 4. Business Analytics & Prediction (Projects 16–20)

These projects turn data into a decision aid:

- segment customers by recency, frequency, and monetary value
- estimate churn risk with logistic regression
- build and test a sales forecast baseline
- recommend products with cosine similarity
- estimate price elasticity with a log-log model

Every model is evaluated on data it did not train on, and every project explains its limitations.

---

## Requirements

```
numpy
pandas
matplotlib
seaborn
scipy
scikit-learn
statsmodels
```

Install with:

```bash
python3 -m pip install -r requirements.txt
```

Python 3.10 or newer is recommended. The pack was tested with Python 3.14, NumPy 2.5, pandas 2.3, Matplotlib 3.11, seaborn 0.13, SciPy 1.18, scikit-learn 1.9, and statsmodels 0.15.

No `openpyxl`, `plotly`, GPU, or internet connection is required.

---

## Suggested learning path

1. **Start with 01 (Café Menu)** — the simplest example of turning messy data into a clean table.
2. **Try 06 (Streaming)** — the simplest example of a useful groupby and chart.
3. **Read 11 (A/B Test)** — the simplest example of a statistical decision.
4. **Move to 16 (Segmentation)** and **17 (Churn)** — two business problems with different modelling styles.
5. **Finish with 18–20** — forecasting, recommendations, and pricing.

Each project README ends with a **Try it yourself** section so you can change one thing and see what happens.

---

## Notes on the data

All datasets are **small, synthetic, and offline-friendly**. They were created by `build_data.py` with fixed random seeds, so every run gives the same result. The data is designed to teach the workflow, not to make real-world decisions.

Projects 01–05 include deliberately messy raw files. Do not "fix" the raw file by hand; the point is to write code that fixes it reproducibly.

When you are ready, replace a CSV in `data/` with a real dataset and rerun the project. The code does not care where the CSV came from, as long as the column names match.

---

## Files in the pack root

- `README.md` — this guide
- `PROJECT_GUIDE.md` — the 20 project concepts and no-code alternatives
- `build_data.py` — regenerates every dataset
- `run_all.py` — runs all 20 projects and reports pass/fail
- `verify_projects.py` — checks that every project and output exists
- `requirements.txt` — Python dependencies
- `.gitignore` — common Python and editor files

---

## Important disclaimer

These projects are for learning. Do not use them to make decisions about real people, money, health, safety, or academic fairness without better data, expert review, and human oversight.
