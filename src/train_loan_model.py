import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
import joblib
import os

# Load dataset
data = pd.read_csv("data/loan_risk_dataset.csv")

# Handle missing values
data = data.fillna(data.median(numeric_only=True))

# Encode categorical features
data = pd.get_dummies(
    data,
    columns=["person_home_ownership", "loan_intent", "loan_grade", "cb_person_default_on_file"],
    drop_first=True
)

# Features and target
X = data.drop("loan_status", axis=1)
y = data["loan_status"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# Train model
model = GradientBoostingClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
print("=== Loan Risk Model Performance ===")
print(classification_report(y_test, y_pred))

# Save model, scaler, feature columns
os.makedirs("models", exist_ok=True)
joblib.dump(model,           "models/loan_risk_model.pkl")
joblib.dump(scaler,          "models/loan_scaler.pkl")
joblib.dump(list(X.columns), "models/loan_features.pkl")
print("Loan Risk Model Trained and Saved")
print("Features:", list(X.columns))