import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

# Load dataset
# creditcard.csv columns: Time, V1-V28 (PCA features), Amount, Class
data = pd.read_csv("data/creditcard.csv")

# Features and target
X = data.drop("Class", axis=1)
y = data["Class"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("=== Credit Card Fraud Model Performance ===")
print(classification_report(y_test, y_pred))

# Save model + feature columns
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/creditcard_model.pkl")
joblib.dump(list(X.columns), "models/creditcard_features.pkl")

print("Credit Card Fraud Model Trained and Saved")
print("Features:", list(X.columns))