# 17. The Churn Early-Warning System

> Train a logistic regression model that estimates each customer's chance of churning.

**Category:** Business Analytics & Prediction  
**Time:** 45–60 minutes  
**Skills:** logistic regression, train/test split, scaling, precision/recall, ROC-AUC

## The goal

A subscription business wants to flag customers who may leave. Build an interpretable model, evaluate it honestly on unseen customers, and explain the coefficients.

## What you will learn

- Load and inspect
- Choose features and target
- Split into train and test
- Scale the features
- Fit logistic regression
- Make predictions
- Evaluate the model
- Explain the coefficients
- Plot the confusion matrix
- Plot the ROC curve

## Dataset at a glance

| File | What it contains |
| --- | --- |
| `data/churn.csv` | 800 customers with tenure, charges, support calls, late payments, usage and churn label. |

`customer_id`, `tenure_months`, `monthly_charges`, `support_calls`, `late_payments`, `usage_hours`, `churned`.

All datasets in this pack are synthetic and deterministic. They are included so the project runs offline and gives the same result every time.

## Step-by-step walkthrough

The comments in `main.py` use the same step numbers. Follow the code and the explanation together.

### Step 1 — Load and inspect

```python
df = pd.read_csv(DATA / "churn.csv")
print(df["churned"].mean())
```

Check the churn rate and missing values. An imbalanced target changes how you should read accuracy.

### Step 2 — Choose features and target

```python
feature_cols = ["tenure_months", "monthly_charges", "support_calls",
                "late_payments", "usage_hours"]
X, y = df[feature_cols], df["churned"]
```

Drop the customer ID because it is an identifier, not a behavioural signal. The target is `churned`.

### Step 3 — Split into train and test

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)
```

The model learns on 70% of customers and is evaluated on the 30% it has never seen. `stratify=y` keeps the churn rate similar in both sets.

### Step 4 — Scale the features

```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

Fit the scaler on the training data only, then apply the same transformation to the test data. This prevents test information from leaking into training.

### Step 5 — Fit logistic regression

```python
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)
```

Logistic regression models the log-odds of churn as a weighted sum of the features. It is a strong, interpretable baseline for binary outcomes.

### Step 6 — Make predictions

```python
y_pred = model.predict(X_test_scaled)
y_prob = model.predict_proba(X_test_scaled)[:, 1]
```

`predict` returns the 0/1 class. `predict_proba[:, 1]` returns the estimated probability of churn, which is useful for ranking customers.

### Step 7 — Evaluate the model

```python
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)
```

Accuracy alone can be misleading. Also report precision, recall, F1 and ROC-AUC, and compare accuracy with the majority-class baseline.

### Step 8 — Explain the coefficients

```python
coef_table = pd.DataFrame({
    "feature": feature_cols,
    "coefficient": model.coef_[0],
    "odds_ratio": np.exp(model.coef_[0]),
})
```

A positive coefficient is associated with more churn; a negative coefficient with less. `exp(coefficient)` is the odds ratio.

### Step 9 — Plot the confusion matrix

```python
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
```

The matrix shows true positives, true negatives, false positives and false negatives. It makes the cost of mistakes concrete.

### Step 10 — Plot the ROC curve

```python
fpr, tpr, _ = roc_curve(y_test, y_prob)
```

The ROC curve shows the trade-off between catching churners and falsely flagging loyal customers. AUC summarises it in one number.

## Outputs to inspect

| File | What it shows |
| --- | --- |
| `outputs/results.txt` | Metrics, confusion matrix, coefficients and interpretation. |
| `outputs/churn_coefficients.csv` | Coefficient and odds ratio for every feature. |
| `outputs/churn_coefficients.png` | Signed coefficient chart. |
| `outputs/confusion_matrix.png` | Test-set confusion matrix. |
| `outputs/roc_curve.png` | ROC curve with AUC. |

## Try it yourself

- Lower the classification threshold from 0.5 to 0.3 and see how recall and precision change.
- Remove `late_payments` and compare the AUC. Does the model lose much?
- Add a `high_support` flag for customers with more than three calls and compare coefficients.

## Run it

From the pack root:

```bash
python3 projects/17_churn_model/main.py
```

The script creates the `data/` and `outputs/` folders if they are missing. It does not need a GPU, an API key, or an internet connection.

## Note

A churn model is a decision aid, not a verdict. The business must decide how much a false positive or false negative costs.
