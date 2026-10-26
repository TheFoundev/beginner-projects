# Predict Your Exam Score

**Category:** Predicting Numbers (Regression)  
**Algorithm:** Linear Regression  
**Style:** Low-code Python

## The concept

You feed the AI pairs of 'hours studied' and 'exam score' and ask it to predict a score for a new number of hours. The AI finds the trend line that best fits the examples. It is like a coach estimating your race time from how many weeks you have trained.

## What you will build

Train a regression model on 28 study records, draw the line of best fit, and predict the score for 6 hours of study.

## Run it

```bash
cd projects/06_exam_score
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `exam_score_regression.png`, `metrics.txt`

## What you will learn

Features and target, model training, prediction, and train/test split.

## Try this

Collect five real study-hour/score pairs and add them to the CSV.

## A note

A straight line is a starting point. Real exam scores also depend on sleep, prior knowledge, and luck.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
