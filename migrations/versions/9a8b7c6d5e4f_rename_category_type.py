"""rename Category_type to category_type

Revision ID: 9a8b7c6d5e4f
Revises: 80fc81b7df29
Create Date: 2026-11-02 00:40:00

"""

from collections.abc import Sequence

from alembic import op

revision: str = "9a8b7c6d5e4f"
down_revision: str | Sequence[str] | None = "80fc81b7df29"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("categories", "Category_type", new_column_name="category_type")


def downgrade() -> None:
    op.alter_column("categories", "category_type", new_column_name="Category_type")
