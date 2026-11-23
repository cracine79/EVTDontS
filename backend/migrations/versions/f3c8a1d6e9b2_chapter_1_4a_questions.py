"""Chapter 1.4a: subtopic names and fifteen new questions (ten with drawn figures)

Reviewed and approved in the "Chapter 1.4a Question Review" doc (2026-11-23):
  * Topics renamed: Reading the PPC (was PPF Interpretation) / Shifts vs Movements Along the PPC (was
    PPF Shifts vs Movement). Existing questions stay where they are; no fixes needed.
  * Six new Reading questions and nine new Shifts questions. Ten use figures the app draws
    (frontend2 QuestionFigure.jsx): one table, four graphs and a four-graph panel, several shared.

Matched by chapter and topic name (ids differ between local and live databases); each step is a
no-op once applied.

Revision ID: f3c8a1d6e9b2
Revises: e1b6d4a8c3f7
Create Date: 2026-11-23
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'f3c8a1d6e9b2'
down_revision = 'e1b6d4a8c3f7'
branch_labels = None
depends_on = None

CHAPTER = '1.4a The Production Possibilities Curve'
READING = ('PPF Interpretation', 'Reading the PPC')
SHIFTS = ('PPF Shifts vs Movement', 'Shifts vs Movements Along the PPC')

FIGURES = {'F1': {'type': 'table',
        'caption': 'Production possibilities for Islandia',
        'columns': ['Option', 'Lobsters', 'Coconuts'],
        'rows': [['A', 10, 0], ['B', 8, 3], ['C', 6, 6], ['D', 4, 9], ['E', 2, 12], ['F', 0, 15]]},
 'F2': {'type': 'graph',
        'alt': 'Bowed-out production possibilities curve with guns on the vertical axis and butter on the '
               'horizontal axis. Point L is where the curve meets the guns axis. Point J is on the curve. Point K '
               'is inside the curve. Point M is outside the curve.',
        'x': {'label': 'Butter', 'max': 10},
        'y': {'label': 'Guns', 'max': 9},
        'curves': [{'ppc': [7.5, 7], 'bow': 2}],
        'points': [{'on': 0, 'x': 0, 'label': 'L', 'pos': 'ne', 'dot': True},
                   {'on': 0, 'x': 5, 'label': 'J', 'pos': 'ne', 'dot': True},
                   {'at': [2.6, 3], 'label': 'K', 'pos': 'e', 'dot': True},
                   {'at': [8.6, 6.4], 'label': 'M', 'pos': 'e', 'dot': True}]},
 'F3': {'type': 'graph',
        'alt': 'Bowed-out production possibilities curve with military goods on the vertical axis and consumer '
               'goods on the horizontal axis. Point Q is on the curve with more military goods; point P is on the '
               'curve with more consumer goods.',
        'x': {'label': 'Consumer\nGoods', 'max': 10},
        'y': {'label': 'Military\nGoods', 'max': 9},
        'curves': [{'ppc': [7.5, 7], 'bow': 2}],
        'points': [{'on': 0, 'x': 2.4, 'label': 'Q', 'pos': 'ne', 'dot': True},
                   {'on': 0, 'x': 5.8, 'label': 'P', 'pos': 'ne', 'dot': True}]},
 'F4': {'type': 'graph',
        'alt': 'Two production possibilities curves for fish (vertical axis) and coconuts (horizontal axis). PPC1 '
               'runs from 5 fish to 6 coconuts. PPC2, dashed, runs from 8 fish to the same 6 coconuts.',
        'x': {'label': 'Coconuts', 'max': 10},
        'y': {'label': 'Fish', 'max': 10},
        'curves': [{'ppc': [6, 5], 'bow': 2, 'label': 'PPC₁', 'labelAt': [1.2, 3.4]},
                   {'ppc': [6, 8],
                    'bow': 2,
                    'dashed': True,
                    'color': 'supply',
                    'label': 'PPC₂',
                    'labelAt': [4.4, 6.6]}],
        'arrows': [{'from': [0.5, 5.3], 'to': [0.5, 7.5]}]},
 'F5': {'type': 'panels',
        'alt': 'Four graphs, each with fish on the vertical axis, coconuts on the horizontal axis, an original '
               'curve PPC1 and a dashed new curve PPC2. Graph I: PPC2 is outward on both axes. Graph II: PPC2 is '
               'outward on the coconuts axis only. Graph III: PPC2 is outward on the fish axis only. Graph IV: '
               'PPC2 is inward on both axes.',
        'panels': [{'type': 'graph',
                    'caption': 'Graph I',
                    'x': {'label': 'Coconuts', 'max': 10},
                    'y': {'label': 'Fish', 'max': 10},
                    'curves': [{'ppc': [5, 5], 'bow': 2},
                               {'ppc': [7.5, 7.5], 'bow': 2, 'dashed': True, 'color': 'supply'}]},
                   {'type': 'graph',
                    'caption': 'Graph II',
                    'x': {'label': 'Coconuts', 'max': 10},
                    'y': {'label': 'Fish', 'max': 10},
                    'curves': [{'ppc': [5, 5], 'bow': 2},
                               {'ppc': [8, 5], 'bow': 2, 'dashed': True, 'color': 'supply'}]},
                   {'type': 'graph',
                    'caption': 'Graph III',
                    'x': {'label': 'Coconuts', 'max': 10},
                    'y': {'label': 'Fish', 'max': 10},
                    'curves': [{'ppc': [5, 5], 'bow': 2},
                               {'ppc': [5, 8], 'bow': 2, 'dashed': True, 'color': 'supply'}]},
                   {'type': 'graph',
                    'caption': 'Graph IV',
                    'x': {'label': 'Coconuts', 'max': 10},
                    'y': {'label': 'Fish', 'max': 10},
                    'curves': [{'ppc': [7, 7], 'bow': 2},
                               {'ppc': [4.5, 4.5], 'bow': 2, 'dashed': True, 'color': 'supply'}]}]},
 'F6': {'type': 'graph',
        'alt': 'Two production possibilities curves for capital goods (vertical axis) and consumer goods '
               '(horizontal axis). PPC2, dashed, lies outside PPC1 on both axes. Point A is on PPC1. Point B is '
               'on PPC2, outside PPC1.',
        'x': {'label': 'Consumer\nGoods', 'max': 10},
        'y': {'label': 'Capital\nGoods', 'max': 10},
        'curves': [{'ppc': [5.5, 5.5], 'bow': 2, 'label': 'PPC₁', 'labelAt': [0.6, 4.2]},
                   {'ppc': [8, 8],
                    'bow': 2,
                    'dashed': True,
                    'color': 'supply',
                    'label': 'PPC₂',
                    'labelAt': [7.3, 4.3]}],
        'points': [{'on': 0, 'x': 3.9, 'label': 'A', 'pos': 'sw', 'dot': True},
                   {'on': 1, 'x': 5.7, 'label': 'B', 'pos': 'ne', 'dot': True}]}}

# (topic, figure key or None, text, video_start seconds, [(answer, is_correct), ...] in A-E order)
NEW_QUESTIONS = [('reading',
  'F1',
  'The table above shows the maximum combinations of lobsters and coconuts Islandia can produce in a day using '
  'all of its resources efficiently. Which of the following combinations is attainable but inefficient?',
  208,
  [('8 lobsters and 3 coconuts', False),
   ('4 lobsters and 6 coconuts', True),
   ('6 lobsters and 8 coconuts', False),
   ('2 lobsters and 13 coconuts', False),
   ('0 lobsters and 15 coconuts', False)]),
 ('reading',
  'F1',
  'The table above shows the maximum combinations of lobsters and coconuts Islandia can produce in a day using '
  'all of its resources efficiently. Producing 6 lobsters and 8 coconuts in a day is',
  393,
  [('attainable and efficient', False),
   ('attainable but inefficient', False),
   ("unattainable with Islandia's current resources", True),
   ('attainable, because 6 lobsters appears in the table', False),
   ('attainable, because 8 coconuts is less than the 15 Islandia can produce', False)]),
 ('reading',
  'F2',
  'Using the production possibilities curve for guns and butter shown above, which of the following points '
  'represent efficient levels of output?<br><br>I. Point J<br>II. Point K<br>III. Point L',
  505,
  [('I only', False),
   ('II only', False),
   ('I and III only', True),
   ('II and III only', False),
   ('I, II and III', False)]),
 ('reading',
  'F2',
  "The graph above shows an economy's production possibilities curve for guns and butter. If the economy is "
  'producing at point K, it can produce more guns and more butter without any additional resources because',
  459,
  [('point K is unattainable', False),
   ('some of its resources are unemployed or not used efficiently', True),
   ('producing more of one good never requires producing less of the other', False),
   ('its production possibilities curve will shift outward automatically', False),
   ('point K is an efficient level of output', False)]),
 ('reading',
  None,
  'A production possibilities curve shows',
  371,
  [('all combinations of two goods an economy can produce when it uses all of its available resources efficiently',
    True),
   ('the combinations of two goods consumers most want to buy', False),
   ("the combination of two goods that maximizes firms' profits", False),
   ('the prices of two goods', False),
   ('how much of two goods the economy produced last year', False)]),
 ('reading',
  'F3',
  'A country is producing at point P on the production possibilities curve shown above. If it moves to point Q, '
  'which of the following is true?',
  720,
  [('It produces more military goods and fewer consumer goods.', True),
   ('It produces more of both goods.', False),
   ('It moves from efficient to inefficient output.', False),
   ('Its production possibilities curve has shifted outward.', False),
   ('It gives up nothing, because both points are efficient.', False)]),
 ('shifts',
  'F2',
  "The graph above shows an economy's production possibilities curve for guns and butter. Point M could become "
  'attainable if the economy',
  669,
  [('gains more or better factors of production', True),
   ('uses its current resources more fully', False),
   ('produces fewer guns', False),
   ('produces less butter', False),
   ('moves from point J to point L', False)]),
 ('shifts',
  'F4',
  'The shift from PPC₁ to PPC₂ shown above is most likely the result of',
  536,
  [('a new tool that makes catching fish easier', True),
   ('better tree-climbing skills that speed up coconut collection', False),
   ('an improvement that helps produce both goods', False),
   ('putting unemployed workers back to work', False),
   ('a decrease in the number of coconut trees', False)]),
 ('shifts',
  'F5',
  "In each of Graphs I–IV above, PPC₁ (solid) is an economy's original production possibilities curve and PPC₂ "
  '(dashed) is its new curve. Which graph best shows the effect of workers becoming stronger, so they can collect '
  'coconuts faster but catch fish no faster?',
  570,
  [('Graph I', False),
   ('Graph II', True),
   ('Graph III', False),
   ('Graph IV', False),
   ('None of the graphs', False)]),
 ('shifts',
  'F5',
  "In each of Graphs I–IV above, PPC₁ (solid) is an economy's original production possibilities curve and PPC₂ "
  '(dashed) is its new curve. Which graph best shows the effect of a new fishing technology that makes catching '
  'fish faster but does not affect coconut collection?',
  546,
  [('Graph I', False),
   ('Graph II', False),
   ('Graph III', True),
   ('Graph IV', False),
   ('None of the graphs', False)]),
 ('shifts',
  'F5',
  "In each of Graphs I–IV above, PPC₁ (solid) is an economy's original production possibilities curve and PPC₂ "
  '(dashed) is its new curve. Which graph best shows the effect of higher education levels that make workers '
  'better at producing both goods?',
  795,
  [('Graph I', True),
   ('Graph II', False),
   ('Graph III', False),
   ('Graph IV', False),
   ('None of the graphs', False)]),
 ('shifts',
  None,
  "Which of the following would cause a movement along a country's production possibilities curve rather than a "
  'shift of the curve?',
  738,
  [('Moving workers from producing consumer goods to producing military goods', True),
   ('Discovering new natural resources', False),
   ('An increase in literacy rates', False),
   ('New and better machinery', False),
   ('An increase in the number of workers', False)]),
 ('shifts',
  None,
  "Which of the following could cause a country's production possibilities curve to shift outward?<br><br>I. An "
  'increase in the size of the labor force<br>II. Better-educated workers<br>III. A decision to produce more '
  'consumer goods and fewer military goods',
  669,
  [('I only', False),
   ('II only', False),
   ('I and II only', True),
   ('II and III only', False),
   ('I, II and III', False)]),
 ('shifts',
  None,
  'An economy moves from a point inside its production possibilities curve to a point on its curve. This movement '
  'represents',
  480,
  [('a more efficient use of its existing resources', True),
   ('economic growth', False),
   ('an outward shift of its production possibilities curve', False),
   ('an improvement in technology', False),
   ('an increase in its factors of production', False)]),
 ('shifts',
  'F6',
  "The graph above shows an economy's production possibilities curve shifting from PPC₁ to PPC₂. Which of the "
  'following is true about point B?',
  530,
  [('It is unattainable on PPC₁ but attainable and efficient on PPC₂.', True),
   ('It is attainable on PPC₁ but inefficient.', False),
   ('It is inefficient on PPC₂.', False),
   ('It can be reached from point A without any additional resources.', False),
   ('It requires fewer resources to produce than point A.', False)])]


def upgrade():
    conn = op.get_bind()
    one = lambda sql, **kw: conn.execute(sa.text(sql), kw).scalar()
    run = lambda sql, **kw: conn.execute(sa.text(sql), kw)

    chapter_id = one("SELECT id FROM chapter WHERE name = :n", n=CHAPTER)
    if chapter_id is None:
        return
    topics = {}
    for key, (old, new) in (('reading', READING), ('shifts', SHIFTS)):
        run("UPDATE question_topic SET name = :new WHERE chapter_id = :c AND name = :old", new=new, old=old, c=chapter_id)
        topics[key] = one("SELECT id FROM question_topic WHERE chapter_id = :c AND name = :n", c=chapter_id, n=new)

    for which, fig, text, start, answers in NEW_QUESTIONS:
        if one("SELECT count(*) FROM question WHERE chapter_id = :c AND text = :t", c=chapter_id, t=text):
            continue
        qid = one("INSERT INTO question (text, chapter_id, topic_id, video_start, figure) "
                  "VALUES (:t, :c, :tp, :v, CAST(:f AS JSON)) RETURNING id",
                  t=text, c=chapter_id, tp=topics[which], v=start, f=json.dumps(FIGURES[fig]) if fig else None)
        for answer, correct in answers:
            run("INSERT INTO answer (text, question_id, is_correct) VALUES (:t, :q, :c)", t=answer, q=qid, c=correct)


def downgrade():
    # Not reversible once students have answered the new questions; restore from a backup if needed.
    pass
