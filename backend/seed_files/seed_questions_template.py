from exts import db
from main import create_app
from config import ProdConfig
from models import Chapter, QuestionTopic, Unit, Question, Answer
from sqlalchemy.exc import IntegrityError

app = create_app(ProdConfig)

#be sure to check for chapter ID and stuff first in Heroku.

def seed_tax_chapter():
    unit4 = db.session.get(Unit, 4)
    if not unit4:
        print("Unit with ID 4 does not exist. Seeding aborted.")
        return

    chapter4_1 = Chapter(name="4.1 Taxes", unit=unit4, video_url="https://www.youtube.com", order=25)

    topic34 = QuestionTopic(name='Taxes - Impact on price and quantity', chapter=chapter4_1)
    topic35 = QuestionTopic(name='Taxes - Impact on Producer Revenue, Consumer Expenditure & Government Revenue', chapter=chapter4_1)
    topic36 = QuestionTopic(name='Taxes - Impact on Social Surplus & Deadweight Loss', chapter=chapter4_1)
    topic37 = QuestionTopic(name='Taxes - Elasticity and Tax Burden', chapter=chapter4_1)

    topics = [topic34, topic35, topic36, topic37]

    question1 = Question(text='Assume that supply for a good is upward sloping and demand is downward sloping.  The imposition of a specific exise tax on the sale of that good would result in which of the following changes to equilibrium price and quantity?', chapter=chapter4_1, topic=topic34)
    question2 = Question(text='', chapter=chapter4_1, topic=topic34)


    question4 = Question(text='Assume that the government increases the unit exise tax on alcohol suppliers and also at the same time, the demand for alcohol increases due to increases in stress levels at work.   As a result, equilibrium price and quantity of alcohol will most likely change in which of the following ways?', chapter=chapter4_1, topic=topic34)
    question1burden = Question(text='If market demand for a good is elastic and supply is inelastic, which of the following is true when there is an increase in sales tax?', chapter=chapter4_1, topic=topic37)
    question2burden = Question(text="Assume that price elasticity of demand for good A is -0.3 and price elasticity of demand for good B is -2.5.  Assume goods A and B have identical demand curves.  If a per-unit excise tax of the same amount is imposed on both goods, which of the following is true?", topic=topic37, chapter=chapter4_1)
    questions = [question1, question2, question4, question1burden, question2burden]

    answer1a = Answer(text="Price: Increase, Quantity: Increase", question=question1, is_correct=False)
    answer1b = Answer(text="Price: Increase, Quantity: Decrease", question=question1, is_correct=True)
    answer1c = Answer(text="Price: Increase, Quantity: No Change", question=question1, is_correct=False)
    answer1d = Answer(text="Price: Decrease, Quantity: Increase", question=question1, is_correct=False)
    answer1e = Answer(text="Price: Decrease, Quantity: No Change", question=question1, is_correct=False)

    answer4a = Answer(text="Price: Decrease, Quantity: Decrease", question=question4, is_correct=False)
    answer4b = Answer(text="Price: Increase, Quantity: Decrease", question=question4, is_correct=False)
    answer4c = Answer(text="Price: Increase, Quantity: Increase", question=question4, is_correct=False)
    answer4d = Answer(text="Price: Increase, Quantity: Indeterminate", question=question4, is_correct=True)
    answer4e = Answer(text="Price: Indeterminate, Quantity: Increase", question=question4, is_correct=False)

    answer1ba = Answer(text="Producers will bear more of the burden of the tax", question=question1burden, is_correct=False)
    answer1bb = Answer(text="Consumers will bear more of the burden of the tax", question=question1burden, is_correct=False)
    answer1bc = Answer(text="Producers will bear all of the burden of the tax", question=question1burden, is_correct=False)
    answer1bd = Answer(text="Consumers will bear all of the burden of the tax", question=question1burden, is_correct=False)
    answer1be = Answer(text="The burden of the tax will be split evenly between producers and consumers", question=question1burden, is_correct=False)
                       
    answer2ba = Answer(text="Good A will see a bigger percentage decrease in quantity demanded than good B.", question=question2burden, is_correct=False)
    answer2bb = Answer(text="The tax burden paid by consumers of good A would be relatively higher than that paid by consumers of good B", question=question2burden, is_correct=True)
    answer2bc = Answer(text="The tax burden paid by consumers of good B would be relatively higher than that paid by consumers of good A", question=question2burden, is_correct=False)
    answer2bd = Answer(text="The tax burden paid by producers of good B would be relatively lower than that paid by producers of good A", question=question2burden, is_correct=False)
    answer2be = Answer(text="The tax share paid by suppliers of goods A and B would be the same", question=question2burden, is_correct=False)
    
    answers = [
        answer1a, answer1b, answer1c, answer1d, answer1e, 

        answer4a, answer4b, answer4c, answer4d, answer4e, 
        answer1ba, answer1bb, answer1bc, answer1bd, answer1be, 
        answer2ba, answer2bb, answer2bc, answer2bd, answer2be
    ]

    try:
        with db.session.begin():
            db.session.add(chapter4_1)
            db.session.add_all(topics)
            db.session.add_all(questions)
            db.session.add_all(answers)
        print("Chapter seeded successfully")
    except IntegrityError as e:
        db.session.rollback()
        print(f"IntegrityError occurred: {e}")

    print("Chapter seeded successfully")
    
def main():
    with app.app_context():
        seed_tax_chapter()

if __name__=="__main__":
    try:
        main()
    except IntegrityError:
        db.session.rollback()
        print(f"There was an error seeding the chapter")