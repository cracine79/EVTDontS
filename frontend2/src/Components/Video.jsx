import { useSelector, useDispatch } from "react-redux"
import { useNavigate, useLocation, useParams } from "react-router-dom"
import { csrfFetch } from "../csrf"
import { updateUserChapters } from "../Slices/userChaptersSlice"
import { getQuestions } from "../Slices/questionsActions"
import { getChapterBlurb } from "../Slices/chaptersActions"
import { useEffect, useState } from "react"





export const Video = () => {
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const location = useLocation()
    const [blurb, setBlurb] = useState(null)
    const {chapterId} = useParams()
    
    const currentChapter = useSelector((state)=>state.chapters[chapterId])
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

    const updateVideoProgress = async(chapterId) => {
        try {
            const response = await csrfFetch('/api/progress/' , {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                  },
                body: JSON.stringify({ chapter_id: chapterId }),
            });

        const data = await response.json()

        dispatch(updateUserChapters(data))
        } catch (error) {
            console.error("error finding", error)
        }
    }

    const completeVid = () => {
        updateVideoProgress(chapterId)
        navigate('/quiz', {state: {chapter: chapterId, type: 'chapterQuiz', topics:[]}})
    }
    

  
    return(
        <div className="w-full flex flex-col justify-center items-center mt-24">
             <div className='text-center sm:text-3xl text-xl  my-6'>{currentChapter.name}</div>
        
        <div className='aspect-video justify-between sm:w-1/2 w-full flex flex-col'>
           
            <div className="w-full h-full">
                <iframe className="w-full h-full" 
                        src={`${source}?modestbranding=1&rel=0&controls=1&autohide=1`}
                        title="title" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                        referrerPolicy="strict-origin-when-cross-origin" 
                        allowFullScreen></iframe>
            </div>
        </div>


            <p className="whitespace-pre-line sm:w-3/4 w-5/6 mt-10 hidden sm:block" dangerouslySetInnerHTML={{ __html: blurb }}></p>
            <div className='flex justify-between sm:flex-row flex-col w-1/2 mt-6 mb-8'>
                <div onClick = {completeVid} className="button  !px-8 !py-2">
                        <p className='hidden sm:inline'>Mark as Completed &&nbsp;</p>
                        <p>Rock the Quiz</p>
                </div>
                <div onClick = {handleClick} className="button !flex !items-center !justify-center !py-2 mt-6 sm:mt-0">
                    Back to my Dashboard
                </div>

                
            </div>
            <p className="whitespace-pre-line sm:w-3/4 w-5/6 mt-4 mb-6 sm:hidden" dangerouslySetInnerHTML={{ __html: blurb }}>
                {/* {blurb} */}
            </p>
        </div>
    )
}
