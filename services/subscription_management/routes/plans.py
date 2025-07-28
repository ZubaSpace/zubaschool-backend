from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime
from shared.database.supabase import get_supabase_client
from shared.database.mongodb import db
from shared.models.audit_log import AuditLog
from shared.auth.dependencies import get_current_user
from ..models.plan import SubscriptionPlanCreate, SubscriptionPlanResponse, Feature
from supabase import Client

router = APIRouter()

@router.post("", response_model=SubscriptionPlanResponse)
async def create_subscription_plan(
    plan: SubscriptionPlanCreate,
    user: dict = Depends(get_current_user),
    supabase: Client = Depends(get_supabase_client)
):
    """
    Create a subscription plan (system admin only).
    Stores plan in Supabase public.subscription_plans and logs action in MongoDB.
    """
    plan_id = uuid.uuid4()
    data = {
        "plan_id": str(plan_id),
        "name": plan.name,
        "description": plan.description,
        "price_monthly": plan.price_monthly,
        "price_yearly": plan.price_yearly,
        "features": [f.dict() for f in plan.features],
        "max_users": plan.max_users,
        "max_storage_mb": plan.max_storage_mb,
        "created_at": datetime.utcnow().isoformat()
    }
    
    response = supabase.table("subscription_plans").insert(data).execute()
    
    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to create plan")
    
    audit_log = AuditLog(
        tenant_id=None,
        user_id=uuid.UUID(user["id"]),
        action="CreateSubscriptionPlan",
        details={"plan_id": str(plan_id), "name": plan.name},
        created_at=datetime.utcnow()
    )
    await db.audit_logs.insert_one(audit_log.dict())
    
    return SubscriptionPlanResponse(**response.data[0])