"""empty message

Revision ID: 9247c6882078
Revises: 6c64397d8c1b
Create Date: 2024-09-03 11:58:11.174497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9247c6882078'
down_revision = '6c64397d8c1b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.drop_constraint('chapter_user_id_fkey', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('chapter_user_id_fkey', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###