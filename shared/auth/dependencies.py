from fastapi import Header, HTTPException, Depends
from supabase import Client
import jwt
import os
from .supabase import get_supabase_client

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

async def get_current_user(authorization: str = Header(...), supabase: Client = Depends(get_supabase_client)):
    """
    Validate JWT and return user data with role.
    """
    try:
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid token format")
        
        token = authorization.replace("Bearer ", "")
        decoded = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"])
        
        user_id = decoded.get("sub")
        role = decoded.get("role")
        
        if not user_id or not role:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        if role != "sysadmin":
            raise HTTPException(status_code=403, detail="System admin access required")
        
        return {"id": user_id, "email": decoded.get("email"), "role": role}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")