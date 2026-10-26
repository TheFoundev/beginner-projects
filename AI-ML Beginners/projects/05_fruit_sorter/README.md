# The Fruit Basket Sorter

**Category:** No-Code Intuition Builders (code version)  
**Algorithm:** K-Nearest Neighbors  
**Style:** Low-code Python (the original no-code tool is Orange Data Mining)

## The concept

You describe fruits with simple numbers—sweetness, weight, size, and colour score—and let an AI sort a new fruit by finding the most similar ones. It is like a new student choosing a lunch table: they sit with the group that seems most like them.

## What you will build

Train a KNN classifier on 60 fruit examples, classify a mystery fruit, and save a scatter plot that shows the groups.

## Run it

```bash
cd projects/05_fruit_sorter
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `fruit_scatter.png`, `confusion_matrix.png`, `metrics.txt`

## What you will learn

Classification, similarity/distance, and why feature choice matters.

## Try this

Change `n_neighbors` from 5 to 1 and then 9. Which setting feels most stable?

## A note

The features are synthetic but the workflow is exactly the same as the Orange drag-and-drop version.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
