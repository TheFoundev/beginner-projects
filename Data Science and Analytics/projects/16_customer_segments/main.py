"""Project 16 - The Customer Segmentation Studio.

Goal: use RFM (recency, frequency, monetary value) and K-Means clustering to
group customers into useful segments.

Run from the pack root:
    python3 projects/16_customer_segments/main.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")


def main() -> None:
    print("=" * 70)
    print("PROJECT 16 - THE CUSTOMER SEGMENTATION STUDIO")
    print("=" * 70)

    # STEP 1 - Load the customer table.
    df = pd.read_csv(DATA / "customers.csv")
    print(f"\nSTEP 1: loaded {len(df)} customers")
    print(df.head(3).to_string(index=False))

    # STEP 2 - Check the three RFM columns.
    # Recency: days since last purchase (lower is better).
    # Frequency: number of purchases (higher is better).
    # Monetary: total spend (higher is better).
    print("\nSTEP 2: RFM quality check")
    print("Missing values:", int(df.isna().sum().sum()))
    print(df[["recency_days", "frequency", "monetary"]].describe().round(2).to_string())

    # STEP 3 - Scale the RFM columns.
    # K-Means uses distance, so a column measured in dollars must not dominate
    # a column measured in small counts. StandardScaler puts each on a similar scale.
    features = ["recency_days", "frequency", "monetary"]
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[features])
    print("\nSTEP 3: standardised RFM features")

    # STEP 4 - Use the elbow method to choose a sensible number of clusters.
    # Inertia is the total distance from points to their cluster centre.
    # We look for the point where adding more clusters stops helping much.
    inertias = []
    k_values = list(range(2, 9))
    for k in k_values:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(scaled)
        inertias.append(model.inertia_)
    elbow = pd.DataFrame({"k": k_values, "inertia": inertias})
    elbow.to_csv(OUT / "elbow_values.csv", index=False)
    print("\nSTEP 4: elbow values")
    print(elbow.round(1).to_string(index=False))

    # STEP 5 - Fit the final K-Means model with four segments.
    k = 4
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    df["cluster"] = model.fit_predict(scaled)
    silhouette = silhouette_score(scaled, df["cluster"])
    print(f"\nSTEP 5: fitted {k} clusters; silhouette score = {silhouette:.3f}")

    # STEP 6 - Profile each cluster.
    profiles = (
        df.groupby("cluster")
        .agg(
            customers=("customer_id", "count"),
            avg_recency_days=("recency_days", "mean"),
            avg_frequency=("frequency", "mean"),
            avg_monetary=("monetary", "mean"),
        )
        .round(1)
    )

    # STEP 7 - Give each cluster a plain-English name.
    # Lower recency is better, so recency is ranked ascending; frequency and
    # monetary are ranked descending. The combined rank orders the segments.
    ranked = profiles.assign(
        recency_rank=profiles["avg_recency_days"].rank(ascending=True),
        frequency_rank=profiles["avg_frequency"].rank(ascending=False),
        monetary_rank=profiles["avg_monetary"].rank(ascending=False),
    )
    ranked["score"] = ranked["recency_rank"] + ranked["frequency_rank"] + ranked["monetary_rank"]
    ordered_clusters = ranked.sort_values("score").index.tolist()
    segment_names = ["High-value loyal", "Promising", "Occasional", "At risk / dormant"]
    name_map = dict(zip(ordered_clusters, segment_names))
    df["segment_name"] = df["cluster"].map(name_map)
    profiles["segment_name"] = profiles.index.map(name_map)
    profiles = profiles.set_index("segment_name")
    profiles.to_csv(OUT / "segment_profiles.csv")
    print("\nSTEP 6-7: segment profiles")
    print(profiles.to_string())

    # STEP 8 - Save the labelled customer table.
    out_cols = [
        "customer_id", "recency_days", "frequency", "monetary", "signup_days_ago",
        "channel", "cluster", "segment_name",
    ]
    df[out_cols].to_csv(DATA / "customers_with_segments.csv", index=False)
    print(f"\nSTEP 8: labelled customers saved to {DATA / 'customers_with_segments.csv'}")

    # STEP 9 - Plot the elbow curve.
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(elbow["k"], elbow["inertia"], marker="o", color="#1b9e77")
    ax.set_title("Elbow method for choosing K")
    ax.set_xlabel("Number of clusters")
    ax.set_ylabel("Inertia (lower = tighter clusters)")
    ax.set_xticks(elbow["k"])
    fig.tight_layout()
    fig.savefig(OUT / "elbow_plot.png", dpi=140)
    plt.close(fig)

    # STEP 10 - Plot frequency vs monetary value, coloured by segment.
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.scatterplot(
        data=df, x="frequency", y="monetary", hue="segment_name",
        palette="Set2", s=60, alpha=0.8, ax=ax,
    )
    ax.set_title("Customer segments: frequency vs monetary value")
    ax.set_xlabel("Frequency (number of purchases)")
    ax.set_ylabel("Monetary value ($)")
    ax.legend(title="Segment", bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT / "segment_scatter.png", dpi=140)
    plt.close(fig)

    # STEP 11 - Plot recency vs monetary value.
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.scatterplot(
        data=df, x="recency_days", y="monetary", hue="segment_name",
        palette="Set2", s=60, alpha=0.8, ax=ax,
    )
    ax.set_title("Customer segments: recency vs monetary value")
    ax.set_xlabel("Days since last purchase")
    ax.set_ylabel("Monetary value ($)")
    ax.legend(title="Segment", bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT / "recency_scatter.png", dpi=140)
    plt.close(fig)

    # STEP 12 - Write the business interpretation.
    results = [
        "CUSTOMER SEGMENTATION RESULTS",
        "=" * 60,
        f"Customers: {len(df)}",
        f"Clusters: {k}",
        f"Silhouette score: {silhouette:.3f} (closer to 1 means better separated)",
        "",
        "Segment profiles:",
        profiles.to_string(),
        "",
        "How to use this:",
        "- High-value loyal: protect with loyalty rewards and early access.",
        "- Promising: encourage a second/third purchase with a targeted offer.",
        "- Occasional: low-cost reminders and bundles.",
        "- At risk / dormant: win-back campaign or a feedback survey.",
        "",
        "RFM means: recency = days since last purchase, frequency = purchase count,",
        "monetary = total spend. Lower recency is better.",
    ]
    (OUT / "insights.txt").write_text("\n".join(results), encoding="utf-8")
    print("\n" + "\n".join(results))
    print("\nDONE. Check outputs for the elbow plot, segment charts and profiles.")


if __name__ == "__main__":
    main()
