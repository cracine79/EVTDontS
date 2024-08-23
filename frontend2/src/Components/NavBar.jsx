import { useSelector } from "react-redux"



export const NavBar = () => {
    const currentUser = useSelector(state=>(state.user.username))
    console.log(currentUser)

    const sessionLinks = currentUser ? (
        <>Signed In Already</>
    ) : (
        <>
            <p>Sign Up</p>
            <p>Log In</p>
        </>
    )
    return(
        <>
        
            <nav className="w-full h-24 bg-lime-500 items-center flex">
                
                <img src="/Logo.svg" alt="Logo" className="h-3/4 ml-2.5"/>
                {sessionLinks}
            </nav>
        </>
    )
}