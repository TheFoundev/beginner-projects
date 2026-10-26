"""Project 20: The Study Buddy Planner (decision tree).

Run:
    python main.py              # scripted demo
    python main.py --interactive # answer four questions

A tiny recommendation system.  The decision tree learns rules for choosing a
study strategy, and the rules are printed so you can question them.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

FEATURES = ["hours_left", "difficulty", "energy", "distraction"]
QUESTIONS = [
    ("How many hours do you have left? (1-10) ", "hours_left", 1, 10),
    ("How difficult is the subject? (1-5) ", "difficulty", 1, 5),
    ("How much energy do you have? (1-5) ", "energy", 1, 5),
    ("How distracted do you feel? (1-5) ", "distraction", 1, 5),
]


def ask_situation() -> pd.DataFrame:
    values = {}
    for question, key, low, high in QUESTIONS:
        while True:
            raw = input(question).strip()
            try:
                value = int(raw)
            except ValueError:
                print(f"Please enter a whole number from {low} to {high}.")
                continue
            if low <= value <= high:
                values[key] = value
                break
            print(f"Please enter a number from {low} to {high}.")
    return pd.DataFrame([values])


def main() -> None:
    df = pd.read_csv(DATA / "study_situations.csv")
    X = df[FEATURES]
    y = df["strategy"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = DecisionTreeClassifier(max_depth=4, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print("=" * 60)
    print("THE STUDY BUDDY PLANNER")
    print("=" * 60)
    print(f"Accuracy: {accuracy:.1%}\n")
    print(classification_report(y_test, predictions, zero_division=0))
    print("Learned rules:\n")
    print(export_text(model, feature_names=FEATURES))

    demo_situations = pd.DataFrame(
        [
            {"hours_left": 2, "difficulty": 4, "energy": 3, "distraction": 2},
            {"hours_left": 6, "difficulty": 5, "energy": 4, "distraction": 1},
            {"hours_left": 4, "difficulty": 3, "energy": 1, "distraction": 2},
            {"hours_left": 8, "difficulty": 2, "energy": 4, "distraction": 5},
        ]
    )
    demo_predictions = model.predict(demo_situations)
    print("Demo plans:")
    for situation, plan in zip(demo_situations.to_dict("records"), demo_predictions):
        print(f"  {situation} -> {plan}")

    # ---- Draw the tree -------------------------------------------------
    fig, ax = plt.subplots(figsize=(16, 8))
    plot_tree(
        model,
        feature_names=FEATURES,
        class_names=list(model.classes_),
        filled=True,
        rounded=True,
        fontsize=8,
        ax=ax,
    )
    ax.set_title("The Study Buddy decision tree")
    fig.tight_layout()
    fig.savefig(OUT / "study_tree.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---- Confusion matrix ---------------------------------------------
    labels = sorted(df["strategy"].unique())
    cm = confusion_matrix(y_test, predictions, labels=labels)
    fig, ax = plt.subplots(figsize=(7, 5.5))
    ConfusionMatrixDisplay(cm, display_labels=labels).plot(ax=ax, cmap="Purples", colorbar=False)
    ax.set_title("Study strategy predictions")
    fig.tight_layout()
    fig.savefig(OUT / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "rules.txt", "w", encoding="utf-8") as handle:
        handle.write(f"accuracy: {accuracy:.4f}\n\n")
        handle.write(export_text(model, feature_names=FEATURES))
        handle.write("\ndemo plans:\n")
        for situation, plan in zip(demo_situations.to_dict("records"), demo_predictions):
            handle.write(f"{situation} -> {plan}\n")
        handle.write("\n" + classification_report(y_test, predictions, zero_division=0))

    print("\nSaved: outputs/study_tree.png, outputs/confusion_matrix.png, outputs/rules.txt")

    if "--interactive" in sys.argv:
        print("\nAnswer four questions and the planner will suggest a strategy.\n")
        situation = ask_situation()
        plan = model.predict(situation)[0]
        print(f"\nSuggested strategy: {plan}")
    else:
        print("Run `python main.py --interactive` to get a personal plan.")
        print("Try this: add a 'deadline soon' feature and retrain.")


if __name__ == "__main__":
    main()
