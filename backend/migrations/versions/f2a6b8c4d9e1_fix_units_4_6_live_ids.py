"""Apply the question fixes and rewatch times to units 4-6 on the live database

The live database numbers the unit 4-6 chapters, questions and answers differently from local
development, so d5a1c7e9f2b4 and e8c3d1f5a7b2 (written against local ids) skipped them there.
These are the same fixes, keyed to the live ids. Every change is guarded by the row's current
text/value, so it is a no-op anywhere the fix is already in place (e.g. local databases).

Revision ID: f2a6b8c4d9e1
Revises: e8c3d1f5a7b2
Create Date: 2026-11-22
"""
from alembic import op
import sqlalchemy as sa

revision = 'f2a6b8c4d9e1'
down_revision = 'e8c3d1f5a7b2'
branch_labels = None
depends_on = None

# (question_id, old_text, new_text)
QUESTION_TEXT = [(333,
  'Assume that supply for a good is upward sloping and demand is downward sloping.  The imposition of a specific exise tax on the sale of that good '
  'would result in which of the following changes to equilibrium price and quantity?',
  'Assume that supply for a good is upward sloping and demand is downward sloping.  The imposition of a specific excise tax on the sale of that good '
  'would result in which of the following changes to equilibrium price and quantity?'),
 (336,
  'Assume that the government increases the unit exise tax on alcohol suppliers and also at the same time, the demand for alcohol increases due to '
  'increases in stress levels at work.   As a result, equilibrium price and quantity of alcohol will most likely change in which of the following '
  'ways?',
  'Assume that the government increases the unit excise tax on alcohol suppliers and also at the same time, the demand for alcohol increases due to '
  'increases in stress levels at work.   As a result, equilibrium price and quantity of alcohol will most likely change in which of the following '
  'ways?'),
 (340,
  'Assume that price elasticity of demand for good A is -0.3 and price elasticity of demand for good B is -2.5.  Assume goods A and B have identical '
  'demand curves.  If a per-unit excise tax of the same amount is imposed on both goods, which of the following is true?',
  'Assume that price elasticity of demand for good A is -0.3 and price elasticity of demand for good B is -2.5.  Assume goods A and B have identical '
  'supply curves.  If a per-unit excise tax of the same amount is imposed on both goods, which of the following is true?'),
 (341,
  'Assume that supply of wheat is relatively price inelastic while demand for wheat is relatively price elastic.  If the government imposes a '
  'specific exise tax on the production of corn, the incidence of tax will fall',
  'Assume that supply of wheat is relatively price inelastic while demand for wheat is relatively price elastic.  If the government imposes a '
  'specific excise tax on the production of wheat, the incidence of tax will fall'),
 (342,
  'Assume demand for cigarettes is inelastic and supply of cigarettes is elastic. If the government applies an exise tax on cigarettes, which of the '
  'following will occur in the short run?',
  'Assume demand for cigarettes is inelastic and supply of cigarettes is elastic. If the government applies an excise tax on cigarettes, which of '
  'the following will occur in the short run?'),
 (357,
  'In the graph above, an exise tax has been imposed, moving supply from Supply to Supply + Tax.  Total consumer surplus after imposition of the tax '
  'is:',
  'In the graph above, an excise tax has been imposed, moving supply from Supply to Supply + Tax.  Total consumer surplus after imposition of the '
  'tax is:'),
 (358,
  'In the graph above, an exise tax has been imposed, moving supply from Supply to Supply + Tax.  Total producer surplus after imposition of the tax '
  'is:',
  'In the graph above, an excise tax has been imposed, moving supply from Supply to Supply + Tax.  Total producer surplus after imposition of the '
  'tax is:'),
 (371,
  'The above diagram shows the impact of a subsidy in the market for agricultural products in the EU.  What is the cost of financing the subsidy to '
  'government',
  'The above diagram shows the impact of a subsidy in the market for agricultural products in the EU.  What is the cost of financing the subsidy to '
  'government?')]

# (question_id, old_image_url, new_image_url)
QUESTION_IMAGE = [(357, None, 'https://evtds-seeds.s3.us-east-2.amazonaws.com/TaxPsCsCalc_1.png'),
 (358, None, 'https://evtds-seeds.s3.us-east-2.amazonaws.com/TaxPsCsCalc_1.png'),
 (377, 'https://evtds-seeds.s3.us-east-2.amazonaws.com/subswithn.png', 'https://evtds-seeds.s3.us-east-2.amazonaws.com/subswithnumbs.png')]

# (answer_id, from_question_id, to_question_id) — answers attached to the wrong question
ANSWER_MOVES = [(1703, 349, 350),
 (1704, 349, 350),
 (1705, 349, 350),
 (1706, 349, 350),
 (1707, 349, 350),
 (1708, 349, 351),
 (1709, 349, 351),
 (1710, 349, 351),
 (1711, 349, 351),
 (1712, 349, 351),
 (1810, 377, 376),
 (1811, 377, 376),
 (1812, 377, 376),
 (1813, 377, 376),
 (1814, 377, 376)]

# (answer_id, old_text, new_text)
ANSWER_TEXT = [(1638, 'The price recieved by producers of electric vehicles will increase', 'The price received by producers of electric vehicles will increase'),
 (1676, 'Tax burden will fall entirely on consumeres', 'Tax burden will fall entirely on consumers'),
 (1679, 'Result in no change to after tax revenue recieved by producers', 'Result in no change to after tax revenue received by producers'),
 (1681, 'Decrease after tax revenue recieved by producers', 'Decrease after tax revenue received by producers'),
 (1682, 'Not change total exp', 'Not change total expenditure by consumers'),
 (1690, 'P2, C, Q2, 0, ', 'P2, C, Q2, 0'),
 (1695, 'P2, C, Q2, 0, ', 'P2, C, Q2, 0'),
 (1704,
  'Consumer Expenditure Before Tax: $1,000, Consumer Expenditure After Tax: $1,310',
  'Consumer Expenditure Before Tax: $1,000, Consumer Expenditure After Tax: $1,260'),
 (1723, 'Increase or decrease, depending on price elastiicty of demand', 'Increase or decrease, depending on price elasticity of demand'),
 (1734,
  'Buyer Price Paid: $14, Seller Price Received: $9, Deadweight Loss: $125',
  'Buyer Price Paid: $14, Seller Price Received: $9, Deadweight Loss: $25'),
 (1738, '$405', '$495'),
 (1751, 'Consumers buy more gas powered cars cars', 'Consumers buy more gas-powered cars'),
 (1769,
  'The price that higher educations receive for supplying education falls',
  'The price that higher education institutions receive for supplying education falls'),
 (1850, 'People may resort to black markets to aquire the good', 'People may resort to black markets to acquire the good')]

# (answer_id, old_is_correct, new_is_correct)
ANSWER_KEY = [(1648, False, True), (1649, True, False), (1774, True, False), (1776, True, False)]

# (question_id, text, is_correct) — answers that never existed live; added only if the question has none
ANSWER_INSERT = [(355, 'Increase or decrease, depending on price elasticity of supply', False),
 (355, 'Increase, because airline companies will sell more airline travel', False),
 (355, 'Increase, because airline companies will pass the tax on to consumers', False),
 (355, 'Decrease, because there will be more airline travel available', False),
 (355, 'Decrease, because price received by airline companies for supplying airline travel will decrease, and quantity supplied will decrease', True)]

# question_id -> (chapter_id, current text) for ANSWER_INSERT targets
INSERT_TARGETS = {355: (38, 'If the government imposes a per-unit tax on airline travel, producer surplus in the airline travel market will')}

# (question_id, chapter_id, seconds) — rewatch times
VIDEO_START = [(333, 38, 424),
 (334, 38, 538),
 (335, 38, 300),
 (336, 38, 389),
 (337, 38, 424),
 (338, 38, 538),
 (339, 38, 986),
 (340, 38, 986),
 (341, 38, 986),
 (342, 38, 986),
 (343, 38, 441),
 (344, 38, 986),
 (345, 38, 538),
 (346, 38, 591),
 (347, 38, 497),
 (348, 38, 538),
 (349, 38, 538),
 (350, 38, 497),
 (351, 38, 591),
 (352, 38, 629),
 (353, 38, 770),
 (354, 38, 629),
 (355, 38, 684),
 (356, 38, 770),
 (357, 38, 647),
 (358, 38, 703),
 (364, 67, 424),
 (365, 67, 335),
 (366, 67, 440),
 (367, 67, 528),
 (368, 67, 335),
 (369, 67, 528),
 (370, 67, 548),
 (371, 67, 587),
 (372, 67, 841),
 (373, 67, 478),
 (374, 67, 685),
 (375, 67, 646),
 (376, 67, 646),
 (377, 67, 685),
 (397, 100, 242),
 (398, 100, 260),
 (399, 100, 398),
 (400, 100, 548),
 (401, 100, 260),
 (402, 100, 466),
 (403, 100, 260),
 (404, 100, 156),
 (430, 133, 408),
 (431, 133, 103),
 (432, 133, 444),
 (433, 133, 444),
 (434, 133, 391),
 (435, 133, 444),
 (436, 133, 495),
 (437, 133, 650),
 (438, 133, 687),
 (439, 134, 171),
 (440, 134, 139),
 (441, 134, 256),
 (442, 134, 222),
 (443, 134, 232),
 (444, 134, 239),
 (445, 134, 413),
 (446, 134, 171),
 (447, 135, 38),
 (448, 135, 413),
 (449, 135, 110),
 (450, 135, 195),
 (451, 135, 299),
 (452, 135, 315),
 (453, 135, 247),
 (454, 135, 363),
 (455, 135, 38),
 (456, 136, 465),
 (457, 136, 258),
 (458, 136, 552),
 (459, 136, 328),
 (460, 136, 777),
 (461, 136, 913),
 (462, 136, 828),
 (463, 136, 552),
 (464, 136, 878),
 (465, 137, 86),
 (466, 137, 207),
 (467, 137, 224),
 (468, 137, 190),
 (469, 137, 688),
 (470, 137, 738),
 (471, 137, 758),
 (472, 137, 863),
 (473, 137, 967)]


def upgrade():
    conn = op.get_bind()
    run = lambda sql, **kw: conn.execute(sa.text(sql), kw)
    for aid, frm, to in ANSWER_MOVES:
        run("UPDATE answer SET question_id = :to WHERE id = :aid AND question_id = :frm", to=to, aid=aid, frm=frm)
    for aid, old, new in ANSWER_TEXT:
        run("UPDATE answer SET text = :new WHERE id = :aid AND text = :old", new=new, aid=aid, old=old)
    for aid, old, new in ANSWER_KEY:
        run("UPDATE answer SET is_correct = :new WHERE id = :aid AND is_correct = :old", new=new, aid=aid, old=old)
    for qid in sorted({q for q, _, _ in ANSWER_INSERT}):
        # Only the live question this was written for: right chapter, right wording, and still no answers
        chapter_id, qtext = INSERT_TARGETS[qid]
        exists = conn.execute(sa.text("SELECT count(*) FROM question WHERE id = :q AND chapter_id = :c AND text = :t"),
                              {"q": qid, "c": chapter_id, "t": qtext}).scalar()
        if exists and conn.execute(sa.text("SELECT count(*) FROM answer WHERE question_id = :q"), {"q": qid}).scalar() == 0:
            for q, text, ok in ANSWER_INSERT:
                if q == qid:
                    run("INSERT INTO answer (text, question_id, is_correct) VALUES (:t, :q, :c)", t=text, q=qid, c=ok)
    for qid, old, new in QUESTION_TEXT:
        run("UPDATE question SET text = :new WHERE id = :q AND text = :old", new=new, q=qid, old=old)
    for qid, old, new in QUESTION_IMAGE:
        run("UPDATE question SET image_url = :new WHERE id = :q AND image_url IS NOT DISTINCT FROM :old", new=new, q=qid, old=old)
    for qid, chapter_id, start in VIDEO_START:
        run("UPDATE question SET video_start = :s WHERE id = :q AND chapter_id = :c AND video_start IS NULL", s=start, q=qid, c=chapter_id)


def downgrade():
    conn = op.get_bind()
    run = lambda sql, **kw: conn.execute(sa.text(sql), kw)
    for qid, chapter_id, start in VIDEO_START:
        run("UPDATE question SET video_start = NULL WHERE id = :q AND chapter_id = :c AND video_start = :s", s=start, q=qid, c=chapter_id)
    for qid, old, new in QUESTION_IMAGE:
        run("UPDATE question SET image_url = :old WHERE id = :q AND image_url IS NOT DISTINCT FROM :new", new=new, q=qid, old=old)
    for qid, old, new in QUESTION_TEXT:
        run("UPDATE question SET text = :old WHERE id = :q AND text = :new", new=new, q=qid, old=old)
    for aid, old, new in ANSWER_KEY:
        run("UPDATE answer SET is_correct = :old WHERE id = :aid AND is_correct = :new", new=new, aid=aid, old=old)
    for aid, old, new in ANSWER_TEXT:
        run("UPDATE answer SET text = :old WHERE id = :aid AND text = :new", new=new, aid=aid, old=old)
    for aid, frm, to in ANSWER_MOVES:
        run("UPDATE answer SET question_id = :frm WHERE id = :aid AND question_id = :to", to=to, aid=aid, frm=frm)
