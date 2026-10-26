# Spam Detective

**Category:** No-Code Intuition Builders (code version)  
**Algorithm:** Naive Bayes  
**Style:** Low-code Python (the original no-code tool is Machine Learning for Kids + Scratch)

## The concept

You teach an AI to separate spam from normal messages by showing it examples of both. It learns which words are suspicious—'free', 'winner', 'urgent'—and uses those clues to label new messages. It is like a detective who notices red flags in a letter.

## What you will build

Train a text classifier on 80 messages, test it on new messages, and save the top spam/ham clues plus a confusion matrix.

## Run it

```bash
cd projects/04_spam_detective
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

Text classification, training data bias, and false positives.

## Try this

Add five of your own spam messages and five normal messages, then retrain.

## A note

The messages are generated from templates so the project runs offline and contains no private data.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
