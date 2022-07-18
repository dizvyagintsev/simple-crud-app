"""create user-profiles table

Revision ID: 59ae8eb39620
Revises: 
Create Date: 2022-07-16 22:17:54.983190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "59ae8eb39620"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_profiles",
        sa.Column("user_id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(40), nullable=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("birth_date", sa.Date, nullable=False),
        sa.Column("is_banned", sa.Boolean, default=False, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("user_profiles")
