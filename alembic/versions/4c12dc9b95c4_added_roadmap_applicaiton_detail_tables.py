from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4c12dc9b95c4"
down_revision: Union[str, Sequence[str], None] = "b07a7fecb702"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---------------------------------------------------------
    # 1. Roadmap phases
    # ---------------------------------------------------------
    op.create_table(
        "roadmap_phases",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("display_name", sa.String(length=150), nullable=False),
        sa.Column(
            "display_order",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_index(
        op.f("ix_roadmap_phases_name"),
        "roadmap_phases",
        ["name"],
        unique=True,
    )

    # ---------------------------------------------------------
    # 2. Roadmap environments
    # ---------------------------------------------------------
    op.create_table(
        "roadmap_environments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("display_name", sa.String(length=150), nullable=False),
        sa.Column(
            "display_order",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_index(
        op.f("ix_roadmap_environments_name"),
        "roadmap_environments",
        ["name"],
        unique=True,
    )

    # ---------------------------------------------------------
    # 3. Roadmap teams
    # ---------------------------------------------------------
    op.create_table(
        "roadmap_teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("normalized_name", sa.String(length=150), nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("normalized_name"),
    )

    op.create_index(
        op.f("ix_roadmap_teams_name"),
        "roadmap_teams",
        ["name"],
        unique=True,
    )

    op.create_index(
        op.f("ix_roadmap_teams_normalized_name"),
        "roadmap_teams",
        ["normalized_name"],
        unique=True,
    )

    # ---------------------------------------------------------
    # 4. Roadmap resources
    # ---------------------------------------------------------
    op.create_table(
        "roadmap_resources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("normalized_name", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["roadmap_teams.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("normalized_name"),
    )

    op.create_index(
        op.f("ix_roadmap_resources_name"),
        "roadmap_resources",
        ["name"],
        unique=False,
    )

    op.create_index(
        op.f("ix_roadmap_resources_normalized_name"),
        "roadmap_resources",
        ["normalized_name"],
        unique=True,
    )

    op.create_index(
        op.f("ix_roadmap_resources_team_id"),
        "roadmap_resources",
        ["team_id"],
        unique=False,
    )

    # ---------------------------------------------------------
    # 5. Application roadmap imports
    # ---------------------------------------------------------
    op.create_table(
        "application_roadmap_imports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("application_id", sa.Integer(), nullable=False),
        sa.Column(
            "original_filename",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "stored_file_path",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column("sheet_name", sa.String(length=255), nullable=True),
        sa.Column(
            "import_status",
            sa.String(length=50),
            nullable=False,
            server_default=sa.text("'PENDING'"),
        ),
        sa.Column(
            "total_rows",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "imported_rows",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "skipped_rows",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "failed_rows",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column("error_details", sa.Text(), nullable=True),
        sa.Column(
            "started_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "completed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["applications.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_application_roadmap_imports_application_id"),
        "application_roadmap_imports",
        ["application_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_application_roadmap_imports_import_status"),
        "application_roadmap_imports",
        ["import_status"],
        unique=False,
    )

    # ---------------------------------------------------------
    # 6. Application roadmap details
    # ---------------------------------------------------------
    op.create_table(
        "application_roadmap_details",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("application_id", sa.Integer(), nullable=False),
        sa.Column("phase_id", sa.Integer(), nullable=False),
        sa.Column("environment_id", sa.Integer(), nullable=False),
        sa.Column("import_batch_id", sa.Integer(), nullable=True),
        sa.Column("section_name", sa.String(length=255), nullable=True),
        sa.Column("activity_number", sa.Integer(), nullable=True),
        sa.Column("activity", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("planned_start_date", sa.Date(), nullable=True),
        sa.Column("planned_end_date", sa.Date(), nullable=True),
        sa.Column("actual_start_date", sa.Date(), nullable=True),
        sa.Column("actual_end_date", sa.Date(), nullable=True),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column(
            "display_order",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "raw_responsible_team",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "raw_support_team",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "raw_assigned_resource",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "source_sheet_name",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column("source_row_number", sa.Integer(), nullable=True),
        sa.Column("import_warning", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.ForeignKeyConstraint(
            ["application_id"],
            ["applications.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["phase_id"],
            ["roadmap_phases.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["environment_id"],
            ["roadmap_environments.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["import_batch_id"],
            ["application_roadmap_imports.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_application_roadmap_details_application_id"),
        "application_roadmap_details",
        ["application_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_application_roadmap_details_phase_id"),
        "application_roadmap_details",
        ["phase_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_application_roadmap_details_environment_id"),
        "application_roadmap_details",
        ["environment_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_application_roadmap_details_import_batch_id"),
        "application_roadmap_details",
        ["import_batch_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_application_roadmap_details_status"),
        "application_roadmap_details",
        ["status"],
        unique=False,
    )

    op.create_index(
        "ix_roadmap_app_phase_environment",
        "application_roadmap_details",
        ["application_id", "phase_id", "environment_id"],
        unique=False,
    )

    op.create_index(
        "ix_roadmap_app_status",
        "application_roadmap_details",
        ["application_id", "status"],
        unique=False,
    )

    # ---------------------------------------------------------
    # 7. Application roadmap teams
    # ---------------------------------------------------------
    op.create_table(
        "application_roadmap_teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("roadmap_detail_id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=30), nullable=False),
        sa.Column(
            "is_primary",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.ForeignKeyConstraint(
            ["roadmap_detail_id"],
            ["application_roadmap_details.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["roadmap_teams.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "roadmap_detail_id",
            "team_id",
            "role",
            name="uq_roadmap_detail_team_role",
        ),
    )

    op.create_index(
        op.f("ix_application_roadmap_teams_roadmap_detail_id"),
        "application_roadmap_teams",
        ["roadmap_detail_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_application_roadmap_teams_team_id"),
        "application_roadmap_teams",
        ["team_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_application_roadmap_teams_role"),
        "application_roadmap_teams",
        ["role"],
        unique=False,
    )

    # ---------------------------------------------------------
    # 8. Application roadmap resources
    # ---------------------------------------------------------
    op.create_table(
        "application_roadmap_resources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("roadmap_detail_id", sa.Integer(), nullable=False),
        sa.Column("resource_id", sa.Integer(), nullable=False),
        sa.Column(
            "is_primary",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.ForeignKeyConstraint(
            ["roadmap_detail_id"],
            ["application_roadmap_details.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["resource_id"],
            ["roadmap_resources.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "roadmap_detail_id",
            "resource_id",
            name="uq_roadmap_detail_resource",
        ),
    )

    op.create_index(
        op.f("ix_application_roadmap_resources_roadmap_detail_id"),
        "application_roadmap_resources",
        ["roadmap_detail_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_application_roadmap_resources_resource_id"),
        "application_roadmap_resources",
        ["resource_id"],
        unique=False,
    )


def downgrade() -> None:
    # Drop child tables before parent tables.

    op.drop_index(
        op.f("ix_application_roadmap_resources_resource_id"),
        table_name="application_roadmap_resources",
    )
    op.drop_index(
        op.f("ix_application_roadmap_resources_roadmap_detail_id"),
        table_name="application_roadmap_resources",
    )
    op.drop_table("application_roadmap_resources")

    op.drop_index(
        op.f("ix_application_roadmap_teams_role"),
        table_name="application_roadmap_teams",
    )
    op.drop_index(
        op.f("ix_application_roadmap_teams_team_id"),
        table_name="application_roadmap_teams",
    )
    op.drop_index(
        op.f("ix_application_roadmap_teams_roadmap_detail_id"),
        table_name="application_roadmap_teams",
    )
    op.drop_table("application_roadmap_teams")

    op.drop_index(
        "ix_roadmap_app_status",
        table_name="application_roadmap_details",
    )
    op.drop_index(
        "ix_roadmap_app_phase_environment",
        table_name="application_roadmap_details",
    )
    op.drop_index(
        op.f("ix_application_roadmap_details_status"),
        table_name="application_roadmap_details",
    )
    op.drop_index(
        op.f("ix_application_roadmap_details_import_batch_id"),
        table_name="application_roadmap_details",
    )
    op.drop_index(
        op.f("ix_application_roadmap_details_environment_id"),
        table_name="application_roadmap_details",
    )
    op.drop_index(
        op.f("ix_application_roadmap_details_phase_id"),
        table_name="application_roadmap_details",
    )
    op.drop_index(
        op.f("ix_application_roadmap_details_application_id"),
        table_name="application_roadmap_details",
    )
    op.drop_table("application_roadmap_details")

    op.drop_index(
        op.f("ix_application_roadmap_imports_import_status"),
        table_name="application_roadmap_imports",
    )
    op.drop_index(
        op.f("ix_application_roadmap_imports_application_id"),
        table_name="application_roadmap_imports",
    )
    op.drop_table("application_roadmap_imports")

    op.drop_index(
        op.f("ix_roadmap_resources_team_id"),
        table_name="roadmap_resources",
    )
    op.drop_index(
        op.f("ix_roadmap_resources_normalized_name"),
        table_name="roadmap_resources",
    )
    op.drop_index(
        op.f("ix_roadmap_resources_name"),
        table_name="roadmap_resources",
    )
    op.drop_table("roadmap_resources")

    op.drop_index(
        op.f("ix_roadmap_teams_normalized_name"),
        table_name="roadmap_teams",
    )
    op.drop_index(
        op.f("ix_roadmap_teams_name"),
        table_name="roadmap_teams",
    )
    op.drop_table("roadmap_teams")

    op.drop_index(
        op.f("ix_roadmap_environments_name"),
        table_name="roadmap_environments",
    )
    op.drop_table("roadmap_environments")

    op.drop_index(
        op.f("ix_roadmap_phases_name"),
        table_name="roadmap_phases",
    )
    op.drop_table("roadmap_phases")