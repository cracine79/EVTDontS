"""Chapter 1.5: two subtopics, sixteen new questions, three questions move out, two pictures redrawn

Reviewed and approved in the "Chapter 1.5 Question Review" doc (2026-11-23):
  * The one topic (Theory of Absolute and Comparative Advantage) becomes Specialization and Gains from
    Trade; a new Absolute vs Comparative Advantage topic takes three existing questions.
  * Moved out (as decided in the Unit 1 plan): the lemons and limes table and the Metalland domestic
    opportunity cost questions go to 1.5a (Comparative Advantage Calculations); the "inside its
    production possibilities frontier" question goes to 1.4a (Reading the PPC).
  * The Metalland/Grungeton and Alpha/Beta pictures become drawn figures.
  * Nine new absolute vs comparative questions and seven new specialization questions.

Matched by chapter name, topic name and question text or picture address (ids differ between local and
live databases); each step is a no-op once applied. Students' per-topic running totals move with the
questions, as in b4c8e1f6a2d9 (chapter 1.1).

Revision ID: b8d1f4a7c2e6
Revises: a5e2c7b9d4f1
Create Date: 2026-11-23
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'b8d1f4a7c2e6'
down_revision = 'a5e2c7b9d4f1'
branch_labels = None
depends_on = None

CHAPTER = '1.5 Absolute and Comparative Advantage'
SPEC = ('Theory of Absolute and Comparative Advantage', 'Specialization and Gains from Trade')
ABS = 'Absolute vs Comparative Advantage'

MOVED_TO_ABS = ['Assume both France and Spain produce only two goods: cheese and olives',
                'Nations X and Y produce only shirts and ties',
                'If Country A can produce more units of both coffee and tea than Country B']

# (question start, destination chapter, destination topic)
MOVED_OUT = [('The table above shows the opportunity cost of producing lemons and limes',
              '1.5a Answering AP and University Level Comparative Advantage Questions', 'Comparative Advantage Calculations'),
             ('The above diagram shows the production of two countries, Metalland and Grungeton',
              '1.5a Answering AP and University Level Comparative Advantage Questions', 'Comparative Advantage Calculations'),
             ('When a country produces at a point inside its production possibilities frontier',
              '1.4a The Production Possibilities Curve', 'Reading the PPC')]

BASE = 'https://evtds-seeds.s3.us-east-2.amazonaws.com/'
PICTURES = {BASE + 'MettallandGrungeTon.png': 'MG', BASE + 'AlphaBetaLimesLemons.png': 'AB'}

FIGURES = {'MG': {'type': 'graph',
        'alt': 'Straight-line production possibilities curves for two countries producing guns (vertical axis, in '
               'tons) and butter (horizontal axis, in tons). Metalland: 30 tons of guns or 30 tons of butter. '
               'Grungeton: 10 tons of guns or 20 tons of butter.',
        'x': {'label': 'Butter (tons)', 'max': 36},
        'y': {'label': 'Guns (tons)', 'max': 36},
        'curves': [{'points': [[0, 30], [30, 0]], 'label': 'Metalland', 'labelAt': [17, 16]},
                   {'points': [[0, 10], [20, 0]], 'label': 'Grungeton', 'color': 'supply', 'labelAt': [1, 2]}],
        'xTicks': [[20, '20'], [30, '30']],
        'yTicks': [[10, '10'], [30, '30']],
        'origin': '0'},
 'AB': {'type': 'table',
        'columns': ['Country',
                    'Opportunity cost of producing 1 ton of limes',
                    'Opportunity cost of producing 1 ton of lemons'],
        'rows': [['Alpha', '1 ton of lemons', '1 ton of limes'],
                 ['Beta', '2 tons of lemons', '1/2 ton of limes']]},
 'H1': {'type': 'graph',
        'alt': 'Straight-line production possibilities curves for Northland and Southland, which use the same '
               'amount of resources to produce fish (vertical axis) and bread (horizontal axis). Northland: 12 '
               'fish or 6 bread. Southland: 4 fish or 8 bread.',
        'x': {'label': 'Bread', 'max': 10},
        'y': {'label': 'Fish', 'max': 14},
        'curves': [{'points': [[0, 12], [6, 0]], 'label': 'Northland', 'labelAt': [3.3, 6.6]},
                   {'points': [[0, 4], [8, 0]], 'label': 'Southland', 'color': 'supply', 'labelAt': [6.4, 1.9]}],
        'xTicks': [[6, '6'], [8, '8']],
        'yTicks': [[4, '4'], [12, '12']],
        'origin': '0'},
 'H2': {'type': 'graph',
        'alt': 'Straight-line production possibilities curves for Highland and Lowland, which use the same amount '
               'of resources to produce phones (vertical axis) and laptops (horizontal axis). Highland: 24 phones '
               'or 12 laptops. Lowland: 12 phones or 3 laptops.',
        'x': {'label': 'Laptops', 'max': 15},
        'y': {'label': 'Phones', 'max': 28},
        'curves': [{'points': [[0, 24], [12, 0]], 'label': 'Highland', 'labelAt': [6.6, 13.4]},
                   {'points': [[0, 12], [3, 0]], 'label': 'Lowland', 'color': 'supply', 'labelAt': [2.2, 7.5]}],
        'xTicks': [[3, '3'], [12, '12']],
        'yTicks': [[12, '12'], [24, '24']],
        'origin': '0'}}

# (topic, figure key or None, text, video_start seconds, [(answer, is_correct), ...] in A-E order)
NEW_QUESTIONS = [('abs',
  None,
  'A country has an absolute advantage in producing a good if it can',
  125,
  [('produce the good using fewer resources than another country', True),
   ('produce the good at a lower opportunity cost than another country', False),
   ('sell the good at a higher price than another country', False),
   ('export more of the good than another country imports', False),
   ('produce every good at a lower opportunity cost', False)]),
 ('abs',
  None,
  'A person has a comparative advantage in producing a good or service if he or she can produce it',
  237,
  [('using fewer resources than anyone else', False),
   ('at a lower opportunity cost than someone else', True),
   ('in greater total quantity than someone else', False),
   ('while earning a higher wage than someone else', False),
   ('only when he or she has an absolute advantage in it', False)]),
 ('abs',
  None,
  'Country X can produce a car with 10 hours of labor, while Country Y needs 20 hours of labor to produce a car. '
  'Which of the following is necessarily true?',
  125,
  [('Country X has an absolute advantage in producing cars.', True),
   ('Country X has a comparative advantage in producing cars.', False),
   ('Country X should specialize in producing cars.', False),
   ('Country Y has a comparative advantage in producing cars.', False),
   ('Country X has an absolute advantage in producing all goods.', False)]),
 ('abs',
  None,
  'A lawyer can type 100 words per minute and earns $300 an hour practicing law. Her assistant can type 60 words '
  'per minute and earns $25 an hour. Which of the following is true?',
  233,
  [('The lawyer has both an absolute and a comparative advantage in typing.', False),
   ('The lawyer has an absolute advantage in typing, but the assistant has a comparative advantage in typing.',
    True),
   ('The assistant has an absolute advantage in typing.', False),
   ('The assistant has both an absolute and a comparative advantage in typing.', False),
   ('Neither has a comparative advantage in typing.', False)]),
 ('abs',
  None,
  'Which of the following is impossible when two countries produce two goods?',
  760,
  [('One country has an absolute advantage in both goods.', False),
   ('One country has a comparative advantage in both goods.', True),
   ('One country has an absolute advantage in neither good.', False),
   ('One country has a comparative advantage in a good in which it has no absolute advantage.', False),
   ('Each country has an absolute advantage in one good.', False)]),
 ('abs',
  None,
  'Using the same resources, Country A can produce more wheat and more cloth than Country B. Which of the '
  'following must be true?<br><br>I. Country A has an absolute advantage in both goods.<br>II. Country A has a '
  'comparative advantage in both goods.<br>III. Country A cannot gain from trading with Country B.',
  591,
  [('I only', True),
   ('II only', False),
   ('I and II only', False),
   ('I and III only', False),
   ('I, II and III', False)]),
 ('abs',
  None,
  'Maya, a surgeon, can paint her fence in 4 hours; her teenage neighbor would need 8 hours. Maya earns $200 an '
  'hour at the hospital, and the neighbor earns $10 an hour at a grocery store. Who has the comparative advantage '
  'in painting the fence?',
  152,
  [('Maya, because she paints faster', False),
   ('Maya, because she earns more per hour', False),
   ("The neighbor, because her opportunity cost is $80 compared with Maya's $800", True),
   ('The neighbor, because she paints more slowly', False),
   ('Neither, because Maya has the absolute advantage', False)]),
 ('abs',
  None,
  'Which of the following statements is true?',
  613,
  [('A country can have a comparative advantage in a good even if it has no absolute advantage in any good.',
    True),
   ('A country with an absolute advantage in a good always has a comparative advantage in it.', False),
   ('Comparative advantage depends on which country produces more total output.', False),
   ('A country with an absolute advantage in both goods cannot gain from trade.', False),
   ('Comparative advantage is determined by which country has more resources.', False)]),
 ('abs',
  'H1',
  'The graph above shows the production possibilities curves for Northland and Southland, which use the same '
  'amount of resources to produce fish and bread. Which of the following is true?',
  430,
  [('Northland has an absolute advantage in both goods.', False),
   ('Southland has an absolute advantage in both goods.', False),
   ('Northland has an absolute advantage in fish, and Southland has an absolute advantage in bread.', True),
   ('Northland has an absolute advantage in bread, and Southland has an absolute advantage in fish.', False),
   ('Neither country has an absolute advantage.', False)]),
 ('spec',
  None,
  'A lawyer can type 100 words per minute and earns $300 an hour practicing law. Her assistant can type 60 words '
  'per minute and earns $25 an hour. To make the best use of her time, the lawyer should',
  233,
  [('hire the assistant to type and spend her own time practicing law', True),
   ('do her own typing, because she types faster', False),
   ('split her time equally between typing and practicing law', False),
   ('stop practicing law and become a full-time typist', False),
   ('hire the assistant only if he types faster than she does', False)]),
 ('spec',
  None,
  'Maya, a surgeon, can paint her fence in 4 hours, giving up $800 in hospital earnings. Her teenage neighbor '
  'would need 8 hours, giving up $80 in grocery store wages. For both to benefit, Maya should pay her neighbor',
  255,
  [('less than $80', False),
   ('exactly $80', False),
   ('more than $80 but less than $800', True),
   ('more than $800', False),
   ('between $10 and $200', False)]),
 ('spec',
  'H1',
  'The graph above shows the production possibilities curves for Northland and Southland, which use the same '
  'amount of resources to produce fish and bread. If each country specializes in the good in which it has an '
  'absolute advantage and the two countries trade, they can',
  487,
  [('consume combinations of fish and bread outside their own production possibilities curves', True),
   ('shift their production possibilities curves outward', False),
   ('produce more of both goods without specializing', False),
   ('eliminate scarcity in both countries', False),
   ('consume only what they could produce on their own', False)]),
 ('spec',
  'H1',
  'The graph above shows the production possibilities curves for Northland and Southland, which use the same '
  'amount of resources to produce fish and bread. Northland should',
  498,
  [('specialize in fish and trade for bread', True),
   ('specialize in bread and trade for fish', False),
   ('produce both goods and not trade', False),
   ('specialize in fish and not trade', False),
   ('import both goods from Southland', False)]),
 ('spec',
  'H2',
  'The graph above shows the production possibilities curves for Highland and Lowland, which use the same amount '
  'of resources to produce phones and laptops. Which of the following is true?',
  714,
  [('Highland has a comparative advantage in both goods.', False),
   ('Highland has an absolute advantage in both goods, but Lowland has a comparative advantage in phones.', True),
   ('Lowland has an absolute advantage in phones.', False),
   ('Lowland has a comparative advantage in laptops.', False),
   ('Neither country can gain from trade.', False)]),
 ('spec',
  'H2',
  'The graph above shows the production possibilities curves for Highland and Lowland, which use the same amount '
  'of resources to produce phones and laptops. According to the theory of comparative advantage, Lowland should',
  797,
  [('specialize in phones and import laptops', True),
   ('specialize in laptops and import phones', False),
   ('not trade, because Highland is better at producing both goods', False),
   ('stop producing both goods', False),
   ('produce equal amounts of both goods', False)]),
 ('spec',
  None,
  'Two countries specialize according to comparative advantage and trade with each other. Which of the following '
  'can result?<br><br>I. Both countries consume beyond their own production possibilities curves.<br>II. The '
  "total output of the two goods combined increases.<br>III. Each country's production possibilities curve shifts "
  'outward.',
  882,
  [('I only', False),
   ('II only', False),
   ('I and II only', True),
   ('II and III only', False),
   ('I, II and III', False)])]


def upgrade():
    conn = op.get_bind()
    one = lambda sql, **kw: conn.execute(sa.text(sql), kw).scalar()
    run = lambda sql, **kw: conn.execute(sa.text(sql), kw)

    chapter_id = one("SELECT id FROM chapter WHERE name = :n", n=CHAPTER)
    if chapter_id is None:
        return

    def topic(ch, name, create=True):
        found = one("SELECT id FROM question_topic WHERE chapter_id = :c AND name = :n", c=ch, n=name)
        if found is None and create:
            found = one("INSERT INTO question_topic (name, chapter_id) VALUES (:n, :c) RETURNING id", n=name, c=ch)
        return found

    def move(qids, from_topic, to_topic, to_chapter):
        """Move questions to another topic (and chapter), shifting each student's running totals with them."""
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
        run("UPDATE question SET topic_id = :t, chapter_id = :c WHERE id = ANY(:q)", t=to_topic, c=to_chapter, q=list(qids))

    def find(start, topic_id):
        return [r[0] for r in conn.execute(sa.text(
            "SELECT id FROM question WHERE chapter_id = :c AND topic_id = :t AND text LIKE :s"),
            {'c': chapter_id, 't': topic_id, 's': start + '%'}).all()]

    # Topics
    run("UPDATE question_topic SET name = :new WHERE chapter_id = :c AND name = :old", new=SPEC[1], old=SPEC[0], c=chapter_id)
    spec_id = topic(chapter_id, SPEC[1])
    abs_id = topic(chapter_id, ABS)
    topics = {'spec': spec_id, 'abs': abs_id}

    # Pictures become drawn figures (before any questions move, so both chapters' copies get them)
    for url, key in PICTURES.items():
        run("UPDATE question SET figure = CAST(:f AS JSON) WHERE image_url = :u AND figure IS NULL",
            f=json.dumps(FIGURES[key]), u=url)

    # Within the chapter
    for start in MOVED_TO_ABS:
        move(find(start, spec_id), spec_id, abs_id, chapter_id)

    # Out of the chapter
    for start, dest_chapter, dest_topic in MOVED_OUT:
        dest_ch = one("SELECT id FROM chapter WHERE name = :n", n=dest_chapter)
        dest_t = topic(dest_ch, dest_topic, create=False) if dest_ch else None
        if dest_t is not None:
            move(find(start, spec_id), spec_id, dest_t, dest_ch)

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
