"""Project 19 - The Product Recommendation Engine.

Goal: use purchase history and cosine similarity to recommend related products
and personalised products for a customer.

Run from the pack root:
    python3 projects/19_recommendation/main.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")


def main() -> None:
    print("=" * 70)
    print("PROJECT 19 - THE PRODUCT RECOMMENDATION ENGINE")
    print("=" * 70)

    # STEP 1 - Load the transaction lines.
    # Each row means: this customer bought this product in this transaction.
    df = pd.read_csv(DATA / "transactions.csv")
    print(f"\nSTEP 1: loaded {len(df)} transaction lines")
    print(df.head(5).to_string(index=False))

    # STEP 2 - Check the data.
    print("\nSTEP 2: quality check")
    print("Missing values:", int(df.isna().sum().sum()))
    print(f"Customers: {df['customer_id'].nunique()}")
    print(f"Products: {df['product'].nunique()}")
    print(f"Transactions: {df['transaction_id'].nunique()}")

    # STEP 3 - Count how often each product was purchased.
    product_counts = df["product"].value_counts().rename_axis("product").reset_index(name="purchases")
    product_counts.to_csv(OUT / "product_counts.csv", index=False)
    print("\nSTEP 3: top products")
    print(product_counts.head(8).to_string(index=False))

    # STEP 4 - Build a product-by-customer matrix.
    # Rows are products, columns are customers, and each cell counts purchases.
    # This matrix lets us compare products by the customers who bought them.
    product_matrix = df.pivot_table(
        index="product",
        columns="customer_id",
        values="transaction_id",
        aggfunc="count",
        fill_value=0,
    )
    print(f"\nSTEP 4: product matrix shape = {product_matrix.shape}")

    # STEP 5 - Calculate cosine similarity between products.
    # Cosine similarity compares the angle between two purchase vectors.
    # 1.0 means two products are bought by very similar customers; 0 means no overlap.
    similarity = cosine_similarity(product_matrix)
    sim_df = pd.DataFrame(similarity, index=product_matrix.index, columns=product_matrix.index)
    sim_df.round(3).to_csv(OUT / "product_similarity.csv")
    print("\nSTEP 5: similarity matrix created")

    # STEP 6 - Recommend products similar to a chosen product.
    def similar_products(product: str, n: int = 5) -> pd.Series:
        scores = sim_df.loc[product].drop(product).sort_values(ascending=False)
        return scores.head(n)

    example_product = "Laptop"
    print(f"\nSTEP 6: products similar to {example_product}")
    print(similar_products(example_product).round(3).to_string())

    # STEP 7 - Build a customer-by-product matrix.
    customer_matrix = df.pivot_table(
        index="customer_id",
        columns="product",
        values="transaction_id",
        aggfunc="count",
        fill_value=0,
    )

    # STEP 8 - Recommend products for a customer.
    # For every product the customer has not bought, add up its similarity to
    # the products they did buy. Higher total score = stronger recommendation.
    def recommend_for_customer(customer_id: int, n: int = 5) -> pd.Series:
        owned = customer_matrix.loc[customer_id]
        owned_products = owned[owned > 0].index
        scores = pd.Series(0.0, index=sim_df.index)
        for product in owned_products:
            scores += sim_df[product] * owned[product]
        scores = scores.drop(labels=owned_products, errors="ignore")
        # Cold-start fallback: if every unseen product has zero similarity
        # (for example, the customer already owns their whole product cluster),
        # fall back to the most popular products instead of showing all zeros.
        if scores.empty or scores.max() <= 0:
            scores = (
                product_counts.set_index("product")["purchases"]
                .reindex(scores.index)
                .fillna(0)
                .astype(float)
            )
        return scores.sort_values(ascending=False).head(n)

    print("\nSTEP 8: recommendations for customer 1")
    print(recommend_for_customer(1).round(3).to_string())

    # STEP 9 - Save recommendations for the first 20 customers.
    rows = []
    for customer_id in customer_matrix.index[:20]:
        for rank, (product, score) in enumerate(recommend_for_customer(int(customer_id)).items(), start=1):
            rows.append(
                {
                    "customer_id": int(customer_id),
                    "rank": rank,
                    "recommended_product": product,
                    "score": round(float(score), 3),
                }
            )
    recommendations = pd.DataFrame(rows)
    recommendations.to_csv(OUT / "customer_recommendations.csv", index=False)
    print("\nSTEP 9: saved recommendations for 20 customers")

    # STEP 10 - Plot the most purchased products.
    fig, ax = plt.subplots(figsize=(8, 5))
    top = product_counts.head(10).sort_values("purchases")
    ax.barh(top["product"], top["purchases"], color="#1b9e77")
    ax.set_title("Top 10 most purchased products")
    ax.set_xlabel("Purchase lines")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(OUT / "top_products.png", dpi=140)
    plt.close(fig)

    # STEP 11 - Plot the product similarity heatmap.
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(sim_df, cmap="YlGnBu", linewidths=0.2, ax=ax)
    ax.set_title("Product-to-product cosine similarity")
    ax.set_xlabel("Product")
    ax.set_ylabel("Product")
    plt.xticks(rotation=60, ha="right", fontsize=8)
    plt.yticks(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "similarity_heatmap.png", dpi=140)
    plt.close(fig)

    # STEP 12 - Write the explanation and example output.
    results = [
        "RECOMMENDATION ENGINE RESULTS",
        "=" * 60,
        f"Customers: {df['customer_id'].nunique()}",
        f"Products: {df['product'].nunique()}",
        f"Transactions: {df['transaction_id'].nunique()}",
        "",
        f"Products similar to {example_product}:",
        similar_products(example_product).round(3).to_string(),
        "",
        "Recommendations for customer 1:",
        recommend_for_customer(1).round(3).to_string(),
        "",
        "How it works:",
        "1. Count how often each customer bought each product.",
        "2. Compare product purchase vectors with cosine similarity.",
        "3. For a customer, score each unseen product by summing similarities",
        "   to the products they already bought.",
        "4. Show the highest-scoring unseen products.",
        "",
        "Limitation: this is a popularity/similarity baseline. It does not use",
        "ratings, prices, or whether a recommendation was actually clicked.",
    ]
    (OUT / "results.txt").write_text("\n".join(results), encoding="utf-8")
    print("\n" + "\n".join(results))
    print("\nDONE. Check outputs for recommendations and similarity charts.")


if __name__ == "__main__":
    main()
