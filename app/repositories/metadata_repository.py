from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.application_metadata import ApplicationMetadata


class MetadataRepository:

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
        application_id: int,
        data: dict
    ) -> ApplicationMetadata:

        try:

            meta_data = ApplicationMetadata(

                application_id=application_id,

                dx_uid=data.get(
                    "dx_uid"
                ),

                mcp_id=data.get(
                    "mcp_id"
                ),

                wave=data.get(
                    "wave"
                ),

                gate=data.get(
                    "gate"
                ),

                assessment_status=data.get(
                    "assessment_status"
                ),

                data_anonymization_status=data.get(
                    "data_anonymization_status"
                )

            )

            self.db.add(meta_data)

            self.db.flush()

            return meta_data

        except SQLAlchemyError:

            self.db.rollback()

            raise

    # ----------------------------------
    # Get By Application
    # ----------------------------------

    def get_by_application(
        self,
        application_id: int
    ) -> Optional[ApplicationMetadata]:

        return (

            self.db.query(ApplicationMetadata)

            .filter(

                ApplicationMetadata.application_id == application_id

            )

            .first()

        )

    # ----------------------------------
    # Get By ID
    # ----------------------------------

    def get_by_id(
        self,
        metadata_id: int
    ) -> Optional[ApplicationMetadata]:

        return (

            self.db.query(ApplicationMetadata)

            .filter(

                ApplicationMetadata.id == metadata_id

            )

            .first()

        )

    # ----------------------------------
    # Update Metadata
    # ----------------------------------

    def update(
        self,
        meta_data: ApplicationMetadata,
        data: dict
    ) -> ApplicationMetadata:

        try:

            for key, value in data.items():
                setattr(meta_data, key, value)
            return meta_data

        except SQLAlchemyError:

            self.db.rollback()

            raise

    # ----------------------------------
    # Create Or Update
    # ----------------------------------

    def create_or_update(
        self,
        application_id: int,
        data: dict
    ) -> ApplicationMetadata:

        meta_data = self.get_by_application(
            application_id
        )

        if meta_data:

            return self.update(
                meta_data,
                data
            )

        return self.create(
            application_id,
            data
        )

    # ----------------------------------
    # Delete
    # ----------------------------------

    def delete(
        self,
        application_id: int
    ) -> bool:

        meta_data = self.get_by_application(
            application_id
        )

        if not meta_data:

            return False

        try:

            self.db.delete(meta_data)

            self.db.flush()

            return True

        except SQLAlchemyError:

            self.db.rollback()

            raise