import { useSelector, useDispatch } from "react-redux"
import { useLocation, useNavigate } from "react-router-dom"
import { getQuestions } from "../Slices/questionsActions"
import { useEffect } from "react"
import { QuestionComponent } from "./QuestionComponent"
import { openQuizModal } from "../Slices/modalSlice"


export const Quiz = () => {
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const location = useLocation()
    const chapter = location.state?.chapter
    console.log(chapter)

    useEffect(()=>{
        dispatch(getQuestions(chapter)), [dispatch]
    })

    const handleOpen = () => {
        dispatch(openQuizModal())
    }
    const goHome = ()=>{
        navigate('/userhome')
    }

    return (
        <div className="w-full flex flex-col justify-center items-center">
            <div className='mt-40  aspect-video justify-center w-3/4'>
                <div>This is the page for the quiz for Chapter {chapter}</div>
                <button onClick={handleOpen}>Start The Quiz</button>
                <button onClick={goHome}>Back to Dashboard</button>
            </div>
            <QuestionComponent />
        </div>
      
    )
}