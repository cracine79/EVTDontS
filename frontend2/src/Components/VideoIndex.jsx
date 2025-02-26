import { useState, useEffect } from "react"
import { useSelector, useDispatch } from "react-redux"
import { getAllChapters } from "../Slices/chaptersActions"
import { openLoginModal, openSignupModal } from "../Slices/modalSlice"
import { useNavigate, useLocation, Outlet } from "react-router-dom"
import { getAllTopics } from "../Slices/topicsActions"
import { updateVideoProgress } from "../Slices/videoActions"
import { VideoLibrary } from "./VideoLibrary"


export const VideoIndex = () => {
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const location = useLocation()
    const currentUser = useSelector(state=>(state.user.username))
    const chapters = useSelector(state=>(state.chapters))
    const currentUserChapters = useSelector(state=>state.userChapters)
    const topics = useSelector((state)=>state.topics)
    const userProg = useSelector((state)=>state.topicProg)
 
    let chaptersObj = []

    chaptersObj = Object.keys(chapters).map((key)=>({
        id: key,
        ...chapters[key]
    }))
    const [videoId, setVideoId] = useState(false)
    const [chapterId, setChapterId] = useState(false)
    const [menuOpen, setMenuOpen] = useState(false)
    const selectedChapterVideoUrl = location.state?.videoUrl

    useEffect(()=>{
        window.scrollTo(0,0)
      
    },[])

    return(
        <div className = 'sm:mt-24 mt-[78px]'>
                    
            <div className='min-h-screen w-100  flex'>
                <VideoLibrary />
                <div className='sm:w-5/6 w-full'>
                    <Outlet /> 
                </div>

            
                    
            </div>
        
        </div>
    )
}