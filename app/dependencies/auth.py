from app.repositories.audit_repository import AuditRepository
from app.services.audit_service import AuditService
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.users import User
from app.core.security import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.repositories.upload_file_repository import UploadRepository
from app.services.upload_service import UploadService

security = HTTPBearer()

from enum import Enum

class UserRole(str, Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    EMPLOYEE = "employee"
    VIEWER = "Viewer"


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_token(token)

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


    user = (
        db.query(User)
        .filter(
            User.id == int(user_id)
        )
        .first()
    )


    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )


    return user


def require_roles(*allowed_roles):

    allowed = [
        role.value if hasattr(role, "value") else role
        for role in allowed_roles
    ]

    def dependency(current_user=Depends(get_current_user)):
        if current_user.role.name not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have permission."
            )

        return current_user

    return dependency

def get_upload_service(
    db: Session = Depends(get_db)
):

    repository = UploadRepository(db)
    audit_repo = AuditRepository(db)
    audit_service = AuditService(
        db=db,
        audit_repo=audit_repo
    )
    return UploadService(
        repository=repository,
        audit_service=audit_service
    )
