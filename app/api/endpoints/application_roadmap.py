from pathlib import Path
from tempfile import NamedTemporaryFile

from app.services.roadmap_query_service import get_application_with_all_roadmap_details, patch_application_roadmap_detail
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.application import Application
from app.models.application_roadmap import (
    ApplicationRoadmapImport,
)
from app.schemas.application_roadmap import (
    ApplicationRoadmapCompleteResponse,
    RoadmapDetailPatchRequest,
    RoadmapDetailResponse,
    RoadmapImportResponse,
    RoadmapImportStatusResponse,
)
from app.services.roadmap_import_service import (
    process_roadmap_excel_background,
)


router = APIRouter(
    prefix="/roadmap",
    tags=["Application Roadmap"],
)

ALLOWED_EXTENSIONS = {
    ".xlsx",
    ".xlsm",
}

MAX_FILE_SIZE = 20 * 1024 * 1024


@router.post(
    "/{application_id}/roadmap/import",
    response_model=RoadmapImportResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_application_roadmap(
    application_id: int,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    replace_existing: bool = Query(default=False),
    db: Session = Depends(get_db),
):
    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .one_or_none()
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )

    original_filename = (
        file.filename or "application_roadmap.xlsx"
    )

    extension = Path(
        original_filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Only .xlsx and .xlsm Excel files "
                "are supported."
            ),
        )

    file_content = await file.read()

    if not file_content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded Excel file is empty.",
        )

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Excel file cannot exceed 20 MB.",
        )

    temporary_file = NamedTemporaryFile(
        mode="wb",
        suffix=extension,
        prefix=f"application_{application_id}_roadmap_",
        delete=False,
    )

    try:
        temporary_file.write(file_content)
        temporary_file.flush()
        temporary_file_path = temporary_file.name

    finally:
        temporary_file.close()

    import_record = ApplicationRoadmapImport(
        application_id=application_id,
        original_filename=original_filename,
        stored_file_path=temporary_file_path,
        import_status="PENDING",
    )

    db.add(import_record)
    db.commit()
    db.refresh(import_record)

    background_tasks.add_task(
        process_roadmap_excel_background,
        import_record.id,
        application_id,
        temporary_file_path,
        replace_existing,
    )

    return RoadmapImportResponse(
        import_id=import_record.id,
        application_id=application_id,
        filename=original_filename,
        status="PENDING",
        message=(
            "Excel file uploaded successfully. "
            "Extraction is running in the background."
        ),
    )


@router.get(
    "/{application_id}/roadmap/imports/{import_id}",
    response_model=RoadmapImportStatusResponse,
)
def get_roadmap_import_status(
    application_id: int,
    import_id: int,
    db: Session = Depends(get_db),
):
    import_record = (
        db.query(ApplicationRoadmapImport)
        .filter(
            ApplicationRoadmapImport.id == import_id,
            ApplicationRoadmapImport.application_id
            == application_id,
        )
        .one_or_none()
    )

    if import_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Roadmap import was not found.",
        )

    return import_record


@router.get(
    "/applications/{application_id}/roadmap-details",
    response_model=ApplicationRoadmapCompleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Get application roadmap",
)
def get_application_roadmap_details(
    application_id: int,
    db: Session = Depends(get_db),
):
    result = get_application_with_all_roadmap_details(
        db=db,
        application_id=application_id,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )

    return result


@router.patch(
    "/applications/{application_id}/"
    "roadmap-details/{roadmap_detail_id}",
    response_model=RoadmapDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a roadmap detail",
)
def patch_roadmap_detail(
    application_id: int,
    roadmap_detail_id: int,
    payload: RoadmapDetailPatchRequest,
    db: Session = Depends(get_db),
) -> RoadmapDetailResponse:
    try:
        result = (
            patch_application_roadmap_detail(
                db=db,
                application_id=application_id,
                roadmap_detail_id=(
                    roadmap_detail_id
                ),
                payload=payload,
            )
        )

    except ValueError as error:
        raise HTTPException(
            status_code=(
                status.HTTP_400_BAD_REQUEST
            ),
            detail=str(error),
        ) from error

    if result is None:
        raise HTTPException(
            status_code=(
                status.HTTP_404_NOT_FOUND
            ),
            detail=(
                "Roadmap detail was not found "
                "for the specified application."
            ),
        )

    return result
