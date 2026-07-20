from app.repositories.audit_repository import AuditRepository
from app.schemas.audit_logs import AuditLogListResponse
from app.services.audit_service import AuditService
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from datetime import date
from app.dependencies.auth import UserRole, require_roles


def get_audit_service(
    db: Session = Depends(get_db),
) -> AuditService:
    return AuditService(db, AuditRepository)

router = APIRouter(
    prefix="/audit-logs",
    tags=["AuditLogs"]
)

@router.get(
    "",
    response_model=AuditLogListResponse
)
def get_audit_logs(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    user: str | None = None,
    action: str | None = None,
    module: str | None = None,
    search: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN.value,
            UserRole.MANAGER.value,
        )
    ),
    service: AuditService = Depends(get_audit_service),
):
    return service.get_logs(
        page=page,
        size=size,
        user=user,
        action=action,
        module=module,
        search=search,
        from_date=from_date,
        to_date=to_date,
    )