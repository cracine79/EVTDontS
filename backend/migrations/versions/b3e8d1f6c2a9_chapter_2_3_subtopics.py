"""Chapter 2.3: three subtopics, thirteen new questions, one answer fix, four pictures redrawn

Reviewed and approved in the "Chapter 2.3 Question Review" doc (2026-11-23):
  * Topics: Surpluses and Shortages (was Supply and Demand in Equilibrium; keeps ten questions) /
    Equilibrium Price and Quantity (new; takes the two "equilibrium price" questions) /
    How Markets Return to Equilibrium (new; takes the "below equilibrium price" question).
  * Fix: "What is the expected outcome at a market price of $3?" (SDSchedule2) was marked "A surplus of
    30 units"; at $3, 30 are supplied and 60 demanded, so "A shortage of 30 units" is correct. Its
    rewatch time moves to the price-below-equilibrium section.
  * The four pictures become drawn figures (supply blue, demand red, as in the other chapters).
  * Five new equilibrium, two new surplus/shortage and six new return-to-equilibrium questions, with
    one new labeled graph (P1-P3, Q1-Q3).

Matched by chapter name, topic name, question/answer text and picture address (ids differ between
local and live databases); each step is a no-op once applied. Students' per-topic running totals move
with the questions, as in b4c8e1f6a2d9 (chapter 1.1).

Revision ID: b3e8d1f6c2a9
Revises: a7c4e2d9f3b6
Create Date: 2026-11-23
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'b3e8d1f6c2a9'
down_revision = 'a7c4e2d9f3b6'
branch_labels = None
depends_on = None

CHAPTER = '2.3 Supply and Demand in Equilibrium'
SURPLUS = ('Supply and Demand in Equilibrium', 'Surpluses and Shortages')
EQUILIBRIUM = 'Equilibrium Price and Quantity'
RETURN = 'How Markets Return to Equilibrium'

# LIKE patterns for the existing questions that leave the old topic
MOVED = {'equilibrium': ['%At which price will neither a shortage nor a surplus occur in the market?%',
                         '%The equilibrium price in the market is%'],
         'return': ['If the price in a perfectly competitive market is currently below equilibrium price%']}

FIX = ('%What is the expected outcome at a market price of $3?%', 'A shortage of 30 units', 289)

BASE = 'https://evtds-seeds.s3.us-east-2.amazonaws.com/'
PICTURES = {BASE + k: v for k, v in {'SDSchedule.png': 'SCHED1', 'SDSchedule2.png': 'SCHED2',
                                     'SD1.png': 'SD1', 'SD2.png': 'SD2'}.items()}

FIGURES = {'SCHED1': {'type': 'table',
            'caption': 'Market Supply & Demand Schedule',
            'columns': ['Price', 'Quantity Supplied', 'Quantity Demanded'],
            'rows': [['$50', 300, 800],
                     ['$75', 450, 700],
                     ['$100', 600, 600],
                     ['$125', 750, 500],
                     ['$150', 900, 400]]},
 'SCHED2': {'type': 'table',
            'caption': 'Market Supply & Demand Schedule',
            'columns': ['Price', 'Quantity Supplied', 'Quantity Demanded'],
            'rows': [['$1', 10, 120],
                     ['$2', 20, 90],
                     ['$3', 30, 60],
                     ['$4', 40, 40],
                     ['$5', 50, 10]]},
 'SD1': {'type': 'graph',
         'alt': 'Supply and demand curves. Supply is a straight line from the origin through a price of $5 at '
                'quantity 500. Demand is a straight line through a price of $5 at quantity 100 and a price of '
                '$1 at quantity 500. They cross at a price of $3 and quantity 300. Dashed lines mark the '
                'quantities at each whole-dollar price.',
         'x': {'label': 'Quantity', 'max': 600},
         'y': {'label': 'Price', 'max': 6},
         'xTicks': [[100, '100'], [200, '200'], [300, '300'], [400, '400'], [500, '500']],
         'yTicks': [[1, '$1'], [2, '$2'], [3, '$3'], [4, '$4'], [5, '$5']],
         'origin': '0',
         'curves': [{'points': [[0, 0], [550, 5.5]], 'label': 'Supply', 'labelAt': [556, 5.3], 'color': 'supply'},
                    {'points': [[50, 5.5], [550, 0.5]], 'label': 'Demand', 'labelAt': [556, 0.4], 'color': 'demand'}],
         'guides': [[[0, 1], [500, 1]], [[0, 2], [400, 2]], [[0, 3], [300, 3]], [[0, 4], [400, 4]],
                    [[0, 5], [500, 5]], [[100, 0], [100, 5]], [[200, 0], [200, 4]], [[300, 0], [300, 3]],
                    [[400, 0], [400, 4]], [[500, 0], [500, 5]]]},
 'SD2': {'type': 'graph',
         'alt': 'Supply and demand curves. Supply is a straight line from a price of $5 at quantity 0 through a '
                'price of $10 at quantity 200 and $15 at quantity 400. Demand is a straight line through a price '
                'of $25 at quantity 100, $20 at 200, $15 at 300, $10 at 400 and $5 at 500. They cross between '
                '$10 and $15, at a quantity between 300 and 400.',
         'x': {'label': 'Quantity', 'max': 600},
         'y': {'label': 'Price', 'max': 30},
         'xTicks': [[100, '100'], [200, '200'], [300, '300'], [400, '400'], [500, '500']],
         'yTicks': [[5, '$5'], [10, '$10'], [15, '$15'], [20, '$20'], [25, '$25']],
         'origin': '0',
         'curves': [{'points': [[0, 5], [550, 18.75]], 'label': 'Supply', 'labelAt': [556, 18.5], 'color': 'supply'},
                    {'points': [[50, 27.5], [550, 2.5]], 'label': 'Demand', 'labelAt': [556, 2.2], 'color': 'demand'}],
         'guides': [[[0, 25], [100, 25]], [[0, 20], [200, 20]], [[0, 15], [400, 15]], [[0, 10], [400, 10]],
                    [[0, 5], [500, 5]], [[100, 0], [100, 25]], [[200, 0], [200, 20]], [[300, 0], [300, 15]],
                    [[400, 0], [400, 15]], [[500, 0], [500, 5]]]},
 'LABELS': {'type': 'graph',
            'alt': 'Supply and demand curves that cross at price P2 and quantity Q2. At the higher price P3, '
                   'quantity demanded is Q1 and quantity supplied is Q3. At the lower price P1, quantity '
                   'supplied is Q1 and quantity demanded is Q3.',
            'x': {'label': 'Quantity', 'max': 10},
            'y': {'label': 'Price', 'max': 10},
            'xTicks': [[3, 'Q₁'], [5, 'Q₂'], [7, 'Q₃']],
            'yTicks': [[3, 'P₁'], [5, 'P₂'], [7, 'P₃']],
            'origin': '0',
            'curves': [{'points': [[0.5, 0.5], [9.5, 9.5]], 'label': 'S', 'color': 'supply'},
                       {'points': [[0.5, 9.5], [9.5, 0.5]], 'label': 'D', 'color': 'demand'}],
            'guides': [[[0, 7], [7, 7]], [[0, 5], [5, 5]], [[0, 3], [7, 3]],
                       [[3, 0], [3, 7]], [[5, 0], [5, 5]], [[7, 0], [7, 7]]]}}

GRAPH = 'The graph above shows the supply and demand curves for a perfectly competitive market. '

# (topic, figure, text, video_start seconds, [(answer, is_correct), ...]) in A-E order
NEW_QUESTIONS = [('equilibrium',
  'LABELS',
  GRAPH + 'The equilibrium price and quantity are',
  107,
  [('P₂ and Q₂', True),
   ('P₃ and Q₃', False),
   ('P₁ and Q₃', False),
   ('P₃ and Q₁', False),
   ('P₁ and Q₁', False)]),
 ('equilibrium',
  None,
  'A market is in equilibrium when',
  107,
  [('quantity supplied equals quantity demanded at the market price', True),
   ('the price is halfway between the highest and lowest prices in the market', False),
   ('there is a shortage at the market price', False),
   ('the price is as low as producers are willing to go', False),
   ('demand is greater than supply', False)]),
 ('equilibrium',
  'SCHED1',
  'The above table shows the supply and demand schedule for a perfectly competitive market. What are the '
  'equilibrium price and quantity?',
  107,
  [('$100 and 600 units', True),
   ('$75 and 700 units', False),
   ('$125 and 750 units', False),
   ('$100 and 1,200 units', False),
   ('$150 and 900 units', False)]),
 ('equilibrium',
  'SD1',
  'The above graph shows the supply and demand curves for a perfectly competitive market. The equilibrium '
  'quantity is',
  107,
  [('300 units', True),
   ('200 units', False),
   ('400 units', False),
   ('600 units', False),
   ('500 units', False)]),
 ('equilibrium',
  None,
  'In a market for pizza, at a price of $6, 10 pizzas are supplied and 80 are demanded; at $10, 50 are '
  'supplied and 50 are demanded; at $14, 100 are supplied and 30 are demanded. Which of the following is true?',
  107,
  [('The equilibrium price is $10 and the equilibrium quantity is 50.', True),
   ('The equilibrium price is $14, because producers supply the most pizza.', False),
   ('The equilibrium price is $6, because consumers buy the most pizza.', False),
   ('The equilibrium quantity is 100, the sum of quantity supplied and quantity demanded at $10.', False),
   ('The market is in equilibrium at all three prices.', False)]),
 ('surplus',
  'LABELS',
  GRAPH + 'If the price is P₃, there will be',
  192,
  [('a surplus equal to Q₃ − Q₁', True),
   ('a shortage equal to Q₃ − Q₁', False),
   ('a surplus equal to Q₂ − Q₁', False),
   ('a shortage equal to Q₃ − Q₂', False),
   ('neither a surplus nor a shortage', False)]),
 ('surplus',
  'LABELS',
  GRAPH + 'If the price is P₁, there will be',
  289,
  [('a shortage equal to Q₃ − Q₁', True),
   ('a surplus equal to Q₃ − Q₁', False),
   ('a shortage equal to Q₂ − Q₁', False),
   ('a surplus equal to Q₃ − Q₂', False),
   ('neither a surplus nor a shortage', False)]),
 ('return',
  None,
  'If the price of a good is above its equilibrium price, which of the following will occur?<br><br>I. There '
  'is a surplus<br>II. The price falls<br>III. Quantity supplied decreases as the price falls',
  352,
  [('I only', False),
   ('I and II only', False),
   ('I and III only', False),
   ('II and III only', False),
   ('I, II and III', True)]),
 ('return',
  None,
  'At a price of $14, pizza restaurants supply 100 pizzas a day, but consumers buy only 30. Which of the '
  'following is most likely to happen?',
  192,
  [('The price falls, quantity demanded increases and quantity supplied decreases until they are equal.', True),
   ('The price rises, quantity demanded decreases and quantity supplied increases until they are equal.', False),
   ('The supply curve shifts to the left until the surplus is gone.', False),
   ('The demand curve shifts to the right until the surplus is gone.', False),
   ('Nothing, because restaurants set the price of pizza.', False)]),
 ('return',
  'LABELS',
  GRAPH + 'If the price is currently P₁, which of the following will occur as the market moves to equilibrium?',
  289,
  [('The price rises, quantity supplied increases from Q₁ to Q₂, and quantity demanded decreases from Q₃ to Q₂.', True),
   ('The price falls, quantity supplied decreases from Q₂ to Q₁, and quantity demanded increases from Q₂ to Q₃.', False),
   ('The price rises and the demand curve shifts to the left.', False),
   ('The price rises and quantity supplied increases from Q₁ to Q₃.', False),
   ('The price stays at P₁, because buyers want more than sellers offer.', False)]),
 ('return',
  None,
  'A shortage in a market',
  289,
  [('puts upward pressure on price', True),
   ('puts downward pressure on price', False),
   ('is eliminated by a decrease in price', False),
   ('occurs when the price is above equilibrium', False),
   ('has no effect on price', False)]),
 ('return',
  None,
  'As the price of a good falls to eliminate a surplus, which of the following occurs?',
  192,
  [('Quantity demanded increases and quantity supplied decreases.', True),
   ('Demand increases and supply decreases.', False),
   ('Quantity demanded decreases and quantity supplied increases.', False),
   ('The demand curve shifts to the right.', False),
   ('Both quantity demanded and quantity supplied increase.', False)]),
 ('return',
  'SD2',
  'The above graph shows the supply and demand curves for a perfectly competitive market. If the current '
  'market price is $10, which of the following will happen as the market moves to equilibrium?',
  289,
  [('The price will rise and quantity supplied will increase.', True),
   ('The price will fall and quantity supplied will decrease.', False),
   ('The price will rise and quantity demanded will increase.', False),
   ('The price will fall and quantity demanded will increase.', False),
   ('The price will stay at $10, because the market is in equilibrium.', False)])]


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

    def find(pattern, topic_id):
        return [r[0] for r in conn.execute(sa.text(
            "SELECT id FROM question WHERE topic_id = :t AND text LIKE :s"), {'t': topic_id, 's': pattern}).all()]

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
        new=SURPLUS[1], old=SURPLUS[0], c=chapter_id)
    topics = {'surplus': topic(SURPLUS[1]), 'equilibrium': topic(EQUILIBRIUM), 'return': topic(RETURN)}

    # Three existing questions move out of Surpluses and Shortages
    for which, patterns in MOVED.items():
        for pattern in patterns:
            move(find(pattern, topics['surplus']), topics['surplus'], topics[which])

    # Pictures become drawn figures
    for url, key in PICTURES.items():
        run("UPDATE question SET figure = CAST(:f AS JSON) WHERE image_url = :u AND figure IS NULL",
            f=json.dumps(FIGURES[key]), u=url)

    # Fix: at $3 there is a shortage of 30, not a surplus
    pattern, right, start = FIX
    for qid in [r[0] for r in conn.execute(sa.text(
            "SELECT id FROM question WHERE chapter_id = :c AND text LIKE :s"), {'c': chapter_id, 's': pattern}).all()]:
        if one("SELECT count(*) FROM answer WHERE question_id = :q AND text = :t", q=qid, t=right):
            run("UPDATE answer SET is_correct = (text = :t) WHERE question_id = :q", t=right, q=qid)
            run("UPDATE question SET video_start = :v WHERE id = :q", v=start, q=qid)

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
