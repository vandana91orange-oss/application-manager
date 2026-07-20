from typing import Optional

from app.models.application_cloud import ApplicationCloud
from app.models.application_cloud_mapping import ApplicationCloudMapping
from app.models.application_migration import Migration
from app.models.application_owner import ApplicationOwner
from app.models.application_remark import ApplicationRemark
from app.models.application_security import ApplicationSecurity
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from app.models.application import Application


def to_dict(obj):
    if obj is None:
        return None

    return {
        column.name: getattr(obj, column.name)
        for column in obj.__table__.columns
    }


class ApplicationRepository:

    def __init__(self, db: Session):

        self.db = db

    # -----------------------------
    # Create
    # -----------------------------
    def create(
        self,
        data: dict
    ) -> Application:

        try:
            

            application = Application(

                carto_id=data.get("carto_id"),
                application_name=data.get("application_name"),
                basicat=data.get("basicat"),
                domain=data.get("domain"),
                portfolio=data.get("portfolio"),
                confirmed_domain = data.get("confirmed_domain"),
                business_importance=data.get(
                    "business_importance"
                ),
                sov_type=data.get("sov_type"),
                uploaded_file_id=data.get(
                    "uploaded_file_id"
                ),
                application_status=data.get("application_status"),
                priority = data.get("priority")


            )

            self.db.add(application)

            self.db.flush()

            return application

        except SQLAlchemyError:

            self.db.rollback()

            raise

    # -----------------------------
    # Get by Carto ID
    # -----------------------------
    def get_by_carto_id(
        self,
        carto_id: str
    ) -> Optional[Application]:

        return (

            self.db.query(Application)

            .filter(

                Application.carto_id == carto_id

            )

            .first()

        )

    # -----------------------------
    # Get by ID
    # -----------------------------
    def get_by_id(
        self,
        application_id: int
    ) -> Optional[Application]:

        return (

            self.db.query(Application)

            .filter(

                Application.id == application_id

            )

            .first()

        )

    # -----------------------------
    # Get All
    # -----------------------------
    def get_all(self):

        return (

            self.db.query(Application)

            .order_by(

                Application.application_name

            )

            .all()

        )

    # -----------------------------
    # Update
    # -----------------------------
    def update(
        self,
        application: Application,
        data: dict
    ) -> Application:

        try:
            for key, value in data.items():
                setattr(application, key, value)

            self.db.flush()
            return application

        except SQLAlchemyError:

            self.db.rollback()

            raise

    # -----------------------------
    # Delete
    # -----------------------------
    def delete(
        self,
        application_id: int
    ) -> bool:

        application = self.get_by_id(
            application_id
        )

        if not application:

            return False

        try:

            self.db.delete(application)

            self.db.commit()

            return True

        except SQLAlchemyError:

            self.db.rollback()

            raise
    
    def delete_by_upload_id(self, upload_id: int):

        applications = (
            self.db.query(Application)
            .filter(Application.uploaded_file_id == upload_id)
            .all()
        )

        for application in applications:
            self.db.delete(application)

        self.db.flush()
    # -----------------------------
    # Upsert
    # -----------------------------
    def create_or_update(
        self,
        data: dict
    ) -> Application:

        application = self.get_by_carto_id(

            data.get("carto_id")

        )

        if application:

            return self.update(

                application,

                data

            )

        return self.create(data)


    def get_applications(
        self,
        page: int,
        size: int,
        search: str | None = None,
        cloud: str | None = None,
        owner: str | None = None,
        domain: str | None = None,
    ):

        query = (
            self.db.query(Application)
            .options(
                joinedload(Application.migration),
                joinedload(Application.security),
                joinedload(Application.meta_data),
                joinedload(Application.owners),
                joinedload(Application.remarks),
                joinedload(Application.cloud_mappings)
                .joinedload(ApplicationCloudMapping.cloud)
            )
        )

        # Join once if either search or cloud filter needs it
        if search or cloud:
            query = (
                query.outerjoin(ApplicationCloudMapping)
                    .outerjoin(ApplicationCloud)
            )

        if search:
            query = query.filter(
                or_(
                    Application.application_name.ilike(f"%{search}%"),
                    Application.carto_id.ilike(f"%{search}%"),
                    ApplicationCloud.name.ilike(f"%{search}%"),
                )
            )

        if cloud:
            query = query.filter(
                ApplicationCloud.name.ilike(f"%{cloud}%")
            )

        if owner:
            query = query.join(ApplicationOwner).filter(
                ApplicationOwner.owner_name.ilike(f"%{owner}%")
            )

        if domain:
            query = query.filter(
                Application.domain.ilike(f"%{domain}%")
            )

        total = query.distinct().count()

        applications = (
            query.distinct()
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )

        return {
            "page": page,
            "size": size,
            "total": total,
            "data": applications,
        }
    def export(
        self,
        search=None,
        cloud=None,
        owner=None,
        domain=None,
    ):

        query = self.db.query(Application)

        query = query.outerjoin(Application.owners)
        query = query.outerjoin(Application.migration)
        query = query.outerjoin(Application.security)
        query = query.outerjoin(Application.meta_data)
        query = query.outerjoin(Application.remarks)
        query = query.outerjoin(Application.cloud_mappings)

        if search:
            query = query.filter(
                Application.application_name.ilike(f"%{search}%")
            )

        if domain:
            query = query.filter(
                Application.domain == domain
            )

        if owner:
            query = query.filter(
                ApplicationOwner.owner_name.ilike(f"%{owner}%")
            )

        if cloud:
            query = (
                query.join(ApplicationCloudMapping)
                    .join(ApplicationCloud)
                    .filter(ApplicationCloud.name == cloud)
            )

        return query.distinct().all()
    