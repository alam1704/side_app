"""Initial migration

Revision ID: 0072d9e66e16
Revises: 
Create Date: 2021-11-18 11:37:20.609101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0072d9e66e16'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flasklogin-users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('pharmacies',
    sa.Column('pharmacy_id', sa.Integer(), nullable=False),
    sa.Column('pharmacy_name', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('pharmacy_id'),
    sa.UniqueConstraint('pharmacy_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pharmacies')
    op.drop_table('flasklogin-users')
    # ### end Alembic commands ###