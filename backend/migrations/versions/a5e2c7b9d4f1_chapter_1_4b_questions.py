"""Chapter 1.4b: two subtopics and sixteen new questions

Reviewed and approved in the "Chapter 1.4b Question Review" doc (2026-11-23):
  * The one topic (PPF Opportunity Cost) becomes Constant vs Increasing Opportunity Cost, and a new
    Calculating Opportunity Cost on the PPC topic takes the cherries and apples question.
  * Twelve new calculation questions and four new constant vs increasing questions, using a
    straight-line graph, the Robotland table and the pizza and taco graph (frontend2 QuestionFigure.jsx).

Matched by chapter name, topic name and question text (ids differ between local and live databases);
each step is a no-op once applied. Students' per-topic running totals move with the cherries question,
as in b4c8e1f6a2d9 (chapter 1.1).

Revision ID: a5e2c7b9d4f1
Revises: f3c8a1d6e9b2
Create Date: 2026-11-23
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'a5e2c7b9d4f1'
down_revision = 'f3c8a1d6e9b2'
branch_labels = None
depends_on = None

CHAPTER = '1.4b Opportunity Cost and the PPF'
SHAPE = ('PPF Opportunity Cost', 'Constant vs Increasing Opportunity Cost')
CALC = 'Calculating Opportunity Cost on the PPC'
MOVED_TO_CALC = 'Based on the production possibilities curve for cherries and apples'

FIGURES = {'G1': {'type': 'graph',
        'alt': 'Straight-line production possibilities curve from 40 units of wheat on the vertical axis to 20 '
               'units of cloth on the horizontal axis.',
        'x': {'label': 'Cloth', 'max': 30},
        'y': {'label': 'Wheat', 'max': 50},
        'curves': [{'points': [[0, 40], [20, 0]], 'color': 'supply'}],
        'xTicks': [[20, '20']],
        'yTicks': [[40, '40']],
        'origin': '0'},
 'G2': {'type': 'table',
        'caption': 'Production possibilities for Robotland',
        'columns': ['Option', 'Robots', 'Cars'],
        'rows': [['A', 0, 20], ['B', 1, 18], ['C', 2, 14], ['D', 3, 8], ['E', 4, 0]]},
 'G3': {'type': 'graph',
        'alt': 'Production possibilities curve for pizzas (vertical axis) and tacos (horizontal axis) through '
               'point A (0 tacos, 50 pizzas), B (10 tacos, 45 pizzas), C (20 tacos, 35 pizzas), D (30 tacos, 20 '
               'pizzas) and E (40 tacos, 0 pizzas). Point F, at 10 tacos and 20 pizzas, is inside the curve.',
        'x': {'label': 'Tacos', 'max': 50},
        'y': {'label': 'Pizzas', 'max': 60},
        'curves': [{'points': [[0, 50], [10, 45], [20, 35], [30, 20], [40, 0]]}],
        'guides': [[[0, 45], [10, 45], [10, 0]], [[0, 35], [20, 35], [20, 0]], [[0, 20], [30, 20], [30, 0]]],
        'xTicks': [[10, '10'], [20, '20'], [30, '30'], [40, '40']],
        'yTicks': [[20, '20'], [35, '35'], [45, '45'], [50, '50']],
        'origin': '0',
        'points': [{'at': [0, 50], 'label': 'A', 'pos': 'ne', 'dot': True},
                   {'at': [10, 45], 'label': 'B', 'pos': 'ne', 'dot': True},
                   {'at': [20, 35], 'label': 'C', 'pos': 'ne', 'dot': True},
                   {'at': [30, 20], 'label': 'D', 'pos': 'ne', 'dot': True},
                   {'at': [40, 0], 'label': 'E', 'pos': 'ne', 'dot': True},
                   {'at': [10, 20], 'label': 'F', 'pos': 'ne', 'dot': True, 'color': 'demand'}]}}

# (topic, figure key or None, text, video_start seconds, [(answer, is_correct), ...] in A-E order)
NEW_QUESTIONS = [('calc',
  'G1',
  'The graph above shows the production possibilities curve for an economy that produces wheat and cloth. What is '
  'the opportunity cost of producing one unit of cloth?',
  180,
  [('1/2 unit of wheat', False),
   ('2 units of wheat', True),
   ('20 units of wheat', False),
   ('40 units of wheat', False),
   ('60 units of wheat', False)]),
 ('calc',
  'G1',
  'Using the production possibilities curve for wheat and cloth shown above, which of the following statements '
  'are true?<br><br>I. The opportunity cost of 1 unit of cloth is 2 units of wheat.<br>II. The opportunity cost '
  'of 1 unit of wheat is 1/2 unit of cloth.<br>III. The opportunity cost of cloth rises as more cloth is '
  'produced.',
  291,
  [('I only', False),
   ('II only', False),
   ('I and II only', True),
   ('II and III only', False),
   ('I, II and III', False)]),
 ('calc',
  None,
  'Bikeland can produce either 100 bicycles or 50 scooters, or any combination along a straight-line production '
  "possibilities curve between them. What is Bikeland's opportunity cost of producing one bicycle?",
  255,
  [('1/2 of a scooter', True),
   ('2 scooters', False),
   ('50 scooters', False),
   ('100 scooters', False),
   ('1/100 of a scooter', False)]),
 ('calc',
  None,
  'An economy whose resources are all identical can produce 6 movies and 0 tons of steel, or 4 movies and 2 tons '
  'of steel. What is the opportunity cost of each ton of steel?',
  511,
  [('1/2 of a movie', False), ('1 movie', True), ('2 movies', False), ('4 movies', False), ('6 movies', False)]),
 ('calc',
  'G2',
  'The table above shows the maximum combinations of robots and cars Robotland can produce. What is the '
  'opportunity cost of producing the third robot?',
  764,
  [('2 cars', False), ('4 cars', False), ('6 cars', True), ('8 cars', False), ('14 cars', False)]),
 ('calc',
  'G2',
  'The table above shows the maximum combinations of robots and cars Robotland can produce. What is the total '
  'opportunity cost of producing the first two robots?',
  764,
  [('2 cars', False), ('4 cars', False), ('6 cars', True), ('14 cars', False), ('18 cars', False)]),
 ('calc',
  'G2',
  'The table above shows the maximum combinations of robots and cars Robotland can produce. What is the '
  'opportunity cost of producing the fourth robot?',
  764,
  [('0 cars', False), ('2 cars', False), ('6 cars', False), ('8 cars', True), ('20 cars', False)]),
 ('calc',
  'G3',
  'The graph above shows the production possibilities curve for pizzas and tacos. If the economy moves from point '
  'B to point C, what is the opportunity cost of each additional taco?',
  764,
  [('1/2 of a pizza', False),
   ('1 pizza', True),
   ('1.5 pizzas', False),
   ('10 pizzas', False),
   ('35 pizzas', False)]),
 ('calc',
  'G3',
  'The graph above shows the production possibilities curve for pizzas and tacos. If the economy moves from point '
  'C to point D, what is the opportunity cost of each additional taco?',
  786,
  [('2/3 of a pizza', False),
   ('1 pizza', False),
   ('1.5 pizzas', True),
   ('15 pizzas', False),
   ('20 pizzas', False)]),
 ('calc',
  'G3',
  'The graph above shows the production possibilities curve for pizzas and tacos. If the economy moves from point '
  'D to point C, what is the opportunity cost of each additional pizza?',
  797,
  [('2/3 of a taco', True), ('1 taco', False), ('1.5 tacos', False), ('10 tacos', False), ('15 tacos', False)]),
 ('calc',
  'G3',
  'The graph above shows the production possibilities curve for pizzas and tacos. If the economy moves from point '
  'F to point C, what is the opportunity cost of the additional pizzas and tacos?',
  126,
  [('Zero', True),
   ('10 tacos', False),
   ('15 pizzas', False),
   ('1.5 pizzas per taco', False),
   ('35 pizzas', False)]),
 ('calc',
  None,
  "In one hour, Kai can either catch 3 fish or collect 6 coconuts. What is Kai's opportunity cost of catching one "
  'fish?',
  180,
  [('1/2 of a coconut', False),
   ('2 coconuts', True),
   ('3 coconuts', False),
   ('6 coconuts', False),
   ('18 coconuts', False)]),
 ('shape',
  'G2',
  'The table above shows the maximum combinations of robots and cars Robotland can produce. As Robotland produces '
  'more robots, the opportunity cost of each additional robot',
  734,
  [('increases, because resources better suited to making cars must be shifted into making robots', True),
   ('decreases, because Robotland gets better at making robots', False),
   ('stays the same, because each robot requires the same resources', False),
   ('increases, because robots sell for higher prices than cars', False),
   ('cannot be determined from the table', False)]),
 ('shape',
  None,
  "A straight-line production possibilities curve implies that the economy's resources are",
  314,
  [('specialized, with some better at producing one good', False),
   ('equally well suited to producing either good', True),
   ('partly unemployed', False),
   ('growing over time', False),
   ('scarce for only one of the two goods', False)]),
 ('shape',
  None,
  'An economy with specialized resources has been producing only steel and decides to begin producing movies. To '
  'keep its opportunity cost as low as possible, which resources should it shift into movie production first?',
  674,
  [('The resources that are best at producing movies', True),
   ('The resources that are best at producing steel', False),
   ('Any resources, since all resources are the same', False),
   ('All of its resources at once', False),
   ('The resources that are least productive at everything', False)]),
 ('shape',
  'G3',
  'The graph above shows the production possibilities curve for pizzas and tacos. As the economy moves from point '
  'A toward point E, the opportunity cost of each additional taco',
  938,
  [('stays constant at 1 pizza', False),
   ('increases, from 1/2 pizza to 2 pizzas', True),
   ('decreases, from 2 pizzas to 1/2 pizza', False),
   ('increases, then decreases', False),
   ('is zero, because every point on the curve is efficient', False)])]


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

    run("UPDATE question_topic SET name = :new WHERE chapter_id = :c AND name = :old", new=SHAPE[1], old=SHAPE[0], c=chapter_id)
    topics = {'shape': topic(SHAPE[1]), 'calc': topic(CALC)}

    # Move the cherries and apples question, with each student's running totals for it
    moved = [r[0] for r in conn.execute(sa.text(
        "SELECT id FROM question WHERE chapter_id = :c AND topic_id = :t AND text LIKE :s"),
        {'c': chapter_id, 't': topics['shape'], 's': MOVED_TO_CALC + '%'}).all()]
    if moved:
        rows = conn.execute(sa.text(
            "SELECT user_id, count(*), sum(CASE WHEN is_correct THEN 1 ELSE 0 END) FROM user_performance "
            "WHERE question_id = ANY(:q) GROUP BY user_id"), {'q': moved}).all()
        for user_id, asked, correct in rows:
            run("UPDATE user_topic_progress SET questions_asked = GREATEST(questions_asked - :a, 0), "
                "answered_correctly = GREATEST(LEAST(answered_correctly - :r, questions_asked - :a), 0) "
                "WHERE user_id = :u AND topic_id = :t", a=asked, r=correct, u=user_id, t=topics['shape'])
            updated = run("UPDATE user_topic_progress SET questions_asked = questions_asked + :a, "
                          "answered_correctly = answered_correctly + :r WHERE user_id = :u AND topic_id = :t",
                          a=asked, r=correct, u=user_id, t=topics['calc']).rowcount
            if not updated:
                run("INSERT INTO user_topic_progress (user_id, topic_id, questions_asked, answered_correctly) "
                    "VALUES (:u, :t, :a, :r)", u=user_id, t=topics['calc'], a=asked, r=correct)
        run("DELETE FROM user_topic_progress WHERE topic_id = :t AND questions_asked = 0", t=topics['shape'])
        run("UPDATE question SET topic_id = :t WHERE id = ANY(:q)", t=topics['calc'], q=moved)

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
