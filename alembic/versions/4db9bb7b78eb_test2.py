"""test2

Revision ID: 4db9bb7b78eb
Revises: 900b084825af
Create Date: 2024-07-23 21:39:20.568250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4db9bb7b78eb'
down_revision: Union[str, None] = '900b084825af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
