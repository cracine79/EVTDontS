"""Chapter 2.4: twelve new questions, one answer fix, two new drawn figures

Reviewed and approved in the "Chapter 2.4 Question Review" doc (2026-11-23):
  * Topics stay: Disequilibrium - Shifts to Demand / Disequilibrium - Shifts to Supply.
  * Fix: the energy drinks NOT question had a second correct choice ("A decrease in consumer incomes,
    assuming energy drinks are normal goods"); it becomes "An increase in consumer incomes...".
  * Seven new demand-shift questions and five new supply-shift questions, with two new labeled
    graphs (a demand shift and a supply shift).

Matched by chapter name, topic name and question/answer text (ids differ between local and live
databases); each step is a no-op once applied.

Revision ID: c6f2a9e4d8b1
Revises: b3e8d1f6c2a9
Create Date: 2026-11-23
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'c6f2a9e4d8b1'
down_revision = 'b3e8d1f6c2a9'
branch_labels = None
depends_on = None

CHAPTER = '2.4 Shifts to Supply and Demand'
DEMAND = 'Disequilibrium - Shifts to Demand'
SUPPLY = 'Disequilibrium - Shifts to Supply'

ENERGY_FIX = ('Which of the following would NOT be expected to cause both the equilibrium price and quantity of energy drinks to rise?',
              'A decrease in consumer incomes, assuming energy drinks are normal goods',
              'An increase in consumer incomes, assuming energy drinks are normal goods')

FIGURES = {'DSHIFT': {'type': 'graph',
            'alt': 'A supply curve S and two demand curves. The market starts at point A, where S crosses D1 at '
                   'price P1 and quantity Q1. Demand shifts right to D2, which crosses S at point B, at the '
                   'higher price P2 and quantity Q2. Point C is on D2 at the original price P1 and quantity Q3.',
            'x': {'label': 'Quantity', 'max': 10},
            'y': {'label': 'Price', 'max': 10},
            'xTicks': [[4, 'Q₁'], [6, 'Q₂'], [8, 'Q₃']],
            'yTicks': [[4, 'P₁'], [6, 'P₂']],
            'origin': '0',
            'curves': [{'points': [[0.5, 0.5], [9.5, 9.5]], 'label': 'S', 'color': 'supply'},
                       {'points': [[0.5, 7.5], [7.5, 0.5]], 'label': 'D₁', 'color': 'demand'},
                       {'points': [[2.5, 9.5], [9.5, 2.5]], 'label': 'D₂', 'color': 'demand'}],
            'guides': [[[0, 4], [8, 4]], [[0, 6], [6, 6]], [[4, 0], [4, 4]], [[6, 0], [6, 6]], [[8, 0], [8, 4]]],
            'points': [{'at': [4, 4], 'label': 'A', 'pos': 'n', 'dot': True},
                       {'at': [6, 6], 'label': 'B', 'pos': 'n', 'dot': True},
                       {'at': [8, 4], 'label': 'C', 'pos': 'ne', 'dot': True}]},
 'SSHIFT': {'type': 'graph',
            'alt': 'A demand curve D and two supply curves. The market starts at point A, where D crosses S1 at '
                   'price P1 and quantity Q1. Supply shifts right to S2, which crosses D at point B, at the lower '
                   'price P2 and quantity Q2. Point C is on S2 at the original price P1 and quantity Q3.',
            'x': {'label': 'Quantity', 'max': 12},
            'y': {'label': 'Price', 'max': 12},
            'xTicks': [[6, 'Q₁'], [8, 'Q₂'], [10, 'Q₃']],
            'yTicks': [[6, 'P₁'], [4, 'P₂']],
            'origin': '0',
            'curves': [{'points': [[1, 11], [11, 1]], 'label': 'D', 'color': 'demand'},
                       {'points': [[1, 1], [11, 11]], 'label': 'S₁', 'color': 'supply'},
                       {'points': [[4.5, 0.5], [11.5, 7.5]], 'label': 'S₂', 'color': 'supply'}],
            'guides': [[[0, 6], [10, 6]], [[0, 4], [8, 4]], [[6, 0], [6, 6]], [[8, 0], [8, 4]], [[10, 0], [10, 6]]],
            'points': [{'at': [6, 6], 'label': 'A', 'pos': 'n', 'dot': True},
                       {'at': [8, 4], 'label': 'B', 'pos': 'e', 'dot': True},
                       {'at': [10, 6], 'label': 'C', 'pos': 'nw', 'dot': True}]}}

D_GRAPH = ('The graph above shows the market for a good, initially in equilibrium at point A. '
           'Demand then shifts from D₁ to D₂. ')
S_GRAPH = ('The graph above shows the market for a good, initially in equilibrium at point A. '
           'Supply then shifts from S₁ to S₂. ')
EQ = 'Equilibrium price and equilibrium quantity both '

# (topic, figure, text, video_start seconds, [(answer, is_correct), ...]) in A-E order
NEW_QUESTIONS = [('demand',
  'DSHIFT',
  D_GRAPH + 'At the original price P₁, there is',
  129,
  [('a shortage equal to Q₃ − Q₁', True),
   ('a surplus equal to Q₃ − Q₁', False),
   ('a shortage equal to Q₂ − Q₁', False),
   ('a surplus equal to Q₂ − Q₁', False),
   ('neither a shortage nor a surplus', False)]),
 ('demand',
  'DSHIFT',
  D_GRAPH + 'When the market reaches its new equilibrium,',
  129,
  [('price rises from P₁ to P₂ and quantity rises from Q₁ to Q₂', True),
   ('price rises from P₁ to P₂ and quantity rises from Q₁ to Q₃', False),
   ('price stays at P₁ and quantity rises from Q₁ to Q₃', False),
   ('price falls and quantity rises from Q₁ to Q₂', False),
   ('price rises from P₁ to P₂ and quantity falls', False)]),
 ('demand',
  'DSHIFT',
  'The graph above shows the market for a good, initially in equilibrium at point A. Which of the following '
  'could cause demand to shift from D₁ to D₂?<br><br>I. Consumer incomes rise, and the good is a normal '
  'good<br>II. The price of a substitute good rises<br>III. The cost of producing the good falls',
  129,
  [('I only', False),
   ('II only', False),
   ('I and II only', True),
   ('I and III only', False),
   ('I, II and III', False)]),
 ('demand',
  None,
  'A decrease in consumer incomes is most likely to have which of the following effects on the market for '
  'instant noodles, an inferior good?',
  438,
  [(EQ + 'rise.', True),
   (EQ + 'fall.', False),
   ('Equilibrium price rises and equilibrium quantity falls.', False),
   ('Equilibrium price falls and equilibrium quantity rises.', False),
   ('Equilibrium price rises and equilibrium quantity does not change.', False)]),
 ('demand',
  None,
  'When the demand for a good decreases, which of the following happens before the market reaches its new '
  'equilibrium?',
  235,
  [('A surplus develops at the original price, putting downward pressure on price.', True),
   ('A shortage develops at the original price, putting upward pressure on price.', False),
   ('The supply curve shifts to the left.', False),
   ('The price falls straight to the new equilibrium without any surplus.', False),
   ('Quantity supplied increases at the original price.', False)]),
 ('demand',
  None,
  'A widely shared report finds that a popular brand of sneakers causes blisters. Which of the following is '
  'the most likely effect on the market for those sneakers?',
  235,
  [(EQ + 'fall.', True),
   (EQ + 'rise.', False),
   ('Equilibrium price falls and equilibrium quantity rises.', False),
   ('Equilibrium price rises and equilibrium quantity falls.', False),
   ('Equilibrium price falls and equilibrium quantity does not change.', False)]),
 ('demand',
  None,
  'Pizza is a normal good, and burgers are a substitute for pizza. Which of the following would decrease both '
  'the equilibrium price and the equilibrium quantity of pizza?<br><br>I. The price of burgers falls<br>II. '
  'Consumer incomes fall<br>III. The cost of cheese used to make pizza rises',
  235,
  [('I only', False),
   ('II only', False),
   ('I and II only', True),
   ('II and III only', False),
   ('I, II and III', False)]),
 ('supply',
  'SSHIFT',
  S_GRAPH + 'At the original price P₁, there is',
  296,
  [('a surplus equal to Q₃ − Q₁', True),
   ('a shortage equal to Q₃ − Q₁', False),
   ('a surplus equal to Q₂ − Q₁', False),
   ('a shortage equal to Q₂ − Q₁', False),
   ('neither a surplus nor a shortage', False)]),
 ('supply',
  'SSHIFT',
  S_GRAPH + 'When the market reaches its new equilibrium,',
  296,
  [('price falls from P₁ to P₂ and quantity rises from Q₁ to Q₂', True),
   ('price falls from P₁ to P₂ and quantity rises from Q₁ to Q₃', False),
   ('price stays at P₁ and quantity rises from Q₁ to Q₃', False),
   ('price rises and quantity rises from Q₁ to Q₂', False),
   ('price falls from P₁ to P₂ and quantity falls', False)]),
 ('supply',
  'SSHIFT',
  'The graph above shows the market for a good, initially in equilibrium at point A. Which of the following '
  'could cause supply to shift from S₁ to S₂?',
  296,
  [('The government lowers the minimum wage paid to workers who make the good.', True),
   ('The price of the good rises.', False),
   ('Consumer incomes rise, and the good is a normal good.', False),
   ('The government places a new tax on each unit of the good sold.', False),
   ('Several firms leave the market.', False)]),
 ('supply',
  None,
  'Pizza is a normal good. Which of the following would increase the equilibrium price and decrease the '
  'equilibrium quantity of pizza?<br><br>I. Several pizza restaurants close and leave the market<br>II. The '
  'cost of cheese used to make pizza rises<br>III. Consumer incomes rise',
  385,
  [('I only', False),
   ('II only', False),
   ('I and II only', True),
   ('II and III only', False),
   ('I, II and III', False)]),
 ('supply',
  None,
  'When the supply of a good decreases, which of the following happens before the market reaches its new '
  'equilibrium?',
  385,
  [('A shortage develops at the original price, putting upward pressure on price.', True),
   ('A surplus develops at the original price, putting downward pressure on price.', False),
   ('The demand curve shifts to the left.', False),
   ('The price falls to attract more buyers.', False),
   ('Quantity demanded increases at the original price.', False)])]


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

    topics = {'demand': topic(DEMAND), 'supply': topic(SUPPLY)}

    # Fix: lower incomes also fail to raise price and quantity (a second correct choice)
    run("UPDATE answer SET text = :new WHERE text = :old AND question_id IN "
        "(SELECT id FROM question WHERE chapter_id = :c AND text LIKE :s)",
        new=ENERGY_FIX[2], old=ENERGY_FIX[1], c=chapter_id, s=ENERGY_FIX[0] + '%')

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
