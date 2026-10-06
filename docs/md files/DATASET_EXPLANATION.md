# 📊 Dataset Structure & Labels — Important Information

## Understanding the Data

### Dataset: Indian_Online_Scam_Dataset.csv

**The `is_fraudulent` Column**:
```
0 = SAFE (transaction is not fraudulent)
1 = FRAUD (transaction IS fraudulent)
```

**The `fraud_type` Column**:
- Contains fraud category names (Phishing, Malware, etc.)
- Present for ALL transactions (both safe and fraudulent)
- This can be confusing! A safe transaction (is_fraudulent=0) may still have a fraud_type value

---

## 🔍 The Issue Discovered

### Problem:
The initial documentation used these supposedly "fraud" customer IDs for testing:
- 684415, 447448, 975001, 976547, 935741

**But these are actually SAFE transactions!** (is_fraudulent=0)

### Why This Matters:
When the model predicted SAFE for these customers, the documentation incorrectly said it should have predicted FRAUD. This created confusion about whether the system was working correctly.

---

## ✅ Correct Test Data

### ACTUAL Fraudulent Transactions (is_fraudulent=1):

| Customer ID | Fraud Type | Amount | Test Use |
|------------|-----------|--------|----------|
| **774817** | Scam | 8,526 | ✅ Test FRAUD detection |
| **679113** | Payment Card Fraud | 11,430 | ✅ Test fraud type prediction |
| **953752** | Malware | 14,762 | ✅ Test malware detection |
| **766497** | Identity Theft | 14,823 | ✅ Test identity theft |
| **559002** | Phishing | 9,713 | ✅ Test phishing |

### SAFE Transactions (is_fraudulent=0):

| Customer ID | Fraud Type* | Amount | Test Use |
|------------|-----------|--------|----------|
| **684415** | Identity theft | 1,263 | Reference (shows SAFE) |
| **447448** | Malware | 2,223 | Reference (shows SAFE) |
| **975001** | Malware | 7,510 | Reference (shows SAFE) |

*Note: fraud_type exists for safe transactions too, which can be confusing!

---

## 🎯 How to Use Correct Test Data

### For Fraud Detection Testing:
```
1. Enter Customer ID: 774817
2. Enter Amount: 15000 (or any amount)
3. Click "Analyze Transaction"
4. Expected: Shows "FRAUD DETECTED"
5. Verify: is_fraudulent=1 in dataset
```

### For Customer Profiling:
```
1. Enter Customer ID: 774817
2. View profile
3. Expected: Should show fraud cases and high fraud rate
4. Verify: Dataset shows multiple fraud cases
```

### For Safe Transaction Reference:
```
1. Enter Customer ID: 684415
2. Enter Amount: 5000
3. Click "Analyze Transaction"
4. Expected: Shows "SAFE"
5. Verify: is_fraudulent=0 in dataset
```

---

## 💡 Key Insights

### 1. **Model vs Reality**
- The model predicts based on learned patterns
- Dataset labels (is_fraudulent) represent the ground truth
- Predictions should generally align with dataset labels for customers in training set
- But predictions may differ if features are different from what model learned

### 2. **Fraud Type Column is Misleading**
- Fraud_type exists even for safe transactions
- This represents "what type of fraud this would be if it were fraudulent"
- Only rely on fraud_type when `is_fraudulent=1`

### 3. **Data Quality**
- Total records: 7,953
- Fraudulent (is_fraudulent=1): 2,265 (28.5%)
- Safe (is_fraudulent=0): 4,963 (62.4%)
- Missing is_fraudulent: ~725 (9.1%)

---

## 🔧 How to Verify Data Consistency

### Check a Customer's Label:

```python
import pandas as pd
df = pd.read_csv('data/Indian_Online_Scam_Dataset.csv')

# Check customer 774817
customer_data = df[df['customer_id'] == 774817]
print(customer_data[['customer_id', 'is_fraudulent', 'fraud_type']])

# Output should show:
# is_fraudulent: 1.0 (FRAUD)
# fraud_type: scam
```

### Check Multiple Records:

```python
test_ids = [774817, 679113, 953752, 684415, 447448]
for cid in test_ids:
    row = df[df['customer_id'] == cid].iloc[0]
    label = "FRAUD" if row['is_fraudulent'] == 1 else "SAFE"
    print(f"Customer {cid}: {label}")
```

---

## 📋 Updated Documentation Files

All documentation has been updated to use correct test data:

✅ **QUICK_START.md** - Uses 774817 for fraud examples  
✅ **FEATURE_IMPLEMENTATION.md** - Added label explanation  
✅ **VERIFICATION_CHECKLIST.md** - Updated test cases  

---

## 🎯 Action Items

When testing the system:

1. **Always check `is_fraudulent`** in the dataset first
2. **For FRAUD tests**: Use customer IDs where is_fraudulent=1
3. **For SAFE tests**: Use customer IDs where is_fraudulent=0
4. **Match expectations** with dataset labels, not vice versa

---

## ✅ Summary

**Before (Incorrect)**:
- Used customer 684415 (is_fraudulent=0) as fraud example
- System correctly predicted SAFE
- Documentation said this was wrong ❌

**After (Correct)**:
- Use customer 774817 (is_fraudulent=1) as fraud example
- System predicts FRAUD
- Documentation matches reality ✅

---

**Last Updated**: 2025-03-27  
**Status**: ✅ All documentation corrected with accurate test data
