"""third commit

Revision ID: a28878687280
Revises: 46d4d2b19794
Create Date: 2024-07-23 21:23:04.720690

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a28878687280'
down_revision: Union[str, None] = '46d4d2b19794'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
