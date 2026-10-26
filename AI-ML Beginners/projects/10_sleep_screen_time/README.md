# The Sleep vs. Screen Time Detective

**Category:** Predicting Numbers (Regression)  
**Algorithm:** Linear Regression  
**Style:** Low-code Python

## The concept

You explore whether more screen time before bed is linked to fewer hours of sleep. The AI fits a line to the data and predicts sleep hours for a given screen time. It is like a detective looking for a pattern—not proving a crime.

## What you will build

Train a regression model on 35 records, interpret the slope, and predict sleep for three hours of screen time.

## Run it

```bash
cd projects/10_sleep_screen_time
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `sleep_regression.png`, `metrics.txt`

## What you will learn

Negative correlation, interpreting slope, and the limits of prediction.

## Try this

Add a weekend feature and see whether it improves the model.

## A note

A negative correlation does not prove that screen time causes less sleep.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
