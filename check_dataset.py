import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('data/Indian_Online_Scam_Dataset.csv')

print("=" * 60)
print("DATASET ANALYSIS")
print("=" * 60)
print(f"\nDataset Shape: {df.shape}")
print(f"\nColumn 'is_fraudulent' - Unique values: {sorted(df['is_fraudulent'].dropna().unique())}")
print(f"\nValue Counts for is_fraudulent:")
print(df['is_fraudulent'].value_counts().sort_index())

print("\n" + "=" * 60)
print("SAMPLE FRAUD RECORDS (is_fraudulent = 1)")
print("=" * 60)
fraud_df = df[df['is_fraudulent'] == 1]
print(f"\nTotal fraud records: {len(fraud_df)}")
print("\nFirst 10 fraud records:")
print(fraud_df[['customer_id', 'amount', 'is_fraudulent', 'fraud_type']].head(10).to_string())

print("\n" + "=" * 60)
print("SAMPLE SAFE RECORDS (is_fraudulent = 0)")
print("=" * 60)
safe_df = df[df['is_fraudulent'] == 0]
print(f"\nTotal safe records: {len(safe_df)}")
print("\nFirst 10 safe records:")
print(safe_df[['customer_id', 'amount', 'is_fraudulent', 'fraud_type']].head(10).to_string())

print("\n" + "=" * 60)
print("DATA TYPES")
print("=" * 60)
print(df.dtypes)
