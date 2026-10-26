# The Used Car Price Whisperer

**Category:** Predicting Numbers (Regression)  
**Algorithm:** Multiple Linear Regression  
**Style:** Low-code Python

## The concept

You estimate a used car's price from its age and kilometres driven. The AI learns how much each clue usually affects price, then combines them into one estimate. It is like an experienced dealer who can eyeball a car and guess its value.

## What you will build

Train a two-feature regression model on 45 cars, print the model's weights, and predict the price of a 5-year-old car with 60,000 km.

## Run it

```bash
cd projects/07_car_price
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `actual_vs_predicted.png`, `metrics.txt`

## What you will learn

Multiple features, coefficients, and mean absolute error.

## Try this

Add a fuel-type column, encode it as 0/1, and retrain.

## A note

The coefficients are associations, not guarantees. A real car's price also depends on condition and demand.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
