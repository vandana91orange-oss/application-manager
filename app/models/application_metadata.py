from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,

)
from sqlalchemy.orm import relationship
from app.database import Base


class ApplicationMetadata(Base):

    __tablename__="application_metadata"

    id=Column(Integer,primary_key=True)

    application_id=Column(
        Integer,
        ForeignKey("applications.id")
    )

    dx_uid=Column(String(200))
    mcp_id=Column(String(200))
    wave=Column(String(50))
    gate=Column(String(50))
    assessment_status = Column(String(100))

    data_anonymization_status = Column(String(100))
    application = relationship(
            "Application",
            back_populates="meta_data"
        )
