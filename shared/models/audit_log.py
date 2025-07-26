from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Dict, Optional

class AuditLog(BaseModel):
    tenant_id: Optional[UUID4]
    user_id: UUID4
    action: str
    details: Dict
    created_at: datetime