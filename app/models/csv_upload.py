from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


class CSVUploadedFile(Base):
    __tablename__ = "csv_uploaded_files"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    file_name = Column(
        String(255),
        nullable=False
    )

    original_file_name = Column(
        String(255),
        nullable=True
    )

    file_path = Column(
        String(500),
        nullable=False
    )

    status = Column(
        String(50),
        default="PROCESSING"
    )

    total_rows = Column(
        Integer,
        default=0
    )

    processed_rows = Column(
        Integer,
        default=0
    )

    failed_rows = Column(
        Integer,
        default=0
    )

    uploaded_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    user = relationship("User")
