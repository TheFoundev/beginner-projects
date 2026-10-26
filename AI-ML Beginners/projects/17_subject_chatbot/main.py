"""Project 17: The Chatbot That Guesses Your Favorite Subject.

Run:
    python main.py              # scripted demo
    python main.py --interactive # answer the questions yourself

A tiny decision-tree chatbot.  The tree is trained on example answer
profiles and then converted into a readable flowchart.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

FEATURES = [
    "likes_numbers",
    "likes_living_things",
    "likes_stories",
    "enjoys_experiments",
    "enjoys_debate",
    "likes_programming",
]
QUESTIONS = [
    "Do you enjoy working with numbers?",
    "Do you like learning about living things?",
    "Do you enjoy stories and writing?",
    "Do you like running experiments?",
    "Do you enjoy debating ideas?",
    "Do you like programming?",
]


def ask_profile() -> pd.DataFrame:
    answers = []
    for question in QUESTIONS:
        while True:
            answer = input(f"{question} (y/n): ").strip().lower()
            if answer in ("y", "yes", "1"):
                answers.append(1)
                break
            if answer in ("n", "no", "0"):
                answers.append(0)
                break
            print("Please type y or n.")
    return pd.DataFrame([dict(zip(FEATURES, answers))])


def main() -> None:
    df = pd.read_csv(DATA / "subject_answers.csv")
    X = df[FEATURES]
    y = df["subject"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = DecisionTreeClassifier(max_depth=4, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print("=" * 60)
    print("THE FAVORITE-SUBJECT CHATBOT")
    print("=" * 60)
    print(f"Accuracy: {accuracy:.1%}\n")
    print(classification_report(y_test, predictions, zero_division=0))
    print("Learned question path:\n")
    print(export_text(model, feature_names=FEATURES))

    demo_profiles = pd.DataFrame(
        [
            {"likes_numbers": 1, "likes_living_things": 0, "likes_stories": 0, "enjoys_experiments": 1, "enjoys_debate": 0, "likes_programming": 1},
            {"likes_numbers": 0, "likes_living_things": 1, "likes_stories": 0, "enjoys_experiments": 1, "enjoys_debate": 0, "likes_programming": 0},
            {"likes_numbers": 0, "likes_living_things": 0, "likes_stories": 1, "enjoys_experiments": 0, "enjoys_debate": 1, "likes_programming": 0},
        ]
    )
    demo_predictions = model.predict(demo_profiles)
    print("Demo profiles:")
    for index, prediction in enumerate(demo_predictions, start=1):
        print(f"  Student {index}: {prediction}")

    # ---- Draw the tree -------------------------------------------------
    fig, ax = plt.subplots(figsize=(15, 8))
    plot_tree(
        model,
        feature_names=FEATURES,
        class_names=list(model.classes_),
        filled=True,
        rounded=True,
        fontsize=8,
        ax=ax,
    )
    ax.set_title("The chatbot's decision tree")
    fig.tight_layout()
    fig.savefig(OUT / "chatbot_tree.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "rules.txt", "w", encoding="utf-8") as handle:
        handle.write(f"accuracy: {accuracy:.4f}\n\n")
        handle.write(export_text(model, feature_names=FEATURES))
        handle.write("\ndemo predictions:\n")
        for index, prediction in enumerate(demo_predictions, start=1):
            handle.write(f"student {index}: {prediction}\n")
        handle.write("\n" + classification_report(y_test, predictions, zero_division=0))

    print("\nSaved: outputs/chatbot_tree.png, outputs/rules.txt")

    if "--interactive" in sys.argv:
        print("\nAnswer six questions and the chatbot will guess your subject.\n")
        profile = ask_profile()
        prediction = model.predict(profile)[0]
        probabilities = model.predict_proba(profile)[0]
        confidence = probabilities.max()
        print(f"\nThe chatbot guesses: {prediction} ({confidence:.0%} confident)")
    else:
        print("Run `python main.py --interactive` to chat with it yourself.")
        print("Try this: add a new subject and 20 example profiles.")


if __name__ == "__main__":
    main()
