# 19. The Product Recommendation Engine

> Use purchase history and cosine similarity to recommend related and personalised products.

**Category:** Business Analytics & Prediction  
**Time:** 45–60 minutes  
**Skills:** pivot tables, cosine similarity, cold-start fallback, recommendation logic

## The goal

A store has transaction lines showing which customer bought which product. Build a simple recommender that suggests similar products and personalised products for a customer.

## What you will learn

- Load and inspect
- Count product popularity
- Build a product-by-customer matrix
- Calculate cosine similarity
- Recommend similar products
- Build a customer-by-product matrix
- Score unseen products for a customer
- Add a cold-start fallback
- Save recommendations
- Plot the similarity heatmap
- State the limitation

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/transactions.csv` | About 700 transaction lines across 120 customers and 20 products. |

`transaction_id`, `customer_id`, `product`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load and inspect

```python
df = pd.read_csv(DATA / "transactions.csv")
```

Each row is one product line in a transaction. A customer can appear many times, which is exactly what a recommender needs.

### Step 2 — Count product popularity

```python
product_counts = df["product"].value_counts()
```

`value_counts()` gives a baseline: recommend the most popular products. It is simple but ignores personalisation.

### Step 3 — Build a product-by-customer matrix

```python
product_matrix = df.pivot_table(
    index="product", columns="customer_id",
    values="transaction_id", aggfunc="count", fill_value=0,
)
```

Rows are products, columns are customers, and cells count purchases. This is the table used to compare products.

### Step 4 — Calculate cosine similarity

```python
similarity = cosine_similarity(product_matrix)
sim_df = pd.DataFrame(similarity, index=product_matrix.index,
                      columns=product_matrix.index)
```

Cosine similarity compares the angle between two purchase vectors. A score near 1 means the same customers buy both products.

### Step 5 — Recommend similar products

```python
scores = sim_df.loc[product].drop(product).sort_values(ascending=False)
```

For a chosen product, drop itself from the similarity row and take the highest remaining scores.

### Step 6 — Build a customer-by-product matrix

```python
customer_matrix = df.pivot_table(
    index="customer_id", columns="product",
    values="transaction_id", aggfunc="count", fill_value=0,
)
```

Transpose the perspective: rows are customers, columns are products, and cells count purchases.

### Step 7 — Score unseen products for a customer

```python
for product in owned_products:
    scores += sim_df[product] * owned[product]
scores = scores.drop(labels=owned_products, errors="ignore")
```

For every product the customer has not bought, add its similarity to the products they did buy, weighted by how often they bought them.

### Step 8 — Add a cold-start fallback

```python
if scores.max() <= 0:
    scores = product_counts.reindex(scores.index).fillna(0)
```

If a customer already owns every product in their similar cluster, all similarity scores can be zero. Fall back to popular products instead of showing an empty list.

### Step 9 — Save recommendations

```python
recommendations.to_csv(OUT / "customer_recommendations.csv", index=False)
```

Write the top five recommendations for the first 20 customers to a CSV for review.

### Step 10 — Plot the similarity heatmap

```python
sns.heatmap(sim_df, cmap="YlGnBu")
```

The heatmap shows which products form natural groups. Strong blocks often correspond to product categories.

### Step 11 — State the limitation

```python
results.append("This is not a production recommender.")
```

This is a similarity/popularity baseline. It does not use ratings, prices or click feedback.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/product_counts.csv` | Purchase count for every product. |
| `outputs/product_similarity.csv` | 20×20 product similarity matrix. |
| `outputs/customer_recommendations.csv` | Top five recommendations for 20 customers. |
| `outputs/top_products.png` | Top 10 products by purchase lines. |
| `outputs/similarity_heatmap.png` | Product-to-product similarity heatmap. |
| `outputs/results.txt` | Example recommendations and method explanation. |

## Try it yourself

- Increase the recommendation list to 10 and inspect whether the extra items are sensible.
- Add a simple hit-rate test: hide one purchased product per customer and see whether it appears in the top five.
- Use the customer-by-customer similarity matrix to recommend products from similar customers instead.

## Run it

From the pack root:

```bash
python3 projects/19_recommendation/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

A recommender can look impressive on a heatmap and still be useless in production. Real evaluation needs clicks, purchases and a holdout period.
