from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AuditLogResponse(BaseModel):
    id: int
    user_id: int | None
    user_email: str | None
    role: str | None

    action: str
    module: str
    resource_id: str | None
    description: str

    old_values: dict | None
    new_values: dict | None

    ip_address: str | None
    user_agent: str | None

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuditLogListResponse(BaseModel):
    items: list[AuditLogResponse]
    total: int
    page: int
    size: int
