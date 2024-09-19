"""add order column to Chapter

Revision ID: 562e26f20306
Revises: 0b32e2b9e376
Create Date: 2024-09-19 11:11:44.133273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '562e26f20306'
down_revision = '0b32e2b9e376'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.drop_column('order')

    # ### end Alembic commands ###
