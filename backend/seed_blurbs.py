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
    chapter2.quiz_blurb = "Alright, you made it through Factors of Production—the thrilling world of land, labor, capital, and entrepreneurship! Now it’s quiz time. Brace yourself for questions that will ask if you really paid attention or if you were daydreaming about anything other than economic resources. Let’s see if all that ‘knowledge’ from the video stuck around long enough to help you out. Good luck!"
    chapter2.quiz_blurb_img_url="https://evtds-seeds.s3.us-east-2.amazonaws.com/FOP+Cartoon_2.png"
    chapter3 = db.session.get(Chapter, 3)
    chapter3.video_blurb =  "Hey there, economic adventurer! You’ve made it to Chapter 3, and things are really heating up. Welcome to <em>Economic Systems</em>: where we categorize the world's economies like a reality TV show judge. Capitalism, socialism, mixed economies — it's like choosing your favorite flavor of ice cream, but with more debates and fewer sprinkles. \n\n In this chapter, we’ll break down the pros and cons of each system, explaining why some countries have thriving free markets while others prefer the government to take the wheel. And hey, you might even discover which system suits your inner economist. \n\n Stay tuned for the quiz afterwards to see if you’re more Adam Smith or Karl Marx. It’s the ultimate personality test, econ style! Don’t worry, there are no wrong answers (except the wrong ones), and as always, it’s all in good fun. So grab your popcorn, sit back, and let’s figure out where you land on the economics spectrum!"

    chapter4 = db.session.get(Chapter, 4)
    chapter4.video_blurb = "Welcome to the thrilling world of the Production Possibilities Frontier, or as we like to call it, the ‘How Much Coconuts vs. Fish Can One Person Collect Before Losing Their Mind’ scenario. Imagine you’re a castaway, just you and the open sea. You’ve got two main goals: gather coconuts and catch fish, both essential for survival and maybe, just maybe, for bargaining with a volleyball named Wilson if things get lonely enough. But here’s the catch: every time you spend an hour hauling coconuts, that’s an hour you’re not fishing. Enter the Production Possibilities Frontier, the ultimate balancing act between making sure you don’t starve and maybe avoiding scurvy with those occasional coconuts. \n\nThis video will guide you through the delicate and riveting trade-offs of island economics, where you’ll start to think, “If only I had more hours in the day… or maybe a third arm.” And let’s be real, this concept might seem a bit ‘why am I learning this’ at first, but imagine the skills you’ll have if you’re ever stranded on a deserted island with only your AP Econ notes to keep you company. You’ll be ready to maximize your production and make life a little less miserable. \n\n So, sit back, take in the island vibes, and let’s figure out just how many coconuts you can collect before your fish stocks start to dwindle. Spoiler alert: the struggle is real. This is the survival story you didn’t know you signed up for, but trust us—you’ll be glad you’re equipped with some survival econ 101 if your plane ever takes an unexpected detour."
    
    chapter5 = db.session.get(Chapter, 5)
    chapter5.video_blurb = "Welcome to <em>Production Possibilities Frontier: Part II</em>, where we dive deeper into the high-stakes drama of opportunity cost. Now, if you’ve sat through any sequels, you know there’s a mixed bag. <em>Back to the Future Part II</em>? Questionable.  <em>Speed 2: Cruise Control</em>? Hot Dumpster Fire - Jason Patric is a fine actor, but watching him fill Keanu's shoes was like watching someone try to run a marathon in flip flops.  But <em>The Godfather Part II</em>?  That's cinema. We’re aiming for a Godfather level here, breaking down why every choice you make on our deserted island means sacrificing something else. Yes, it's gritty, it's real, and you can leave your coconuts—and your dignity—at the door. \n\n Here's where things get interesting: in the real world (not on our fantasy island where we wish we were right now), producing more of something means producing less of something else.  In the sequel, the stakes are higher - it's not just about how much more you can produce-it's about what you're giving up in the process. Picture it: you're getting really good at fishing, but each hour casting a line means coconuts slipping through your fingers. And those coconuts? They represent every Saturday morning you’ve spent studying instead of sleeping in. That's the brutal reality of opportunity cost, and it hits harder than any disappointing sequel ever could. \n\n So, buckle up for Part II of the PPF, where you’ll learn that every fish, every coconut, every single decision carries a hidden cost. There’s no DeLorean to go back and fix your choices here—just cold, hard trade-offs and a lifetime supply of hypothetical coconuts."
    
    chapter6 = db.session.get(Chapter, 6)
    chapter6.video_blurb = "Alright, brace yourself: it’s time to dive into the world of Absolute and Comparative Advantage. No, it’s not a new Marvel movie, though it could be—after all, one is all about who’s got the bigger superpower (spoiler: it’s not always Robert Downey Jr.) You think being the best at something means you're automatically the one who should do it? Well, think again. This video will show you how even if you're the world's best at something, it doesn’t mean you’re <em>actually</em> the best person to do it. Sounds confusing? That's because it is... but in the best way possible. \n\n Forget about 'who’s better,' and start thinking about 'who’s least bad.' We’ll break down comparative advantage, where doing what you're least inefficient at might just be your golden ticket. So, get ready to rethink everything you thought you knew about trading, specialization, and making the most of your time—because economics has some real curveballs. And by the end of this, you might just feel like you’ve unlocked a cheat code to life-but probably not."
    
    chapter7 = db.session.get(Chapter, 7)
    chapter7.video_blurb = "Ready to show the AP exam who’s boss? In this follow-up video, we're taking you from 'okay, I sort of get it' to 'I could teach this stuff!' We're diving into those tricky AP-style questions on Absolute and Comparative Advantage that always seem designed to make you question your life choices. But don’t worry—we've got your back. \n\n By the end of this video, you’ll be breezing through questions that make most people sweat like they just opened a textbook in front of the whole class. You'll learn how to spot the sneaky tricks that AP loves to throw at you, and how to tackle them like an econ pro. No more guessing or second-guessing—just straight-up strategy and the confidence that comes with knowing you've got this in the bag. Ready to make the AP exam your personal playground? Yeah, we thought so."
    
    chapter8 = db.session.get(Chapter, 8)
    chapter8.video_blurb = "Ever notice how you <em>really</em> wanted to buy that life-sized gold statue of yourself… until you saw the price? Suddenly, it’s “maybe I’ll just get a nice framed photo.” That’s the Law of Demand in action—the idea that when prices go up, people decide they don’t actually need the 24-karat ego trip. It’s like how everyone wanted to own a Tesla... until they saw it costs about as much as a small island. Price has a magical way of turning “must-have” into “maybe I’ll pass.” \n\n In this video, we’re breaking down how the price of something can make you rethink your life choices. Think of it like hunting down rare, limited-edition sneakers or tickets Taylor Swift's concert—when the price is right, you feel like you have to have it, but raise it too much and suddenly you’re like, “I’m good, I’ll just stream it.” Once you get the Law of Demand, you’ll start seeing it everywhere, from your impulse buys to how much you’re willing to spend on a bottle of wine that tastes like regret. "

    chapter9 = db.session.get(Chapter, 9)
    chapter9.video_blurb = "Welcome to the wild world of demand shifts — where nothing stays the same, and everything gets a little more complicated. If you thought demand only changes when prices do, well, surprise! Just like how The Office had a whole new vibe after Steve Carell left (no, it wasn’t the same, and we all know it), demand can shift due to all sorts of crazy factors.  We're talking about when substitute goods, like switching from Starbucks to Dunkin' because your local Starbucks is out of oat milk, or complement goods, like nachos and cheese, because who eats nachos alone? \n\nIn this video, we’ll cover the big players: normal and inferior goods, consumer preferences, and the demographic changes that make demand curve-shifting almost as dramatic as a plot twist in Game of Thrones (but hopefully with fewer disappointing outcomes). When people suddenly start loving avocado toast and stop buying… whatever the opposite of avocado toast is, that’s a shift in demand. It’s not just about price anymore — it’s about what's cool, what's not, and who’s influencing your decisions. \n\n So grab your popcorn and get ready to see how even the smallest changes in the market — from new trends to demographic shifts — can make demand go totally haywire. It’s like the world is always changing the channel, and the remote is out of reach. Just like those Fast and Furious movies that won’t stop at part 10, demand doesn’t know when to quit. "
    
    chapter10 = db.session.get(Chapter, 10)
    chapter10.video_blurb = "Let’s talk about the law of supply, which is about as intuitive as trying to solve a Rubik’s Cube blindfolded. Essentially, the idea is simple: when prices go up, producers want to make and sell more. Sounds straightforward, right? But for some reason, this is where most econ teachers like to gloss over things or turn it into a maze of confusing explanations that leave you wondering if economics is secretly just a cruel joke. It’s counterintuitive, frustrating, and honestly, sometimes it just sucks. \n\n So why is it so confusing? Well, it doesn’t always make sense that the more expensive something is, the more of it people are willing to make. Isn’t that just... greedy? Exactly. It’s a strange concept, and it definitely feels like economics is out to make you feel dumb. But don’t worry — you’re not alone in thinking this is confusing, and you’re definitely not the only one who wishes you could just skip ahead to the part where economics gets <em>fun.</em>(This isn't fun?!?) \n\n Here’s the good news: by the end of this video, you’ll begrudgingly accept the law of supply as one of those things that <em>sort of</em> makes sense. I’m not saying you’ll love it, but you’ll get it, and that’s what really matters. So hang in there, we’ll pull this all together and make it clear enough that you can nod along and pretend you’re an economics expert."
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


