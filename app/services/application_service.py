from app.repositories.application_cloud_mapping_repository import ApplicationCloudMappingRepository
from app.repositories.metadata_repository import MetadataRepository
from app.repositories.migration_repository import MigrationRepository
from app.repositories.owner_repository import OwnerRepository
from app.repositories.remark_repository import RemarkRepository
from app.repositories.security_repository import SecurityRepository
from app.schemas.application import ApplicationCreate, ApplicationDetailsResponse, ApplicationUpdate
from app.services.audit_service import AuditService
from app.utils.model_dict import model_to_dict
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
import io
import pandas as pd
from fastapi.responses import StreamingResponse
from app.repositories.application_repository import ApplicationRepository
from app.repositories.application_cloud_repository import (
    ApplicationCloudRepository
)
from sqlalchemy.orm import Session


class ApplicationService:

    def __init__(
        self,
        db: Session,
        application_repo: ApplicationRepository,
        metadata_repo: MetadataRepository,
        migration_repo: MigrationRepository,
        security_repo: SecurityRepository,
        remark_repo: RemarkRepository,
        owner_repo: OwnerRepository,
        cloud_repo: ApplicationCloudRepository,
        cloud_mapping_repo: ApplicationCloudMappingRepository,
        audit_service: AuditService,

    ):
        self.db = db
        self.application_repo = application_repo
        self.metadata_repo = metadata_repo
        self.migration_repo = migration_repo
        self.security_repo = security_repo
        self.remark_repo = remark_repo
        self.owner_repo = owner_repo
        self.cloud_repo = cloud_repo
        self.cloud_mapping_repo = cloud_mapping_repo
        self.audit_service = audit_service

    # ----------------------------------
    # Get All
    # ----------------------------------

    def get_all(self):

        return self.cloud_repository.get_all_cloud()

    # ----------------------------------
    # Get By ID
    # ----------------------------------

    def get_by_id(
        self,
        application_id: int
    ):

        application = self.application_repo.get_by_id(
            application_id
        )

        if not application:

            raise HTTPException(
                status_code=404,
                detail="Application not found."
            )

        return application

    # ----------------------------------
    # Get By Cloud
    # ----------------------------------

    def get_by_cloud(
        self,
        cloud_id: int
    ):

        cloud = self.cloud_repository.get_by_id(
            cloud_id
        )

        if not cloud:

            raise HTTPException(
                status_code=404,
                detail="Cloud not found."
            )

        applications = self.application_repo.get_by_cloud(
            cloud_id
        )

        return {
            "cloud_id": cloud.id,
            "cloud_name": cloud.name,
            "total_applications": len(applications),
            "applications": applications
        }

    # ----------------------------------
    # Delete
    # ----------------------------------

    def delete(
        self,
        application_id: int,
        current_user
    ):

        application = self.application_repo.get_by_id(
            application_id
        )

        if not application:

            raise HTTPException(
                status_code=404,
                detail="Application not found."
            )



        old_data = model_to_dict(application)

        self.application_repo.delete(application.id)
        self.application_repo.db.commit()

        self.audit_service.log(
            current_user=current_user,
            action="DELETE",
            module="Application",
            description=f"Deleted application {application.application_name}",
            resource_id=application.id,
            old_values=old_data,
        )

        self.db.commit()
        return {
            "message": "Application deleted successfully."
        }

    def get_applications_by_cloud(
        self,
        page: int,
        size: int,
        search: str | None = None,
        cloud: str | None = None,
        owner: str | None = None,
        domain: str | None = None,
    ):
        return self.application_repo.get_applications(
            page=page,
            size=size,
            search=search,
            cloud=cloud,
            owner=owner,
            domain=domain,
        )
    
    def update(
        self,
        application_id: int,
        request: ApplicationUpdate,
        current_user
    ):
        application = self.application_repo.get_by_id(application_id)

        if not application:
            raise HTTPException(
                status_code=404,
                detail="Application not found."
            )

        # Before update
        old_data = model_to_dict(application)

        # Update application
        self.application_repo.update(
            application,
            request.application.model_dump(
                exclude_unset=True,
                exclude_none=True
            )
        )

        # Update related entities
        if request.meta_data is not None:
            self.metadata_repo.create_or_update(
                application.id,
                request.meta_data.model_dump(
                    exclude_unset=True,
                    exclude_none=True
                )
            )

        if request.migration is not None:
            self.migration_repo.create_or_update(
                application.id,
                request.migration.model_dump(
                    exclude_unset=True,
                    exclude_none=True
                )
            )

        if request.security is not None:
            self.security_repo.create_or_update(
                application.id,
                request.security.model_dump(
                    exclude_unset=True,
                    exclude_none=True
                )
            )

        if request.remark is not None:
            self.remark_repo.create_or_update(
                application.id,
                request.remark.model_dump(
                    exclude_unset=True,
                    exclude_none=True
                )
            )

        if request.owners is not None:
            self.owner_repo.replace_all(
                application.id,
                request.owners
            )

        if request.cloud_ids is not None:
            self.cloud_mapping_repo.replace_all(
                application.id,
                request.cloud_ids
            )

        # Flush so relationships/updates are reflected
        self.db.flush()

        # Capture new state
        new_data = model_to_dict(application)

        # Audit
        self.audit_service.log(
            current_user=current_user,
            action="UPDATE",
            module="Application",
            description=f"Updated application '{application.application_name}'",
            resource_id=application.id,
            old_values=old_data,
            new_values=new_data,
        )

        self.db.commit()
        self.db.refresh(application)

        return self.build_application_response(application)


    def build_application_response(
        self,
        application
    ):

        return ApplicationDetailsResponse(
            application=application,
            meta_data=application.meta_data,
            migration=application.migration,
            security=application.security,
            remark=application.remarks,
            owners=application.owners,
            clouds=[
                mapping.cloud
                for mapping in application.cloud_mappings
            ]
        )

    def create(
        self,
        request: ApplicationCreate,
        current_user
    ):

        try:

            existing_application = self.application_repo.get_by_carto_id(
                request.application.carto_id
            )

            if existing_application:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Application with Carto ID '{request.application.carto_id}' already exists."
                )
            # ----------------------------
            # Create Application
            # ----------------------------

            application = self.application_repo.create(
                request.application.model_dump()
            )

            application_id = application.id

            # ----------------------------
            # Metadata
            # ----------------------------

            self.metadata_repo.create(
                application_id,
                request.meta_data.model_dump()
            )

            # ----------------------------
            # Migration
            # ----------------------------

            self.migration_repo.create(
                application_id,
                request.migration.model_dump()
            )

            # ----------------------------
            # Security
            # ----------------------------

            self.security_repo.create(
                application_id,
                request.security.model_dump()
            )

            # ----------------------------
            # Remark
            # ----------------------------

            self.remark_repo.create_or_update(
                application_id,
                request.remark.model_dump()
            )

            # ----------------------------
            # Owners
            # ----------------------------

            for owner in request.owners:

                self.owner_repo.create(
                    application_id,
                    owner.model_dump()
                )

            # ----------------------------
            # Cloud Mapping
            # ----------------------------

            for cloud_id in request.cloud_ids:

                self.cloud_mapping_repo.create(
                    application_id=application_id,
                    cloud_id=cloud_id
                )

            new_data = model_to_dict(application)

             # Audit
            self.audit_service.log(
                current_user=current_user,
                action="UPDATE",
                module="Application",
                description=f"Updated application '{application.application_name}'",
                resource_id=application.id,
                new_values=new_data,
            )

            self.db.commit()

            self.db.refresh(application)

            return self.build_application_response(
                application
            )

        except SQLAlchemyError as ex:

            self.db.rollback()

            raise HTTPException(
                status_code=500,
                detail=str(ex)
            )

    def export_csv(
        self,
        search=None,
        cloud=None,
        owner=None,
        domain=None,
    ):
        applications = self.application_repo.export(
            search=search,
            cloud=cloud,
            owner=owner,
            domain=domain,
        )

        rows = []

        for app in applications:

            rows.append({
                "Carto ID": app.carto_id,
                "Application Name": app.application_name,
                "BASICAT": app.basicat,
                "Domain": app.domain,
                "Portfolio": app.portfolio,
                "Business Importance": app.business_importance,
                "SOV Type": app.sov_type,
                "Priority": app.priority,
                "Application Status": app.application_status,
                "Confirmed Domain": app.confirmed_domain,
                "Out Of Scope": app.out_of_scope,

                "Migration Status": app.migration.migration_status if app.migration else "",
                "Migration Progress": app.migration.migration_progress if app.migration else "",

                "Benchmark Status": app.security.benchmark_status if app.security else "",
                "Nexus Status": app.security.nexus_status if app.security else "",

                "Wave": app.meta_data.wave if app.meta_data else "",
                "Assessment Status": app.meta_data.assessment_status if app.meta_data else "",

                "Remark": app.remarks[0].remark if app.remarks else "",

                "Cloud": ", ".join(
                    mapping.cloud.name
                    for mapping in app.cloud_mappings
                ),

                "Owners": ", ".join(
                    owner.owner_name
                    for owner in app.owners
                ),
            })

        df = pd.DataFrame(rows)

        stream = io.StringIO()

        df.to_csv(
            stream,
            index=False
        )

        stream.seek(0)

        return StreamingResponse(
            iter([stream.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition":
                "attachment; filename=applications.csv"
            }
        )