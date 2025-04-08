from exts import db
from main import create_app
from config import ProdConfig
from models import Chapter, QuestionTopic, Unit, Question, Answer
from sqlalchemy.exc import IntegrityError

app = create_app(ProdConfig)

def seed_price_ceiling_chapter():
    unit4 = db.session.get(Unit, 4)

    if not unit4:
        print("Unit with ID 4 does not exist. Seeding aborted.")
        return
    
    chapter4_3 = Chapter(
        unit=unit4,
        video_url = "https://www.youtube.com/embed/LAW_K3rDvdI?si=fQZJKqjrDt9z0yu9",
        order=27,
        slug="price ceilings",
        video_blurb = "Think rent control sounds like a dream? Imagine locking in a super low price for your apartment—forever. Now imagine a city where everyone else had that idea before you, and now you're 30, still on the waiting list, sleeping in your childhood bedroom next to your old participation trophies. Price ceilings, like rent control, are meant to make housing affordable, but they can lead to shortages, long waitlists, and some seriously awkward family dinners. \n\n In this video, we break down how price ceilings work, why politicians love them, and why economists side-eye them harder than your mom does when you say you're “just figuring things out right now.” We’ll look at real-world rent control examples and the unintended consequences that come with artificially capping prices. So grab a snack (but not from your parents’ fridge), hit play, and let’s dive into the hidden costs of 'affordable' rent."
        quiz_blurb = "Ready to test your rent control wisdom? This quiz will see if you actually understood how price ceilings mess with supply and demand—or if you were too distracted imagining your 30th birthday party in your mom’s basement. /n/nExpect questions about shortages, market distortions, and why getting a cheap apartment might just mean never getting an apartment. Don’t worry, it’s multiple choice—no essays explaining your life plan to your mom required. "
    )

    topic40=QuestionTopic(name="Price Ceilings")


    question1 = Question(text="Which of the following is NOT expected to be an impact of implementing a price ceiling?", chapter=chapter4_3, topic=topic40)
    question2 = Question(text="The above diagram shows the market for a good.  If a price ceiling is implemented at P2, what is the total quantity that will be purchased in the market?", chapter=chapter4_3, topic=topic40, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/PcPf_3.png")
    question3 = Question(text="The above diagram shows the market for a good.  If a price ceiling is implemented at P2, which of the following is true?", chapter=chapter4_3, topic=topic40, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/PcPf_3.png")
    question4 = Question(text="The above diagram shows a market for a good.  If a price ceiling is implemented at P2, which area represents total social surplus after implementation fo the price ceiling", chapter=chapter4_3, topic=topic40, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/PcPf_3.png")
    questions = [question1]

    answer1a = Answer(text="A shortage of the good will arise", question=question1, is_correct=False)
    answer1b = Answer(text="People may resort to black markets to aquire the good", question=question1, is_correct=False)
    answer1c = Answer(text="Some people who would have gotten the good with no price ceiling may find themselves unable to get it after implementation of the price ceiling", question=question1, is_correct=False)
    answer1d = Answer(text="Businesses will produce more of the good", question=question1, is_correct=True)
    answer1e = Answer(text="The market will require some allocation method other than the price method of allocation", question=question1, is_correct=False)

    answer2a = Answer(text="Q1", question=question2, is_correct=True)
    answer2b = Answer(text="Q2", question=question2, is_correct=False)
    answer2c = Answer(text="Q3", question=question2, is_correct=False)
    answer2d = Answer(text="Q3 x P2", question=question2, is_correct=False)
    answer2e = Answer(text="Q2 x P2", question=question2, is_correct=False)

    answer3a = Answer(text="Total consumer expenditure changes from area P3,D,Q2,0 to P2, G, Q3, 0", question=question3, is_correct=False)
    answer3b = Answer(text="Total producer revenue changes from area P3,D,Q2,0 to P2, E, Q3, 0", question=question3, is_correct=True)
    answer3c = Answer(text="Deadweight loss is area B, D, G", question=question3, is_correct=False)
    answer3d = Answer(text="Producer revenue definitely rises", question=question3, is_correct=False)
    answer3e = Answer(text="Consumer excpenditure definitely rises", question=question3, is_correct=False)


    answers = [answer1a, answer1b, answer1c, answer1d, answer1e]

