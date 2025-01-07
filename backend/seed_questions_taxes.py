from exts import db
from main import create_app
from config import ProdConfig
from models import Chapter, QuestionTopic, Unit, Question, Answer
from sqlalchemy.exc import IntegrityError

app = create_app(ProdConfig)


def seed_tax_chapter():
    unit4 = db.session.get(Unit, 4)

    chapter4_1 = Chapter(name="4.1 Taxes", unit=unit4, video_url="https://www.youtube.com", order=25)

    db.session.add(chapter4_1)
    db.session.commit()

    topic34 = QuestionTopic(name='Taxes - Impact on price and quantity', chapter=chapter4_1)
    topic35 = QuestionTopic(name='Taxes - Impact on Producer Revenue, Consumer Expenditure & Government Revenue', chapter=chapter4_1)
    topic36 = QuestionTopic(name='Taxes - Impact on Social Surplus & Deadweight Loss', chapter=chapter4_1)
