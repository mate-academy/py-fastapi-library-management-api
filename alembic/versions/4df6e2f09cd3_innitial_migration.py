"""Innitial migration

Revision ID: 4df6e2f09cd3
Revises: f031f82c91b3
Create Date: 2023-04-07 15:44:37.185219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4df6e2f09cd3'
down_revision = 'f031f82c91b3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('bio', sa.String(length=512), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_author_id'), 'author', ['id'], unique=False)
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('summary', sa.String(length=512), nullable=True),
    sa.Column('publication_date', sa.Date(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_book_id'), 'book', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_book_id'), table_name='book')
    op.drop_table('book')
    op.drop_index(op.f('ix_author_id'), table_name='author')
    op.drop_table('author')
    # ### end Alembic commands ###
