"""Chapter 2.5: three subtopics, thirteen new questions, one picture redrawn

Reviewed and approved in the "Chapter 2.5 Question Review" doc (2026-11-23):
  * Topics: Predicting Price and Quantity (was Simultaneous Shifts to Supply and Demand; keeps six) /
    Simultaneous Shifts on a Graph (new; takes the two quadrant questions) / Working Backward from
    Price and Quantity (new; takes the four "last year / last month" questions).
  * The quadrant picture becomes a drawn figure (supply blue, demand red).
  * Four new predicting, five new graph (one new drawn figure) and four new working-backward questions.

Matched by chapter name, topic name, question text and picture address (ids differ between local and
live databases); each step is a no-op once applied. Students' per-topic running totals move with the
questions, as in b4c8e1f6a2d9 (chapter 1.1).

Revision ID: d9b5e3a7f1c4
Revises: c6f2a9e4d8b1
Create Date: 2026-11-23
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'd9b5e3a7f1c4'
down_revision = 'c6f2a9e4d8b1'
branch_labels = None
depends_on = None

CHAPTER = '2.5 Simultaneous Shifts to Supply and Demand'
PREDICT = ('Simultaneous Shifts to Supply and Demand', 'Predicting Price and Quantity')
GRAPH = 'Simultaneous Shifts on a Graph'
BACKWARD = 'Working Backward from Price and Quantity'

QUAD_URL = 'https://evtds-seeds.s3.us-east-2.amazonaws.com/SDABCD.png'
BACKWARD_PATTERN = 'Last %'

FIGURES = {'QUAD': {'type': 'graph',
          'alt': 'An upward-sloping supply curve and a downward-sloping demand curve crossing in the middle of '
                 'the graph. The curves divide the graph into four regions around the equilibrium point: A above '
                 'it, B to its right, C below it and D to its left.',
          'x': {'label': 'Quantity', 'max': 10},
          'y': {'label': 'Price', 'max': 10},
          'xTicks': [],
          'yTicks': [],
          'curves': [{'points': [[0.5, 0.5], [9.5, 9.5]], 'label': 'Supply', 'labelAt': [9.6, 9.3], 'color': 'supply'},
                     {'points': [[0.5, 9.5], [9.5, 0.5]], 'label': 'Demand', 'labelAt': [9.6, 0.4], 'color': 'demand'}],
          'points': [{'at': [5, 8], 'label': 'A', 'pos': 'n'},
                     {'at': [8.2, 5], 'label': 'B', 'pos': 'n'},
                     {'at': [5, 1.6], 'label': 'C', 'pos': 'n'},
                     {'at': [1.8, 5], 'label': 'D', 'pos': 'n'}]},
 'TWO': {'type': 'graph',
         'alt': 'Demand shifts right from D1 to D2 and supply shifts right from S1 to S2, with supply shifting '
                'further. The first equilibrium E1 is at price P1 and quantity Q1; the new equilibrium E2 is at '
                'the lower price P2 and the higher quantity Q2.',
         'x': {'label': 'Quantity', 'max': 13},
         'y': {'label': 'Price', 'max': 12},
         'xTicks': [[5, 'Q₁'], [8, 'Q₂']],
         'yTicks': [[5, 'P₁'], [4, 'P₂']],
         'origin': '0',
         'curves': [{'points': [[1, 9], [9, 1]], 'label': 'D₁', 'color': 'demand'},
                    {'points': [[2, 10], [11, 1]], 'label': 'D₂', 'color': 'demand'},
                    {'points': [[1, 1], [10, 10]], 'label': 'S₁', 'color': 'supply'},
                    {'points': [[4.5, 0.5], [12, 8]], 'label': 'S₂', 'color': 'supply'}],
         'guides': [[[0, 5], [5, 5]], [[5, 0], [5, 5]], [[0, 4], [8, 4]], [[8, 0], [8, 4]]],
         'points': [{'at': [5, 5], 'label': 'E₁', 'pos': 'e', 'dot': True},
                    {'at': [8, 4], 'label': 'E₂', 'pos': 'e', 'dot': True}]}}

PQ = lambda p, q: f'Price: {p}, Quantity: {q}'
DS = lambda d, s: f'Demand: {d}, Supply: {s}'
TWO_STEM = 'The graph above shows demand shifting from D₁ to D₂ and supply shifting from S₁ to S₂. '

# (topic, figure, text, video_start seconds, [(answer, is_correct), ...]) in A-E order
NEW_QUESTIONS = [('predict',
  None,
  'More students enroll in college, increasing the demand for textbooks. At the same time, the cost of running '
  'printing presses falls. As a result, the equilibrium price and quantity of textbooks are expected to change '
  'in which of the following ways?',
  41,
  [(PQ('Increase', 'Increase'), False),
   (PQ('Decrease', 'Increase'), False),
   (PQ('Indeterminate', 'Increase'), True),
   (PQ('Increase', 'Indeterminate'), False),
   (PQ('Indeterminate', 'Decrease'), False)]),
 ('predict',
  None,
  'In early 2020, the demand for hand sanitizer rose sharply, while factory shutdowns decreased its supply. As '
  'a result, the equilibrium price and quantity of hand sanitizer were expected to change in which of the '
  'following ways?',
  556,
  [(PQ('Increase', 'Increase'), False),
   (PQ('Increase', 'Indeterminate'), True),
   (PQ('Indeterminate', 'Increase'), False),
   (PQ('Indeterminate', 'Decrease'), False),
   (PQ('Decrease', 'Indeterminate'), False)]),
 ('predict',
  None,
  'The demand for and supply of a good both decrease. Which of the following must be true?<br><br>I. '
  'Equilibrium quantity falls<br>II. Equilibrium price falls<br>III. Whether equilibrium price rises or falls '
  'depends on the relative sizes of the two shifts',
  280,
  [('I only', False),
   ('II only', False),
   ('I and III only', True),
   ('II and III only', False),
   ('I, II and III', False)]),
 ('predict',
  None,
  'In the market for a good, supply increases and demand decreases. If the increase in supply is much larger '
  'than the decrease in demand, which of the following is most likely?',
  354,
  [('Equilibrium price falls and equilibrium quantity rises.', True),
   ('Equilibrium price falls and equilibrium quantity falls.', False),
   ('Equilibrium price rises and equilibrium quantity rises.', False),
   ('Equilibrium price rises and equilibrium quantity falls.', False),
   ('Equilibrium price and equilibrium quantity do not change.', False)]),
 ('graph',
  'QUAD',
  'The above diagram shows the market in equilibrium for textbooks. If the demand for textbooks and the supply '
  'of textbooks both increase, we know that the new equilibrium point must land somewhere in:',
  388,
  [('Quadrant A, meaning price definitely increases', False),
   ('Quadrant B, meaning quantity definitely increases', True),
   ('Quadrant C, meaning price definitely decreases', False),
   ('Quadrant D, meaning quantity definitely decreases', False),
   ('Quadrant B, meaning price definitely increases', False)]),
 ('graph',
  'QUAD',
  'The above diagram shows the market in equilibrium for apples. If the demand for apples and the supply of '
  'apples both decrease, we know that the new equilibrium point must land somewhere in:',
  388,
  [('Quadrant A, meaning price definitely increases', False),
   ('Quadrant B, meaning quantity definitely increases', False),
   ('Quadrant C, meaning price definitely decreases', False),
   ('Quadrant D, meaning quantity definitely decreases', True),
   ('Quadrant D, meaning price definitely decreases', False)]),
 ('graph',
  'QUAD',
  'The above diagram shows the market in equilibrium for a good. After two changes in the market, the new '
  'equilibrium point lands in Quadrant A. Which of the following could have caused this?',
  494,
  [('Demand increased and supply decreased.', True),
   ('Demand and supply both increased.', False),
   ('Demand and supply both decreased.', False),
   ('Supply increased and demand decreased.', False),
   ('Only supply increased.', False)]),
 ('graph',
  'TWO',
  TWO_STEM + 'Compared with E₁, at the new equilibrium E₂,',
  388,
  [('price is lower and quantity is higher', True),
   ('price and quantity are both higher', False),
   ('price is higher and quantity is lower', False),
   ('price and quantity are both lower', False),
   ('price is lower and quantity is unchanged', False)]),
 ('graph',
  'TWO',
  TWO_STEM + 'Equilibrium price fell even though demand increased because',
  223,
  [('the increase in supply was larger than the increase in demand', True),
   ('the increase in demand was larger than the increase in supply', False),
   ('an increase in demand always lowers equilibrium price', False),
   ('supply shifted to the left', False),
   ('the increase in demand created a surplus', False)]),
 ('backward',
  None,
  'Last year, 500 used cars were sold for $8,000 each. This year, 500 used cars were sold for $9,500 each. '
  'Which of the following changes in demand and supply could have caused this outcome?',
  315,
  [(DS('Decrease', 'Decrease'), False),
   (DS('Decrease', 'Increase'), False),
   (DS('Increase', 'Decrease'), True),
   (DS('Increase', 'No Change'), False),
   (DS('No Change', 'Increase'), False)]),
 ('backward',
  None,
  'Last month, 2,000 sandwiches were sold for $6 each. This month, 1,600 sandwiches were sold for $6 each. '
  'Which of the following changes in demand and supply could have caused this outcome?',
  280,
  [(DS('Increase', 'Increase'), False),
   (DS('Decrease', 'Decrease'), True),
   (DS('Increase', 'Decrease'), False),
   (DS('Decrease', 'Increase'), False),
   (DS('No Change', 'Increase'), False)]),
 ('backward',
  None,
  'This year, the price of avocados rose and the quantity of avocados sold fell. Which of the following could '
  'explain this?<br><br>I. Supply decreased and demand did not change<br>II. Supply decreased and demand '
  'increased<br>III. Demand decreased and supply did not change',
  315,
  [('I only', False),
   ('II only', False),
   ('I and II only', True),
   ('II and III only', False),
   ('I, II and III', False)]),
 ('backward',
  None,
  'Last month, 800 boxes were sold for $12 each. This month, 600 boxes were sold for $10 each. Which of the '
  'following changes to supply and demand could have resulted in this change to the market?',
  183,
  [('Only a decrease in demand', True),
   ('Only an increase in supply', False),
   ('Only a decrease in supply', False),
   ('An increase in demand and a decrease in supply', False),
   ('An increase in demand and an increase in supply', False)])]


def upgrade():
    conn = op.get_bind()
    one = lambda sql, **kw: conn.execute(sa.text(sql), kw).scalar()
    run = lambda sql, **kw: conn.execute(sa.text(sql), kw)

    chapter_id = one("SELECT id FROM chapter WHERE name = :n", n=CHAPTER)
    if chapter_id is None:
        return

    def topic(name):
        found = one("SELECT id FROM question_topic WHERE chapter_id = :c AND name = :n", c=chapter_id, n=name)
        if found is None:
            found = one("INSERT INTO question_topic (name, chapter_id) VALUES (:n, :c) RETURNING id", n=name, c=chapter_id)
        return found

    def ids(sql, **kw):
        return [r[0] for r in conn.execute(sa.text(sql), kw).all()]

    def move(qids, from_topic, to_topic):
        if not qids:
            return
        rows = conn.execute(sa.text(
            "SELECT user_id, count(*), sum(CASE WHEN is_correct THEN 1 ELSE 0 END) FROM user_performance "
            "WHERE question_id = ANY(:q) GROUP BY user_id"), {'q': list(qids)}).all()
        for user_id, asked, correct in rows:
            run("UPDATE user_topic_progress SET questions_asked = GREATEST(questions_asked - :a, 0), "
                "answered_correctly = GREATEST(LEAST(answered_correctly - :r, questions_asked - :a), 0) "
                "WHERE user_id = :u AND topic_id = :t", a=asked, r=correct, u=user_id, t=from_topic)
            updated = run("UPDATE user_topic_progress SET questions_asked = questions_asked + :a, "
                          "answered_correctly = answered_correctly + :r WHERE user_id = :u AND topic_id = :t",
                          a=asked, r=correct, u=user_id, t=to_topic).rowcount
            if not updated:
                run("INSERT INTO user_topic_progress (user_id, topic_id, questions_asked, answered_correctly) "
                    "VALUES (:u, :t, :a, :r)", u=user_id, t=to_topic, a=asked, r=correct)
        run("DELETE FROM user_topic_progress WHERE topic_id = :t AND questions_asked = 0", t=from_topic)
        run("UPDATE question SET topic_id = :t WHERE id = ANY(:q)", t=to_topic, q=list(qids))

    # Topics
    run("UPDATE question_topic SET name = :new WHERE chapter_id = :c AND name = :old",
        new=PREDICT[1], old=PREDICT[0], c=chapter_id)
    topics = {'predict': topic(PREDICT[1]), 'graph': topic(GRAPH), 'backward': topic(BACKWARD)}

    # The two quadrant questions and the four "last year / last month" questions move out of Predicting
    move(ids("SELECT id FROM question WHERE topic_id = :t AND image_url = :u", t=topics['predict'], u=QUAD_URL),
         topics['predict'], topics['graph'])
    move(ids("SELECT id FROM question WHERE topic_id = :t AND text LIKE :s", t=topics['predict'], s=BACKWARD_PATTERN),
         topics['predict'], topics['backward'])

    # The quadrant picture becomes a drawn figure
    run("UPDATE question SET figure = CAST(:f AS JSON) WHERE image_url = :u AND figure IS NULL",
        f=json.dumps(FIGURES['QUAD']), u=QUAD_URL)

    # New questions (skipped if already there)
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
