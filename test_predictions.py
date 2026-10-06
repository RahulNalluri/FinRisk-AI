import pandas as pd
import joblib
import numpy as np

# Load dataset and models
df = pd.read_csv('data/Indian_Online_Scam_Dataset.csv')
scam_model = joblib.load('models/scam_model.pkl')
scam_features = joblib.load('models/scam_features.pkl')

def build_scam_features(customer_row, amount):
    row = {col: 0.0 for col in scam_features}
    row["amount"]       = float(amount)
    row["customer_age"] = float(customer_row.get("customer_age", 30))

    card = str(customer_row.get("card_type", ""))
    card_col = f"card_type_{card}"
    if card_col in row:
        row[card_col] = 1.0

    loc = str(customer_row.get("location", ""))
    loc_col = f"location_{loc}"
    if loc_col in row:
        row[loc_col] = 1.0

    cat = str(customer_row.get("purchase_category", ""))
    cat_col = f"purchase_category_{cat}"
    if cat_col in row:
        row[cat_col] = 1.0

    return np.array([[row[c] for c in scam_features]])

def get_probability(model, features):
    try:
        proba = model.predict_proba(features)[0]
        return round(float(proba[1]) * 100, 2)
    except Exception:
        pred = model.predict(features)[0]
        return 85.0 if int(pred) == 1 else 10.0

# Test cases from dataset
test_customers = [684415, 447448, 975001, 976547, 935741]

print("=" * 80)
print("COMPARING MODEL PREDICTIONS VS ACTUAL DATASET LABELS")
print("=" * 80)

for cust_id in test_customers:
    # Get customer data from dataset
    cust_rows = df[df['customer_id'] == cust_id]
    
    if cust_rows.empty:
        print(f"\nCustomer {cust_id}: NOT FOUND IN DATASET")
        continue
    
    customer_row = cust_rows.iloc[-1].to_dict()
    actual_label = int(customer_row['is_fraudulent'])
    actual_label_text = "FRAUD" if actual_label == 1 else "SAFE"
    amount = customer_row.get('amount', 5000)
    
    # Get model prediction
    features = build_scam_features(customer_row, amount)
    score = get_probability(scam_model, features)
    model_pred = int(scam_model.predict(features)[0])
    model_pred_text = "FRAUD" if model_pred == 1 else "SAFE"
    
    # Check for mismatch
    match = "✓ MATCH" if actual_label == model_pred else "✗ MISMATCH"
    
    print(f"\nCustomer ID: {cust_id}")
    print(f"  Amount: {amount:,.2f}")
    print(f"  Location: {customer_row.get('location', 'Unknown')}")
    print(f"  Card Type: {customer_row.get('card_type', 'Unknown')}")
    print(f"  Customer Age: {int(customer_row.get('customer_age', 30))}")
    print(f"  Actual Label (from dataset): {actual_label_text} ({actual_label})")
    print(f"  Model Prediction: {model_pred_text} ({model_pred})")
    print(f"  Risk Score: {score}%")
    print(f"  Status: {match}")

print("\n" + "=" * 80)
print("CHECKING ALL CUSTOMER RECORDS FOR PATTERN")
print("=" * 80)

mismatches = 0
total_checked = 0
mismatch_examples = []

for cust_id in df['customer_id'].dropna().unique()[:500]:  # Check first 500 unique customers
    cust_rows = df[df['customer_id'] == cust_id]
    
    for idx, (_, row) in enumerate(cust_rows.iterrows()):
        if pd.isna(row['is_fraudulent']) or pd.isna(row['customer_id']):
            continue
            
        actual_label = int(row['is_fraudulent'])
        amount = row['amount'] if not pd.isna(row['amount']) else 5000
        
        features = build_scam_features(row.to_dict(), amount)
        model_pred = int(scam_model.predict(features)[0])
        
        if actual_label != model_pred:
            mismatches += 1
            if len(mismatch_examples) < 20:  # Store first 20 mismatches
                mismatch_examples.append({
                    'customer_id': cust_id,
                    'actual': actual_label,
                    'predicted': model_pred,
                    'amount': amount
                })
        
        total_checked += 1

print(f"\nTotal records checked: {total_checked}")
print(f"Total mismatches: {mismatches}")
print(f"Match rate: {((total_checked - mismatches) / total_checked * 100):.2f}%")

if mismatch_examples:
    print(f"\nFirst {len(mismatch_examples)} mismatches found:")
    for ex in mismatch_examples:
        print(f"  Customer {ex['customer_id']}: Actual={ex['actual']} (Dataset), Predicted={ex['predicted']} (Model)")
