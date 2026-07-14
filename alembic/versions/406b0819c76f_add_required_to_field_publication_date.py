"""add required to field publication_date

Revision ID: 406b0819c76f
Revises: 75e42b78f44f
Create Date: 2026-07-14 12:46:42.380960

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '406b0819c76f'
down_revision: Union[str, Sequence[str], None] = '75e42b78f44f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("books") as batch_op:
        batch_op.alter_column(
            "publication_date",
            existing_type=sa.DATE(),
            nullable=False,
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    with op.batch_alter_table("books") as batch_op:
        batch_op.alter_column(
            "publication_date",
            existing_type=sa.DATE(),
            nullable=True,
        )
    # ### end Alembic commands ###
