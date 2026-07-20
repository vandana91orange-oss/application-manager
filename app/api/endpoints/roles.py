from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.role import (
    RoleCreate,
    RoleUpdate,
    RoleResponse
)

from app.repositories.role_repository import RoleRepository
from app.services.role_service import RoleService

from app.dependencies.auth import UserRole, require_roles


router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)


def get_role_service(
    db: Session = Depends(get_db)
):

    repository = RoleRepository(db)

    return RoleService(repository)


# CREATE ROLE
@router.post(
    "",
    response_model=RoleResponse
)
def create_role(
    role: RoleCreate,
    service: RoleService = Depends(get_role_service),
    current_user=Depends(
            require_roles(
                UserRole.ADMIN
            )
        )

    ):

    return service.create(role)



# GET ALL ROLES
@router.get(
    "",
    response_model=list[RoleResponse]
)
def get_roles(
    service: RoleService = Depends(get_role_service),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
            UserRole.EMPLOYEE,
            UserRole.VIEWER,

        )
    )

):

    return service.get_roles()



# GET ROLE BY ID
@router.get(
    "/{role_id}",
    response_model=RoleResponse
)
def get_role(
    role_id: int,
    service: RoleService = Depends(get_role_service),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
            UserRole.EMPLOYEE,
            UserRole.VIEWER,

        )
    )
):

    return service.get_role(role_id)



# UPDATE ROLE
@router.put(
    "/{role_id}",
    response_model=RoleResponse
)
def update_role(
    role_id: int,
    data: RoleUpdate,
    service: RoleService = Depends(get_role_service),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN
        )
    )
):

    return service.update(
        role_id,
        data
    )



# DELETE ROLE
@router.delete(
    "/{role_id}"
)
def delete_role(
    role_id: int,
    service: RoleService = Depends(get_role_service),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN

        )
    )
):

    service.delete(role_id)

    return {
        "message": "Role deleted successfully"
    }
