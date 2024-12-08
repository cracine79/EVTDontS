
from exts import db
from main import create_app
from config import ProdConfig
from models import Chapter, QuestionTopic, Unit, Question, Answer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

app = create_app(ProdConfig)

def seed_unit2_questions():
    print('Seeding Unit 2 Questions')
    
    demandCurveTopic = db.session.get(QuestionTopic,10)
    demandChapter = db.session.get(Chapter, 8)
    shiftsDemandTopic = db.session.get(QuestionTopic,11)
    shiftsDemandChapter = db.session.get(Chapter, 9)
    supplyCurveTopic = db.session.get(QuestionTopic,12)
    supplyChapter = db.session.get(Chapter, 10)
    

    question1 = Question(text="Which of the following occurs as a result of the substitution effect of a decrease in the price of a normal good?", chapter=demandChapter, topic=demandCurveTopic)
    question2 = Question(text = "The table above lists the monthly individual demahd schedules for pizza for the only three buyers in the market, April, Bob and Charlie.  Which of the following combinations of price and quantity lies on the demand curve?", chapter=demandChapter, topic=demandCurveTopic, image_url="https://evtds-seeds.s3.us-east-2.amazonaws.com/Screenshot+2024-11-14+at+8.14.41+PM.png")
    question3 = Question(text="The graphs above show the individual demand curves for two consumers, Wes and Wyatt, in the market for salted peanuts.  As the price of salted peanuts decreases from $10 to $4, now does the quantity demanded change along the market demand curve?",  chapter=demandChapter, topic=demandCurveTopic, image_url="https://evtds-seeds.s3.us-east-2.amazonaws.com/WWDemands.png")
    question4 = Question(text="For normal goods, the income effect of a price change refers to the change in the consumption of the good that takes place as a result of:", chapter=demandChapter, topic=demandCurveTopic)
    question5 = Question(text="Which of the following can be used to explain why the demand curve for a normal good is downward sloping?", chapter=demandChapter, topic=demandCurveTopic)
    question6 = Question(text="Which of the following most accurately defines the economic concept of demand?", chapter=demandChapter, topic=demandCurveTopic)
    question7 = Question(text="Assume that pizza is a normal good.  If the price of pizza incerases, the substitution efefc and income effect will lead to which of the following changes in pizza consumption?", chapter=demandChapter, topic=demandCurveTopic)
    question8 = Question(text="The above graphs show Frank's demand for hot dogs and Sam's demand for hot dogs.  Suppose Frank and Sam are the only two consumers in the market.  Which of the following is a point on the market demand curve for hot dogs?", chapter=demandChapter, topic=demandCurveTopic, image_url="https://evtds-seeds.s3.us-east-2.amazonaws.com/HDDemands.png")
    question9 = Question(text="According to the law of demand, an increase in the price of peanut butter will result in", chapter=demandChapter, topic=demandCurveTopic)
    question10 = Question(text="Which of the following best describes the law of demand?", chapter=demandChapter, topic=demandCurveTopic)
    question11 = Question(text="All of the following cause a leftward shift in the demand for a normal good EXCEPT", chapter=shiftsDemandChapter, topic=shiftsDemandTopic)
    question12 = Question(text="Jake consumes both pizza and hamburgers.  For Jake, pizza is a normal good, and hamburgers are an inferior good.  If Jake's income increases, which of the following will be the immediate impact on his consumption?", chapter=shiftsDemandChapter, topic=shiftsDemandTopic)
    question13 = Question(text="An increase in the price of good X results in a decrease in the quantity demanded of good Y.  It can be inferred that good X and good Y are:" , chapter=shiftsDemandChapter, topic=shiftsDemandTopic)
    question14 = Question(text="When consumers experience a decrease in income, this causes the demand curve for inferior goods to:", chapter=shiftsDemandChapter, topic=shiftsDemandTopic)
    question15 = Question(text="Which of the following will cause the demand curve for good A to shift to the right?", chapter=shiftsDemandChapter, topic=shiftsDemandTopic)
    question16 = Question(text="Which of the following will most likely happen if the market for good Z if the price of good Z increases?", chapter=shiftsDemandChapter, topic=shiftsDemandTopic)
    question17 = Question(text="If good X is a normal good and consumer incomes increase, which of the following is most likely to happen to the demand for good X?", chapter=shiftsDemandChapter, topic=shiftsDemandTopic)
    question18 = Question(text="If the price of good A increases and good B is a substitute for good A, what will happen to the demand for good B?", chapter=shiftsDemandChapter, topic=shiftsDemandTopic)
    question19 = Question(text="A decrease in the price of good C, a complement to good D, will cause which of the following changes in the demand for good D?", chapter=shiftsDemandChapter, topic=shiftsDemandTopic)
    question20 = Question(text="If a new study shows that consuming good Y has significant health benefits, how will this likely affect the demand for good Y?", chapter=shiftsDemandChapter, topic=shiftsDemandTopic)
    question21 = Question(text="An increase in the population of a city is most likely to affect the demand for which of the following goods?", chapter=shiftsDemandChapter, topic=shiftsDemandTopic)
    question22 = Question(text="Which of the following will most likely result from a decrease in the price of good Z, a normal good?", chapter=shiftsDemandChapter, topic=shiftsDemandTopic)
    question23 = Question(text="If the price of a good increases, which of the following would be expected in the market?", chapter = supplyChapter, topic=supplyCurveTopic)
    question24 = Question(text="Which of the following explains why supply is assumed to be upward sloping?", chapter = supplyChapter, topic=supplyCurveTopic)
    question25 = Question(text='According to the law of supply, what would we expect to see happen in the market if the price of salty snacks that firms can sell their product at decreases?', chapter = supplyChapter, topic=supplyCurveTopic)
    question26 = Question(text="The entire market for chairs in Shermer, Illinois consists of two firms, Firm A and Firm B.  Each firm's supply curve is shown above.  Given the supply curves, which of the following point is on the market supply curve?", chapter = supplyChapter, topic=supplyCurveTopic, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/TwoSupplyCurves_3.png")
    question27 = Question(text='The law of supply is best illustrated by which of the following examples?', chapter = supplyChapter, topic=supplyCurveTopic)
    question28 = Question(text='Supply is most accurately defined by which of the following?', chapter = supplyChapter, topic=supplyCurveTopic)
    question29 = Question(text="According to the law of supply, what would we expect to happen if the price of a good increases?", chapter=supplyChapter, topic=supplyCurveTopic)
    question30 = Question(text="Which of the following best describes the supply curve?", chapter=supplyChapter, topic=supplyCurveTopic)
    question31 = Question(text="The market for pencils in the town of Springfield consists of three firms. Each firm’s supply table is shown above. Based on this information, what point is on the market supply curve?", chapter=supplyChapter, topic=supplyCurveTopic, image_url="https://evtds-seeds.s3.us-east-2.amazonaws.com/ThreeFIrmSupplyTable.png")
    question32 = Question(text='When the price of wine increases in the market, firms are observed to increase their production of wine in the following year.  This phenomenon best illustrates which economic concept?', chapter=supplyChapter, topic=supplyCurveTopic)
    question33 = Question(text='The law of supply can be used to explain which of the following: \n\n I. The upward slope of the supply curve.  \n II.  Why firms are expected to produce more when prices increase. \n III. Why consumers will buy less of a good when prices increase', chapter=supplyChapter, topic=supplyCurveTopic)

    questions = [question1, question2, question3, 
                 question4, question5, question6, 
                 question7, question8, question9,
                 question10, question11, question12,
                 question13, question14, question15,
                 question16, question17, question18,
                 question19, question20, question21, 
                 question22, question23, question24,
                 question25, question26, question27,
                 question28, question29, question30, 
                 question31, question32, question33]

    print("questions created")
    db.session.add_all(questions)
    print("questions added")
    db.session.commit()
    return questions

def seed_answers(questions):
    answer1a = Answer(text="The demand for a complementary good will decrease", question=questions[0], is_correct=False)
    answer1b = Answer(text="The demand for a substitute good will decrease", question=questions[0], is_correct=False)
    answer1c = Answer(text="No change is exected as a result of the substitution effect", question=questions[0], is_correct=False)
    answer1d = Answer(text="Quantity demanded increases as the good is now cheaper relative to other substitute goods", question=questions[0], is_correct=True)
    answer1e = Answer(text="Quantity demanded decreases as the good is now more expensive relative to other substitute goods", question=questions[0], is_correct=False)

    answer2a = Answer(text="Price: $5, Quantity: 10", question=questions[1], is_correct=False)    
    answer2b = Answer(text="Price: $10, Quantity: 9", question=questions[1], is_correct=False)
    answer2c = Answer(text="Price: $15, Quantity: 12", question=questions[1], is_correct=True)
    answer2d = Answer(text="Price: $20, Quantity: 5", question=questions[1], is_correct=False)
    answer2e = Answer(text="Price: $25, Quantity: 0", question=questions[1], is_correct=False)

    answer3a = Answer(text="It increases from 1 to 14 units", question=questions[2], is_correct=False)
    answer3b = Answer(text="It increases from 10 to 14 units", question=questions[2], is_correct=False)
    answer3c = Answer(text="It increases from 4 to 6 units", question=questions[2], is_correct=False)
    answer3d = Answer(text="It increases from 4 to 8 units", question=questions[2], is_correct=False)
    answer3e = Answer(text="It increases from 4 to 10 units", question=questions[2], is_correct=True)
 
    answer4a = Answer(text="Consumers' purchasing power", question=questions[3], is_correct=True)
    answer4b = Answer(text="Demand for a complement good", question=questions[3], is_correct=False)
    answer4c = Answer(text="Quantity supplied of the good", question=questions[3], is_correct=False)
    answer4d = Answer(text="Inflation", question=questions[3], is_correct=False)
    answer4e = Answer(text="The marginal benefit", question=questions[3], is_correct=False)

    answer5a = Answer(text="The income effect and substitution effect cause quantity demanded to move in the same direction", question=questions[4], is_correct=True)
    answer5b = Answer(text="The substitution effect moves the quanitty demanded in the opposite direction than the substitution effect", question=questions[4], is_correct=False)
    answer5c = Answer(text="The substitution effect is dominated by the income effect", question=questions[4], is_correct=False)
    answer5d = Answer(text="The income effect is dominated by the substitution effect", question=questions[4], is_correct=False)
    answer5e = Answer(text="With an increase in income, the consumer decreases consumption of the good", question=questions[4], is_correct=False)

    answer6a = Answer(text="The total quantity of a good that consumers want to buy at a specific point in time", question=questions[5], is_correct=False)
    answer6b = Answer(text="The quantity of a good people would buy if they had zero budget constraint", question=questions[5], is_correct=False)
    answer6c = Answer(text="The total quantity of a good a person or people will buy at different prices", question=questions[5], is_correct=True)
    answer6d = Answer(text="How badly people want to buy a particular product or service", question=questions[5], is_correct=False)
    answer6e = Answer(text="The total quantity that firms will sell at a given time", question=questions[5], is_correct=False)

    answer7a = Answer(text="Substitution Effect: Increase, Income Effect: No Change", question=questions[6], is_correct=False)
    answer7b = Answer(text="Substitution Effect: Increase, Income Effect, Decrease ", question=questions[6], is_correct=False)
    answer7c = Answer(text="Substitution Effect: Decrease, Income Effect, No Change", question=questions[6], is_correct=False)
    answer7d = Answer(text="Substitution Effect: Decrease, Income Effect, Decrease", question=questions[6], is_correct=True)
    answer7e = Answer(text="Substitution Effect: Decrease, Income Effecxt: Increase", question=questions[6], is_correct=False)

    answer8a = Answer(text="Price: 2, Quantity: 12", question=questions[7], is_correct=False)
    answer8b = Answer(text="Price: 4, Quantity: 6", question=questions[7], is_correct=False)
    answer8c = Answer(text="Price: 6, Quantity: 4", question=questions[7], is_correct=True)
    answer8d = Answer(text="Price: 9, Quantity: 2", question=questions[7], is_correct=False)
    answer8e = Answer(text="Price: 10, Quantity: 5", question=questions[7], is_correct=False)

    answer9a = Answer(text="The demand curve for peanut butter getting steeper", question=questions[8], is_correct=False)
    answer9b = Answer(text="The demand curve for peanut butter getting flatter", question=questions[8], is_correct=False)
    answer9c = Answer(text="a decrease in the demand for almond butter, a substitute good.", question=questions[8], is_correct=False)
    answer9d = Answer(text="a decrease in the quanitty of peanut butter demanded", question=questions[8], is_correct=True)
    answer9e = Answer(text="an increase in the quanitty of peanut butter supplied", question=questions[8], is_correct=False)

    answer10a = Answer(text="When the price of a good falls, the quantity demanded increases", question=questions[9], is_correct=True)
    answer10b = Answer(text="Demand is met buy Supply", question=questions[9], is_correct=False)
    answer10c = Answer(text="When the price of a good rises, its demand decreases", question=questions[9], is_correct=False)
    answer10d = Answer(text="The price of a good increases when the supply of the good increases", question=questions[9], is_correct=False)
    answer10e = Answer(text="The price of a good decreases when the demand for the good decreases", question=questions[9], is_correct=False)

    answer11a = Answer(text='An increase in the price of the good', question=questions[10], is_correct=True)
    answer11b = Answer(text='An increase in the price of a complementary good', question=questions[10], is_correct=False)
    answer11c = Answer(text='A decrease in the price of a substitute good', question=questions[10], is_correct=False)
    answer11d = Answer(text='A decrease in consumer income', question=questions[10], is_correct=False)
    answer11e = Answer(text='A decrease in consumer preference for the good', question=questions[10], is_correct=False)
    
    answer12a = Answer(text='Pizza: Increase, Hamburger: Increase', question=questions[11], is_correct=False)
    answer12b = Answer(text='Pizza: Increase, Hamburger: No Change', question=questions[11], is_correct=False)
    answer12c = Answer(text='Pizza: No Change, Hamburger: Increase', question=questions[11], is_correct=False)
    answer12d = Answer(text='Pizza: Increase, Hamburger: Decrease', question=questions[11], is_correct=True)
    answer12e = Answer(text='Pizza: Decrease, Hamburger: Increase', question=questions[11], is_correct=False)

    answer13a = Answer(text='Inferior Goods', question=questions[12], is_correct=False)
    answer13b = Answer(text='Normal Goods', question=questions[12], is_correct=False)
    answer13c = Answer(text='Complement Goods', question=questions[12], is_correct=True)
    answer13d = Answer(text='Substitute Goods', question=questions[12], is_correct=False)
    answer13e = Answer(text='Veblen Goods', question=questions[12], is_correct=False)

    answer14a = Answer(text='Shift Down', question=questions[13], is_correct=False)
    answer14b = Answer(text='Shift to the left', question=questions[13], is_correct=False)
    answer14c = Answer(text='Shift to the right', question=questions[13], is_correct=True)
    answer14d = Answer(text='Become steeper', question=questions[13], is_correct=False)
    answer14e = Answer(text='Become flatter', question=questions[13], is_correct=False)

    answer15a = Answer(text='A decrease in the price of good B, a substitute for good A', question=questions[14], is_correct=False)
    answer15b = Answer(text='An decrease in the price of good C, a complement for good A', question=questions[14], is_correct=True)
    answer15c = Answer(text='A decrease in consumer income and good A is a normal good', question=questions[14], is_correct=False)
    answer15d = Answer(text='A decrease in the price of good A', question=questions[14], is_correct=False)
    answer15e = Answer(text='An increase in the price of good A', question=questions[14], is_correct=False)

    answer16a = Answer(text='The demand for good Z will increase', question=questions[15], is_correct=False)
    answer16b = Answer(text='The demand for good Z will decrease', question=questions[15], is_correct=False)
    answer16c = Answer(text='The quantity demanded of good Z will increase', question=questions[15], is_correct=False)
    answer16d = Answer(text='The quantity demanded of good Z will decrease', question=questions[15], is_correct=True)
    answer16e = Answer(text='The demand for good Z will possibly increase or decrease, but not stay the same', question=questions[15], is_correct=False)

    answer17a = Answer(text='The demand for good X will increase', question=questions[16], is_correct=True)
    answer17b = Answer(text='The demand for good X will decrease', question=questions[16], is_correct=False)
    answer17c = Answer(text='The quantity demanded of good X will decrease', question=questions[16], is_correct=False)
    answer17d = Answer(text='The quantity demanded of good X will stay the same', question=questions[16], is_correct=False)
    answer17e = Answer(text='The demand for good X will shift to the left', question=questions[16], is_correct=False)

    answer18a = Answer(text='The demand for good B will increase', question=questions[17], is_correct=True)
    answer18b = Answer(text='The demand for good B will decrease', question=questions[17], is_correct=False)
    answer18c = Answer(text='The demand for good A will increase', question=questions[17], is_correct=False)
    answer18d = Answer(text='The quantity demanded of good A will stay the same', question=questions[17], is_correct=False)
    answer18e = Answer(text='The demand for good B will shift to the left', question=questions[17], is_correct=False)

    answer19a = Answer(text='The demand for good D will increase', question=questions[18], is_correct=True)
    answer19b = Answer(text='The demand for good D will decrease', question=questions[18], is_correct=False)
    answer19c = Answer(text='The quantity demanded of good C will decrease', question=questions[18], is_correct=False)
    answer19d = Answer(text='The demand for good D will stay the same', question=questions[18], is_correct=False)
    answer19e = Answer(text='The demand for good D will shift to the left', question=questions[18], is_correct=False)

    answer20a = Answer(text='The demand for good Y will increase', question=questions[19], is_correct=True)
    answer20b = Answer(text='The demand for good Y will decrease', question=questions[19], is_correct=False)
    answer20c = Answer(text='The quantity demanded of good Y will decrease', question=questions[19], is_correct=False)
    answer20d = Answer(text='The demand for good Y will stay the same', question=questions[19], is_correct=False)
    answer20e = Answer(text='The demand for good Y will shift to the left', question=questions[19], is_correct=False)

    answer21a = Answer(text='Demand for housing will increase', question=questions[20], is_correct=True)
    answer21b = Answer(text='Demand for housing will decrease', question=questions[20], is_correct=False)
    answer21c = Answer(text='Demand for housing will stay the same', question=questions[20], is_correct=False)
    answer21d = Answer(text='Demand for unrelated goods will decrease', question=questions[20], is_correct=False)
    answer21e = Answer(text='Demand for housing will shift to the left', question=questions[20], is_correct=False)

    answer22a = Answer(text='The demand for good Z will increase', question=questions[21], is_correct=True)
    answer22b = Answer(text='The demand for good Z will decrease', question=questions[21], is_correct=False)
    answer22c = Answer(text='The quantity demanded of good Z will decrease', question=questions[21], is_correct=False)
    answer22d = Answer(text='The demand for good Z will stay the same', question=questions[21], is_correct=False)
    answer22e = Answer(text='The demand for good Z will shift to the left', question=questions[21], is_correct=False)

    answer23a = Answer(text='The quantity supplied of the good will decrease', question=questions[22], is_correct=True)
    answer23b = Answer(text='The quantity demanded of the good will decrease', question=questions[22], is_correct=False)
    answer23c = Answer(text='The quantity supplied of the good will increase', question=questions[22], is_correct=False)
    answer23d = Answer(text='The demand for the good will increase', question=questions[22], is_correct=False)
    answer23e = Answer(text='The demand for the good will decrease', question=questions[22], is_correct=False)
    
    answer24a = Answer(text='Firms will buy fewer inputs if the price of their output increases', question=questions[23], is_correct=False)
    answer24b = Answer(text='Firms will produce less if workers are more expensive to employ', question=questions[23], is_correct=False)
    answer24c = Answer(text='Firms will increase price if the quantity supplied in the market increases', question=questions[23], is_correct=False)
    answer24d = Answer(text='Firms will increase quantity supplied if the market price increases', question=questions[23], is_correct=True)
    answer24e = Answer(text='Consumers will buy less if the price increases', question=questions[23], is_correct=False)
 
    answer25a = Answer(text='More firms will leave the market in the short run because the price is lower, benefiting firms that remain', question=questions[24], is_correct=False)
    answer25b = Answer(text='More firms will enter the market in the short run because the price is lower so they will want to sell more', question=questions[24], is_correct=False)
    answer25c = Answer(text='More firms still try to make and sell as many as possible, and consumers will buy more', question=questions[24], is_correct=False)
    answer25d = Answer(text='Firms will reduce the quantity they prouduce and sell, decreasing the total quantity supplied in the market', question=questions[24], is_correct=True)
    answer25e = Answer(text='The answer depends whether or not the good is an inferior good', question=questions[24], is_correct=False)
    
    answer26a = Answer(text='Price: $1, Quantity Supplied: 150', question=questions[25], is_correct=False)
    answer26b = Answer(text='Price: $2, Quantity Supplied: 450', question=questions[25], is_correct=True)
    answer26c = Answer(text='Price: $3, Quantity Supplied: 600', question=questions[25], is_correct=False)
    answer26d = Answer(text='Price: $4, Quantity Supplied: 1600', question=questions[25], is_correct=False)
    answer26e = Answer(text='None of the above', question=questions[25], is_correct=False)

    answer27a = Answer(text='The price of apples fall, so apple manufacturers reduce the total amount of apples they grow that year', question = questions[26], is_correct=True)
    answer27b = Answer(text='The price of tea increases, so tea farmers grow less that year because they can sell fewer units of tea and still make the same amount total revenue.', question = questions[26], is_correct=False)
    answer27c = Answer(text='The price of cars falls so more people buy cars', question = questions[26], is_correct=False)
    answer27d = Answer(text='When more pizza restaurants open, this causes the price of pizza in the market to fall.', question = questions[26], is_correct=False)
    answer27e = Answer(text='If there are fewer companies producing Blu-Ray players, the total amount of Blu-Ray players supplied in the market falls.', question = questions[26], is_correct=False)
    
    answer28a = Answer(text='The total amount of product for sale in the market at a given time.', question=questions[27], is_correct=False)
    answer28b = Answer(text='The process by which firms sell their product to consumers.', question=questions[27], is_correct=False)
    answer28c = Answer(text='The relationship between the possible prices of a good in the market and the total quantity supplied by a firm or firms at those prices', question=questions[27], is_correct=True)
    answer28d = Answer(text='The total capital value of all firms in a particular industry', question=questions[27], is_correct=False)
    answer28e = Answer(text='The total amount of product that is sold and purchased in a year', question=questions[27], is_correct=False)
    
    answer29a = Answer(text="The quantity supplied will decrease.", question=questions[28], is_correct=False)
    answer29b = Answer(text="The quantity supplied will increase.", question=questions[28], is_correct=True)
    answer29c = Answer(text="The quantity demanded will increase.", question=questions[28], is_correct=False)
    answer29d = Answer(text="The quantity demanded will decrease.", question=questions[28], is_correct=False)
    answer29e = Answer(text="The market price will stabilize.", question=questions[28], is_correct=False)

    answer30a = Answer(text="It slopes downward from left to right.", question=questions[29], is_correct=False)
    answer30b = Answer(text="It slopes upward from left to right.", question=questions[29], is_correct=True)
    answer30c = Answer(text="It is a straight vertical line.", question=questions[29], is_correct=False)
    answer30d = Answer(text="It is a straight horizontal line.", question=questions[29], is_correct=False)
    answer30e = Answer(text="It slopes downward from right to left.", question=questions[29], is_correct=False)

    answer31a = Answer(text="Price: $50, Quantity Supplied: 1000", question=questions[30], is_correct=False)
    answer31b = Answer(text="Price: $75, Quantity Supplied: 1300", question=questions[30], is_correct=False)
    answer31c = Answer(text="Price: $100, Quantity Supplied: 1500", question=questions[30], is_correct=True)
    answer31d = Answer(text="Price: $125, Quantity Supplied: 1700", question=questions[30], is_correct=False)
    answer31e = Answer(text="Price: $150, Quantity Supplied: 2000", question=questions[30], is_correct=False)

    answer32a = Answer(text='The theory of comparative advantage', question=questions[31], is_correct=False)
    answer32b = Answer(text='The theory of absolute advantage', question=questions[31], is_correct=False)
    answer32c = Answer(text='The law of Demand', question=questions[31], is_correct=False)
    answer32d = Answer(text='The law of Supply', question=questions[31], is_correct=True)
    answer32e = Answer(text='The law of diminishing marginal returns', question=questions[31], is_correct=False)

    answer33a = Answer(text='I only', question=questions[32], is_correct=False)
    answer33b = Answer(text='II only', question=questions[32], is_correct=False)
    answer33c = Answer(text='III only', question=questions[32], is_correct=False)
    answer33d = Answer(text='I and II', question=questions[32], is_correct=True)
    answer33e = Answer(text='I, II and III', question=questions[32], is_correct=False)

    answers = [answer1a, answer1b, answer1c, answer1e, answer1d,
               answer2a, answer2b, answer2c, answer2e, answer2d,
               answer3a, answer3b, answer3c, answer3d, answer3e,
               answer4a, answer4b, answer4c, answer4d, answer4e,
               answer5a, answer5b, answer5c, answer5d, answer5e,
               answer6a, answer6b, answer6c, answer6d, answer6e,
               answer7a, answer7b, answer7c, answer7d, answer7e,
               answer8a, answer8b, answer8c, answer8d, answer8e,
               answer9a, answer9b, answer9c, answer9d, answer9e,
               answer10a, answer10b, answer10c, answer10d, answer10e,
               answer11a, answer11b, answer11c, answer11d, answer11e,
               answer12a, answer12b, answer12c, answer12d, answer12e,
               answer13a, answer13b, answer13c, answer13d, answer13e,
               answer14a, answer14b, answer14c, answer14d, answer14e,
               answer15a, answer15b, answer15c, answer15d, answer15e,
               answer16a, answer16b, answer16c, answer16d, answer16e,
               answer17a, answer17b, answer17c, answer17d, answer17e,
               answer18a, answer18b, answer18c, answer18d, answer18e,
               answer19a, answer19b, answer19c, answer19d, answer19e,
               answer20a, answer20b, answer20c, answer20d, answer20e,
               answer21a, answer21b, answer21c, answer21d, answer21e,
               answer22a, answer22b, answer22c, answer22d, answer22e,
               answer23a, answer23b, answer23c, answer23d, answer23e,
               answer24a, answer24b, answer24c, answer24d, answer24e,
               answer25a, answer25b, answer25c, answer25d, answer25e,
               answer26a, answer26b, answer26c, answer26d, answer26e,
               answer27a, answer27b, answer27c, answer27d, answer27e,
               answer28a, answer28b, answer28c, answer28d, answer28e,
               answer29a, answer29b, answer29c, answer29d, answer29e,
               answer30a, answer30b, answer30c, answer30d, answer30e,
               answer31a, answer31b, answer31c, answer31d, answer31e,
               answer32a, answer32b, answer32c, answer32d, answer32e,
               answer33a, answer33b, answer33c, answer33d, answer33e, ]

    db.session.add_all(answers)
    db.session.commit()

def main():
    with app.app_context():
        unit2_questions = seed_unit2_questions()
        seed_answers(unit2_questions)


if __name__=="__main__":
    try:
        main()
    except IntegrityError:
        db.session.rollback()
        print("There was an error seeding the database")