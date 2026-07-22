from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime



class ApplicationUpdateData(BaseModel):

    application_name: Optional[str] = None
    carto_id: Optional[str] = None
    basicat: Optional[str] = None
    priority: Optional[str] = None
    confirmed_domain: Optional[str] = None
    application_status: Optional[str] = None
    domain: Optional[str] = None
    portfolio: Optional[str] = None
    business_importance: Optional[str] = None
    sov_type: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ApplicationMetadataUpdate(BaseModel):

    dx_uid: Optional[str] = None
    mcp_id: Optional[str] = None
    wave: Optional[str] = None
    gate: Optional[str] = None
    assessment_status: Optional[str] = None
    data_anonymization_status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MigrationUpdate(BaseModel):

    migration_status: Optional[str] = None
    migration_progress: Optional[int] = None
    strategy: Optional[str] = None
    hosting_location: Optional[str] = None
    cloud_squad: Optional[str] = None

    initiated: Optional[date] = None
    tentative_start: Optional[date] = None
    tentative_end: Optional[date] = None
    confirmed_end: Optional[date] = None
    go_live: Optional[date] = None

    total_ns: Optional[int] = None
    ns_migration_progress: Optional[str] = None
    assessment_status: Optional[str] = None
    data_anonymization_status: Optional[str] = None
    ns_backup_creation: Optional[str] = None
    ns_migration_status: Optional[str] = None
    cluster: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class SecurityUpdate(BaseModel):

    benchmark_status: Optional[str] = None
    nexus_status: Optional[str] = None
    rooted_status: Optional[str] = None
    network_policy_status: Optional[str] = None

    security_prod_status: Optional[str] = None
    security_prod_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


class RemarkUpdate(BaseModel):

    remark: Optional[str] = None
    remarks_imp: Optional[str] = None
    source_comments: Optional[str] = None
    archived_remarks: Optional[str] = None
    out_of_scope: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class OwnerUpdate(BaseModel):

    owner_type: str
    owner_name: Optional[str] = None
    owner_email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ApplicationUpdate(BaseModel):
    application: Optional[ApplicationUpdateData] = None

    meta_data: Optional[ApplicationMetadataUpdate] = None
    migration: Optional[MigrationUpdate] = None
    security: Optional[SecurityUpdate] = None
    remark: Optional[RemarkUpdate] = None

    owners: Optional[List[OwnerUpdate]] = Field(default=None)
    cloud_ids: Optional[List[int]] = Field(default=None)

    model_config = ConfigDict(from_attributes=True)


class ApplicationCloudResponse(BaseModel):

    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class ApplicationResponse(BaseModel):

    id: int
    carto_id: str | None = None
    application_name: str | None = None
    basicat: str | None = None
    priority: str | None = None
    confirmed_domain: str | None = None
    application_status: str | None = None
    domain: str | None = None
    portfolio: str | None = None
    business_importance: str | None = None
    sov_type: str | None = None
    uploaded_file_id: int | None = None
    model_config = ConfigDict(from_attributes=True)


class ApplicationMetadataResponse(BaseModel):

    id: int
    application_id: int

    dx_uid: str | None = None
    mcp_id: str | None = None
    wave: str | None = None
    gate: str | None = None
    model_config = ConfigDict(from_attributes=True)


class MigrationResponse(BaseModel):

    id: int
    application_id: int

    migration_status: str | None = None
    migration_progress: int | None = None

    strategy: str | None = None
    hosting_location: str | None = None
    cloud_squad: str | None = None

    initiated: date | None = None
    tentative_start: date | None = None
    tentative_end: date | None = None
    confirmed_end: date | None = None
    go_live: date | None = None

    total_ns: int | None = None
    ns_migration_progress: str | None = None

    assessment_status: str | None = None
    data_anonymization_status: str | None = None

    ns_backup_creation: str | None = None
    ns_migration_status: str | None = None

    cluster: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ApplicationSecurityResponse(BaseModel):

    id: int
    application_id: int

    benchmark_status: str | None = None
    nexus_status: str | None = None
    rooted_status: str | None = None
    network_policy_status: str | None = None

    security_prod_status: str | None = None
    security_prod_date: date | None = None


    model_config = ConfigDict(from_attributes=True)


class ApplicationRemarkResponse(BaseModel):

    id: int
    application_id: int

    remark: str | None = None
    remarks_imp: str | None = None
    source_comments: str | None = None
    archived_remarks: str | None = None
    out_of_scope: str | None = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OwnerResponse(BaseModel):

    id: int
    application_id: int
    owner_type: str
    owner_name: str | None = None
    owner_email: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ApplicationDetailsResponse(BaseModel):
    application: ApplicationResponse

    meta_data: ApplicationMetadataResponse | None = None
    migration: MigrationResponse | None = None
    security: ApplicationSecurityResponse | None = None

    remark: list[ApplicationRemarkResponse] = Field(
        default_factory=list
    )
    owners: list[OwnerResponse] = Field(
        default_factory=list
    )
    clouds: list[ApplicationCloudResponse] = Field(
        default_factory=list
    )

    model_config = ConfigDict(from_attributes=True)


class ApplicationCreate(BaseModel):

    application: ApplicationUpdateData
    meta_data: ApplicationMetadataUpdate
    migration: MigrationUpdate

    security: SecurityUpdate
    remark: RemarkUpdate

    owners: list[OwnerUpdate] = []
    cloud_ids: list[int] = []

    model_config = ConfigDict(from_attributes=True)
