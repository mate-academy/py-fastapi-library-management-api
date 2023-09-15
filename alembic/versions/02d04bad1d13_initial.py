"""initial

Revision ID: 02d04bad1d13
Revises: 330322221bd9
Create Date: 2023-09-15 19:53:54.376738

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02d04bad1d13'
down_revision: Union[str, None] = '330322221bd9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
