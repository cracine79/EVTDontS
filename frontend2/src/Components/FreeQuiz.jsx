import { useSelector, useDispatch } from "react-redux"
import { useParams } from "react-router-dom"
import { getQuestions } from "../Slices/questionsActions"
import { getAllChapters } from "../Slices/chaptersActions"
import { useEffect } from "react"
import { QuestionComponent } from "./QuestionComponent"
import { openQuizModal } from "../Slices/modalSlice"
import { clearQuestions } from "../Slices/questionsSlice"
import { useState } from "react"
import { IntroCard } from "./Quiz"
import { goToVideoPage, splitChapterName, unitStyle } from "./ui"


export const FreeQuiz = () => {

    const dispatch = useDispatch()
    const {chapterslug} = useParams()

    const chapterEntry = useSelector((state)=>
        Object.entries(state.chapters).find(([id, chapter]) => chapter.slug === chapterslug)
    );
    // chapterEntry is undefined until chapters load (e.g. when opened from a public page)
    const [chapterId, chapter] = chapterEntry || []

    const [quizBlurb, setQuizBlurb] = useState("")
    const [quizBlurbImgUrl, setQuizBlurbImgUrl] = useState("")
    
    const data = {
        chapter:chapterId,
        type:"chapterQuizNoUser",
        topics:[]
    }

    useEffect(()=>{
        if (!chapterEntry) dispatch(getAllChapters())
    }, [chapterEntry, dispatch])

    useEffect(()=>{
        if (!chapterId) return
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

    if (!chapter) {
        return <div className='pt-32 pb-32 text-center text-xl'>Loading quiz...</div>
    }

    const [num, title] = splitChapterName(chapter.name)

    const goBack = () => {
        dispatch(clearQuestions())
        goToVideoPage(chapter)
    }

    return (
        <div className="pt-24 sm:pt-28 pb-16 px-5 sm:px-10">
            <div className="max-w-6xl mx-auto">
                <IntroCard style={unitStyle(null)} eyebrow="Free practice quiz"
                    title={<>Are you ready to rock?<span className="block mt-2 text-2xl sm:text-3xl text-gray-200">{num} {title}</span></>}
                    image={quizBlurbImgUrl}>
                    <div className="whitespace-pre-line" dangerouslySetInnerHTML={{ __html: quizBlurb }}></div>
                </IntroCard>
                <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
                    <button type="button" className="btn-primary text-lg px-8 py-3" onClick={() => dispatch(openQuizModal())}>
                        <i className="fa-solid fa-play"></i> Start the quiz
                    </button>
                    <button type="button" className="btn-secondary text-lg px-8 py-2.5" onClick={goBack}>Back to the video</button>
                </div>
            </div>
            <QuestionComponent chapter={chapterId} type="chapterQuizNoUser" topics={[]} unit="1"/>
        </div>
    )
}
