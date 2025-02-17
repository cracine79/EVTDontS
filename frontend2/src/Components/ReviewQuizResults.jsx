import { useLocation, useNavigate } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux"
import { openResultsModal } from "../Slices/modalSlice"
import { ResultsModal } from "./ResultsModal"
import { clearUserResults } from "../Slices/resultsSlice"
import { clearQuestions } from "../Slices/questionsSlice"
import { useMemo, useEffect } from "react"

export const ReviewQuizResults = () => {
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const results = useSelector(state=>(state.results))
    const resultsObj = Object.values(results)
    const location = useLocation()
    const topics = location.state?.topics
    const type = location.state?.type
    const topicProg = useSelector(state=>state.topicProg)
    const topicProgObj = Object.values(topicProg)
    const mergedTopics = useMemo(() => {
        return topics.map(topic => {
            const dictEntry = topicProg[topic.topic_id];
            return { ...topic, ...dictEntry };
        });
    }, [topics, topicProg]);

    const names = topics.map(topic => topic.topic_name)

    const formattedNames = names.length > 1 
    ? names.slice(0, -1).join (', ') + ' and ' + names[names.length -1]    
    : names[0]

    let numCorrect = 0
    resultsObj.forEach((result)=>{
        if (result.isCorrect == true){
            numCorrect += 1
        }
    })
    const percentageScore = Math.floor((numCorrect/resultsObj.length)*100)
    useEffect(()=>{
        window.scrollTo(0,0)
    },[])
    const showResults = () => {
        dispatch(openResultsModal())
    }

    const goHome = () => {
        dispatch(clearUserResults())
        dispatch(clearQuestions())
        navigate('/userhome')
    }

    const goAgain = () => {
        dispatch(clearUserResults())
        dispatch(clearQuestions())
        navigate('/quiz', {state: {chapter: 1, type: 'topicQuiz', topics: topics}})

    }
 
    const ranking = (percent) => {
   
        if(percent > 80){
            return(
                <div className='text-green-700'>
             Neo in the Matrix Level Clarity
            </div>
            )
        } else if (percent > 70) {
            return (
                <div className='text-lime-600'>
                A Werner Herzog Documentary Production Value
                </div>)
        } else if (percent > 60) {
            return (
                <div className='text-amber-500'>
                     An Intern on their Third Cup of Coffee Level Sharpness
                </div>
               )
        } else if (percent > 50) {
            return (
                <div claddName='text-pink-700'>
                The depth of the lyrics of an early 2000s Boy Band Song
                </div>)
        } else {
            return (<div className='text-red-500'>Michael Scott Trying to Declare Bankruptcy Level Knowledge
            </div>)
        }
    }

    const getQuestionsAsked = (topicName) => {
        const topic = topicProgObj.find(topic => topic.topic_name == topicName)
        return topic.questions_asked
    }

    const getQuestionsAnswered = (topicName) => {
        const topic = topicProgObj.find(topic => topic.topic_name == topicName)
        return topic.answered_correctly
    }

    const topicMastery = () => {
        return(
            <div className='flex sm:flex-wrap sm:flex-row flex-col justify-start sm:mr-8 mt-6'>
                {mergedTopics.map((topic=>{
                    return(
                        <div key={topic.id} className=' sm:basis-1/5 mx-6 my-2 border-2 rounded-lg border-slate-300'>  
                            <div className='mt-4 mx-4'>
                                <div className='mt-2 font-bold text-center text-xl'>
                                    Topic: {topic.topic_name}
                                </div>
                                <div>
                                    You have faced down&nbsp;<span className='font-bold text-lg'>
                                        {topic.questions_asked}
                                    </span>
                                    &nbsp;questions on this topic and answered&nbsp;
                                    <span className='font-bold text-lg'>{topic.answered_correctly} </span>correctly.
                                </div>
                                <div className='mt-2'>
                                    Your current level of understanding of {topic.topic_name} is equivalent to: 
                                </div>
                                <div className='font-bold mb-4'>
                                    {ranking(topic.percent_correct)}
                                </div>

                            </div>
                        
                        </div>
                    )
                }))}
            </div>
        )

    }
    const goodSentence = [
        "Well, look at you, making economic principles bow before your mighty intellect! Somewhere, a supply-and-demand curve just shed a proud tear.",
        "You crushed that quiz like a monopolist crushing competition!",
        "Some people balance budgets; you just balanced right on the line between impressive and economically intimidating!",
        "Boom! You absolutely Ricardianly owned that quiz. Comparative advantage? Clearly, it's you vs. the rest of us mere mortals.",
        "That was some fine-tuned economic genius. You’re practically a walking case study on human capital!"
    ]

    const mediumSentence = [
        "Not exactly breaking economic records, but hey, there were some correct answers in there!",
        "Not bad, not great—kind of like a lukewarm cup of coffee. But, hey, caffeine is caffeine!",
        "In the economic cycle of quiz performance, consider this a gentle recession. Not great, not the end of the world either!",
        "Not too hot, not too cold—call it the Goldilocks of quiz scores!",
        "I wouldn't brag to Dave Grohl about that score, but I'd probably tell my mom"
    ]

    const badSentence = [
        "Oof. That score tanked harder than Blockbuster stock in 2008.",
        "Alright, maybe not quite booming, but still very much in the expansion territory for effort!",
        "It’s a marathon, not a sprint—just think of this score as a warm-up lap!",
        "Think of it as an investment in learning—sometimes the market just dips a little.",
        "Even the best economists hit a rough patch! You’ve got a strong foundation for next time."
    ]
    const scorePraise = () => {
        const randomNumber = Math.floor(Math.random() * 5);
        if(percentageScore > 85){
            return goodSentence[randomNumber] 
        } else if (percentageScore > 50){
            return mediumSentence[randomNumber] 
        } else {
            return badSentence[randomNumber]
        }
    }
    return(
        <>

            <div className='w-screen flex justify-center min-h-[calc(100vh-100px)]'>
            <div className="sm:mt-40 mt-28 mb-24 w-11/12 h-auto border-black border-2 rounded-lg shadow-2xl">
                <div className='flex flex-col items-center justify-center '>
                <div className='sm:mt-10 mt-4 w-full'>

                <div >
                    <div className='sm:text-3xl text-xl text-center px-4'>
                    Results for {type=="review_quiz" ? "Topic Review": "Gauntlet"} Quiz on: <span className='text-blue'>{formattedNames}</span>
                    </div>
                <div className='flex'>
                    <div className='text-lg sm:mx-10 mx-2 sm:mt-10 mt-4'>
                        You answered {numCorrect} out of a total {resultsObj.length} questions correctly, for a quiz score of {percentageScore}%.  &nbsp;
                        {scorePraise()}
                    </div>
                </div>
                <div className="text-2xl text-center sm:ml-10 mx-2 sm: mt-10">
                    Topic Mastery Progress from This Quiz:
                </div>
                <div>
                    {topicMastery()}
                </div>
                </div>
                </div>
                <div className='flex flex-row justify-around my-10 w-full'>
                    <button className='
                            button' 
                            onClick={showResults }>Show Me What I Missed</button>
                    {type == 'topicQuiz' &&
                    <button className='
                    button' 
                    onClick={goAgain }>Take Another One</button>
                    }

                        <button className='
                       button' 
                            onClick={goHome}
                           >Back to Dashboard</button>
                            </div>
                </div>
            </div>
            
         
            </div>
     
            <ResultsModal />
       
        </>
    )
}