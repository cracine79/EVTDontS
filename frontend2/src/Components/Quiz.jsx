import { useSelector, useDispatch } from "react-redux"
import { useLocation } from "react-router-dom"
import { getQuestions } from "../Slices/questionsActions"
import { useEffect } from "react"
export const Quiz = () => {
    const dispatch = useDispatch()
    const location = useLocation()
    const chapter = location.state?.chapter
    console.log(chapter)
    useEffect(()=>{
        dispatch(getQuestions(chapter)), [dispatch]
    })

    return (
        <div className="w-full flex flex-col justify-center items-center">
            <div className='mt-40  aspect-video justify-center w-3/4'>
                <div>This is the page for the quiz for Chapter {chapter}</div>
                <button>Start The Quiz</button>
            </div>
        </div>
      
    )
}