from exts import db
from main import create_app
from models import User, Unit, Chapter, Question, QuestionTopic, Answer, UserPerformance, UserChapterProgress
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from config import ProdConfig
from sqlalchemy import text

app = create_app(ProdConfig)

def seed_users():
    print("Seeding users")
    password = "password"
    hashed_password=generate_password_hash(password)

    user1 = User(username="charlee", email="user1@exdample.com", password_hash=hashed_password)
    user2 = User(username="user", email="user1@exdample.com", password_hash=hashed_password)

    users = [user1, user2]
    db.session.add_all(users)
    db.session.commit()

    return users

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
    chapter1_1 = Chapter(name="1.1 Scarcity, Choice and Opportunity Cost", unit = units[0], video_url="https://www.youtube.com/embed/mfGKKxwC_fE", order=1)
    chapter1_2 = Chapter(name="1.2 Factors of Production", unit = units[0], video_url="https://www.youtube.com/embed/WqlGzTYXd0U", order=2)
    chapter1_3 = Chapter(name="1.3 Economic Systems", unit = units[0], video_url="https://www.youtube.com/embed/X0ak8ID7zY8", order=3)
    chapter1_4a = Chapter(name="1.4a The Production Possibilities Curve", unit = units[0], video_url="https://www.youtube.com/embed/HeUTq7VwZaI", order=4)
    chapter1_4b = Chapter(name="1.4b Opportunity Cost and the PPF", unit = units[0], video_url="https://www.youtube.com/embed/6CQvC5rugh4", order=5)
    chapter1_5 = Chapter(name="1.5 Absolute and Comparative Advantage", unit = units[0], video_url="https://www.youtube.com/embed/Z7dXOetE3CQ", order=6)
    chapter1_5a = Chapter(name="1.5a Answering AP and University Level Comparative Advantage Questions", unit=units[0], video_url="https://www.youtube.com/embed/euARcQwvT5Y", order=7)
    chapter2_1 = Chapter(name="2.1 Demand Introduced", unit = units[1], video_url="https://www.youtube.com/embed/xiS1DiQbo74", order=8)
    chapter2_1a = Chapter(name="2.1a Non-Price Determinants of Demand", unit = units[1], video_url="https://www.youtube.com/embed/t9vqT36mg2E", order=9)
    chapter2_2 = Chapter(name="2.2 Supply Introduced", unit = units[1], video_url="https://www.youtube.com/embed/AUPcL91u008", order=10)
    chapter2_2a = Chapter(name="2.2a Non-Price Determinants of Supply", unit = units[1], video_url="https://www.youtube.com/embed/QByejdJI58o", order=11)
    chapter2_3 = Chapter(name="2.3 Supply and Demand in Equilibrium", unit = units[1], video_url="https://www.youtube.com/embed/V10jYy7maS4", order=12)
    chapter2_4 = Chapter(name="2.4 Shifts to Supply and Demand", unit = units[1], video_url="https://www.youtube.com/embed/Cf0J-2dY7Dg", order=13)
    chapter2_5 = Chapter(name="2.5 Simultaneous Shifts to Supply and Demand", unit = units[1], video_url="https://www.youtube.com/embed/ZtEp5B-xeMI", order=14)
    chapter2_6a = Chapter(name="2.6a Marginal Utility, Marginal Benefit, and Demand", unit = units[1], video_url="https://www.youtube.com/embed/9UzdtdrjURY", order=15)
    chapter2_6b = Chapter(name="2.6b Marginal Cost and Supply", unit = units[1], video_url="https://www.youtube.com/embed/QByejdJI58o", order=16)
    chapter2_7 = Chapter(name="2.7 Consumer Surplus, Producer Surplus, and Social Surplus", unit = units[1], video_url="https://www.youtube.com/embed/HNhtJYbagF0", order=17)
    chapter2_8 = Chapter(name="2.8 Allocative Efficiency", unit = units[1], video_url="https://www.youtube.com/embed/kPwEpVKTD0A", order=18)
    chapter3_1 = Chapter(name="3.1 Price Elasticity of Demand (PED)", unit = units[2], video_url="https://www.youtube.com/embed/bYUkZeZfZO8", order=19)
    chapter3_2 = Chapter(name="3.2 Determinants of Price Elasticity of Demand", unit = units[2], video_url="https://www.youtube.com/embed/40ZX1_6ebEY", order=20)
    chapter3_3 = Chapter(name="3.3 PED and Total Revenue", unit = units[2], video_url="https://www.youtube.com/embed/A7MHjOWFTv0", order=21)
    chapter3_4 = Chapter(name="3.4 Cross Price Elasticity of Demand (XED)", unit = units[2], video_url="https://www.youtube.com/embed/O-gLeuGNgAs", order=22)
    chapter3_5 = Chapter(name="3.5 Income Elasticity of Demand", unit = units[2], video_url="https://www.youtube.com/embed/lZVZYc1yVbY", order=23)
    chapter3_6 = Chapter(name="3.6 Price Elasticity of Supply", unit = units[2], video_url="https://www.youtube.com/embed/4Jpvus1kpr8", order=24)

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

def seed_topics(chapters):
    topic1=QuestionTopic(name="Scarcity", chapter=chapters[0])
    topic2=QuestionTopic(name='Opportunity Cost', chapter=chapters[0])
    topic3=QuestionTopic(name="Factors of Production", chapter=chapters[1])
    topic4=QuestionTopic(name='Economic Systems', chapter=chapters[2])
    

    topics = [topic1, topic2, topic3, topic4]
    db.session.add_all(topics)
    db.session.commit()
    return topics

def seed_questions(chapters, topics):
    print("seeding questions")
    question1=Question(text="The fundamental issue that economics examines and the primary reason it exists as a subject is that of:", chapter=chapters[0], topic=topics[0])
    question2=Question(text="The basic problem that all economies face is deciding how to best utilize", chapter=chapters[0], topic=topics[0])
    question3=Question(text="Scarcity exists because", chapter=chapters[0], topic=topics[0])
    question4=Question(text="Individuals in all societies are forced to make choices regarding the types of goods and services to be produced and consumed because", chapter=chapters[0], topic=topics[0])
    question5=Question(text="If you see a question about the fundamental/primary question of economics, you know it is somehow related to the idea of:", chapter=chapters[0], topic=topics[0])
    question6=Question(text='The opportunity cost of an activity is', chapter=chapters[0], topic=topics[1])
    question7=Question(text='Fredrick chose to attend college after graduating from high school.  Samuel went to work full time directly out of college.  Which of the following best describes the opportunity costs for these decisions?', chapter=chapters[0], topic=topics[1])
    question8=Question(text='Sarah has two free hours this evening.  She can attend a movie, which costs $10.  She can babysit for her neighbor and earn $7.50 an hour.  She can also go to work at her part time job and earn $10 an hour.  Sarah chooses to go to the movie.  Which of the following is true?', chapter=chapters[0], topic=topics[1])
    question9=Question(text='Which of the following best defines opportunity cost?', chapter=chapters[0], topic=topics[1])
    question10=Question(text='The concept of opportunity cost would become irrelevant if', chapter=chapters[0], topic=topics[1])    
    question11 = Question(text="Which of the following statements best represents the concept of scarcity?", chapter=chapters[0], topic=topics[0])
    question12 = Question(text="Why is scarcity considered the basic economic problem?", chapter=chapters[0], topic=topics[0])
    question13 = Question(text="Which of the following statements is true about scarcity?", chapter=chapters[0], topic=topics[0])
    question14 = Question(text="Which of the following statements about scarcity and choice is incorrect?", chapter=chapters[0], topic=topics[0])
    question15 = Question(text="The concept of scarcity can best be defined as:", chapter=chapters[0], topic=topics[0])
    question16 = Question(text="The opportunity cost of choosing to study instead of working is", chapter=chapters[0], topic=topics[1])
    question17 = Question(text="Which of the following is a defining characteristic of a market economy?", chapter=chapters[2], topic=topics[3])
    question18 = Question(text="A fundamental difference between a market economy and command economy lies in which of the following?", chapter=chapters[2], topic=topics[3])
    question19 = Question(text="Unlike a market economy, a command economy uses", chapter=chapters[2], topic=topics[3])
    question20 = Question(text="Which economic system is characterized by a combination of government intervention and market force?", chapter=chapters[2], topic=topics[3])
    question21 = Question(text="In a market economy, prices are primarily determined by: ", chapter=chapters[2], topic=topics[3])
    question22 = Question(text="Which economic system places the most emphasis on individual self-interest as a driving force for economic activity? ", chapter=chapters[2], topic=topics[3])
    question23 = Question(text='Which of the following factors of production refers to the physical space where production occurs and the natural resources used in production?',chapter=chapters[1], topic=topics[2])
    question24 = Question(text='A factory building, machinery, and equipment are examples of which factor of production?',chapter=chapters[1], topic=topics[2])
    question25 = Question(text='When referring to the four factors of production, which of the following would not be referred to as capital?',chapter=chapters[1], topic=topics[2])
    question26 = Question(text='Which of the following describes the factor of production known as Land?',chapter=chapters[1], topic=topics[2])
    question27 = Question(text='Which of the following is an example of Capital as a factor of production?',chapter=chapters[1], topic=topics[2])
    question28 = Question(text='Which of the following statements about factors of production is true?',chapter=chapters[1], topic=topics[2])

    
    
    questions = [question1, question2, question3, 
                 question4, question5, question6, 
                 question7, question8, question9, 
                 question10, question11, question12,
                 question13, question14, question15,
                 question16, question17, question18,
                 question19, question20, question21,
                 question22, question23, question24,
                 question25, question26, question27,
                 question28]
    print("questions created")
    db.session.add_all(questions)
    print("questions added")
    db.session.commit()
    print('questions committed')


    return questions

def seed_answers(questions):
    print("seeding Answers")
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

    answer5a=Answer(text='Scarcity', question=questions[4], is_correct=True)
    answer5b=Answer(text='The Central Bank', question=questions[4], is_correct=False)
    answer5c=Answer(text='The Stock Market', question=questions[4], is_correct=False)
    answer5d=Answer(text='Money', question=questions[4], is_correct=False)
    answer5e=Answer(text='Wealth', question=questions[4], is_correct=False)

    answer6a=Answer(text='The value of the benefit received from engaging in the activity', question=questions[5], is_correct=False)
    answer6b=Answer(text='Zero, if the activity is rewarding', question=questions[5], is_correct=False)
    answer6c=Answer(text='The amount of money spent to engage in the activity', question=questions[5], is_correct=False)
    answer6d=Answer(text='The value of the foregone benefit of the next best alternative', question=questions[5], is_correct=True)
    answer6e=Answer(text='The usm of bneefits from all foregone alternatives', question=questions[5], is_correct=False)
   
    answer7a=Answer(text='Fredrick’s opportunity cost includes the foregone salary he could have earned if he had gone to work.', question=questions[6], is_correct=True)
    answer7b=Answer(text='Frederick’s total opportunity cost is the tuition he must pay to attend school plus the price of books.', question=questions[6], is_correct=False)
    answer7c=Answer(text='Samuel doesn’t have an opportunity cost, as he is earning money directly.', question=questions[6], is_correct=False)
    answer7d=Answer(text='Samuel’s opportunity cost includes the cost of purchasing food to survive to work.', question=questions[6], is_correct=False)
    answer7e=Answer(text='Samuel’s opportunity costs is certainly less than Fredrick’s', question=questions[6], is_correct=False)
    
    answer8a=Answer(text='The opportunity cost of Sarah’s decision includes the $15 she could have earned from babysitting and the $20 she could have earned from her part time job. ', question=questions[7], is_correct=False)
    answer8b=Answer(text='The opportunity cost of Sarah’s decision does not include the $10 she paid to go to the movie.', question=questions[7], is_correct=False)
    answer8c=Answer(text='The opportunity cost of Sarah’s decision includes both the $10 she would still have if she didn’t go to the movie, plus the $20 she could have earned from the part time job.', question=questions[7], is_correct=True)
    answer8d=Answer(text='Since both the other options involve earning money and not spending, there is no opportunity cost to Sarah’s decision.', question=questions[7], is_correct=False)
    answer8e=Answer(text='It is not possible to determine the opportunity cost of Sarah’s decision, as we do not know if she enjoyed the movie or not. ', question=questions[7], is_correct=False)
    
    answer9a=Answer(text='The cost of purchasing all goods and services in an economy', question=questions[8], is_correct=False)
    answer9b=Answer(text='The lowest possible cost combination of labor and capital a firm can employ', question=questions[8], is_correct=False)
    answer9c=Answer(text='The cost of producing when profits are maximized', question=questions[8], is_correct=False)
    answer9d=Answer(text='The sum of the values of all forgone options when one makes a choice', question=questions[8], is_correct=False)
    answer9e=Answer(text='The value of the next best alternative that one forgoes when making a choice', question=questions[8], is_correct=True)

    answer10a=Answer(text='Everyone’s salary increased by 100%', question=questions[9], is_correct=False)
    answer10b=Answer(text='Market failure were eliminated', question=questions[9], is_correct=False)
    answer10c=Answer(text='Real wages rose at the same rate as inflation', question=questions[9], is_correct=True)
    answer10d=Answer(text='Supply of all resources became unlimited', question=questions[9], is_correct=False)
    answer10e=Answer(text='People stopped consuming and reinvested all income into production of capital', question=questions[9], is_correct=False)

    answer11a = Answer(text="Resources are unlimited, and human desires are limited.", question=questions[10], is_correct=False)
    answer11b = Answer(text="Human desires are unlimited, and resources are limited.", question=questions[10], is_correct=True)
    answer11c = Answer(text="All goods and services are freely available.", question=questions[10], is_correct=False)
    answer11d = Answer(text="Prices will never change due to resource abundance.", question=questions[10], is_correct=False)
    answer11e = Answer(text="The government can always produce more money to avoid scarcity.", question=questions[10], is_correct=False)

    answer12a = Answer(text="Because not all resources have a monetary cost.", question=questions[11], is_correct=False)
    answer12b = Answer(text="Because individuals and societies have to choose how to allocate limited resources.", question=questions[11], is_correct=True)
    answer12c = Answer(text="Because there are no opportunity costs in decision-making.", question=questions[11], is_correct=False)
    answer12d = Answer(text="Because resources and wants are always perfectly matched.", question=questions[11], is_correct=False)
    answer12e = Answer(text="Because not everyone can be employed at the same time.", question=questions[11], is_correct=False)

    answer13a = Answer(text="Scarcity affects only developing economies.", question=questions[12], is_correct=False)
    answer13b = Answer(text="Scarcity exists because human wants exceed the resources available.", question=questions[12], is_correct=True)
    answer13c = Answer(text="Scarcity can be eliminated by producing more goods.", question=questions[12], is_correct=False)
    answer13d = Answer(text="Scarcity is not a problem when an economy is growing.", question=questions[12], is_correct=False)
    answer13e = Answer(text="Scarcity exists only in market economies.", question=questions[12], is_correct=False)

    answer14a = Answer(text="Scarcity requires people to make choices.", question=questions[13], is_correct=False)
    answer14b = Answer(text="Opportunity cost arises because of scarcity.", question=questions[13], is_correct=False)
    answer14c = Answer(text="Scarcity exists in all societies.", question=questions[13], is_correct=False)
    answer14d = Answer(text="Scarcity can be eliminated if we all consume a little less", question=questions[13], is_correct=True)
    answer14e = Answer(text="Scarcity leads to competition for resources.", question=questions[13], is_correct=False)

    answer15a = Answer(text="Limited resources in relation to unlimited wants.", question=questions[14], is_correct=True)
    answer15b = Answer(text="Unlimited resources in relation to limited wants.", question=questions[14], is_correct=False)
    answer15c = Answer(text="The need for government intervention in markets.", question=questions[14], is_correct=False)
    answer15d = Answer(text="The accumulation of wealth by firms and individuals.", question=questions[14], is_correct=False)
    answer15e = Answer(text="A situation where there are no opportunity costs.", question=questions[14], is_correct=False)

    answer16a = Answer(text='The potential income lost from not working during that time.', question=questions[15], is_correct=True)
    answer16b = Answer(text='The cost of books and materials for studying.', question=questions[15], is_correct=False)
    answer16c = Answer(text='The value of leisure time.', question=questions[15], is_correct=False)
    answer16d = Answer(text='The cost of transportation to work.', question=questions[15], is_correct=False)
    answer16e = Answer(text='The enjoyment gained from studying.', question=questions[15], is_correct=False)
    
    answer17a = Answer(text="Private ownership of resources", question=questions[16], is_correct=True)
    answer17b = Answer(text="Progressive income taxes", question=questions[16], is_correct=False)
    answer17c = Answer(text="Equitable distribution of income", question=questions[16], is_correct=False)
    answer17d = Answer(text="Government provided public goods", question=questions[16], is_correct=False)
    answer17e = Answer(text="Central planning for resource allocation", question=questions[16], is_correct=False)

    answer18a = Answer(text="Property rights and protection of private property", question=questions[17], is_correct=True)
    answer18b = Answer(text="Specialization and trade", question=questions[17], is_correct=False)
    answer18c = Answer(text="Market economies have a central economic decision maker", question=questions[17], is_correct=False)
    answer18d = Answer(text="Command economies generally don’t need a government", question=questions[17], is_correct=False)
    answer18e = Answer(text="Days it takes to open a business", question=questions[17], is_correct=False)

    answer19a = Answer(text="Consumer preference to determine output", question=questions[18], is_correct=False)
    answer19b = Answer(text="Prices as signals to producers to change output level", question=questions[18], is_correct=False)
    answer19c = Answer(text="Taxes on imports", question=questions[18], is_correct=False)
    answer19d = Answer(text="Profits as motivators for firms", question=questions[18], is_correct=False)
    answer19e = Answer(text="Centralized planning for economic decision making", question=questions[18], is_correct=True)

    answer20a = Answer(text="Traditional economy", question=questions[19], is_correct=False)
    answer20b = Answer(text="Command economy", question=questions[19], is_correct=False)
    answer20c = Answer(text="Mixed economy", question=questions[19], is_correct=True)
    answer20d = Answer(text="Market economy", question=questions[19], is_correct=False)
    answer20e = Answer(text="Planned economy", question=questions[19], is_correct=False)

    answer21a = Answer(text="Government Regulations", question=questions[20], is_correct=False)
    answer21b = Answer(text="Forces of Supply and Demand", question=questions[20], is_correct=True)
    answer21c = Answer(text="Central Planners", question=questions[20], is_correct=False)
    answer21d = Answer(text="Historical Prices", question=questions[20], is_correct=False)
    answer21e = Answer(text="A fixed price ceiling", question=questions[20], is_correct=False)

    answer22a = Answer(text="Traditional Economy", question=questions[21], is_correct=False)
    answer22b = Answer(text="Command Economy", question=questions[21], is_correct=False)
    answer22c = Answer(text="Cooperative Economy", question=questions[21], is_correct=False)
    answer22d = Answer(text="Market Economy", question=questions[21], is_correct=True)
    answer22e = Answer(text="Psuedo Economy", question=questions[21], is_correct=False)

    answer23a = Answer(text='Land', question=questions[22], is_correct=False)
    answer23b = Answer(text='Capital', question=questions[22], is_correct=False)
    answer23c = Answer(text='Entrepreneurship', question=questions[22], is_correct=False)
    answer23d = Answer(text='Labor', question=questions[22], is_correct=False)
    answer23e = Answer(text='Land', question=questions[22], is_correct=True)

    answer24a = Answer(text='Labor', question=questions[23], is_correct=False)
    answer24b = Answer(text='Capital', question=questions[23], is_correct=True)
    answer24c = Answer(text='Entrepreneurship', question=questions[23], is_correct=False)
    answer24d = Answer(text='Land', question=questions[23], is_correct=False)
    answer24e = Answer(text='Financial capital', question=questions[23], is_correct=False)

    answer25a = Answer(text='Machinery in a factory', question=questions[24], is_correct=False)
    answer25b = Answer(text='Computers in a law firm', question=questions[24], is_correct=False)
    answer25c = Answer(text='The building where a software firm operates', question=questions[24], is_correct=False)
    answer25d = Answer(text='A hot dog vendor’s hot dog stand', question=questions[24], is_correct=False)
    answer25e = Answer(text='The money a hair salon has in its bank account', question=questions[24], is_correct=True)

    answer26a = Answer(text='Natural resources like water and minerals.', question=questions[25], is_correct=True)
    answer26b = Answer(text='Skills and education of workers.', question=questions[25], is_correct=False)
    answer26c = Answer(text='Investment in training programs.', question=questions[25], is_correct=False)
    answer26d = Answer(text='Funds used for purchasing equipment.', question=questions[25], is_correct=False)
    answer26e = Answer(text='Planning and decision-making by executives.', question=questions[25], is_correct=False)

    answer27a = Answer(text='Employee salaries.', question=questions[26], is_correct=False)
    answer27b = Answer(text='The creativity and initiative of business owners.', question=questions[26], is_correct=False)
    answer27c = Answer(text='Buildings, machinery, and technology.', question=questions[26], is_correct=True)
    answer27d = Answer(text='Government grants to start businesses.', question=questions[26], is_correct=False)
    answer27e = Answer(text='The time spent by workers on production.', question=questions[26], is_correct=False)

    answer28a = Answer(text='Entrepreneurship is an unlimited resource.', question=questions[27], is_correct=False)
    answer28b = Answer(text='Labor and Capital are the same.', question=questions[27], is_correct=False)
    answer28c = Answer(text='Land includes all natural resources.', question=questions[27], is_correct=True)
    answer28d = Answer(text='Capital refers only to financial investments.', question=questions[27], is_correct=False)
    answer28e = Answer(text='All resources are considered capital.', question=questions[27], is_correct=False)

    answers = [answer1a, answer1b, answer1c, answer1d, answer1e, 
               answer2a, answer2b, answer2c, answer2e, answer2d, 
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
               answer14a, answer14b, answer14c, answer14d, answer14e, 
               answer15a, answer15b, answer15c, answer15d, answer15e, 
               answer16a, answer16b, answer16c, answer16d, answer16e,
               answer17a, answer17b, answer17c, answer17d, answer17e, 
               answer18a, answer18b, answer18c, answer18d, answer18e,
               answer19a, answer19b, answer19c, answer19d, answer19e,
               answer20a, answer20b, answer20c, answer20e, answer20d, 
               answer21a, answer21b, answer21c, answer21d, answer21e,
               answer22a, answer22b, answer22c, answer22d, answer22e,
               answer23a, answer23b, answer23c, answer23d, answer23e,
               answer24a, answer24b, answer24c, answer24d, answer24e, 
               answer25a, answer25b, answer25c, answer25d, answer25e, 
               answer26a, answer26b, answer26c, answer26d, answer26e,
               answer27a, answer27b, answer27c, answer27d, answer27e, 
               answer28a, answer28b, answer28c, answer28d, answer28e]

    db.session.add_all(answers)
    db.session.commit()


def seed_progress():
    print("seeding progress")
    progress1 = UserChapterProgress(user_id = 1, chapter_id = 1, video_completed=True, quiz_grade=None)
    progress2 = UserChapterProgress(user_id = 1, chapter_id = 2, video_completed=False, quiz_grade=None)
    progresses = [progress1, progress2]
    db.session.add_all(progresses)
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
        db.session.query(UserChapterProgress).delete()
        db.session.commit()
        print("DB Deleted")


        users = seed_users()
        units= seed_units()
        assign_units_to_users(users, units)
        chapters = seed_chapters(units)
        topics = seed_topics(chapters)
        questions = seed_questions(chapters, topics)
        seed_answers(questions)
        seed_progress()
        users[0].current_chapter = chapters[0]
        db.session.commit()
        

        print("Database seeded succsesfully")


if __name__=="__main__":
    try:
        main()
    except IntegrityError:
        db.session.rollback()
        print("There was an error seeding the database")