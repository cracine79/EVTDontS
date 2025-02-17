from exts import db
from models import Chapter
from config import ProdConfig
from main import create_app
from sqlalchemy.exc import IntegrityError


app = create_app(ProdConfig)

def seed_cartoons():
    print('seeding Cartoons')
    chapter5 = db.session.get(Chapter, 6)
    chapter5.quiz_blurb_img_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/Comparativeadvantagecartoon1.png'

    db.session.commit()

def main():
    with app.app_context():
        seed_cartoons()

if __name__=="__main__":
    try:
        main()
    except IntegrityError:
        db.session.rollback()
        print("There was an error seeding the database")