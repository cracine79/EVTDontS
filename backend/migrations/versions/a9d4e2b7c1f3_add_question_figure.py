"""Add question.figure (graphs and tables drawn by the app) and draw the price ceiling diagram

question.figure holds a graph or table described as data (see frontend2 QuestionFigure.jsx); the app
shows it instead of question.image_url. The 4.3 Price Ceilings questions that used the
PCPFFinalpng.png picture get the same diagram as a figure. They're found by that picture's address
(not by id, since ids differ between local and live databases), and image_url is kept as a fallback.
Also fixes the marked-correct answer on one of those questions (Q3 -> Q1).

Revision ID: a9d4e2b7c1f3
Revises: f2a6b8c4d9e1
Create Date: 2026-11-23
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'a9d4e2b7c1f3'
down_revision = 'f2a6b8c4d9e1'
branch_labels = None
depends_on = None

PRICE_CEILING_IMAGE = 'https://evtds-seeds.s3.us-east-2.amazonaws.com/PCPFFinalpng.png'

PRICE_CEILING_FIGURE = {'type': 'graph',
 'alt': 'Supply and demand graph. Demand slopes down from P5 and supply slopes up from P1; they cross at '
        'point D, at price P3 and quantity Q2. At price P4, point A is on demand at Q1 and point B is on '
        'supply at Q3. At price P2, point E is on supply at Q1, point F is below D at Q2, and point G is on '
        'demand at Q3. Point C is at price P3 and quantity Q1.',
 'x': {'label': 'Quantity', 'max': 10},
 'y': {'label': 'Price', 'max': 10},
 'origin': '0',
 'curves': [{'label': 'Demand', 'points': [[0, 9], [8.5, 0.5]], 'color': 'demand'},
            {'label': 'Supply', 'points': [[0, 1], [8.5, 9.5]], 'color': 'supply'}],
 'guides': [[[0, 7], [6, 7]],
            [[0, 5], [4, 5]],
            [[0, 3], [6, 3]],
            [[2, 7], [2, 0]],
            [[4, 5], [4, 0]],
            [[6, 7], [6, 0]]],
 'xTicks': [[2, 'Q1'], [4, 'Q2'], [6, 'Q3']],
 'yTicks': [[9, 'P5'], [7, 'P4'], [5, 'P3'], [3, 'P2'], [1, 'P1']],
 'points': [{'at': [2, 7], 'label': 'A', 'pos': 'ne'},
            {'at': [6, 7], 'label': 'B', 'pos': 'e'},
            {'at': [2, 5], 'label': 'C', 'pos': 'nw'},
            {'at': [4, 5], 'label': 'D', 'pos': 'n'},
            {'at': [2, 3], 'label': 'E', 'pos': 'nw'},
            {'at': [4, 3], 'label': 'F', 'pos': 'nw'},
            {'at': [6, 3], 'label': 'G', 'pos': 'ne'}]}


def upgrade():
    op.add_column('question', sa.Column('figure', sa.JSON(), nullable=True))
    op.get_bind().execute(
        sa.text("UPDATE question SET figure = CAST(:figure AS JSON) WHERE image_url = :url AND figure IS NULL"),
        {'figure': json.dumps(PRICE_CEILING_FIGURE), 'url': PRICE_CEILING_IMAGE})
    # The correct answer to "If a price ceiling is implemented at P2, which of the following is true?"
    # named the wrong rectangle: at P2 only Q1 is sold, so producer revenue is P2, E, Q1, 0 (not Q3).
    # Matched by its old text on a question using the price ceiling picture; a no-op once fixed.
    op.get_bind().execute(
        sa.text("UPDATE answer SET text = :new FROM question "
                "WHERE answer.question_id = question.id AND question.image_url = :url AND answer.text = :old"),
        {'old': 'Total producer revenue changes from area P3,D,Q2,0 to P2, E, Q3, 0',
         'new': 'Total producer revenue changes from area P3,D,Q2,0 to P2, E, Q1, 0',
         'url': PRICE_CEILING_IMAGE})


def downgrade():
    op.drop_column('question', 'figure')
