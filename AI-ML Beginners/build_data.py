"""Generate the small, self-contained datasets used by all 20 projects.

Run from the project pack root:

    python build_data.py

Most datasets are intentionally small, synthetic, and easy to inspect.  The
projects are real machine-learning programs; synthetic data keeps them fast,
private, and runnable on any laptop without downloads.  The Iris dataset is
the real classic dataset, loaded from scikit-learn.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw

BASE = Path(__file__).resolve().parent
PROJECTS = BASE / "projects"


def _data_dir(project: str) -> Path:
    path = PROJECTS / project / "data"
    path.mkdir(parents=True, exist_ok=True)
    return path


# ---------------------------------------------------------------------------
# 01. Snack Sorter: synthetic snack photos + image features
# ---------------------------------------------------------------------------
def build_snacks() -> None:
    data = _data_dir("01_snack_sorter")
    images = data / "images"
    images.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(7)
    rows = []

    def make_image(kind: str, index: int) -> Image.Image:
        background = (
            int(rng.integers(238, 250)),
            int(rng.integers(232, 246)),
            int(rng.integers(215, 232)),
        )
        img = Image.new("RGB", (32, 32), background)
        draw = ImageDraw.Draw(img)
        cx = int(rng.integers(14, 19))
        cy = int(rng.integers(14, 19))

        if kind == "apple":
            r = int(rng.integers(8, 11))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 35, 45))
            draw.line([cx, cy - r, cx, cy - r - 4], fill=(65, 115, 40), width=2)
            draw.ellipse([cx + 2, cy - r - 4, cx + 7, cy - r + 1], fill=(55, 135, 45))
        elif kind == "banana":
            x0 = int(rng.integers(2, 6))
            y0 = int(rng.integers(1, 5))
            x1 = int(rng.integers(26, 30))
            y1 = int(rng.integers(27, 31))
            draw.arc([x0, y0, x1, y1], start=200, end=340, fill=(235, 200, 45), width=8)
            draw.ellipse([x0, y1 - 6, x0 + 5, y1 - 1], fill=(175, 135, 25))
            draw.ellipse([x1 - 5, y1 - 6, x1, y1 - 1], fill=(175, 135, 25))
        else:  # orange
            r = int(rng.integers(9, 12))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(238, 125, 28))
            for _ in range(18):
                x = int(rng.integers(cx - r + 2, cx + r - 2))
                y = int(rng.integers(cy - r + 2, cy + r - 2))
                if (x - cx) ** 2 + (y - cy) ** 2 < (r - 2) ** 2:
                    draw.point((x, y), fill=(195, 90, 18))

        arr = np.asarray(img).astype(np.int16)
        arr += rng.integers(-10, 11, arr.shape)
        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

    for kind in ("apple", "banana", "orange"):
        for i in range(30):
            img = make_image(kind, i)
            filename = f"{kind}_{i:02d}.png"
            img.save(images / filename)

            arr = np.asarray(img).astype(float)
            bg = np.array([245.0, 239.0, 224.0])
            mask = np.linalg.norm(arr - bg, axis=2) > 45
            pixels = arr[mask]
            if len(pixels) == 0:
                pixels = arr.reshape(-1, 3)
                mask = np.ones(arr.shape[:2], dtype=bool)
            ys, xs = np.where(mask)
            width = float(xs.max() - xs.min() + 1)
            height = float(ys.max() - ys.min() + 1)
            rows.append(
                {
                    "image_path": f"images/{filename}",
                    "label": kind,
                    "mean_r": round(float(pixels[:, 0].mean()), 2),
                    "mean_g": round(float(pixels[:, 1].mean()), 2),
                    "mean_b": round(float(pixels[:, 2].mean()), 2),
                    "color_fraction": round(float(mask.mean()), 4),
                    "aspect_ratio": round(width / height, 3),
                }
            )

    pd.DataFrame(rows).to_csv(data / "snacks.csv", index=False)


# ---------------------------------------------------------------------------
# 02. Lemonade stand
# ---------------------------------------------------------------------------
def build_lemonade() -> None:
    rng = np.random.default_rng(11)
    temp = np.round(rng.uniform(21, 39, 16), 1)
    cups = np.clip(1.9 * temp - 18 + rng.normal(0, 3.5, len(temp)), 0, None)
    df = pd.DataFrame(
        {
            "day": np.arange(1, len(temp) + 1),
            "temperature_c": temp,
            "cups_sold": np.round(cups).astype(int),
        }
    )
    df.to_csv(_data_dir("02_lemonade_stand") / "lemonade_days.csv", index=False)


# ---------------------------------------------------------------------------
# 03. Titanic-style survival data
# ---------------------------------------------------------------------------
def build_titanic() -> None:
    rng = np.random.default_rng(23)
    n = 90
    pclass = rng.choice([1, 2, 3], size=n, p=[0.24, 0.24, 0.52])
    sex = rng.choice(["male", "female"], size=n, p=[0.62, 0.38])
    age = np.clip(rng.normal(30, 15, n), 1, 80).round(0)
    fare = np.where(
        pclass == 1,
        rng.normal(85, 30, n),
        np.where(pclass == 2, rng.normal(30, 10, n), rng.normal(12, 5, n)),
    ).clip(5, 220).round(1)

    logit = (
        -1.25
        + 1.55 * (sex == "female")
        + 0.65 * (pclass == 1)
        - 0.45 * (pclass == 3)
        + 0.9 * (age < 12)
        - 0.012 * age
    )
    prob = 1 / (1 + np.exp(-logit))
    survived = rng.binomial(1, prob)

    df = pd.DataFrame(
        {
            "passenger_id": np.arange(1, n + 1),
            "pclass": pclass,
            "sex": sex,
            "age": age.astype(int),
            "fare": fare,
            "survived": survived,
        }
    )
    df.to_csv(_data_dir("03_titanic_survival") / "titanic_practice.csv", index=False)


# ---------------------------------------------------------------------------
# 04. Spam detective
# ---------------------------------------------------------------------------
def build_spam() -> None:
    rng = np.random.default_rng(31)
    spam_templates = [
        "Congratulations! You have won a free {prize}. Click {link} now to claim your cash reward.",
        "URGENT: Your account is at risk. Verify your password immediately at {link}.",
        "Buy cheap {product} today! Best price, limited offer, order now.",
        "Winner! Claim your free gift card worth ${amount}. Act fast!",
        "Lowest price guaranteed! Get {product} at 50% off. Buy now.",
        "Final notice: unpaid bill. Send payment today to avoid suspension.",
        "Exclusive deal just for you! Free trial, no risk, cancel anytime.",
        "Make money fast from home. Earn ${amount} per week. Sign up now.",
        "You are selected for a special reward. Reply YES to receive your prize.",
        "Flash sale! Free shipping on every {product}. Order in the next hour.",
    ]
    ham_templates = [
        "Hi {name}, are we still meeting for lunch at {time} tomorrow?",
        "Reminder: the team meeting is moved to {time} in room {room}.",
        "Thanks for your help with the {task}. I really appreciate it.",
        "Please find the {document} attached. Let me know if you have questions.",
        "Are you free to review the {project} draft this week?",
        "Happy birthday, {name}! Hope you have a wonderful day.",
        "Can you send me the notes from today's class?",
        "The library book is due on Friday. Please return it.",
        "See you at the {event} on Saturday. Bring your camera!",
        "I'll be a few minutes late to the {meeting}. Start without me.",
    ]
    prizes = ["smartphone", "laptop", "vacation", "gift card", "TV"]
    products = ["watches", "shoes", "vitamins", "software", "headphones"]
    links = ["www.free-prize.example", "www.secure-verify.example", "www.best-deal.example"]
    names = ["Maya", "Arjun", "Sara", "Leo", "Nina", "Omar"]
    times = ["9:30", "11:00", "2:15", "4:00", "6:30"]
    rooms = ["B12", "204", "the lab", "the library"]
    tasks = ["poster", "slides", "report", "dataset"]
    documents = ["notes", "schedule", "draft", "budget"]
    projects = ["robotics", "website", "survey", "presentation"]
    events = ["club fair", "hackathon", "football match", "science expo"]
    meetings = ["stand-up", "study group", "project review", "lab session"]

    rows = []
    for _ in range(40):
        text = rng.choice(spam_templates).format(
            prize=rng.choice(prizes),
            product=rng.choice(products),
            link=rng.choice(links),
            amount=rng.choice([100, 250, 500, 1000, 5000]),
        )
        rows.append({"text": text, "label": "spam"})
    for _ in range(40):
        text = rng.choice(ham_templates).format(
            name=rng.choice(names),
            time=rng.choice(times),
            room=rng.choice(rooms),
            task=rng.choice(tasks),
            document=rng.choice(documents),
            project=rng.choice(projects),
            event=rng.choice(events),
            meeting=rng.choice(meetings),
        )
        rows.append({"text": text, "label": "ham"})

    df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(_data_dir("04_spam_detective") / "messages.csv", index=False)


# ---------------------------------------------------------------------------
# 05. Fruit basket sorter
# ---------------------------------------------------------------------------
def build_fruit() -> None:
    rng = np.random.default_rng(41)
    specs = {
        "apple": dict(sweet=(7.0, 0.5), weight=(160, 18), size=(8.0, 0.6), color=(8.0, 0.5)),
        "banana": dict(sweet=(8.1, 0.5), weight=(125, 12), size=(17.0, 1.4), color=(7.0, 0.5)),
        "orange": dict(sweet=(5.2, 0.5), weight=(200, 18), size=(9.0, 0.6), color=(6.0, 0.5)),
    }
    rows = []
    for fruit, spec in specs.items():
        for _ in range(20):
            rows.append(
                {
                    "fruit": fruit,
                    "sweetness": round(float(rng.normal(*spec["sweet"])), 1),
                    "weight_g": int(round(rng.normal(*spec["weight"]))),
                    "size_cm": round(float(rng.normal(*spec["size"])), 1),
                    "color_score": round(float(rng.normal(*spec["color"])), 1),
                }
            )
    df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(_data_dir("05_fruit_sorter") / "fruits.csv", index=False)


# ---------------------------------------------------------------------------
# 06. Exam score
# ---------------------------------------------------------------------------
def build_exam_score() -> None:
    rng = np.random.default_rng(51)
    hours = np.round(rng.uniform(1, 10, 28), 1)
    score = np.clip(34 + 5.7 * hours + rng.normal(0, 5.5, len(hours)), 0, 100)
    df = pd.DataFrame({"hours_studied": hours, "exam_score": np.round(score, 1)})
    df.to_csv(_data_dir("06_exam_score") / "exam_scores.csv", index=False)


# ---------------------------------------------------------------------------
# 07. Used car price
# ---------------------------------------------------------------------------
def build_cars() -> None:
    rng = np.random.default_rng(61)
    n = 45
    age = rng.integers(0, 13, n)
    km = np.round(rng.uniform(5_000, 150_000, n), -2).astype(int)
    price = 26_000 - 1_250 * age - 0.085 * km + rng.normal(0, 1_800, n)
    price = np.clip(price, 1_500, None)
    df = pd.DataFrame(
        {
            "age_years": age,
            "kilometers": km,
            "price_usd": np.round(price, 0).astype(int),
        }
    )
    df.to_csv(_data_dir("07_car_price") / "used_cars.csv", index=False)


# ---------------------------------------------------------------------------
# 08. Pizza price
# ---------------------------------------------------------------------------
def build_pizza() -> None:
    rng = np.random.default_rng(71)
    n = 45
    diameter = np.round(rng.uniform(8, 18, n), 1)
    toppings = rng.integers(0, 6, n)
    price = 4.5 + 0.95 * diameter + 1.7 * toppings + rng.normal(0, 0.8, n)
    df = pd.DataFrame(
        {
            "diameter_inches": diameter,
            "toppings": toppings,
            "price_usd": np.round(np.clip(price, 5, None), 2),
        }
    )
    df.to_csv(_data_dir("08_pizza_price") / "pizza_menu.csv", index=False)


# ---------------------------------------------------------------------------
# 09. Height predictor
# ---------------------------------------------------------------------------
def build_heights() -> None:
    rng = np.random.default_rng(81)
    n = 60
    mother = np.round(rng.normal(162, 6, n), 1)
    father = np.round(rng.normal(176, 7, n), 1)
    midparent = (mother + father) / 2
    child = 0.72 * midparent + 49 + rng.normal(0, 3.5, n)
    df = pd.DataFrame(
        {
            "mother_cm": mother,
            "father_cm": father,
            "child_cm": np.round(np.clip(child, 145, 205), 1),
        }
    )
    df.to_csv(_data_dir("09_height_predictor") / "heights.csv", index=False)


# ---------------------------------------------------------------------------
# 10. Sleep vs screen time
# ---------------------------------------------------------------------------
def build_sleep() -> None:
    rng = np.random.default_rng(91)
    screen = np.round(rng.uniform(0.5, 5.5, 35), 1)
    sleep = 9.3 - 0.62 * screen + rng.normal(0, 0.45, len(screen))
    df = pd.DataFrame(
        {
            "screen_time_hours": screen,
            "sleep_hours": np.round(np.clip(sleep, 4, 10), 1),
        }
    )
    df.to_csv(_data_dir("10_sleep_screen_time") / "sleep_screen.csv", index=False)


# ---------------------------------------------------------------------------
# 11. Pass/fail predictor
# ---------------------------------------------------------------------------
def build_pass_fail() -> None:
    rng = np.random.default_rng(101)
    n = 120
    hours = np.round(rng.uniform(1, 10, n), 1)
    attendance = np.round(rng.uniform(40, 100, n), 0)
    logit = -8.0 + 0.95 * hours + 0.07 * attendance
    prob = 1 / (1 + np.exp(-logit))
    passed = rng.binomial(1, prob)
    df = pd.DataFrame(
        {
            "hours_studied": hours,
            "attendance_percent": attendance,
            "passed": passed,
        }
    )
    df.to_csv(_data_dir("11_exam_pass_predictor") / "student_results.csv", index=False)


# ---------------------------------------------------------------------------
# 12. Fake review spotter
# ---------------------------------------------------------------------------
def build_reviews() -> None:
    rng = np.random.default_rng(111)
    fake_templates = [
        "AMAZING product!!! Best purchase ever. Buy now, you will not regret it!!!",
        "Totally changed my life. Five stars. Highly recommend to everyone!",
        "This is the best thing I have ever bought. Absolutely perfect in every way.",
        "Do not think twice! Incredible quality, super fast shipping, buy it today!",
        "WOW WOW WOW. I love it so much. Best seller ever. 10/10.",
        "Perfect! Exactly as described. Amazing value. Order yours now!",
        "Absolutely flawless. I cannot believe how good this is. Must buy!",
        "Five stars! Best product on the market. You need this right now.",
        "Unbelievable deal! This is a game changer. Best money I ever spent!",
        "I am obsessed! Perfect quality, perfect price, perfect everything!",
    ]
    real_templates = [
        "The product arrived on time and works as described. The battery lasts about a day.",
        "I liked the design, but the instructions were confusing. Customer support helped.",
        "Good value for the price. It is not perfect, but it does the job.",
        "The size runs a little small, so order one size up. Otherwise comfortable.",
        "Works well for light use. The material feels durable, though the color is different.",
        "Shipping was slow, but the item was well packaged and in good condition.",
        "It does what it promises. I would have liked a longer cable, but overall fine.",
        "Decent quality. One of the buttons is stiff, but it is usable.",
        "The first unit had a scratch, and the replacement was fine. Mixed experience.",
        "Comfortable for short walks. Not sure I would use it for a long hike.",
    ]
    rows = [{"review": rng.choice(fake_templates), "label": "fake"} for _ in range(40)]
    rows += [{"review": rng.choice(real_templates), "label": "real"} for _ in range(40)]
    df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(_data_dir("12_fake_review_spotter") / "reviews.csv", index=False)


# ---------------------------------------------------------------------------
# 13. Penguin detective
# ---------------------------------------------------------------------------
def build_penguins() -> None:
    rng = np.random.default_rng(121)
    specs = {
        "Adelie": dict(bill_len=(38.8, 2.2), bill_dep=(18.3, 1.0), flipper=(190, 6), mass=(3700, 350)),
        "Gentoo": dict(bill_len=(47.5, 2.5), bill_dep=(15.0, 0.9), flipper=(217, 6), mass=(5076, 450)),
        "Chinstrap": dict(bill_len=(48.8, 3.0), bill_dep=(18.4, 1.1), flipper=(196, 6), mass=(3733, 380)),
    }
    rows = []
    for species, s in specs.items():
        for _ in range(50):
            rows.append(
                {
                    "species": species,
                    "bill_length_mm": round(float(rng.normal(*s["bill_len"])), 1),
                    "bill_depth_mm": round(float(rng.normal(*s["bill_dep"])), 1),
                    "flipper_length_mm": int(round(rng.normal(*s["flipper"]))),
                    "body_mass_g": int(round(rng.normal(*s["mass"]))),
                }
            )
    df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(_data_dir("13_penguin_detective") / "penguins.csv", index=False)


# ---------------------------------------------------------------------------
# 14. Iris (classic built-in dataset, saved as CSV for inspection)
# ---------------------------------------------------------------------------
def build_iris() -> None:
    from sklearn.datasets import load_iris

    iris = load_iris(as_frame=True)
    df = iris.frame.copy()
    df.columns = [c.replace(" (cm)", "").replace(" ", "_") for c in df.columns]
    df["species"] = df["target"].map(dict(enumerate(iris.target_names)))
    df = df.drop(columns=["target"])
    df.to_csv(_data_dir("14_iris_identifier") / "iris.csv", index=False)


# ---------------------------------------------------------------------------
# 15. Pumpkin seed sorter
# ---------------------------------------------------------------------------
def build_pumpkin() -> None:
    rng = np.random.default_rng(131)
    specs = {
        "Urgup_Sivrisi": dict(area=(1150, 70), perimeter=(54, 3), major=(12.0, 0.6), minor=(5.6, 0.3), ecc=(0.86, 0.02)),
        "Cercevelik": dict(area=(1500, 100), perimeter=(63, 3), major=(14.0, 0.7), minor=(6.5, 0.3), ecc=(0.90, 0.02)),
        "Karacabey": dict(area=(950, 70), perimeter=(50, 3), major=(11.0, 0.6), minor=(5.4, 0.3), ecc=(0.80, 0.03)),
    }
    rows = []
    for variety, s in specs.items():
        for _ in range(60):
            rows.append(
                {
                    "variety": variety,
                    "area": int(round(rng.normal(*s["area"]))),
                    "perimeter": round(float(rng.normal(*s["perimeter"])), 2),
                    "major_axis": round(float(rng.normal(*s["major"])), 2),
                    "minor_axis": round(float(rng.normal(*s["minor"])), 2),
                    "eccentricity": round(float(rng.normal(*s["ecc"])), 3),
                }
            )
    df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(_data_dir("15_pumpkin_seed_sorter") / "pumpkin_seeds.csv", index=False)


# ---------------------------------------------------------------------------
# 16. Movie review mood ring
# ---------------------------------------------------------------------------
def build_mood_reviews() -> None:
    rng = np.random.default_rng(141)
    positive = [
        "I loved this movie. The acting was wonderful and the story kept me smiling.",
        "A delightful film with charming characters and a warm, funny script.",
        "The visuals were beautiful and the ending made me cheer.",
        "Great performances, a clever plot, and a soundtrack I want to replay.",
        "I had a fantastic time watching this. It was funny, moving, and fun.",
        "The director did a wonderful job. I would happily watch it again.",
        "A feel-good movie with sharp dialogue and a big heart.",
        "The cast had great chemistry, and the jokes landed every time.",
        "Surprisingly moving and beautifully shot. I recommend it.",
        "A joyful surprise. The story was simple but told with real warmth.",
    ]
    negative = [
        "I hated this movie. The plot was boring and the acting felt wooden.",
        "A dull, confusing film that wasted a talented cast.",
        "The story dragged and the ending made no sense.",
        "I kept checking the time. The jokes were flat and the pacing was awful.",
        "Poor writing, weak characters, and a soundtrack that never fit the scene.",
        "One of the most disappointing films I have seen this year.",
        "The visuals were ugly and the dialogue was painful to listen to.",
        "A messy movie with no clear point and far too many cliches.",
        "I wanted to like it, but the story lost me after twenty minutes.",
        "Boring, predictable, and far too long. I would not recommend it.",
    ]
    mixed = [
        "The visuals were stunning, but the story dragged. I liked the ending, though.",
        "Great acting and a beautiful score, but the plot had several holes.",
        "It started strong and then lost its way. Still, the final scene was lovely.",
        "The comedy worked, but the emotional moments felt forced.",
        "I enjoyed the characters, yet the pacing made it hard to stay engaged.",
        "A stylish film with a weak script. Worth watching for the cinematography.",
        "Some scenes were brilliant and others were painfully slow.",
        "The first half was fun, but the second half felt rushed and messy.",
        "Good performances cannot fully save a predictable story.",
        "I am glad I watched it, but I would not rush to see it again.",
    ]
    rows = []
    for label, texts in (("positive", positive), ("negative", negative), ("mixed", mixed)):
        for _ in range(30):
            rows.append({"review": rng.choice(texts), "mood": label})
    df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(_data_dir("16_movie_mood_ring") / "movie_reviews.csv", index=False)


# ---------------------------------------------------------------------------
# 17. Subject chatbot
# ---------------------------------------------------------------------------
def build_subject_chatbot() -> None:
    rng = np.random.default_rng(151)
    rows = []
    for _ in range(90):
        a = rng.integers(0, 2)
        b = rng.integers(0, 2)
        c = rng.integers(0, 2)
        d = rng.integers(0, 2)
        e = rng.integers(0, 2)
        f = rng.integers(0, 2)

        math_score = 2.2 * a + 1.8 * f + 1.2 * d + rng.normal(0, 0.7)
        bio_score = 2.1 * b + 1.6 * d + 1.0 * (1 - e) + rng.normal(0, 0.7)
        lit_score = 2.2 * c + 1.8 * e + 1.0 * (1 - f) + rng.normal(0, 0.7)
        scores = {"Math": math_score, "Biology": bio_score, "Literature": lit_score}
        label = max(scores, key=scores.get)
        rows.append(
            {
                "likes_numbers": int(a),
                "likes_living_things": int(b),
                "likes_stories": int(c),
                "enjoys_experiments": int(d),
                "enjoys_debate": int(e),
                "likes_programming": int(f),
                "subject": label,
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(_data_dir("17_subject_chatbot") / "subject_answers.csv", index=False)


# ---------------------------------------------------------------------------
# 18. Recipe recommender
# ---------------------------------------------------------------------------
def build_recipes() -> None:
    recipes = [
        ("Margherita Pizza", "Italian", 2, 2, 5, 3, 2),
        ("Spicy Ramen", "Japanese", 5, 1, 5, 2, 2),
        ("Chicken Tikka Masala", "Indian", 4, 2, 5, 2, 2),
        ("Pad Thai", "Thai", 3, 3, 4, 4, 2),
        ("Sushi", "Japanese", 1, 1, 4, 3, 1),
        ("Taco", "Mexican", 4, 1, 4, 3, 2),
        ("Greek Salad", "Greek", 1, 1, 3, 4, 3),
        ("Pancakes", "American", 1, 5, 2, 1, 1),
        ("Chocolate Cake", "Dessert", 1, 5, 2, 1, 1),
        ("Tom Yum Soup", "Thai", 5, 1, 4, 5, 2),
        ("Lasagna", "Italian", 2, 2, 5, 2, 2),
        ("Falafel Wrap", "Middle Eastern", 2, 1, 4, 3, 3),
        ("Bibimbap", "Korean", 3, 2, 4, 2, 3),
        ("Butter Chicken", "Indian", 3, 3, 5, 1, 1),
        ("Fish and Chips", "British", 1, 1, 4, 3, 1),
        ("Paella", "Spanish", 2, 1, 5, 2, 2),
        ("Miso Soup", "Japanese", 1, 1, 3, 3, 1),
        ("Burrito Bowl", "Mexican", 3, 1, 4, 3, 3),
        ("Caprese Salad", "Italian", 1, 2, 3, 4, 3),
        ("Thai Green Curry", "Thai", 4, 3, 4, 2, 2),
        ("Blueberry Muffin", "American", 1, 4, 2, 2, 1),
        ("Lemon Tart", "French", 1, 4, 2, 5, 1),
        ("Mushroom Risotto", "Italian", 1, 1, 5, 2, 2),
        ("Kimchi Fried Rice", "Korean", 4, 1, 4, 3, 2),
    ]
    df = pd.DataFrame(
        recipes,
        columns=["name", "cuisine", "spice", "sweet", "savory", "sour", "veggie"],
    )
    df.to_csv(_data_dir("18_recipe_recommender") / "recipes.csv", index=False)


# ---------------------------------------------------------------------------
# 19. News topic sorter
# ---------------------------------------------------------------------------
def build_news() -> None:
    rng = np.random.default_rng(191)
    sports = [
        "Local team wins the championship in a thrilling final",
        "Star player scores twice in comeback victory",
        "Coach announces new lineup for the season opener",
        "Marathon runner breaks the national record",
        "Injury update: captain expected to return next week",
        "Fans celebrate as underdogs reach the playoffs",
        "Tennis champion advances to the semifinals",
        "New stadium opens with a sold-out match",
        "Olympic hopefuls train for the qualifying event",
        "Cricket league announces its summer schedule",
    ]
    tech = [
        "New smartphone promises a week-long battery life",
        "Researchers unveil a faster way to train small AI models",
        "Open-source project reaches one million downloads",
        "Startup launches a robot that sorts recycling",
        "Cybersecurity experts warn about a new phishing scam",
        "Laptop maker announces a repairable budget model",
        "Developers release a free tool for learning Python",
        "Satellite internet service expands to rural schools",
        "Tech conference highlights affordable health gadgets",
        "New browser update blocks trackers by default",
    ]
    food = [
        "Street food festival returns with fifty local vendors",
        "Simple one-pot pasta recipe wins over busy students",
        "New bakery opens with a focus on sourdough",
        "Study finds students eat more vegetables when meals are colorful",
        "Campus cafe adds affordable breakfast options",
        "Chef shares a five-minute recipe for spicy noodles",
        "Farmers market expands its weekend hours",
        "Food waste project turns leftovers into free lunches",
        "Regional dish named among the world's best street food",
        "Coffee shop introduces a reusable cup discount",
    ]
    rows = []
    for label, headlines in (("sports", sports), ("technology", tech), ("food", food)):
        for _ in range(30):
            rows.append({"headline": rng.choice(headlines), "topic": label})
    df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(_data_dir("19_news_topic_sorter") / "headlines.csv", index=False)


# ---------------------------------------------------------------------------
# 20. Study buddy planner
# ---------------------------------------------------------------------------
def build_study_planner() -> None:
    rng = np.random.default_rng(201)
    rows = []
    for _ in range(120):
        hours = int(rng.integers(1, 11))
        difficulty = int(rng.integers(1, 6))
        energy = int(rng.integers(1, 6))
        distraction = int(rng.integers(1, 6))

        if hours <= 2:
            strategy = "Quick review"
        elif energy <= 2 or distraction >= 4:
            strategy = "Take a break first"
        elif difficulty >= 4 and energy >= 3:
            strategy = "Practice problems"
        elif difficulty >= 4:
            strategy = "Ask a friend"
        else:
            strategy = "Deep focus block"

        rows.append(
            {
                "hours_left": hours,
                "difficulty": difficulty,
                "energy": energy,
                "distraction": distraction,
                "strategy": strategy,
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(_data_dir("20_study_buddy_planner") / "study_situations.csv", index=False)


def main() -> None:
    builders = [
        build_snacks,
        build_lemonade,
        build_titanic,
        build_spam,
        build_fruit,
        build_exam_score,
        build_cars,
        build_pizza,
        build_heights,
        build_sleep,
        build_pass_fail,
        build_reviews,
        build_penguins,
        build_iris,
        build_pumpkin,
        build_mood_reviews,
        build_subject_chatbot,
        build_recipes,
        build_news,
        build_study_planner,
    ]
    for builder in builders:
        builder()
        print(f"built: {builder.__name__}")
    print(f"\nAll datasets written under {PROJECTS}")


if __name__ == "__main__":
    main()
