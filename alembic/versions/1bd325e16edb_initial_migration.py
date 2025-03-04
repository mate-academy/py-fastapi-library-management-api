"""Initial migration

Revision ID: 1bd325e16edb
Revises: 
Create Date: 2025-03-04 02:10:11.419990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bd325e16edb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Alter column to DateTime
    op.alter_column('book', 'publication_date',
                    existing_type=sa.DateTime(),  # Old type (if applicable)
                    type_=sa.String())


def downgrade() -> None:
    # Reverse the alteration (if necessary)
    op.alter_column('book', 'publication_date',
                    existing_type=sa.DateTime(),
                    type_=sa.String(),  # Revert to the original type
                    nullable=True)
