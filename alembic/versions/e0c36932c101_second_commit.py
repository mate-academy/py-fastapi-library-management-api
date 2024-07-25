"""second commit

Revision ID: e0c36932c101
Revises: 214e6c762ead
Create Date: 2024-07-23 20:26:53.116318

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0c36932c101'
down_revision: Union[str, None] = '214e6c762ead'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
