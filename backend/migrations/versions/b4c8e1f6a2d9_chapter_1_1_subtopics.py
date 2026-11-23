"""Chapter 1.1: three subtopics, six new opportunity cost calculation questions, two fixes

Reviewed and approved in the "Chapter 1.1 Question Review" doc (2026-11-23):
  * Topics become: Scarcity, Choice and Trade-offs (was Scarcity) / Identifying Opportunity Cost
    (was Opportunity Cost) / Calculating Opportunity Cost (new). The Sarah, Jeff and Mary questions
    move to the new one.
  * The "If you see a question about the fundamental/primary question..." question is removed.
  * Mary's question had the wrong answer marked: 90 minutes = 3 math assignments, not 1/3.
  * Six new AP-style calculation questions.

Everything is matched by chapter name, topic name and question/answer text (ids differ between
local and live databases), and each step is a no-op once applied.

Students' per-topic running totals (user_topic_progress) move with the questions: each student's
answers to the three moved questions shift from the old topic's totals to the new topic's, and their
answers to the removed question come off. Mastery is computed from user_performance, so it follows
the questions automatically. Past answers to Mary's question keep the grade they were given.

Revision ID: b4c8e1f6a2d9
Revises: a9d4e2b7c1f3
Create Date: 2026-11-23
"""
from alembic import op
import sqlalchemy as sa

revision = 'b4c8e1f6a2d9'
down_revision = 'a9d4e2b7c1f3'
branch_labels = None
depends_on = None

CHAPTER = '1.1 Scarcity, Choice and Opportunity Cost'
SCARCITY = ('Scarcity', 'Scarcity, Choice and Trade-offs')
IDENTIFYING = ('Opportunity Cost', 'Identifying Opportunity Cost')
CALCULATING = 'Calculating Opportunity Cost'

# Questions that move to Calculating Opportunity Cost (matched by the start of their text)
MOVED = ['Sarah has two free hours this evening.',
         'Jeff works part time at a local gas station',
         'It takes Mary 30 minutes to complete a math homework assignment']

REMOVED = 'If you see a question about the fundamental/primary question of economics'

MARY = 'It takes Mary 30 minutes to complete a math homework assignment'
MARY_WRONG = 'Completing 1/3 of a math homework assignment'
MARY_RIGHT = 'Completing 3 math homework assignments'

# (text, video_start seconds, [(answer, is_correct), ...]) in A-E order
NEW_QUESTIONS = [
    ("Dana is given a free ticket to a basketball game. The ticket's face value is $75. To attend the game, Dana "
     "gives up a 4-hour shift at her job, where she earns $14 an hour; working is her next best alternative. "
     "What is Dana's opportunity cost of attending the game?", 478,
     [('$0', False), ('$14', False), ('$56', True), ('$75', False), ('$131', False)]),
    ("Alex has a free Saturday afternoon and three options: work an overtime shift that pays $90, help a friend "
     "move, which he values at $40, or attend a free outdoor concert, which he values at $120. Alex chooses the "
     "concert. What is Alex's opportunity cost of attending the concert?", 408,
     [('$0', False), ('$30', False), ('$90', True), ('$120', False), ('$130', False)]),
    ("After high school, Jordan can either attend college for four years, paying $25,000 per year in tuition, or "
     "take a full-time job that pays $30,000 per year. Jordan chooses college. What is Jordan's total opportunity "
     "cost of the four years of college?", 456,
     [('$30,000', False), ('$55,000', False), ('$100,000', False), ('$120,000', False), ('$220,000', True)]),
    ("It takes Kendra 2 hours to write an English essay and 20 minutes to complete a chemistry lab report. "
     "Assuming Kendra spends her time on only these two activities, what is the opportunity cost to Kendra of "
     "writing one English essay?", 531,
     [('1/6 of a lab report', False), ('2 lab reports', False), ('6 lab reports', True), ('20 lab reports', False),
      ('It cannot be determined without knowing the grade she earns on each', False)]),
    ("Priya spends 3 hours at an amusement park, paying a $50 admission fee. Her other options were babysitting "
     "for 3 hours at $12 an hour, or mowing a neighbor's lawn for $25, which she ranked below babysitting. Which "
     "of the following are included in Priya's opportunity cost of going to the amusement park?<br><br>"
     "I. The $50 admission fee<br>II. The $36 she could have earned babysitting<br>"
     "III. The $25 she could have earned mowing the lawn", 478,
     [('I only', False), ('II only', False), ('I and II only', True), ('II and III only', False),
      ('I, II and III', False)]),
    ("Ben and Chloe each take the same 3-hour cooking class, which costs $45. If they hadn't taken the class, Ben "
     "would have worked at a job paying $10 an hour and Chloe would have worked at a job paying $20 an hour. "
     "Which of the following correctly states their opportunity costs of taking the class?", 478,
     [('Ben: $45, Chloe: $45', False), ('Ben: $30, Chloe: $60', False), ('Ben: $75, Chloe: $105', True),
      ('Ben: $105, Chloe: $75', False), ('Ben: $75, Chloe: $60', False)]),
]


def upgrade():
    conn = op.get_bind()
    one = lambda sql, **kw: conn.execute(sa.text(sql), kw).scalar()
    run = lambda sql, **kw: conn.execute(sa.text(sql), kw)

    chapter_id = one("SELECT id FROM chapter WHERE name = :n", n=CHAPTER)
    if chapter_id is None:
        return  # database without this chapter (e.g. an empty one): nothing to do

    def topic(name):
        return one("SELECT id FROM question_topic WHERE chapter_id = :c AND name = :n", c=chapter_id, n=name)

    # Topics: rename the two existing ones, add the new one
    for old, new in (SCARCITY, IDENTIFYING):
        run("UPDATE question_topic SET name = :new WHERE chapter_id = :c AND name = :old", new=new, old=old, c=chapter_id)
    scarcity_id, identifying_id = topic(SCARCITY[1]), topic(IDENTIFYING[1])
    calculating_id = topic(CALCULATING)
    if calculating_id is None:
        calculating_id = one("INSERT INTO question_topic (name, chapter_id) VALUES (:n, :c) RETURNING id",
                             n=CALCULATING, c=chapter_id)

    def shift_progress(question_ids, from_topic, to_topic=None):
        """Move each student's answers to these questions from one topic's running totals to another's
        (or just take them off when to_topic is None)."""
        if not question_ids:
            return
        rows = conn.execute(sa.text(
            "SELECT user_id, count(*), sum(CASE WHEN is_correct THEN 1 ELSE 0 END) FROM user_performance "
            "WHERE question_id = ANY(:q) GROUP BY user_id"), {'q': list(question_ids)}).all()
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

    # Move the three calculation questions (only those still under Identifying)
    moved_ids = []
    for start in MOVED:
        moved_ids += [r[0] for r in conn.execute(sa.text(
            "SELECT id FROM question WHERE chapter_id = :c AND topic_id = :t AND text LIKE :s"),
            {'c': chapter_id, 't': identifying_id, 's': start + '%'}).all()]
    shift_progress(moved_ids, identifying_id, calculating_id)
    if moved_ids:
        run("UPDATE question SET topic_id = :t WHERE id = ANY(:q)", t=calculating_id, q=moved_ids)

    # Remove the study-tip question, with its answers and students' answers to it
    removed_ids = [r[0] for r in conn.execute(sa.text(
        "SELECT id FROM question WHERE chapter_id = :c AND text LIKE :s"), {'c': chapter_id, 's': REMOVED + '%'}).all()]
    shift_progress(removed_ids, scarcity_id)
    if removed_ids:
        run("DELETE FROM user_performance WHERE question_id = ANY(:q)", q=removed_ids)
        run("DELETE FROM answer WHERE question_id = ANY(:q)", q=removed_ids)
        run("DELETE FROM question WHERE id = ANY(:q)", q=removed_ids)

    # Mary: mark 3 assignments correct, 1/3 wrong
    mary = "SELECT id FROM question WHERE chapter_id = :c AND text LIKE :s"
    run("UPDATE answer SET is_correct = (text = :right) WHERE question_id IN (" + mary + ") AND text IN (:right, :wrong)",
        c=chapter_id, s=MARY + '%', right=MARY_RIGHT, wrong=MARY_WRONG)

    # New questions (skipped if already there)
    for text, start, answers in NEW_QUESTIONS:
        if one("SELECT count(*) FROM question WHERE chapter_id = :c AND text = :t", c=chapter_id, t=text):
            continue
        qid = one("INSERT INTO question (text, chapter_id, topic_id, video_start) VALUES (:t, :c, :tp, :v) RETURNING id",
                  t=text, c=chapter_id, tp=calculating_id, v=start)
        for answer, correct in answers:
            run("INSERT INTO answer (text, question_id, is_correct) VALUES (:t, :q, :c)", t=answer, q=qid, c=correct)


def downgrade():
    # Not reversible: a question and students' answers to it were deleted, and new questions may
    # already have answers from students. Restore from a backup if this ever needs undoing.
    pass
