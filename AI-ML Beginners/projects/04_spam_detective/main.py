"""Project 04: Spam Detective (Naive Bayes text classification).

Run:
    python main.py

The model learns which words are common in spam and which are common in
normal messages, then classifies new messages.
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
    df = pd.read_csv(DATA / "messages.csv")
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["label"], test_size=0.25, random_state=42, stratify=df["label"]
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
    print("SPAM DETECTIVE")
    print("=" * 60)
    print(f"Accuracy: {accuracy:.1%}\n")
    print(classification_report(y_test, predictions, zero_division=0))

    classes = list(model.named_steps["classifier"].classes_)
    spam_index = classes.index("spam")
    spam_words = top_words(model, spam_index)
    ham_words = top_words(model, 1 - spam_index)
    print("Top spam clues:", ", ".join(spam_words))
    print("Top normal clues:", ", ".join(ham_words))

    # ---- Test a few new messages --------------------------------------
    new_messages = [
        "Congratulations! You won a free smartphone. Click now to claim your prize.",
        "Can we meet at the library at 4 pm to review the project?",
        "URGENT: verify your password immediately or your account will be suspended.",
        "Thanks for sending the notes. I will read them tonight.",
    ]
    new_predictions = model.predict(new_messages)
    probabilities = model.predict_proba(new_messages)
    print("\nNew message predictions:")
    for message, prediction, probability in zip(new_messages, new_predictions, probabilities):
        confidence = probability[classes.index(prediction)]
        print(f"  {prediction:4s} ({confidence:.0%}) -> {message}")

    # ---- Top-word chart ------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, words, title, colour in (
        (axes[0], spam_words, "Words that suggest spam", "#c0392b"),
        (axes[1], ham_words, "Words that suggest a normal message", "#2471a3"),
    ):
        ax.barh(words[::-1], range(1, len(words) + 1), color=colour)
        ax.set_title(title)
        ax.set_xlabel("relative clue strength")
        ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "top_words.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---- Confusion matrix ---------------------------------------------
    labels = ["ham", "spam"]
    cm = confusion_matrix(y_test, predictions, labels=labels)
    fig, ax = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay(cm, display_labels=labels).plot(ax=ax, cmap="Reds", colorbar=False)
    ax.set_title("Spam filter mistakes")
    fig.tight_layout()
    fig.savefig(OUT / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "predictions.txt", "w", encoding="utf-8") as handle:
        handle.write(f"accuracy: {accuracy:.4f}\n\n")
        handle.write(classification_report(y_test, predictions, zero_division=0))
        handle.write("\nNew messages:\n")
        for message, prediction, probability in zip(new_messages, new_predictions, probabilities):
            handle.write(f"{prediction} ({probability[classes.index(prediction)]:.2%}) -> {message}\n")

    print("\nSaved: outputs/top_words.png, outputs/confusion_matrix.png, outputs/predictions.txt")
    print("Try this: add five of your own spam and normal messages, then retrain.")


if __name__ == "__main__":
    main()
