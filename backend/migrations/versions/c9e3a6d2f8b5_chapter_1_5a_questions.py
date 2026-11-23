"""Chapter 1.5a: output, input and terms of trade subtopics; fifteen new questions; five fixes

Reviewed and approved in the "Chapter 1.5a Question Review" doc (2026-11-23):
  * Topics: Output Questions (was Comparative Advantage Calculations) / Input Questions (new; takes
    Japan and China) / Terms of Trade (new; takes Mark and Donny).
  * Fixes: Japan and China had the wrong answer marked (China's comparative advantage is computers);
    Mark and Donny's choices said "palm leaves" instead of fish and marked a trade at Mark's exact
    opportunity cost (now 1 coconut for 2 fish); Katie/Lucas, Factory A/B and Factory C/D each had a
    second true choice, reworded from "absolute" to "comparative advantage in both".
  * The seven remaining pictures become drawn figures (frontend2 QuestionFigure.jsx).
  * Eight new input questions and seven new terms of trade questions; 1.5a ends at 30.

Matched by chapter name, topic name, question/answer text and picture address (ids differ between
local and live databases); each step is a no-op once applied. Students' per-topic running totals move
with the questions, as in b4c8e1f6a2d9 (chapter 1.1). Past answers keep the grade they were given.

Revision ID: c9e3a6d2f8b5
Revises: b8d1f4a7c2e6
Create Date: 2026-11-23
"""
import json

from alembic import op
import sqlalchemy as sa

revision = 'c9e3a6d2f8b5'
down_revision = 'b8d1f4a7c2e6'
branch_labels = None
depends_on = None

CHAPTER = '1.5a Answering AP and University Level Comparative Advantage Questions'
OUTPUT = ('Comparative Advantage Calculations', 'Output Questions')
INPUT = 'Input Questions'
TERMS = 'Terms of Trade'

JAPAN = 'Japan and China produce both computers and printers'
MARK = 'The table above shows the maximum number of fish or coconuts that Mark and Donny'

# (question start, old answer text, new answer text or None to keep, new is_correct or None to keep)
ANSWER_FIXES = [
    (JAPAN, 'China has a comparative advantage in producing printers.', None, False),
    (JAPAN, 'China has a comparative advantage in producing computers.', None, True),
    (MARK, 'Mark and Donny can both benefit from trade with each other if 1 coconut is traded for 2 palm leaves.',
     'Mark and Donny can both benefit from trade with each other if 1 coconut is traded for 2 fish.', True),
    (MARK, 'Mark and Donny can both benefit from trade with each other if 1 coconut is traded for 3 palm leaves.',
     'Mark and Donny can both benefit from trade with each other if 1 coconut is traded for 3 fish.', False),
    ('Both Katie and Lucas produce chocolate bars and cake slices',
     'Katie has an absolute advantage in producing both chocolate bars and cake slices.',
     'Katie has a comparative advantage in producing both chocolate bars and cake slices.', None),
    ('Both Factory A and Factory B produce computers and smartphones',
     'Factory A has an absolute advantage in producing both computers and smartphones.',
     'Factory A has a comparative advantage in producing both computers and smartphones.', None),
    ('The diagram above shows the production possibilities for Factory C and Factory D',
     'Factory C has an absolute advantage in producing both products.',
     'Factory C has a comparative advantage in producing both products.', None),
]

BASE = 'https://evtds-seeds.s3.us-east-2.amazonaws.com/'
PICTURES = {BASE + k: v for k, v in {'ABMusicMovies.png': 'MUSIC', 'CountryABCoffeeTea.png': 'COFFEE', 'FacCDGoodAB.png': 'FACCD', 'FactoryMNTabletsHeadphones.png': 'FACMN', 'FacXYRollerbladesHelmetsPPF.png': 'FACXY', 'JapanChinaPrinterComputerTable.png': 'JAPAN', 'MarkDonnyFishCoconutsTable.png': 'MARK'}.items()}

FIGURES = {'MUSIC': {'type': 'graph',
           'alt': 'Straight-line production possibilities curves for Country A and Country B, which produce music '
                  '(vertical axis) and movies (horizontal axis). Country A: 80 music or 40 movies. Country B: 80 '
                  'music or 120 movies.',
           'x': {'label': 'Movies', 'max': 140},
           'y': {'label': 'Music', 'max': 100},
           'curves': [{'points': [[0, 80], [40, 0]], 'label': 'A', 'labelAt': [26, 30]},
                      {'points': [[0, 80], [120, 0]], 'label': 'B', 'color': 'supply', 'labelAt': [64, 48]}],
           'xTicks': [[40, '40'], [120, '120']],
           'yTicks': [[80, '80']],
           'origin': '0'},
 'JAPAN': {'type': 'table',
           'columns': ['Country', 'Labor hours per computer', 'Labor hours per printer'],
           'rows': [['Japan', 12, 4], ['China', 6, 4]]},
 'MARK': {'type': 'table',
          'caption': 'Maximum that can be caught or gathered in a day',
          'columns': ['', 'Fish', 'Coconuts'],
          'rows': [['Mark', 12, 4], ['Donny', 6, 4]]},
 'FACXY': {'type': 'panels',
           'alt': 'Two straight-line production possibilities curves for helmets (vertical axis) and rollerblades '
                  '(horizontal axis). Factory X: 40 helmets or 30 rollerblades. Factory Y: 20 helmets or 30 '
                  'rollerblades.',
           'panels': [{'type': 'graph',
                       'caption': 'Factory X',
                       'x': {'label': 'Rollerblades', 'max': 40},
                       'y': {'label': 'Helmets', 'max': 50},
                       'curves': [{'points': [[0, 40], [30, 0]]}],
                       'xTicks': [[30, '30']],
                       'yTicks': [[40, '40']],
                       'origin': '0'},
                      {'type': 'graph',
                       'caption': 'Factory Y',
                       'x': {'label': 'Rollerblades', 'max': 40},
                       'y': {'label': 'Helmets', 'max': 50},
                       'curves': [{'points': [[0, 20], [30, 0]], 'color': 'supply'}],
                       'xTicks': [[30, '30']],
                       'yTicks': [[20, '20']],
                       'origin': '0'}]},
 'FACCD': {'type': 'graph',
           'alt': 'Straight-line production possibilities curves for Factory C and Factory D, which produce Good '
                  'B (vertical axis) and Good A (horizontal axis). Factory C: 30 of Good B or 30 of Good A. '
                  'Factory D: 10 of Good B or 20 of Good A.',
           'x': {'label': 'Good A', 'max': 36},
           'y': {'label': 'Good B', 'max': 36},
           'curves': [{'points': [[0, 30], [30, 0]], 'label': 'Factory C', 'labelAt': [17, 16]},
                      {'points': [[0, 10], [20, 0]], 'label': 'Factory D', 'color': 'supply', 'labelAt': [1, 2]}],
           'xTicks': [[20, '20'], [30, '30']],
           'yTicks': [[10, '10'], [30, '30']],
           'origin': '0'},
 'FACMN': {'type': 'graph',
           'alt': 'Straight-line production possibilities curves for Factory M and Factory N, which produce '
                  'headphones (vertical axis) and tablets (horizontal axis). Factory M: 300 headphones or 300 '
                  'tablets. Factory N: 250 headphones or 50 tablets.',
           'x': {'label': 'Tablets', 'max': 360},
           'y': {'label': 'Headphones', 'max': 360},
           'curves': [{'points': [[0, 300], [300, 0]], 'label': 'Factory M', 'labelAt': [170, 160]},
                      {'points': [[0, 250], [50, 0]],
                       'label': 'Factory N',
                       'color': 'supply',
                       'labelAt': [42, 110]}],
           'xTicks': [[50, '50'], [300, '300']],
           'yTicks': [[250, '250'], [300, '300']],
           'origin': '0'},
 'COFFEE': {'type': 'graph',
            'alt': 'Straight-line production possibilities curves for Country A and Country B, which produce '
                   'coffee (vertical axis) and tea (horizontal axis). Country A: 300 coffee or 150 tea. Country '
                   'B: 200 coffee or 50 tea.',
            'x': {'label': 'Tea', 'max': 180},
            'y': {'label': 'Coffee', 'max': 360},
            'curves': [{'points': [[0, 300], [150, 0]], 'label': 'Country A', 'labelAt': [84, 160]},
                       {'points': [[0, 200], [50, 0]],
                        'label': 'Country B',
                        'color': 'supply',
                        'labelAt': [36, 92]}],
            'xTicks': [[50, '50'], [150, '150']],
            'yTicks': [[200, '200'], [300, '300']],
            'origin': '0'},
 'STEEL': {'type': 'table',
           'caption': 'Hours of labor needed to produce one ton',
           'columns': ['Country', 'Steel', 'Wheat'],
           'rows': [['Country X', 4, 2], ['Country Y', 6, 2]]},
 'WORKERS': {'type': 'table',
             'caption': 'Workers needed for one day to produce one unit',
             'columns': ['Country', 'Cars', 'Computers'],
             'rows': [['Country P', 10, 5], ['Country Q', 12, 4]]},
 'ACRES': {'type': 'table',
           'caption': 'Acres of land needed to grow one ton',
           'columns': ['Farm', 'Corn', 'Soybeans'],
           'rows': [['Farm A', 2, 4], ['Farm B', 3, 3]]},
 'BAKE': {'type': 'table',
          'caption': 'Hours needed to bake one',
          'columns': ['Baker', 'Pie', 'Cake'],
          'rows': [['Lia', 1, 2], ['Max', 3, 4]]}}

# (topic, figure key or None, text, video_start seconds, [(answer, is_correct), ...] in A-E order)
NEW_QUESTIONS = [('input',
  'STEEL',
  'The table above shows the hours of labor Country X and Country Y each need to produce one ton of steel or one '
  'ton of wheat. Which of the following is true?',
  432,
  [('Country Y has an absolute advantage in steel.', False),
   ('Country X has a comparative advantage in steel, and Country Y has a comparative advantage in wheat.', True),
   ('Country X has a comparative advantage in both goods.', False),
   ('Country Y has an absolute advantage in wheat.', False),
   ('Country X has a comparative advantage in wheat.', False)]),
 ('input',
  'STEEL',
  'The table above shows the hours of labor Country X and Country Y each need to produce one ton of steel or one '
  "ton of wheat. What is Country Y's opportunity cost of producing one ton of steel?",
  432,
  [('1/3 ton of wheat', False),
   ('2 tons of wheat', False),
   ('3 tons of wheat', True),
   ('6 tons of wheat', False),
   ('12 tons of wheat', False)]),
 ('input',
  None,
  'It takes Ana 2 hours to bake a cake and 1 hour to bake a loaf of bread. It takes Ben 3 hours to bake a cake '
  'and 2 hours to bake a loaf of bread. Which of the following is true?',
  432,
  [('Ben has an absolute advantage in both goods, because his numbers are larger.', False),
   ('Ana has an absolute advantage in both goods, and Ben has a comparative advantage in cakes.', True),
   ('Ana has a comparative advantage in both goods.', False),
   ('Ben has a comparative advantage in bread.', False),
   ('Ana has an absolute advantage in cakes only.', False)]),
 ('input',
  'WORKERS',
  'The table above shows the number of workers each country needs for one day to produce one car or one computer. '
  "Which of the following correctly identifies each country's comparative advantage?",
  432,
  [('Country P: cars; Country Q: computers', True),
   ('Country P: computers; Country Q: cars', False),
   ('Country P: both goods', False),
   ('Country Q: both goods', False),
   ('Neither country has a comparative advantage.', False)]),
 ('input',
  'ACRES',
  'The table above shows the acres of land each farm needs to grow one ton of corn or one ton of soybeans. Which '
  'of the following is true?',
  432,
  [('Farm A has an absolute advantage in both crops.', False),
   ('Farm B has both the absolute and the comparative advantage in soybeans.', True),
   ('Farm B has a comparative advantage in corn.', False),
   ('Farm A has a comparative advantage in soybeans.', False),
   ('Neither farm has a comparative advantage.', False)]),
 ('input',
  None,
  "It takes Nina 3 hours to build a chair and 2 hours to build a table. What is Nina's opportunity cost of "
  'building one chair?',
  432,
  [('1/3 of a table', False),
   ('2/3 of a table', False),
   ('1.5 tables', True),
   ('3 tables', False),
   ('6 tables', False)]),
 ('input',
  'BAKE',
  'The table above shows the hours Lia and Max each need to bake one pie or one cake. Which of the following are '
  'true?<br><br>I. Lia has an absolute advantage in both goods.<br>II. Max has a comparative advantage in '
  'cakes.<br>III. Lia has a comparative advantage in both goods.',
  432,
  [('I only', False),
   ('II only', False),
   ('I and II only', True),
   ('II and III only', False),
   ('I, II and III', False)]),
 ('input',
  None,
  'A factory in Country R uses 10 gallons of water to make a shirt and 40 gallons to make a pair of jeans. A '
  'factory in Country S uses 15 gallons to make a shirt and 30 gallons to make a pair of jeans. If water is the '
  'only input, according to the theory of comparative advantage, Country R should',
  432,
  [('specialize in shirts and import jeans', True),
   ('specialize in jeans and import shirts', False),
   ('produce both goods and not trade', False),
   ('import both goods from Country S', False),
   ('specialize in jeans, because it uses fewer gallons per pair', False)]),
 ('terms',
  None,
  "Jo's opportunity cost of making one shirt is 2 hats. Kim's opportunity cost of making one shirt is 4 hats. Jo "
  'makes shirts and Kim makes hats. Which of the following trades would benefit both?',
  562,
  [('1 shirt for 1 hat', False),
   ('1 shirt for 2 hats', False),
   ('1 shirt for 3 hats', True),
   ('1 shirt for 4 hats', False),
   ('1 shirt for 5 hats', False)]),
 ('terms',
  None,
  'Two people specialize according to comparative advantage and trade. For the trade to benefit both, the terms '
  'of trade must be',
  562,
  [("between the two people's opportunity costs of producing the good", True),
   ("lower than both people's opportunity costs", False),
   ("higher than both people's opportunity costs", False),
   ('equal to the higher of the two opportunity costs', False),
   ('equal to the market price of the good', False)]),
 ('terms',
  None,
  'In one hour, Rosa can make 6 bracelets or 3 necklaces, and Sam can make 4 bracelets or 4 necklaces. Sam '
  'specializes in necklaces and Rosa specializes in bracelets. Which of the following trades would benefit both?',
  562,
  [('1 necklace for 1/2 bracelet', False),
   ('1 necklace for 1 bracelet', False),
   ('1 necklace for 1.5 bracelets', True),
   ('1 necklace for 2 bracelets', False),
   ('1 necklace for 3 bracelets', False)]),
 ('terms',
  'MUSIC',
  'The graph above shows the production possibilities curves for Country A and Country B, which use equal '
  'resources. Country A specializes in music and Country B in movies. Which of the following terms of trade would '
  'benefit both countries?',
  562,
  [('1 unit of music for 1/4 movie', False),
   ('1 unit of music for 1/2 movie', False),
   ('1 unit of music for 1 movie', True),
   ('1 unit of music for 1.5 movies', False),
   ('1 unit of music for 2 movies', False)]),
 ('terms',
  'COFFEE',
  'The graph above shows the production possibilities curves for Country A and Country B, which use equal '
  'resources. Country A specializes in tea and Country B in coffee. Which of the following terms of trade would '
  'benefit both countries?',
  562,
  [('1 unit of tea for 1 unit of coffee', False),
   ('1 unit of tea for 2 units of coffee', False),
   ('1 unit of tea for 3 units of coffee', True),
   ('1 unit of tea for 4 units of coffee', False),
   ('1 unit of tea for 6 units of coffee', False)]),
 ('terms',
  'STEEL',
  'The table above shows the hours of labor Country X and Country Y each need to produce one ton of steel or one '
  'ton of wheat. Country X specializes in steel and Country Y in wheat. Which of the following terms of trade '
  'would benefit both?',
  562,
  [('1 ton of steel for 1.5 tons of wheat', False),
   ('1 ton of steel for 2 tons of wheat', False),
   ('1 ton of steel for 2.5 tons of wheat', True),
   ('1 ton of steel for 3 tons of wheat', False),
   ('1 ton of steel for 4 tons of wheat', False)]),
 ('terms',
  None,
  "Dexter's opportunity cost of waxing one snowboard base is 2 edge sharpenings. Dexter would be unwilling to wax "
  'a base for TJ in exchange for fewer than 2 edge sharpenings because',
  580,
  [('he could get 2 sharpenings by spending that time sharpening edges himself', True),
   ('TJ has an absolute advantage in waxing', False),
   ('waxing is worth less than sharpening', False),
   ('trade never benefits the side with the absolute advantage', False),
   ('Dexter has a comparative advantage in sharpening edges', False)])]


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

    def find(start, topic_id=None):
        sql = "SELECT id FROM question WHERE chapter_id = :c AND text LIKE :s" + (" AND topic_id = :t" if topic_id else "")
        return [r[0] for r in conn.execute(sa.text(sql), {'c': chapter_id, 's': start + '%', 't': topic_id}).all()]

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
    run("UPDATE question_topic SET name = :new WHERE chapter_id = :c AND name = :old", new=OUTPUT[1], old=OUTPUT[0], c=chapter_id)
    topics = {'output': topic(OUTPUT[1]), 'input': topic(INPUT), 'terms': topic(TERMS)}
    move(find(JAPAN, topics['output']), topics['output'], topics['input'])
    move(find(MARK, topics['output']), topics['output'], topics['terms'])

    # Fixes
    for start, old, new, correct in ANSWER_FIXES:
        qids = find(start)
        if correct is not None:
            run("UPDATE answer SET is_correct = :c WHERE question_id = ANY(:q) AND text = :t", c=correct, q=qids, t=old)
        if new is not None:
            run("UPDATE answer SET text = :new WHERE question_id = ANY(:q) AND text = :old", new=new, old=old, q=qids)

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
