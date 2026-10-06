# Quick Start Guide — FinRisk AI v2.0

## 🚀 Getting Started in 3 Minutes

### Step 1: Start the Application
```bash
cd d:\projects\Financial-Fraud-Risk-System
python src/app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

### Step 2: Open in Browser
```
http://localhost:5000/
```

---

## 📊 Feature 1: Try the Dashboard

**Access**: Click **"📊 View Dashboard"** button on homepage
- OR go to: `http://localhost:5000/dashboard`

**What You'll See**:
- 📈 Total transactions in dataset
- 🚨 Count of fraudulent transactions  
- 📍 Top cities with fraud cases
- 🎯 Types of fraud detected (pie chart)
- 🌐 Fraud distribution by location (bar chart)
- 🔄 Auto-refreshes every 30 seconds

**Try It**: Click "🔄 Refresh Data" button to manually update

---

## 🔍 Feature 2: Fraud Type Prediction

**Access**: Use the main fraud detection form

### Test This:
1. Enter **Customer ID**: `774817` (actual fraud case)
2. Enter **Amount**: `15000`
3. Click **"Analyze Transaction"**

**What You'll See**:
- FRAUD verdict (because this customer has is_fraudulent=1 in dataset)
- Risk score (will be high)
- **NEW**: Yellow box showing fraud type like:
  - "Fraud Type Detected: **Scam**"
  - Try other IDs to see different fraud types

### Test Different Fraud Types
| Customer ID | Dataset Label | Expected Result | Fraud Type |
|-----------|----------------|-----------------|-----------|
| 774817    | 1 (FRAUD)      | FRAUD           | Scam  |
| 679113    | 1 (FRAUD)      | FRAUD           | Payment Card Fraud |
| 953752    | 1 (FRAUD)      | FRAUD           | Malware |
| 766497    | 1 (FRAUD)      | FRAUD           | Identity Theft |
| 559002    | 1 (FRAUD)      | FRAUD           | Phishing |
| 684415    | 0 (SAFE)       | SAFE            | None |

---

## 👤 Feature 3: Customer Risk Profiling  

**Access**: Click **"👤 Customer Profile"** button on homepage
- OR go to: `http://localhost:5000/customer-profile`

**Try This**:
1. Enter **Customer ID**: `774817`
2. Click **"Search"**

**What You'll See**:

### Risk Badge
```
🔴 Risk Level: High (actual fraudulent customer)
```

### Recommendation
```
Recommended Action: Monitor Closely / Escalate to Investigation
```

### Statistics
- Total Transactions: Customer transaction count
- Fraud Cases: Will be > 0 for actual fraud case
- Fraud Rate: Will be high (>50%)
- Primary Fraud Type: Scam

### Recent Transactions
- Shows last 20 transactions
- Each shows: Amount | Status (FRAUD/SAFE) | Type

**Try Different IDs**:
```
774817    → High risk, actual fraud case
679113    → Fraud customer, Payment Card Fraud
953752    → Fraud customer, Malware
766497    → Fraud customer, Identity Theft
684415    → Safe customer (is_fraudulent=0)
```

**Look For**:
- ✅ Green "SAFE" labels for safe transactions
- ❌ Red "FRAUD" labels for fraudulent ones
- 🏷️ Yellow tags showing fraud type
- 📊 Risk levels and recommendations

---

## 🎯 Test Scenarios

### Scenario 1: Find a High-Risk Customer
1. Go to Dashboard → see Top Fraud Locations
2. Note which cities have most fraud
3. Go to Customer Profile
4. Try IDs from those cities (check dataset)
5. Look for customers with 50%+ fraud rate

### Scenario 2: Understand Fraud Types
1. Go to Dashboard → Fraud Types pie chart
2. See distribution of different fraud types
3. Go to fraud detection form
4. Test with different customer IDs to see various fraud types

### Scenario 3: Investigate a Customer
1. Go to Customer Profile
2. Enter a customer ID
3. View their complete transaction history
4. Identify patterns in fraud (amounts, locations, types)
5. Use "Escalate to Investigation" recommendation if needed

---

## 📱 Mobile Testing

All pages are fully responsive. Try:
```
Desktop version on full screen → Responsive grid
Mobile: Resize browser to 375px width → Mobile layout works
```

---

## 🔧 Troubleshooting

### Error: "Customer not found"
- Customer ID may not exist in the dataset
- Try actual fraud IDs: 774817, 679113, 953752, 766497, 559002
- Or safe ID for comparison: 684415

### Error: "Could not connect to Flask backend"
- Make sure Flask is running: `python src/app.py`
- Check console for error messages
- Verify port 5000 is not in use

### Dashboard shows "—" for values
- Wait 2 seconds for data to load
- Check browser console for JavaScript errors (F12)
- Click "Refresh Data" button manually
  
### Predictions not matching dataset
- Model predicts based on learned patterns, not just dataset labels
- Dataset label (is_fraudulent) is the ground truth
- Model may differ due to training variance

### No fraud type showing in predictions
- Only appears for transactions predicted as **FRAUD**
- For SAFE transactions, box is hidden
- Try customer ID 684415 with amount 25000

---

## 📊 Sample Test Data

### Fraudulent Customers (is_fraudulent=1):
| ID | Fraud Type | Action |
|----|-----------| --------|
| 774817 | Scam | Escalate |
| 679113 | Payment Card Fraud | Escalate |
| 953752 | Malware | Monitor |
| 766497 | Identity Theft | Escalate |
| 559002 | Phishing | Monitor |

### Safe Customer (is_fraudulent=0):
| ID | Risk | Label | Action |
|----|------|------|--------|
| 684415 | Low | SAFE | Regular Review |

---

## ✅ Verification Checklist

- [ ] Flask running without errors
- [ ] Home page loads (http://localhost:5000)
- [ ] Dashboard loads with charts (http://localhost:5000/dashboard)
- [ ] Customer Profile loads with search form
- [ ] Fraud prediction shows fraud type for ID 774817
- [ ] Dashboard metrics update when clicking refresh
- [ ] Customer profile shows transaction history
- [ ] Pages are responsive on mobile view

---

## 🎓 What Each Feature Does

| Feature | Purpose | Use Case |
|---------|---------|----------|
| **Dashboard** | Live analytics | Executive monitoring, real-time insights |
| **Fraud Type Prediction** | Categorize fraud | Understand attack vectors, improve security |
| **Customer Profile** | Risk analysis | Investigator research, escalation decisions |

---

## 💡 Pro Tips

1. **Use Dashboard First** - Get overview of fraud landscape
2. **Investigate Patterns** - Profile high-risk cities' customers
3. **Check Recommendations** - Use system guidance for actions
4. **Export Data** - Manually copy customer profiles for reports
5. **Monitor Trends** - Dashboard auto-refreshes for live monitoring

---

## 📞 Need Help?

Check this file: `FEATURE_IMPLEMENTATION.md` for detailed technical documentation

---

**Happy Testing! 🎉**

*FinRisk AI v2.0 is production ready and packed with intelligence.*
