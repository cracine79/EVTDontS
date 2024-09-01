import { useSelector } from "react-redux"
import { Progress } from "./Progress"
import { useNavigate } from "react-router-dom"
import { Video } from "./Video"

export const UserHome = () => {
    const navigate = useNavigate()
    const userName = useSelector((state)=>state.user.username)
    const messages = [
        "Glad to see you're back.  We were starting to think you'd mastered economics overnight",
        "Already back for more?  Guess Netflix isn't cutting it today",
        "Here again?, we knew you couldn't resist the allure of more charts and graphs",
        "We're starting to think you actually enjoy this stuff.",
        "Back for more?  We promise not to make this TOO interesting.",
        "We've got to stop meeting like this!",
        "We've never felt so loved before.  Except the time our Mom subscribed to our Youtube channel"
    ]

    const genMessage = () =>{
        const number = Math.floor(Math.random()*6)
        return (
        <>
            {messages[number]}
        </>)
    }

    const handleClick = () => {
        navigate('/Video')
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
                            <p className='ml-10 text-5xl'>
                                Welcome Back {userName[0].toUpperCase() + userName.slice(1)}.
                            </p>
                            <p className='text-xl w-4/5 text-center mt-6'>
                                {genMessage()}
                            </p>
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
                        <p className='mt-10' onClick={handleClick}>Take me to the next video</p>
                    </div>
                </div>
            </div>
        </div>
    )
}