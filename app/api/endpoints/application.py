from app.repositories.application_repository import  ApplicationRepository
from app.repositories.audit_repository import AuditRepository
from app.schemas.application import ApplicationDetailsResponse, ApplicationUpdate, ApplicationCreate
from app.services.application_service import ApplicationService
from app.services.audit_service import AuditService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.repositories.application_cloud_repository import (
    ApplicationCloudRepository
)

from app.services.application_cloud_service import (
    ApplicationCloudService
)

from app.dependencies.auth import UserRole, require_roles


router = APIRouter(
    prefix="/application",
    tags=["Applications"]
)


def get_application_cloud_service(
    db: Session = Depends(get_db)
):

    return ApplicationCloudService(
        repository=ApplicationCloudRepository(db),
    )
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.application_repository import ApplicationRepository
from app.repositories.metadata_repository import MetadataRepository
from app.repositories.migration_repository import MigrationRepository
from app.repositories.security_repository import SecurityRepository
from app.repositories.remark_repository import RemarkRepository
from app.repositories.owner_repository import OwnerRepository
from app.repositories.application_cloud_repository import ApplicationCloudRepository
from app.repositories.application_cloud_mapping_repository import ApplicationCloudMappingRepository
from app.services.application_service import ApplicationService


def get_application_service(
    db: Session = Depends(get_db)
):

    return ApplicationService(
        db=db,
        application_repo=ApplicationRepository(db),
        metadata_repo=MetadataRepository(db),
        migration_repo=MigrationRepository(db),
        security_repo=SecurityRepository(db),
        remark_repo=RemarkRepository(db),
        owner_repo=OwnerRepository(db),
        cloud_repo=ApplicationCloudRepository(db),
        cloud_mapping_repo=ApplicationCloudMappingRepository(db),
        audit_service=AuditService(db, AuditRepository)
    )


@router.delete(
    "/{application_id}"
)
def delete_application(
    application_id: int,
    service: ApplicationService = Depends(
        get_application_service
    ),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    )
):

    service.delete(
        application_id,
        current_user
    )

    return {
        "message": "Application deleted successfully."
    }


@router.patch(
    "/{application_id}",
    response_model=ApplicationDetailsResponse
)
def update_application(
    application_id: int,
    request: ApplicationUpdate,
    service: ApplicationService = Depends(
        get_application_service
    ),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    )
):

    return service.update(
        application_id,
        request,
        current_user
    )


@router.post(
    "",
    response_model=ApplicationDetailsResponse,
    status_code=201
)
def create_application(
    request: ApplicationCreate,
    service: ApplicationService = Depends(get_application_service),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    )
):

    return service.create(request, current_user)


@router.get("/export")
def export_applications(
    search: str | None = None,
    cloud: str | None = None,
    owner: str | None = None,
    domain: str | None = None,
    service=Depends(get_application_service),
):
    return service.export_csv(
        search=search,
        cloud=cloud,
        owner=owner,
        domain=domain,
    )
