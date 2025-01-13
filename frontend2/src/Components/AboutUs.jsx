import { useEffect } from "react"
export const AboutUs = () => {
    useEffect(()=>{
        scrollTo(0,0)
    },[])
    return(
        <div className='w-full flex flex-col  items-center  mt-44'>
            <div className='sm:w-7/12 w-5/6 flex flex-col'>
                <div className='text-4xl font-bold'>
                    About Us
                </div>
                <div className="mt-4">
                Welcome to <strong>Economics Videos That Don't Suck </strong>- the scrappy little website on a mission to revolutionize economics education (and maybe education in general). This site is what happens when an educator with over 20 years of experience teaching business and econ at the high school and university level decides to tackle two burning questions: “Why does learning economics feel like pulling teeth?” and “Can we make AP test prep suck less?” Spoiler: Yes, we can. (And we’re doing it.)
                </div>
                <div className='text-xl mt-4 mb-2 font-bold'>
                    Who's Behind This?
                </div>
                <div>
                It’s just me. Literally. Every video, quiz, diagram, illustration, and animation, and even the entire website—from front to backend—was created by yours truly. I’m also the designer of the algorithm that tracks which topics and questions trip you up, so I can throw better, more targeted review quizzes your way. (You’re welcome.)  
                </div>
                <div className='my-4'>
                When I’m not creating content for this website, I’m dreaming up even more features to make economics engaging, digestible, and downright enjoyable. This site might be in its infancy, but I’ve got big plans. Think more videos, smarter quizzes, and who knows, maybe a feature where your wrong answers unlock old movie trivia… because keeping classic films relevant feels like the right thing to do.
                </div>
                <div className='text-xl mt-2 mb-2 font-bold'>
                    What is the Goal Here?
                </div>
                <div>
                    I'm here to:
                </div>
                <ol className="list-decimal ml-8 mt-2">
                    <li><strong>Make Videos That Don’t Waste Your Time</strong>: These videos don’t just skim the surface. They’re comprehensive, clear, and filled with tips to help you crush the AP exam like it’s no big deal.</li>
                    <li className='my-2'><strong>Revolutionize Review</strong>: Tired of answering the same old questions? The EVTDS algorithm tracks the topics and types of questions you struggle with and builds quizzes tailored to YOUR weaknesses. It’s like having a personal tutor, but less awkward.</li>
                    <li><strong>Inject Some Fun (and Some Obscure Movie References) into Learning:</strong> Let’s face it, economics can be dry. I’m doing my best to fix that while sneaking in some nostalgia for classic films. (Economics meets the Breakfast Club? Stranger things have happened.)</li>
                </ol>
                <div className='text-xl mt-4 mb-2 font-bold'>
                    The Future Looks Bright!
                </div>
                <div>This site is just getting started. Over time, you can expect a tidal wave of content, features, and who knows what else. I’m aiming to make this the best resource out there for economics students and AP test-takers. And if you’re not a student? Stick around anyway. You might actually start to like economics.</div>

                <div className='text-xl mt-4 mb-2 font-bold'>
                    Oh, By the Way . . .
                </div>
                <div>
                If you’re hiring, <a className='font-bold hover:cursor-pointer'href="mailto:charleelracine@gmail.com">let’s talk</a>. I’m an educator with decades of experience, a knack for breaking down tough concepts, and a proven track record of building engaging content from scratch. (Seriously, you’re looking at it.) I’d love to bring my skills to a forward-thinking organization that’s ready to change how the world learns.
                </div>
                <div className='mt-2 mb-12'>
                So, whether you’re here for the videos, the quizzes, or the dry wit, welcome aboard. Let’s make economics make sense – and maybe even have some fun while we’re at it.
                </div>
            </div>
        </div>
    )
}