"""Chapter 2.2a: two subtopics, fourteen new questions, one answer fix, one question moved

Reviewed and approved in the "Chapter 2.2a Question Review" doc (2026-11-23):
  * Topics: Change in Supply vs Change in Quantity Supplied (new; takes the "supply curve shifts to the
    right" question) / The Supply Shifters (was Shifts to supply).
  * Fix: the laptops question had a second correct choice ("A decrease in the cost of transportation for
    laptops"); it becomes "A decrease in the number of laptop manufacturers".
  * Seven new supply vs quantity supplied questions (one new drawn figure) and seven new shifter questions.

Matched by chapter name, topic name and question/answer text (ids differ between local and live
databases); each step is a no-op once applied. Students' per-topic running totals move with the
questions, as in b4c8e1f6a2d9 (chapter 1.1).

Revision ID: a7c4e2d9f3b6
Revises: f5b9d2a7e3c4
Create Date: 2026-11-23
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'a7c4e2d9f3b6'
down_revision = 'f5b9d2a7e3c4'
branch_labels = None
depends_on = None

CHAPTER = '2.2a Non-Price Determinants of Supply'
SHIFTERS = ('Shifts to supply', 'The Supply Shifters')
CHANGE = 'Change in Supply vs Change in Quantity Supplied'

MOVED_TO_CHANGE = ['When the supply curve shifts to the right (in a perfectly competitive market)']

LAPTOP_FIX = ('Which of the following would shift the supply curve for laptops to the right?',
              'A decrease in the cost of transportation for laptops',
              'A decrease in the number of laptop manufacturers')

FIGURES = {'SHIFT': {'type': 'graph',
           'alt': 'Two upward-sloping supply curves on a gridded graph. S1 runs from the origin to a price '
                  'of $11 at quantity 11. S2 lies to the right, from quantity 4 at $0 to a price of $10 at '
                  'quantity 14. Point A is on S1 at $4 and 4 units; point B is on S1 at $8 and 8 units; '
                  'point C is on S2 at $4 and 8 units.',
           'x': {'label': 'Quantity', 'max': 15},
           'y': {'label': 'Price', 'max': 13, 'prefix': '$'},
           'grid': {'x': 2, 'y': 2},
           'origin': '0',
           'curves': [{'points': [[0, 0], [11, 11]],
                       'label': 'S₁',
                       'labelAt': [11.5, 11.4],
                       'color': 'supply'},
                      {'points': [[4, 0], [14, 10]],
                       'label': 'S₂',
                       'labelAt': [14.4, 10.4],
                       'color': 'supply'}],
           'points': [{'at': [4, 4], 'label': 'A', 'pos': 'nw', 'dot': True},
                      {'at': [8, 8], 'label': 'B', 'pos': 'nw', 'dot': True},
                      {'at': [8, 4], 'label': 'C', 'pos': 'se', 'dot': True}]}}

# (topic, figure, text, video_start seconds, [(answer, is_correct), ...]) in A-E order
NEW_QUESTIONS = [('change',
  'SHIFT',
  'The graph above shows two supply curves for a good. The movement from point A to point C is best '
  'described as',
  224,
  [('an increase in supply', True),
   ('an increase in quantity supplied', False),
   ('a decrease in supply', False),
   ('a decrease in quantity supplied', False),
   ('a movement along the supply curve S₁', False)]),
 ('change',
  'SHIFT',
  'The graph above shows two supply curves for a good. The movement from point A to point B is best '
  'described as',
  24,
  [('an increase in quantity supplied', True),
   ('an increase in supply', False),
   ('a decrease in supply', False),
   ('a decrease in quantity supplied', False),
   ('a rightward shift of the supply curve', False)]),
 ('change',
  'SHIFT',
  'The graph above shows two supply curves for a good. The movement from point A to point B is caused by',
  24,
  [('an increase in the price of the good', True),
   ('a decrease in the price of the good', False),
   ('a decrease in the cost of the inputs used to make the good', False),
   ('an improvement in the technology used to make the good', False),
   ('an increase in the number of firms in the market', False)]),
 ('change',
  'SHIFT',
  'The graph above shows two supply curves for a good. Which of the following could cause the movement '
  'from point A to point C?<br><br>I. A decrease in the cost of the inputs used to make the good<br>II. An '
  'increase in the price of the good<br>III. An increase in government subsidies to producers of the good',
  184,
  [('I only', False),
   ('II only', False),
   ('I and III only', True),
   ('II and III only', False),
   ('I, II and III', False)]),
 ('change',
  'SHIFT',
  'The graph above shows two supply curves for a good. When supply shifts from S₁ to S₂, the quantity '
  'supplied at a price of $4',
  224,
  [('increases from 4 to 8 units', True),
   ('increases from 4 to 6 units', False),
   ('increases from 8 to 12 units', False),
   ('decreases from 8 to 4 units', False),
   ('does not change, because the price has not changed', False)]),
 ('change',
  None,
  'Which of the following would cause a movement along the supply curve for coffee rather than a shift of '
  'the curve?',
  153,
  [('A change in the price of coffee', True),
   ('A change in the wages of coffee farmworkers', False),
   ('A change in the technology used to harvest coffee', False),
   ('A change in the tax on each pound of coffee sold', False),
   ('A change in the number of coffee growers', False)]),
 ('change',
  'SHIFT',
  'The graph above shows two supply curves for a good. Which of the following would most likely cause '
  'supply to shift from S₂ to S₁?',
  255,
  [('An increase in the cost of the inputs used to make the good', True),
   ('A decrease in the price of the good', False),
   ('An increase in the price of the good', False),
   ('An improvement in the technology used to make the good', False),
   ('An increase in government subsidies to producers of the good', False)]),
 ('shifters',
  None,
  'Producers of a good expect its price to rise sharply next year. Which of the following is most likely to '
  'happen to the supply of the good today?',
  380,
  [('It will decrease.', True),
   ('It will increase.', False),
   ("It will not change, because today's price has not changed.", False),
   ('Quantity supplied will increase, but supply will not change.', False),
   ('The supply curve will shift to the right.', False)]),
 ('shifters',
  None,
  'A farm can use the same land and equipment to grow either corn or wheat. If the price of wheat rises, '
  'which of the following is most likely to happen in the market for corn?',
  419,
  [('The supply of corn decreases.', True),
   ('The supply of corn increases.', False),
   ('The quantity of corn supplied increases.', False),
   ('The demand for corn decreases.', False),
   ('Nothing, because corn and wheat are different goods.', False)]),
 ('shifters',
  None,
  'Beef and leather both come from cattle. If the price of beef increases, which of the following is most '
  'likely to happen in the market for leather?',
  485,
  [('The supply of leather increases.', True),
   ('The supply of leather decreases.', False),
   ('The quantity of leather supplied decreases.', False),
   ('The demand for leather increases.', False),
   ('Nothing, because the price of leather has not changed.', False)]),
 ('shifters',
  None,
  'The government imposes a tax of 25 cents on each chocolate bar that producers sell. Which of the '
  'following is the most likely result in the market for chocolate?',
  304,
  [('Supply decreases, shifting the supply curve to the left.', True),
   ('Supply increases, shifting the supply curve to the right.', False),
   ('Quantity supplied increases, a movement along the supply curve.', False),
   ('Demand decreases, shifting the demand curve to the left.', False),
   ('Nothing, because the tax is paid to the government.', False)]),
 ('shifters',
  None,
  'Which of the following is most likely to increase the supply of pizza in a city?',
  538,
  [('Several new pizza restaurants open in the city.', True),
   ('The price of pizza increases.', False),
   ('The price of cheese used to make pizza increases.', False),
   ('The government imposes a tax on each pizza sold.', False),
   ('Pizza makers expect the price of pizza to rise next month.', False)]),
 ('shifters',
  None,
  'Which of the following would shift the supply curve for a good to the left?<br><br>I. An increase in the '
  'cost of the inputs used to make the good<br>II. A decrease in government subsidies to producers of the '
  'good<br>III. Producers expect the price of the good to rise in the future',
  255,
  [('I only', False),
   ('I and II only', False),
   ('I and III only', False),
   ('II and III only', False),
   ('I, II and III', True)]),
 ('shifters',
  None,
  'A factory can use the same workers and equipment to make either scooters or bicycles. Which of the '
  'following would most likely increase the supply of bicycles?',
  419,
  [('A decrease in the price of scooters', True),
   ('An increase in the price of scooters', False),
   ('An increase in the price of bicycles', False),
   ("An increase in the wages of the factory's workers", False),
   ('An increase in consumer incomes', False)])]


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

    def find(start, topic_id):
        return [r[0] for r in conn.execute(sa.text(
            "SELECT id FROM question WHERE topic_id = :t AND text LIKE :s"), {'t': topic_id, 's': start + '%'}).all()]

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
        new=SHIFTERS[1], old=SHIFTERS[0], c=chapter_id)
    topics = {'shifters': topic(SHIFTERS[1]), 'change': topic(CHANGE)}

    # "Shifts to the right" asks what a shift means, so it moves to Change in Supply vs Quantity Supplied
    for start in MOVED_TO_CHANGE:
        move(find(start, topics['shifters']), topics['shifters'], topics['change'])

    # Fix: lower transportation costs also shift laptop supply right (a second correct choice)
    run("UPDATE answer SET text = :new WHERE text = :old AND question_id IN "
        "(SELECT id FROM question WHERE chapter_id = :c AND text LIKE :s)",
        new=LAPTOP_FIX[2], old=LAPTOP_FIX[1], c=chapter_id, s=LAPTOP_FIX[0] + '%')

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
