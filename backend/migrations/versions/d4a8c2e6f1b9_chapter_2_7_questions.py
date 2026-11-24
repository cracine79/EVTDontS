"""Chapter 2.7: seven new questions, six pictures redrawn, three fixes

Reviewed and approved in the "Chapter 2.7 Question Review" doc (2026-11-24):
  * Topics stay as they are: Consumer Surplus / Producer Surplus / Social Surplus.
  * The six old pictures (one demand graph, two supply graphs, three supply-and-demand graphs) become drawn
    graph figures with the same numbers.
  * Fix 1: "Social Surplus is defined as ... All of the above" becomes a Roman numeral question
    (answers rewritten in place, so the correct one, "I, II and III", shows last).
  * Fix 2: the "if demand increases" producer surplus question stays as it is.
  * Fix 3: "Increase by $200" / "Increase by $50" lowercased; the $400 / $150 social surplus question reworded.
  * New: two consumer surplus questions (buyers' table, area in words), one producer surplus question
    (sellers' table), four social surplus questions (new juice market graph: consumer surplus at $7,
    producer surplus at $3, social surplus at $3, Roman numerals on equilibrium).

Matched by chapter name, topic name, question/answer text and picture address (ids differ between local
and live databases); each step is a no-op once applied. No questions change topic, so no student progress moves.

Revision ID: d4a8c2e6f1b9
Revises: b3f7d1a9c6e2
Create Date: 2026-11-24
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'd4a8c2e6f1b9'
down_revision = 'b3f7d1a9c6e2'
branch_labels = None
depends_on = None

CHAPTER = '2.7 Consumer Surplus, Producer Surplus, and Social Surplus'
TOPICS = {'cs': 'Consumer Surplus', 'ps': 'Producer Surplus', 'ss': 'Social Surplus'}

S3 = 'https://evtds-seeds.s3.us-east-2.amazonaws.com/'
PICTURE_URLS = {
    S3 + 'DemandPQDash15100500.png': 'DEMAND_5_500',
    S3 + 'SD1P1Q.png': 'SD_25_15_300',
    S3 + 'SD1P1Q-2.png': 'SD_5_2_70',
    S3 + 'SD1P1Q-3.png': 'SD_5_2_60',
    S3 + 'SupplyPQDash.png': 'SUPPLY_ORIGIN',
    S3 + 'SupplyPQDash-2.png': 'SUPPLY_5_15',
}


def dollars(values):
    return [[v, f'${v:.2f}' if v % 1 else f'${v:g}'] for v in values]


FIGURES = {
    'DEMAND_5_500': {
        'type': 'graph',
        'alt': 'A demand curve from $5 at a quantity of 0 down to a quantity of 500 at $0, with dashed lines at '
               '($4, 100), ($3, 200), ($2, 300) and ($1, 400).',
        'x': {'label': 'Quantity', 'max': 560}, 'y': {'label': 'Price', 'max': 5.5}, 'origin': '0',
        'xTicks': [[q, str(q)] for q in (100, 200, 300, 400, 500)], 'yTicks': dollars([1, 2, 3, 4, 5]),
        'curves': [{'label': 'Demand', 'points': [[0, 5], [500, 0]], 'color': 'demand', 'labelAt': [420, 1.3]}],
        'guides': [[[0, p], [100 * (5 - p), p], [100 * (5 - p), 0]] for p in (4, 3, 2, 1)],
    },
    'SD_25_15_300': {
        'type': 'graph',
        'alt': 'Supply and demand. Demand starts at $25 and slopes down; supply starts at $10 and slopes up. '
               'They cross at a price of $15 and a quantity of 300.',
        'x': {'label': 'Quantity', 'max': 600}, 'y': {'label': 'Price', 'max': 27}, 'origin': '0',
        'xTicks': [[q, str(q)] for q in (100, 200, 300, 400, 500)], 'yTicks': dollars([5, 10, 15, 20, 25]),
        'curves': [{'label': 'Demand', 'points': [[0, 25], [570, 6]], 'color': 'demand'},
                   {'label': 'Supply', 'points': [[0, 10], [570, 19.5]], 'color': 'supply'}],
        'guides': [[[0, 15], [300, 15], [300, 0]]],
    },
    'SD_5_2_70': {
        'type': 'graph',
        'alt': 'Supply and demand. Demand starts at $5 and slopes down; supply starts at about $0.60 and slopes up. '
               'They cross at a price of $2 and a quantity of 70.',
        'x': {'label': 'Quantity', 'max': 120}, 'y': {'label': 'Price', 'max': 5.5}, 'origin': '0',
        'xTicks': [[q, str(q)] for q in (20, 40, 70, 100)], 'yTicks': dollars([1, 2, 3, 4, 5]),
        'curves': [{'label': 'Demand', 'points': [[0, 5], [100, 5 - 300 / 70]], 'color': 'demand'},
                   {'label': 'Supply', 'points': [[0, 0.6], [110, 2.8]], 'color': 'supply'}],
        'guides': [[[0, 2], [70, 2], [70, 0]]],
    },
    'SD_5_2_60': {
        'type': 'graph',
        'alt': 'Supply and demand. Demand starts at $5 and reaches a quantity of 100 at $0; supply starts at $0.50 '
               'and slopes up. They cross at a price of $2 and a quantity of 60.',
        'x': {'label': 'Quantity', 'max': 120}, 'y': {'label': 'Price', 'max': 5.5}, 'origin': '0',
        'xTicks': [[q, str(q)] for q in (20, 40, 60, 80, 100)], 'yTicks': dollars([0.5, 1, 2, 3, 4, 5]),
        'curves': [{'label': 'Demand', 'points': [[0, 5], [100, 0]], 'color': 'demand', 'labelAt': [96, 0.7]},
                   {'label': 'Supply', 'points': [[0, 0.5], [100, 3]], 'color': 'supply'}],
        'guides': [[[0, 2], [60, 2], [60, 0]]],
    },
    'SUPPLY_ORIGIN': {
        'type': 'graph',
        'alt': 'A supply curve starting at the origin and rising to $5 at a quantity of 500, with dashed lines at '
               '($1, 100), ($2, 200), ($3, 300), ($4, 400) and ($5, 500).',
        'x': {'label': 'Quantity', 'max': 560}, 'y': {'label': 'Price', 'max': 5.5}, 'origin': '0',
        'xTicks': [[q, str(q)] for q in (100, 200, 300, 400, 500)], 'yTicks': dollars([1, 2, 3, 4, 5]),
        'curves': [{'label': 'Supply', 'points': [[0, 0], [510, 5.1]], 'color': 'supply'}],
        'guides': [[[0, p], [100 * p, p], [100 * p, 0]] for p in (1, 2, 3, 4, 5)],
    },
    'SUPPLY_5_15': {
        'type': 'graph',
        'alt': 'A supply curve starting at $5 at a quantity of 0 and rising through ($10, 40) and ($15, 80).',
        'x': {'label': 'Quantity', 'max': 110}, 'y': {'label': 'Price', 'max': 18}, 'origin': '0',
        'xTicks': [[q, str(q)] for q in (20, 40, 60, 80, 100)], 'yTicks': dollars([5, 10, 15]),
        'curves': [{'label': 'Supply', 'points': [[0, 5], [100, 17.5]], 'color': 'supply'}],
        'guides': [[[0, 10], [40, 10], [40, 0]], [[0, 15], [80, 15], [80, 0]]],
    },
    'BUYERS': {'type': 'table', 'caption': 'Concert tickets', 'columns': ['Buyer', 'Maximum willing to pay'],
               'rows': [['Ana', '$60'], ['Ben', '$45'], ['Cara', '$35'], ['Dev', '$25']]},
    'SELLERS': {'type': 'table', 'caption': 'Used bicycles', 'columns': ['Seller', 'Minimum price to sell'],
                'rows': [['Kai', '$80'], ['Lena', '$120'], ['Omar', '$150'], ['Pia', '$200']]},
    'JUICE': {
        'type': 'graph',
        'alt': 'Supply and demand for juice. Demand runs from $10 at 0 to a quantity of 100 at $0; supply runs from '
               'the origin to $10 at 100. They cross at $5 and 50. At $7, quantity demanded is 30 and quantity '
               'supplied is 70; at $3, quantity demanded is 70 and quantity supplied is 30.',
        'x': {'label': 'Quantity', 'max': 110}, 'y': {'label': 'Price', 'max': 11}, 'origin': '0',
        'xTicks': [[30, '30'], [50, '50'], [70, '70'], [100, '100']],
        'yTicks': [[3, '$3'], [5, '$5'], [7, '$7'], [10, '$10']],
        'curves': [{'label': 'Demand', 'points': [[0, 10], [100, 0]], 'color': 'demand', 'labelAt': [90, 2]},
                   {'label': 'Supply', 'points': [[0, 0], [100, 10]], 'color': 'supply'}],
        'guides': [[[0, 7], [70, 7]], [[30, 7], [30, 0]], [[70, 7], [70, 0]], [[0, 5], [50, 5], [50, 0]],
                   [[0, 3], [70, 3]], [[30, 3], [30, 0]], [[70, 3], [70, 0]]],
    },
}

# Fix 1: (old answer text, new answer text, correct), rewritten in place so the order runs A-E
DEFINITION_OLD = 'Social Surplus is defined as'
DEFINITION_NEW = ('Social surplus is equal to which of the following?<br><br>I. The sum of consumer surplus and '
                  'producer surplus<br>II. The sum of the differences between the prices consumers would have been '
                  'willing to pay and the prices producers would have been willing to accept<br>III. The total '
                  'additional benefit to buyers and sellers when a good is bought and sold')
DEFINITION_ANSWERS = [
    ('The sum of consumer surplus and producer surplus', 'I only', False),
    ('The sum of the differences between the prices consumers would have been willing to pay and the prices '
     'producers would have been willing to accept.', 'II only', False),
    ('The total additional benefit to all stakeholders when a good is bought and sold.', 'I and II only', False),
    ('All of the above', 'II and III only', False),
    ('None of the above', 'I, II and III', True),
]

# Fix 3
LOWERCASE = [('Increase by $200', 'increase by $200'), ('Increase by $50', 'increase by $50')]
REWORD_MATCH = 'If the total Social Surplus in a market is calculated to be $400'
REWORD_NEW = ('If total social surplus in a market is $400 and consumer surplus is $150, and the market is in '
              'equilibrium so social surplus is maximized, then producer surplus must be')

JUICE_STEM = 'The graph above shows the market for juice. '

# (topic, figure, text, video_start seconds, [(answer, is_correct), ...]) in A-E order
NEW_QUESTIONS = [
    ('cs', 'BUYERS', 'The table above shows the most each of four buyers is willing to pay for a concert ticket. '
                     'If the market price of a ticket is $35, what is total consumer surplus in this market?', 196,
     [('$10', False), ('$25', False), ('$35', True), ('$105', False), ('$140', False)]),
    ('cs', None, 'On a supply and demand graph, consumer surplus is represented by the area', 262,
     [('below the demand curve, above the price, and to the left of the quantity consumers buy', True),
      ('above the supply curve, below the price, and to the left of the quantity producers sell', False),
      ('below the demand curve, above the supply curve, and to the left of the quantity traded', False),
      ('below the price and to the left of the quantity consumers buy', False),
      ('below the demand curve and to the right of the quantity consumers buy', False)]),
    ('ps', 'SELLERS', 'The table above shows the lowest price each of four sellers needs to receive to be willing '
                      'to sell a used bicycle. If the market price of a used bicycle is $150, what is total '
                      'producer surplus in this market?', 325,
     [('$50', False), ('$70', False), ('$100', True), ('$350', False), ('$450', False)]),
    ('ss', 'JUICE', JUICE_STEM + 'Compared with the equilibrium price of $5, how will consumer surplus change if '
                    'the price of juice is $7?', 481,
     [('decrease by $20', False), ('decrease by $45', False), ('decrease by $60', False),
      ('decrease by $80', True), ('increase by $80', False)]),
    ('ss', 'JUICE', JUICE_STEM + 'Compared with the equilibrium price of $5, how will producer surplus change if '
                    'the price of juice is $3?', 539,
     [('decrease by $80', True), ('decrease by $60', False), ('decrease by $45', False),
      ('decrease by $20', False), ('increase by $40', False)]),
    ('ss', 'JUICE', JUICE_STEM + 'Compared with the equilibrium price of $5, at a price of $3 social surplus will be',
     560,
     [('lower, because only 30 units are bought and sold', True),
      ('higher, because consumers pay a lower price', False),
      ('higher, because consumers want to buy 70 units', False),
      ('the same, because what consumers gain is exactly what producers lose', False),
      ('lower, because 70 units are bought and sold', False)]),
    ('ss', None, 'In a well-functioning market, which of the following is true at the equilibrium price and '
                 'quantity?<br><br>I. Quantity supplied equals quantity demanded<br>II. Social surplus is '
                 'maximized<br>III. Consumer surplus equals producer surplus', 571,
     [('I only', False), ('II only', False), ('I and II only', True), ('II and III only', False),
      ('I, II and III', False)]),
]


def upgrade():
    conn = op.get_bind()
    one = lambda sql, **kw: conn.execute(sa.text(sql), kw).scalar()
    run = lambda sql, **kw: conn.execute(sa.text(sql), kw)

    chapter_id = one("SELECT id FROM chapter WHERE name = :n", n=CHAPTER)
    if chapter_id is None:
        return

    topics = {}
    for key, name in TOPICS.items():
        topics[key] = one("SELECT id FROM question_topic WHERE chapter_id = :c AND name = :n", c=chapter_id, n=name)
        if topics[key] is None:
            topics[key] = one("INSERT INTO question_topic (name, chapter_id) VALUES (:n, :c) RETURNING id",
                              n=name, c=chapter_id)

    # Pictures become drawn graphs
    for url, fig in PICTURE_URLS.items():
        run("UPDATE question SET figure = CAST(:f AS JSON) WHERE chapter_id = :c AND image_url = :u AND figure IS NULL",
            f=json.dumps(FIGURES[fig]), c=chapter_id, u=url)

    # Fix 1: "All of the above" becomes Roman numerals
    qid = one("SELECT id FROM question WHERE chapter_id = :c AND text = :t", c=chapter_id, t=DEFINITION_OLD)
    if qid is not None:
        run("UPDATE question SET text = :t WHERE id = :q", t=DEFINITION_NEW, q=qid)
        for old, new, correct in DEFINITION_ANSWERS:
            run("UPDATE answer SET text = :n, is_correct = :c WHERE question_id = :q AND text = :o",
                n=new, c=correct, q=qid, o=old)

    # Fix 3: wording
    for old, new in LOWERCASE:
        run("UPDATE answer SET text = :n WHERE text = :o AND question_id IN "
            "(SELECT id FROM question WHERE chapter_id = :c)", n=new, o=old, c=chapter_id)
    run("UPDATE question SET text = :n WHERE chapter_id = :c AND position(:m in text) > 0",
        n=REWORD_NEW, m=REWORD_MATCH, c=chapter_id)

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
