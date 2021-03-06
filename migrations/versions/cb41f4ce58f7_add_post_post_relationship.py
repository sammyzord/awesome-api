"""add post-post relationship

Revision ID: cb41f4ce58f7
Revises: feb7af9e3a29
Create Date: 2022-03-22 21:20:40.818759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb41f4ce58f7'
down_revision = 'feb7af9e3a29'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('parent_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'posts', 'posts', ['parent_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'parent_id')
    # ### end Alembic commands ###
