from fastapi import APIRouter, Depends
from app.schemas.document_upload import UploadedFileResponse, UploadedFileCreate, UploadedFileUpdate
from app.dependencies.auth import UserRole, get_current_user, get_upload_service, require_roles


router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"]
)

from fastapi import APIRouter, Depends, File, UploadFile

@router.post(
    "",
    response_model=UploadedFileResponse
)
async def create_upload(
    file: UploadFile = File(...),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER

        )
    ),
    service=Depends(get_upload_service)
):
    return await service.create(
        file=file,
        user=current_user
    )

@router.get(
    "",
    response_model=list[UploadedFileResponse]
)
def get_uploads(
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
            UserRole.EMPLOYEE,
            UserRole.VIEWER,

        )
    ),
    service=Depends(get_upload_service)
):

    return service.get_all()

@router.get(
    "/{upload_id}",
    response_model=UploadedFileResponse
)
def get_upload(
    upload_id: int,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
            UserRole.EMPLOYEE,
            UserRole.VIEWER,

        )
    ),
    service=Depends(get_upload_service)
):

    return service.get_one(upload_id)


@router.put(
    "/{upload_id}",
    response_model=UploadedFileResponse
)
def update_upload(
    upload_id: int,
    data: UploadedFileUpdate,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
    service=Depends(get_upload_service)
):
    return service.update(
        upload_id,
        data,
        user=current_user
    )


@router.delete("/{upload_id}")
def delete_upload(
    upload_id: int,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,

        )
    ),
    service=Depends(get_upload_service)
):

    return service.delete(upload_id, user=current_user)
