# The Fake Review Spotter

**Category:** Sorting & Filtering (Classification)  
**Algorithm:** Naive Bayes  
**Style:** Low-code Python

## The concept

You train an AI to spot suspicious product reviews by learning the words that tend to appear in fake ones—'amazing', 'best ever', 'buy now'. It is not a lie detector; it is a pattern finder. It is like a shopkeeper who notices when a review sounds copied and pasted.

## What you will build

Train a text classifier on 80 reviews, inspect the strongest fake/real words, and test four new reviews.

## Run it

```bash
cd projects/12_fake_review_spotter
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `top_words.png`, `confusion_matrix.png`, `predictions.txt`

## What you will learn

Text classification, precision vs. recall, and the danger of false accusations.

## Try this

Add 10 honest reviews that sound enthusiastic and see whether they fool the model.

## A note

Never use a model like this to accuse a real person. It only detects word patterns.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
