"""Project 13: The Penguin Detective (K-Nearest Neighbours).

Run:
    python main.py

Classify a penguin's species from four body measurements.  The script
compares k=3 and k=5 so you can see that a hyperparameter changes the answer.
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

FEATURES = ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
COLOURS = {"Adelie": "#2471a3", "Gentoo": "#c0392b", "Chinstrap": "#16a085"}


def main() -> None:
    df = pd.read_csv(DATA / "penguins.csv")
    X = df[FEATURES]
    y = df["species"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    results = {}
    for k in (3, 5):
        model = Pipeline(
            [
                ("scale", StandardScaler()),
                ("knn", KNeighborsClassifier(n_neighbors=k)),
            ]
        )
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        results[k] = (model, predictions, accuracy_score(y_test, predictions))

    print("=" * 60)
    print("THE PENGUIN DETECTIVE")
    print("=" * 60)
    for k, (_, _, accuracy) in results.items():
        print(f"k={k}: accuracy {accuracy:.1%}")

    best_k = max(results, key=lambda k: results[k][2])
    best_model, best_predictions, best_accuracy = results[best_k]
    print(f"\nBest k: {best_k}\n")
    print(classification_report(y_test, best_predictions, zero_division=0))

    new_penguin = pd.DataFrame(
        [
            {
                "bill_length_mm": 39.0,
                "bill_depth_mm": 18.0,
                "flipper_length_mm": 190,
                "body_mass_g": 3700,
            }
        ]
    )
    new_species = best_model.predict(new_penguin)[0]
    new_confidence = best_model.predict_proba(new_penguin).max()
    print(f"New penguin -> {new_species} ({new_confidence:.0%} confident)")

    # ---- Scatter plot --------------------------------------------------
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    for species, group in df.groupby("species"):
        ax.scatter(
            group["bill_length_mm"],
            group["flipper_length_mm"],
            s=45,
            alpha=0.8,
            label=species,
            color=COLOURS[species],
        )
    ax.scatter(
        new_penguin["bill_length_mm"],
        new_penguin["flipper_length_mm"],
        marker="*",
        s=280,
        color="#111111",
        label=f"new -> {new_species}",
        zorder=5,
    )
    ax.set_xlabel("Bill length (mm)")
    ax.set_ylabel("Flipper length (mm)")
    ax.set_title("Penguin species form clusters")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "penguin_scatter.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---- Confusion matrix ---------------------------------------------
    labels = sorted(df["species"].unique())
    cm = confusion_matrix(y_test, best_predictions, labels=labels)
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    ConfusionMatrixDisplay(cm, display_labels=labels).plot(ax=ax, cmap="Blues", colorbar=False)
    ax.set_title(f"Penguin predictions (k={best_k})")
    fig.tight_layout()
    fig.savefig(OUT / "confusion_matrix.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "metrics.txt", "w", encoding="utf-8") as handle:
        for k, (_, _, accuracy) in results.items():
            handle.write(f"k={k}: accuracy {accuracy:.4f}\n")
        handle.write(f"\nbest k: {best_k}\n")
        handle.write(f"new penguin: {new_species} ({new_confidence:.4f})\n\n")
        handle.write(classification_report(y_test, best_predictions, zero_division=0))

    print("\nSaved: outputs/penguin_scatter.png, outputs/confusion_matrix.png, outputs/metrics.txt")
    print("Try this: remove body_mass_g and see whether accuracy changes.")


if __name__ == "__main__":
    main()
