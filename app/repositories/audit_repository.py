from app.models.audit_logs import AuditLog
from sqlalchemy.orm import Session
from sqlalchemy import or_


class AuditRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict):

        log = AuditLog(**data)

        self.db.add(log)
    

    def get_all(
        self,
        page: int = 1,
        size: int = 10,
        user: str | None = None,
        action: str | None = None,
        module: str | None = None,
        search: str | None = None,
        from_date=None,
        to_date=None,
    ):
        query = self.db.query(AuditLog)

        if user:
            query = query.filter(
                AuditLog.user_email.ilike(f"%{user}%")
            )

        if action:
            query = query.filter(
                AuditLog.action == action
            )

        if module:
            query = query.filter(
                AuditLog.module == module
            )

        if search:
            query = query.filter(
                or_(
                    AuditLog.description.ilike(f"%{search}%"),
                    AuditLog.user_email.ilike(f"%{search}%"),
                    AuditLog.resource_id.ilike(f"%{search}%"),
                    AuditLog.module.ilike(f"%{search}%")
                )
            )

        if from_date:
            query = query.filter(
                AuditLog.created_at >= from_date
            )

        if to_date:
            query = query.filter(
                AuditLog.created_at <= to_date
            )

        total = query.count()

        logs = (
            query.order_by(AuditLog.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )

        return logs, total
