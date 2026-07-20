from typing import Any

from app.repositories.audit_repository import AuditRepository
from app.schemas.audit_logs import AuditLogListResponse
from fastapi import Request
from sqlalchemy.orm import Session

from app.models.audit_logs import AuditLog
from app.models.users import User


class AuditService:

    def __init__(self, db: Session,
                 audit_repo: AuditRepository,
                 ):
        self.db = db
        self.audit_repo = audit_repo

    def log(
        self,
        *,
        current_user: User | None,
        action: str,
        module: str,
        description: str,
        resource_id: int | str | None = None,
        old_values: dict | None = None,
        new_values: dict | None = None,
        request: Request | None = None,
    ) -> AuditLog:

        ip_address = None
        user_agent = None

        if request:
            ip_address = request.client.host if request.client else None
            user_agent = request.headers.get("user-agent")

        audit_log = AuditLog(
            user_id=current_user.id if current_user else None,
            user_email=current_user.email if current_user else None,
            role=current_user.role.name if current_user and current_user.role else None,
            action=action,
            module=module,
            resource_id=str(resource_id) if resource_id else None,
            description=description,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        self.db.add(audit_log)
        self.db.flush()

        return audit_log

    def get_logs(
        self,
        page: int,
        size: int,
        user: str = None,
        action: str = None,
        module: str = None,
        search: str = None,
        from_date=None,
        to_date=None,
    ):
        logs, total = self.audit_repo.get_all(
            page=page,
            size=size,
            user=user,
            action=action,
            module=module,
            search=search,
            from_date=from_date,
            to_date=to_date,
        )

        return AuditLogListResponse(
            items=logs,
            total=total,
            page=page,
            size=size,
        )
