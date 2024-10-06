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
    ? names.slice(0, -1).join (' and ') + ' and ' + names[names.length -1]    
    : names[0]
    return(
        <>
            <div className='h-20'>

            </div>
            <div className='mt-10'>
                Hello from Review Page Results
                <div>

                This is the results for the topic review quiz on {formattedNames}
                </div>
            </div>
        </>
    )
}