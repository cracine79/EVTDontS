"""Add video upload date, duration and transcript to chapter

Revision ID: 9c4e2b7a1d3f
Revises: 6a938e1b0606
Create Date: 2026-11-20

"""
from alembic import op
import sqlalchemy as sa


revision = '9c4e2b7a1d3f'
down_revision = '6a938e1b0606'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.add_column(sa.Column('video_upload_date', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('video_duration_seconds', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('transcript', sa.Text(), nullable=True))


def downgrade():
    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.drop_column('transcript')
        batch_op.drop_column('video_duration_seconds')
        batch_op.drop_column('video_upload_date')
