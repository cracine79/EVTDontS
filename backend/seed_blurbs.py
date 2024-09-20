from exts import db
from models import Chapter
from config import ProdConfig
from main import create_app
from sqlalchemy.exc import IntegrityError

app = create_app(ProdConfig)

def seed_blurbs():
    print('seeding Blurbs')
    chapter1 = db.session.get(Chapter, 1)
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

    chapter2 = db.session.get(Chapter, 2)
    chapter2.video_blurb = """
    Get ready to dive into the world of Factors of Production, where we’ll explore the essential ingredients for creating, well, pretty much everything. Land, labor, capital, and entrepreneurship — it’s like the recipe for an economic casserole. Spoiler: there’s no secret sauce, just a lot of work. \n\nLearn why land isn’t just 
    about real estate, why labor isn't just about suffering through your part-time job, and how entrepreneurs are 
    basically the adventurous chefs of the economic world. \n\nStick around after the video for a quiz, so you can 
    prove you've mastered the art of economic cooking (or at least know your ingredients)!
    """

    chapter3 = db.session.get(Chapter, 3)
    chapter3.video_blurb="""
    Hey there, economic adventurer! You’ve made it to Chapter 3, and things are really heating up.
    Welcome to Economic Systems: where we categorize the world's economies like a reality TV show judge. 
    Capitalism, socialism, mixed economies — it's like choosing your favorite flavor of ice cream, but with 
    more debates and fewer sprinkles. \n\nIn this chapter, we’ll break down the pros and cons of each system, 
    explaining why some countries have thriving free markets while others prefer the government to take the 
    wheel. And hey, you might even discover which system suits your inner economist. \n\nStay tuned for the quiz 
    afterwards to see if you’re more Adam Smith or Karl Marx. It’s the ultimate personality test, econ style!
    Don’t worry, there are no wrong answers (except the wrong ones), and as always, it’s all in good fun. 
    So grab your popcorn, sit back, and let’s figure out where you land on the economics spectrum!
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


