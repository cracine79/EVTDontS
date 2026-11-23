"""Chapter 1.2: two subtopics, eleven new questions, two fixes, two removals

Reviewed and approved in the "Chapter 1.2 Question Review" doc (2026-11-23):
  * Topics become: The Four Factors Defined (was Factors of Production) / Classifying Inputs in
    Real Businesses (new). Seven existing classification questions move to the new one.
  * Removed (not taught in the video): "...which factors of production earns wages?" and
    "The term "human capital" refers to...".
  * Fixes: rented office space is Capital, not Land (the video calls buildings capital); labor is
    "physical and mental effort", not just physical.
  * Three new definition questions and eight new classification questions.

Matched by chapter name, topic name and question/answer text (ids differ between local and live
databases); each step is a no-op once applied. Students' per-topic running totals move with the
questions, as in b4c8e1f6a2d9 (chapter 1.1).

Revision ID: c2d5f8a3b7e4
Revises: b4c8e1f6a2d9
Create Date: 2026-11-23
"""
from alembic import op
import sqlalchemy as sa

revision = 'c2d5f8a3b7e4'
down_revision = 'b4c8e1f6a2d9'
branch_labels = None
depends_on = None

CHAPTER = '1.2 Factors of Production'
DEFINED = ('Factors of Production', 'The Four Factors Defined')
CLASSIFYING = 'Classifying Inputs in Real Businesses'

MOVED = ['A factory building, machinery, and equipment are examples of',
         'When referring to the four factors of production, which of the following would not be referred to as capital',
         'Which of the following is an example of Capital as a factor of production',
         'A businessperson starting a new business would be an example of',
         'The office space rented by a company is an example of',
         'Which of the following is an example of Land as a factor of production',
         'Which of the following is an example of Labor as a factor of production']

REMOVED = ['Which of the following factors of production earns wages',
           'The term "human capital" refers to which factor of production']

OFFICE = 'The office space rented by a company is an example of'
LABOR = 'Which of the following best describes Labor as a factor of production'
LABOR_OLD, LABOR_NEW = 'The physical effort workers provide', 'The physical and mental effort workers provide'

# (topic, text, video_start seconds, [(answer, is_correct), ...]) in A-E order
NEW_QUESTIONS = [
    ('defined', "According to the basic production model, all businesses", 86,
     [('combine inputs through a production process to create output', True),
      ('use only labor and capital to produce goods', False),
      ('produce goods but not services', False),
      ('use the same inputs regardless of what they produce', False),
      ('must be organized by the government', False)]),
    ('defined', "Which of the following best distinguishes capital from land?", 290,
     [('Capital is the money used to start a business; land is the property the business sits on.', False),
      ('Capital is man-made and requires an upfront investment; land is natural and unprocessed.', True),
      ('Capital is owned by firms; land is owned by the government.', False),
      ('Capital includes all human effort; land includes all natural resources.', False),
      ('Capital can be used only once; land can be used again and again.', False)]),
    ('defined', "For a restaurant, which of the following is an output rather than a factor of production?", 125,
     [('The chef who prepares the food', False), ('The stove in the kitchen', False),
      ('Fresh fish caught for the restaurant', False), ('The meals served to customers', True),
      ('The owner who organized the restaurant', False)]),
    ('classifying', "Which of the following inputs used by a bakery is an example of capital?", 290,
     [('The baker who shapes the loaves', False), ('The oven used to bake the bread', True),
      ('The well water used in the dough', False), ("The owner's decision to open a second location", False),
      ("The money in the bakery's checking account", False)]),
    ('classifying', "A pizza shop takes out a $5,000 bank loan and uses it to buy a delivery truck. Which of the "
     "following would be classified as capital for the pizza shop?<br><br>I. The delivery truck<br>"
     "II. The $5,000 loan<br>III. The pizza oven", 296,
     [('I only', False), ('II only', False), ('I and III only', True), ('II and III only', False),
      ('I, II and III', False)]),
    ('classifying', "Which of the following correctly matches an input used by a laundromat with its factor of "
     "production?", 235,
     [('The washing machines — labor', False), ('The water used in the machines — land', True),
      ('The attendant who cleans the machines — capital', False), ('The building — entrepreneurship', False),
      ('The money collected from customers — capital', False)]),
    ('classifying', "A film studio hires a director, rents cameras, and films on location in a national forest. The "
     "project was organized by a producer who risked her own savings on it. In this example, the national forest "
     "is an example of", 235,
     [('land', True), ('labor', False), ('capital', False), ('entrepreneurship', False), ('output', False)]),
    ('classifying', "An oil company uses crude oil pumped from the ground, engineers who operate its refinery, and "
     "the refinery's equipment. These three inputs are, respectively, examples of", 217,
     [('capital, labor, land', False), ('land, labor, capital', True), ('land, capital, labor', False),
      ('land, entrepreneurship, capital', False), ('capital, labor, capital', False)]),
    ('classifying', "The south of France has a climate well suited to growing wine grapes and hundreds of years of "
     "winemaking expertise. Its specialization in wine is best explained by", 419,
     [('the land and labor available in the region', True),
      ("the region's lower cost of borrowing money", False),
      ('government orders requiring farmers to grow grapes', False),
      ('a lack of other natural resources in France', False),
      ('consumers in the region preferring wine to other goods', False)]),
    ('classifying', "Tech startups are concentrated in Silicon Valley mainly because", 450,
     [('the factors of production they need, such as skilled programmers and computer equipment, are '
       'concentrated there', True),
      ('the government requires technology firms to locate there', False),
      ('land in Silicon Valley is less expensive than elsewhere', False),
      ('technology firms do not require labor', False),
      ('entrepreneurship is not needed in other regions', False)]),
    ('classifying', "A restaurant's head chef creates new dishes for the menu and cooks during dinner service. The "
     "restaurant is owned by an investor who organized the business. The head chef's work is an example of", 273,
     [('land', False), ('labor', True), ('capital', False), ('entrepreneurship', False), ('output', False)]),
]


def upgrade():
    conn = op.get_bind()
    one = lambda sql, **kw: conn.execute(sa.text(sql), kw).scalar()
    run = lambda sql, **kw: conn.execute(sa.text(sql), kw)

    chapter_id = one("SELECT id FROM chapter WHERE name = :n", n=CHAPTER)
    if chapter_id is None:
        return

    def topic(name):
        return one("SELECT id FROM question_topic WHERE chapter_id = :c AND name = :n", c=chapter_id, n=name)

    def question_ids(starts, topic_id=None):
        ids = []
        for start in starts:
            sql = "SELECT id FROM question WHERE chapter_id = :c AND text LIKE :s"
            if topic_id is not None:
                sql += " AND topic_id = :t"
            ids += [r[0] for r in conn.execute(sa.text(sql), {'c': chapter_id, 's': start + '%', 't': topic_id}).all()]
        return ids

    def shift_progress(qids, from_topic, to_topic=None):
        """Move each student's answers to these questions from one topic's running totals to another's
        (or just take them off when to_topic is None)."""
        if not qids:
            return
        rows = conn.execute(sa.text(
            "SELECT user_id, count(*), sum(CASE WHEN is_correct THEN 1 ELSE 0 END) FROM user_performance "
            "WHERE question_id = ANY(:q) GROUP BY user_id"), {'q': list(qids)}).all()
        for user_id, asked, correct in rows:
            run("UPDATE user_topic_progress SET questions_asked = GREATEST(questions_asked - :a, 0), "
                "answered_correctly = GREATEST(LEAST(answered_correctly - :r, questions_asked - :a), 0) "
                "WHERE user_id = :u AND topic_id = :t", a=asked, r=correct, u=user_id, t=from_topic)
            if to_topic is not None:
                updated = run("UPDATE user_topic_progress SET questions_asked = questions_asked + :a, "
                              "answered_correctly = answered_correctly + :r WHERE user_id = :u AND topic_id = :t",
                              a=asked, r=correct, u=user_id, t=to_topic).rowcount
                if not updated:
                    run("INSERT INTO user_topic_progress (user_id, topic_id, questions_asked, answered_correctly) "
                        "VALUES (:u, :t, :a, :r)", u=user_id, t=to_topic, a=asked, r=correct)
        run("DELETE FROM user_topic_progress WHERE topic_id = :t AND questions_asked = 0", t=from_topic)

    # Topics
    run("UPDATE question_topic SET name = :new WHERE chapter_id = :c AND name = :old",
        new=DEFINED[1], old=DEFINED[0], c=chapter_id)
    defined_id = topic(DEFINED[1])
    classifying_id = topic(CLASSIFYING)
    if classifying_id is None:
        classifying_id = one("INSERT INTO question_topic (name, chapter_id) VALUES (:n, :c) RETURNING id",
                             n=CLASSIFYING, c=chapter_id)

    # Move the classification questions (only those still under Defined)
    moved_ids = question_ids(MOVED, defined_id)
    shift_progress(moved_ids, defined_id, classifying_id)
    if moved_ids:
        run("UPDATE question SET topic_id = :t WHERE id = ANY(:q)", t=classifying_id, q=moved_ids)

    # Remove the two questions the video doesn't teach
    removed_ids = question_ids(REMOVED)
    shift_progress(removed_ids, defined_id)
    if removed_ids:
        run("DELETE FROM user_performance WHERE question_id = ANY(:q)", q=removed_ids)
        run("DELETE FROM answer WHERE question_id = ANY(:q)", q=removed_ids)
        run("DELETE FROM question WHERE id = ANY(:q)", q=removed_ids)

    # Fixes
    run("UPDATE answer SET is_correct = (text = 'Capital') WHERE question_id = ANY(:q) AND text IN ('Capital', 'Land')",
        q=question_ids([OFFICE]))
    run("UPDATE answer SET text = :new WHERE question_id = ANY(:q) AND text = :old",
        q=question_ids([LABOR]), old=LABOR_OLD, new=LABOR_NEW)

    # New questions (skipped if already there)
    topics = {'defined': defined_id, 'classifying': classifying_id}
    for which, text, start, answers in NEW_QUESTIONS:
        if one("SELECT count(*) FROM question WHERE chapter_id = :c AND text = :t", c=chapter_id, t=text):
            continue
        qid = one("INSERT INTO question (text, chapter_id, topic_id, video_start) VALUES (:t, :c, :tp, :v) RETURNING id",
                  t=text, c=chapter_id, tp=topics[which], v=start)
        for answer, correct in answers:
            run("INSERT INTO answer (text, question_id, is_correct) VALUES (:t, :q, :c)", t=answer, q=qid, c=correct)


def downgrade():
    # Not reversible: two questions and students' answers to them were deleted. Restore from a backup
    # if this ever needs undoing.
    pass
