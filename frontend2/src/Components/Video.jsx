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
        console.log('fetching blurb')
        fetchBlurb()
    }, [chapterId])

    console.log(blurb)
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
        console.log(data)

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
             <div className='text-center text-3xl my-6'>{currentChapter.name}</div>
        <div className='aspect-video justify-between w-7/12 flex flex-col'>
           
            <div className="w-full h-full">
                <iframe className="w-full h-full" 
                        src={`${source}?modestbranding=1&rel=0&controls=1&autohide=1`}
                        title="title" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                        referrerPolicy="strict-origin-when-cross-origin" 
                        allowfullscreen></iframe>
            </div>
        </div>


            <div className="whitespace-pre-line w-3/4 mt-10">
                {blurb}
            </div>
            <div className='flex justify-between w-1/2 mt-6'>
                <div onClick = {handleClick} className={
                            `mt-10 
                            border-black 
                            h-auto 
                            w-1/3
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-xl
                            bg-slate-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer
                            mb-6
                            text-center
                            `}>
                    Back to my Dashboard
                </div>
                <div onClick = {completeVid} className=
                            {`mt-10 
                            flex
                            flex-col
                            border-black 
                            h-auto
                            w-1/3 
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-xl
                            bg-slate-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer
                            mb-6
                            `}>
                    <p>Mark as Completed</p>
                    <p>Let's Rock the Quiz</p>
                </div>
            </div>
        </div>
    )
}
