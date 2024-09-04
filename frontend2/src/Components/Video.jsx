import { useSelector, useDispatch } from "react-redux"
import { useNavigate } from "react-router-dom"
import { csrfFetch } from "../csrf"
import { updateUserChapters } from "../Slices/chaptersSlice"




export const Video = () => {
    const navigate = useNavigate()
    const dispatch = useDispatch
    
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
       
    }
  
    return(
        <div className="w-full flex flex-col justify-center items-center">
        <div className='mt-40  aspect-video justify-center w-3/4'>
    
            <iframe className="w-full h-full" src="https://www.youtube.com/embed/WqlGzTYXd0U"   title="title" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            </div>
            <div>
                Text text text text
            </div>
            <div>
                <div onClick = {handleClick}>
                    Back to my Dashboarddd
                </div>
                <div onClick = {completeVid}>
                    Mark as Complete
                    (take me to the quiz)
                </div>
            </div>
        </div>
    )
}
