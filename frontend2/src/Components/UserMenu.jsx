import { FaUserCircle } from "react-icons/fa";
import { useSelector } from "react-redux";
import LogoutButton from "./LogoutComponent";



export const UserMenu = () => {
    const username = useSelector((state) => state.user.username)
    return(
            <div className='relative inline-block group'>
                <div className='flex flex-col items-center mr-10 mt-2 hover:cursor-pointer text-slate-600 '>
                    <FaUserCircle className='text-3xl '/>
                    <div>Menu</div>
                </div>
                <div className=
                    'h-36 w-52 shadow-lg  
                    border-slate-900 border 
                    border-solid bg-white 
                    rounded-lg text-right px-6 pt-2 absolute -ml-32 flex flex-col hidden group-hover:block'>
                    <div>{username}</div>
                    <div className="hover:bg-slate-400 hover:bg-slate-400 w-52 -ml-6 px-6">Jump to next thing</div>
                    <LogoutButton/>
                </div>
                
            

            </div>
        )


}