"""update users

Revision ID: 8b1ae3b7b90e
Revises: f5eb341b7fa5
Create Date: 2024-12-03 22:42:27.193688

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8b1ae3b7b90e"
down_revision: Union[str, None] = "f5eb341b7fa5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("name", sa.String(length=200), nullable=True))
    op.add_column("users", sa.Column("login", sa.String(length=200), nullable=False))


def downgrade() -> None:
    op.drop_column("users", "login")
    op.drop_column("users", "name")
