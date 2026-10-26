# The Titanic Survival Oracle

**Category:** No-Code Intuition Builders (code version)  
**Algorithm:** Decision Tree  
**Style:** Low-code Python (the original no-code tool is Machine Learning for Kids or Orange)

## The concept

You use passenger details such as age, sex, and ticket class to predict who survived the Titanic. The AI learns a chain of simple yes/no questions that separate survivors from non-survivors. It is like a game of 20 Questions where each answer narrows the possibilities.

## What you will build

Train a shallow decision tree on a small Titanic-style dataset, print the rules it learned, test a made-up passenger, and save a diagram of the tree.

## Run it

```bash
cd projects/03_titanic_survival
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `titanic_tree.png`, `confusion_matrix.png`, `rules.txt`

## What you will learn

Classification, interpretable rules, and overfitting.

## Try this

Change `max_depth` from 4 to 2, then to 8, and compare the rules and accuracy.

## A note

The dataset is a small synthetic practice set inspired by the Titanic. Replace it with a real Titanic CSV when you are ready.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
