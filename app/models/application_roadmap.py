from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship
from app.database import Base


class RoadmapPhase(Base):
    __tablename__ = "roadmap_phases"

    id = Column(Integer, primary_key=True)

    name = Column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    display_name = Column(
        String(150),
        nullable=False,
    )

    display_order = Column(
        Integer,
        nullable=False,
        default=0,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    roadmap_details = relationship(
        "ApplicationRoadmapDetail",
        back_populates="phase",
    )


class RoadmapEnvironment(Base):
    __tablename__ = "roadmap_environments"

    id = Column(Integer, primary_key=True)

    name = Column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    display_name = Column(
        String(150),
        nullable=False,
    )

    display_order = Column(
        Integer,
        nullable=False,
        default=0,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    roadmap_details = relationship(
        "ApplicationRoadmapDetail",
        back_populates="environment",
    )


class RoadmapTeam(Base):
    __tablename__ = "roadmap_teams"

    id = Column(Integer, primary_key=True)

    name = Column(
        String(150),
        nullable=False,
        unique=True,
        index=True,
    )

    normalized_name = Column(
        String(150),
        nullable=False,
        unique=True,
        index=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    assignments = relationship(
        "ApplicationRoadmapTeam",
        back_populates="team",
        cascade="all, delete-orphan",
    )

    resources = relationship(
        "RoadmapResource",
        back_populates="team",
    )


class RoadmapResource(Base):
    __tablename__ = "roadmap_resources"

    id = Column(Integer, primary_key=True)

    name = Column(
        String(150),
        nullable=False,
        index=True,
    )

    normalized_name = Column(
        String(150),
        nullable=False,
        unique=True,
        index=True,
    )

    email = Column(
        String(255),
        nullable=True,
        unique=True,
    )

    team_id = Column(
        Integer,
        ForeignKey(
            "roadmap_teams.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    team = relationship(
        "RoadmapTeam",
        back_populates="resources",
    )

    assignments = relationship(
        "ApplicationRoadmapResource",
        back_populates="resource",
        cascade="all, delete-orphan",
    )


class ApplicationRoadmapImport(Base):
    __tablename__ = "application_roadmap_imports"

    id = Column(Integer, primary_key=True)

    application_id = Column(
        Integer,
        ForeignKey(
            "applications.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    original_filename = Column(
        String(255),
        nullable=False,
    )

    stored_file_path = Column(
        String(500),
        nullable=True,
    )

    sheet_name = Column(
        String(255),
        nullable=True,
    )

    import_status = Column(
        String(50),
        nullable=False,
        default="PENDING",
        index=True,
    )

    total_rows = Column(
        Integer,
        nullable=False,
        default=0,
    )

    imported_rows = Column(
        Integer,
        nullable=False,
        default=0,
    )

    skipped_rows = Column(
        Integer,
        nullable=False,
        default=0,
    )

    failed_rows = Column(
        Integer,
        nullable=False,
        default=0,
    )

    error_details = Column(
        Text,
        nullable=True,
    )

    started_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    application = relationship(
        "Application",
        back_populates="roadmap_imports",
    )

    roadmap_details = relationship(
        "ApplicationRoadmapDetail",
        back_populates="import_batch",
    )


class ApplicationRoadmapDetail(Base):
    __tablename__ = "application_roadmap_details"

    id = Column(Integer, primary_key=True)

    application_id = Column(
        Integer,
        ForeignKey(
            "applications.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    phase_id = Column(
        Integer,
        ForeignKey(
            "roadmap_phases.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    environment_id = Column(
        Integer,
        ForeignKey(
            "roadmap_environments.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    import_batch_id = Column(
        Integer,
        ForeignKey(
            "application_roadmap_imports.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    section_name = Column(
        String(255),
        nullable=True,
    )

    activity_number = Column(
        Integer,
        nullable=True,
    )

    activity = Column(
        Text,
        nullable=False,
    )

    status = Column(
        String(50),
        nullable=True,
        index=True,
    )

    planned_start_date = Column(
        Date,
        nullable=True,
    )

    planned_end_date = Column(
        Date,
        nullable=True,
    )

    actual_start_date = Column(
        Date,
        nullable=True,
    )

    actual_end_date = Column(
        Date,
        nullable=True,
    )

    remarks = Column(
        Text,
        nullable=True,
    )

    display_order = Column(
        Integer,
        nullable=False,
        default=0,
    )

    raw_responsible_team = Column(
        String(500),
        nullable=True,
    )

    raw_support_team = Column(
        String(500),
        nullable=True,
    )

    raw_assigned_resource = Column(
        String(500),
        nullable=True,
    )

    source_sheet_name = Column(
        String(255),
        nullable=True,
    )

    source_row_number = Column(
        Integer,
        nullable=True,
    )

    import_warning = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    application = relationship(
        "Application",
        back_populates="roadmap_details",
    )

    phase = relationship(
        "RoadmapPhase",
        back_populates="roadmap_details",
    )

    environment = relationship(
        "RoadmapEnvironment",
        back_populates="roadmap_details",
    )

    import_batch = relationship(
        "ApplicationRoadmapImport",
        back_populates="roadmap_details",
    )

    team_assignments = relationship(
        "ApplicationRoadmapTeam",
        back_populates="roadmap_detail",
        cascade="all, delete-orphan",
    )

    resource_assignments = relationship(
        "ApplicationRoadmapResource",
        back_populates="roadmap_detail",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index(
            "ix_roadmap_app_phase_environment",
            "application_id",
            "phase_id",
            "environment_id",
        ),
        Index(
            "ix_roadmap_app_status",
            "application_id",
            "status",
        ),
    )


class ApplicationRoadmapTeam(Base):
    __tablename__ = "application_roadmap_teams"

    id = Column(Integer, primary_key=True)

    roadmap_detail_id = Column(
        Integer,
        ForeignKey(
            "application_roadmap_details.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    team_id = Column(
        Integer,
        ForeignKey(
            "roadmap_teams.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    role = Column(
        String(30),
        nullable=False,
        index=True,
    )

    is_primary = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    roadmap_detail = relationship(
        "ApplicationRoadmapDetail",
        back_populates="team_assignments",
    )

    team = relationship(
        "RoadmapTeam",
        back_populates="assignments",
    )

    __table_args__ = (
        UniqueConstraint(
            "roadmap_detail_id",
            "team_id",
            "role",
            name="uq_roadmap_detail_team_role",
        ),
    )


class ApplicationRoadmapResource(Base):
    __tablename__ = "application_roadmap_resources"

    id = Column(Integer, primary_key=True)

    roadmap_detail_id = Column(
        Integer,
        ForeignKey(
            "application_roadmap_details.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    resource_id = Column(
        Integer,
        ForeignKey(
            "roadmap_resources.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    is_primary = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    roadmap_detail = relationship(
        "ApplicationRoadmapDetail",
        back_populates="resource_assignments",
    )

    resource = relationship(
        "RoadmapResource",
        back_populates="assignments",
    )

    __table_args__ = (
        UniqueConstraint(
            "roadmap_detail_id",
            "resource_id",
            name="uq_roadmap_detail_resource",
        ),
    )