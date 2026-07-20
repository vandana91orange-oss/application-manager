from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,

)
from sqlalchemy.orm import relationship

from app.database import Base

from sqlalchemy.orm import relationship, foreign

class ApplicationOwner(Base):

    __tablename__ = "application_owners"

    id = Column(Integer, primary_key=True)

    application_id = Column(
        Integer,
        ForeignKey("applications.id")
    )

    owner_type = Column(String(50))
    owner_name = Column(String(255))
    owner_email = Column(String(255))

    application = relationship(
        "Application",
        back_populates="owners"
    )

    user = relationship(
        "User",
        primaryjoin="foreign(ApplicationOwner.owner_email) == User.email",
        back_populates="owned_applications",
        viewonly=True
    )