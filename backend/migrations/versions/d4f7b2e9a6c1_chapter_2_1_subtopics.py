"""Chapter 2.1: two subtopics, fifteen new questions, three pictures redrawn

Reviewed and approved in the "Chapter 2.1 Question Review" doc (2026-11-23):
  * Topics: Demand and the Law of Demand (was The demand curve; keeps the seven concept questions) /
    Reading Demand Curves and Market Demand (new; takes the pizza table, Wes and Wyatt, and Frank
    and Sam questions).
  * The three pictures become drawn figures (frontend2 QuestionFigure.jsx, which now draws gridlines).
  * Five new law of demand questions and ten new reading/market demand questions. No fixes needed.

Matched by chapter name, topic name, question text and picture address (ids differ between local and
live databases); each step is a no-op once applied. Students' per-topic running totals move with the
questions, as in b4c8e1f6a2d9 (chapter 1.1).

Revision ID: d4f7b2e9a6c1
Revises: c9e3a6d2f8b5
Create Date: 2026-11-23
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'd4f7b2e9a6c1'
down_revision = 'c9e3a6d2f8b5'
branch_labels = None
depends_on = None

CHAPTER = '2.1 Demand Introduced'
LAW = ('The demand curve', 'Demand and the Law of Demand')
READING = 'Reading Demand Curves and Market Demand'

BASE = 'https://evtds-seeds.s3.us-east-2.amazonaws.com/'
PICTURES = {BASE + k: v for k, v in {'Screenshot+2024-11-14+at+8.14.41+PM.png': 'PIZZA', 'WWDemands.png': 'WW',
                                     'HDDemands.png': 'HD'}.items()}

FIGURES = {'PIZZA': {'type': 'table',
           'caption': 'Pizzas demanded per month',
           'columns': ['Price per pizza', 'April', 'Bob', 'Charlie'],
           'rows': [['$5', 10, 8, 7],
                    ['$10', 9, 4, 5],
                    ['$15', 8, 2, 2],
                    ['$20', 7, 1, 1],
                    ['$25', 6, 0, 0]]},
 'WW': {'type': 'panels',
        'alt': 'Two individual demand curves for salted peanuts on gridded graphs. Wes: a straight line from '
               'a price of 16 at quantity 0 to quantity 8 at a price of 0. Wyatt: a straight line from a '
               'price of 12 at quantity 0 to quantity 6 at a price of 0.',
        'panels': [{'type': 'graph',
                    'caption': 'Wes',
                    'x': {'label': 'Quantity', 'max': 9},
                    'y': {'label': 'Price', 'max': 18},
                    'grid': {'x': 1, 'y': 2},
                    'origin': '0',
                    'curves': [{'points': [[0, 16], [8, 0]]}]},
                   {'type': 'graph',
                    'caption': 'Wyatt',
                    'x': {'label': 'Quantity', 'max': 9},
                    'y': {'label': 'Price', 'max': 18},
                    'grid': {'x': 1, 'y': 2},
                    'origin': '0',
                    'curves': [{'points': [[0, 12], [6, 0]]}]}]},
 'HD': {'type': 'panels',
        'alt': 'Two individual demand curves for hot dogs on gridded graphs. Frank: a straight line from $10 '
               'at quantity 0 to quantity 5 at $0. Sam: a straight line from $8 at quantity 0 to quantity 8 '
               'at $0.',
        'panels': [{'type': 'graph',
                    'caption': 'Frank',
                    'x': {'label': 'Quantity', 'max': 8},
                    'y': {'label': 'Price', 'max': 12, 'prefix': '$'},
                    'grid': {'x': 1, 'y': 2},
                    'origin': '0',
                    'curves': [{'points': [[0, 10], [5, 0]]}]},
                   {'type': 'graph',
                    'caption': 'Sam',
                    'x': {'label': 'Quantity', 'max': 8},
                    'y': {'label': 'Price', 'max': 12, 'prefix': '$'},
                    'grid': {'x': 1, 'y': 2},
                    'origin': '0',
                    'curves': [{'points': [[0, 8], [8, 0]]}]}]},
 'COFFEE': {'type': 'table',
            'caption': 'Cups of coffee demanded per week',
            'columns': ['Price per cup', 'Ann', 'Ben', 'Cal'],
            'rows': [['$1', 6, 5, 4], ['$2', 5, 3, 3], ['$3', 4, 2, 1], ['$4', 3, 1, 0], ['$5', 2, 0, 0]]},
 'DEMAND': {'type': 'graph',
            'alt': 'A downward-sloping demand curve on a gridded graph, from a price of $10 at quantity 0 to '
                   'quantity 10 at a price of $0. Point A is at a price of $8 and quantity 2; point B is at '
                   'a price of $4 and quantity 6.',
            'x': {'label': 'Quantity', 'max': 12},
            'y': {'label': 'Price', 'max': 12, 'prefix': '$'},
            'grid': {'x': 2, 'y': 2},
            'origin': '0',
            'curves': [{'points': [[0, 10], [10, 0]], 'color': 'demand'}],
            'points': [{'at': [2, 8], 'label': 'A', 'pos': 'ne', 'dot': True},
                       {'at': [6, 4], 'label': 'B', 'pos': 'ne', 'dot': True}]},
 'LO': {'type': 'panels',
        'alt': 'Two individual demand curves for movie tickets on gridded graphs. Lena: a straight line from '
               '$12 at quantity 0 to quantity 6 at $0. Omar: a straight line from $8 at quantity 0 to '
               'quantity 8 at $0.',
        'panels': [{'type': 'graph',
                    'caption': 'Lena',
                    'x': {'label': 'Quantity', 'max': 10},
                    'y': {'label': 'Price', 'max': 14, 'prefix': '$'},
                    'grid': {'x': 1, 'y': 2},
                    'origin': '0',
                    'curves': [{'points': [[0, 12], [6, 0]]}]},
                   {'type': 'graph',
                    'caption': 'Omar',
                    'x': {'label': 'Quantity', 'max': 10},
                    'y': {'label': 'Price', 'max': 14, 'prefix': '$'},
                    'grid': {'x': 1, 'y': 2},
                    'origin': '0',
                    'curves': [{'points': [[0, 8], [8, 0]]}]}]}}

# (topic, figure, text, video_start seconds, [(answer, is_correct), ...]) in A-E order
NEW_QUESTIONS = [('law',
  None,
  'Which of the following is an example of the law of demand?',
  382,
  [('When movie tickets fall from $15 to $10, Ana goes to the movies three times a month instead of once.',
    True),
   ("When Ana's income rises, she goes to the movies more often.", False),
   ('When the price of popcorn rises, Ana goes to the movies less often.', False),
   ('Movie ticket prices rise because more people want to see a new film.', False),
   ('When movie tickets rise from $10 to $15, Ana goes to the movies more often.', False)]),
 ('law',
  None,
  'The price of gasoline falls sharply, and Maria finds that her paycheck now stretches further, so she '
  "drives more. The increase in Maria's driving that comes from her paycheck stretching further is an "
  'example of',
  430,
  [('the income effect', True),
   ('the substitution effect', False),
   ('the law of supply', False),
   ('an increase in demand for gasoline', False),
   ('a change in consumer preferences', False)]),
 ('law',
  None,
  'When the price of beef rises, Tom buys less beef and more chicken because chicken is now relatively '
  "cheaper. The decrease in Tom's beef purchases caused by chicken becoming relatively cheaper is an example "
  'of',
  476,
  [('the income effect', False),
   ('the substitution effect', True),
   ('a decrease in the demand for beef', False),
   ('the law of supply', False),
   ('a leftward shift of the demand curve for beef', False)]),
 ('law',
  None,
  'Which of the following help explain why the demand curve for a normal good slopes downward?<br><br>I. The '
  'substitution effect<br>II. The income effect<br>III. A change in consumer preferences',
  430,
  [('I only', False),
   ('II only', False),
   ('I and II only', True),
   ('II and III only', False),
   ('I, II and III', False)]),
 ('law',
  None,
  'In economics, "demand" differs from "quantity demanded" because demand refers to',
  528,
  [("the whole relationship between a good's price and the amount buyers will purchase at each price, while "
    'quantity demanded is the amount at one particular price',
    True),
   ('the amount buyers want at the current price, while quantity demanded is the amount actually sold',
    False),
   ('how badly buyers want a good, while quantity demanded is how many they buy', False),
   ('what firms are willing to sell, while quantity demanded is what buyers want', False),
   ('the amount buyers purchase in the long run, while quantity demanded is the amount in the short run',
    False)]),
 ('reading',
  'COFFEE',
  'The table above shows the weekly demand for coffee of Ann, Ben and Cal, the only three buyers in the '
  'market. At a price of $3 per cup, what is the market quantity demanded?',
  978,
  [('1 cup', False), ('4 cups', False), ('6 cups', False), ('7 cups', True), ('11 cups', False)]),
 ('reading',
  'COFFEE',
  'The table above shows the weekly demand for coffee of Ann, Ben and Cal, the only three buyers in the '
  'market. If the price rises from $2 to $4 per cup, the market quantity demanded',
  978,
  [('falls from 11 to 4 cups', True),
   ('falls from 5 to 3 cups', False),
   ('rises from 4 to 11 cups', False),
   ('falls from 11 to 7 cups', False),
   ('does not change, because demand has not changed', False)]),
 ('reading',
  'COFFEE',
  'The table above shows the weekly demand for coffee of Ann, Ben and Cal, the only three buyers in the '
  'market. Which of the following is true?',
  978,
  [('At a price of $5, Ann is the only buyer.', True),
   ('At a price of $1, the market quantity demanded is 6 cups.', False),
   ("Ben's demand does not follow the law of demand.", False),
   ('At a price of $4, the market quantity demanded is 3 cups.', False),
   ('Market quantity demanded falls by the same amount with each $1 price increase.', False)]),
 ('reading',
  'DEMAND',
  'The graph above shows the demand curve for a good. If the price falls from $8 to $4, the quantity '
  'demanded',
  828,
  [('increases from 2 to 6 units', True),
   ('decreases from 6 to 2 units', False),
   ('increases from 4 to 8 units', False),
   ('stays the same, because the demand curve has shifted right', False),
   ('stays the same, because demand has not changed', False)]),
 ('reading',
  'DEMAND',
  'The graph above shows the demand curve for a good. The movement from point A to point B is best described '
  'as',
  828,
  [('an increase in quantity demanded', True),
   ('an increase in demand', False),
   ('a decrease in demand', False),
   ('a decrease in quantity demanded', False),
   ('a rightward shift of the demand curve', False)]),
 ('reading',
  'DEMAND',
  'The graph above shows the demand curve for a good. The movement from point A to point B is caused by',
  828,
  [('a decrease in the price of the good', True),
   ("an increase in buyers' incomes", False),
   ('an increase in the price of a substitute good', False),
   ("a change in buyers' tastes in favor of the good", False),
   ('an increase in the number of buyers', False)]),
 ('reading',
  'LO',
  'The graphs above show the individual demand curves for movie tickets of Lena and Omar, the only two '
  'buyers in the market. At a price of $4, what is the market quantity demanded?',
  978,
  [('4 tickets', False),
   ('6 tickets', False),
   ('8 tickets', True),
   ('12 tickets', False),
   ('16 tickets', False)]),
 ('reading',
  'LO',
  'The graphs above show the individual demand curves for movie tickets of Lena and Omar, the only two '
  'buyers in the market. Which of the following is a point on the market demand curve?',
  978,
  [('Price $6, quantity 5', True),
   ('Price $6, quantity 3', False),
   ('Price $4, quantity 4', False),
   ('Price $2, quantity 6', False),
   ('Price $8, quantity 4', False)]),
 ('reading',
  None,
  'A demand schedule shows that at a price of $10, buyers want 100 units; at $8, 150 units; and at $6, 200 '
  'units. If the price falls from $10 to $6, which of the following occurs?',
  828,
  [('Quantity demanded increases by 100 units.', True),
   ('Quantity demanded increases by 50 units.', False),
   ('Quantity demanded decreases by 100 units.', False),
   ('Demand increases by 100 units.', False),
   ('Nothing changes, because the schedule stays the same.', False)]),
 ('reading',
  None,
  'The market demand curve for a good is found by',
  978,
  [('adding the quantities demanded by all buyers at each price', True),
   ('adding the prices all buyers are willing to pay at each quantity', False),
   ('averaging the quantities demanded by all buyers at each price', False),
   ('using the demand of the buyer who wants the most', False),
   ("multiplying one buyer's quantity demanded by the number of buyers", False)])]


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
    run("UPDATE question_topic SET name = :new WHERE chapter_id = :c AND name = :old", new=LAW[1], old=LAW[0], c=chapter_id)
    topics = {'law': topic(LAW[1]), 'reading': topic(READING)}

    # The three picture questions move to Reading (only those still under Law)
    pictured = [r[0] for r in conn.execute(sa.text(
        "SELECT id FROM question WHERE chapter_id = :c AND topic_id = :t AND image_url = ANY(:u)"),
        {'c': chapter_id, 't': topics['law'], 'u': list(PICTURES)}).all()]
    move(pictured, topics['law'], topics['reading'])

    # Pictures become drawn figures
    for url, key in PICTURES.items():
        run("UPDATE question SET figure = CAST(:f AS JSON) WHERE image_url = :u AND figure IS NULL",
            f=json.dumps(FIGURES[key]), u=url)

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
