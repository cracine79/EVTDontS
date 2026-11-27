"""Chapter 3.1: ten new questions, three subtopics, two pictures redrawn (and un-swapped), one question cut, four fixes

Reviewed and approved in the "Chapter 3.1 Question Review" doc (2026-11-26):
  * "PED Calculation" becomes "Calculating PED"; "Price Elasticity of Demand Concepts" becomes "Elastic, Inelastic
    and Unit Elastic Demand"; the three perfectly elastic/inelastic questions and the PED coefficient picture
    question move to a new "Perfectly Elastic and Perfectly Inelastic Demand" topic, with student progress.
  * Cut (Unit 3 plan): the straight-line demand curve question, with students' answers and topic progress.
    The cheese question stays here until the 3.3 migration moves it.
  * Pictures become drawn graphs. Fix 1: the "Perfectly inelastic" question showed the horizontal curve and the
    "Perfectly elastic" one the vertical curve; each now gets the right curve (matched by its correct answer).
  * Fix 2: the boxing question says the price is cut from $10 to $5.
  * Fix 3: the picture question stems are reworded.
  * Fix 4: the 1.5 coefficient question's answers are rewritten in place to run -30%, -20%, +10%, +20%, +30%.
  * New: five calculation questions (two on demand graphs), four elastic/inelastic/unit elastic questions and
    one perfectly elastic question.

Matched by chapter name, topic name, question/answer text and picture address (ids differ between local
and live databases); each step is a no-op once applied.

Revision ID: f1b5d9c3a7e8
Revises: e7c3b9a1d5f2
Create Date: 2026-11-26
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'f1b5d9c3a7e8'
down_revision = 'e7c3b9a1d5f2'
branch_labels = None
depends_on = None

CHAPTER = '3.1 Price Elasticity of Demand (PED)'
CALC = ('PED Calculation', 'Calculating PED')
ELASTIC = ('Price Elasticity of Demand Concepts', 'Elastic, Inelastic and Unit Elastic Demand')
PERFECT = 'Perfectly Elastic and Perfectly Inelastic Demand'

CUT = 'Moving from right to left upwards along a downward sloping linear demand curve'

OLD_PICTURE_STEM = 'For the above demand curve, demand is'
OLD_COEFFICIENT_STEM = 'For the above demand curve, the value of the (absolute value of the) PED coefficient is:'
NEW_PICTURE_STEM = 'Demand for the good shown in the graph above is'
NEW_COEFFICIENT_STEM = 'The PED coefficient for the demand curve shown above is'
# questions that move to PERFECT, by the start of their (old or new) text
MOVED_TO_PERFECT = [OLD_PICTURE_STEM, NEW_PICTURE_STEM, OLD_COEFFICIENT_STEM, NEW_COEFFICIENT_STEM,
                    'What does it mean for a good to have perfectly inelastic demand?']

FIGURES = {
    'VERT': {'type': 'graph', 'alt': 'A vertical demand curve: quantity demanded stays the same at every price.',
             'x': {'label': 'Quantity', 'max': 10}, 'y': {'label': 'Price', 'max': 10}, 'xTicks': [], 'yTicks': [],
             'curves': [{'label': 'Demand', 'points': [[5, 0.2], [5, 9.6]], 'color': 'demand',
                         'labelAt': [6.2, 9.2]}]},
    'HORIZ': {'type': 'graph',
              'alt': 'A horizontal demand curve: consumers buy any quantity at one price, and none at a higher price.',
              'x': {'label': 'Quantity', 'max': 10}, 'y': {'label': 'Price', 'max': 10}, 'xTicks': [], 'yTicks': [],
              'curves': [{'label': 'Demand', 'points': [[0, 5], [9.4, 5]], 'color': 'demand',
                          'labelAt': [8.6, 4.2]}]},
    'CALC1': {'type': 'graph',
              'alt': 'A downward-sloping demand curve from $14 to 70 units. Point A is at a price of $10 and a '
                     'quantity of 20; point B is at a price of $8 and a quantity of 30.',
              'x': {'label': 'Quantity', 'max': 75}, 'y': {'label': 'Price', 'max': 15},
              'xTicks': [[20, '20'], [30, '30']], 'yTicks': [[10, '$10'], [8, '$8']],
              'curves': [{'label': 'Demand', 'points': [[0, 14], [70, 0]], 'color': 'demand', 'labelAt': [62, 3.2]}],
              'guides': [[[0, 10], [20, 10], [20, 0]], [[0, 8], [30, 8], [30, 0]]],
              'points': [{'at': [20, 10], 'label': 'A', 'pos': 'ne', 'dot': True},
                         {'at': [30, 8], 'label': 'B', 'pos': 'ne', 'dot': True}]},
    'CALC2': {'type': 'graph',
              'alt': 'A downward-sloping demand curve from $12 to 60 units. Point X is at a price of $4 and a '
                     'quantity of 40; point Y is at a price of $2 and a quantity of 50.',
              'x': {'label': 'Quantity', 'max': 65}, 'y': {'label': 'Price', 'max': 13},
              'xTicks': [[40, '40'], [50, '50']], 'yTicks': [[4, '$4'], [2, '$2']],
              'curves': [{'label': 'Demand', 'points': [[0, 12], [60, 0]], 'color': 'demand', 'labelAt': [16, 11]}],
              'guides': [[[0, 4], [40, 4], [40, 0]], [[0, 2], [50, 2], [50, 0]]],
              'points': [{'at': [40, 4], 'label': 'X', 'pos': 'ne', 'dot': True},
                         {'at': [50, 2], 'label': 'Y', 'pos': 'ne', 'dot': True}]},
}

# Fix 1 + pictures: (question text start, correct answer text, figure)
PICTURES = [(OLD_PICTURE_STEM, 'Perfectly inelastic', 'VERT'),
            (OLD_PICTURE_STEM, 'Perfectly elastic', 'HORIZ'),
            (OLD_COEFFICIENT_STEM, 'equal to 0', 'VERT')]

# Fix 2
BOXING_OLD = ('Promoters of a boxing match know that if they charged $10 a ticket, 4,000 people would buy tickets, '
              'and if they charged $5 a ticket, 10,000 people would buy tickets.  Over this price range, the demand '
              'for tickets is')
BOXING_NEW = ('Promoters of a boxing match know that if they charged $10 a ticket, 4,000 people would buy tickets, '
              'and if they charged $5 a ticket, 10,000 people would buy tickets. If the promoters cut the price from '
              '$10 to $5, then over this price range the demand for tickets is')

# Fix 4: answers in id order, before and after
COEFF_15 = 'The PED coefficient for a product is calculated as 1.5.'
COEFF_15_OLD = ['+10%', '+20%', '+30%', '-30%', '-20%']
COEFF_15_NEW = [('-30%', True), ('-20%', False), ('+10%', False), ('+20%', False), ('+30%', False)]

GRAPH = 'The graph above shows the demand for a good. '

# (topic, figure, text, video_start seconds, [(answer, is_correct), ...]) in A-E order
NEW_QUESTIONS = [
    ('calc', None, 'When the price of a sandwich rises from $8 to $10, the quantity demanded falls from 400 to 340. '
                   'What is the price elasticity of demand coefficient for sandwiches?', 383,
     [('0.15', False), ('0.25', False), ('0.6', True), ('1.67', False), ('6.0', False)]),
    ('calc', None, 'The price of good X rises from $2 to $4, and the quantity demanded falls from 2,000 to 1,998. '
                   'The price of good Y rises from $8,000 to $8,002, and the quantity demanded falls from 4 to 2. '
                   'Which of the following is true?', 115,
     [('Demand for X and Y is equally sensitive to price, because each price rose by $2 and each quantity demanded '
       'fell by 2 units.', False),
      ('Demand for X is more sensitive to price, because the price of X rose by a larger percentage.', False),
      ('Demand for Y is more sensitive to price, because a very small percentage increase in its price cut quantity '
       'demanded in half.', True),
      ('Demand for X is more sensitive to price, because more units of X are bought.', False),
      ('The two cannot be compared, because the goods have very different prices.', False)]),
    ('calc', None, 'A store cuts the price of a video game from $60 to $45, and the number of games sold each week '
                   'rises from 80 to 120. Which of the following gives the price elasticity of demand coefficient '
                   'and describes demand for the game?', 502,
     [('0.5, inelastic', False), ('2, inelastic', False), ('2, elastic', True), ('0.5, elastic', False),
      ('1, unit elastic', False)]),
    ('calc', 'CALC1', GRAPH + 'If the price falls from $10 (point A) to $8 (point B), the price elasticity of demand '
                              'coefficient is', 502,
     [('0.4', False), ('0.8', False), ('1.0', False), ('2.5', True), ('5.0', False)]),
    ('calc', 'CALC2', GRAPH + 'If the price rises from $2 (point Y) to $4 (point X), which of the following gives the '
                              'price elasticity of demand coefficient and describes demand?', 235,
     [('0.2, inelastic', True), ('5, elastic', False), ('0.2, elastic', False), ('5, inelastic', False),
      ('1, unit elastic', False)]),

    ('elastic', None, 'Price elasticity of demand measures', 65,
     [('how far the demand curve shifts when consumer income changes', False),
      ('the sensitivity of quantity demanded to changes in price', True),
      ('the sensitivity of quantity supplied to changes in price', False),
      ('how much the price changes when demand increases', False),
      ('the dollar change in price divided by the change in units demanded', False)]),
    ('elastic', None, 'If the price of a good increases by 15 percent and, as a result, the quantity demanded '
                      'decreases by 15 percent, demand for the good is', 642,
     [('perfectly inelastic', False), ('relatively inelastic', False), ('unit elastic', True),
      ('relatively elastic', False), ('perfectly elastic', False)]),
    ('elastic', None, 'Demand for a good is unit elastic. If the price of the good decreases by 8 percent, the '
                      'quantity demanded will', 642,
     [('not change', False), ('increase by less than 8 percent', False), ('increase by exactly 8 percent', True),
      ('increase by more than 8 percent', False), ('decrease by 8 percent', False)]),
    ('elastic', None, 'Demand for a good is price elastic. Which of the following is true?<br><br>I. The PED '
                      'coefficient is greater than 1<br>II. A change in price leads to a larger percentage change in '
                      'quantity demanded<br>III. Quantity demanded is relatively insensitive to changes in price', 588,
     [('I only', False), ('II only', False), ('I and II only', True), ('II and III only', False),
      ('I, II and III', False)]),

    ('perfect', None, 'If the price elasticity of demand coefficient for a good is equal to infinity, which of the '
                      'following is true?', 728,
     [('Consumers buy the same quantity regardless of the price.', False),
      ('Quantity demanded changes by the same percentage as the price.', False),
      ('Consumers will buy any quantity at one price, but if the price rises at all, quantity demanded falls to '
       'zero.', True),
      ('Quantity demanded changes by a smaller percentage than the price.', False),
      ('The demand curve is vertical.', False)]),
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
            "SELECT id FROM question WHERE topic_id = :t AND position(:s in text) = 1"),
            {'t': topic_id, 's': phrase}).all()]

    def take_out(qids, from_topic):
        """Subtract these questions' answers from each student's progress in from_topic; return them per user."""
        rows = conn.execute(sa.text(
            "SELECT user_id, count(*), sum(CASE WHEN is_correct THEN 1 ELSE 0 END) FROM user_performance "
            "WHERE question_id = ANY(:q) GROUP BY user_id"), {'q': list(qids)}).all()
        for user_id, asked, correct in rows:
            run("UPDATE user_topic_progress SET questions_asked = GREATEST(questions_asked - :a, 0), "
                "answered_correctly = GREATEST(LEAST(answered_correctly - :r, questions_asked - :a), 0) "
                "WHERE user_id = :u AND topic_id = :t", a=asked, r=correct, u=user_id, t=from_topic)
        run("DELETE FROM user_topic_progress WHERE topic_id = :t AND questions_asked = 0", t=from_topic)
        return rows

    def move(qids, from_topic, to_topic):
        if not qids:
            return
        for user_id, asked, correct in take_out(qids, from_topic):
            updated = run("UPDATE user_topic_progress SET questions_asked = questions_asked + :a, "
                          "answered_correctly = answered_correctly + :r WHERE user_id = :u AND topic_id = :t",
                          a=asked, r=correct, u=user_id, t=to_topic).rowcount
            if not updated:
                run("INSERT INTO user_topic_progress (user_id, topic_id, questions_asked, answered_correctly) "
                    "VALUES (:u, :t, :a, :r)", u=user_id, t=to_topic, a=asked, r=correct)
        run("UPDATE question SET topic_id = :t WHERE id = ANY(:q)", t=to_topic, q=list(qids))

    # Topics
    for old, new in (CALC, ELASTIC):
        run("UPDATE question_topic SET name = :new WHERE chapter_id = :c AND name = :old", new=new, old=old, c=chapter_id)
    topics = {'calc': topic(CALC[1]), 'elastic': topic(ELASTIC[1]), 'perfect': topic(PERFECT)}

    # Cut the straight-line demand question, with answers and progress
    cut = [r[0] for r in conn.execute(sa.text(
        "SELECT id FROM question WHERE chapter_id = :c AND position(:s in text) = 1"), {'c': chapter_id, 's': CUT}).all()]
    if cut:
        for t in set(one("SELECT topic_id FROM question WHERE id = :q", q=q) for q in cut):
            take_out([q for q in cut if one("SELECT topic_id FROM question WHERE id = :q", q=q) == t], t)
        run("DELETE FROM user_performance WHERE question_id = ANY(:q)", q=cut)
        run("DELETE FROM answer WHERE question_id = ANY(:q)", q=cut)
        run("DELETE FROM question WHERE id = ANY(:q)", q=cut)

    # Pictures become drawn graphs, each matched by its correct answer (Fix 1 un-swaps the two curves)
    for stem, correct, fig in PICTURES:
        run("UPDATE question SET figure = CAST(:f AS JSON) WHERE chapter_id = :c AND text = :s AND figure IS NULL "
            "AND id IN (SELECT question_id FROM answer WHERE is_correct AND text = :a)",
            f=json.dumps(FIGURES[fig]), c=chapter_id, s=stem, a=correct)

    # Move to the perfectly elastic / inelastic topic
    for source in ('calc', 'elastic'):
        for phrase in MOVED_TO_PERFECT:
            move(find(phrase, topics[source]), topics[source], topics['perfect'])

    # Fix 2
    run("UPDATE question SET text = :n WHERE chapter_id = :c AND text = :o", n=BOXING_NEW, o=BOXING_OLD, c=chapter_id)

    # Fix 3
    run("UPDATE question SET text = :n WHERE chapter_id = :c AND text = :o",
        n=NEW_PICTURE_STEM, o=OLD_PICTURE_STEM, c=chapter_id)
    run("UPDATE question SET text = :n WHERE chapter_id = :c AND text = :o",
        n=NEW_COEFFICIENT_STEM, o=OLD_COEFFICIENT_STEM, c=chapter_id)

    # Fix 4: rewrite by id order, only while the answers are still the old ones
    qid = one("SELECT id FROM question WHERE chapter_id = :c AND position(:p in text) = 1", c=chapter_id, p=COEFF_15)
    if qid is not None:
        rows = conn.execute(sa.text("SELECT id, text FROM answer WHERE question_id = :q ORDER BY id"), {'q': qid}).all()
        if [r[1] for r in rows] == COEFF_15_OLD:
            for (aid, _), (text, correct) in zip(rows, COEFF_15_NEW):
                run("UPDATE answer SET text = :t, is_correct = :k WHERE id = :a", t=text, k=correct, a=aid)

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
