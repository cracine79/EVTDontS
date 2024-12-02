from exts import db
from main import create_app
from models import User, Unit, Chapter, Question, QuestionTopic, Answer, UserPerformance, UserChapterProgress, UserTopicProgress, Subject
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from config import ProdConfig
from sqlalchemy import text

app = create_app(ProdConfig)

def seed_users():
    print("Seeding users")
    password = "password"
    hashed_password=generate_password_hash(password)

    user1 = User(username="charlee", email="charleelracine@gmail.com", password_hash=hashed_password)
    user2 = User(username="user", email="user2@example.com", password_hash=hashed_password)

    users = [user1, user2]
    db.session.add_all(users)
    db.session.commit()

    return users

def seed_subjects():
    print("Seeding Subjects")

    subject0 = Subject(name='Introduction to Economics')
    subject1 = Subject(name='Microeconomics')
    subject2 = Subject(name='Macroeconomics')

    subjects = [subject0, subject1, subject2]
    db.session.add_all(subjects)
    db.session.commit()

    return subjects


def seed_units(subjects):
    print("Seeding units")
    unit1 = Unit(name="Unit 1: Fundamental Economic Concepts", subject=subjects[0])
    unit2 = Unit(name="Unit 2: Supply and Demand", subject=subjects[1])
    unit3 = Unit(name="Unit 3: Elasticity", subject=subjects[1])
    unit4 = Unit(name="Unit 4: Government Intervention", subject=subjects[1])
    unit5 = Unit(name="Unit 5: Consumer Theory", subject=subjects[1])
    unit6 = Unit(name="Unit 6: Producer Theory", subject=subjects[1])
    unit7 = Unit(name="Unit 7: Macroeconomic Objectives", subject=subjects[2])
    unit8 = Unit(name="Unit 8: Macroeconomic Models", subject=subjects[2])
    unit9 = Unit(name='Unit 9: Macroeconomic Policies', subject=subjects[2])
    unit10 = Unit(name="Unit 10: Trade and the Balance of Payments", subject=subjects[2])
    
    units = [unit1, unit2, unit3, unit4, unit5, unit6, unit7, unit8, unit9, unit10]
    db.session.add_all(units)
    db.session.commit()
    
    return (units)

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
    print("seeding topics")
    topic1=QuestionTopic(name="Scarcity", chapter=chapters[0])
    topic2=QuestionTopic(name='Opportunity Cost', chapter=chapters[0])
    topic3=QuestionTopic(name="Factors of Production", chapter=chapters[1])
    topic4=QuestionTopic(name='Economic Systems', chapter=chapters[2])
    topic5=QuestionTopic(name='PPF Interpretation', chapter=chapters[3])
    topic6=QuestionTopic(name='PPF Shifts vs Movement', chapter=chapters[3])
    topic7=QuestionTopic(name='PPF Opportunity Cost', chapter=chapters[4])
    topic8=QuestionTopic(name='Theory of Absolute and Comparative Advantage', chapter = chapters[5])
    topic9=QuestionTopic(name='Comparative Advantage Calculations', chapter=chapters[6])
    topic10=QuestionTopic(name='The demand curve', chapter=chapters[7])
    topic11=QuestionTopic(name='Shifts to Demand', chapter=chapters[8])
    topic12=QuestionTopic(name='The supply curve', chapter=chapters[9])
    topic13 = QuestionTopic(name='Shifts to supply', chapter=chapters[10])
    topic14 = QuestionTopic(name='Supply and Demand in Equilibrium', chapter=chapters[11])
    topic15 = QuestionTopic(name='Shifts to Demand', chapter=chapters[12])
    topic16 = QuestionTopic(name='Shifts to Supply', chapter=chapters[12])
    topic34 = QuestionTopic(name='Simultaneous Shifts', chapter=chapters[13])
    topic17 = QuestionTopic(name='Marginal Utility', chapter=chapters[14])    
    topic18 = QuestionTopic(name='Marginal Benefit and Demand', chapter = chapters[14])
    topic19 = QuestionTopic(name='Marginal Cost and Supply', chapter=chapters[15])
    topic20 = QuestionTopic(name='Consumer Surplus', chapter=chapters[16])
    topic21 = QuestionTopic(name='Producer Surplus', chapter=chapters[16])
    topic22 = QuestionTopic(name='Social Surplus', chapter=chapters[16])
    topic23 = QuestionTopic(name='Allocative Efficiency', chapter = chapters[17])
    topic24 = QuestionTopic(name='Price Elasticity of Demand Concepts', chapter = chapters[18])
    topic25 = QuestionTopic(name='PED Calculation', chapter = chapters[18])
    topic26 = QuestionTopic(name='PED determinants', chapter = chapters[19])
    topic27 = QuestionTopic(name='PED and Total Revenue', chapter=chapters[20])
    topic28 = QuestionTopic(name='XED - calculation', chapter = chapters[21])
    topic29 = QuestionTopic(name='XED - interpretation', chapter = chapters[21])
    topic30 = QuestionTopic(name='YED - calculation', chapter = chapters[22])
    topic31 = QuestionTopic(name='YED - interpretation', chapter = chapters[22])
    topic32 = QuestionTopic(name= 'PES Calculation', chapter = chapters[23])
    topic33 = QuestionTopic(name='PES - determinants', chapter = chapters[23])
    


    topics = [topic1, topic2, topic3, topic4, topic5, topic6, topic7, topic8, topic9, topic10,
              topic11, topic12, topic13, topic14, topic15, topic16, topic17, topic18, topic19, topic20,
              topic21, topic22, topic23, topic24, topic25, topic26, topic27, topic28, topic29, topic30,
              topic31, topic32, topic33, topic34]
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
    question18 = Question(text="Which of the following is a key requirement for a market/capitalist economy, but not necessarily so for a command economy?", chapter=chapters[2], topic=topics[3])
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
    question29 = Question(text='The diagram above shows the production possibilities curve for country D.  Which of the following points represents an obtainable level of output, but inefficient use of resources?',chapter=chapters[3], topic=topics[4], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/PPF2.png')
    question30 = Question(text='An increase in the amount of available capital and land in an economy must result in', chapter=chapters[3], topic=topics[5])
    question31 = Question(text='The diagram above shows the production possibilities curve for country D. Which of the following is true about Country D?', chapter=chapters[3], topic=topics[4], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/PPF2.png')
    question32 = Question(text='An economy is operating at a point inside its production possibilities curve. Which of the following will most likely cause the economy to move toward the current PPC in the short run?', chapter=chapters[3], topic=topics[5])
    question33 = Question(text='An outward shift of a production possibilities curve could have been caused by which of the following?', chapter=chapters[3], topic=topics[5])
    question34 = Question(text='Given the production possibilities curve above, which of the following represents a movement from efficiency to inefficiency?', chapter=chapters[3], topic=topics[4], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/PPF3.png')
    question35 = Question(text='Improvements in technology for producing all goods must result in', chapter=chapters[3], topic=topics[5])
    question36 = Question(text='The diagram above shows the production possibilities curve for Capital City. Which of the following statements is true?', chapter=chapters[3], topic=topics[4], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/PPFCapCity.png')
    question37 = Question(text='Which of the following is always true about an economy operating at a point on its production possibilities frontier?', chapter=chapters[3], topic=topics[4])
    question38 = Question(text='Any point inside a production possibilities curve is', chapter=chapters[3], topic=topics[4])
    question39 = Question(text='Which of the following explains why the PPF is depicted as outward bowed (concave) from the origin.',chapter=chapters[4], topic=topics[6], image_url=None)
    question40 = Question(text='Based on the production possibilities curve for cherries and apples shown above, what is the opportunity cost of producing a cherry?',chapter=chapters[4], topic=topics[6], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/apple_cherry_ppf.png')
    question41 = Question(text='Two alternative production possibility frontiers for forks and knives are shown in the figures below. As more knives are produced, how will the opportunity cost of producing knives, as represented in figures A and B, be affected?',chapter=chapters[4], topic=topics[6], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/Constant_increasing_PPF.png')
    question42 = Question(text='The table above shows the maximum output combinations of good A and Good B that Econoworld can produce when using all of its resources efficiently. As the production of good A increases, what happens to the opportunity cost of producing good A?',chapter=chapters[4], topic=topics[6], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/PPF_Opp_cost_table.png')
    question43 = Question(text='Based on a comparison of points X, Y and Z, the opportunity cost of an additional capital good is',chapter=chapters[4], topic=topics[6], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/PPF3.png')
    question44 = Question(text='Which of the following is an explanation of why we generally represent the production possibilities curve as concave, or outward bowed?',chapter=chapters[4], topic=topics[6], image_url=None)
    question45 = Question(text='An outward bowed PPC implies that as more of a good is produced, its opportunity cost:',chapter=chapters[4], topic=topics[6], image_url=None)
    question46 = Question(text='The table above shows the opportunity cost of producing lemons and limes in Countries Alpha and Beta. Which of the following can be concluded based on data given in the table?', chapter=chapters[5], topic=topics[7], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/AlphaBetaLimesLemons.png')
    question47 = Question(text='The above diagram shows the production of two countries, Metalland and Grungeton, which produce guns and butter. The domestic opportunity cost of producing one ton of butter is which of the following?', chapter=chapters[5], topic=topics[7], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/MettallandGrungeTon.png')
    question48 = Question(text='The theory of comparative advantage implies that Metalland would find it advantageous to:', chapter=chapters[5], topic=topics[7], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/MettallandGrungeTon.png')
    question49 = Question(text='Assume both France and Spain produce only two goods: cheese and olives. If France holds a comparative advantage in the production of cheese, then which of the following statements is NOT true?', chapter=chapters[5], topic=topics[7], image_url=None)
    question50 = Question(text='Both Tayloronia and Davenia produce guitars and synthesizers. Which of the following is true if Tayloronia imports guitars from Davenia?', chapter=chapters[5], topic=topics[7], image_url=None)
    question51 = Question(text='If two nations specialize according to the law of comparative advantage and then trade with one another, which of the following is true?', chapter=chapters[5], topic=topics[7], image_url=None)
    question52 = Question(text='Nations X and Y produce only shirts and ties. If each laborer in Nation X can produce twice as many shirts as each laborer in Nation Y, then which of the following is necessarily true?', chapter=chapters[5], topic=topics[7], image_url=None)
    question53 = Question(text='If Nation A has an absolute advantage in producing both wheat and corn, but Nation B has a comparative advantage in corn, what should Nation B specialize in?', chapter=chapters[5], topic=topics[7], image_url=None)
    question54 = Question(text='Which of the following best explains why a country can have an absolute advantage in producing all goods but still benefit from trade?', chapter=chapters[5], topic=topics[7], image_url=None)
    question55 = Question(text='Assume Country X has a lower opportunity cost for producing textiles, and Country Y has a lower opportunity cost for producing cars. According to the theory of comparative advantage, which of the following should happen?', chapter=chapters[5], topic=topics[7], image_url=None)
    question56 = Question(text='When a country produces at a point inside its production possibilities frontier, what can be said about its resource usage?', chapter=chapters[5], topic=topics[7], image_url=None)
    question57 = Question(text='If Country A can produce more units of both coffee and tea than Country B using the same resources, what is true about their trade potential?', chapter=chapters[5], topic=topics[7], image_url=None)
    question58 = Question(text='Both Albert and Becky produce and consume hamburgers and French fries. In one hour, Albert makes five hamburgers or 10 baskets of French fries, while Becky makes fifteen hamburgers or fifteen baskets of French fries. Based on the above information, one can correctly conclude that:', chapter=chapters[6], topic=topics[8], image_url=None)
    question59 = Question(text='The diagram above shows the production possibilities for two countries, Country A and Country B. Assume that both countries use equal amounts of resources in production. If the two countries engage in trade, both would be better off under which of the following conditions?', chapter=chapters[6], topic=topics[8], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/ABMusicMovies.png')
    question60 = Question(text='Gilligan and Skipper can produce hot dogs or hamburgers. In one hour, Gilligan can make 20 hot dogs or 10 hamburgers. In one hour, Skipper can make 18 hot dogs or 6 hamburgers. Which of the following statements is true?', chapter=chapters[6], topic=topics[8], image_url=None)
    question61 = Question(text='Japan and China produce both computers and printers using labor as the only input. The table above shows the labor hours required to produce one computer and one printer in each country. Based on the information in the table, which of the following is true?', chapter=chapters[6], topic=topics[8], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/JapanChinaPrinterComputerTable.png')
    question62 = Question(text='The table above shows the maximum number of fish or coconuts that Mark and Donny can catch or gather in a day. Which of the following is true?', chapter=chapters[6], topic=topics[8], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/MarkDonnyFishCoconutsTable.png')
    question63 = Question(text='Both Katie and Lucas produce chocolate bars and cake slices. In one hour, Katie can make eight chocolate bars or twelve cake slices, while Lucas can make six chocolate bars or six cake slices. Based on the above information, one can correctly conclude that:', chapter=chapters[6], topic=topics[8], image_url=None)
    question64 = Question(text='Both Factory A and Factory B produce computers and smartphones. In one hour, Factory A can produce 20 computers or 30 smartphones, while Factory B can produce 15 computers or 15 smartphones. Based on the information provided, which of the following is true?', chapter=chapters[6], topic=topics[8], image_url=None)
    question65 = Question(text='Both Carol and Dave produce t-shirts and hoodies. In one hour, Carol makes 10 t-shirts or 5 hoodies, while Dave can make 6 t-shirts or 6 hoodies. Which of the following statements is correct?', chapter=chapters[6], topic=topics[8], image_url=None)
    question66 = Question(text='Both Alice and Tom produce pizzas and sandwiches. In one hour, Alice makes 12 pizzas or 18 sandwiches, while Tom makes 8 pizzas or 10 sandwiches. Based on the above information, one can correctly conclude that:', chapter=chapters[6], topic=topics[8], image_url=None)
    question67 = Question(text='The graph above shows the production possibilities curve for Factory X and Factory Y. If Factory X uses the same amount of resources to produce rollerblades and helmets as Factory Y uses, which of the following is true?', chapter=chapters[6], topic=topics[8], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/FacXYRollerbladesHelmetsPPF.png')
    question68 = Question(text='The diagram above shows the production possibilities for Factory C and Factory D. Assume both factories use the same amount of resources. Based on the graph, which of the following is correct?', chapter=chapters[6], topic=topics[8], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/FacCDGoodAB.png')
    question69 = Question(text='The graph above compares the production capabilities of Factory M and Factory N, which produce tablets and headphones. Using equal resources, which statement about comparative advantage is true?', chapter=chapters[6], topic=topics[8], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/FactoryMNTabletsHeadphones.png')
    question70 = Question(text='The diagram above shows the production possibilities curve for two countries, Country A and Country B, which produce coffee and tea. Assuming both countries use equal resources, which of the following is true?', chapter=chapters[6], topic=topics[8], image_url='https://evtds-seeds.s3.us-east-2.amazonaws.com/CountryABCoffeeTea.png')
    question71 = Question(text='Which of the following best describes Labor as a factor of production?',chapter=chapters[1], topic=topics[2])
    question72 = Question(text='An businesman starting a new business would be an example of which factor of production?',chapter=chapters[1], topic=topics[2])
    question73 = Question(text='Which of the following is NOT a factor of production?',chapter=chapters[1], topic=topics[2])
    question74 = Question(text='The office space rented by a company is an example of which factor of production?',chapter=chapters[1], topic=topics[2])
    question75 = Question(text='What distinguishes Entrepreneurship from the other factors of production?',chapter=chapters[1], topic=topics[2])
    question76 = Question(text='Which of the following is an example of Land as a factor of production?',chapter=chapters[1], topic=topics[2])
    question77 = Question(text='Which of the following factors of production earns wages?',chapter=chapters[1], topic=topics[2])
    question78 = Question(text='The term "human capital" refers to which factor of production?',chapter=chapters[1], topic=topics[2])
    question79 = Question(text='Which of the following is an example of Labor as a factor of production?',chapter=chapters[1], topic=topics[2])
    question80 = Question(text='Which factor of production involves risk-taking and innovation?',chapter=chapters[1], topic=topics[2])
    question81 = Question(text='Jeff works part time at a local gas station and earns $15 an hour.  He wants to spend next Thursday afternoon attending a comic book convention. The full price of a convention ticket is $80, but he was able to get a discounted price of $60 online. If Jeff took 4 hours off to go to the convention, what was his opportunity cost of attending the concert?', chapter=chapters[0], topic=topics[1])
    question82 = Question(text='A linear production possibliites curve suggests which of the following?', chapter=chapters[4], topic=topics[6])
    question83 = Question(text='An outward bowed production possibliites curve suggests which of the following?', chapter=chapters[4], topic=topics[6])
    question84 = Question(text="As compared to a command economy, resources in a market economy are more often allocated according to:", chapter=chapters[2], topic=topics[3])
    question85 = Question(text="Command economies are different from capitalist economies in which of the following ways?", chapter=chapters[2], topic=topics[3])
    question86 = Question(text="One of the key differences of a command economy as compared to a market economy is:", chapter=chapters[2], topic=topics[3])
    question87 = Question(text="Which of the following is a common feature of market economies that differentiates them from command economies?", chapter=chapters[2], topic=topics[3])
    question88 = Question(text="In a command economy, resource allocation decisions are typically made by:", chapter=chapters[2], topic=topics[3])
    question89 = Question(text="Which of the following characteristics is more associated with a capitalist economy than a command economy?", chapter=chapters[2], topic=topics[3])
    question90 = Question(text='The amount of good H that must be given up in order to produce one more unit of good G is called:', chapter=chapters[0], topic=topics[1])   
    question91 = Question(
    text='An opportunity cost is involved in which of the following decisions? <br><br>'
         'I. A student decides to attend college full time<br>'
         'II. An individual uses $3,000 of his savings to buy a 4k big screen TV<br>'
         'III. A factory decides to produce more iPhone cases and fewer iPad cases',
    chapter=chapters[0], topic=topics[1]
    )
    question92 = Question(
    text='It takes Mary 30 minutes to complete a math homework and 90 minutes to study for an Economics exam. '
         'Assuming Mary can only engage in these two activities, what is the opportunity cost to Mary of studying '
         'for one Economics exam?',
    chapter=chapters[0], topic=topics[1]
    )
    question93 = Question(
    text='Quinn just graduated from high school and has decided to take a Gap year and travel the world. '
         'Before making this decision, she was also considering:<br><br>'
         'I. Going to college<br>'
         'II. Getting a job<br>'
         'III. Volunteering locally<br><br>'
         'Which of the following is an opportunity cost to Quinn and her decision to travel the world?',
    chapter=chapters[0], topic=topics[1]
    )



    questions = [question1, question2, question3, 
                 question4, question5, question6, 
                 question7, question8, question9, 
                 question10, question11, question12,
                 question13, question14, question15,
                 question16, question17, question18,
                 question19, question20, question21,
                 question22, question23, question24,
                 question25, question26, question27,
                 question28, question29, question30,
                 question31, question32, question33,
                 question34, question35, question36,
                 question37, question38, question39,
                 question40, question41, question42,
                 question43, question44, question45,
                 question46, question47, question48, 
                 question49, question50, question51,
                 question52, question53, question54, 
                 question55,question56, question57,
                 question58, question59, question60,
                 question61, question62, question63, 
                 question64, question65, question66, 
                 question67,question68, question69, 
                 question70, question71, question72, 
                 question73, question74, question75,
                 question76, question77, question78,
                 question79, question80, question81, 
                 question82, question83, question84,
                 question85, question86, question87,
                 question88, question89, question90,
                 question91, question92, question93
                 ]
    
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
    answer6e=Answer(text='The sum of benefits from all foregone alternatives', question=questions[5], is_correct=False)
   
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
    answer10c=Answer(text='Real wages rose at the same rate as inflation', question=questions[9], is_correct=False)
    answer10d=Answer(text='Supply of all resources became unlimited', question=questions[9], is_correct=True)
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

    answer23a = Answer(text='Interest', question=questions[22], is_correct=False)
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

    answer29a = Answer(text='Point A', question=questions[28], is_correct=False)
    answer29b = Answer(text='Point B', question=questions[28], is_correct=True)
    answer29c = Answer(text='Point C', question=questions[28], is_correct=False)
    answer29d = Answer(text='Point D', question=questions[28], is_correct=False)
    answer29e = Answer(text='None of the above', question=questions[28], is_correct=False)

    answer30a = Answer(text='A steeper production possibilities frontier', question=questions[29], is_correct=False)
    answer30b = Answer(text='A flatter production possibilities frontier', question=questions[29], is_correct=False)
    answer30c = Answer(text='An outward shift of the production possibilities frontier', question=questions[29], is_correct=True)
    answer30d = Answer(text='An inward shift of the production possibilities frontier', question=questions[29], is_correct=False)
    answer30e = Answer(text='A decrease in the cost of labor', question=questions[29], is_correct=False)

    answer31a = Answer(text='If Country D is producing at point A, it is using all its resources efficiently', question=questions[30], is_correct=True)
    answer31b = Answer(text='The opportunity cost of producing franks is more than the opportunity cost of producing beans', question=questions[30], is_correct=False)
    answer31c = Answer(text='The opportunity cost of producing more beans is constant', question=questions[30], is_correct=False)
    answer31d = Answer(text='The economy is in recession if it is not producing at point D', question=questions[30], is_correct=False)
    answer31e = Answer(text='The economy is not capable of producing at point A', question=questions[30], is_correct=False)

    answer32a = Answer(text='An increase in taxes', question=questions[31], is_correct=False)
    answer32b = Answer(text='An increase in inflation', question=questions[31], is_correct=False)
    answer32c = Answer(text='An increase in physical capital', question=questions[31], is_correct=False)
    answer32d = Answer(text='An increase in employment', question=questions[31], is_correct=True)
    answer32e = Answer(text='A decrease in exports', question=questions[31], is_correct=False)

    answer33a = Answer(text='Manufacturers producing more profitable electronics', question=questions[32], is_correct=False)
    answer33b = Answer(text='Improvement in technology', question=questions[32], is_correct=True)
    answer33c = Answer(text='Employment of previously unemployed labor', question=questions[32], is_correct=False)
    answer33d = Answer(text='Consumers indicating a desire for more durable goods', question=questions[32], is_correct=False)
    answer33e = Answer(text='An increase in the minimum wage', question=questions[32], is_correct=False)

    answer34a = Answer(text='Point X to Point Y', question=questions[33], is_correct=False)
    answer34b = Answer(text='Point Y to Point X', question=questions[33], is_correct=False)
    answer34c = Answer(text='Point Y to Point W', question=questions[33], is_correct=True)
    answer34d = Answer(text='Point Y to Point V', question=questions[33], is_correct=False)
    answer34e = Answer(text='Point V to Point Z', question=questions[33], is_correct=False)

    answer35a = Answer(text='The production possibilities curve becoming steeper', question=questions[34], is_correct=False)
    answer35b = Answer(text='The production possibilities curve becoming flatter', question=questions[34], is_correct=False)
    answer35c = Answer(text='The production possibilities curve shifting outward', question=questions[34], is_correct=True)
    answer35d = Answer(text='The production possibilities curve shifting inward', question=questions[34], is_correct=False)
    answer35e = Answer(text='The creation of a third axis on the production possibilities curve', question=questions[34], is_correct=False)

    answer36a = Answer(text='If the Capital City is producing at point A, it is using all of its resources efficiently.', question=questions[35], is_correct=True)
    answer36b = Answer(text='The opportunity cost of producing more Metal records is constant.', question=questions[35], is_correct=False)
    answer36c = Answer(text='Producing at point C is not preferrable, because there are other options that allow for a greater variety of music.', question=questions[35], is_correct=False)
    answer36d = Answer(text='Capital City can produce at point D.', question=questions[35], is_correct=False)
    answer36e = Answer(text='It’s not possible to produce at point E.', question=questions[35], is_correct=False)

    answer37a = Answer(text='Income is distributed equitably.', question=questions[36], is_correct=False)
    answer37b = Answer(text='It must be a market economy.', question=questions[36], is_correct=False)
    answer37c = Answer(text='It was not operating at the same point in the previous calendar year.', question=questions[36], is_correct=False)
    answer37d = Answer(text='It will not engage with trade with other nations, as it is already fully efficient.', question=questions[36], is_correct=False)
    answer37e = Answer(text='Its resources are fully employed.', question=questions[36], is_correct=True)

    answer38a = Answer(text='A point that does not involve opportunity cost', question=questions[37], is_correct=False)
    answer38b = Answer(text='Associated with an inefficient use or unemployment of resources', question=questions[37], is_correct=True)
    answer38c = Answer(text='Infeasible', question=questions[37], is_correct=False)
    answer38d = Answer(text='Efficient', question=questions[37], is_correct=False)
    answer38e = Answer(text='Associated with changes to technology', question=questions[37], is_correct=False)

    answer39a = Answer(text='The marginal benefit of consuming one more of each good decreases with consumption', question=questions[38], is_correct=False)
    answer39b = Answer(text='Production of goods and services is limited by the availability of factors of production', question=questions[38], is_correct=False)
    answer39c = Answer(text='There are only two goods being represented on the diagram', question=questions[38], is_correct=False)
    answer39d = Answer(text='The opportunity cost of producing one good increases as more of the good is produced', question=questions[38], is_correct=True)
    answer39e = Answer(text='The law of demand', question=questions[38], is_correct=False)

    answer40a = Answer(text='30 apples', question=questions[39], is_correct=False)
    answer40b = Answer(text='90 apples', question=questions[39], is_correct=False)
    answer40c = Answer(text='3 apples', question=questions[39], is_correct=False)
    answer40d = Answer(text='1/3 of an apple', question=questions[39], is_correct=True)
    answer40e = Answer(text='1/9 of an apple', question=questions[39], is_correct=False)

    answer41a = Answer(text='A: No change, B: Increase', question=questions[40], is_correct=False)
    answer41b = Answer(text='A: No change, B: Decrease', question=questions[40], is_correct=False)
    answer41c = Answer(text='A: Increase, B: No Change', question=questions[40], is_correct=True)
    answer41d = Answer(text='A: Decrease, B: No Change', question=questions[40], is_correct=False)
    answer41e = Answer(text='A: Decrease, B: Decrease', question=questions[40], is_correct=False)

    answer42a = Answer(text='It decreases, because the production of good B decreases by greater amounts', question=questions[41], is_correct=False)
    answer42b = Answer(text='It decreases, because the production of good Y increases by smaller amounts', question=questions[41], is_correct=False)
    answer42c = Answer(text='It remains constant, because the production of good A increases by the same amount', question=questions[41], is_correct=False)
    answer42d = Answer(text='It increases, because the production of good B decreases by greater amounts', question=questions[41], is_correct=True)
    answer42e = Answer(text='It increases, because the production of good B decreases by smaller amount', question=questions[41], is_correct=False)

    answer43a = Answer(text='Highest at point X', question=questions[42], is_correct=True)
    answer43b = Answer(text='Highest at point Y', question=questions[42], is_correct=False)
    answer43c = Answer(text='Highest at point Z', question=questions[42], is_correct=False)
    answer43d = Answer(text='The same at points X, Y, and Z', question=questions[42], is_correct=False)
    answer43e = Answer(text='It is not possible to determine opportunity cost of an additional capital good from the diagram', question=questions[42], is_correct=False)

    answer44a = Answer(text='Capital is generally more expensive than labor', question=questions[43], is_correct=False)
    answer44b = Answer(text='One economy produces more than two goods, so we draw an outward bowed PPF to account for the fact that there are more than two products in real economies.', question=questions[43], is_correct=False)
    answer44c = Answer(text='The opportunity cost of producing of a good increases as more of it is produced.', question=questions[43], is_correct=True)
    answer44d = Answer(text='The opportunity cost of producing a good decreases as more of it is produced.', question=questions[43], is_correct=False)
    answer44e = Answer(text='The law of supply.', question=questions[43], is_correct=False)

    answer45a = Answer(text='Is constant', question=questions[44], is_correct=False)
    answer45b = Answer(text='Increases', question=questions[44], is_correct=True)
    answer45c = Answer(text='Decreases', question=questions[44], is_correct=False)
    answer45d = Answer(text='Increases, then remains constant', question=questions[44], is_correct=False)
    answer45e = Answer(text='Decreases at an increasing rate.', question=questions[44], is_correct=False)

    answer46a = Answer(text='Country Beta has an absolute advantage in producing both goods.', question=questions[45], is_correct=False)
    answer46b = Answer(text='Country Beta has a comparative advantage in producing both goods.', question=questions[45], is_correct=False)
    answer46c = Answer(text='Country Alpha has an absolute advantage in producing both goods.', question=questions[45], is_correct=False)
    answer46d = Answer(text='Country Alpha has a comparative advantage in producing limes.', question=questions[45], is_correct=True)
    answer46e = Answer(text='Country Alpha has a comparative advantage in producing lemons.', question=questions[45], is_correct=False)

    answer47a = Answer(text='M: 1 ton of guns, G: 1 ton of guns.', question=questions[46], is_correct=False)
    answer47b = Answer(text='M: 1 ton of guns, G: 2 tons of guns.', question=questions[46], is_correct=False)
    answer47c = Answer(text='M: 2 tons of guns, G: 1 ton of guns.', question=questions[46], is_correct=False)
    answer47d = Answer(text='M: 1 ton of guns, G: 0.5 tons of guns.', question=questions[46], is_correct=True)
    answer47e = Answer(text='M: 0.33 tons of guns, G: 1.5 tons of guns.', question=questions[46], is_correct=False)

    answer48a = Answer(text='Export guns and import butter.', question=questions[47], is_correct=True)
    answer48b = Answer(text='Export butter and import guns.', question=questions[47], is_correct=False)
    answer48c = Answer(text='Export both guns and butter and import nothing.', question=questions[47], is_correct=False)
    answer48d = Answer(text='Import both grain and steel and export nothing.', question=questions[47], is_correct=False)
    answer48e = Answer(text='Trade 1 ton of grain for 0.5 tons of steel.', question=questions[47], is_correct=False)

    answer49a = Answer(text='France must hold an absolute advantage in the production of cheese.', question=questions[48], is_correct=True)
    answer49b = Answer(text='Spain holds a comparative advantage in the production of olives.', question=questions[48], is_correct=False)
    answer49c = Answer(text='France’s opportunity cost of producing one additional unit of cheese is less than Spain’s.', question=questions[48], is_correct=False)
    answer49d = Answer(text='Spain’s opportunity cost of producing one additional unit of olives is lower than France’s.', question=questions[48], is_correct=False)
    answer49e = Answer(text='If trade is open between them, these countries have an incentive to trade.', question=questions[48], is_correct=False)

    answer50a = Answer(text='The opportunity cost of producing synthesizers is higher in Taloronia than Davenia.', question=questions[49], is_correct=False)
    answer50b = Answer(text='Davenia has a comparative advantage in producing guitars.', question=questions[49], is_correct=True)
    answer50c = Answer(text='Tayloronia must be specializing in guitars.', question=questions[49], is_correct=False)
    answer50d = Answer(text='Workers in Tayloronia produce more guitars per hour than workers in Davenia.', question=questions[49], is_correct=False)
    answer50e = Answer(text='Consumers in Davenia buy more synthesizers than in Tayloronia.', question=questions[49], is_correct=False)

    answer51a = Answer(text='Consumers will have access to fewer goods in each nation.', question=questions[50], is_correct=False)
    answer51b = Answer(text='Total world GDP will decrease.', question=questions[50], is_correct=False)
    answer51c = Answer(text='Every stakeholder in each nation will be made better off.', question=questions[50], is_correct=False)
    answer51d = Answer(text='Each nation will be able to consume more overall.', question=questions[50], is_correct=True)
    answer51e = Answer(text='Each nation will be able to produce more overall.', question=questions[50], is_correct=False)

    answer52a = Answer(text='Nation X has a comparative advantage in shirts.', question=questions[51], is_correct=False)
    answer52b = Answer(text='Nation X has a comparative advantage in ties.', question=questions[51], is_correct=False)
    answer52c = Answer(text='Nation X has an absolute advantage in shirts.', question=questions[51], is_correct=True)
    answer52d = Answer(text='Nation Y has an absolute advantage in ties.', question=questions[51], is_correct=False)
    answer52e = Answer(text='Nation X should specialize in producing shirts.', question=questions[51], is_correct=False)

    answer53a = Answer(text='Nation A should specialize in wheat.', question=questions[52], is_correct=True)
    answer53b = Answer(text='Nation B should specialize in wheat.', question=questions[52], is_correct=False)
    answer53c = Answer(text='Nation A should stop trading with Nation B.', question=questions[52], is_correct=False)
    answer53d = Answer(text='Nation B should specialize in corn.', question=questions[52], is_correct=True)
    answer53e = Answer(text='Both nations should specialize in wheat.', question=questions[52], is_correct=False)

    answer54a = Answer(text='Trade allows countries to consume beyond their production possibilities.', question=questions[53], is_correct=True)
    answer54b = Answer(text='Countries with absolute advantages always produce more efficiently.', question=questions[53], is_correct=False)
    answer54c = Answer(text='Comparative advantage only applies to one good.', question=questions[53], is_correct=False)
    answer54d = Answer(text='Absolute advantage is always irrelevant to trade decisions.', question=questions[53], is_correct=False)
    answer54e = Answer(text='Countries with absolute advantages are less reliant on international markets.', question=questions[53], is_correct=False)

    answer55a = Answer(text='Country X should export textiles and import cars.', question=questions[54], is_correct=True)
    answer55b = Answer(text='Country Y should specialize in textiles.', question=questions[54], is_correct=False)
    answer55c = Answer(text='Country X should stop producing textiles.', question=questions[54], is_correct=False)
    answer55d = Answer(text='Both countries should produce both goods equally.', question=questions[54], is_correct=False)
    answer55e = Answer(text='Country Y should export textiles and import cars.', question=questions[54], is_correct=False)

    answer56a = Answer(text='The country is underutilizing its resources.', question=questions[55], is_correct=True)
    answer56b = Answer(text='The country is fully efficient in its production.', question=questions[55], is_correct=False)
    answer56c = Answer(text='The country is overusing its resources.', question=questions[55], is_correct=False)
    answer56d = Answer(text='The country cannot benefit from trade.', question=questions[55], is_correct=False)
    answer56e = Answer(text='The country is operating beyond its capacity.', question=questions[55], is_correct=False)

    answer57a = Answer(text='Country A has an absolute advantage in both goods, but could still benefit from trading with Country B.', question=questions[56], is_correct=True)
    answer57b = Answer(text='Country B should stop producing both goods.', question=questions[56], is_correct=False)
    answer57c = Answer(text='Country A should only export tea.', question=questions[56], is_correct=False)
    answer57d = Answer(text='Country A and Country B should not trade.', question=questions[56], is_correct=False)
    answer57e = Answer(text='Country B has an absolute advantage in tea.', question=questions[56], is_correct=False)

    answer58a = Answer(text='Albert has an absolute advantage in making French fries and will sell French fries to Becky.', question=questions[57], is_correct=False)
    answer58b = Answer(text='Albert has a comparative advantage in making French Fries and will sell French Fries to Becky.', question=questions[57], is_correct=True)
    answer58c = Answer(text='Albert does not have a comparative advantage in making either good and will not trade with Becky.', question=questions[57], is_correct=False)
    answer58d = Answer(text='Albert has an absolute advantage in making hamburgers but a comparative advantage in making French fries.', question=questions[57], is_correct=False)
    answer58e = Answer(text='Albert’s opportunity cost of making French fries is higher than Becky’s.', question=questions[57], is_correct=False)

    answer59a = Answer(text='Country A produced both music and movies because it has an absolute advantage in the production of both goods.', question=questions[58], is_correct=False)
    answer59b = Answer(text='Country B produced both music and movies because it has a comparative advantage in the production of both goods.', question=questions[58], is_correct=False)
    answer59c = Answer(text='Country A specialized in the production of movies because it has an absolute advantage in the production of movies.', question=questions[58], is_correct=False)
    answer59d = Answer(text='Country A specialized in the production of music because it has a comparative advantage in producing music.', question=questions[58], is_correct=True)
    answer59e = Answer(text='Country B specialized in the production of music because it has a comparative advantage in the production of music.', question=questions[58], is_correct=False)

    answer60a = Answer(text='Skipper has an absolute advantage in making hot dogs and a comparative advantage in making hamburgers.', question=questions[59], is_correct=False)
    answer60b = Answer(text='Skipper has both an absolute advantage and comparative advantage in making hamburgers.', question=questions[59], is_correct=False)
    answer60c = Answer(text='Gilligan has a comparative advantage in making both hot dogs and hamburgers.', question=questions[59], is_correct=False)
    answer60d = Answer(text='Gilligan has a comparative advantage in making hamburgers and Skipper has a comparative advantage in making hot dogs.', question=questions[59], is_correct=True)
    answer60e = Answer(text='Gilligan has a comparative advantage in making hot dogs and Skipper has a comparative advantage in making hamburgers.', question=questions[59], is_correct=False)

    answer61a = Answer(text='China has a comparative advantage in producing printers.', question=questions[60], is_correct=True)
    answer61b = Answer(text='China has an absolute advantage in producing printers.', question=questions[60], is_correct=False)
    answer61c = Answer(text='Japan has an absolute advantage in producing printers.', question=questions[60], is_correct=False)
    answer61d = Answer(text='China has a comparative advantage in producing computers.', question=questions[60], is_correct=False)
    answer61e = Answer(text='Japan has a comparative advantage in producing computers.', question=questions[60], is_correct=False)

    answer62a = Answer(text='Mark has a comparative advantage in picking coconuts.', question=questions[61], is_correct=False)
    answer62b = Answer(text='Donny has a comparative advantage in catching fish.', question=questions[61], is_correct=False)
    answer62c = Answer(text='Mark and Donny can both benefit from trade with each other if 1 coconut is traded for 1 fish.', question=questions[61], is_correct=False)
    answer62d = Answer(text='Mark and Donny can both benefit from trade with each other if 1 coconut is traded for 2 palm leaves.', question=questions[61], is_correct=False)
    answer62e = Answer(text='Mark and Donny can both benefit from trade with each other if 1 coconut is traded for 3 palm leaves.', question=questions[61], is_correct=True)

    answer63a = Answer(text='Katie has an absolute advantage in producing both chocolate bars and cake slices.', question=questions[62], is_correct=False)
    answer63b = Answer(text='Lucas has an absolute advantage in producing both chocolate bars and cake slices.', question=questions[62], is_correct=False)
    answer63c = Answer(text='Katie has a comparative advantage in producing cake slices, and Lucas has a comparative advantage in chocolate bars.', question=questions[62], is_correct=True)
    answer63d = Answer(text='Lucas has a comparative advantage in producing both products.', question=questions[62], is_correct=False)
    answer63e = Answer(text='Neither Katie nor Lucas has a comparative advantage in either product.', question=questions[62], is_correct=False)

    answer64a = Answer(text='Factory A has an absolute advantage in producing both computers and smartphones.', question=questions[63], is_correct=False)
    answer64b = Answer(text='Factory B has a comparative advantage in producing computers.', question=questions[63], is_correct=True)
    answer64c = Answer(text='Factory B has an absolute advantage in producing both computers and smartphones.', question=questions[63], is_correct=False)
    answer64d = Answer(text='Factory A has a comparative advantage in producing computers, and Factory B has an absolute advantage in producing computers.', question=questions[63], is_correct=False)
    answer64e = Answer(text='Factory A and Factory B should not trade because they produce at the same opportunity cost.', question=questions[63], is_correct=False)

    answer65a = Answer(text='Carol has a comparative advantage in producing t-shirts, while Dave has a comparative advantage in producing hoodies.', question=questions[64], is_correct=True)
    answer65b = Answer(text='Dave has an absolute advantage in producing both t-shirts and hoodies.', question=questions[64], is_correct=False)
    answer65c = Answer(text='Carol has an absolute advantage in producing both products.', question=questions[64], is_correct=False)
    answer65d = Answer(text='Neither Carol nor Dave has a comparative advantage in producing either good.', question=questions[64], is_correct=False)
    answer65e = Answer(text='Dave has a comparative advantage in producing t-shirts, while Carol has a comparative advantage in producing hoodies.', question=questions[64], is_correct=False)

    answer66a = Answer(text='Alice has an absolute advantage in producing both pizzas and sandwiches.', question=questions[65], is_correct=True)
    answer66b = Answer(text='Tom has a absolute advantage in producing pizzas, while Alice has an absolute advantage in producing sandwiches.', question=questions[65], is_correct=False)
    answer66c = Answer(text='Alice has a comparative advantage in producing both pizzas and sandwiches.', question=questions[65], is_correct=False)
    answer66d = Answer(text='Tom has an absolute advantage in producing sandwiches.', question=questions[65], is_correct=False)
    answer66e = Answer(text='Neither Alice nor Tom has a comparative advantage in producing either good.', question=questions[65], is_correct=False)

    answer67a = Answer(text='Factory Y has an absolute advantage in producing rollerblades.', question=questions[66], is_correct=False)
    answer67b = Answer(text='Factory Y has an absolute advantage in producing rollerblades.', question=questions[66], is_correct=False)
    answer67c = Answer(text='Factory X has a comparative advantage in producing rollerblades.', question=questions[66], is_correct=False)
    answer67d = Answer(text='Factory Y has a comparative advantage in producing rollerblades.', question=questions[66], is_correct=True)
    answer67e = Answer(text='Factory X has an absolute advantage in producing rollerblades.', question=questions[66], is_correct=False)

    answer68a = Answer(text='Factory C has an absolute advantage in producing both products.', question=questions[67], is_correct=False)
    answer68b = Answer(text='Factory D has a comparative advantage in producing one of the goods.', question=questions[67], is_correct=True)
    answer68c = Answer(text='Neither Factory C nor Factory D has a comparative advantage.', question=questions[67], is_correct=False)
    answer68d = Answer(text='Factory C should specialize in producing both goods.', question=questions[67], is_correct=False)
    answer68e = Answer(text='Factory D has an absolute advantage in producing both products.', question=questions[67], is_correct=False)

    answer69a = Answer(text='Factory M has a comparative advantage in producing tablets, while Factory N has a comparative advantage in producing headphones.', question=questions[68], is_correct=True)
    answer69b = Answer(text='Factory N has an absolute advantage in producing both products.', question=questions[68], is_correct=False)
    answer69c = Answer(text='Factory M should specialize in producing headphones.', question=questions[68], is_correct=False)
    answer69d = Answer(text='Neither factory has a comparative advantage.', question=questions[68], is_correct=False)
    answer69e = Answer(text='Factory N has a comparative advantage in producing both products.', question=questions[68], is_correct=False)

    answer70a = Answer(text='Country A has a comparative advantage in producing tea, and Country B has a comparative advantage in producing coffee.', question=questions[69], is_correct=True)
    answer70b = Answer(text='Country B has an absolute advantage in producing both coffee and tea.', question=questions[69], is_correct=False)
    answer70c = Answer(text='Neither Country A nor Country B has a comparative advantage in producing any good.', question=questions[69], is_correct=False)
    answer70d = Answer(text='Country A should specialize in producing coffee.', question=questions[69], is_correct=False)
    answer70e = Answer(text='Country B has a comparative advantage in producing tea.', question=questions[69], is_correct=False)

    answer71a = Answer(text='The physical effort workers provide', question=questions[70], is_correct=True)
    answer71b = Answer(text='The machinery used in production', question=questions[70], is_correct=False)
    answer71c = Answer(text='The land where production occurs', question=questions[70], is_correct=False)
    answer71d = Answer(text='The financial investment made by owners', question=questions[70], is_correct=False)
    answer71e = Answer(text='The entrepreneurial skill used to combine other factors', question=questions[70], is_correct=False)

    answer72a = Answer(text='Capital', question=questions[71], is_correct=False)
    answer72b = Answer(text='Labor', question=questions[71], is_correct=False)
    answer72c = Answer(text='Entrepreneurship', question=questions[71], is_correct=True)
    answer72d = Answer(text='Land', question=questions[71], is_correct=False)
    answer72e = Answer(text='Technology', question=questions[71], is_correct=False)

    answer73a = Answer(text='Labor', question=questions[72], is_correct=False)
    answer73b = Answer(text='Capital', question=questions[72], is_correct=False)
    answer73c = Answer(text='Money', question=questions[72], is_correct=True)
    answer73d = Answer(text='Land', question=questions[72], is_correct=False)
    answer73e = Answer(text='Entrepreneurship', question=questions[72], is_correct=False)

    answer74a = Answer(text='Capital', question=questions[73], is_correct=False)
    answer74b = Answer(text='Labor', question=questions[73], is_correct=False)
    answer74c = Answer(text='Entrepreneurship', question=questions[73], is_correct=False)
    answer74d = Answer(text='Land', question=questions[73], is_correct=True)
    answer74e = Answer(text='Human capital', question=questions[73], is_correct=False)

    answer75a = Answer(text='It involves the physical resources of production', question=questions[74], is_correct=False)
    answer75b = Answer(text='It represents the human effort in the production process', question=questions[74], is_correct=False)
    answer75c = Answer(text='It combines all other factors and takes risks to create new businesses', question=questions[74], is_correct=True)
    answer75d = Answer(text='It refers to the natural resources available for production', question=questions[74], is_correct=False)
    answer75e = Answer(text='It is the financial resources available for production', question=questions[74], is_correct=False)

    answer76a = Answer(text='A factory building', question=questions[75], is_correct=False)
    answer76b = Answer(text='Crude oil in the Gulf of Mexico', question=questions[75], is_correct=True)
    answer76c = Answer(text='The machines used to harvest crops', question=questions[75], is_correct=False)
    answer76d = Answer(text='The workers operating machinery', question=questions[75], is_correct=False)
    answer76e = Answer(text='The financial capital used to fund production', question=questions[75], is_correct=False)

    answer77a = Answer(text='Capital', question=questions[76], is_correct=False)
    answer77b = Answer(text='Entrepreneurship', question=questions[76], is_correct=False)
    answer77c = Answer(text='Labor', question=questions[76], is_correct=True)
    answer77d = Answer(text='Land', question=questions[76], is_correct=False)
    answer77e = Answer(text='Technology', question=questions[76], is_correct=False)

    answer78a = Answer(text='Labor', question=questions[77], is_correct=True)
    answer78b = Answer(text='Entrepreneurship', question=questions[77], is_correct=False)
    answer78c = Answer(text='Capital', question=questions[77], is_correct=False)
    answer78d = Answer(text='Land', question=questions[77], is_correct=False)
    answer78e = Answer(text='Financial capital', question=questions[77], is_correct=False)

    answer79a = Answer(text='The factory building used in production', question=questions[78], is_correct=False)
    answer79b = Answer(text='A software developer creating a new application', question=questions[78], is_correct=True)
    answer79c = Answer(text='The farmland owned by a farmer', question=questions[78], is_correct=False)
    answer79d = Answer(text='The investment used to start a business', question=questions[78], is_correct=False)
    answer79e = Answer(text='The entrepreneurial skills of a business owner', question=questions[78], is_correct=False)

    answer80a = Answer(text='Capital', question=questions[79], is_correct=False)
    answer80b = Answer(text='Entrepreneurship', question=questions[79], is_correct=True)
    answer80c = Answer(text='Labor', question=questions[79], is_correct=False)
    answer80d = Answer(text='Land', question=questions[79], is_correct=False)
    answer80e = Answer(text='Technology', question=questions[79], is_correct=False)

    answer81a = Answer(text='$60', question=questions[80], is_correct=False)
    answer81b = Answer(text='$75', question=questions[80], is_correct=False)
    answer81c = Answer(text='$80', question=questions[80], is_correct=False)
    answer81d = Answer(text='$120', question=questions[80], is_correct=True)
    answer81e = Answer(text='$140', question=questions[80], is_correct=False)

    answer82a = Answer(text='Constant opportunity cost', question=questions[81], is_correct=True)
    answer82b = Answer(text='Increasing opportunity cost', question=questions[81], is_correct=False)
    answer82c = Answer(text='Decreasing opportunity cost', question=questions[81], is_correct=False)
    answer82d = Answer(text='Increasing returns to scale', question=questions[81], is_correct=False)
    answer82e = Answer(text='Decreasing returns to scale', question=questions[81], is_correct=False)

    answer83a = Answer(text='Constant opportunity cost', question=questions[82], is_correct=False)
    answer83b = Answer(text='Increasing opportunity cost', question=questions[82], is_correct=True)
    answer83c = Answer(text='Decreasing opportunity cost', question=questions[82], is_correct=False)
    answer83d = Answer(text='Increasing returns to scale', question=questions[82], is_correct=False)
    answer83e = Answer(text='Decreasing returns to scale', question=questions[82], is_correct=False)

    answer84a = Answer(text="Elections", question=questions[83], is_correct=False)
    answer84b = Answer(text="Government mandates", question=questions[83], is_correct=False)
    answer84c = Answer(text="The pricing mechanism", question=questions[83], is_correct=True)
    answer84d = Answer(text="Traditions and norms", question=questions[83], is_correct=False)
    answer84e = Answer(text="Congress/Parliament", question=questions[83], is_correct=False)

    answer85a = Answer(text="Command economies tend to charge more for goods like energy or crude oil", question=questions[84], is_correct=False)
    answer85b = Answer(text="Capitalist economies tend to charge more for goods like energy or crude oil", question=questions[84], is_correct=False)
    answer85c = Answer(text="Command economies have a higher degree of government ownership and control of resources", question=questions[84], is_correct=True)
    answer85d = Answer(text="Capitalist economies have a higher degree of government ownership of resources", question=questions[84], is_correct=False)
    answer85e = Answer(text="Capitalist economies include more planning in the labor market", question=questions[84], is_correct=False)

    answer86a = Answer(text="Consumers and firms are more important in deciding pricing and output decisions.", question=questions[85], is_correct=False)
    answer86b = Answer(text="Taxes are always higher in command economies", question=questions[85], is_correct=False)
    answer86c = Answer(text="Resources are allocated according to central planning in command economies", question=questions[85], is_correct=True)
    answer86d = Answer(text="People have less religious freedom in command economies", question=questions[85], is_correct=False)
    answer86e = Answer(text="Individuals own resources in command economies", question=questions[85], is_correct=False)

    answer87a = Answer(text="High levels of government control in all industries", question=questions[86], is_correct=False)
    answer87b = Answer(text="Resource allocation through voluntary exchange", question=questions[86], is_correct=True)
    answer87c = Answer(text="Decisions are made by a central authority", question=questions[86], is_correct=False)
    answer87d = Answer(text="Limited availability of consumer goods", question=questions[86], is_correct=False)
    answer87e = Answer(text="Rigid wage and price controls", question=questions[86], is_correct=False)

    answer88a = Answer(text="Individual consumers", question=questions[87], is_correct=False)
    answer88b = Answer(text="Firms in competitive markets", question=questions[87], is_correct=False)
    answer88c = Answer(text="A central government authority", question=questions[87], is_correct=True)
    answer88d = Answer(text="International trade bodies", question=questions[87], is_correct=False)
    answer88e = Answer(text="Non-governmental organizations", question=questions[87], is_correct=False)

    answer89a = Answer(text="High degree of government ownership", question=questions[88], is_correct=False)
    answer89b = Answer(text="Resource allocation by supply and demand", question=questions[88], is_correct=True)
    answer89c = Answer(text="Strict central planning", question=questions[88], is_correct=False)
    answer89d = Answer(text="Government control of all prices", question=questions[88], is_correct=False)
    answer89e = Answer(text="Limited role for consumer choice", question=questions[88], is_correct=False)

    answer90a = Answer(text='Marginal benefit', question=questions[89], is_correct=False)
    answer90b = Answer(text='Marginal cost', question=questions[89], is_correct=False)
    answer90c = Answer(text='Opportunity cost', question=questions[89], is_correct=True)
    answer90d = Answer(text='Variable Cost', question=questions[89], is_correct=False)
    answer90e = Answer(text='Diminishing Marginal Returns', question=questions[89], is_correct=False)

    answer91a = Answer(text='I only', question=questions[90], is_correct=False)
    answer91b = Answer(text='I and II', question=questions[90], is_correct=False)
    answer91c = Answer(text='II and III', question=questions[90], is_correct=False)
    answer91d = Answer(text='I and III', question=questions[90], is_correct=False)
    answer91e = Answer(text='I, II and III', question=questions[90], is_correct=True)

    answer92a = Answer(text='Completing 1/3 of a math homework assignment', question=questions[91], is_correct=True)
    answer92b = Answer(text='Completing 3 math homework assignments', question=questions[91], is_correct=False)
    answer92c = Answer(text='Completing 1 math homework assignment', question=questions[91], is_correct=False)
    answer92d = Answer(text='It depends upon what grade she gets on the exam', question=questions[91], is_correct=False)
    answer92e = Answer(text='There is no opportunity cost as exams and homework cannot be compared', question=questions[91], is_correct=False)

    answer93a = Answer(text='Zero', question=questions[92], is_correct=False)
    answer93b = Answer(text='I only', question=questions[92], is_correct=False)
    answer93c = Answer(text='I or II but not III', question=questions[92], is_correct=False)
    answer93d = Answer(text='The sum of I, II, III and any other opportunity she passed up', question=questions[92], is_correct=False)
    answer93e = Answer(text='I, II, or III, whichever is the next most valuable/beneficial to Quinn', question=questions[92], is_correct=True)



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
               answer28a, answer28b, answer28c, answer28d, answer28e,
               answer29a, answer29b, answer29c, answer29d, answer29e,
               answer30a, answer30b, answer30c, answer30e, answer30d, 
               answer31a, answer31b, answer31c, answer31d, answer31e,
               answer32a, answer32b, answer32c, answer32d, answer32e,
               answer33a, answer33b, answer33c, answer33d, answer33e,
               answer34a, answer34b, answer34c, answer34d, answer34e, 
               answer35a, answer35b, answer35c, answer35d, answer35e, 
               answer36a, answer36b, answer36c, answer36d, answer36e,
               answer37a, answer37b, answer37c, answer37d, answer37e, 
               answer38a, answer38b, answer38c, answer38d, answer38e,
               answer39a, answer39b, answer39c, answer39d, answer39e,
               answer40a, answer40b, answer40c, answer40e, answer40d, 
               answer41a, answer41b, answer41c, answer41d, answer41e,
               answer42a, answer42b, answer42c, answer42d, answer42e,
               answer43a, answer43b, answer43c, answer43d, answer43e,
               answer44a, answer44b, answer44c, answer44d, answer44e, 
               answer45a, answer45b, answer45c, answer45d, answer45e,
               answer46a, answer46b, answer46c, answer46d, answer46e,
               answer47a, answer47b, answer47c, answer47d, answer47e, 
               answer48a, answer48b, answer48c, answer48d, answer48e,
               answer49a, answer49b, answer49c, answer49d, answer49e,
               answer50a, answer50b, answer50c, answer50e, answer50d, 
               answer51a, answer51b, answer51c, answer51d, answer51e,
               answer52a, answer52b, answer52c, answer52d, answer52e,
               answer53a, answer53b, answer53c, answer53d, answer53e,
               answer54a, answer54b, answer54c, answer54d, answer54e, 
               answer55a, answer55b, answer55c, answer55d, answer55e,
               answer56a, answer56b, answer56c, answer56d, answer56e,
               answer57a, answer57b, answer57c, answer57d, answer57e,
               answer58a, answer58b, answer58c, answer58d, answer58e,
               answer59a, answer59b, answer59c, answer59d, answer59e,
               answer60a, answer60b, answer60c, answer60e, answer60d, 
               answer61a, answer61b, answer61c, answer61d, answer61e,
               answer62a, answer62b, answer62c, answer62d, answer62e,
               answer63a, answer63b, answer63c, answer63d, answer63e,
               answer64a, answer64b, answer64c, answer64d, answer64e, 
               answer65a, answer65b, answer65c, answer65d, answer65e,
               answer66a, answer66b, answer66c, answer66d, answer66e,
               answer67a, answer67b, answer67c, answer67d, answer67e, 
               answer68a, answer68b, answer68c, answer68d, answer68e,
               answer69a, answer69b, answer69c, answer69d, answer69e,
               answer70a, answer70b, answer70c, answer70e, answer70d, 
               answer71a, answer71b, answer71c, answer71d, answer71e,
               answer72a, answer72b, answer72c, answer72d, answer72e,
               answer73a, answer73b, answer73c, answer73d, answer73e,
               answer74a, answer74b, answer74c, answer74d, answer74e, 
               answer75a, answer75b, answer75c, answer75d, answer75e,
               answer76a, answer76b, answer76c, answer76d, answer76e,
               answer77a, answer77b, answer77c, answer77d, answer77e, 
               answer78a, answer78b, answer78c, answer78d, answer78e,
               answer79a, answer79b, answer79c, answer79d, answer79e,
               answer80a, answer80b, answer80c, answer80d, answer80e, 
               answer81a, answer81b, answer81c, answer81d, answer81e, 
               answer82a, answer82b, answer82c, answer82d, answer82e,
               answer83a, answer83b, answer83c, answer83d, answer83e,
               answer84a, answer84b, answer84c, answer84d, answer84e, 
               answer85a, answer85b, answer85c, answer85d, answer85e,
               answer86a, answer86b, answer86c, answer86d, answer86e,
               answer87a, answer87b, answer87c, answer87d, answer87e, 
               answer88a, answer88b, answer88c, answer88d, answer88e,
               answer89a, answer89b, answer89c, answer89d, answer89e,
               answer90a, answer90b, answer90c, answer90d, answer90e, 
               answer91a, answer91b, answer91c, answer91d, answer91e, 
               answer92a, answer92b, answer92c, answer92d, answer92e,
               answer93a, answer93b, answer93c, answer93d, answer93e 
               ]

    db.session.add_all(answers)
    db.session.commit()


def seed_progress():
    print("seeding progress")
    progress1 = UserChapterProgress(user_id = 1, chapter_id = 1, video_completed=True, quiz_grade=100, active=True)
    progress2 = UserChapterProgress(user_id = 1, chapter_id = 2, video_completed=True, quiz_grade=66, active=True)
    progress3 = UserChapterProgress(user_id = 1, chapter_id = 3, video_completed=False, quiz_grade=None, active=True)
  
    
    progresses = [progress1, progress2, progress3]
    db.session.add_all(progresses)
    db.session.commit()

def seed_topic_progress():
    print('seeding topic progress')
    progress1 = UserTopicProgress(user_id = 1, topic_id = 1, questions_asked = 3, answered_correctly = 3)
    progress2 = UserTopicProgress(user_id = 1, topic_id = 2, questions_asked = 3, answered_correctly = 3)
    progress3 = UserTopicProgress(user_id = 1, topic_id = 3, questions_asked = 6, answered_correctly = 4)

    progresses = [progress1, progress2, progress3]
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
        db.session.query(UserTopicProgress).delete()
        db.session.commit()
        print("DB Deleted")


        users = seed_users()
        subjects = seed_subjects()
        units= seed_units(subjects)
        assign_units_to_users(users, units)
        chapters = seed_chapters(units)
        topics = seed_topics(chapters)
        questions = seed_questions(chapters, topics)
        seed_answers(questions)
        seed_progress()
        seed_topic_progress()
        users[0].current_chapter = chapters[2]
        db.session.commit()
        

        print("Database seeded succsesfully")


if __name__=="__main__":
    try:
        main()
    except IntegrityError:
        db.session.rollback()
        print("There was an error seeding the database")