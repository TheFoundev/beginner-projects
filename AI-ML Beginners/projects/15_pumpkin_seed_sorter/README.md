# The Pumpkin Seed Sorter

**Category:** Sorting & Filtering (Classification)  
**Algorithm:** Decision Tree  
**Style:** Low-code Python

## The concept

You sort pumpkin seeds into three varieties using measurements such as area, perimeter, and axis lengths. The AI learns a set of yes/no rules that separate the varieties. It is like sorting seeds into labeled jars by feel and size.

## What you will build

Train three decision trees with different depths, print the rules for the best one, and classify a new seed.

## Run it

```bash
cd projects/15_pumpkin_seed_sorter
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `pumpkin_tree.png`, `confusion_matrix.png`, `rules.txt`

## What you will learn

Multi-class classification, rule-based models, and train/test evaluation.

## Try this

Add a fourth variety to the CSV and retrain.

## A note

The measurements are synthetic, inspired by the UCI pumpkin-seed dataset.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
