import pandas as pd
import numpy as np
from sklearn.svm import OneClassSVM
import joblib
import os

MODEL_PATH = "app/ml/oneclass_svm_model.pkl"

def train_anomaly_model():
    # Load dataset
    df = pd.read_csv("app/ml/bank_transactions_data_2.csv")

    # Select relevant columns that exist in your CSV
    numeric_cols = ["TransactionAmount", "CustomerAge", "LoginAttempts", "AccountBalance"]

    # Clean data
    df = df[numeric_cols].dropna()
    df = df.astype(float)

    # Train SVM
    model = OneClassSVM(kernel='rbf', gamma=0.001, nu=0.05)
    model.fit(df)

    # Save model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print("✅ One-Class SVM model trained and saved successfully.")


def detect_anomaly(transaction: dict):
    if not os.path.exists(MODEL_PATH):
        train_anomaly_model()

    model = joblib.load(MODEL_PATH)

    # Match feature order used during training
    features = np.array([[
        transaction["amount"],
        transaction["customer_age"],
        transaction["login_attempts"],
        transaction["account_balance"]
    ]])

    prediction = model.predict(features)[0]  # 1 = normal, -1 = anomaly
    is_suspicious = bool(prediction == -1)

    return {
        "is_suspicious": is_suspicious,
        "message": "⚠️ Suspicious transaction detected!" if is_suspicious else "✅ Transaction appears normal."
    }


# 👇 Run this directly to train
if __name__ == "__main__":
    train_anomaly_model()
