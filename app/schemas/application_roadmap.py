from datetime import date, datetime
from typing import Generic, TypeVar

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class RoadmapPhaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    display_name: str
    display_order: int


class RoadmapEnvironmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    display_name: str
    display_order: int


class RoadmapTeamResponse(BaseModel):
    id: int
    name: str
    role: str
    is_primary: bool


class RoadmapResourceResponse(BaseModel):
    id: int
    name: str
    email: str | None = None
    is_primary: bool


class RoadmapDetailResponse(BaseModel):
    id: int
    application_id: int

    phase: RoadmapPhaseResponse
    environment: RoadmapEnvironmentResponse

    section_name: str | None = None
    activity_number: int | None = None
    activity: str
    status: str | None = None

    planned_start_date: date | None = None
    planned_end_date: date | None = None
    actual_start_date: date | None = None
    actual_end_date: date | None = None

    remarks: str | None = None
    display_order: int

    responsible_teams: list[RoadmapTeamResponse] = Field(
        default_factory=list
    )

    support_teams: list[RoadmapTeamResponse] = Field(
        default_factory=list
    )

    assigned_resources: list[RoadmapResourceResponse] = Field(
        default_factory=list
    )

    source_sheet_name: str | None = None
    source_row_number: int | None = None

    import_batch_id: int | None = None

    created_at: datetime
    updated_at: datetime


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool


class ApplicationRoadmapListResponse(BaseModel):
    application_id: int
    carto_id: str | None = None
    application_name: str | None = None

    pagination: PaginationMeta
    items: list[RoadmapDetailResponse]


class RoadmapStatusSummaryResponse(BaseModel):
    status: str
    count: int


class RoadmapEnvironmentSummaryResponse(BaseModel):
    environment_id: int
    environment_name: str
    environment_display_name: str
    total_activities: int
    completed_activities: int
    in_progress_activities: int
    pending_activities: int
    completion_percentage: float


class RoadmapPhaseSummaryResponse(BaseModel):
    phase_id: int
    phase_name: str
    phase_display_name: str
    total_activities: int
    completed_activities: int
    completion_percentage: float


class ApplicationRoadmapSummaryResponse(BaseModel):
    application_id: int
    application_name: str | None = None

    total_activities: int
    completed_activities: int
    in_progress_activities: int
    pending_activities: int
    blocked_activities: int
    completion_percentage: float

    statuses: list[RoadmapStatusSummaryResponse]
    phases: list[RoadmapPhaseSummaryResponse]
    environments: list[RoadmapEnvironmentSummaryResponse]


class GroupedRoadmapEnvironmentResponse(BaseModel):
    id: int
    name: str
    display_name: str
    display_order: int
    total_activities: int
    activities: list[RoadmapDetailResponse]


class GroupedRoadmapPhaseResponse(BaseModel):
    id: int
    name: str
    display_name: str
    display_order: int
    total_activities: int
    environments: list[GroupedRoadmapEnvironmentResponse]


class ApplicationRoadmapGroupedResponse(BaseModel):
    application_id: int
    carto_id: str | None = None
    application_name: str | None = None
    total_activities: int
    phases: list[GroupedRoadmapPhaseResponse]


class RoadmapImportListItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    application_id: int
    original_filename: str
    import_status: str

    total_rows: int
    imported_rows: int
    skipped_rows: int
    failed_rows: int

    error_details: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime


class RoadmapImportListResponse(BaseModel):
    application_id: int
    total_imports: int
    imports: list[RoadmapImportListItemResponse]
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# ROADMAP IMPORT SCHEMAS
# ============================================================


class RoadmapImportResponse(BaseModel):
    import_id: int
    application_id: int
    filename: str
    status: str
    message: str


class RoadmapImportStatusResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    application_id: int
    original_filename: str
    import_status: str

    total_rows: int = 0
    imported_rows: int = 0
    skipped_rows: int = 0
    failed_rows: int = 0

    error_details: str | None = None

    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime


class RoadmapImportListItemResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    application_id: int
    original_filename: str
    import_status: str

    total_rows: int = 0
    imported_rows: int = 0
    skipped_rows: int = 0
    failed_rows: int = 0

    error_details: str | None = None

    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime


class RoadmapImportListResponse(BaseModel):
    application_id: int
    total_imports: int
    imports: list[RoadmapImportListItemResponse] = Field(
        default_factory=list
    )


# ============================================================
# LOOKUP SCHEMAS
# ============================================================


class RoadmapPhaseResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    display_name: str
    display_order: int


class RoadmapEnvironmentResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    display_name: str
    display_order: int


class RoadmapTeamResponse(BaseModel):
    id: int
    name: str
    role: str
    is_primary: bool


class RoadmapResourceResponse(BaseModel):
    id: int
    name: str
    email: str | None = None
    is_primary: bool


# ============================================================
# ROADMAP DETAIL SCHEMAS
# ============================================================


class RoadmapDetailResponse(BaseModel):
    id: int
    application_id: int

    phase: RoadmapPhaseResponse
    environment: RoadmapEnvironmentResponse

    section_name: str | None = None
    activity_number: int | None = None
    activity: str
    status: str | None = None

    planned_start_date: date | None = None
    planned_end_date: date | None = None
    actual_start_date: date | None = None
    actual_end_date: date | None = None

    remarks: str | None = None
    display_order: int

    responsible_teams: list[RoadmapTeamResponse] = Field(
        default_factory=list
    )

    support_teams: list[RoadmapTeamResponse] = Field(
        default_factory=list
    )

    assigned_resources: list[
        RoadmapResourceResponse
    ] = Field(default_factory=list)

    source_sheet_name: str | None = None
    source_row_number: int | None = None
    import_batch_id: int | None = None

    created_at: datetime
    updated_at: datetime


# ============================================================
# PAGINATION SCHEMAS
# ============================================================


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool


class ApplicationRoadmapListResponse(BaseModel):
    application_id: int
    carto_id: str | None = None
    application_name: str | None = None

    pagination: PaginationMeta

    items: list[RoadmapDetailResponse] = Field(
        default_factory=list
    )


# ============================================================
# GROUPED ROADMAP SCHEMAS
# ============================================================


class GroupedRoadmapEnvironmentResponse(BaseModel):
    id: int
    name: str
    display_name: str
    display_order: int
    total_activities: int

    activities: list[RoadmapDetailResponse] = Field(
        default_factory=list
    )


class GroupedRoadmapPhaseResponse(BaseModel):
    id: int
    name: str
    display_name: str
    display_order: int
    total_activities: int

    environments: list[
        GroupedRoadmapEnvironmentResponse
    ] = Field(default_factory=list)


class ApplicationRoadmapGroupedResponse(BaseModel):
    application_id: int
    carto_id: str | None = None
    application_name: str | None = None
    total_activities: int

    phases: list[
        GroupedRoadmapPhaseResponse
    ] = Field(default_factory=list)


# ============================================================
# SUMMARY SCHEMAS
# ============================================================


class RoadmapStatusSummaryResponse(BaseModel):
    status: str
    count: int


class RoadmapPhaseSummaryResponse(BaseModel):
    phase_id: int
    phase_name: str
    phase_display_name: str
    total_activities: int
    completed_activities: int
    completion_percentage: float


class RoadmapEnvironmentSummaryResponse(BaseModel):
    environment_id: int
    environment_name: str
    environment_display_name: str

    total_activities: int
    completed_activities: int
    in_progress_activities: int
    pending_activities: int

    completion_percentage: float


class ApplicationRoadmapSummaryResponse(BaseModel):
    application_id: int
    application_name: str | None = None

    total_activities: int
    completed_activities: int
    in_progress_activities: int
    pending_activities: int
    blocked_activities: int
    completion_percentage: float

    statuses: list[
        RoadmapStatusSummaryResponse
    ] = Field(default_factory=list)

    phases: list[
        RoadmapPhaseSummaryResponse
    ] = Field(default_factory=list)

    environments: list[
        RoadmapEnvironmentSummaryResponse
    ] = Field(default_factory=list)


class RoadmapApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    carto_id: str | None = None
    application_name: str | None = None
    description: str | None = None
    status: str | None = None
    is_active: bool | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None


class ApplicationRoadmapCompleteResponse(BaseModel):
    application: RoadmapApplicationResponse

    total_roadmap_activities: int

    roadmap_details: list[RoadmapDetailResponse] = Field(
        default_factory=list
    )


class RoadmapDetailPatchRequest(BaseModel):
    phase_id: int | None = None
    environment_id: int | None = None

    section_name: str | None = None
    activity_number: int | None = Field(
        default=None,
        ge=1,
    )
    activity: str | None = Field(
        default=None,
        min_length=1,
        max_length=2000,
    )
    status: str | None = None

    planned_start_date: date | None = None
    planned_end_date: date | None = None
    actual_start_date: date | None = None
    actual_end_date: date | None = None

    remarks: str | None = None
    display_order: int | None = Field(
        default=None,
        ge=0,
    )

    responsible_team_ids: list[int] | None = None
    support_team_ids: list[int] | None = None
    assigned_resource_ids: list[int] | None = None
