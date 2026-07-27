"""updated application cloud name table

Revision ID: 86674be39b99
Revises: 4664125a91fd
Create Date: 2026-07-14 09:29:39.136842
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# Alembic revision identifiers.
revision: str = "86674be39b99"
down_revision: Union[str, Sequence[str], None] = "4664125a91fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


CLOUD_TABLE = "application_cloud"
CLOUD_MAPPING_TABLE = "application_cloud_mapping"

OLD_CLOUD_TABLE = "application_could"
OLD_CLOUD_MAPPING_TABLE = "application_could_mapping"

UNIQUE_CONSTRAINT_NAME = "uq_application_cloud_name"


def _get_table_names() -> set[str]:
    """Return all tables currently present in the public schema."""
    bind = op.get_bind()
    inspector = inspect(bind)
    return set(inspector.get_table_names())


def _get_unique_constraints(table_name: str) -> list[dict]:
    """Return the unique constraints defined on a table."""
    bind = op.get_bind()
    inspector = inspect(bind)
    return inspector.get_unique_constraints(table_name)


def upgrade() -> None:
    """Upgrade schema."""

    existing_tables = _get_table_names()

    # Rename the old misspelled cloud table when it exists.
    if OLD_CLOUD_TABLE in existing_tables and CLOUD_TABLE not in existing_tables:
        op.rename_table(OLD_CLOUD_TABLE, CLOUD_TABLE)
        existing_tables.remove(OLD_CLOUD_TABLE)
        existing_tables.add(CLOUD_TABLE)

    # A clean database may have neither the old nor the corrected table.
    # Create the corrected table in that case.
    if CLOUD_TABLE not in existing_tables:
        op.create_table(
            CLOUD_TABLE,
            sa.Column(
                "id",
                sa.Integer(),
                autoincrement=True,
                nullable=False,
            ),
            sa.Column(
                "name",
                sa.String(length=200),
                nullable=False,
            ),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=True,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=True,
            ),
            sa.PrimaryKeyConstraint(
                "id",
                name="application_cloud_pkey",
            ),
        )
        existing_tables.add(CLOUD_TABLE)

    else:
        # Prevent ALTER COLUMN SET NOT NULL from failing if old rows contain
        # a NULL value.
        op.execute(
            sa.text(
                """
                UPDATE application_cloud
                SET name = 'Unknown Cloud ' || id::text
                WHERE name IS NULL
                """
            )
        )

        op.alter_column(
            CLOUD_TABLE,
            "name",
            existing_type=sa.String(length=200),
            nullable=False,
        )

    # Add the unique constraint only when one does not already exist on name.
    unique_constraints = _get_unique_constraints(CLOUD_TABLE)

    has_name_unique_constraint = any(
        set(constraint.get("column_names") or []) == {"name"}
        for constraint in unique_constraints
    )

    if not has_name_unique_constraint:
        op.create_unique_constraint(
            UNIQUE_CONSTRAINT_NAME,
            CLOUD_TABLE,
            ["name"],
        )

    # Rename the old misspelled mapping table when it exists.
    existing_tables = _get_table_names()

    if (
        OLD_CLOUD_MAPPING_TABLE in existing_tables
        and CLOUD_MAPPING_TABLE not in existing_tables
    ):
        op.rename_table(
            OLD_CLOUD_MAPPING_TABLE,
            CLOUD_MAPPING_TABLE,
        )

    elif CLOUD_MAPPING_TABLE not in existing_tables:
        op.create_table(
            CLOUD_MAPPING_TABLE,
            sa.Column(
                "id",
                sa.Integer(),
                autoincrement=True,
                nullable=False,
            ),
            sa.Column(
                "application_id",
                sa.Integer(),
                nullable=False,
            ),
            sa.Column(
                "cloud_id",
                sa.Integer(),
                nullable=False,
            ),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=True,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=True,
            ),
            sa.ForeignKeyConstraint(
                ["application_id"],
                ["applications.id"],
                name="fk_application_cloud_mapping_application_id",
                ondelete="CASCADE",
            ),
            sa.ForeignKeyConstraint(
                ["cloud_id"],
                ["application_cloud.id"],
                name="fk_application_cloud_mapping_cloud_id",
                ondelete="CASCADE",
            ),
            sa.PrimaryKeyConstraint(
                "id",
                name="application_cloud_mapping_pkey",
            ),
            sa.UniqueConstraint(
                "application_id",
                "cloud_id",
                name="uq_application_cloud_mapping",
            ),
        )


def downgrade() -> None:
    """Downgrade schema."""

    existing_tables = _get_table_names()

    if CLOUD_MAPPING_TABLE in existing_tables:
        op.drop_table(CLOUD_MAPPING_TABLE)

    existing_tables = _get_table_names()

    if CLOUD_TABLE in existing_tables:
        op.drop_table(CLOUD_TABLE)

    # Restore the original typo-named tables.
    op.create_table(
        OLD_CLOUD_TABLE,
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=200),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name="application_could_pkey",
        ),
    )

    op.create_table(
        OLD_CLOUD_MAPPING_TABLE,
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "application_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "cloud_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name="application_could_mapping_pkey",
        ),
    )