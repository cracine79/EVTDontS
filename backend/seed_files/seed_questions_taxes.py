from exts import db
from main import create_app
from config import ProdConfig
from models import Chapter, QuestionTopic, Unit, Question, Answer
from sqlalchemy.exc import IntegrityError

app = create_app(ProdConfig)

def seed_tax_chapter():
    print('seeding chapter')

    chapter4_1 = db.session.get(Chapter, 35)

    topic34 = db.session.get(QuestionTopic, 75)
    topic35 = db.session.get(QuestionTopic, 77)
    topic36 = db.session.get(QuestionTopic, 78)
    topic37 = db.session.get(QuestionTopic, 76)


    question1 = Question(text='Assume that supply for a good is upward sloping and demand is downward sloping.  The imposition of a specific exise tax on the sale of that good would result in which of the following changes to equilibrium price and quantity?', chapter=chapter4_1, topic=topic34)
    question2 = Question(text='The diagram above shows the effect of a unit tax placed on a good.  What is the price paid by consumers and price received by producers after the tax is paid?', chapter=chapter4_1, topic=topic34, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/TaxCalcDiagram.png")
    question3 = Question(text='The diagram above shows the effect of a unit tax placed on a good.  According to the diagram, what is the dollar amount of the unit tax?', chapter=chapter4_1, topic=topic34, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/TaxCalcDiagram.png")
    question4 = Question(text='Assume that the government increases the unit exise tax on alcohol suppliers and also at the same time, the demand for alcohol increases due to increases in stress levels at work.   As a result, equilibrium price and quantity of alcohol will most likely change in which of the following ways?', chapter=chapter4_1, topic=topic34)
    question5 = Question(text="Assume supply of electric vehicles is upward sloping and demand is downward sloping.  An imposition of a specific tax on suppliers of electric vehicles would result in which of the following?", chapter=chapter4_1, topic=topic34)
    question6 = Question(text='The diagram above shows the effect of a unit tax placed on a good.  What is the price paid by consumers and price received by producers after the tax is paid?', chapter=chapter4_1, topic=topic34, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/TaxRevCalcDiagram_1.png")
    
    question1burden = Question(text='If market demand for a good is elastic and supply is inelastic, which of the following is true when there is an increase in sales tax?', chapter=chapter4_1, topic=topic37)
    question2burden = Question(text="Assume that price elasticity of demand for good A is -0.3 and price elasticity of demand for good B is -2.5.  Assume goods A and B have identical demand curves.  If a per-unit excise tax of the same amount is imposed on both goods, which of the following is true?", topic=topic37, chapter=chapter4_1)
    question3burden = Question(text="Assume that supply of wheat is relatively price inelastic while demand for wheat is relatively price elastic.  If the government imposes a specific exise tax on the production of corn, the incidence of tax will fall")
    question4burden = Question(text="Assume demand for cigarettes is inelastic and supply of cigarettes is elastic. If the government applies an exise tax on cigarettes, which of the following will occur in the short run?", topic = topic37, chapter=chapter4_1)
    question5burden = Question(text="Assume that the government imposes a specific excise tax on the producers of a good that faces perfectly inelastic demand.  After the tax, the price and the quantity will change in which of the following ways?", topic = topic37, chapter=chapter4_1)
    question6burden = Question(text="Assume demand for luxury cars faces PED of 1.5 and supply of luxury cars faces PES of 0.3.  If the government imposes a specific sales tax on the production of luxury cars, which of the following is true?")

    question1rev = Question(text="If the demand for a good is downward sloping and supply is upward sloping, imposing a sales tax on the good will", topic=topic35, chapter=chapter4_1)
    question2rev = Question(text="In the graph above, an excise tax has been imposed, moving supply from Supply to Supply + Tax.  The area representing the tax revenue to the government is", topic=topic35, chapter=chapter4_1, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/TaxRevCalcDiagram_1.png")
    question3rev = Question(text="In the graph above, an excise tax has been imposed, moving supply from Supply to Supply + Tax.  The area representing total consumer expenditure after imposition of the tax is", topic=topic35, chapter=chapter4_1, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/TaxRevCalcDiagram_1.png")
    question4rev = Question(text="In the graph above, an excise tax has been imposed, moving supply from Supply to Supply + Tax.  The area representing total producer revenue after imposition of the tax is", topic=topic35, chapter=chapter4_1, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/TaxRevCalcDiagram_1.png")
    question5rev = Question(text="In the graph above, an excise tax has been imposed, moving supply from Supply to Supply + Tax.  Producer revenue before and after tax is:", topic=topic35, chapter=chapter4_1, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/TaxPsCsCalc_1.png")
    question6rev = Question(text="In the graph above, an excise tax has been imposed, moving supply from Supply to Supply + Tax.  Total consumer expenditure before and after tax is:", topic=topic35, chapter=chapter4_1, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/TaxPsCsCalc_1.png")
    question7rev = Question(text="In the graph above, an excise tax has been imposed, moving supply from Supply to Supply + Tax.  Total government revenue from the tax is equal to:", topic=topic35, chapter=chapter4_1, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/TaxPsCsCalc_1.png")

    question1s = Question(text='Suppose that the market supply for pants is upward sloping and the market demand for pants is downward sloping.  How will the imposition of a sales tax on pants affect the consumer surplus (CS), producer surplus (PS), and total surplus (TS)?', chapter=chapter4_1, topic=topic36)
    question2s = Question(text='In the graph above, an excise tax has been imposed, moving supply from Supply to Supply + Tax.  The area representing total Loss of Social Surplus/Deadweight Loss is represented by:', chapter=chapter4_1, topic=topic36, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/TaxRevCalcDiagram_1.png")
    question3s = Question(text='If the government imposes a per-unit tax on airline travel, consumer surplus in the airline travel market will', chapter=chapter4_1, topic=topic36)
    question4s = Question(text='If the government imposes a per-unit tax on airline travel, producer surplus in the airline travel market will', chapter=chapter4_1, topic=topic36)
    question5s = Question(text='Assume that the government imposes a $5 per-unit tax on the sellers of a good in the market depicted in the diagram above.  What are the price paid by consumers, price received by producers, and deadweight loss?', chapter=chapter4_1, topic=topic36, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/5DollarTaxCalc_1.png")
    question6s = Question(text='In the graph above, an exise tax has been imposed, moving supply from Supply to Supply + Tax.  Total consumer surplus after imposition of the tax is:', chapter=chapter4_1, topic=topic36)
    question7s = Question(text='In the graph above, an exise tax has been imposed, moving supply from Supply to Supply + Tax.  Total producer surplus after imposition of the tax is:', chapter=chapter4_1, topic=topic36)
    
    questions = [question1, question2, question3, question4, question5, question6, 
                 question1burden, question2burden, question3burden,
                 question4burden, question5burden, question6burden,
                 question1rev, question2rev, question3rev,
                 question4rev, question5rev, question6rev, question7rev,
                 question1s, question2s, question3s,
                 question4s, question5s, question6s, question7s]

    answer1a = Answer(text="Price: Increase, Quantity: Increase", question=question1, is_correct=False)
    answer1b = Answer(text="Price: Increase, Quantity: Decrease", question=question1, is_correct=True)
    answer1c = Answer(text="Price: Increase, Quantity: No Change", question=question1, is_correct=False)
    answer1d = Answer(text="Price: Decrease, Quantity: Increase", question=question1, is_correct=False)
    answer1e = Answer(text="Price: Decrease, Quantity: No Change", question=question1, is_correct=False)

    answer2a = Answer(text="Consumers: $6.00, Producer: $5.80", question=question2, is_correct=False)
    answer2b = Answer(text="Consumers: $6.00, Producer: $5.00", question=question2, is_correct=False)
    answer2c = Answer(text="Consumers: $5.80, Producer: $5.00", question=question2, is_correct=False)
    answer2d = Answer(text="Consumers: $5.80, Producer: $4.80", question=question2, is_correct=True)
    answer2e = Answer(text="Consumers: $5.00, Producer: $4.80", question=question2, is_correct=False)

    answer3a = Answer(text="$0.00", question=question3, is_correct=False)
    answer3b = Answer(text="$0.20", question=question3, is_correct=False)
    answer3c = Answer(text="$0.80", question=question3, is_correct=False)
    answer3d = Answer(text="$1.00", question=question3, is_correct=True)
    answer3e = Answer(text="$1.20", question=question3, is_correct=False)

    answer4a = Answer(text="Price: Decrease, Quantity: Decrease", question=question4, is_correct=False)
    answer4b = Answer(text="Price: Increase, Quantity: Decrease", question=question4, is_correct=False)
    answer4c = Answer(text="Price: Increase, Quantity: Increase", question=question4, is_correct=False)
    answer4d = Answer(text="Price: Increase, Quantity: Indeterminate", question=question4, is_correct=True)
    answer4e = Answer(text="Price: Indeterminate, Quantity: Increase", question=question4, is_correct=False)

    answer5a = Answer(text="The price recieved by producers of electric vehicles will increase", question=question5, is_correct=False)
    answer5b = Answer(text="The price paid by consumers of electric vehicles will decrease", question=question5, is_correct=False)
    answer5c = Answer(text="The quantity purchased of electric vehicles will increase", question=question5, is_correct=False)
    answer5d = Answer(text="The quantity sold of electric vehicles will decrease", question=question5, is_correct=True)
    answer5e = Answer(text="The total revenue of electric vehicle manufacturers will increase", question=question5, is_correct=False)

    answer6a = Answer(text="Consumers: P1, Producers: P4", question=question6, is_correct=False)
    answer6b = Answer(text="Consumers: P1, Producers: P3", question=question6, is_correct=False)
    answer6c = Answer(text="Consumers: P2, Producers: P3", question=question6, is_correct=False)
    answer6d = Answer(text="Consumers: P2, Producers: P4", question=question6, is_correct=True)
    answer6e = Answer(text="Consumers: P3, Producers: P2", question=question6, is_correct=False)


    answer1ba = Answer(text="Producers will bear more of the burden of the tax", question=question1burden, is_correct=False)
    answer1bb = Answer(text="Consumers will bear more of the burden of the tax", question=question1burden, is_correct=True)
    answer1bc = Answer(text="Producers will bear all of the burden of the tax", question=question1burden, is_correct=False)
    answer1bd = Answer(text="Consumers will bear all of the burden of the tax", question=question1burden, is_correct=False)
    answer1be = Answer(text="The burden of the tax will be split evenly between producers and consumers", question=question1burden, is_correct=False)
                       
    answer2ba = Answer(text="Good A will see a bigger percentage decrease in quantity demanded than good B.", question=question2burden, is_correct=False)
    answer2bb = Answer(text="The tax burden paid by consumers of good A would be relatively higher than that paid by consumers of good B", question=question2burden, is_correct=True)
    answer2bc = Answer(text="The tax burden paid by consumers of good B would be relatively higher than that paid by consumers of good A", question=question2burden, is_correct=False)
    answer2bd = Answer(text="The tax burden paid by producers of good B would be relatively lower than that paid by producers of good A", question=question2burden, is_correct=False)
    answer2be = Answer(text="The tax share paid by suppliers of goods A and B would be the same", question=question2burden, is_correct=False)
    
    answer3ba = Answer(text="completely on consumers", question=question3burden, is_correct=False)
    answer3bb = Answer(text="more on consumers than producers", question=question3burden, is_correct=False)
    answer3bc = Answer(text="completely on producers", question=question3burden, is_correct=False)
    answer3bd = Answer(text="more on producers than consumers", question=question3burden, is_correct=True)
    answer3be = Answer(text="equally on consumers and producers", question=question3burden, is_correct=False)

    answer4ba = Answer(text = "Tax burden will fall equally on producers and consumers", is_correct=False, question=question4burden)
    answer4bb = Answer(text = "Tax burden will fall more on consumers", is_correct=True, question=question4burden)
    answer4bc = Answer(text = "Tax burden will fall more on producers", is_correct=False, question=question4burden)
    answer4bd = Answer(text = "Percentage increase in price of cigarettes will exceed the percentage increase in quantity demanded", is_correct=False, question=question4burden)
    answer4be = Answer(text = "Percentage decrease in total revenue will exceed the percentage decrease in quantity demanded", is_correct=False, question=question4burden)
    
    answer5ba = Answer(text="Price: Decrease, Quantity: No Change", question=question5burden, is_correct=False)
    answer5bb = Answer(text="Price: No Change, Quantity: Increase", question=question5burden, is_correct=False)
    answer5bc = Answer(text="Price: Increase, Quantity: No Change", question=question5burden, is_correct=True)
    answer5bd = Answer(text="Price: Increase, Quantity: Increase", question=question5burden, is_correct=False)
    answer5be = Answer(text="Price: Increase, Quantity: Decrease", question=question5burden, is_correct=False)

    answer6ba = Answer(text = "Tax burden will fall equally on producers and consumers", is_correct=False, question=question6burden)
    answer6bb = Answer(text = "Tax burden will fall more on consumers", is_correct=False, question=question6burden)
    answer6bc = Answer(text = "Tax burden will fall more on producers", is_correct=True, question=question6burden)
    answer6bd = Answer(text = "Tax burden will fall entirely on consumeres", is_correct=False, question=question6burden)
    answer6be = Answer(text = "Tax burden will fall entirely on producers", is_correct=False, question=question6burden)
    

    answer1sa = Answer(text="CS: Decrease, PS: Decrease, TS: Decrease", question=question1s, is_correct=True)
    answer1sb = Answer(text="CS: Decrease, PS: Increase, TS: Increase", question=question1s, is_correct=False)
    answer1sc = Answer(text="CS: Decrease, PS: Increase, TS: Decrease", question=question1s, is_correct=False)
    answer1sd = Answer(text="CS: Increase, PS: Decrease, TS: Decrease", question=question1s, is_correct=False)
    answer1se = Answer(text="CS: Increase, PS: Increase, TS: Increase", question=question1s, is_correct=False)

    answer2sa = Answer(text="C, F, G", question=question2s, is_correct=True)
    answer2sb = Answer(text="C, F, B", question=question2s, is_correct=False)
    answer2sc = Answer(text="C, E, F", question=question2s, is_correct=False)
    answer2sd = Answer(text="E, F, G", question=question2s, is_correct=False)
    answer2se = Answer(text="A, B, F, D", question=question2s, is_correct=False)

    answer3sa = Answer(text="Increase or decrease, depending on price elastiicty of demand", question=question3s, is_correct=False)
    answer3sb = Answer(text="Increase, because consumers will buy more airline travel", question=question3s, is_correct=False)
    answer3sc = Answer(text="Increase, because airline companies will pass the tax on to consumers", question=question3s, is_correct=False)
    answer3sd = Answer(text="Decrease, because there will be more airline travel available", question=question3s, is_correct=False)
    answer3se = Answer(text="Decrease, because price paid for airline travel will increase, and quantity consumed will decrease", question=question3s, is_correct=True)

    answer4sa = Answer(text="Increase or decrease, depending on price elastiicty of supply", question=question3s, is_correct=False)
    answer4sb = Answer(text="Increase, because airline companies will sell more airline travel", question=question3s, is_correct=False)
    answer4sc = Answer(text="Increase, because airline companies will pass the tax on to consumers", question=question3s, is_correct=False)
    answer4sd = Answer(text="Decrease, because there will be more airline travel available", question=question3s, is_correct=False)
    answer4se = Answer(text="Decrease, because price received by airline companies for supplying airline travel will decrease, and quantity supplied will decrease", question=question3s, is_correct=True)

    answer5sa = Answer(text="Buyer Price Paid: $14, Seller Price Received: $10, Deadweight Loss: $50", question=question5s, is_correct=False)
    answer5sb = Answer(text="Buyer Price Paid: $14, Seller Price Received: $9, Deadweight Loss: $125", question=question5s, is_correct=True)
    answer5sc = Answer(text="Buyer Price Paid: $10, Seller Price Received: $10, Deadweight Loss: $0", question=question5s, is_correct=False)
    answer5sd = Answer(text="Buyer Price Paid: $9, Seller Price Received: $14, Deadweight Loss: $50", question=question5s, is_correct=False)
    answer5se = Answer(text="Buyer Price Paid: $9, Seller Price Received: $14, Deadweight Loss: $125", question=question5s, is_correct=False)

    answer6sa = Answer(text="$405", question=question6s, is_correct=True)
    answer6sb = Answer(text="$450", question=question6s, is_correct=False)
    answer6sc = Answer(text="$750", question=question6s, is_correct=False)
    answer6sd = Answer(text="$1,000", question=question6s, is_correct=False)
    answer6se = Answer(text="$1,260", question=question6s, is_correct=False)

    answer7sa = Answer(text="$270", question=question7s, is_correct=True)
    answer7sb = Answer(text="$350", question=question7s, is_correct=False)
    answer7sc = Answer(text="$450", question=question7s, is_correct=False)
    answer7sd = Answer(text="$810", question=question7s, is_correct=False)
    answer7se = Answer(text="$1,000", question=question7s, is_correct=False)


    answer1ra = Answer(text="Result in no change to price paid by consumers", question=question1rev, is_correct=False)
    answer1rb = Answer(text="Result in no change to after tax revenue recieved by producers", question=question1rev, is_correct=False)
    answer1rc = Answer(text="Increase after tax revenue received by producers", question=question1rev, is_correct=False)
    answer1rd = Answer(text="Decrease after tax revenue recieved by producers", question=question1rev, is_correct=True)
    answer1re = Answer(text="Not change total exp", question=question1rev, is_correct=False)

    answer2ra = Answer(text="P1, B, F, P3", question=question2rev, is_correct = False)
    answer2rb = Answer(text="P1, B, Q3, 0", question=question2rev, is_correct = False)
    answer2rc = Answer(text="P2, C, G, P4", question=question2rev, is_correct = True)
    answer2rd = Answer(text="P2, C, Q2, 0", question=question2rev, is_correct = False)
    answer2re = Answer(text="P3, F, Q3, 0", question=question2rev, is_correct = False)

    answer3ra = Answer(text="P1, B, Q3, 0", question=question3rev, is_correct=False)
    answer3rb = Answer(text="P2, C, G, P4", question=question3rev, is_correct=False)
    answer3rc = Answer(text="P2, C, Q2, 0, ", question=question3rev, is_correct=True)
    answer3rd = Answer(text="P3, F, Q3, 0", question=question3rev, is_correct=False)
    answer3re = Answer(text="P4, G, Q2, 0", question=question3rev, is_correct=False)

    answer4ra = Answer(text="P1, B, Q3, 0", question=question4rev, is_correct=False)
    answer4rb = Answer(text="P2, C, G, P4", question=question4rev, is_correct=False)
    answer4rc = Answer(text="P2, C, Q2, 0, ", question=question4rev, is_correct=False)
    answer4rd = Answer(text="P3, F, Q3, 0", question=question4rev, is_correct=False)
    answer4re = Answer(text="P4, G, Q2, 0", question=question4rev, is_correct=True)


    answer5ra = Answer(text="Producer Revenue Before Tax: $1,000, Producer Revenue After Tax: $1,400", question=question5rev, is_correct=False)
    answer5rb = Answer(text="Producer Revenue Before Tax: $1,000, Producer Revenue After Tax: $900", question=question5rev, is_correct=False)
    answer5rc = Answer(text="Producer Revenue Before Tax: $1,000, Producer Revenue After Tax: $810", question=question5rev, is_correct=True)
    answer5rd = Answer(text="Producer Revenue Before Tax: $1,310, Producer Revenue After Tax: $900", question=question5rev, is_correct=False)
    answer5re = Answer(text="Producer Revenue Before Tax: $810 Producer Revenue After Tax: $1,310", question=question5rev, is_correct=False)

    answer6ra = Answer(text="Consumer Expenditure Before Tax: $1,000, Consumer Expenditure After Tax: $1,400", question=question5rev, is_correct=False)
    answer6rb = Answer(text="Consumer Expenditure Before Tax: $1,000, Consumer Expenditure After Tax: $1,310", question=question5rev, is_correct=True)
    answer6rc = Answer(text="Consumer Expenditure Before Tax: $1,000, Consumer Expenditure After Tax: $810", question=question5rev, is_correct=False)
    answer6rd = Answer(text="Consumer Expenditure Before Tax: $1,310, Consumer Expenditure After Tax: $900", question=question5rev, is_correct=False)
    answer6re = Answer(text="Consumer Expenditure Before Tax: $810 Consumer Expenditure After Tax: $1,310", question=question5rev, is_correct=False)


    answer7ra = Answer(text="$1,310", question=question5rev, is_correct=False)
    answer7rb = Answer(text="$1,000", question=question5rev, is_correct=False)
    answer7rc = Answer(text="$810", question=question5rev, is_correct=False)
    answer7rd = Answer(text="$450", question=question5rev, is_correct=True)
    answer7re = Answer(text="Cannot be determined from information given", question=question5rev, is_correct=False)


    answers = [
        answer1a, answer1b, answer1c, answer1d, answer1e, 
        answer2a, answer2b, answer2c, answer2d, answer2e, 
        answer3a, answer3b, answer3c, answer3d, answer3e, 
        answer4a, answer4b, answer4c, answer4d, answer4e, 
        answer5a, answer5b, answer5c, answer5d, answer5e,
        answer6a, answer6b, answer6c, answer6d, answer6e,

        answer1ba, answer1bb, answer1bc, answer1bd, answer1be, 
        answer2ba, answer2bb, answer2bc, answer2bd, answer2be,
        answer3ba, answer3bb, answer3bc, answer3bd, answer3be,
        answer4ba, answer4bb, answer4bc, answer4bd, answer4be,
        answer5ba, answer5bb, answer5bc, answer5bd, answer5be,
        answer6ba, answer6bb, answer6bc, answer6bd, answer6be,

        answer1sa, answer1sb, answer1sc, answer1sd, answer1se, 
        answer2sa, answer2sb, answer2sc, answer2sd, answer2se,
        answer3sa, answer3sb, answer3sc, answer3sd, answer3se,
        answer4sa, answer4sb, answer4sc, answer4sd, answer4se,
        answer5sa, answer5sb, answer5sc, answer5sd, answer5se,
        answer6sa, answer6sb, answer6sc, answer6sd, answer6se,
        answer7sa, answer7sb, answer7sc, answer7sd, answer7se,

        answer1ra, answer1rb, answer1rc, answer1rd, answer1re,
        answer2ra, answer2rb, answer2rc, answer2rd, answer2re,
        answer3ra, answer3rb, answer3rc, answer3rd, answer3re,
        answer4ra, answer4rb, answer4rc, answer4rd, answer4re,
        answer5ra, answer5rb, answer5rc, answer5rd, answer5re,
        answer6ra, answer6rb, answer6rc, answer6rd, answer6re,
        answer7ra, answer7rb, answer7rc, answer7rd, answer7re
    ]

    db.session.add_all(questions)
    db.session.add_all(answers)

    db.session.commit()
    print("Questions seeded successfully")
    
def main():
    with app.app_context():
        seed_tax_chapter()

if __name__=="__main__":
    try:
        main()
    except IntegrityError:
        db.session.rollback()
        print("There was an error seeding the database")