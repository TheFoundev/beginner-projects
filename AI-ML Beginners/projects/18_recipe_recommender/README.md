# The Recipe Recommender

**Category:** Text & Logic  
**Algorithm:** K-Nearest Neighbors  
**Style:** Low-code Python

## The concept

You recommend recipes based on how similar they are to one you already like. The AI compares flavor profiles—spicy, sweet, savory, sour, veggie—and finds the closest matches. It is like a friend saying, 'If you liked that dish, try this one.'

## What you will build

Treat 24 recipes as points in flavor space, find the nearest neighbours for three base recipes, and add a 'surprise me' option from a different cuisine.

## Run it

```bash
cd projects/18_recipe_recommender
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `similarity_scores.png`, `recommendations.txt`

## What you will learn

Recommendation systems, similarity, feature scaling, and diversity vs. accuracy.

## Try this

Add 10 recipes you actually like and rerun the recommendations.

## A note

The flavor scores are subjective. That is fine—the model is a helper, not a judge.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
