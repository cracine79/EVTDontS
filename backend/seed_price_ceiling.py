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
        name="4.3 Price Ceilings",
        unit=unit4,
        video_url = "https://www.youtube.com/embed/LAW_K3rDvdI?si=fQZJKqjrDt9z0yu9",
        order=27,
        slug="price ceilings",
        video_blurb = "Think rent control sounds like a dream? Imagine locking in a super low price for your apartment—forever. Now imagine a city where everyone else had that idea before you, and now you're 30, still on the waiting list, sleeping in your childhood bedroom next to your old participation trophies. Price ceilings, like rent control, are meant to make housing affordable, but they can lead to shortages, long waitlists, and some seriously awkward family dinners. \n\n In this video, we break down how price ceilings work, why politicians love them, and why economists side-eye them harder than your mom does when you say you're “just figuring things out right now.” We’ll look at real-world rent control examples and the unintended consequences that come with artificially capping prices. So grab a snack (but not from your parents’ fridge), hit play, and let’s dive into the hidden costs of 'affordable' rent.",
        quiz_blurb = "Ready to test your rent control wisdom? This quiz will see if you actually understood how price ceilings mess with supply and demand—or if you were too distracted imagining your 30th birthday party in your mom’s basement. /n/nExpect questions about shortages, market distortions, and why getting a cheap apartment might just mean never getting an apartment. Don’t worry, it’s multiple choice—no essays explaining your life plan to your mom required. "
    )

    topic40=QuestionTopic(name="Price Ceilings", chapter=chapter4_3)


    question1 = Question(text="Which of the following is NOT expected to be an impact of implementing a price ceiling?", chapter=chapter4_3, topic=topic40)
    question2 = Question(text="The above diagram shows the market for a good.  If a price ceiling is implemented at P2, what is the total quantity that will be purchased in the market?", chapter=chapter4_3, topic=topic40, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/PcPf_3.png")
    question3 = Question(text="The above diagram shows the market for a good.  If a price ceiling is implemented at P2, which of the following is true?", chapter=chapter4_3, topic=topic40, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/PcPf_3.png")
    question4 = Question(text="The above diagram shows a market for a good.  If a price ceiling is implemented at P2, which area represents total social surplus after implementation of the price ceiling?", chapter=chapter4_3, topic=topic40, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/PcPf_3.png")
    question5 = Question(text="Assume that the current market equilibrium price for eggs is $8 per carton and that 3 million cartons of eggs are sold per day.  If the government sets a price ceiling of $6.50 per carton, which of the following is true?", chapter=chapter4_3, topic=topic40)
    question6 = Question(text="In the diagram above, if there is a price ceiling set at P2, consumer surplus will be represented by the area", chapter=chapter4_3, topic=topic40, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/PcPf_3.png")
    question7 = Question(text="The diagram above depicts the supply and demand curves for a city's rental housing market.  If a price ceiling is imposed at P2, which of the followin gwill occur?", chapter=chapter4_3, topic=topic40, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/PcPf_3.png")
    question8 = Question(text="If the market depicted in the diagram above is initially in equilibrium, which of the following will result from the government setting a price ceiling at P4?", chapter=chapter4_3, topic=topic40, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/PcPf_3.png")
    questions = [question1, question2, question3, question4, question5, question6, question7, question8]

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

    answer4a = Answer(text="ADC", question=question4, is_correct=False)
    answer4b = Answer(text="CDE", question=question4, is_correct=False)
    answer4c = Answer(text="ADE", question=question4, is_correct=True)
    answer4d = Answer(text="BDG", question=question4, is_correct=False)
    answer4e = Answer(text="ABGE", question=question4, is_correct=False)

    answer5a = Answer(text="Less than 3 million cartons of eggs will be sold", question=question5, is_correct=True)
    answer5b = Answer(text="More than 3 million cartons of eggs will be sold", question=question5, is_correct=False)
    answer5c = Answer(text="There will be a surplus of eggs in the market", question=question5, is_correct=False)
    answer5d = Answer(text="The supply of eggs will decrease", question=question5, is_correct=False)
    answer5e = Answer(text="The demand for eggs will increase", question=question5, is_correct=False)

    answer6a = Answer(text="A,D,E", question=question6, is_correct=False)
    answer6b = Answer(text="P3, D, P1", question=question6, is_correct=False)
    answer6c = Answer(text="P5, B, P3", question=question6, is_correct=False)
    answer6d = Answer(text="P5, A, E, P2", question=question6, is_correct=True)
    answer6e = Answer(text="P5, D, E, P2", question=question6, is_correct=False)

    answer7a = Answer(text="The demand curve for housing will shift to the right", question=question7, is_correct=False)
    answer7b = Answer(text="The supply curve for housing will shift to the right", question=question7, is_correct=False)
    answer7c = Answer(text="There will be a surplus of rental housing in the city", question=question7, is_correct=False)
    answer7d = Answer(text="The quantity of rental housing supplied will decrease", question=question7, is_correct=True)
    answer7e = Answer(text="The quantity of rental housind demanded will decrease", question=question7, is_correct=False)

    answer8a = Answer(text="Quantity demanded will exceed quantity supplied", question=question8, is_correct=False)
    answer8b = Answer(text="Quantity supplied will exceed quantity demanded", question=question8, is_correct=False)
    answer8c = Answer(text="Market price will increase", question=question8, is_correct=False)
    answer8d = Answer(text="Market price will be unaffected", question=question8, is_correct=True)
    answer8e = Answer(text="Market price will decrease", question=question8, is_correct=False)

    answers = [answer1a, answer1b, answer1c, answer1d, answer1e,
               answer2a, answer2b, answer2c, answer2d, answer2e,
               answer3a, answer3b, answer3c, answer3d, answer3e,
               answer4a, answer4b, answer4c, answer4d, answer4e,
               answer5a, answer5b, answer5c, answer5d, answer5e,
               answer6a, answer6b, answer6c, answer6d, answer6e,
               answer7a, answer7b, answer7c, answer7d, answer7e,
               answer8a, answer8b, answer8c, answer8d, answer8e,]

    print('seeding chapter')
    db.session.add(chapter4_3)
    print('seeding topics')
    db.session.add(topic40)
    print('seeding questions')
    db.session.add_all(questions)
    print('seeding answers')
    db.session.add_all(answers)
    db.session.commit()
    print("Chapter seeded")

def main():
    with app.app_context():
        try:
            seed_price_ceiling_chapter()
        except IntegrityError as e:
            db.session.rollback()  # Now within the app context
            print(f"There was an error seeding the chapter: {e}")

if __name__=="__main__":
    try:
        main()
    except IntegrityError:
        db.session.rollback()
        print("There was an error seeding the database")