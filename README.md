# 🏦 SmartBank – User Registration & KYC Module

## 🚀 Objective
This module is part of the **SmartBank Modular Banking Backend System**, designed to handle secure **user onboarding and KYC verification**.  
It enables users to **register**, **log in**, and **upload simulated KYC documents**, forming the base for fraud detection and other banking modules.

---

## ⚙️ Tech Stack
- **Backend:** FastAPI (Python)
- **Database:** MySQL (via PyMySQL)
- **Authentication:** JWT (JSON Web Tokens)
- **Validation:** Pydantic (for request body validation)
- **Testing:** Swagger UI (FastAPI built-in)
- **Environment:** Local MySQL instance

---

## 🧱 Project Structure (Simplified)
smartbank/
│
├── app/
│   ├── main.py               # App entry point (starts FastAPI)
│   ├── models.py             # User & KYC table schemas
│   ├── database.py           # MySQL setup using PyMySQL
│   │
│   ├── routes/
│   │   ├── auth.py           # User registration & login
│   │   └── kyc.py            # KYC upload endpoint
│   │
│   └── utils/
│       └── jwt_handler.py    # Create & verify JWT tokens
│
├── .env                      # Environment variables (not committed)
├── .gitignore                # To exclude .env and venv
├── requirements.txt          # Python dependencies
└── README.md                 # Project info

---

## 🧩 Database Schema
```
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

---
```
## ⚡ Setup Instructions

### 1️⃣ Clone the Repository
git clone https://github.com/<your-username>/smartbank.git
cd smartbank

### 2️⃣ Set Up Virtual Environment
python -m venv venv
source venv/bin/activate     # On Mac/Linux
venv\Scripts\activate        # On Windows

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Configure MySQL Connection
In `database.py`, update:
DATABASE_URL = {
    "host": "localhost",
    "user": "root",
    "password": "yourpassword",
    "database": "smartbank"
}

### 5️⃣ Run FastAPI Server
uvicorn app.main:app --reload

Visit **http://127.0.0.1:8000/docs** to open **Swagger UI**.

---

## 🔐 Authentication – JWT
**JSON Web Token (JWT)** is used for secure login and authorization.  
When a user logs in successfully, a signed JWT token is returned.  
This token must be passed in the `Authorization` header for all protected endpoints.

Example:
Authorization: Bearer <your_token>

---

## 📡 API Endpoints

### ➕ POST `/register`
Registers a new user.  
**Body Example:**
{
  "name": "Alice",
  "email": "alice@gmail.com",
  "password": "securepass"
}

### 🔑 POST `/login`
Authenticates user and returns JWT token.  
**Response Example:**
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}

### 📄 POST `/kyc/upload`
Uploads (simulated) KYC document.  
**Headers:**
Authorization: Bearer <JWT_TOKEN>
**Body Example:**
{
  "document_type": "Aadhar",
  "document_number": "1234-5678-9012"
}

---

## 🧪 Testing via Swagger UI
1. Run server → open http://127.0.0.1:8000/docs  
2. Register a new user  
3. Log in → copy the `access_token`  
4. Click **Authorize** → paste the token  
5. Test `/kyc/upload`  

---

## 🧭 Next Steps
✅ Integrate **Fraud Detection** module  
## 🧠 Fraud Detection
The **Support Vector Machine (SVM)** model uses historical transaction data (amount, frequency, location, and behavior patterns) to flag potential fraudulent activities in real time.

---

**Developed with ❤️ using FastAPI, MySQL, and JWT.**
