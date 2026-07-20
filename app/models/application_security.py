from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date
)
from sqlalchemy.orm import relationship

from app.database import Base


class ApplicationSecurity(Base):

    __tablename__="application_security"

    id=Column(Integer,primary_key=True)

    application_id=Column(
        Integer,
        ForeignKey("applications.id")
    )

    benchmark_status=Column(String(50))

    nexus_status=Column(String(50))

    rooted_status=Column(String(50))

    security_prod_status=Column(String(50))
    network_policy_status = Column(String(100))

    security_prod_date = Column(Date)
    application = relationship(
            "Application",
            back_populates="security"
        )