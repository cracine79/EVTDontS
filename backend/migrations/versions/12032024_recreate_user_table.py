"""RECREATE USER MODEL AFTER THE FACT

Revision ID: 12032024
Revises: 
Create Date: 2024-12-03

"""

from alembic import op
import sqlalchemy as sa


revision = '12032024'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password_hash', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),                
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('email')
    )

def downgrade():
    op.drop_table('user')