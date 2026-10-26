# The Pizza Price Calculator

**Category:** Predicting Numbers (Regression)  
**Algorithm:** Linear Regression  
**Style:** Low-code Python

## The concept

You build a mini app that quotes a pizza price based on size and number of toppings. The AI learns the pricing pattern from a small menu of examples. It is like a pizzeria owner who scales prices up as the pizza gets bigger.

## What you will build

Train a regression model on 45 menu items, print the pricing equation, and use a `quote_pizza()` function to price four orders.

## Run it

```bash
cd projects/08_pizza_price
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `actual_vs_predicted.png`, `quotes.txt`

## What you will learn

Feature engineering, interactive prediction, and model assumptions.

## Try this

Add a stuffed-crust true/false column and compare the new model's error.

## A note

The menu is synthetic. Replace it with a real price list to make the calculator useful.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
