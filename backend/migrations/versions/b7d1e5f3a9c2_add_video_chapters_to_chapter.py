"""Add YouTube key moments (description timestamps) to chapter

Revision ID: b7d1e5f3a9c2
Revises: 9c4e2b7a1d3f
Create Date: 2026-11-20

"""
from alembic import op
import sqlalchemy as sa


revision = 'b7d1e5f3a9c2'
down_revision = '9c4e2b7a1d3f'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.add_column(sa.Column('video_chapters', sa.JSON(), nullable=True))


def downgrade():
    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.drop_column('video_chapters')
