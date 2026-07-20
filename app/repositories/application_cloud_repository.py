from typing import Optional

from app.models.application import Application
from app.models.application_cloud_mapping import ApplicationCloudMapping
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload


from app.models.application_cloud import ApplicationCloud


class ApplicationCloudRepository:

    def __init__(
        self,
        db: Session
    ):

        self.db = db

    # ----------------------------------
    # Create Metadata
    # ----------------------------------

    def create(
        self,
        name
    ) -> ApplicationCloud:

        try:
            app_cloud = ApplicationCloud(
                name=name
            )

            self.db.add(app_cloud)
            self.db.flush()
            return app_cloud

        except SQLAlchemyError:
            self.db.rollback()

            raise

    # ----------------------------------
    # Get By ID
    # ----------------------------------

    def get_by_id(
        self,
        id: int
    ) -> Optional[ApplicationCloud]:

        return (

            self.db.query(ApplicationCloud)

            .filter(

                ApplicationCloud.id == id

            )

            .first()

        )

    # ----------------------------------
    # Update Metadata
    # ----------------------------------

    def update(
        self,
        app_cloud: ApplicationCloud,
        name: str
    ) -> ApplicationCloud:

        try:

            app_cloud.name = name
            self.db.flush()

            return app_cloud

        except SQLAlchemyError:

            self.db.rollback()
            raise
    

    def get_by_cloud_name(
            self,
            name: str
    ):
        return self.db.query(ApplicationCloud).filter(
                ApplicationCloud.name == name
            ).first()
    

    # ----------------------------------
    # Create Or Update
    # ----------------------------------
    def create_or_update(
        self,
        name: str
    ):

        app_cloud = self.get_by_cloud_name(name)

        if app_cloud:
            return app_cloud

        return self.create(name)

    # ----------------------------------
    # Delete
    # ----------------------------------

    def delete(
        self,
        id: int
    ) -> bool:

        app_cloud = self.get_by_id(id)
        if not app_cloud:

            return False

        try:

            self.db.delete(app_cloud)

            self.db.flush()

            return True

        except SQLAlchemyError:

            self.db.rollback()

            raise
    
    def get_by_cloud(
        self,
        cloud_id: int
    ):

        return (
            self.db.query(Application)
            .join(
                ApplicationCloudMapping,
                Application.id == ApplicationCloudMapping.application_id
            )
            .filter(
                ApplicationCloudMapping.cloud_id == cloud_id
            )
            .all()
        )

    def get_all_cloud(self):
        return (
            self.db.query(ApplicationCloud)
            .order_by(ApplicationCloud.name)
            .all()
        )

