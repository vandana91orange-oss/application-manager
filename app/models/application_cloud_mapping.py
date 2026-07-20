from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.database import Base


class ApplicationCloudMapping(Base):

    __tablename__ = "application_cloud_mapping"

    id = Column(Integer, primary_key=True, autoincrement=True)

    application_id = Column(
        Integer,
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False
    )

    cloud_id = Column(
        Integer,
        ForeignKey("application_cloud.id", ondelete="CASCADE")
        ,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            "application_id",
            "cloud_id",
            name="uq_application_cloud"
        ),
    )

    application = relationship(
        "Application",
        back_populates="cloud_mappings"
    )

    cloud = relationship(
        "ApplicationCloud",
        back_populates="application_mappings"
    )
