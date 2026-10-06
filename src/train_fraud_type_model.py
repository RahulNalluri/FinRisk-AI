import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib
import os

# Load dataset
data = pd.read_csv("data/Indian_Online_Scam_Dataset.csv")

# Filter only fraudulent transactions (is_fraudulent == 1)
fraud_data = data[data["is_fraudulent"] == 1].copy()

print(f"Total fraud transactions: {fraud_data.shape[0]}")
print(f"Fraud types distribution:\n{fraud_data['fraud_type'].value_counts()}")

# Drop rows with missing fraud_type
fraud_data = fraud_data.dropna(subset=["fraud_type"])

# Drop unnecessary columns
fraud_data = fraud_data.drop(
    ["transaction_id", "merchant_id", "transaction_time", "is_fraudulent"],
    axis=1
)

# Drop rows with any null values except fraud_type
fraud_data = fraud_data.dropna(subset=["customer_id", "amount", "customer_age", "card_type", "location", "purchase_category"])

print(f"\nCleaned fraud dataset shape: {fraud_data.shape}")

# Encode categorical features including fraud_type target
fraud_data = pd.get_dummies(fraud_data, columns=["card_type", "location", "purchase_category"], drop_first=True)

# Separate features and target
X = fraud_data.drop("fraud_type", axis=1)
y = fraud_data["fraud_type"]

# Create target encoder for fraud types
le = LabelEncoder()
y_encoded = le.fit_transform(y)

print(f"Fraud type classes: {le.classes_}")
print(f"Encoded target shape: {y_encoded.shape}")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
    max_depth=8,
    min_samples_leaf=2
)
model.fit(X_train, y_train)

# Evaluate
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"\n=== Fraud Type Classification Model ===")
print(f"Train Accuracy: {train_score:.4f}")
print(f"Test Accuracy: {test_score:.4f}")

# Save model, encoder, features, and class mapping
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/fraud_type_model.pkl")
joblib.dump(list(X.columns), "models/fraud_type_features.pkl")
joblib.dump(le, "models/fraud_type_encoder.pkl")

print(f"\nFraud Type Classification Model Trained and Saved")
print(f"Features: {len(X.columns)} total features")
