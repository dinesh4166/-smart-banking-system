from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field
from app.database import get_connection
import bcrypt
from datetime import datetime, timedelta
from jwt_handler import create_access_token

router = APIRouter()

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

@router.post('/register', status_code=201)
def register(payload: RegisterRequest):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # check existing
            cur.execute("SELECT id FROM users WHERE email = %s", (payload.email,))
            if cur.fetchone():
                raise HTTPException(status_code=400, detail="Email already registered")
            hashed = bcrypt.hashpw(payload.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (payload.name, payload.email, hashed))
            return {"message": "User registered successfully"}
    finally:
        conn.close()

@router.post('/login')
def login(payload: LoginRequest):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, password FROM users WHERE email = %s", (payload.email,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=401, detail="Invalid credentials")

            stored = row["password"].encode("utf-8")

            if not bcrypt.checkpw(payload.password.encode("utf-8"), stored):
                raise HTTPException(status_code=401, detail="Invalid credentials")

            token = create_access_token({"user_id": row["id"], "email": payload.email})

            return {
                "message": "Login successful",
                "user_id": row["id"],
                "access_token": token,
                "token_type": "bearer"
            }
    finally:
        conn.close()
