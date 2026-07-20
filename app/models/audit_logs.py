from app.database import Base
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    func,
    String,
    Text,
    JSON
)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    user_email = Column(String(255))

    role = Column(String(50))

    action = Column(String(50))

    module = Column(String(100))

    resource_id = Column(String(100))

    description = Column(Text)

    old_values = Column(JSON)

    new_values = Column(JSON)

    ip_address = Column(String(50))

    user_agent = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )