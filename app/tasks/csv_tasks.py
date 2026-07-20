from app.schemas.document_upload import UploadStatus
from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.celery_app import celery

from app.services.csv_processor import CSVProcessor
from app.repositories.upload_file_repository import UploadRepository


@celery.task
def process_csv_file(uploaded_file_id: int):

    db: Session = SessionLocal()

    try:

        repository = UploadRepository(db)

        uploaded_file = repository.get_by_id(uploaded_file_id)

        if not uploaded_file:
            return

        processor = CSVProcessor(db)

        result = processor.process_file(
            uploaded_file.file_path, 
            uploaded_file_id = uploaded_file_id
        )

        repository.update(
            uploaded_file,
            result
        )

    except Exception as ex:

        repository.update(
        uploaded_file,
            {
                "status": UploadStatus.FAILED,
                "error_message": str(ex)
            }
        )

        raise

    finally:

        db.close()

