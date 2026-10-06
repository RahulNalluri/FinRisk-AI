import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

# Load dataset
data = pd.read_csv("data/online_payment_dataset.csv")

# Remove account IDs
data = data.drop(["nameOrig", "nameDest"], axis=1)

# Encode transaction type
data = pd.get_dummies(data, columns=["type"], drop_first=True)

# Features and target
X = data.drop("isFraud", axis=1)
y = data["isFraud"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("=== Payment Fraud Model Performance ===")
print(classification_report(y_test, y_pred))

# Save model + feature columns
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/payment_model.pkl")
joblib.dump(list(X.columns), "models/payment_features.pkl")
print("Payment Fraud Model Trained and Saved")
print("Features:", list(X.columns))