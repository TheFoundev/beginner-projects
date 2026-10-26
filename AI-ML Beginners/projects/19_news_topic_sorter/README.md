# The News Topic Sorter

**Category:** Text & Logic  
**Algorithm:** Naive Bayes  
**Style:** Low-code Python

## The concept

You teach an AI to sort short headlines into sports, technology, or food. It learns the words that usually belong to each topic, then labels new headlines. It is like a librarian who files books by subject after seeing enough examples.

## What you will build

Train a three-class text classifier on 90 headlines, inspect the strongest words per topic, and classify five fresh headlines.

## Run it

```bash
cd projects/19_news_topic_sorter
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `confusion_matrix.png`, `predictions.txt`

## What you will learn

Multi-class text classification, confusion matrices, and ambiguous data.

## Try this

Write a headline that could belong to two topics and see which one wins.

## A note

The headlines are synthetic and deliberately simple. Real news is messier.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
