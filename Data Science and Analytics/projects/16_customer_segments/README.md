# 16. The Customer Segmentation Studio

> Use RFM and K-Means to group customers into useful, explainable segments.

**Category:** Business Analytics & Prediction  
**Time:** 45–60 minutes  
**Skills:** RFM, StandardScaler, K-Means, elbow method, silhouette score

## The goal

A business has 400 customers with recency, frequency and monetary value. Group them into segments that suggest different marketing actions.

## What you will learn

- Load and inspect the RFM columns
- Scale the features
- Try several values of K
- Fit the final model
- Measure cluster separation
- Profile the clusters
- Name the segments
- Save the labelled customers
- Plot the elbow curve
- Plot the segments

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/customers.csv` | 400 customers with RFM measures, signup age and channel. |
| `data/customers_with_segments.csv` | The output table with a K-Means cluster and a segment name. |

`customer_id`, `recency_days`, `frequency`, `monetary`, `signup_days_ago`, `channel`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load and inspect the RFM columns

```python
df = pd.read_csv(DATA / "customers.csv")
print(df[["recency_days", "frequency", "monetary"]].describe())
```

Recency is days since last purchase (lower is better). Frequency is purchase count (higher is better). Monetary is total spend (higher is better).

### Step 2 — Scale the features

```python
scaler = StandardScaler()
scaled = scaler.fit_transform(df[["recency_days", "frequency", "monetary"]])
```

K-Means uses distance. Without scaling, monetary value in dollars would dominate frequency counts. `StandardScaler` puts each feature on a comparable scale.

### Step 3 — Try several values of K

```python
for k in range(2, 9):
    model = KMeans(n_clusters=k, random_state=42, n_init=10).fit(scaled)
    inertias.append(model.inertia_)
```

The elbow method plots inertia against K. Inertia falls as clusters increase; look for the point where the improvement slows down.

### Step 4 — Fit the final model

```python
model = KMeans(n_clusters=4, random_state=42, n_init=10)
df["cluster"] = model.fit_predict(scaled)
```

Choose K=4 for this dataset. `fit_predict` both fits the clusters and assigns each customer to one.

### Step 5 — Measure cluster separation

```python
silhouette = silhouette_score(scaled, df["cluster"])
```

The silhouette score summarises how similar each point is to its own cluster compared with the next closest cluster. Higher is better, up to 1.

### Step 6 — Profile the clusters

```python
profiles = df.groupby("cluster").agg(
    avg_recency_days=("recency_days", "mean"),
    avg_frequency=("frequency", "mean"),
    avg_monetary=("monetary", "mean"),
)
```

Go back to the original RFM units and compute the average recency, frequency and monetary value for each cluster.

### Step 7 — Name the segments

```python
segment_names = ["High-value loyal", "Promising", "Occasional", "At risk / dormant"]
```

Rank the clusters on recency, frequency and monetary value, then map the order to plain-English names such as `High-value loyal` and `At risk / dormant`.

### Step 8 — Save the labelled customers

```python
df.to_csv(DATA / "customers_with_segments.csv", index=False)
```

Write the original rows plus `cluster` and `segment_name` so the business team can filter and act on the segments.

### Step 9 — Plot the elbow curve

```python
ax.plot(elbow["k"], elbow["inertia"], marker="o")
```

The elbow chart documents why K=4 is a reasonable choice instead of an arbitrary one.

### Step 10 — Plot the segments

```python
sns.scatterplot(data=df, x="frequency", y="monetary", hue="segment_name")
```

A scatterplot of frequency versus monetary value, coloured by segment, makes the business meaning visible.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `data/customers_with_segments.csv` | Every customer with a cluster and segment name. |
| `outputs/elbow_values.csv` | Inertia for K=2 through K=8. |
| `outputs/elbow_plot.png` | The elbow chart. |
| `outputs/segment_profiles.csv` | Average RFM values by named segment. |
| `outputs/segment_scatter.png` | Frequency versus monetary value by segment. |
| `outputs/recency_scatter.png` | Recency versus monetary value by segment. |
| `outputs/insights.txt` | Segment profiles and suggested actions. |

## Try it yourself

- Try K=3 and K=5 and compare the segment profiles.
- Use quantile-based RFM scores instead of K-Means and compare the groups.
- Add `signup_days_ago` as a feature and see whether the segments change.

## Run it

From the pack root:

```bash
python3 projects/16_customer_segments/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

Clusters are not automatically meaningful. Always translate them back into original units and ask whether the business can act on them.
