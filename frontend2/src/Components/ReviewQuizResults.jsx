import { useLocation } from "react-router-dom"
import { useSelector } from "react-redux"

export const ReviewQuizResults = () => {
    const results = useSelector(state=>(state.results))
    const resultsObj = Object.values(results)
    const location = useLocation()
    const topics = location.state?.topics
    console.log(topics)

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
    return(
        <>
            <div className='h-20'>

            </div>

            <div className='w-screen flex justify-center'>
            <div className="mt-40 w-5/6 h-auto border-black border-2 rounded-lg shadow-2xl">
                <div className='flex flex-col items-center justify-center'>
                <div className='mt-10'>

                <div>

                This is the results for the topic review quiz on {formattedNames}
                <div>
                    You scored {percentageScore}% on the quiz
                </div>
                </div>
            </div>
            
            </div>
            </div>
            </div>
       
        </>
    )
}