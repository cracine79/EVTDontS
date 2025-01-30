import { useLocation } from "react-router-dom"
export const UserlessResults = () => {
    const location = useLocation()
    const quizData = location.state?.quizData
    console.log(quizData.answers)
    return(
        <>
            <div className='mt-36'>Hello from Userless Results</div>
            <>{quizData.quiz_score}</>

        </>
    )
}