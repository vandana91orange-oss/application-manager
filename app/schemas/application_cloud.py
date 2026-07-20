from datetime import datetime
from pydantic import BaseModel


class ApplicationCloudBase(BaseModel):
    name: str


class ApplicationCloudCreate(ApplicationCloudBase):
    pass


class ApplicationCloudUpdate(ApplicationCloudBase):
    pass


class ApplicationCloudResponse(ApplicationCloudBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
