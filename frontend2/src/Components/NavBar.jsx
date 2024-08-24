import { useSelector, useDispatch } from "react-redux"
import LoginComponent from "./LoginComponent"
import LogoutButton from "./LogoutComponent"
import { openLoginModal } from "../Slices/modalSlice"



export const NavBar = () => {
    let loginFormOpen = useSelector(state=>(state.modal.isLoginOpen))
    const currentUser = useSelector(state=>(state.user.username))
    const dispatch = useDispatch()
   
    const handleLogin = ()=>{
    dispatch(openLoginModal())
    }

    const sessionLinks = currentUser ? (
            <LogoutButton />
    ) : (
        <div className="flex w-32 justify-around mr-10">
            <p className="hover:cursor-pointer">Sign Up</p>
            <p className="hover:cursor-pointer" onClick = {handleLogin} >Log In</p>
        </div>
    )
    return(
        <>
        
            <nav className=
                "w-full 
                h-24 
                z-0
                bg-lime-500 
                items-center 
                flex justify-between">
                <img src="/Logo.svg" alt="EVTDS Logo" className="h-3/4 ml-2.5"/>
                <div>
                    {sessionLinks}
                </div>
            </nav>
            {loginFormOpen && (<LoginComponent className="z-10" />)}     
        </>
    )
}