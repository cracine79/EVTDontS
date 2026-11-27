"""Chapter 2.8: sixteen new questions, two subtopics, two pictures redrawn, four fixes

Reviewed and approved in the "Chapter 2.8 Question Review" doc (2026-11-26):
  * "Allocative Efficiency" becomes "Allocative Efficiency Defined"; the two questions on quantities other than
    equilibrium (80 units, 20 units) move to a new "Producing Too Little or Too Much" topic, with student progress.
  * The two old pictures (SDMBMC, SDMBMC2) become drawn graph figures with the same numbers.
  * Fix 1: "Equilibrium price = Equilibrium quantity" and "Marginal Utility = Marginal Cost" become
    "Consumer surplus = Producer surplus" and "Marginal Benefit < Marginal Cost".
  * Fix 2: "Allocative efficiency occurs when which of the following conditions is met?" is reworded in words
    (answers rewritten in place, so the correct one still shows third).
  * Fix 3: "MC = 60, MB = 60" becomes "MB = $20, MC = $20"; "MB=$50" gets its spaces.
  * Fix 4: "The above diagram shows the supply/MC ..." stems reworded; "When 20 units are sold" ends as a question.
  * New: five definition questions (demand = MB, supply = MC, tacos at equilibrium, MB/MC table, Roman numerals)
    and eleven too little / too much questions (new cookie market graph, words, the MB/MC table again).

Matched by chapter name, topic name, question/answer text and picture address (ids differ between local
and live databases); each step is a no-op once applied.

Revision ID: e7c3b9a1d5f2
Revises: d4a8c2e6f1b9
Create Date: 2026-11-26
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'e7c3b9a1d5f2'
down_revision = 'd4a8c2e6f1b9'
branch_labels = None
depends_on = None

CHAPTER = '2.8 Allocative Efficiency'
DEFINED = ('Allocative Efficiency', 'Allocative Efficiency Defined')
OFF = 'Producing Too Little or Too Much'

MOVED_TO_OFF = ['If 80 units of output are produced', 'When 20 units are sold']

S3 = 'https://evtds-seeds.s3.us-east-2.amazonaws.com/'
PICTURE_URLS = {S3 + 'SDMBMC.png': 'SDMBMC', S3 + 'SDMBMC2.png': 'SDMBMC2'}


def dollars(values):
    return [[v, f'${v:.2f}' if v % 1 else f'${v:g}'] for v in values]


FIGURES = {
    'SDMBMC': {
        'type': 'graph',
        'alt': 'Supply = MC starts at $0.50 and rises to $3 at a quantity of 100; Demand = MB starts at $5 and reaches '
               'a quantity of 100 at $0. They cross at $2 and 60. Dashed lines mark quantities of 40, 60 and 80.',
        'x': {'label': 'Quantity', 'max': 120}, 'y': {'label': 'Price', 'max': 5.5}, 'origin': '0',
        'xTicks': [[q, str(q)] for q in (20, 40, 60, 80, 100)], 'yTicks': dollars([1, 2, 3, 4, 5]),
        'curves': [{'label': 'Demand = MB', 'points': [[0, 5], [100, 0]], 'color': 'demand', 'labelAt': [88, 1.3]},
                   {'label': 'Supply = MC', 'points': [[0, 0.5], [100, 3]], 'color': 'supply'}],
        'guides': [[[40, 3], [40, 0]], [[60, 2], [60, 0]], [[80, 2.5], [80, 0]]],
    },
    'SDMBMC2': {
        'type': 'graph',
        'alt': 'Supply = MC starts at $5 and rises to $30 at a quantity of 100; Demand = MB starts at $50 and reaches '
               'a quantity of 100 at $0. They cross at $20 and 60. Dashed lines mark quantities of 20, 40, 60, 80 '
               'and 90 and the prices on each curve there.',
        'x': {'label': 'Quantity', 'max': 120}, 'y': {'label': 'Price', 'max': 55}, 'origin': '0',
        'xTicks': [[q, str(q)] for q in (20, 40, 60, 80, 90)], 'yTicks': dollars([5, 10, 15, 20, 25, 30, 40, 50]),
        'curves': [{'label': 'Demand = MB', 'points': [[0, 50], [100, 0]], 'color': 'demand', 'labelAt': [95, 9]},
                   {'label': 'Supply = MC', 'points': [[0, 5], [100, 30]], 'color': 'supply'}],
        'guides': [[[0, 40], [20, 40], [20, 0]], [[0, 10], [20, 10]], [[0, 30], [40, 30], [40, 0]], [[0, 15], [40, 15]],
                   [[0, 20], [60, 20], [60, 0]], [[0, 25], [80, 25], [80, 0]], [[0, 10], [80, 10]],
                   [[0, 27.5], [90, 27.5], [90, 0]], [[0, 5], [90, 5]]],
    },
    'COOKIES': {
        'type': 'graph',
        'alt': 'Market for cookies. Demand = MB runs from $20 at 0 to a quantity of 100 at $0; Supply = MC starts at '
               '$2 and rises to $12 at 100. They cross at $8 and 60. At 30 cookies, MB is $14 and MC is $5; at 90 '
               'cookies, MC is $11 and MB is $2.',
        'x': {'label': 'Quantity', 'max': 120}, 'y': {'label': 'Price', 'max': 22}, 'origin': '0',
        'xTicks': [[q, str(q)] for q in (30, 60, 90)], 'yTicks': dollars([2, 5, 8, 11, 14, 20]),
        'curves': [{'label': 'Demand = MB', 'points': [[0, 20], [100, 0]], 'color': 'demand', 'labelAt': [100, 3.5]},
                   {'label': 'Supply = MC', 'points': [[0, 2], [100, 12]], 'color': 'supply'}],
        'guides': [[[0, 14], [30, 14], [30, 0]], [[0, 5], [30, 5]], [[0, 8], [60, 8], [60, 0]],
                   [[0, 11], [90, 11], [90, 0]], [[0, 2], [90, 2]]],
    },
    'MBMC_TABLE': {'type': 'table', 'caption': 'Marginal benefit and marginal cost',
                   'columns': ['Quantity', 'Marginal benefit', 'Marginal cost'],
                   'rows': [['1', '$14', '$2'], ['2', '$12', '$4'], ['3', '$10', '$6'], ['4', '$8', '$8'],
                            ['5', '$6', '$10']]},
}

# Fix 1: answer texts on the first definition question
FIRST_DEF = 'Which of the following conditions would suggest the market has achieved allocative efficiency'
FIRST_DEF_ANSWERS = [('Equilibrium price = Equilibrium quantity', 'Consumer surplus = Producer surplus'),
                     ('Marginal Utility = Marginal Cost', 'Marginal Benefit < Marginal Cost')]

# Fix 2: (old answer, new answer, correct), rewritten in place so the order runs A-E
CONDITION_OLD = 'Allocative efficiency occurs when which of the following conditions is met?'
CONDITION_NEW = 'A market achieves allocative efficiency when the last unit sold'
CONDITION_ANSWERS = [
    ('Marginal Benefit > Marginal Cost.',
     'gives consumers an additional benefit greater than the additional cost of producing it', False),
    ('Marginal Benefit < Marginal Cost.',
     'gives consumers an additional benefit less than the additional cost of producing it', False),
    ('Marginal Benefit = Marginal Cost.',
     'gives consumers an additional benefit equal to the additional cost of producing it', True),
    ('Total revenue equals total surplus.', 'sells for a price equal to the average cost of producing all units', False),
    ('Producers maximize profits.', 'earns producers the most profit', False),
]

# Fix 3: answers on the "20 units" question
TWENTY_ANSWERS = [('MC = 60, MB = 60, allocative efficiency is achieved',
                   'MB = $20, MC = $20, allocative efficiency is achieved'),
                  ('MC = $5, MB=$50, allocative efficiency is achieved',
                   'MC = $5, MB = $50, allocative efficiency is achieved')]

# Fix 4: (phrase that finds the question, new full text)
GRAPH_STEM = 'The graph above shows the supply (marginal cost) and demand (marginal benefit) curves for a market. '
REWORDS = [
    ('If 80 units of output are produced',
     GRAPH_STEM + 'If 80 units of output are produced, does the market achieve allocative efficiency?'),
    ('Which quantity of output is allocatively efficient?',
     GRAPH_STEM + 'Which quantity of output is allocatively efficient?'),
    ('When 20 units are sold', GRAPH_STEM + 'When 20 units are sold, which of the following is true?'),
]

COOKIES = ('The graph above shows the market for cookies, where supply is marginal cost (MC) and demand is '
           'marginal benefit (MB). ')
TABLE = 'The table above shows the marginal benefit and marginal cost of each unit of a good. '

# (topic, figure, text, video_start seconds, [(answer, is_correct), ...]) in A-E order
NEW_QUESTIONS = [
    ('def', None, "A market's demand curve also shows", 54,
     [('the marginal cost to producers of making each additional unit', False),
      ('the marginal benefit to consumers of consuming each additional unit', True),
      ('the total benefit to consumers of all the units they consume', False),
      ('the consumer surplus at each price', False),
      ('the quantity producers are willing to sell at each price', False)]),
    ('def', None, "A market's supply curve also shows", 109,
     [('the marginal benefit to consumers of consuming each additional unit', False),
      ('the total cost to producers of making all the units they sell', False),
      ('the marginal cost to producers of making each additional unit', True),
      ('the producer surplus at each price', False),
      ('the price at which producers earn the most profit', False)]),
    ('def', None, 'In the market for tacos, the equilibrium price is $3 and the equilibrium quantity is 200 tacos. '
                  'Which of the following is true of the 200th taco?', 190,
     [('Its marginal benefit to consumers is $3, and its marginal cost to producers is less than $3.', False),
      ('Its marginal benefit to consumers and its marginal cost to producers are both $3.', True),
      ('Its marginal benefit to consumers is greater than $3, and its marginal cost to producers is $3.', False),
      ('Its marginal cost to producers is $3, and its marginal benefit to consumers is $0.', False),
      ('Its marginal benefit to consumers and its marginal cost to producers are both $600.', False)]),
    ('def', 'MBMC_TABLE', TABLE + 'Which quantity is allocatively efficient?', 221,
     [('1 unit', False), ('2 units', False), ('3 units', False), ('4 units', True), ('5 units', False)]),
    ('def', None, 'In a well-functioning market producing the equilibrium quantity, which of the following is true?'
                  '<br><br>I. The marginal benefit of the last unit sold equals its marginal cost<br>II. Allocative '
                  'efficiency is achieved<br>III. Social surplus is maximized', 391,
     [('I only', False), ('II only', False), ('I and II only', False), ('II and III only', False),
      ('I, II and III', True)]),

    ('off', 'COOKIES', COOKIES + 'If 30 cookies are produced and sold, which of the following is true?', 243,
     [('MB = $14 and MC = $5, so too few cookies are produced', True),
      ('MB = $5 and MC = $14, so too few cookies are produced', False),
      ('MB = $14 and MC = $5, so too many cookies are produced', False),
      ('MB = $8 and MC = $8, so allocative efficiency is achieved', False),
      ('MB = $5 and MC = $14, so too many cookies are produced', False)]),
    ('off', 'COOKIES', COOKIES + 'If 90 cookies are produced and sold, which of the following is true?', 327,
     [('MB = $11 and MC = $2; resources are underallocated to cookies', False),
      ('MB = $2 and MC = $11; resources are underallocated to cookies', False),
      ('MC = $11 and MB = $2; resources are overallocated to cookies', True),
      ('MC = $8 and MB = $8; allocative efficiency is achieved', False),
      ('MC = $11 and MB = $2; allocative efficiency is achieved', False)]),
    ('off', 'COOKIES', COOKIES + 'At which of the following quantities would there be an overallocation of resources '
                                 'to cookie production?', 365,
     [('20', False), ('40', False), ('50', False), ('60', False), ('80', True)]),
    ('off', 'COOKIES', COOKIES + 'If only 30 cookies are being produced, why should a 31st cookie be produced and '
                                 'sold?', 269,
     [('Its additional cost to producers is greater than its additional benefit to consumers.', False),
      ('Its additional benefit to consumers equals its additional cost to producers.', False),
      ('Its additional benefit to consumers is greater than its additional cost to producers.', True),
      ('Producing more cookies lowers the marginal cost of each cookie.', False),
      ('Consumers will buy any quantity that producers make.', False)]),
    ('off', 'COOKIES', COOKIES + 'If the quantity of cookies produced increases from 30 to 60, social surplus will',
     287,
     [('decrease, because the marginal cost of each cookie rises', False),
      ('increase, because each cookie from the 31st to the 60th adds more benefit to consumers than it costs to '
       'make', True),
      ('stay the same, because what consumers gain is exactly what producers lose', False),
      ('decrease, because the marginal benefit of each cookie falls', False),
      ('increase, because each cookie from the 31st to the 60th costs more to make than it adds in benefit', False)]),
    ('off', 'COOKIES', COOKIES + 'If 90 cookies are produced, which cookies should not have been produced?', 358,
     [('The 1st through the 30th', False), ('The 31st through the 60th', False),
      ('The 61st through the 90th', True), ('All 90 cookies', False),
      ('None, because consumers bought every cookie produced', False)]),
    ('off', None, 'If a market produces a quantity at which marginal benefit is greater than marginal cost, then', 303,
     [('too much of the good is produced, and resources are overallocated to it', False),
      ('too little of the good is produced, and resources are underallocated to it', True),
      ('too little of the good is produced, and resources are overallocated to it', False),
      ('too much of the good is produced, and resources are underallocated to it', False),
      ('allocative efficiency is achieved', False)]),
    ('off', None, 'The marginal cost of producing the last unit of a good is $12, and the marginal benefit to '
                  'consumers of that unit is $7. To achieve allocative efficiency, the market should', 365,
     [('produce more of the good, because consumers still value the last unit at $7', False),
      ('keep producing the same quantity, because consumers are still buying the good', False),
      ('stop producing the good entirely', False),
      ('produce less of the good', True),
      ('produce more of the good, until marginal cost falls to $7', False)]),
    ('off', None, 'At the quantity a market is producing, the marginal benefit of the last unit is $9 and its '
                  'marginal cost is $4. Which of the following is true?<br><br>I. Allocative efficiency is not '
                  'achieved<br>II. Too little of the good is produced<br>III. Resources are overallocated to the good',
     303,
     [('I only', False), ('II only', False), ('I and II only', True), ('II and III only', False),
      ('I, II and III', False)]),
    ('off', None, 'In a well-functioning market, at a quantity less than the equilibrium quantity, marginal benefit '
                  'is ___ marginal cost; at a quantity greater than the equilibrium quantity, marginal benefit is ___ '
                  'marginal cost.', 231,
     [('less than; greater than', False), ('equal to; equal to', False), ('greater than; greater than', False),
      ('greater than; less than', True), ('less than; less than', False)]),
    ('off', 'MBMC_TABLE', TABLE + 'If 2 units are produced, which of the following is true?', 303,
     [('Allocative efficiency is achieved, because marginal benefit is greater than marginal cost.', False),
      ("Too little is produced, because the 2nd unit's marginal benefit ($12) is greater than its marginal cost "
       "($4).", True),
      ("Too much is produced, because the 2nd unit's marginal benefit ($12) is greater than its marginal cost "
       "($4).", False),
      ('Too much is produced, because marginal benefit falls as more is produced.', False),
      ("Too little is produced, because the 2nd unit's marginal cost ($4) is greater than its marginal benefit "
       "($12).", False)]),
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
        new=DEFINED[1], old=DEFINED[0], c=chapter_id)
    topics = {'def': topic(DEFINED[1]), 'off': topic(OFF)}

    for phrase in MOVED_TO_OFF:
        move(find(phrase, topics['def']), topics['def'], topics['off'])

    # Pictures become drawn graphs
    for url, fig in PICTURE_URLS.items():
        run("UPDATE question SET figure = CAST(:f AS JSON) WHERE chapter_id = :c AND image_url = :u AND figure IS NULL",
            f=json.dumps(FIGURES[fig]), c=chapter_id, u=url)

    def answer_in(phrase, old, new, correct=None):
        sql = "UPDATE answer SET text = :n" + (", is_correct = :k" if correct is not None else "") + \
              " WHERE text = :o AND question_id IN (SELECT id FROM question WHERE chapter_id = :c " \
              "AND position(:p in text) > 0)"
        run(sql, n=new, k=correct, o=old, c=chapter_id, p=phrase)

    # Fix 1
    for old, new in FIRST_DEF_ANSWERS:
        answer_in(FIRST_DEF, old, new)

    # Fix 2: reworded in words
    qid = one("SELECT id FROM question WHERE chapter_id = :c AND text = :t", c=chapter_id, t=CONDITION_OLD)
    if qid is not None:
        run("UPDATE question SET text = :t WHERE id = :q", t=CONDITION_NEW, q=qid)
        for old, new, correct in CONDITION_ANSWERS:
            run("UPDATE answer SET text = :n, is_correct = :k WHERE question_id = :q AND text = :o",
                n=new, k=correct, q=qid, o=old)

    # Fix 3
    for old, new in TWENTY_ANSWERS:
        answer_in('When 20 units are sold', old, new)

    # Fix 4
    for phrase, new in REWORDS:
        run("UPDATE question SET text = :n WHERE chapter_id = :c AND position(:p in text) > 0 AND text <> :n",
            n=new, p=phrase, c=chapter_id)

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
