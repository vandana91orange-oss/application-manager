"""created csv upload file

Revision ID: 709151d7c2d9
Revises: 1f318087b595
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "709151d7c2d9"
down_revision: Union[str, Sequence[str], None] = "1f318087b595"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "csv_uploaded_files",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=True),
        sa.Column("file_path", sa.String(length=500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("csv_uploaded_files")