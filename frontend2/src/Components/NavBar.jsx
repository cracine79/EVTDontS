import { useSelector } from "react-redux"
import { useState } from "react"
import LoginComponent from "./LoginComponent"
import LogoutButton from "./LogoutComponent"



export const NavBar = () => {
    const [loginFormOpen, setLoginFormOpen] = useState(false)
    const currentUser = useSelector(state=>(state.user.username))
    console.log(currentUser)
    const handleLogin = () =>{
        setLoginFormOpen(true)
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
            {loginFormOpen && (<LoginComponent />)}
            
            
        </>
    )
}