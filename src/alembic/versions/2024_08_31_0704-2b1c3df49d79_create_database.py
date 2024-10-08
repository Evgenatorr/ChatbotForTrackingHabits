"""create database

Revision ID: 2b1c3df49d79
Revises: 
Create Date: 2024-08-31 07:04:40.429869

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "2b1c3df49d79"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("tg_user_id", sa.BIGINT(), nullable=False),
        sa.Column("username", sa.VARCHAR(length=50), nullable=False),
        sa.Column("password", postgresql.BYTEA(), nullable=False),
        sa.Column("active", sa.BOOLEAN(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tg_user_id"),
    )
    op.create_table(
        "habit",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("user_id", sa.BIGINT(), nullable=False),
        sa.Column("title", sa.VARCHAR(length=50), nullable=False),
        sa.Column("description", sa.VARCHAR(length=300), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["user.tg_user_id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "habit_tracking",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("habit_id", sa.INTEGER(), nullable=False),
        # sa.Column("alert_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("alert_time", sa.Time(), nullable=True),
        sa.Column("count", sa.INTEGER(), nullable=True),
        sa.ForeignKeyConstraint(["habit_id"], ["habit.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("habit_tracking")
    op.drop_table("habit")
    op.drop_table("user")
    # ### end Alembic commands ###
