from exts import db
from main import create_app
from config import ProdConfig
from models import Chapter, QuestionTopic, Unit, Question, Answer
from sqlalchemy.exc import IntegrityError


app = create_app(ProdConfig)

def seed_tax_chapter_topic():

    print('seeding chapter')
    unit4 = db.session.get(Unit, 4)
    if not unit4:
        print("Unit with ID 4 does not exist. Seeding aborted.")
        return

    chapter4_1 = Chapter(name="4.1 Taxes", unit=unit4, video_url="https://www.youtube.com/embed/4Jpvus1kpr8", order=25)

    topic34 = QuestionTopic(name='Taxes - Impact on price and quantity', chapter=chapter4_1)
    topic35 = QuestionTopic(name='Taxes - Impact on Producer Revenue, Consumer Expenditure & Government Revenue', chapter=chapter4_1)
    topic36 = QuestionTopic(name='Taxes - Impact on Social Surplus & Deadweight Loss', chapter=chapter4_1)
    topic37 = QuestionTopic(name='Taxes - Elasticity and Tax Burden', chapter=chapter4_1)

    topics = [topic34, topic35, topic36, topic37]

    db.session.add(chapter4_1)
    db.session.add_all(topics)

    db.session.commit()

def main():
    with app.app_context():
        seed_tax_chapter_topic()

if __name__=="__main__":
    try:
        main()
    except IntegrityError:
        db.session.rollback()
        print("There was an error seeding the database")