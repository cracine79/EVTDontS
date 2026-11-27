"""Chapter 3.2: sixteen new questions, two subtopics, one fix

Reviewed and approved in the "Chapter 3.2 Question Review" doc (2026-11-26):
  * "PED determinants" becomes "Necessity and Proportion of Budget"; the two substitutes questions move to a new
    "Substitutes and Time Period" topic, with student progress.
  * Fix 1: "Why would the price elasticity of demand for a good decrease?" gets its answers rewritten in place so
    the correct one is about budget share, and its rewatch time moves to 4:43 (proportion of budget).
  * New: five necessity/budget questions and eleven substitutes/time period questions.

Matched by chapter name, topic name and question/answer text (ids differ between local and live databases);
each step is a no-op once applied.

Revision ID: a4c8e2f6b1d9
Revises: f1b5d9c3a7e8
Create Date: 2026-11-26
"""
from alembic import op
import sqlalchemy as sa

revision = 'a4c8e2f6b1d9'
down_revision = 'f1b5d9c3a7e8'
branch_labels = None
depends_on = None

CHAPTER = '3.2 Determinants of Price Elasticity of Demand'
BUDGET = ('PED determinants', 'Necessity and Proportion of Budget')
SUBST = 'Substitutes and Time Period'

# questions that move to SUBST, by the start of their text
MOVED_TO_SUBST = ['What may be one reason that Figlebaums face',
                  'Which of the following will make the demand for a product more elastic?']

# Fix 1: answers in id order, before and after
FIX1 = 'Why would the price elasticity of demand for a good decrease?'
FIX1_OLD = ['The good becomes less of a necessity.', 'The good has more substitutes available.',
            'The good becomes more necessary.', 'The good’s price becomes a larger proportion of income.',
            'The good becomes more of a luxury.']
FIX1_NEW = [('The good becomes less of a necessity.', False), ('The good has more substitutes available.', False),
            ("The good's price becomes a smaller proportion of consumers' incomes.", True),
            ("The good's price becomes a larger proportion of consumers' incomes.", False),
            ('The good becomes more of a luxury.', False)]
FIX1_START = 283

GAS = 'The price elasticity of demand coefficient for gasoline is 0.2 in the short run and 0.7 in the long run. '

# (topic, text, video_start seconds, [(answer, is_correct), ...]) in A-E order
NEW_QUESTIONS = [
    ('budget', 'Studies estimate the price elasticity of demand coefficient for gasoline at 0.2 and for restaurant '
               'meals at greater than 1. Which of the following best explains the difference?', 124,
     [('Gasoline has more close substitutes than restaurant meals.', False),
      ("Restaurant meals take up a smaller proportion of consumers' budgets than gasoline.", False),
      ('Gasoline is a necessity for car owners, while restaurant meals are more of a luxury.', True),
      ('Consumers have more time to adjust to changes in the price of gasoline.', False),
      ('Restaurant meals are a necessity, while gasoline is a luxury.', False)]),
    ('budget', 'Over a certain range of prices, demand for insulin is perfectly inelastic. If the price of insulin '
               'increases by 10 percent, the quantity of insulin demanded will', 182,
     [('decrease by more than 10 percent', False), ('decrease by exactly 10 percent', False),
      ('decrease by less than 10 percent', False), ('not change', True), ('increase by 10 percent', False)]),
    ('budget', 'Toothpicks have a low degree of necessity, yet demand for toothpicks is price inelastic. Which of the '
               'following best explains this?', 226,
     [('Toothpicks have many close substitutes.', False),
      ("Toothpicks take up a very small proportion of consumers' budgets.", True),
      ('Consumers have a long period of time to adjust to price changes.', False),
      ('Toothpicks are a luxury good.', False),
      ("Toothpicks take up a large proportion of consumers' budgets.", False)]),
    ('budget', 'An investment banker earns $600,000 a year and a service worker earns $30,000 a year. The price of a '
               'wedding ring doubles from $2,000 to $4,000. Which of the following is most likely true?', 314,
     [("The banker's demand for the ring is more elastic, because the banker has more income to spend.", False),
      ('Both have the same price elasticity of demand, because the price change is the same for both.', False),
      ("The banker's demand for the ring is more elastic, because the ring is a luxury for the banker.", False),
      ("The service worker's demand for the ring is more elastic, because the ring takes up a larger proportion of "
       "the service worker's income.", True),
      ("The service worker's demand for the ring is more inelastic, because the ring takes up a larger proportion "
       "of the service worker's income.", False)]),
    ('budget', 'Which of the following would make demand for a good more inelastic?<br><br>I. The good becomes more '
               "of a necessity<br>II. The good takes up a smaller proportion of consumers' budgets<br>III. More close "
               'substitutes for the good become available', 525,
     [('I only', False), ('III only', False), ('I and II only', True), ('II and III only', False),
      ('I, II and III', False)]),

    ('subst', 'Demand for fresh tomatoes is highly price elastic. Which of the following best explains this?', 358,
     [("Fresh tomatoes take up a large proportion of consumers' budgets.", False),
      ('Fresh tomatoes are a necessity.', False),
      ('Shoppers can easily switch to canned tomatoes, a close substitute.', True),
      ('Shoppers have no other way to make tomato sauce.', False),
      ('Shoppers cannot change their buying habits in the short run.', False)]),
    ('subst', 'When Chevrolet raises the price of its cars by 10 percent, the quantity of Chevrolets demanded falls by '
              '25 percent. Which of the following best explains this response?', 424,
     [('Cars are a necessity for most consumers.', False),
      ('Consumers can buy close substitutes from Ford, Jeep, Tesla and Toyota.', True),
      ("Cars take up a small proportion of consumers' budgets.", False),
      ('Chevrolet is the only firm that sells cars.', False),
      ('The price increase caused the demand curve for Chevrolets to shift left.', False)]),
    ('subst', "A firm is the only seller of a product, and the product has no close substitutes. Demand for the "
              "firm's product is most likely", 556,
     [('perfectly elastic, because consumers will buy any quantity at one price', False),
      ('relatively elastic, because consumers can switch to other sellers', False),
      ('unit elastic, because the firm sets the price', False),
      ('relatively inelastic, because consumers have few alternatives if the price rises', True),
      ('relatively elastic, because the firm has no competitors', False)]),
    ('subst', 'Two brands of a product are close substitutes. If one brand stops selling its product, demand for the '
              'remaining brand will most likely become', 435,
     [('more inelastic, because consumers have fewer close substitutes to switch to', True),
      ('more elastic, because consumers have fewer close substitutes to switch to', False),
      ('more elastic, because the remaining brand becomes more of a luxury', False),
      ('perfectly elastic, because only one brand is sold', False),
      ('unchanged, because the number of substitutes does not affect elasticity', False)]),
    ('subst', 'Good X has a price elasticity of demand coefficient of 3.0, and good Y has a coefficient of 0.3. Which '
              'of the following is one possible explanation for this?', 402,
     [('Good X has fewer close substitutes than good Y.', False),
      ('Good X has a higher degree of necessity than good Y.', False),
      ('Good X has many close substitutes, while good Y has few.', True),
      ("Good X takes up a smaller proportion of consumers' budgets than good Y.", False),
      ("Good Y's coefficient was measured over a longer period of time than good X's.", False)]),
    ('subst', 'Which of the following would most likely face the most price elastic demand?', 392,
     [('Insulin for a person with diabetes', False), ('Gasoline in the week after a price increase', False),
      ('Toothpicks', False), ('Physician services', False),
      ('Fresh tomatoes in a supermarket that also sells canned tomatoes', True)]),
    ('subst', GAS + 'Which of the following best explains why demand is more elastic in the long run?', 494,
     [('Gasoline becomes more of a necessity over time.', False),
      ("Gasoline takes up a smaller proportion of consumers' budgets in the long run.", False),
      ('Over time, consumers can change their habits, such as riding the bus, biking or carpooling.', True),
      ('Fewer substitutes for gasoline are available in the long run.', False),
      ('Consumers become used to the higher price and stop reacting to it.', False)]),
    ('subst', GAS + 'If the price of gasoline rises by 20 percent and stays high, by how much will the quantity of '
                    'gasoline demanded fall in the short run and in the long run?', 445,
     [('4 percent in the short run, 14 percent in the long run', True),
      ('14 percent in the short run, 4 percent in the long run', False),
      ('0.2 percent in the short run, 0.7 percent in the long run', False),
      ('20 percent in both the short run and the long run', False),
      ('100 percent in the short run, about 29 percent in the long run', False)]),
    ('subst', 'A driver pulls into a gas station with an almost empty tank and sees that the price of gasoline has '
              'doubled. Which of the following is most likely?', 469,
     [('The driver buys no gasoline today, because demand for gasoline is elastic in the short run.', False),
      ('The driver still buys gasoline today, but if the price stays high, the driver may later carpool or take the '
       'bus.', True),
      ('The driver buys the same amount of gasoline today and forever, because gasoline has perfectly inelastic '
       'demand.', False),
      ('The driver buys more gasoline today, because the price is higher.', False),
      ("The driver's demand for gasoline becomes more inelastic as time passes.", False)]),
    ('subst', 'The price of a good rises and stays high. As more time passes after the price increase, demand for the '
              'good will most likely become', 598,
     [('more inelastic, because consumers get used to the higher price', False),
      ('more inelastic, because the good becomes more of a necessity', False),
      ('more elastic, because consumers have more opportunity to change their consumption habits', True),
      ("more elastic, because the good takes up a smaller proportion of consumers' budgets", False),
      ('perfectly inelastic, because the price no longer changes', False)]),
    ('subst', 'Which of the following would make demand for a good more elastic?<br><br>I. More close substitutes for '
              'the good become available<br>II. A longer period of time passes after a price change<br>III. The good '
              'becomes more of a necessity', 525,
     [('I only', False), ('II only', False), ('III only', False), ('I and II only', True),
      ('I, II and III', False)]),
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
        new=BUDGET[1], old=BUDGET[0], c=chapter_id)
    topics = {'budget': topic(BUDGET[1]), 'subst': topic(SUBST)}

    # Move the substitutes questions
    for phrase in MOVED_TO_SUBST:
        move(find(phrase, topics['budget']), topics['budget'], topics['subst'])

    # Fix 1: rewrite by id order, only while the answers are still the old ones
    qid = one("SELECT id FROM question WHERE chapter_id = :c AND text = :t", c=chapter_id, t=FIX1)
    if qid is not None:
        rows = conn.execute(sa.text("SELECT id, text FROM answer WHERE question_id = :q ORDER BY id"), {'q': qid}).all()
        if [r[1] for r in rows] == FIX1_OLD:
            for (aid, _), (text, correct) in zip(rows, FIX1_NEW):
                run("UPDATE answer SET text = :t, is_correct = :k WHERE id = :a", t=text, k=correct, a=aid)
            run("UPDATE question SET video_start = :v WHERE id = :q", v=FIX1_START, q=qid)

    # New questions (skipped if already there)
    for which, text, start, answers in NEW_QUESTIONS:
        if one("SELECT count(*) FROM question WHERE chapter_id = :c AND text = :t", c=chapter_id, t=text):
            continue
        qid = one("INSERT INTO question (text, chapter_id, topic_id, video_start) "
                  "VALUES (:t, :c, :tp, :v) RETURNING id", t=text, c=chapter_id, tp=topics[which], v=start)
        for answer, correct in answers:
            run("INSERT INTO answer (text, question_id, is_correct) VALUES (:t, :q, :c)", t=answer, q=qid, c=correct)


def downgrade():
    # Not reversible once students have answered the new questions; restore from a backup if needed.
    pass
