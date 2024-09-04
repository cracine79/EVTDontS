from exts import db
from main import create_app
from models import User, Unit, Chapter, Question, QuestionTopic, Answer, UserPerformance
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from config import ProdConfig

app = create_app(ProdConfig)

def seed_users():
    print("Seeding users")
    password = "password"
    hashed_password=generate_password_hash(password)

    user1 = User(username="charlee", email="user1@exdample.com", password_hash=hashed_password)
    user2 = User(username="user", email="user1@exdample.com", password_hash=hashed_password)

    db.session.add_all([user1, user2])
    db.session.commit()

    return user1, user2

def seed_units():
    print("Seeding units")
    unit1 = Unit(name="Unit 1: Introduction to Economic Concepts", subject="both")
    unit2 = Unit(name="Unit 2: Supply and Demand", subject="both")
    unit3 = Unit(name="Unit 3: Elasticity", subject="both")

    db.session.add_all([unit1, unit2, unit3])
    db.session.commit()
    
    return [unit1, unit2, unit3]

def seed_chapters(units):
    print("seeding chapters")
    chapter1_1 = Chapter(name="1.1 Scarcity, Choice and Opportunity Cost", unit = units[0], video_url="https://www.youtube.com/embed/mfGKKxwC_fE")
    chapter1_2 = Chapter(name="1.2 Factors of Production", unit = units[0], video_url="https://www.youtube.com/embed/WqlGzTYXd0U")
    chapter1_3 = Chapter(name="1.3 Economic Systems", unit = units[0], video_url="https://www.youtube.com/embed/X0ak8ID7zY8")
    chapter1_4a = Chapter(name="1.4a The Production Possibilities Curve", unit = units[0], video_url="https://www.youtube.com/embed/HeUTq7VwZaI")
    chapter1_4b = Chapter(name="1.4b Opportunity Cost and the PPF", unit = units[0], video_url="https://www.youtube.com/embed/6CQvC5rugh4")
    chapter1_5 = Chapter(name="1.5 Absolute and Comparative Advantage", unit = units[0], video_url="https://www.youtube.com/embed/Z7dXOetE3CQ")
    chapter1_5a = Chapter(name="1.5a Answering AP and University Level Comparative Advantage Questions", unit=units[0], video_url="https://www.youtube.com/embed/euARcQwvT5Y")
    chapter2_1 = Chapter(name="2.1 Demand Introduced", unit = units[1], video_url="https://www.youtube.com/embed/xiS1DiQbo74")
    chapter2_1a = Chapter(name="2.1a Non-Price Determinants of Demand", unit = units[1], video_url="https://www.youtube.com/embed/t9vqT36mg2E")
    chapter2_2 = Chapter(name="2.2 Supply Introduced", unit = units[1], video_url="https://www.youtube.com/embed/AUPcL91u008")
    chapter2_2a = Chapter(name="2.2a Non-Price Determinants of Supply", unit = units[1], video_url="https://www.youtube.com/embed/QByejdJI58o")
    chapter2_3 = Chapter(name="2.3 Supply and Demand in Equilibrium", unit = units[1], video_url="https://www.youtube.com/embed/V10jYy7maS4")
    chapter2_4 = Chapter(name="2.4 Shifts to Supply and Demand", unit = units[1], video_url="https://www.youtube.com/embed/Cf0J-2dY7Dg")
    chapter2_5 = Chapter(name="2.5 Simultaneous Shifts to Supply and Demand", unit = units[1], video_url="https://www.youtube.com/embed/ZtEp5B-xeMI")
    chapter2_6a = Chapter(name="2.6a Marginal Utility, Marginal Benefit, and Demand", unit = units[1], video_url="https://www.youtube.com/embed/9UzdtdrjURY")
    chapter2_6b = Chapter(name="2.6b Marginal Cost and Supply", unit = units[1], video_url="https://www.youtube.com/embed/QByejdJI58o")
    chapter2_7 = Chapter(name="2.7 Consumer Surplus, Producer Surplus, and Social Surplus", unit = units[1], video_url="https://www.youtube.com/embed/HNhtJYbagF0")
    chapter2_8 = Chapter(name="2.8 Allocative Efficiency", unit = units[1], video_url="https://www.youtube.com/embed/kPwEpVKTD0A")
    chapter3_1 = Chapter(name="3.1 Price Elasticity of Demand (PED)", unit = units[2], video_url="https://www.youtube.com/embed/bYUkZeZfZO8")
    chapter3_2 = Chapter(name="3.2 Determinants of Price Elasticity of Demand", unit = units[2], video_url="https://www.youtube.com/embed/40ZX1_6ebEY")
    chapter3_3 = Chapter(name="3.3 PED and Total Revenue", unit = units[2], video_url="https://www.youtube.com/embed/A7MHjOWFTv0")
    chapter3_4 = Chapter(name="3.4 Cross Price Elasticity of Demand (XED)", unit = units[2], video_url="https://www.youtube.com/embed/O-gLeuGNgAs")
    chapter3_5 = Chapter(name="3.5 Income Elasticity of Demand", unit = units[2], video_url="https://www.youtube.com/embed/lZVZYc1yVbY")
    chapter3_6 = Chapter(name="3.6 Price Elasticity of Supply", unit = units[2], video_url="https://www.youtube.com/embed/4Jpvus1kpr8")

    chapters = [chapter1_1, chapter1_2, chapter1_3, chapter1_4a, chapter1_4b, chapter1_5, chapter1_5a, chapter2_1, chapter2_1a, chapter2_2, chapter2_2a, chapter2_3, chapter2_5, chapter2_4, chapter2_6a, chapter2_6b, chapter2_7, chapter2_8, chapter3_1, chapter3_2, chapter3_3, chapter3_4, chapter3_5, chapter3_6]
    db.session.add_all(chapters)
    db.session.commit()

    return chapters

def assign_units_to_users(users, units):
    print("assigning units")
    for unit in units:
        users[0].units.append(unit)
    
    users[1].units.append(units[0])

    db.session.commit()

def seed_topics():
    topic1=QuestionTopic(name="Scarcity")

    db.session.add(topic1)
    db.session.commit()

    return [topic1]

def seed_questions(chapters, topics):
    print("seeding questions")
    question1=Question(text="The fundamental issue that economics examines and the primary reason it exists as a subject is that of:", chapter=chapters[0], topic=topics[0])
    question2=Question(text="The basic problem that all economies face is deciding how to best utilize", chapter=chapters[0], topic=topics[0])
    question3=Question(text="Scarcity exists because", chapter=chapters[0], topic=topics[0])
    question4=Question(text="Individuals in all societies are forced to make choices regarding the types of goods and services to be produced and consumed because", chapter=chapters[0], topic=topics[0])
    
    questions = [question1, question2, question3, question4]
    print("questions created")
    db.session.add_all(questions)
    print("questions added")
    db.session.commit()
    print('questions committed')


    return questions

def seed_answers(questions):
    print("seeding Questions")
    answer1a=Answer(text="Oligopoly", question=questions[0], is_correct=False)
    answer1b=Answer(text="Positive externality", question=questions[0], is_correct=False)
    answer1c=Answer(text="Scarcity", question=questions[0], is_correct=True)
    answer1d=Answer(text="Surpluses of goods", question=questions[0], is_correct=False)
    answer1e=Answer(text="The substitution effect", question=questions[0], is_correct=False)

    answer2a=Answer(text="Unlimited resources to satisfy limited wants", question=questions[1], is_correct=False)
    answer2b=Answer(text="Unlimited resources to satisfy unlimited wants", question=questions[1], is_correct=False)
    answer2c=Answer(text="Limited resource to satisfy unlimited wants", question=questions[1], is_correct=True)
    answer2d=Answer(text="Limited resources to satisfy limited wants", question=questions[1], is_correct=False)
    answer2e=Answer(text="Limited resources to provide a social safety net", question=questions[1], is_correct=False)

    answer3a=Answer(text="Natural resources are essentially free, so unlimited", question=questions[2], is_correct=False)
    answer3b=Answer(text="Physical capital lasts for many years ", question=questions[2], is_correct=False)
    answer3c=Answer(text="Birth rates are rapidly declining, globally", question=questions[2], is_correct=False)
    answer3d=Answer(text="Innovation ensures economic growth", question=questions[2], is_correct=False)
    answer3e=Answer(text="Human wants exceed the productive capacity available, finite resources", question=questions[2], is_correct=True)

    answer4a=Answer(text="Free markets are less efficient than publicly provided goods", question=questions[3], is_correct=False)
    answer4b=Answer(text="Free markets are profit oriented", question=questions[3], is_correct=False)
    answer4c=Answer(text="The consumption of goods includes opportunity costs", question=questions[3], is_correct=False)
    answer4d=Answer(text="Resources are scarce and human wants and needs are unlimited", question=questions[3], is_correct=True)
    answer4e=Answer(text="Resources are allocated in a way that is often unequal and unfair", question=questions[3], is_correct=False)


    answers = [answer1a, answer1b, answer1c, answer1d, answer1e, answer2a, answer2b, answer2c, answer2e, answer2d, answer3a, answer3b, answer3c, answer3d, answer3e, answer4a, answer4b, answer4c, answer4d, answer4e]

    db.session.add_all(answers)
    db.session.commit()


def main():
    with app.app_context():
        db.drop_all()
        db.create_all()


        print("deleting old DB")
        db.session.query(User).delete()
        db.session.query(Unit).delete()
        db.session.query(Chapter).delete()
        db.session.query(Question).delete()
        db.session.commit()
        print("DB Deleted")


        users = seed_users()
        units= seed_units()
        assign_units_to_users(users, units)
        chapters = seed_chapters(units)
        topics = seed_topics()
        questions = seed_questions(chapters, topics)
        seed_answers(questions)
        

        print("Database seeded succsesfully")

        db.session.execute('ALTER SEQUENCE users_id_seq RESTART WITH 1')  # Adjust sequence name if needed
        db.session.execute('ALTER SEQUENCE units_id_seq RESTART WITH 1')
        db.session.execute('ALTER SEQUENCE chapters_id_seq RESTART WITH 1')
        db.session.execute('ALTER SEQUENCE questions_id_seq RESTART WITH 1')
        db.session.commit()

if __name__=="__main__":
    try:
        main()
    except IntegrityError:
        db.session.rollback()
        print("There was an error seeding the database")