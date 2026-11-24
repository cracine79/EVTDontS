"""Chapter 2.6a: eleven new questions, five pictures redrawn, two wording fixes

Reviewed and approved in the "Chapter 2.6a Question Review" doc (2026-11-24):
  * Topics unchanged: Marginal Utility / Marginal Benefit and Demand.
  * The cotton candy graph and the toy car, sushi, blue jeans and board game tables become drawn figures.
  * Fix 1: "The above diagram shows" becomes "The table above shows" on the eight table questions.
  * Fix 2: "Sammy's / Wes's dollar value total benefit she/he receives" reworded.
  * Five new marginal utility questions (new pizza table) and six new marginal benefit questions
    (new movie ticket graph).

Matched by chapter name, topic name, question text and picture address (ids differ between local and
live databases); each step is a no-op once applied.

Revision ID: e2c7a4f9b3d6
Revises: d9b5e3a7f1c4
Create Date: 2026-11-24
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'e2c7a4f9b3d6'
down_revision = 'd9b5e3a7f1c4'
branch_labels = None
depends_on = None

CHAPTER = '2.6a Marginal Utility, Marginal Benefit, and Demand'
MU = 'Marginal Utility'
MB = 'Marginal Benefit and Demand'

S3 = 'https://evtds-seeds.s3.us-east-2.amazonaws.com/'
COTTON_URL = S3 + 'TotalUtilityGraph.png'
TABLE_URLS = {S3 + 'ToyCarMarginalUtility.png': 'TOYCARS', S3 + 'SushiMU.png': 'SUSHI',
              S3 + 'BlueJeansTB.png': 'JEANS', S3 + 'BoardGamesMB.png': 'BOARDGAMES'}

FIGURES = {
    'COTTON': {'type': 'graph',
               'alt': 'A total utility curve for cotton candy that starts at the origin, rises steeply at first, '
                      'then flattens out as quantity increases.',
               'x': {'label': 'Quantity of cotton\ncandy (grams)', 'max': 10},
               'y': {'label': 'Total utility\n(utils)', 'max': 10},
               'xTicks': [], 'yTicks': [], 'origin': '0',
               'curves': [{'points': [[round(x / 4, 2), round(9.2 * (1 - (1 - x / 36) ** 3), 3)] for x in range(37)]
                                     + [[9.6, 9.2]],
                           'label': 'Total Utility', 'labelAt': [7.6, 8.1]}]},
    'TICKETS': {'type': 'graph',
                'alt': "Ana's marginal benefit curve for movie tickets, a downward-sloping line through the points "
                       "(1, $12), (2, $10), (3, $8), (4, $6), (5, $4) and (6, $2).",
                'x': {'label': 'Movie tickets', 'max': 7},
                'y': {'label': 'Price and\nmarginal benefit', 'max': 14, 'prefix': '$'},
                'grid': {'x': 1, 'y': 2}, 'origin': '0',
                'curves': [{'points': [[1, 12], [6, 2]], 'label': 'MB', 'labelAt': [6.15, 2.4], 'color': 'demand'}],
                'points': [{'at': [q, 14 - 2 * q], 'label': '', 'dot': True, 'color': 'demand'} for q in range(1, 7)]},
    'PIZZA': {'type': 'table', 'caption': "Priya's slices of pizza", 'columns': ['Quantity', 'Marginal utility (utils)'],
              'rows': [[1, 30], [2, 24], [3, 15], [4, 6], [5, -4]]},
    'TOYCARS': {'type': 'table', 'caption': 'Toy cars', 'columns': ['Quantity', 'Marginal utility (utils)'],
                'rows': [[1, 10], [2, 8], [3, 6], [4, 4], [5, 2]]},
    'SUSHI': {'type': 'table', 'caption': 'Sushi orders', 'columns': ['Quantity', 'Total utility (utils)'],
              'rows': [[1, 7], [2, 12], [3, 15], [4, 16], [5, 15]]},
    'JEANS': {'type': 'table', 'caption': 'Blue jeans', 'columns': ['Quantity', 'Total benefit'],
              'rows': [[0, '$0'], [1, '$50'], [2, '$95'], [3, '$135'], [4, '$170'], [5, '$200'], [6, '$225']]},
    'BOARDGAMES': {'type': 'table', 'caption': 'Board games', 'columns': ['Quantity', 'Marginal benefit'],
                   'rows': [[1, '$25'], [2, '$20'], [3, '$15'], [4, '$10'], [5, '$5']]},
}

# (old phrase, new phrase), applied only to questions using the given pictures
WORDING = [
    ('The above diagram shows', 'The table above shows'),
    ('Sammy’s dollar value total benefit she receives from buying',
     'the total benefit, in dollars, that Sammy receives from buying'),
    ('Wes’s dollar value total benefit he receives from buying',
     'the total benefit, in dollars, that Wes receives from buying'),
]

PIZZA_STEM = 'The table above shows Priya’s marginal utility from slices of pizza. '
TICKETS_STEM = 'The graph above shows Ana’s marginal benefit from movie tickets. '

# (topic, figure, text, video_start seconds, [(answer, is_correct), ...]) in A-E order
NEW_QUESTIONS = [
    (MU, 'PIZZA', PIZZA_STEM + 'What is her total utility from eating four slices?', 557,
     [('6 utils', False), ('15 utils', False), ('69 utils', False), ('75 utils', True), ('71 utils', False)]),
    (MU, 'PIZZA', PIZZA_STEM + 'If the pizza is free, how many slices will Priya eat to maximize her total utility?', 630,
     [('One, because the first slice gives her the most marginal utility', False),
      ('Three, because marginal utility falls below 10 utils after the third slice', False),
      ('Four, because each of the first four slices adds to her total utility and the fifth would lower it', True),
      ('Five, because the pizza is free', False),
      ('None, because she has no price to compare with her marginal utility', False)]),
    (MU, 'PIZZA', PIZZA_STEM + 'If Priya eats a fifth slice, her total utility will', 614,
     [('fall by 4 utils', True), ('become negative', False), ('rise by 4 utils', False), ('be maximized', False),
      ('fall to -4 utils', False)]),
    (MU, None, 'Which of the following best illustrates the law of diminishing marginal utility?', 494,
     [('A family gains more satisfaction from its first car than from its second car.', True),
      ("A family's total satisfaction falls when it buys a second car.", False),
      ('As the price of cars rises, a family buys fewer cars.', False),
      ('A family gains more satisfaction from a car than from a bicycle.', False),
      ("A family's second car adds more satisfaction than its first car.", False)]),
    (MU, None, 'If a consumer’s marginal utility from a good is positive but decreasing, which of the following must '
               'be true?<br><br>I. Total utility is increasing<br>II. Total utility is decreasing<br>III. Each '
               'additional unit adds less satisfaction than the unit before it', 459,
     [('I only', False), ('II only', False), ('III only', False), ('I and III only', True), ('II and III only', False)]),
    (MB, 'TICKETS', TICKETS_STEM + 'If the price of a movie ticket is $8, how many tickets will Ana buy?', 821,
     [('1', False), ('2', False), ('3', True), ('4', False), ('6', False)]),
    (MB, 'TICKETS', TICKETS_STEM + 'Which of the following can be read from the point at 3 tickets and $8?<br><br>'
                    'I. The third ticket brings Ana $8 of additional benefit<br>II. At a price of $8, Ana will buy 3 '
                    'tickets<br>III. Ana’s total benefit from 3 tickets is $8', 941,
     [('I only', False), ('II only', False), ('I and II only', True), ('I and III only', False),
      ('I, II and III', False)]),
    (MB, 'TICKETS', TICKETS_STEM + 'If the price of a movie ticket falls from $8 to $4, the number of tickets Ana '
                    'buys will', 850,
     [('increase from 3 to 5', True), ('increase from 3 to 4', False), ('increase from 2 to 4', False),
      ('stay at 3, because her marginal benefit has not changed', False), ('decrease from 5 to 3', False)]),
    (MB, None, 'Marginal benefit differs from marginal utility in that marginal benefit', 680,
     [('is measured in dollars rather than utils', True),
      ('increases as more of a good is consumed', False),
      ('measures total satisfaction rather than additional satisfaction', False),
      ('applies only to goods that are free', False),
      ('is always equal to the price of the good', False)]),
    (MB, None, 'The idea of diminishing marginal benefit helps explain why the demand curve slopes downward. Which of '
               'the following best states that explanation?', 927,
     [('Each additional unit brings a consumer less benefit, so the consumer will buy more units only at a lower '
       'price.', True),
      ('Each additional unit costs more to produce, so sellers charge more for it.', False),
      ('Total benefit falls as more units are consumed, so consumers buy fewer units.', False),
      ('Marginal benefit rises as more units are consumed, so consumers buy more at higher prices.', False),
      ('Consumers buy more of a good when its price rises.', False)]),
    (MB, None, 'Lena values her first cup of coffee each day at $5.00, her second at $3.50, her third at $2.00 and '
               'her fourth at $0.50. If a cup of coffee costs $2.00, how many cups will Lena buy each day?', 850,
     [('1', False), ('2', False), ('3', True), ('4', False), ('0', False)]),
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

    topics = {MU: topic(MU), MB: topic(MB)}

    # Pictures become drawn figures
    for url, fig in [(COTTON_URL, 'COTTON')] + list(TABLE_URLS.items()):
        run("UPDATE question SET figure = CAST(:f AS JSON) WHERE chapter_id = :c AND image_url = :u AND figure IS NULL",
            f=json.dumps(FIGURES[fig]), c=chapter_id, u=url)

    # Wording fixes on the table questions
    for old, new in WORDING:
        run("UPDATE question SET text = replace(text, :o, :n) WHERE chapter_id = :c AND image_url = ANY(:u) "
            "AND position(:o in text) > 0", o=old, n=new, c=chapter_id, u=list(TABLE_URLS))

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
