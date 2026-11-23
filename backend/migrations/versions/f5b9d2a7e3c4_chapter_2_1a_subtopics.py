"""Chapter 2.1a: two subtopics, twelve new questions, two wording fixes, one question in from 2.4

Reviewed and approved in the "Chapter 2.1a Question Review" doc (2026-11-23):
  * Topics: Change in Demand vs Change in Quantity Demanded (new; takes the two good Z price-change
    questions) / The Demand Shifters (was Shifts to Demand).
  * The apples question ("...decrease in demand for apples?") moves from 2.4 to The Demand Shifters,
    the only 2.4 question that asks just which way a curve shifts. Its rewatch time moves to this
    video's consumer preference section.
  * Fixes: "...a decrease in the quantity demanded of good Y" becomes "...the demand for good Y"; the
    population question asks for an effect, since every choice is about housing.
  * Eight new demand vs quantity demanded questions (one new drawn figure) and four new shifter questions.

Matched by chapter name, topic name and question text (ids differ between local and live databases);
each step is a no-op once applied. Students' per-topic running totals move with the questions, as in
b4c8e1f6a2d9 (chapter 1.1).

Revision ID: f5b9d2a7e3c4
Revises: e8a3c6f1b5d2
Create Date: 2026-11-23
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'f5b9d2a7e3c4'
down_revision = 'e8a3c6f1b5d2'
branch_labels = None
depends_on = None

CHAPTER = '2.1a Non-Price Determinants of Demand'
SHIFTERS = ('Shifts to Demand', 'The Demand Shifters')
CHANGE = 'Change in Demand vs Change in Quantity Demanded'

MOVED_TO_CHANGE = ['Which of the following will most likely happen in the market for good Z if the price of good Z increases',
                   'Which of the following will most likely result from a decrease in the price of good Z']

FROM_CHAPTER = '2.4 Shifts to Supply and Demand'
FROM_TOPIC = 'Disequilibrium - Shifts to Demand'
APPLES = 'Which of the following would most likely result in the decrease in demand for apples'
APPLES_START = 483

# (question start, old words, new words)
TEXT_FIXES = [
    ('An increase in the price of good X results in a decrease in the', 'the quantity demanded of good Y', 'the demand for good Y'),
    ('An increase in the population of a city is most likely to affect',
     'most likely to affect the demand for which of the following goods?', 'most likely to have which of the following effects?'),
]

FIGURES = {'SHIFT': {'type': 'graph',
           'alt': 'Two downward-sloping demand curves for scooters on a gridded graph. D1 runs from a price '
                  'of $10 at quantity 0 to quantity 10 at $0. D2 lies to the right, from a price of $12 at '
                  'quantity 2 to quantity 14 at $0. Point A is on D1 at $6 and 4 scooters; point B is on D1 '
                  'at $4 and 6 scooters; point C is on D2 at $6 and 8 scooters.',
           'x': {'label': 'Quantity', 'max': 15},
           'y': {'label': 'Price', 'max': 13, 'prefix': '$'},
           'grid': {'x': 2, 'y': 2},
           'origin': '0',
           'curves': [{'points': [[0, 10], [10, 0]],
                       'label': 'D₁',
                       'labelAt': [10.3, 1.2],
                       'color': 'demand'},
                      {'points': [[2, 12], [14, 0]],
                       'label': 'D₂',
                       'labelAt': [14.3, 1.2],
                       'color': 'demand'}],
           'points': [{'at': [4, 6], 'label': 'A', 'pos': 'ne', 'dot': True},
                      {'at': [6, 4], 'label': 'B', 'pos': 'ne', 'dot': True},
                      {'at': [8, 6], 'label': 'C', 'pos': 'ne', 'dot': True}]}}

# (topic, figure, text, video_start seconds, [(answer, is_correct), ...]) in A-E order
NEW_QUESTIONS = [('change',
  'SHIFT',
  'The graph above shows two demand curves for scooters. The movement from point A to point C is best '
  'described as',
  247,
  [('an increase in demand', True),
   ('an increase in quantity demanded', False),
   ('a decrease in demand', False),
   ('a decrease in quantity demanded', False),
   ('a movement along the demand curve D₁', False)]),
 ('change',
  'SHIFT',
  'The graph above shows two demand curves for scooters. The movement from point A to point B is caused by',
  363,
  [('a decrease in the price of scooters', True),
   ('an increase in consumer incomes, if scooters are a normal good', False),
   ('an increase in the price of bicycles, a substitute for scooters', False),
   ('a celebrity being seen riding a scooter', False),
   ('consumers expecting the price of scooters to rise next month', False)]),
 ('change',
  'SHIFT',
  'The graph above shows two demand curves for scooters. Which of the following could cause the movement '
  'from point A to point C?<br><br>I. A popular celebrity is seen riding a scooter<br>II. The price of '
  'scooters falls<br>III. Consumers expect the price of scooters to rise next month',
  465,
  [('I only', False),
   ('II only', False),
   ('I and III only', True),
   ('II and III only', False),
   ('I, II and III', False)]),
 ('change',
  'SHIFT',
  'The graph above shows two demand curves for scooters. When demand shifts from D₁ to D₂, the quantity '
  'demanded at a price of $6',
  265,
  [('increases from 4 to 8 scooters', True),
   ('increases from 6 to 8 scooters', False),
   ('increases from 4 to 6 scooters', False),
   ('decreases from 8 to 4 scooters', False),
   ('does not change, because the price has not changed', False)]),
 ('change',
  None,
  'Which of the following would cause a movement along the demand curve for coffee rather than a shift of '
  'the curve?',
  363,
  [('A change in the price of coffee', True),
   ('A change in the price of tea', False),
   ('A change in consumer incomes', False),
   ("A change in consumers' tastes for coffee", False),
   ('A change in the number of coffee drinkers', False)]),
 ('change',
  None,
  'An increase in demand for a good means that',
  265,
  [('buyers are willing to buy a greater quantity at every price', True),
   ('the price of the good has fallen', False),
   ('buyers are buying more because the price has fallen', False),
   ('the demand curve has become steeper', False),
   ('quantity demanded has risen only at the current price', False)]),
 ('change',
  'SHIFT',
  'The graph above shows two demand curves for scooters. Which of the following would most likely cause '
  'demand to shift from D₂ to D₁?',
  310,
  [('A news report reveals a safety problem with scooters.', True),
   ('The price of scooters increases.', False),
   ('The price of scooters decreases.', False),
   ('Consumer incomes increase, and scooters are a normal good.', False),
   ('The price of bicycles, a substitute for scooters, increases.', False)]),
 ('change',
  None,
  'After a widely shared report that a brand of sneakers causes blisters, the price of the sneakers stays '
  'the same, but consumers want to buy fewer of them at that price. This is best described as',
  310,
  [('a decrease in demand', True),
   ('a decrease in quantity demanded', False),
   ('an increase in demand', False),
   ('a movement along the demand curve', False),
   ('an increase in quantity demanded', False)]),
 ('shifters',
  None,
  'Consumers learn that the price of a new gaming console will rise sharply next month. Which of the '
  'following is most likely to happen to the demand for the console today?',
  736,
  [('It will increase.', True),
   ('It will decrease.', False),
   ("It will not change, because today's price has not changed.", False),
   ('Quantity demanded will decrease, but demand will not change.', False),
   ('The demand curve will shift to the left.', False)]),
 ('shifters',
  None,
  'A large increase in the number of families with young children in a city would most likely increase the '
  'demand for which of the following?',
  791,
  [("Children's car seats", True),
   ('Retirement homes', False),
   ('Hearing aids', False),
   ('College dormitory rooms', False),
   ('Golf club memberships', False)]),
 ('shifters',
  None,
  'Which of the following would increase the demand for tennis rackets?<br><br>I. A decrease in the price of '
  'tennis balls, a complement for tennis rackets<br>II. An increase in consumer incomes, if tennis rackets '
  'are a normal good<br>III. A decrease in the price of tennis rackets',
  672,
  [('I only', False),
   ('II only', False),
   ('I and II only', True),
   ('II and III only', False),
   ('I, II and III', False)]),
 ('shifters',
  None,
  "When Maya's income falls, she buys more instant noodles and fewer restaurant meals. For Maya,",
  561,
  [('instant noodles are an inferior good and restaurant meals are a normal good', True),
   ('instant noodles are a normal good and restaurant meals are an inferior good', False),
   ('both are normal goods', False),
   ('both are inferior goods', False),
   ('instant noodles and restaurant meals are complements', False)])]


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
        run("UPDATE question SET topic_id = :t, chapter_id = :c WHERE id = ANY(:q)", t=to_topic, c=chapter_id, q=list(qids))

    # Topics
    run("UPDATE question_topic SET name = :new WHERE chapter_id = :c AND name = :old",
        new=SHIFTERS[1], old=SHIFTERS[0], c=chapter_id)
    topics = {'shifters': topic(SHIFTERS[1]), 'change': topic(CHANGE)}

    # The two price-change questions move to Change in Demand vs Change in Quantity Demanded
    for start in MOVED_TO_CHANGE:
        move(find(start, topics['shifters']), topics['shifters'], topics['change'])

    # The apples question moves in from 2.4 (only while it is still there)
    from_topic = one("SELECT t.id FROM question_topic t JOIN chapter c ON c.id = t.chapter_id "
                     "WHERE c.name = :c AND t.name = :t", c=FROM_CHAPTER, t=FROM_TOPIC)
    if from_topic is not None:
        apples = find(APPLES, from_topic)
        move(apples, from_topic, topics['shifters'])
        if apples:
            run("UPDATE question SET video_start = :v WHERE id = ANY(:q)", v=APPLES_START, q=apples)

    # Wording fixes
    for start, old, new in TEXT_FIXES:
        run("UPDATE question SET text = replace(text, :old, :new) WHERE chapter_id = :c AND text LIKE :s",
            old=old, new=new, c=chapter_id, s=start + '%')

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
