"""Project 19: The News Topic Sorter (Naive Bayes).

Run:
    python main.py

Multi-class text classification with three topics: sports, technology, and
food.  The confusion matrix shows which topics are easiest to confuse.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)


def main() -> None:
    df = pd.read_csv(DATA / "headlines.csv")
    X_train, X_test, y_train, y_test = train_test_split(
        df["headline"], df["topic"], test_size=0.25, random_state=42, stratify=df["topic"]
    )

    model = Pipeline(
        [
            ("vectorizer", CountVectorizer(stop_words="english", ngram_range=(1, 2))),
            ("classifier", MultinomialNB()),
        ]
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print("=" * 60)
    print("THE NEWS TOPIC SORTER")
    print("=" * 60)
    print(f"Accuracy: {accuracy:.1%}\n")
    print(classification_report(y_test, predictions, zero_division=0))

    vectorizer = model.named_steps["vectorizer"]
    classifier = model.named_steps["classifier"]
    names = vectorizer.get_feature_names_out()
    classes = list(classifier.classes_)
    print("Strongest words per topic:")
    for index, topic in enumerate(classes):
        top = np.argsort(classifier.feature_log_prob_[index])[-8:][::-1]
        print(f"  {topic:10s}: {', '.join(names[top])}")

    new_headlines = [
        "Team wins the final after a dramatic last-minute goal",
        "New open-source tool makes Python debugging easier",
        "Five quick recipes for a healthy student lunch",
        "The city opens a new food market this weekend",
        "A smartphone that folds into a tablet",
    ]
    new_predictions = model.predict(new_headlines)
    new_probabilities = model.predict_proba(new_headlines)
    print("\nNew headline predictions:")
    for headline, prediction, probability in zip(new_headlines, new_predictions, new_probabilities):
        confidence = probability[classes.index(prediction)]
        print(f"  {prediction:10s} ({confidence:.0%}) -> {headline}")

    # ---- Confusion matrix ---------------------------------------------
    labels = sorted(df["topic"].unique())
    cm = confusion_matrix(y_test, predictions, labels=labels)
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    ConfusionMatrixDisplay(cm, display_labels=labels).plot(ax=ax, cmap="Blues", colorbar=False)
    ax.set_title("News topic classification")
    fig.tight_layout()
    fig.savefig(OUT / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "predictions.txt", "w", encoding="utf-8") as handle:
        handle.write(f"accuracy: {accuracy:.4f}\n\n")
        handle.write(classification_report(y_test, predictions, zero_division=0))
        handle.write("\nNew headlines:\n")
        for headline, prediction, probability in zip(new_headlines, new_predictions, new_probabilities):
            handle.write(f"{prediction} ({probability[classes.index(prediction)]:.2%}) -> {headline}\n")

    print("\nSaved: outputs/confusion_matrix.png, outputs/predictions.txt")
    print("Try this: add a 'sports + food' headline and see which topic wins.")


if __name__ == "__main__":
    main()
