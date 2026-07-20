from app.repositories.application_cloud_mapping_repository import ApplicationCloudMappingRepository
from app.repositories.application_repository import ApplicationRepository
from app.repositories.audit_repository import AuditRepository
from app.repositories.metadata_repository import MetadataRepository
from app.repositories.migration_repository import MigrationRepository
from app.repositories.owner_repository import OwnerRepository
from app.repositories.remark_repository import RemarkRepository
from app.repositories.security_repository import SecurityRepository
from app.services.application_service import ApplicationService
from app.services.audit_service import AuditService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.application_cloud import (
    ApplicationCloudCreate,
    ApplicationCloudUpdate,
    ApplicationCloudResponse
)

from app.repositories.application_cloud_repository import (
    ApplicationCloudRepository
)

from app.services.application_cloud_service import (
    ApplicationCloudService
)

from app.dependencies.auth import UserRole, require_roles


router = APIRouter(
    prefix="/clouds",
    tags=["Clouds"]
)


def get_application_cloud_service(
    db: Session = Depends(get_db)
):

    return ApplicationCloudService(
        repository=ApplicationCloudRepository(db),
    )

def get_application_service(
        db: Session = Depends(get_db)
):
    return ApplicationService(
    db = db,
    application_repo=ApplicationRepository(db),
    migration_repo=MigrationRepository(db),
    metadata_repo=MetadataRepository(db),
    security_repo=SecurityRepository(db),
    owner_repo=OwnerRepository(db),
    remark_repo=RemarkRepository(db),
    cloud_repo=ApplicationCloudRepository(db),
    cloud_mapping_repo=ApplicationCloudMappingRepository(db),
    audit_service= AuditService(db, AuditRepository)
)


@router.post(
    "",
    response_model=ApplicationCloudResponse
)
def create_cloud(
    request: ApplicationCloudCreate,
    service: ApplicationCloudService = Depends(get_application_cloud_service),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,

        )
    )
):

    return service.create(
        request.name
    )

@router.get(
    "",
    response_model=list[ApplicationCloudResponse]
)
def get_all_clouds(
    service: ApplicationCloudService = Depends(get_application_cloud_service),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
            UserRole.EMPLOYEE,
            UserRole.VIEWER,

        )
    )
):

    return service.get_all()


@router.get(
    "/{id}",
    response_model=ApplicationCloudResponse
)
def get_cloud(
    id: int,
    service: ApplicationCloudService = Depends(get_application_cloud_service),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
            UserRole.EMPLOYEE,
            UserRole.VIEWER,

        )
    )
):

    return service.get_by_id(id)


@router.put(
    "/{id}",
    response_model=ApplicationCloudResponse
)
def update_cloud(
    id: int,
    request: ApplicationCloudUpdate,
    service: ApplicationCloudService = Depends(get_application_cloud_service),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER
        )
    )
):

    return service.update(
        id,
        request.name
    )

@router.delete("/{id}")
def delete_cloud(
    id: int,
    service: ApplicationCloudService = Depends(get_application_cloud_service),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER

        )
    )
):

    return service.delete(id)


@router.get("/all/applications")
def get_cloud_applications(
    page: int = 1,
    size: int = 10,
    search: str | None = None,
    cloud: str | None = None,
    owner: str | None = None,
    domain: str | None = None,
    service: ApplicationCloudService = Depends(get_application_service),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
            UserRole.EMPLOYEE,
            UserRole.VIEWER,

        )
    )
):
    return service.get_applications_by_cloud(
        page=page,
        size=size,
        search=search,
        cloud=cloud,
        owner=owner,
        domain=domain,
    )
