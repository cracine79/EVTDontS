import { useSelector, useDispatch } from "react-redux"
import { useNavigate, useLocation, useParams } from "react-router-dom"
import { csrfFetch } from "../csrf"
import { updateUserChapters } from "../Slices/userChaptersSlice"
import { getQuestions } from "../Slices/questionsActions"
import { getChapterBlurb } from "../Slices/chaptersActions"
import { useEffect, useState } from "react"
import { updateVideoProgress } from "../Slices/videoActions"





export const Video = () => {
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const location = useLocation()
    const [blurb, setBlurb] = useState(null)
    const {chapterId} = useParams()
    
    const currentChapter = useSelector((state)=>state.chapters[chapterId])
    const currentUserChapter = useSelector((state)=>state.userChapters[chapterId])
    const alreadyWatched = currentUserChapter.video_completed
    const source = currentChapter.video_url


    useEffect(()=>{
        const fetchBlurb = async () => {
            const chapterBlurb = await getChapterBlurb(chapterId)
            setBlurb(chapterBlurb)
        }
        fetchBlurb()
        window.scrollTo(0,0)
    }, [chapterId])

    const handleClick = () => {
        navigate('/userhome')
    }

    const completeVid = () => {
        if(!alreadyWatched){
            dispatch(updateVideoProgress(chapterId, "watched"))
        }
        navigate('/quiz', {state: {chapter: chapterId, type: 'chapterQuiz', topics:[]}})
    }
    
    return(
        <div className='flex flex-col justify-center items-center'>
            <div className="mt-24 sm:mt-40 sm:mb-12 sm:min-h-[65vh] mx-auto px-8 grid grid-cols-1  sm:grid-cols-2  items-start">
                <div className="w-full">
                    <iframe
                    className="w-full aspect-video rounded-lg shadow-lg"
                    src={`${source}?modestbranding=1&rel=0&controls=1&autohide=1`}
                            title="title" 
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                            referrerPolicy="strict-origin-when-cross-origin" 
                            allowFullScreen
                    ></iframe>
                    
                </div>

                <div className='flex flex-col items-center'>
                <div className='text-center sm:text-3xl text-lg  mt-4 sm:mt-0 sm:mb-6'>{currentChapter.name}</div>
                <p className="whitespace-pre-line sm:w-3/4 w-full sm:mt-2 mt-4 sm:block" dangerouslySetInnerHTML={{ __html: blurb }}></p>
                </div>

                    

            </div>
            <div className='flex justify-around sm:flex-row flex-col  w-2/3 sm:w-1/2  mb-8'>
                    <div onClick = {handleClick} className="button !flex !items-center !justify-center my-4 sm:my-0 !py-2">
                        Back to my Dashboard
                    </div>
                    <div onClick = {completeVid} className="button  !px-8 !py-2">
                            {!alreadyWatched ?  <>
                                <p className='hidden sm:inline'>Mark as Completed &&nbsp;</p>
                                <p>Rock the Quiz</p>
                            </> : <>
                                    Take The Chapter Quiz {currentUserChapter.quiz_grade == null ? "" : "Again"}
                                </>}
                    </div>
                
            </div>
        </div>

    )
}
