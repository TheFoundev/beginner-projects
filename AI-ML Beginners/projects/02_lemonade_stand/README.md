# The Lemonade Stand Fortune Teller

**Category:** No-Code Intuition Builders (code version)  
**Algorithm:** Linear Regression  
**Style:** Low-code Python (the original no-code tool is Google Sheets)

## The concept

You predict how many cups of lemonade you will sell based on the day's temperature. The AI looks at past days and finds the overall trend—hotter days usually mean more sales—then extends that trend to a new day. It is like drawing a straight line through a scatter of dots.

## What you will build

Load 16 days of temperature and sales, train a line of best fit, and predict a 35°C day. The script saves the scatter plot and the equation.

## Run it

```bash
cd projects/02_lemonade_stand
python main.py
```

If you are using Google Colab, upload the whole project folder and run the same command in a code cell with `!python main.py`.

## Files

- `main.py` — the complete, runnable project
- `data/` — the small dataset used by the project
- `outputs/` — charts, predictions, and summaries created when you run the script

## What you will see

The script saves: `lemonade_regression.png`, `prediction.txt`

## What you will learn

Prediction vs. classification, trendlines, and mean absolute error.

## Try this

Add a rainy-day column or a weekend column and see whether the model improves.

## A note

The original no-code version is in `PROJECT_GUIDE.md`; it uses a Google Sheets trendline.

---

*Part of the 20 Beginner-Friendly AI & ML Projects pack. See the root `README.md` for the full map.*
