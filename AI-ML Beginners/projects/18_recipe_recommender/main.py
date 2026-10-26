"""Project 18: The Recipe Recommender (K-Nearest Neighbours).

Run:
    python main.py

Recipes are points in a five-dimensional flavour space.  The recommender
finds the closest points and suggests them, with a "surprise me" option for
a different cuisine.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

FEATURES = ["spice", "sweet", "savory", "sour", "veggie"]


def main() -> None:
    df = pd.read_csv(DATA / "recipes.csv")
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[FEATURES])
    model = NearestNeighbors(n_neighbors=6, metric="euclidean")
    model.fit(scaled_features)

    def recommend(recipe_name: str, n: int = 3) -> pd.DataFrame:
        matches = df.index[df["name"].str.lower() == recipe_name.lower()]
        if len(matches) == 0:
            raise ValueError(f"Recipe not found: {recipe_name}")
        index = int(matches[0])
        distances, indices = model.kneighbors(scaled_features[index].reshape(1, -1), n_neighbors=n + 1)
        rows = []
        for distance, neighbor in zip(distances[0][1:], indices[0][1:]):
            rows.append(
                {
                    "name": df.loc[neighbor, "name"],
                    "cuisine": df.loc[neighbor, "cuisine"],
                    "similarity": 1 / (1 + distance),
                }
            )
        return pd.DataFrame(rows)

    def surprise_me(recipe_name: str) -> pd.Series:
        matches = df.index[df["name"].str.lower() == recipe_name.lower()]
        if len(matches) == 0:
            raise ValueError(f"Recipe not found: {recipe_name}")
        base = df.loc[int(matches[0])]
        different = df[df["cuisine"] != base["cuisine"]]
        return different.sample(1, random_state=7).iloc[0]

    print("=" * 60)
    print("THE RECIPE RECOMMENDER")
    print("=" * 60)
    for recipe in ("Margherita Pizza", "Spicy Ramen", "Chocolate Cake"):
        recommendations = recommend(recipe, n=3)
        print(f"\nIf you like {recipe}, try:")
        for row in recommendations.itertuples():
            print(f"  {row.name:22s} ({row.cuisine:14s}) similarity {row.similarity:.2f}")

    surprise = surprise_me("Margherita Pizza")
    print(f"\nSurprise me: {surprise['name']} ({surprise['cuisine']})")

    # ---- Similarity chart ---------------------------------------------
    base_recipe = "Spicy Ramen"
    recommendations = recommend(base_recipe, n=5)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(recommendations["name"][::-1], recommendations["similarity"][::-1], color="#e67e22")
    ax.set_xlim(0, 1)
    ax.set_xlabel("similarity score (higher is closer)")
    ax.set_title(f"Recipes most similar to {base_recipe}")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "similarity_scores.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    with open(OUT / "recommendations.txt", "w", encoding="utf-8") as handle:
        for recipe in ("Margherita Pizza", "Spicy Ramen", "Chocolate Cake"):
            handle.write(f"If you like {recipe}, try:\n")
            for row in recommend(recipe, n=3).itertuples():
                handle.write(f"  {row.name} ({row.cuisine}), similarity {row.similarity:.3f}\n")
            handle.write("\n")
        handle.write(f"Surprise me: {surprise['name']} ({surprise['cuisine']})\n")

    print("\nSaved: outputs/similarity_scores.png, outputs/recommendations.txt")
    print("Try this: add 10 recipes you actually like and rerun the recommendations.")


if __name__ == "__main__":
    main()
