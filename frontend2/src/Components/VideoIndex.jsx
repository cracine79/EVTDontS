import { useState, useEffect } from "react"
import { useSelector, useDispatch } from "react-redux"
import { getAllChapters } from "../Slices/chaptersActions"
import { openLoginModal, openSignupModal } from "../Slices/modalSlice"
import { useNavigate, useLocation } from "react-router-dom"
import { getAllTopics } from "../Slices/topicsActions"


export const VideoIndex = () => {
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const location = useLocation()
    const currentUser = useSelector(state=>(state.user.username))
    const chapters = useSelector(state=>(state.chapters))
    const chaptersObj = Object.values(chapters)
    const [videoId, setVideoId] = useState(false)
    const [menuOpen, setMenuOpen] = useState(false)
    const selectedChapterVideoUrl = location.state?.videoUrl

    useEffect(()=>{
        window.scrollTo(0,0)

        dispatch(getAllChapters())
        if(selectedChapterVideoUrl)
            setVideoId(selectedChapterVideoUrl)
      
    },[selectedChapterVideoUrl])
    console.log(selectedChapterVideoUrl)
    const videoGo = (chapter) => {
        setMenuOpen(false)
        setVideoId(chapter.video_url)
    }

    const chapterVid = (videoId) => {
        const chapter = chaptersObj.find(chapter=>chapter.video_url === videoId)
        return chapter? chapter.name : ""
    }

    const handleGoToQuiz = () => {
        if(!currentUser){
            dispatch(openSignupModal())
        } else {
            navigate('/userhome')
        }
    }
    return(
        <div className = 'mt-24'>
                    
            <div className='min-h-screen w-100  flex'>
             
                <div onClick={()=>setMenuOpen(true)} className='sm:hidden absolute bg-lime-100 z-1 w-1/2 text-center border-green-600 border-solid border'> ☰ Video Library</div>
                <div className={`sm:static fixed sm:w-1/5 min-h-[100vh] w-5/6 bg-lime-100 text-sm transform ${
                    menuOpen ? 'translate-x-0' : '-translate-x-full'
                } transition-transform sm:translate-x-0`}>
                    <div className='ml-4'>
                    <div className='sm:hidden mt-2 -mb-4' onClick={()=>{setMenuOpen(false)}}>X Close</div>
                    <div className='text-2xl font-bold text-center mt-4 -ml-8'>Video Library</div>
                    <div className='font-bold mt-2 text-lg'>Unit 1: Intro to Economic Concepts</div>
                    {chaptersObj.slice(0,6).map(chapter=>{
                        return(
                            <div key={chapter.id} className='hover:cursor-pointer ' onClick={()=>videoGo(chapter)}>{chapter.name}</div>
                        )
                    })}
                    <div className='font-bold mt-2 text-lg'>Unit 2: Supply & Demand</div>
                    {chaptersObj.slice(7, 18).map(chapter=>{
                        return(
                            <div key={chapter.id} className='hover:cursor-pointer ' onClick={()=>videoGo(chapter)}>{chapter.name}</div>
                        )
                    })}
                    <div className='font-bold mt-2 text-lg'>Unit 3: Elasticities</div>
                       {chaptersObj.slice(18).map(chapter=>{
                        return(
                            <div key={chapter.id} className='hover:cursor-pointer ' onClick={()=>videoGo(chapter)}>{chapter.name}</div>
                        )
                    })}

                    <div className='font-bold mt-2 text-lg'>Unit 4: Government Intervention in Markets</div>
                        <div className='mt-2'>(Coming Soon!)</div>
                    </div>
                </div>
                <div className='sm:w-5/6 w-full'>
                    <div className='flex flex-col items-center'>
                        {!videoId && <>
                            <div className='text-center mt-10 text-4xl font-bold'>
                        Welcome to the Video Cache!
                        </div>
                        <img className='max-h-[60vh] 'src='https://evtds-seeds.s3.us-east-2.amazonaws.com/ChooseWiselyCartoon_1.png'></img>
                        <div className='mx-8 mt-10 text-lg'>
                        Welcome to the ultimate treasure trove of economics videos! Here, you'll find everything you need to navigate the wild world of supply, demand, 
                            and opportunity cost—with just the right amount of bad animation and obscure movie references to keep things interesting. Each video is a 
                            stepping stone to mastering economic concepts, and you can access any and all of our treasure trove of videos that absolutely don't suck 
                            <span className='inline sm:hidden'> by accessing the <span className='font-bold'>Video Library</span> above.</span> 
                            <span className='hidden sm:inline'> from the menu on the left.</span>
                            
                        </div>
                        <div className='mx-8 mt-4 text-lg'>
                        Choose wisely—unlike that guy in Indiana Jones and the Last Crusade. You know, the one who didn’t. Your economics journey depends on it.
                        </div>
                        </>}
                    </div>
                    <div className='flex flex-col items-center justify-center sm:mt-10 mt-6 '>
                        <div className='sm:text-2xl text-lg my-4'>
                            {videoId ? `Video for ${chapterVid(videoId)}`: ''}
                        </div>
                        {videoId && (
                        <>
                        <div className='sm:w-11/12 w-full max-w-6xl aspect-video'>
                            <iframe 
                                className="w-full h-full"
                                src={videoId} 
                                allowFullScreen>
                            </iframe>
                        </div>
                        <div className='my-8 border py-4 px-2 bg-slate-400 border-black rounded-xl hover:bg-slate-600 hover:cursor-pointer' onClick={handleGoToQuiz}>
                            {currentUser ? 'Back to User Dashboard' : 'Sign Up to Access Quizzes & More!'}
                        </div>
                        </>
                        )}
                    </div>
                </div>

            
                    
            </div>
        
        </div>
    )
}