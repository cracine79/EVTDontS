"""Add search_vector column with GIN index

Revision ID: 1318a15852da
Revises: 5a61937f2b9d
Create Date: 2024-12-18 09:10:05.713126

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1318a15852da'
down_revision = '5a61937f2b9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.add_column(sa.Column('search_vector', postgresql.TSVECTOR(), nullable=True))
    
    op.create_index('search_vector_idx', 'chapter', ['search_vector'], unique=False, postgresql_using='gin')

    op.execute("""
    CREATE OR REPLACE FUNCTION update_search_vector() RETURNS trigger AS $$
    BEGIN
    NEW.search_vector = to_tsvector('english', NEW.name || ' ' || NEW.quiz_blurb || ' ' || NEW.video_blurb);
    RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_update_search_vector
    BEFORE INSERT OR UPDATE ON chapter
    FOR EACH ROW EXECUTE FUNCTION update_search_vector();
    """)




    # ### end Alembic commands ###


def downgrade():
    op.execute("""
    DROP TRIGGER IF EXISTS trigger_update_search_vector ON chapter;
    DROP FUNCTION IF EXISTS update_search_vector;
    """)

    op.drop_index('search_vector_idx', table_name='chapter')

    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chapter', schema=None) as batch_op:
        batch_op.drop_column('search_vector')

    # ### end Alembic commands ###