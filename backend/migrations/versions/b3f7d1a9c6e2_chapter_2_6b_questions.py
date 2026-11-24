"""Chapter 2.6b: two subtopics, fourteen new questions, two pictures redrawn, three fixes

Reviewed and approved in the "Chapter 2.6b Question Review" doc (2026-11-24):
  * Topics: Calculating Marginal Cost (was Marginal Cost and Supply) / Marginal Cost and Output Decisions
    (new; takes the five "how many / what price" and rising marginal cost questions).
  * The truffles total cost and candy cane marginal cost pictures become drawn tables.
  * Fix 1: the truffles question's price changes from $35 to $28 so "4 Truffles" is correct
    (at $35 the fifth truffle, marginal cost $30, would also be made).
  * Fix 2: the $2 candy cane answer says "less than or equal to" the price.
  * Fix 3: "The above diagram shows" becomes "The table above shows" on the eight table questions.
  * Seven new calculation questions (new pies table) and seven new output decision questions
    (new bagel marginal cost graph).

Matched by chapter name, topic name, question/answer text and picture address (ids differ between local
and live databases); each step is a no-op once applied. Students' per-topic running totals move with the
questions, as in a7c4e2d9f3b6 (chapter 2.2a).

Revision ID: b3f7d1a9c6e2
Revises: e2c7a4f9b3d6
Create Date: 2026-11-24
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'b3f7d1a9c6e2'
down_revision = 'e2c7a4f9b3d6'
branch_labels = None
depends_on = None

CHAPTER = '2.6b Marginal Cost and Supply'
CALC = ('Marginal Cost and Supply', 'Calculating Marginal Cost')
OUTPUT = 'Marginal Cost and Output Decisions'

S3 = 'https://evtds-seeds.s3.us-east-2.amazonaws.com/'
TABLE_URLS = {S3 + 'TrufflesTC.png': 'TRUFFLES', S3 + 'CandyCaneMC.png': 'CANDY'}

# Distinctive phrases of the existing questions that move to Marginal Cost and Output Decisions
MOVED_TO_OUTPUT = [
    'how many truffles will Harold produce and sell',
    'If Harold produced and sold 4 truffles',
    'If the firm produced and sold 3 candy canes',
    'If the market price is $2, how many candy canes',
    'If marginal cost is increasing, this suggests',
]

PRICE_FIX = ('If the market price of truffles is $35', 'If the market price of truffles is $28')
ANSWER_FIX = ('3 candy canes, because firms will always produce and sell as long as the additional cost of '
              'producing one more is less than the price they receive for selling it',
              '3 candy canes, because firms will produce and sell as long as the additional cost of producing '
              'one more is less than or equal to the price they receive for selling it')
WORDING = ('The above diagram shows', 'The table above shows')

FIGURES = {
    'TRUFFLES': {'type': 'table', 'caption': 'Truffles', 'columns': ['Quantity', 'Total cost'],
                 'rows': [[1, '$10'], [2, '$25'], [3, '$45'], [4, '$70'], [5, '$100']]},
    'CANDY': {'type': 'table', 'caption': 'Candy canes', 'columns': ['Quantity', 'Marginal cost'],
              'rows': [[1, '$1'], [2, '$1.50'], [3, '$2'], [4, '$2.50'], [5, '$3']]},
    'PIES': {'type': 'table', 'caption': 'Ben’s pies', 'columns': ['Quantity of pies', 'Total cost'],
             'rows': [[0, '$20'], [1, '$26'], [2, '$34'], [3, '$44'], [4, '$58'], [5, '$76']]},
    'BAGELS': {'type': 'graph',
               'alt': "Rosa's marginal cost curve for bagels, an upward-sloping line through the points "
                      "(100, $1.00), (200, $1.50), (300, $2.00), (400, $2.50) and (500, $3.00).",
               'x': {'label': 'Bagels per day', 'max': 600},
               'y': {'label': 'Price and\nmarginal cost', 'max': 3.5},
               'grid': {'x': 100, 'y': 0.5}, 'origin': '0',
               'yTicks': [[0.5, '$0.50'], [1, '$1.00'], [1.5, '$1.50'], [2, '$2.00'], [2.5, '$2.50'],
                          [3, '$3.00'], [3.5, '$3.50']],
               'curves': [{'points': [[100, 1], [500, 3]], 'label': 'MC', 'labelAt': [515, 3.1], 'color': 'supply'}],
               'points': [{'at': [q, 0.5 + q / 200], 'label': '', 'dot': True, 'color': 'supply'}
                          for q in (100, 200, 300, 400, 500)]},
}

PIES_STEM = 'The table above shows the total cost to Ben of baking different quantities of pies. '
BAGELS_STEM = 'The graph above shows the marginal cost to Rosa’s bakery of producing bagels. '

# (topic, figure, text, video_start seconds, [(answer, is_correct), ...]) in A-E order
NEW_QUESTIONS = [
    ('calc', 'PIES', PIES_STEM + 'What is the marginal cost of the fourth pie?', 204,
     [('$10', False), ('$14', True), ('$14.50', False), ('$38', False), ('$58', False)]),
    ('calc', 'PIES', PIES_STEM + 'What is the marginal cost of the first pie?', 243,
     [('$6', True), ('$20', False), ('$26', False), ('$46', False), ('$0', False)]),
    ('calc', 'PIES', PIES_STEM + 'Which of the following is true?<br><br>I. The marginal cost of the second pie '
                     'is $8<br>II. Marginal cost increases as Ben bakes more pies<br>III. The total cost of baking '
                     '3 pies is $44', 397,
     [('I only', False), ('II only', False), ('I and II only', False), ('II and III only', False),
      ('I, II and III', True)]),
    ('calc', None, 'When a hot dog vendor increases output from 20 hot dogs to 30 hot dogs, total cost rises from '
                   '$50 to $90. What is the marginal cost of each of the 21st through 30th hot dogs?', 373,
     [('$3', False), ('$4', True), ('$9', False), ('$40', False), ('$90', False)]),
    ('calc', None, 'Ella’s total cost of making 10 bracelets is $120. Her total cost of making 12 bracelets is '
                   '$150. What is the marginal cost of each of the 11th and 12th bracelets?', 215,
     [('$12', False), ('$12.50', False), ('$15', True), ('$30', False), ('$150', False)]),
    ('calc', None, 'Marginal cost is calculated as the', 215,
     [('change in total cost divided by the change in quantity of output', True),
      ('total cost divided by the quantity of output', False),
      ('change in quantity of output divided by the change in total cost', False),
      ('change in total cost divided by the change in price', False),
      ('price minus total cost', False)]),
    ('calc', None, 'A hot dog vendor rents a cart for a flat monthly fee and pays the city a fixed license fee. '
                   'Which of the following is NOT part of the marginal cost of producing one more hot dog?', 243,
     [('The bun', False), ('The meat', False), ('The condiments', False),
      ('Wages for an extra worker needed to sell more hot dogs', False),
      ('The monthly rent on the cart', True)]),
    ('output', 'BAGELS', BAGELS_STEM + 'If the price of a bagel is $2.00, how many bagels per day will Rosa '
                         'produce?', 596,
     [('100', False), ('200', False), ('300', True), ('400', False), ('500', False)]),
    ('output', 'BAGELS', BAGELS_STEM + 'If the price of a bagel rises from $2.00 to $3.00, the number of bagels '
                         'Rosa produces per day will', 607,
     [('increase from 300 to 500', True), ('increase from 300 to 400', False),
      ('stay at 300, because her marginal cost has not changed', False), ('decrease from 500 to 300', False),
      ('increase from 200 to 400', False)]),
    ('output', 'BAGELS', BAGELS_STEM + 'Which of the following can be read from the point at 300 bagels and '
                         '$2.00?<br><br>I. Producing the 300th bagel adds $2.00 to Rosa’s total cost<br>II. At a '
                         'price of $2.00, Rosa will produce 300 bagels<br>III. Rosa’s total cost of producing 300 '
                         'bagels is $2.00', 659,
     [('I only', False), ('II only', False), ('I and II only', True), ('I and III only', False),
      ('I, II and III', False)]),
    ('output', 'PIES', PIES_STEM + 'If Ben can sell pies for $5 each, how many pies will he bake?', 483,
     [('0', True), ('1', False), ('4', False), ('5', False),
      ('It cannot be determined from the information provided', False)]),
    ('output', 'PIES', PIES_STEM + 'If Ben can sell pies for $12 each, how many pies will he bake?', 522,
     [('1', False), ('2', False), ('3', True), ('4', False), ('5', False)]),
    ('output', None, 'Which of the following best explains why the supply curve slopes upward?', 771,
     [('Marginal cost rises as output increases, so a producer will make more units only at a higher price.', True),
      ('Producers want to sell as much as possible at every price.', False),
      ('Each additional unit brings consumers less marginal benefit.', False),
      ('A higher price lowers the cost of producing each unit.', False),
      ('Consumers buy more of a good when its price rises.', False)]),
    ('output', None, 'In the short run, a hot dog vendor can only sell more hot dogs by hiring more workers, and '
                     'each additional worker sells fewer hot dogs than the one before. As the vendor’s output '
                     'increases, marginal cost will', 133,
     [('increase', True), ('decrease', False),
      ('stay the same, because each hot dog uses the same ingredients', False), ('fall to zero', False),
      ('increase at first, then decrease', False)]),
]


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

    def find(phrase, topic_id):
        return [r[0] for r in conn.execute(sa.text(
            "SELECT id FROM question WHERE topic_id = :t AND position(:s in text) > 0"),
            {'t': topic_id, 's': phrase}).all()]

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
        new=CALC[1], old=CALC[0], c=chapter_id)
    topics = {'calc': topic(CALC[1]), 'output': topic(OUTPUT)}

    for phrase in MOVED_TO_OUTPUT:
        move(find(phrase, topics['calc']), topics['calc'], topics['output'])

    # Pictures become drawn tables
    for url, fig in TABLE_URLS.items():
        run("UPDATE question SET figure = CAST(:f AS JSON) WHERE chapter_id = :c AND image_url = :u AND figure IS NULL",
            f=json.dumps(FIGURES[fig]), c=chapter_id, u=url)

    # Fix 3: they are tables, not diagrams
    run("UPDATE question SET text = replace(text, :o, :n) WHERE chapter_id = :c AND image_url = ANY(:u) "
        "AND position(:o in text) > 0", o=WORDING[0], n=WORDING[1], c=chapter_id, u=list(TABLE_URLS))

    # Fix 1: at $35 the fifth truffle (marginal cost $30) is worth making; $28 keeps "4 Truffles" correct
    run("UPDATE question SET text = replace(text, :o, :n) WHERE chapter_id = :c AND position(:o in text) > 0",
        o=PRICE_FIX[0], n=PRICE_FIX[1], c=chapter_id)

    # Fix 2: the third candy cane's marginal cost equals the $2 price
    run("UPDATE answer SET text = :new WHERE text = :old AND question_id IN "
        "(SELECT id FROM question WHERE chapter_id = :c)", new=ANSWER_FIX[1], old=ANSWER_FIX[0], c=chapter_id)

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
