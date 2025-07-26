from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional, Dict
from datetime import datetime

class TenantCreate(BaseModel):
    school_name: str
    address: Optional[str]
    contact_email: EmailStr
    contact_phone: Optional[str]
    principal_name: Optional[str]
    subscription_plan_id: UUID4
    branding_config: Optional[Dict] = {}

class TenantResponse(BaseModel):
    tenant_id: UUID4
    school_name: str
    address: Optional[str]
    contact_email: EmailStr
    contact_phone: Optional[str]
    principal_name: Optional[str]
    subscription_plan_id: UUID4
    branding_config: Dict
    created_at: datetime
    status: str