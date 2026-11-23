"""Chapter 1.3: three subtopics and thirteen new questions

Reviewed and approved in the "Chapter 1.3 Question Review" doc (2026-11-23):
  * Topics become: The Three Economic Questions (new) / Command vs Market Systems (was Economic
    Systems) / Mixed Economies and the Spectrum (new). The mixed economy definition and property
    rights questions move to Mixed Economies.
  * Six new questions on the three economic questions, seven on mixed economies. No fixes needed.

Matched by chapter name, topic name and question text (ids differ between local and live
databases); each step is a no-op once applied. Students' per-topic running totals move with the
questions, as in b4c8e1f6a2d9 (chapter 1.1).

Revision ID: d7a3c9e2f5b1
Revises: c2d5f8a3b7e4
Create Date: 2026-11-23
"""
from alembic import op
import sqlalchemy as sa

revision = 'd7a3c9e2f5b1'
down_revision = 'c2d5f8a3b7e4'
branch_labels = None
depends_on = None

CHAPTER = '1.3 Economic Systems'
COMMAND_MARKET = ('Economic Systems', 'Command vs Market Systems')
THREE_QUESTIONS = 'The Three Economic Questions'
MIXED = 'Mixed Economies and the Spectrum'

MOVED_TO_MIXED = ['Which economic system is characterized by a combination of government intervention and market forces',
                  'Which of the following is a key requirement for a market/capitalist economy']

# (topic, text, video_start seconds, [(answer, is_correct), ...]) in A-E order
NEW_QUESTIONS = [
    ('three', "The three basic economic questions that every economic system must answer are", 50,
     [('what to produce, how much to charge, and who should pay taxes', False),
      ('what to produce, how to produce it, and for whom to produce it', True),
      ('how much to save, how much to invest, and how much to consume', False),
      ('who owns resources, who sets prices, and who collects taxes', False),
      ('what to import, what to export, and what to tax', False)]),
    ('three', "A farmer decides to plant corn rather than wheat on his land this year. Which basic economic question "
     "does this decision answer?", 50,
     [('What to produce', True), ('How to produce', False), ('For whom to produce', False),
      ('How much to charge', False), ('Whether to trade', False)]),
    ('three', "A clothing company replaces its sewing workers with automated sewing machines. This decision "
     "primarily answers which basic economic question?", 50,
     [('What to produce', False), ('How to produce', True), ('For whom to produce', False),
      ('How much to produce', False), ('Who owns the factors of production', False)]),
    ('three', "In a command economy, the government issues ration tickets that determine how much rice each "
     "household may receive. The ration system answers which basic economic question?", 148,
     [('What to produce', False), ('How to produce', False), ('For whom to produce', True),
      ('How to set the price of rice', False), ('Who owns the land used to grow rice', False)]),
    ('three', "Which of the following is true about the three basic economic questions?", 101,
     [('Only market economies must answer them.', False),
      ('Only command economies must answer them.', False),
      ('Every economy must answer them, and its economic system determines how they are answered.', True),
      ('Consumers alone answer them in every economic system.', False),
      ('Wealthy economies no longer need to answer them.', False)]),
    ('three', "Which of the following decisions answer the question of how goods are produced?<br><br>"
     "I. A bakery switches from kneading dough by hand to using electric mixers<br>"
     "II. A government orders a factory to make tractors instead of cars<br>"
     "III. A carmaker moves production to a plant that uses more robots", 50,
     [('I only', False), ('II only', False), ('I and III only', True), ('II and III only', False),
      ('I, II and III', False)]),
    ('mixed', "In a mixed economy,", 406,
     [('the government owns all resources but allows prices to be set by supply and demand', False),
      ('some economic decisions are made through markets and others by a central authority', True),
      ("firms decide what to produce, but consumers' purchases are rationed", False),
      ('economic decisions are made by tradition and custom', False),
      ('there is no government involvement in economic activity', False)]),
    ('mixed', "Which of the following best explains why there are no pure market economies?", 373,
     [('Some services, such as police protection and roads, are not provided well by private markets alone.', True),
      ('Market economies cannot use prices to allocate goods.', False),
      ('Consumers prefer rationing to paying market prices.', False),
      ('Private ownership of resources is illegal in most countries.', False),
      ('Firms in market economies do not try to earn profits.', False)]),
    ('mixed', "An economy engages in free and open trade, has relatively flexible labor regulations, and makes it "
     "relatively easy to open and operate a business. This economy is best described as", 484,
     [('a pure market economy', False), ('a mixed economy close to the market end of the spectrum', True),
      ('a mixed economy close to the command end of the spectrum', False), ('a pure command economy', False),
      ('a traditional economy', False)]),
    ('mixed', "Even in North Korea, one of the most centrally planned economies in the world, some citizens buy food "
     "and other necessities in informal markets. This best illustrates that", 478,
     [('North Korea is a pure market economy', False), ('command economies eliminate scarcity', False),
      ("rationing always provides for everyone's needs", False),
      ('even economies close to the command end of the spectrum include some market activity', True),
      ('informal markets are a form of central planning', False)]),
    ('mixed', "In the mixed economy of the United States, which of the following are determined mainly by a central "
     "authority?<br><br>I. The minimum wage employers may pay<br>II. The price of video game consoles<br>"
     "III. Free K–12 public education", 426,
     [('I only', False), ('II only', False), ('I and III only', True), ('II and III only', False),
      ('I, II and III', False)]),
    ('mixed', "A government that moves its economy toward the command end of the spectrum would most likely", 457,
     [('set production quotas for more industries', True), ('remove the minimum wage', False),
      ('sell government-owned businesses to private individuals', False),
      ('let supply and demand set more prices', False), ('strengthen private property rights', False)]),
    ('mixed', "Which of the following statements about economic systems is true?", 406,
     [('The United States is a pure market economy.', False),
      ('Command economies have no market activity of any kind.', False),
      ('All economies are mixed economies, falling somewhere between command and market.', True),
      ('Mixed economies have no government involvement.', False),
      ('Switzerland is a pure market economy.', False)]),
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

    def shift_progress(qids, from_topic, to_topic):
        """Move each student's answers to these questions from one topic's running totals to another's."""
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

    # Topics (the new ones are created in video order: three questions first, mixed last)
    run("UPDATE question_topic SET name = :new WHERE chapter_id = :c AND name = :old",
        new=COMMAND_MARKET[1], old=COMMAND_MARKET[0], c=chapter_id)
    command_market_id = topic(COMMAND_MARKET[1])
    three_id = topic(THREE_QUESTIONS)
    mixed_id = topic(MIXED)

    # Move the two mixed economy questions (only those still under Command vs Market)
    moved_ids = []
    for start in MOVED_TO_MIXED:
        moved_ids += [r[0] for r in conn.execute(sa.text(
            "SELECT id FROM question WHERE chapter_id = :c AND topic_id = :t AND text LIKE :s"),
            {'c': chapter_id, 't': command_market_id, 's': start + '%'}).all()]
    shift_progress(moved_ids, command_market_id, mixed_id)
    if moved_ids:
        run("UPDATE question SET topic_id = :t WHERE id = ANY(:q)", t=mixed_id, q=moved_ids)

    # New questions (skipped if already there)
    topics = {'three': three_id, 'mixed': mixed_id}
    for which, text, start, answers in NEW_QUESTIONS:
        if one("SELECT count(*) FROM question WHERE chapter_id = :c AND text = :t", c=chapter_id, t=text):
            continue
        qid = one("INSERT INTO question (text, chapter_id, topic_id, video_start) VALUES (:t, :c, :tp, :v) RETURNING id",
                  t=text, c=chapter_id, tp=topics[which], v=start)
        for answer, correct in answers:
            run("INSERT INTO answer (text, question_id, is_correct) VALUES (:t, :q, :c)", t=answer, q=qid, c=correct)


def downgrade():
    # Not reversible once students have answered the new questions; restore from a backup if needed.
    pass
