"""update users, add constraints unique email, login

Revision ID: b1fad94fa72a
Revises: 8b1ae3b7b90e
Create Date: 2024-12-04 14:25:15.207163

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b1fad94fa72a"
down_revision: Union[str, None] = "8b1ae3b7b90e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("hashed_password", sa.String(length=200), nullable=False)
    )
    op.create_unique_constraint('users_login_key', "users", ["login"])
    op.create_unique_constraint('users_email_key', "users", ["email"])
    op.drop_column("users", "password")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column("password", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_constraint('users_email_key', "users", type_="unique")
    op.drop_constraint('users_login_key', "users", type_="unique")
    op.drop_column("users", "hashed_password")
