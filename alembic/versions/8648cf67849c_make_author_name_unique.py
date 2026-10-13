"""make author name unique

Revision ID: 8648cf67849c
Revises: 6066a0d01e77
Create Date: 2026-10-13 12:54:20.512711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8648cf67849c'
down_revision: Union[str, Sequence[str], None] = '6066a0d01e77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('author', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_author_name', ['name'])

    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.alter_column(
            'author_id',
            existing_type=sa.INTEGER(),
            nullable=False,
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.alter_column(
            'author_id',
            existing_type=sa.INTEGER(),
            nullable=True,
        )

    with op.batch_alter_table('author', schema=None) as batch_op:
        batch_op.drop_constraint('uq_author_name', type_='unique')
