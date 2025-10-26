from fastapi import FastAPI
from app.routes import auth, kyc, fraud   # ✅ Import all routes first
from app.database import init_db

# Initialize FastAPI app
app = FastAPI(title="SmartBank - User Registration, KYC & Fraud Detection")

# ✅ Root route
@app.get("/")
def home():
    return {"message": "Welcome to SmartBank API"}


#  routers
app.include_router(auth.router)
app.include_router(kyc.router)
app.include_router(fraud.router)

# ✅ Startup event: Initialize DB
@app.on_event("startup")
def startup():
    init_db()

