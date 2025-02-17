import { useSelector, useDispatch } from "react-redux"
import { useLocation, useNavigate, useParams } from "react-router-dom"
import { getQuestions } from "../Slices/questionsActions"
import { useEffect } from "react"
import { QuestionComponent } from "./QuestionComponent"
import { openQuizModal } from "../Slices/modalSlice"
import { clearQuestions } from "../Slices/questionsSlice"
import { useState } from "react"


export const FreeQuiz = () => {

    const navigate = useNavigate()
    const dispatch = useDispatch()
    const location = useLocation()
    const {chapterslug} = useParams()

    const chapterEntry = useSelector((state)=>
        Object.entries(state.chapters).find(([id, chapter]) => chapter.slug === chapterslug)
    );
    const [chapterId, chapter] = chapterEntry

    const [quizBlurb, setQuizBlurb] = useState("")
    const [quizBlurbImgUrl, setQuizBlurbImgUrl] = useState("")
    
    const data = {
        chapter:chapterId,
        type:"chapterQuizNoUser",
        topics:[]
    }

    useEffect(()=>{
        const fetchData = async () => {
            const results =  await dispatch(getQuestions(data))
            
            setQuizBlurb(results.quiz_blurb)
            if(results.quiz_blurb_img_url){
                setQuizBlurbImgUrl(results.quiz_blurb_img_url)
            } else {
                setQuizBlurbImgUrl("https://evtds-seeds.s3.us-east-2.amazonaws.com/inprogresscartoon.png")
            }
            
         
        }
        fetchData()
        window.scrollTo(0,0)
        
    }, [chapterId, dispatch]
    )

    const chapterName = chapter.name

    const handleOpen = () => {
        dispatch(openQuizModal())
    }

    const goHome = ()=>{
        dispatch(clearQuestions())
        navigate('/video-library')
    }

    return(
        <div className='flex flex-col justify-center items-center'>
            <div className="max-w-10xl   mt-24 sm:mt-32 sm:min-h-[65vh] sm:ml-20 px-8 grid grid-cols-1  sm:grid-cols-2  items-center">
                
                <div>
                    <div className='sm:text-2xl sm:w-5/6 text-xl text-center'>
                            <div className='sm:text-4xl text-3xl sm:mb-4'>
                            Are You Ready To Rock?
                            </div>
                            <div>
                            Get Ready to Take a Free Review Quiz on: <p className='font-bold'>Chapter {chapterName}</p>
                            </div>
                            <div className ='sm:w-full sm:hidden '>
                                <img src = {quizBlurbImgUrl} />
                            </div>
                            <div className = 'whitespace-pre-line mt-8  w-full  text-left text-xl' dangerouslySetInnerHTML={{__html: quizBlurb}}>
                            {/* {quizBlurb} */}
                            </div>
                    </div>
                </div>
                <div>
                <div className ='sm:w-8/12 hidden sm:block'>
                                <img src = {quizBlurbImgUrl} />
                            </div>
                </div>
          
            </div>
            <div className='flex justify-center w-full mt-8 mb-12'>
                    <button className="button !text-base !py-0 !px-4 my-4 !rounded-3xl" onClick={handleOpen}>Start The Quiz</button>
                    <div className='w-20'></div>
                    <button className="button !text-base !py-0 !px-4 my-4 !rounded-3xl"
                            onClick={goHome}> Back to Videos</button>
                </div>
            <QuestionComponent chapter={chapterId} type="chapterQuizNoUser" topics={[]} unit="1"/>
        </div>
    )
}