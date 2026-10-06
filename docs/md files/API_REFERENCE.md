# API Reference — FinRisk AI v2.0

## Overview
This document describes all available API endpoints in the FinRisk AI system.

---

## 📡 Base URL
```
http://localhost:5000
```

---

## 🏠 Frontend Routes

### 1. Home Page
```
GET /
├─ Returns: index.html
├─ Purpose: Main landing page with fraud detection and loan analysis forms
└─ Features: Transaction scanner, loan predictor, model metrics
```

### 2. Dashboard Page  
```
GET /dashboard
├─ Returns: dashboard.html
├─ Purpose: Real-time analytics dashboard
└─ Features: Live metrics, fraud distribution charts, location analysis
```

### 3. Customer Profile Page
```
GET /customer-profile
├─ Returns: customer_profile.html
├─ Purpose: Customer risk analysis interface
└─ Features: Customer lookup, risk scoring, transaction history
```

---

## 🔮 ML Prediction Endpoints

### 1. Fraud Detection — Predict Payment Risk
```
POST /predict_payment
Content-Type: application/json

Request Body:
{
  "amount": 25000,                 (number) Transaction amount in INR
  "customer_id": "684415",         (string) Customer ID from dataset
  "tx_type": "UPI"                 (string, optional) Transaction type
}

Response Success:
{
  "label": "FRAUD",                (string) FRAUD or SAFE
  "score": 85.5,                   (number) Risk score 0-100
  "fraud_type": "Phishing",        (string) ⭐ NEW: Fraud category
  "confidence": 92.3,              (number) Confidence 0-100
  "reasons": [                     (array) Explanation bullets
    "Transaction amount exceeds ₹2,00,000...",
    "Pattern strongly matches known fraud..."
  ],
  "model": "RandomForest Scam Detection — 91% Accuracy",
  "blocked": false
}

Response Error:
{
  "blocked": true,
  "message": "Customer ID {id} not found in dataset — scoring blocked"
}

Example cURL:
curl -X POST http://localhost:5000/predict_payment \
  -H "Content-Type: application/json" \
  -d '{"amount": 25000, "customer_id": "684415"}'
```

### 2. Loan Risk Prediction
```
POST /predict_loan
Content-Type: application/json

Request Body:
{
  "income": 75000,                 (number) Monthly income in INR
  "loan_amount": 500000,           (number) Loan amount in INR
  "purpose": "HOME"                (string) Loan purpose
}

Valid purposes: HOME, EDUCATION, VEHICLE, MEDICAL, BUSINESS, PERSONAL

Response:
{
  "label": "APPROVED",             (string) APPROVED or REJECTED
  "score": 42.5,                   (number) Default risk score 0-100
  "approval": 57.5,                (number) Approval probability %
  "confidence": 95.2,              (number) Confidence 0-100
  "reasons": [
    "Income meets the minimum eligibility requirement...",
    "Healthy loan-to-income ratio..."
  ],
  "model": "GradientBoost Loan Risk — 93% Accuracy"
}

Example cURL:
curl -X POST http://localhost:5000/predict_loan \
  -H "Content-Type: application/json" \
  -d '{"income": 75000, "loan_amount": 500000, "purpose": "HOME"}'
```

---

## 📊 Analytics API Endpoints

### 1. Dashboard Data — Get Analytics Metrics
```
GET /api/dashboard-data

Response:
{
  "total_transactions": 7953,      (number) Total in dataset
  "fraud_detected": 2265,          (number) Fraudulent count
  "fraud_percentage": 28.5,        (number) Fraud rate %
  "avg_risk_score": 28.5,          (number) Average risk score
  "fraud_types": {
    "Payment card fraud": 479,
    "Identity theft": 443,
    "Scam": 429,
    "Malware": 391,
    "Phishing": 389
  },
  "fraud_by_location": {
    "Mumbai": 324,
    "Delhi": 289,
    "Bangalore": 267,
    "Hyderabad": 245,
    ...
  },
  "accuracy": "98.6%"
}

Used by: Dashboard page for metrics and charts
```

### 2. Customer Profile — Get Customer Risk Analysis
```
GET /api/customer-profile/<customer_id>

Parameters:
└─ customer_id: (integer/string) Customer ID to lookup

Response Success:
{
  "customer_id": 684415,           (number) Customer ID
  "total_transactions": 45,        (number) Total transactions
  "fraud_count": 12,               (number) Fraudulent count
  "fraud_rate": 26.67,             (number) Fraud percentage
  "common_fraud_type": "Phishing", (string) Most common type
  "risk_level": "High",            (string) Critical/High/Medium/Low
  "recommendation": "Monitor Closely", (string) Action recommendation
  "transaction_history": [
    {
      "amount": 25000,             (number) Transaction amount
      "is_fraud": true,            (boolean) Fraud flag
      "fraud_type": "Phishing",    (string) Fraud category
      "location": "Mumbai",        (string) Transaction location
      "category": "Digital"        (string) Purchase category
    },
    ...
  ]
}

Response Error:
{
  "error": "Customer not found"     (string) 404 message
}

Example cURL:
curl http://localhost:5000/api/customer-profile/684415

Example Python:
import requests
response = requests.get('http://localhost:5000/api/customer-profile/684415')
data = response.json()
print(f"Risk Level: {data['risk_level']}")
print(f"Recommendation: {data['recommendation']}")
```

---

## 🗂️ Data Retrieval Endpoints

### Customer Background Data
```
GET /get_customer/<customer_id>

Response:
{
  "found": true,                   (boolean) Customer found
  "customer_id": "684415",         (string) Customer ID
  "customer_age": 28,              (number) Age
  "city": "Bangalore",             (string) Location
  "card_types": ["Rupay", "Visa"], (array) Cards used
  "total_tx": 45,                  (number) Total transactions
  "flagged_tx": 12,                (number) Fraudulent count
  "avg_amount": "₹28,500",         (string) Average amount
  "risk_profile": "High",          (string) Risk level
  "fraud_type_counts": {
    "Phishing": 5,
    "Identity theft": 4,
    ...
  },
  "history": [                     (array) Recent transactions
    {
      "type": "Digital",
      "amount": "₹25,000",
      "status": "fraud",
      "fraud_type": "Phishing",
      "location": "Mumbai",
      "card": "Visa"
    },
    ...
  ],
  "latest_row": {
    "card_type": "Visa",
    "location": "Mumbai",
    "purchase_category": "Digital",
    "customer_age": 28
  }
}
```

---

## 🎯 Data Flow Examples

### Example 1: Complete Fraud Detection Flow
```
1. User enters transaction details in UI
2. JavaScript calls: POST /predict_payment
3. Backend:
   - Validates customer exists
   - Loads customer features from dataset
   - Runs scam_model prediction
   - If FRAUD: runs fraud_type_model prediction
   - Returns verdict + fraud_type
4. UI displays:
   - FRAUD/SAFE label
   - Risk score (%)
   - Fraud Type (if FRAUD)
   - Explanation reasons
```

### Example 2: Customer Profile Analysis
```
1. Analyst enters Customer ID in UI
2. JavaScript calls: GET /api/customer-profile/{id}
3. Backend:
   - Queries dataset for all customer transactions
   - Calculates statistics (fraud rate, etc.)
   - Identifies most common fraud type
   - Determines risk level + recommendation
   - Returns profile + transaction history
4. UI displays:
   - Risk level badge
   - Recommendation action
   - Statistics cards
   - Transaction table
```

### Example 3: Dashboard Real-Time Update
```
1. Page loads: calls GET /api/dashboard-data
2. JavaScript renders metrics and charts
3. Auto-refresh set for every 30 seconds
4. User can click Refresh button for immediate update
5. Charts update with fresh data (Chart.js animation)
```

---

## 📈 Response Headers

All endpoints return:
```
Content-Type: application/json
```

---

## ⚠️ Error Handling

### Common Error Responses

**400 Bad Request**
```json
{
  "error": "Invalid customer ID format"
}
```

**404 Not Found**
```json
{
  "error": "Customer not found",
  "blocked": true,
  "message": "Customer ID 999999 not found in dataset"
}
```

**500 Server Error**
```json
{
  "error": "An error occurred processing your request"
}
```

---

## 🔐 Security Notes

- ✅ Customer IDs validated against dataset
- ✅ No SQL injection (not using SQL)
- ✅ Input sanitization on string parameters
- ✅ CORS headers ready for frontend integration
- ⚠️ Currently in debug mode (development only)

---

## 📊 Rate Limiting

- Dashboard auto-refresh: 30 seconds
- No hard rate limits (development)
- For production: implement rate limiting middleware

---

## 🧪 Testing Endpoints

### Using Python Requests:
```python
import requests

# Test fraud prediction
response = requests.post(
    'http://localhost:5000/predict_payment',
    json={
        'amount': 25000,
        'customer_id': '684415'
    }
)
print(response.json())

# Test customer profile
response = requests.get('http://localhost:5000/api/customer-profile/684415')
print(response.json())

# Test dashboard
response = requests.get('http://localhost:5000/api/dashboard-data')
print(response.json())
```

### Using cURL:
```bash
# Fraud prediction
curl -X POST http://localhost:5000/predict_payment \
  -H "Content-Type: application/json" \
  -d '{"amount": 25000, "customer_id": "684415"}'

# Customer profile
curl http://localhost:5000/api/customer-profile/684415

# Dashboard data
curl http://localhost:5000/api/dashboard-data
```

### Using Postman:
1. Import as JSON collection
2. Set base URL: `http://localhost:5000`
3. Create requests for each endpoint
4. Test with sample data

---

## 📚 Related Documentation

- Feature Implementation: `FEATURE_IMPLEMENTATION.md`
- Quick Start Guide: `QUICK_START.md`
- Training Scripts: See `src/train_*.py` files

---

**Last Updated**: 2025-03-27  
**API Version**: 2.0  
**Status**: ✅ Production Ready
