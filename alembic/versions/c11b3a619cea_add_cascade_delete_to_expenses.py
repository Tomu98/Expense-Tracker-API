"""Add cascade delete to expenses

Revision ID: c11b3a619cea
Revises: 
Create Date: 2024-10-03 19:34:40.514671

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c11b3a619cea'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("expenses_user_id_fkey", "expenses", type_="foreignkey")
    op.create_foreign_key(
        "expenses_user_id_fkey", "expenses", "users",
        ["user_id"], ["id"], ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint("expenses_user_id_fkey", "expenses", type_="foreignkey")
    op.create_foreign_key(
        "expenses_user_id_fkey", "expenses", "users",
        ["user_id"], ["id"]
    )
