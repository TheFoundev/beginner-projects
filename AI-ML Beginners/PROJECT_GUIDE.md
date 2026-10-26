# 20 Beginner-Friendly AI & ML Projects — Concept Guide

> **Looking for the runnable code?** Every project in this guide now has a real, working implementation in the [`projects/`](projects/) folder. Start with the root [`README.md`](README.md) and run `python3 run_all.py`.

**For 1st-semester engineering students with zero AI/ML background, no advanced math, and only basic programming experience.**

Welcome! You do **not** need to be a math genius or a professional coder to start with AI. Every project below follows the same simple loop:

> **Show examples → let the computer find a pattern → test it on something new → improve it.**

That's it. That's machine learning.

This guide is organized into four categories, with **5 projects in each**, so you can pick a path that matches your comfort level:

| Category | What it teaches | Style |
|---|---|---|
| [1. No-Code Intuition Builders](#category-1-no-code-intuition-builders) | What "training" and "prediction" actually feel like | No-code, browser/visual tools |
| [2. Predicting Numbers (Regression)](#category-2-predicting-numbers-regression) | Predicting a number, like a price or a score | Low-code Python in Google Colab |
| [3. Sorting & Filtering (Classification)](#category-3-sorting--filtering-classification) | Putting things into categories, like spam or not spam | Low-code Python in Google Colab |
| [4. Text & Logic](#category-4-text--logic) | Words, recommendations, and simple decision-making | Mix of no-code and low-code |

**A quick note on the two big ideas:**
- **Regression** = predicting a **number** (e.g., "How many cups of lemonade will I sell?").
- **Classification** = predicting a **category** (e.g., "Is this email spam or not spam?").

Start with Category 1 if you're brand new. Come back to Categories 2–4 when you're ready to type a little Python. Every project is small enough to finish in one sitting, and every dataset runs on a normal laptop or free Google Colab.

---

## Category 1: No-Code Intuition Builders

*Start here. These projects use visual, drag-and-drop tools so you can see AI learn in real time—no programming required.*

### 1. The Snack Sorter: Teach AI to See

**The Concept:** You'll show a computer pictures of two or three snacks (or objects on your desk) and teach it to tell them apart. Behind the scenes, the AI learns visual patterns—color, shape, texture—the same way you learn to recognize a friend's face after seeing it many times. It's like teaching a younger sibling by holding up examples and saying, "This is an apple. This is an orange."

**What You Will Build/Do:** Use your webcam to record 30–50 images for each snack category, train the model, and test it with a snack it has never seen. Then make a "smart lunchbox" label that changes when you show each item.

**Basic Algorithm Used:** **K-Nearest Neighbors (the "similar examples vote" idea)** — When a new picture arrives, the AI compares it with the examples it has already seen and lets the closest matches vote on the label. *(Teachable Machine hides its exact model, but this project builds the KNN intuition you'll use later.)*

**Tools Needed:** Google Teachable Machine (free, browser-based).

**What You Will Learn:** Classification and training data—how the number and quality of examples change what the AI gets right or wrong.

---

### 2. The Lemonade Stand Fortune Teller

**The Concept:** You'll predict how many cups of lemonade you'll sell based on the day's temperature. The AI looks at past days and finds the overall trend—hotter days usually mean more sales—then uses that trend to make a guess. It's like drawing a straight line through a scatter of dots and extending it to tomorrow.

**What You Will Build/Do:** In Google Sheets, enter 12–15 days of temperature and cups sold. Create a scatter chart, add a trendline, and use the equation to predict a 35°C day. Then test the prediction against your own intuition.

**Basic Algorithm Used:** **Linear Regression** — It draws the best straight line through the examples and reads the predicted number off that line.

**Tools Needed:** Google Sheets (free, browser-based).

**What You Will Learn:** Prediction vs. classification, correlation, trendlines, and why a single weird day (an outlier) can bend the line.

---

### 3. The Titanic Survival Oracle

**The Concept:** You'll use passenger details like age, sex, and ticket class to predict who survived the Titanic. The AI learns a chain of simple yes/no questions that separate survivors from non-survivors. It's like a game of 20 Questions where each answer narrows down the possibilities.

**What You Will Build/Do:** Load the kid-friendly Titanic dataset in Machine Learning for Kids (or Orange Data Mining), train a decision tree, and look at the rules it learned. Test a made-up passenger, then simplify the tree and see whether accuracy drops.

**Basic Algorithm Used:** **Decision Tree** — It asks a series of yes/no questions—like "Are you female?" or "Were you in first class?"—until it reaches a prediction.

**Tools Needed:** Machine Learning for Kids (free, browser-based, requires a free IBM account) or Orange Data Mining (free desktop app).

**What You Will Learn:** Classification, interpretable rules, and overfitting—why a tree that's too detailed can memorize instead of learn.

---

### 4. Spam Detective: The Email Filter Game

**The Concept:** You'll teach an AI to separate annoying spam from real messages by showing it examples of both. It learns which words are suspicious—"free," "winner," "urgent"—and uses those clues to label new messages. It's like a detective who notices red flags in a letter.

**What You Will Build/Do:** Type 20–30 spam and normal messages into Machine Learning for Kids' text classifier, train it, and test it with new messages. Then connect it to a Scratch game that shows a "SPAM ALERT!" pop-up.

**Basic Algorithm Used:** **Naive Bayes** — It treats each word as a separate clue, combines the clues, and picks the category with the highest probability.

**Tools Needed:** Machine Learning for Kids + Scratch (both free and browser-based).

**What You Will Learn:** Text classification, training data bias, and false positives—flagging a real email as spam.

---

### 5. The Fruit Basket Sorter

**The Concept:** You'll describe fruits with simple numbers—sweetness, weight, and size—and let an AI sort a new fruit by finding the most similar ones. It's like a new student choosing a lunch table: they sit with the group that seems most like them.

**What You Will Build/Do:** Create a 30-row spreadsheet of apple, banana, and orange examples, load it into Orange Data Mining, run the K-Nearest Neighbors widget, and test a mystery fruit. Then plot the data to see the groups form before your eyes.

**Basic Algorithm Used:** **K-Nearest Neighbors (KNN)** — It finds the closest examples in the data and lets the majority decide the label.

**Tools Needed:** Google Sheets + Orange Data Mining (free desktop app; drag-and-drop, no coding).

**What You Will Learn:** Classification, similarity/distance, and why the features you choose matter more than the algorithm.

---

## Category 2: Predicting Numbers (Regression)

*These projects predict a number instead of a category. You'll write a few lines of Python in Google Colab—no installation, no setup, just a browser.*

### 6. Predict Your Exam Score

**The Concept:** You'll feed the AI pairs of "hours studied" and "exam score" and ask it to predict a score for a new number of hours. The AI finds the trend line that best fits your study history. It's like a coach estimating your race time from how many weeks you've trained.

**What You Will Build/Do:** Create a 12-row table in Colab, plot it, train a Linear Regression model with scikit-learn, draw the line, and predict the score for 6 hours of study. Then compare the AI's guess with a friend's guess.

**Basic Algorithm Used:** **Linear Regression** — It fits a straight line through the data and uses the line to estimate a number.

**Tools Needed:** Google Colab, pandas, matplotlib, scikit-learn (all free).

**What You Will Learn:** Features and target, model training, prediction, and a basic train/test split.

---

### 7. The Used Car Price Whisperer

**The Concept:** You'll estimate a used car's price from its age and kilometers driven. The AI learns how much each clue usually affects price, then combines them into one estimate. It's like an experienced dealer who can eyeball a car and guess its value.

**What You Will Build/Do:** Use a 15-car CSV (age, kilometers, price), train a multiple linear regression, and predict the price of a 5-year-old car with 60,000 km. Print the model's weights to see which clue matters more.

**Basic Algorithm Used:** **Multiple Linear Regression** — It gives each clue a weight, adds up the weighted clues, and produces an estimate.

**Tools Needed:** Google Colab, pandas, scikit-learn, matplotlib.

**What You Will Learn:** Multiple features, coefficients (the "weights"), and mean absolute error—a simple way to measure how wrong the predictions are.

---

### 8. The Pizza Price Calculator

**The Concept:** You'll build a mini app that quotes a pizza price based on size and number of toppings. The AI learns the pricing pattern from a small menu of examples. It's like a pizzeria owner who scales prices up as the pizza gets bigger.

**What You Will Build/Do:** Generate a tiny menu dataset, train a regression model, and write a `quote_pizza(size, toppings)` function. Test it with a 12-inch pizza with 3 toppings and compare the result with the real menu.

**Basic Algorithm Used:** **Linear Regression** — It finds the pricing trend in the examples and applies it to a new pizza.

**Tools Needed:** Google Colab, pandas, scikit-learn.

**What You Will Learn:** Feature engineering (diameter vs. area), interactive prediction, and the assumptions a model quietly makes.

---

### 9. How Tall Will You Be? The Height Predictor

**The Concept:** You'll use parents' heights to predict a child's adult height. The AI learns the average pattern—taller parents tend to have taller kids—without claiming to know the future. It's like a growth chart that gives a reasonable estimate, not a guarantee.

**What You Will Build/Do:** Load a small parent–child height dataset, plot the points, train a linear regression, and predict for a new family. Then discuss why real height also depends on nutrition, health, and chance.

**Basic Algorithm Used:** **Linear Regression** — It draws the best-fit line between parent height and child height and reads a prediction from it.

**Tools Needed:** Google Colab, pandas, matplotlib, scikit-learn.

**What You Will Learn:** Correlation vs. causation, noise in data, and making responsible predictions.

---

### 10. The Sleep vs. Screen Time Detective

**The Concept:** You'll explore whether more screen time before bed is linked to fewer hours of sleep. The AI fits a line to your dataset and predicts sleep hours for a given amount of screen time. It's like a detective looking for a pattern—not proving a crime.

**What You Will Build/Do:** Use a 20-row sample dataset, train a linear regression, and interpret the slope (for example, "Each extra hour of screen time is associated with X fewer hours of sleep"). Visualize the line, then list what the model cannot tell you.

**Basic Algorithm Used:** **Linear Regression** — It finds the straight-line trend and uses it to estimate a number.

**Tools Needed:** Google Colab, pandas, matplotlib, scikit-learn.

**What You Will Learn:** Negative correlation, interpreting slope, and the limits of prediction.

---

## Category 3: Sorting & Filtering (Classification)

*Here the AI picks a label: pass/fail, fake/real, species A/B/C. You'll use small, clean datasets that train in seconds—even on a basic laptop.*

### 11. Will You Pass? The Exam Predictor

**The Concept:** You'll predict whether a student passes based on hours studied and attendance. Instead of a simple yes/no guess, the AI outputs a probability—like a weather app saying "80% chance of rain." It's like a coach drawing a boundary between "ready" and "not ready."

**What You Will Build/Do:** Create a small dataset, train logistic regression, print the probability for a new student, and plot the decision boundary using two features. Then change the cutoff from 50% to 70% and see how the predictions change.

**Basic Algorithm Used:** **Logistic Regression** — It combines the clues into a score, converts that score into a probability, and picks the category above a cutoff.

**Tools Needed:** Google Colab, pandas, scikit-learn, matplotlib.

**What You Will Learn:** Binary classification, probability thresholds, and decision boundaries.

---

### 12. The Fake Review Spotter

**The Concept:** You'll train an AI to spot suspicious product reviews by learning the words that tend to appear in fake ones—"amazing," "best ever," "buy now." It's not a lie detector; it's a pattern finder. It's like a shopkeeper who notices when a review sounds copied and pasted.

**What You Will Build/Do:** Collect 40–60 short reviews (or use a provided sample), label them real or fake, convert the words into numbers with CountVectorizer, train a Naive Bayes classifier, and test it on new reviews. Inspect the words that push a review toward "fake."

**Basic Algorithm Used:** **Naive Bayes** — It treats each word as a clue, combines the clues, and chooses the most likely label.

**Tools Needed:** Google Colab, pandas, scikit-learn.

**What You Will Learn:** Text classification, word features, and precision vs. recall—avoiding false accusations.

---

### 13. The Penguin Detective

**The Concept:** You'll identify a penguin's species from simple measurements like beak length and flipper length. The AI compares a new penguin to the most similar penguins it has seen. It's like recognizing a bird by its body shape, the way a birder does.

**What You Will Build/Do:** Load the Palmer Penguins dataset (only about 344 rows), make a scatter plot, train KNN with k=3 and k=5, predict a new penguin, and see how the choice of k changes the answer.

**Basic Algorithm Used:** **K-Nearest Neighbors (KNN)** — It finds the closest examples and lets the majority vote.

**Tools Needed:** Google Colab, pandas, seaborn, scikit-learn.

**What You Will Learn:** KNN, distance, choosing k, and feature scaling.

---

### 14. The Iris Flower Identifier

**The Concept:** You'll classify iris flowers into three species using petal and sepal measurements. The AI builds a flowchart of yes/no questions that a human can read and understand. It's like a botanist's field guide turned into a decision chart.

**What You Will Build/Do:** Load the classic 150-row Iris dataset, train a decision tree, plot the tree, and test a new flower. Then limit the tree's depth and see whether a simpler tree performs better.

**Basic Algorithm Used:** **Decision Tree** — It asks a series of yes/no questions about the measurements until it reaches a species.

**Tools Needed:** Google Colab, pandas, scikit-learn, matplotlib.

**What You Will Learn:** Decision trees, interpretability, overfitting, and accuracy.

---

### 15. The Pumpkin Seed Sorter

**The Concept:** You'll sort pumpkin seeds into different varieties using measurements like length, width, and weight. The AI learns a set of rules that separate the varieties, and you can visually check where it succeeds and fails. It's like sorting seeds into labeled jars by feel and size.

**What You Will Build/Do:** Load a small pumpkin-seed dataset, train a decision tree, print its rules, and test a few held-out seeds. Then compare a shallow tree with a deep tree and discuss which one you'd trust.

**Basic Algorithm Used:** **Decision Tree** — It splits the seeds with yes/no rules until it reaches a variety.

**Tools Needed:** Google Colab, pandas, scikit-learn, matplotlib.

**What You Will Learn:** Multi-class classification, rule-based models, and train/test evaluation.

---

## Category 4: Text & Logic

*These projects work with words, recommendations, and decision-making. They're a little more open-ended—perfect for a mini hackathon, a club demo, or a final showcase.*

### 16. The Movie Review Mood Ring

**The Concept:** You'll build a sentiment detector that reads a short movie review and labels it happy, unhappy, or mixed. The AI learns which words tend to signal positive or negative opinions. It's like a friend who can tell your mood from a text message.

**What You Will Build/Do:** Use 60–100 short reviews (or write your own), train a Naive Bayes text classifier, test it on reviews it has never seen, and display the most important words. Bonus: build a simple "mood meter" bar in Colab.

**Basic Algorithm Used:** **Naive Bayes** — It adds up the positive and negative word clues and picks the more likely mood.

**Tools Needed:** Google Colab, pandas, scikit-learn, matplotlib.

**What You Will Learn:** Sentiment analysis, tokenization, and the confusion matrix.

---

### 17. The Chatbot That Guesses Your Favorite Subject

**The Concept:** You'll build a chatbot that asks a few questions and guesses whether you're a math, biology, or literature person. The AI uses a decision tree—a flowchart of questions—to narrow down the answer. It's like a friendly career counselor with a stack of index cards.

**What You Will Build/Do:** In Machine Learning for Kids + Scratch, create a training table of answers and subjects, train a decision tree, and connect it to a Scratch chatbot. Test it on friends and improve the questions.

**Basic Algorithm Used:** **Decision Tree** — It follows a path of yes/no questions until it reaches a guess.

**Tools Needed:** Machine Learning for Kids + Scratch (both free and browser-based; no Python required).

**What You Will Learn:** Conversational logic, decision trees, and bias in training data.

---

### 18. The Recipe Recommender

**The Concept:** You'll recommend recipes based on how similar they are to one you already like. The AI compares flavor profiles—spicy, sweet, savory—and finds the closest matches. It's like a friend saying, "If you liked that dish, try this one."

**What You Will Build/Do:** Create a 20-recipe table with simple flavor scores, train a KNN model, and recommend the top 3 recipes for a dish you love. Then add a "surprise me" option that picks a recipe from a different cuisine.

**Basic Algorithm Used:** **K-Nearest Neighbors (KNN)** — It finds the recipes with the most similar flavor profiles and recommends them.

**Tools Needed:** Google Colab, pandas, scikit-learn.

**What You Will Learn:** Recommendation systems, similarity, feature scaling, and the trade-off between accuracy and variety.

---

### 19. The News Topic Sorter

**The Concept:** You'll teach an AI to sort short news headlines into sports, technology, or food. It learns the words that usually belong to each topic, then labels new headlines. It's like a librarian who files books by subject after seeing enough examples.

**What You Will Build/Do:** Collect 60 headlines (20 per topic), train a Naive Bayes classifier, test it on fresh headlines, and show a confusion matrix. Then try a headline that could belong to two topics and discuss why the AI struggles.

**Basic Algorithm Used:** **Naive Bayes** — It treats each word as a clue and picks the topic with the highest combined probability.

**Tools Needed:** Google Colab, pandas, scikit-learn, seaborn.

**What You Will Learn:** Multi-class text classification, confusion matrices, and ambiguous data.

---

### 20. The Study Buddy Planner

**The Concept:** You'll build a small decision-tree assistant that recommends a study strategy based on hours left, subject difficulty, and energy level. The AI learns from examples of what worked for past students—and you can read its rules. It's like a wise senior giving you a study plan.

**What You Will Build/Do:** Create a 20-row dataset of study situations and recommended strategies, train a decision tree, print the rules, and build a simple quiz that asks three questions and outputs a plan. Then test the advice and improve the dataset.

**Basic Algorithm Used:** **Decision Tree** — It asks a few yes/no questions about your situation and follows the branch to a recommendation.

**Tools Needed:** Google Colab, pandas, scikit-learn (optional: ipywidgets for buttons).

**What You Will Learn:** Rule-based recommendations, data quality, and human oversight.

---

## Pick Your First Project

- **Brand new to AI?** Start with **#1 (Snack Sorter)** and **#2 (Lemonade Stand)**. You'll understand "training" and "prediction" in under an hour.
- **Want to type a little Python?** Try **#6 (Exam Score)** or **#13 (Penguin Detective)**. Both use tiny, friendly datasets.
- **Love words and stories?** Jump to **#16 (Movie Review Mood Ring)** or **#19 (News Topic Sorter)**.
- **Want something visual for a demo?** Build **#1**, **#5**, or **#14**—they produce charts, live webcam reactions, or a readable tree.

## Mini Glossary

- **Model:** The pattern the computer learns from examples.
- **Training data:** The examples you show the computer.
- **Feature:** A clue the model uses (temperature, beak length, a word in an email).
- **Label:** The answer you want to predict (spam, species, price).
- **Prediction:** The model's guess for a new example.
- **Overfitting:** When a model memorizes the training examples instead of learning the general pattern.
- **Train/test split:** Keeping some examples hidden so you can check whether the model actually learned.

## A Few Friendly Rules

1. **Start small.** Ten good examples beat a thousand messy ones.
2. **Always test on something new.** A model that only remembers its training data hasn't really learned.
3. **Expect mistakes.** Every AI project has weird failures—that's where the learning happens.
4. **Ask "why?"** If a model makes a surprising prediction, inspect the data and the clues.
5. **Keep humans in the loop.** AI is a helper, not a replacement for your judgment—especially for decisions about people.

Happy building! 🚀
