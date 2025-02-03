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

    const videoWatched = currentChapterId && userChapters?.[currentChapterId]?.video_completed ? true : false;
    const navigate = useNavigate()
    const dispatch = useDispatch()
    
    const thing = videoWatched ? "Take chapter quiz" : "go to next video"


    const nextThing = () => {
        if(currentChapterId){
            videoWatched 
            ? navigate('/Quiz', {state: {chapter: currentChapterId, type: 'chapterQuiz', topics: []}}) 
            : navigate(`/video/${currentChapterId}`)
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
                <div className='flex flex-col items-center mr-6 mt-2 hover:cursor-pointer text-slate-600 text-white'>
                    <FaUserCircle className='text-3xl '/>
                    <div>Menu</div>
                </div>
                <div className=
                    'h-auto w-48 shadow-lg  
                    border-slate-900 border 
                    border-solid bg-white 
                    rounded-lg px-6 pt-2 absolute -ml-32 flex flex-col hidden group-hover:block'>
                    <div className = 'font-bold text-lg'>{capitalized}</div>
                    <div className='text-left'>User Account</div>
                    <hr className='border-gray-400 w-full mb-2'></hr>
                    <div className='text-right'>
                        <div className="hover:bg-[#0088a8] hover:text-white hover:cursor-pointer w-48 -ml-6 px-4" onClick = {nextThing}>{thing}</div>
                        <div className="hover:bg-[#0088a8] hover:text-white  hover:cursor-pointer w-48 -ml-6 px-4" onClick = {() => {navigate('/quizgenerator')}}>Create review quiz</div>
                        <div className="hover:bg-[#0088a8] hover:text-white  hover:cursor-pointer w-48 -ml-6 px-4" onClick = {goAllVids}>Go to all Videos</div>
                        <div className="hover:bg-[#0088a8] hover:text-white  hover:cursor-pointer w-48 -ml-6 px-4" onClick = {goHome}>User dashboard</div>
                        <div className="hover:bg-[#0088a8] hover:text-white  hover:cursor-pointer w-48 -ml-6 px-4 my-4">
                            <LogoutButton/>
                        </div>
                    </div>
                </div>
                
            

            </div>
        )


}