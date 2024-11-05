
from exts import db
from main import create_app
from config import ProdConfig
from models import Chapter, QuestionTopic, Unit
from sqlalchemy.exc import IntegrityError

app = create_app(ProdConfig)

def seed_unit2_questions():
    print('Seeding Unit 2 Questions')
    unit2 = Unit.query.get(2)
    unit2_chapters = unit2.chapters
    unit2_chapters_sorted = sorted(unit2_chapters, key=lambda chapter: chapter.order)
    demand_curve_topic = unit2_chapters_sorted[0].topics
    shifts_to_demand_topic = unit2_chapters_sorted[1].topics

    

def main():
    with app.app_context():
        pass

if __name__=="__main__":
    try:
        main()
    except IntegrityError:
        db.session.rollback()
        print("There was an error seeding the database")