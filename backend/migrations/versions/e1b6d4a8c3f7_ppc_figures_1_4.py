"""Draw the 1.4a and 1.4b production possibilities pictures as figures

Six uploaded pictures become figures the app draws (frontend2 QuestionFigure.jsx): four
production possibilities curves (one shown as two side-by-side graphs) and one table. Questions
are found by their picture's address (ids differ between local and live databases); image_url is
kept as a fallback, and a question that already has a figure is left alone.

Revision ID: e1b6d4a8c3f7
Revises: d7a3c9e2f5b1
Create Date: 2026-11-23
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'e1b6d4a8c3f7'
down_revision = 'd7a3c9e2f5b1'
branch_labels = None
depends_on = None

# picture address -> figure
FIGURES = {'https://evtds-seeds.s3.us-east-2.amazonaws.com/PPF2.png': {'type': 'graph',
                                                             'alt': 'Production possibilities curve for Country '
                                                                    'D, bowed out, with franks on the vertical '
                                                                    'axis and beans on the horizontal axis. Point '
                                                                    'A is where the curve meets the franks axis. '
                                                                    'Point C is on the curve. Point B is inside '
                                                                    'the curve. Point D is outside the curve.',
                                                             'x': {'label': 'Beans', 'max': 10},
                                                             'y': {'label': 'Franks', 'max': 9},
                                                             'curves': [{'ppc': [8, 7], 'bow': 2}],
                                                             'points': [{'on': 0,
                                                                         'x': 0,
                                                                         'label': 'A',
                                                                         'pos': 'ne',
                                                                         'dot': True},
                                                                        {'at': [2.8, 3.4],
                                                                         'label': 'B',
                                                                         'pos': 'n',
                                                                         'dot': True},
                                                                        {'on': 0,
                                                                         'x': 5.6,
                                                                         'label': 'C',
                                                                         'pos': 'n',
                                                                         'dot': True},
                                                                        {'at': [9.2, 6.4],
                                                                         'label': 'D',
                                                                         'pos': 'n',
                                                                         'dot': True}]},
 'https://evtds-seeds.s3.us-east-2.amazonaws.com/PPF3.png': {'type': 'graph',
                                                             'alt': 'Bowed-out production possibilities curve '
                                                                    'with capital goods on the vertical axis and '
                                                                    'consumer goods on the horizontal axis. '
                                                                    'Points X, Y and Z are on the curve, from '
                                                                    'most capital goods to most consumer goods. '
                                                                    'Point W is inside the curve. Point V is '
                                                                    'outside the curve.',
                                                             'x': {'label': 'Consumer\nGoods', 'max': 10},
                                                             'y': {'label': 'Capital\nGoods', 'max': 9},
                                                             'curves': [{'ppc': [7, 7.5], 'bow': 2}],
                                                             'points': [{'on': 0,
                                                                         'x': 2,
                                                                         'label': 'X',
                                                                         'pos': 'ne',
                                                                         'dot': True},
                                                                        {'on': 0,
                                                                         'x': 4.4,
                                                                         'label': 'Y',
                                                                         'pos': 'ne',
                                                                         'dot': True},
                                                                        {'on': 0,
                                                                         'x': 6,
                                                                         'label': 'Z',
                                                                         'pos': 'e',
                                                                         'dot': True},
                                                                        {'at': [2.4, 3.4],
                                                                         'label': 'W',
                                                                         'pos': 'e',
                                                                         'dot': True},
                                                                        {'at': [8.4, 7.4],
                                                                         'label': 'V',
                                                                         'pos': 'e',
                                                                         'dot': True}]},
 'https://evtds-seeds.s3.us-east-2.amazonaws.com/PPFCapCity.png': {'type': 'graph',
                                                                   'alt': 'Production possibilities curve for '
                                                                          'Capital City, bowed out, with hip hop '
                                                                          'records on the vertical axis and metal '
                                                                          'records on the horizontal axis. Points '
                                                                          'A, B and C are on the curve, from most '
                                                                          'hip hop to most metal. Point E is '
                                                                          'inside the curve. Point D is outside '
                                                                          'the curve.',
                                                                   'x': {'label': 'Quantity of\nMetal Records',
                                                                         'max': 10},
                                                                   'y': {'label': 'Quantity of\nHip Hop Records',
                                                                         'max': 9},
                                                                   'curves': [{'ppc': [7, 7.5], 'bow': 2}],
                                                                   'points': [{'on': 0,
                                                                               'x': 2,
                                                                               'label': 'A',
                                                                               'pos': 'ne',
                                                                               'dot': True},
                                                                              {'on': 0,
                                                                               'x': 4.4,
                                                                               'label': 'B',
                                                                               'pos': 'ne',
                                                                               'dot': True},
                                                                              {'on': 0,
                                                                               'x': 6,
                                                                               'label': 'C',
                                                                               'pos': 'e',
                                                                               'dot': True},
                                                                              {'at': [8.4, 7.4],
                                                                               'label': 'D',
                                                                               'pos': 'e',
                                                                               'dot': True},
                                                                              {'at': [2.4, 3.4],
                                                                               'label': 'E',
                                                                               'pos': 'e',
                                                                               'dot': True}]},
 'https://evtds-seeds.s3.us-east-2.amazonaws.com/apple_cherry_ppf.png': {'type': 'graph',
                                                                         'alt': 'Straight-line production '
                                                                                'possibilities curve from 90 '
                                                                                'cherries on the vertical axis to '
                                                                                '30 apples on the horizontal '
                                                                                'axis.',
                                                                         'x': {'label': 'Apples', 'max': 50},
                                                                         'y': {'label': 'Cherries', 'max': 120},
                                                                         'curves': [{'points': [[0, 90], [30, 0]],
                                                                                     'color': 'supply'}],
                                                                         'xTicks': [[30, '30']],
                                                                         'yTicks': [[90, '90']]},
 'https://evtds-seeds.s3.us-east-2.amazonaws.com/Constant_increasing_PPF.png': {'type': 'panels',
                                                                                'alt': 'Two production '
                                                                                       'possibilities frontiers '
                                                                                       'for forks (vertical axis) '
                                                                                       'and knives (horizontal '
                                                                                       'axis). Figure A is bowed '
                                                                                       'out from the origin. '
                                                                                       'Figure B is a straight '
                                                                                       'line.',
                                                                                'panels': [{'type': 'graph',
                                                                                            'caption': 'Figure A',
                                                                                            'x': {'label': 'Knives',
                                                                                                  'max': 10},
                                                                                            'y': {'label': 'Forks',
                                                                                                  'max': 9},
                                                                                            'curves': [{'ppc': [7.5,
                                                                                                                7],
                                                                                                        'bow': 2}]},
                                                                                           {'type': 'graph',
                                                                                            'caption': 'Figure B',
                                                                                            'x': {'label': 'Knives',
                                                                                                  'max': 10},
                                                                                            'y': {'label': 'Forks',
                                                                                                  'max': 9},
                                                                                            'curves': [{'points': [[0,
                                                                                                                    7],
                                                                                                                   [8,
                                                                                                                    0]]}]}]},
 'https://evtds-seeds.s3.us-east-2.amazonaws.com/PPF_Opp_cost_table.png': {'type': 'table',
                                                                           'columns': ['Good A (units)',
                                                                                       'Good B (units)'],
                                                                           'rows': [[0, 50],
                                                                                    [10, 47],
                                                                                    [20, 41],
                                                                                    [30, 32],
                                                                                    [40, 20],
                                                                                    [50, 0]]}}


def upgrade():
    conn = op.get_bind()
    for url, figure in FIGURES.items():
        conn.execute(sa.text("UPDATE question SET figure = CAST(:f AS JSON) WHERE image_url = :u AND figure IS NULL"),
                     {'f': json.dumps(figure), 'u': url})


def downgrade():
    conn = op.get_bind()
    for url in FIGURES:
        conn.execute(sa.text("UPDATE question SET figure = NULL WHERE image_url = :u"), {'u': url})
