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
    const type = location.state?.type
    const topics = location.state?.topics



    const data = {
        chapter: chapter,
        type: type,
        topics: topics
    }


    useEffect(()=>{
        dispatch(getQuestions(data)), [dispatch]
    })
    
    
    // const whole_chapter = useSelector((state)=>state.chapters[chapter])
    // const chapter_name = whole_chapter.name
    
    // console.log(type == 'chapterQuiz')
    const handleOpen = () => {
        dispatch(openQuizModal())
    }
    const goHome = ()=>{
        navigate('/userhome')
    }

    return (
        <div className="w-full flex flex-col justify-center items-center">
            <div className='mt-40  aspect-video justify-center w-3/4'>
                <div>
                    {type == 'chapterQuiz' && <>This is the page for the quiz for Chapter {chapter_name}</>}
                </div>
                <div>
                    {type == 'topicQuiz' && <>This is the page for the quiz for topic review</>}
                </div>
                <div className='flex justify-around'>
                <button className='mt-10 
                            border-black 
                            h-1/5 
                            w-40 
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-stone-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer
                            mb-6'
                            onClick={handleOpen}>Start The Quiz</button>

                <button className='mt-10 
                            border-black 
                            h-1/5 
                            w-40 
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-stone-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer
                            mb-6'
                            onClick={goHome}>Back to Dashboard</button>
                </div>
               
            </div>
            <QuestionComponent chapter={chapter} type={type}/>
        </div>
      
    )
}