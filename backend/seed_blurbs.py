from exts import db
from models import Chapter
from config import ProdConfig
from main import create_app
from sqlalchemy.exc import IntegrityError

app = create_app(ProdConfig)

def seed_blurbs():
    print('seeding Blurbs')
    chapter1 = db.session.get(Chapter, 1)
    chapter1.video_blurb = "Welcome to the thrilling kickoff of our economics video series, 'Scarcity, Choice, and Opportunity Cost!' We know, we know — you're on the edge of your seat already. This is the first video of Introduction to Economic Concepts, so buckle up! It’s like the opening act at a concert, but instead of loud music, we’re here with something much better: cold, hard economics. Don’t worry, we’ll keep the math to a minimum… for now. \n\n In this video, we’ll guide you through the magical world where limited resources meet unlimited wants (spoiler alert: things get tricky). You'll learn about scarcity (aka, why you cannot have everything), choice (aka, why you have to make decisions, like choosing this video over cat memes), and opportunity cost (aka, the price of watching this video when you could have been napping). \n\n After the video, stick around for a quiz to show off your newfound econ knowledge. You know, just to make sure you're paying attention and not just here for our witty commentary. Go ahead, click play — your future self (and all the scarce resources) will thank you!"
    chapter1.quiz_blurb = "Congrats!  You've officially conquered your first EVTDS Video - Scarcity, Choice and Opportunity Cost!  Now it's time to take your first quiz, which is like a personality test from Cosmo but for Econ - are you more Econ 101 or The Wolf of Wall Street?  There are six questions - AP style -- so channel your inner economic mastermind and let’s see those skills in action!"
    chapter1.quiz_blurb_img_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/OCCartoon.png"

    chapter2 = db.session.get(Chapter, 2)
    chapter2.video_blurb = "Get ready to dive into the world of Factors of Production, where we’ll explore the essential ingredients for creating, well, pretty much everything. Land, labor, capital, and entrepreneurship — it’s like the recipe for an economic casserole. Spoiler: there’s no secret sauce, just a lot of work ... and some wonky definitions. \n\n Learn why land is not just about real estate, why labor is not just about suffering through your part-time job, and how entrepreneurs are basically the adventurous chefs of the economic world.  Just like chefs experiment with wild ingredients (Rocky Mountain Oysters anyone?), entrepreneurs toss around ideas that sometimes tase like gourmet meals and other times taste like... well, let's just say they might need more salt. \n\n Stick around after the video for a quiz, so you can prove you've mastered the art of economic cooking (or at least know your ingredients)! And if you manage to make a Fight Club version of the economic soup, not to worry, there's more review down the line!"
    chapter2.quiz_blurb = "Welcome to Factors of Production—aka the ‘behind-the-scenes’ of how everything in economics happens (you know, the stuff AP and College Board won’t tell you). Grab some popcorn, because it's time to learn about the four magical ingredients that make the economy go. No, it's not the secret to a perfect Netflix binge—it's land, labor, capital, and entrepreneurship. So, sit back, relax, and try not to nod off like you’re in the middle of an AP Econ lecture!"

    chapter3 = db.session.get(Chapter, 3)
    chapter3.video_blurb =  "Hey there, economic adventurer! You’ve made it to Chapter 3, and things are really heating up. Welcome to Economic Systems: where we categorize the world's economies like a reality TV show judge. Capitalism, socialism, mixed economies — it's like choosing your favorite flavor of ice cream, but with more debates and fewer sprinkles. \n\n In this chapter, we’ll break down the pros and cons of each system, explaining why some countries have thriving free markets while others prefer the government to take the wheel. And hey, you might even discover which system suits your inner economist. \n\n Stay tuned for the quiz afterwards to see if you’re more Adam Smith or Karl Marx. It’s the ultimate personality test, econ style! Don’t worry, there are no wrong answers (except the wrong ones), and as always, it’s all in good fun. So grab your popcorn, sit back, and let’s figure out where you land on the economics spectrum!"

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


