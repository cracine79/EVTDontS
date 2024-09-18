import { useSelector, useDispatch } from "react-redux"
import { useNavigate } from "react-router-dom"
import { csrfFetch } from "../csrf"
import { updateUserChapters } from "../Slices/chaptersSlice"
import { getQuestions } from "../Slices/questionsActions"




export const Video = () => {
    const navigate = useNavigate()
    const dispatch = useDispatch()
    
    const currentChapterId = useSelector((state)=>state.user.currentChapter)
    
    const currentChapter = useSelector((state)=>state.chapters[currentChapterId])

    const source = currentChapter.video_url
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
        updateVideoProgress(currentChapterId)
        navigate('/quiz', {state: {chapter: currentChapterId}})
    }

  
    return(
        <div className="w-full flex flex-col justify-center items-center">
        <div className='mt-40  aspect-video justify-center w-3/4'>
    
            <iframe className="w-full h-full" 
                    src={`${source}?modestbranding=1&rel=0&controls=1&autohide=1`}
                    title="title" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                    referrerpolicy="strict-origin-when-cross-origin" 
                    allowfullscreen></iframe>
        </div>
            <div className="whitespace-pre-line">
                {currentChapter.video_blurb}
            </div>
            <div className='flex justify-between w-1/2 mt-6'>
                <div onClick = {handleClick} className=
                            'mt-10 
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
                            '>
                    Back to my Dashboard
                </div>
                <div onClick = {completeVid} className=
                            'mt-10 
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
                            '>
                    <p>Mark as Completed</p>
                    <p>Let's Rock the Quiz</p>
                </div>
            </div>
        </div>
    )
}
