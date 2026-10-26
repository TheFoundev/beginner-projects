"""Project 16: The Movie Review Mood Ring (Naive Bayes).

Run:
    python main.py

A three-class sentiment project: positive, negative, or mixed.  The script
also turns one prediction into a simple "mood meter" chart.
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
    df = pd.read_csv(DATA / "movie_reviews.csv")
    X_train, X_test, y_train, y_test = train_test_split(
        df["review"], df["mood"], test_size=0.25, random_state=42, stratify=df["mood"]
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
    print("THE MOVIE REVIEW MOOD RING")
    print("=" * 60)
    print(f"Accuracy: {accuracy:.1%}\n")
    print(classification_report(y_test, predictions, zero_division=0))

    vectorizer = model.named_steps["vectorizer"]
    classifier = model.named_steps["classifier"]
    feature_names = vectorizer.get_feature_names_out()
    classes = list(classifier.classes_)
    print("Top words per mood:")
    for index, mood in enumerate(classes):
        top = np.argsort(classifier.feature_log_prob_[index])[-8:][::-1]
        print(f"  {mood:8s}: {', '.join(feature_names[top])}")

    new_reviews = [
        "I loved the acting and the story was beautiful, but the ending felt rushed.",
        "A boring, confusing mess. I kept checking the time.",
        "A delightful film with warm characters and a happy ending.",
    ]
    new_predictions = model.predict(new_reviews)
    new_probabilities = model.predict_proba(new_reviews)
    print("\nNew review predictions:")
    for review, prediction, probability in zip(new_reviews, new_predictions, new_probabilities):
        confidence = probability[classes.index(prediction)]
        print(f"  {prediction:8s} ({confidence:.0%}) -> {review}")

    # ---- Mood meter for one review ------------------------------------
    sample_review = new_reviews[0]
    sample_probabilities = model.predict_proba([sample_review])[0]
    fig, ax = plt.subplots(figsize=(6, 4))
    colours = {"positive": "#27ae60", "negative": "#c0392b", "mixed": "#e67e22"}
    ax.bar(classes, sample_probabilities, color=[colours[c] for c in classes])
    ax.set_ylim(0, 1)
    ax.set_ylabel("probability")
    ax.set_title("Mood meter for: 'I loved the acting... but the ending felt rushed'")
    for i, probability in enumerate(sample_probabilities):
        ax.text(i, probability + 0.02, f"{probability:.0%}", ha="center")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "mood_meter.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---- Confusion matrix ---------------------------------------------
    labels = sorted(df["mood"].unique())
    cm = confusion_matrix(y_test, predictions, labels=labels)
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    ConfusionMatrixDisplay(cm, display_labels=labels).plot(ax=ax, cmap="YlGnBu", colorbar=False)
    ax.set_title("Mood classification results")
    fig.tight_layout()
    fig.savefig(OUT / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "predictions.txt", "w", encoding="utf-8") as handle:
        handle.write(f"accuracy: {accuracy:.4f}\n\n")
        handle.write(classification_report(y_test, predictions, zero_division=0))
        handle.write("\nNew reviews:\n")
        for review, prediction, probability in zip(new_reviews, new_predictions, new_probabilities):
            handle.write(f"{prediction} ({probability[classes.index(prediction)]:.2%}) -> {review}\n")

    print("\nSaved: outputs/mood_meter.png, outputs/confusion_matrix.png, outputs/predictions.txt")
    print("Try this: write a review that is sarcastic and see whether the model understands.")


if __name__ == "__main__":
    main()
