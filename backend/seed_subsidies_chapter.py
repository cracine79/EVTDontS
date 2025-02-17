from exts import db
from main import create_app
from config import ProdConfig
from models import Chapter, QuestionTopic, Unit, Question, Answer
from sqlalchemy.exc import IntegrityError

app = create_app(ProdConfig)

def seed_subsidies_chapter():
        unit4=db.session.get(Unit, 4)

        if not unit4:
            print("Unit with ID 4 does not exist. Seeding aborted.")
            return
        
        chapter4_2 = Chapter(name="4.2 Subsidies", 
                             unit=unit4, 
                             video_url="https://www.youtube.com/embed/r9td5tmpSnI?si=F4JWIjpGHP4ERP5U", 
                             order=26, 
                             slug="subsidies",
                             video_blurb = "Ever wonder why the U.S. grows so much corn? It’s not just because we love popcorn—it's because subsidies help make it happen. The government, in its infinite wisdom (or at least its strong opinions), steps in to support farmers, ensuring that fields stay planted, prices stay stable, and ethanol keeps flowing into gas tanks. Sure, maybe we don’t all need quite this much corn, but hey, when Washington says, <em>“Grow it, and we’ll pay,”</em> who’s turning that down? \n\n  But subsidies aren’t just about corn—they shape industries, influence prices, and keep certain businesses afloat when markets get rough. Some call it economic stability, others call it market interference. Either way, when it comes to government incentives, one thing’s for sure: if there’s money on the table, someone’s going to build something to take it.",
                             quiz_blurb = "Alright, economics whiz—it's quiz time! You’ve learned about how subsidies shape markets, how they affect everything from cornfields to ethanol, and why Uncle Sam sometimes steps in to keep things running smoothly. Now, let’s see if all that brainpower sticks. Are you ready to prove you can separate the myths from the facts? Take this quiz and show us just how much you really know about government intervention—and maybe learn a few things you didn’t expect along the way!")
        
        topic38 = QuestionTopic(name='Subsidies = Impact on price and quantity', chapter=chapter4_2)
        topic39 = QuestionTopic(name='Subsidies = Impact on Stakeholders', chapter=chapter4_2)

        topics = [topic38, topic39]

        question1 = Question(text="Assume the government provides a per-unit subsidy to the producers of electric cars in Germany.  Which of the following could be expected to happen in the market as a result?", chapter=chapter4_2, topic=topic38)
        question2 = Question(text="What is the size of the subsidy per unit in the above diagram?", chapter=chapter4_2, topic=topic38, image_url="https://evtds-seeds.s3.us-east-2.amazonaws.com/Subsidy1.png")
        question3 = Question(text="Which of the following would NOT be a reason for a government to impose a subsidy on the production of a good?", chapter=chapter4_2, topic=topic38)
        question4 = Question(text="Which of the following would NOT be an expected outcome of the government providing a subsidy to suppliers of higher-education in the US?", chapter=chapter4_2, topic=topic38)
        question5 = Question(text="Which of the following could be an accurate description of the above diagram?", chapter=chapter4_2, topic=topic38, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/ABCsubsidyCAPS.png")
        question6 = Question(text="If the government imposes a subsidy on the production of solar panels in China, which of the following might be expected to occur?", chapter=chapter4_2, topic=topic38)
       
        question7 = Question(text="The above diagram shows the impact of a subsidy in the market for agricultural products in the EU.  What is the total revenue to producers after imposition of the subsidy?", chapter=chapter4_2, topic=topic39, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/subswithn.png")
        question8 = Question(text="The above diagram shows the impact of a subsidy in the market for agricultural products in the EU.  What is the cost of financing the subsidy to government", chapter=chapter4_2, topic=topic39, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/subswithn.png")
        question9 = Question(text="The above diagram shows the impact of a subsidy in the market for agricultural products in the EU.  Assuming no externalities, which area represents the deadweight loss arising as a result of the subsidy?", chapter=chapter4_2, topic=topic39, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/subswithn.png")
        question10 = Question(text="The above diagram shows the impact of a subsidy in the market for agricultural products in the EU.  What is the total change to consumer expenditure as a result of the subsidy?", chapter=chapter4_2, topic=topic39, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/subswithnumbs.png")
        question11 = Question(text="The above diagram shows the impact of a subsidy in the market for agricultural products in the EU.  What area represents producer surplus after imposition of the subsidy?", chapter=chapter4_2, topic=topic39, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/subswithn.png")
        question12 = Question(text="The above diagram shows the impact of a subsidy in the market for agricultural products in the EU.  What is the total value of consumer surplus after imposition of the subsidy?", chapter=chapter4_2, topic=topic39, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/subswithnumbs.png")
        question13 = Question(text="The above diagram shows the impact of a subsidy in the market for agricultural products in the EU.  What area represents consumer surplus after imposition of the subsidy?", chapter=chapter4_2, topic=topic39, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/subswithn.png")
        question14 = Question(text="The above diagram shows the impact of a subsidy in the market for agricultural products in the EU.  What is the total value of producer surplus after imposition of the subsidy?", chapter=chapter4_2, topic=topic39, image_url = "https://evtds-seeds.s3.us-east-2.amazonaws.com/subswithn.png")
   
        questions = [question1, question2, question3, question4, question5, question6, question7, question8,
                     question9, question10, question11, question12, question13, question14]
        

        answer1a = Answer(text="Consumers buy fewer electric cars", question=question1, is_correct=False)
        answer1b = Answer(text="Consumers buy more gas powered cars cars", question=question1, is_correct=False)
        answer1c = Answer(text="Producers sell fewer electric cars", question=question1, is_correct=False)
        answer1d = Answer(text="The market price consumers pay for electric cars goes down", question=question1, is_correct=True)
        answer1e = Answer(text="The revenue per electric car sold that producers earn goes down ", question=question1, is_correct=False)
  
        answer2a =Answer(text="35 units", question=question2, is_correct=False)
        answer2b =Answer(text="135 units", question=question2, is_correct=False)
        answer2c =Answer(text="$1", question=question2, is_correct=False)
        answer2d =Answer(text="$3", question=question2, is_correct=False)
        answer2e =Answer(text="$4", question=question2, is_correct=True)

        answer3a =Answer(text="To restrict the quantity consumed of a particular good, especially among minors", question=question3, is_correct=True)
        answer3b =Answer(text="To lower the price of the good for consumers", question=question3, is_correct=False)
        answer3c =Answer(text="To help raise the revenues of producers", question=question3, is_correct=False)
        answer3d =Answer(text="To increase the quantity sold in the market", question=question3, is_correct=False)
        answer3e =Answer(text="To encourage consumers to purchase a greater quantity of the good", question=question3, is_correct=False)

        answer4a =Answer(text="More students attend higher education institutions", question=question4, is_correct=False)
        answer4b =Answer(text="The price students pay for higher education falls", question=question4, is_correct=False)
        answer4c =Answer(text="Higher education revenues rise", question=question4, is_correct=False)
        answer4d =Answer(text="Higher education institutions supply a greater quantity of education", question=question4, is_correct=False)
        answer4e =Answer(text="The price that higher educations receive for supplying education falls", question=question4, is_correct=True)
        
        answer5a =Answer(text="The size of the subsidy is $B - $C", question=question5, is_correct=False)
        answer5b =Answer(text="The size of the subsidy is $A - $C", question=question5, is_correct=True)
        answer5c =Answer(text="The size of the subsidy is $A - $B", question=question5, is_correct=False)
        answer5d =Answer(text="Price received by producers after implementing the subsidy is $C", question=question5, is_correct=False)
        answer5e =Answer(text="Price paid by consumers after implementing the subsidy is $A", question=question5, is_correct=True)

        answer6a =Answer(text="The quantity sold of solar panels will fall", question=question6, is_correct=False)
        answer6b =Answer(text="The price paid by consumers to purchase solar panels will rise", question=question6, is_correct=True)
        answer6c =Answer(text="The price received by producers for selling solar panels will rise", question=question6, is_correct=True)
        answer6d =Answer(text="The supply curve for solar panels will shift upwards by the amount of the subsidy per unit", question=question6, is_correct=False)
        answer6e =Answer(text="The market supply for solar panels will decrease", question=question6, is_correct=False)

        answer7a = Answer(text="dkh0", question=question7, is_correct=False)
        answer7b = Answer(text="cjg0", question=question7, is_correct=False)
        answer7c = Answer(text="bikd", question=question7, is_correct=False)
        answer7d = Answer(text="bih0", question=question7, is_correct=True)
        answer7e = Answer(text="ejc", question=question7, is_correct=False)

        answer8a = Answer(text="bih0", question=question8, is_correct=False)
        answer8b = Answer(text="bikd", question=question8, is_correct=True)
        answer8c = Answer(text="bijc", question=question8, is_correct=False)
        answer8d = Answer(text="cjkd", question=question8, is_correct=False)
        answer8e = Answer(text="dkh0", question=question8, is_correct=False)

        answer9a = Answer(text="dme", question=question9, is_correct=False)
        answer9b = Answer(text="cje", question=question9, is_correct=False)
        answer9c = Answer(text="ajc", question=question9, is_correct=False)
        answer9d = Answer(text="ijk", question=question9, is_correct=True)
        answer9e = Answer(text="jkn", question=question9, is_correct=False)

        answer10a = Answer(text="Consumer expenditure increases by $10", question=question10, is_correct=True)
        answer10b = Answer(text="Consumer expenditure decreases by $10", question=question10, is_correct=False)
        answer10c = Answer(text="Consumer expenditure does not change", question=question10, is_correct=False)
        answer10d = Answer(text="Consumer expenditure increases by $130", question=question10, is_correct=False)
        answer10e = Answer(text="Consumer expenditure increases by $70", question=question10, is_correct=False)

        answer11a = Answer(text="dme", question=question11, is_correct=False)
        answer11b = Answer(text="cje", question=question11, is_correct=False)
        answer11c = Answer(text="bie", question=question11, is_correct=True)
        answer11d = Answer(text="ajc", question=question11, is_correct=False)
        answer11e = Answer(text="akd", question=question11, is_correct=False)

        answer12a = Answer(text="$80", question=question12, is_correct=False)
        answer12b = Answer(text="$160", question=question12, is_correct=True)
        answer12c = Answer(text="$240", question=question12, is_correct=False)
        answer12d = Answer(text="$280", question=question12, is_correct=False)
        answer12e = Answer(text="$400", question=question12, is_correct=False)
                          
        answer13a = Answer(text="dme", question=question14, is_correct=False)
        answer13b = Answer(text="cje", question=question14, is_correct=False)
        answer13c = Answer(text="bie", question=question14, is_correct=False)
        answer13d = Answer(text="ajc", question=question14, is_correct=False)
        answer13e = Answer(text="akd", question=question14, is_correct=True)

        answer14a = Answer(text="$45", question=question14, is_correct=False)
        answer14b = Answer(text="$80", question=question14, is_correct=True)
        answer14c = Answer(text="$100", question=question14, is_correct=False)
        answer14d = Answer(text="$280", question=question14, is_correct=False)
        answer14e = Answer(text="$400", question=question14, is_correct=False)


        answers = [
                answer1a, answer1b, answer1c, answer1d, answer1e,
                answer2a, answer2b, answer2c, answer2d, answer2e,
                answer3a, answer3b, answer3c, answer3d, answer3e,
                answer4a, answer4b, answer4c, answer4d, answer4e,
                answer5a, answer5b, answer5c, answer5d, answer5e,
                answer6a, answer6b, answer6c, answer6d, answer6e,
                answer7a, answer7b, answer7c, answer7d, answer7e,
                answer8a, answer8b, answer8c, answer8d, answer8e,
                answer9a, answer9b, answer9c, answer9d, answer9e,
                answer10a, answer10b, answer10c, answer10d, answer10e,
                answer11a, answer11b, answer11c, answer11d, answer11e,
                answer12a, answer12b, answer12c, answer12d, answer12e,
                answer13a, answer13b, answer13c, answer13d, answer13e,
                answer14a, answer14b, answer14c, answer14d, answer14e
        ]
        print('seeding chapter')
        db.session.add(chapter4_2)
        print('seeding topics')
        db.session.add_all(topics)
        print('seeding questions')
        db.session.add_all(questions)
        print('seeding answers')
        db.session.add_all(answers)
        db.session.commit()
        print("Chapter seeded")

def main():
    with app.app_context():
        try:
            seed_subsidies_chapter()
        except IntegrityError as e:
            db.session.rollback()  # Now within the app context
            print(f"There was an error seeding the chapter: {e}")

if __name__=="__main__":
    try:
        main()
    except IntegrityError:
        db.session.rollback()
        print("There was an error seeding the database")
                          