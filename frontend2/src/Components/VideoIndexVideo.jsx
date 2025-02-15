import { useParams, useNavigate } from "react-router-dom"
import { useSelector } from "react-redux";
import { useDispatch } from "react-redux";
import { openSignupModal } from "../Slices/modalSlice";
import { updateVideoProgress } from "../Slices/videoActions";

export const VideoIndexVideo = () => {
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const {slug} = useParams()
    const chapterEntry = useSelector((state)=>
        Object.entries(state.chapters).find(([id, chapter]) => chapter.slug === slug)
    );
    const userProg = useSelector((state)=>state.topicProg)
    const [chapterId, chapter] = chapterEntry
    const userChapter = useSelector((state)=>state.userChapters[chapterId])
    console.log(userChapter)
    const topics = useSelector((state)=>state.topics)
   const videoId = chapter.video_url
   const currentUser = useSelector((state)=>state.user.username)
   const currentUserChapters = useSelector(state=>state.userChapters)
   const chapters = useSelector(state=>(state.chapters))
   const handleGoToQuiz = () => {
    // console.log(chapterId)
    if(!currentUser){
        navigate(`/freequiz/${chapter.slug}`)
    } else if (userChapter.quiz_grade == null || userChapter.quiz_grade < 50){
        navigate('/quiz', {state:{chapter:chapterId, type:'chapterQuiz', topics:[]}})
    } else {
        const chapter_topics = []
        Object.entries(topics).forEach(([topicId, topic])=>{
            if(topic.chapter_id == chapterId){
                chapter_topics.push({...topic, topic_id: topicId, ...userProg[topicId] })
            }
        })
        navigate('/quiz', {state:{chapter:1, type: 'topicQuiz', topics:chapter_topics}})
        console.log(chapter_topics)
    }
    }


    const LeftButton = () => {
        if (currentUser){
            if(currentUserChapters[chapterId].video_completed==false){
                return<>
                          <div className='button w-11/12 sm:w-auto sm:h-12' onClick={handleSignUp}>
                                Mark Video As Watched
                            </div>
                </>
            } else {
                return<>
                            <div className='button w-11/12 sm:w-auto sm:h-12' onClick={handleSignUp}>
                                Mark Video as Unwatched
                            </div>
                </>
            }
        } else {
            return <>
                <div className='button w-11/12 sm:w-auto sm:h-12' onClick={handleSignUp}>
                    Sign Up To Track Progress & More!
                </div>
            </>              
            
        }
    }

    let chaptersObj = []

    chaptersObj = Object.keys(chapters).map((key)=>({
        id: key,
        ...chapters[key]
    }))

    const chapterVid = (videoId) => {
        const chapter = chaptersObj.find(chapter=>chapter.video_url === videoId)
        return chapter? chapter.name : ""
    }

    const shortenedVideoName = (video) =>{
        return video.split(" ").slice(1).join(" ")
    }
        const handleSignUp = () => {
            if(!currentUser){
                dispatch(openSignupModal())
            } else if (currentUserChapters[chapterId].video_completed == false){
                dispatch(updateVideoProgress(chapterId, 'watched'))
            } else {
                dispatch(updateVideoProgress(chapterId, 'unwatched'))
            }
        }

    const rightButton = () => {
        if(!currentUser){
            return(
                <>
                    Take a Free Quiz on {shortenedVideoName(chapterVid(videoId))}   
                </>
            )
        } else {
            if (currentUserChapters[chapterId].quiz_grade == null) {
                return(
                    <>
                        Take the Chapter Quiz for: &nbsp; <span className='text-[#0088A8]'>{shortenedVideoName(chapterVid(videoId))}   </span>
                    </>
                )
            } else if (currentUserChapters[chapterId].quiz_grade <= 50)
            {
            return(
                    <>
                        Retake the Chapter Quiz for: &nbsp; <span className='text-[#0088A8]'>{shortenedVideoName(chapterVid(videoId))}   </span>
                    </>
                )
            }else {
                return(
                    <>
                        Get some more practice on: &nbsp;<span className='text-[#0088A8]'>{shortenedVideoName(chapterVid(videoId))} </span>
                   </>)
            }
        }
    }
   return <>
         <div className='flex flex-col items-center justify-center sm:mt-10 mt-6 '>
                        <div className='sm:text-2xl text-center text-lg mb-4 relative'>
                            {videoId ? <>
                            {currentUser && currentUserChapters[chapterId].video_completed && 
                            <img src='/alreadyWatched.png' className='sm:h-full h-2/3 sm:-top-[15px] sm:-left-[44px]   absolute  -rotate-12'/>
                            }
                            <div>Video for {chapter.name}</div></>: ''}
                        </div>
                        <div>
                            {/* {currentUser && watchedStatus(chapterId) && <>Watched!</>} */}

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
                            
                            {LeftButton()}
                            {/* <div className='button w-11/12 sm:w-auto sm:h-12' onClick={handleSignUp}>
                                {currentUser ? 'Mark Video As Watched' : 'Sign Up to Access Quizzes & More!'}
                            </div> */}
                            <div className='mx-12 py-2 sm:py-0 text-2xl'></div>
                            <div className='button w-11/12 sm:w-auto sm:h-12' onClick={handleGoToQuiz}>
                                {rightButton()}
                                
                            </div>
                        </div>
                            {/* <div className='my-8 border py-4 px-2 bg-slate-400 border-black rounded-xl hover:bg-slate-600 hover:cursor-pointer' onClick={()=>videoGo(videoId, 'short')}>
                                Feeling Lazy?  Watch the (SUPER) short version.
                            </div> */}
                        {/* </div> */}
                        
                        </>
                        )}
                    </div>
    </>
}