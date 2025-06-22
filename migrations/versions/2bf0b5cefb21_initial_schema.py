"""initial schema

Revision ID: 2bf0b5cefb21
Revises: fe9585969165
Create Date: 2025-06-23 00:41:52.222801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bf0b5cefb21'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'authors',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, unique=True),
        sa.Column('bio', sa.String(500), nullable=False),
    )
    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('summary', sa.String(500), nullable=False),
        sa.Column('publication_date', sa.Date(), nullable=False),
        sa.Column('author_id', sa.Integer(), sa.ForeignKey('authors.id'), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('books')
    op.drop_table('authors')

