import pandas as pd
import numpy as np
import os

np.random.seed(42)

normal_data = {
    "amount": np.random.normal(2000, 1000, 270).clip(10, 8000),
    "transaction_count": np.random.randint(1, 20, 270),
    "account_age": np.random.randint(30, 3000, 270),
    "label": "normal"
}

# Suspicious: very high amounts, new accounts, burst activity
suspicious_data = {
    "amount": np.random.normal(15000, 5000, 30).clip(8000, 50000),
    "transaction_count": np.random.randint(30, 80, 30),
    "account_age": np.random.randint(1, 60, 30),
    "label": "suspicious"
}

# Combine & shuffle
df = pd.concat([pd.DataFrame(normal_data), pd.DataFrame(suspicious_data)])
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save to CSV
os.makedirs("app/ml", exist_ok=True)
df.to_csv("app/ml/sample_data.csv", index=False)

print("✅ Generated 300 realistic transactions (270 normal, 30 suspicious)")
