"""Project 12: The Fake Review Spotter (Naive Bayes).

Run:
    python main.py

A text classifier that learns word patterns.  It is a pattern finder, not a
lie detector: the README explains why that distinction matters.
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


def top_words(model: Pipeline, class_index: int, n: int = 10) -> list[str]:
    vectorizer = model.named_steps["vectorizer"]
    classifier = model.named_steps["classifier"]
    names = vectorizer.get_feature_names_out()
    scores = classifier.feature_log_prob_[class_index] - classifier.feature_log_prob_[1 - class_index]
    return list(names[np.argsort(scores)[-n:][::-1]])


def main() -> None:
    df = pd.read_csv(DATA / "reviews.csv")
    X_train, X_test, y_train, y_test = train_test_split(
        df["review"], df["label"], test_size=0.25, random_state=42, stratify=df["label"]
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
    print("THE FAKE REVIEW SPOTTER")
    print("=" * 60)
    print(f"Accuracy: {accuracy:.1%}\n")
    print(classification_report(y_test, predictions, zero_division=0))

    classes = list(model.named_steps["classifier"].classes_)
    fake_index = classes.index("fake")
    fake_words = top_words(model, fake_index)
    real_words = top_words(model, 1 - fake_index)
    print("Top 'fake' clues:", ", ".join(fake_words))
    print("Top 'real' clues:", ", ".join(real_words))

    new_reviews = [
        "AMAZING!!! Best product ever. Buy it now, you will not regret it!",
        "The item arrived on time. The battery is fine, but the cable is short.",
        "Perfect quality, perfect price, perfect everything. Five stars!",
        "It works as described. Shipping took a week longer than expected.",
    ]
    new_predictions = model.predict(new_reviews)
    new_probabilities = model.predict_proba(new_reviews)
    print("\nNew review predictions:")
    for review, prediction, probability in zip(new_reviews, new_predictions, new_probabilities):
        confidence = probability[classes.index(prediction)]
        print(f"  {prediction:4s} ({confidence:.0%}) -> {review}")

    # ---- Top-word chart ------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, words, title, colour in (
        (axes[0], fake_words, "Words that suggest a fake review", "#c0392b"),
        (axes[1], real_words, "Words that suggest a real review", "#2471a3"),
    ):
        ax.barh(words[::-1], range(1, len(words) + 1), color=colour)
        ax.set_title(title)
        ax.set_xlabel("relative clue strength")
        ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "top_words.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---- Confusion matrix ---------------------------------------------
    labels = ["fake", "real"]
    cm = confusion_matrix(y_test, predictions, labels=labels)
    fig, ax = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay(cm, display_labels=labels).plot(ax=ax, cmap="Purples", colorbar=False)
    ax.set_title("Fake review classification")
    fig.tight_layout()
    fig.savefig(OUT / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "predictions.txt", "w", encoding="utf-8") as handle:
        handle.write(f"accuracy: {accuracy:.4f}\n\n")
        handle.write(classification_report(y_test, predictions, zero_division=0))
        handle.write("\nNew reviews:\n")
        for review, prediction, probability in zip(new_reviews, new_predictions, new_probabilities):
            handle.write(f"{prediction} ({probability[classes.index(prediction)]:.2%}) -> {review}\n")

    print("\nSaved: outputs/top_words.png, outputs/confusion_matrix.png, outputs/predictions.txt")
    print("Try this: add 10 honest reviews that sound enthusiastic and see whether they fool the model.")


if __name__ == "__main__":
    main()
