import { useSelector, useDispatch } from "react-redux"
import { useLocation, useNavigate } from "react-router-dom"
import { getQuestions } from "../Slices/questionsActions"
import { useEffect } from "react"
import { QuestionComponent } from "./QuestionComponent"
import { openQuizModal } from "../Slices/modalSlice"
import { clearQuestions } from "../Slices/questionsSlice"


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
    const whole_chapter = useSelector((state)=>state.chapters[chapter])
    const chapter_name = whole_chapter ? whole_chapter.name : ''

    const names = topics.map(topic => topic.topic_name)

    const formattedNames = names.length > 1 
    ? names.slice(0, -1).join (' and ') + ' and ' + names[names.length -1]    
    : names[0]

    const handleOpen = () => {
        dispatch(openQuizModal())
    }
    const goHome = ()=>{
        dispatch(clearQuestions())
        navigate('/userhome')
    }

    return (
        <div className="w-full flex flex-col justify-center items-center">
            <div className='mt-40  aspect-video justify-center w-3/4'>
                <div>
                    {type == 'chapterQuiz' && <>This is the page for the quiz for Chapter {chapter_name}</>}
                </div>
                <div>
                    {type == 'topicQuiz' && <>This is the page for the quiz to review the topics of of {formattedNames}</>}
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
            <QuestionComponent chapter={chapter} type={type} topics={topics}/>
        </div>
      
    )
}