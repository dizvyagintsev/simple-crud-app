"""user_profiles.email uniq index

Revision ID: 77fd32f340d3
Revises: 59ae8eb39620
Create Date: 2022-07-17 18:03:29.123836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "77fd32f340d3"
down_revision = "59ae8eb39620"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        index_name="user_profiles_email_uindex",
        table_name="user_profiles",
        columns=["email"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("user_profiles_email_uindex")
