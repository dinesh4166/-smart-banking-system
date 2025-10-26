# 🏦 SmartBank – User Registration, KYC & Fraud Detection System

## 🚀 Objective
**SmartBank** is a modular backend system built to simulate real-world banking features like:
- 🔐 **User Authentication & Registration**
- 🪪 **KYC Document Upload**
- 🤖 **Fraud Detection using Machine Learning (One-Class SVM)**  
It provides a complete backend foundation for secure and intelligent banking operations.

---

## ⚙️ Tech Stack
- **Backend:** FastAPI (Python)
- **Database:** MySQL (via PyMySQL)
- **Machine Learning:** Scikit-learn (One-Class SVM)
- **Validation:** Pydantic
- **Email Alerts:** smtplib (Gmail SMTP)
- **Testing:** Swagger UI (FastAPI built-in)
- **Environment:** `.env` configuration for secrets

---

## 🧱 Project Structure
```
smartbank/
│
├── app/
│   ├── main.py                # App entry point (FastAPI initialization)
│   ├── database.py            # MySQL connection setup
│   │
│   ├── routes/
│   │   ├── auth.py            # User registration & login
│   │   ├── kyc.py             # KYC document upload (no JWT for now)
│   │   └── fraud.py           # Fraud detection API + email alert
│   │
│   ├── ml/
│   │   ├── svm_model.py       # One-Class SVM model training & detection
│   │   └── sample_data.csv    # Transaction dataset for model training
│
├── .env                       # Environment variables
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```

---

## 🧩 Database Schema

### 1️⃣ `users` Table
| Field | Type | Description |
|-------|------|--------------|
| id | INT (PK, AUTO_INCREMENT) | Unique user ID |
| name | VARCHAR(100) | Full name |
| email | VARCHAR(100) | Unique email |
| password | VARCHAR(255) | Hashed password (bcrypt) |
| created_at | TIMESTAMP | Default: current timestamp |

### 2️⃣ `kyc_documents` Table
| Field | Type | Description |
|-------|------|--------------|
| id | INT (PK, AUTO_INCREMENT) | Unique KYC record |
| user_id | INT (FK → users.id) | Associated user |
| document_type | VARCHAR(50) | e.g., Aadhar, PAN, Passport |
| document_number | VARCHAR(100) | Simulated KYC number |
| status | ENUM('PENDING', 'VERIFIED') | Verification status |
| uploaded_at | TIMESTAMP | Default: current timestamp |


### ⚠️ `fraud_logs` Table
| Field | Type | Description |
|-------|------|--------------|
| id | INT (PK, AUTO_INCREMENT) | Log ID |
| amount | FLOAT | Transaction amount |
| customer_age | INT | Age of customer |
| login_attempts | INT | Number of login attempts |
| account_balance | FLOAT | Balance before transaction |
| is_suspicious | BOOLEAN | Flag if fraud detected |
| message | VARCHAR(255) | Detection message |
| created_at | TIMESTAMP | Default: current timestamp |

---

## 🧠 Fraud Detection Module

### Model: **One-Class SVM**
The ML model identifies unusual transactions by learning the *pattern of normal behavior*.

**Features used:**
- `amount` → transaction amount  
- `customer_age` → customer’s age  
- `login_attempts` → number of login attempts  
- `account_balance` → account balance before transaction  

If a new transaction deviates significantly, it’s flagged as **suspicious**.

---

### 🧩 Workflow
1. A transaction occurs → API `/fraud/check` is called.  
2. The model (`oneclass_svm_model.pkl`) evaluates the transaction.  
3. If it’s an anomaly →  
   - Stored in `fraud_logs`  
   - Sends an email alert to the **Admin**

---

## 📡 API Endpoints

### 👤 POST `/register`
Registers a new user.  
```json
{
  "name": "Alice",
  "email": "alice@gmail.com",
  "password": "securepass"
}
```

---

### 🔑 POST `/login`
Authenticates user and returns a JWT token.  
```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

---

### 🪪 POST `/kyc/upload`
Uploads KYC document for a registered user.  
```json
{
  "document_type": "Aadhar",
  "document_number": "1234-5678-9012"
}
```

---

### ⚠️ POST `/fraud/check`
Checks for fraudulent transactions using the ML model.  
```json
{
  "amount": 12000,
  "customer_age": 25,
  "login_attempts": 3,
  "account_balance": 8000
}
```

**Response Example:**
```json
{
  "is_suspicious": true,
  "message": "⚠️ Suspicious transaction detected!"
}
```

---

## 📧 Email Alert (Admin Notification)
If a transaction is flagged as suspicious, the system sends an email alert:

```
Subject: 🚨 Suspicious Transaction Alert
Body:
⚠️ Suspicious Transaction Detected!

Details:
- Amount: 12000
- Customer Age: 25
- Login Attempts: 3
- Account Balance: 8000
```

Configured via `.env`:
```
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_generated_app_password
ADMIN_EMAIL=admin@gmail.com
```

---

## ⚡ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/<your-username>/smartbank.git
cd smartbank
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Database
Update `.env` with your MySQL credentials and run:
```bash
python -m app.database
```

### 5️⃣ Train Fraud Model
```bash
python app/ml/svm_model.py
```

### 6️⃣ Run FastAPI Server
```bash
uvicorn app.main:app --reload
```

Swagger Docs → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧭 Demo Flow
1. Register a user  
2. Upload a KYC document  
3. Run a transaction via `/fraud/check`  
4. View results in **DB** and **console**  
5. (Optional) Email alert sent to admin if suspicious  

---

## 🧩 Future Enhancements
- ✅ Admin dashboard to view fraud logs  
- ✅ Email verification for users  
- 🔄 Retrain ML model with live transaction data  

---

**Developed with ❤️ using FastAPI, MySQL, and Scikit-learn**
