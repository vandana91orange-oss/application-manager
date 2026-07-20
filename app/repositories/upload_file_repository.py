from app.models.csv_upload import CSVUploadedFile


class UploadRepository:

    def __init__(self, db):
        self.db = db

    def create(
        self,
        file_name,
        original_file_name,
        file_path,
        user_id
    ):

        upload = CSVUploadedFile(
            file_name=file_name,
            original_file_name=original_file_name,
            file_path=file_path,
            uploaded_by=user_id,
            status="PROCESSING"
        )

        self.db.add(upload)
        self.db.commit()
        self.db.refresh(upload)
        return upload

    def get_all(self):
        return self.db.query(CSVUploadedFile).all()

    def get_by_id(self, upload_id):
        return (
            self.db.query(CSVUploadedFile)
            .filter(CSVUploadedFile.id == upload_id)
            .first()
        )

    def update(self, upload, data):

        upload.status = data.get("status")

        self.db.commit()
        self.db.refresh(upload)

        return upload

    def delete(self, upload_id):
        upload = (
            self.db.query(CSVUploadedFile)
            .filter(CSVUploadedFile.id == upload_id.id)
            .first()
        )
        if upload:
            self.db.delete(upload)
            self.db.commit()
