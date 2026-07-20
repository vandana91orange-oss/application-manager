from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    func

)
from sqlalchemy.orm import relationship
from app.database import Base


class ApplicationCloud(Base):

    __tablename__ = "application_cloud"

    id=Column(Integer,primary_key=True)
    name=Column(String(200), unique=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    application_mappings = relationship(
        "ApplicationCloudMapping",
        back_populates="cloud",
        cascade="all, delete-orphan"
    )
