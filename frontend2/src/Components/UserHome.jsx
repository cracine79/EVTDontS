import { useSelector } from "react-redux"
import { Progress } from "./Progress"
import { useNavigate, useLocation } from "react-router-dom"
import { csrfFetch } from "../csrf"
import { useDispatch } from "react-redux"
import { updateUserChapters } from "../Slices/userChaptersSlice"
import { Tutorial } from "./Tutorial"
import { useEffect } from "react"

export const UserHome = () => {
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const location = useLocation()
    const userName = useSelector((state)=>state.user.username)
    const currentChapterId = useSelector((state)=>state.user.currentChapter)
    const currentBookChapter = useSelector((state)=>state.chapters[currentChapterId])
    const currentUserChapter = useSelector((state)=>state.userChapters[currentChapterId])
    const showModal = location.state?.showModal
    console.log('showModal:' , showModal)
    const messages = [
        "Glad to see you're back.  We were starting to think you'd mastered economics overnight",
        "Already back for more?  Guess Netflix isn't cutting it today.",
        "Here again?, we knew you couldn't resist the allure of more charts and graphs",
        "We're starting to think you actually enjoy this sh... this stuff.",
        "Back for more?  We promise not to make this TOO interesting.",
        "We've got to stop meeting like this!",
        "We've never felt so loved before.  Except the time our Mom subscribed to our Youtube channel",
        "You like us!  You really like us!"
    ]


    useEffect(() => {
        window.scrollTo(0, 0);  // Scroll to top when the component mounts
      }, []);

    const workingOn = () =>{
        if(currentBookChapter){
            return (
                <>
                    <div className="text-xl">You are currently working on:</div>
                    <div className="text-xl"> Chapter {currentBookChapter.name.slice(0,3)}: {currentBookChapter.name.slice(3)}</div>
                </>
            )
        } else{
            return (
              <>Get Started</>  
            )
        }
    }
    const genMessage = () =>{
        const number = Math.floor(Math.random()*6)
        return (
        <>
            {messages[number]}
        </>)
    }

    const handleClick = () => {
        if(currentUserChapter){
            if(!currentUserChapter.video_completed){
                navigate(`/video/${currentChapterId}`)
            } else {
                navigate('/Quiz', {state: {chapter: currentChapterId, type: 'chapterQuiz', topics: []}})
            }
        }
    }



    const UpNext = () => {
        if(!currentUserChapter){
            return(
                <>Get Started</>
            )
        }else if(!currentUserChapter.video_completed){
            return(
                <div onClick={handleClick}><p > Watch the next video </p></div>
            )
        } else {
            return(
                <div onClick={handleClick}><p > Go To Chapter Quiz </p></div>
            )
        }
    }

    const startChapterProgress = async(chapterId) => {
        try{
            const response = await csrfFetch('/api/progress/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                  },
                body: JSON.stringify({ chapter_id: chapterId }),
            });
    
        const data = await response.json()
        
        dispatch(updateUserChapters(data))
    
        } catch (error) {
            console.error('Error finding', error)
        }
    }

    
    return(
        <>  
            <Tutorial showModal = {showModal} />
            <div className=
                {`flex 
                items-center 
                w-screen 
                bg-slate-50 
                flex-col
                min-h-screen`}>
                <div className='h-100 flex flex-row mt-26 w-3/4'>
                    <div className=
                        {`mt-36 
                        min-w-96
                        w-3/5 
                        h-auto
                        bg-white 
                        rounded-3xl 
                        shadow-2xl 
                        flex 
                        flex-row 
                        items-center
                        justify-center`}>
                    {userName ? (
                                <div className='flex flex-col items-center justify-center'>
                                    <div className='ml-10 text-5xl '>
                                        Welcome Back {userName[0].toUpperCase() + userName.slice(1)}.
                                    </div>
                                    <div className='text-xl w-4/5 text-center mt-6'>
                                        {genMessage()}
                                    </div>
                                </div>
                    
                        ) : (
                            <p className='ml-10 text-5xl'>
                            </p>
                        )}
                    </div>
                    <div className="w-1/3 min-w-80 bg-white 100 h-100 mt-36 ml-12 rounded-3xl shadow-2xl flex flex-col items-center">
                            <p className="mt-8 text-3xl underline">Progress</p>
                            <div className = "mt-2 ml-4 mr-2">
                                {workingOn()}
                            </div>
                            <div className=
                                {`mt-10 
                                border-black 
                                h-1/5 
                                w-1/2 
                                border-2 
                                flex 
                                justify-center 
                                items-center
                                rounded-lg
                                bg-slate-300
                                hover:bg-slate-500
                                font-medium
                                hover:cursor-pointer
                                mb-6`}>
                                <div onClick={handleClick}><UpNext /></div>
                            </div>
                        </div>

                </div>
        
                    <div className='flex flex-row items-center justify-center w-full mt-20 mb-20'>
                        <Progress />
                    </div>

                    <div className = 'w-full'>
                        <div className=
                        {`
                        ml-20
                        w-1/3
                        h-auto
                        text-center
                        p-4
                        rounded-3xl 
                        shadow-2xl 
                        flex 
                        flex-col 
                        items-center
                        justify-center`}>
                            <div className='text-2xl mt-3'>Update Your Study Plan</div>
                            <p className='my-4'>Not everyone gets it right on the first try - you should see Mr. Racine's last haircut!</p>
                            <p>Adjust the units/chapters you want to study here and get back on track like the deicsion making pro we all know you are</p>
                            <button  className={`
                                mt-4
                                border-black 
                                h-1/5 
                                w-1/2 
                                border-2 
                                flex 
                                justify-center 
                                items-center
                                rounded-lg
                                bg-slate-300
                                hover:bg-slate-500
                                font-medium
                                hover:cursor-pointer
                                mb-6`}
                                onClick = {()=>navigate('/updateunits')}
                                >Fix Life Choices</button>
                        </div>
                    </div>
            
            </div>
        </>
    )
}