from sqlalchemy.orm import (
    Session,
    joinedload,
    selectinload,
)

from app.models.application import Application

from app.models.application_roadmap import (
    ApplicationRoadmapDetail,
    ApplicationRoadmapResource,
    ApplicationRoadmapTeam,
    RoadmapEnvironment,
    RoadmapPhase,
    RoadmapResource,
    RoadmapTeam
)

from app.schemas.application_roadmap import (
    ApplicationRoadmapCompleteResponse,
    RoadmapApplicationResponse,
    RoadmapDetailResponse,
    RoadmapEnvironmentResponse,
    RoadmapPhaseResponse,
    RoadmapResourceResponse,
    RoadmapTeamResponse,
)


def serialize_phase(
    phase: RoadmapPhase,
) -> RoadmapPhaseResponse:
    return RoadmapPhaseResponse(
        id=phase.id,
        name=phase.name,
        display_name=phase.display_name,
        display_order=phase.display_order,
    )


def serialize_environment(
    environment: RoadmapEnvironment,
) -> RoadmapEnvironmentResponse:
    return RoadmapEnvironmentResponse(
        id=environment.id,
        name=environment.name,
        display_name=environment.display_name,
        display_order=environment.display_order,
    )


def serialize_team_assignments(
    detail: ApplicationRoadmapDetail,
) -> tuple[
    list[RoadmapTeamResponse],
    list[RoadmapTeamResponse],
]:
    responsible_teams: list[RoadmapTeamResponse] = []
    support_teams: list[RoadmapTeamResponse] = []

    for assignment in detail.team_assignments or []:
        if assignment.team is None:
            continue

        team_response = RoadmapTeamResponse(
            id=assignment.team.id,
            name=assignment.team.name,
            role=assignment.role,
            is_primary=bool(assignment.is_primary),
        )

        if assignment.role == "RESPONSIBLE":
            responsible_teams.append(team_response)

        elif assignment.role == "SUPPORT":
            support_teams.append(team_response)

    responsible_teams.sort(
        key=lambda team: (
            not team.is_primary,
            team.name.casefold(),
            team.id,
        )
    )

    support_teams.sort(
        key=lambda team: (
            not team.is_primary,
            team.name.casefold(),
            team.id,
        )
    )

    return responsible_teams, support_teams


def serialize_resource_assignments(
    detail: ApplicationRoadmapDetail,
) -> list[RoadmapResourceResponse]:
    resources: list[RoadmapResourceResponse] = []

    for assignment in detail.resource_assignments or []:
        if assignment.resource is None:
            continue

        resources.append(
            RoadmapResourceResponse(
                id=assignment.resource.id,
                name=assignment.resource.name,
                email=getattr(
                    assignment.resource,
                    "email",
                    None,
                ),
                is_primary=bool(
                    assignment.is_primary
                ),
            )
        )

    resources.sort(
        key=lambda resource: (
            not resource.is_primary,
            resource.name.casefold(),
            resource.id,
        )
    )

    return resources


def serialize_roadmap_detail(
    detail: ApplicationRoadmapDetail,
) -> RoadmapDetailResponse:
    """
    Convert ApplicationRoadmapDetail SQLAlchemy model
    into RoadmapDetailResponse.
    """

    if detail.phase is None:
        raise ValueError(
            f"Roadmap detail {detail.id} has no phase."
        )

    if detail.environment is None:
        raise ValueError(
            f"Roadmap detail {detail.id} "
            "has no environment."
        )

    (
        responsible_teams,
        support_teams,
    ) = serialize_team_assignments(detail)

    assigned_resources = (
        serialize_resource_assignments(detail)
    )

    return RoadmapDetailResponse(
        id=detail.id,
        application_id=detail.application_id,
        phase=serialize_phase(detail.phase),
        environment=serialize_environment(
            detail.environment
        ),
        section_name=detail.section_name,
        activity_number=detail.activity_number,
        activity=detail.activity,
        status=detail.status,
        planned_start_date=(
            detail.planned_start_date
        ),
        planned_end_date=(
            detail.planned_end_date
        ),
        actual_start_date=(
            detail.actual_start_date
        ),
        actual_end_date=(
            detail.actual_end_date
        ),
        remarks=detail.remarks,
        display_order=detail.display_order,
        responsible_teams=responsible_teams,
        support_teams=support_teams,
        assigned_resources=assigned_resources,
        source_sheet_name=(
            detail.source_sheet_name
        ),
        source_row_number=(
            detail.source_row_number
        ),
        import_batch_id=(
            detail.import_batch_id
        ),
        created_at=detail.created_at,
        updated_at=detail.updated_at,
    )

def get_application_with_all_roadmap_details(
    db: Session,
    *,
    application_id: int,
) -> ApplicationRoadmapCompleteResponse | None:
    """
    Return application details together with all roadmap activities.
    """

    application = (
        db.query(Application)
        .filter(
            Application.id == application_id
        )
        .one_or_none()
    )

    if application is None:
        return None

    roadmap_details = (
        db.query(ApplicationRoadmapDetail)
        .join(
            RoadmapPhase,
            ApplicationRoadmapDetail.phase_id
            == RoadmapPhase.id,
        )
        .join(
            RoadmapEnvironment,
            ApplicationRoadmapDetail.environment_id
            == RoadmapEnvironment.id,
        )
        .options(
            joinedload(
                ApplicationRoadmapDetail.phase
            ),
            joinedload(
                ApplicationRoadmapDetail.environment
            ),
            selectinload(
                ApplicationRoadmapDetail.team_assignments
            ).joinedload(
                ApplicationRoadmapTeam.team
            ),
            selectinload(
                ApplicationRoadmapDetail.resource_assignments
            ).joinedload(
                ApplicationRoadmapResource.resource
            ),
        )
        .filter(
            ApplicationRoadmapDetail.application_id
            == application_id
        )
        .order_by(
            RoadmapPhase.display_order,
            RoadmapEnvironment.display_order,
            ApplicationRoadmapDetail.display_order,
            ApplicationRoadmapDetail.id,
        )
        .all()
    )

    return ApplicationRoadmapCompleteResponse(
        application=RoadmapApplicationResponse(
            id=application.id,
            carto_id=getattr(
                application,
                "carto_id",
                None,
            ),
            application_name=getattr(
                application,
                "application_name",
                None,
            ),
            description=getattr(
                application,
                "description",
                None,
            ),
            status=getattr(
                application,
                "status",
                None,
            ),
            is_active=getattr(
                application,
                "is_active",
                None,
            ),
            created_at=getattr(
                application,
                "created_at",
                None,
            ),
            updated_at=getattr(
                application,
                "updated_at",
                None,
            ),
        ),
        total_roadmap_activities=len(
            roadmap_details
        ),
        roadmap_details=[
            serialize_roadmap_detail(detail)
            for detail in roadmap_details
        ],
    )


def normalize_roadmap_status(
    value: str | None,
) -> str | None:
    if value is None:
        return None

    normalized = (
        value.strip()
        .upper()
        .replace("-", "_")
        .replace(" ", "_")
    )

    allowed_statuses = {
        "TO_DO",
        "IN_PROGRESS",
        "DONE",
        "NOT_REQUIRED",
        "BLOCKED",
    }

    if normalized not in allowed_statuses:
        raise ValueError(
            "Invalid roadmap status. Allowed values are: "
            "TO_DO, IN_PROGRESS, DONE, NOT_REQUIRED, BLOCKED."
        )

    return normalized

def get_roadmap_detail_for_update(
    db: Session,
    *,
    application_id: int,
    roadmap_detail_id: int,
) -> ApplicationRoadmapDetail | None:
    return (
        db.query(ApplicationRoadmapDetail)
        .options(
            joinedload(
                ApplicationRoadmapDetail.phase
            ),
            joinedload(
                ApplicationRoadmapDetail.environment
            ),
            selectinload(
                ApplicationRoadmapDetail.team_assignments
            ).joinedload(
                ApplicationRoadmapTeam.team
            ),
            selectinload(
                ApplicationRoadmapDetail.resource_assignments
            ).joinedload(
                ApplicationRoadmapResource.resource
            ),
        )
        .filter(
            ApplicationRoadmapDetail.id
            == roadmap_detail_id,
            ApplicationRoadmapDetail.application_id
            == application_id,
        )
        .one_or_none()
    )

def patch_application_roadmap_detail(
    db: Session,
    *,
    application_id: int,
    roadmap_detail_id: int,
    payload: RoadmapDetailPatchRequest,
) -> RoadmapDetailResponse | None:
    """
    Partially update one roadmap detail.

    Only fields supplied in the request are changed.
    """

    detail = get_roadmap_detail_for_update(
        db=db,
        application_id=application_id,
        roadmap_detail_id=roadmap_detail_id,
    )

    if detail is None:
        return None

    update_data = payload.model_dump(
        exclude_unset=True
    )

    responsible_team_ids = update_data.pop(
        "responsible_team_ids",
        None,
    )

    support_team_ids = update_data.pop(
        "support_team_ids",
        None,
    )

    assigned_resource_ids = update_data.pop(
        "assigned_resource_ids",
        None,
    )

    if "phase_id" in update_data:
        phase_id = update_data["phase_id"]

        phase = (
            db.query(RoadmapPhase)
            .filter(
                RoadmapPhase.id == phase_id
            )
            .one_or_none()
        )

        if phase is None:
            raise ValueError(
                f"Roadmap phase {phase_id} was not found."
            )

    if "environment_id" in update_data:
        environment_id = update_data[
            "environment_id"
        ]

        environment = (
            db.query(RoadmapEnvironment)
            .filter(
                RoadmapEnvironment.id
                == environment_id
            )
            .one_or_none()
        )

        if environment is None:
            raise ValueError(
                f"Roadmap environment "
                f"{environment_id} was not found."
            )

    if "status" in update_data:
        update_data["status"] = (
            normalize_roadmap_status(
                update_data["status"]
            )
        )

    if "activity" in update_data:
        activity = update_data["activity"]

        if activity is None or not activity.strip():
            raise ValueError(
                "Activity cannot be empty."
            )

        update_data["activity"] = (
            activity.strip()
        )

    text_fields = {
        "section_name",
        "remarks",
    }

    for field_name in text_fields:
        if field_name in update_data:
            value = update_data[field_name]

            if isinstance(value, str):
                update_data[field_name] = (
                    value.strip() or None
                )

    planned_start = update_data.get(
        "planned_start_date",
        detail.planned_start_date,
    )

    planned_end = update_data.get(
        "planned_end_date",
        detail.planned_end_date,
    )

    actual_start = update_data.get(
        "actual_start_date",
        detail.actual_start_date,
    )

    actual_end = update_data.get(
        "actual_end_date",
        detail.actual_end_date,
    )

    if (
        planned_start is not None
        and planned_end is not None
        and planned_end < planned_start
    ):
        raise ValueError(
            "Planned end date cannot be before "
            "planned start date."
        )

    if (
        actual_start is not None
        and actual_end is not None
        and actual_end < actual_start
    ):
        raise ValueError(
            "Actual end date cannot be before "
            "actual start date."
        )

    try:
        for field_name, value in (
            update_data.items()
        ):
            setattr(
                detail,
                field_name,
                value,
            )

        if responsible_team_ids is not None:
            replace_roadmap_team_assignments(
                db=db,
                detail=detail,
                team_ids=responsible_team_ids,
                role="RESPONSIBLE",
            )

        if support_team_ids is not None:
            replace_roadmap_team_assignments(
                db=db,
                detail=detail,
                team_ids=support_team_ids,
                role="SUPPORT",
            )

        if assigned_resource_ids is not None:
            replace_roadmap_resource_assignments(
                db=db,
                detail=detail,
                resource_ids=(
                    assigned_resource_ids
                ),
            )

        db.commit()

    except Exception:
        db.rollback()
        raise

    detail = get_roadmap_detail_for_update(
        db=db,
        application_id=application_id,
        roadmap_detail_id=roadmap_detail_id,
    )

    return serialize_roadmap_detail(detail)

def replace_roadmap_team_assignments(
    db: Session,
    *,
    detail: ApplicationRoadmapDetail,
    team_ids: list[int],
    role: str,
) -> None:
    unique_team_ids = list(
        dict.fromkeys(team_ids)
    )

    db.query(
        ApplicationRoadmapTeam
    ).filter(
        ApplicationRoadmapTeam.roadmap_detail_id
        == detail.id,
        ApplicationRoadmapTeam.role == role,
    ).delete(
        synchronize_session=False
    )

    if not unique_team_ids:
        return

    teams = (
        db.query(RoadmapTeam)
        .filter(
            RoadmapTeam.id.in_(
                unique_team_ids
            )
        )
        .all()
    )

    found_team_ids = {
        team.id
        for team in teams
    }

    missing_team_ids = set(
        unique_team_ids
    ) - found_team_ids

    if missing_team_ids:
        raise ValueError(
            "Roadmap teams not found: "
            + ", ".join(
                str(team_id)
                for team_id in sorted(
                    missing_team_ids
                )
            )
        )

    for index, team_id in enumerate(
        unique_team_ids
    ):
        db.add(
            ApplicationRoadmapTeam(
                roadmap_detail_id=detail.id,
                team_id=team_id,
                role=role,
                is_primary=index == 0,
            )
        )


def replace_roadmap_resource_assignments(
    db: Session,
    *,
    detail: ApplicationRoadmapDetail,
    resource_ids: list[int],
) -> None:
    unique_resource_ids = list(
        dict.fromkeys(resource_ids)
    )

    db.query(
        ApplicationRoadmapResource
    ).filter(
        ApplicationRoadmapResource.roadmap_detail_id
        == detail.id
    ).delete(
        synchronize_session=False
    )

    if not unique_resource_ids:
        return

    resources = (
        db.query(RoadmapResource)
        .filter(
            RoadmapResource.id.in_(
                unique_resource_ids
            )
        )
        .all()
    )

    found_resource_ids = {
        resource.id
        for resource in resources
    }

    missing_resource_ids = set(
        unique_resource_ids
    ) - found_resource_ids

    if missing_resource_ids:
        raise ValueError(
            "Roadmap resources not found: "
            + ", ".join(
                str(resource_id)
                for resource_id in sorted(
                    missing_resource_ids
                )
            )
        )

    for index, resource_id in enumerate(
        unique_resource_ids
    ):
        db.add(
            ApplicationRoadmapResource(
                roadmap_detail_id=detail.id,
                resource_id=resource_id,
                is_primary=index == 0,
            )
        )