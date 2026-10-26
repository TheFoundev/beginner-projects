# The Chatbot That Guesses Your Favorite Subject

**Category:** Text & Logic  
**Algorithm:** Decision Tree  
**Style:** No-code option available (Machine Learning for Kids + Scratch); this is the Python version

## The concept

You build a chatbot that asks six questions and guesses whether you are a math, biology, or literature person. The AI uses a decision tree—a flowchart of questions—to narrow down the answer. It is like a friendly career counselor with a stack of index cards.

## What you will build

Train a decision tree on 90 answer profiles, print the question path, test three demo students, and optionally run an interactive quiz.

## Run it

```bash
cd projects/17_subject_chatbot
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `chatbot_tree.png`, `rules.txt`

## What you will learn

Conversational logic, decision trees, and bias in training data.

## Try this

Add a new subject and 20 example profiles. Does the tree still make sense?

## A note

Run `python main.py --interactive` to answer the questions yourself.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
