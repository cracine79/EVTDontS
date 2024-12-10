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

    const quizTopicList = () => {
        return(
            <>
            {names.map((name)=>{
                return(<>name</>)
            })}
            </>
        )


    }

    const weaknessBlurb = () => {
        return(
            <div className='flex flex-col items-center w-3/4'>
                <p className='text-2xl font-bold mb-4'>Welcome to the Quiz of Reckoning!</p>
                <p>You’ve bravely clicked your way here, which means you're ready to face the ultimate showdown: you vs. your weak spots. Every wrong answer, every forgotten concept, every question that left you scratching your head is back—like the ghost of marginal utility haunting your economic soul. Don’t be surprised if your quiz is filled with questions from the topics you’d rather forget. Scarcity of knowledge? Let’s fix that. This quiz is designed to hit where it hurts—so we can turn those weaknesses into strengths.</p>
                <p className='my-6'>Take a deep breath and dive in. Remember, this is not just about acing the quiz—it’s about growth. The more you lean into your weak spots, the more of an econo ninja you’ll become. Every mistake is just another step toward mastery, and every correct answer is one closer to total economic enlightenment. So take the quiz, do your best, and don’t let a few wrong answers derail you. Weakness today, strength tomorrow!</p>

            </div>
        )
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
                            <div className = 'whitespace-pre-line mt-8 w-3/4 text-center' dangerouslySetInnerHTML={{__html: quizBlurb}}>
                                {/* {quizBlurb} */}
                            </div>
                        </div>}
                    {type == 'topicQuiz' && <>This is the page for the quiz to review the topics of of {formattedNames}</>}
                    {type == 'shortWeakspotQuiz' && weaknessBlurb()}
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