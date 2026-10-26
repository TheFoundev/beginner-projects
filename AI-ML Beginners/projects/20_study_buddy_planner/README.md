# The Study Buddy Planner

**Category:** Text & Logic  
**Algorithm:** Decision Tree  
**Style:** Low-code Python (optional interactive mode)

## The concept

You build a small decision-tree assistant that recommends a study strategy based on hours left, subject difficulty, energy, and distraction. The AI learns from examples of what worked for past students—and you can read its rules. It is like a wise senior giving you a study plan.

## What you will build

Train a decision tree on 120 study situations, print the rules, test four demo plans, and optionally run an interactive quiz.

## Run it

```bash
cd projects/20_study_buddy_planner
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `study_tree.png`, `confusion_matrix.png`, `rules.txt`

## What you will learn

Rule-based recommendations, data quality, and human oversight.

## Try this

Add a 'deadline soon' feature and retrain. Does the advice improve?

## A note

Run `python main.py --interactive` to get a personal plan.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
