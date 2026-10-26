# The Penguin Detective

**Category:** Sorting & Filtering (Classification)  
**Algorithm:** K-Nearest Neighbors  
**Style:** Low-code Python

## The concept

You identify a penguin's species from measurements such as bill length, bill depth, flipper length, and body mass. The AI compares a new penguin to the most similar penguins it has seen. It is like recognising a bird by its body shape, the way a birder does.

## What you will build

Train KNN with k=3 and k=5, compare accuracy, classify a new penguin, and save a scatter plot of the species clusters.

## Run it

```bash
cd projects/13_penguin_detective
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `penguin_scatter.png`, `confusion_matrix.png`, `metrics.txt`

## What you will learn

KNN, distance, choosing k, and feature scaling.

## Try this

Remove `body_mass_g` and see whether accuracy changes. Why?

## A note

The measurements are synthetic, inspired by the Palmer Penguins dataset.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
