"""Add unique constraint for book title

Revision ID: ffe85200e436
Revises: 6aafc55bec5d
Create Date: 2023-12-28 12:50:36.694939

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ffe85200e436"
down_revision: Union[str, None] = "6aafc55bec5d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f("ix_book_title"), "book", ["title"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_book_title"), table_name="book")
    # ### end Alembic commands ###