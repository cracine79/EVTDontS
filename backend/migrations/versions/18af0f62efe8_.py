"""empty message

Revision ID: 18af0f62efe8
Revises: 9247c6882078
Create Date: 2024-09-03 13:41:22.073416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18af0f62efe8'
down_revision = '9247c6882078'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_chapter_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'chapter', ['current_chapter_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('current_chapter_id')

    # ### end Alembic commands ###
