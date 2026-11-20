from exts import db
from main import create_app
from config import ProdConfig
from models import Chapter, QuestionTopic, Unit, Question, Answer
from sqlalchemy.exc import IntegrityError

app = create_app(ProdConfig)

# Units 5 and 6 already exist (as "Consumer Theory" / "Producer Theory") with no
# chapters or users attached, so they are renamed rather than recreated.
UNIT_RENAMES = {
    5: "Unit 5: Market Failure",
    6: "Unit 6: Production, Costs, Perfect & Imperfect Competition",
}

# Each question: (text, [answers], index of correct answer)
CHAPTERS = [
    {
        "unit_id": 4,
        "name": "4.4a Price Floors - Minimum Wage",
        "slug": "price-floors-minimum-wage",
        "order": 28,
        "video_url": "https://www.youtube.com/embed/_MTCi6wkUo4",
        "video_blurb": "Ever wondered why your first job paid exactly the legal minimum and not a penny more? Welcome to the world of price floors, where the government says \"no lower than this\" and the labor market says \"well, okay, but fewer of you are getting hired.\" Minimum wage is the most famous price floor out there, and it sparks more family-dinner arguments than pineapple on pizza.\n\nIn this video, we introduce price floors, break down how labor markets work (spoiler: firms are the buyers and you are the product), and walk through what happens when a minimum wage is set above equilibrium. We'll cover unemployment, who wins and who loses, what happens to social surplus and allocative efficiency, and why some jobs quietly slip off the books and into the underground economy. Grab your name tag and clock in.",
        "quiz_blurb": "Think you've mastered the minimum wage? Time to find out whether you're management material or still stuck folding T-shirts in the back.\n\nThis quiz covers binding price floors, labor surpluses (a.k.a. unemployment), deadweight loss, and who actually benefits when the wage floor goes up. No overtime pay, but bragging rights are included.",
        "topic": "Price Floors - Minimum Wage",
        "questions": [
            ("A price floor will only have an effect on a market (be binding) if it is set", [
                "above the equilibrium price",
                "below the equilibrium price",
                "exactly at the equilibrium price",
                "at the price where marginal cost is lowest",
                "by firms rather than the government",
            ], 0),
            ("In a labor market, which of the following correctly identifies the buyers and sellers?", [
                "Households demand labor and firms supply labor",
                "The government demands labor and households supply labor",
                "Firms demand labor and workers supply labor",
                "Workers demand labor and firms supply labor",
                "Labor unions both demand and supply labor",
            ], 2),
            ("If the government sets a minimum wage above the equilibrium wage, which of the following will result?", [
                "A shortage of labor",
                "A surplus of labor, also known as unemployment",
                "An increase in the quantity of labor demanded",
                "A rightward shift of the demand for labor",
                "No change in the number of workers employed",
            ], 1),
            ("The equilibrium wage in a local labor market is $12 per hour and 500 workers are employed. If the government imposes a minimum wage of $15 per hour, which of the following is true?", [
                "More than 500 workers will be employed",
                "There will be a shortage of workers",
                "The supply of labor will shift to the right",
                "Fewer than 500 workers will be employed",
                "The demand for labor will shift to the right",
            ], 3),
            ("The equilibrium wage in a labor market is $10 per hour. If the government sets a minimum wage of $7 per hour, which of the following will occur?", [
                "Unemployment will increase",
                "There will be a shortage of labor",
                "The minimum wage will have no effect on the wage or the number of workers employed",
                "Firms will hire fewer workers",
                "Workers will supply more labor",
            ], 2),
            ("At a minimum wage of $15 per hour, firms want to hire 400 workers and 650 workers are willing and able to work. How many workers are unemployed as a result of the minimum wage?", [
                "150",
                "250",
                "400",
                "650",
                "1,050",
            ], 1),
            ("Which group is most likely to benefit from a binding minimum wage?", [
                "Workers who keep their jobs and now earn a higher wage",
                "Workers who lose their jobs because of the higher wage",
                "Firms that hire low-wage workers",
                "Consumers of goods produced with low-wage labor",
                "Workers who would have been hired at the equilibrium wage but are not hired at the minimum wage",
            ], 0),
            ("Which of the following best describes the effect of a binding minimum wage on social surplus?", [
                "Social surplus increases because workers earn more",
                "Social surplus is unchanged because the gains to workers equal the losses to firms",
                "Deadweight loss is created because more workers are hired than is allocatively efficient",
                "Producer surplus is completely eliminated",
                "Deadweight loss is created because fewer workers are hired than is allocatively efficient",
            ], 4),
            ("Why might a binding minimum wage lead to an underground or black market for labor?", [
                "Firms face a shortage of workers and must pay above the minimum wage",
                "Some unemployed workers are willing to work for less than the minimum wage, and some firms are willing to hire them off the books",
                "The government hires the surplus workers",
                "The demand for labor increases above the minimum wage",
                "Workers are no longer willing to work at the minimum wage",
            ], 1),
        ],
    },
    {
        "unit_id": 4,
        "name": "4.4b Agricultural Price Floors",
        "slug": "agricultural-price-floors",
        "order": 29,
        "video_url": "https://www.youtube.com/embed/ndjjp1B8PhA",
        "video_blurb": "What happens when the government decides the price of wheat is just too darn low? It sets a price floor, farmers grow a mountain of extra wheat, and then... somebody has to buy it. Spoiler: that somebody is the government, which means that somebody is you, the taxpayer. Somewhere out there is a warehouse full of cheese with your name on it.\n\nIn this video, we look at how agricultural price floors work, why they create a surplus that the government has to buy up, and who wins and loses in the process. We'll run through a full stakeholder analysis of farmers, consumers, taxpayers, and even farmers in other countries, so you'll know exactly who to thank (or blame) the next time you see a government cheese cave.",
        "quiz_blurb": "Ready to put your agricultural knowledge to the test? This quiz will separate the economic wheat from the chaff.\n\nExpect questions on surpluses, government purchases, stakeholder analysis, and why paying farmers to grow more food than anyone wants to buy might not be the most efficient use of resources. No overalls required.",
        "topic": "Agricultural Price Floors",
        "questions": [
            ("The government sets a price floor for wheat above the equilibrium price. In order to maintain the price floor, the government must", [
                "sell wheat from its own reserves",
                "buy the surplus of wheat",
                "place a tax on wheat consumers",
                "decrease the demand for wheat",
                "ban imports of wheat",
            ], 1),
            ("The equilibrium price of wheat is $5 per bushel and 100 million bushels are sold. The government sets a price floor of $6 per bushel. At $6, consumers demand 80 million bushels and farmers supply 120 million bushels. How many bushels must the government buy to maintain the price floor?", [
                "20 million",
                "40 million",
                "80 million",
                "100 million",
                "120 million",
            ], 1),
            ("The government sets a price floor for wheat of $6 per bushel. At $6, consumers demand 80 million bushels and farmers supply 120 million bushels. How much will the government spend buying the surplus?", [
                "$40 million",
                "$200 million",
                "$240 million",
                "$480 million",
                "$720 million",
            ], 2),
            ("Which group is most clearly made worse off by an agricultural price floor?", [
                "Consumers, who pay a higher price and buy a smaller quantity",
                "Farmers, who receive a higher price",
                "Farmers, who sell a larger quantity",
                "The government agency that stores the surplus",
                "Firms that sell fertilizer to farmers",
            ], 0),
            ("When the government maintains an agricultural price floor by buying the surplus, what happens to farmers' total revenue?", [
                "It decreases, because consumers buy less",
                "It stays the same, because the price increase and quantity decrease cancel out",
                "It increases, because farmers receive a higher price and sell a larger quantity",
                "It decreases, because the government pays less than the market price",
                "It cannot change, because farmers do not receive government payments",
            ], 2),
            ("Who ultimately bears the cost of the government purchasing the surplus created by an agricultural price floor?", [
                "Farmers",
                "Foreign consumers",
                "Taxpayers",
                "Fertilizer producers",
                "Nobody, because the surplus is free to store",
            ], 2),
            ("Compared to the free market equilibrium, an agricultural price floor maintained by government purchases will lead to", [
                "an underallocation of resources to the good",
                "allocative efficiency in the market",
                "a shortage of the good",
                "an overallocation of resources to the good",
                "a decrease in the quantity supplied",
            ], 3),
            ("If the government sells its surplus of a crop on world markets at low prices, which group is most likely to be harmed?", [
                "Domestic consumers of the crop",
                "Farmers in other countries who grow the same crop",
                "Domestic farmers who grow the crop",
                "Consumers in other countries who buy the crop",
                "Domestic taxpayers",
            ], 1),
        ],
    },
    {
        "unit_id": 5,
        "name": "5.1 Introduction to Market Failure",
        "slug": "introduction-to-market-failure",
        "order": 30,
        "video_url": "https://www.youtube.com/embed/Rnhh47UME30",
        "video_blurb": "We've spent a lot of time bragging about how great free markets are at allocating resources. Well, it's time for a little humility. Sometimes the invisible hand trips over its own shoelaces, and economists call that market failure.\n\nIn this video, we define market failure and introduce the five big ways the free market drops the ball: positive externalities, negative externalities, common access resources, public goods, and monopoly. Think of it as the trailer for the rest of the unit, complete with neighbors who won't stop playing loud music, oceans with no fish left, and a fireworks show nobody wants to pay for.",
        "quiz_blurb": "Time to see if you can spot a market failure when you see one. (Hint: it's not your last quiz grade.)\n\nThis quiz covers the definition of market failure, externalities, public goods and the free rider problem, common access resources, and monopoly. Get through it and you'll be ready for the rest of the unit.",
        "topic": "Market Failure Introduced",
        "questions": [
            ("Market failure occurs when", [
                "a firm goes out of business",
                "the free market fails to allocate resources efficiently",
                "the government sets a price below equilibrium",
                "consumers cannot afford a good",
                "prices rise due to inflation",
            ], 1),
            ("Which of the following is NOT a source of market failure?", [
                "Negative externalities",
                "Public goods",
                "Common access resources",
                "Monopoly",
                "Perfect competition",
            ], 4),
            ("Which of the following is the best example of a positive externality?", [
                "A student gets a flu vaccine, reducing the chance that classmates get sick",
                "A factory pollutes a river used by a nearby town",
                "A consumer buys a new phone and enjoys using it",
                "A firm raises its price after a competitor exits the market",
                "A neighbor plays loud music late at night",
            ], 0),
            ("Which of the following is the best example of a negative externality?", [
                "A homeowner plants a beautiful garden that neighbors enjoy",
                "A firm trains workers who later work for other firms",
                "A factory emits smoke that harms the health of nearby residents",
                "A consumer pays a high price for concert tickets",
                "A city builds a public park",
            ], 2),
            ("Public goods have which two characteristics?", [
                "Rivalrous and excludable",
                "Rivalrous and non-excludable",
                "Non-rivalrous and excludable",
                "Non-rivalrous and non-excludable",
                "Scarce and expensive",
            ], 3),
            ("The free rider problem is most closely associated with which type of market failure?", [
                "Monopoly",
                "Public goods",
                "Negative externalities of production",
                "Price floors",
                "Demerit goods",
            ], 1),
            ("Ocean fish stocks are often overfished because they are", [
                "rivalrous and non-excludable common access resources",
                "non-rivalrous public goods",
                "produced by a monopoly",
                "subject to a binding price ceiling",
                "goods with a positive externality of consumption",
            ], 0),
            ("Why is monopoly considered a source of market failure?", [
                "A monopoly produces more output than is allocatively efficient",
                "A monopoly creates a positive externality",
                "A monopoly produces less output and charges a higher price than is allocatively efficient",
                "A monopoly always earns zero economic profit",
                "A monopoly cannot exclude non-paying consumers",
            ], 2),
            ("Resources are allocated efficiently from society's point of view where", [
                "marginal private benefit equals marginal private cost",
                "marginal social benefit equals marginal social cost",
                "total revenue is maximized",
                "price equals average cost",
                "consumer surplus is maximized",
            ], 1),
        ],
    },
    {
        "unit_id": 5,
        "name": "5.2 Negative Externalities of Consumption",
        "slug": "negative-externalities-of-consumption",
        "order": 31,
        "video_url": "https://www.youtube.com/embed/W06iI6rFqLk",
        "video_blurb": "You know that person on the airplane who decides it's the perfect time to eat a tuna sandwich? Congratulations, you've experienced a negative externality of consumption. When people consume certain goods, the costs don't stop with them. They spill over onto everyone else nearby.\n\nIn this video, we dig into demerit goods and how their consumption creates negative externalities. We'll use diagrams to show how the marginal private benefit and marginal social benefit curves split apart, why that leads to overconsumption and market failure, how it shows up as a welfare loss, and what governments can do about it, from taxes to bans to awareness campaigns. Please keep your tuna sandwiches stowed until the video is over.",
        "quiz_blurb": "Ready to test your knowledge of demerit goods and the people who overconsume them? This quiz is externality-free, so the only one who suffers if you don't study is you.\n\nExpect questions on MPB vs. MSB, overconsumption, welfare loss, and the policies governments use to bring consumption back to the socially optimal level.",
        "topic": "Negative Externalities of Consumption",
        "questions": [
            ("A negative externality of consumption exists when", [
                "marginal social benefit is greater than marginal private benefit",
                "marginal social benefit is less than marginal private benefit",
                "marginal social cost is less than marginal private cost",
                "marginal private benefit equals marginal social benefit",
                "the good is non-rivalrous and non-excludable",
            ], 1),
            ("Which of the following is the best example of a negative externality of consumption?", [
                "Secondhand smoke from a person smoking cigarettes",
                "Pollution from a factory producing steel",
                "A person getting a college education",
                "A homeowner painting their house",
                "A farmer using fertilizer that runs into a river",
            ], 0),
            ("In a free market for a good with a negative externality of consumption, which of the following is true?", [
                "The good is underconsumed relative to the socially optimal quantity",
                "The market produces the allocatively efficient quantity",
                "The good is overconsumed relative to the socially optimal quantity",
                "The price of the good is too high",
                "There is a shortage of the good",
            ], 2),
            ("Goods that are harmful to the people who consume them and to others, and that tend to be overconsumed in a free market, are called", [
                "merit goods",
                "public goods",
                "inferior goods",
                "demerit goods",
                "normal goods",
            ], 3),
            ("In a market with a negative externality of consumption, the welfare loss (deadweight loss) is the area", [
                "between the MPB and MSB curves, from the socially optimal quantity to the free market quantity",
                "below the supply curve and above the price",
                "between the demand curve and the price, from zero to the market quantity",
                "between the MPB and MSB curves, from zero to the socially optimal quantity",
                "above the MSB curve and below the price",
            ], 0),
            ("Which government policy would move a market with a negative externality of consumption toward the socially optimal quantity?", [
                "A subsidy to consumers of the good",
                "A price ceiling below equilibrium",
                "A subsidy to producers of the good",
                "Removing existing taxes on the good",
                "An indirect (excise) tax on the good",
            ], 4),
            ("A government education campaign about the dangers of vaping is intended to", [
                "shift the supply curve to the right",
                "shift the MPB (demand) curve to the left, closer to MSB",
                "shift the MSB curve to the right",
                "increase the price of vaping products",
                "increase the quantity of vaping products consumed",
            ], 1),
            ("In a market for a demerit good, the free market quantity is 10 million units and the socially optimal quantity is 7 million units. Which of the following is true?", [
                "Resources are underallocated by 3 million units",
                "The market is allocatively efficient",
                "Resources are overallocated by 3 million units",
                "Resources are overallocated by 7 million units",
                "Resources are underallocated by 10 million units",
            ], 2),
            ("Which of the following is a potential drawback of banning a demerit good outright?", [
                "It will cause the good to be overconsumed",
                "It increases government tax revenue",
                "It shifts the MSB curve to the right",
                "It may lead to the growth of black markets for the good",
                "It has no effect on consumption",
            ], 3),
        ],
    },
    {
        "unit_id": 6,
        "name": "6.1 The Short Run Production Function",
        "slug": "the-short-run-production-function",
        "order": 32,
        "video_url": "https://www.youtube.com/embed/N-m_MUmg--I",
        "video_blurb": "Picture a tiny kitchen with one oven. One cook? Great. Two cooks? Even better. Ten cooks? Now everyone is bumping elbows, fighting over the oven, and somebody just put a spatula in the dishwasher. Welcome to the law of diminishing marginal returns.\n\nIn this video, we kick off the study of production by separating the short run from the long run, and then introduce total product, average product, and marginal product. We'll build a short run production function step by step, see exactly where diminishing returns kick in, and explore how marginal product relates to both total product and average product. Aprons on.",
        "quiz_blurb": "Time to see how productive your studying has been. Hopefully you haven't hit diminishing returns yet.\n\nThis quiz covers the short run vs. the long run, calculating total, average, and marginal product, the law of diminishing marginal returns, and the relationships between the product curves. Calculators welcome. Spatulas, not so much.",
        "topic": "The Short Run Production Function",
        "questions": [
            ("In economics, the short run is a period of time in which", [
                "all factors of production are variable",
                "at least one factor of production is fixed",
                "firms can enter and exit the industry freely",
                "output cannot be changed",
                "less than one year has passed",
            ], 1),
            ("Marginal product of labor is calculated as", [
                "total product divided by the number of workers",
                "the change in total product divided by the change in the number of workers",
                "total product multiplied by the wage",
                "the change in total cost divided by the change in output",
                "total product minus average product",
            ], 1),
            ("A bakery produces 30 cakes per day with 3 workers and 38 cakes per day with 4 workers. What is the marginal product of the 4th worker?", [
                "4",
                "8",
                "9.5",
                "10",
                "38",
            ], 1),
            ("A bakery produces 38 cakes per day with 4 workers. What is the average product of labor?", [
                "8",
                "9",
                "9.5",
                "10",
                "38",
            ], 2),
            ("The law of diminishing marginal returns states that", [
                "as more units of a variable factor are added to a fixed factor, the marginal product of the variable factor will eventually fall",
                "as a firm increases all of its inputs, output increases by a smaller proportion",
                "total product always falls as more workers are hired",
                "average product is always greater than marginal product",
                "marginal product is constant in the short run",
            ], 0),
            ("When marginal product is positive but falling, total product is", [
                "decreasing",
                "constant",
                "increasing at an increasing rate",
                "increasing at a decreasing rate",
                "equal to zero",
            ], 3),
            ("Total product is at its maximum when marginal product is", [
                "at its maximum",
                "equal to average product",
                "equal to zero",
                "negative",
                "rising",
            ], 2),
            ("If the marginal product of the next worker is greater than the current average product, then hiring that worker will cause average product to", [
                "fall",
                "rise",
                "stay the same",
                "become negative",
                "equal zero",
            ], 1),
            ("The marginal product curve intersects the average product curve", [
                "at the maximum point of the average product curve",
                "at the minimum point of the average product curve",
                "where total product is at its maximum",
                "where marginal product equals zero",
                "the curves never intersect",
            ], 0),
        ],
    },
]


def seed():
    existing = [c["slug"] for c in CHAPTERS if Chapter.query.filter_by(slug=c["slug"]).first()]
    if existing:
        print(f"These chapters already exist, seeding aborted: {existing}")
        return

    for unit_id, name in UNIT_RENAMES.items():
        unit = db.session.get(Unit, unit_id)
        if not unit:
            print(f"Unit with ID {unit_id} does not exist. Seeding aborted.")
            return
        unit.name = name

    for data in CHAPTERS:
        unit = db.session.get(Unit, data["unit_id"])
        if not unit:
            print(f"Unit with ID {data['unit_id']} does not exist. Seeding aborted.")
            db.session.rollback()
            return

        chapter = Chapter(
            name=data["name"],
            unit=unit,
            video_url=data["video_url"],
            order=data["order"],
            slug=data["slug"],
            video_blurb=data["video_blurb"],
            quiz_blurb=data["quiz_blurb"],
        )
        topic = QuestionTopic(name=data["topic"], chapter=chapter)
        db.session.add_all([chapter, topic])
        # Flush per chapter so chapter IDs are assigned in library order
        db.session.flush()

        for text, answers, correct in data["questions"]:
            question = Question(text=text, chapter=chapter, topic=topic)
            db.session.add(question)
            for i, answer_text in enumerate(answers):
                db.session.add(Answer(text=answer_text, question=question, is_correct=(i == correct)))

        print(f"Seeded {data['name']} ({len(data['questions'])} questions)")

    db.session.commit()
    print("All chapters seeded")


def main():
    with app.app_context():
        try:
            seed()
        except IntegrityError as e:
            db.session.rollback()
            print(f"There was an error seeding the chapters: {e}")


if __name__ == "__main__":
    main()
