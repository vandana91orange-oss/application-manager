from datetime import datetime
from pydantic import BaseModel


class UploadedFileCreate(BaseModel):
    file_name: str
    original_file_name: str
    file_path: str


class UploadedFileUpdate(BaseModel):
    status: str


class UploadedFileResponse(BaseModel):
    id: int
    file_name: str
    original_file_name: str
    file_path: str
    status: str
    total_rows: int
    processed_rows: int
    failed_rows: int
    uploaded_by: int
    uploaded_at: datetime

    class Config:
        from_attributes = True


class UploadStatus:

    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"
    PARTIAL_SUCCESS = "Partial"
