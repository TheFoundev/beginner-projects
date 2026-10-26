"""Project 01: The Snack Sorter (image classification with KNN).

Run:
    python main.py

The script loads 90 tiny snack photos, turns each photo into five simple
numbers (average colour, colour coverage, and shape), trains a K-Nearest
Neighbours classifier, and saves visual results in outputs/.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

FEATURES = ["mean_r", "mean_g", "mean_b", "color_fraction", "aspect_ratio"]


def main() -> None:
    df = pd.read_csv(DATA / "snacks.csv")
    X = df[FEATURES]
    y = df["label"]

    X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
        X, y, df.index, test_size=0.25, random_state=42, stratify=y
    )

    model = Pipeline(
        [
            ("scale", StandardScaler()),
            ("knn", KNeighborsClassifier(n_neighbors=5)),
        ]
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    print("=" * 60)
    print("THE SNACK SORTER")
    print("=" * 60)
    print(f"Training photos: {len(X_train)}")
    print(f"Test photos:     {len(X_test)}")
    print(f"Accuracy:        {accuracy:.1%}")
    print("\nClassification report:\n")
    print(classification_report(y_test, predictions, zero_division=0))

    # ---- Save a contact sheet of training examples ---------------------
    fig, axes = plt.subplots(3, 4, figsize=(8, 6))
    for row, label in enumerate(sorted(df["label"].unique())):
        samples = df[df["label"] == label].head(4)
        for col, (_, sample) in enumerate(samples.iterrows()):
            ax = axes[row, col]
            ax.imshow(mpimg.imread(DATA / sample["image_path"]))
            ax.set_title(label, fontsize=9)
            ax.axis("off")
    fig.suptitle("Example snack photos used for training", fontsize=13)
    fig.tight_layout()
    fig.savefig(OUT / "sample_snacks.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---- Show a few test predictions ----------------------------------
    test_df = df.loc[idx_test].head(9)
    test_pred = model.predict(test_df[FEATURES])
    fig, axes = plt.subplots(3, 3, figsize=(7, 7))
    for ax, (_, row), prediction in zip(axes.ravel(), test_df.iterrows(), test_pred):
        ax.imshow(mpimg.imread(DATA / row["image_path"]))
        ax.set_title(f"true: {row['label']}\npredicted: {prediction}", fontsize=9)
        ax.axis("off")
    fig.suptitle("Test photos: true label vs. model prediction", fontsize=13)
    fig.tight_layout()
    fig.savefig(OUT / "predictions.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---- Confusion matrix ---------------------------------------------
    labels = sorted(df["label"].unique())
    cm = confusion_matrix(y_test, predictions, labels=labels)
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    ConfusionMatrixDisplay(cm, display_labels=labels).plot(ax=ax, cmap="Greens", colorbar=False)
    ax.set_title("Which snacks did the AI confuse?")
    fig.tight_layout()
    fig.savefig(OUT / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---- Text summary --------------------------------------------------
    with open(OUT / "metrics.txt", "w", encoding="utf-8") as handle:
        handle.write(f"accuracy: {accuracy:.4f}\n\n")
        handle.write(classification_report(y_test, predictions, zero_division=0))

    print("\nSaved:")
    for name in ("sample_snacks.png", "predictions.png", "confusion_matrix.png", "metrics.txt"):
        print(f"  outputs/{name}")
    print("\nTry this: add a fourth snack photo class and rerun the script.")


if __name__ == "__main__":
    main()
