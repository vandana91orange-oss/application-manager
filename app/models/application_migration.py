from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    DateTime
)
from sqlalchemy.orm import relationship
from app.database import Base


class Migration(Base):

    __tablename__="application_migrations"

    id=Column(Integer,primary_key=True)

    application_id=Column(
        Integer,
        ForeignKey("applications.id")
    )

    migration_status=Column(String(100))

    migration_progress=Column(Integer)

    strategy=Column(String(100))

    hosting_location=Column(String(100))

    cloud_squad=Column(String(100))

    initiated=Column(Date)

    tentative_start=Column(Date)

    tentative_end=Column(Date)

    confirmed_end=Column(Date)

    go_live=Column(Date)
    non_production_azure_clusters = Column(String(255))
    total_ns = Column(Integer)
    ns_migration_progress = Column(String(100))

    tentative_end_nonprod = Column(DateTime, nullable=True)

    tentative_end_prod = Column(DateTime, nullable=True)

    ns_backup_creation = Column(String(255))

    ns_migration_status = Column(String(100))

    cluster = Column(String(100))

    application = relationship(
            "Application",
            back_populates="migration"
        )