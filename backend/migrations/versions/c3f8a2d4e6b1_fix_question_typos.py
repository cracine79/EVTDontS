"""Fix quiz typos: "grain and steel" in a guns-and-butter question, "Taloronia", and "Disequlibrium" topic names.

Data-only migration. Matches on the exact old text, so it's safe to run on any copy of the database.

Revision ID: c3f8a2d4e6b1
Revises: b7d1e5f3a9c2
Create Date: 2026-11-22
"""
from alembic import op
import sqlalchemy as sa


revision = 'c3f8a2d4e6b1'
down_revision = 'b7d1e5f3a9c2'
branch_labels = None
depends_on = None

FIXES = [
    ('Import both grain and steel and export nothing.',
     'Import both guns and butter and export nothing.'),
    ('Trade 1 ton of grain for 0.5 tons of steel.',
     'Trade 1 ton of guns for 0.5 tons of butter.'),
    ('The opportunity cost of producing synthesizers is higher in Taloronia than Davenia.',
     'The opportunity cost of producing synthesizers is higher in Tayloronia than Davenia.'),
]


TOPIC_FIXES = [
    ('Disequlibrium - Shifts to Demand', 'Disequilibrium - Shifts to Demand'),
    ('Disequlibrium - Shifts to Supply', 'Disequilibrium - Shifts to Supply'),
]


def _apply(table, pairs):
    conn = op.get_bind()
    column = 'text' if table == 'answer' else 'name'
    for old, new in pairs:
        conn.execute(sa.text(f'UPDATE {table} SET {column} = :new WHERE {column} = :old'), {'old': old, 'new': new})


def upgrade():
    _apply('answer', FIXES)
    _apply('question_topic', TOPIC_FIXES)


def downgrade():
    _apply('answer', [(new, old) for old, new in FIXES])
    _apply('question_topic', [(new, old) for old, new in TOPIC_FIXES])
