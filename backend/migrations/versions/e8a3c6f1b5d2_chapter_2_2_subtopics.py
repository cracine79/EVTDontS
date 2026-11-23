"""Chapter 2.2: two subtopics, fourteen new questions, one fix, two pictures redrawn

Reviewed and approved in the "Chapter 2.2 Question Review" doc (2026-11-23):
  * Topics: Supply and the Law of Supply (was The supply curve; keeps the nine concept questions) /
    Reading Supply Curves and Market Supply (new; takes the Firm A and Firm B graphs and the
    three-firm pencil table questions).
  * Fix: "Which of the following best describes the supply curve?" had a second true choice ("slopes
    downward from right to left" is the correct line read backwards); it becomes "slopes downward,
    then turns upward".
  * The two pictures become drawn figures.
  * Three new law of supply questions and eleven new reading/market supply questions.

Matched by chapter name, topic name, question/answer text and picture address (ids differ between
local and live databases); each step is a no-op once applied. Students' per-topic running totals move
with the questions, as in b4c8e1f6a2d9 (chapter 1.1).

Revision ID: e8a3c6f1b5d2
Revises: d4f7b2e9a6c1
Create Date: 2026-11-23
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'e8a3c6f1b5d2'
down_revision = 'd4f7b2e9a6c1'
branch_labels = None
depends_on = None

CHAPTER = '2.2 Supply Introduced'
LAW = ('The supply curve', 'Supply and the Law of Supply')
READING = 'Reading Supply Curves and Market Supply'

CURVE_FIX = ('Which of the following best describes the supply curve?', 'It slopes downward from right to left.',
             'It slopes downward, then turns upward.')

BASE = 'https://evtds-seeds.s3.us-east-2.amazonaws.com/'
PICTURES = {BASE + k: v for k, v in {'TwoSupplyCurves_3.png': 'FIRMAB', 'ThreeFIrmSupplyTable.png': 'PENCILS'}.items()}

FIGURES = {'FIRMAB': {'type': 'panels',
            'alt': 'Two individual supply curves for chairs on gridded graphs. Firm A: a straight line from '
                   'the origin through a price of $5 at quantity 500. Firm B: a straight line from the '
                   'origin through a price of $4 at quantity 500. Dashed lines mark the quantity at each '
                   'whole-dollar price: Firm A 100, 200, 300, 400 and 500; Firm B 125, 250, 375 and 500.',
            'panels': [{'type': 'graph',
                        'caption': 'Firm A',
                        'x': {'label': 'Quantity', 'max': 550},
                        'y': {'label': 'Price', 'max': 5.5, 'prefix': '$'},
                        'grid': {'x': 100, 'y': 1},
                        'origin': '0',
                        'curves': [{'points': [[0, 0], [500, 5]], 'color': 'supply'}],
                        'guides': [[[0, 1], [100, 1], [100, 0]],
                                   [[0, 2], [200, 2], [200, 0]],
                                   [[0, 3], [300, 3], [300, 0]],
                                   [[0, 4], [400, 4], [400, 0]],
                                   [[0, 5], [500, 5], [500, 0]]]},
                       {'type': 'graph',
                        'caption': 'Firm B',
                        'x': {'label': 'Quantity', 'max': 550},
                        'y': {'label': 'Price', 'max': 5.5, 'prefix': '$'},
                        'grid': {'x': 100, 'y': 1},
                        'origin': '0',
                        'curves': [{'points': [[0, 0], [550, 4.4]], 'color': 'supply'}],
                        'guides': [[[0, 1], [125, 1], [125, 0]],
                                   [[0, 2], [250, 2], [250, 0]],
                                   [[0, 3], [375, 3], [375, 0]],
                                   [[0, 4], [500, 4], [500, 0]]]}]},
 'PENCILS': {'type': 'table',
             'caption': 'Pencils supplied',
             'columns': ['Price', 'Firm A', 'Firm B', 'Firm C'],
             'rows': [['$50', 100, 200, 300],
                      ['$75', 200, 400, 450],
                      ['$100', 300, 600, 600],
                      ['$125', 400, 800, 750],
                      ['$150', 500, 1000, 900]]},
 'BIKES': {'type': 'table',
           'caption': 'Bike repairs supplied per week',
           'columns': ['Price per repair', 'Nia', 'Owen', 'Pat'],
           'rows': [['$10', 2, 0, 1],
                    ['$20', 4, 2, 2],
                    ['$30', 6, 4, 4],
                    ['$40', 8, 6, 5],
                    ['$50', 10, 8, 6]]},
 'SUPPLY': {'type': 'graph',
            'alt': 'An upward-sloping supply curve on a gridded graph, starting at a price of $2 at quantity '
                   '0 and rising to a price of $12 at quantity 10. Point A is at a price of $4 and quantity '
                   '2; point B is at a price of $8 and quantity 6.',
            'x': {'label': 'Quantity', 'max': 12},
            'y': {'label': 'Price', 'max': 12, 'prefix': '$'},
            'grid': {'x': 2, 'y': 2},
            'origin': '0',
            'curves': [{'points': [[0, 2], [10, 12]], 'color': 'supply'}],
            'points': [{'at': [2, 4], 'label': 'A', 'pos': 'nw', 'dot': True},
                       {'at': [6, 8], 'label': 'B', 'pos': 'nw', 'dot': True}]},
 'RS': {'type': 'panels',
        'alt': 'Two individual supply curves for candles on gridded graphs. Rosa: a straight line from the '
               'origin through a price of $8 at quantity 16. Sami: a straight line from a price of $2 at '
               'quantity 0 through a price of $10 at quantity 8.',
        'panels': [{'type': 'graph',
                    'caption': 'Rosa',
                    'x': {'label': 'Quantity', 'max': 18},
                    'y': {'label': 'Price', 'max': 11, 'prefix': '$'},
                    'grid': {'x': 2, 'y': 2},
                    'origin': '0',
                    'curves': [{'points': [[0, 0], [18, 9]], 'color': 'supply'}]},
                   {'type': 'graph',
                    'caption': 'Sami',
                    'x': {'label': 'Quantity', 'max': 18},
                    'y': {'label': 'Price', 'max': 11, 'prefix': '$'},
                    'grid': {'x': 2, 'y': 2},
                    'origin': '0',
                    'curves': [{'points': [[0, 2], [9, 11]], 'color': 'supply'}]}]}}

# (topic, figure, text, video_start seconds, [(answer, is_correct), ...]) in A-E order
NEW_QUESTIONS = [('law',
  None,
  'A town has hundreds of lawn-mowing services, all offering an identical service. In the supply model, each '
  'service decides how many lawns to mow at the market price rather than setting its own price. Which of the '
  'following best explains why?',
  302,
  [('If one service charged more than the others, no homeowner would hire it.', True),
   ('The government sets the price of lawn mowing.', False),
   ('Each service wants to mow as many lawns as possible regardless of price.', False),
   ('Homeowners are willing to pay any price for lawn mowing.', False),
   ('Each service sets its price to equal the quantity it wants to supply.', False)]),
 ('law',
  None,
  'A bakery can make up to 100 loaves a day with its current ovens and staff. To make more than 100, it must '
  'pay its workers overtime. Which of the following best explains why the bakery will supply more than 100 '
  'loaves a day only at a higher price?',
  543,
  [('Each loaf beyond 100 costs more to make, so the bakery needs a higher price to cover that cost.', True),
   ('Consumers buy more bread when the price is higher.', False),
   ('The bakery wants to sell as many loaves as possible at any price.', False),
   ("A higher price lowers the bakery's cost of making bread.", False),
   ('The law of demand requires the bakery to raise its price.', False)]),
 ('law',
  None,
  'According to the law of supply, which of the following would occur if the price of strawberries '
  'increases?<br><br>I. Strawberry growers become more willing to produce strawberries<br>II. The quantity '
  'of strawberries supplied increases<br>III. The supply curve for strawberries shifts to the right',
  500,
  [('I only', False),
   ('II only', False),
   ('I and II only', True),
   ('II and III only', False),
   ('I, II and III', False)]),
 ('reading',
  'BIKES',
  'The table above shows the weekly supply of bike repairs by Nia, Owen and Pat, the only three sellers in '
  'the market. At a price of $30 per repair, what is the market quantity supplied?',
  659,
  [('4 repairs', False),
   ('6 repairs', False),
   ('10 repairs', False),
   ('14 repairs', True),
   ('19 repairs', False)]),
 ('reading',
  'BIKES',
  'The table above shows the weekly supply of bike repairs by Nia, Owen and Pat, the only three sellers in '
  'the market. If the price rises from $20 to $40 per repair, the market quantity supplied',
  659,
  [('increases from 8 to 19 repairs', True),
   ('increases from 4 to 8 repairs', False),
   ('decreases from 19 to 8 repairs', False),
   ('increases from 8 to 14 repairs', False),
   ('does not change, because supply has not changed', False)]),
 ('reading',
  'BIKES',
  'The table above shows the weekly supply of bike repairs by Nia, Owen and Pat, the only three sellers in '
  'the market. Which of the following is true?',
  659,
  [('At a price of $10, Owen supplies no repairs.', True),
   ('At a price of $50, the market quantity supplied is 10 repairs.', False),
   ("Pat's supply does not follow the law of supply.", False),
   ('At a price of $20, the market quantity supplied is 6 repairs.', False),
   ('Market quantity supplied rises by the same amount with each $10 price increase.', False)]),
 ('reading',
  'SUPPLY',
  'The graph above shows the supply curve for a good. If the price rises from $4 to $8, the quantity '
  'supplied',
  500,
  [('increases from 2 to 6 units', True),
   ('decreases from 6 to 2 units', False),
   ('increases from 4 to 8 units', False),
   ('stays the same, because the supply curve has shifted right', False),
   ('stays the same, because supply has not changed', False)]),
 ('reading',
  'SUPPLY',
  'The graph above shows the supply curve for a good. The movement from point A to point B is best described '
  'as',
  500,
  [('an increase in quantity supplied', True),
   ('an increase in supply', False),
   ('a decrease in supply', False),
   ('a decrease in quantity supplied', False),
   ('a rightward shift of the supply curve', False)]),
 ('reading',
  'SUPPLY',
  'The graph above shows the supply curve for a good. The movement from point A to point B is caused by',
  500,
  [('an increase in the price of the good', True),
   ('a decrease in the price of the good', False),
   ('a decrease in the cost of the inputs used to make the good', False),
   ('an improvement in the technology used to make the good', False),
   ('an increase in the number of sellers', False)]),
 ('reading',
  'RS',
  'The graphs above show the individual supply curves for candles of Rosa and Sami, the only two sellers in '
  'the market. At a price of $4, what is the market quantity supplied?',
  659,
  [('2 candles', False),
   ('8 candles', False),
   ('10 candles', True),
   ('12 candles', False),
   ('16 candles', False)]),
 ('reading',
  'RS',
  'The graphs above show the individual supply curves for candles of Rosa and Sami, the only two sellers in '
  'the market. Which of the following is a point on the market supply curve?',
  659,
  [('Price $6, quantity 16', True),
   ('Price $6, quantity 12', False),
   ('Price $4, quantity 12', False),
   ('Price $2, quantity 6', False),
   ('Price $8, quantity 16', False)]),
 ('reading',
  'RS',
  'The graphs above show the individual supply curves for candles of Rosa and Sami, the only two sellers in '
  'the market. At a price of $2, which of the following is true?',
  659,
  [('The market quantity supplied is 4, all of it from Rosa.', True),
   ('The market quantity supplied is 0, because Sami supplies none.', False),
   ('The market quantity supplied is 6.', False),
   ('Rosa supplies 4 candles and Sami supplies 2.', False),
   ('The market quantity supplied is 2.', False)]),
 ('reading',
  None,
  'A supply schedule shows that at a price of $5, farms supply 200 bushels of apples; at $6, 260 bushels; '
  'and at $7, 320 bushels. If the price falls from $7 to $5, which of the following occurs?',
  500,
  [('Quantity supplied decreases by 120 bushels.', True),
   ('Quantity supplied decreases by 60 bushels.', False),
   ('Quantity supplied increases by 120 bushels.', False),
   ('Supply decreases by 120 bushels.', False),
   ('Nothing changes, because the schedule stays the same.', False)]),
 ('reading',
  None,
  'The market supply curve for a good is found by',
  659,
  [('adding the quantities supplied by all sellers at each price', True),
   ('adding the prices all sellers are willing to accept at each quantity', False),
   ('averaging the quantities supplied by all sellers at each price', False),
   ('using the supply of the largest seller', False),
   ("multiplying one seller's quantity supplied by the number of sellers", False)])]


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

    # The two picture questions move to Reading (only those still under Law)
    pictured = [r[0] for r in conn.execute(sa.text(
        "SELECT id FROM question WHERE chapter_id = :c AND topic_id = :t AND image_url = ANY(:u)"),
        {'c': chapter_id, 't': topics['law'], 'u': list(PICTURES)}).all()]
    move(pictured, topics['law'], topics['reading'])

    # Pictures become drawn figures
    for url, key in PICTURES.items():
        run("UPDATE question SET figure = CAST(:f AS JSON) WHERE image_url = :u AND figure IS NULL",
            f=json.dumps(FIGURES[key]), u=url)

    # Fix: choice E described the same line as the correct answer
    run("UPDATE answer SET text = :new WHERE text = :old AND question_id IN "
        "(SELECT id FROM question WHERE chapter_id = :c AND text LIKE :s)",
        new=CURVE_FIX[2], old=CURVE_FIX[1], c=chapter_id, s=CURVE_FIX[0] + '%')

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
