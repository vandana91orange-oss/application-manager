from typing import Annotated, Literal

from app.schemas.pagination import PaginatedResponse
from fastapi import APIRouter, Depends, Query, status, UploadFile, File
from app.schemas.document_upload import UploadedFileResponse, UploadedFileUpdate
from app.dependencies.auth import UserRole, get_current_user, get_upload_service, require_roles


router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"]
)


@router.post(
    "",
    response_model=list[UploadedFileResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_upload(
    files: list[UploadFile] = File(
        ...,
        description="Select one or more CSV, XLSX, or XLS files",
    ),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
        )
    ),
    service=Depends(get_upload_service),
):
    return await service.create(
        files=files,
        user=current_user,
    )


@router.get(
    "",
    response_model=PaginatedResponse[UploadedFileResponse],
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
    service=Depends(get_upload_service),

    # Pagination
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,

    # Searching
    search: Annotated[
        str | None,
        Query(max_length=150),
    ] = None,

    # Filtering
    status: str | None = None,
    file_type: str | None = None,
    uploaded_by_id: Annotated[int | None, Query(ge=1)] = None,

    # Sorting
    sort_by: Literal[
        "id",
        "original_filename",
        "file_type",
        "status",
        "created_at",
    ] = "created_at",

    sort_order: Literal["asc", "desc"] = "desc",
):
    return service.get_all(
        page=page,
        page_size=page_size,
        search=search,
        status=status,
        file_type=file_type,
        uploaded_by_id=uploaded_by_id,
        sort_by=sort_by,
        sort_order=sort_order,
    )

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
