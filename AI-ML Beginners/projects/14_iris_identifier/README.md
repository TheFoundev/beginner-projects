# The Iris Flower Identifier

**Category:** Sorting & Filtering (Classification)  
**Algorithm:** Decision Tree  
**Style:** Low-code Python

## The concept

You classify iris flowers into three species using petal and sepal measurements. The AI builds a flowchart of yes/no questions that a human can read and understand. It is like a botanist's field guide turned into a decision chart.

## What you will build

Train decision trees with different depths on the classic 150-row Iris dataset, plot the best tree, and classify a new flower.

## Run it

```bash
cd projects/14_iris_identifier
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `iris_tree.png`, `confusion_matrix.png`, `rules.txt`

## What you will learn

Decision trees, interpretability, overfitting, and accuracy.

## Try this

Set `max_depth=2` and compare the simpler tree with the deeper one.

## A note

Iris is the classic beginner dataset. It is small, clean, and built into scikit-learn, but we save it as a CSV so you can inspect it.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
