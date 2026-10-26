"""Generate the datasets for the 20 Data Science & Analytics projects.

Run from the pack root:

    python build_data.py

Projects 01-05 deliberately start with messy data so students can practise
cleaning.  Every other project starts with a clean, tidy dataset.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
PROJECTS = BASE / "projects"


def data_dir(project: str) -> Path:
    path = PROJECTS / project / "data"
    path.mkdir(parents=True, exist_ok=True)
    return path


# ---------------------------------------------------------------------------
# 01. Messy cafe orders
# ---------------------------------------------------------------------------
def build_cafe() -> None:
    rng = np.random.default_rng(101)
    prices = {"Latte": 4.50, "Cappuccino": 4.00, "Muffin": 3.00, "Sandwich": 6.50}
    categories = {"Latte": "Drink", "Cappuccino": "Drink", "Muffin": "Food", "Sandwich": "Food"}
    customer_types = ["student", "Student", "regular", "Regular", "tourist", "Tourist"]
    rows = []

    for order_id in range(1, 101):
        item = str(rng.choice(list(prices)))
        quantity = int(rng.integers(1, 4))
        unit_price = round(prices[item] + rng.normal(0, 0.20), 2)
        date = pd.Timestamp("2025-01-01") + pd.Timedelta(days=int(rng.integers(0, 60)))
        date_style = int(rng.integers(0, 3))
        if date_style == 0:
            date_text = date.strftime("%Y-%m-%d")
        elif date_style == 1:
            date_text = date.strftime("%b %d, %Y")
        else:
            date_text = date.strftime("%d-%b-%Y")

        item_text = str(rng.choice([item, item.lower(), item.upper(), f" {item} "]))
        category_text = str(rng.choice([categories[item], categories[item].lower(), ""]))
        rows.append(
            {
                "order_id": order_id,
                "date": date_text,
                "item": item_text,
                "category": category_text,
                "quantity": quantity,
                "unit_price": f"{unit_price:.2f}",
                "customer_type": str(rng.choice(customer_types)),
            }
        )

    df = pd.DataFrame(rows)
    # Add realistic mess: missing values, a negative quantity, currency strings.
    missing_qty = rng.choice(df.index, 10, replace=False)
    missing_price = rng.choice(df.index, 10, replace=False)
    df.loc[missing_qty, "quantity"] = np.nan
    df.loc[missing_price, "unit_price"] = np.nan
    df.loc[0, "quantity"] = -2
    df.loc[1, "unit_price"] = "$4.50"
    df.loc[2, "unit_price"] = " 5.25 "
    # Duplicate 18 rows exactly to create duplicate order IDs.
    df = pd.concat([df, df.sample(18, random_state=12)], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(data_dir("01_cafe_cleanup") / "cafe_orders_raw.csv", index=False)


# ---------------------------------------------------------------------------
# 02. Messy student records + scores
# ---------------------------------------------------------------------------
def build_students() -> None:
    rng = np.random.default_rng(102)
    names = [
        "Aarav", "Diya", "Kabir", "Meera", "Rohan", "Sara", "Vivaan", "Anaya",
        "Ishaan", "Nisha", "Arjun", "Tara", "Dev", "Priya", "Kiran", "Neha",
    ]
    programs = ["CSE", "ECE", "MECH", "CIVIL"]
    students = []
    for i in range(1, 81):
        raw_id = f"S{i:03d}"
        style = int(rng.integers(0, 4))
        if style == 0:
            student_id = raw_id
        elif style == 1:
            student_id = raw_id.lower()
        elif style == 2:
            student_id = f"S-{i:03d}"
        else:
            student_id = f" {raw_id} "
        students.append(
            {
                "student_id": student_id,
                "name": names[i % len(names)] + f" {i}",
                "program": str(rng.choice(programs + [p.lower() for p in programs])),
                "email": f"student{i}@college.edu",
            }
        )
    student_df = pd.DataFrame(students)
    student_df = pd.concat([student_df, student_df.sample(8, random_state=3)], ignore_index=True)

    subjects = ["Math", "Science", "English"]
    scores = []
    score_id = 1
    for i in range(1, 86):
        student_id = f"S{i:03d}" if i <= 80 else f"S{i:03d}"
        style = int(rng.integers(0, 4))
        if style == 0:
            sid = student_id
        elif style == 1:
            sid = student_id.lower()
        elif style == 2:
            sid = f"S-{i:03d}"
        else:
            sid = f" {student_id} "
        for subject in subjects:
            score = float(np.clip(rng.normal(70, 12), 0, 100))
            scores.append({"score_id": score_id, "student_id": sid, "subject": subject, "score": round(score, 1)})
            score_id += 1
    score_df = pd.DataFrame(scores)
    # Missing and impossible scores.
    score_df.loc[rng.choice(score_df.index, 18, replace=False), "score"] = np.nan
    score_df.loc[0, "score"] = 105
    score_df.loc[1, "score"] = -5
    score_df.loc[2, "score"] = "88"
    # Scores for students who are not in the student table.
    for i in range(81, 86):
        score_df = pd.concat(
            [
                score_df,
                pd.DataFrame(
                    [
                        {"score_id": score_id + j, "student_id": f"S{i:03d}", "subject": subject, "score": 75.0}
                        for j, subject in enumerate(subjects)
                    ]
                ),
            ],
            ignore_index=True,
        )
        score_id += 3

    student_df.to_csv(data_dir("02_student_records") / "students_raw.csv", index=False)
    score_df.to_csv(data_dir("02_student_records") / "scores_raw.csv", index=False)


# ---------------------------------------------------------------------------
# 03. Daily sales with outliers
# ---------------------------------------------------------------------------
def build_sales() -> None:
    rng = np.random.default_rng(103)
    rows = []
    for store, effect in (("A", 30), ("B", -20), ("C", 10)):
        for day in range(120):
            sales = 420 + 1.6 * day + 70 * np.sin(2 * np.pi * day / 7) + effect + rng.normal(0, 25)
            rows.append(
                {
                    "date": pd.Timestamp("2025-01-01") + pd.Timedelta(days=day),
                    "store": store,
                    "sales": round(float(max(sales, 0)), 2),
                }
            )
    df = pd.DataFrame(rows)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    # Inject bad values.
    df.loc[rng.choice(df.index, 5, replace=False), "sales"] = np.nan
    df.loc[rng.choice(df.index, 4, replace=False), "sales"] = [4800, 5200, 6100, 4300]
    df.loc[rng.choice(df.index, 4, replace=False), "sales"] = [-80, -45, -120, -60]
    df = df.sample(frac=1, random_state=7).reset_index(drop=True)
    df.to_csv(data_dir("03_sales_outliers") / "daily_sales_raw.csv", index=False)


# ---------------------------------------------------------------------------
# 04. Survey with inconsistent answers
# ---------------------------------------------------------------------------
def build_survey() -> None:
    rng = np.random.default_rng(104)
    gender_values = ["M", "F", "Male", "Female", "male", "female", "Other", ""]
    recommend_values = ["Yes", "yes", "YES", "Y", "y", "1", "No", "no", "N", "0", ""]
    satisfaction_values = ["1", "2", "3", "4", "5", "5 - Very satisfied", "4 - Satisfied", "3 - Neutral", ""]
    rows = []
    for respondent_id in range(1, 251):
        age = int(rng.integers(18, 61))
        if rng.random() < 0.04:
            age = 999
        elif rng.random() < 0.03:
            age = np.nan
        rows.append(
            {
                "respondent_id": respondent_id,
                "age": age,
                "gender": str(rng.choice(gender_values)),
                "satisfaction": str(rng.choice(satisfaction_values)),
                "would_recommend": str(rng.choice(recommend_values)),
                "comments": str(rng.choice(["", "Great service", "Could be better", "Loved it", "Not sure"])),
            }
        )
    df = pd.DataFrame(rows)
    df = pd.concat([df, df.sample(40, random_state=11)], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(data_dir("04_survey_cleanup") / "survey_raw.csv", index=False)


# ---------------------------------------------------------------------------
# 05. Mixed timestamp events
# ---------------------------------------------------------------------------
def build_events() -> None:
    rng = np.random.default_rng(105)
    event_types = ["view", "click", "purchase"]
    rows = []
    for event_id in range(1, 401):
        moment = pd.Timestamp("2025-03-01") + pd.Timedelta(
            days=int(rng.integers(0, 30)),
            hours=int(rng.integers(6, 23)),
            minutes=int(rng.integers(0, 60)),
        )
        style = int(rng.integers(0, 3))
        if style == 0:
            timestamp = moment.strftime("%Y-%m-%d %H:%M:%S")
        elif style == 1:
            timestamp = moment.strftime("%m/%d/%Y %I:%M %p")
        else:
            timestamp = moment.strftime("%Y-%m-%dT%H:%M:%S")
        rows.append(
            {
                "event_id": event_id,
                "user_id": int(rng.integers(1, 81)),
                "timestamp": timestamp,
                "event_type": str(rng.choice(event_types)),
                "duration_min": round(float(rng.uniform(0.5, 20)), 1),
            }
        )
    df = pd.DataFrame(rows)
    df.loc[rng.choice(df.index, 25, replace=False), "duration_min"] = np.nan
    df = pd.concat([df, df.sample(20, random_state=5)], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(data_dir("05_datetime_events") / "events_raw.csv", index=False)


# ---------------------------------------------------------------------------
# 06. Streaming viewing
# ---------------------------------------------------------------------------
def build_streaming() -> None:
    rng = np.random.default_rng(106)
    genres = ["Drama", "Comedy", "Documentary", "Sci-Fi", "Reality"]
    shows = {
        "Drama": ["The Long Road", "City Lights", "Second Chances"],
        "Comedy": ["Laugh Track", "Roommates", "The Office Party"],
        "Documentary": ["Ocean Deep", "Cities of Tomorrow", "Wild Routes"],
        "Sci-Fi": ["Orbit 9", "Signal Lost", "The Last Colony"],
        "Reality": ["Kitchen Clash", "Island House", "The Big Audition"],
    }
    rows = []
    for _ in range(700):
        genre = str(rng.choice(genres))
        show = str(rng.choice(shows[genre]))
        minutes = int(np.clip(rng.normal(70, 35), 5, 220))
        completed = int(rng.random() < (0.55 + 0.08 * (minutes > 90)))
        rows.append(
            {
                "user_id": int(rng.integers(1, 121)),
                "date": pd.Timestamp("2025-01-01") + pd.Timedelta(days=int(rng.integers(0, 30))),
                "show": show,
                "genre": genre,
                "minutes_watched": minutes,
                "completed": completed,
            }
        )
    df = pd.DataFrame(rows)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    df.to_csv(data_dir("06_streaming_analysis") / "streaming_viewing.csv", index=False)


# ---------------------------------------------------------------------------
# 07. Coffee shop orders
# ---------------------------------------------------------------------------
def build_coffee() -> None:
    rng = np.random.default_rng(107)
    items = {"Latte": 4.5, "Cappuccino": 4.0, "Cold Brew": 4.8, "Croissant": 3.2, "Bagel": 3.0}
    rows = []
    for order_id in range(1, 801):
        day = int(rng.integers(0, 14))
        hour = int(rng.choice(range(7, 19), p=np.array([4, 7, 10, 12, 10, 8, 9, 8, 7, 6, 4, 3]) / 88))
        item = str(rng.choice(list(items)))
        quantity = int(rng.integers(1, 4))
        rows.append(
            {
                "order_id": order_id,
                "timestamp": pd.Timestamp("2025-02-01") + pd.Timedelta(days=day, hours=hour, minutes=int(rng.integers(0, 60))),
                "item": item,
                "category": "Drink" if item in ("Latte", "Cappuccino", "Cold Brew") else "Food",
                "quantity": quantity,
                "unit_price": round(items[item] + rng.normal(0, 0.15), 2),
                "channel": str(rng.choice(["walk-in", "mobile"], p=[0.65, 0.35])),
            }
        )
    df = pd.DataFrame(rows)
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df.to_csv(data_dir("07_coffee_rush") / "coffee_orders.csv", index=False)


# ---------------------------------------------------------------------------
# 08. Study habits
# ---------------------------------------------------------------------------
def build_study_habits() -> None:
    rng = np.random.default_rng(108)
    rows = []
    for student_id in range(1, 221):
        study = round(float(rng.uniform(1, 10)), 1)
        sleep = round(float(np.clip(rng.normal(6.8, 1.1), 4, 9)), 1)
        attendance = round(float(np.clip(rng.normal(78, 12), 40, 100)), 0)
        screen = round(float(np.clip(rng.normal(4.5, 1.5), 1, 8)), 1)
        score = 25 + 4.5 * study + 0.35 * attendance + 1.5 * sleep - 1.2 * screen + rng.normal(0, 5)
        rows.append(
            {
                "student_id": student_id,
                "study_hours": study,
                "sleep_hours": sleep,
                "attendance_percent": attendance,
                "screen_time_hours": screen,
                "exam_score": round(float(np.clip(score, 0, 100)), 1),
                "study_method": str(rng.choice(["solo", "group", "online"], p=[0.45, 0.35, 0.20])),
                "year": int(rng.integers(1, 5)),
            }
        )
    pd.DataFrame(rows).to_csv(data_dir("08_study_habits") / "study_habits.csv", index=False)


# ---------------------------------------------------------------------------
# 09. Daily weather
# ---------------------------------------------------------------------------
def build_weather() -> None:
    rng = np.random.default_rng(109)
    rows = []
    for day in range(365):
        date = pd.Timestamp("2025-01-01") + pd.Timedelta(days=day)
        seasonal = 22 + 10 * np.sin(2 * np.pi * (day - 100) / 365)
        temp_max = seasonal + rng.normal(0, 2.2)
        temp_min = temp_max - rng.uniform(6, 10)
        rain_prob = 0.08 + 0.12 * max(0, np.sin(2 * np.pi * (day - 150) / 365))
        rainfall = float(rng.gamma(1.4, 4.0)) if rng.random() < rain_prob else 0.0
        rows.append(
            {
                "date": date.strftime("%Y-%m-%d"),
                "temp_max_c": round(float(temp_max), 1),
                "temp_min_c": round(float(temp_min), 1),
                "rainfall_mm": round(rainfall, 1),
                "humidity_percent": int(np.clip(rng.normal(62, 12), 25, 95)),
                "wind_kmh": round(float(np.clip(rng.normal(12, 5), 1, 35)), 1),
            }
        )
    pd.DataFrame(rows).to_csv(data_dir("09_weather_story") / "weather_daily.csv", index=False)


# ---------------------------------------------------------------------------
# 10. E-commerce funnel
# ---------------------------------------------------------------------------
def build_funnel() -> None:
    rng = np.random.default_rng(110)
    channel_specs = {
        "Organic": (900, 0.55, 0.28, 0.22),
        "Paid": (1200, 0.45, 0.22, 0.16),
        "Social": (700, 0.40, 0.18, 0.12),
        "Email": (350, 0.62, 0.35, 0.30),
    }
    rows = []
    for day in range(90):
        for channel, (base, view_rate, cart_rate, buy_rate) in channel_specs.items():
            visits = int(np.clip(rng.normal(base, base * 0.12), 50, None))
            views = int(visits * np.clip(rng.normal(view_rate, 0.04), 0.1, 0.95))
            carts = int(views * np.clip(rng.normal(cart_rate, 0.03), 0.05, 0.8))
            purchases = int(carts * np.clip(rng.normal(buy_rate, 0.03), 0.03, 0.7))
            rows.append(
                {
                    "date": (pd.Timestamp("2025-01-01") + pd.Timedelta(days=day)).strftime("%Y-%m-%d"),
                    "channel": channel,
                    "visits": visits,
                    "product_views": views,
                    "add_to_carts": carts,
                    "purchases": purchases,
                }
            )
    pd.DataFrame(rows).to_csv(data_dir("10_funnel_analysis") / "funnel_events.csv", index=False)


# ---------------------------------------------------------------------------
# 11. A/B test
# ---------------------------------------------------------------------------
def build_ab_test() -> None:
    rng = np.random.default_rng(111)
    rows = []
    for user_id in range(1, 3001):
        group = "A" if user_id <= 1500 else "B"
        probability = 0.10 if group == "A" else 0.13
        converted = int(rng.random() < probability)
        revenue = round(float(rng.uniform(20, 70)), 2) if converted else 0.0
        rows.append({"user_id": user_id, "group": group, "converted": converted, "revenue": revenue})
    pd.DataFrame(rows).to_csv(data_dir("11_ab_test") / "ab_test.csv", index=False)


# ---------------------------------------------------------------------------
# 12. Study break experiment
# ---------------------------------------------------------------------------
def build_study_break() -> None:
    rng = np.random.default_rng(112)
    rows = []
    for student_id in range(1, 81):
        group = "break" if student_id <= 40 else "no_break"
        score = 72 + (6 if group == "break" else 0) + rng.normal(0, 8)
        rows.append(
            {
                "student_id": student_id,
                "group": group,
                "score": round(float(np.clip(score, 0, 100)), 1),
                "study_minutes": int(np.clip(rng.normal(90, 15), 40, 140)),
            }
        )
    pd.DataFrame(rows).to_csv(data_dir("12_study_break") / "study_break.csv", index=False)


# ---------------------------------------------------------------------------
# 13. Satisfaction survey
# ---------------------------------------------------------------------------
def build_satisfaction() -> None:
    rng = np.random.default_rng(113)
    rows = []
    for respondent_id in range(1, 301):
        segment = str(rng.choice(["new", "returning", "vip"], p=[0.35, 0.45, 0.20]))
        mean = {"new": 3.4, "returning": 3.9, "vip": 4.4}[segment]
        satisfaction = int(np.clip(round(rng.normal(mean, 0.9)), 1, 5))
        recommend_prob = {"new": 0.45, "returning": 0.65, "vip": 0.82}[segment]
        rows.append(
            {
                "respondent_id": respondent_id,
                "segment": segment,
                "satisfaction": satisfaction,
                "would_recommend": int(rng.random() < recommend_prob),
                "age": int(np.clip(rng.normal(35, 10), 18, 70)),
            }
        )
    pd.DataFrame(rows).to_csv(data_dir("13_satisfaction_survey") / "satisfaction_survey.csv", index=False)


# ---------------------------------------------------------------------------
# 14. Sleep and focus
# ---------------------------------------------------------------------------
def build_sleep_focus() -> None:
    rng = np.random.default_rng(114)
    rows = []
    for student_id in range(1, 151):
        sleep = round(float(np.clip(rng.normal(6.8, 1.0), 4, 9)), 1)
        caffeine = int(np.clip(rng.normal(120, 70), 0, 400))
        screen = round(float(np.clip(rng.normal(4.0, 1.5), 1, 8)), 1)
        focus = 32 + 7.0 * sleep - 0.03 * caffeine - 2.0 * screen + rng.normal(0, 6)
        rows.append(
            {
                "student_id": student_id,
                "sleep_hours": sleep,
                "focus_score": round(float(np.clip(focus, 0, 100)), 1),
                "caffeine_mg": caffeine,
                "screen_time_hours": screen,
            }
        )
    pd.DataFrame(rows).to_csv(data_dir("14_sleep_focus") / "sleep_focus.csv", index=False)


# ---------------------------------------------------------------------------
# 15. Delivery times across warehouses
# ---------------------------------------------------------------------------
def build_delivery() -> None:
    rng = np.random.default_rng(115)
    rows = []
    for order_id in range(1, 181):
        warehouse = str(rng.choice(["A", "B", "C"], p=[0.34, 0.33, 0.33]))
        distance = round(float(np.clip(rng.normal(12, 5), 2, 30)), 1)
        base = {"A": 2.4, "B": 3.4, "C": 2.9}[warehouse]
        delivery_days = base + 0.06 * distance + rng.normal(0, 0.6)
        rows.append(
            {
                "order_id": order_id,
                "warehouse": warehouse,
                "delivery_days": round(float(np.clip(delivery_days, 0.5, 12)), 1),
                "distance_km": distance,
                "order_value": round(float(rng.uniform(15, 250)), 2),
            }
        )
    pd.DataFrame(rows).to_csv(data_dir("15_delivery_anova") / "delivery_times.csv", index=False)


# ---------------------------------------------------------------------------
# 16. Customer RFM data
# ---------------------------------------------------------------------------
def build_customers() -> None:
    rng = np.random.default_rng(116)
    segments = ["loyal", "new", "at_risk", "occasional"]
    rows = []
    for customer_id in range(1, 401):
        segment = str(rng.choice(segments, p=[0.22, 0.30, 0.20, 0.28]))
        if segment == "loyal":
            recency = rng.integers(1, 61)
            frequency = rng.integers(10, 31)
            monetary = rng.normal(1300, 300)
        elif segment == "new":
            recency = rng.integers(1, 31)
            frequency = rng.integers(1, 6)
            monetary = rng.normal(120, 50)
        elif segment == "at_risk":
            recency = rng.integers(120, 366)
            frequency = rng.integers(5, 16)
            monetary = rng.normal(900, 250)
        else:
            recency = rng.integers(30, 181)
            frequency = rng.integers(2, 9)
            monetary = rng.normal(320, 120)
        rows.append(
            {
                "customer_id": customer_id,
                "recency_days": int(recency),
                "frequency": int(frequency),
                "monetary": round(float(max(monetary, 20)), 2),
                "signup_days_ago": int(rng.integers(30, 900)),
                "channel": str(rng.choice(["organic", "paid", "referral"], p=[0.4, 0.35, 0.25])),
            }
        )
    pd.DataFrame(rows).to_csv(data_dir("16_customer_segments") / "customers.csv", index=False)


# ---------------------------------------------------------------------------
# 17. Churn data
# ---------------------------------------------------------------------------
def build_churn() -> None:
    rng = np.random.default_rng(117)
    rows = []
    for customer_id in range(1, 801):
        tenure = int(rng.integers(1, 61))
        monthly = round(float(rng.uniform(20, 100)), 2)
        support = int(rng.poisson(2.2))
        late = int(rng.poisson(1.4))
        usage = round(float(np.clip(rng.normal(45, 20), 1, 100)), 1)
        logit = -1.4 - 0.045 * tenure - 0.025 * usage + 0.35 * support + 0.45 * late + 0.004 * monthly
        churned = int(rng.random() < 1 / (1 + np.exp(-logit)))
        rows.append(
            {
                "customer_id": customer_id,
                "tenure_months": tenure,
                "monthly_charges": monthly,
                "support_calls": support,
                "late_payments": late,
                "usage_hours": usage,
                "churned": churned,
            }
        )
    pd.DataFrame(rows).to_csv(data_dir("17_churn_model") / "churn.csv", index=False)


# ---------------------------------------------------------------------------
# 18. Monthly sales forecast
# ---------------------------------------------------------------------------
def build_forecast() -> None:
    rng = np.random.default_rng(118)
    rows = []
    for month_index in range(36):
        month = pd.Timestamp("2023-01-01") + pd.DateOffset(months=month_index)
        sales = 1000 + 40 * month_index + 70 * np.sin(2 * np.pi * (month_index % 12) / 12) + rng.normal(0, 30)
        rows.append({"month": month.strftime("%Y-%m"), "sales": round(float(max(sales, 0)), 2)})
    pd.DataFrame(rows).to_csv(data_dir("18_sales_forecast") / "monthly_sales.csv", index=False)


# ---------------------------------------------------------------------------
# 19. Product transactions
# ---------------------------------------------------------------------------
def build_transactions() -> None:
    rng = np.random.default_rng(119)
    products = [
        "Laptop", "Mouse", "Keyboard", "Monitor", "Headphones", "Webcam", "USB Hub", "Notebook",
        "Pen Set", "Backpack", "Water Bottle", "Desk Lamp", "Phone Stand", "Charger", "Cable",
        "Speaker", "Microphone", "Tablet", "Smartwatch", "Docking Station",
    ]
    clusters = [
        ["Laptop", "Mouse", "Keyboard", "Monitor", "Docking Station", "USB Hub"],
        ["Notebook", "Pen Set", "Backpack", "Water Bottle", "Desk Lamp"],
        ["Headphones", "Speaker", "Microphone", "Phone Stand", "Charger", "Cable"],
        ["Tablet", "Smartwatch", "Webcam", "Phone Stand", "USB Hub"],
    ]
    rows = []
    transaction_id = 1
    for customer_id in range(1, 121):
        cluster = clusters[customer_id % len(clusters)]
        for _ in range(int(rng.integers(4, 10))):
            n_items = int(rng.integers(1, 4))
            chosen = rng.choice(cluster, size=n_items, replace=False)
            for product in chosen:
                rows.append(
                    {
                        "transaction_id": transaction_id,
                        "customer_id": customer_id,
                        "product": str(product),
                    }
                )
            transaction_id += 1
    pd.DataFrame(rows).to_csv(data_dir("19_recommendation") / "transactions.csv", index=False)


# ---------------------------------------------------------------------------
# 20. Pricing and demand
# ---------------------------------------------------------------------------
def build_pricing() -> None:
    rng = np.random.default_rng(120)
    products = {
        "Coffee": 5.0,
        "Sandwich": 8.0,
        "Salad": 7.0,
        "Juice": 4.0,
        "Cookie": 2.5,
    }
    rows = []
    for product, base_price in products.items():
        for month_index in range(24):
            month = pd.Timestamp("2024-01-01") + pd.DateOffset(months=month_index)
            price = base_price * (1 + rng.normal(0, 0.08))
            competitor_price = base_price * (1 + rng.normal(0, 0.10))
            promotion = int(rng.random() < 0.20)
            elasticity = -1.8 + rng.normal(0, 0.10)
            quantity = 500 * (price / base_price) ** elasticity
            quantity *= 1 + 0.22 * promotion
            quantity *= (competitor_price / base_price) ** 0.5
            quantity += rng.normal(0, 20)
            rows.append(
                {
                    "product": product,
                    "month": month.strftime("%Y-%m"),
                    "price": round(float(max(price, 0.5)), 2),
                    "quantity": int(max(10, round(quantity))),
                    "promotion": promotion,
                    "competitor_price": round(float(max(competitor_price, 0.5)), 2),
                }
            )
    pd.DataFrame(rows).to_csv(data_dir("20_pricing_elasticity") / "pricing_data.csv", index=False)


def main() -> None:
    builders = [
        build_cafe,
        build_students,
        build_sales,
        build_survey,
        build_events,
        build_streaming,
        build_coffee,
        build_study_habits,
        build_weather,
        build_funnel,
        build_ab_test,
        build_study_break,
        build_satisfaction,
        build_sleep_focus,
        build_delivery,
        build_customers,
        build_churn,
        build_forecast,
        build_transactions,
        build_pricing,
    ]
    for builder in builders:
        builder()
        print(f"built: {builder.__name__}")
    print(f"\nAll datasets written under {PROJECTS}")


if __name__ == "__main__":
    main()
