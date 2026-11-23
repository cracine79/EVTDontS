"""Fix question errors: wrong answer keys, misplaced answers, missing graphs, duplicates, typos, remove Q244

Every change is guarded: a row is only updated when it still has the exact text/value this
migration expects, so anything edited since is left alone. Review list: question_fixes.html.

Revision ID: d5a1c7e9f2b4
Revises: c3f8a2d4e6b1
Create Date: 2026-11-22
"""
from alembic import op
import sqlalchemy as sa

revision = 'd5a1c7e9f2b4'
down_revision = 'c3f8a2d4e6b1'
branch_labels = None
depends_on = None

# Chapter 4.1 exact duplicates: (remove, keep)
DEDUPE = [(572, 665),
 (573, 666),
 (574, 667),
 (575, 668),
 (576, 669),
 (577, 670),
 (578, 671),
 (579, 672),
 (580, 674),
 (581, 675),
 (582, 677),
 (583, 678),
 (584, 679),
 (585, 680),
 (586, 681),
 (587, 682),
 (588, 683),
 (589, 684),
 (590, 685),
 (591, 686),
 (592, 687),
 (593, 688),
 (594, 689),
 (595, 690)]

# Questions removed outright: (id, exact text). Q244 refers to a graph that doesn't exist.
REMOVE = [(244, 'In the diagram above, at which point is demand most inelastic?')]

# Answers attached to the wrong question: (answer_id, from_question, to_question)
MOVES = [(1681, 586, 587),
 (1682, 586, 587),
 (1683, 586, 587),
 (1684, 586, 587),
 (1685, 586, 587),
 (1686, 586, 588),
 (1687, 586, 588),
 (1688, 586, 588),
 (1689, 586, 588),
 (1690, 586, 588),
 (1706, 591, 592),
 (1707, 591, 592),
 (1708, 591, 592),
 (1709, 591, 592),
 (1710, 591, 592),
 (1811, 681, 682),
 (1812, 681, 682),
 (1813, 681, 682),
 (1814, 681, 682),
 (1815, 681, 682),
 (1816, 681, 683),
 (1817, 681, 683),
 (1818, 681, 683),
 (1819, 681, 683),
 (1820, 681, 683),
 (1836, 686, 687),
 (1837, 686, 687),
 (1838, 686, 687),
 (1839, 686, 687),
 (1840, 686, 687),
 (1916, 704, 703),
 (1917, 704, 703),
 (1918, 704, 703),
 (1919, 704, 703),
 (1920, 704, 703)]

# Answer key: (answer_id, question_id, old_is_correct, new_is_correct)
CORRECT = [(261, 53, True, False),
 (571, 115, True, False),
 (573, 115, False, True),
 (576, 116, True, False),
 (578, 116, False, True),
 (743, 149, True, False),
 (841, 169, True, False),
 (842, 169, False, True),
 (956, 192, False, True),
 (1167, 234, True, False),
 (1169, 234, False, True),
 (1202, 241, True, False),
 (1201, 241, False, True),
 (1229, 246, True, False),
 (1228, 246, False, True),
 (1297, 260, True, False),
 (1296, 260, False, True),
 (1402, 281, True, False),
 (1405, 281, False, True),
 (1414, 283, True, False),
 (1415, 283, False, True),
 (1637, 578, True, False),
 (1636, 578, False, True),
 (1757, 671, True, False),
 (1756, 671, False, True),
 (1880, 695, True, False),
 (1882, 696, True, False)]

# Graphs: (question_id, old_url, new_url)
IMAGES = [(235,
  'https://evtds-seeds.s3.us-east-2.amazonaws.com/PerfectlyElasticDemand.png',
  'https://evtds-seeds.s3.us-east-2.amazonaws.com/PerfectlyElasticDemand.png'),
 (236,
  'https://evtds-seeds.s3.us-east-2.amazonaws.com/PerfectlyInelasticDemand.png',
  'https://evtds-seeds.s3.us-east-2.amazonaws.com/PerfectlyInelasticDemand.png'),
 (147, None, 'https://evtds-seeds.s3.us-east-2.amazonaws.com/SD2.png'),
 (148, None, 'https://evtds-seeds.s3.us-east-2.amazonaws.com/SD2.png'),
 (594, None, 'https://evtds-seeds.s3.us-east-2.amazonaws.com/TaxPsCsCalc_1.png'),
 (595, None, 'https://evtds-seeds.s3.us-east-2.amazonaws.com/TaxPsCsCalc_1.png'),
 (689, None, 'https://evtds-seeds.s3.us-east-2.amazonaws.com/TaxPsCsCalc_1.png'),
 (690, None, 'https://evtds-seeds.s3.us-east-2.amazonaws.com/TaxPsCsCalc_1.png'),
 (704, 'https://evtds-seeds.s3.us-east-2.amazonaws.com/subswithn.png', 'https://evtds-seeds.s3.us-east-2.amazonaws.com/subswithnumbs.png')]

# Text: (table, id, old_text, new_text)
TEXT = [('answer', 8, 'Limited resource to satisfy unlimited wants', 'Limited resources to satisfy unlimited wants'),
 ('answer',
  32,
  'Frederick’s total opportunity cost is the tuition he must pay to attend school plus the price of books.',
  'Fredrick’s total opportunity cost is the tuition he must pay to attend school plus the price of books.'),
 ('answer',
  35,
  'Samuel’s opportunity costs is certainly less than Fredrick’s',
  'Samuel’s opportunity cost is certainly less than Fredrick’s'),
 ('answer', 110, 'Psuedo Economy', 'Pseudo Economy'),
 ('answer',
  178,
  'Producing at point C is not preferrable, because there are other options that allow for a greater variety of music.',
  'Producing at point C is not preferable, because there are other options that allow for a greater variety of music.'),
 ('answer',
  207,
  'It decreases, because the production of good Y increases by smaller amounts',
  'It decreases, because the production of good B increases by smaller amounts'),
 ('answer',
  210,
  'It increases, because the production of good B decreases by smaller amount',
  'It increases, because the production of good B decreases by smaller amounts'),
 ('answer',
  218,
  'The opportunity cost of producing of a good increases as more of it is produced.',
  'The opportunity cost of producing a good increases as more of it is produced.'),
 ('answer', 261, 'Nation A should specialize in wheat.', 'Nation B should specialize in both goods.'),
 ('answer',
  327,
  'Tom has a absolute advantage in producing pizzas, while Alice has an absolute advantage in producing sandwiches.',
  'Tom has an absolute advantage in producing pizzas, while Alice has an absolute advantage in producing sandwiches.'),
 ('answer',
  332,
  'Factory Y has an absolute advantage in producing rollerblades.',
  'Factory Y has an absolute advantage in producing helmets.'),
 ('answer',
  468,
  'No change is exected as a result of the substitution effect',
  'No change is expected as a result of the substitution effect'),
 ('answer',
  487,
  'The substitution effect moves the quanitty demanded in the opposite direction than the substitution effect',
  'The substitution effect moves the quantity demanded in the opposite direction from the income effect'),
 ('answer', 497, 'Substitution Effect: Increase, Income Effect, Decrease ', 'Substitution Effect: Increase, Income Effect: Decrease '),
 ('answer', 498, 'Substitution Effect: Decrease, Income Effect, No Change', 'Substitution Effect: Decrease, Income Effect: No Change'),
 ('answer', 499, 'Substitution Effect: Decrease, Income Effect, Decrease', 'Substitution Effect: Decrease, Income Effect: Decrease'),
 ('answer', 500, 'Substitution Effect: Decrease, Income Effecxt: Increase', 'Substitution Effect: Decrease, Income Effect: Increase'),
 ('answer', 509, 'a decrease in the quanitty of peanut butter demanded', 'a decrease in the quantity of peanut butter demanded'),
 ('answer', 510, 'an increase in the quanitty of peanut butter supplied', 'an increase in the quantity of peanut butter supplied'),
 ('answer', 512, 'Demand is met buy Supply', 'Demand is met by supply'),
 ('answer',
  537,
  'An decrease in the price of good C, a complement for good A',
  'A decrease in the price of good C, a complement for good A'),
 ('answer', 573, 'The quantity demanded of good Z will decrease', 'The quantity demanded of good Z will increase'),
 ('answer', 577, 'The quantity demanded of the good will decrease', 'The quantity demanded of the good will increase'),
 ('answer',
  588,
  'More firms still try to make and sell as many as possible, and consumers will buy more',
  'Firms will still try to make and sell as many as possible, and consumers will buy more'),
 ('answer',
  589,
  'Firms will reduce the quantity they prouduce and sell, decreasing the total quantity supplied in the market',
  'Firms will reduce the quantity they produce and sell, decreasing the total quantity supplied in the market'),
 ('answer',
  590,
  'The answer depends whether or not the good is an inferior good',
  'The answer depends on whether or not the good is an inferior good'),
 ('answer',
  596,
  'The price of apples fall, so apple manufacturers reduce the total amount of apples they grow that year',
  'The price of apples falls, so apple growers reduce the total amount of apples they grow that year'),
 ('answer',
  597,
  'The price of tea increases, so tea farmers grow less that year because they can sell fewer units of tea and still make the same amount '
  'total revenue.',
  'The price of tea increases, so tea farmers grow less that year because they can sell fewer units of tea and still make the same amount '
  'of total revenue.'),
 ('answer', 652, 'an increase in the price of cookies, a comlement to tea', 'an increase in the price of cookies, a complement to tea'),
 ('answer', 655, 'an increae in the price of tea', 'an increase in the price of tea'),
 ('answer',
  715,
  'Greater than $3, because no supplier will sell any output at a price less tahn $3',
  'Greater than $3, because no supplier will sell any output at a price less than $3'),
 ('answer',
  717,
  'A shortage in the market, which should downward pressure on prices',
  'A shortage in the market, which should put downward pressure on prices'),
 ('answer', 724, 'At equilibrium, fewer than 200 sandiwches will be sold', 'At equilibrium, fewer than 200 sandwiches will be sold'),
 ('answer', 741, 'There is a shortage of earrings at a price of $100', 'There is a surplus of earrings at a price of $100'),
 ('answer', 743, 'At equilibrium, fewer than 500 earrings will be purchased', 'At equilibrium, more than 500 earrings will be purchased'),
 ('answer', 748, 'The market is in equilbrium', 'The market is in equilibrium'),
 ('answer',
  757,
  'The price of oranges, a substitute for oranges, is higher than last year',
  'The price of oranges, a substitute for apples, is higher than last year'),
 ('answer',
  758,
  'New medical studies show that if consuming apples can cause infertility and in some cases, temporary blindness, due to a new strain of '
  'apple worm',
  'New medical studies show that consuming apples can cause infertility and in some cases, temporary blindness, due to a new strain of '
  'apple worm'),
 ('answer', 759, 'Consumers income increase and apples are normal goods', 'Consumer incomes increase and apples are normal goods'),
 ('answer',
  771,
  'Record rainfall make the climate especially good for the growth of corn, doubling farmers output',
  'Record rainfall makes the climate especially good for the growth of corn, doubling farmers’ output'),
 ('answer',
  772,
  'A Tiktok trend which takes the nation where teenagers try to buy as much corn as possible and eat it in one sitting. ',
  'A TikTok trend sweeps the nation, where teenagers try to buy as much corn as possible and eat it in one sitting. '),
 ('answer', 775, 'The size of hte population doubles', 'The size of the population doubles'),
 ('answer',
  791,
  'Price of haircuts and total quantity haircuts performed fall',
  'Price of haircuts and total quantity of haircuts performed fall'),
 ('answer',
  792,
  'Price of haircuts and total quantity haircuts performed rise',
  'Price of haircuts and total quantity of haircuts performed rise'),
 ('answer', 795, 'No change to price or quanitty of haircuts performed.', 'No change to price or quantity of haircuts performed.'),
 ('answer', 802, 'A holiday rush causes a spike in demand for Pokemn cards', 'A holiday rush causes a spike in demand for Pokemon cards'),
 ('answer',
  803,
  'A rival colletor card - Jokedude cards cuts its prices in half',
  'A rival collector card, Jokedude cards, cuts its prices in half'),
 ('answer',
  809,
  'An intiative by local activists encouraging consumers to buy fewer paper plates',
  'An initiative by local activists encouraging consumers to buy fewer paper plates'),
 ('answer',
  810,
  'In increase in the cost of labor employed in the production of paper plates',
  'An increase in the cost of labor employed in the production of paper plates'),
 ('answer', 849, 'Quadrant D meaning quantity definitely decreases', 'Quadrant D, meaning quantity definitely decreases'),
 ('answer', 850, 'Quadrant D, but we do not know hwat happens to quantity', 'Quadrant D, but we do not know what happens to quantity'),
 ('answer', 853, 'Price: Decrease, Quantity: Decrease', 'Price: Increase, Quantity: Indeterminate'),
 ('answer', 856, 'Only an decrease in demand', 'Only a decrease in demand'),
 ('answer', 857, 'Only an decrease in supply', 'Only a decrease in supply'),
 ('answer', 860, 'An decrease in demand and a decrease in supply', 'A decrease in demand and a decrease in supply'),
 ('answer', 886, 'Only an increasein demand', 'Only an increase in demand'),
 ('answer', 894, 'Increasing opporunity cost', 'Increasing opportunity cost'),
 ('answer',
  900,
  'The total utility of consumin gone unit is greater than the total utility of consuming two units',
  'The total utility of consuming one unit is greater than the total utility of consuming two units'),
 ('answer', 908, 'Marginal utility is mazimized', 'Marginal utility is maximized'),
 ('answer',
  936,
  'Two board games, because only the fifth and fourth board game have loewr marginal benefit than price',
  'Two board games, because only the fifth and fourth board game have lower marginal benefit than price'),
 ('answer',
  959,
  'Two distinct curves, with the marignal benefit curve lying above the demand curve',
  'Two distinct curves, with the marginal benefit curve lying above the demand curve'),
 ('answer', 975, 'It cannot be determined from the informatino provided', 'It cannot be determined from the information provided'),
 ('answer', 1020, 'remain constant at 400', 'remain constant at $400'),
 ('answer',
  1030,
  'The sum of the differences between the prices that consumers are willing to pay for a good and the minimum price that producers need to '
  'recieve to sell the good',
  'The sum of the differences between the prices that consumers are willing to pay for a good and the minimum price that producers need to '
  'receive to sell the good'),
 ('answer', 1066, 'fall by $750', 'fall by $300'),
 ('answer',
  1115,
  'Indeterminant from given information - need more information about sellers average total costs',
  'Indeterminate from given information - need more information about sellers’ average total costs'),
 ('answer', 1127, 'MB = $40, MC = $10, alocative efficiency is not achieved', 'MB = $40, MC = $10, allocative efficiency is not achieved'),
 ('answer', 1168, 'An excess demand for bottled water', 'An excess demand for cheese'),
 ('answer',
  1169,
  'An increase in price, leading to a relatively smaller decrease in quantity demanded of cheese',
  'An increase in price, leading to a relatively larger decrease in quantity demanded of cheese'),
 ('answer',
  1268,
  'Good A takes up a smaller proportion of income than good B',
  'Good A takes up a larger proportion of income than good B'),
 ('answer', 1270, 'Good B is very, very cheap and good A is very expensive.', 'Good A is very, very cheap and good B is very expensive.'),
 ('answer',
  1300,
  'No change to quantity demanded or supplied of enery drinks',
  'No change to quantity demanded or supplied of energy drinks'),
 ('answer',
  1302,
  'PED: Inelastic, Price: Increasees, Total Revenue: Increases',
  'PED: Inelastic, Price: Increases, Total Revenue: Increases'),
 ('answer', 1305, 'PED: Elsatic, Price: Increases, Total Revenue: Increases', 'PED: Elastic, Price: Increases, Total Revenue: Increases'),
 ('answer', 1317, 'Park Visitors: Increase, Revenues, Decrease', 'Park Visitors: Increase, Revenues: Decrease'),
 ('answer', 1318, 'Park Visitors: Decrease, Revenues, Decrease', 'Park Visitors: Decrease, Revenues: Decrease'),
 ('answer', 1319, 'Park Visitor: Decrease, Revenues: Increase', 'Park Visitors: Decrease, Revenues: Increase'),
 ('answer', 1401, 'The price of mustard is expected to fall by 40%', 'The quantity demanded of mustard is expected to fall by 40%'),
 ('answer', 1402, 'The price of mustard is expected to fall by 12%', 'The quantity demanded of mustard is expected to fall by 12%'),
 ('answer', 1403, 'The price of mustard is expected to fall by 4%', 'The quantity demanded of mustard is expected to fall by 4%'),
 ('answer', 1404, 'The price of mustard is expected to rise by 4%', 'The quantity demanded of mustard is expected to rise by 4%'),
 ('answer', 1405, 'The price of mustard is expected to rise by 12%', 'The quantity demanded of mustard is expected to rise by 12%'),
 ('answer', 1462, 'Good X is an inferior good, Good Y is a normal goo', 'Good X is an inferior good, Good Y is a normal good'),
 ('answer', 1468, 'No Change: Decrease, Instant Noodles: Increase', 'Entertainment: No Change, Instant Noodles: Increase'),
 ('answer', 1508, 'Quantity demande of bus tickets will rise by 80%', 'Quantity demanded of bus tickets will rise by 80%'),
 ('answer', 1518, 'Yellow wigs are inferior goods, and YED = 0.75', 'Yellow wigs are inferior goods, and YED = -0.75'),
 ('answer', 1544, 'PES = ∞, Suppy is perfectly inelastic', 'PES = ∞, Supply is perfectly inelastic'),
 ('answer', 1545, 'PES = ∞, Suppy is perfectly elastic', 'PES = ∞, Supply is perfectly elastic'),
 ('answer', 1553, 'The quanitty supplied of automobiles will increase by 16%', 'The quantity supplied of automobiles will increase by 16%'),
 ('answer', 1579, 'PES = -0.5, and supply is  inelastic', 'PES = -0.5, and supply is inelastic'),
 ('answer',
  1626,
  'The price recieved by producers of electric vehicles will increase',
  'The price received by producers of electric vehicles will increase'),
 ('answer',
  1657,
  'Result in no change to after tax revenue recieved by producers',
  'Result in no change to after tax revenue received by producers'),
 ('answer', 1659, 'Decrease after tax revenue recieved by producers', 'Decrease after tax revenue received by producers'),
 ('answer', 1660, 'Not change total exp', 'Not change total expenditure by consumers'),
 ('answer', 1668, 'P2, C, Q2, 0, ', 'P2, C, Q2, 0'),
 ('answer', 1673, 'P2, C, Q2, 0, ', 'P2, C, Q2, 0'),
 ('answer',
  1682,
  'Consumer Expenditure Before Tax: $1,000, Consumer Expenditure After Tax: $1,310',
  'Consumer Expenditure Before Tax: $1,000, Consumer Expenditure After Tax: $1,260'),
 ('answer',
  1701,
  'Increase or decrease, depending on price elastiicty of demand',
  'Increase or decrease, depending on price elasticity of demand'),
 ('answer',
  1706,
  'Increase or decrease, depending on price elastiicty of supply',
  'Increase or decrease, depending on price elasticity of supply'),
 ('answer',
  1712,
  'Buyer Price Paid: $14, Seller Price Received: $9, Deadweight Loss: $125',
  'Buyer Price Paid: $14, Seller Price Received: $9, Deadweight Loss: $25'),
 ('answer', 1716, '$405', '$495'),
 ('answer',
  1746,
  'The price recieved by producers of electric vehicles will increase',
  'The price received by producers of electric vehicles will increase'),
 ('answer', 1784, 'Tax burden will fall entirely on consumeres', 'Tax burden will fall entirely on consumers'),
 ('answer',
  1787,
  'Result in no change to after tax revenue recieved by producers',
  'Result in no change to after tax revenue received by producers'),
 ('answer', 1789, 'Decrease after tax revenue recieved by producers', 'Decrease after tax revenue received by producers'),
 ('answer', 1790, 'Not change total exp', 'Not change total expenditure by consumers'),
 ('answer', 1798, 'P2, C, Q2, 0, ', 'P2, C, Q2, 0'),
 ('answer', 1803, 'P2, C, Q2, 0, ', 'P2, C, Q2, 0'),
 ('answer',
  1812,
  'Consumer Expenditure Before Tax: $1,000, Consumer Expenditure After Tax: $1,310',
  'Consumer Expenditure Before Tax: $1,000, Consumer Expenditure After Tax: $1,260'),
 ('answer',
  1831,
  'Increase or decrease, depending on price elastiicty of demand',
  'Increase or decrease, depending on price elasticity of demand'),
 ('answer',
  1836,
  'Increase or decrease, depending on price elastiicty of supply',
  'Increase or decrease, depending on price elasticity of supply'),
 ('answer',
  1842,
  'Buyer Price Paid: $14, Seller Price Received: $9, Deadweight Loss: $125',
  'Buyer Price Paid: $14, Seller Price Received: $9, Deadweight Loss: $25'),
 ('answer', 1846, '$405', '$495'),
 ('answer', 1857, 'Consumers buy more gas powered cars cars', 'Consumers buy more gas-powered cars'),
 ('answer',
  1875,
  'The price that higher educations receive for supplying education falls',
  'The price that higher education institutions receive for supplying education falls'),
 ('answer', 1927, 'People may resort to black markets to aquire the good', 'People may resort to black markets to acquire the good'),
 ('answer', 1940, 'Consumer excpenditure definitely rises', 'Consumer expenditure definitely rises'),
 ('answer', 1960, 'The quantity of rental housind demanded will decrease', 'The quantity of rental housing demanded will decrease'),
 ('question',
  7,
  'Fredrick chose to attend college after graduating from high school.  Samuel went to work full time directly out of college.  Which of '
  'the following best describes the opportunity costs for these decisions?',
  'Fredrick chose to attend college after graduating from high school.  Samuel went to work full time directly out of high school.  Which '
  'of the following best describes the opportunity costs for these decisions?'),
 ('question',
  20,
  'Which economic system is characterized by a combination of government intervention and market force?',
  'Which economic system is characterized by a combination of government intervention and market forces?'),
 ('question',
  39,
  'Which of the following explains why the PPF is depicted as outward bowed (concave) from the origin.',
  'Which of the following explains why the PPF is depicted as outward bowed (concave) from the origin?'),
 ('question',
  72,
  'An businesman starting a new business would be an example of which factor of production?',
  'A businessperson starting a new business would be an example of which factor of production?'),
 ('question',
  81,
  'Jeff works part time at a local gas station and earns $15 an hour.  He wants to spend next Thursday afternoon attending a comic book '
  'convention. The full price of a convention ticket is $80, but he was able to get a discounted price of $60 online. If Jeff took 4 hours '
  'off to go to the convention, what was his opportunity cost of attending the concert?',
  'Jeff works part time at a local gas station and earns $15 an hour.  He wants to spend next Thursday afternoon attending a comic book '
  'convention. The full price of a convention ticket is $80, but he was able to get a discounted price of $60 online. If Jeff took 4 hours '
  'off to go to the convention, what was his opportunity cost of attending the convention?'),
 ('question',
  82,
  'A linear production possibliites curve suggests which of the following?',
  'A linear production possibilities curve suggests which of the following?'),
 ('question',
  83,
  'An outward bowed production possibliites curve suggests which of the following?',
  'An outward bowed production possibilities curve suggests which of the following?'),
 ('question',
  91,
  'An opportunity cost is involved in which of the following decisions? <br><br>I. A student decides to attend college full time<br>II. An '
  'individual uses $3,000 of his savings to buy a 4k big screen TV<br>III. A factory decides to produce more iPhone cases and fewer iPad '
  'cases',
  'An opportunity cost is involved in which of the following decisions? <br><br>I. A student decides to attend college full time<br>II. An '
  'individual uses $3,000 of his savings to buy a 4K big screen TV<br>III. A factory decides to produce more iPhone cases and fewer iPad '
  'cases'),
 ('question',
  92,
  'It takes Mary 30 minutes to complete a math homework and 90 minutes to study for an Economics exam. Assuming Mary can only engage in '
  'these two activities, what is the opportunity cost to Mary of studying for one Economics exam?',
  'It takes Mary 30 minutes to complete a math homework assignment and 90 minutes to study for an Economics exam. Assuming Mary can only '
  'engage in these two activities, what is the opportunity cost to Mary of studying for one Economics exam?'),
 ('question',
  93,
  'Quinn just graduated from high school and has decided to take a Gap year and travel the world. Before making this decision, she was '
  'also considering:<br><br>I. Going to college<br>II. Getting a job<br>III. Volunteering locally<br><br>Which of the following is an '
  'opportunity cost to Quinn and her decision to travel the world?',
  'Quinn just graduated from high school and has decided to take a gap year and travel the world. Before making this decision, she was '
  'also considering:<br><br>I. Going to college<br>II. Getting a job<br>III. Volunteering locally<br><br>Which of the following is an '
  'opportunity cost to Quinn and her decision to travel the world?'),
 ('question',
  95,
  'The table above lists the monthly individual demahd schedules for pizza for the only three buyers in the market, April, Bob and '
  'Charlie.  Which of the following combinations of price and quantity lies on the demand curve?',
  'The table above lists the monthly individual demand schedules for pizza for the only three buyers in the market, April, Bob and '
  'Charlie.  Which of the following combinations of price and quantity lies on the demand curve?'),
 ('question',
  96,
  'The graphs above show the individual demand curves for two consumers, Wes and Wyatt, in the market for salted peanuts.  As the price of '
  'salted peanuts decreases from $10 to $4, now does the quantity demanded change along the market demand curve?',
  'The graphs above show the individual demand curves for two consumers, Wes and Wyatt, in the market for salted peanuts.  As the price of '
  'salted peanuts decreases from $10 to $4, how does the quantity demanded change along the market demand curve?'),
 ('question',
  100,
  'Assume that pizza is a normal good.  If the price of pizza incerases, the substitution efefc and income effect will lead to which of '
  'the following changes in pizza consumption?',
  'Assume that pizza is a normal good.  If the price of pizza increases, the substitution effect and income effect will lead to which of '
  'the following changes in pizza consumption?'),
 ('question',
  109,
  'Which of the following will most likely happen if the market for good Z if the price of good Z increases?',
  'Which of the following will most likely happen in the market for good Z if the price of good Z increases?'),
 ('question',
  119,
  "The entire market for chairs in Shermer, Illinois consists of two firms, Firm A and Firm B.  Each firm's supply curve is shown above.  "
  'Given the supply curves, which of the following point is on the market supply curve?',
  "The entire market for chairs in Shermer, Illinois consists of two firms, Firm A and Firm B.  Each firm's supply curve is shown above.  "
  'Given the supply curves, which of the following points is on the market supply curve?'),
 ('question',
  139,
  'The above table shows the supply and demand schedule for a perfectly competitive market.   It the price in the market, which of the '
  'following is expected?',
  'The above table shows the supply and demand schedule for a perfectly competitive market.   If the price in the market is $75, which of '
  'the following is expected?'),
 ('question',
  147,
  'The above graph shows the supply and demand curves for a perfectly competitive market.  What is the expected outcome if the current '
  'market price is $10',
  'The above graph shows the supply and demand curves for a perfectly competitive market.  What is the expected outcome if the current '
  'market price is $10?'),
 ('question',
  150,
  'The above table shows the supply and demand schedule for a perfectly competitive market. If the market price is $2.50, what can be '
  'inferred about the market.',
  'The above table shows the supply and demand schedule for a perfectly competitive market. If the market price is $2.50, what can be '
  'inferred about the market?'),
 ('question',
  154,
  'In a competitive market for baseballs, a change in the market caused equilibrium price and equilbrium quantity of baseballs to fall.  '
  'Which of the following changes could have caused this to happen?',
  'In a competitive market for baseballs, a change in the market caused equilibrium price and equilibrium quantity of baseballs to fall.  '
  'Which of the following changes could have caused this to happen?'),
 ('question',
  161,
  'If the market for Pokemon cards saw a simultaneous decrease in equilibrium price and increase in equilibirum quantity, this could have '
  'been caused by which of the following changes?',
  'If the market for Pokemon cards saw a simultaneous decrease in equilibrium price and increase in equilibrium quantity, this could have '
  'been caused by which of the following changes?'),
 ('question',
  162,
  'Which of the following is NOT expected to result in an increase in equilibrium price and a decrease in the quantity consumed of paper '
  'plates',
  'Which of the following is NOT expected to result in an increase in equilibrium price and a decrease in the quantity consumed of paper '
  'plates?'),
 ('question',
  167,
  'Assume that more wheat is demanded as it is used to produce flour.  At the same time, more effective irrigation techniques allows '
  'farmers to produce more wheat.  Which of the following will definitely occur in the wheat market?',
  'Assume that more wheat is demanded as it is used to produce flour.  At the same time, more effective irrigation techniques allow '
  'farmers to produce more wheat.  Which of the following will definitely occur in the wheat market?'),
 ('question',
  168,
  'The market for olives is in equilibrium.  Assume that the surgeon general announces that eating 20 olives a day will greatly reduce the '
  'chances of fatal heart disease.  At the same time, there a draught severely damages the olive crop.  WHich of the following will '
  'definitely occur as a result?',
  'The market for olives is in equilibrium.  Assume that the surgeon general announces that eating 20 olives a day will greatly reduce the '
  'chances of fatal heart disease.  At the same time, a drought severely damages the olive crop.  Which of the following will definitely '
  'occur as a result?'),
 ('question',
  170,
  'The above diagram shows the market in equilibrium for milk.  If the demand for milk decreases and simultaneously the supply of milk '
  'increases, we know that the new equilibirum point must land somewhere in:',
  'The above diagram shows the market in equilibrium for milk.  If the demand for milk decreases and simultaneously the supply of milk '
  'increases, we know that the new equilibrium point must land somewhere in:'),
 ('question',
  171,
  'Assume that the government increases taxes on gasoline, and at the same time people are commuting less as they work from home more.  As '
  'a result, the equilibrium price and quantity of gasoline is expeced to change in which of the following ways?',
  'Assume that the government increases taxes on gasoline, and at the same time people are commuting less as they work from home more.  As '
  'a result, the equilibrium price and quantity of gasoline is expected to change in which of the following ways?'),
 ('question',
  172,
  'Last month 3,000 boxes were sold for $10 a box.  This month 3,150 boxes were sold for $8 a box.  WHich of the following changes to '
  'supply and demand could have resulted in this change to the market?',
  'Last month 3,000 boxes were sold for $10 a box.  This month 3,150 boxes were sold for $8 a box.  Which of the following changes to '
  'supply and demand could have resulted in this change to the market?'),
 ('question',
  179,
  'The diagram above shows Taylor`s utility function for cotton candy.  Her utility function illustrates the principal of',
  'The diagram above shows Taylor’s utility function for cotton candy.  Her utility function illustrates the principle of'),
 ('question',
  181,
  'The above diagram shows Wyatt`s marginal utility from toy cars.  What is his total utility from purchasing three cars?',
  'The above diagram shows Wyatt’s marginal utility from toy cars.  What is his total utility from purchasing three cars?'),
 ('question',
  184,
  'The above diagram shows Bob`s total utility for consumption of different quantities of Sushi.  Which sushi order has a Marginal Utility '
  'of five utils?',
  'The above diagram shows Bob’s total utility for consumption of different quantities of Sushi.  Which sushi order has a Marginal Utility '
  'of five utils?'),
 ('question',
  185,
  'The above diagram shows Bob`s total utility for consumption of different quantities of Sushi. What is the marginal utility of the fifth '
  'box of Sushi?',
  'The above diagram shows Bob’s total utility for consumption of different quantities of Sushi. What is the marginal utility of the fifth '
  'box of Sushi?'),
 ('question',
  186,
  'The above diagram shows Sammy`s dollar value total benefit she receives from buying various quantities of blue jeans.  What is the '
  'marginal benefit Sammy recieves from buying the third pair of blue jeans?',
  'The above diagram shows Sammy’s dollar value total benefit she receives from buying various quantities of blue jeans.  What is the '
  'marginal benefit Sammy receives from buying the third pair of blue jeans?'),
 ('question',
  187,
  'The above diagram shows Bill`s marginal benefit from purchasing different quantities of board games. Calculate Bill`s total benefit '
  'when he purchases four board games.',
  'The above diagram shows Bill’s marginal benefit from purchasing different quantities of board games. Calculate Bill’s total benefit '
  'when he purchases four board games.'),
 ('question',
  188,
  'The above diagram shows Bill`s marginal benefit from purchasing different quantities of board games.  If the price of board games is '
  '$10, how many board games will Bill buy?',
  'The above diagram shows Bill’s marginal benefit from purchasing different quantities of board games.  If the price of board games is '
  '$10, how many board games will Bill buy?'),
 ('question',
  190,
  'The above diagram shows Bill`s marginal benefit from purchasing different quantities of board games. When Bill purchases three board '
  'games, which of the following is true?',
  'The above diagram shows Bill’s marginal benefit from purchasing different quantities of board games. When Bill purchases three board '
  'games, which of the following is true?'),
 ('question',
  191,
  'The above diagram shows Wes`s dollar value total benefit he receives from buying various quantities of blue jeans. Which pair of blue '
  'jeans brings Wes a marginal benefit of $30?',
  'The above diagram shows Wes’s dollar value total benefit he receives from buying various quantities of blue jeans. Which pair of blue '
  'jeans brings Wes a marginal benefit of $30?'),
 ('question',
  207,
  'The difference between what Jaqueline is willing to pay for a new pair of sunglasses and what she actually pays is a measure of her',
  'The difference between what Jacqueline is willing to pay for a new pair of sunglasses and what she actually pays is a measure of her'),
 ('question',
  212,
  'The concept of producer surplus refers to which of the following',
  'The concept of producer surplus refers to which of the following?'),
 ('question',
  218,
  'If the total Social Surplus in a market is calculated to be $400, and Consumer Surplus is $150. The market is in equilibrium, and '
  'Social Surplus is maximizied.  Then Producer Surplus must be',
  'If the total Social Surplus in a market is calculated to be $400, and Consumer Surplus is $150. The market is in equilibrium, and '
  'Social Surplus is maximized.  Then Producer Surplus must be'),
 ('question',
  221,
  'In the market for hats there are buyers and sellers and the market is in equilibirum.  The sum of the differences between what buyers '
  'were willing to pay and what they actually paid was $400.  The sum of the differences of the prices that producers actually recieved '
  'and the prices they required in order to be willing to sell was $700.  From this information, social surplus is',
  'In the market for hats there are buyers and sellers and the market is in equilibrium.  The sum of the differences between what buyers '
  'were willing to pay and what they actually paid was $400.  The sum of the differences of the prices that producers actually received '
  'and the prices they required in order to be willing to sell was $700.  From this information, social surplus is'),
 ('question',
  222,
  'Which of the following conditions would suggest the market has achieved allocative efficiency (no externalities are present)',
  'Which of the following conditions would suggest the market has achieved allocative efficiency (no externalities are present)?'),
 ('question',
  233,
  'Moving from right to left upwards along a downward sloping linear demand curves, in which way does price elasticity of demand vary?',
  'Moving from right to left upwards along a downward sloping linear demand curve, in which way does price elasticity of demand vary?'),
 ('question',
  241,
  'The quantity demanded of hampsters increased from 800 to 1200 when the price of hampsters decreased from $20 to $18.  The price '
  'elasticity of demand for hampsters over this range is',
  'The quantity demanded of hamsters increased from 800 to 1200 when the price of hamsters decreased from $20 to $18.  The price '
  'elasticity of demand for hamsters over this range is'),
 ('question',
  251,
  'A firm`s demand curve is expected to be highly elastic if which of the following exists?',
  'A firm’s demand curve is expected to be highly elastic if which of the following exists?'),
 ('question',
  253,
  'What may be one reason that fidglebaums face a price elasticity demand coefficient of 2.5?',
  'What may be one reason that Figlebaums face a price elasticity of demand coefficient of 2.5?'),
 ('question',
  263,
  'If excellent weather and rain create an unusually large supply of grapes and grape farmers` revenues decrease as a result, which of the '
  'following is true over the observed range of prices?',
  'If excellent weather and rain create an unusually large supply of grapes and grape farmers’ revenues decrease as a result, which of the '
  'following is true over the observed range of prices?'),
 ('question',
  264,
  'Local government has decided to increase the price of admission to city parks from $2 to $2.50.  IF demand for these tickets is price '
  'inelastic, the number of people visitng parks and the city park revenues will most likely change in which of the following ways?',
  'Local government has decided to increase the price of admission to city parks from $2 to $2.50.  If demand for these tickets is price '
  'inelastic, the number of people visiting parks and the city park revenues will most likely change in which of the following ways?'),
 ('question',
  273,
  'If cross price elasticity between good X and good Y is positive, which of the following must be true about good X and good Y',
  'If cross price elasticity between good X and good Y is positive, which of the following must be true about good X and good Y?'),
 ('question',
  282,
  'The above table shows the price of good A and quantity of demanded of good Y in two different time periods.  Based upon the table, it '
  'can be inferred that good A and good B are',
  'The above table shows the price of good A and quantity demanded of good B in two different time periods.  Based upon the table, it can '
  'be inferred that good A and good B are'),
 ('question',
  293,
  'If income elastity for good X is 0.5 and for good Y is 1.2, which of the following is true?',
  'If income elasticity for good X is 0.5 and for good Y is 1.2, which of the following is true?'),
 ('question',
  309,
  'The above diagram shows the supply curve for a rare earth mineral.  Which of the following is true',
  'The above diagram shows the supply curve for a rare earth mineral.  Which of the following is true?'),
 ('question',
  311,
  'The price elasticity of supply of automobiles was calculated to be 0.8.  If the price of automobiles increase by 20%, what is the '
  'expected impact on the quantity supplied of automobiles?',
  'The price elasticity of supply of automobiles was calculated to be 0.8.  If the price of automobiles increases by 20%, what is the '
  'expected impact on the quantity supplied of automobiles?'),
 ('question',
  313,
  'The above diagram shows the supply curve for good Z.  According to the diagram, supply for good Y is',
  'The above diagram shows the supply curve for good Z.  According to the diagram, supply for good Z is'),
 ('question',
  572,
  'Assume that supply for a good is upward sloping and demand is downward sloping.  The imposition of a specific exise tax on the sale of '
  'that good would result in which of the following changes to equilibrium price and quantity?',
  'Assume that supply for a good is upward sloping and demand is downward sloping.  The imposition of a specific excise tax on the sale of '
  'that good would result in which of the following changes to equilibrium price and quantity?'),
 ('question',
  575,
  'Assume that the government increases the unit exise tax on alcohol suppliers and also at the same time, the demand for alcohol '
  'increases due to increases in stress levels at work.   As a result, equilibrium price and quantity of alcohol will most likely change '
  'in which of the following ways?',
  'Assume that the government increases the unit excise tax on alcohol suppliers and also at the same time, the demand for alcohol '
  'increases due to increases in stress levels at work.   As a result, equilibrium price and quantity of alcohol will most likely change '
  'in which of the following ways?'),
 ('question',
  579,
  'Assume that price elasticity of demand for good A is -0.3 and price elasticity of demand for good B is -2.5.  Assume goods A and B have '
  'identical demand curves.  If a per-unit excise tax of the same amount is imposed on both goods, which of the following is true?',
  'Assume that price elasticity of demand for good A is -0.3 and price elasticity of demand for good B is -2.5.  Assume goods A and B have '
  'identical supply curves.  If a per-unit excise tax of the same amount is imposed on both goods, which of the following is true?'),
 ('question',
  580,
  'Assume demand for cigarettes is inelastic and supply of cigarettes is elastic. If the government applies an exise tax on cigarettes, '
  'which of the following will occur in the short run?',
  'Assume demand for cigarettes is inelastic and supply of cigarettes is elastic. If the government applies an excise tax on cigarettes, '
  'which of the following will occur in the short run?'),
 ('question',
  594,
  'In the graph above, an exise tax has been imposed, moving supply from Supply to Supply + Tax.  Total consumer surplus after imposition '
  'of the tax is:',
  'In the graph above, an excise tax has been imposed, moving supply from Supply to Supply + Tax.  Total consumer surplus after imposition '
  'of the tax is:'),
 ('question',
  595,
  'In the graph above, an exise tax has been imposed, moving supply from Supply to Supply + Tax.  Total producer surplus after imposition '
  'of the tax is:',
  'In the graph above, an excise tax has been imposed, moving supply from Supply to Supply + Tax.  Total producer surplus after imposition '
  'of the tax is:'),
 ('question',
  665,
  'Assume that supply for a good is upward sloping and demand is downward sloping.  The imposition of a specific exise tax on the sale of '
  'that good would result in which of the following changes to equilibrium price and quantity?',
  'Assume that supply for a good is upward sloping and demand is downward sloping.  The imposition of a specific excise tax on the sale of '
  'that good would result in which of the following changes to equilibrium price and quantity?'),
 ('question',
  668,
  'Assume that the government increases the unit exise tax on alcohol suppliers and also at the same time, the demand for alcohol '
  'increases due to increases in stress levels at work.   As a result, equilibrium price and quantity of alcohol will most likely change '
  'in which of the following ways?',
  'Assume that the government increases the unit excise tax on alcohol suppliers and also at the same time, the demand for alcohol '
  'increases due to increases in stress levels at work.   As a result, equilibrium price and quantity of alcohol will most likely change '
  'in which of the following ways?'),
 ('question',
  672,
  'Assume that price elasticity of demand for good A is -0.3 and price elasticity of demand for good B is -2.5.  Assume goods A and B have '
  'identical demand curves.  If a per-unit excise tax of the same amount is imposed on both goods, which of the following is true?',
  'Assume that price elasticity of demand for good A is -0.3 and price elasticity of demand for good B is -2.5.  Assume goods A and B have '
  'identical supply curves.  If a per-unit excise tax of the same amount is imposed on both goods, which of the following is true?'),
 ('question',
  673,
  'Assume that supply of wheat is relatively price inelastic while demand for wheat is relatively price elastic.  If the government '
  'imposes a specific exise tax on the production of corn, the incidence of tax will fall',
  'Assume that supply of wheat is relatively price inelastic while demand for wheat is relatively price elastic.  If the government '
  'imposes a specific excise tax on the production of wheat, the incidence of tax will fall'),
 ('question',
  674,
  'Assume demand for cigarettes is inelastic and supply of cigarettes is elastic. If the government applies an exise tax on cigarettes, '
  'which of the following will occur in the short run?',
  'Assume demand for cigarettes is inelastic and supply of cigarettes is elastic. If the government applies an excise tax on cigarettes, '
  'which of the following will occur in the short run?'),
 ('question',
  689,
  'In the graph above, an exise tax has been imposed, moving supply from Supply to Supply + Tax.  Total consumer surplus after imposition '
  'of the tax is:',
  'In the graph above, an excise tax has been imposed, moving supply from Supply to Supply + Tax.  Total consumer surplus after imposition '
  'of the tax is:'),
 ('question',
  690,
  'In the graph above, an exise tax has been imposed, moving supply from Supply to Supply + Tax.  Total producer surplus after imposition '
  'of the tax is:',
  'In the graph above, an excise tax has been imposed, moving supply from Supply to Supply + Tax.  Total producer surplus after imposition '
  'of the tax is:'),
 ('question',
  698,
  'The above diagram shows the impact of a subsidy in the market for agricultural products in the EU.  What is the cost of financing the '
  'subsidy to government',
  'The above diagram shows the impact of a subsidy in the market for agricultural products in the EU.  What is the cost of financing the '
  'subsidy to government?'),
 ('question',
  711,
  "The diagram above depicts the supply and demand curves for a city's rental housing market.  If a price ceiling is imposed at P2, which "
  'of the followin gwill occur?',
  "The diagram above depicts the supply and demand curves for a city's rental housing market.  If a price ceiling is imposed at P2, which "
  'of the following will occur?')]


def _same_question(conn, a, b):
    rows = conn.execute(sa.text("SELECT id, text, image_url, topic_id, chapter_id FROM question WHERE id IN (:a, :b)"),
                        {"a": a, "b": b}).fetchall()
    if len(rows) != 2:
        return False
    x, y = rows
    return x[1:] == y[1:]


def upgrade():
    conn = op.get_bind()

    # 1. Remove the duplicate tax questions; move any student history to the copy that stays
    for old, keep in DEDUPE:
        if not _same_question(conn, old, keep):
            continue
        conn.execute(sa.text("UPDATE user_performance SET question_id = :keep WHERE question_id = :old"), {"keep": keep, "old": old})
        conn.execute(sa.text("DELETE FROM answer WHERE question_id = :old"), {"old": old})
        conn.execute(sa.text("DELETE FROM question WHERE id = :old"), {"old": old})

    # 1b. Remove questions that can't be fixed (and their answers and answer history)
    for qid, qtext in REMOVE:
        if conn.execute(sa.text("SELECT 1 FROM question WHERE id = :id AND text = :t"), {"id": qid, "t": qtext}).first() is None:
            continue
        conn.execute(sa.text("DELETE FROM user_performance WHERE question_id = :id"), {"id": qid})
        conn.execute(sa.text("DELETE FROM answer WHERE question_id = :id"), {"id": qid})
        conn.execute(sa.text("DELETE FROM question WHERE id = :id"), {"id": qid})

    # 2. Put answers back on the question they belong to
    for aid, frm, to in MOVES:
        conn.execute(sa.text("UPDATE answer SET question_id = :to WHERE id = :aid AND question_id = :frm"),
                     {"to": to, "aid": aid, "frm": frm})

    # 3. Text fixes (only where the text is still exactly the old version)
    for table, rid, old, new in TEXT:
        conn.execute(sa.text(f"UPDATE {table} SET text = :new WHERE id = :id AND text = :old"), {"new": new, "id": rid, "old": old})

    # 4. Answer key
    for aid, qid, old, new in CORRECT:
        conn.execute(sa.text("UPDATE answer SET is_correct = :new WHERE id = :aid AND question_id = :qid AND is_correct = :old"),
                     {"new": new, "aid": aid, "qid": qid, "old": old})

    # 5. Graphs
    for qid, old, new in IMAGES:
        conn.execute(sa.text("UPDATE question SET image_url = :new WHERE id = :qid AND image_url IS NOT DISTINCT FROM :old"),
                     {"new": new, "qid": qid, "old": old})


def downgrade():
    # Reverses steps 2-5. Removed questions (the exact duplicates and Q244) are not re-created.
    conn = op.get_bind()
    for qid, old, new in IMAGES:
        conn.execute(sa.text("UPDATE question SET image_url = :old WHERE id = :qid AND image_url IS NOT DISTINCT FROM :new"),
                     {"new": new, "qid": qid, "old": old})
    for aid, qid, old, new in CORRECT:
        conn.execute(sa.text("UPDATE answer SET is_correct = :old WHERE id = :aid AND question_id = :qid AND is_correct = :new"),
                     {"new": new, "aid": aid, "qid": qid, "old": old})
    for table, rid, old, new in TEXT:
        conn.execute(sa.text(f"UPDATE {table} SET text = :old WHERE id = :id AND text = :new"), {"new": new, "id": rid, "old": old})
    for aid, frm, to in MOVES:
        conn.execute(sa.text("UPDATE answer SET question_id = :frm WHERE id = :aid AND question_id = :to"),
                     {"to": to, "aid": aid, "frm": frm})
