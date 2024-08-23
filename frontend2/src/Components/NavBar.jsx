import { useSelector } from "react-redux"



export const NavBar = () => {
    const currentUser = useSelector(state=>(state.user.username))
    console.log(currentUser)
    const handleLogin = () =>{

    }

    const sessionLinks = currentUser ? (
        <>Signed In Already</>
    ) : (
        <>
            <p>Sign Up</p>
            <p onClick = {handleLogin} >Log In Here</p>
        </>
    )
    return(
        <>
        
            <nav className="w-full h-24 bg-lime-500 items-center flex">
                
                <img src="/Logo.svg" alt="EVTDS Logo" className="h-3/4 ml-2.5"/>
                {sessionLinks}
            </nav>
        </>
    )
}