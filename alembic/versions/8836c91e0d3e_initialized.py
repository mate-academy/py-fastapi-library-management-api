"""initialized

Revision ID: 8836c91e0d3e
Revises: e0c36932c101
Create Date: 2024-07-23 20:57:59.862804

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8836c91e0d3e'
down_revision: Union[str, None] = 'e0c36932c101'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
