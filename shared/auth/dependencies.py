from fastapi import Header, HTTPException, Depends
from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def get_current_user(authorization: str = Header(...)):
    # Simplified for learning; in production, validate JWT
    # Assume token contains user_id and role
    try:
        token = authorization.replace("Bearer ", "")
        # For now, return a mock user (replace with real JWT validation later)
        return {"id": "550e8400-e29b-41d4-a716-446655440000", "email": "sysadmin@zubaschool.com", "role": "sysadmin"}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")