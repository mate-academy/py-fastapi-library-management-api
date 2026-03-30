"""dd uniq to title field in DBBook

Revision ID: 80100b21d4f4
Revises: 9dfaa5d54278
Create Date: 2026-03-30 22:11:26.707997

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "80100b21d4f4"
down_revision: Union[str, Sequence[str], None] = "9dfaa5d54278"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("books", schema=None) as batch_op:
        batch_op.create_index("ix_books_title_unique", ["title"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("books", schema=None) as batch_op:
        batch_op.drop_index("ix_books_title_unique")
