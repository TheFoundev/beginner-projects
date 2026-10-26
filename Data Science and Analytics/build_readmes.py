"""Generate the per-project README walkthroughs.

Run from the pack root:
    python3 build_readmes.py

Each README explains the dataset, the purpose of every code step, the files
produced, and a few sensible experiments to try next.
"""

from __future__ import annotations

from pathlib import Path

BASE = Path(__file__).resolve().parent
PROJECTS = BASE / "projects"

PROJECTS_DATA = [
    # ------------------------------------------------------------------
    {
        "number": r'''01''',
        "folder": r'''01_cafe_cleanup''',
        "title": r'''The Messy Café Menu''',
        "tagline": r'''Turn a deliberately messy order log into a clean revenue table.''',
        "category": r'''Data Cleaning & Preparation''',
        "time": r'''30–45 minutes''',
        "skills": r'''pandas, missing values, duplicates, dates, text cleaning''',
        "goal": r'''A café exports orders from three different systems. Dates, item names, categories, quantities and prices are inconsistent. Your job is to make one clean table that a manager could actually use.''',
        "dataset": [
            (r'''`data/cafe_orders_raw.csv`''', r'''The messy input: 118 rows, 7 columns.'''),
            (r'''`data/cafe_orders_clean.csv`''', r'''The cleaned output written by `main.py`.'''),
        ],
        "columns": r'''`order_id`, `date`, `item`, `category`, `quantity`, `unit_price`, `customer_type`.''',
        "steps": [
            (r"""Load the raw file""", r"""`pd.read_csv` turns the CSV into a DataFrame. A DataFrame is a table with named columns and numbered rows.""", r"""df = pd.read_csv(DATA / "cafe_orders_raw.csv")"""),
            (r"""Measure the mess before changing it""", r"""`isna().sum()` counts empty cells. `duplicated(subset=['order_id']).sum()` counts repeated order IDs. Always record the “before” numbers so you can prove what changed.""", r"""print(df.isna().sum())
print(df.duplicated(subset=["order_id"]).sum())"""),
            (r"""Standardise text""", r"""`str.strip()` removes accidental spaces. `str.title()` converts `LATTE`, `latte` and ` Latte ` into `Latte`. This makes grouping reliable.""", r"""df["item"] = df["item"].str.strip().str.title()"""),
            (r"""Parse the dates""", r"""The file mixes `2025-01-05`, `Jan 05, 2025` and `05-Jan-2025`. `pd.to_datetime(..., format="mixed")` reads each row in its own format.""", r"""df["date"] = pd.to_datetime(df["date"], format="mixed", errors="coerce")"""),
            (r"""Rebuild category from item""", r"""The original category column is unreliable. A dictionary maps each known item to `Drink` or `Food`, which is a safer rule.""", r"""df["category"] = df["item"].map(item_to_category)"""),
            (r"""Repair quantity""", r"""`pd.to_numeric` converts numbers stored as text and turns bad text into `NaN`. A quantity of zero or less is impossible, so it becomes missing and is filled with the median.""", r"""df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df.loc[df["quantity"] <= 0, "quantity"] = np.nan
df["quantity"] = df["quantity"].fillna(df["quantity"].median()).astype(int)"""),
            (r"""Repair unit price""", r"""Prices arrive as `4.50`, `$4.50` and blank. Remove the dollar sign, convert to a number, then fill each missing price with the median price for that same item.""", r"""df["unit_price"] = df["unit_price"].astype(str).str.replace("$", "", regex=False)
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
df["unit_price"] = df.groupby("item")["unit_price"].transform(
    lambda s: s.fillna(s.median())
)"""),
            (r"""Create the order total""", r"""Revenue per row is `quantity × unit_price`. This is called a derived column: it did not exist in the raw file.""", r"""df["total"] = (df["quantity"] * df["unit_price"]).round(2)"""),
            (r"""Remove duplicates and bad dates""", r"""`drop_duplicates(subset=['order_id'], keep='first')` keeps one row per order. `dropna(subset=['date'])` removes rows with an unreadable date.""", r"""df = df.dropna(subset=["date"])
df = df.drop_duplicates(subset=["order_id"], keep="first")"""),
            (r"""Save and audit""", r"""Write the clean CSV, then save a text report with row counts, missing counts, revenue and the repair actions.""", r"""df.to_csv(DATA / "cafe_orders_clean.csv", index=False)"""),
            (r"""Visualise the result""", r"""A missing-value bar chart documents the starting point. A revenue-by-item chart shows that the clean table is useful.""", r"""df.groupby("item")["total"].sum().sort_values().plot(kind="barh")"""),
        ],
        "outputs": [
            (r'''`outputs/cleaning_report.txt`''', r'''Before/after row counts, missing cells, duplicate count, total revenue.'''),
            (r'''`outputs/missing_before.png`''', r'''Which columns had empty cells before cleaning.'''),
            (r'''`outputs/revenue_by_item.png`''', r'''Revenue per menu item after cleaning.'''),
            (r'''`outputs/daily_revenue.png`''', r'''Daily revenue over the two-month period.'''),
        ],
        "try_it": [
            r'''Fill missing prices with the mean instead of the median and compare the total revenue.''',
            r'''Add a `weekday` column with `df['date'].dt.day_name()` and chart revenue by weekday.''',
            r'''Change `keep='first'` to `keep='last'` and explain why the result might differ.''',
        ],
        "note": r'''This project intentionally starts with dirty data. The clean file is the deliverable, not the raw file.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''02''',
        "folder": r'''02_student_records''',
        "title": r'''The Student Records Rescue''',
        "tagline": r'''Clean two messy tables, join them, and produce one trustworthy gradebook.''',
        "category": r'''Data Cleaning & Preparation''',
        "time": r'''35–50 minutes''',
        "skills": r'''ID normalisation, merge, pivot_table, grade calculation''',
        "goal": r'''A college has student details in one file and scores in another. Student IDs are written in four different ways, some rows are duplicated, and a few scores are impossible. Build one clean gradebook.''',
        "dataset": [
            (r'''`data/students_raw.csv`''', r'''About 88 student rows, including duplicate IDs.'''),
            (r'''`data/scores_raw.csv`''', r'''About 255 score rows across Math, Science and English.'''),
            (r'''`data/clean_student_scores.csv`''', r'''One row per student with subject columns and an average.'''),
        ],
        "columns": r'''Students: `student_id`, `name`, `program`, `email`. Scores: `score_id`, `student_id`, `subject`, `score`.''',
        "steps": [
            (r"""Load both tables""", r"""The two files have different grains: one row per student versus one row per student-subject. A join needs a shared key.""", r"""students = pd.read_csv(DATA / "students_raw.csv")
scores = pd.read_csv(DATA / "scores_raw.csv")"""),
            (r"""Inspect the join key""", r"""Print the first few IDs. You will see `S001`, `s001`, `S-001` and ` S001 `. A direct merge would treat these as four different students.""", r"""print(students["student_id"].head())
print(scores["student_id"].head())"""),
            (r"""Normalise IDs""", r"""Strip spaces, uppercase everything, and remove hyphens. All four versions become `S001`.""", r"""def clean_id(series):
    return (series.astype(str).str.strip().str.upper()
            .str.replace("-", "", regex=False)
            .str.replace(" ", "", regex=False))"""),
            (r"""Remove duplicate students""", r"""After cleaning the key, repeated student rows become visible. Keep the first record for each ID.""", r"""students = students.drop_duplicates(subset=["student_id"], keep="first")"""),
            (r"""Clean scores""", r"""`pd.to_numeric` converts `"88"` to `88`. Scores outside 0–100 are clipped to the valid range, then missing scores are filled with the median for that subject.""", r"""scores["score"] = pd.to_numeric(scores["score"], errors="coerce").clip(0, 100)
scores["score"] = scores.groupby("subject")["score"].transform(
    lambda s: s.fillna(s.median())
)"""),
            (r"""Merge the tables""", r"""`merge(..., how='left')` keeps every student, even if they have no score. `validate='one_to_many'` documents that one student can have several subject rows.""", r"""merged = students.merge(scores, on="student_id", how="left",
                        validate="one_to_many")"""),
            (r"""Reshape to one row per student""", r"""`pivot_table` turns the long score table into three columns: Math, Science and English.""", r"""wide = merged.pivot_table(index=["student_id", "name", "program"],
                          columns="subject", values="score", aggfunc="mean").reset_index()"""),
            (r"""Calculate average and status""", r"""The average is the mean of the three subject columns. A simple rule labels students at or above 50 as `Pass`.""", r"""wide["average_score"] = wide[["Math", "Science", "English"]].mean(axis=1)
wide["status"] = np.where(wide["average_score"] >= 50, "Pass", "Needs support")"""),
            (r"""Save and audit""", r"""Save the clean gradebook and a report that records duplicate rows, filled scores, unknown IDs and program averages.""", r"""wide.to_csv(DATA / "clean_student_scores.csv", index=False)"""),
            (r"""Visualise""", r"""A histogram shows the shape of the average-score distribution. A bar chart compares programs.""", r"""sns.histplot(wide["average_score"], bins=12, kde=True)"""),
        ],
        "outputs": [
            (r'''`outputs/merge_report.txt`''', r'''Duplicate counts, missing-score repairs, unmatched IDs and program averages.'''),
            (r'''`outputs/score_distribution.png`''', r'''Distribution of average scores.'''),
            (r'''`outputs/program_averages.png`''', r'''Average score by program.'''),
        ],
        "try_it": [
            r'''Change the pass mark from 50 to 60 and count how many students move into support.''',
            r'''Use `how='inner'` in the merge and explain which students disappear.''',
            r'''Add a `top_subject` column using `idxmax(axis=1)`.''',
        ],
        "note": r'''The most important idea is that a merge is only as good as the key you join on.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''03''',
        "folder": r'''03_sales_outliers''',
        "title": r'''The Sales Data Detective''',
        "tagline": r'''Find impossible sales values and statistical outliers, repair them, and compare daily with weekly trends.''',
        "category": r'''Data Cleaning & Preparation''',
        "time": r'''35–50 minutes''',
        "skills": r'''IQR rule, median imputation, resampling, before/after charts''',
        "goal": r'''Three stores report daily sales. The file contains negative revenue, missing days and a few enormous values. Decide what is invalid, repair it carefully, and summarise the business trend.''',
        "dataset": [
            (r'''`data/daily_sales_raw.csv`''', r'''360 rows: 3 stores × 120 days, with injected bad values.'''),
            (r'''`data/clean_daily_sales.csv`''', r'''The repaired daily table.'''),
            (r'''`outputs/weekly_sales.csv`''', r'''Weekly totals by store.'''),
        ],
        "columns": r'''`date`, `store`, `sales`.''',
        "steps": [
            (r"""Load and sort""", r"""Parse the date, drop unreadable dates, and sort by store and date so the time order is clear.""", r"""raw = pd.read_csv(DATA / "daily_sales_raw.csv")
raw["date"] = pd.to_datetime(raw["date"])
raw = raw.sort_values(["store", "date"])"""),
            (r"""Describe the values""", r"""`describe()` shows the minimum, maximum and quartiles. A negative minimum or a maximum many times larger than the 75th percentile is a warning sign.""", r"""print(raw["sales"].describe())"""),
            (r"""Mark negative sales as missing""", r"""Revenue cannot be negative in this dataset, so a negative row is not a usable observation.""", r"""df.loc[df["sales"] < 0, "sales"] = np.nan"""),
            (r"""Calculate IQR bounds""", r"""For each store, Q1 and Q3 split the middle 50% of values. The IQR is Q3 − Q1. Values beyond 1.5 × IQR from the box are flagged.""", r"""q1 = df.groupby("store")["sales"].transform(lambda s: s.quantile(0.25))
q3 = df.groupby("store")["sales"].transform(lambda s: s.quantile(0.75))
iqr = q3 - q1
outliers = (df["sales"] < q1 - 1.5 * iqr) | (df["sales"] > q3 + 1.5 * iqr)"""),
            (r"""Replace outliers with the store median""", r"""The median is robust: one extreme value does not drag it around. Replace flagged values with the median for that same store.""", r"""df.loc[outliers, "sales"] = np.nan
df["sales"] = df["sales"].fillna(df.groupby("store")["sales"].transform("median"))"""),
            (r"""Aggregate to weeks""", r"""`dt.to_period('W')` groups dates into weeks. Summing sales per week turns noisy daily data into a smoother business signal.""", r"""df["week"] = df["date"].dt.to_period("W").dt.start_time
weekly = df.groupby(["week", "store"])["sales"].sum()"""),
            (r"""Save the clean data and report""", r"""Keep both the cleaned daily rows and the weekly summary. The report records how many values were repaired.""", r"""df.to_csv(DATA / "clean_daily_sales.csv", index=False)"""),
            (r"""Compare before and after""", r""", r'''Two boxplots make the effect of the repair visible. The before panel shows the extreme values; the after panel shows a usable range.""", r"""sns.boxplot(data=raw, x="store", y="sales")"""),
            (r"""Chart the trend""", r"""A daily line chart shows seasonality; a weekly line chart shows the bigger direction.""", r"""ax.plot(weekly["week"], weekly["sales"], marker="o")"""),
        ],
        "outputs": [
            (r'''`outputs/outlier_report.txt`''', r'''Counts of negative, missing and IQR-flagged values plus clean totals.'''),
            (r'''`outputs/outliers_before_after.png`''', r'''Side-by-side boxplots before and after repair.'''),
            (r'''`outputs/daily_trend.png`''', r'''Daily sales by store after cleaning.'''),
            (r'''`outputs/weekly_trend.png`''', r'''Total weekly sales.'''),
            (r'''`outputs/weekly_sales.csv`''', r'''Weekly totals by store.'''),
        ],
        "try_it": [
            r'''Change 1.5 × IQR to 3.0 × IQR and count how many outliers remain.''',
            r'''Compare median imputation with dropping the bad rows. Which changes the weekly total more?''',
            r'''Add a 7-day rolling average to the daily chart.''',
        ],
        "note": r'''Outlier rules are judgement calls. The code documents the rule so a reviewer can disagree with it and re-run the analysis.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''04''',
        "folder": r'''04_survey_cleanup''',
        "title": r'''The Survey Cleanup Crew''',
        "tagline": r'''Turn inconsistent survey answers into clean numeric fields and summarise what respondents said.''',
        "category": r'''Data Cleaning & Preparation''',
        "time": r'''30–45 minutes''',
        "skills": r'''categorical mapping, regex extraction, duplicates, missing values''',
        "goal": r'''A survey exports free-text-style answers such as `YES`, `y`, `1`, `5 - Very satisfied` and blank cells. Clean the answers without accidentally changing their meaning.''',
        "dataset": [
            (r'''`data/survey_raw.csv`''', r'''290 rows before de-duplication, with inconsistent labels.'''),
            (r'''`data/clean_survey.csv`''', r'''250 unique respondents with numeric fields.'''),
        ],
        "columns": r'''`respondent_id`, `age`, `gender`, `satisfaction`, `would_recommend`, `comments`.''',
        "steps": [
            (r"""Load and inspect the raw answers""", r"""Print the unique values in the categorical columns. This is how you discover every spelling and format you need to handle.""", r"""raw = pd.read_csv(DATA / "survey_raw.csv")
print(raw["would_recommend"].unique())"""),
            (r"""Remove duplicate respondents""", r"""Duplicate `respondent_id` values usually mean the same person submitted twice. Keep one record per ID.""", r"""df = raw.drop_duplicates(subset=["respondent_id"], keep="first")"""),
            (r"""Clean age""", r"""`999` is a placeholder for “prefer not to say”, not a real age. Convert to numeric, mark values above 100 as missing, then fill with the median.""", r"""df["age"] = pd.to_numeric(df["age"], errors="coerce")
df.loc[df["age"] > 100, "age"] = np.nan
df["age"] = df["age"].fillna(df["age"].median())"""),
            (r"""Map gender labels""", r"""A dictionary converts `M`, `male` and `Male` to one label. Anything unrecognised becomes `Unknown` instead of silently disappearing.""", r"""gender_map = {"m": "Male", "male": "Male", "f": "Female", "female": "Female"}
df["gender"] = df["gender"].str.lower().map(gender_map).fillna("Unknown")"""),
            (r"""Extract the satisfaction number""", r""", r'''"`str.extract(r'(\\d)')` pulls the first digit out of answers such as `5 - Very satisfied`. Blank answers become missing.""", r"""df["satisfaction"] = df["satisfaction"].str.extract(r"(\\d)", expand=False)
df["satisfaction"] = pd.to_numeric(df["satisfaction"], errors="coerce").clip(1, 5)"""),
            (r"""Convert yes/no to 1/0""", r"""A second dictionary maps every accepted “yes” spelling to 1 and every “no” spelling to 0. Blanks are treated as 0 for this simple analysis.""", r"""yes_no = {"yes": 1, "y": 1, "1": 1, "no": 0, "n": 0, "0": 0}
df["would_recommend"] = df["would_recommend"].str.lower().map(yes_no).fillna(0)"""),
            (r"""Save and report""", r"""The report records how many duplicates, placeholder ages, missing satisfaction values and blank recommendations were handled.""", r"""df.to_csv(DATA / "clean_survey.csv", index=False)"""),
            (r"""Chart the cleaned answers""", r"""A count plot shows the satisfaction distribution. A stacked bar shows the recommendation rate by gender.""", r"""sns.countplot(data=df, x="satisfaction")"""),
        ],
        "outputs": [
            (r'''`outputs/survey_summary.txt`''', r'''Cleaning counts, average satisfaction and recommendation rate.'''),
            (r'''`outputs/satisfaction_distribution.png`''', r'''How respondents rated satisfaction.'''),
            (r'''`outputs/recommend_by_gender.png`''', r'''Recommendation share by gender.'''),
        ],
        "try_it": [
            r'''Treat blank recommendations as missing and drop them instead of coding them as 0. How does the rate change?''',
            r'''Add a `satisfaction_label` column that maps 1–5 to words such as `Very low` and `Very high`.''',
            r'''Compare average age for people who recommend versus people who do not.''',
        ],
        "note": r'''Never map unknown categories to a real category silently. `Unknown` is honest; guessing can bias the result.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''05''',
        "folder": r'''05_datetime_events''',
        "title": r'''The Date & Time Fixer''',
        "tagline": r'''Parse mixed timestamp formats, remove duplicate events, and build hourly and daily activity summaries.''',
        "category": r'''Data Cleaning & Preparation''',
        "time": r'''30–45 minutes''',
        "skills": r'''datetime parsing, dt accessors, resampling, event aggregation''',
        "goal": r'''An event log contains timestamps in ISO, US-style and ISO-with-T formats. Turn them into real datetime values, then answer: when are users most active?''',
        "dataset": [
            (r'''`data/events_raw.csv`''', r'''420 rows with three timestamp styles and duplicate event IDs.'''),
            (r'''`data/clean_events.csv`''', r'''400 unique events with date, hour, weekday and month columns.'''),
        ],
        "columns": r'''`event_id`, `user_id`, `timestamp`, `event_type`, `duration_min`.''',
        "steps": [
            (r"""Load the event log""", r"""Each row is one user action. The raw timestamp is currently text, so it cannot be sorted or grouped by time yet.""", r"""raw = pd.read_csv(DATA / "events_raw.csv")"""),
            (r"""Look at the formats""", r"""Print a few raw timestamps. You should see all three styles side by side.""", r"""print(raw["timestamp"].head(8))"""),
            (r"""Parse with format='mixed'""", r"""Pandas reads each row in its own format. `errors='coerce'` turns a broken timestamp into `NaT` instead of crashing the whole script.""", r"""df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed", errors="coerce")"""),
            (r"""Remove duplicates and bad times""", r"""Drop rows with no valid timestamp, then keep the first event for each `event_id`.""", r"""df = df.dropna(subset=["timestamp"])
df = df.drop_duplicates(subset=["event_id"], keep="first")"""),
            (r"""Create time parts""", r"""`dt.hour`, `dt.day_name()` and `dt.date` expose the parts you need for grouping and charts.""", r"""df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.day_name()
df["date"] = df["timestamp"].dt.date"""),
            (r"""Fill missing durations""", r"""A missing duration is filled with the median duration for the same event type, so a purchase is not filled with a view median.""", r"""df["duration_min"] = df.groupby("event_type")["duration_min"].transform(
    lambda s: s.fillna(s.median())
)"""),
            (r"""Save the clean event table""", r"""The output contains the original columns plus the new time parts.""", r"""df.to_csv(DATA / "clean_events.csv", index=False)"""),
            (r"""Aggregate by hour""", r""", r'''Counting event IDs per hour reveals peak activity periods.""", r"""hourly = df.groupby("hour").size()"""),
            (r"""Aggregate by day""", r"""Resampling by day lets you count events and unique active users for each date.""", r"""daily = df.set_index("timestamp").resample("D").agg(
    events=("event_id", "count"), active_users=("user_id", "nunique")
)"""),
            (r"""Plot the patterns""", r"""A bar chart shows the busiest hours; a line chart shows daily active users.""", r"""sns.barplot(data=hourly, x="hour", y="events")"""),
        ],
        "outputs": [
            (r'''`outputs/time_cleaning_report.txt`''', r'''Parsing counts, date range and busiest hours.'''),
            (r'''`outputs/hourly_activity.csv`''', r'''Event count for every hour.'''),
            (r'''`outputs/hourly_activity.png`''', r'''Activity by hour of day.'''),
            (r'''`outputs/daily_activity.csv`''', r'''Daily events and unique active users.'''),
            (r'''`outputs/daily_active_users.png`''', r'''Daily active-user trend.'''),
        ],
        "try_it": [
            r'''Add a `is_weekend` column and compare average hourly activity on weekends.''',
            r'''Find the top 10 users by number of events.''',
            r'''Change the resample frequency from daily to weekly and describe the trade-off.''',
        ],
        "note": r'''The mixed-format parser is convenient for teaching, but production pipelines should enforce one timestamp format at the source.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''06''',
        "folder": r'''06_streaming_analysis''',
        "title": r'''The Streaming Showdown''',
        "tagline": r'''Compare genres and shows by watch time and completion rate, then show the weekly viewing pattern.''',
        "category": r'''Exploratory Analysis & Visualization''',
        "time": r'''35–50 minutes''',
        "skills": r'''groupby, aggregation, rates, categorical charts''',
        "goal": r'''A streaming service wants to know which genres hold attention. Total minutes show popularity; completion rate shows whether viewers finish what they start.''',
        "dataset": [
            (r'''`data/streaming_viewing.csv`''', r'''700 viewing records across 120 users, 5 genres and 30 days.'''),
        ],
        "columns": r'''`user_id`, `date`, `show`, `genre`, `minutes_watched`, `completed`.''',
        "steps": [
            (r"""Load and parse the date""", r"""The date column is text until you convert it with `pd.to_datetime`. After that, `.dt` accessors and weekday grouping work.""", r"""df = pd.read_csv(DATA / "streaming_viewing.csv")
df["date"] = pd.to_datetime(df["date"])"""),
            (r"""Check the data""", r"""Look at dtypes, missing values and the range of `minutes_watched`. A clean dataset still deserves a quick sanity check.""", r"""print(df.dtypes)
print(df["minutes_watched"].describe())"""),
            (r"""Add a weekday label""", r"""`dt.day_name()` creates labels such as `Monday`. An ordered category keeps charts in calendar order instead of alphabetical order.""", r"""df["weekday"] = pd.Categorical(df["date"].dt.day_name(), categories=WEEK_ORDER, ordered=True)"""),
            (r"""Summarise by genre""", r"""`agg` can compute several statistics at once. Total minutes measure volume; mean minutes measure depth; mean of `completed` is a completion rate because the column is 0/1.""", r"""summary = df.groupby("genre").agg(
    total_minutes=("minutes_watched", "sum"),
    avg_minutes=("minutes_watched", "mean"),
    completion_rate=("completed", "mean"),
)"""),
            (r"""Summarise by show""", r"""A second groupby at the show level finds individual hits that may be hidden inside a genre total.""", r"""shows = df.groupby(["genre", "show"]).agg(
    total_minutes=("minutes_watched", "sum"),
    completion_rate=("completed", "mean"),
)"""),
            (r"""Summarise by weekday""", r"""Grouping by the ordered weekday category shows whether viewing rises on weekends.""", r"""weekday = df.groupby("weekday", observed=True).agg(
    total_minutes=("minutes_watched", "sum"),
)"""),
            (r"""Chart volume and completion""", r"""A horizontal bar chart is easy to read for named categories. A second chart shows that the most-watched genre is not always the most-completed genre.""", r"""summary["total_minutes"].sort_values().plot(kind="barh")"""),
            (r"""Write the insight file""", r"""A short text file forces you to state the finding in plain English, not just produce a chart.""", r"""top_genre = summary.index[0]
(OUT / "insights.txt").write_text(f"Most-watched genre: {top_genre}")"""),
        ],
        "outputs": [
            (r'''`outputs/genre_summary.csv`''', r'''Total minutes, average minutes, completion rate and views by genre.'''),
            (r'''`outputs/show_summary.csv`''', r'''The same measures at show level.'''),
            (r'''`outputs/weekday_summary.csv`''', r'''Viewing volume by weekday.'''),
            (r'''`outputs/genre_watch_time.png`''', r'''Genre popularity by total minutes.'''),
            (r'''`outputs/genre_completion.png`''', r'''Completion rate by genre.'''),
            (r'''`outputs/weekday_viewing.png`''', r'''Viewing by day of week.'''),
            (r'''`outputs/insights.txt`''', r'''Plain-English summary of the main findings.'''),
        ],
        "try_it": [
            r'''Find the show with the highest completion rate among shows with at least 30 views.''',
            r'''Compare average minutes for completed versus unfinished views.''',
            r'''Add a stacked bar showing minutes by genre for each weekday.''',
        ],
        "note": r'''Popularity and quality are different questions. Always report both volume and rate.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''07''',
        "folder": r'''07_coffee_rush''',
        "title": r'''The Coffee Shop Morning Rush''',
        "tagline": r'''Find the busiest hours, compare channels, and measure average order value.''',
        "category": r'''Exploratory Analysis & Visualization''',
        "time": r'''35–50 minutes''',
        "skills": r'''derived revenue, pivot_table, heatmaps, AOV''',
        "goal": r'''A café wants to staff the right hours and understand whether mobile orders are worth the same as walk-in orders. Build an hourly and channel view of the business.''',
        "dataset": [
            (r'''`data/coffee_orders.csv`''', r'''800 orders over 14 days, with item, price, channel and timestamp.'''),
        ],
        "columns": r'''`order_id`, `timestamp`, `item`, `category`, `quantity`, `unit_price`, `channel`.''',
        "steps": [
            (r"""Load and parse timestamps""", r"""The timestamp is text until parsed. Sorting and hour extraction require a real datetime.""", r"""df = pd.read_csv(DATA / "coffee_orders.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])"""),
            (r"""Check quantity and price""", r"""A quick `describe()` catches impossible values before they affect revenue.""", r"""print(df[["quantity", "unit_price"]].describe())"""),
            (r"""Create revenue and time fields""", r"""`total = quantity × unit_price` is the order line value. `dt.hour` and `dt.day_name()` create the grouping keys.""", r"""df["total"] = df["quantity"] * df["unit_price"]
df["hour"] = df["timestamp"].dt.hour
df["weekday"] = df["timestamp"].dt.day_name()"""),
            (r"""Summarise by hour""", r""", r'''"Count orders and sum revenue per hour. Average order value is total revenue divided by order count.""", r"""hourly = df.groupby("hour").agg(
    orders=("order_id", "count"),
    revenue=("total", "sum"),
)"""),
            (r"""Compare channels""", r"""The same aggregation by channel answers whether mobile customers spend more or less per order.""", r"""channel = df.groupby("channel").agg(
    orders=("order_id", "count"),
    revenue=("total", "sum"),
    avg_order_value=("total", "mean"),
)"""),
            (r"""Build an hour × weekday table""", r"""`pivot_table` makes a two-dimensional table: weekdays as rows, hours as columns, revenue as the cell value. That is exactly the shape a heatmap needs.""", r"""heat = df.pivot_table(index="weekday", columns="hour",
                       values="total", aggfunc="sum", fill_value=0)"""),
            (r"""Plot the hourly revenue""", r"""The line chart makes the morning peak and afternoon dip easy to see.""", r"""ax.plot(hourly["hour"], hourly["revenue"], marker="o")"""),
            (r"""Plot the heatmap""", r"""Colour intensity shows the strongest weekday-hour combinations. This is useful for shift planning.""", r"""sns.heatmap(heat, cmap="YlGnBu")"""),
            (r"""Write the staffing insight""", r"""State the peak hour, the best channel and the overall average order value in a text file.""", r"""peak_hour = hourly.sort_values("revenue", ascending=False).iloc[0]"""),
        ],
        "outputs": [
            (r'''`outputs/hourly_summary.csv`''', r'''Orders, revenue and AOV for each hour.'''),
            (r'''`outputs/channel_summary.csv`''', r'''Orders, revenue and AOV by channel.'''),
            (r'''`outputs/hour_weekday_heatmap.csv`''', r'''The revenue table behind the heatmap.'''),
            (r'''`outputs/hourly_revenue.png`''', r'''Revenue by hour.'''),
            (r'''`outputs/hour_weekday_heatmap.png`''', r'''Weekday × hour revenue heatmap.'''),
            (r'''`outputs/channel_aov.png`''', r'''Average order value by channel.'''),
            (r'''`outputs/insights.txt`''', r'''Peak hour and channel findings.'''),
        ],
        "try_it": [
            r'''Add a `is_weekend` flag and compare average order value on weekdays versus weekends.''',
            r'''Find the top three items by revenue, not by order count.''',
            r'''Create a second heatmap using order count instead of revenue.''',
        ],
        "note": r'''A heatmap is just a table with colour. Always keep the underlying CSV so the chart can be checked.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''08''',
        "folder": r'''08_study_habits''',
        "title": r'''The Study Habits Explorer''',
        "tagline": r'''Describe distributions, measure relationships, and compare exam scores across study methods.''',
        "category": r'''Exploratory Analysis & Visualization''',
        "time": r'''35–50 minutes''',
        "skills": r'''distributions, correlation, scatterplots, boxplots''',
        "goal": r'''A group of students reports study hours, sleep, attendance, screen time and exam scores. Explore the data before making any claims about what “causes” a better score.''',
        "dataset": [
            (r'''`data/study_habits.csv`''', r'''220 students with five numeric measures and a study-method label.'''),
        ],
        "columns": r'''`student_id`, `study_hours`, `sleep_hours`, `attendance_percent`, `screen_time_hours`, `exam_score`, `study_method`, `year`.''',
        "steps": [
            (r"""Load and inspect""", r"""Start with the shape, missing values and descriptive statistics. This tells you whether the data is plausible before you plot it.""", r"""df = pd.read_csv(DATA / "study_habits.csv")
print(df.describe())"""),
            (r"""Select numeric columns""", r"""Correlation only works on numbers. Keep the five numeric measures in a list so the analysis is explicit.""", r"""numeric_cols = ["study_hours", "sleep_hours", "attendance_percent",
                "screen_time_hours", "exam_score"]"""),
            (r"""Calculate the correlation matrix""", r"""Each cell is a Pearson correlation between two columns. Values near +1 move together; values near -1 move in opposite directions.""", r"""corr = df[numeric_cols].corr().round(2)"""),
            (r"""Summarise study methods""", r"""Grouping compares average exam score and average habits for solo, group and online study.""", r"""summary = df.groupby("study_method").agg(
    avg_exam_score=("exam_score", "mean"),
    avg_study_hours=("study_hours", "mean"),
)"""),
            (r"""Plot distributions""", r"""Histograms with a KDE curve show the shape: symmetric, skewed, or clustered. A 2×2 grid keeps four variables comparable.""", r"""sns.histplot(df["exam_score"], bins=14, kde=True)"""),
            (r"""Plot the correlation heatmap""", r"""The heatmap makes the strongest relationships jump out. Read the `exam_score` row first.""", r"""sns.heatmap(corr, annot=True, cmap="RdBu_r", vmin=-1, vmax=1)"""),
            (r"""Plot study hours against score""", r"""`regplot` adds a straight trend line. It helps you see direction, but it does not prove that studying more causes a higher score.""", r"""sns.regplot(data=df, x="study_hours", y="exam_score")"""),
            (r"""Compare methods with a boxplot""", r"""A boxplot shows the median, middle 50% and potential outliers for each method.""", r"""sns.boxplot(data=df, x="study_method", y="exam_score")"""),
            (r"""Write the findings""", r"""Report the strongest correlation, the best average method and the correlation warning in plain English.""", r"""strongest = corr["exam_score"].drop("exam_score").abs().idxmax()"""),
        ],
        "outputs": [
            (r'''`outputs/correlation_matrix.csv`''', r'''The numeric correlation table.'''),
            (r'''`outputs/method_summary.csv`''', r'''Average score and habits by study method.'''),
            (r'''`outputs/study_distributions.png`''', r'''Histograms of study, sleep, attendance and score.'''),
            (r'''`outputs/correlation_heatmap.png`''', r'''The full correlation matrix.'''),
            (r'''`outputs/study_vs_score.png`''', r'''Study hours versus exam score with a trend line.'''),
            (r'''`outputs/method_boxplot.png`''', r'''Exam score by study method.'''),
            (r'''`outputs/insights.txt`''', r'''Plain-English findings and the correlation caveat.'''),
        ],
        "try_it": [
            r'''Filter to students with attendance above 80% and recompute the correlation.''',
            r'''Compare the mean score for first-year versus final-year students.''',
            r'''Use `sns.pairplot` on the numeric columns and explain what it adds.''',
        ],
        "note": r'''Correlation measures association, not causation. A hidden variable such as motivation could affect both study time and score.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''09''',
        "folder": r'''09_weather_story''',
        "title": r'''The City Weather Story''',
        "tagline": r'''Turn one year of daily weather into a monthly story about temperature, rain and extreme days.''',
        "category": r'''Exploratory Analysis & Visualization''',
        "time": r'''30–45 minutes''',
        "skills": r'''date grouping, monthly aggregation, time-series charts''',
        "goal": r'''A city has 365 days of daily weather. Build a monthly summary, identify extreme days, and present the year in a way a non-specialist can understand.''',
        "dataset": [
            (r'''`data/weather_daily.csv`''', r'''365 daily rows with temperature, rainfall, humidity and wind.'''),
        ],
        "columns": r'''`date`, `temp_max_c`, `temp_min_c`, `rainfall_mm`, `humidity_percent`, `wind_kmh`.''',
        "steps": [
            (r"""Load and parse dates""", r"""A real date column allows grouping by calendar month and finding extreme days.""", r"""df = pd.read_csv(DATA / "weather_daily.csv")
df["date"] = pd.to_datetime(df["date"])"""),
            (r"""Check the ranges""", r"""Are temperatures plausible? Is rainfall ever negative? A quick `describe()` catches data-entry problems.""", r"""print(df[["temp_max_c", "rainfall_mm"]].describe())"""),
            (r"""Create month labels""", r"""`dt.to_period('M')` groups by calendar month. `dt.strftime('%b')` creates short labels such as `Jan` for charts.""", r"""df["month"] = df["date"].dt.to_period("M")
df["month_label"] = df["date"].dt.strftime("%b")"""),
            (r"""Aggregate by month""", r"""For each month, calculate average high, average low, total rain, rainy days and average humidity.""", r"""monthly = df.groupby(["month", "month_label"]).agg(
    avg_max_c=("temp_max_c", "mean"),
    total_rain_mm=("rainfall_mm", "sum"),
)"""),
            (r"""Find extreme days""", r"""`idxmax()` and `idxmin()` return the row labels of the hottest, coldest and wettest days.""", r"""hottest = df.loc[df["temp_max_c"].idxmax()]
coldest = df.loc[df["temp_min_c"].idxmin()]"""),
            (r"""Plot monthly temperature""", r"""Two lines on one chart show the average high and average low across the year.""", r"""ax.plot(monthly["month_label"], monthly["avg_max_c"], marker="o")"""),
            (r"""Plot monthly rainfall""", r"""A bar chart is a good choice for totals because each month is a separate quantity.""", r"""ax.bar(monthly["month_label"], monthly["total_rain_mm"])"""),
            (r"""Plot the temperature distribution""", r"""A histogram shows how many days fell into each temperature band, not just the monthly average.""", r"""sns.histplot(df["temp_max_c"], bins=24, kde=True)"""),
            (r"""Write the weather story""", r"""Save the warmest month, wettest month, hottest day, coldest day and rainy-day count in a text file.""", r"""monthly.loc[monthly["avg_max_c"].idxmax(), "month_label"]"""),
        ],
        "outputs": [
            (r'''`outputs/monthly_weather.csv`''', r'''Monthly temperature, rainfall and humidity summary.'''),
            (r'''`outputs/monthly_temperature.png`''', r'''Average high and low by month.'''),
            (r'''`outputs/monthly_rainfall.png`''', r'''Total rainfall by month.'''),
            (r'''`outputs/temperature_distribution.png`''', r'''Distribution of daily high temperatures.'''),
            (r'''`outputs/insights.txt`''', r'''Extreme days and the main seasonal findings.'''),
        ],
        "try_it": [
            r'''Add a `season` column using month numbers and compare average rainfall by season.''',
            r'''Find the longest run of consecutive rainy days.''',
            r'''Plot humidity against rainfall and describe the relationship.''',
        ],
        "note": r'''Monthly averages hide daily extremes. Report both when the decision depends on unusual days.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''10''',
        "folder": r'''10_funnel_analysis''',
        "title": r'''The E-Commerce Funnel''',
        "tagline": r'''Measure how visitors move from a visit to a purchase, then compare acquisition channels.''',
        "category": r'''Exploratory Analysis & Visualization''',
        "time": r'''35–50 minutes''',
        "skills": r'''funnel conversion, rates, grouped aggregation, charts''',
        "goal": r'''An online store records visits, product views, add-to-carts and purchases by channel. Find where the biggest drop-off happens and which channel converts best.''',
        "dataset": [
            (r'''`data/funnel_events.csv`''', r'''360 rows: 90 days × 4 acquisition channels.'''),
        ],
        "columns": r'''`date`, `channel`, `visits`, `product_views`, `add_to_carts`, `purchases`.''',
        "steps": [
            (r"""Load and parse the date""", r"""The daily table is already aggregated by channel, so each row is a day-channel combination rather than a single user.""", r"""df = pd.read_csv(DATA / "funnel_events.csv")
df["date"] = pd.to_datetime(df["date"])"""),
            (r"""Check the funnel order""", r""", r'''"Each stage should be no larger than the previous one. A broken order means the data needs investigation.""", r"""ordered = ((df["visits"] >= df["product_views"]) &
           (df["product_views"] >= df["add_to_carts"]) &
           (df["add_to_carts"] >= df["purchases"]))"""),
            (r"""Calculate step conversion rates""", r"""A conversion rate is the next stage divided by the previous stage. Keep the overall visit-to-purchase rate as a separate measure.""", r"""df["view_rate"] = df["product_views"] / df["visits"]
df["cart_rate"] = df["add_to_carts"] / df["product_views"]
df["purchase_rate"] = df["purchases"] / df["add_to_carts"]"""),
            (r"""Build the overall funnel""", r"""Sum each stage across every day and channel. The share of visits shows how much of the original audience remains.""", r"""overall = df[STAGES].sum()"""),
            (r"""Compare channels""", r"""Group by channel and recompute the rates. A channel can bring many visits but convert poorly, or bring few visits and convert well.""", r"""channel = df.groupby("channel")[STAGES].sum()"""),
            (r"""Chart the funnel""", r"""A horizontal bar chart with four stages makes the drop-off visible. Label each bar with the count.""", r"""ax.barh(overall_table["stage"], overall_table["count"])"""),
            (r"""Chart final conversion by channel""", r"""A sorted bar chart makes the best and worst channels easy to compare.""", r"""channel["visit_to_purchase"].sort_values().plot(kind="barh")"""),
            (r"""Plot the daily trend""", r"""A line chart checks whether conversion is stable over time or driven by a few unusual days.""", r"""daily["visit_to_purchase"] = daily["purchases"] / daily["visits"]"""),
            (r"""Write the funnel insight""", r"""Identify the smallest step conversion and the best final channel in a text file.""", r"""biggest_drop = overall_table.loc[overall_table["step_conversion"].idxmin(), "stage"]"""),
        ],
        "outputs": [
            (r'''`outputs/overall_funnel.csv`''', r'''Stage counts, share of visits and step conversion.'''),
            (r'''`outputs/channel_funnel.csv`''', r'''The same funnel metrics by channel.'''),
            (r'''`outputs/funnel_chart.png`''', r'''Overall funnel with labelled counts.'''),
            (r'''`outputs/channel_conversion.png`''', r'''Visit-to-purchase rate by channel.'''),
            (r'''`outputs/daily_conversion.png`''', r'''Daily conversion trend.'''),
            (r'''`outputs/insights.txt`''', r'''Biggest drop-off and best channel.'''),
        ],
        "try_it": [
            r'''Calculate revenue per visit if you add an `average_order_value` column.''',
            r'''Compare weekday and weekend conversion rates.''',
            r'''Find the channel with the largest absolute drop from product view to cart.''',
        ],
        "note": r'''A high final conversion rate can still mean few purchases if the channel brings very little traffic. Always show volume next to rate.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''11''',
        "folder": r'''11_ab_test''',
        "title": r'''The A/B Test Lab''',
        "tagline": r'''Compare two landing-page variants with a two-proportion z-test and a confidence interval.''',
        "category": r'''Statistics & Experiments''',
        "time": r'''40–55 minutes''',
        "skills": r'''conversion rates, z-test, confidence intervals, practical significance''',
        "goal": r'''Variant A and variant B were shown to different users. Decide whether B really converts better, or whether the difference could easily be random noise.''',
        "dataset": [
            (r'''`data/ab_test.csv`''', r'''3,000 users, split evenly between variants A and B, with conversion and revenue.'''),
        ],
        "columns": r'''`user_id`, `group`, `converted`, `revenue`.''',
        "steps": [
            (r"""Load and inspect""", r"""Check group sizes and the conversion column. A balanced experiment is easier to compare.""", r"""df = pd.read_csv(DATA / "ab_test.csv")
print(df.groupby("group").size())"""),
            (r"""Calculate conversion rates""", r"""For each group, divide conversions by users. This is the basic metric the test compares.""", r"""summary = df.groupby("group").agg(
    users=("user_id", "count"),
    conversions=("converted", "sum"),
)
summary["conversion_rate"] = summary["conversions"] / summary["users"]"""),
            (r"""Calculate the lift""", r"""The absolute difference is B minus A. The relative lift divides that difference by A's rate.""", r"""diff = b["conversion_rate"] - a["conversion_rate"]
relative_lift = diff / a["conversion_rate"]"""),
            (r"""Run the z-test""", r"""`proportions_ztest` tests the null hypothesis that both groups have the same true conversion rate. The p-value measures how surprising the observed difference would be under that null.""", r"""z_stat, p_value = proportions_ztest(
    [b["conversions"], a["conversions"]],
    [b["users"], a["users"]],
    alternative="two-sided",
)"""),
            (r"""Build a 95% confidence interval""", r"""The interval estimates a plausible range for the true difference. If it excludes zero, the result is statistically significant at the 5% level.""", r"""se = np.sqrt(pA * (1 - pA) / nA + pB * (1 - pB) / nB)
ci_low, ci_high = diff - 1.96 * se, diff + 1.96 * se"""),
            (r"""Check revenue per user""", r""", r'''A higher conversion rate is not automatically better if the revenue per user is worse. Always connect the metric to the business outcome.""", r"""summary["revenue_per_user"] = summary["revenue"] / summary["users"]"""),
            (r"""Write the decision report""", r"""Save the rates, difference, lift, z-statistic, p-value, confidence interval and a plain-English verdict.""", r"""verdict = "statistically significant" if p_value < 0.05 else "not statistically significant\""""),
            (r"""Plot rates with error bars""", r"""The error bars show uncertainty around each group's conversion rate. Overlapping bars are a visual warning that the difference may be noisy.""", r"""ax.bar(groups, rates, yerr=errors, capsize=8)"""),
        ],
        "outputs": [
            (r'''`outputs/ab_test_results.txt`''', r'''Full statistical result and interpretation.'''),
            (r'''`outputs/conversion_rates.png`''', r'''Conversion rate by variant with 95% error bars.'''),
            (r'''`outputs/revenue_per_user.png`''', r'''Revenue per user by variant.'''),
        ],
        "try_it": [
            r'''Re-run the test with a one-sided alternative and explain when that is appropriate.''',
            r'''Split the data by revenue quartile and compare conversion within each quartile.''',
            r'''Change the significance level to 1% and see whether the verdict changes.''',
        ],
        "note": r'''Statistical significance is not the same as business importance. A tiny lift can be significant with a huge sample and still not be worth shipping.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''12''',
        "folder": r'''12_study_break''',
        "title": r'''The Study Break Experiment''',
        "tagline": r'''Compare exam scores for students who took a break versus students who studied straight through.''',
        "category": r'''Statistics & Experiments''',
        "time": r'''35–50 minutes''',
        "skills": r'''t-test, Cohen's d, confidence intervals, boxplots''',
        "goal": r'''Two groups of students studied the same material. One group took a short break; the other did not. Test whether the average scores differ and how large the difference is.''',
        "dataset": [
            (r'''`data/study_break.csv`''', r'''80 students: 40 in the break group and 40 in the no-break group.'''),
        ],
        "columns": r'''`student_id`, `group`, `score`, `study_minutes`.''',
        "steps": [
            (r"""Load and check groups""", r"""Count rows, means and standard deviations for each group. This is the descriptive part before any test.""", r"""df = pd.read_csv(DATA / "study_break.csv")
print(df.groupby("group")["score"].agg(["count", "mean", "std"]))"""),
            (r"""Separate the two score vectors""", r"""The t-test needs two separate arrays, one per group.""", r"""break_scores = df.loc[df["group"] == "break", "score"]
no_break_scores = df.loc[df["group"] == "no_break", "score"]"""),
            (r"""Run Welch's t-test""", r"""The null hypothesis is that both groups have the same average score. Welch's version does not assume equal variances.""", r"""t_stat, p_value = stats.ttest_ind(
    break_scores, no_break_scores, equal_var=False
)"""),
            (r"""Calculate Cohen's d""", r"""A p-value says whether a difference is likely, not how big it is. Cohen's d standardises the mean difference by the pooled standard deviation.""", r"""pooled_sd = np.sqrt(((n1 - 1) * sd1**2 + (n2 - 1) * sd2**2) / (n1 + n2 - 2))
cohens_d = (mean1 - mean2) / pooled_sd"""),
            (r"""Build a 95% confidence interval""", r"""The interval shows the plausible range for the true mean difference. It is more informative than a bare p-value.""", r"""se = np.sqrt(sd1**2 / n1 + sd2**2 / n2)
ci_low, ci_high = diff - t_critical * se, diff + t_critical * se"""),
            (r"""Write the result""", r"""Report the means, difference, t-statistic, p-value, Cohen's d and confidence interval together.""", r"""verdict = "statistically significant" if p_value < 0.05 else "not statistically significant\""""),
            (r"""Plot the distributions""", r"""A boxplot with individual points shows the median, spread and outliers. The points prevent the box from hiding the raw data.""", r"""sns.boxplot(data=df, x="group", y="score")
sns.stripplot(data=df, x="group", y="score")"""),
            (r"""Plot the means with error bars""", r"""The bar chart summarises the group means, and the error bars show uncertainty around each mean.""", r"""ax.bar(["break", "no_break"], means, yerr=errors, capsize=8)"""),
        ],
        "outputs": [
            (r'''`outputs/results.txt`''', r'''Means, t-test, effect size, confidence interval and verdict.'''),
            (r'''`outputs/study_break_boxplot.png`''', r'''Score distributions with individual students shown.'''),
            (r'''`outputs/group_means.png`''', r'''Group means with 95% error bars.'''),
        ],
        "try_it": [
            r'''Run the standard Student t-test with `equal_var=True` and compare the p-value.''',
            r'''Check whether study minutes differ between the groups. If they do, the comparison is confounded.''',
            r'''Calculate a 99% confidence interval instead of 95%.''',
        ],
        "note": r'''A statistically significant result does not prove that breaks caused the score difference. Random assignment and a clean protocol matter.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''13''',
        "folder": r'''13_satisfaction_survey''',
        "title": r'''The Customer Satisfaction Survey''',
        "tagline": r'''Compare satisfaction across segments and test whether recommendation is associated with segment.''',
        "category": r'''Statistics & Experiments''',
        "time": r'''35–50 minutes''',
        "skills": r'''confidence intervals, chi-square test, Cramér's V, stacked bars''',
        "goal": r'''New, returning and VIP customers rated satisfaction and answered whether they would recommend the service. Compare the groups and test the recommendation pattern.''',
        "dataset": [
            (r'''`data/satisfaction_survey.csv`''', r'''300 respondents with segment, satisfaction, recommendation and age.'''),
        ],
        "columns": r'''`respondent_id`, `segment`, `satisfaction`, `would_recommend`, `age`.''',
        "steps": [
            (r"""Load and check groups""", r"""Count respondents per segment and inspect the satisfaction range.""", r"""df = pd.read_csv(DATA / "satisfaction_survey.csv")
print(df.groupby("segment").size())"""),
            (r"""Summarise satisfaction""", r"""For each segment, calculate the mean, standard deviation, recommendation rate and a 95% margin of error.""", r"""summary = df.groupby("segment").agg(
    respondents=("respondent_id", "count"),
    avg_satisfaction=("satisfaction", "mean"),
    sd_satisfaction=("satisfaction", "std"),
    recommend_rate=("would_recommend", "mean"),
)"""),
            (r"""Build a contingency table""", r"""`pd.crosstab` counts how many respondents in each segment said yes versus no. This is the input for the chi-square test.""", r"""table = pd.crosstab(df["segment"], df["would_recommend"])"""),
            (r"""Run the chi-square test""", r"""The null hypothesis is independence: recommendation does not depend on segment. A small p-value suggests an association.""", r"""chi2, p_value, dof, expected = chi2_contingency(table)"""),
            (r"""Calculate Cramér's V""", r"""Cramér's V turns chi-square into an effect size between 0 and 1. It helps distinguish a real association from a trivial one with a large sample.""", r"""cramers_v = np.sqrt(chi2 / (n * (min(table.shape) - 1)))"""),
            (r"""Write the result""", r"""Report the average satisfaction, recommendation rate, chi-square, p-value, Cramér's V and the expected counts.""", r"""print(f"chi-square={chi2:.3f}, p={p_value:.5f}, V={cramers_v:.2f}")"""),
            (r"""Plot satisfaction with error bars""", r"""A bar chart with error bars shows both the average and the uncertainty around it.""", r"""ax.bar(summary.index, summary["avg_satisfaction"],
       yerr=summary["margin_of_error"], capsize=8)"""),
            (r"""Plot recommendation shares""", r"""A 100% stacked bar shows the yes/no mix within each segment. It is easier to compare composition than raw counts.""", r"""rec_share = pd.crosstab(df["segment"], df["would_recommend"], normalize="index")"""),
        ],
        "outputs": [
            (r'''`outputs/segment_summary.csv`''', r'''Satisfaction and recommendation metrics by segment.'''),
            (r'''`outputs/results.txt`''', r'''Chi-square result, effect size and expected counts.'''),
            (r'''`outputs/satisfaction_by_segment.png`''', r'''Average satisfaction with 95% error bars.'''),
            (r'''`outputs/recommend_by_segment.png`''', r'''Recommendation mix by segment.'''),
        ],
        "try_it": [
            r'''Run the chi-square test with age groups instead of segments.''',
            r'''Compare average satisfaction for recommenders versus non-recommenders.''',
            r'''Check whether the expected counts are all at least 5, a common rule of thumb for chi-square.''',
        ],
        "note": r'''Satisfaction is ordinal (1–5). Treating the average as a number is common but loses some information; always look at the full distribution too.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''14''',
        "folder": r'''14_sleep_focus''',
        "title": r'''The Sleep & Focus Correlation''',
        "tagline": r'''Measure whether sleep, caffeine and screen time move together with focus.''',
        "category": r'''Statistics & Experiments''',
        "time": r'''30–45 minutes''',
        "skills": r'''Pearson correlation, Spearman correlation, regression plots''',
        "goal": r'''Students recorded sleep, caffeine, screen time and focus. Measure the relationships, separate correlation from causation, and present the evidence honestly.''',
        "dataset": [
            (r'''`data/sleep_focus.csv`''', r'''150 students with sleep, focus, caffeine and screen time.'''),
        ],
        "columns": r'''`student_id`, `sleep_hours`, `focus_score`, `caffeine_mg`, `screen_time_hours`.''',
        "steps": [
            (r"""Load and inspect""", r"""Check ranges and missing values. Correlations can be distorted by impossible values such as 30 hours of sleep.""", r"""df = pd.read_csv(DATA / "sleep_focus.csv")
print(df.describe())"""),
            (r"""Calculate the correlation matrix""", r"""A matrix shows every pairwise Pearson correlation at once. Read the `focus_score` column for the main relationships.""", r"""corr = df.drop(columns=["student_id"]).corr(method="pearson")"""),
            (r"""Test sleep versus focus""", r"""`pearsonr` returns the correlation and a p-value for the null hypothesis of no linear relationship.""", r"""r_value, p_value = pearsonr(df["sleep_hours"], df["focus_score"])"""),
            (r"""Add Spearman correlation""", r"""Spearman works on ranks. It is useful when the relationship is monotonic but not perfectly linear, or when there are outliers.""", r"""rho_value, rho_p = spearmanr(df["sleep_hours"], df["focus_score"])"""),
            (r"""Check the other variables""", r"""Repeat the Pearson test for caffeine and screen time. Report all relationships, not just the one that supports your story.""", r"""for column in ["caffeine_mg", "screen_time_hours"]:
    r, p = pearsonr(df[column], df["focus_score"])"""),
            (r"""Interpret the strength""", r"""A rough guide: |r| below 0.4 is weak, 0.4–0.7 is moderate, and above 0.7 is strong. The sign gives the direction.""", r"""strength = "strong" if abs(r_value) >= 0.7 else "moderate" if abs(r_value) >= 0.4 else "weak\""""),
            (r"""Plot sleep versus focus""", r"""`regplot` adds a linear trend line to the scatterplot. It makes the direction visible without hiding the individual points.""", r"""sns.regplot(data=df, x="sleep_hours", y="focus_score")"""),
            (r"""Plot the correlation heatmap""", r"""The heatmap gives a quick overview of all pairwise relationships and makes the strongest cells easy to spot.""", r"""sns.heatmap(corr, annot=True, cmap="RdBu_r", vmin=-1, vmax=1)"""),
            (r"""Write the caveat""", r"""State the correlation, the p-value and the fact that correlation does not prove causation.""", r"""results.append("Correlation does not prove causation.")"""),
        ],
        "outputs": [
            (r'''`outputs/correlation_matrix.csv`''', r'''Pearson correlations for all numeric columns.'''),
            (r'''`outputs/results.txt`''', r'''Pearson and Spearman results plus interpretation and caveats.'''),
            (r'''`outputs/sleep_focus_scatter.png`''', r'''Sleep hours versus focus with a trend line.'''),
            (r'''`outputs/correlation_heatmap.png`''', r'''Full correlation heatmap.'''),
            (r'''`outputs/screen_focus_scatter.png`''', r'''Screen time versus focus.'''),
        ],
        "try_it": [
            r'''Filter to students with less than 200 mg of caffeine and recompute the sleep correlation.''',
            r'''Compare Pearson and Spearman results and explain any difference.''',
            r'''Add a simple linear regression with `scipy.stats.linregress` and interpret the slope.''',
        ],
        "note": r'''A third variable such as stress or workload could influence both sleep and focus. The analysis cannot rule that out.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''15''',
        "folder": r'''15_delivery_anova''',
        "title": r'''The Delivery Time ANOVA''',
        "tagline": r'''Compare delivery times across three warehouses with ANOVA and a Tukey post-hoc test.''',
        "category": r'''Statistics & Experiments''',
        "time": r'''40–55 minutes''',
        "skills": r'''one-way ANOVA, Tukey HSD, eta squared, group comparisons''',
        "goal": r'''Three warehouses serve the same region. Compare their delivery times, test whether at least one warehouse differs, and identify which pairs differ.''',
        "dataset": [
            (r'''`data/delivery_times.csv`''', r'''180 orders across warehouses A, B and C.'''),
        ],
        "columns": r'''`order_id`, `warehouse`, `delivery_days`, `distance_km`, `order_value`.''',
        "steps": [
            (r"""Load and check groups""", r"""Count orders and summarise delivery days for each warehouse before testing.""", r"""df = pd.read_csv(DATA / "delivery_times.csv")
print(df.groupby("warehouse")["delivery_days"].agg(["count", "mean", "std"]))"""),
            (r"""Summarise the warehouses""", r"""A compact table with average delivery time, standard deviation and average distance makes the raw pattern visible.""", r"""summary = df.groupby("warehouse").agg(
    orders=("order_id", "count"),
    avg_delivery_days=("delivery_days", "mean"),
    sd_delivery_days=("delivery_days", "std"),
)"""),
            (r"""Run one-way ANOVA""", r"""The null hypothesis is that all three warehouses have the same average delivery time. The F-statistic compares between-group variation with within-group variation.""", r"""groups = [g["delivery_days"].values for _, g in df.groupby("warehouse")]
f_stat, p_value = f_oneway(*groups)"""),
            (r"""Calculate eta squared""", r"""Eta squared is the share of total variation explained by warehouse differences. It is an effect size, not a p-value.""", r"""eta_squared = ss_between / (ss_between + ss_within)"""),
            (r"""Run Tukey HSD""", r"""ANOVA says “at least one group differs”, not which one. Tukey compares every pair while controlling the family-wise error rate.""", r"""tukey = pairwise_tukeyhsd(
    endog=df["delivery_days"], groups=df["warehouse"], alpha=0.05
)"""),
            (r"""Read the Tukey table""", r"""`meandiff` is the difference in means, `p-adj` is the adjusted p-value, and `reject=True` means the pair differs significantly.""", r"""tukey_table = pd.DataFrame(
    tukey.summary().data[1:], columns=tukey.summary().data[0]
)"""),
            (r"""Write the result""", r"""Report F, p, eta squared and the pairwise Tukey comparisons together.""", r"""print(f"F={f_stat:.3f}, p={p_value:.5f}, eta squared={eta_squared:.3f}")"""),
            (r"""Plot the distributions""", r"""Boxplots with individual points show the spread, median and outliers for each warehouse.""", r"""sns.boxplot(data=df, x="warehouse", y="delivery_days")
sns.stripplot(data=df, x="warehouse", y="delivery_days")"""),
            (r"""Plot the means with error bars""", r"""The bar chart summarises the group means and shows uncertainty around each mean.""", r"""ax.bar(summary.index, summary["avg_delivery_days"],
       yerr=errors, capsize=8)"""),
        ],
        "outputs": [
            (r'''`outputs/warehouse_summary.csv`''', r'''Delivery-time summary by warehouse.'''),
            (r'''`outputs/anova_results.txt`''', r'''F-test, effect size, Tukey table and interpretation.'''),
            (r'''`outputs/tukey_results.csv`''', r'''Pairwise Tukey comparisons.'''),
            (r'''`outputs/delivery_boxplot.png`''', r'''Delivery-time distributions by warehouse.'''),
            (r'''`outputs/warehouse_means.png`''', r'''Average delivery time with 95% error bars.'''),
        ],
        "try_it": [
            r'''Add `distance_km` as a covariate in a two-way model and see whether the warehouse effect shrinks.''',
            r'''Compare the ANOVA result with a Kruskal–Wallis test, which does not assume normality.''',
            r'''Recode delivery time into fast/medium/slow and run a chi-square test by warehouse.''',
        ],
        "note": r'''ANOVA assumes independent observations and roughly normal residuals. The boxplot and group sizes help you judge whether that is plausible.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''16''',
        "folder": r'''16_customer_segments''',
        "title": r'''The Customer Segmentation Studio''',
        "tagline": r'''Use RFM and K-Means to group customers into useful, explainable segments.''',
        "category": r'''Business Analytics & Prediction''',
        "time": r'''45–60 minutes''',
        "skills": r'''RFM, StandardScaler, K-Means, elbow method, silhouette score''',
        "goal": r'''A business has 400 customers with recency, frequency and monetary value. Group them into segments that suggest different marketing actions.''',
        "dataset": [
            (r'''`data/customers.csv`''', r'''400 customers with RFM measures, signup age and channel.'''),
            (r'''`data/customers_with_segments.csv`''', r'''The output table with a K-Means cluster and a segment name.'''),
        ],
        "columns": r'''`customer_id`, `recency_days`, `frequency`, `monetary`, `signup_days_ago`, `channel`.''',
        "steps": [
            (r"""Load and inspect the RFM columns""", r"""Recency is days since last purchase (lower is better). Frequency is purchase count (higher is better). Monetary is total spend (higher is better).""", r"""df = pd.read_csv(DATA / "customers.csv")
print(df[["recency_days", "frequency", "monetary"]].describe())"""),
            (r"""Scale the features""", r"""K-Means uses distance. Without scaling, monetary value in dollars would dominate frequency counts. `StandardScaler` puts each feature on a comparable scale.""", r"""scaler = StandardScaler()
scaled = scaler.fit_transform(df[["recency_days", "frequency", "monetary"]])"""),
            (r"""Try several values of K""", r"""The elbow method plots inertia against K. Inertia falls as clusters increase; look for the point where the improvement slows down.""", r"""for k in range(2, 9):
    model = KMeans(n_clusters=k, random_state=42, n_init=10).fit(scaled)
    inertias.append(model.inertia_)"""),
            (r"""Fit the final model""", r"""Choose K=4 for this dataset. `fit_predict` both fits the clusters and assigns each customer to one.""", r"""model = KMeans(n_clusters=4, random_state=42, n_init=10)
df["cluster"] = model.fit_predict(scaled)"""),
            (r"""Measure cluster separation""", r"""The silhouette score summarises how similar each point is to its own cluster compared with the next closest cluster. Higher is better, up to 1.""", r"""silhouette = silhouette_score(scaled, df["cluster"])"""),
            (r"""Profile the clusters""", r"""Go back to the original RFM units and compute the average recency, frequency and monetary value for each cluster.""", r"""profiles = df.groupby("cluster").agg(
    avg_recency_days=("recency_days", "mean"),
    avg_frequency=("frequency", "mean"),
    avg_monetary=("monetary", "mean"),
)"""),
            (r"""Name the segments""", r"""Rank the clusters on recency, frequency and monetary value, then map the order to plain-English names such as `High-value loyal` and `At risk / dormant`.""", r"""segment_names = ["High-value loyal", "Promising", "Occasional", "At risk / dormant"]"""),
            (r"""Save the labelled customers""", r"""Write the original rows plus `cluster` and `segment_name` so the business team can filter and act on the segments.""", r"""df.to_csv(DATA / "customers_with_segments.csv", index=False)"""),
            (r"""Plot the elbow curve""", r"""The elbow chart documents why K=4 is a reasonable choice instead of an arbitrary one.""", r"""ax.plot(elbow["k"], elbow["inertia"], marker="o")"""),
            (r"""Plot the segments""", r"""A scatterplot of frequency versus monetary value, coloured by segment, makes the business meaning visible.""", r"""sns.scatterplot(data=df, x="frequency", y="monetary", hue="segment_name")"""),
        ],
        "outputs": [
            (r'''`data/customers_with_segments.csv`''', r'''Every customer with a cluster and segment name.'''),
            (r'''`outputs/elbow_values.csv`''', r'''Inertia for K=2 through K=8.'''),
            (r'''`outputs/elbow_plot.png`''', r'''The elbow chart.'''),
            (r'''`outputs/segment_profiles.csv`''', r'''Average RFM values by named segment.'''),
            (r'''`outputs/segment_scatter.png`''', r'''Frequency versus monetary value by segment.'''),
            (r'''`outputs/recency_scatter.png`''', r'''Recency versus monetary value by segment.'''),
            (r'''`outputs/insights.txt`''', r'''Segment profiles and suggested actions.'''),
        ],
        "try_it": [
            r'''Try K=3 and K=5 and compare the segment profiles.''',
            r'''Use quantile-based RFM scores instead of K-Means and compare the groups.''',
            r'''Add `signup_days_ago` as a feature and see whether the segments change.''',
        ],
        "note": r'''Clusters are not automatically meaningful. Always translate them back into original units and ask whether the business can act on them.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''17''',
        "folder": r'''17_churn_model''',
        "title": r'''The Churn Early-Warning System''',
        "tagline": r'''Train a logistic regression model that estimates each customer's chance of churning.''',
        "category": r'''Business Analytics & Prediction''',
        "time": r'''45–60 minutes''',
        "skills": r'''logistic regression, train/test split, scaling, precision/recall, ROC-AUC''',
        "goal": r'''A subscription business wants to flag customers who may leave. Build an interpretable model, evaluate it honestly on unseen customers, and explain the coefficients.''',
        "dataset": [
            (r'''`data/churn.csv`''', r'''800 customers with tenure, charges, support calls, late payments, usage and churn label.'''),
        ],
        "columns": r'''`customer_id`, `tenure_months`, `monthly_charges`, `support_calls`, `late_payments`, `usage_hours`, `churned`.''',
        "steps": [
            (r"""Load and inspect""", r"""Check the churn rate and missing values. An imbalanced target changes how you should read accuracy.""", r"""df = pd.read_csv(DATA / "churn.csv")
print(df["churned"].mean())"""),
            (r"""Choose features and target""", r"""Drop the customer ID because it is an identifier, not a behavioural signal. The target is `churned`.""", r"""feature_cols = ["tenure_months", "monthly_charges", "support_calls",
                "late_payments", "usage_hours"]
X, y = df[feature_cols], df["churned"]"""),
            (r"""Split into train and test""", r"""The model learns on 70% of customers and is evaluated on the 30% it has never seen. `stratify=y` keeps the churn rate similar in both sets.""", r"""X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)"""),
            (r"""Scale the features""", r"""Fit the scaler on the training data only, then apply the same transformation to the test data. This prevents test information from leaking into training.""", r"""scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)"""),
            (r"""Fit logistic regression""", r"""Logistic regression models the log-odds of churn as a weighted sum of the features. It is a strong, interpretable baseline for binary outcomes.""", r"""model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)"""),
            (r"""Make predictions""", r"""`predict` returns the 0/1 class. `predict_proba[:, 1]` returns the estimated probability of churn, which is useful for ranking customers.""", r"""y_pred = model.predict(X_test_scaled)
y_prob = model.predict_proba(X_test_scaled)[:, 1]"""),
            (r"""Evaluate the model""", r"""Accuracy alone can be misleading. Also report precision, recall, F1 and ROC-AUC, and compare accuracy with the majority-class baseline.""", r"""accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)"""),
            (r"""Explain the coefficients""", r"""A positive coefficient is associated with more churn; a negative coefficient with less. `exp(coefficient)` is the odds ratio.""", r"""coef_table = pd.DataFrame({
    "feature": feature_cols,
    "coefficient": model.coef_[0],
    "odds_ratio": np.exp(model.coef_[0]),
})"""),
            (r"""Plot the confusion matrix""", r"""The matrix shows true positives, true negatives, false positives and false negatives. It makes the cost of mistakes concrete.""", r"""sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")"""),
            (r"""Plot the ROC curve""", r"""The ROC curve shows the trade-off between catching churners and falsely flagging loyal customers. AUC summarises it in one number.""", r"""fpr, tpr, _ = roc_curve(y_test, y_prob)"""),
        ],
        "outputs": [
            (r'''`outputs/results.txt`''', r'''Metrics, confusion matrix, coefficients and interpretation.'''),
            (r'''`outputs/churn_coefficients.csv`''', r'''Coefficient and odds ratio for every feature.'''),
            (r'''`outputs/churn_coefficients.png`''', r'''Signed coefficient chart.'''),
            (r'''`outputs/confusion_matrix.png`''', r'''Test-set confusion matrix.'''),
            (r'''`outputs/roc_curve.png`''', r'''ROC curve with AUC.'''),
        ],
        "try_it": [
            r'''Lower the classification threshold from 0.5 to 0.3 and see how recall and precision change.''',
            r'''Remove `late_payments` and compare the AUC. Does the model lose much?''',
            r'''Add a `high_support` flag for customers with more than three calls and compare coefficients.''',
        ],
        "note": r'''A churn model is a decision aid, not a verdict. The business must decide how much a false positive or false negative costs.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''18''',
        "folder": r'''18_sales_forecast''',
        "title": r'''The Sales Forecast Baseline''',
        "tagline": r'''Build a simple sales forecast with a moving average and a linear trend, then test it on the last six months.''',
        "category": r'''Business Analytics & Prediction''',
        "time": r'''40–55 minutes''',
        "skills": r'''time index, moving average, train/test split, MAE, RMSE''',
        "goal": r'''A business has 36 months of sales. Build an explainable baseline, measure its error on a holdout period, and forecast the next three months.''',
        "dataset": [
            (r'''`data/monthly_sales.csv`''', r'''36 monthly sales values from 2023 through 2025.'''),
        ],
        "columns": r'''`month`, `sales`.''',
        "steps": [
            (r"""Load and parse the month""", r"""The month is stored as `YYYY-MM`. Appending `-01` and parsing gives a real date that can be sorted and plotted.""", r"""df = pd.read_csv(DATA / "monthly_sales.csv")
df["month"] = pd.to_datetime(df["month"] + "-01")"""),
            (r"""Create a time index""", r"""A linear model needs a number, not a date. `t = 0, 1, 2, ...` represents the passage of time.""", r"""df["t"] = np.arange(len(df))"""),
            (r"""Add a moving average""", r"""`rolling(3).mean()` smooths short-term noise using the current month and the two before it.""", r"""df["moving_avg_3"] = df["sales"].rolling(window=3).mean()"""),
            (r"""Hold out the last six months""", r"""The model trains on the first 30 months and is tested on the last 6. The test period must come after the training period, never before.""", r"""train = df.iloc[:-6]
test = df.iloc[-6:]"""),
            (r"""Fit a linear trend""", r"""`LinearRegression` finds the straight line that minimises squared error between the time index and sales.""", r"""model = LinearRegression()
model.fit(train[["t"]], train["sales"])"""),
            (r"""Predict and measure error""", r""", r'''"MAE is the average absolute miss in sales dollars. RMSE penalises larger misses more heavily.""", r"""test_pred = model.predict(test[["t"]])
mae = mean_absolute_error(test["sales"], test_pred)
rmse = np.sqrt(mean_squared_error(test["sales"], test_pred))"""),
            (r"""Compare with a naive baseline""", r"""A forecast is only useful if it beats a simple benchmark. The naive forecast repeats the last training value for every future month.""", r"""naive_pred = np.repeat(train["sales"].iloc[-1], len(test))
naive_mae = mean_absolute_error(test["sales"], naive_pred)"""),
            (r"""Forecast the next three months""", r"""Extend the time index beyond the observed data and use the fitted line to predict.""", r"""future_t = np.arange(len(df), len(df) + 3).reshape(-1, 1)
future_pred = model.predict(future_t)"""),
            (r"""Plot the forecast""", r"""The chart shows history, the moving average, the test predictions and the future forecast on the same timeline.""", r"""ax.plot(df["month"], df["sales"], label="Actual")
ax.plot(forecast["month"], forecast["forecast_sales"], label="Forecast")"""),
            (r"""Explain the limitation""", r"""A linear trend captures direction but not seasonality or sudden shocks. The report states this explicitly.""", r"""results.append("A linear trend does not capture seasonality.")"""),
        ],
        "outputs": [
            (r'''`outputs/results.txt`''', r'''MAE, RMSE, naive baseline, trend slope and forecast.'''),
            (r'''`outputs/next_three_months.csv`''', r'''Forecast values for the next three months.'''),
            (r'''`outputs/sales_forecast.png`''', r'''History, moving average, test predictions and future forecast.'''),
            (r'''`outputs/test_predictions.png`''', r'''Actual versus predicted sales in the test period.'''),
        ],
        "try_it": [
            r'''Add month-of-year dummy variables and compare test MAE with the plain trend.''',
            r'''Use a 6-month moving average instead of 3 and describe the trade-off.''',
            r'''Evaluate with rolling-origin validation instead of a single holdout.''',
        ],
        "note": r'''A more complex model is not automatically better. Always compare against a naive baseline and report the error in the original units.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''19''',
        "folder": r'''19_recommendation''',
        "title": r'''The Product Recommendation Engine''',
        "tagline": r'''Use purchase history and cosine similarity to recommend related and personalised products.''',
        "category": r'''Business Analytics & Prediction''',
        "time": r'''45–60 minutes''',
        "skills": r'''pivot tables, cosine similarity, cold-start fallback, recommendation logic''',
        "goal": r'''A store has transaction lines showing which customer bought which product. Build a simple recommender that suggests similar products and personalised products for a customer.''',
        "dataset": [
            (r'''`data/transactions.csv`''', r'''About 700 transaction lines across 120 customers and 20 products.'''),
        ],
        "columns": r'''`transaction_id`, `customer_id`, `product`.''',
        "steps": [
            (r"""Load and inspect""", r"""Each row is one product line in a transaction. A customer can appear many times, which is exactly what a recommender needs.""", r"""df = pd.read_csv(DATA / "transactions.csv")"""),
            (r"""Count product popularity""", r"""`value_counts()` gives a baseline: recommend the most popular products. It is simple but ignores personalisation.""", r"""product_counts = df["product"].value_counts()"""),
            (r"""Build a product-by-customer matrix""", r"""Rows are products, columns are customers, and cells count purchases. This is the table used to compare products.""", r"""product_matrix = df.pivot_table(
    index="product", columns="customer_id",
    values="transaction_id", aggfunc="count", fill_value=0,
)"""),
            (r"""Calculate cosine similarity""", r"""Cosine similarity compares the angle between two purchase vectors. A score near 1 means the same customers buy both products.""", r"""similarity = cosine_similarity(product_matrix)
sim_df = pd.DataFrame(similarity, index=product_matrix.index,
                      columns=product_matrix.index)"""),
            (r"""Recommend similar products""", r"""For a chosen product, drop itself from the similarity row and take the highest remaining scores.""", r"""scores = sim_df.loc[product].drop(product).sort_values(ascending=False)"""),
            (r"""Build a customer-by-product matrix""", r"""Transpose the perspective: rows are customers, columns are products, and cells count purchases.""", r"""customer_matrix = df.pivot_table(
    index="customer_id", columns="product",
    values="transaction_id", aggfunc="count", fill_value=0,
)"""),
            (r"""Score unseen products for a customer""", r""", r'''"For every product the customer has not bought, add its similarity to the products they did buy, weighted by how often they bought them.""", r"""for product in owned_products:
    scores += sim_df[product] * owned[product]
scores = scores.drop(labels=owned_products, errors="ignore")"""),
            (r"""Add a cold-start fallback""", r"""If a customer already owns every product in their similar cluster, all similarity scores can be zero. Fall back to popular products instead of showing an empty list.""", r"""if scores.max() <= 0:
    scores = product_counts.reindex(scores.index).fillna(0)"""),
            (r"""Save recommendations""", r"""Write the top five recommendations for the first 20 customers to a CSV for review.""", r"""recommendations.to_csv(OUT / "customer_recommendations.csv", index=False)"""),
            (r"""Plot the similarity heatmap""", r"""The heatmap shows which products form natural groups. Strong blocks often correspond to product categories.""", r"""sns.heatmap(sim_df, cmap="YlGnBu")"""),
            (r"""State the limitation""", r"""This is a similarity/popularity baseline. It does not use ratings, prices or click feedback.""", r"""results.append("This is not a production recommender.")"""),
        ],
        "outputs": [
            (r'''`outputs/product_counts.csv`''', r'''Purchase count for every product.'''),
            (r'''`outputs/product_similarity.csv`''', r'''20×20 product similarity matrix.'''),
            (r'''`outputs/customer_recommendations.csv`''', r'''Top five recommendations for 20 customers.'''),
            (r'''`outputs/top_products.png`''', r'''Top 10 products by purchase lines.'''),
            (r'''`outputs/similarity_heatmap.png`''', r'''Product-to-product similarity heatmap.'''),
            (r'''`outputs/results.txt`''', r'''Example recommendations and method explanation.'''),
        ],
        "try_it": [
            r'''Increase the recommendation list to 10 and inspect whether the extra items are sensible.''',
            r'''Add a simple hit-rate test: hide one purchased product per customer and see whether it appears in the top five.''',
            r'''Use the customer-by-customer similarity matrix to recommend products from similar customers instead.''',
        ],
        "note": r'''A recommender can look impressive on a heatmap and still be useless in production. Real evaluation needs clicks, purchases and a holdout period.''',
    },
    # ------------------------------------------------------------------
    {
        "number": r'''20''',
        "folder": r'''20_pricing_elasticity''',
        "title": r'''The Pricing & Demand Analyzer''',
        "tagline": r'''Estimate price elasticity with a log-log regression and simulate how demand changes when price moves.''',
        "category": r'''Business Analytics & Prediction''',
        "time": r'''45–60 minutes''',
        "skills": r'''log-log regression, elasticity, OLS, simulation, causal caution''',
        "goal": r'''A business has monthly price, quantity, promotion and competitor-price data for five products. Estimate how sensitive demand is to price and simulate a price change.''',
        "dataset": [
            (r'''`data/pricing_data.csv`''', r'''120 product-month rows: 5 products × 24 months.'''),
        ],
        "columns": r'''`product`, `month`, `price`, `quantity`, `promotion`, `competitor_price`.''',
        "steps": [
            (r"""Load and check positivity""", r"""Logs require positive values. Check price and quantity before transforming them.""", r"""df = pd.read_csv(DATA / "pricing_data.csv")
print((df["price"] <= 0).sum(), (df["quantity"] <= 0).sum())"""),
            (r"""Create log variables""", r"""`np.log` compresses multiplicative relationships into additive ones. In a log-log model, the price coefficient is an elasticity.""", r"""df["log_quantity"] = np.log(df["quantity"])
df["log_price"] = np.log(df["price"])
df["log_competitor_price"] = np.log(df["competitor_price"])"""),
            (r"""Fit the main regression""", r"""`sm.add_constant` adds the intercept. Control for promotion and competitor price so the price coefficient is not contaminated by those effects.""", r"""X = sm.add_constant(df[["log_price", "promotion", "log_competitor_price"]])
model = sm.OLS(df["log_quantity"], X).fit()"""),
            (r"""Read the elasticity""", r"""The coefficient on `log_price` is the estimated percentage change in quantity for a 1% change in price. Values below -1 are elastic; between -1 and 0 are inelastic.""", r"""elasticity = model.params["log_price"]"""),
            (r"""Check significance and fit""", r"""The p-value tests whether the elasticity is different from zero. R-squared shows how much of the variation the model explains.""", r"""print(model.pvalues["log_price"], model.rsquared)"""),
            (r"""Fit separate models per product""", r"""Pooling products can hide different customer responses. A per-product loop estimates a separate elasticity for each one.""", r"""for product, group in df.groupby("product"):
    m = sm.OLS(group["log_quantity"], sm.add_constant(
        group[["log_price", "promotion", "log_competitor_price"]]
    )).fit()"""),
            (r"""Simulate a demand curve""", r"""Hold promotion off and competitor price at its average, then vary price across a range. `exp(prediction)` converts log quantity back to units.""", r"""simulation["predicted_quantity"] = np.exp(product_model.predict(sim_X))"""),
            (r"""Plot the demand curve""", r"""The observed points show the raw months; the line shows the model's predicted demand at each price.""", r"""ax.plot(simulation["price"], simulation["predicted_quantity"])
ax.scatter(product_df["price"], product_df["quantity"])"""),
            (r"""Plot elasticity by product""", r"""A sorted bar chart with a reference line at -1 makes it easy to see which products are most price-sensitive.""", r"""ax.axvline(-1, color="grey", linestyle="--")"""),
            (r"""Write the causal caveat""", r"""The regression is observational. It describes association, not proof that changing price will cause exactly that quantity change.""", r"""results.append("This is an observational model, not a pricing experiment.")"""),
        ],
        "outputs": [
            (r'''`outputs/results.txt`''', r'''Regression coefficients, elasticity, p-values and interpretation.'''),
            (r'''`outputs/elasticity_by_product.csv`''', r'''Elasticity, p-value and R-squared for each product.'''),
            (r'''`outputs/coffee_price_simulation.csv`''', r'''Predicted quantity at 25 simulated coffee prices.'''),
            (r'''`outputs/demand_curve.png`''', r'''Observed coffee points plus the simulated demand curve.'''),
            (r'''`outputs/elasticity_by_product.png`''', r'''Elasticity comparison with the -1 reference line.'''),
        ],
        "try_it": [
            r'''Add `month` as a categorical control and see whether the elasticity changes.''',
            r'''Simulate a 10% price increase and calculate the predicted revenue change.''',
            r'''Run the model without `log_competitor_price` and explain why the price coefficient may shift.''',
        ],
        "note": r'''The cleanest way to learn the causal effect of price is a controlled experiment or a natural experiment, not a single observational regression.''',
    },
]


def build_readme(project: dict) -> str:
    """Create one Markdown README from a project dictionary."""
    lines = [
        f"# {project['number']}. {project['title']}",
        "",
        f"> {project['tagline']}",
        "",
        f"**Category:** {project['category']}  ",
        f"**Time:** {project['time']}  ",
        f"**Skills:** {project['skills']}",
        "",
        "## The goal",
        "",
        project["goal"],
        "",
        "## What you will learn",
        "",
    ]
    for step in project["steps"]:
        lines.append(f"- {step[0]}")
    lines += [
        "",
        "## Dataset at a glance",
        "",
        "| File | What it contains |",
        "| --- | --- |",
    ]
    for filename, description in project["dataset"]:
        lines.append(f"| {filename} | {description} |")
    lines += [
        "",
        project["columns"],
        "",
        "All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.",
        "",
        "## Step-by-step walkthrough",
        "",
        "The comments in `main.py` use the same step numbers. Follow the code and the explanation together.",
        "",
    ]
    for index, (heading, explanation, code) in enumerate(project["steps"], start=1):
        lines += [
            f"### Step {index} — {heading}",
            "",
            "```python",
            code,
            "```",
            "",
            explanation,
            "",
        ]
    lines += [
        "## Outputs to inspect",
        "",
        "| File | What it shows |",
        "| --- | --- |",
    ]
    for filename, description in project["outputs"]:
        lines.append(f"| {filename} | {description} |")
    lines += [
        "",
        "## Try it yourself",
        "",
    ]
    for item in project["try_it"]:
        lines.append(f"- {item}")
    lines += [
        "",
        "## Run it",
        "",
        "From the pack root:",
        "",
        "```bash",
        f"python3 projects/{project['folder']}/main.py",
        "```",
        "",
        "The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.",
        "",
        "## Note",
        "",
        project["note"],
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    for project in PROJECTS_DATA:
        folder = PROJECTS / project["folder"]
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / "README.md"
        path.write_text(build_readme(project), encoding="utf-8")
        print(f"wrote {path.relative_to(BASE)}")


if __name__ == "__main__":
    main()
