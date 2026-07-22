import math

from app.models.application import Application
from app.repositories.upload_file_repository import UploadRepository
from app.schemas.document_upload import UploadedFileCreate
from app.utils.model_dict import model_to_dict
from fastapi import HTTPException, UploadFile
import os
import uuid
import shutil
from app.tasks.csv_tasks import process_csv_file
from pathlib import Path
from app.services.audit_service import AuditService
from app.repositories.application_repository import ApplicationRepository



UPLOAD_DIR = "documents"
ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

class UploadService:

    def __init__(self, 
                 repository: UploadRepository,
                 audit_service: AuditService
                 ):
        self.repository = repository
        self.audit_service = audit_service
        self.application_repo = ApplicationRepository(repository.db)

    async def create(
        self,
        files: list[UploadFile],
        user,
    ):
        if not files:
            raise HTTPException(
                status_code=400,
                detail="At least one file is required.",
            )

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        created_uploads = []
        saved_paths = []

        try:
            # Validate all files first
            for file in files:
                if not file.filename:
                    raise HTTPException(
                        status_code=400,
                        detail="One of the uploaded files has no filename.",
                    )

                extension = Path(file.filename).suffix.lower()

                if extension not in ALLOWED_EXTENSIONS:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            f"Invalid file '{file.filename}'. "
                            "Only CSV, XLSX and XLS files are allowed."
                        ),
                    )

            # Save each file
            for file in files:
                extension = Path(file.filename).suffix.lower()
                unique_filename = f"{uuid.uuid4()}{extension}"

                file_path = os.path.join(
                    UPLOAD_DIR,
                    unique_filename,
                )

                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

                saved_paths.append(file_path)

                upload_data = UploadedFileCreate(
                    file_name=unique_filename,
                    original_file_name=file.filename,
                    file_path=file_path,
                )

                upload = self.repository.create(
                    file_name=upload_data.file_name,
                    original_file_name=upload_data.original_file_name,
                    file_path=upload_data.file_path,
                    user_id=user.id,
                )

                self.repository.db.flush()

                self.audit_service.log(
                    current_user=user,
                    action="CREATE",
                    module="Upload",
                    description=f"Uploaded file '{file.filename}'",
                    resource_id=upload.id,
                    new_values={
                        "original_file_name": file.filename,
                        "stored_file_name": unique_filename,
                        "file_path": file_path,
                    },
                )

                created_uploads.append(upload)

            self.repository.db.commit()

            for upload in created_uploads:
                self.repository.db.refresh(upload)

            # Trigger processing after successful commit
            for upload in created_uploads:
                process_csv_file.delay(upload.id)

            return created_uploads

        except HTTPException:
            self.repository.db.rollback()

            for path in saved_paths:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except OSError:
                        pass

            raise

        except Exception as exc:
            self.repository.db.rollback()

            for path in saved_paths:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except OSError:
                        pass

            raise HTTPException(
                status_code=500,
                detail=f"Unable to upload files: {str(exc)}",
            )

        finally:
            for file in files:
                await file.close()

    def get_all(
        self,
        page: int = 1,
        page_size: int = 10,
        search: str | None = None,
        status: str | None = None,
        file_type: str | None = None,
        uploaded_by_id: int | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ):
        uploads, total = self.repository.get_all(
            page=page,
            page_size=page_size,
            search=search,
            status=status,
            file_type=file_type,
            uploaded_by_id=uploaded_by_id,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        return {
            "items": uploads,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (
                math.ceil(total / page_size)
                if total > 0
                else 0
            ),
        }

    def get_one(self, upload_id):

        upload = self.repository.get_by_id(upload_id)

        if not upload:
            raise HTTPException(
                404,
                "Upload not found"
            )

        return upload

    def update(
        self,
        upload_id,
        data,
        user
    ):

        upload = self.repository.get_by_id(upload_id)
        old_data = model_to_dict(upload)
        if not upload:
            raise HTTPException(
                404,
                "Upload not found"
            )
        updated = self.repository.update(upload, data)
        self.audit_service.log(
            current_user=user,
            action="UPDATE",
            module="Upload",
            description=f"Updated upload {upload.id}",
            resource_id=upload.id,
            old_values=old_data,
            new_values=model_to_dict(updated)
        )
        self.repository.db.commit()
        return updated

    def delete(self, upload_id: int, user):

        upload = self.repository.get_by_id(upload_id)

        if not upload:
            raise HTTPException(
                status_code=404,
                detail="File not found."
            )

        old_data = model_to_dict(upload)

        try:
            # Delete all applications and their related records
            self.application_repo.delete_by_upload_id(upload.id)

            # Delete upload record
            self.repository.db.delete(upload)           

            # Delete physical file after successful DB commit
            if upload.file_path and os.path.exists(upload.file_path):
                try:
                    os.remove(upload.file_path)
                except OSError:
                    pass

            # Save audit log
            self.audit_service.log(
                current_user=user,
                action="DELETE",
                module="Upload",
                description=f"Deleted upload '{upload.original_file_name}'",
                resource_id=upload.id,
                old_values=old_data
            )
            self.repository.db.commit()
            return {
                "message": "File deleted successfully."
            }

        except Exception:
            self.repository.db.rollback()
            raise
