# The Movie Review Mood Ring

**Category:** Text & Logic  
**Algorithm:** Naive Bayes  
**Style:** Low-code Python

## The concept

You build a sentiment detector that reads a short movie review and labels it positive, negative, or mixed. The AI learns which words tend to signal each mood. It is like a friend who can tell your mood from a text message.

## What you will build

Train a three-class text classifier on 90 reviews, inspect the top words for each mood, and turn one prediction into a 'mood meter' chart.

## Run it

```bash
cd projects/16_movie_mood_ring
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `mood_meter.png`, `confusion_matrix.png`, `predictions.txt`

## What you will learn

Sentiment analysis, multi-class text classification, and the confusion matrix.

## Try this

Write a sarcastic review and see whether the model understands the joke.

## A note

Sarcasm is hard for bag-of-words models. That limitation is part of the lesson.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
