"""initialized

Revision ID: eb3b4a82daf9
Revises: 8836c91e0d3e
Create Date: 2024-07-23 20:58:46.621402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb3b4a82daf9'
down_revision: Union[str, None] = '8836c91e0d3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
