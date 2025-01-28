from exts import db
from main import create_app
from config import ProdConfig
from models import Chapter, QuestionTopic, Unit, Question, Answer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text


app = create_app(ProdConfig)

def seed_tax_chapter_topic():

    print('seeding chapter')
    unit4 = db.session.get(Unit, 4)
    if not unit4:
        print("Unit with ID 4 does not exist. Seeding aborted.")
        return
    video_blurb = "Welcome to the first video in your Government Intervention Unit, where the market's smooth sailing meets the iceberg of good intentions. Watch as we explore how the government wades in, armed with taxes, subsidies, and the occasional 'oops, didn't see that coming!' It's like a reality show where the market's the hero, and the government is the overly confident contestant causing drama. \n\n Remember: watch the video, take the quiz, and brace yourself for the classic duo—taxes and death—because at least one of them has homework. Nobody likes taxes, but hey, at least they're not grading your quizzes... yet."
    quiz_blurb =  "Congrats on surviving the video! Now it’s time for the Taxes and Death Quiz Spectacular—where the questions are taxing, but thankfully not fatal. Test your knowledge of government intervention, and see if you can outsmart the invisible hand (and maybe the heavy one too). \n\n Taxes are no fun, but at least this quiz won’t take a percentage of your paycheck. (We realize that this joke is referring to direct, not indirect taxes, so completely inappropriate for this section.  So sue us!) Good luck—you’ve got this!"
    name = "4.1 Taxes"
    content = f"{name}{quiz_blurb}{video_blurb}"
    search_vector = text(f"to_tsvector('english', :content)")
    
    chapter4_1 = Chapter(name=name, unit=unit4, video_url="https://www.youtube.com/embed/RakGotBbbKY?si=lvwOdy9K9HK3h7Ct", order=25, video_blurb=video_blurb, quiz_blurb=quiz_blurb,
                         search_vector=search_vector
                        )

    topic34 = QuestionTopic(name='Taxes - Impact on price and quantity', chapter=chapter4_1)
    topic35 = QuestionTopic(name='Taxes - Impact on Producer Revenue, Consumer Expenditure & Government Revenue', chapter=chapter4_1)
    topic36 = QuestionTopic(name='Taxes - Impact on Social Surplus & Deadweight Loss', chapter=chapter4_1)
    topic37 = QuestionTopic(name='Taxes - Elasticity and Tax Burden', chapter=chapter4_1)

    topics = [topic34, topic35, topic36, topic37]

    db.session.add(chapter4_1)
    db.session.add_all(topics)

    db.session.commit()
    print("Chapter seeded")

def main():
    with app.app_context():
        try:
            seed_tax_chapter_topic()
        except IntegrityError as e:
            db.session.rollback()  # Now within the app context
            print(f"There was an error seeding the chapter: {e}")

if __name__=="__main__":
    try:
        main()
    except IntegrityError:
        db.session.rollback()
        print("There was an error seeding the database")