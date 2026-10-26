"""Project 10 - The E-Commerce Funnel.

Goal: measure how many visitors move from a visit to a product view, a cart,
and finally a purchase, then compare acquisition channels.

Run from the pack root:
    python3 projects/10_funnel_analysis/main.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")
STAGES = ["visits", "product_views", "add_to_carts", "purchases"]
STAGE_LABELS = ["Visits", "Product views", "Add to carts", "Purchases"]


def main() -> None:
    print("=" * 70)
    print("PROJECT 10 - THE E-COMMERCE FUNNEL")
    print("=" * 70)

    # STEP 1 - Load the daily channel-level funnel table.
    df = pd.read_csv(DATA / "funnel_events.csv")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    print(f"\nSTEP 1: loaded {len(df)} daily channel rows")
    print(df.head(3).to_string(index=False))

    # STEP 2 - Check that the funnel is logically ordered.
    # Each stage should be no larger than the stage before it.
    print("\nSTEP 2: quality check")
    print("Missing values:", int(df.isna().sum().sum()))
    ordered = (df["visits"] >= df["product_views"]) & (df["product_views"] >= df["add_to_carts"]) & (
        df["add_to_carts"] >= df["purchases"]
    )
    print(f"Rows with a broken funnel order: {int((~ordered).sum())}")

    # STEP 3 - Add stage-to-stage conversion rates.
    # Example: view_rate = product_views / visits.
    df["view_rate"] = df["product_views"] / df["visits"]
    df["cart_rate"] = df["add_to_carts"] / df["product_views"]
    df["purchase_rate"] = df["purchases"] / df["add_to_carts"]
    df["visit_to_purchase"] = df["purchases"] / df["visits"]

    # STEP 4 - Build the overall funnel.
    overall = df[STAGES].sum()
    overall_table = pd.DataFrame(
        {
            "stage": STAGE_LABELS,
            "count": overall.values,
        }
    )
    overall_table["share_of_visits"] = overall_table["count"] / overall_table.loc[0, "count"]
    overall_table["step_conversion"] = [
        1.0,
        overall["product_views"] / overall["visits"],
        overall["add_to_carts"] / overall["product_views"],
        overall["purchases"] / overall["add_to_carts"],
    ]
    overall_table.to_csv(OUT / "overall_funnel.csv", index=False)
    print("\nSTEP 4: overall funnel")
    print(overall_table.round(3).to_string(index=False))

    # STEP 5 - Compare channels.
    channel = (
        df.groupby("channel")[STAGES]
        .sum()
        .assign(
            view_rate=lambda x: x["product_views"] / x["visits"],
            cart_rate=lambda x: x["add_to_carts"] / x["product_views"],
            purchase_rate=lambda x: x["purchases"] / x["add_to_carts"],
            visit_to_purchase=lambda x: x["purchases"] / x["visits"],
        )
        .sort_values("visit_to_purchase", ascending=False)
        .round(3)
    )
    channel.to_csv(OUT / "channel_funnel.csv")
    print("\nSTEP 5: channel comparison")
    print(channel.to_string())

    # STEP 6 - Chart the overall funnel.
    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = ["#1b9e77", "#66a61e", "#e6ab02", "#d95f02"]
    bars = ax.barh(overall_table["stage"][::-1], overall_table["count"][::-1], color=colors[::-1])
    ax.set_title("Overall e-commerce funnel")
    ax.set_xlabel("People reaching each stage")
    for bar, count in zip(bars, overall_table["count"][::-1]):
        ax.text(bar.get_width() * 0.98, bar.get_y() + bar.get_height() / 2, f" {count:,.0f}",
                va="center", ha="right", color="white", fontsize=10, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "funnel_chart.png", dpi=140)
    plt.close(fig)

    # STEP 7 - Chart the final conversion rate by channel.
    fig, ax = plt.subplots(figsize=(8, 4))
    channel["visit_to_purchase"].sort_values().plot(kind="barh", color="#7570b3", ax=ax)
    ax.set_title("Visit-to-purchase rate by channel")
    ax.set_xlabel("Conversion rate")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    fig.tight_layout()
    fig.savefig(OUT / "channel_conversion.png", dpi=140)
    plt.close(fig)

    # STEP 8 - Plot the daily visit-to-purchase trend.
    daily = df.groupby("date")[STAGES].sum()
    daily["visit_to_purchase"] = daily["purchases"] / daily["visits"]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(daily.index, daily["visit_to_purchase"], color="#e7298a", linewidth=1.5)
    ax.set_title("Daily visit-to-purchase conversion")
    ax.set_ylabel("Conversion rate")
    ax.set_xlabel("Date")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    fig.tight_layout()
    fig.savefig(OUT / "daily_conversion.png", dpi=140)
    plt.close(fig)

    # STEP 9 - Write the findings.
    best_channel = channel.index[0]
    biggest_drop = overall_table.loc[overall_table["step_conversion"].idxmin(), "stage"]
    insights = [
        "FUNNEL INSIGHTS",
        "=" * 50,
        f"Total visits: {overall['visits']:,.0f}",
        f"Total purchases: {overall['purchases']:,.0f}",
        f"Overall visit-to-purchase rate: {overall['purchases'] / overall['visits']:.2%}",
        f"Best channel by final conversion: {best_channel} ({channel.loc[best_channel, 'visit_to_purchase']:.2%})",
        f"Smallest step conversion: {biggest_drop}",
        "",
        "Overall funnel:",
        overall_table.round(3).to_string(index=False),
        "",
        "Channel funnel:",
        channel.to_string(),
    ]
    (OUT / "insights.txt").write_text("\n".join(insights), encoding="utf-8")
    print("\n" + "\n".join(insights))
    print("\nDONE. Check outputs for the funnel and channel charts.")


if __name__ == "__main__":
    main()
