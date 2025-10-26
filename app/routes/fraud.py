from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.ml.svm_model import detect_anomaly
from app.database import get_connection
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

router = APIRouter(prefix="/fraud", tags=["Fraud Detection"])

# --- Request schema ---
class TransactionRequest(BaseModel):
    amount: float
    customer_age: int
    login_attempts: int
    account_balance: float

# --- Helper: Send alert email ---
def send_email_alert(transaction: dict):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("ADMIN_EMAIL")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🚨 Suspicious Transaction Alert"
    msg["From"] = sender
    msg["To"] = receiver

    body = f"""
    ⚠️ Suspicious Transaction Detected!

    Details:
    - Amount: {transaction['amount']}
    - Customer Age: {transaction['customer_age']}
    - Login Attempts: {transaction['login_attempts']}
    - Account Balance: {transaction['account_balance']}
    - Message: {transaction['message']}

    Please review this transaction immediately.
    """
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
        print("📧 Email alert sent to admin.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# --- POST /fraud/check ---
@router.post("/check")
def check_fraud(transaction: TransactionRequest):
    result = detect_anomaly(transaction.dict())
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO fraud_logs (amount, customer_age, login_attempts, account_balance, is_suspicious, message)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                transaction.amount,
                transaction.customer_age,
                transaction.login_attempts,
                transaction.account_balance,
                result["is_suspicious"],
                result["message"]
            ))
            conn.commit()

        # Send email only if suspicious
        if result["is_suspicious"]:
            send_email_alert({**transaction.dict(), **result})

        return result
    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
