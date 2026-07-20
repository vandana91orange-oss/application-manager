from app.repositories.application_cloud_mapping_repository import ApplicationCloudMappingRepository
from app.repositories.application_cloud_repository import ApplicationCloudRepository
from sqlalchemy.orm import Session

from app.repositories.application_repository import ApplicationRepository
from app.repositories.metadata_repository import MetadataRepository
from app.repositories.migration_repository import MigrationRepository
from app.repositories.owner_repository import OwnerRepository
from app.repositories.security_repository import SecurityRepository
from app.repositories.remark_repository import RemarkRepository

from app.utils.converters import (
    DateConverter,
    PercentageConverter,
    StringConverter,
    to_bool,
)
import re


EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"


class RowProcessor:

    def __init__(
        self,
        db: Session
    ):

        self.db = db

        self.application_repo = ApplicationRepository(db)

        self.owner_repo = OwnerRepository(db)

        self.migration_repo = MigrationRepository(db)

        self.metadata_repo = MetadataRepository(db)

        self.security_repo = SecurityRepository(db)
        self.remark_repo = RemarkRepository(db)

        self.application_cloud_repo = ApplicationCloudRepository(db)

        self.application_cloud_mapping_repo = (
                ApplicationCloudMappingRepository(db)
            )

    # --------------------------------------------------
    # Process Single Row
    # --------------------------------------------------

    def process(
        self,
        row: dict,
        uploaded_file_id: int,
        cloud_name: str
    ):

        if not any(row.values()):

            return

        carto_id = StringConverter.convert(
            row.get("carto_id")
        )

        if not carto_id:

            raise ValueError(
                "Carto ID is required."
            )
        try:
            row["uploaded_file_id"] = uploaded_file_id
            row["out_of_scope"] = to_bool(row.get("out_of_scope"))

            application = self.application_repo.create_or_update(row)

            if cloud_name:

                cloud = self.application_cloud_repo.create_or_update(
                    cloud_name.strip()
                )

                self.application_cloud_mapping_repo.create_or_update(
                    application.id,
                    cloud.id
                )

            self._save_metadata(
                application.id,
                row
            )

            self._save_migration(
                application.id,
                row
            )

            self._save_security(
                application.id,
                row
            )

            self._save_owners(
                application.id,
                row
            )
            self._save_remark(
                application.id,
                row
            )

            self.db.commit()

        except Exception:

            self.db.rollback()

            raise

    # --------------------------------------------------
    # Owners
    # --------------------------------------------------

    def _extract_email(self, text: str) -> str | None:

        if not text:
            return None

        match = re.search(EMAIL_REGEX, text)

        if match:
            return match.group(0)

        return None

    def _save_owners(
        self,
        application_id: int,
        row: dict
    ):

        owners = [

            {
                "owner_type": "Application Manager",
                "owner_name": row.get("application_manager"),
                "owner_email": self._extract_email(
                    row.get("application_manager_email")
                )
            },

            {
                "owner_type": "PM",
                "owner_name": row.get("pm"),
                "owner_email": None
            },

            {
                "owner_type": "DevOps",
                "owner_name": row.get("assigned_devops"),
                "owner_email": None
            },

            {
                "owner_type": "QA",
                "owner_name": row.get("qa"),
                "owner_email": None
            }

        ]

        for owner in owners:

            if not owner["owner_name"]:
                continue

            self.owner_repo.create_or_update(
                application_id=application_id,
                owner_type=owner["owner_type"],
                owner_name=owner["owner_name"],
                owner_email=owner["owner_email"],
            )
    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    def _save_metadata(
        self,
        application_id,
        row
    ):

        self.metadata_repo.create_or_update(

            application_id,
    
            {

                "dx_uid": StringConverter.convert(
                    row.get("dx_uid")
                ),

                "mcp_id": StringConverter.convert(
                    row.get("mcp_id")
                ),

                "wave": StringConverter.convert(
                    row.get("wave")
                ),

                "gate": StringConverter.convert(
                    row.get("gate")
                ),

                "assessment_status": StringConverter.convert(
                    row.get("assessment_status")
                ),

                "data_anonymization_status": StringConverter.convert(
                    row.get("data_anonymization_status")
                ),

            }

        )
    # --------------------------------------------------
    # Migration
    # --------------------------------------------------

    def _save_migration(
        self,
        application_id,
        row
    ):

        self.migration_repo.create_or_update(

            application_id,

            {

                "migration_status": StringConverter.convert(
                    row.get("migration_status")
                ),

                "migration_progress": PercentageConverter.convert(
                    row.get("migration_progress")
                ),

                "hz_strategy": StringConverter.convert(
                    row.get("hz_strategy")
                ),

                "hosting_location": StringConverter.convert(
                    row.get("hosting_location")
                ),

                "cloud_squad": StringConverter.convert(
                    row.get("cloud_squad")
                ),

                "non_production_azure_clusters": StringConverter.convert(
                    row.get("non_production_azure_clusters")
                ),

                "initiated": DateConverter.convert(
                    row.get("initiated")
                ),

                "tentative_start": DateConverter.convert(
                    row.get("tentative_start")
                ),

                "tentative_end_nonprod": DateConverter.convert(
                    row.get("tentative_end_nonprod")
                ),

                "tentative_end_prod": DateConverter.convert(
                    row.get("tentative_end_prod")
                ),

                "total_ns": row.get("total_ns"),

                "ns_migration_progress": StringConverter.convert(
                    row.get("ns_migration_progress")
                ),

                "ns_backup_creation": StringConverter.convert(
                    row.get("ns_backup_creation")
                ),

                "ns_migration_status": StringConverter.convert(
                    row.get("ns_migration_status")
                ),

                "cluster": StringConverter.convert(
                    row.get("cluster")
                ),

            }

        )

    # --------------------------------------------------
    # Security
    # --------------------------------------------------

    def _save_security(
        self,
        application_id,
        row
    ):

        self.security_repo.create_or_update(

            application_id,

            {

                "benchmark_status": StringConverter.convert(
                    row.get("benchmark_status")
                ),

                "nexus_status": StringConverter.convert(
                    row.get("nexus_status")
                ),

                "rooted_status": StringConverter.convert(
                    row.get("rooted_status")
                ),

                "network_policy_status": StringConverter.convert(
                    row.get("network_policy_status")
                ),

                "security_prod_status": StringConverter.convert(
                    row.get("security_prod_status")
                ),

                "security_prod_date": DateConverter.convert(
                    row.get("security_prod_date")
                ),

            }

        )


    def _save_remark(
        self,
        application_id: int,
        row: dict
    ):
        converted = to_bool(
                    row.get("out_of_scope")
                )
        self.remark_repo.create_or_update(

            application_id,

            {

                "remark": StringConverter.convert(
                    row.get("remark")
                ),

                "remarks_imp": StringConverter.convert(
                    row.get("remarks_imp")
                ),

                "source_comments": StringConverter.convert(
                    row.get("source_comments")
                ),

                "archived_remarks": StringConverter.convert(
                    row.get("archived_remarks")
                ),

                "out_of_scope":converted

            }

        )
