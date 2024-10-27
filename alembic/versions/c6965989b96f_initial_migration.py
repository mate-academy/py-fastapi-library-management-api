"""Initial migration

Revision ID: c6965989b96f
Revises: 95a1fd846f59
Create Date: 2024-10-27 13:43:39.412409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6965989b96f'
down_revision: Union[str, None] = '95a1fd846f59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("books", schema=None) as batch_op:
        batch_op.create_foreign_key("fk_author_id", "authors", ["author_id"], ["id"])

def downgrade():
    with op.batch_alter_table("books", schema=None) as batch_op:
        batch_op.drop_constraint("fk_author_id", type_="foreignkey")
