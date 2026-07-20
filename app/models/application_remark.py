from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    Text,
    func
)
from sqlalchemy.orm import relationship
from app.database import Base


class ApplicationRemark(Base):

    __tablename__="application_remarks"

    id=Column(Integer,primary_key=True)

    application_id=Column(
        Integer,
        ForeignKey("applications.id")
    )

    remark=Column(Text)
    remarks_imp = Column(Text)
    source_comments = Column(Text)
    archived_remarks = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    application = relationship(
            "Application",
            back_populates="remarks"
        )
