from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func,
    Boolean
)
from sqlalchemy.orm import relationship
from app.database import Base


class Application(Base):

    __tablename__="applications"

    id = Column(Integer, primary_key=True)
    carto_id = Column(String(50), unique=True)
    application_name = Column(String(255))
    basicat = Column(String(100))
    domain = Column(String(150))
    portfolio = Column(String(150))
    business_importance = Column(String(100))
    sov_type = Column(String(50))
    uploaded_file_id = Column(
        Integer,
        ForeignKey("csv_uploaded_files.id")
    )
    priority = Column(String(50))

    confirmed_domain = Column(String(150))

    application_status = Column(String(100))

    out_of_scope = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    owners = relationship(
                "ApplicationOwner",
                back_populates="application",
                cascade="all, delete-orphan"
            )

    migration = relationship(
        "Migration",
        back_populates="application",
        uselist=False,
        cascade="all, delete-orphan"
    )

    meta_data = relationship(
        "ApplicationMetadata",
        back_populates="application",
        uselist=False,
        cascade="all, delete-orphan"
    )

    security = relationship(
        "ApplicationSecurity",
        back_populates="application",
        uselist=False,
        cascade="all, delete-orphan"
    )

    remarks = relationship(
        "ApplicationRemark",
        back_populates="application",
        cascade="all, delete-orphan"
    )
    cloud_mappings = relationship(
        "ApplicationCloudMapping",
        back_populates="application",
        cascade="all, delete-orphan"
    )
