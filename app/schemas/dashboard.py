# app/schemas/dashboard.py

from datetime import datetime
from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_applications: int
    total_uploads: int
    completed_migrations: int
    in_progress_migrations: int
    pending_migrations: int
    failed_uploads: int
    total_users: int


class MigrationStatusItem(BaseModel):
    status: str
    count: int


class CloudDistributionItem(BaseModel):
    cloud: str
    count: int


class DomainDistributionItem(BaseModel):
    domain: str
    count: int


class RecentUploadItem(BaseModel):
    id: int
    file_name: str
    status: str
    uploaded_by: str
    created_at: datetime


class RecentAuditLogItem(BaseModel):
    user: str
    action: str
    module: str
    description: str
    created_at: datetime


class DashboardResponse(BaseModel):
    summary: DashboardSummary
    migration_status: list[MigrationStatusItem]
    cloud_distribution: list[CloudDistributionItem]
    applications_by_domain: list[DomainDistributionItem]
    recent_uploads: list[RecentUploadItem]
    recent_audit_logs: list[RecentAuditLogItem]
