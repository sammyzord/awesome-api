"""add user model

Revision ID: 6717d6c7a259
Revises: 77af61c17c9a
Create Date: 2022-03-19 21:48:20.372138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6717d6c7a259'
down_revision = '77af61c17c9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=25), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('recovery_key', sa.String(), nullable=True),
    sa.Column('refresh_token', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
