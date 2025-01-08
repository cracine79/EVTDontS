from exts import db
from main import create_app
from config import ProdConfig
from models import Chapter, QuestionTopic, Unit, Question, Answer
from sqlalchemy.exc import IntegrityError


app = create_app(ProdConfig)

def seed_tax_chapter_blurbs():
    chapter = db.session.get(Chapter, 35)    
    print("Chapter", chapter)
    chapter.video_blurb = "Welcome to the first video in your Government Intervention Unit, where the market's smooth sailing meets the iceberg of good intentions. Watch as we explore how the government wades in, armed with taxes, subsidies, and the occasional 'oops, didn't see that coming!' It's like a reality show where the market's the hero, and the government is the overly confident contestant causing drama. \n\n Remember: watch the video, take the quiz, and brace yourself for the classic duo—taxes and death—because at least one of them has homework. Nobody likes taxes, but hey, at least they're not grading your quizzes... yet."
    chapter.quiz_blurb = "Congrats on surviving the video! Now it’s time for the Taxes and Death Quiz Spectacular—where the questions are taxing, but thankfully not fatal. Test your knowledge of government intervention, and see if you can outsmart the invisible hand (and maybe the heavy one too). \n\n Taxes are no fun, but at least this quiz won’t take a percentage of your paycheck. (We realize that this joke is referring to direct, not indirect taxes, so completely inappropriate for this section.  So sue us!) Good luck—you’ve got this!"
    db.session.commit()
    print('added blurbios!')
def main():
    with app.app_context():
        seed_tax_chapter_blurbs()

if __name__=="__main__":
    try:
        main()
    except IntegrityError:
        db.session.rollback()
        print("There was an error seeding the database")