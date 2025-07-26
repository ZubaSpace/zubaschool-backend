from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Optional, Union

class AuditLog(BaseModel):
    tenant_id: Optional[Union[str, None]] = None
    user_id: str
    action: str
    details: Dict
    created_at: datetime
    
    class Config:
        # Allow population by field name and alias
        populate_by_name = True
        # JSON encoders for MongoDB compatibility
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }