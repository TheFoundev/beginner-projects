# 20 Beginner-Friendly AI & ML Projects — Runnable Code Pack

A complete set of **20 real, runnable machine-learning projects** for 1st-semester engineering students.

No GPU. No API keys. No massive downloads. Every project runs on a normal laptop with Python 3.10+.

Each project has its own folder containing:

- `main.py` — the full project code
- `data/` — the dataset (CSV, or generated snack photos)
- `README.md` — a short student guide
- `outputs/` — charts, predictions, and summaries created when you run it

---

## Quick start

```bash
cd "/home/aziz/foundev/AI-ML beginners"
python3 -m pip install -r requirements.txt
python3 build_data.py          # regenerate all datasets (already included)
python3 projects/06_exam_score/main.py
```

Or run everything at once:

```bash
python3 run_all.py
```

Check that all 20 projects and their outputs are present:

```bash
python3 verify_projects.py
```

Every script is headless-friendly: it saves figures to `outputs/` instead of opening a window. If you use Google Colab, upload a project folder and run `!python main.py`.

---

## Project map

| # | Project | Category | Algorithm | Code style |
|---|---|---|---|---|
| 01 | [The Snack Sorter](projects/01_snack_sorter/) | No-Code Intuition Builders | K-Nearest Neighbors | Python, image features |
| 02 | [The Lemonade Stand Fortune Teller](projects/02_lemonade_stand/) | No-Code Intuition Builders | Linear Regression | Python |
| 03 | [The Titanic Survival Oracle](projects/03_titanic_survival/) | No-Code Intuition Builders | Decision Tree | Python |
| 04 | [Spam Detective](projects/04_spam_detective/) | No-Code Intuition Builders | Naive Bayes | Python, text |
| 05 | [The Fruit Basket Sorter](projects/05_fruit_sorter/) | No-Code Intuition Builders | K-Nearest Neighbors | Python |
| 06 | [Predict Your Exam Score](projects/06_exam_score/) | Predicting Numbers | Linear Regression | Python |
| 07 | [The Used Car Price Whisperer](projects/07_car_price/) | Predicting Numbers | Multiple Linear Regression | Python |
| 08 | [The Pizza Price Calculator](projects/08_pizza_price/) | Predicting Numbers | Linear Regression | Python |
| 09 | [How Tall Will You Be?](projects/09_height_predictor/) | Predicting Numbers | Linear Regression | Python |
| 10 | [The Sleep vs. Screen Time Detective](projects/10_sleep_screen_time/) | Predicting Numbers | Linear Regression | Python |
| 11 | [Will You Pass?](projects/11_exam_pass_predictor/) | Sorting & Filtering | Logistic Regression | Python |
| 12 | [The Fake Review Spotter](projects/12_fake_review_spotter/) | Sorting & Filtering | Naive Bayes | Python, text |
| 13 | [The Penguin Detective](projects/13_penguin_detective/) | Sorting & Filtering | K-Nearest Neighbors | Python |
| 14 | [The Iris Flower Identifier](projects/14_iris_identifier/) | Sorting & Filtering | Decision Tree | Python |
| 15 | [The Pumpkin Seed Sorter](projects/15_pumpkin_seed_sorter/) | Sorting & Filtering | Decision Tree | Python |
| 16 | [The Movie Review Mood Ring](projects/16_movie_mood_ring/) | Text & Logic | Naive Bayes | Python, text |
| 17 | [The Favorite-Subject Chatbot](projects/17_subject_chatbot/) | Text & Logic | Decision Tree | Python + interactive mode |
| 18 | [The Recipe Recommender](projects/18_recipe_recommender/) | Text & Logic | K-Nearest Neighbors | Python |
| 19 | [The News Topic Sorter](projects/19_news_topic_sorter/) | Text & Logic | Naive Bayes | Python, text |
| 20 | [The Study Buddy Planner](projects/20_study_buddy_planner/) | Text & Logic | Decision Tree | Python + interactive mode |

---

## What each project actually does

### No-Code Intuition Builders
The original course design used visual no-code tools. This pack gives each one a **real Python implementation** so students can inspect the data, run the model, and see the output files. The no-code alternatives are still listed in each project README and in `PROJECT_GUIDE.md`.

### Predicting Numbers (Regression)
Projects 06–10 predict a number: a score, a price, a height, or hours of sleep. They use `scikit-learn`'s `LinearRegression`, `train_test_split`, and error metrics such as MAE and R².

### Sorting & Filtering (Classification)
Projects 11–15 predict a category: pass/fail, fake/real, penguin species, iris species, or pumpkin variety. They cover logistic regression, Naive Bayes, KNN, and decision trees.

### Text & Logic
Projects 16–20 work with words, recommendations, and rule-based decisions. They include three text classifiers, a KNN recommender, and two interactive decision-tree demos.

---

## Requirements

```
numpy
pandas
matplotlib
scikit-learn
Pillow
```

Install with:

```bash
python3 -m pip install -r requirements.txt
```

Python 3.10 or newer is recommended. The pack was tested with Python 3.14, NumPy 2.5, pandas 2.3, scikit-learn 1.9, and Matplotlib 3.11.

---

## Suggested learning path

1. **Start with 02 (Lemonade Stand)** — the simplest possible regression.
2. **Try 11 (Will You Pass?)** — the simplest possible classification with probabilities.
3. **Move to 06 (Exam Score)** and **13 (Penguin Detective)** — one regression, one classification, both with clear charts.
4. **Read 14 (Iris)** — a decision tree you can trace by hand.
5. **Finish with 16–20** — text, recommendations, and an interactive planner.

Each project README ends with a **Try this** prompt so students can change one thing and see what happens.

---

## Notes on the data

Most datasets are **small, synthetic, and offline-friendly**. They were created with `build_data.py` so the pack runs without internet access, accounts, or privacy concerns. Project 14 uses the real classic Iris dataset, loaded from scikit-learn and saved as a CSV. All datasets are designed to teach the workflow, not to make real-world decisions.

When you are ready, replace a `data/*.csv` with a real dataset and rerun the script. The code does not care where the CSV came from.

---

## Files in the pack root

- `README.md` — this guide
- `PROJECT_GUIDE.md` — the original 20-project concept guide with no-code tool suggestions
- `build_data.py` — regenerates every dataset
- `build_readmes.py` — regenerates the 20 project READMEs
- `run_all.py` — runs all 20 projects and reports pass/fail
- `verify_projects.py` — checks that every project and output exists
- `requirements.txt` — Python dependencies

---

## Important disclaimer

These projects are for learning. Do not use them to make decisions about real people, real money, health, safety, or academic fairness without expert review, better data, and human oversight.
