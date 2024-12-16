import { useSelector, useDispatch } from "react-redux"
import LoginComponent from "./LoginComponent"
import SignupComponent from "./SignupComponent"
import LogoutButton from "./LogoutComponent"
import { openLoginModal, openSignupModal } from "../Slices/modalSlice"
import { UserMenu } from "./UserMenu"
import { useNavigate } from "react-router-dom"
import { getAllChapters } from "../Slices/chaptersActions"



export const NavBar = () => {
    const navigate = useNavigate()
    let loginFormOpen = useSelector(state=>(state.modal.isLoginOpen))
    let signupFormOpen = useSelector(state=>(state.modal.isSignupOpen))
    const currentUser = useSelector(state=>(state.user.username))
    const dispatch = useDispatch()
   
    const handleLogin = ()=>{
        dispatch(openLoginModal())
    }

    const handleSignup = () => {
        dispatch(openSignupModal())
    }

    const sessionLinks = currentUser ? (
        <div className="mr-8">
            <UserMenu/>
            {/* <LogoutButton/> */}
        </div>
    ) : (
        <div className="flex w-32 justify-between mr-10 text-xs md:text-sm">
            <p className="hover:cursor-pointer" onClick = {handleSignup}>Sign Up</p>
            <p className="hover:cursor-pointer" onClick = {handleLogin} >Log In</p>
        </div>
    )

    const goToVideos = () => {
        navigate('/videoindex')
    }
    return(
        <>
        
            <nav className=
                "w-full  
                z-10
                bg-lime-500
                items-center 
                flex justify-between
                sticky
                top-0">
                <span className='flex w-11/12 items-center'>
                    <img src="/Logo.svg" onClick = {()=>navigate('/')}alt="EVTDS Logo" className="w-1/12  my-2 sm:ml-14 ml-4 lg:ml-16 min-w-20 hover:cursor-pointer"/>
                    <span className='ml-2 md:text-2xl text-lg font-bold text-slate-600'>BETA</span>
                </span>
                <div className='flex items-center justify-between'>
                    {!currentUser &&
                        <button className="mr-4 text-xs md:text-sm" onClick={goToVideos}>Jump To Videos</button>
                    }
                    {sessionLinks}
                </div>
            </nav>
            {loginFormOpen && (<LoginComponent className="z-10" />)}   
            {signupFormOpen && (<SignupComponent className="z-10" />)}     
        </>
    )
}