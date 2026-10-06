import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, precision_recall_curve
import numpy as np
import joblib
import os

# Load dataset
data = pd.read_csv("data/Indian_Online_Scam_Dataset.csv")

# Drop columns we don't need including fraud_type
data = data.drop(["transaction_id", "merchant_id", "transaction_time", "fraud_type"], axis=1)

# Drop ALL rows that have any null values — clean data only
data = data.dropna(subset=["customer_id", "amount", "is_fraudulent", "customer_age", "card_type", "location", "purchase_category"])

print(f"Clean dataset shape: {data.shape}")
print("\nClass distribution:")
print(data["is_fraudulent"].value_counts())

# Encode categorical features
data = pd.get_dummies(data, columns=["card_type", "location", "purchase_category"], drop_first=True)

# Make sure all columns are numeric
data = data.astype(float)

# Features and target
X = data.drop("is_fraudulent", axis=1)
y = data["is_fraudulent"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
    max_depth=10,
    min_samples_leaf=2
)
model.fit(X_train, y_train)

# Find best threshold using precision-recall curve
y_proba = model.predict_proba(X_test)[:, 1]
precisions, recalls, thresholds = precision_recall_curve(y_test, y_proba)
f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-9)
best_threshold = thresholds[np.argmax(f1_scores)]
print(f"\nBest threshold: {best_threshold:.3f}")

# Evaluate with best threshold
y_pred = (y_proba >= best_threshold).astype(int)
print("\n=== Scam Model Performance ===")
print(classification_report(y_test, y_pred))

# Save model + threshold + feature columns
os.makedirs("models", exist_ok=True)
joblib.dump(model,                 "models/scam_model.pkl")
joblib.dump(list(X.columns),       "models/scam_features.pkl")
joblib.dump(float(best_threshold), "models/scam_threshold.pkl")

print(f"\nScam Detection Model Trained and Saved with threshold {best_threshold:.3f}")
print("Features:", list(X.columns))
