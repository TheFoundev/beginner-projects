# Will You Pass? The Exam Predictor

**Category:** Sorting & Filtering (Classification)  
**Algorithm:** Logistic Regression  
**Style:** Low-code Python

## The concept

You predict whether a student passes based on hours studied and attendance. Instead of a simple yes/no guess, the AI outputs a probability—like a weather app saying '80% chance of rain'. It is like a coach drawing a boundary between 'ready' and 'not ready'.

## What you will build

Train a logistic regression on 120 students, plot the decision boundary, and compare predictions at 50% and 70% cutoffs.

## Run it

```bash
cd projects/11_exam_pass_predictor
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `decision_boundary.png`, `confusion_matrix.png`, `metrics.txt`

## What you will learn

Binary classification, probability thresholds, and decision boundaries.

## Try this

Change the cutoff to 0.8 and discuss which mistake is worse: a false pass or a false fail.

## A note

The dataset is synthetic. A real academic model would need careful ethical review.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
