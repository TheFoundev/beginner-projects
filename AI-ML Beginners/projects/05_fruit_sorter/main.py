"""Project 05: The Fruit Basket Sorter (K-Nearest Neighbours).

Run:
    python main.py

Fruits are described by sweetness, weight, size, and colour.  The model
classifies a mystery fruit by finding the most similar training examples.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
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

FEATURES = ["sweetness", "weight_g", "size_cm", "color_score"]
COLOURS = {"apple": "#c0392b", "banana": "#f1c40f", "orange": "#e67e22"}


def main() -> None:
    df = pd.read_csv(DATA / "fruits.csv")
    X = df[FEATURES]
    y = df["fruit"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
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
    print("THE FRUIT BASKET SORTER")
    print("=" * 60)
    print(f"Accuracy: {accuracy:.1%}\n")
    print(classification_report(y_test, predictions, zero_division=0))

    mystery = pd.DataFrame(
        [
            {
                "sweetness": 7.2,
                "weight_g": 170,
                "size_cm": 8.5,
                "color_score": 8.0,
            }
        ]
    )
    mystery_prediction = model.predict(mystery)[0]
    mystery_probability = model.predict_proba(mystery).max()
    print(f"Mystery fruit -> {mystery_prediction} ({mystery_probability:.0%} confident)")

    # ---- Scatter plot --------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    for fruit, group in df.groupby("fruit"):
        ax.scatter(
            group["sweetness"],
            group["weight_g"],
            s=60,
            alpha=0.8,
            label=fruit,
            color=COLOURS[fruit],
        )
    ax.scatter(
        mystery["sweetness"],
        mystery["weight_g"],
        marker="*",
        s=260,
        color="#111111",
        label=f"mystery -> {mystery_prediction}",
        zorder=5,
    )
    ax.set_xlabel("Sweetness score")
    ax.set_ylabel("Weight (g)")
    ax.set_title("Similar fruits form groups")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "fruit_scatter.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---- Confusion matrix ---------------------------------------------
    labels = sorted(df["fruit"].unique())
    cm = confusion_matrix(y_test, predictions, labels=labels)
    fig, ax = plt.subplots(figsize=(5, 4.2))
    ConfusionMatrixDisplay(cm, display_labels=labels).plot(ax=ax, cmap="Oranges", colorbar=False)
    ax.set_title("Fruit classification results")
    fig.tight_layout()
    fig.savefig(OUT / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "metrics.txt", "w", encoding="utf-8") as handle:
        handle.write(f"accuracy: {accuracy:.4f}\n")
        handle.write(f"mystery prediction: {mystery_prediction} ({mystery_probability:.4f})\n\n")
        handle.write(classification_report(y_test, predictions, zero_division=0))

    print("\nSaved: outputs/fruit_scatter.png, outputs/confusion_matrix.png, outputs/metrics.txt")
    print("Try this: change n_neighbors from 5 to 1 or 9 and compare.")


if __name__ == "__main__":
    main()
