from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import datetime
from shared.database.supabase import get_supabase_client
from shared.database.mongodb import db
from shared.models.audit_log import AuditLog
from shared.auth.dependencies import get_current_user
from ..models.tenant import TenantCreate, TenantResponse
from supabase import Client

router = APIRouter()

@router.post("", response_model=TenantResponse)
async def create_tenant(
    tenant: TenantCreate,
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):
    """
    Create a new tenant (school) in Supabase public.tenants table.
    Requires sysadmin role.
    """
    tenant_id = uuid.uuid4()
    data = {
        "tenant_id": str(tenant_id),
        "school_name": tenant.school_name,
        "address": tenant.address,
        "contact_email": tenant.contact_email,
        "contact_phone": tenant.contact_phone,
        "principal_name": tenant.principal_name,
        "subscription_plan_id": str(tenant.subscription_plan_id),
        "branding_config": tenant.branding_config,
        "status": "Active",
        "created_at": datetime.utcnow().isoformat()
    }
    
    response = supabase.table("tenants").insert(data).execute()
    
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to create tenant")
    
    audit_log = AuditLog(
        tenant_id=tenant_id,
        user_id=uuid.UUID(user["id"]),
        action="CreateTenant",
        details={"school_name": tenant.school_name, "tenant_id": str(tenant_id)},
        created_at=datetime.utcnow()
    )
    await db.audit_logs.insert_one(audit_log.dict())
    
    return TenantResponse(**response.data[0])