from exts import db
from models import Chapter
from config import ProdConfig
from main import create_app
from sqlalchemy.exc import IntegrityError

app = create_app(ProdConfig)

def seed_blurbs():
    print('seeding Blurbs')
    chapter1 = Chapter.query.get(1)
    chapter1.video_blurb = """
    Welcome to the thrilling kickoff of our economics video series, "Scarcity, Choice, and Opportunity Cost!" 
    We know, we know — you're on the edge of your seat already. This is the first video of Introduction to Economic 
    Concepts, so buckle up! It’s like the opening act at a concert, but instead of loud music, we’re here 
    with something much better: cold, hard economics. Don’t worry, we’ll keep the math to a minimum… for now.\n\nIn this video, we’ll guide you through the magical world where limited resources meet unlimited wants 
    (spoiler alert: things get tricky). You'll learn about scarcity (aka, why you can’t have everything), choice 
    (aka, why you have to make decisions, like choosing this video over cat memes), and opportunity cost (aka, 
    the price of watching this video when you could have been napping).\n\nAfter the video, stick around for a quiz to show off your newfound econ knowledge. You know, just to make 
    sure you're paying attention and not just here for our witty commentary. Go ahead, click play — your future
      self (and all the scarce resources) will thank you!
"""
    db.session.commit()

def main():
    with app.app_context():
        seed_blurbs()

if __name__=="__main__":
    try:
        main()
    except IntegrityError:
        db.session.rollback()
        print("There was an error seeding the database")


