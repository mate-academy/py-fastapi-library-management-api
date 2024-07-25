"""initialized

Revision ID: 46d4d2b19794
Revises: eb3b4a82daf9
Create Date: 2024-07-23 21:02:09.017950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46d4d2b19794'
down_revision: Union[str, None] = 'eb3b4a82daf9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
