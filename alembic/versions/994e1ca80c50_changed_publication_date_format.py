"""Changed publication_date format

Revision ID: 994e1ca80c50
Revises: 012d20fe4cb6
Create Date: 2025-11-25 21:55:26.547355

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '994e1ca80c50'
down_revision: Union[str, None] = '012d20fe4cb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - SQLite compatible version."""
    # Create a new table with the correct schema
    op.create_table('books_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('summary', sa.String(), nullable=True),
        sa.Column('publication_date', sa.Date(), nullable=True),  # Changed to Date
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('title')
    )

    # Copy data from old table to new table, converting datetime to date
    op.execute("""
        INSERT INTO books_new (id, title, summary, publication_date, author_id)
        SELECT id, title, summary, DATE(publication_date), author_id FROM books
    """)

    # Drop old table and rename new table
    op.drop_table('books')
    op.rename_table('books_new', 'books')


def downgrade() -> None:
    """Downgrade schema - SQLite compatible version."""
    # Create table with datetime format
    op.create_table('books_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('summary', sa.String(), nullable=True),
        sa.Column('publication_date', sa.DateTime(), nullable=True),  # Back to DateTime
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('title')
    )

    # Copy data back (date will be converted back to datetime automatically)
    op.execute("""
        INSERT INTO books_new (id, title, summary, publication_date, author_id)
        SELECT id, title, summary, publication_date, author_id FROM books
    """)

    op.drop_table('books')
    op.rename_table('books_new', 'books')
