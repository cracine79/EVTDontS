
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
    shiftsSupplyTopic = db.session.get(QuestionTopic, 13)
    shiftsSupplyChapter = db.session.get(Chapter, 11)
    sdeqTopic = db.session.get(QuestionTopic, 14)
    sdeqChapter = db.session.get(Chapter, 12)
    disequilibriumDemandShiftTopic = db.session.get(QuestionTopic, 15)
    disequilbriumSupplyShiftTopic = db.session.get(QuestionTopic, 16)
    disequilibriumChapter = db.session.get(Chapter, 13)
    

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
    
    question34 = Question(text='Which of the following would shift the supply curve for corn to the left?', chapter = shiftsSupplyChapter, topic=shiftsSupplyTopic)
    question35 = Question(text='Which of the following would NOT be expected to result in a shift of the supply curve of bicycles in the city of New York in the short run?', chapter = shiftsSupplyChapter, topic=shiftsSupplyTopic)
    question36 = Question(text='Which of the following would shift the short-run supply curve for blueberries?', chapter = shiftsSupplyChapter, topic=shiftsSupplyTopic)
    question37 = Question(text='A rightward shift in the supply curve of T-shirts could be caused by', chapter = shiftsSupplyChapter, topic=shiftsSupplyTopic)
    question38 = Question(text='An increase in the supply of tea could be caused by', chapter = shiftsSupplyChapter, topic=shiftsSupplyTopic)
    question39 = Question(text='When the supply curve shifts to the right (in a perfectly competitive market), this is an indication that', chapter = shiftsSupplyChapter, topic=shiftsSupplyTopic)
    question40 = Question(text='A leftward shift in the supply curve for wheat could be caused by', chapter=shiftsSupplyChapter, topic=shiftsSupplyTopic)
    question41 = Question(text='Which of the following events is likely to cause a rightward shift in the supply curve for electric cars?', chapter=shiftsSupplyChapter, topic=shiftsSupplyTopic)
    question42 = Question(text='What would cause a decrease in the supply of oranges?', chapter=shiftsSupplyChapter, topic=shiftsSupplyTopic)
    question43 = Question(text='Which of the following would shift the supply curve for laptops to the right?', chapter=shiftsSupplyChapter, topic=shiftsSupplyTopic)
    question44 = Question(text='An increase in the supply of oil is most likely caused by', chapter=shiftsSupplyChapter, topic=shiftsSupplyTopic)
    question45 = Question(text='Which of the following would NOT shift the supply curve for bananas in the short run?', chapter=shiftsSupplyChapter, topic=shiftsSupplyTopic)

    question46 = Question(text='The above table shows the supply and demand schedule for a perfectly competitive market.   It the price in the market, which of the following is expected?', chapter = sdeqChapter, topic = sdeqTopic, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/SDSchedule.png")
    question47 = Question(text='The above table shows the supply and demand schedule for a perfectly competitive market. At which price will a surplus of 250 units occur?', chapter = sdeqChapter, topic = sdeqTopic, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/SDSchedule.png")
    question48 = Question(text='The above graph shows the supply and demand curves for a perfectly competitive market.  If the price is $4 in the market, which of the following is expected to occur?', chapter = sdeqChapter, topic = sdeqTopic, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/SD1.png")
    question49 = Question(text='The above graph shows the supply and demand curves for a perfectly competitive market.  At which price will neither a shortage nor a surplus occur in the market?', chapter = sdeqChapter, topic = sdeqTopic, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/SD1.png")
    question50 = Question(text='The above graph shows the supply and demand curves for a perfectly competitive market.  The equilibrium price in the market is', chapter = sdeqChapter, topic = sdeqTopic, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/SD1.png")
    question51 = Question(text='If the price in a perfectly competitive market is currently below equilibrium price, which of the following is expected?', chapter = sdeqChapter, topic = sdeqTopic)
    question52 = Question(text='At a price of $5, the quantity demanded of sandwiches is 200 and the quantity supplied is 300.  Which of the following must be true?', chapter = sdeqChapter, topic = sdeqTopic)
    question53 = Question(text='The above graph shows the supply and demand curves for a perfectly competitive market.  If there currently is a surplus of 320 units in the market, what can be concluded?', chapter = sdeqChapter, topic = sdeqTopic, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/SD1.png")
    question54 = Question(text='The above graph shows the supply and demand curves for a perfectly competitive market.  What is the expected outcome if the current market price is $10', chapter = sdeqChapter, topic = sdeqTopic)
    question55 = Question(text='The above graph shows the supply and demand curves for a perfectly competitive market.  If there currently is a surplus in the market, which of the following is a possible market price?', chapter = sdeqChapter, topic = sdeqTopic)
    question56 = Question(text='At a price of $100, the quantity demanded of earrings is 500 and the quantity supplied is 300.  Which of the following must be true?', chapter = sdeqChapter, topic = sdeqTopic)
    question57 = Question(text='The above table shows the supply and demand schedule for a perfectly competitive market. If the market price is $2.50, what can be inferred about the market.', chapter = sdeqChapter, topic = sdeqTopic, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/SDSchedule2.png")
    question58 = Question(text='The above table shows the supply and demand schedule for a perfectly competitive market.  What is the expected outcome at a market price of $3?', chapter = sdeqChapter, topic = sdeqTopic, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/SDSchedule2.png")

    question59 = Question(text='Which of the following would most likely result in the decrease in demand for apples?', chapter=disequilibriumChapter, topic=disequilibriumDemandShiftTopic)
    question60 = Question(text='Assume that people like to eat bread with cheese.  If the price of bread decreased we would expect to see:', chapter=disequilibriumChapter, topic=disequilibriumDemandShiftTopic)
    question61 = Question(text='In a competitive market for baseballs, a change in the market caused equilibrium price and equilbrium quantity of baseballs to fall.  Which of the following changes could have caused this to happen?', chapter=disequilibriumChapter, topic=disequilibriumDemandShiftTopic)
    question62 = Question(text='Which of the following will NOT result in an increase in equilibrium price and equilibrium quantity in the market for corn?', chapter=disequilibriumChapter, topic=disequilibriumDemandShiftTopic)
    question63 = Question(text='If a large study reveals that eating dark chocolate reduces the risk of heart disease, which of the following is the most likely effect on the market for dark chocolate?', chapter=disequilibriumChapter, topic=disequilibriumDemandShiftTopic)
    question64 = Question(text='Which of the following could cause both the equilibrium price and quantity to increase in the market for electric vehicles?', chapter=disequilibriumChapter, topic=disequilibriumDemandShiftTopic)
    question65 = Question(text='Which of the following would NOT be expected to cause both the equilibrium price and quantity of energy drinks to rise?', chapter=disequilibriumChapter, topic=disequilibriumDemandShiftTopic)

    question66 = Question(text='An increase in the supply of haircuts in a competitive market would have what expected impact on the market?', chapter=disequilibriumChapter, topic=disequilbriumSupplyShiftTopic)
    question67 = Question(text='If the number of firms producing flip phones decreases from 8 firms to 3 firms, what would the expected impact on the market for flip phones be?', chapter=disequilibriumChapter, topic=disequilbriumSupplyShiftTopic)
    question68 = Question(text='If the market for Pokemon cards saw a simultaneous decrease in equilibrium price and increase in equilibirum quantity, this could have been caused by which of the following changes?', chapter=disequilibriumChapter, topic=disequilbriumSupplyShiftTopic)
    question69 = Question(text='Which of the following is NOT expected to result in an increase in equilibrium price and a decrease in the quantity consumed of paper plates', chapter=disequilibriumChapter, topic=disequilbriumSupplyShiftTopic)
    question70 = Question(text='A decrease in the supply of electric cars in the market would most likely result in which of the following outcomes?', chapter=disequilibriumChapter, topic=disequilbriumSupplyShiftTopic)
    question71 = Question(text='If the cost of producing chocolate bars decreases significantly, what would the expected impact on the chocolate bar market be?', chapter=disequilibriumChapter, topic=disequilbriumSupplyShiftTopic)
    question72 = Question(text='Which of the following is NOT expected to result in a decrease in equilibrium price and increase in equilibrium quantity in the market for bottled water?', chapter=disequilibriumChapter, topic=disequilbriumSupplyShiftTopic)
    question73 = Question(text='An increase in the equilibrium price and decrease in equilibrium quantity of airplane tickets could be caused by which of the following?', chapter=disequilibriumChapter, topic=disequilbriumSupplyShiftTopic)

    
    

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
                 question31, question32, question33,
                 question34, question35, question36, 
                 question37, question38, question39,
                 question40, question41, question42,
                 question43, question44, question45,
                 question46, question47, question48,
                 question49, question50, question51, 
                 question52, question53, question54,
                 question55, question56, question57,
                 question58, question59, question60, 
                 question61, question62, question63,
                 question64, question65, question66, 
                 question67, question68, question69,
                 question70, question71, question72, 
                 question73, ]

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

    answer34a = Answer(text='A decrease in consumer incomes', question=questions[33], is_correct=False)
    answer34b = Answer(text='A decrease in the price of corn', question=questions[33], is_correct=False)
    answer34c = Answer(text='A decrease in the wages of corn harvesting labor', question=questions[33], is_correct=False)
    answer34d = Answer(text='An increase in the rental price for corn harvesting equipment', question=questions[33], is_correct=True)
    answer34e = Answer(text='A decrease in the demand for cucumbers, a substitute in consumption', question=questions[33], is_correct=False)


    answer35a = Answer(text='An increase in the cost of steel required to manufacture bicycle frames', question=questions[34], is_correct=False)
    answer35b = Answer(text='A decrease in the cost of taking taxis, a substitute for bicycles', question=questions[34], is_correct=True)
    answer35c = Answer(text='A decrease in the number of firms producing bicycles in the city', question=questions[34], is_correct=False)
    answer35d = Answer(text='A decrease in business taxes on bicycle manufacturers', question=questions[34], is_correct=False)
    answer35e = Answer(text='An increase in subsidies provided to bicycle manufacturers', question=questions[34], is_correct=False)


    answer36a = Answer(text='An increase in the consumption of blueberries', question=questions[35], is_correct=False)
    answer36b = Answer(text='A decrease in the price of blueberries', question=questions[35], is_correct=False)
    answer36c = Answer(text='An increase in the cost of employing farmworkers used to pick blueberries', question=questions[35], is_correct=True)
    answer36d = Answer(text='A decrease in household incomes', question=questions[35], is_correct=False)
    answer36e = Answer(text='An announcement of a study showing the negative health impacts of eating blueberries', question=questions[35], is_correct=False)


    answer37a = Answer(text='a decrease in the price of T-shirts', question=questions[36], is_correct=False)
    answer37b = Answer(text='an increase in the price of T-shirts', question=questions[36], is_correct=False)
    answer37c = Answer(text='an increase in the population', question=questions[36], is_correct=False)
    answer37d = Answer(text='an increase in the cost of materials used to produce T-shirts', question=questions[36], is_correct=False)
    answer37e = Answer(text='an improvement in technology associated with manufacturing T-shirts', question=questions[36], is_correct=True)


    answer38a = Answer(text='a decrease in the cost of land needed to grow tea', question=questions[37], is_correct=True)
    answer38b = Answer(text='an increase in the price of cookies, a comlement to tea', question=questions[37], is_correct=False)
    answer38c = Answer(text='a decrease in consumer incomes', question=questions[37], is_correct=False)
    answer38d = Answer(text='a decrease in the demand for tea', question=questions[37], is_correct=False)
    answer38e = Answer(text='an increae in the price of tea', question=questions[37], is_correct=False)


    answer39a = Answer(text='firms will definitely increase their prices', question=questions[38], is_correct=False)
    answer39b = Answer(text='firms will definitely decrease their prices', question=questions[38], is_correct=False)
    answer39c = Answer(text='firms will sell less than before at whatever price is in the market', question=questions[38], is_correct=False)
    answer39d = Answer(text='firms will sell the same amount if possible', question=questions[38], is_correct=False)
    answer39e = Answer(text='firms will increase the quantity supplied at every possible market price', question=questions[38], is_correct=True)


    answer40a = Answer(text='A decrease in the cost of fertilizers used for wheat production', question=questions[39], is_correct=False)
    answer40b = Answer(text='A natural disaster damaging large areas of farmland', question=questions[39], is_correct=True)
    answer40c = Answer(text='An increase in subsidies for wheat farmers', question=questions[39], is_correct=False)
    answer40d = Answer(text='A decrease in the price of wheat', question=questions[39], is_correct=False)
    answer40e = Answer(text='An improvement in wheat harvesting technology', question=questions[39], is_correct=False)

    answer41a = Answer(text='An increase in the price of lithium used in batteries', question=questions[40], is_correct=False)
    answer41b = Answer(text='A decrease in labor costs for factory workers assembling electric cars', question=questions[40], is_correct=True)
    answer41c = Answer(text='A reduction in consumer demand for electric cars', question=questions[40], is_correct=False)
    answer41d = Answer(text='An increase in government regulations on electric car manufacturing', question=questions[40], is_correct=False)
    answer41e = Answer(text='A rise in electricity prices', question=questions[40], is_correct=False)

    answer42a = Answer(text='An improvement in irrigation technology for orange orchards', question=questions[41], is_correct=False)
    answer42b = Answer(text='A drought affecting major orange-producing regions', question=questions[41], is_correct=True)
    answer42c = Answer(text='A decrease in the price of pesticides used on orange trees', question=questions[41], is_correct=False)
    answer42d = Answer(text='A subsidy for farmers growing oranges', question=questions[41], is_correct=False)
    answer42e = Answer(text='A decrease in the price of oranges', question=questions[41], is_correct=False)

    answer43a = Answer(text='A tax increase on laptop manufacturers', question=questions[42], is_correct=False)
    answer43b = Answer(text='A decrease in the cost of skilled labor required for assembling laptops', question=questions[42], is_correct=True)
    answer43c = Answer(text='An increase in consumer incomes', question=questions[42], is_correct=False)
    answer43d = Answer(text='A decrease in the cost of transportation for laptops', question=questions[42], is_correct=False)
    answer43e = Answer(text='An increase in the price of laptops', question=questions[42], is_correct=False)

    answer44a = Answer(text='An increase in the efficiency of oil drilling technology', question=questions[43], is_correct=True)
    answer44b = Answer(text='A rise in the cost of oil drilling equipment', question=questions[43], is_correct=False)
    answer44c = Answer(text='A decrease in government subsidies for oil production', question=questions[43], is_correct=False)
    answer44d = Answer(text='A natural disaster affecting oil drilling regions', question=questions[43], is_correct=False)
    answer44e = Answer(text='An increase in the price of gasoline', question=questions[43], is_correct=False)

    answer45a = Answer(text='An improvement in the shipping logistics for bananas', question=questions[44], is_correct=False)
    answer45b = Answer(text='A decrease in the price of fertilizer used for banana plants', question=questions[44], is_correct=False)
    answer45c = Answer(text='A rise in demand for bananas due to a new diet trend', question=questions[44], is_correct=True)
    answer45d = Answer(text='A decrease in the wages of farmworkers harvesting bananas', question=questions[44], is_correct=False)
    answer45e = Answer(text='A favorable change in weather conditions for banana cultivation', question=questions[44], is_correct=False)

    answer46a = Answer(text='Market equilibrium', question=questions[45], is_correct=False)
    answer46b = Answer(text='A shortage of 250 units', question=questions[45], is_correct=True)
    answer46c = Answer(text='A surplus of 250 units', question=questions[45], is_correct=False)
    answer46d = Answer(text='A shortage of 500 units', question=questions[45], is_correct=False)
    answer46e = Answer(text='A surplus of 500 units', question=questions[45], is_correct=False)


    answer47a = Answer(text='$50', question=questions[46], is_correct=False)
    answer47b = Answer(text='$75', question=questions[46], is_correct=False)
    answer47c = Answer(text='$125', question=questions[46], is_correct=True)
    answer47d = Answer(text='$150', question=questions[46], is_correct=False)
    answer47e = Answer(text='No price will yield that result', question=questions[46], is_correct=False)

    answer48a = Answer(text='A shortage of 400 units', question=questions[47], is_correct=False)
    answer48b = Answer(text='A surplus of 400 units', question=questions[47], is_correct=False)
    answer48c = Answer(text='A shortage of 200 units', question=questions[47], is_correct=False)
    answer48d = Answer(text='A surplus of 200 units', question=questions[47], is_correct=True)
    answer48e = Answer(text='A shortage of $1', question=questions[47], is_correct=False)


    answer49a = Answer(text='$1', question=questions[48], is_correct=False)
    answer49b = Answer(text='$2', question=questions[48], is_correct=False)
    answer49c = Answer(text='$3', question=questions[48], is_correct=True)
    answer49d = Answer(text='$4', question=questions[48], is_correct=False)
    answer49e = Answer(text='$5', question=questions[48], is_correct=False)

    answer50a = Answer(text='Indeterminate, because there are many prices that could be charged in the market', question=questions[49], is_correct=False)
    answer50b = Answer(text='Less than $3, because $3 is the maximum consumers are willing to pay in this market', question=questions[49], is_correct=False)
    answer50c = Answer(text='Equal to $3, because $3 is the exact middle price in the market (halfway between $1 and $5)', question=questions[49], is_correct=False)
    answer50d = Answer(text='Equal to $3, because that is the price where quantity supplied equals quantity demanded', question=questions[49], is_correct=True)
    answer50e = Answer(text='Greater than $3, because no supplier will sell any output at a price less tahn $3', question=questions[49], is_correct=False)


    answer51a = Answer(text='A shortage in the market, which should put upward pressure on prices.', question=questions[50], is_correct=True)
    answer51b = Answer(text='A shortage in the market, which should downward pressure on prices', question=questions[50], is_correct=False)
    answer51c = Answer(text='A surplus in the market, which should put upward pressure on prices', question=questions[50], is_correct=False)
    answer51d = Answer(text='A surplus in the market, which should put downward pressure on prices', question=questions[50], is_correct=False)
    answer51e = Answer(text='A surplus in the market, which has no impact on market prices', question=questions[50], is_correct=False)

    answer52a = Answer(text='There is a shortage of sandwiches at a price of $5', question=questions[51], is_correct=False)
    answer52b = Answer(text='The equilibrium price of sandwiches is below $5', question=questions[51], is_correct=True)
    answer52c = Answer(text='The quantity of sandwiches sold will be 300', question=questions[51], is_correct=False)
    answer52d = Answer(text='At equilibrium, fewer than 200 sandiwches will be sold', question=questions[51], is_correct=False)
    answer52e = Answer(text='The sandwich market is in equilibrium', question=questions[51], is_correct=False)

    answer53a = Answer(text='The market could be in equilibrium', question=questions[52], is_correct=False)
    answer53b = Answer(text='Price is definitely below $3', question=questions[52], is_correct=False)
    answer53c = Answer(text='Price must be between $1 and $2', question=questions[52], is_correct=False)
    answer53d = Answer(text='Price must be between $3 and $4', question=questions[52], is_correct=False)
    answer53e = Answer(text='Price must be between $4 and $5', question=questions[52], is_correct=True)

    answer54a = Answer(text='A shortage of 200 units', question=questions[53], is_correct=True)
    answer54b = Answer(text='A shortage of 300 units', question=questions[53], is_correct=False)
    answer54c = Answer(text='A shortage of 500 units', question=questions[53], is_correct=False)
    answer54d = Answer(text='A surplus of 100 units', question=questions[53], is_correct=False)
    answer54e = Answer(text='A surplus of greater than 100 units', question=questions[53], is_correct=False)


    answer55a = Answer(text='$2.50', question=questions[54], is_correct=False)
    answer55b = Answer(text='$5.00', question=questions[54], is_correct=False)
    answer55c = Answer(text='$10.00', question=questions[54], is_correct=False)
    answer55d = Answer(text='$15.00', question=questions[54], is_correct=True)
    answer55e = Answer(text='None of the above', question=questions[54], is_correct=False)


    answer56a = Answer(text='There is a shortage of earrings at a price of $100', question=questions[55], is_correct=False)
    answer56b = Answer(text='The quantity sold of earrings will be 500', question=questions[55], is_correct=False)
    answer56c = Answer(text='At equilibrium, fewer than 500 earrings will be purchased', question=questions[55], is_correct=True)
    answer56d = Answer(text='The equilibrium price is above $100', question=questions[55], is_correct=True)
    answer56e = Answer(text='If the price of earrings falls, quantity supplied will also fall', question=questions[55], is_correct=False)

    answer57a = Answer(text='There is definitely a surplus in the market', question=questions[56], is_correct=False)
    answer57b = Answer(text='There is definitely a shortage in the market', question=questions[56], is_correct=True)
    answer57c = Answer(text='The market is in equilbrium', question=questions[56], is_correct=False)
    answer57d = Answer(text='The current price is above equilibrium price', question=questions[56], is_correct=False)
    answer57e = Answer(text='None of the above', question=questions[56], is_correct=False)

    answer58a = Answer(text='A shortage of 40 units', question=questions[57], is_correct=False)
    answer58b = Answer(text='A shortage of 30 units', question=questions[57], is_correct=False)
    answer58c = Answer(text='A surplus of 30 units', question=questions[57], is_correct=True)
    answer58d = Answer(text='A surplus of 70 units', question=questions[57], is_correct=False)
    answer58e = Answer(text='A surplus of 110 units', question=questions[57], is_correct=False)

    answer59a = Answer(text='The weather for growing apples is not as good as it was in previous years', question=questions[58], is_correct=False)
    answer59b = Answer(text='The price of oranges, a substitute for oranges, is higher than last year', question=questions[58], is_correct=False)
    answer59c = Answer(text='New medical studies show that if consuming apples can cause infertility and in some cases, temporary blindness, due to a new strain of apple worm', question=questions[58], is_correct=True)
    answer59d = Answer(text='Consumers income increase and apples are normal goods', question=questions[58], is_correct=False)
    answer59e = Answer(text='The price of peanut butter, a complement good for apples, falls.', question=questions[58], is_correct=False)


    answer60a = Answer(text='The price of cheese will fall and the quantity consumed of cheese will fall', question=questions[59], is_correct=False)
    answer60b = Answer(text='The price of cheese will rise and the quantity consumed of cheese will fall', question=questions[59], is_correct=False)
    answer60c = Answer(text='The price of cheese will fall and the quantity consumed of cheese will rise', question=questions[59], is_correct=False)
    answer60d = Answer(text='The price of cheese will rise and the quantity consumed of cheese will rise', question=questions[59], is_correct=True)
    answer60e = Answer(text='The quantity consumed of cheese will fall, but the price of cheese could rise or fall.', question=questions[59], is_correct=False)

    answer61a = Answer(text='More firms begin producing baseballs in the market', question=questions[60], is_correct=False)
    answer61b = Answer(text='The price of tennis balls, a substitute good for baseballs, increases', question=questions[60], is_correct=False)
    answer61c = Answer(text='Consumer incomes rise and baseballs are normal goods', question=questions[60], is_correct=False)
    answer61d = Answer(text='Consumers expect the price of baseballs to rise in the future', question=questions[60], is_correct=False)
    answer61e = Answer(text='The price of bats, a complement for baseballs, increases', question=questions[60], is_correct=True)

    answer62a = Answer(text='Record rainfall make the climate especially good for the growth of corn, doubling farmers output', question=questions[61], is_correct=True)
    answer62b = Answer(text='A Tiktok trend which takes the nation where teenagers try to buy as much corn as possible and eat it in one sitting. ', question=questions[61], is_correct=False)
    answer62c = Answer(text='An increase in the price of potatoes, a substitute for corn.', question=questions[61], is_correct=False)
    answer62d = Answer(text='Incomes fall, and corn is an inferior product', question=questions[61], is_correct=False)
    answer62e = Answer(text='The size of hte population doubles', question=questions[61], is_correct=False)

    answer63a = Answer(text='The equilibrium price will rise, and the equilibrium quantity will fall', question=questions[62], is_correct=False)
    answer63b = Answer(text='The equilibrium price will fall, and the equilibrium quantity will rise', question=questions[62], is_correct=False)
    answer63c = Answer(text='The equilibrium price and equilibrium quantity will both rise', question=questions[62], is_correct=True)
    answer63d = Answer(text='The equilibrium price and equilibrium quantity will both fall', question=questions[62], is_correct=False)
    answer63e = Answer(text='The equilibrium price will stay the same, but the equilibrium quantity will rise', question=questions[62], is_correct=False)

    answer64a = Answer(text='The price of gasoline, a substitute for electric vehicles, increases significantly', question=questions[63], is_correct=True)
    answer64b = Answer(text='Government subsidies for electric vehicle manufacturers decrease', question=questions[63], is_correct=False)
    answer64c = Answer(text='The cost of batteries for electric vehicles rises sharply', question=questions[63], is_correct=False)
    answer64d = Answer(text='A major recall decreases consumer confidence in electric vehicles', question=questions[63], is_correct=False)
    answer64e = Answer(text='The supply of electric vehicles increases due to new manufacturers entering the market', question=questions[63], is_correct=False)

    answer65a = Answer(text='An increase in the popularity of energy drinks among consumers', question=questions[64], is_correct=False)
    answer65b = Answer(text='A decrease in the price of coffee, a substitute for energy drinks', question=questions[64], is_correct=True)
    answer65c = Answer(text='A nationwide marketing campaign promoting energy drinks', question=questions[64], is_correct=False)
    answer65d = Answer(text='A decrease in consumer incomes, assuming energy drinks are normal goods', question=questions[64], is_correct=False)
    answer65e = Answer(text='An increase in the number of consumers in the market for energy drinks', question=questions[64], is_correct=False)
    
    answer66a = Answer(text='Price of haircuts and total quantity haircuts performed fall', question=questions[65], is_correct=False)
    answer66b = Answer(text='Price of haircuts and total quantity haircuts performed rise', question=questions[65], is_correct=False)
    answer66c = Answer(text='Price of haircuts rises and total quantity of haircuts performed falls', question=questions[65], is_correct=False)
    answer66d = Answer(text='Price of haircuts falls and total quantity of haircuts performed rises', question=questions[65], is_correct=True)
    answer66e = Answer(text='No change to price or quanitty of haircuts performed.', question=questions[65], is_correct=False)

    answer67a = Answer(text='Equilibrium price and quantity of flip phones both rise', question=questions[66], is_correct=False)
    answer67b = Answer(text='Equilibrium price and quantity of flip phones both fall', question=questions[66], is_correct=False)
    answer67c = Answer(text='Equilibrium price of flip phones rises and equilibrium quantity falls', question=questions[66], is_correct=True)
    answer67d = Answer(text='Equilibrium price of flip phones falls and equilibrium quantity rises', question=questions[66], is_correct=False)
    answer67e = Answer(text='Equilibrium price of flip phones is unchanged and equilibrium quantity rises', question=questions[66], is_correct=False)

    answer68a = Answer(text='A doubling in the total number of Pokemon cards printed and released to the market by the Pokemon manufacturers', question=questions[67], is_correct=True)
    answer68b = Answer(text='A holiday rush causes a spike in demand for Pokemn cards', question=questions[67], is_correct=False)
    answer68c = Answer(text='A rival colletor card - Jokedude cards cuts its prices in half', question=questions[67], is_correct=False)
    answer68d = Answer(text='Incomes fall and Pokemon cards are a luxury good', question=questions[67], is_correct=False)
    answer68e = Answer(text='A huge shipment of Pokemon cards is lost at sea when a container ship sinks en route from China, decreasing the available number of cards in the market by 40%', question=questions[67], is_correct=False)

    answer69a = Answer(text='An increase in the cost of paper pulp needed in the manufacture of paper plates', question=questions[68], is_correct=False)
    answer69b = Answer(text='An imposition of business taxes on the producers of paper plates by local government.', question=questions[68], is_correct=False)
    answer69c = Answer(text='A decrease in the total number of firms producing paper plates', question=questions[68], is_correct=False)
    answer69d = Answer(text='An intiative by local activists encouraging consumers to buy fewer paper plates', question=questions[68], is_correct=True)
    answer69e = Answer(text='In increase in the cost of labor employed in the production of paper plates', question=questions[68], is_correct=False)
    
    answer70a = Answer(text='Equilibrium price rises, and equilibrium quantity falls.', question=questions[69], is_correct=True)
    answer70b = Answer(text='Equilibrium price and equilibrium quantity both rise.', question=questions[69], is_correct=False)
    answer70c = Answer(text='Equilibrium price falls, and equilibrium quantity rises.', question=questions[69], is_correct=False)
    answer70d = Answer(text='Equilibrium price and equilibrium quantity both fall.', question=questions[69], is_correct=False)
    answer70e = Answer(text='No change in price or quantity.', question=questions[69], is_correct=False)

    answer71a = Answer(text='Equilibrium price and equilibrium quantity both fall.', question=questions[70], is_correct=False)
    answer71b = Answer(text='Equilibrium price rises, and equilibrium quantity falls.', question=questions[70], is_correct=False)
    answer71c = Answer(text='Equilibrium price falls, and equilibrium quantity rises.', question=questions[70], is_correct=True)
    answer71d = Answer(text='Equilibrium price and equilibrium quantity both rise.', question=questions[70], is_correct=False)
    answer71e = Answer(text='No change in price or quantity.', question=questions[70], is_correct=False)

    answer72a = Answer(text='Record rainfall increases the water supply available for bottling companies.', question=questions[71], is_correct=False)
    answer72b = Answer(text='Government decreases taxes on bottled water production.', question=questions[71], is_correct=False)
    answer72c = Answer(text='Record immigration doubles the labor force available for the production of bottled water.', question=questions[71], is_correct=False)
    answer72d = Answer(text='Three factories close, halving the supply of bottled water.', question=questions[71], is_correct=True)
    answer72e = Answer(text='Transportation costs for bottled water decrease significantly.', question=questions[71], is_correct=False)

    answer73a = Answer(text='A rise in fuel costs increases airline operating expenses.', question=questions[72], is_correct=True)
    answer73b = Answer(text='Airline companies experience record efficiency improvements in operations.', question=questions[72], is_correct=False)
    answer73c = Answer(text='An increase in subsidies for airlines lowers production costs.', question=questions[72], is_correct=False)
    answer73d = Answer(text='The number of competitors in the airline market increases significantly.', question=questions[72], is_correct=False)
    answer73e = Answer(text='Government reduces taxes on airline ticket sales.', question=questions[72], is_correct=False)

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
               answer33a, answer33b, answer33c, answer33d, answer33e, 
               answer34a, answer34b, answer34c, answer34d, answer34e,
               answer35a, answer35b, answer35c, answer35d, answer35e,
               answer36a, answer36b, answer36c, answer36d, answer36e,
               answer37a, answer37b, answer37c, answer37d, answer37e,
               answer38a, answer38b, answer38c, answer38d, answer38e,
               answer39a, answer39b, answer39c, answer39d, answer39e,
               answer40a, answer40b, answer40c, answer40d, answer40e,
               answer41a, answer41b, answer41c, answer41d, answer41e,
               answer42a, answer42b, answer42c, answer42d, answer42e,
               answer43a, answer43b, answer43c, answer43d, answer43e,
               answer44a, answer44b, answer44c, answer44d, answer44e,
               answer45a, answer45b, answer45c, answer45d, answer45e,
               answer46a, answer46b, answer46c, answer46d, answer46e,
               answer47a, answer47b, answer47c, answer47d, answer47e,
               answer48a, answer48b, answer48c, answer48d, answer48e,
               answer49a, answer49b, answer49c, answer49d, answer49e,
               answer50a, answer50b, answer50c, answer50d, answer50e,
               answer51a, answer51b, answer51c, answer51d, answer51e,
               answer52a, answer52b, answer52c, answer52d, answer52e,
               answer53a, answer53b, answer53c, answer53d, answer53e, 
               answer54a, answer54b, answer54c, answer54d, answer54e,
               answer55a, answer55b, answer55c, answer55d, answer55e,
               answer56a, answer56b, answer56c, answer56d, answer56e,
               answer57a, answer57b, answer57c, answer57d, answer57e,
               answer58a, answer58b, answer58c, answer58d, answer58e,
               answer59a, answer59b, answer59c, answer59d, answer59e,
               answer60a, answer60b, answer60c, answer60d, answer60e,
               answer61a, answer61b, answer61c, answer61d, answer61e,
               answer62a, answer62b, answer62c, answer62d, answer62e,
               answer63a, answer63b, answer63c, answer63d, answer63e,
               answer64a, answer64b, answer64c, answer64d, answer64e,
               answer65a, answer65b, answer65c, answer65d, answer65e,
               answer66a, answer66b, answer66c, answer66d, answer66e,
               answer67a, answer67b, answer67c, answer67d, answer67e,
               answer68a, answer68b, answer68c, answer68d, answer68e,
               answer69a, answer69b, answer69c, answer69d, answer69e,
               answer70a, answer70b, answer70c, answer70d, answer70e,
               answer71a, answer71b, answer71c, answer71d, answer71e,
               answer72a, answer72b, answer72c, answer72d, answer72e,
               answer73a, answer73b, answer73c, answer73d, answer73e,]

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