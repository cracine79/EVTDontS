import { useState, useEffect } from "react"
import { useSelector, useDispatch } from "react-redux"
import { getAllChapters } from "../Slices/chaptersActions"
import { openLoginModal, openSignupModal } from "../Slices/modalSlice"
import { useNavigate } from "react-router-dom"
import { getAllTopics } from "../Slices/topicsActions"



export const VideoIndex = () => {
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const currentUser = useSelector(state=>(state.user))
    const chapters = useSelector(state=>(state.chapters))
    const chaptersObj = Object.values(chapters)
    const topics = useSelector(state=>state.topics)
    const [videoId, setVideoId] = useState(false)
    const [currentTopics, setCurrentTopics] = useState([])

    useEffect(()=>{
        dispatch(getAllTopics())
    },[])

    const videoGo = (chapter) => {
        setVideoId(chapter.video_url)
        const chapter_topics = topics.filter(topic=>{topic.chapter_id = chapter.id})
        console.log(chapter_topics)
    }

    const chapterVid = (videoId) => {
        const chapter = chaptersObj.find(chapter=>chapter.video_url === videoId)
        return chapter.name
    }

    const handleGoToQuiz = () => {
        if(currentUser){
            navigate('/quiz', {state:{chapter: 1, type: 'chapterQuiz', topics: topics}})
        } else {
            dispatch(openSignupModal())
        }
    }
    return(
        <div className = 'mt-24'>

            <div className='min-h-screen w-100 flex'>
                <div className=' w-1/5 bg-lime-100 text-sm'>
                    <div>Video Library</div>
                    {chaptersObj.map(chapter=>{
                        return(
                            <div key={chapter.id} className='hover:cursor-pointer' onClick={()=>videoGo(chapter)}>{chapter.name}</div>
                        )
                    })}
                </div>
                <div className='w-5/6'>
                    <div className='text-center mt-10 text-4xl font-bold'>
                    Welcome to the Video Cache!
                    </div>
                    <div className='mx-8 mt-10 text-lg'>
                        You can access any and all of our treasure trove of videos that absolutely don't suck from the navigation bar on the left. 
                    </div>
                    <div className='mx-8 mt-4 text-lg'>
                    Choose wisely, and don't be like the Nazi guy in the end of Indiana Jones & The Last Crusade!
                    </div>
                    <div className='flex flex-col items-center justify-center mt-10 border'>
                        <div className='text-2xl my-4'>
                            {videoId ? `Video for ${chapterVid(videoId)}`: 'Choose a video already!'}
                        </div>
                        {videoId && (
                        <>
                        <div className='w-11/12 max-w-6xl aspect-video'>
                            <iframe 
                                className="w-full h-full"
                                src={videoId} 
                                allowFullScreen>
                            </iframe>
                        </div>
                        <div className='my-8 border py-4 px-2 bg-slate-400 border-black rounded-xl hover:bg-slate-600 hover:cursor-pointer' onClick={handleGoToQuiz}>
                            {currentUser ? 'Jump to Practice Quiz' : 'Sign Up to Access Practice Quiz'}
                        </div>
                        </>
                        )}
                    </div>
                </div>

            
                    
            </div>
        
        </div>
    )
}