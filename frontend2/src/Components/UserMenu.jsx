import { FaUserCircle } from "react-icons/fa";
import { useSelector, useDispatch } from "react-redux";
import LogoutButton from "./LogoutComponent";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { clearQuestions } from "../Slices/questionsSlice"
import { clearUserResults } from "../Slices/resultsSlice"
import { getAllChapters } from "../Slices/chaptersActions";

export const UserMenu = () => {
    const username = useSelector((state) => state.user.username)
    const capitalized = username ? username[0].toUpperCase() + username.slice(1) : "";
    const currentChapterId = useSelector((state) => state.user.currentChapter)
    const bookChapters = useSelector((state) => state.chapters); 
    const userChapters = useSelector((state) => state.userChapters)
    console.log("CCID", currentChapterId)
    const videoWatched = currentChapterId && userChapters?.[currentChapterId]?.video_completed ? true : false;
    const navigate = useNavigate()
    const dispatch = useDispatch()
    
    const thing = videoWatched ? "chapter quiz" : "next video"


    const nextThing = () => {
        return (<>Thing</>)
        if(currentChapterId){
            videoWatched 
            ? navigate('/Quiz', {state: {chapter: currentChapterId, type: 'chapterQuiz', topics: []}}) 
            : navigate('/Video', {state: {chapter: currentChapterId}})
        }
    }

    const goHome = () => {
        dispatch(clearQuestions())
        dispatch(clearUserResults())
        navigate('/userhome')
    }

    const goAllVids = () => {
        dispatch(getAllChapters())
        navigate('/videoindex')

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
                        <div className="hover:bg-green-400  hover:cursor-pointer w-48 -ml-6 px-4" onClick = {goAllVids}>Go to all Videos</div>
                        <div className="hover:bg-green-400  hover:cursor-pointer w-48 -ml-6 px-4" onClick = {goHome}>User dashboard</div>
                        <div className="hover:bg-green-400  hover:cursor-pointer w-48 -ml-6 px-4 my-4">
                            <LogoutButton/>
                        </div>
                    </div>
                </div>
                
            

            </div>
        )


}