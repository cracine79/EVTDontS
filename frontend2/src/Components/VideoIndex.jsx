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

        dispatch(getAllChapters())
        if(selectedChapterVideoUrl)
            setVideoId(selectedChapterVideoUrl)
      
    },[selectedChapterVideoUrl])

    const videoGo = (chapter, type) => {
        setMenuOpen(false)
        if(type=='long'){
            setVideoId(chapter.video_url)
            setChapterId(chapter.id)
        } else {
            setVideoId(false);
        }
  
    }

    const chapterVid = (videoId) => {
        const chapter = chaptersObj.find(chapter=>chapter.video_url === videoId)
        return chapter? chapter.name : ""
    }


    const handleSignUp = () => {
        if(!currentUser){
            dispatch(openSignupModal())
        } else {
            navigate('/userhome')
        }
    }

    const shortenedVideoName = (video) =>{
        return video.split(" ").slice(1).join(" ")
    }
    const handleGoToQuiz = () => {
        // console.log(chapterId)
        navigate('/quiz', {state:{chapter:chapterId, type: 'chapterQuizNoUser', topics:[]}})
    }
    return(
        <div className = 'mt-24'>
                    
            <div className='min-h-screen w-100  flex'>
             
                <div onClick={()=>setMenuOpen(true)} className='sm:hidden absolute bg-[#D6E6E2] z-1 w-1/2 text-center border-blue-600 border-solid border text-black'> ☰ Video Library</div>
                <div className={`sm:static fixed sm:w-1/5 min-h-[100vh] w-5/6 bg-[#D6E6E2]  z-10 text-sm text-black transform ${
                    menuOpen ? 'translate-x-0' : '-translate-x-full'
                } transition-transform sm:translate-x-0`}>
                    <div className='ml-4'>
                    <div className='sm:hidden mt-2 -mb-4' onClick={()=>{setMenuOpen(false)}}>X Close</div>
                    <div className='text-2xl font-bold text-center mt-4 -ml-8'>Video Library</div>
                    <div className='font-bold mt-2 text-lg'>Unit 1: Intro to Economic Concepts</div>
                    {chaptersObj.slice(0,6).map(chapter=>{
                        return(
                            <div key={chapter.id} className='hover:cursor-pointer ' onClick={()=>videoGo(chapter, "long")}>{chapter.name}</div>
                        )
                    })}
                    <div className='font-bold mt-2 text-lg'>Unit 2: Supply & Demand</div>
                    {chaptersObj.slice(7, 18).map(chapter=>{
                        return(
                            <div key={chapter.id} className='hover:cursor-pointer ' onClick={()=>videoGo(chapter, "long")}>{chapter.name}</div>
                        )
                    })}
                    <div className='font-bold mt-2 text-lg'>Unit 3: Elasticities</div>
                       {chaptersObj.slice(18, 24).map(chapter=>{
                        return(
                            <div key={chapter.id} className='hover:cursor-pointer ' onClick={()=>videoGo(chapter, "long")}>{chapter.name}</div>
                        )
                    })}

                    <div className='font-bold mt-2 text-lg'>Unit 4: Government Intervention </div>
                    {chaptersObj.slice(24).map(chapter=>{
                        return(
                            <>
                                <div key={chapter.id} className='hover:cursor-pointer ' onClick={()=>videoGo(chapter, "long")}>{chapter.name}</div>
                                <div className='text-gray-600'>4.2 Subsidies (coming soon!)</div>
                                <div className='text-gray-600'>4.3 Price Floors (coming soon!)</div>
                                <div className='text-gray-600'>4.4 Price Ceilings (coming soon!)</div>
                            </>
                        )
                    })}
                    </div>
                </div>
                <div className='sm:w-5/6 w-full'>
                    <div className='flex flex-col items-center'>
                        {!videoId && <>
                            <div className='text-center mt-6 text-4xl font-bold'>
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
                        <div className='mx-8 mt-4 text-lg'>After watching the video you can also try a practice quiz to test your economic skills.</div>
                        <div className='mx-8 mt-4 text-lg'>
                        Choose wisely—unlike that guy in Indiana Jones and the Last Crusade. You know, the one who didn’t. Your economics journey depends on it.
                        </div>
                        </>}
                    </div>
                    <div className='flex flex-col items-center justify-center sm:mt-10 mt-6 '>
                        <div className='sm:text-2xl text-lg mb-4'>
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
                        {/* <div className='flex justify-around  w-3/4'> */}
                        <div className='w-full justify-center flex flex-col sm:flex-row items-center mt-8'>
                            
                            <div className='button w-11/12 sm:w-auto sm:h-12' onClick={handleSignUp}>
                                {currentUser ? 'Mark Video As Watched' : 'Sign Up to Access Quizzes & More!'}
                            </div>
                            <div className='mx-12 py-2 sm:py-0 text-2xl'></div>
                            <div className='button w-11/12 sm:w-auto sm:h-12' onClick={handleGoToQuiz}>
                                Take a Practice Quiz on {shortenedVideoName(chapterVid(videoId))}
                        </div>
                    </div>
                            {/* <div className='my-8 border py-4 px-2 bg-slate-400 border-black rounded-xl hover:bg-slate-600 hover:cursor-pointer' onClick={()=>videoGo(videoId, 'short')}>
                                Feeling Lazy?  Watch the (SUPER) short version.
                            </div> */}
                        {/* </div> */}
                        
                        </>
                        )}
                    </div>
                </div>

            
                    
            </div>
        
        </div>
    )
}