"""Project 03: The Titanic Survival Oracle (decision tree).

Run:
    python main.py

A small practice dataset inspired by the Titanic.  The decision tree learns
simple yes/no rules and prints them so you can read the model's logic.
"""

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


def main() -> None:
    df = pd.read_csv(DATA / "titanic_practice.csv")
    df["is_female"] = (df["sex"] == "female").astype(int)

    features = ["pclass", "is_female", "age", "fare"]
    X = df[features]
    y = df["survived"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = DecisionTreeClassifier(max_depth=4, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    print("=" * 60)
    print("THE TITANIC SURVIVAL ORACLE")
    print("=" * 60)
    print(f"Accuracy: {accuracy:.1%}\n")
    print("Learned rules:\n")
    print(
        export_text(
            model,
            feature_names=["passenger class", "is female (1=yes)", "age", "fare"],
        )
    )
    print(classification_report(y_test, predictions, zero_division=0))

    # A made-up passenger: third class, female, age 25, fare 10.
    new_passenger = pd.DataFrame(
        [{"pclass": 3, "is_female": 1, "age": 25, "fare": 10.0}]
    )
    probability = model.predict_proba(new_passenger)[0, 1]
    print(f"Made-up passenger survival probability: {probability:.1%}")

    # ---- Draw the tree -------------------------------------------------
    fig, ax = plt.subplots(figsize=(13, 7))
    plot_tree(
        model,
        feature_names=["passenger class", "is female", "age", "fare"],
        class_names=["did not survive", "survived"],
        filled=True,
        rounded=True,
        fontsize=9,
        ax=ax,
    )
    ax.set_title("A decision tree you can read from top to bottom")
    fig.tight_layout()
    fig.savefig(OUT / "titanic_tree.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---- Confusion matrix ---------------------------------------------
    cm = confusion_matrix(y_test, predictions, labels=[0, 1])
    fig, ax = plt.subplots(figsize=(5.2, 4.3))
    ConfusionMatrixDisplay(cm, display_labels=["did not survive", "survived"]).plot(
        ax=ax, cmap="Blues", colorbar=False
    )
    ax.set_title("Titanic predictions on unseen passengers")
    fig.tight_layout()
    fig.savefig(OUT / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "rules.txt", "w", encoding="utf-8") as handle:
        handle.write(export_text(model, feature_names=features))
        handle.write(f"\naccuracy: {accuracy:.4f}\n")
        handle.write(f"made-up passenger survival probability: {probability:.4f}\n")

    print("\nSaved: outputs/titanic_tree.png, outputs/confusion_matrix.png, outputs/rules.txt")
    print("Try this: change max_depth to 2 or 5 and compare the rules.")


if __name__ == "__main__":
    main()
