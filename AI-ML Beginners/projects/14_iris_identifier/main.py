"""Project 14: The Iris Flower Identifier (decision tree).

Run:
    python main.py

The classic 150-row Iris dataset.  The decision tree is drawn as a flowchart
so every prediction can be traced back to a readable rule.
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

FEATURES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]


def main() -> None:
    df = pd.read_csv(DATA / "iris.csv")
    X = df[FEATURES]
    y = df["species"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    print("=" * 60)
    print("THE IRIS FLOWER IDENTIFIER")
    print("=" * 60)
    print("Comparing tree depths:\n")
    models = {}
    for depth in (2, 3, None):
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

    new_flower = pd.DataFrame(
        [{"sepal_length": 5.8, "sepal_width": 2.7, "petal_length": 4.1, "petal_width": 1.0}]
    )
    new_species = model.predict(new_flower)[0]
    print(f"New flower -> {new_species}")

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
    ax.set_title("Iris decision tree")
    fig.tight_layout()
    fig.savefig(OUT / "iris_tree.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---- Confusion matrix ---------------------------------------------
    labels = sorted(df["species"].unique())
    cm = confusion_matrix(y_test, predictions, labels=labels)
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    ConfusionMatrixDisplay(cm, display_labels=labels).plot(ax=ax, cmap="Greens", colorbar=False)
    ax.set_title("Iris classification results")
    fig.tight_layout()
    fig.savefig(OUT / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "rules.txt", "w", encoding="utf-8") as handle:
        for depth, (_, _, acc) in models.items():
            handle.write(f"depth={depth}: accuracy={acc:.4f}\n")
        handle.write(f"\nbest depth: {best_depth}\n\n")
        handle.write(export_text(model, feature_names=FEATURES))
        handle.write(f"\nnew flower prediction: {new_species}\n")
        handle.write("\n" + classification_report(y_test, predictions, zero_division=0))

    print("\nSaved: outputs/iris_tree.png, outputs/confusion_matrix.png, outputs/rules.txt")
    print("Try this: set max_depth=2 and compare the simpler tree with the deeper one.")


if __name__ == "__main__":
    main()
