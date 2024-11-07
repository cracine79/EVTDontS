import { useSelector, useDispatch } from "react-redux"
import { useLocation, useNavigate } from "react-router-dom"
import { useMemo } from "react"
import { ResultsModal } from "./ResultsModal"
import { openResultsModal } from "../Slices/modalSlice"
import { clearUserResults } from "../Slices/resultsSlice"
import { clearQuestions } from "../Slices/questionsSlice"
export const UnitQuizResults = () => {
    const dispatch = useDispatch()
    const location = useLocation()
    const navigate = useNavigate()

    const topics = location.state?.topics
    const topicProg = useSelector(state=>state.topicProg)
    const topicProgObj = Object.values(topicProg)
    const mergedTopics = useMemo(()=>{
        return topics.map(topic=>{
            const dictEntry = topicProg[topic.topic_id]
            return {...topic, ...dictEntry}
        })
    }, [topics, topicProg])

    const currentChapterId = useSelector(state=>state.user.currentChapter)
    const currentUnitId = location.state?.unitId
    const units = useSelector(state=>state.units)
    const currentUnit = units[currentUnitId]
    
    const results = useSelector(state=>(state.results))
    const resultsObj = Object.values(results)

    let numCorrect = 0
    resultsObj.forEach((result)=>{
        if (result.isCorrect == true){
            numCorrect += 1
        }
    })
    const percentageScore = Math.floor((numCorrect/resultsObj.length)*100)

    const scoreHeader = () => {
        if(percentageScore >= 70){
            return(<p>Absolutely destroyed it! If the AP exam had legs, it’d be sprinting away in the other direction right now. With skills like that, you’re on the fast track to making College Board’s hardest questions look like elementary math. Seriously, if they awarded trophies for multiple-choice annihilation, we’d be shipping one to you right now. But we’ll settle for sending you back to destroy the next unit instead – this AP exam doesn’t stand a chance!</p>)
        }else if (percentageScore >50){
            return(<p>Nice work! You’re pacing yourself perfectly for a victory lap when the AP exam comes around. Sure, you could stop here and probably make College Board mildly uncomfortable, but a few more rounds with these quizzes will have them issuing a warning. Come back, sharpen those skills a bit more, and soon you’ll be making those exam questions feel as weak as our ‘state-of-the-art’ website! Keep it up – greatness awaits!</p>)
        }else {
            return(<p>Let’s just say you’re giving the AP exam way too much confidence. But no worries – that’s why these quizzes are here (we’ll let you practice while the College Board sweats). Give it another go, take down those questions one by one, and show that AP test it can’t hide behind fancy vocab and graphs forever. You’ve got this, and, unlike our ‘super helpful’ website, the AP exam isn’t actually impossible! </p>)
        }
    }

    const showResults = () => {
        dispatch(openResultsModal())
    }

    const retake = () => {
        dispatch(clearUserResults())
        dispatch(clearQuestions())
        navigate('/Quiz',  {state: {chapter: 1, type: 'unitQuiz', topics: [], unit: currentUnitId}})

    }

    const goHome = () => {
        dispatch(clearUserResults())
        dispatch(clearQuestions())
        navigate('/userhome')
    }
    return(
        <>

        <div className='w-screen flex justify-center min-h-[calc(100vh-100px)]'>
            <div className="mt-40 mb-24 w-11/12 h-auto border-black border-2 rounded-lg shadow-2xl">
                <div className='flex flex-col items-center justify-center '>
                    <div className='mt-10 ml-8 w-full'>
                        <div className='text-3xl text-center'>
                            Results for quiz on {currentUnit.name}
                        </div>
                        <div className = 'mt-4 text-xl'>You answered <span className='font-bold'>{numCorrect} out of a total possible {resultsObj.length} questions</span> correctly.  Your total score on this quiz was <span className = 'font-extrabold'>{percentageScore}%</span></div>
                        <div className = 'mt-4 text-xl'>{scoreHeader()}</div>
                    </div>
                    <div className='flex flex-row justify-around my-10'>
                    <button className='
                            border-black 
                            h-1/5 
                            w-1/5
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-stone-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer' 
                            onClick={showResults}>Show Me What I Missed</button>
                    <button className='
                            border-black 
                            h-1/5 
                            w-1/5
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-stone-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer' 
                            onClick={retake}>Gimme A Mulligan.  Take that bad boy again.</button>
            
                    <button className='
                            border-black 
                            h-1/5 
                            w-1/5
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-stone-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer' 
                            onClick={goHome}>Back to my dashboard please.</button>
                </div>
                </div>
            </div>
            <ResultsModal />
        </div>
        </>
    )
}