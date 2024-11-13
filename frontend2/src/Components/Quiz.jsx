import { useSelector, useDispatch } from "react-redux"
import { useLocation, useNavigate } from "react-router-dom"
import { getQuestions } from "../Slices/questionsActions"
import { useEffect } from "react"
import { QuestionComponent } from "./QuestionComponent"
import { openQuizModal } from "../Slices/modalSlice"
import { clearQuestions } from "../Slices/questionsSlice"
import { useState } from "react"


export const Quiz = () => {
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const location = useLocation()
    const chapter = location.state?.chapter
    const type = location.state?.type
    const topics = location.state?.topics
    const unitQuizUnitId = location.state?.unit
    const units = useSelector(state=>state.units)
    const [quizBlurb, setQuizBlurb] = useState("")
    const [quizBlurbImgUrl, setQuizBlurbImgUrl] = useState("")
    const data = {
        chapter: chapter,
        type: type,
        topics: topics
    }
     
    const currentUnit = units[unitQuizUnitId]

    useEffect(()=>{
        const fetchData = async () => {
            const results =  await dispatch(getQuestions(data))
            setQuizBlurb(results.quiz_blurb)
            setQuizBlurbImgUrl(results.quiz_blurb_img_url)
        }
        fetchData()
        }, [dispatch]
        
    )
    
    

    const wholeChapter = useSelector((state)=>state.chapters[chapter])
    console.log('WC', chapter)
    // const currentUnit = wholeChapter ? useSelector((state)=>state.units[wholeChapter.unit_id]) : ""
    const chapterName = wholeChapter ? wholeChapter.name : ''

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
                <div className='flex justify-center'>
                    {type == 'chapterQuiz' && 
                        <div className='items-center flex flex-col'>
                            <div className='text-2xl text-center'>
                                <div>
                                Prepare to Show Your Stuff! 
                                </div>
                                <div>
                                This is the quiz for Chapter {chapterName}
                                </div>
                            </div>
                            <div className ='mt-6 w-5/12'>
                                <img src = {quizBlurbImgUrl} />
                            </div>
                            <div className = 'mt-8 w-3/4 text-center' dangerouslySetInnerHTML={{__html: quizBlurb}}>
                                {/* {quizBlurb} */}
                            </div>
                        </div>}
                    {type == 'topicQuiz' && <>This is the page for the quiz to review the topics of of {formattedNames}</>}
                    {type == 'shortWeakspotQuiz' && <>This is the page to take a quiz that focuses on your weaknesses</>}
                    {type == 'unitQuiz' && <>This is the page for Unit Quiz on {currentUnit.name}</>}
                </div>
                <div>
                  
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
            <QuestionComponent chapter={chapter} type={type} topics={topics} unit={unitQuizUnitId}/>
        </div>
      
    )
}