from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.application_migration import Migration


class MigrationRepository:

    def __init__(
        self,
        db: Session
    ):

        self.db = db

    # ----------------------------------
    # Create Migration
    # ----------------------------------

    def create(
        self,
        application_id: int,
        data: dict
    ) -> Migration:

        try:

            migration = Migration(
                application_id=application_id,
                migration_status=data.get("migration_status"),
                migration_progress=data.get("migration_progress"),
                strategy=data.get("hz_strategy"),
                hosting_location=data.get("hosting_location"),
                cloud_squad=data.get("cloud_squad"),
                initiated=data.get("initiated"),
                tentative_start=data.get("tentative_start"),
                tentative_end=data.get("tentative_end_nonprod"),
                confirmed_end=data.get("tentative_end_prod"),
                go_live=data.get("security_prod_date"),

                total_ns=data.get("total_ns"),
                ns_migration_progress=data.get("ns_migration_progress"),
                ns_migration_status=data.get("ns_migration_status"),
                non_production_azure_clusters=data.get("non_production_azure_clusters"),
                cluster=data.get("cluster"),
                ns_backup_creation=data.get("ns_backup_creation"),
            )

            self.db.add(migration)

            self.db.flush()

            return migration

        except SQLAlchemyError:

            self.db.rollback()

            raise

    # ----------------------------------
    # Get Migration
    # ----------------------------------

    def get_by_application(
        self,
        application_id: int
    ) -> Optional[Migration]:

        return (

            self.db.query(Migration)

            .filter(

                Migration.application_id == application_id

            )

            .first()

        )

    # ----------------------------------
    # Get By ID
    # ----------------------------------

    def get_by_id(
        self,
        migration_id: int
    ) -> Optional[Migration]:

        return (

            self.db.query(Migration)

            .filter(

                Migration.id == migration_id

            )

            .first()

        )

    # ----------------------------------
    # Update Migration
    # ----------------------------------

    def update(
        self,
        migration: Migration,
        data: dict
    ) -> Migration:

        try:

            for key, value in data.items():
                setattr(migration, key, value)
            return migration

        except SQLAlchemyError:
            self.db.rollback()
            raise
    # ----------------------------------
    # Create or Update
    # ----------------------------------

    def create_or_update(
        self,
        application_id: int,
        data: dict
    ) -> Migration:

        migration = self.get_by_application(
            application_id
        )

        if migration:

            return self.update(
                migration,
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

        migration = self.get_by_application(
            application_id
        )

        if not migration:

            return False

        try:

            self.db.delete(
                migration
            )

            self.db.flush()

            return True

        except SQLAlchemyError:

            self.db.rollback()

            raise
