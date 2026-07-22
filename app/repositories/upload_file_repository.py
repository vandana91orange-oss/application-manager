from app.models.csv_upload import CSVUploadedFile
from app.models.users import User
from sqlalchemy import func, or_, select


class UploadRepository:

    def __init__(self, db):
        self.db = db

    SORTABLE_COLUMNS = {
        "id": CSVUploadedFile.id,
        "status": CSVUploadedFile.status,
        "file_name": CSVUploadedFile.file_name,
        "uploaded_by": CSVUploadedFile.uploaded_by,
        "uploaded_at": CSVUploadedFile.uploaded_at
    }
    
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
    ) -> tuple[list[CSVUploadedFile], int]:

        filters = []

        # Searching
        if search:
            normalized_search = search.strip()

            if normalized_search:
                search_pattern = f"%{normalized_search}%"

                filters.append(
                    or_(
                        CSVUploadedFile.original_filename.ilike(
                            search_pattern
                        ),
                        CSVUploadedFile.file_type.ilike(
                            search_pattern
                        ),
                        CSVUploadedFile.status.ilike(
                            search_pattern
                        ),
                    )
                )

        # Filtering
        if status:
            filters.append(
                CSVUploadedFile.status == status
            )

        if file_type:
            filters.append(
                CSVUploadedFile.file_type == file_type
            )

        if uploaded_by_id is not None:
            filters.append(
                CSVUploadedFile.uploaded_by_id == uploaded_by_id
            )

        # Count filtered records
        count_statement = (
            select(func.count(CSVUploadedFile.id))
            .select_from(CSVUploadedFile)
            .where(*filters)
        )

        total = self.db.scalar(count_statement) or 0

        # Safe sorting
        sort_column = self.SORTABLE_COLUMNS.get(
            sort_by,
            CSVUploadedFile.uploaded_at,
        )

        if sort_order.lower() == "asc":
            order_expression = sort_column.asc()
        else:
            order_expression = sort_column.desc()

        offset = (page - 1) * page_size

        statement = (
            select(CSVUploadedFile)
            .where(*filters)
            .order_by(
                order_expression,
                CSVUploadedFile.id.desc(),
            )
            .offset(offset)
            .limit(page_size)
        )

        uploads = self.db.scalars(statement).all()

        return list(uploads), total

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

