from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import get_connection
import pymysql

router = APIRouter(prefix="/kyc", tags=["KYC"])

# --- Request Model ---
class KYCRequest(BaseModel):
    document_type: str
    document_number: str

# --- POST /kyc/upload ---
@router.post("/upload")
def upload_kyc(payload: KYCRequest):
    """Simplified version (no JWT auth)."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO kyc_documents (user_id, document_type, document_number, status)
                VALUES (%s, %s, %s, %s)
            """, (1, payload.document_type, payload.document_number, 'PENDING'))  # fixed user_id=1 for testing
            conn.commit()
            return {
                "message": "KYC document uploaded successfully",
                "user_id": 1,
                "document_type": payload.document_type,
                "status": "PENDING"
            }
    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
