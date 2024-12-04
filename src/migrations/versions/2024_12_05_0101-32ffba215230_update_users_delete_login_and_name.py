"""update users, delete login and name

Revision ID: 32ffba215230
Revises: b1fad94fa72a
Create Date: 2024-12-05 01:01:51.638189

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "32ffba215230"
down_revision: Union[str, None] = "b1fad94fa72a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("users_login_key", "users", type_="unique")
    op.drop_column("users", "name")
    op.drop_column("users", "login")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column("login", sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    )
    op.add_column(
        "users",
        sa.Column("name", sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    )
    op.create_unique_constraint("users_login_key", "users", ["login"])
