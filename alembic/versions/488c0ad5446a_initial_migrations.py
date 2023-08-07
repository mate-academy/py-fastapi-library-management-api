"""Initial migrations

Revision ID: 488c0ad5446a
Revises: a5994c853e9a
Create Date: 2023-08-07 11:29:46.383647

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '488c0ad5446a'
down_revision: Union[str, None] = 'a5994c853e9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('publication_date', sa.Date(), nullable=True))
    op.drop_column('books', 'public_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('public_date', sa.DATE(), nullable=True))
    op.drop_column('books', 'publication_date')
    # ### end Alembic commands ###
