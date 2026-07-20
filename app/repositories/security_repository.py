from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.application_security import ApplicationSecurity


class SecurityRepository:

    def __init__(
        self,
        db: Session
    ):

        self.db = db

    # ----------------------------------
    # Create Security Record
    # ----------------------------------

    def create(
        self,
        application_id: int,
        data: dict
    ) -> ApplicationSecurity:

        try:

            security = ApplicationSecurity(

                application_id=application_id,

                benchmark_status=data.get(
                    "benchmark_status"
                ),

                nexus_status=data.get(
                    "nexus_status"
                ),

                rooted_status=data.get(
                    "rooted_status"
                ),

                network_policy_status=data.get(
                    "network_policy_status"
                ),

                security_prod_status=data.get(
                    "security_prod_status"
                ),

                security_prod_date=data.get(
                    "security_prod_date"
                )

            )

            self.db.add(security)

            self.db.flush()

            return security

        except SQLAlchemyError:

            self.db.rollback()

            raise

    # ----------------------------------
    # Get By Application
    # ----------------------------------

    def get_by_application(
        self,
        application_id: int
    ) -> Optional[ApplicationSecurity]:

        return (

            self.db.query(ApplicationSecurity)

            .filter(

                ApplicationSecurity.application_id == application_id

            )

            .first()

        )

    # ----------------------------------
    # Get By ID
    # ----------------------------------

    def get_by_id(
        self,
        security_id: int
    ) -> Optional[ApplicationSecurity]:

        return (

            self.db.query(ApplicationSecurity)

            .filter(

                ApplicationSecurity.id == security_id

            )

            .first()

        )

    # ----------------------------------
    # Update Security
    # ----------------------------------

    def update(
        self,
        security: ApplicationSecurity,
        data: dict
    ) -> ApplicationSecurity:

        try:

            for key, value in data.items():
                setattr(security, key, value)
            return security

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
    ) -> ApplicationSecurity:

        security = self.get_by_application(
            application_id
        )

        if security:

            return self.update(
                security,
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

        security = self.get_by_application(
            application_id
        )

        if not security:

            return False

        try:

            self.db.delete(
                security
            )

            self.db.flush()

            return True

        except SQLAlchemyError:

            self.db.rollback()

            raise
