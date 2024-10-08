import { FaUserCircle } from "react-icons/fa";
import { useSelector, useDispatch } from "react-redux";
import LogoutButton from "./LogoutComponent";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { clearQuestions } from "../Slices/questionsSlice"
import { clearUserResults } from "../Slices/resultsSlice"

export const UserMenu = () => {
    const username = useSelector((state) => state.user.username)
    const capitalized = username[0].toUpperCase()+username.slice(1)
    const currentChapterId = useSelector((state) => state.user.currentChapter)
    const videoWatched = useSelector((state)=>state.chapters[currentChapterId].video_completed)
    const navigate = useNavigate()
    const dispatch = useDispatch()
    
    const thing = videoWatched ? "chapter quiz" : "next video"
    console.log(videoWatched)

    const nextThing = () => {videoWatched ? 
        navigate('/Quiz', {state: {chapter: currentChapterId, type: 'chapterQuiz', topics: []}}) :
        navigate('/Video', {state: {chapter: currentChapterId}})
    }

    const goHome = () => {
        dispatch(clearQuestions)
        dispatch(clearUserResults)
        navigate('/userhome')
    }

    return(
            <div className='relative inline-block group'>
                <div className='flex flex-col items-center mr-6 mt-2 hover:cursor-pointer text-slate-600 '>
                    <FaUserCircle className='text-3xl '/>
                    <div>Menu</div>
                </div>
                <div className=
                    'h-auto w-54 shadow-lg  
                    border-slate-900 border 
                    border-solid bg-white 
                    rounded-lg px-6 pt-2 absolute -ml-32 flex flex-col hidden group-hover:block'>
                    <div className = 'font-bold text-lg'>{capitalized}</div>
                    <hr className='border-gray-400 w-full my-2'></hr>
                    <div className='text-right'>
                        <div className="hover:bg-green-400 hover:cursor-pointer w-48 -ml-6 px-4" onClick = {nextThing}>Go to {thing}</div>
                        <div className="hover:bg-green-400  hover:cursor-pointer w-48 -ml-6 px-4">Create review quiz</div>
                        <div className="hover:bg-green-400  hover:cursor-pointer w-48 -ml-6 px-4" onClick = {goHome}>User dashboard</div>
                        <div className="hover:bg-green-400  hover:cursor-pointer w-48 -ml-6 px-4 my-4">
                            <LogoutButton/>
                        </div>
                    </div>
                </div>
                
            

            </div>
        )


}