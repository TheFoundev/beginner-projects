"""Project 15: The Pumpkin Seed Sorter (decision tree).

Run:
    python main.py

A multi-class decision tree.  The script compares a shallow tree, a deeper
tree, and an unlimited tree, then prints the rules in plain English.
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

FEATURES = ["area", "perimeter", "major_axis", "minor_axis", "eccentricity"]


def main() -> None:
    df = pd.read_csv(DATA / "pumpkin_seeds.csv")
    X = df[FEATURES]
    y = df["variety"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    print("=" * 60)
    print("THE PUMPKIN SEED SORTER")
    print("=" * 60)
    print("Comparing tree depths:\n")
    models = {}
    for depth in (2, 4, None):
        model = DecisionTreeClassifier(max_depth=depth, random_state=42)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        models[depth] = (model, predictions, accuracy)
        label = "unlimited" if depth is None else str(depth)
        print(f"  max_depth={label:9s} accuracy={accuracy:.1%}")

    best_depth = max(models, key=lambda depth: models[depth][2])
    model, predictions, accuracy = models[best_depth]
    print(f"\nBest tree: max_depth={best_depth}")
    print("\nLearned rules for the best tree:\n")
    print(export_text(model, feature_names=FEATURES))
    print(classification_report(y_test, predictions, zero_division=0))

    new_seed = pd.DataFrame(
        [{"area": 1180, "perimeter": 55.0, "major_axis": 12.2, "minor_axis": 5.7, "eccentricity": 0.86}]
    )
    new_variety = model.predict(new_seed)[0]
    print(f"New seed -> {new_variety}")

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
    ax.set_title("Pumpkin seed decision tree")
    fig.tight_layout()
    fig.savefig(OUT / "pumpkin_tree.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---- Confusion matrix ---------------------------------------------
    labels = sorted(df["variety"].unique())
    cm = confusion_matrix(y_test, predictions, labels=labels)
    fig, ax = plt.subplots(figsize=(6, 4.6))
    ConfusionMatrixDisplay(cm, display_labels=labels).plot(ax=ax, cmap="YlOrBr", colorbar=False)
    ax.set_title("Pumpkin seed classification")
    fig.tight_layout()
    fig.savefig(OUT / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "rules.txt", "w", encoding="utf-8") as handle:
        for depth, (_, _, acc) in models.items():
            handle.write(f"depth={depth}: accuracy={acc:.4f}\n")
        handle.write(f"\nbest depth: {best_depth}\n\n")
        handle.write(export_text(model, feature_names=FEATURES))
        handle.write(f"\nnew seed prediction: {new_variety}\n")
        handle.write("\n" + classification_report(y_test, predictions, zero_division=0))

    print("\nSaved: outputs/pumpkin_tree.png, outputs/confusion_matrix.png, outputs/rules.txt")
    print("Try this: add a new seed variety to the CSV and retrain.")


if __name__ == "__main__":
    main()
