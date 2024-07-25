"""test

Revision ID: 900b084825af
Revises: a28878687280
Create Date: 2024-07-23 21:31:00.630502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '900b084825af'
down_revision: Union[str, None] = 'a28878687280'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "author",
        sa.Column("id", sa.Integer, autoincrement=True, nullable=False),
        sa.Column("name", sa.String, nullable=False, unique=True),
        sa.Column("bio", sa.String, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "book",
        sa.Column("id", sa.Integer, autoincrement=True, nullable=False),
        sa.Column("title", sa.String, nullable=False, unique=True),
        sa.Column("summary", sa.String, nullable=False),
        sa.Column("author_id", sa.Integer, sa.ForeignKey('author.id'), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["author.id"],
            ondelete="CASCADE"
        )
    )


def downgrade() -> None:
    op.drop_table("book")
    op.drop_table("author")
