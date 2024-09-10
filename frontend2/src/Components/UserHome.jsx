import { useSelector } from "react-redux"
import { Progress } from "./Progress"
import { useNavigate } from "react-router-dom"
import { csrfFetch } from "../csrf"
import { useDispatch } from "react-redux"
import { updateUserChapters } from "../Slices/chaptersSlice"

export const UserHome = () => {
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const userName = useSelector((state)=>state.user.username)
    const userId = useSelector((state)=>state.user.id)
    const messages = [
        "Glad to see you're back.  We were starting to think you'd mastered economics overnight",
        "Already back for more?  Guess Netflix isn't cutting it today",
        "Here again?, we knew you couldn't resist the allure of more charts and graphs",
        "We're starting to think you actually enjoy this stuff.",
        "Back for more?  We promise not to make this TOO interesting.",
        "We've got to stop meeting like this!",
        "We've never felt so loved before.  Except the time our Mom subscribed to our Youtube channel",
        "You like us!  You really like us!"
    ]

    const currentChapterId = useSelector((state)=>state.user.currentChapter)
    const currentChapter = useSelector((state)=>state.chapters[currentChapterId])
    const workingOn = () =>{
        if(currentChapter){
            return (
                <div>You are currently working on: {currentChapter.name}</div>
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
        if(!currentChapter.video_completed){
            if(!("video_completed" in currentChapter)){
                (startChapterProgress(currentChapterId, userId))
            }
            navigate('/Video')
        } else {
            navigate('/Quiz', {state: {chapter: currentChapterId}})
        }
    }



    const upNext = () => {
        if(currentChapter==null){
            return(
                <>Get Started</>
            )
        }else if(!currentChapter.video_completed){
            return(
                <div onClick={handleClick}><p > The next video </p></div>
            )
        } else {
            return(
                <div onClick={handleClick}><p > Review Quiz </p></div>
            )
        }
    }

    const startChapterProgress = async(chapterId, userId) => {
        try{
            const response = await csrfFetch('/api/progress/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                  },
                body: JSON.stringify({ chapter_id: chapterId, user_id: userId }),
            });
    
        const data = await response.json()
        
        dispatch(updateUserChapters(data))
    
        } catch (error) {
            console.error('Error finding', error)
        }
    }

    
    return(
        <div className=
            'flex 
            items-center 
            w-screen 
            mt 
            bg-slate-50 
            h-screen
            flex-col'>
            <div className=
                'mt-36 
                w-3/4 
                h-1/4 
                bg-white 
                rounded-3xl 
                shadow-2xl 
                flex 
                flex-row 
                items-center
                justify-center'>
               {userName ? (
                        <div className='flex flex-col ml-10 items-center justify-center'>
                            <div className='ml-10 text-5xl'>
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
            <div className='flex flex-com justify-center w-screen'>
                <div className='flex flex-row items-center justify-center w-11/12'>
                    <Progress />
                    <div className="w-1/6 bg-white 100 h-3/5 mt-20 ml-12 rounded-3xl shadow-2xl">
                        {workingOn()}
                        <p>Up Next</p>
                        <div className='mt-10' onClick={handleClick}>{upNext()}</div>
                    </div>
                </div>
            </div>
        </div>
    )
}