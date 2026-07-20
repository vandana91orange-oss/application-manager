from app.models.application import Application
from app.repositories.upload_file_repository import UploadRepository
from app.utils.model_dict import model_to_dict
from fastapi import HTTPException
import os
import uuid
import shutil
from app.tasks.csv_tasks import process_csv_file
from pathlib import Path
from app.services.audit_service import AuditService
from app.repositories.application_repository import ApplicationRepository



UPLOAD_DIR = "documents"
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
        file,
        user
    ):

        allowed_extensions = (".csv", ".xlsx", ".xls")

        if not file.filename.lower().endswith(allowed_extensions):
            raise HTTPException(
                status_code=400,
                detail="Only CSV, XLSX and XLS files are allowed."
            )

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        extension = Path(file.filename).suffix.lower()

        unique_filename = f"{uuid.uuid4()}{extension}"

        file_path = os.path.join(
            UPLOAD_DIR,
            unique_filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        upload = self.repository.create(
            file_name=unique_filename,
            original_file_name=file.filename,
            file_path=file_path,
            user_id=user.id
        )
        
        self.audit_service.log(
            current_user=user,
            action="CREATE",
            module="Upload",
            description=f"Uploaded file '{file.filename}'",
            resource_id=upload.id,
            new_values={
                "file_name": file.filename,
                "stored_name": unique_filename
            }
        )
        self.repository.db.commit() 
        process_csv_file.delay(upload.id)
        return upload

    def get_all(self):
        return self.repository.get_all()

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
