"""empty message

Revision ID: fda01c3a45c8
Revises: 747df35cef47
Create Date: 2024-09-03 09:12:31.863507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fda01c3a45c8'
down_revision = '747df35cef47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_chapter_progress', schema=None) as batch_op:
        batch_op.alter_column('quiz_grade',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               type_=sa.Integer(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_chapter_progress', schema=None) as batch_op:
        batch_op.alter_column('quiz_grade',
               existing_type=sa.Integer(),
               type_=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)

    # ### end Alembic commands ###
