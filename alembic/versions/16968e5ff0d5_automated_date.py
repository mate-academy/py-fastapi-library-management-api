"""Automated date

Revision ID: 16968e5ff0d5
Revises: 8b1f375d0dc4
Create Date: 2024-03-09 17:56:56.798310

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16968e5ff0d5'
down_revision: Union[str, None] = '8b1f375d0dc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
