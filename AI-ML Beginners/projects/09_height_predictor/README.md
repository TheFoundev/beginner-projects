# How Tall Will You Be?

**Category:** Predicting Numbers (Regression)  
**Algorithm:** Linear Regression  
**Style:** Low-code Python

## The concept

You use parents' heights to predict a child's adult height. The AI learns the average pattern—taller parents tend to have taller kids—without claiming to know the future. It is like a growth chart that gives a reasonable estimate, not a guarantee.

## What you will build

Train a model on 60 parent-child height records, plot the trend, and predict a child's height for a midparent height of 170 cm.

## Run it

```bash
cd projects/09_height_predictor
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `height_regression.png`, `metrics.txt`

## What you will learn

Correlation vs. causation, noise in data, and responsible predictions.

## Try this

Use mother and father as two separate features and compare the error.

## A note

This is an educational model, not medical advice. Nutrition, health, sleep, and chance also matter.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
