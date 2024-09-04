import { useSelector } from "react-redux"
import { useNavigate } from "react-router-dom"



export const Video = () => {
    const navigate = useNavigate()
    const currentChapterId = useSelector((state)=>state.user.currentChapter)
    
    const currentChapter = useSelector((state)=>state.chapters[currentChapterId])

    const source = currentChapter.video_url
    const handleClick = () => {
        navigate('/userhome')
    }
    console.log(source)
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
                <div>
                    Mark as Complete
                    (take me to the quiz)
                </div>
            </div>
        </div>
    )
}
