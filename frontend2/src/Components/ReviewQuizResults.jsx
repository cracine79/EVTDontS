import { useLocation, useNavigate } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux"
import { openResultsModal } from "../Slices/modalSlice"
import { ResultsModal } from "./ResultsModal"



export const ReviewQuizResults = () => {
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const results = useSelector(state=>(state.results))
    const resultsObj = Object.values(results)
    const location = useLocation()
    const topics = location.state?.topics
    console.log('TOPICS ARE', topics)

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

    const showResults = () => {
    
        dispatch(openResultsModal())
    }

    const goHome = () => {
        navigate('/userhome')
    }

    const goAgain = () => {
        navigate('/quiz', {state: {chapter: 1, type: 'topicQuiz', topics: topics}})

    }

    const topicMastery = () => {
        return(
            topics.map((topic=>{
            return(
                <>  
                    <div>
                        {topic.topic_name}
                        <div>
                            You have faced down {topic.questions_asked} questions on this topic and answered {topic.answered_correctly} correctly
                        </div>
                        <div>
                            Your current status for {topic.topic_name} mastery is: 
                        </div>
                    </div>
                

                </>
            )
        })
                
    )
        

    )

    }
    return(
        <>
            <div className='h-20'>

            </div>

            <div className='w-screen flex justify-center'>
            <div className="mt-40 w-11/12 h-auto border-black border-2 rounded-lg shadow-2xl">
                <div className='flex flex-col items-center justify-center '>
                <div className='mt-10 ml-8 w-full'>

                <div >

                This is the results for the topic review quiz on {formattedNames}
                <div>
                    You scored {percentageScore}% on the quiz
                </div>
                <div className="text-4xl">
                    Topic Mastery Breakdown
                </div>
                <div>
                    {topicMastery()}
                </div>
                </div>
                </div>
                <div className='flex flex-row justify-around my-10 w-full'>
                    <button className='
                            border-black 
                            h-1/5 
                            w-1/4
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-stone-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer' 
                            onClick={showResults }>Show Me What I Missed</button>
                    <button className='
                            border-black 
                            h-1/5 
                            w-1/4
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-stone-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer' 
                            onClick={goAgain }>Take Another One</button>

                        <button className='
                            border-black 
                            h-1/5 
                            w-1/4
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-stone-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer' 
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