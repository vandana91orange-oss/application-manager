from app.models.application import Application
from app.models.application_cloud import ApplicationCloud
from app.models.application_cloud_mapping import ApplicationCloudMapping
from app.models.application_migration import Migration
from app.models.audit_logs import AuditLog
from app.models.csv_upload import CSVUploadedFile
from app.models.users import User
from app.schemas.document_upload import UploadStatus
from sqlalchemy import func


class DashboardRepository:

    def __init__(self, db):
        self.db = db

    def get_summary(self):
        return {
            "total_applications": self.db.query(Application).count(),

            "total_uploads": self.db.query(CSVUploadedFile).count(),

            "failed_uploads": self.db.query(CSVUploadedFile)
                .filter(CSVUploadedFile.status == UploadStatus.FAILED)
                .count(),

            "total_users": self.db.query(User).count(),

            "completed_migrations": self.db.query(Migration)
                .filter(Migration.migration_status == "Completed")
                .count(),

            "in_progress_migrations": self.db.query(Migration)
                .filter(Migration.migration_status == "In progress")
                .count(),

            "pending_migrations": self.db.query(Migration)
                .filter(Migration.migration_status == "Pending")
                .count(),
        }
    def migration_chart(self):
        return (
            self.db.query(
                Migration.migration_status,
                func.count(Migration.id)
            )
            .group_by(Migration.migration_status)
            .all()
        )
    def domain_chart(self):
        return (
            self.db.query(
                Application.domain,
                func.count(Application.id)
            )
            .group_by(Application.domain)
            .all()
        )
    
    def cloud_chart(self):
        return (
            self.db.query(
                ApplicationCloud.name.label("cloud"),
                func.count(Application.id).label("count")
            )
            .select_from(ApplicationCloud)
            .join(
                ApplicationCloudMapping,
                ApplicationCloud.id == ApplicationCloudMapping.cloud_id
            )
            .join(
                Application,
                Application.id == ApplicationCloudMapping.application_id
            )
            .group_by(ApplicationCloud.name)
            .all()
        )
    
    def recent_uploads(self):
        uploads = (
            self.db.query(CSVUploadedFile)
            .order_by(CSVUploadedFile.uploaded_at.desc())
            .limit(5)
            .all()
        )

        return [
            {
                "id": u.id,
                "file_name": u.original_file_name,
                "status": u.status,
                "uploaded_by": u.user.first_name,   # relationship
                "created_at": u.uploaded_at
            }
            for u in uploads
        ]

    def recent_logs(self):
        logs = (
            self.db.query(AuditLog, User)
            .join(User, User.id == AuditLog.user_id)
            .order_by(AuditLog.created_at.desc())
            .limit(10)
            .all()
        )

        return [
            {
                "id": log.id,
                "user": f"{user.first_name} {user.last_name}",
                "action": log.action,
                "module": log.module,
                "description": log.description,
                "created_at": log.created_at,
            }
            for log, user in logs
        ]