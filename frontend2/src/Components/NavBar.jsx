import { useSelector, useDispatch } from "react-redux"
import LoginComponent from "./LoginComponent"
import SignupComponent from "./SignupComponent"
import LogoutButton from "./LogoutComponent"
import { openLoginModal, openSignupModal } from "../Slices/modalSlice"



export const NavBar = () => {
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
            <LogoutButton/>
        </div>
    ) : (
        <div className="flex w-32 justify-around mr-10">
            <p className="hover:cursor-pointer" onClick = {handleSignup}>Sign Up</p>
            <p className="hover:cursor-pointer" onClick = {handleLogin} >Log In</p>
        </div>
    )
    return(
        <>
        
            <nav className=
                "w-full 
                h-24 
                z-0
                
                items-center 
                flex justify-between
                sticky
                top-0">
                <img src="/Logo.svg" alt="EVTDS Logo" className="h-3/4 ml-2.5"/>
                <div>
                    {sessionLinks}
                </div>
            </nav>
            {loginFormOpen && (<LoginComponent className="z-10" />)}   
            {signupFormOpen && (<SignupComponent className="z-10" />)}     
        </>
    )
}